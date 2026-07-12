"""Regression tests for the supported Gate 3 command dispatcher."""

from __future__ import annotations

import subprocess
import unittest
from contextlib import redirect_stdout
from io import StringIO
from unittest.mock import Mock, patch

from scripts import check


class VerifyToolchainsTests(unittest.TestCase):
    @patch("scripts.check.subprocess.run")
    def test_verifies_the_selected_python_interpreter(self, run_mock: Mock) -> None:
        outputs = {
            ("uv", "--version"): "uv 0.11.28 (test build)",
            (
                "uv",
                "run",
                "--no-project",
                "--python",
                check.PYTHON_VERSION,
                "python",
                "--version",
            ): f"Python {check.PYTHON_VERSION}",
            ("node", "--version"): "v24.18.0",
            ("corepack", "pnpm", "--version"): "11.10.0",
        }

        def result(command: tuple[str, ...], **_: object) -> subprocess.CompletedProcess[str]:
            return subprocess.CompletedProcess(command, 0, stdout=outputs[command], stderr="")

        run_mock.side_effect = result

        check.verify_toolchains()

        commands = [call.args[0] for call in run_mock.call_args_list]
        self.assertIn(
            (
                "uv",
                "run",
                "--no-project",
                "--python",
                check.PYTHON_VERSION,
                "python",
                "--version",
            ),
            commands,
        )

    @patch("scripts.check.uv")
    def test_uv_run_rejects_lock_drift(self, uv_mock: Mock) -> None:
        check.uv_run("pytest", "-q")

        uv_mock.assert_called_once_with(
            "run",
            "--locked",
            "--python",
            check.PYTHON_VERSION,
            "pytest",
            "-q",
        )

    @patch("scripts.check.uv_run")
    @patch("scripts.check.pnpm")
    @patch("scripts.check.uv")
    @patch("scripts.check.verify_toolchains")
    def test_bootstrap_checks_locks_and_installs_both_hooks(
        self,
        verify_mock: Mock,
        uv_mock: Mock,
        pnpm_mock: Mock,
        uv_run_mock: Mock,
    ) -> None:
        check.bootstrap()

        verify_mock.assert_called_once_with()
        self.assertIn(("lock", "--check"), [call.args for call in uv_mock.call_args_list])
        self.assertIn(
            ("sync", "--locked", "--group", "dev", "--python", check.PYTHON_VERSION),
            [call.args for call in uv_mock.call_args_list],
        )
        pnpm_mock.assert_called_once_with("install", "--frozen-lockfile")
        uv_run_mock.assert_called_once_with(
            "pre-commit",
            "install",
            "--hook-type",
            "pre-commit",
            "--hook-type",
            "commit-msg",
        )

    @patch("scripts.check.uv")
    def test_python_build_uses_the_locked_build_backend(self, uv_mock: Mock) -> None:
        check.build_python()

        self.assertEqual(
            [call.args for call in uv_mock.call_args_list],
            [
                (
                    "sync",
                    "--locked",
                    "--group",
                    "dev",
                    "--group",
                    "build",
                    "--no-install-project",
                    "--python",
                    check.PYTHON_VERSION,
                ),
                (
                    "build",
                    "--no-build-isolation",
                    "--no-sources",
                    "--python",
                    check.PYTHON_VERSION,
                ),
            ],
        )

    @patch("scripts.check.subprocess.run")
    def test_node_license_inventory_rejects_denied_licenses(self, run_mock: Mock) -> None:
        run_mock.return_value = subprocess.CompletedProcess(
            (),
            0,
            stdout='{"MIT": [{"name": "safe"}], "AGPL-3.0": [{"name": "blocked"}]}',
            stderr="",
        )

        with self.assertRaisesRegex(SystemExit, "AGPL-3.0"):
            check.pnpm_license_inventory()

    @patch("scripts.check.subprocess.run")
    def test_node_license_inventory_reports_reviewed_package_count(self, run_mock: Mock) -> None:
        run_mock.return_value = subprocess.CompletedProcess(
            (),
            0,
            stdout='{"MIT": [{"name": "one"}, {"name": "two"}], "MPL-2.0": [{"name": "three"}]}',
            stderr="",
        )
        stdout = StringIO()

        with redirect_stdout(stdout):
            check.pnpm_license_inventory()

        self.assertIn("3 packages across 2 license expressions", stdout.getvalue())


if __name__ == "__main__":
    unittest.main()
