from __future__ import annotations

from copy import deepcopy
from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from nvda_desk.contracts.options_flow import OptionsFlowContextInput
from nvda_desk.contracts.packets import DeskModulePacketV3, _deep_merge_dicts
from nvda_desk.contracts.regime import MarketRegimeContextInput
from nvda_desk.contracts.stage_inputs import StageInputBundle
from nvda_desk.contracts.temporal import (
    SourceTemporalStandard,
    TemporalContextInput,
    TemporalContextOutput,
    build_source_temporal_payload,
)
from nvda_desk.packets.dmp_packets import build_dmp_v3_packet, build_parallel_risk_packet

PARALLEL_RISK_BOOTSTRAP_INPUT_DATASCHEMA = (
    "urn:nvda:schema:parallel_risk_lane.bootstrap_input:1.0.0"
)
PARALLEL_RISK_LANE_DATASCHEMA = "urn:nvda:schema:parallel_risk_lane.output:1.0.0"
SERIAL_RUNTIME_TEMPORAL_BOOTSTRAP_SOURCE = "serial_runtime.stage_packets.temporal"
STAGE_INPUT_BUNDLE_TEMPORAL_BOOTSTRAP_SOURCE = "stage_input_bundle.temporal"
STAGE_INPUT_BUNDLE_PARALLEL_RISK_PRIMITIVES_SOURCE = "stage_input_bundle.parallel_risk_primitives"
PARALLEL_RISK_ALLOWED_BOOTSTRAP_SOURCES = (
    SERIAL_RUNTIME_TEMPORAL_BOOTSTRAP_SOURCE,
    STAGE_INPUT_BUNDLE_TEMPORAL_BOOTSTRAP_SOURCE,
    STAGE_INPUT_BUNDLE_PARALLEL_RISK_PRIMITIVES_SOURCE,
)
PARALLEL_RISK_FORBIDDEN_AUTHORITY_KEYS = (
    "authorised_deployable_pct",
    "authorised_notional_usd",
    "position_size",
    "brokerage_order",
    "lead_playbook_id",
    "review_explanation",
    "coefficient_modifier",
)


class _DetachedMutableModel(BaseModel):
    @field_validator("*", mode="before")
    @classmethod
    def _detach_mutable_inputs(cls, value: Any) -> Any:
        return deepcopy(value)


class ParallelRiskStageReadRecord(BaseModel):
    """One bounded stage-read state carried by the parallel-risk lane."""

    model_config = ConfigDict(extra="forbid")

    stage_name: str = Field(min_length=1)
    state: str = Field(min_length=1)
    note: str | None = None


class ParallelRiskEnvironmentAssessment(SourceTemporalStandard):
    """Bounded independent environment-assessment surface for Stage A."""

    model_config = ConfigDict(extra="forbid")

    next_event_time_utc: datetime | None = None
    window_ids: list[str] = Field(default_factory=list)
    window_tags: list[str] = Field(default_factory=list)
    invariant_reads: list[str] = Field(default_factory=list)
    assessment: str = "bounded_environment_assessment"
    assessment_basis: str = "bootstrap_temporal_input"
    notes: list[str] = Field(default_factory=list)


class ParallelRiskEnvelopeContribution(BaseModel):
    """One independent contribution to the parallel-risk envelope state."""

    model_config = ConfigDict(extra="forbid")

    source_family: str = Field(min_length=1)
    state: str = Field(min_length=1)
    reason: str = Field(min_length=1)


class ParallelRiskEnvelope(BaseModel):
    """Independent risk envelope emitted by the parallel-risk lane."""

    model_config = ConfigDict(extra="forbid")

    envelope_state: str = "tight"
    state_ladder: list[str] = Field(default_factory=lambda: ["tight", "broad", "caution", "block"])
    contributions: list[ParallelRiskEnvelopeContribution] = Field(default_factory=list)
    hard_blocks: list[str] = Field(default_factory=list)
    caution_flags: list[str] = Field(default_factory=list)
    decision_authority: str = "independent_risk_envelope_only"

    @model_validator(mode="after")
    def _validate_envelope_ladder(self) -> "ParallelRiskEnvelope":
        if self.envelope_state not in self.state_ladder:
            raise ValueError("parallel_risk_envelope_state_not_in_ladder")
        if self.hard_blocks and self.envelope_state != "block":
            raise ValueError("parallel_risk_hard_blocks_require_block_state")
        return self


