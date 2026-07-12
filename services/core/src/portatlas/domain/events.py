"""Schema-versioned domain events suitable for an outbox and SSE hints."""

from __future__ import annotations

import re
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from datetime import datetime
from typing import cast

from portatlas.domain.clock import Clock, SystemClock, require_utc
from portatlas.domain.errors import (
    FrozenSafeValue,
    SafeValue,
    freeze_safe_value,
    safe_value_as_json,
)
from portatlas.domain.identity import OpaqueId, ResourceKind
from portatlas.domain.revision import Revision

_EVENT_TYPE = re.compile(r"^[a-z][a-z0-9]*(?:\.[a-z][a-z0-9_]*)+$")
IdFactory = Callable[[ResourceKind], OpaqueId]


@dataclass(frozen=True, slots=True)
class ResourceReference:
    resource_type: str
    resource_id: OpaqueId
    revision: Revision

    def __post_init__(self) -> None:
        if not re.fullmatch(r"[a-z][a-z0-9_]{0,63}", self.resource_type):
            raise ValueError("Event resource type has an unsafe shape.")


@dataclass(frozen=True, slots=True)
class DomainEvent:
    event_id: OpaqueId
    event_type: str
    timestamp: datetime
    resource: ResourceReference
    payload: Mapping[str, SafeValue]
    schema_version: int = 1

    def __post_init__(self) -> None:
        if self.event_id.kind is not ResourceKind.EVENT:
            raise ValueError("A domain event requires an event identifier.")
        if not _EVENT_TYPE.fullmatch(self.event_type):
            raise ValueError("Event type must be a stable dotted identifier.")
        require_utc(self.timestamp)
        if self.schema_version != 1:
            raise ValueError("Unsupported domain event schema version.")
        frozen_payload = freeze_safe_value(dict(self.payload))
        if not isinstance(frozen_payload, Mapping):
            raise TypeError("Event payload must be a mapping.")
        object.__setattr__(self, "payload", frozen_payload)

    @classmethod
    def create(
        cls,
        *,
        event_type: str,
        resource: ResourceReference,
        payload: Mapping[str, SafeValue],
        clock: Clock | None = None,
        id_factory: IdFactory = OpaqueId.new,
    ) -> DomainEvent:
        active_clock = clock or SystemClock()
        return cls(
            event_id=id_factory(ResourceKind.EVENT),
            event_type=event_type,
            timestamp=active_clock.now(),
            resource=resource,
            payload=payload,
        )

    def as_dict(self) -> dict[str, object]:
        timestamp = require_utc(self.timestamp).isoformat().replace("+00:00", "Z")
        return {
            "id": str(self.event_id),
            "type": self.event_type,
            "timestamp": timestamp,
            "schema_version": self.schema_version,
            "resource": {
                "type": self.resource.resource_type,
                "id": str(self.resource.resource_id),
                "revision": self.resource.revision.value,
            },
            "payload": safe_value_as_json(cast(FrozenSafeValue, self.payload)),
        }
