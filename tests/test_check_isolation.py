"""Regression tests for the default-path isolation proof."""

from __future__ import annotations

import contextlib
import io
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from scripts import check_isolation


class CheckIsolationTests(unittest.TestCase):
    def run_validator(self, root: Path) -> tuple[int, str]:
        stderr = io.StringIO()
        with (
            mock.patch.object(check_isolation, "ROOT", root),
            mock.patch("scripts.check_isolation.importlib.util.find_spec", return_value=None),
            contextlib.redirect_stderr(stderr),
        ):
            result = check_isolation.main()
        return result, stderr.getvalue()

    def test_rejects_optional_and_process_imports_in_core_source(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "services/core/src/portatlas/bad.py"
            source.parent.mkdir(parents=True)
            source.write_text("import docker\nimport subprocess\n", encoding="utf-8")

            result, stderr = self.run_validator(root)

        self.assertEqual(result, 1)
        self.assertIn("forbidden default-path imports", stderr)
        self.assertIn("docker", stderr)
        self.assertIn("subprocess", stderr)

    def test_rejects_rust_project_artifacts_from_the_gate3_foundation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "services/core/src/portatlas/__init__.py"
            source.parent.mkdir(parents=True)
            source.write_text("", encoding="utf-8")
            (root / "Cargo.toml").write_text("[package]\nname='unexpected'\n", encoding="utf-8")

            result, stderr = self.run_validator(root)

        self.assertEqual(result, 1)
        self.assertIn("Rust artifacts are outside Gate 3", stderr)


if __name__ == "__main__":
    unittest.main()
