"""Create the Gate 3 metadata and repository-compatible identity tables.

Revision ID: 0001_foundation
Revises:
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0001_foundation"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    metadata_table = op.create_table(
        "foundation_metadata",
        sa.Column("key", sa.String(length=64), nullable=False),
        sa.Column("value", sa.String(length=256), nullable=False),
        sa.PrimaryKeyConstraint("key"),
    )
    op.bulk_insert(
        metadata_table,
        [
            {"key": "foundation_schema", "value": "1"},
            {"key": "working_title", "value": "PortAtlas"},
        ],
    )
    op.create_table(
        "projects",
        sa.Column("project_id", sa.String(length=64), nullable=False),
        sa.Column("display_name", sa.String(length=200), nullable=False),
        sa.Column("repository_identity", sa.String(length=512), nullable=True),
        sa.Column("manifest_identity", sa.String(length=256), nullable=True),
        sa.Column("revision", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint("revision >= 1", name="ck_projects_revision_positive"),
        sa.PrimaryKeyConstraint("project_id"),
    )
    op.create_table(
        "project_instances",
        sa.Column("instance_id", sa.String(length=64), nullable=False),
        sa.Column("project_id", sa.String(length=64), nullable=False),
        sa.Column("root_id", sa.String(length=64), nullable=False),
        sa.Column("canonical_path", sa.String(length=4096), nullable=False),
        sa.Column("worktree_identity", sa.String(length=512), nullable=True),
        sa.Column("state", sa.String(length=32), nullable=False),
        sa.Column("revision", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "revision >= 1",
            name="ck_project_instances_revision_positive",
        ),
        sa.ForeignKeyConstraint(
            ["project_id"],
            ["projects.project_id"],
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("instance_id"),
    )
    op.create_index(
        "ix_project_instances_project_id",
        "project_instances",
        ["project_id"],
        unique=False,
    )
    op.create_index(
        "uq_project_instances_active_path",
        "project_instances",
        ["canonical_path"],
        unique=True,
    )


def downgrade() -> None:
    op.drop_index("uq_project_instances_active_path", table_name="project_instances")
    op.drop_index("ix_project_instances_project_id", table_name="project_instances")
    op.drop_table("project_instances")
    op.drop_table("projects")
    op.drop_table("foundation_metadata")