class ParallelRiskInputTrace(BaseModel):
    """Trace of the lawful inputs consumed by one parallel-risk evaluation."""

    model_config = ConfigDict(extra="forbid")

    bootstrap_input_packet_id: str = Field(min_length=1)
    bootstrap_source: str = Field(min_length=1)
    admitted_semantic_inputs: list[str] = Field(default_factory=list)
    parent_packet_ids: list[str] = Field(default_factory=list)
    dependency_packet_ids: list[str] = Field(default_factory=list)
    selected_stage_packet_ids: list[str] = Field(default_factory=list)
    forbidden_authority_keys_consumed: list[str] = Field(default_factory=list)
    decision_authority: str = "parallel_risk_input_trace_only"

    @model_validator(mode="after")
    def _validate_parallel_risk_input_trace(self) -> "ParallelRiskInputTrace":
        if self.bootstrap_source not in PARALLEL_RISK_ALLOWED_BOOTSTRAP_SOURCES:
            raise ValueError("parallel_risk_bootstrap_source_not_admitted")
        if self.forbidden_authority_keys_consumed:
            raise ValueError("parallel_risk_forbidden_authority_consumed")
        return self


ParallelRiskConsequencePosture = Literal["observe", "caution", "block"]
ParallelRiskAtomStateValue = Literal["inactive", "observe", "caution", "block"]
ParallelRiskEnvelopeStateValue = Literal["tight", "broad", "observe", "caution", "block", "unknown"]
ParallelRiskSignalKind = Literal["raw", "derived", "metadata", "config", "trace"]
ParallelRiskFreshnessState = Literal["fresh", "ageing", "stale", "unknown"]
ParallelRiskSignalPresenceState = Literal[
    "present", "missing", "quarantined", "rejected", "not_expected"
]
ParallelRiskMissingImpact = Literal[
    "none", "lowers_confidence", "disables_atom", "forces_caution", "forces_block"
]


ParallelRiskSignalInventoryStatus = Literal[
    "available_now",
    "upstream_but_not_projected",
    "missing",
    "deferred",
    "excluded",
]
ParallelRiskRuntimeUsePermission = Literal[
    "runtime_allowed_from_typed_inputs_only",
    "not_runtime_allowed",
    "not_runtime_allowed_until_typed_projection",
    "excluded_from_prl_runtime",
]


class AuthorityFlags(BaseModel):
    """Default-deny authority flags for enriched parallel-risk profile contracts."""

    model_config = ConfigDict(extra="forbid")

    candidate_formation_allowed: bool = False
    playbook_selection_allowed: bool = False
    capital_sizing_allowed: bool = False
    broker_execution_allowed: bool = False
    serial_stage_mutation_allowed: bool = False
    review_judgement_authority: bool = False
    direct_workbook_runtime_read_allowed: bool = False

    @model_validator(mode="after")
    def _validate_default_deny_authority(self) -> "AuthorityFlags":
        if any(
            (
                self.candidate_formation_allowed,
                self.playbook_selection_allowed,
                self.capital_sizing_allowed,
                self.broker_execution_allowed,
                self.serial_stage_mutation_allowed,
                self.review_judgement_authority,
                self.direct_workbook_runtime_read_allowed,
            )
        ):
            raise ValueError("parallel_risk_authority_flags_must_remain_false")
        return self


class ParallelRiskExpectedSignalRecord(BaseModel):
    """One workbook-governed expected signal promoted to runtime-safe config."""

    model_config = ConfigDict(extra="forbid")

    signal_id: str = Field(min_length=1)
    signal_family: str = Field(min_length=1)
    inventory_status: ParallelRiskSignalInventoryStatus
    raw_derived_config_trace_classification: str = Field(min_length=1)
    workbook_lineage_refs: list[str] = Field(default_factory=list)
    runtime_contract_target: str = Field(min_length=1)
    lawful_prl_use: str = Field(min_length=1)
    runtime_use_permission: ParallelRiskRuntimeUsePermission
    required_for_current_atom: bool = False
    missing_handling: str = Field(min_length=1)
    unavailable_handling: str = Field(min_length=1)
    exclusion_reason: str | None = None
    status_rationale: str = Field(min_length=1)
    risk_semantics_note: str = Field(min_length=1)
    label_ref: str | None = None
    description_ref: str | None = None
    promotion_record_key: str = Field(min_length=1)

    @model_validator(mode="after")
    def _validate_expected_signal_record(self) -> "ParallelRiskExpectedSignalRecord":
        if not self.workbook_lineage_refs:
            raise ValueError("parallel_risk_signal_inventory_lineage_required")
        if self.inventory_status == "available_now":
            if self.runtime_use_permission != "runtime_allowed_from_typed_inputs_only":
                raise ValueError("available_parallel_risk_signal_requires_typed_runtime_permission")
        else:
            if self.runtime_use_permission == "runtime_allowed_from_typed_inputs_only":
                raise ValueError("unavailable_parallel_risk_signal_must_not_be_runtime_allowed")
        if self.inventory_status == "excluded":
            if self.required_for_current_atom:
                raise ValueError("excluded_parallel_risk_signal_cannot_be_required")
            if not self.exclusion_reason:
                raise ValueError("excluded_parallel_risk_signal_requires_reason")
        return self


