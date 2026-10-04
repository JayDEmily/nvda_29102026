from __future__ import annotations

import hashlib
import shutil
import subprocess
import sys
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
    tmp_path.mkdir(parents=True, exist_ok=True)
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
        ("M02", "create"),
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
        ("create", "new_owner", "M02")
    ]


def test_target_projection_rejects_inconsistent_current_registry_state(tmp_path: Path) -> None:
    modify_missing, brief_path = _write_binding(
        tmp_path,
        b"brief\n",
        targets=[{"object_id": "M100", "action": "modify"}],
    )
    with pytest.raises(ImplementationAuthorityError, match="is not registered"):
        validate_implementation_authority(REPO_ROOT, modify_missing, brief_path)


def _copy_architecture_state(tmp_path: Path, name: str) -> Path:
    repository = tmp_path / name
    shutil.copytree(REPO_ROOT / "config", repository / "config")
    shutil.copytree(REPO_ROOT / "schemas", repository / "schemas")
    return repository


def test_create_forbids_caller_selected_numeric_identifier(tmp_path: Path) -> None:
    binding_path, brief_path = _write_binding(
        tmp_path,
        b"brief\n",
        targets=[
            {
                "action": "create",
                "category": "M",
                "name": "new_owner",
                "object_id": "M16",
            }
        ],
    )

    with pytest.raises(ImplementationAuthorityError, match="schema failure"):
        validate_implementation_authority(REPO_ROOT, binding_path, brief_path)


def test_create_requires_lawful_category_and_distinguishing_name(tmp_path: Path) -> None:
    missing_name, brief_path = _write_binding(
        tmp_path / "missing-name",
        b"brief\n",
        targets=[{"action": "create", "category": "M"}],
    )
    with pytest.raises(ImplementationAuthorityError, match="schema failure"):
        validate_implementation_authority(REPO_ROOT, missing_name, brief_path)

    invalid_category, brief_path = _write_binding(
        tmp_path / "invalid-category",
        b"brief\n",
        targets=[{"action": "create", "category": "X", "name": "new_owner"}],
    )
    with pytest.raises(ImplementationAuthorityError, match="schema failure"):
        validate_implementation_authority(REPO_ROOT, invalid_category, brief_path)


def test_multiple_same_category_creates_resolve_in_request_order(tmp_path: Path) -> None:
    binding_path, brief_path = _write_binding(
        tmp_path,
        b"brief\n",
        targets=[
            {"action": "create", "category": "M", "name": "first_owner"},
            {"action": "create", "category": "M", "name": "second_owner"},
        ],
    )

    binding = validate_implementation_authority(REPO_ROOT, binding_path, brief_path)

    assert [(item.name, item.object_id) for item in binding.targets] == [
        ("first_owner", "M02"),
        ("second_owner", "M03"),
    ]


