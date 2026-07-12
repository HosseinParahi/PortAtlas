"""CT-MCP-001: MCP revision and assurance-language foundation contract."""

from __future__ import annotations

import unittest

from portatlas.mcp.constants import (
    MANAGED_ASSURANCE_NOTICE,
    MCP_SPEC_REVISION,
    UNMANAGED_EVIDENCE_NOTICE,
    McpTransport,
)


class McpFoundationContractTests(unittest.TestCase):
    def test_revision_and_mvp_transports_are_locked(self) -> None:
        self.assertEqual(MCP_SPEC_REVISION, "2025-11-25")
        self.assertEqual(
            {transport.value for transport in McpTransport},
            {"stdio", "streamable-http"},
        )

    def test_managed_assurance_and_unmanaged_evidence_are_distinct(self) -> None:
        self.assertIn("reservation", MANAGED_ASSURANCE_NOTICE.lower())
        self.assertIn("atomic lease", MANAGED_ASSURANCE_NOTICE.lower())
        self.assertIn("observation", UNMANAGED_EVIDENCE_NOTICE.lower())
        self.assertIn("stale", UNMANAGED_EVIDENCE_NOTICE.lower())
        self.assertNotEqual(MANAGED_ASSURANCE_NOTICE, UNMANAGED_EVIDENCE_NOTICE)


if __name__ == "__main__":
    unittest.main()