class ParallelRiskSignalInventoryDocument(BaseModel):
    """Runtime-safe promoted PRL expected-signal inventory document."""

    model_config = ConfigDict(extra="forbid")

    inventory_id: str = Field(min_length=1)
    schema_version: str = Field(min_length=1)
    source_workbook_path: str = Field(min_length=1)
    source_workbook_sha256: str = Field(min_length=64, max_length=64)
    source_workbook_sheet: str = Field(min_length=1)
    source_workbook_sheet_range: str = Field(min_length=1)
    generated_from_workbook_tab: bool = True
    direct_workbook_runtime_read_allowed: bool = False
    authority_flags: AuthorityFlags = Field(default_factory=lambda: AuthorityFlags())
    records: list[ParallelRiskExpectedSignalRecord] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def _validate_expected_signal_inventory_document(
        self,
    ) -> "ParallelRiskSignalInventoryDocument":
        if self.direct_workbook_runtime_read_allowed:
            raise ValueError("parallel_risk_inventory_runtime_workbook_read_forbidden")
        if not self.generated_from_workbook_tab:
            raise ValueError("parallel_risk_inventory_requires_workbook_tab_lineage")
        record_ids = [record.signal_id for record in self.records]
        if len(record_ids) != len(set(record_ids)):
            raise ValueError("parallel_risk_inventory_signal_ids_must_be_unique")
        if not self.records:
            raise ValueError("parallel_risk_inventory_requires_records")
        required_supported = {
            "source_time_utc",
            "scheduled_event_window_active",
            "vix_level",
            "spot_price",
            "front_dte",
            "next_dte",
        }
        missing_supported = sorted(required_supported - set(record_ids))
        if missing_supported:
            raise ValueError(
                f"parallel_risk_inventory_missing_supported_signals: {missing_supported}"
            )
        return self

    def record_map(self) -> dict[str, ParallelRiskExpectedSignalRecord]:
        """Return expected signal records keyed by signal id."""

        return {record.signal_id: record for record in self.records}

    def required_runtime_records(self) -> list[ParallelRiskExpectedSignalRecord]:
        """Return records demanded by current atoms and lawfully available after promotion."""

        return [
            record
            for record in self.records
            if record.required_for_current_atom
            and record.inventory_status == "available_now"
            and record.runtime_use_permission == "runtime_allowed_from_typed_inputs_only"
        ]

    def unavailable_records(self) -> list[ParallelRiskExpectedSignalRecord]:
        """Return non-excluded records that are unavailable to runtime now."""

        return [
            record
            for record in self.records
            if record.inventory_status in {"upstream_but_not_projected", "missing", "deferred"}
        ]


def parallel_risk_signal_inventory_document_from_dict(
    payload: dict[str, Any],
) -> ParallelRiskSignalInventoryDocument:
    """Build and validate one promoted PRL signal-inventory document."""

    return ParallelRiskSignalInventoryDocument(**payload)


class SignalSnapshotEntry(BaseModel):
    """One signal-like value or absence recorded for a minute-level risk profile."""

    model_config = ConfigDict(extra="forbid")

    signal_id: str = Field(min_length=1)
    signal_family: str = Field(min_length=1)
    raw_or_derived: ParallelRiskSignalKind
    value: Any | None = None
    units: str | None = None
    source_time_utc: datetime | None = None
    captured_at_utc: datetime | None = None
    persisted_at_utc: datetime | None = None
    freshness_state: ParallelRiskFreshnessState = "unknown"
    freshness_reason: str | None = None
    lineage_refs: list[str] = Field(default_factory=list)
    source_ids: list[str] = Field(default_factory=list)
    workbook_lineage_refs: list[str] = Field(default_factory=list)
    used_by_risk_atoms: list[str] = Field(default_factory=list)
    missing_or_quarantined: ParallelRiskSignalPresenceState = "present"
    rejection_reason: str | None = None
    lawful_prl_use_allowed: bool = True
    lawful_prl_use_reason: str | None = None


