"""Behavioral tests for the documentation quality gate."""

from __future__ import annotations

import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

from scripts import validate_docs


class ValidateDocsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def write(self, relative_path: str, content: str) -> Path:
        path = self.root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def codes(self, issues: list[validate_docs.Issue]) -> set[str]:
        return {issue.code for issue in issues}

    def test_required_files_reports_missing_and_empty_content(self) -> None:
        self.write("present.md", "# Present\n")
        self.write("empty.md", "  \n")

        issues = validate_docs.check_required_files(
            self.root, ("present.md", "empty.md", "missing.md")
        )

        self.assertEqual(
            {"REQUIRED_EMPTY", "REQUIRED_MISSING"},
            self.codes(issues),
        )

    def test_internal_markdown_links_accept_fragments_and_reject_missing_targets(self) -> None:
        self.write("docs/target.md", "# Target heading\n")
        self.write(
            "README.md",
            "# Index\n\n[good](docs/target.md#target-heading)\n"
            "[bad](docs/missing.md)\n[external](https://example.com)\n",
        )

        issues = validate_docs.check_internal_links(self.root)

        self.assertEqual(["LINK_TARGET_MISSING"], [issue.code for issue in issues])
        self.assertIn("docs/missing.md", issues[0].message)

    def test_adr_numbering_requires_unique_contiguous_0001_through_0023(self) -> None:
        for number in range(1, 24):
            self.write(f"docs/adr/{number:04d}-decision.md", f"# ADR-{number:04d}\n")
        self.write("docs/adr/0001-duplicate.md", "# ADR-0001\n")
        (self.root / "docs/adr/0010-decision.md").unlink()

        issues = validate_docs.check_adr_numbering(self.root)

        self.assertEqual({"ADR_DUPLICATE", "ADR_SEQUENCE"}, self.codes(issues))

    def test_unique_id_check_distinguishes_definitions_from_references(self) -> None:
        self.write(
            "docs/requirements/functional-requirements.md",
            "# A\n\n### SRS-COL-001 — First definition\n"
            "Reference SRS-COL-001.\n\n### SRS-COL-001 — Duplicate definition\n",
        )
        self.write(
            "docs/requirements/acceptance-criteria.md",
            "# Verification\n\n| ID | Requirement |\n|---|---|\n"
            "| VT-SRS-COL-001 | SRS-COL-001 |\n"
            "| VT-SRS-COL-001 | SRS-COL-001 |\n",
        )
        self.write(
            "docs/testing/test-strategy.md",
            "# Tests\n\n| ID | Purpose |\n|---|---|\n| UAT-001 | First |\n"
            "| UAT-001 | Duplicate |\n",
        )

        issues = validate_docs.check_unique_id_definitions(self.root)

        self.assertEqual(
            {"REQUIREMENT_ID_DUPLICATE", "TEST_ID_DUPLICATE"},
            self.codes(issues),
        )

    def test_invalid_utf8_becomes_a_deterministic_issue_and_cli_failure(self) -> None:
        bad_path = self.root / "docs/bad.md"
        bad_path.parent.mkdir(parents=True, exist_ok=True)
        bad_path.write_bytes(b"# bad\n\xff\xfe")

        issues = validate_docs.validate_repository(
            self.root,
            required_files=(),
            require_full_adr_set=False,
            require_traceability=False,
        )
        output = StringIO()
        with redirect_stdout(output):
            exit_code = validate_docs.main(["--root", str(self.root)])

        self.assertIn("CONTENT_ENCODING", self.codes(issues))
        self.assertEqual(1, exit_code)
        self.assertIn("CONTENT_ENCODING", output.getvalue())

    def test_adr_numbering_rejects_empty_and_mismatched_documents(self) -> None:
        for number in range(1, 24):
            content = "" if number == 7 else f"# ADR-{number:04d}\n"
            self.write(f"docs/adr/{number:04d}-decision.md", content)
        self.write("docs/adr/0012-decision.md", "# ADR-9999\n")

        issues = validate_docs.check_adr_numbering(self.root)

        self.assertIn("ADR_EMPTY", self.codes(issues))
        self.assertIn("ADR_HEADING_MISMATCH", self.codes(issues))

    def test_traceability_ignores_reference_shaped_prose(self) -> None:
        lines = [
            f"AC-{number:03d} BO-01 PF-001 SRS-COL-001 CMP-COL UAT-001 Gate 4"
            for number in range(1, 16)
        ]
        self.write("docs/requirements/traceability-matrix.md", "\n".join(lines))

        issues = validate_docs.check_traceability(self.root)

        self.assertIn("TRACEABILITY_COUNT", self.codes(issues))

    def test_internal_link_check_covers_images_and_reference_definitions(self) -> None:
        self.write(
            "README.md",
            "# Links\n\n![missing image](docs/missing.png)\n"
            "Read the [guide][guide-ref].\n\n[guide-ref]: docs/missing.md\n",
        )

        issues = validate_docs.check_internal_links(self.root)

        self.assertEqual(2, len(issues))
        self.assertTrue(all(issue.code == "LINK_TARGET_MISSING" for issue in issues))

    def test_content_safety_covers_text_markers_and_fine_grained_github_tokens(self) -> None:
        marker = "T" + "BD"
        token = "github" + "_pat_" + "A" * 30 + "_" + "B" * 40
        self.write("notes.txt", f"{marker}\n{token}\n")

        issues = validate_docs.check_content_safety(self.root)

        self.assertEqual({"PLACEHOLDER", "SECRET_PATTERN"}, self.codes(issues))

    def test_traceability_reference_integrity_rejects_undefined_ids(self) -> None:
        self.write(
            "docs/requirements/traceability-matrix.md",
            "| AC-001 | BO-01 | PF-001 | SRS-COL-999 | CMP-COL | UAT-999 | Gate 4 |\n",
        )

        issues = validate_docs.check_traceability_reference_integrity(self.root)

        self.assertEqual(
            {"TRACEABILITY_REQUIREMENT_UNDEFINED", "TRACEABILITY_TEST_UNDEFINED"},
            self.codes(issues),
        )

    def test_traceability_requires_fifteen_complete_acceptance_scenarios(self) -> None:
        rows = [
            "| Scenario | BRD | PRD | Requirement | Component | Test | Gate |",
            "|---|---|---|---|---|---|---|",
        ]
        for number in range(1, 16):
            rows.append(
                f"| AC-{number:03d} | BRD-OBJ-001 | PRD-FEAT-001 | "
                f"SRS-COL-{number:03d} | CMP-COL | UAT-{number:03d} | Gate 4 |"
            )
        self.write("docs/requirements/traceability-matrix.md", "\n".join(rows))

        self.assertEqual([], validate_docs.check_traceability(self.root))

        rows.pop()
        rows[-1] = "| AC-014 | BRD-OBJ-001 |  | SRS-COL-014 | CMP-COL | UAT-014 | Gate 4 |"
        self.write("docs/requirements/traceability-matrix.md", "\n".join(rows))

        self.assertEqual(
            {"TRACEABILITY_COUNT", "TRACEABILITY_INCOMPLETE"},
            self.codes(validate_docs.check_traceability(self.root)),
        )

    def test_placeholder_personal_path_and_secret_checks_detect_unsafe_text(self) -> None:
        placeholder = "TO" + "DO"
        personal_path = "/Users/" + "founder" + "/project"
        secret = "gh" + "p_" + "A" * 36
        self.write(
            "docs/unsafe.md",
            f"# Unsafe\n\n{placeholder}: later\n{personal_path}\n{secret}\n",
        )

        issues = validate_docs.check_content_safety(self.root)

        self.assertEqual(
            {"PLACEHOLDER", "PERSONAL_PATH", "SECRET_PATTERN"},
            self.codes(issues),
        )

    def test_validate_repository_combines_checks_and_passes_safe_minimal_tree(self) -> None:
        self.write("README.md", "# Safe repository\n")
        self.write("docs/note.md", "# Note\n\nNo unresolved markers.\n")

        issues = validate_docs.validate_repository(
            self.root,
            required_files=("README.md", "docs/note.md"),
            require_full_adr_set=False,
            require_traceability=False,
        )

        self.assertEqual([], issues)

    def test_validate_repository_runs_full_adr_and_traceability_checks(self) -> None:
        for number in range(1, 24):
            self.write(f"docs/adr/{number:04d}-decision.md", f"# ADR-{number:04d}\n\nDecision.\n")
        self.write(
            "docs/requirements/functional-requirements.md",
            "# Requirements\n\n### SRS-COL-001 — Collector\n",
        )
        self.write(
            "docs/testing/uat-plan.md",
            "# UAT\n\n| Test ID | Case |\n|---|---|\n| UAT-001 | Case |\n",
        )
        rows = [
            "| Scenario | BRD | PRD | Requirement | Component | Test | Gate |",
            "|---|---|---|---|---|---|---|",
        ]
        rows.extend(
            f"| AC-{number:03d} | BO-01 | PF-001 | SRS-COL-001 | CMP-COL | UAT-001 | Gate 4 |"
            for number in range(1, 16)
        )
        self.write("docs/requirements/traceability-matrix.md", "\n".join(rows))

        issues = validate_docs.validate_repository(self.root, required_files=())

        self.assertEqual([], issues)


if __name__ == "__main__":
    unittest.main()
