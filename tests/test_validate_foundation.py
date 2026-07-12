"""Regression tests for the standard-library Gate 3 foundation validator."""

from __future__ import annotations

import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from scripts import validate_foundation

PINNED_SHA = "0123456789abcdef0123456789abcdef01234567"


class FoundationRepository:
    """Build a minimal synthetic repository accepted by the validator."""

    def __init__(self, root: Path) -> None:
        self.root = root

    def write(self, relative: str, content: str) -> None:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def write_json(self, relative: str, value: object) -> None:
        self.write(relative, json.dumps(value, indent=2) + "\n")

    def create(self) -> None:
        for relative in validate_foundation.REQUIRED:
            self.write(relative, "foundation\n")

        self.write(".python-version", "3.13.14\n")
        self.write(".node-version", "24.18.0\n")
        self.write(
            "pyproject.toml",
            """\
[project]
name = "portatlas-foundation"
version = "0.0.0.dev0"
classifiers = ["Private :: Do Not Upload"]

[tool.uv]
default-groups = ["dev"]
""",
        )
        self.write_json(
            "package.json",
            {
                "name": "portatlas-foundation-workspace",
                "private": True,
                "scripts": {"check": "node --check checker.mjs"},
            },
        )
        self.write_json(
            "apps/web/package.json",
            {"name": "@portatlas/web", "private": True, "scripts": {}},
        )
        self.write_json(
            "packages/api-client/package.json",
            {"name": "@portatlas/api-client", "private": True, "scripts": {}},
        )
        self.write_json("contracts/openapi/v1.json", {})
        self.write(
            "docs/testing/test-strategy.md",
            """\
# Test strategy

| Test ID | Suite |
| --- | --- |
| AI-EVAL-SAFE-001 | AI safety |
| IT-DKR-001 | Docker |
| PERF-INV-001 | Capacity |
| SEC-T-SECRET-001 | Secrets |
| UT-ALC-001 | Allocator |
| UT-COL-001 | Runtime |
| UT-SCN-001 | Scanners and identity |
""",
        )
        self.write(
            ".github/workflows/ci.yml",
            f"""\
name: Foundation
on: push
permissions:
  contents: read
jobs:
  checks:
    runs-on: ubuntu-24.04
    steps:
      - uses: actions/checkout@{PINNED_SHA}
""",
        )
        for family in validate_foundation.FIXTURE_FAMILIES:
            scenarios = [
                {
                    "id": f"{family}-{kind}",
                    "kind": kind,
                    "seed": index,
                    "sensitivity": "synthetic-canary" if kind == "adversarial" else "synthetic",
                    "test_ids": ["G3-T-FIX-001"],
                }
                for index, kind in enumerate(("benign", "degraded", "adversarial"), start=1)
            ]
            self.write_json(
                f"tests/fixtures/{family}/manifest.json",
                {
                    "schema_version": 1,
                    "family": family,
                    "purpose": f"Synthetic {family} foundation inputs",
                    "scenarios": scenarios,
                },
            )


class ValidateFoundationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)
        self.root = Path(self.temporary_directory.name)
        self.repository = FoundationRepository(self.root)
        self.repository.create()
        patcher = mock.patch.object(validate_foundation, "ROOT", self.root)
        patcher.start()
        self.addCleanup(patcher.stop)

    def run_validator(self, *arguments: str) -> tuple[int, str, str]:
        stdout = io.StringIO()
        stderr = io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            result = validate_foundation.main(list(arguments))
        return result, stdout.getvalue(), stderr.getvalue()

    def test_valid_synthetic_repository_passes(self) -> None:
        result, stdout, stderr = self.run_validator()

        self.assertEqual(result, 0)
        self.assertIn("Gate 3 foundation validation passed", stdout)
        self.assertEqual(stderr, "")

    def test_each_required_file_is_reported_without_crashing(self) -> None:
        for relative in validate_foundation.REQUIRED:
            with self.subTest(relative=relative):
                path = self.root / relative
                original = path.read_bytes()
                path.unlink()
                try:
                    result, _, stderr = self.run_validator()
                finally:
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_bytes(original)

                self.assertEqual(result, 1)
                self.assertIn(f"missing substantive foundation file: {relative}", stderr)

    def test_malformed_project_and_workspace_metadata_are_diagnostics(self) -> None:
        cases = (
            ("pyproject.toml", "[project\n"),
            ("package.json", "{not-json}\n"),
        )
        for relative, invalid in cases:
            with self.subTest(relative=relative):
                path = self.root / relative
                original = path.read_text(encoding="utf-8")
                path.write_text(invalid, encoding="utf-8")
                try:
                    result, _, stderr = self.run_validator()
                finally:
                    path.write_text(original, encoding="utf-8")

                self.assertEqual(result, 1)
                self.assertIn(f"invalid foundation metadata: {relative}", stderr)

    def test_every_workspace_manifest_must_be_private(self) -> None:
        self.repository.write_json(
            "packages/api-client/package.json",
            {"name": "@portatlas/api-client", "private": False, "scripts": {}},
        )

        result, _, stderr = self.run_validator()

        self.assertEqual(result, 1)
        self.assertIn("packages/api-client/package.json must be private", stderr)

    def test_publication_commands_and_configuration_are_rejected(self) -> None:
        cases = (
            ({"scripts": {"release": "npm publish"}}, "publication command"),
            ({"publishConfig": {"access": "public"}}, "publication configuration"),
        )
        for update, expected in cases:
            with self.subTest(expected=expected):
                manifest = {
                    "name": "@portatlas/web",
                    "private": True,
                    "scripts": {},
                    **update,
                }
                self.repository.write_json("apps/web/package.json", manifest)

                result, _, stderr = self.run_validator()

                self.assertEqual(result, 1)
                self.assertIn(expected, stderr)

    def test_fixture_schema_rejects_ambiguous_or_non_synthetic_data(self) -> None:
        path = "tests/fixtures/runtime/manifest.json"
        original = json.loads((self.root / path).read_text(encoding="utf-8"))
        cases = (
            (lambda data: data.pop("purpose"), "purpose"),
            (
                lambda data: data["scenarios"][1].update({"id": data["scenarios"][0]["id"]}),
                "duplicate fixture scenario id",
            ),
            (
                lambda data: data["scenarios"][0].update({"seed": "random"}),
                "integer seed",
            ),
            (
                lambda data: data["scenarios"][0].update({"sensitivity": "private"}),
                "non-synthetic sensitivity",
            ),
            (
                lambda data: data["scenarios"][0].update({"test_ids": []}),
                "test IDs",
            ),
        )
        for mutate, expected in cases:
            with self.subTest(expected=expected):
                manifest = json.loads(json.dumps(original))
                mutate(manifest)
                self.repository.write_json(path, manifest)

                result, _, stderr = self.run_validator()

                self.assertEqual(result, 1)
                self.assertIn(expected, stderr)

    def test_referenced_test_ids_must_have_one_documented_definition(self) -> None:
        manifest_path = "tests/fixtures/runtime/manifest.json"
        manifest = json.loads((self.root / manifest_path).read_text(encoding="utf-8"))
        manifest["scenarios"][0]["test_ids"] = ["TEST-UNKNOWN-999"]
        self.repository.write_json(manifest_path, manifest)

        result, _, stderr = self.run_validator()

        self.assertEqual(result, 1)
        self.assertIn("undefined focused test ID: TEST-UNKNOWN-999", stderr)

    def test_module_docstring_test_ids_are_validated(self) -> None:
        self.repository.write(
            "tests/unit/test_unknown.py",
            '"""TEST-UNKNOWN-998: undocumented focused suite."""\n',
        )

        result, _, stderr = self.run_validator()

        self.assertEqual(result, 1)
        self.assertIn("undefined focused test ID: TEST-UNKNOWN-998", stderr)

    def test_telemetry_dependencies_are_rejected_from_manifests_and_locks(self) -> None:
        cases = (
            (
                "apps/web/package.json",
                json.dumps(
                    {
                        "name": "@portatlas/web",
                        "private": True,
                        "dependencies": {"posthog-js": "1.0.0"},
                    }
                ),
                "posthog",
            ),
            ("uv.lock", 'name = "sentry-sdk"\n', "sentry-sdk"),
            ("pnpm-lock.yaml", "  '@sentry/core@1.0.0': {}\n", "@sentry/"),
        )
        for relative, content, dependency in cases:
            with self.subTest(relative=relative):
                path = self.root / relative
                original = path.read_text(encoding="utf-8")
                path.write_text(content, encoding="utf-8")
                try:
                    result, _, stderr = self.run_validator("--security-only")
                finally:
                    path.write_text(original, encoding="utf-8")

                self.assertEqual(result, 1)
                self.assertIn(f"telemetry dependency is forbidden: {dependency}", stderr)

    def test_all_workflows_reject_unpinned_remote_actions(self) -> None:
        self.repository.write(
            ".github/workflows/secondary.yaml",
            """\
name: Secondary
on: push
permissions:
  contents: read
jobs:
  checks:
    runs-on: ubuntu-24.04
    steps:
      - uses: actions/cache@v4
""",
        )

        result, _, stderr = self.run_validator()

        self.assertEqual(result, 1)
        self.assertIn("secondary.yaml contains an action reference that is not SHA-pinned", stderr)

    def test_workflow_service_images_require_sha256_digests(self) -> None:
        self.repository.write(
            ".github/workflows/secondary.yaml",
            f"""\
name: Secondary
on: push
permissions:
  contents: read
jobs:
  checks:
    runs-on: ubuntu-24.04
    services:
      database:
        image: postgres:18-alpine
    steps:
      - uses: actions/checkout@{PINNED_SHA}
""",
        )

        result, _, stderr = self.run_validator()

        self.assertEqual(result, 1)
        self.assertIn("service image is not digest-pinned", stderr)

    def test_workflow_parser_ignores_comments_and_allows_local_actions(self) -> None:
        self.repository.write(
            ".github/workflows/secondary.yaml",
            """\
name: Secondary
on: push
permissions:
  contents: read
jobs:
  checks:
    runs-on: ubuntu-24.04
    steps:
      # Documentation example: uses: actions/cache@v4
      - uses: ./.github/actions/foundation-check
""",
        )

        result, _, stderr = self.run_validator()

        self.assertEqual(result, 0, stderr)

    def test_pull_request_dco_check_uses_the_authored_head_not_merge_commit(self) -> None:
        self.repository.write(
            ".github/workflows/ci.yml",
            f"""\
name: Foundation
on: [push, pull_request]
permissions:
  contents: read
jobs:
  provenance:
    runs-on: ubuntu-24.04
    steps:
      - uses: actions/checkout@{PINNED_SHA}
        with:
          fetch-depth: 0
      - run: python3 scripts/check_dco.py --range baseline..HEAD
""",
        )

        result, _, stderr = self.run_validator()

        self.assertEqual(result, 1)
        self.assertIn("pull-request DCO check must inspect the authored head", stderr)

    def test_job_level_workflow_permissions_cannot_override_read_only_policy(self) -> None:
        self.repository.write(
            ".github/workflows/ci.yml",
            f"""\
name: Foundation
on: push
permissions:
  contents: read
jobs:
  checks:
    permissions:
      issues: write
    runs-on: ubuntu-24.04
    steps:
      - uses: actions/checkout@{PINNED_SHA}
""",
        )

        result, _, stderr = self.run_validator()

        self.assertEqual(result, 1)
        self.assertIn("grants write permission", stderr)


if __name__ == "__main__":
    unittest.main()