class MissingSignalRegisterEntry(BaseModel):
    """Metadata-only record for an expected signal absent from the PRL input surface."""

    model_config = ConfigDict(extra="forbid")

    signal_id: str = Field(min_length=1)
    signal_family: str = Field(min_length=1)
    expected_reason: str = Field(min_length=1)
    missing_reason: str = Field(min_length=1)
    impact_on_profile: ParallelRiskMissingImpact = "none"
    source_refs: list[str] = Field(default_factory=list)
    expected_signal_inventory_ref: str | None = None
    workbook_lineage_refs: list[str] = Field(default_factory=list)


class FreshnessRegisterEntry(BaseModel):
    """Contract record for signal/source freshness state; calculation lives elsewhere."""

    model_config = ConfigDict(extra="forbid")

    signal_id: str = Field(min_length=1)
    source_time_utc: datetime | None = None
    captured_at_utc: datetime | None = None
    persisted_at_utc: datetime | None = None
    generated_at_utc: datetime | None = None
    max_allowed_age_seconds: int | None = Field(default=None, ge=0)
    observed_age_seconds: int | None = Field(default=None, ge=0)
    freshness_state: ParallelRiskFreshnessState = "unknown"
    impact_on_profile: str | None = None
    source_refs: list[str] = Field(default_factory=list)


class EventProximityRegisterEntry(BaseModel):
    """Contract record for projected event proximity without trade authority."""

    model_config = ConfigDict(extra="forbid")

    event_id: str = Field(min_length=1)
    event_type: str = Field(min_length=1)
    starts_at_utc: datetime | None = None
    ends_at_utc: datetime | None = None
    proximity_seconds: int | None = None
    materiality: str | None = None
    materiality_rank: int | None = None
    runtime_tags: list[str] = Field(default_factory=list)
    evaluation_tags: list[str] = Field(default_factory=list)
    risk_interpretation: str = Field(min_length=1)
    source_refs: list[str] = Field(default_factory=list)


class RiskAtomState(BaseModel):
    """One contract-only environmental risk atom state, not a trade action."""

    model_config = ConfigDict(extra="forbid")

    risk_atom_id: str = Field(min_length=1)
    name: str | None = None
    family: str = Field(min_length=1)
    state: ParallelRiskAtomStateValue = "inactive"
    intensity: float = Field(default=0.0, ge=0.0, le=1.0)
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    trigger_condition: str = Field(min_length=1)
    observable_cues: list[dict[str, Any]] = Field(default_factory=list)
    calculation_basis: dict[str, Any] = Field(default_factory=dict)
    source_refs: list[str] = Field(default_factory=list)
    time_sensitivity: dict[str, Any] = Field(default_factory=dict)
    trader_cognition_update: dict[str, Any] = Field(default_factory=dict)
    why_this_is_risk_not_play: str = Field(min_length=1)


class RiskFamilyState(BaseModel):
    """Aggregated descriptive state for one risk family."""

    model_config = ConfigDict(extra="forbid")

    family: str = Field(min_length=1)
    state: ParallelRiskAtomStateValue = "inactive"
    intensity: float = Field(default=0.0, ge=0.0, le=1.0)
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    dominant_atoms: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)


class ContributionBreakdownEntry(BaseModel):
    """Traceable descriptive contribution to the minute-level risk profile."""

    model_config = ConfigDict(extra="forbid")

    contribution_id: str = Field(min_length=1)
    family: str = Field(min_length=1)
    risk_atom_id: str | None = None
    state: ParallelRiskAtomStateValue = "observe"
    intensity_delta: float = Field(default=0.0, ge=0.0, le=1.0)
    reason: str = Field(min_length=1)
    source_signal_ids: list[str] = Field(default_factory=list)
    source_refs: list[str] = Field(default_factory=list)


