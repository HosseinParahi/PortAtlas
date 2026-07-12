"""Opaque, resource-prefixed identity primitives."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from enum import StrEnum
from uuid import UUID, uuid4


class ResourceKind(StrEnum):
    """Resource kinds whose prefix is stable but whose payload is opaque."""

    PROJECT_ROOT = "prt_"
    PROJECT = "prj_"
    PROJECT_INSTANCE = "ins_"
    SERVICE = "svc_"
    OBSERVATION = "obs_"
    DECLARATION = "dec_"
    RESERVATION = "res_"
    LEASE = "lea_"
    CONFLICT = "con_"
    EVIDENCE = "evd_"
    AUDIT = "aud_"
    AI_RECORD = "air_"
    EVENT = "evt_"
    REQUEST = "req_"
    PRINCIPAL = "pri_"
    CREDENTIAL = "crd_"

    @property
    def prefix(self) -> str:
        return self.value

    @classmethod
    def from_value(cls, value: str) -> ResourceKind:
        matches = [kind for kind in cls if value.startswith(kind.prefix)]
        if len(matches) != 1:
            raise ValueError("Identifier has an unsupported resource prefix.")
        return matches[0]


UuidFactory = Callable[[], UUID]


@dataclass(frozen=True, slots=True)
class OpaqueId:
    """An immutable identifier that clients must compare, never parse."""

    kind: ResourceKind
    value: str

    def __post_init__(self) -> None:
        parsed = self._validate(self.value)
        if parsed is not self.kind:
            raise ValueError("Identifier prefix does not match its resource kind.")

    @classmethod
    def new(
        cls,
        kind: ResourceKind,
        *,
        uuid_factory: UuidFactory = uuid4,
    ) -> OpaqueId:
        return cls(kind=kind, value=f"{kind.prefix}{uuid_factory()}")

    @classmethod
    def parse(
        cls,
        value: str,
        *,
        expected_kind: ResourceKind | None = None,
    ) -> OpaqueId:
        kind = cls._validate(value)
        if expected_kind is not None and kind is not expected_kind:
            raise ValueError("Identifier has the wrong resource kind.")
        return cls(kind=kind, value=value)

    @staticmethod
    def _validate(value: str) -> ResourceKind:
        if not isinstance(value, str) or value != value.lower():
            raise ValueError("Identifier must be a lowercase string.")
        kind = ResourceKind.from_value(value)
        payload = value.removeprefix(kind.prefix)
        try:
            parsed = UUID(payload)
        except (AttributeError, ValueError) as error:
            raise ValueError("Identifier payload must be a canonical UUID.") from error
        if str(parsed) != payload:
            raise ValueError("Identifier payload must be a canonical UUID.")
        return kind

    def __str__(self) -> str:
        return self.value
