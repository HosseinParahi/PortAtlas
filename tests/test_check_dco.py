"""Regression tests for the standard-library commit-message DCO hook."""

from __future__ import annotations

import contextlib
import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from scripts import check_dco


class CheckDcoTests(unittest.TestCase):
    def check_message(self, message: str) -> tuple[int, str]:
        with tempfile.TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "COMMIT_EDITMSG"
            path.write_text(message, encoding="utf-8")
            stderr = io.StringIO()
            with contextlib.redirect_stderr(stderr):
                result = check_dco.main([str(path)])
        return result, stderr.getvalue()

    def test_accepts_signed_off_by_in_the_final_trailer_block(self) -> None:
        message = (
            "test: exercise the hook\n\n"
            "Keep the body distinct from trailers.\n\n"
            "Signed-off-by: Ada Lovelace <ada@example.com>\n"
            "Co-authored-by: Grace Hopper <grace@example.com>\n"
        )

        result, stderr = self.check_message(message)

        self.assertEqual(result, 0)
        self.assertEqual(stderr, "")

    def test_accepts_trailing_commit_template_comments(self) -> None:
        message = (
            "test: exercise template cleanup\n\n"
            "Signed-off-by: Ada Lovelace <ada@example.com>\n\n"
            "# Please enter the commit message.\n"
        )

        result, stderr = self.check_message(message)

        self.assertEqual(result, 0)
        self.assertEqual(stderr, "")

    def test_rejects_signed_off_by_text_outside_the_trailer_block(self) -> None:
        message = (
            "test: reject body lookalikes\n\n"
            "Signed-off-by: Ada Lovelace <ada@example.com>\n\n"
            "This final paragraph is ordinary body text.\n"
        )

        result, stderr = self.check_message(message)

        self.assertEqual(result, 1)
        self.assertIn("requires a Signed-off-by trailer", stderr)

    def test_rejects_malformed_or_missing_sign_offs(self) -> None:
        messages = (
            "test: no sign-off\n",
            "test: blank name\n\nSigned-off-by:  <ada@example.com>\n",
            "test: missing address\n\nSigned-off-by: Ada Lovelace\n",
            "test: malformed address\n\nSigned-off-by: Ada Lovelace <ada example.com>\n",
            "test: wrong key\n\nsigned-off-by: Ada Lovelace <ada@example.com>\n",
        )
        for message in messages:
            with self.subTest(message=message.splitlines()[0]):
                result, stderr = self.check_message(message)

                self.assertEqual(result, 1)
                self.assertIn("requires a Signed-off-by trailer", stderr)

    def test_usage_and_missing_message_file_are_reported(self) -> None:
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            usage_result = check_dco.main([])
            missing_result = check_dco.main(["/does/not/exist/COMMIT_EDITMSG"])

        self.assertEqual(usage_result, 2)
        self.assertEqual(missing_result, 2)
        self.assertIn("usage: check_dco.py COMMIT_MESSAGE", stderr.getvalue())
        self.assertIn("cannot read commit message", stderr.getvalue())

    def test_committed_sign_off_can_be_required_to_match_the_author(self) -> None:
        message = "test: signed\n\nSigned-off-by: Ada Lovelace <ada@example.com>\n"

        self.assertTrue(
            check_dco.has_dco_trailer(
                message,
                expected_name="Ada Lovelace",
                expected_email="ada@example.com",
            )
        )
        self.assertFalse(
            check_dco.has_dco_trailer(
                message,
                expected_name="Grace Hopper",
                expected_email="grace@example.com",
            )
        )

    @patch("scripts.check_dco.check_commit_range", return_value=[])
    def test_range_mode_checks_committed_history(self, range_mock: Mock) -> None:
        result = check_dco.main(["--range", "baseline..HEAD"])

        self.assertEqual(result, 0)
        range_mock.assert_called_once_with("baseline..HEAD")


if __name__ == "__main__":
    unittest.main()