class ParallelRiskMinuteProfile(_DetachedMutableModel):
    """Contract-only minute-level environmental risk profile for the PRL."""

    model_config = ConfigDict(extra="forbid")

    packet_id: str = Field(min_length=1)
    packet_schema_version: str = "parallel_risk_minute_profile.v1"
    lane_id: str = "parallel_risk_lane"
    symbol: str = Field(min_length=1)
    source_time_utc: datetime
    generated_at_utc: datetime
    runtime_bar_time_utc: datetime | None = None
    session_state: str = "unknown"
    risk_envelope_state: ParallelRiskEnvelopeStateValue = "unknown"
    active_risk_atoms: list[RiskAtomState] = Field(default_factory=list)
    watched_risk_atoms: list[RiskAtomState] = Field(default_factory=list)
    risk_family_states: list[RiskFamilyState] = Field(default_factory=list)
    signal_snapshot: list[SignalSnapshotEntry] = Field(default_factory=list)
    missing_signal_register: list[MissingSignalRegisterEntry] = Field(default_factory=list)
    freshness_register: list[FreshnessRegisterEntry] = Field(default_factory=list)
    event_proximity_register: list[EventProximityRegisterEntry] = Field(default_factory=list)
    contribution_breakdown: list[ContributionBreakdownEntry] = Field(default_factory=list)
    hard_blocks: list[str] = Field(default_factory=list)
    caution_flags: list[str] = Field(default_factory=list)
    uncertainty_summary: dict[str, Any] = Field(default_factory=dict)
    authority_flags: AuthorityFlags = Field(default_factory=AuthorityFlags)
    expected_signal_inventory_ref: str | None = None
    workbook_lineage_refs: list[str] = Field(default_factory=list)
    vocabulary_dictionary_refs: list[str] = Field(default_factory=list)
    description_template_id: str | None = None
    description_vocabulary_refs: list[str] = Field(default_factory=list)
    mechanical_summary: dict[str, Any] = Field(default_factory=dict)
    lineage: dict[str, Any] = Field(default_factory=dict)
    open_unresolved_signals: list[dict[str, Any]] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)


class ParallelRiskDescriptionTemplateRef(BaseModel):
    """Metadata-only reference to a deterministic PRL description template."""

    model_config = ConfigDict(extra="forbid")

    template_id: str = Field(min_length=1)
    template_registry_ref: str = Field(min_length=1)
    vocabulary_dictionary_refs: list[str] = Field(default_factory=list)
    description_vocabulary_refs: list[str] = Field(default_factory=list)
    deterministic_template_only: bool = True
    free_form_generation_allowed: bool = False
    trade_advice_allowed: bool = False
    capital_or_order_language_allowed: bool = False

    @model_validator(mode="after")
    def _validate_description_template_ref(self) -> "ParallelRiskDescriptionTemplateRef":
        if not self.deterministic_template_only:
            raise ValueError("parallel_risk_description_template_ref_must_remain_bounded")
        if (
            self.free_form_generation_allowed
            or self.trade_advice_allowed
            or self.capital_or_order_language_allowed
        ):
            raise ValueError("parallel_risk_description_template_ref_must_remain_bounded")
        return self


class ParallelRiskFragilityDimension(BaseModel):
    """One descriptive candidate fragility dimension without sizing authority."""

    model_config = ConfigDict(extra="forbid")

    dimension_id: str = Field(min_length=1)
    score: float = Field(ge=0.0, le=1.0)
    reason: str = Field(min_length=1)


class ParallelRiskCandidateAuditSurface(BaseModel):
    """Bounded candidate-audit surface with descriptive semantics only."""

    model_config = ConfigDict(extra="forbid")

    candidate_id: str | None = None
    semantic_tags: list[str] = Field(default_factory=list)
    audit_state: str = "no_candidate"
    consequence_posture: ParallelRiskConsequencePosture = "observe"
    fragility_dimensions: list[ParallelRiskFragilityDimension] = Field(default_factory=list)
    descriptive_semantics: list[str] = Field(default_factory=list)
    risk_event_ids: list[str] = Field(default_factory=list)
    decision_authority: str = "parallel_risk_candidate_audit_only"
    capital_sizing_allowed: bool = False


class ParallelRiskPolicyDecision(BaseModel):
    """Risk-gateway observation record for one candidate-policy evaluation."""

    model_config = ConfigDict(extra="forbid")

    decision_id: str = Field(min_length=1)
    policy_id: str = Field(min_length=1)
    candidate: ParallelRiskCandidateAuditSurface
    decision_authority: str = "risk_gateway_observation_only"
    capital_sizing_allowed: bool = False


class ParallelRiskPreparationPacket(BaseModel):
    """Bootstrap payload admitted at the Module 8-owned parallel-risk input seam."""

    model_config = ConfigDict(extra="forbid")

    lane_id: str = "parallel_risk_lane"
    temporal_input: TemporalContextInput
    regime_input: MarketRegimeContextInput = Field(default_factory=MarketRegimeContextInput)
    options_flow_input: OptionsFlowContextInput = Field(default_factory=OptionsFlowContextInput)
    invariant_reads: list[str] = Field(default_factory=list)
    stage_read_state: list[ParallelRiskStageReadRecord] = Field(default_factory=list)
    bootstrap_source: str = STAGE_INPUT_BUNDLE_TEMPORAL_BOOTSTRAP_SOURCE
    serial_spine_preserved: bool = True


