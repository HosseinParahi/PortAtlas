"""Injected wall and monotonic clocks for deterministic behavior."""

from __future__ import annotations

import math
import time
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Protocol


def require_utc(value: datetime) -> datetime:
    """Return a timezone-aware UTC instant or fail closed."""

    if value.tzinfo is None or value.utcoffset() != timedelta(0):
        raise ValueError("Domain timestamps must be timezone-aware UTC instants.")
    return value.astimezone(UTC)


class Clock(Protocol):
    """Wall time is persisted; monotonic time protects in-process deadlines."""

    def now(self) -> datetime: ...

    def monotonic(self) -> float: ...


@dataclass(frozen=True, slots=True)
class SystemClock:
    def now(self) -> datetime:
        return datetime.now(UTC)

    def monotonic(self) -> float:
        return time.monotonic()


@dataclass(slots=True)
class FrozenClock:
    """A deterministic clock intended for tests and explicit simulations."""

    current: datetime
    monotonic_value: float = 0.0

    def __post_init__(self) -> None:
        self.current = require_utc(self.current)
        if not math.isfinite(self.monotonic_value) or self.monotonic_value < 0:
            raise ValueError("Monotonic time must be a finite non-negative value.")

    def now(self) -> datetime:
        return self.current

    def monotonic(self) -> float:
        return self.monotonic_value

    def advance(self, amount: timedelta) -> None:
        seconds = amount.total_seconds()
        if seconds < 0:
            raise ValueError("A test clock cannot move backwards.")
        self.current += amount
        self.monotonic_value += seconds
