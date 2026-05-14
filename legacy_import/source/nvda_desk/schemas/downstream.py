"""Architecture-only downstream operating-layer contracts.

These contracts reserve lawful homes for the post-serial operating layer without
smuggling behavioural policy into the bootstrap tranche.
"""

from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, Field

from nvda_desk.schemas.checkpoints import CheckpointObservation

from nvda_desk.schemas.execution_records import (
    BrokerFillEventPayload,
    BrokerOrderEventPayload,
    CapitalStateSnapshotPayload,
    ModuleSignalEventPayload,
    ModuleVetoEventPayload,
    PositionInstanceSnapshotPayload,
    PositionSnapshotPayload,
    RiskBlockEventPayload,
)


class DownstreamPolicyStatus(StrEnum):
    """Truthful policy status for architecture-only downstream shells."""

    DEFERRED_POLICY = "deferred_policy"
    DELEGATED_TO_EXISTING_OWNER = "delegated_to_existing_owner"
    RESERVED_HOME_ONLY = "reserved_home_only"
    STATE_ATTACHED_NO_POLICY = "state_attached_no_policy"
    REVIEW_RECEIPT_ONLY = "review_receipt_only"


class DownstreamReadSurface(StrEnum):
    """Named read surfaces for downstream shell receipts."""

    SERIAL_CANDIDATE = "serial_candidate"
    STAGE_LOCAL_HANDOFF = "stage_local_handoff"
    PARALLEL_RISK_LANE = "independent_parallel_risk_lane"
    CAPITAL_DEPLOYMENT_AUTHORITY_DECISION = "capital_deployment_authority_decision"
    CAPITAL_STATE = "capital_state"
    POSITIONS = "positions"
    POSITION_INSTANCES = "position_instances"
    SIGNAL_RECEIPTS = "signal_receipts"
    VETO_RECEIPTS = "veto_receipts"
    RISK_BLOCK_RECEIPTS = "risk_block_receipts"
    ORDER_EVENT_RECEIPTS = "order_event_receipts"
    FILL_EVENT_RECEIPTS = "fill_event_receipts"
    RECOMMENDATION_HISTORY_RESERVATION = "recommendation_history_reservation"


class DownstreamStateSource(StrEnum):
    """Where a downstream state read came from."""

    PROVIDED_SNAPSHOT = "provided_snapshot"
    EXECUTION_RECORDS = "execution_records"
    NOT_AVAILABLE = "not_available"


class DownstreamRecommendationHistoryReservation(BaseModel):
    """Reserved lawful home for every-pass recommendation-history truth."""

    reservation_version: str = "downstream_recommendation_history_reservation.v1"
    reservation_state: str = "reserved_without_first_class_table"
    existing_receipt_tables: list[str] = Field(default_factory=list)
    future_home: str = Field(min_length=1)
    every_pass_receipt_required: bool = True
    notes: list[str] = Field(default_factory=list)


class DownstreamStateSnapshot(BaseModel):
    """Summary of repo-native state attached to downstream shells."""

    snapshot_version: str = "downstream_state_snapshot.v1"
    state_source: DownstreamStateSource
    capital_state_present: bool = False
    open_position_count: int = Field(default=0, ge=0)
    position_instance_count: int = Field(default=0, ge=0)
    signal_receipt_count: int = Field(default=0, ge=0)
    veto_receipt_count: int = Field(default=0, ge=0)
    risk_block_receipt_count: int = Field(default=0, ge=0)
    order_event_count: int = Field(default=0, ge=0)
    fill_event_count: int = Field(default=0, ge=0)
    recommendation_history_reserved: bool = False
    degraded_reason: str | None = None
    notes: list[str] = Field(default_factory=list)


class DownstreamStateReadResult(BaseModel):
    """Explicit repo-native state read result for downstream architecture."""

    read_version: str = "downstream_state_read.v1"
    state_snapshot: DownstreamStateSnapshot
    capital_state: CapitalStateSnapshotPayload | None = None
    positions: list[PositionSnapshotPayload] = Field(default_factory=list)
    position_instances: list[PositionInstanceSnapshotPayload] = Field(default_factory=list)
    signal_receipts: list[ModuleSignalEventPayload] = Field(default_factory=list)
    veto_receipts: list[ModuleVetoEventPayload] = Field(default_factory=list)
    risk_block_receipts: list[RiskBlockEventPayload] = Field(default_factory=list)
    order_event_receipts: list[BrokerOrderEventPayload] = Field(default_factory=list)
    fill_event_receipts: list[BrokerFillEventPayload] = Field(default_factory=list)
    recommendation_history_reservation: DownstreamRecommendationHistoryReservation