def test_create_resolution_honours_current_retired_and_durable_state(tmp_path: Path) -> None:
    repository = _copy_architecture_state(tmp_path, "state")

    modules_path = repository / "config/architecture/modules.yaml"
    modules = yaml.safe_load(modules_path.read_text(encoding="utf-8"))
    modules["retired_ids"] = ["M02"]
    modules_path.write_text(yaml.safe_dump(modules, sort_keys=False), encoding="utf-8")

    allocations_path = repository / "config/architecture/implementation_allocations.yaml"
    allocations_path.write_text(
        yaml.safe_dump(
            {
                "schema_version": "1.0",
                "implementation_allocations": [
                    {
                        "object_id": "M03",
                        "name": "already_implemented",
                        "implemented_on": "2026-09-10",
                    }
                ],
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )

    m_binding, m_brief = _write_binding(
        tmp_path / "m-binding",
        b"brief\n",
        targets=[{"action": "create", "category": "M", "name": "next_module"}],
    )
    a_binding, a_brief = _write_binding(
        tmp_path / "a-binding",
        b"brief\n",
        targets=[{"action": "create", "category": "A", "name": "second_shell"}],
    )

    m_result = validate_implementation_authority(repository, m_binding, m_brief)
    a_result = validate_implementation_authority(repository, a_binding, a_brief)
    assert m_result.targets[0].object_id == "M04"
    assert a_result.targets[0].object_id == "A01"


def test_modify_requires_existing_current_object_and_forbids_create_fields(tmp_path: Path) -> None:
    existing, brief_path = _write_binding(
        tmp_path / "existing",
        b"brief\n",
        targets=[{"action": "modify", "object_id": "A00"}],
    )
    binding = validate_implementation_authority(REPO_ROOT, existing, brief_path)
    assert [(item.action, item.object_id) for item in binding.targets] == [("modify", "A00")]

    masquerading, brief_path = _write_binding(
        tmp_path / "masquerading",
        b"brief\n",
        targets=[
            {
                "action": "modify",
                "object_id": "A00",
                "category": "A",
                "name": "application_shell",
            }
        ],
    )
    with pytest.raises(ImplementationAuthorityError, match="schema failure"):
        validate_implementation_authority(REPO_ROOT, masquerading, brief_path)


def test_missing_external_acceptance_record_fails_closed(tmp_path: Path) -> None:
    binding_path, brief_path = _write_binding(tmp_path, b"brief\n")
    document = yaml.safe_load(binding_path.read_text(encoding="utf-8"))
    del document["acceptance"]
    binding_path.write_text(yaml.safe_dump(document, sort_keys=False), encoding="utf-8")

    with pytest.raises(ImplementationAuthorityError, match="schema failure"):
        validate_implementation_authority(REPO_ROOT, binding_path, brief_path)


def test_rehearsal_is_non_mutating_and_candidate_resolution_is_non_durable(tmp_path: Path) -> None:
    watched = [
        REPO_ROOT / "config/architecture/modules.yaml",
        REPO_ROOT / "config/architecture/surfaces.yaml",
        REPO_ROOT / "config/architecture/implementation_allocations.yaml",
    ]
    before = {path: path.read_bytes() for path in watched}
    binding_path, brief_path = _write_binding(
        tmp_path,
        b"brief\n",
        targets=[
            {"action": "create", "category": "M", "name": "new_owner"},
            {"action": "modify", "object_id": "A00"},
        ],
    )

    first = validate_implementation_authority(REPO_ROOT, binding_path, brief_path)
    second = validate_implementation_authority(REPO_ROOT, binding_path, brief_path)

    assert [item.object_id for item in first.targets] == ["M02", "A00"]
    assert [item.object_id for item in second.targets] == ["M02", "A00"]
    assert {path: path.read_bytes() for path in watched} == before


def test_repository_binding_template_matches_executable_contract(tmp_path: Path) -> None:
    brief = b"brief\n"
    brief_path = tmp_path / "brief.md"
    brief_path.write_bytes(brief)
    rendered = (
        (REPO_ROOT / "templates/implementation_authority/binding.yaml.template")
        .read_text(encoding="utf-8")
        .replace("{{brief_sha256}}", hashlib.sha256(brief).hexdigest())
        .replace("{{acceptance_ref}}", "human-acceptance:template-test")
        .replace("{{category}}", "M")
        .replace("{{responsibility_name}}", "template_owner")
        .replace("{{existing_object_id}}", "A00")
    )
    binding_path = tmp_path / "binding.yaml"
    binding_path.write_text(rendered, encoding="utf-8")

    binding = validate_implementation_authority(REPO_ROOT, binding_path, brief_path)

    assert [(item.action, item.name, item.object_id) for item in binding.targets] == [
        ("create", "template_owner", "M02"),
        ("modify", None, "A00"),
    ]


def test_repository_ingress_command_reports_non_durable_named_candidate(tmp_path: Path) -> None:
    binding_path, brief_path = _write_binding(
        tmp_path,
        b"brief\n",
        targets=[
            {"action": "create", "category": "M", "name": "new_owner"},
            {"action": "modify", "object_id": "A00"},
        ],
    )

    result = subprocess.run(
        [
            sys.executable,
            str(REPO_ROOT / "tools/validate_implementation_authority.py"),
            "--binding",
            str(binding_path),
            "--brief",
            str(brief_path),
        ],
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert "candidate_targets: create:new_owner->M02, modify:A00" in result.stdout
