"""Database engine/session construction with SQLite safety settings."""

from __future__ import annotations

import sqlite3
from collections.abc import Mapping
from typing import Any

from sqlalchemy import Engine, create_engine, event
from sqlalchemy.engine import make_url
from sqlalchemy.orm import Session, sessionmaker

from portatlas.persistence.sqlalchemy.models import Base

_MIN_BUSY_TIMEOUT_MS = 100
_MAX_BUSY_TIMEOUT_MS = 60_000


def create_database_engine(
    url: str,
    *,
    busy_timeout_ms: int = 5_000,
    connect_args: Mapping[str, Any] | None = None,
) -> Engine:
    """Construct a SQLAlchemy engine for an accepted persistence profile."""

    parsed = make_url(url)
    if parsed.drivername not in {"sqlite+pysqlite", "postgresql+psycopg"}:
        raise ValueError("Unsupported database driver for the foundation profile.")
    arguments = dict(connect_args or {})
    if parsed.drivername == "sqlite+pysqlite":
        arguments.setdefault("check_same_thread", False)
    engine = create_engine(
        parsed,
        connect_args=arguments,
        pool_pre_ping=True,
    )
    if parsed.drivername == "sqlite+pysqlite":
        _configure_sqlite(engine, busy_timeout_ms=busy_timeout_ms)
    return engine


def create_sqlite_engine(url: str, *, busy_timeout_ms: int = 5_000) -> Engine:
    parsed = make_url(url)
    if parsed.drivername != "sqlite+pysqlite":
        raise ValueError("Embedded engine requires sqlite+pysqlite.")
    return create_database_engine(url, busy_timeout_ms=busy_timeout_ms)


def _configure_sqlite(engine: Engine, *, busy_timeout_ms: int) -> None:
    if not _MIN_BUSY_TIMEOUT_MS <= busy_timeout_ms <= _MAX_BUSY_TIMEOUT_MS:
        raise ValueError("SQLite busy timeout is outside the bounded range.")

    @event.listens_for(engine, "connect")
    def configure_connection(
        connection: sqlite3.Connection,
        _connection_record: object,
    ) -> None:
        cursor = connection.cursor()
        try:
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.execute(f"PRAGMA busy_timeout={busy_timeout_ms:d}")
            database = cursor.execute("PRAGMA database_list").fetchone()
            if database is not None and database[2] not in ("", ":memory:"):
                cursor.execute("PRAGMA journal_mode=WAL")
        finally:
            cursor.close()


def create_schema(engine: Engine) -> None:
    """Create the migration-equivalent schema for isolated test harnesses only."""

    Base.metadata.create_all(engine)


def create_session_factory(engine: Engine) -> sessionmaker[Session]:
    return sessionmaker(bind=engine, expire_on_commit=False)
