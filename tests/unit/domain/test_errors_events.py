"""UT-DOM-001 and CT-API-001: safe error and event contracts."""

from __future__ import annotations

import unittest
from datetime import UTC, datetime
from math import inf, nan

from portatlas.domain.clock import FrozenClock
from portatlas.domain.errors import ErrorCode, SafeError
from portatlas.domain.events import DomainEvent, ResourceReference
from portatlas.domain.identity import OpaqueId
from portatlas.domain.revision import Revision


class ErrorAndEventTests(unittest.TestCase):
    def test_safe_error_has_a_stable_code_and_bounded_safe_details(self) -> None:
        error = SafeError(
            ErrorCode.RESOURCE_NOT_FOUND,
            "The authorized resource does not exist.",
            details={"resource_type": "project"},
        )

        self.assertEqual(
            error.as_dict(request_id="req_00000000-0000-4000-8000-000000000001"),
            {
                "code": "RESOURCE_NOT_FOUND",
                "message": "The authorized resource does not exist.",
                "retryable": False,
                "request_id": "req_00000000-0000-4000-8000-000000000001",
                "details": {"resource_type": "project"},
            },
        )

    def test_safe_error_rejects_secret_bearing_detail_names_and_multiline_text(self) -> None:
        for details in ({"token": "canary"}, {"database_password": "canary"}):
            with self.subTest(details=details), self.assertRaises(ValueError):
                SafeError(ErrorCode.REQUEST_INVALID, "Invalid input.", details=details)

        with self.assertRaises(ValueError):
            SafeError(ErrorCode.REQUEST_INVALID, "Invalid\nsecret-bearing line.")

    def test_safe_values_reject_secret_shapes_and_non_finite_numbers(self) -> None:
        secret_shapes = (
            "gh" + "p_" + "A" * 30,
            "Bearer " + "A" * 32,
            "https://user:" + "value@example.invalid/resource",
        )
        for value in (*secret_shapes, inf, -inf, nan):
            with self.subTest(value=repr(value)), self.assertRaises(ValueError):
                SafeError(
                    ErrorCode.REQUEST_INVALID,
                    "Invalid input.",
                    details={"value": value},
                )

    def test_safe_error_snapshots_nested_details_before_exposure(self) -> None:
        nested = {"context": {"values": ["safe"]}}
        error = SafeError(
            ErrorCode.REQUEST_INVALID,
            "Invalid input.",
            details=nested,
        )

        nested["context"]["values"][0] = "gh" + "p_" + "A" * 30

        representation = error.as_dict(request_id="req_00000000-0000-4000-8000-000000000001")
        self.assertEqual(representation["details"], {"context": {"values": ["safe"]}})

    def test_domain_event_carries_schema_resource_revision_and_injected_time(self) -> None:
        clock = FrozenClock(datetime(2026, 7, 11, tzinfo=UTC))
        project_id = OpaqueId.parse("prj_00000000-0000-4000-8000-000000000001")
        event = DomainEvent.create(
            event_type="project.created",
            resource=ResourceReference("project", project_id, Revision.initial()),
            payload={"state": "active"},
            clock=clock,
            id_factory=lambda _: OpaqueId.parse("evt_00000000-0000-4000-8000-000000000004"),
        )

        representation = event.as_dict()
        self.assertEqual(representation["schema_version"], 1)
        self.assertEqual(representation["timestamp"], "2026-07-11T00:00:00Z")
        self.assertEqual(representation["resource"]["revision"], 1)
        self.assertEqual(representation["resource"]["id"], str(project_id))

    def test_event_payload_rejects_secret_keys(self) -> None:
        clock = FrozenClock(datetime(2026, 7, 11, tzinfo=UTC))
        project_id = OpaqueId.parse("prj_00000000-0000-4000-8000-000000000001")
        with self.assertRaises(ValueError):
            DomainEvent.create(
                event_type="project.created",
                resource=ResourceReference("project", project_id, Revision.initial()),
                payload={"auth": {"bearer_token": "canary"}},
                clock=clock,
            )

    def test_event_snapshots_nested_payload_before_serialization(self) -> None:
        clock = FrozenClock(datetime(2026, 7, 11, tzinfo=UTC))
        project_id = OpaqueId.parse("prj_00000000-0000-4000-8000-000000000001")
        payload = {"state": {"labels": ["safe"]}}
        event = DomainEvent.create(
            event_type="project.created",
            resource=ResourceReference("project", project_id, Revision.initial()),
            payload=payload,
            clock=clock,
        )

        payload["state"]["labels"][0] = "gh" + "p_" + "A" * 30

        self.assertEqual(event.as_dict()["payload"], {"state": {"labels": ["safe"]}})


if __name__ == "__main__":
    unittest.main()
