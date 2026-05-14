from __future__ import annotations

import json
from pathlib import Path

import pytest

from nvda_desk.schemas.vocabulary import VocabularyDocument, VocabularyEntry


def _entry() -> VocabularyEntry:
    return VocabularyEntry(
        canonical_slug="json_helper_contract",
        canonical_label="JSON Helper Contract",
        category="workflow",
        stage_owner="vocabulary_governance",
        maps_to_contract="VocabularyDocument.json_helpers",
        allowed_aliases=["json helper boundary"],
    )


def _payload() -> dict:
    return VocabularyDocument(
        schema_version="v1",
        registry_version="test",
        notes=["round-trip proof fixture"],
        entries=[_entry()],
    ).to_dict()


def test_from_json_text_loads_mapping_and_delegates_to_document_validation() -> None:
    document = VocabularyDocument.from_json_text(json.dumps(_payload()))

    assert document.schema_version == "v1"
    assert document.registry_version == "test"
    assert document.entry_index["json_helper_contract"].maps_to_contract == (
        "VocabularyDocument.json_helpers"
    )


@pytest.mark.parametrize("payload", ['[]', '"not an object"', '7'])
def test_from_json_text_rejects_non_object_json(payload: str) -> None:
    with pytest.raises(ValueError, match="decode to an object"):
        VocabularyDocument.from_json_text(payload)


def test_from_json_text_rejects_invalid_document_shape() -> None:
    payload = _payload()
    payload["entries"] = "not a list"

    with pytest.raises(ValueError, match="entries must be a list"):
        VocabularyDocument.from_json_text(json.dumps(payload))


def test_from_json_path_reads_utf8_and_delegates_to_from_json_text(tmp_path: Path) -> None:
    path = tmp_path / "vocabulary.json"
    path.write_text(json.dumps(_payload()), encoding="utf-8")

    document = VocabularyDocument.from_json_path(path)

    assert document.entry_index["json_helper_contract"].canonical_label == (
        "JSON Helper Contract"
    )


def test_to_json_text_emits_round_trippable_validated_json() -> None:
    document = VocabularyDocument(
        schema_version="v1",
        registry_version="test",
        entries=[_entry()],
    )

    emitted = document.to_json_text()

    assert emitted.endswith("\n")
    reparsed = VocabularyDocument.from_json_text(emitted)
    assert reparsed.to_dict() == document.to_dict()


def test_to_json_text_does_not_mutate_committed_canonical_vocabulary() -> None:
    path = Path("data/vocabulary/canonical_vocabulary.json")
    before = path.read_text(encoding="utf-8")

    VocabularyDocument(schema_version="v1", registry_version="test").to_json_text()

    assert path.read_text(encoding="utf-8") == before
