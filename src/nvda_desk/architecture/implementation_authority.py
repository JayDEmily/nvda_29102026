"""Mechanical binding of an accepted implementation-ready brief to architecture targets."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from .allocation import consumed_identifiers, resolve_candidate_identifiers
from .registry import ArchitectureRegistry
from .schema import validate_instance


class ImplementationAuthorityError(ValueError):
    """Raised when implementation-authority ingress is mechanically invalid."""


@dataclass(frozen=True, slots=True)
class ImplementationTarget:
    object_id: str
    action: str
    name: str | None = None
    category: str | None = None


@dataclass(frozen=True, slots=True)
class ImplementationAuthorityBinding:
    brief_sha256: str
    acceptance_ref: str
    targets: tuple[ImplementationTarget, ...]


def render_candidate_target(target: ImplementationTarget) -> str:
    """Render a resolved projection target without implying durable allocation."""

    if target.action == "create":
        return f"create:{target.name}->{target.object_id}"
    return f"modify:{target.object_id}"


def sha256_file(path: Path) -> str:
    """Return SHA-256 over the exact raw bytes at *path*."""

    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _load_binding_document(repository_root: Path, binding_path: Path) -> dict[str, Any]:
    try:
        document = yaml.safe_load(binding_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        raise ImplementationAuthorityError(f"cannot read implementation binding: {exc}") from exc
    if not isinstance(document, dict):
        raise ImplementationAuthorityError("implementation binding must be a mapping")

    schema_path = repository_root / "schemas" / "implementation_authority_binding.schema.json"
    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        validate_instance(document, schema)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        raise ImplementationAuthorityError(f"implementation binding schema failure: {exc}") from exc
    return document


def _resolve_target_projection(
    repository_root: Path, raw_targets: list[dict[str, str]]
) -> tuple[ImplementationTarget, ...]:
    create_categories = [item["category"] for item in raw_targets if item["action"] == "create"]
    create_ids = iter(resolve_candidate_identifiers(repository_root, create_categories))
    targets: list[ImplementationTarget] = []
    for item in raw_targets:
        if item["action"] == "create":
            targets.append(
                ImplementationTarget(
                    object_id=next(create_ids),
                    action="create",
                    name=item["name"],
                    category=item["category"],
                )
            )
        else:
            targets.append(ImplementationTarget(object_id=item["object_id"], action="modify"))
    return tuple(targets)


def _validate_target_projection(
    repository_root: Path, targets: tuple[ImplementationTarget, ...]
) -> None:
    try:
        registry = ArchitectureRegistry.from_repository(repository_root)
        consumed = consumed_identifiers(repository_root)
    except (OSError, ValueError) as exc:
        raise ImplementationAuthorityError(
            f"cannot validate target projection against architecture state: {exc}"
        ) from exc
    current_ids = {item.id for item in registry.objects}
    seen: set[str] = set()
    for target in targets:
        if target.object_id in seen:
            raise ImplementationAuthorityError(
                f"implementation binding resolves {target.object_id} more than once"
            )
        seen.add(target.object_id)
        if target.action == "create":
            if target.object_id in consumed:
                raise ImplementationAuthorityError(
                    "create target "
                    f"{target.object_id} is already consumed by current post-reset state"
                )
        elif target.action == "modify" and target.object_id not in current_ids:
            raise ImplementationAuthorityError(
                f"modify target {target.object_id} is not registered"
            )


def validate_implementation_authority(
    repository_root: Path, binding_path: Path, brief_path: Path
) -> ImplementationAuthorityBinding:
    """Validate exact brief-byte binding and current create/modify target state.

    This function establishes mechanical byte and architecture-state facts only. It
    does not establish that the external acceptance is legitimate or that the brief
    is semantically complete.
    """

    document = _load_binding_document(repository_root, binding_path)
    expected_sha256 = document["brief_sha256"]
    try:
        actual_sha256 = sha256_file(brief_path)
    except OSError as exc:
        raise ImplementationAuthorityError(f"cannot read implementation brief: {exc}") from exc
    if actual_sha256 != expected_sha256:
        raise ImplementationAuthorityError(
            "implementation brief bytes do not match the bound SHA-256"
        )

    targets = _resolve_target_projection(repository_root, document["targets"])
    _validate_target_projection(repository_root, targets)
    return ImplementationAuthorityBinding(
        brief_sha256=expected_sha256,
        acceptance_ref=document["acceptance"]["authority_ref"],
        targets=targets,
    )
