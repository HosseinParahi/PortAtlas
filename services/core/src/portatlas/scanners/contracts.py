"""Safe-source parser contracts that cannot execute project code."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import PurePosixPath
from typing import Protocol

_MAX_SOURCE_BYTES = 2_000_000


@dataclass(frozen=True, slots=True)
class ParserDescriptor:
    parser_id: str
    version: str
    supported_patterns: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class SafeSource:
    relative_path: PurePosixPath
    content: bytes
    fingerprint: str

    def __post_init__(self) -> None:
        if self.relative_path.is_absolute() or ".." in self.relative_path.parts:
            raise ValueError("Parser source must remain relative to an approved root.")
        if len(self.content) > _MAX_SOURCE_BYTES:
            raise ValueError("Parser source exceeds its per-file byte budget.")


@dataclass(frozen=True, slots=True)
class ParseContext:
    instance_id: str
    source_budget: int


@dataclass(frozen=True, slots=True)
class ParseResult:
    declarations: tuple[object, ...]
    limitations: tuple[str, ...] = ()


class ProjectParser(Protocol):
    descriptor: ParserDescriptor

    async def parse(self, source: SafeSource, context: ParseContext) -> ParseResult: ...
