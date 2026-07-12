"""Strict configuration values with no telemetry or raw-secret fields."""

from __future__ import annotations

import ipaddress
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import urlsplit

_MAX_PORT = 65_535
_MIN_BUSY_TIMEOUT_MS = 100
_MAX_BUSY_TIMEOUT_MS = 60_000


@dataclass(frozen=True, slots=True)
class AppPaths:
    config_dir: Path
    data_dir: Path
    cache_dir: Path

    def __post_init__(self) -> None:
        for name in ("config_dir", "data_dir", "cache_dir"):
            path = getattr(self, name)
            if not isinstance(path, Path) or not path.is_absolute():
                raise ValueError(f"{name} must be an absolute local path.")


@dataclass(frozen=True, slots=True)
class ServerSettings:
    host: str = "127.0.0.1"
    port: int = 4765
    trusted_origins: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        try:
            address = ipaddress.ip_address(self.host)
        except ValueError as error:
            raise ValueError("Server host must be a loopback IP address.") from error
        if not address.is_loopback:
            raise ValueError("Server host must remain loopback-only.")
        if isinstance(self.port, bool) or not isinstance(self.port, int):
            raise TypeError("Server port must be an integer.")
        if not 1 <= self.port <= _MAX_PORT:
            raise ValueError("Server port must be between 1 and 65535.")
        for origin in self.trusted_origins:
            parsed = urlsplit(origin)
            if parsed.scheme not in {"http", "https"} or parsed.hostname is None:
                raise ValueError("Trusted origins must be absolute HTTP origins.")
            if (
                parsed.username is not None
                or parsed.password is not None
                or parsed.query
                or parsed.fragment
            ):
                raise ValueError("Trusted origins cannot contain credentials, query, or fragment.")
            try:
                _origin_port = parsed.port
            except ValueError as error:
                raise ValueError("Trusted origins must use a valid TCP port.") from error
            try:
                origin_address = ipaddress.ip_address(parsed.hostname)
            except ValueError as error:
                raise ValueError(
                    "Trusted origins must resolve to literal loopback hosts."
                ) from error
            if not origin_address.is_loopback or parsed.path not in ("", "/"):
                raise ValueError("Trusted origins must be loopback origins without paths.")


@dataclass(frozen=True, slots=True)
class DatabaseSettings:
    profile: str
    url: str
    busy_timeout_ms: int = 5_000

    def __post_init__(self) -> None:
        if self.profile not in {"sqlite", "postgresql"}:
            raise ValueError("Database profile must be sqlite or postgresql.")
        expected_prefix = (
            "sqlite+pysqlite:///" if self.profile == "sqlite" else "postgresql+psycopg://"
        )
        if not self.url.startswith(expected_prefix):
            raise ValueError("Database URL does not match its explicit profile.")
        parsed = urlsplit(self.url)
        if parsed.username is not None or parsed.password is not None:
            raise ValueError("Raw database credentials are not configuration values.")
        if self.profile == "sqlite":
            path_text = self.url.removeprefix("sqlite+pysqlite://")
            if path_text != "/:memory:" and not path_text.startswith("/"):
                raise ValueError("SQLite databases must use an absolute local path.")
        if not _MIN_BUSY_TIMEOUT_MS <= self.busy_timeout_ms <= _MAX_BUSY_TIMEOUT_MS:
            raise ValueError("Database busy timeout is outside the bounded range.")

    @classmethod
    def sqlite(cls, path: Path, *, busy_timeout_ms: int = 5_000) -> DatabaseSettings:
        if not path.is_absolute():
            raise ValueError("SQLite path must be absolute.")
        return cls(
            profile="sqlite",
            url=f"sqlite+pysqlite:///{path}",
            busy_timeout_ms=busy_timeout_ms,
        )


@dataclass(frozen=True, slots=True)
class AppSettings:
    paths: AppPaths
    schema_version: int = 1
    server: ServerSettings = field(default_factory=ServerSettings)
    database: DatabaseSettings | None = None

    def __post_init__(self) -> None:
        if isinstance(self.schema_version, bool) or not isinstance(self.schema_version, int):
            raise TypeError("Configuration schema version must be an integer.")
        if self.schema_version != 1:
            raise ValueError("Configuration schema version is not supported.")
        if self.database is None:
            object.__setattr__(
                self,
                "database",
                DatabaseSettings.sqlite(self.paths.data_dir / "portatlas.sqlite3"),
            )
