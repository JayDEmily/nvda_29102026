"""Pure downstream opening calculations."""

from __future__ import annotations

from nvda_desk.contracts.capital import CapitalDeploymentDecision
from nvda_desk.contracts.downstream import (
    DownstreamOpeningSnapshot,
    PlacementReadinessResult,
)
from nvda_desk.downstream.opening import evaluate_placement_readiness


def build_opening_snapshot(opening_ids: list[str] | None = None) -> DownstreamOpeningSnapshot:
    """Return one bounded opening snapshot without injecting policy."""
    return DownstreamOpeningSnapshot(opening_ids=list(opening_ids or []))


def build_placement_readiness(
    *,
    decision: CapitalDeploymentDecision,
    serial_candidate_id: str,
    placement_constraint_ids: list[str] | None = None,
    broker_boundary_mode: str = "protocol_only",
    readiness_id: str = "placement-readiness",
) -> PlacementReadinessResult:
    """Return non-executing placement readiness from capital authority output."""
    return evaluate_placement_readiness(
        decision=decision,
        serial_candidate_id=serial_candidate_id,
        placement_constraint_ids=placement_constraint_ids,
        broker_boundary_mode=broker_boundary_mode,
        readiness_id=readiness_id,
    )
