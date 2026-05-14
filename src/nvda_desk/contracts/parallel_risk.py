from __future__ import annotations

from copy import deepcopy
from datetime import datetime
from typing import Any

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


class ParallelRiskCandidateAuditSurface(BaseModel):
    """Bounded candidate-audit surface reserved for later lawful enrichments."""

    model_config = ConfigDict(extra="forbid")

    candidate_id: str | None = None
    semantic_tags: list[str] = Field(default_factory=list)
    audit_state: str = "no_candidate"


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
