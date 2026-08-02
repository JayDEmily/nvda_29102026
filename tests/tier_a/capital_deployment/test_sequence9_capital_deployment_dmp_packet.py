"""Sequence 9 DMPV3 packet tests for capital deployment decisions."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest

from nvda_desk.capital.authority import evaluate_capital_deployment
from nvda_desk.contracts.capital import (
    CapitalDeploymentAuthorityInput,
)
from nvda_desk.contracts.packets import K07_ADMITTED_PACKET_ROLES
from nvda_desk.packets.dmp_packets import build_capital_deployment_packet


def test_sequence9_capital_decision_packet_role_remains_fail_closed_under_k07() -> None:
    """The legacy helper must not create a new capital-authority packet role."""
    decision = evaluate_capital_deployment(
        CapitalDeploymentAuthorityInput(
            final_risk_action="proceed",
            final_risk_receipt_id="final-risk-seq9",
            serial_candidate_id="serial-candidate-seq9",
            serial_candidate_eligible=True,
            serial_confidence=0.77,
            downstream_pre_deployment_allowed=True,
            downstream_pre_deployment_receipt_id="pre-deployment-seq9",
            parallel_risk_packet_id="parallel-risk-envelope-packet-seq9",
            parallel_risk_envelope_state="broad",
            coefficient_min_deployable_floor_pct=2.0,
            capital_state_snapshot_id="capital-state-seq9",
            available_capital_usd=100_000.0,
            bounded_policy_id="bounded-policy-seq9",
            requested_deployable_pct=10.0,
            max_deployable_pct=10.0,
        ),
        receipt_id="capital-deployment-receipt-seq9",
    )

    assert "capital_deployment_decision" not in K07_ADMITTED_PACKET_ROLES
    with pytest.raises(
        ValueError,
        match="packetrole is not admitted by K07: capital_deployment_decision",
    ):
        build_capital_deployment_packet(
            packet_id="capital-deployment-decision-seq9",
            data=decision,
            emitted_at=datetime(2026, 5, 5, tzinfo=UTC),
            traceid="trace-seq9",
            runid="run-seq9",
            scenarioid="sequence9",
            parentids=["serial-candidate-packet-seq5", "parallel-risk-envelope-packet-seq7"],
            dependencyids=["coefficient-authority-seq8", "temporal-context-seq5"],
            derivedfrom="sequence9_downstream_capital_authority",
        )
