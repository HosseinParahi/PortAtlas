"""Shared principals and explicit least-privilege scopes."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from portatlas.domain.errors import ErrorCode, SafeError
from portatlas.domain.identity import OpaqueId, ResourceKind


class Scope(StrEnum):
    STATUS_READ = "status:read"
    INVENTORY_READ = "inventory:read"
    PROJECTS_READ = "projects:read"
    PROJECTS_WRITE = "projects:write"
    CONFLICTS_READ = "conflicts:read"
    RESERVATIONS_WRITE = "reservations:write"
    LEASES_WRITE = "leases:write"
    POLICIES_READ = "policies:read"
    POLICIES_WRITE = "policies:write"
    INTEGRATIONS_MANAGE = "integrations:manage"
    CONFIGURATION_MANAGE = "configuration:manage"
    AI_USE = "ai:use"


@dataclass(frozen=True, slots=True)
class Principal:
    principal_id: OpaqueId
    scopes: frozenset[Scope]
    integration_client_id: OpaqueId | None = None

    def __post_init__(self) -> None:
        if self.principal_id.kind is not ResourceKind.PRINCIPAL:
            raise ValueError("Principal requires a principal identifier.")
        if not isinstance(self.scopes, frozenset) or not all(
            isinstance(scope, Scope) for scope in self.scopes
        ):
            raise ValueError("Principal scopes must be an immutable set of known scopes.")


def require_scopes(principal: Principal, *required: Scope) -> None:
    missing = sorted(scope.value for scope in required if scope not in principal.scopes)
    if missing:
        raise SafeError(
            ErrorCode.AUTHORIZATION_DENIED,
            "The caller is not authorized for this operation.",
            details={"required_scopes": missing},
        )
