from __future__ import annotations

import pytest
from pydantic import ValidationError

from nvda_desk.contracts.review import (
    EffectivePolicySnapshot,
    FailureTaxonomyRecord,
    PacketLineageSurface,
    ReviewLineagePacket,
    ReviewPacket,
)

REVIEW_CONTRACTS = (
    ReviewPacket,
    EffectivePolicySnapshot,
    ReviewLineagePacket,
    PacketLineageSurface,
    FailureTaxonomyRecord,
)
FORBIDDEN_EXECUTION_FIELDS = {
    "trade_allowed": True,
    "broker_order_id": "order-1",
    "capital_sizing": {"notional": 1_000_000},
    "risk_limit_override": True,
}


@pytest.mark.parametrize("model_type", REVIEW_CONTRACTS)
def test_review_contracts_reject_top_level_execution_authority_fields(model_type) -> None:
    for field_name, value in FORBIDDEN_EXECUTION_FIELDS.items():
        with pytest.raises(ValidationError, match="Extra inputs are not permitted"):
            model_type(**{field_name: value})


def test_review_lineage_packet_detaches_input_lists_from_caller() -> None:
    surfaces = ["review_surface"]
    policy_ids = ["policy-1"]
    packet = ReviewLineagePacket(
        resolved_surfaces=surfaces,
        modifier_policy_ids=policy_ids,
    )

    surfaces.append("mutated")
    policy_ids.append("mutated")

    assert packet.resolved_surfaces == ["review_surface"]
    assert packet.modifier_policy_ids == ["policy-1"]
