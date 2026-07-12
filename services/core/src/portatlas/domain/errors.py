"""Stable, secret-resistant errors shared by every transport adapter."""

from __future__ import annotations

import re
from collections.abc import Mapping, Sequence
from enum import StrEnum
from math import isfinite
from types import MappingProxyType

from portatlas.domain.identity import OpaqueId, ResourceKind


class ErrorCode(StrEnum):
    REQUEST_INVALID = "REQUEST_INVALID"
    REQUEST_TOO_LARGE = "REQUEST_TOO_LARGE"
    CURSOR_INVALID = "CURSOR_INVALID"
    CURSOR_EXPIRED = "CURSOR_EXPIRED"
    IDEMPOTENCY_KEY_REQUIRED = "IDEMPOTENCY_KEY_REQUIRED"
    IDEMPOTENCY_KEY_REUSED = "IDEMPOTENCY_KEY_REUSED"
    RESOURCE_REVISION_CONFLICT = "RESOURCE_REVISION_CONFLICT"
    AUTHENTICATION_REQUIRED = "AUTHENTICATION_REQUIRED"
    AUTHENTICATION_INVALID = "AUTHENTICATION_INVALID"
    AUTHORIZATION_DENIED = "AUTHORIZATION_DENIED"
    ORIGIN_DENIED = "ORIGIN_DENIED"
    HOST_DENIED = "HOST_DENIED"
    CSRF_VALIDATION_FAILED = "CSRF_VALIDATION_FAILED"
    ROOT_SCOPE_DENIED = "ROOT_SCOPE_DENIED"
    SYMLINK_SCOPE_DENIED = "SYMLINK_SCOPE_DENIED"
    RESOURCE_NOT_FOUND = "RESOURCE_NOT_FOUND"
    RESOURCE_STATE_INVALID = "RESOURCE_STATE_INVALID"
    PROJECT_INSTANCE_AMBIGUOUS = "PROJECT_INSTANCE_AMBIGUOUS"
    PROJECT_INSTANCE_INACCESSIBLE = "PROJECT_INSTANCE_INACCESSIBLE"
    MANIFEST_INVALID = "MANIFEST_INVALID"
    POLICY_INVALID = "POLICY_INVALID"
    POLICY_VIOLATION = "POLICY_VIOLATION"
    PORT_ALREADY_ALLOCATED = "PORT_ALREADY_ALLOCATED"
    PORT_OBSERVED_IN_USE = "PORT_OBSERVED_IN_USE"
    PORT_AVAILABILITY_UNCERTAIN = "PORT_AVAILABILITY_UNCERTAIN"
    ALLOCATION_RANGE_EXHAUSTED = "ALLOCATION_RANGE_EXHAUSTED"
    LEASE_EXPIRED = "LEASE_EXPIRED"
    LEASE_RENEWAL_DENIED = "LEASE_RENEWAL_DENIED"
    CONFLICT_NOT_ACTIONABLE = "CONFLICT_NOT_ACTIONABLE"
    UNMANAGED_RACE_DETECTED = "UNMANAGED_RACE_DETECTED"
    COLLECTOR_UNAVAILABLE = "COLLECTOR_UNAVAILABLE"
    COLLECTOR_PERMISSION_LIMITED = "COLLECTOR_PERMISSION_LIMITED"
    COLLECTOR_TIMEOUT = "COLLECTOR_TIMEOUT"
    COLLECTOR_OUTPUT_LIMIT = "COLLECTOR_OUTPUT_LIMIT"
    COLLECTOR_PARSE_FAILED = "COLLECTOR_PARSE_FAILED"
    SCAN_CANCELLED = "SCAN_CANCELLED"
    SCAN_BUDGET_EXCEEDED = "SCAN_BUDGET_EXCEEDED"
    SCAN_FILE_UNSUPPORTED = "SCAN_FILE_UNSUPPORTED"
    SCAN_FILE_INVALID = "SCAN_FILE_INVALID"
    SCAN_SECURITY_REJECTED = "SCAN_SECURITY_REJECTED"
    PERSISTENCE_BUSY = "PERSISTENCE_BUSY"
    PERSISTENCE_UNAVAILABLE = "PERSISTENCE_UNAVAILABLE"
    PERSISTENCE_INTEGRITY_ERROR = "PERSISTENCE_INTEGRITY_ERROR"
    MIGRATION_REQUIRED = "MIGRATION_REQUIRED"
    MIGRATION_FAILED = "MIGRATION_FAILED"
    CONFIGURATION_INVALID = "CONFIGURATION_INVALID"
    SECRET_STORE_UNAVAILABLE = "SECRET_STORE_UNAVAILABLE"  # noqa: S105
    MCP_PROTOCOL_UNSUPPORTED = "MCP_PROTOCOL_UNSUPPORTED"
    MCP_CAPABILITY_UNSUPPORTED = "MCP_CAPABILITY_UNSUPPORTED"
    INTEGRATION_DISABLED = "INTEGRATION_DISABLED"
    INTEGRATION_SCOPE_DENIED = "INTEGRATION_SCOPE_DENIED"
    TOOL_ARGUMENT_INVALID = "TOOL_ARGUMENT_INVALID"
    OPERATION_CANCELLED = "OPERATION_CANCELLED"
    AI_DISABLED = "AI_DISABLED"
    AI_PROVIDER_UNAVAILABLE = "AI_PROVIDER_UNAVAILABLE"
    AI_MODEL_NOT_FOUND = "AI_MODEL_NOT_FOUND"
    AI_CAPABILITY_UNSUPPORTED = "AI_CAPABILITY_UNSUPPORTED"
    AI_TIMEOUT = "AI_TIMEOUT"
    AI_CANCELLED = "AI_CANCELLED"
    AI_CONTEXT_REJECTED = "AI_CONTEXT_REJECTED"
    AI_OUTPUT_INVALID = "AI_OUTPUT_INVALID"
    AI_EVIDENCE_INVALID = "AI_EVIDENCE_INVALID"
    AI_TOOL_REQUEST_DENIED = "AI_TOOL_REQUEST_DENIED"
    AI_CIRCUIT_OPEN = "AI_CIRCUIT_OPEN"
    INTERNAL_ERROR = "INTERNAL_ERROR"


