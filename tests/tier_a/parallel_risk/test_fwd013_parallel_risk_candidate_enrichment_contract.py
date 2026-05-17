from __future__ import annotations

from nvda_desk.api.app import create_app
from nvda_desk.contracts.parallel_risk import ParallelRiskFragilityDimension
from nvda_desk.risk.parallel.evaluate import enrich_candidate_semantics
from nvda_desk.services.parallel_risk_lane_service import ParallelRiskLaneService


def test_parallel_risk_candidate_enrichment_projects_semantics_without_arbitration() -> None:
    enriched = enrich_candidate_semantics(
        candidate_id="candidate-1",
        semantic_tags=["earnings", "negative_gamma"],
        fragility_dimensions=[
            ParallelRiskFragilityDimension(
                dimension_id="event_gap_risk",
                score=0.75,
                reason="earnings_window",
            )
        ],
    )

    assert enriched.candidate_id == "candidate-1"
    assert enriched.consequence_posture == "caution"
    assert enriched.fragility_dimensions[0].dimension_id == "event_gap_risk"
    assert enriched.decision_authority == "parallel_risk_candidate_audit_only"
    assert enriched.capital_sizing_allowed is False


def test_parallel_risk_gateway_service_records_policy_decisions_and_api_exposes_them() -> None:
    service = ParallelRiskLaneService()
    decision = service.evaluate_risk_policy(
        policy_id="risk-policy-1",
        candidate_id="candidate-1",
        semantic_tags=["vix_extreme"],
    )

    assert decision.policy_id == "risk-policy-1"
    assert decision.candidate.consequence_posture == "block"
    assert service.list_risk_decisions()[0].decision_id == decision.decision_id

    app = create_app()
    api_decision = app.evaluate_risk_policy(
        "risk-policy-api-1",
        candidate_id="candidate-api",
        semantic_tags=["earnings"],
    )
    assert api_decision["candidate"]["candidate_id"] == "candidate-api"
    assert any(
        decision["policy_id"] == "risk-policy-api-1" for decision in app.list_risk_decisions()
    )
