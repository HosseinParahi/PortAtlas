"""IT-PG-001: opt-in PostgreSQL compatibility smoke through the shared UoW seam."""

from __future__ import annotations

import asyncio
import os
import unittest
from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4

import pytest
from alembic import command
from alembic.config import Config
from portatlas.domain.clock import FrozenClock
from portatlas.domain.projects import Project
from portatlas.persistence.sqlalchemy.database import (
    create_database_engine,
    create_session_factory,
)
from portatlas.persistence.sqlalchemy.unit_of_work import SqlAlchemyUnitOfWork
from sqlalchemy import create_engine, text

TEST_POSTGRES_URL = os.environ.get("TEST_POSTGRES_URL")
MIGRATIONS = Path(__file__).resolve().parents[2] / "services" / "core" / "migrations"
pytestmark = pytest.mark.postgres


@unittest.skipUnless(TEST_POSTGRES_URL, "TEST_POSTGRES_URL is not configured")
class PostgreSQLCompatibilityTests(unittest.TestCase):
    def test_project_round_trip_uses_the_same_repository_and_uow_contract(self) -> None:
        assert TEST_POSTGRES_URL is not None
        schema = f"portatlas_test_{uuid4().hex}"
        administrative_engine = create_engine(TEST_POSTGRES_URL, pool_pre_ping=True)
        engine = None
        try:
            with administrative_engine.begin() as connection:
                connection.execute(text(f'CREATE SCHEMA "{schema}"'))
            engine = create_database_engine(
                TEST_POSTGRES_URL,
                connect_args={"options": f"-csearch_path={schema}"},
            )
            migration_config = Config()
            migration_config.set_main_option("script_location", str(MIGRATIONS))
            with engine.begin() as connection:
                migration_config.attributes["connection"] = connection
                command.upgrade(migration_config, "head")
            sessions = create_session_factory(engine)
            clock = FrozenClock(datetime(2026, 7, 11, tzinfo=UTC))
            project = Project.create(display_name="PostgreSQL smoke", clock=clock)

            async def scenario() -> None:
                async with SqlAlchemyUnitOfWork(sessions) as uow:
                    uow.projects.add(project)
                    await uow.commit()
                async with SqlAlchemyUnitOfWork(sessions) as uow:
                    restored = uow.projects.get(project.project_id)
                self.assertEqual(restored, project)

            asyncio.run(scenario())
        finally:
            if engine is not None:
                engine.dispose()
            with administrative_engine.begin() as connection:
                connection.execute(text(f'DROP SCHEMA IF EXISTS "{schema}" CASCADE'))
            administrative_engine.dispose()


if __name__ == "__main__":
    unittest.main()
