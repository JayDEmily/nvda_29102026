from __future__ import annotations

from nvda_desk.cognition.modifiers.state_conditioned import StateConditionedModifierService
from nvda_desk.config.coefficient_authority import CoefficientAuthorityService
from nvda_desk.contracts.modifiers import ModifierReplayReceipt


def test_coefficient_authority_builds_deterministic_replay_receipt() -> None:
    service = CoefficientAuthorityService()

    first = service.build_replay_receipt(
        active_modifier_ids=["negative_gamma_stress"], owner_stage="posture"
    )
    second = service.build_replay_receipt(
        active_modifier_ids=["negative_gamma_stress"], owner_stage="posture"
    )

    assert isinstance(first, ModifierReplayReceipt)
    assert first.replay_fingerprint == second.replay_fingerprint
    assert [item.coefficient_id for item in first.resolved_coefficients] == sorted(
        item.coefficient_id for item in first.resolved_coefficients
    )
    assert "capital_deployment_decision" in first.closed_authority_classes
    assert "source_data_ingestion" in first.closed_authority_classes
    assert "hidden_strategy_change" in first.closed_authority_classes


def test_state_conditioned_service_exposes_replay_receipt_without_widening_authority() -> None:
    service = StateConditionedModifierService()

    receipt = service.build_replay_receipt(
        active_modifier_ids=["negative_gamma_stress"], owner_stage="posture"
    )

    resolved = {item.coefficient_id: item for item in receipt.resolved_coefficients}
    assert receipt.owner_stage == "posture"
    assert receipt.active_modifier_ids == ["negative_gamma_stress"]
    assert resolved["max_risk_per_trade"].effective_value == 0.25
    assert resolved["hedge_required"].effective_value is True
    assert "unbounded_runtime_mutation" in receipt.closed_authority_classes