class DownstreamShellRequest(BaseModel):
    """Shared request skeleton for downstream architecture shells."""

    request_version: str = "downstream_shell_request.v1"
    lead_playbook_id: str | None = None
    reads_requested: list[DownstreamReadSurface] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)


class OpeningAuthorisationRequest(DownstreamShellRequest):
    """Architecture-only opening-authorisation request shell."""

    capital_deployment_action: str | None = None
    authorised_deployable_pct: float | None = Field(default=None, ge=0.0, le=100.0)


class PlacementReadinessRequest(DownstreamShellRequest):
    """Architecture-only placement-readiness request shell."""


class PlacementHandoffRequest(DownstreamShellRequest):
    """Architecture-only placement-handoff request shell."""


class LivePositionHealthRequest(DownstreamShellRequest):
    """Architecture-only live-position-health request shell."""


class PositionManagementRequest(DownstreamShellRequest):
    """Architecture-only position-management request shell."""


class CapitalRotationRequest(DownstreamShellRequest):
    """Architecture-only capital-rotation request shell."""


class ExitDecisionRequest(DownstreamShellRequest):
    """Architecture-only exit-decision request shell."""


class CloseExecutionRequest(DownstreamShellRequest):
    """Architecture-only close-execution request shell."""


class DownstreamShellResult(BaseModel):
    """Shared result skeleton for architecture-only downstream shells."""

    result_version: str = "downstream_shell_result.v1"
    service_id: str = Field(min_length=1)
    shell_name: str = Field(min_length=1)
    policy_status: DownstreamPolicyStatus
    decision_owner: str | None = None
    reads_from: list[DownstreamReadSurface] = Field(default_factory=list)
    not_read: list[str] = Field(default_factory=list)
    state_snapshot: DownstreamStateSnapshot | None = None
    recommendation_history_reservation: DownstreamRecommendationHistoryReservation | None = None
    notes: list[str] = Field(default_factory=list)
    checkpoint_observations: list[CheckpointObservation] = Field(default_factory=list)


class OpeningAuthorisationResult(DownstreamShellResult):
    """Architecture-only opening-authorisation result shell."""

    recommendation_history_reservation: DownstreamRecommendationHistoryReservation
    authorised_deployable_pct: float | None = Field(default=None, ge=0.0, le=100.0)
    immediate_opening_slice_pct: float | None = Field(default=None, ge=0.0, le=100.0)
    serial_ladder_shape_sum: float | None = Field(default=None, ge=0.0)


class PlacementReadinessResult(DownstreamShellResult):
    """Architecture-only placement-readiness result shell."""


class PlacementHandoffResult(DownstreamShellResult):
    """Architecture-only placement-handoff result shell."""

    recommendation_history_reservation: DownstreamRecommendationHistoryReservation


class LivePositionHealthResult(DownstreamShellResult):
    """Architecture-only live-position-health result shell."""


class PositionManagementResult(DownstreamShellResult):
    """Architecture-only position-management result shell."""


class CapitalRotationResult(DownstreamShellResult):
    """Architecture-only capital-rotation result shell."""


class ExitDecisionResult(DownstreamShellResult):
    """Architecture-only exit-decision result shell."""


class CloseExecutionResult(DownstreamShellResult):
    """Architecture-only close-execution result shell."""


class DownstreamOpeningSnapshot(BaseModel):
    """Aggregate opening-architecture snapshot."""

    snapshot_version: str = "downstream_opening_snapshot.v1"
    opening_authorisation: OpeningAuthorisationResult
    placement_readiness: PlacementReadinessResult
    placement_handoff: PlacementHandoffResult
    notes: list[str] = Field(default_factory=list)


class DownstreamLiveInventorySnapshot(BaseModel):
    """Aggregate live-inventory architecture snapshot."""

    snapshot_version: str = "downstream_live_inventory_snapshot.v1"
    live_position_health: LivePositionHealthResult
    position_management: PositionManagementResult
    capital_rotation: CapitalRotationResult
    exit_decision: ExitDecisionResult
    close_execution: CloseExecutionResult
    notes: list[str] = Field(default_factory=list)


class DownstreamArchitectureReceipt(BaseModel):
    """Review-safe receipt for the downstream architecture bootstrap."""

    receipt_version: str = "downstream_architecture_receipt.v1"
    opening_snapshot: DownstreamOpeningSnapshot
    live_inventory_snapshot: DownstreamLiveInventorySnapshot
    policy_freeze_state: str = "architecture_only_no_policy"
    deferred_domains: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)
