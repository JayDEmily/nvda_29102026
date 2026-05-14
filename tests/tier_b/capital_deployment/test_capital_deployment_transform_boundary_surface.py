from __future__ import annotations

from pathlib import Path

import pytest
from pydantic import ValidationError

from nvda_desk.capital.authority import evaluate_capital_deployment
from nvda_desk.contracts.capital import (
    CapitalDeploymentAuthorityAction,
    CapitalDeploymentAuthorityInput,
)

_DONOR_POSTURE_HARD_INVARIANT_KEYS = {
    "PostureHardInvariantsSurface",
    "block_active",
    "hard_block_reasons",
    "zero_deployable_required",
}

_CAPITAL_SOURCE_PATHS = [
    "src/nvda_desk/capital/authority.py",
    "src/nvda_desk/contracts/capital.py",
    "src/nvda_desk/domain/capital/deployment.py",
    "src/nvda_desk/services/capital_deployment_service.py",
]


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def _capital_input_payload(**overrides: object) -> dict[str, object]:
    payload: dict[str, object] = {
        "final_risk_action": "proceed",
        "final_risk_receipt_id": "final-risk-row039",
        "serial_candidate_id": "serial-candidate-row039",
        "serial_candidate_eligible": True,
        "serial_confidence": 0.81,
        "downstream_pre_deployment_allowed": True,
        "downstream_pre_deployment_receipt_id": "pre-deployment-row039",
        "parallel_risk_packet_id": "parallel-risk-row039",
        "parallel_risk_envelope_state": "broad",
        "parallel_risk_hard_blocks": [],
        "parallel_risk_caution_flags": [],
        "coefficient_min_deployable_floor_pct": 0.0,
        "temporal_event_window_active": False,
        "temporal_event_risk": "normal",
        "capital_state_snapshot_id": "capital-state-row039",
        "available_capital_usd": 100_000.0,
        "bounded_policy_id": "bounded-policy-row039",
        "requested_deployable_pct": 10.0,
        "max_deployable_pct": 10.0,
        "inventory_pct": 0.0,
    }
    payload.update(overrides)
    return payload


def test_capital_source_does_not_import_or_redeclare_posture_hard_invariants_surface() -> None:
    root = _repo_root()

    for rel_path in _CAPITAL_SOURCE_PATHS:
        source_text = (root / rel_path).read_text(encoding="utf-8")
        for donor_key in _DONOR_POSTURE_HARD_INVARIANT_KEYS:
            assert donor_key not in source_text, rel_path


def test_capital_input_contract_rejects_posture_hard_invariants_payload_fields() -> None:
    for donor_key in _DONOR_POSTURE_HARD_INVARIANT_KEYS - {"PostureHardInvariantsSurface"}:
        with pytest.raises(ValidationError):
            CapitalDeploymentAuthorityInput(**_capital_input_payload(**{donor_key: True}))


def test_posture_hard_stop_truth_reaches_capital_only_as_pre_deployment_block() -> None:
    context = CapitalDeploymentAuthorityInput(
        **_capital_input_payload(downstream_pre_deployment_allowed=False)
    )

    decision = evaluate_capital_deployment(context)

    assert decision.action is CapitalDeploymentAuthorityAction.BLOCK
    assert decision.rationale == ["downstream_pre_deployment_blocked_candidate"]
    assert "posture_hard_invariants" not in decision.consumed_inputs
    assert "PostureHardInvariantsSurface" not in decision.model_dump_json()
