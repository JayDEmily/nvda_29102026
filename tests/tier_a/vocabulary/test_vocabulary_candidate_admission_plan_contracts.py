from __future__ import annotations

import pytest

from nvda_desk.schemas.vocabulary import (
    RawDerivedTag,
    VocabularyCandidate,
    VocabularyCandidateAction,
    VocabularyCandidateAdmissionPlan,
    VocabularyDocument,
    VocabularyEntry,
)


def _document() -> VocabularyDocument:
    return VocabularyDocument(
        schema_version="v1",
        registry_version="test",
        entries=[
            VocabularyEntry(
                canonical_slug="governed_term",
                canonical_label="Governed Term",
                category="workflow",
                stage_owner="vocabulary_governance",
                maps_to_contract="GovernedContract",
                allowed_aliases=["known alias"],
                disallowed_phrases=["forbidden phrase"],
            )
        ],
    )


def test_candidate_admission_plan_contract_serialises_quarantine_without_mutation() -> None:
    plan = _document().plan_candidate_admission(
        VocabularyCandidate("forbidden_phrase", "Forbidden Phrase")
    )

    assert isinstance(plan, VocabularyCandidateAdmissionPlan)
    assert plan.classification.action is VocabularyCandidateAction.QUARANTINE
    assert plan.proposed_entry is None
    assert plan.alias_candidates == []
    assert plan.to_dict() == {
        "classification": {
            "action": "quarantine",
            "candidate_slug": "forbidden_phrase",
            "matched_slug": "governed_term",
            "reason": "candidate token matches disallowed vocabulary phrase",
        },
        "proposed_entry": None,
        "alias_candidates": [],
        "quarantine_reason": "candidate token matches disallowed vocabulary phrase",
    }


def test_add_new_admission_plan_requires_full_governance_metadata() -> None:
    with pytest.raises(ValueError, match="add_new candidate admission requires"):
        _document().plan_candidate_admission(
            VocabularyCandidate("new_term", "New Term", category="workflow")
        )


def test_add_new_admission_plan_builds_valid_proposed_entry() -> None:
    plan = _document().plan_candidate_admission(
        VocabularyCandidate(
            candidate_slug="new_term",
            candidate_label="New Term",
            category="workflow",
            stage_owner="vocabulary_governance",
            maps_to_contract="NewTermContract",
            raw_or_derived=RawDerivedTag.DERIVED,
            aliases=["new term alias"],
        )
    )

    assert plan.classification.action is VocabularyCandidateAction.ADD_NEW
    assert plan.proposed_entry is not None
    assert plan.proposed_entry.to_dict() == {
        "namespace": "global",
        "canonical_id": "global.new_term",
        "canonical_slug": "new_term",
        "canonical_label": "New Term",
        "category": "workflow",
        "stage_owner": "vocabulary_governance",
        "maps_to_contract": "NewTermContract",
        "allowed_aliases": ["new term alias"],
        "disallowed_phrases": [],
        "notes": [],
        "raw_or_derived": "derived",
    }
    assert plan.alias_candidates == []
    assert plan.quarantine_reason is None


def test_alias_only_admission_plan_lists_only_new_alias_candidates() -> None:
    plan = _document().plan_candidate_admission(
        VocabularyCandidate(
            candidate_slug="known_alias",
            candidate_label="Known Alias",
            aliases=["fresh alias", "known alias"],
        )
    )

    assert plan.classification.action is VocabularyCandidateAction.ALIAS_ONLY
    assert plan.classification.matched_slug == "governed_term"
    assert plan.proposed_entry is None
    assert plan.alias_candidates == ["fresh alias"]


def test_enrich_existing_admission_plan_can_offer_non_duplicate_aliases() -> None:
    plan = _document().plan_candidate_admission(
        VocabularyCandidate(
            candidate_slug="governed_term",
            candidate_label="Governed Term",
            aliases=["governed term extension"],
        )
    )

    assert plan.classification.action is VocabularyCandidateAction.ENRICH_EXISTING
    assert plan.classification.matched_slug == "governed_term"
    assert plan.alias_candidates == ["governed term extension"]


def test_candidate_admission_summary_counts_governed_actions() -> None:
    summary = _document().candidate_admission_summary(
        [
            VocabularyCandidate("governed_term", "Governed Term"),
            VocabularyCandidate("known_alias", "Known Alias"),
            VocabularyCandidate(
                "new_term",
                "New Term",
                category="workflow",
                stage_owner="vocabulary_governance",
                maps_to_contract="NewTermContract",
                raw_or_derived="derived",
            ),
            VocabularyCandidate("forbidden_phrase", "Forbidden Phrase"),
        ]
    )

    assert summary == {
        "enrich_existing": 1,
        "add_new": 1,
        "alias_only": 1,
        "quarantine": 1,
    }


