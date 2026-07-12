"""UT-DOM-001: Project and worktree-aware ProjectInstance tests."""

from __future__ import annotations

import unittest
from datetime import UTC, datetime

from portatlas.domain.clock import FrozenClock
from portatlas.domain.errors import ErrorCode, SafeError
from portatlas.domain.identity import OpaqueId, ResourceKind
from portatlas.domain.projects import Project, ProjectInstance, ProjectInstanceState


def fixed_id(kind: ResourceKind) -> OpaqueId:
    suffixes = {
        ResourceKind.PROJECT: "00000000-0000-4000-8000-000000000001",
        ResourceKind.PROJECT_INSTANCE: "00000000-0000-4000-8000-000000000002",
        ResourceKind.PROJECT_ROOT: "00000000-0000-4000-8000-000000000003",
    }
    return OpaqueId.parse(f"{kind.prefix}{suffixes[kind]}")


class ProjectIdentityTests(unittest.TestCase):
    def setUp(self) -> None:
        self.clock = FrozenClock(datetime(2026, 7, 11, tzinfo=UTC))

    def test_project_and_instance_have_separate_opaque_identities(self) -> None:
        project = Project.create(
            display_name="Atlas API",
            clock=self.clock,
            id_factory=fixed_id,
            repository_identity="git-common-dir:abc",
        )
        instance = ProjectInstance.create(
            project_id=project.project_id,
            root_id=fixed_id(ResourceKind.PROJECT_ROOT),
            canonical_path="/workspace/atlas-api-feature",
            worktree_identity="git-worktree:feature-a",
            clock=self.clock,
            id_factory=fixed_id,
        )

        self.assertEqual(project.project_id.kind, ResourceKind.PROJECT)
        self.assertEqual(instance.instance_id.kind, ResourceKind.PROJECT_INSTANCE)
        self.assertEqual(instance.project_id, project.project_id)
        self.assertNotEqual(str(instance.instance_id), instance.canonical_path)
        self.assertEqual(instance.state, ProjectInstanceState.DISCOVERED)

    def test_lifecycle_transition_requires_the_expected_revision(self) -> None:
        project = Project.create(display_name="Atlas API", clock=self.clock, id_factory=fixed_id)
        instance = ProjectInstance.create(
            project_id=project.project_id,
            root_id=fixed_id(ResourceKind.PROJECT_ROOT),
            canonical_path="/workspace/atlas-api",
            worktree_identity=None,
            clock=self.clock,
            id_factory=fixed_id,
        )

        active = instance.transition_to(
            ProjectInstanceState.ACTIVE,
            expected_revision=instance.revision,
            clock=self.clock,
        )

        self.assertEqual(active.state, ProjectInstanceState.ACTIVE)
        self.assertEqual(active.revision.value, 2)
        self.assertEqual(instance.revision.value, 1)
        with self.assertRaises(SafeError) as raised:
            active.transition_to(
                ProjectInstanceState.PAUSED,
                expected_revision=instance.revision,
                clock=self.clock,
            )
        self.assertEqual(raised.exception.code, ErrorCode.RESOURCE_REVISION_CONFLICT)

    def test_removed_instances_cannot_be_reactivated(self) -> None:
        project = Project.create(display_name="Atlas API", clock=self.clock, id_factory=fixed_id)
        instance = ProjectInstance.create(
            project_id=project.project_id,
            root_id=fixed_id(ResourceKind.PROJECT_ROOT),
            canonical_path="/workspace/atlas-api",
            worktree_identity=None,
            clock=self.clock,
            id_factory=fixed_id,
            state=ProjectInstanceState.REMOVED,
        )

        with self.assertRaises(SafeError) as raised:
            instance.transition_to(
                ProjectInstanceState.ACTIVE,
                expected_revision=instance.revision,
                clock=self.clock,
            )
        self.assertEqual(raised.exception.code, ErrorCode.RESOURCE_STATE_INVALID)


if __name__ == "__main__":
    unittest.main()
