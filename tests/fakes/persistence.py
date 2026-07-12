"""In-memory repository and unit-of-work fakes owned by the test harness."""

from __future__ import annotations

from dataclasses import dataclass, field
from types import TracebackType

from portatlas.domain.identity import OpaqueId
from portatlas.domain.projects import Project, ProjectInstance


@dataclass(slots=True)
class InMemoryPersistenceState:
    projects: dict[OpaqueId, Project] = field(default_factory=dict)
    project_instances: dict[OpaqueId, ProjectInstance] = field(default_factory=dict)


class InMemoryProjectRepository:
    def __init__(self, items: dict[OpaqueId, Project]) -> None:
        self._items = items

    def add(self, project: Project) -> None:
        self._items[project.project_id] = project

    def get(self, project_id: OpaqueId) -> Project | None:
        return self._items.get(project_id)

    def list(self, *, limit: int = 100) -> list[Project]:
        return [self._items[key] for key in sorted(self._items, key=str)[:limit]]


class InMemoryProjectInstanceRepository:
    def __init__(self, items: dict[OpaqueId, ProjectInstance]) -> None:
        self._items = items

    def add(self, instance: ProjectInstance) -> None:
        self._items[instance.instance_id] = instance

    def get(self, instance_id: OpaqueId) -> ProjectInstance | None:
        return self._items.get(instance_id)

    def list_for_project(
        self,
        project_id: OpaqueId,
        *,
        limit: int = 100,
    ) -> list[ProjectInstance]:
        matching = (item for item in self._items.values() if item.project_id == project_id)
        return sorted(matching, key=lambda item: str(item.instance_id))[:limit]


class InMemoryUnitOfWork:
    def __init__(self, state: InMemoryPersistenceState) -> None:
        self._state = state
        self._entered = False
        self._committed = False
        self._reset_working_state()

    def _reset_working_state(self) -> None:
        self._projects = dict(self._state.projects)
        self._project_instances = dict(self._state.project_instances)
        self.projects = InMemoryProjectRepository(self._projects)
        self.project_instances = InMemoryProjectInstanceRepository(self._project_instances)

    async def __aenter__(self) -> InMemoryUnitOfWork:
        if self._entered:
            raise RuntimeError("In-memory UnitOfWork cannot be re-entered.")
        self._entered = True
        self._committed = False
        self._reset_working_state()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        if exc_type is not None or not self._committed:
            await self.rollback()
        self._entered = False

    async def commit(self) -> None:
        if not self._entered:
            raise RuntimeError("UnitOfWork must be entered before commit.")
        self._state.projects = dict(self._projects)
        self._state.project_instances = dict(self._project_instances)
        self._committed = True

    async def rollback(self) -> None:
        if not self._entered:
            raise RuntimeError("UnitOfWork must be entered before rollback.")
        self._reset_working_state()
        self._committed = False