class ParallelRiskLanePacket(_DetachedMutableModel):
    """Bounded parallel-risk output payload carried through canonical DMPV3."""

    model_config = ConfigDict(extra="forbid")

    lane_id: str = "parallel_risk_lane"
    serial_spine_preserved: bool = True
    co_resident_from_session_start: bool = True
    arbiter_active: bool = False
    environment_assessment: ParallelRiskEnvironmentAssessment
    risk_envelope: ParallelRiskEnvelope = Field(default_factory=ParallelRiskEnvelope)
    input_trace: ParallelRiskInputTrace
    invariant_reads: list[str] = Field(default_factory=list)
    stage_read_state: list[ParallelRiskStageReadRecord] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)


class ParallelRiskObservationRecord(SourceTemporalStandard):
    """Append-only observation record for the parallel-risk write-only persistence seam."""

    model_config = ConfigDict(extra="forbid")

    observation_id: str = Field(min_length=1)
    input_packet_ids: list[str] = Field(default_factory=list)
    output_packet_ids: list[str] = Field(default_factory=list)
    traceid: str = Field(min_length=1)
    runid: str = Field(min_length=1)
    scenarioid: str = Field(min_length=1)
    parentids: list[str] = Field(default_factory=list)
    dependencyids: list[str] = Field(default_factory=list)
    bounded_observation_payload: dict[str, Any] = Field(default_factory=dict)


class ParallelRiskObservationAppendReceipt(BaseModel):
    """Receipt returned after one append-only parallel-risk observation write."""

    model_config = ConfigDict(extra="forbid")

    observation_id: str = Field(min_length=1)
    appended: bool = True
    stored_input_packet_ids: list[str] = Field(default_factory=list)
    stored_output_packet_ids: list[str] = Field(default_factory=list)


NON_TEMPORAL_STAGE_NOTES = {
    "regime": "serial runtime regime packet exists in the boundary product but is not admitted for live semantic read in this tranche",
    "options_flow": "serial runtime options-flow packet exists in the boundary product but is not admitted for live semantic read in this tranche",
    "posture": "serial runtime posture packet exists in the boundary product but is not admitted for live semantic read in this tranche",
    "eligibility": "serial runtime eligibility packet exists in the boundary product but is not admitted for live semantic read in this tranche",
    "execution": "serial runtime execution packet exists in the boundary product but is not admitted for live semantic read in this tranche",
}


def bootstrap_stage_read_state(
    *,
    bootstrap_source: str = STAGE_INPUT_BUNDLE_TEMPORAL_BOOTSTRAP_SOURCE,
) -> list[ParallelRiskStageReadRecord]:
    """Return the truthful bootstrap stage-read state for the admitted source."""

    if bootstrap_source == SERIAL_RUNTIME_TEMPORAL_BOOTSTRAP_SOURCE:
        return [
            ParallelRiskStageReadRecord(
                stage_name="temporal",
                state="bootstrap_input_used",
                note="selected temporal stage packet admitted for live semantic read in this tranche",
            ),
            *[
                ParallelRiskStageReadRecord(
                    stage_name=stage_name,
                    state="not_admitted_for_live_semantic_read",
                    note=note,
                )
                for stage_name, note in NON_TEMPORAL_STAGE_NOTES.items()
            ],
            ParallelRiskStageReadRecord(
                stage_name="review",
                state="not_yet_available",
                note="review remains downstream of the parallel-risk lane",
            ),
        ]

    if bootstrap_source == STAGE_INPUT_BUNDLE_PARALLEL_RISK_PRIMITIVES_SOURCE:
        return [
            ParallelRiskStageReadRecord(
                stage_name="temporal",
                state="bootstrap_input_used",
                note="Stage Input Bundle temporal primitive admitted for independent risk-envelope input",
            ),
            ParallelRiskStageReadRecord(
                stage_name="regime",
                state="bootstrap_input_used",
                note="Stage Input Bundle regime primitive admitted for independent risk-envelope input",
            ),
            ParallelRiskStageReadRecord(
                stage_name="options_flow",
                state="bootstrap_input_used",
                note="Stage Input Bundle options-flow primitive admitted for independent risk-envelope input",
            ),
            ParallelRiskStageReadRecord(
                stage_name="posture",
                state="not_yet_available",
                note="posture is downstream of the bootstrap path",
            ),
            ParallelRiskStageReadRecord(
                stage_name="eligibility",
                state="not_yet_available",
                note="eligibility is downstream of the bootstrap path",
            ),
            ParallelRiskStageReadRecord(
                stage_name="execution",
                state="not_yet_available",
                note="execution is downstream of the bootstrap path",
            ),
            ParallelRiskStageReadRecord(
                stage_name="review",
                state="not_yet_available",
                note="review remains downstream of the parallel-risk lane",
            ),
        ]

    return [
        ParallelRiskStageReadRecord(
            stage_name="temporal",
            state="bootstrap_input_used",
            note="accepted baseline exposes temporal input through Stage Input Bundle only",
        ),
        ParallelRiskStageReadRecord(
            stage_name="regime",
            state="not_yet_available",
            note="no lawful native upstream regime packet exists in the accepted baseline",
        ),
        ParallelRiskStageReadRecord(
            stage_name="options_flow",
            state="not_yet_available",
            note="no lawful native upstream options packet exists in the accepted baseline",
        ),
        ParallelRiskStageReadRecord(
            stage_name="posture",
            state="not_yet_available",
            note="posture is downstream of the bootstrap path",
        ),
        ParallelRiskStageReadRecord(
            stage_name="eligibility",
            state="not_yet_available",
            note="eligibility is downstream of the bootstrap path",
        ),
        ParallelRiskStageReadRecord(
            stage_name="execution",
            state="not_yet_available",
            note="execution is downstream of the bootstrap path",
        ),
        ParallelRiskStageReadRecord(
            stage_name="review",
            state="not_yet_available",
            note="review remains downstream of the parallel-risk lane",
        ),
    ]


