"""Failure-isolated optional local-AI port without a concrete provider."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from enum import StrEnum
from typing import Protocol

from portatlas.application.cancellation import CancellationToken


class ProviderState(StrEnum):
    DISABLED = "disabled"
    UNAVAILABLE = "unavailable"
    READY = "ready"
    DEGRADED = "degraded"


@dataclass(frozen=True, slots=True)
class ProviderHealth:
    state: ProviderState
    safe_reason: str | None = None


@dataclass(frozen=True, slots=True)
class StructuredCompletionRequest:
    schema_name: str
    context: Mapping[str, object]
    maximum_output_bytes: int


@dataclass(frozen=True, slots=True)
class ProviderResponse:
    structured_output: Mapping[str, object]
    model: str


class AIProvider(Protocol):
    async def health(self) -> ProviderHealth: ...

    async def list_models(self) -> list[str]: ...

    async def complete_structured(
        self,
        request: StructuredCompletionRequest,
        cancellation: CancellationToken,
    ) -> ProviderResponse: ...
