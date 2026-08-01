"""Tier A tests for modifier contract authority and copy boundaries."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from nvda_desk.contracts.modifiers import (
    ModifierReplayReceipt,
    ModifierRuntimePacket,
    ResolvedCoefficientValue,
)

FORBIDDEN_AUTHORITY_FIELDS = {
    "trade_allowed": True,
    "broker_order_id": "order-1",
    "capital_sizing": {"notional": 1_000_000},
    "risk_limit_override": True,
}


def _resolved_coefficient() -> ResolvedCoefficientValue:
    return ResolvedCoefficientValue(
        coefficient_id="max_risk_per_trade",
        owner_stage="posture",
        surface_class="mutable_runtime_surface",
        baseline_value=0.35,
        effective_value=0.25,
        transform_family="clamp",
        modifier_inputs=["negative_gamma_stress"],
        workbook_ref="Runtime_Surface_Drivers!B10:H10",
        runtime_mutable=True,
    )


def _resolved_payload() -> dict[str, object]:
    return {
        "coefficient_id": "max_risk_per_trade",
        "owner_stage": "posture",
        "surface_class": "mutable_runtime_surface",
        "baseline_value": 0.35,
        "effective_value": 0.25,
        "transform_family": "clamp",
        "modifier_inputs": ["negative_gamma_stress"],
        "workbook_ref": "Runtime_Surface_Drivers!B10:H10",
        "runtime_mutable": True,
    }


@pytest.mark.parametrize(
    ("model_type", "base_payload"),
    [
        (ResolvedCoefficientValue, _resolved_payload()),
        (
            ModifierRuntimePacket,
            {
                "packet_id": "modifier-packet-fixture",
                "active_modifier_ids": ["negative_gamma_stress"],
                "policy_ids": ["negative_gamma_stress"],
                "resolved_surfaces": ["max_risk_per_trade"],
                "resolved_coefficients": [_resolved_payload()],
            },
        ),
        (
            ModifierReplayReceipt,
            {
                "authority_id": "coefficient_authority.v1",
                "schema_version": "v1",
                "owner_stage": "posture",
                "active_modifier_ids": ["negative_gamma_stress"],
                "resolved_coefficients": [_resolved_payload()],
                "replay_fingerprint": "fixture-fingerprint",
                "closed_authority_classes": ["capital_deployment_decision"],
            },
        ),
    ],
)
def test_modifier_contracts_reject_top_level_closed_authority_fields(
    model_type: type,
    base_payload: dict[str, object],
) -> None:
    """Modifier contracts cannot carry closed execution/capital authority fields."""

    for field_name, field_value in FORBIDDEN_AUTHORITY_FIELDS.items():
        payload = dict(base_payload)
        payload[field_name] = field_value
        with pytest.raises(ValidationError, match="Extra inputs are not permitted"):
            model_type.model_validate(payload)


def test_modifier_runtime_packet_detaches_caller_owned_lists_and_coefficients() -> None:
    """Runtime packets must not retain caller-owned modifier lineage containers."""

    active_modifier_ids = ["negative_gamma_stress"]
    policy_ids = ["negative_gamma_stress"]
    resolved_surfaces = ["max_risk_per_trade"]
    resolved = _resolved_coefficient()

    packet = ModifierRuntimePacket(
        packet_id="modifier-packet-fixture",
        active_modifier_ids=active_modifier_ids,
        policy_ids=policy_ids,
        resolved_surfaces=resolved_surfaces,
        resolved_coefficients=[resolved],
    )

    active_modifier_ids.append("mutated")
    policy_ids.append("mutated")
    resolved_surfaces.append("mutated")
    resolved.modifier_inputs.append("mutated")

    assert packet.active_modifier_ids == ["negative_gamma_stress"]
    assert packet.policy_ids == ["negative_gamma_stress"]
    assert packet.resolved_surfaces == ["max_risk_per_trade"]
    assert packet.resolved_coefficients[0].modifier_inputs == ["negative_gamma_stress"]


def test_modifier_replay_receipt_detaches_caller_owned_lists_and_coefficients() -> None:
    """Replay receipts must preserve immutable replay lineage after construction."""

    active_modifier_ids = ["negative_gamma_stress"]
    closed_authority_classes = ["capital_deployment_decision"]
    resolved = _resolved_coefficient()

    receipt = ModifierReplayReceipt(
        authority_id="coefficient_authority.v1",
        schema_version="v1",
        owner_stage="posture",
        active_modifier_ids=active_modifier_ids,
        resolved_coefficients=[resolved],
        replay_fingerprint="fixture-fingerprint",
        closed_authority_classes=closed_authority_classes,
    )

    active_modifier_ids.append("mutated")
    closed_authority_classes.append("mutated")
    resolved.modifier_inputs.append("mutated")

    assert receipt.active_modifier_ids == ["negative_gamma_stress"]
    assert receipt.closed_authority_classes == ["capital_deployment_decision"]
    assert receipt.resolved_coefficients[0].modifier_inputs == ["negative_gamma_stress"]
