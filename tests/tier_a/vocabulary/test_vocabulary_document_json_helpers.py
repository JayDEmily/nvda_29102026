from __future__ import annotations

import json
from pathlib import Path

import pytest

from nvda_desk.schemas.vocabulary import (
    RawDerivedTag,
    VocabularyCategory,
    VocabularyDocument,
    VocabularyEntry,
)


def _valid_payload() -> dict:
    return {
        "schema_version": "v1",
        "registry_version": "json-helper-test",
        "notes": ["round-trip proof only"],
        "entries": [
            {
                "canonical_slug": "json_helper_entry",
                "canonical_label": "JSON Helper Entry",
                "category": "workflow",
                "stage_owner": "vocabulary_governance",
                "maps_to_contract": "VocabularyDocument.from_json_text",
                "raw_or_derived": "derived",
                "allowed_aliases": ["json helper proof"],
                "disallowed_phrases": ["json helper drift"],
                "notes": ["keeps helper boundary bounded"],
            }
        ],
    }


def test_vocabulary_document_from_json_text_decodes_mapping_and_validates() -> None:
    document = VocabularyDocument.from_json_text(json.dumps(_valid_payload()))

    entry = document.entry_index["json_helper_entry"]
    assert entry.category is VocabularyCategory.WORKFLOW
    assert entry.raw_or_derived is RawDerivedTag.DERIVED
    assert entry.allowed_aliases == ["json helper proof"]


def test_vocabulary_document_from_json_text_rejects_non_mapping_root() -> None:
    with pytest.raises(ValueError, match="JSON root"):
        VocabularyDocument.from_json_text(json.dumps([_valid_payload()]))


def test_vocabulary_document_from_json_text_delegates_to_governed_validation() -> None:
    payload = _valid_payload()
    payload["entries"][0]["category"] = "unguarded_runtime_signal"

    with pytest.raises(ValueError, match="category is not governed"):
        VocabularyDocument.from_json_text(json.dumps(payload))


def test_vocabulary_document_from_json_path_reads_utf8_and_delegates(
    tmp_path: Path,
) -> None:
    payload_path = tmp_path / "vocabulary.json"
    payload_path.write_text(json.dumps(_valid_payload()), encoding="utf-8")

    document = VocabularyDocument.from_json_path(payload_path)

    assert document.entry_index["json_helper_entry"].canonical_label == "JSON Helper Entry"


def test_vocabulary_document_to_json_text_round_trips_without_file_mutation(
    tmp_path: Path,
) -> None:
    document = VocabularyDocument(
        schema_version="v1",
        registry_version="json-helper-test",
        notes=["proof only"],
        entries=[
            VocabularyEntry(
                canonical_slug="round_trip_entry",
                canonical_label="Round Trip Entry",
                category=VocabularyCategory.WORKFLOW,
                stage_owner="vocabulary_governance",
                maps_to_contract="VocabularyDocument.to_json_text",
                raw_or_derived=RawDerivedTag.RAW,
            )
        ],
    )
    target_path = tmp_path / "canonical_vocabulary.json"

    json_text = document.to_json_text()
    round_tripped = VocabularyDocument.from_json_text(json_text)

    assert json_text.endswith("\n")
    assert target_path.exists() is False
    assert round_tripped.entry_index["round_trip_entry"].raw_or_derived is RawDerivedTag.RAW
