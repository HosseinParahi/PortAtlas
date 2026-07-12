"""CT-CLI-001: command-line foundation smoke contract."""

from __future__ import annotations

import unittest

from portatlas.cli.app import app
from typer.testing import CliRunner


class CliFoundationContractTests(unittest.TestCase):
    def test_version_is_machine_stable_and_marks_the_working_title(self) -> None:
        result = CliRunner().invoke(app, ["version", "--json"])

        self.assertEqual(result.exit_code, 0, result.output)
        self.assertEqual(
            result.stdout.strip(),
            '{"name":"PortAtlas","status":"working-title","version":"0.0.0.dev0"}',
        )

    def test_foundation_help_does_not_claim_deferred_mutations(self) -> None:
        result = CliRunner().invoke(app, ["--help"])

        self.assertEqual(result.exit_code, 0, result.output)
        help_text = result.stdout.lower()
        self.assertNotIn("kill", help_text)
        self.assertNotIn("launch", help_text)
        self.assertNotIn("patch", help_text)
        self.assertIn("reservations and atomic leases", help_text)
        self.assertIn("unmanaged", help_text)
        self.assertIn("evidence", help_text)
        self.assertIn("not a guarantee", help_text)


if __name__ == "__main__":
    unittest.main()
