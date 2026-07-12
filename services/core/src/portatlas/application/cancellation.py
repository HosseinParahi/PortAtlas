"""Transport-neutral cancellation contract owned by the application layer."""

from __future__ import annotations

from typing import Protocol


class CancellationToken(Protocol):
    @property
    def cancelled(self) -> bool: ...
