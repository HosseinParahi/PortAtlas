"""Logical Project and concrete worktree-aware ProjectInstance aggregates."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, replace
from datetime import datetime
from enum import StrEnum
from pathlib import Path, PurePath

from portatlas.domain.clock import Clock, require_utc
from portatlas.domain.errors import ErrorCode, SafeError
from portatlas.domain.identity import OpaqueId, ResourceKind
from portatlas.domain.revision import Revision

IdFactory = Callable[[ResourceKind], OpaqueId]


class ProjectInstanceState(StrEnum):
    DISCOVERED = "discovered"
    ACTIVE = "active"
    PAUSED = "paused"
    INACCESSIBLE = "inaccessible"
    ARCHIVED = "archived"
    REMOVED = "removed"


_INSTANCE_TRANSITIONS: dict[ProjectInstanceState, frozenset[ProjectInstanceState]] = {
    ProjectInstanceState.DISCOVERED: frozenset(
        {
            ProjectInstanceState.ACTIVE,
            ProjectInstanceState.PAUSED,
            ProjectInstanceState.INACCESSIBLE,
            ProjectInstanceState.ARCHIVED,
            ProjectInstanceState.REMOVED,
        }
    ),
    ProjectInstanceState.ACTIVE: frozenset(
        {
            ProjectInstanceState.PAUSED,
            ProjectInstanceState.INACCESSIBLE,
            ProjectInstanceState.ARCHIVED,
            ProjectInstanceState.REMOVED,
        }
    ),
    ProjectInstanceState.PAUSED: frozenset(
        {
            ProjectInstanceState.ACTIVE,
            ProjectInstanceState.INACCESSIBLE,
            ProjectInstanceState.ARCHIVED,
            ProjectInstanceState.REMOVED,
        }
    ),
    ProjectInstanceState.INACCESSIBLE: frozenset(
        {
            ProjectInstanceState.ACTIVE,
            ProjectInstanceState.PAUSED,
            ProjectInstanceState.ARCHIVED,
            ProjectInstanceState.REMOVED,
        }
    ),
    ProjectInstanceState.ARCHIVED: frozenset(
        {ProjectInstanceState.ACTIVE, ProjectInstanceState.REMOVED}
    ),
    ProjectInstanceState.REMOVED: frozenset(),
}


def _bounded_text(value: str | None, *, field: str, maximum: int) -> str | None:
    if value is None:
        return None
    normalized = value.strip()
    if (
        not normalized
        or len(normalized) > maximum
        or any(marker in normalized for marker in ("\n", "\r", "\x00"))
    ):
        raise ValueError(f"{field} must be bounded, non-empty, single-line text.")
    return normalized


@dataclass(frozen=True, slots=True)
class Project:
    project_id: OpaqueId
    display_name: str
    revision: Revision
    created_at: datetime
    updated_at: datetime
    repository_identity: str | None = None
    manifest_identity: str | None = None

    def __post_init__(self) -> None:
        if self.project_id.kind is not ResourceKind.PROJECT:
            raise ValueError("Project requires a project identifier.")
        object.__setattr__(
            self,
            "display_name",
            _bounded_text(self.display_name, field="display_name", maximum=200),
        )
        object.__setattr__(
            self,
            "repository_identity",
            _bounded_text(self.repository_identity, field="repository_identity", maximum=512),
        )
        object.__setattr__(
            self,
            "manifest_identity",
            _bounded_text(self.manifest_identity, field="manifest_identity", maximum=256),
        )
        require_utc(self.created_at)
        require_utc(self.updated_at)

    @classmethod
    def create(
        cls,
        *,
        display_name: str,
        clock: Clock,
        id_factory: IdFactory = OpaqueId.new,
        repository_identity: str | None = None,
        manifest_identity: str | None = None,
    ) -> Project:
        now = require_utc(clock.now())
        return cls(
            project_id=id_factory(ResourceKind.PROJECT),
            display_name=display_name,
            repository_identity=repository_identity,
            manifest_identity=manifest_identity,
            revision=Revision.initial(),
            created_at=now,
            updated_at=now,
        )


@dataclass(frozen=True, slots=True)
class ProjectInstance:
    instance_id: OpaqueId
    project_id: OpaqueId
    root_id: OpaqueId
    canonical_path: str
    worktree_identity: str | None
    state: ProjectInstanceState
    revision: Revision
    created_at: datetime
    updated_at: datetime

    def __post_init__(self) -> None:
        expected = (
            (self.instance_id, ResourceKind.PROJECT_INSTANCE),
            (self.project_id, ResourceKind.PROJECT),
            (self.root_id, ResourceKind.PROJECT_ROOT),
        )
        if any(identifier.kind is not kind for identifier, kind in expected):
            raise ValueError("ProjectInstance contains an identifier of the wrong kind.")
        path = PurePath(self.canonical_path)
        if not path.is_absolute() or ".." in path.parts or "\x00" in self.canonical_path:
            raise ValueError("ProjectInstance canonical path must be absolute and normalized.")
        normalized_path = str(path)
        if normalized_path != self.canonical_path:
            raise ValueError("ProjectInstance canonical path must already be normalized.")
        object.__setattr__(
            self,
            "worktree_identity",
            _bounded_text(self.worktree_identity, field="worktree_identity", maximum=512),
        )
        require_utc(self.created_at)
        require_utc(self.updated_at)

    @classmethod
    def create(  # noqa: PLR0913
        cls,
        *,
        project_id: OpaqueId,
        root_id: OpaqueId,
        canonical_path: str | Path,
        worktree_identity: str | None,
        clock: Clock,
        id_factory: IdFactory = OpaqueId.new,
        state: ProjectInstanceState = ProjectInstanceState.DISCOVERED,
    ) -> ProjectInstance:
        now = require_utc(clock.now())
        return cls(
            instance_id=id_factory(ResourceKind.PROJECT_INSTANCE),
            project_id=project_id,
            root_id=root_id,
            canonical_path=str(canonical_path),
            worktree_identity=worktree_identity,
            state=state,
            revision=Revision.initial(),
            created_at=now,
            updated_at=now,
        )

    def transition_to(
        self,
        state: ProjectInstanceState,
        *,
        expected_revision: Revision,
        clock: Clock,
    ) -> ProjectInstance:
        if expected_revision != self.revision:
            raise SafeError(
                ErrorCode.RESOURCE_REVISION_CONFLICT,
                "The ProjectInstance changed; refetch it before retrying.",
                details={
                    "expected_revision": expected_revision.value,
                    "current_revision": self.revision.value,
                },
            )
        if state is self.state:
            return self
        if state not in _INSTANCE_TRANSITIONS[self.state]:
            raise SafeError(
                ErrorCode.RESOURCE_STATE_INVALID,
                "The requested ProjectInstance lifecycle transition is not allowed.",
                details={"from_state": self.state.value, "to_state": state.value},
            )
        return replace(
            self,
            state=state,
            revision=self.revision.next(),
            updated_at=require_utc(clock.now()),
        )
