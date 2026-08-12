"""Unbounded, category-aware architecture identifiers."""

from __future__ import annotations

import re
from dataclasses import dataclass

_IDENTIFIER_RE = re.compile(r"^(?P<prefix>[MPGAKS])(?P<number>0[0-9]|[1-9][0-9]+)$")
_ALLOWED_PREFIXES = frozenset("MPGAKS")


@dataclass(frozen=True, order=True, slots=True)
class ArchitectureIdentifier:
    """Parsed permanent architecture identity."""

    prefix: str
    number: int

    def __post_init__(self) -> None:
        if self.prefix not in _ALLOWED_PREFIXES:
            raise ValueError(f"unsupported architecture category: {self.prefix!r}")
        if self.number < 0:
            raise ValueError("identifier number cannot be negative")

    def __str__(self) -> str:
        return f"{self.prefix}{self.number:02d}"


def parse_identifier(value: str) -> ArchitectureIdentifier:
    """Parse an identifier without imposing an upper bound."""

    match = _IDENTIFIER_RE.fullmatch(value)
    if match is None:
        raise ValueError(f"invalid architecture identifier: {value!r}")
    return ArchitectureIdentifier(match.group("prefix"), int(match.group("number")))


def next_identifier(prefix: str, allocated: list[str] | tuple[str, ...] | set[str]) -> str:
    """Return the next monotonically allocated identifier for *prefix*."""

    if prefix not in _ALLOWED_PREFIXES:
        raise ValueError(f"unsupported architecture category: {prefix!r}")
    numbers = [parse_identifier(value).number for value in allocated if value.startswith(prefix)]
    return str(ArchitectureIdentifier(prefix, max(numbers, default=-1) + 1))
