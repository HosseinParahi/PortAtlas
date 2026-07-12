"""Foundation persistence rows for Project and ProjectInstance identity."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Index, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class FoundationMetadataRow(Base):
    """Migration-owned foundation marker retained in schema metadata."""

    __tablename__ = "foundation_metadata"

    key: Mapped[str] = mapped_column(String(64), primary_key=True)
    value: Mapped[str] = mapped_column(String(256), nullable=False)


class ProjectRow(Base):
    __tablename__ = "projects"
    __table_args__ = (CheckConstraint("revision >= 1", name="ck_projects_revision_positive"),)

    project_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    display_name: Mapped[str] = mapped_column(String(200), nullable=False)
    repository_identity: Mapped[str | None] = mapped_column(String(512))
    manifest_identity: Mapped[str | None] = mapped_column(String(256))
    revision: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    instances: Mapped[list[ProjectInstanceRow]] = relationship(back_populates="project")


class ProjectInstanceRow(Base):
    __tablename__ = "project_instances"
    __table_args__ = (
        CheckConstraint("revision >= 1", name="ck_project_instances_revision_positive"),
        Index(
            "uq_project_instances_active_path",
            "canonical_path",
            unique=True,
            sqlite_where=None,
        ),
        Index("ix_project_instances_project_id", "project_id"),
    )

    instance_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    project_id: Mapped[str] = mapped_column(
        String(64), ForeignKey("projects.project_id", ondelete="RESTRICT"), nullable=False
    )
    root_id: Mapped[str] = mapped_column(String(64), nullable=False)
    canonical_path: Mapped[str] = mapped_column(String(4096), nullable=False)
    worktree_identity: Mapped[str | None] = mapped_column(String(512))
    state: Mapped[str] = mapped_column(String(32), nullable=False)
    revision: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    project: Mapped[ProjectRow] = relationship(back_populates="instances")
