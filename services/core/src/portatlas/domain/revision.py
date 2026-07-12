"""Optimistic-concurrency revision value object."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, order=True, slots=True)
class Revision:
    value: int

    def __post_init__(self) -> None:
        if isinstance(self.value, bool) or not isinstance(self.value, int) or self.value < 1:
            raise ValueError("A revision must be an integer greater than or equal to one.")

    @classmethod
    def initial(cls) -> Revision:
        return cls(1)

    def next(self) -> Revision:
        return type(self)(self.value + 1)

    def __int__(self) -> int:
        return self.value
