"""Build bounded downstream opening and placement-readiness snapshots."""

from __future__ import annotations

from nvda_desk.contracts.capital import (
    CapitalDeploymentAuthorityAction,
    CapitalDeploymentDecision,
)
from nvda_desk.contracts.downstream import (
    DownstreamOpeningSnapshot,
    PlacementHandoffMaterial,
    PlacementReadinessInputTrace,
    PlacementReadinessResult,
)


class DownstreamOpeningService:
    """Create truthful opening snapshots without injecting policy."""

    def build_opening_snapshot(
        self, opening_ids: list[str] | None = None
    ) -> DownstreamOpeningSnapshot:
        return DownstreamOpeningSnapshot(opening_ids=list(opening_ids or []))

    def evaluate_placement_readiness(
        self,
        *,
        decision: CapitalDeploymentDecision,
        serial_candidate_id: str,
        placement_constraint_ids: list[str] | None = None,
        broker_boundary_mode: str = "protocol_only",
        readiness_id: str = "placement-readiness",
    ) -> PlacementReadinessResult:
        """Evaluate non-executing opening readiness from capital authority output."""

        return evaluate_placement_readiness(
            decision=decision,
            serial_candidate_id=serial_candidate_id,
            placement_constraint_ids=placement_constraint_ids,
            broker_boundary_mode=broker_boundary_mode,
            readiness_id=readiness_id,
        )


def _require_protocol_only_boundary(mode: str) -> None:
    if mode != "protocol_only":
        raise ValueError("placement readiness may use broker_boundary_mode='protocol_only' only")


def _trace(
    *,
    decision: CapitalDeploymentDecision,
    serial_candidate_id: str,
    placement_constraint_ids: list[str],
    broker_boundary_mode: str,
) -> PlacementReadinessInputTrace:
    receipt_id = decision.capital_deployment_receipt_id
    if not receipt_id:
        raise ValueError("placement readiness requires capital_deployment_receipt_id")
    if not serial_candidate_id.strip():
        raise ValueError("placement readiness requires serial_candidate_id")
    return PlacementReadinessInputTrace(
        capital_deployment_receipt_id=receipt_id,
        serial_candidate_id=serial_candidate_id,
        placement_constraint_ids=list(placement_constraint_ids),
        broker_boundary_mode=broker_boundary_mode,
    )


def evaluate_placement_readiness(
    *,
    decision: CapitalDeploymentDecision,
    serial_candidate_id: str,
    placement_constraint_ids: list[str] | None = None,
    broker_boundary_mode: str = "protocol_only",
    readiness_id: str = "placement-readiness",
) -> PlacementReadinessResult:
    """Return readiness/handoff material without opening broker execution."""

    _require_protocol_only_boundary(broker_boundary_mode)
    constraints = list(placement_constraint_ids or [])
    trace = _trace(
        decision=decision,
        serial_candidate_id=serial_candidate_id,
        placement_constraint_ids=constraints,
        broker_boundary_mode=broker_boundary_mode,
    )
    blocked_reasons: list[str] = []
    if decision.action != CapitalDeploymentAuthorityAction.CONTINUE:
        blocked_reasons.append(f"capital_deployment_action_{decision.action.value}")
    if decision.authorised_deployable_pct <= 0.0:
        blocked_reasons.append("no_authorised_deployable_percentage")
    if decision.authorised_notional_usd <= 0.0:
        blocked_reasons.append("no_authorised_notional")

    if blocked_reasons:
        return PlacementReadinessResult(
            readiness_id=readiness_id,
            readiness_state="blocked",
            blocked_reasons=blocked_reasons,
            input_trace=trace,
        )

    handoff = PlacementHandoffMaterial(
        handoff_id=f"{readiness_id}::handoff",
        order_intent_preview={
            "serial_candidate_id": serial_candidate_id,
            "capital_deployment_receipt_id": decision.capital_deployment_receipt_id,
            "authorised_deployable_pct": decision.authorised_deployable_pct,
            "authorised_notional_usd": decision.authorised_notional_usd,
            "placement_constraint_ids": constraints,
        },
    )
    return PlacementReadinessResult(
        readiness_id=readiness_id,
        readiness_state="ready_for_protocol_handoff",
        input_trace=trace,
        placement_handoff=handoff,
    )
