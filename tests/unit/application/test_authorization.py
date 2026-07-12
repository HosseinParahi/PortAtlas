"""SEC-T-AUTH-001: shared application authorization contract."""

from __future__ import annotations

import unittest

from portatlas.application.authorization import Principal, Scope, require_scopes
from portatlas.domain.errors import ErrorCode, SafeError
from portatlas.domain.identity import OpaqueId


class AuthorizationTests(unittest.TestCase):
    def test_principal_must_hold_every_required_scope(self) -> None:
        principal = Principal(
            principal_id=OpaqueId.parse("pri_00000000-0000-4000-8000-000000000001"),
            scopes=frozenset({Scope.INVENTORY_READ, Scope.PROJECTS_READ}),
        )

        require_scopes(principal, Scope.INVENTORY_READ, Scope.PROJECTS_READ)

    def test_missing_scope_fails_with_safe_authorization_error(self) -> None:
        principal = Principal(
            principal_id=OpaqueId.parse("pri_00000000-0000-4000-8000-000000000001"),
            scopes=frozenset({Scope.INVENTORY_READ}),
        )

        with self.assertRaises(SafeError) as raised:
            require_scopes(principal, Scope.RESERVATIONS_WRITE)

        self.assertEqual(raised.exception.code, ErrorCode.AUTHORIZATION_DENIED)
        self.assertNotIn("inventory:read", str(raised.exception))

    def test_there_is_no_arbitrary_execution_scope(self) -> None:
        scope_values = {scope.value for scope in Scope}

        self.assertNotIn("*", scope_values)
        self.assertFalse(any("shell" in value or "execute" in value for value in scope_values))


if __name__ == "__main__":
    unittest.main()
