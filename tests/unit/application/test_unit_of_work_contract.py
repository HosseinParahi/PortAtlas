"""TEST-ARCH-001 and IT-SQL-001: reusable persistence fake contracts."""

from __future__ import annotations

import asyncio
import unittest
from datetime import UTC, datetime

from portatlas.application.unit_of_work import (
    ProjectInstanceRepository,
    ProjectRepository,
    UnitOfWork,
)
from portatlas.domain.clock import FrozenClock
from portatlas.domain.projects import Project

from tests.fakes.persistence import InMemoryPersistenceState, InMemoryUnitOfWork


class InMemoryUnitOfWorkContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.state = InMemoryPersistenceState()
        self.clock = FrozenClock(datetime(2026, 7, 11, tzinfo=UTC))

    def test_fake_satisfies_runtime_protocols_and_commits(self) -> None:
        async def scenario() -> None:
            project = Project.create(display_name="Synthetic project", clock=self.clock)
            uow = InMemoryUnitOfWork(self.state)

            self.assertIsInstance(uow, UnitOfWork)
            self.assertIsInstance(uow.projects, ProjectRepository)
            self.assertIsInstance(uow.project_instances, ProjectInstanceRepository)
            async with uow:
                uow.projects.add(project)
                await uow.commit()

            self.assertEqual(self.state.projects[project.project_id], project)

        asyncio.run(scenario())

    def test_fake_rolls_back_when_context_exits_without_commit(self) -> None:
        async def scenario() -> None:
            project = Project.create(display_name="Synthetic project", clock=self.clock)
            uow = InMemoryUnitOfWork(self.state)
            async with uow:
                uow.projects.add(project)

            self.assertEqual(self.state.projects, {})

        asyncio.run(scenario())


if __name__ == "__main__":
    unittest.main()
