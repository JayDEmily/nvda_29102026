"""Aggregate architecture-kernel validation."""

from __future__ import annotations

from pathlib import Path

from .dependencies import analyse_repository
from .proof import load_and_validate_proof_state
from .registry import ArchitectureRegistry


class ArchitectureValidationError(ValueError):
    pass


def _python_path_exists(repository_root: Path, dotted_path: str) -> bool:
    relative = Path(*dotted_path.split("."))
    source_path = repository_root / "src" / relative
    return source_path.with_suffix(".py").is_file() or (source_path / "__init__.py").is_file()


def _validate_active_python_visible_objects(
    repository_root: Path, registry: ArchitectureRegistry
) -> None:
    failures: list[str] = []
    for item in registry.objects:
        if item.status != "active" or item.package is None:
            continue
        if not _python_path_exists(repository_root, item.package):
            failures.append(f"{item.id} registered package does not exist: {item.package}")
        if item.public_seam is None or not _python_path_exists(repository_root, item.public_seam):
            failures.append(f"{item.id} registered public seam does not exist: {item.public_seam}")
    if failures:
        raise ArchitectureValidationError("\n".join(failures))


def validate_architecture(repository_root: Path) -> list[str]:
    registry = ArchitectureRegistry.from_repository(repository_root)
    _validate_active_python_visible_objects(repository_root, registry)
    proof = load_and_validate_proof_state(repository_root)
    violations = analyse_repository(repository_root)
    if violations:
        rendered = "\n".join(f"{item.code}: {item.message}" for item in violations)
        raise ArchitectureValidationError(rendered)
    active_runtime_modules = registry.active_runtime_modules()
    return [
        f"architecture objects: {len(registry.objects)}",
        f"active runtime modules: {len(active_runtime_modules)}",
        f"admitted test families: {len(proof.families)}",
        f"promotion sets: {len(proof.promotion_sets)}",
        "dependency/public-seam violations: 0",
    ]
