from __future__ import annotations

from nvda_desk.contracts.review_replay import ImportedModuleCitation, ReviewReplayDecision
from nvda_desk.replay.review_compare import compare_imported_module_review_replay
from nvda_desk.review.imported_module_citations import map_imported_module_citations


def _citations() -> list[ImportedModuleCitation]:
    return [
        ImportedModuleCitation(
            source_identifier="atlas/module-a.py:10-20",
            imported_module="legacy.module_a",
            cited_claim="legacy module A produced review signal",
        ),
        ImportedModuleCitation(
            source_identifier="atlas/module-b.py:5-7",
            imported_module="legacy.module_b",
            cited_claim="legacy module B was rejected",
        ),
    ]


def test_review_replay_compares_imported_module_claims_without_runtime_promotion() -> None:
    decisions = [
        ReviewReplayDecision(
            source_identifier="atlas/module-a.py:10-20",
            decision_id="decision-a",
            admission_class="admitted_partial",
            status="accepted_for_review_only",
        ),
        ReviewReplayDecision(
            source_identifier="atlas/module-b.py:5-7",
            decision_id="decision-b",
            admission_class="rejected",
            status="superseded",
        ),
    ]

    result = compare_imported_module_review_replay(citations=_citations(), decisions=decisions)

    assert result.promoted_to_runtime is False
    assert result.runtime_side_effects == []
    assert result.compared_source_identifiers == [
        "atlas/module-a.py:10-20",
        "atlas/module-b.py:5-7",
    ]
    assert result.missing_decision_source_identifiers == []


def test_imported_module_citations_are_traceable_to_source_and_decision() -> None:
    mapped = map_imported_module_citations(
        citations=_citations(),
        decisions=[
            ReviewReplayDecision(
                source_identifier="atlas/module-a.py:10-20",
                decision_id="decision-a",
                admission_class="admitted_partial",
                status="accepted_for_review_only",
            ),
            ReviewReplayDecision(
                source_identifier="atlas/module-b.py:5-7",
                decision_id="decision-b",
                admission_class="rejected",
                status="superseded",
                rejection_reason="native owner already exists",
            ),
        ],
    )

    assert [row.source_identifier for row in mapped] == [
        "atlas/module-a.py:10-20",
        "atlas/module-b.py:5-7",
    ]
    assert [row.decision_id for row in mapped] == ["decision-a", "decision-b"]
    assert [row.admission_class for row in mapped] == ["admitted_partial", "rejected"]
    assert mapped[1].rejection_or_supersession_status == "superseded"
    assert mapped[1].rejection_reason == "native owner already exists"


def test_review_replay_result_is_deterministic_for_same_inputs() -> None:
    decisions = [
        ReviewReplayDecision(
            source_identifier="atlas/module-b.py:5-7",
            decision_id="decision-b",
            admission_class="rejected",
            status="superseded",
        ),
        ReviewReplayDecision(
            source_identifier="atlas/module-a.py:10-20",
            decision_id="decision-a",
            admission_class="admitted_partial",
            status="accepted_for_review_only",
        ),
    ]

    first = compare_imported_module_review_replay(citations=_citations(), decisions=decisions)
    second = compare_imported_module_review_replay(
        citations=_citations(), decisions=list(reversed(decisions))
    )

    assert first.model_dump() == second.model_dump()
