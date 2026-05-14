from __future__ import annotations

import json

import pytest

from nvda_desk.schemas.vocabulary import (
    RawDerivedTag,
    VocabularyCategory,
    VocabularyDocument,
    VocabularyEntry,
)


def _enum_values(enum_type: type) -> set[str]:
    return {member.value for member in enum_type}


def test_vocabulary_category_contract_is_bounded_to_current_canonical_categories() -> None:
    committed = json.loads(
        open("data/vocabulary/canonical_vocabulary.json", encoding="utf-8").read()
    )
    committed_categories = {entry["category"] for entry in committed["entries"]}

    assert _enum_values(VocabularyCategory) == committed_categories
    assert "runtime_signal" not in _enum_values(VocabularyCategory)


def test_raw_derived_contract_is_bounded() -> None:
    assert _enum_values(RawDerivedTag) == {"raw", "derived", "not_applicable"}


def test_vocabulary_entry_rejects_unbounded_category_and_raw_derived_values() -> None:
    with pytest.raises((ValueError, TypeError)):
        VocabularyEntry(
            canonical_slug="unbounded_category",
            canonical_label="Unbounded Category",
            category="runtime_signal",
            stage_owner="vocabulary_governance",
            raw_or_derived=RawDerivedTag.NOT_APPLICABLE,
            maps_to_contract="VocabularyEntry.category",
        ).validate()

    with pytest.raises((ValueError, TypeError)):
        VocabularyEntry(
            canonical_slug="unbounded_raw_tag",
            canonical_label="Unbounded Raw Tag",
            category=VocabularyCategory.WORKFLOW,
            stage_owner="vocabulary_governance",
            raw_or_derived="mixed",
            maps_to_contract="VocabularyEntry.raw_or_derived",
        ).validate()


def test_vocabulary_entry_carries_candidate_descriptor_fields() -> None:
    entry = VocabularyEntry(
        canonical_slug="candidate_descriptor_entry",
        canonical_label="Candidate Descriptor Entry",
        category=VocabularyCategory.WORKFLOW,
        stage_owner="vocabulary_governance",
        family="candidate_family",
        setup_variant="candidate_setup",
        execution_expression="candidate_expression",
        horizon="candidate_horizon",
        raw_or_derived=RawDerivedTag.DERIVED,
        maps_to_contract="VocabularyEntry",
    )

    assert entry.family == "candidate_family"
    assert entry.setup_variant == "candidate_setup"
    assert entry.execution_expression == "candidate_expression"
    assert entry.horizon == "candidate_horizon"
    assert entry.raw_or_derived is RawDerivedTag.DERIVED


def test_vocabulary_document_entry_index_is_slug_keyed_projection() -> None:
    entry = VocabularyEntry(
        canonical_slug="slug_indexed_entry",
        canonical_label="Slug Indexed Entry",
        category=VocabularyCategory.WORKFLOW,
        stage_owner="vocabulary_governance",
        raw_or_derived=RawDerivedTag.NOT_APPLICABLE,
        maps_to_contract="VocabularyDocument.entry_index",
    )
    document = VocabularyDocument(schema_version="v1", registry_version="test", entries=[entry])

    assert document.entry_index == {"slug_indexed_entry": entry}


def test_empty_vocabulary_document_entry_index_is_empty() -> None:
    document = VocabularyDocument(schema_version="v1", registry_version="test")

    assert document.entry_index == {}