def build_parallel_risk_bootstrap_input_packet(
    *,
    stage_input_bundle: StageInputBundle,
    packet_id: str,
    emitted_at: datetime | None = None,
    traceid: str | None = None,
    runid: str | None = None,
    scenarioid: str | None = None,
    derivedfrom: str | None = None,
    sourceartifactids: list[str] | None = None,
    inputfingerprint: str | None = None,
    dmpextensions: dict[str, Any] | None = None,
) -> DeskModulePacketV3:
    """Wrap admitted Stage Input Bundle truth into the lawful Module 8 bootstrap packet."""

    payload = ParallelRiskPreparationPacket(
        temporal_input=stage_input_bundle.temporal,
        regime_input=stage_input_bundle.regime,
        options_flow_input=stage_input_bundle.options_flow,
        invariant_reads=[
            "serial_spine_preserved",
            "parallel_risk_lane_is_independent_and_additive",
            "module_8_bootstrap_adapter_only",
        ],
        stage_read_state=bootstrap_stage_read_state(
            bootstrap_source=STAGE_INPUT_BUNDLE_PARALLEL_RISK_PRIMITIVES_SOURCE,
        ),
        bootstrap_source=STAGE_INPUT_BUNDLE_PARALLEL_RISK_PRIMITIVES_SOURCE,
    )
    return build_dmp_v3_packet(
        packet_id=packet_id,
        dataschema=PARALLEL_RISK_BOOTSTRAP_INPUT_DATASCHEMA,
        data=payload,
        packetrole="parallel_risk_bootstrap_input",
        module_id="parallel_risk_lane_bootstrap_adapter",
        grammar_role="parallel_risk_lane",
        behaviour_class="bootstrap_adapter_output",
        stage_name="parallel_risk_lane",
        emitted_at=emitted_at,
        traceid=traceid,
        runid=runid,
        scenarioid=scenarioid,
        derivedfrom=derivedfrom,
        sourceartifactids=sourceartifactids,
        inputfingerprint=inputfingerprint,
        summary_headline="parallel-risk bootstrap input emitted",
        summary_keyflags=["stage_a_bootstrap", "module_8_owned_adapter"],
        summary_humanstate="bootstrap_ready",
        dmpextensions=dmpextensions,
    )


