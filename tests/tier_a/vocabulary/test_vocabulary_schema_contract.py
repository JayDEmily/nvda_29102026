from __future__ import annotations

import importlib
from dataclasses import is_dataclass

import pytest


def _require_module(module_path: str):
    try:
        return importlib.import_module(module_path)
    except ModuleNotFoundError as exc:
        pytest.fail(f"Required module is not implemented: {module_path} ({exc})")


def _require_attr(module, attr_name: str):
    if not hasattr(module, attr_name):
        pytest.fail(f"Required attribute is not implemented: {module.__name__}.{attr_name}")
    return getattr(module, attr_name)


def test_vocabulary_schema_contract_surfaces_are_present() -> None:
    schema_module = _require_module("nvda_desk.schemas.vocabulary")
    assert schema_module.__name__ == "nvda_desk.schemas.vocabulary"

    vocabulary_entry = _require_attr(schema_module, "VocabularyEntry")
    assert vocabulary_entry is getattr(schema_module, "VocabularyEntry")
    vocabulary_document = _require_attr(schema_module, "VocabularyDocument")
    assert vocabulary_document is getattr(schema_module, "VocabularyDocument")
    assert _require_attr(schema_module, "vocabulary_document_from_dict") is getattr(
        schema_module, "vocabulary_document_from_dict"
    )

    assert is_dataclass(vocabulary_entry)
    assert is_dataclass(vocabulary_document)
    assert vocabulary_entry.__dataclass_params__.frozen is True
    assert vocabulary_document.__dataclass_params__.frozen is True


def test_vocabulary_schema_contract_rejects_duplicate_slug_alias_and_disallowed_collisions() -> (
    None
):
    schema_module = _require_module("nvda_desk.schemas.vocabulary")
    assert schema_module.__name__ == "nvda_desk.schemas.vocabulary"
    vocabulary_entry = _require_attr(schema_module, "VocabularyEntry")
    assert vocabulary_entry is getattr(schema_module, "VocabularyEntry")
    vocabulary_document = _require_attr(schema_module, "VocabularyDocument")
    assert vocabulary_document is getattr(schema_module, "VocabularyDocument")

    duplicate_slug_document = vocabulary_document(
        schema_version="v1",
        registry_version="test",
        entries=[
            vocabulary_entry("alpha", "Alpha", "stage", "owner", "ContractA"),
            vocabulary_entry("alpha", "Beta", "stage", "owner", "ContractB"),
        ],
    )
    with pytest.raises(ValueError, match="canonical_slug"):
        duplicate_slug_document.to_dict()

    alias_collision_document = vocabulary_document(
        schema_version="v1",
        registry_version="test",
        entries=[
            vocabulary_entry(
                "alpha",
                "Alpha",
                "stage",
                "owner",
                "ContractA",
                allowed_aliases=["shared alias"],
            ),
            vocabulary_entry(
                "beta",
                "Beta",
                "stage",
                "owner",
                "ContractB",
                allowed_aliases=["shared alias"],
            ),
        ],
    )
    with pytest.raises(ValueError, match="alias collision"):
        alias_collision_document.to_dict()

    disallowed_collision_document = vocabulary_document(
        schema_version="v1",
        registry_version="test",
        entries=[
            vocabulary_entry(
                "alpha",
                "Alpha",
                "stage",
                "owner",
                "ContractA",
                disallowed_phrases=["shared forbidden"],
            ),
            vocabulary_entry(
                "beta",
                "Beta",
                "stage",
                "owner",
                "ContractB",
                disallowed_phrases=["shared forbidden"],
            ),
        ],
    )
    with pytest.raises(ValueError, match="disallowed phrase collision"):
        disallowed_collision_document.to_dict()

    self_alias_entry = vocabulary_entry(
        "parallel_risk_lane",
        "Parallel Risk Lane",
        "workflow",
        "parallel_risk_lane",
        "ParallelRiskLanePacket",
        allowed_aliases=["Parallel Risk Lane"],
    )
    with pytest.raises(ValueError):
        vocabulary_document("v1", "test", entries=[self_alias_entry]).to_dict()


def test_vocabulary_schema_uses_namespaced_machine_identity_and_bounded_collisions() -> None:
    schema_module = _require_module("nvda_desk.schemas.vocabulary")
    vocabulary_entry = _require_attr(schema_module, "VocabularyEntry")
    vocabulary_namespace = _require_attr(schema_module, "VocabularyNamespace")
    vocabulary_document = _require_attr(schema_module, "VocabularyDocument")

    namespaces = {
        "global": vocabulary_namespace(
            namespace="global",
            scan_paths=["src", "tests", "docs", "config"],
            imports=[],
        ),
        "m04": vocabulary_namespace(
            namespace="m04",
            scan_paths=["src/nvda_desk/packets", "tests/tier_a/packets"],
            imports=["global"],
        ),
        "m07": vocabulary_namespace(
            namespace="m07",
            scan_paths=["src/nvda_desk/m07_coefficient_modifier_authority"],
            imports=["global"],
        ),
    }
    document = vocabulary_document(
        schema_version="v2_namespaced",
        registry_version="test",
        namespaces=namespaces,
        entries=[
            vocabulary_entry(
                "shared_local_slug",
                "Shared Local Label",
                "stage",
                "owner-m04",
                "ContractM04",
                namespace="m04",
            ),
            vocabulary_entry(
                "shared_local_slug",
                "Shared Local Label",
                "stage",
                "owner-m07",
                "ContractM07",
                namespace="m07",
            ),
        ],
    )

    payload = document.to_dict()
    assert [entry["canonical_id"] for entry in payload["entries"]] == [
        "m04.shared_local_slug",
        "m07.shared_local_slug",
    ]
    assert set(document.entry_index) == {
        "m04.shared_local_slug",
        "m07.shared_local_slug",
    }

    global_collision = vocabulary_document(
        schema_version="v2_namespaced",
        registry_version="test",
        namespaces=namespaces,
        entries=[
            vocabulary_entry(
                "shared_local_slug",
                "Shared Local Label",
                "stage",
                "global-owner",
                "GlobalContract",
                namespace="global",
            ),
            vocabulary_entry(
                "shared_local_slug",
                "Shared Local Label",
                "stage",
                "owner-m04",
                "ContractM04",
                namespace="m04",
            ),
        ],
    )
    with pytest.raises(ValueError, match="collision"):
        global_collision.to_dict()
