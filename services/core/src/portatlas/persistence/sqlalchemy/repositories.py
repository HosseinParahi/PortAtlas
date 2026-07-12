"""SQLAlchemy implementations of application repository ports."""

from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from portatlas.domain.identity import OpaqueId, ResourceKind
from portatlas.domain.projects import Project, ProjectInstance, ProjectInstanceState
from portatlas.domain.revision import Revision
from portatlas.persistence.sqlalchemy.models import ProjectInstanceRow, ProjectRow

_MAX_PAGE_SIZE = 500


def _restore_utc(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=UTC)
    return value.astimezone(UTC)


def _project_from_row(row: ProjectRow) -> Project:
    return Project(
        project_id=OpaqueId.parse(row.project_id, expected_kind=ResourceKind.PROJECT),
        display_name=row.display_name,
        repository_identity=row.repository_identity,
        manifest_identity=row.manifest_identity,
        revision=Revision(row.revision),
        created_at=_restore_utc(row.created_at),
        updated_at=_restore_utc(row.updated_at),
    )


def _instance_from_row(row: ProjectInstanceRow) -> ProjectInstance:
    return ProjectInstance(
        instance_id=OpaqueId.parse(row.instance_id, expected_kind=ResourceKind.PROJECT_INSTANCE),
        project_id=OpaqueId.parse(row.project_id, expected_kind=ResourceKind.PROJECT),
        root_id=OpaqueId.parse(row.root_id, expected_kind=ResourceKind.PROJECT_ROOT),
        canonical_path=row.canonical_path,
        worktree_identity=row.worktree_identity,
        state=ProjectInstanceState(row.state),
        revision=Revision(row.revision),
        created_at=_restore_utc(row.created_at),
        updated_at=_restore_utc(row.updated_at),
    )


class SqlAlchemyProjectRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, project: Project) -> None:
        self._session.add(
            ProjectRow(
                project_id=str(project.project_id),
                display_name=project.display_name,
                repository_identity=project.repository_identity,
                manifest_identity=project.manifest_identity,
                revision=project.revision.value,
                created_at=project.created_at,
                updated_at=project.updated_at,
            )
        )

    def get(self, project_id: OpaqueId) -> Project | None:
        if project_id.kind is not ResourceKind.PROJECT:
            raise ValueError("Project repository requires a project identifier.")
        row = self._session.get(ProjectRow, str(project_id))
        return _project_from_row(row) if row is not None else None

    def list(self, *, limit: int = 100) -> list[Project]:
        if not 1 <= limit <= _MAX_PAGE_SIZE:
            raise ValueError("Repository page limit is outside its bounded range.")
        rows = self._session.scalars(
            select(ProjectRow).order_by(ProjectRow.project_id).limit(limit)
        )
        return [_project_from_row(row) for row in rows]


class SqlAlchemyProjectInstanceRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, instance: ProjectInstance) -> None:
        row = ProjectInstanceRow(
            instance_id=str(instance.instance_id),
            project_id=str(instance.project_id),
            root_id=str(instance.root_id),
            canonical_path=instance.canonical_path,
            worktree_identity=instance.worktree_identity,
            state=instance.state.value,
            revision=instance.revision.value,
            created_at=instance.created_at,
            updated_at=instance.updated_at,
        )
        pending_parent = next(
            (
                candidate
                for candidate in self._session.new
                if isinstance(candidate, ProjectRow)
                and candidate.project_id == str(instance.project_id)
            ),
            None,
        )
        if pending_parent is not None:
            row.project = pending_parent
        self._session.add(row)

    def get(self, instance_id: OpaqueId) -> ProjectInstance | None:
        if instance_id.kind is not ResourceKind.PROJECT_INSTANCE:
            raise ValueError("Instance repository requires a ProjectInstance identifier.")
        row = self._session.get(ProjectInstanceRow, str(instance_id))
        return _instance_from_row(row) if row is not None else None

    def list_for_project(self, project_id: OpaqueId, *, limit: int = 100) -> list[ProjectInstance]:
        if project_id.kind is not ResourceKind.PROJECT:
            raise ValueError("Instance repository requires a project identifier.")
        if not 1 <= limit <= _MAX_PAGE_SIZE:
            raise ValueError("Repository page limit is outside its bounded range.")
        rows = self._session.scalars(
            select(ProjectInstanceRow)
            .where(ProjectInstanceRow.project_id == str(project_id))
            .order_by(ProjectInstanceRow.instance_id)
            .limit(limit)
        )
        return [_instance_from_row(row) for row in rows]
