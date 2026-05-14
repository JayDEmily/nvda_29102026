from __future__ import annotations

from nvda_desk.schemas.vocabulary import (
    VocabularyCandidate,
    VocabularyCandidateAction,
    VocabularyDocument,
    VocabularyEntry,
)


def _document() -> VocabularyDocument:
    return VocabularyDocument(
        schema_version="v1",
        registry_version="test",
        entries=[
            VocabularyEntry(
                canonical_slug="existing_term",
                canonical_label="Existing Term",
                category="workflow",
                stage_owner="vocabulary_governance",
                maps_to_contract="ExistingContract",
                allowed_aliases=["old desk phrase"],
                disallowed_phrases=["forbidden desk phrase"],
            ),
            VocabularyEntry(
                canonical_slug="second_term",
                canonical_label="Second Term",
                category="workflow",
                stage_owner="vocabulary_governance",
                maps_to_contract="SecondContract",
            ),
        ],
    )


def test_candidate_action_contract_is_the_governed_admission_set() -> None:
    assert {action.value for action in VocabularyCandidateAction} == {
        "enrich_existing",
        "add_new",
        "alias_only",
        "quarantine",
    }


def test_candidate_matching_existing_slug_is_enrich_existing() -> None:
    classification = _document().classify_candidate(
        VocabularyCandidate(
            candidate_slug="existing_term",
            candidate_label="Existing Term Extension",
        )
    )

    assert classification.action is VocabularyCandidateAction.ENRICH_EXISTING
    assert classification.matched_slug == "existing_term"


def test_candidate_matching_existing_label_is_enrich_existing() -> None:
    classification = _document().classify_candidate(
        VocabularyCandidate(
            candidate_slug="fresh_slug",
            candidate_label="Existing Term",
        )
    )

    assert classification.action is VocabularyCandidateAction.ENRICH_EXISTING
    assert classification.matched_slug == "existing_term"


def test_candidate_matching_allowed_alias_is_alias_only() -> None:
    classification = _document().classify_candidate(
        VocabularyCandidate(
            candidate_slug="old_desk_phrase",
            candidate_label="Old Desk Phrase",
        )
    )

    assert classification.action is VocabularyCandidateAction.ALIAS_ONLY
    assert classification.matched_slug == "existing_term"


def test_candidate_with_no_collision_is_add_new() -> None:
    classification = _document().classify_candidate(
        VocabularyCandidate(
            candidate_slug="new_governed_term",
            candidate_label="New Governed Term",
            category="workflow",
            raw_or_derived="not_applicable",
        )
    )

    assert classification.action is VocabularyCandidateAction.ADD_NEW
    assert classification.matched_slug is None


def test_candidate_matching_disallowed_phrase_is_quarantine() -> None:
    classification = _document().classify_candidate(
        VocabularyCandidate(
            candidate_slug="forbidden_desk_phrase",
            candidate_label="Forbidden Desk Phrase",
        )
    )

    assert classification.action is VocabularyCandidateAction.QUARANTINE
    assert classification.matched_slug == "existing_term"


def test_candidate_matching_multiple_entries_is_quarantine() -> None:
    classification = _document().classify_candidate(
        VocabularyCandidate(
            candidate_slug="existing_term",
            candidate_label="Second Term",
        )
    )

    assert classification.action is VocabularyCandidateAction.QUARANTINE
    assert classification.matched_slug is None


def test_candidate_classification_to_dict_is_stable() -> None:
    classification = _document().classify_candidate(
        VocabularyCandidate(
            candidate_slug="new_governed_term",
            candidate_label="New Governed Term",
        )
    )

    assert classification.to_dict() == {
        "action": "add_new",
        "candidate_slug": "new_governed_term",
        "matched_slug": None,
        "reason": "candidate does not match governed slugs, labels, aliases, or disallowed phrases",
    }
