"""Declarative architecture registry and structural validation."""

from .identifiers import ArchitectureIdentifier, next_identifier, parse_identifier
from .registry import ArchitectureObject, ArchitectureRegistry

__all__ = [
    "ArchitectureIdentifier",
    "ArchitectureObject",
    "ArchitectureRegistry",
    "next_identifier",
    "parse_identifier",
]
