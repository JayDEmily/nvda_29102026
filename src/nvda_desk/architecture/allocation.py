"""Post-reset implementation allocation history and candidate resolution."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml

from .identifiers import next_identifier, parse_identifier
from .registry import ArchitectureRegistry
from .schema import validate_document


@dataclass(frozen=True, slots=True)
class ImplementationAllocation:
    """One durably consumed post-reset implementation identity."""

    object_id: str
    name: str
    implemented_on: str


def load_implementation_allocations(repository_root: Path) -> tuple[ImplementationAllocation, ...]:
    """Load and validate the minimal post-reset implementation allocation history."""

    config_path = repository_root / "config" / "architecture" / "implementation_allocations.yaml"
    schema_path = repository_root / "schemas" / "implementation_allocation.schema.json"
    validate_document(config_path, schema_path)
    document = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    allocations = tuple(
        ImplementationAllocation(
            object_id=item["object_id"],
            name=item["name"],
            implemented_on=item["implemented_on"],
        )
        for item in document["implementation_allocations"]
    )
    ids = [item.object_id for item in allocations]
    if len(ids) != len(set(ids)):
        raise ValueError("implementation allocation history contains duplicate object_id values")
    for object_id in ids:
        parse_identifier(object_id)
    return allocations


def consumed_identifiers(repository_root: Path) -> set[str]:
    """Return identities already consumed by current post-reset authority."""

    registry = ArchitectureRegistry.from_repository(repository_root)
    allocations = load_implementation_allocations(repository_root)
    return (
        {item.id for item in registry.objects}
        | set(registry.retired_ids)
        | {item.object_id for item in allocations}
    )


def resolve_candidate_identifiers(
    repository_root: Path, categories: tuple[str, ...] | list[str]
) -> tuple[str, ...]:
    """Resolve non-durable candidate IDs in request order without mutating repository state."""

    consumed = consumed_identifiers(repository_root)
    resolved: list[str] = []
    for category in categories:
        candidate = next_identifier(category, consumed)
        consumed.add(candidate)
        resolved.append(candidate)
    return tuple(resolved)