_RETRYABLE_CODES = frozenset(
    {
        ErrorCode.CURSOR_EXPIRED,
        ErrorCode.RESOURCE_REVISION_CONFLICT,
        ErrorCode.PORT_AVAILABILITY_UNCERTAIN,
        ErrorCode.UNMANAGED_RACE_DETECTED,
        ErrorCode.COLLECTOR_TIMEOUT,
        ErrorCode.PERSISTENCE_BUSY,
        ErrorCode.AI_TIMEOUT,
        ErrorCode.AI_CIRCUIT_OPEN,
    }
)


type SafeScalar = str | int | float | bool | None
type SafeValue = SafeScalar | Sequence[SafeValue] | Mapping[str, SafeValue]
type FrozenSafeValue = SafeScalar | tuple[FrozenSafeValue, ...] | Mapping[str, FrozenSafeValue]

_SAFE_KEY = re.compile(r"^[a-z][a-z0-9_]{0,63}$")
_MAX_DETAIL_DEPTH = 5
_MAX_SAFE_TEXT = 512
_MAX_DETAIL_MEMBERS = 32
_FORBIDDEN_KEY_PARTS = (
    "authorization",
    "bearer",
    "cookie",
    "credential",
    "password",
    "private_key",
    "secret",
    "token",
)
_FORBIDDEN_VALUE_PATTERNS = (
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bgithub_pat_[A-Za-z0-9_]{40,}\b"),
    re.compile(r"\bsk-[A-Za-z0-9_-]{24,}\b"),
    re.compile(r"\bBearer\s+\S+", re.IGNORECASE),
    re.compile(r"\b(?:https?|postgres(?:ql)?|mysql)://[^\s/:]+:[^\s/@]+@", re.IGNORECASE),
)


def freeze_safe_value(  # noqa: PLR0912
    value: SafeValue,
    *,
    depth: int = 0,
) -> FrozenSafeValue:
    """Validate and recursively snapshot one outward-safe JSON value."""
    if depth > _MAX_DETAIL_DEPTH:
        raise ValueError("Safe detail nesting exceeds the supported limit.")
    if value is None or isinstance(value, bool | int):
        return value
    if isinstance(value, float):
        if not isfinite(value):
            raise ValueError("Safe numeric values must be finite.")
        return value
    if isinstance(value, str):
        if len(value) > _MAX_SAFE_TEXT or "\n" in value or "\r" in value or "\x00" in value:
            raise ValueError("Safe text must be bounded and single-line.")
        if any(pattern.search(value) for pattern in _FORBIDDEN_VALUE_PATTERNS):
            raise ValueError("Secret-shaped outward text is forbidden.")
        return value
    if isinstance(value, list | tuple):
        if len(value) > _MAX_DETAIL_MEMBERS:
            raise ValueError("Safe detail arrays are bounded.")
        return tuple(freeze_safe_value(member, depth=depth + 1) for member in value)
    if isinstance(value, Mapping):
        if len(value) > _MAX_DETAIL_MEMBERS:
            raise ValueError("Safe detail objects are bounded.")
        frozen: dict[str, FrozenSafeValue] = {}
        for key, member in value.items():
            if not isinstance(key, str) or not _SAFE_KEY.fullmatch(key):
                raise ValueError("Safe detail keys use lowercase snake case.")
            if any(part in key for part in _FORBIDDEN_KEY_PARTS):
                raise ValueError("Secret-bearing detail fields are forbidden.")
            frozen[key] = freeze_safe_value(member, depth=depth + 1)
        return MappingProxyType(frozen)
    raise ValueError("Safe details contain an unsupported value type.")


def validate_safe_value(value: SafeValue, *, depth: int = 0) -> None:
    freeze_safe_value(value, depth=depth)


def safe_value_as_json(value: FrozenSafeValue) -> object:
    """Return a detached JSON-compatible representation of a frozen safe value."""
    if isinstance(value, Mapping):
        return {key: safe_value_as_json(member) for key, member in value.items()}
    if isinstance(value, tuple):
        return [safe_value_as_json(member) for member in value]
    return value


class SafeError(Exception):
    """An expected error whose public representation is deliberately bounded."""

    def __init__(
        self,
        code: ErrorCode,
        message: str,
        *,
        details: Mapping[str, SafeValue] | None = None,
    ) -> None:
        frozen_message = freeze_safe_value(message)
        if not isinstance(frozen_message, str):
            raise TypeError("Safe error messages must be text.")
        frozen_details = freeze_safe_value(dict(details or {}))
        if not isinstance(frozen_details, Mapping):
            raise TypeError("Safe error details must be a mapping.")
        self.code = code
        self.message = frozen_message
        self.details: Mapping[str, FrozenSafeValue] = frozen_details
        super().__init__(frozen_message)

    @property
    def retryable(self) -> bool:
        return self.code in _RETRYABLE_CODES

    def as_dict(self, *, request_id: str) -> dict[str, object]:
        OpaqueId.parse(request_id, expected_kind=ResourceKind.REQUEST)
        return {
            "code": self.code.value,
            "message": self.message,
            "retryable": self.retryable,
            "request_id": request_id,
            "details": safe_value_as_json(self.details),
        }
