"""Native downstream contract shells for post-capital opening surfaces."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator


class _DetachedMutableModel(BaseModel):
    """Base model that detaches caller-owned mutable field values."""

    @field_validator("*", mode="before")
    @classmethod
    def _detach_mutable_values(cls, value):
        return deepcopy(value)


_LIVE_INVENTORY_TRANSFORM_REQUIRED_DONOR_PAYLOAD_KEYS = frozenset(
    {
        "adjudication_disposition",
        "candidate_shape",
        "champion_candidate_id",
        "comparison_outcome",
        "execution_context_score",
        "fill_bias_adjuster",
        "fill_feedback_router",
        "FillBiasAdjusterContractOutput",
        "FillFeedbackRouterContractOutput",
        "LadderReplayRungOutcome",
        "override_disposition",
        "PostureRiskInput",
        "risk_budget_remaining_pct",
        "shadow_challenger_ids",
        "StrategicLadderValidatorOutput",
    }
)


def _payload_keys(value: Any):
    if isinstance(value, dict):
        for key, child in value.items():
            yield str(key)
            yield from _payload_keys(child)
    elif isinstance(value, (list, tuple, set)):
        for child in value:
            yield from _payload_keys(child)


def _reject_live_inventory_transform_required_donor_payload(value: Any):
    observed = set(_payload_keys(value))
    forbidden = observed & _LIVE_INVENTORY_TRANSFORM_REQUIRED_DONOR_PAYLOAD_KEYS
    if forbidden:
        joined = ", ".join(sorted(forbidden))
        raise ValueError(
            "live inventory source_payload cannot carry transform-required donor "
            f"payload keys: {joined}"
        )
    return value


_PLACEMENT_HANDOFF_BROKER_EXECUTION_KEYS = frozenset(
    {
        "broker_execution_receipt",
        "broker_order_id",
        "execution_allowed",
        "fill_event_id",
        "live_broker_adapter",
        "order_submitted",
    }
)

_PLACEMENT_HANDOFF_EXECUTION_RECORD_DONOR_KEYS = frozenset(
    {
        "broker_execution_record",
        "execution_fill_id",
        "execution_record_id",
        "ExecutionRecord",
        "fill_price_usd",
    }
)


def _reject_placement_handoff_broker_execution_payload(value: Any):
    observed = set(_payload_keys(value))
    execution_record_keys = observed & _PLACEMENT_HANDOFF_EXECUTION_RECORD_DONOR_KEYS
    if execution_record_keys:
        joined = ", ".join(sorted(execution_record_keys))
        raise ValueError(
            "placement handoff order_intent_preview cannot carry execution record "
            f"donor keys: {joined}"
        )
    forbidden = observed & _PLACEMENT_HANDOFF_BROKER_EXECUTION_KEYS
    if forbidden:
        joined = ", ".join(sorted(forbidden))
        raise ValueError(
            "placement handoff order_intent_preview cannot carry broker execution "
            f"keys: {joined}"
        )
    return value


class DownstreamStateSnapshot(BaseModel):
    """Bounded read model for downstream state snapshots."""

    model_config = ConfigDict(extra="forbid")
    stage: str = "downstream"
    position_ids: list[str] = Field(default_factory=list)


class DownstreamStateReadResult(BaseModel):
    """Receipt-bearing downstream state read result."""

    model_config = ConfigDict(extra="forbid")
    snapshot: DownstreamStateSnapshot
    receipt_id: str | None = None


class DownstreamRecommendationHistoryReservation(BaseModel):
    """Reserve recommendation-history capacity before opening placement."""

    model_config = ConfigDict(extra="forbid")
    reservation_id: str
    source_candidate_id: str
    reserved_entry_count: int = Field(default=0, ge=0)


class OpeningAuthorisationResult(BaseModel):
    """Downstream opening-authorisation shell after capital authority."""

    model_config = ConfigDict(extra="forbid")
    recommendation_history_reservation: DownstreamRecommendationHistoryReservation
    authorised_deployable_pct: float = Field(ge=0.0, le=100.0)
    immediate_opening_slice_pct: float = Field(ge=0.0, le=100.0)
    serial_ladder_shape_sum: float = Field(ge=0.0, le=100.0)
    policy_freeze_state: str = "architecture_only_no_policy"


class DownstreamOpeningSnapshot(BaseModel):
    """Opening snapshot owned by downstream opening architecture."""

    model_config = ConfigDict(extra="forbid")
    opening_ids: list[str] = Field(default_factory=list)
    opening_authorisation: OpeningAuthorisationResult | None = None
    policy_freeze_state: str = "architecture_only_no_policy"


class LivePositionState(_DetachedMutableModel):
    """Copy-safe live position state owned by live inventory architecture."""

    model_config = ConfigDict(extra="forbid")
    position_id: str
    source_payload: dict[str, Any] = Field(default_factory=dict)

    @field_validator("source_payload", mode="before")
    @classmethod
    def _reject_transform_required_donor_payload(cls, value):
        return _reject_live_inventory_transform_required_donor_payload(value)


class LiveCapitalState(_DetachedMutableModel):
    """Copy-safe capital-state read owned by live inventory architecture."""

    model_config = ConfigDict(extra="forbid")
    snapshot_id: str
    source_payload: dict[str, Any] = Field(default_factory=dict)

    @field_validator("source_payload", mode="before")
    @classmethod
    def _reject_transform_required_donor_payload(cls, value):
        return _reject_live_inventory_transform_required_donor_payload(value)


class InventoryExposureState(_DetachedMutableModel):
    """Exposure summary derived only from declared position payload fields."""

    model_config = ConfigDict(extra="forbid")
    position_count: int = Field(default=0, ge=0)
    open_position_ids: list[str] = Field(default_factory=list)
    declared_exposure_by_symbol: dict[str, float] = Field(default_factory=dict)


class InventoryStateReceipt(_DetachedMutableModel):
    """Receipt payload for one live inventory snapshot build."""

    model_config = ConfigDict(extra="forbid")
    receipt_id: str
    inventory_id: str
    position_ids: list[str] = Field(default_factory=list)
    capital_snapshot_id: str | None = None
    policy_freeze_state: str = "architecture_only_no_policy"


class DownstreamLiveInventorySnapshot(_DetachedMutableModel):
    """Live inventory snapshot without deployment sizing or broker authority."""

    model_config = ConfigDict(extra="forbid")
    inventory_id: str = "live-inventory"
    live_ids: list[str] = Field(default_factory=list)
    position_states: list[LivePositionState] = Field(default_factory=list)
    capital_state: LiveCapitalState | None = None
    exposure_state: InventoryExposureState = Field(default_factory=InventoryExposureState)
    inventory_receipt: InventoryStateReceipt | None = None
    policy_freeze_state: str = "architecture_only_no_policy"


class DownstreamArchitectureReceipt(BaseModel):
    """Receipt tying downstream opening and inventory snapshots together."""

    model_config = ConfigDict(extra="forbid")
    opening_snapshot: DownstreamOpeningSnapshot
    live_inventory_snapshot: DownstreamLiveInventorySnapshot
    policy_freeze_state: str = "architecture_only_no_policy"


class PlacementReadinessInputTrace(BaseModel):
    """Trace proving placement readiness consumed capital authority output only."""

    model_config = ConfigDict(extra="forbid")
    capital_deployment_receipt_id: str
    serial_candidate_id: str
    placement_constraint_ids: list[str] = Field(default_factory=list)
    broker_boundary_mode: str = "protocol_only"

    @field_validator("broker_boundary_mode")
    @classmethod
    def _require_protocol_only_boundary(cls, value: str) -> str:
        if value != "protocol_only":
            raise ValueError("broker_boundary_mode must be protocol_only")
        return value


class PlacementHandoffMaterial(BaseModel):
    """Non-executing handoff material for a future broker boundary."""

    model_config = ConfigDict(extra="forbid")
    handoff_id: str
    order_intent_preview: dict[str, Any] = Field(default_factory=dict)
    broker_protocol_only: bool = True
    execution_allowed: bool = False

    @field_validator("order_intent_preview", mode="before")
    @classmethod
    def _reject_broker_execution_payload(cls, value):
        return _reject_placement_handoff_broker_execution_payload(value)

    @field_validator("broker_protocol_only")
    @classmethod
    def _require_protocol_only_handoff(cls, value: bool) -> bool:
        if value is not True:
            raise ValueError("broker_protocol_only must remain true")
        return value

    @field_validator("execution_allowed")
    @classmethod
    def _forbid_execution_allowed(cls, value: bool) -> bool:
        if value is not False:
            raise ValueError("execution_allowed must remain false")
        return value


class PlacementReadinessResult(BaseModel):
    """Opening/placement readiness result without concrete broker execution."""

    model_config = ConfigDict(extra="forbid")
    readiness_id: str
    readiness_state: str
    blocked_reasons: list[str] = Field(default_factory=list)
    input_trace: PlacementReadinessInputTrace
    placement_handoff: PlacementHandoffMaterial | None = None
    broker_execution_opened: bool = False
    capital_sizing_recomputed: bool = False

    @field_validator("broker_execution_opened")
    @classmethod
    def _forbid_broker_execution_opened(cls, value: bool) -> bool:
        if value is not False:
            raise ValueError("broker_execution_opened must remain false")
        return value

    @field_validator("capital_sizing_recomputed")
    @classmethod
    def _forbid_capital_sizing_recomputed(cls, value: bool) -> bool:
        if value is not False:
            raise ValueError("capital_sizing_recomputed must remain false")
        return value