def build_parallel_risk_bootstrap_input_packet_from_temporal_stage_packet(
    *,
    temporal_stage_packet: DeskModulePacketV3,
    packet_id: str,
    emitted_at: datetime | None = None,
    traceid: str | None = None,
    runid: str | None = None,
    scenarioid: str | None = None,
    derivedfrom: str | None = None,
    sourceartifactids: list[str] | None = None,
    inputfingerprint: str | None = None,
    dmpextensions: dict[str, Any] | None = None,
) -> DeskModulePacketV3:
    """Translate the selected serial-runtime temporal stage packet into the bootstrap input packet."""

    temporal_output = TemporalContextOutput.model_validate(temporal_stage_packet.data)
    payload = ParallelRiskPreparationPacket(
        temporal_input=_build_bootstrap_temporal_input_from_stage_output(temporal_output),
        invariant_reads=[
            "serial_spine_preserved",
            "parallel_risk_lane_is_independent_and_additive",
            "module_8_bootstrap_adapter_only",
        ],
        stage_read_state=bootstrap_stage_read_state(
            bootstrap_source=SERIAL_RUNTIME_TEMPORAL_BOOTSTRAP_SOURCE,
        ),
        bootstrap_source=SERIAL_RUNTIME_TEMPORAL_BOOTSTRAP_SOURCE,
    )
    return build_dmp_v3_packet(
        packet_id=packet_id,
        dataschema=PARALLEL_RISK_BOOTSTRAP_INPUT_DATASCHEMA,
        data=payload,
        packetrole="parallel_risk_bootstrap_input",
        module_id="parallel_risk_lane_bootstrap_adapter",
        grammar_role="parallel_risk_lane",
        behaviour_class="bootstrap_adapter_output",
        stage_name="parallel_risk_lane",
        emitted_at=emitted_at or temporal_stage_packet.emitted_at,
        traceid=traceid or temporal_stage_packet.traceid,
        runid=runid or temporal_stage_packet.runid,
        scenarioid=scenarioid or temporal_stage_packet.scenarioid,
        parentids=[temporal_stage_packet.packet_id],
        dependencyids=[temporal_stage_packet.packet_id],
        derivedfrom=derivedfrom or "parallel_risk_bootstrap_from_serial_runtime_temporal_packet",
        sourceartifactids=sourceartifactids
        or list(temporal_stage_packet.lineage.sourceartifactids),
        inputfingerprint=inputfingerprint or temporal_stage_packet.lineage.inputfingerprint,
        summary_headline="parallel-risk bootstrap input emitted",
        summary_keyflags=["stage_a_bootstrap", "module_8_owned_adapter"],
        summary_humanstate="bootstrap_ready",
        dmpextensions=dmpextensions,
    )


def build_parallel_risk_lane_output_packet(
    *,
    packet_id: str,
    payload: ParallelRiskLanePacket,
    emitted_at: datetime | None = None,
    traceid: str | None = None,
    runid: str | None = None,
    scenarioid: str | None = None,
    parentids: list[str] | None = None,
    dependencyids: list[str] | None = None,
    derivedfrom: str | None = None,
    sourceartifactids: list[str] | None = None,
    inputfingerprint: str | None = None,
    dmpextensions: dict[str, Any] | None = None,
) -> DeskModulePacketV3:
    """Emit one lawful Stage A parallel-risk output packet through canonical DMPV3."""

    merged_extensions = _deep_merge_dicts(
        {
            "nvda": {
                "parallel_risk": {
                    "stage_b": "reserved_without_lawful_upstream_packets",
                    "stage_c": "reserved_without_lawful_upstream_packets",
                }
            }
        },
        dict(dmpextensions or {}),
    )
    return build_parallel_risk_packet(
        packet_id=packet_id,
        dataschema=PARALLEL_RISK_LANE_DATASCHEMA,
        data=payload,
        emitted_at=emitted_at,
        traceid=traceid,
        runid=runid,
        scenarioid=scenarioid,
        parentids=parentids,
        dependencyids=dependencyids,
        derivedfrom=derivedfrom,
        sourceartifactids=sourceartifactids,
        inputfingerprint=inputfingerprint,
        summary_headline="parallel-risk stage-a output emitted",
        summary_keyflags=["stage_a_bootstrap", "environment_assessment_only"],
        dmpextensions=merged_extensions,
    )


def _build_bootstrap_temporal_input_from_stage_output(
    temporal_output: TemporalContextOutput,
) -> TemporalContextInput:
    """Project the selected temporal stage output into the existing bootstrap payload shape."""

    return TemporalContextInput(
        **build_source_temporal_payload(
            source_time_utc=temporal_output.source_time_utc,
            source_date=temporal_output.source_date,
            source_time_raw=temporal_output.source_time_raw,
            source_time_kind=temporal_output.source_time_kind,
            source_timezone_raw=temporal_output.source_timezone_raw,
            captured_at_utc=temporal_output.captured_at_utc,
            persisted_at_utc=temporal_output.persisted_at_utc,
            source_provider=temporal_output.source_provider,
            source_channel=temporal_output.source_channel,
            time_granularity=temporal_output.time_granularity,
        ),
        next_event_time_utc=temporal_output.next_event_time_utc,
        windows=list(temporal_output.windows),
    )
