"""IT-SQL-001: Alembic creates the repository-compatible embedded schema."""

from __future__ import annotations

import asyncio
import tempfile
import unittest
from datetime import UTC, datetime
from pathlib import Path

from alembic import command
from alembic.autogenerate import compare_metadata
from alembic.config import Config
from alembic.migration import MigrationContext
from portatlas.domain.clock import FrozenClock
from portatlas.domain.projects import Project
from portatlas.persistence.sqlalchemy.database import (
    create_session_factory,
    create_sqlite_engine,
)
from portatlas.persistence.sqlalchemy.models import Base
from portatlas.persistence.sqlalchemy.unit_of_work import SqlAlchemyUnitOfWork
from sqlalchemy import column, create_engine, inspect, select, table

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
MIGRATIONS = REPOSITORY_ROOT / "services" / "core" / "migrations"


class AlembicFoundationTests(unittest.TestCase):
    def test_empty_sqlite_database_upgrades_to_foundation_head(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "migration.sqlite3"
            url = f"sqlite+pysqlite:///{database}"
            config = Config()
            config.set_main_option("script_location", str(MIGRATIONS))
            config.set_main_option("sqlalchemy.url", url)

            command.upgrade(config, "head")

            engine = create_engine(url)
            try:
                self.assertEqual(
                    set(inspect(engine).get_table_names()),
                    {
                        "alembic_version",
                        "foundation_metadata",
                        "project_instances",
                        "projects",
                    },
                )
                metadata = table("foundation_metadata", column("key"), column("value"))
                with engine.connect() as connection:
                    rows = connection.execute(select(metadata.c.key, metadata.c.value)).tuples()
                    values = dict(rows.all())
                self.assertEqual(values["foundation_schema"], "1")
                self.assertEqual(values["working_title"], "PortAtlas")
                with engine.connect() as connection:
                    drift = compare_metadata(
                        MigrationContext.configure(connection),
                        Base.metadata,
                    )
                self.assertEqual(drift, [])
            finally:
                engine.dispose()

            repository_engine = create_sqlite_engine(url)
            try:
                sessions = create_session_factory(repository_engine)
                project = Project.create(
                    display_name="Migrated repository",
                    clock=FrozenClock(datetime(2026, 7, 11, tzinfo=UTC)),
                )

                async def round_trip() -> None:
                    async with SqlAlchemyUnitOfWork(sessions) as uow:
                        uow.projects.add(project)
                        await uow.commit()
                    async with SqlAlchemyUnitOfWork(sessions) as uow:
                        self.assertEqual(uow.projects.get(project.project_id), project)

                asyncio.run(round_trip())
            finally:
                repository_engine.dispose()


if __name__ == "__main__":
    unittest.main()
