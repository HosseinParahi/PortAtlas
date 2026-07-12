"""Bounded TOML loader and platform-path adapter."""

from __future__ import annotations

import tomllib
from collections.abc import Mapping
from pathlib import Path

from platformdirs import user_cache_path, user_config_path, user_data_path

from portatlas.config.schema import AppPaths, AppSettings, DatabaseSettings, ServerSettings

_MAX_CONFIG_BYTES = 256 * 1024
_TOP_LEVEL_KEYS = frozenset({"schema_version", "server", "database"})
_SERVER_KEYS = frozenset({"host", "port", "trusted_origins"})
_DATABASE_KEYS = frozenset({"profile", "url", "busy_timeout_ms"})
_SECRET_KEY_PARTS = (
    "authorization",
    "bearer",
    "cookie",
    "credential",
    "password",
    "private_key",
    "secret",
    "token",
)


def default_paths() -> AppPaths:
    """Resolve per-user paths lazily at the platform adapter boundary."""

    return AppPaths(
        config_dir=user_config_path("PortAtlas", ensure_exists=False),
        data_dir=user_data_path("PortAtlas", ensure_exists=False),
        cache_dir=user_cache_path("PortAtlas", ensure_exists=False),
    )


def _require_mapping(value: object, section: str) -> Mapping[str, object]:
    if not isinstance(value, dict) or not all(isinstance(key, str) for key in value):
        raise ValueError(f"Configuration section {section} must be a table.")
    return value


def _validate_keys(values: Mapping[str, object], allowed: frozenset[str], section: str) -> None:
    unknown = set(values) - allowed
    secret_fields = {
        key for key in values if any(part in key.lower() for part in _SECRET_KEY_PARTS)
    }
    if unknown or secret_fields:
        raise ValueError(f"Configuration section {section} contains unsupported fields.")


def _string_value(values: Mapping[str, object], key: str, default: str) -> str:
    value = values.get(key, default)
    if not isinstance(value, str):
        raise TypeError(f"Configuration field {key} must be text.")
    return value


def _integer_value(values: Mapping[str, object], key: str, default: int) -> int:
    value = values.get(key, default)
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"Configuration field {key} must be an integer.")
    return value


def load_settings(
    path: Path,
    *,
    paths: AppPaths | None = None,
) -> AppSettings:
    """Load only the reviewed foundation schema; unknown fields fail closed."""

    if path.is_symlink():
        raise ValueError("Configuration file may not be a symbolic link.")
    raw = path.read_bytes()
    if len(raw) > _MAX_CONFIG_BYTES:
        raise ValueError("Configuration file exceeds its byte budget.")
    try:
        document = tomllib.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, tomllib.TOMLDecodeError) as error:
        raise ValueError("Configuration file is not valid UTF-8 TOML.") from error
    _validate_keys(document, _TOP_LEVEL_KEYS, "root")
    if "schema_version" not in document:
        raise ValueError("Configuration schema_version is required.")
    schema_version = document["schema_version"]
    if isinstance(schema_version, bool) or not isinstance(schema_version, int):
        raise TypeError("Configuration schema_version must be an integer.")
    if schema_version != 1:
        raise ValueError("Configuration schema_version is not supported.")

    server_values = _require_mapping(document.get("server", {}), "server")
    _validate_keys(server_values, _SERVER_KEYS, "server")
    trusted_origins = server_values.get("trusted_origins", ())
    if not isinstance(trusted_origins, list | tuple) or not all(
        isinstance(origin, str) for origin in trusted_origins
    ):
        raise ValueError("server.trusted_origins must be an array of origins.")
    server = ServerSettings(
        host=_string_value(server_values, "host", "127.0.0.1"),
        port=_integer_value(server_values, "port", 4765),
        trusted_origins=tuple(trusted_origins),
    )

    database_values = _require_mapping(document.get("database", {}), "database")
    _validate_keys(database_values, _DATABASE_KEYS, "database")
    active_paths = paths or default_paths()
    if database_values:
        database = DatabaseSettings(
            profile=_string_value(database_values, "profile", "sqlite"),
            url=_string_value(
                database_values,
                "url",
                f"sqlite+pysqlite:///{active_paths.data_dir / 'portatlas.sqlite3'}",
            ),
            busy_timeout_ms=_integer_value(database_values, "busy_timeout_ms", 5_000),
        )
    else:
        database = DatabaseSettings.sqlite(active_paths.data_dir / "portatlas.sqlite3")
    return AppSettings(
        paths=active_paths,
        schema_version=schema_version,
        server=server,
        database=database,
    )
