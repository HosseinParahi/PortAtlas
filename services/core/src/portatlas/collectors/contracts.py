"""Fixture-testable collector contracts with explicit degradation."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from typing import Protocol

from portatlas.application.cancellation import CancellationToken
from portatlas.domain.clock import require_utc
from portatlas.domain.errors import ErrorCode

_MAX_OBSERVATIONS = 1_000_000


class CollectionCompleteness(StrEnum):
    COMPLETE = "complete"
    PARTIAL = "partial"
    FAILED = "failed"


@dataclass(frozen=True, slots=True)
class CollectionRequest:
    source: str
    deadline: datetime
    observation_limit: int = 100_000

    def __post_init__(self) -> None:
        require_utc(self.deadline)
        if not self.source or not 1 <= self.observation_limit <= _MAX_OBSERVATIONS:
            raise ValueError("Collection request is outside its resource budget.")


@dataclass(frozen=True, slots=True)
class CollectionResult:
    source: str
    completeness: CollectionCompleteness
    observations: tuple[object, ...]
    limitations: tuple[str, ...] = ()
    safe_error_code: ErrorCode | None = None


class RuntimeCollector(Protocol):
    async def collect(
        self,
        request: CollectionRequest,
        cancellation: CancellationToken,
    ) -> CollectionResult: ...


class HostCollector(RuntimeCollector, Protocol):
    """Host-socket collector seam; no platform implementation at Gate 3."""


class DockerCollector(RuntimeCollector, Protocol):
    """Docker evidence collector seam; no Engine implementation at Gate 3."""