def test_batch_admission_plans_preserve_input_order() -> None:
    plans = _document().plan_candidate_admissions(
        [
            VocabularyCandidate("known_alias", "Known Alias"),
            VocabularyCandidate("forbidden_phrase", "Forbidden Phrase"),
        ]
    )

    assert [plan.classification.action for plan in plans] == [
        VocabularyCandidateAction.ALIAS_ONLY,
        VocabularyCandidateAction.QUARANTINE,
    ]


def test_with_candidate_admission_adds_new_entry_without_mutating_source_document() -> None:
    document = _document()
    admitted = document.with_candidate_admission(
        VocabularyCandidate(
            candidate_slug="new_leaf_term",
            candidate_label="New Leaf Term",
            category="workflow",
            stage_owner="vocabulary_governance",
            maps_to_contract="VocabularyDocument.with_candidate_admission",
            raw_or_derived="derived",
        )
    )

    assert "new_leaf_term" not in document.entry_index
    assert admitted.entry_index["new_leaf_term"].canonical_label == "New Leaf Term"
    assert admitted.entry_index["new_leaf_term"]._raw_or_derived() is RawDerivedTag.DERIVED


def test_with_candidate_admission_adds_alias_to_existing_entry() -> None:
    admitted = _document().with_candidate_admission(
        VocabularyCandidate(
            candidate_slug="known_alias",
            candidate_label="Known Alias",
            aliases=["fresh bridge alias"],
        )
    )

    entry = admitted.entry_index["governed_term"]
    assert entry.allowed_aliases == ["known alias", "fresh bridge alias"]


def test_with_candidate_admission_rejects_quarantine_candidate() -> None:
    with pytest.raises(ValueError, match="quarantined vocabulary candidate cannot be admitted"):
        _document().with_candidate_admission(
            VocabularyCandidate("forbidden_phrase", "Forbidden Phrase")
        )


def test_with_candidate_admissions_applies_batch_in_order() -> None:
    admitted = _document().with_candidate_admissions(
        [
            VocabularyCandidate("known_alias", "Known Alias", aliases=["first alias"]),
            VocabularyCandidate(
                "new_leaf_term",
                "New Leaf Term",
                category="workflow",
                stage_owner="vocabulary_governance",
                maps_to_contract="VocabularyDocument.with_candidate_admissions",
                raw_or_derived="derived",
            ),
        ]
    )

    assert admitted.entry_index["governed_term"].allowed_aliases == [
        "known alias",
        "first alias",
    ]
    assert admitted.entry_index["new_leaf_term"].maps_to_contract == (
        "VocabularyDocument.with_candidate_admissions"
    )


def test_add_new_admission_plan_rejects_blank_governance_metadata() -> None:
    with pytest.raises(ValueError, match="stage_owner must be a non-empty string"):
        _document().plan_candidate_admission(
            VocabularyCandidate(
                candidate_slug="blank_owner_term",
                candidate_label="Blank Owner Term",
                category="workflow",
                stage_owner="",
                maps_to_contract="BlankOwnerContract",
                raw_or_derived="derived",
            )
        )

    with pytest.raises(ValueError, match="maps_to_contract must be a non-empty string"):
        _document().plan_candidate_admission(
            VocabularyCandidate(
                candidate_slug="blank_contract_term",
                candidate_label="Blank Contract Term",
                category="workflow",
                stage_owner="vocabulary_governance",
                maps_to_contract="",
                raw_or_derived="derived",
            )
        )


def test_with_candidate_admission_rejects_multi_owner_alias_candidate_before_mutation() -> None:
    document = VocabularyDocument(
        schema_version="v1",
        registry_version="test",
        entries=[
            VocabularyEntry(
                canonical_slug="governed_term",
                canonical_label="Governed Term",
                category="workflow",
                stage_owner="vocabulary_governance",
                maps_to_contract="GovernedContract",
                allowed_aliases=["known alias"],
            ),
            VocabularyEntry(
                canonical_slug="other_term",
                canonical_label="Other Term",
                category="workflow",
                stage_owner="vocabulary_governance",
                maps_to_contract="OtherContract",
            ),
        ],
    )

    with pytest.raises(ValueError, match="quarantined vocabulary candidate cannot be admitted"):
        document.with_candidate_admission(
            VocabularyCandidate(
                candidate_slug="known_alias",
                candidate_label="Known Alias",
                aliases=["OTHER_TERM"],
            )
        )
