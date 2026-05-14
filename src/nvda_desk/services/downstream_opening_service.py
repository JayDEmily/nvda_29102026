"""Compatibility wrapper for workbook-owned downstream opening service path."""

from __future__ import annotations

from nvda_desk.contracts.capital import CapitalDeploymentDecision
from nvda_desk.contracts.downstream import (
    DownstreamOpeningSnapshot,
    PlacementReadinessResult,
)
from nvda_desk.downstream.opening import DownstreamOpeningService as _DownstreamOpeningService


class DownstreamOpeningService(_DownstreamOpeningService):
    """Workbook-owned alias of the bounded downstream opening service."""

    def build_opening_snapshot(
        self, opening_ids: list[str] | None = None
    ) -> DownstreamOpeningSnapshot:
        return super().build_opening_snapshot(opening_ids=opening_ids)

    def evaluate_placement_readiness(
        self,
        *,
        decision: CapitalDeploymentDecision,
        serial_candidate_id: str,
        placement_constraint_ids: list[str] | None = None,
        broker_boundary_mode: str = "protocol_only",
        readiness_id: str = "placement-readiness",
    ) -> PlacementReadinessResult:
        """Delegate to the bounded downstream opening readiness owner."""
        return super().evaluate_placement_readiness(
            decision=decision,
            serial_candidate_id=serial_candidate_id,
            placement_constraint_ids=placement_constraint_ids,
            broker_boundary_mode=broker_boundary_mode,
            readiness_id=readiness_id,
        )
