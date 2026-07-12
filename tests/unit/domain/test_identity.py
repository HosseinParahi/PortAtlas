"""UT-DOM-001: opaque identifier contract tests."""

from __future__ import annotations

import re
import unittest
from uuid import UUID

from portatlas.domain.identity import OpaqueId, ResourceKind


class OpaqueIdTests(unittest.TestCase):
    def test_new_id_has_the_resource_prefix_and_an_opaque_uuid_payload(self) -> None:
        identifier = OpaqueId.new(ResourceKind.PROJECT)

        self.assertEqual(identifier.kind, ResourceKind.PROJECT)
        self.assertRegex(str(identifier), r"^prj_[0-9a-f-]{36}$")
        UUID(str(identifier).removeprefix("prj_"))

    def test_parse_rejects_a_wrong_expected_resource_kind(self) -> None:
        with self.assertRaises(ValueError):
            OpaqueId.parse(
                "ins_00000000-0000-4000-8000-000000000001",
                expected_kind=ResourceKind.PROJECT,
            )

    def test_clients_cannot_smuggle_noncanonical_or_parseable_payloads(self) -> None:
        invalid_ids = (
            "prj_1",
            "prj_00000000000040008000000000000001",
            "prj_00000000-0000-4000-8000-000000000001/child",
            "unknown_00000000-0000-4000-8000-000000000001",
        )

        for candidate in invalid_ids:
            with self.subTest(candidate=candidate), self.assertRaises(ValueError):
                OpaqueId.parse(candidate)

    def test_representation_never_exposes_an_internal_field_name(self) -> None:
        identifier = OpaqueId.parse("prj_00000000-0000-4000-8000-000000000001")

        self.assertEqual(str(identifier), identifier.value)
        self.assertTrue(re.fullmatch(r"prj_[0-9a-f-]{36}", identifier.value))


if __name__ == "__main__":
    unittest.main()
