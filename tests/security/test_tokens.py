"""SEC-T-AUTH-001: high-entropy token and user-only storage tests."""

from __future__ import annotations

import tempfile
import unittest
from datetime import UTC, datetime, timedelta
from pathlib import Path

from portatlas.application.authorization import Scope
from portatlas.domain.clock import FrozenClock
from portatlas.security.tokens import TokenService, write_user_only_secret


class TokenSecurityTests(unittest.TestCase):
    def setUp(self) -> None:
        self.clock = FrozenClock(datetime(2026, 7, 11, tzinfo=UTC))
        self.service = TokenService(clock=self.clock)

    def test_issue_returns_secret_once_and_record_retains_only_hash_material(self) -> None:
        issued = self.service.issue(
            scopes=frozenset({Scope.INVENTORY_READ}),
            expires_in=timedelta(hours=1),
        )

        self.assertGreaterEqual(len(issued.secret), 43)
        self.assertNotIn(issued.secret, repr(issued.record))
        self.assertTrue(self.service.verify(issued.secret, issued.record))
        self.assertFalse(self.service.verify(f"{issued.secret}x", issued.record))

    def test_expired_or_revoked_credentials_fail_closed(self) -> None:
        issued = self.service.issue(
            scopes=frozenset({Scope.INVENTORY_READ}),
            expires_in=timedelta(seconds=1),
        )
        self.clock.advance(timedelta(seconds=2))

        self.assertFalse(self.service.verify(issued.secret, issued.record))
        self.assertFalse(self.service.verify(issued.secret, issued.record.revoke(self.clock)))

    def test_secret_file_is_created_with_user_only_permissions(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bootstrap.secret"

            write_user_only_secret(path, "test-secret")

            self.assertEqual(path.read_text(encoding="utf-8"), "test-secret")
            self.assertEqual(path.stat().st_mode & 0o777, 0o600)

    def test_secret_writer_refuses_to_replace_a_symlink(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "target"
            target.write_text("preserve", encoding="utf-8")
            link = root / "bootstrap.secret"
            link.symlink_to(target)

            with self.assertRaises(ValueError):
                write_user_only_secret(link, "replacement")

            self.assertEqual(target.read_text(encoding="utf-8"), "preserve")


if __name__ == "__main__":
    unittest.main()
