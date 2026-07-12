"""Persistence ports owned by the application layer."""

from __future__ import annotations

from types import TracebackType
from typing import Protocol, runtime_checkable

from portatlas.domain.identity import OpaqueId
from portatlas.domain.projects import Project, ProjectInstance


@runtime_checkable
class ProjectRepository(Protocol):
    def add(self, project: Project) -> None: ...

    def get(self, project_id: OpaqueId) -> Project | None: ...

    def list(self, *, limit: int = 100) -> list[Project]: ...


@runtime_checkable
class ProjectInstanceRepository(Protocol):
    def add(self, instance: ProjectInstance) -> None: ...

    def get(self, instance_id: OpaqueId) -> ProjectInstance | None: ...

    def list_for_project(
        self, project_id: OpaqueId, *, limit: int = 100
    ) -> list[ProjectInstance]: ...


@runtime_checkable
class UnitOfWork(Protocol):
    projects: ProjectRepository
    project_instances: ProjectInstanceRepository

    async def __aenter__(self) -> UnitOfWork: ...

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None: ...

    async def commit(self) -> None: ...

    async def rollback(self) -> None: ...
