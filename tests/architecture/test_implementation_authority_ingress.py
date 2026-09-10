from __future__ import annotations

import hashlib
from pathlib import Path

import pytest
import yaml

from nvda_desk.architecture.implementation_authority import (
    ImplementationAuthorityError,
    validate_implementation_authority,
)

# Proof-addressability markers only; see TEST_AND_PROMOTION_KERNEL.md.
# AK-INGRESS-001 AK-INGRESS-002 AK-INGRESS-003 AK-INGRESS-004 AK-INGRESS-005

REPO_ROOT = Path(__file__).resolve().parents[2]


def _write_binding(
    tmp_path: Path,
    brief: bytes,
    *,
    targets: list[dict[str, str]] | None = None,
    acceptance_ref: str = "human-acceptance:test",
    extras: dict | None = None,
) -> tuple[Path, Path]:
    brief_path = tmp_path / "implementation-ready-brief.md"
    brief_path.write_bytes(brief)
    document = {
        "schema_version": "1.0",
        "brief_sha256": hashlib.sha256(brief).hexdigest(),
        "acceptance": {
            "status": "ACCEPTED_FOR_IMPLEMENTATION",
            "authority_ref": acceptance_ref,
        },
        "targets": targets
        or [{"action": "create", "category": "M", "name": "example_responsibility"}],
    }
    if extras:
        document.update(extras)
    binding_path = tmp_path / "binding.yaml"
    binding_path.write_text(yaml.safe_dump(document, sort_keys=False), encoding="utf-8")
    return binding_path, brief_path


def test_exact_brief_bytes_bind_without_copying_brief(tmp_path: Path) -> None:
    binding_path, brief_path = _write_binding(
        tmp_path,
        b"Implementation-ready instructions.\n",
        targets=[
            {"action": "create", "category": "M", "name": "example_responsibility"},
            {"action": "modify", "object_id": "P01"},
        ],
    )

    binding = validate_implementation_authority(REPO_ROOT, binding_path, brief_path)

    assert binding.brief_sha256 == hashlib.sha256(brief_path.read_bytes()).hexdigest()
    assert binding.acceptance_ref == "human-acceptance:test"
    assert [(item.object_id, item.action) for item in binding.targets] == [
        ("M00", "create"),
        ("P01", "modify"),
    ]
    assert "Implementation-ready instructions" not in binding_path.read_text(encoding="utf-8")


def test_changed_brief_bytes_fail_closed(tmp_path: Path) -> None:
    binding_path, brief_path = _write_binding(tmp_path, b"original\n")
    brief_path.write_bytes(b"changed\n")

    with pytest.raises(ImplementationAuthorityError, match="do not match"):
        validate_implementation_authority(REPO_ROOT, binding_path, brief_path)


def test_binding_requires_nonempty_external_acceptance_reference(tmp_path: Path) -> None:
    binding_path, brief_path = _write_binding(tmp_path, b"brief\n", acceptance_ref="")

    with pytest.raises(ImplementationAuthorityError, match="schema failure"):
        validate_implementation_authority(REPO_ROOT, binding_path, brief_path)


def test_upstream_methodology_metadata_is_not_part_of_ingress_schema(tmp_path: Path) -> None:
    binding_path, brief_path = _write_binding(
        tmp_path,
        b"brief\n",
        extras={"methodology": "M10", "brief_text": "must not be copied here"},
    )

    with pytest.raises(ImplementationAuthorityError, match="schema failure"):
        validate_implementation_authority(REPO_ROOT, binding_path, brief_path)


def test_create_contract_resolves_identifier_without_caller_number(tmp_path: Path) -> None:
    binding_path, brief_path = _write_binding(
        tmp_path,
        b"brief\n",
        targets=[{"action": "create", "category": "M", "name": "new_owner"}],
    )

    binding = validate_implementation_authority(REPO_ROOT, binding_path, brief_path)

    assert [(item.action, item.name, item.object_id) for item in binding.targets] == [
        ("create", "new_owner", "M00")
    ]


def test_target_projection_rejects_inconsistent_current_registry_state(tmp_path: Path) -> None:
    modify_missing, brief_path = _write_binding(
        tmp_path,
        b"brief\n",
        targets=[{"object_id": "M100", "action": "modify"}],
    )
    with pytest.raises(ImplementationAuthorityError, match="is not registered"):
        validate_implementation_authority(REPO_ROOT, modify_missing, brief_path)
