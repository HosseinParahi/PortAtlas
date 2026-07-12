"""UT-CFG-001: local-only configuration foundation tests."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from portatlas.config.loader import default_paths, load_settings
from portatlas.config.schema import AppPaths, AppSettings, DatabaseSettings, ServerSettings


class ConfigurationTests(unittest.TestCase):
    def test_defaults_are_loopback_sqlite_and_have_no_telemetry_capability(self) -> None:
        test_root = Path.cwd() / ".foundation-test-state"
        paths = AppPaths(
            config_dir=test_root / "config",
            data_dir=test_root / "data",
            cache_dir=test_root / "cache",
        )
        settings = AppSettings(paths=paths)

        self.assertEqual(settings.schema_version, 1)
        self.assertEqual(settings.server.host, "127.0.0.1")
        self.assertTrue(settings.database.url.startswith("sqlite+pysqlite:///"))
        self.assertFalse(hasattr(settings, "telemetry"))

    def test_non_loopback_bind_fails_closed(self) -> None:
        for host in ("0.0.0.0", "::", "192.168.1.5", "example.com"):  # noqa: S104
            with self.subTest(host=host), self.assertRaises(ValueError):
                ServerSettings(host=host)

    def test_configuration_rejects_unknown_and_secret_fields(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "config.toml"
            path.write_text("telemetry = true\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                load_settings(path)

            path.write_text('[server]\napi_token = "canary"\n', encoding="utf-8")
            with self.assertRaises(ValueError):
                load_settings(path)

    def test_postgresql_is_optional_but_validated_as_an_explicit_profile(self) -> None:
        sqlite = DatabaseSettings.sqlite(Path.cwd() / ".foundation-test.sqlite3")
        postgres = DatabaseSettings(
            profile="postgresql",
            url="postgresql+psycopg://localhost/portatlas",
        )

        self.assertEqual(sqlite.profile, "sqlite")
        self.assertEqual(postgres.profile, "postgresql")
        with self.assertRaises(ValueError):
            DatabaseSettings(profile="sqlite", url="postgresql://localhost/wrong")

    def test_valid_file_applies_explicit_bounded_values(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            paths = AppPaths(
                config_dir=root / "config",
                data_dir=root / "data",
                cache_dir=root / "cache",
            )
            path = root / "config.toml"
            path.write_text(
                """
schema_version = 1

[server]
host = "::1"
port = 4876
trusted_origins = ["http://127.0.0.1:4876", "https://[::1]:4876"]

[database]
profile = "sqlite"
busy_timeout_ms = 1200
""".strip(),
                encoding="utf-8",
            )

            settings = load_settings(path, paths=paths)

        self.assertEqual(settings.server.host, "::1")
        self.assertEqual(settings.server.port, 4876)
        self.assertEqual(settings.database.busy_timeout_ms, 1200)
        self.assertTrue(settings.database.url.endswith("/data/portatlas.sqlite3"))

    def test_loader_rejects_unsafe_file_and_value_shapes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "config.toml"
            cases = (
                (b"", ValueError),
                (b"schema_version = 2\n", ValueError),
                (b'schema_version = "1"\n', TypeError),
                (b"schema_version = 1\nserver = []\n", ValueError),
                (b"schema_version = 1\n[server]\nport = true\n", TypeError),
                (
                    b'schema_version = 1\n[server]\ntrusted_origins = "loopback"\n',
                    ValueError,
                ),
                (
                    b'schema_version = 1\n[database]\nbusy_timeout_ms = "slow"\n',
                    TypeError,
                ),
                (b"\xff", ValueError),
                (b"x" * (256 * 1024 + 1), ValueError),
            )
            for content, expected_error in cases:
                with self.subTest(content=content[:30]):
                    path.write_bytes(content)
                    with self.assertRaises(expected_error):
                        load_settings(path)

            target = root / "target.toml"
            target.write_text("", encoding="utf-8")
            link = root / "link.toml"
            link.symlink_to(target)
            with self.assertRaises(ValueError):
                load_settings(link)

    def test_schema_rejects_nonlocal_paths_origins_and_credentials(self) -> None:
        with self.assertRaises(ValueError):
            AppPaths(Path("relative"), Path("relative"), Path("relative"))
        for settings in (
            lambda: ServerSettings(port=False),
            lambda: ServerSettings(port=70_000),
            lambda: ServerSettings(trusted_origins=("file:///tmp/app",)),
            lambda: ServerSettings(trusted_origins=("http://localhost:4765",)),
            lambda: ServerSettings(trusted_origins=("http://127.0.0.1:4765/path",)),
            lambda: ServerSettings(trusted_origins=("http://user@127.0.0.1:4765",)),
            lambda: ServerSettings(trusted_origins=("http://127.0.0.1:4765?mode=test",)),
            lambda: ServerSettings(trusted_origins=("http://127.0.0.1:4765#fragment",)),
            lambda: ServerSettings(trusted_origins=("http://127.0.0.1:70000",)),
            lambda: DatabaseSettings(
                profile="postgresql",
                url="postgresql+psycopg://name:value@localhost/database",
            ),
            lambda: DatabaseSettings(
                profile="sqlite",
                url="sqlite+pysqlite://relative.sqlite3",
            ),
            lambda: DatabaseSettings(
                profile="sqlite",
                url="sqlite+pysqlite:///:memory:",
                busy_timeout_ms=1,
            ),
            lambda: DatabaseSettings.sqlite(Path("relative.sqlite3")),
        ):
            with self.subTest(settings=settings), self.assertRaises((TypeError, ValueError)):
                settings()

        resolved = default_paths()
        self.assertTrue(resolved.config_dir.is_absolute())
        self.assertTrue(resolved.data_dir.is_absolute())
        self.assertTrue(resolved.cache_dir.is_absolute())


if __name__ == "__main__":
    unittest.main()
