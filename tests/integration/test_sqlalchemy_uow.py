"""IT-SQL-001: embedded SQLite repository and unit-of-work foundation."""

from __future__ import annotations

import asyncio
import unittest
from datetime import UTC, datetime

from portatlas.domain.clock import FrozenClock
from portatlas.domain.identity import OpaqueId, ResourceKind
from portatlas.domain.projects import Project, ProjectInstance
from portatlas.persistence.sqlalchemy.database import create_schema, create_sqlite_engine
from portatlas.persistence.sqlalchemy.unit_of_work import SqlAlchemyUnitOfWork
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker


def fixed_id(kind: ResourceKind) -> OpaqueId:
    offsets = {
        ResourceKind.PROJECT: 1,
        ResourceKind.PROJECT_INSTANCE: 2,
        ResourceKind.PROJECT_ROOT: 3,
    }
    return OpaqueId.parse(f"{kind.prefix}00000000-0000-4000-8000-{offsets[kind]:012d}")


class SqlAlchemyUnitOfWorkTests(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = create_sqlite_engine("sqlite+pysqlite:///:memory:")
        create_schema(self.engine)
        self.sessions = sessionmaker(bind=self.engine, expire_on_commit=False)
        self.clock = FrozenClock(datetime(2026, 7, 11, tzinfo=UTC))

    def tearDown(self) -> None:
        self.engine.dispose()

    def test_commit_persists_project_and_worktree_instance(self) -> None:
        async def scenario() -> None:
            project = Project.create(display_name="Atlas", clock=self.clock, id_factory=fixed_id)
            instance = ProjectInstance.create(
                project_id=project.project_id,
                root_id=fixed_id(ResourceKind.PROJECT_ROOT),
                canonical_path="/workspace/atlas-feature",
                worktree_identity="git-worktree:feature",
                clock=self.clock,
                id_factory=fixed_id,
            )
            async with SqlAlchemyUnitOfWork(self.sessions) as uow:
                uow.projects.add(project)
                uow.project_instances.add(instance)
                await uow.commit()

            async with SqlAlchemyUnitOfWork(self.sessions) as uow:
                restored_project = uow.projects.get(project.project_id)
                restored_instance = uow.project_instances.get(instance.instance_id)

            self.assertEqual(restored_project, project)
            self.assertEqual(restored_instance, instance)

        asyncio.run(scenario())

    def test_context_exit_rolls_back_uncommitted_changes(self) -> None:
        async def scenario() -> None:
            project = Project.create(display_name="Atlas", clock=self.clock, id_factory=fixed_id)
            async with SqlAlchemyUnitOfWork(self.sessions) as uow:
                uow.projects.add(project)

            async with SqlAlchemyUnitOfWork(self.sessions) as uow:
                self.assertIsNone(uow.projects.get(project.project_id))

        asyncio.run(scenario())

    def test_sqlite_enables_foreign_keys_and_bounded_busy_timeout(self) -> None:
        with self.engine.connect() as connection:
            foreign_keys = connection.execute(text("PRAGMA foreign_keys")).scalar_one()
            busy_timeout = connection.execute(text("PRAGMA busy_timeout")).scalar_one()

        self.assertEqual(foreign_keys, 1)
        self.assertGreater(busy_timeout, 0)


if __name__ == "__main__":
    unittest.main()
