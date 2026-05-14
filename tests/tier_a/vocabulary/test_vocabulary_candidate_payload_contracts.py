from __future__ import annotations

import pytest

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
                allowed_aliases=["legacy phrase"],
                disallowed_phrases=["do not admit"],
            )
        ],
    )


def test_vocabulary_candidate_from_dict_accepts_bridge_payload_shape() -> None:
    candidate = VocabularyCandidate.from_dict(
        {
            "candidate_slug": "bridge_candidate",
            "candidate_label": "Bridge Candidate",
            "category": "workflow",
            "stage_owner": "vocabulary_governance",
            "maps_to_contract": "BridgeContract",
            "raw_or_derived": "derived",
            "aliases": ["bridge phrase"],
        }
    )

    assert candidate.tokens() == {"bridge_candidate", "bridge candidate", "bridge phrase"}


def test_vocabulary_candidate_from_dict_rejects_non_list_aliases() -> None:
    with pytest.raises(ValueError, match="candidate aliases must be a list"):
        VocabularyCandidate.from_dict(
            {
                "candidate_slug": "bad_aliases",
                "candidate_label": "Bad Aliases",
                "aliases": "not a list",
            }
        )


def test_classify_candidate_payload_delegates_to_governed_classification() -> None:
    classification = _document().classify_candidate_payload(
        {
            "candidate_slug": "legacy_phrase",
            "candidate_label": "Legacy Phrase",
            "aliases": [],
        }
    )

    assert classification.action is VocabularyCandidateAction.ALIAS_ONLY
    assert classification.matched_slug == "existing_term"


def test_classify_candidate_payload_rejects_unknown_category() -> None:
    with pytest.raises(ValueError, match="category must be one of"):
        _document().classify_candidate_payload(
            {
                "candidate_slug": "bad_category",
                "candidate_label": "Bad Category",
                "category": "runtime_signal",
            }
        )


def test_classify_candidates_preserves_input_order_and_action_values() -> None:
    classifications = _document().classify_candidates(
        [
            VocabularyCandidate("existing_term", "Existing Term"),
            VocabularyCandidate("fresh_term", "Fresh Term"),
            VocabularyCandidate("do_not_admit", "Do Not Admit"),
        ]
    )

    assert [item.action for item in classifications] == [
        VocabularyCandidateAction.ENRICH_EXISTING,
        VocabularyCandidateAction.ADD_NEW,
        VocabularyCandidateAction.QUARANTINE,
    ]
