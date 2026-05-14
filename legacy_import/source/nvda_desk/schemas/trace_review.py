"""Typed contracts for bounded real-data trace-review scenarios.

These contracts freeze a small sibling-scenario pack built around one admitted
prepared-runtime anchor. They exist for semantic review and regression, not for
runtime authority or coefficient tuning.
"""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from nvda_desk.schemas.checkpoints import CheckpointObservation
from nvda_desk.schemas.cognition import (
    EligibilityAdmissibilitySurface,
    ExecutionCandidateOwnershipSurface,
    InventoryState,
    MarketRegimeContextInput,
    TerminalRiskApplicationSurface,
)
from nvda_desk.schemas.dataset import PreparedRuntimeSnapshot
from nvda_desk.schemas.risk import RiskDecision


class TraceScenarioPerturbation(BaseModel):
    """One explicit bounded perturbation applied to the anchor scenario."""

    model_config = ConfigDict(extra="forbid")

    field_name: str
    baseline_value: str
    scenario_value: str
    rationale: str


class BoundedTraceScenario(BaseModel):
    """One bounded sibling scenario anchored to an admitted prepared snapshot."""

    model_config = ConfigDict(extra="forbid")

    scenario_id: str
    scenario_label: str
    scenario_family: str
    anchor_snapshot_ts: datetime
    provenance_note: str
    expected_human_read: str
    perturbations: list[TraceScenarioPerturbation] = Field(default_factory=list)
    prepared_snapshot: PreparedRuntimeSnapshot
    regime_input: MarketRegimeContextInput
    inventory_state: InventoryState
    risk_budget_remaining_pct: float = Field(ge=0.0, le=100.0)


class BoundedTraceFixturePack(BaseModel):
    """One deterministic bounded-scenario pack for human logic tracing."""

    model_config = ConfigDict(extra="forbid")

    pack_id: str
    source_fixture_pack_id: str
    anchor_snapshot_ts: datetime
    anchor_symbol: str
    scenario_ids: list[str]
    scenarios: list[BoundedTraceScenario]


class BoundedTraceRunResult(BaseModel):
    """Observed runtime outputs for one bounded trace-review scenario."""

    model_config = ConfigDict(extra="forbid")

    scenario_id: str
    desk_window: str
    event_window_state: str
    event_minutes_remaining: int | None = None
    options_behavior_cluster: str
    permission_state: str
    active_playbook_ids: list[str] = Field(default_factory=list)
    final_risk_action: str
    recommendation_target_pct: float
    capital_deployment_action: str
    capital_deployment_opportunity_pct: float
    capital_deployment_authorised_pct: float
    downstream_policy_freeze_state: str
    downstream_deferred_domains: list[str] = Field(default_factory=list)
    effective_surfaces: dict[str, float | bool | None] = Field(default_factory=dict)
    admissibility_surface: EligibilityAdmissibilitySurface
    candidate_ownership: ExecutionCandidateOwnershipSurface
    overlay_risk_decision: RiskDecision
    terminal_risk_application: TerminalRiskApplicationSurface
    summary: str
    expected_human_read: str
    checkpoint_observations: list[CheckpointObservation] = Field(default_factory=list)


class BoundedTraceReviewReport(BaseModel):
    """Simplified report for a bounded trace-review pack."""

    model_config = ConfigDict(extra="forbid")

    pack_id: str
    scenario_ids: list[str]
    runs: list[BoundedTraceRunResult]
    narrative_summary: list[str] = Field(default_factory=list)
