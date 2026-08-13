"""Aggregate architecture-kernel validation."""

from __future__ import annotations

from pathlib import Path

from .dependencies import analyse_repository
from .proof import load_and_validate_proof_state
from .registry import ArchitectureRegistry
from .schema import validate_document


class ArchitectureValidationError(ValueError):
    pass


def validate_architecture(repository_root: Path) -> list[str]:
    registry = ArchitectureRegistry.from_repository(repository_root)
    validate_document(
        repository_root / "config" / "vocabulary" / "vocabulary.yaml",
        repository_root / "schemas" / "vocabulary.schema.json",
    )
    proof = load_and_validate_proof_state(repository_root)
    violations = analyse_repository(repository_root)
    if violations:
        rendered = "\n".join(f"{item.code}: {item.message}" for item in violations)
        raise ArchitectureValidationError(rendered)
    if registry.active_runtime_modules():
        raise ArchitectureValidationError("runtime module registry must be empty during the reset")
    return [
        f"architecture objects: {len(registry.objects)}",
        "active runtime modules: 0",
        f"admitted test families: {len(proof.families)}",
        f"promotion sets: {len(proof.promotion_sets)}",
        "dependency/public-seam violations: 0",
    ]
