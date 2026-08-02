"""Immutable M00 application-shell contracts for bounded alpha composition."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from decimal import Decimal
from hashlib import sha256
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from nvda_desk.contracts.packets import DeskModulePacketV3, DmpV3ExecutionContext
from nvda_desk.m01_source_admission import (
    SourceAdmissionAccepted,
    SourceAdmissionRequest,
    SourceAdmissionResult,
    SourceNonAdmission,
)
from nvda_desk.m02_financial_calendar import (
    CalendarFieldResolutionPolicy,
    CalendarProjection,
    FinancialCalendarSnapshot,
)
from nvda_desk.m03_preparation import (
    DerivationReceipt,
    FieldResolutionReceipt,
    PreparedDataEnvelope,
    PreparedRuntimePayloadV1,
)
from nvda_desk.m05_serial_cognition import SerialCandidate, StageContext, StageInput
from nvda_desk.m06_parallel_risk import ParallelRiskAssessment, ParallelRiskInput
from nvda_desk.m07_coefficient_modifier_authority import ModifierApplicationReceipt
from nvda_desk.m09_capital_authority import (
    CapitalDeploymentDecision,
    CapitalDeploymentPolicy,
    CapitalDeploymentReceipt,
    CapitalState,
    FinalRiskDecision,
    FinalRiskJoinPolicy,
)
from nvda_desk.m10_execution_gateway import (
    ExecutionReceipt,
    PlacementIntent,
    PlacementPolicy,
)
from nvda_desk.m11_portfolio_lifecycle import (
    FillReconciliationReceipt,
    PortfolioSnapshot,
)
from nvda_desk.m12_evidence_replay import ReplayEnvelope

ApplicationOutcome = Literal[
    "serial_stand_down",
    "serial_withheld",
    "serial_rejected",
    "block",
    "no_trade",
    "paper_filled",
]


def _canonical(value: Any) -> Any:
    if isinstance(value, datetime):
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("datetime_must_be_timezone_aware")
        return value.astimezone(UTC).isoformat().replace("+00:00", "Z")
    if isinstance(value, Decimal):
        if not value.is_finite():
            raise ValueError("decimal_must_be_finite")
        return "0" if value == 0 else format(value.normalize(), "f")
    if isinstance(value, bytes):
        return {"sha256": sha256(value).hexdigest(), "length": len(value)}
    if isinstance(value, BaseModel):
        return _canonical(value.model_dump(mode="python"))
    if isinstance(value, dict):
        return {str(key): _canonical(item) for key, item in sorted(value.items())}
    if isinstance(value, (tuple, list)):
        return [_canonical(item) for item in value]
    return value


def semantic_fingerprint(value: Any) -> str:
    return sha256(
        json.dumps(_canonical(value), sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def _require_utc(value: datetime, reason: str) -> datetime:
    if value.tzinfo is None or value.utcoffset() != UTC.utcoffset(value):
        raise ValueError(reason)
    return value


class PacketEmissionSpec(BaseModel):
    """One caller-supplied packet identity and occurrence boundary."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    packet_id: str = Field(min_length=1)
    emitted_at_utc: datetime
    module_version: str = Field(min_length=1)
    module_instance_id: str = Field(min_length=1)

    @field_validator("emitted_at_utc")
    @classmethod
    def _emitted_at_utc(cls, value: datetime) -> datetime:
        return _require_utc(value, "packet_emission_time_must_be_utc")


class CalendarProjectionRequest(BaseModel):
    """Exact M02 projection request carried by one upstream operation."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    snapshot: FinancialCalendarSnapshot
    policy: CalendarFieldResolutionPolicy
    projection_id: str = Field(min_length=1)


class PreparationSpec(BaseModel):
    """Exact caller-owned M03 builder facts excluding owner-produced lineage."""

    model_config = ConfigDict(extra="forbid", frozen=True, allow_inf_nan=False)

    input_schema_versions: tuple[tuple[str, str], ...] = Field(min_length=1)
    schema_version: str = Field(min_length=1)
    preparation_policy_version: str = Field(min_length=1)
    alignment_policy_version: str = Field(min_length=1)
    fingerprint_policy_version: str = Field(min_length=1)
    canonicalisation_version: str = Field(min_length=1)
    derivation_versions: tuple[tuple[str, str], ...] = ()
    effective_at_utc: datetime
    payload: PreparedRuntimePayloadV1
    payload_schema_version: Literal["1.0.0"]
    field_resolution_receipts: tuple[FieldResolutionReceipt, ...] = ()
    derivation_receipts: tuple[DerivationReceipt, ...] = ()
    validation_state: Literal["valid", "degraded"] = "valid"
    completeness_state: Literal["complete", "degraded"] = "complete"
    limitations: tuple[str, ...] = ()
    failed_mandatory_transformations: tuple[str, ...] = ()
    missing_optional_enrichments: tuple[str, ...] = ()
    parent_prepared_ids: tuple[str, ...] = ()

    @field_validator("input_schema_versions", "derivation_versions", mode="before")
    @classmethod
    def _version_pairs(cls, value: Any) -> tuple[tuple[str, str], ...]:
        pairs = (
            tuple(value.items())
            if isinstance(value, dict)
            else tuple(tuple(item) for item in value)
        )
        if any(len(item) != 2 or not item[0] or not item[1] for item in pairs):
            raise ValueError("upstream_version_mapping_entries_must_be_named")
        if len({str(item[0]) for item in pairs}) != len(pairs):
            raise ValueError("duplicate_upstream_version_mapping_key")
        return tuple(sorted((str(key), str(version)) for key, version in pairs))

    @field_validator("effective_at_utc")
    @classmethod
    def _effective_time(cls, value: datetime) -> datetime:
        return _require_utc(value, "upstream_preparation_time_must_be_utc")


class UpstreamPreparationCommand(BaseModel):
    """One canonical application request delegating M01, M02 and M03 work."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    command_id: str = Field(min_length=1)
    source_requests: tuple[SourceAdmissionRequest, ...] = Field(min_length=1)
    calendar_requests: tuple[CalendarProjectionRequest, ...] = Field(min_length=1)
    preparation: PreparationSpec


UpstreamPreparationStatus = Literal[
    "prepared",
    "source_not_admitted",
    "calendar_withheld",
]


class UpstreamPreparationReceipt(BaseModel):
    """Immutable aggregation of exact M01/M02 owner outputs and optional M03 output."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    receipt_id: str = Field(min_length=1)
    contract_version: Literal["1.0.0"] = "1.0.0"
    semantic_fingerprint: str = Field(pattern=r"^[0-9a-f]{64}$")
    command_id: str = Field(min_length=1)
    status: UpstreamPreparationStatus
    source_results: tuple[SourceAdmissionAccepted | SourceNonAdmission, ...] = Field(min_length=1)
    calendar_projections: tuple[CalendarProjection, ...] = ()
    prepared_data: PreparedDataEnvelope | None = None
    failure_stage: Literal["M01", "M02"] | None = None
    failure_reason: str | None = None

    @model_validator(mode="after")
    def _status_law(self) -> "UpstreamPreparationReceipt":
        if self.status == "prepared":
            if self.prepared_data is None or self.failure_stage is not None or self.failure_reason:
                raise ValueError("prepared_upstream_receipt_status_mismatch")
            if any(item.status != "accepted" for item in self.source_results):
                raise ValueError("prepared_upstream_receipt_has_non_admission")
            if any(
                item.status not in {"projected", "degraded"} for item in self.calendar_projections
            ):
                raise ValueError("prepared_upstream_receipt_has_unusable_calendar")
        elif self.status == "source_not_admitted":
            if self.failure_stage != "M01" or self.prepared_data is not None:
                raise ValueError("source_terminal_receipt_status_mismatch")
            if not any(item.status == "not_admitted" for item in self.source_results):
                raise ValueError("source_terminal_receipt_requires_non_admission")
            if self.calendar_projections:
                raise ValueError("calendar_must_not_run_after_source_non_admission")
        elif self.status == "calendar_withheld":
            if self.failure_stage != "M02" or self.prepared_data is not None:
                raise ValueError("calendar_terminal_receipt_status_mismatch")
            if any(item.status != "accepted" for item in self.source_results):
                raise ValueError("calendar_terminal_receipt_requires_accepted_sources")
            if not any(
                item.status in {"withheld", "rejected"} for item in self.calendar_projections
            ):
                raise ValueError("calendar_terminal_receipt_requires_withheld_projection")
        return self

    @classmethod
    def create(
        cls,
        *,
        command_id: str,
        status: UpstreamPreparationStatus,
        source_results: tuple[SourceAdmissionResult, ...],
        calendar_projections: tuple[CalendarProjection, ...] = (),
        prepared_data: PreparedDataEnvelope | None = None,
        failure_stage: Literal["M01", "M02"] | None = None,
        failure_reason: str | None = None,
    ) -> "UpstreamPreparationReceipt":
        material = {
            "contract_version": "1.0.0",
            "command_id": command_id,
            "status": status,
            "source_results": source_results,
            "calendar_projections": calendar_projections,
            "prepared_data": prepared_data,
            "failure_stage": failure_stage,
            "failure_reason": failure_reason,
        }
        fingerprint = semantic_fingerprint(material)
        return cls(
            receipt_id=f"upstream-preparation:{fingerprint[:24]}",
            semantic_fingerprint=fingerprint,
            **material,
        )


class ApplicationCommand(BaseModel):
    """Exact caller-owned facts required for one prepared paper run."""

    model_config = ConfigDict(extra="forbid", frozen=True, allow_inf_nan=False)

    command_id: str = Field(min_length=1)
    execution_context: DmpV3ExecutionContext
    prepared_data: PreparedDataEnvelope
    serial_context: StageContext
    serial_stage_inputs: tuple[StageInput, ...] = Field(min_length=1)
    parallel_input: ParallelRiskInput
    prepared_packet: PacketEmissionSpec
    serial_packet: PacketEmissionSpec
    parallel_packet: PacketEmissionSpec
    final_risk_policy: FinalRiskJoinPolicy
    capital_state: CapitalState
    modifier_receipt: ModifierApplicationReceipt
    capital_policy: CapitalDeploymentPolicy
    capital_receipt_emitted_at_utc: datetime
    placement_policy: PlacementPolicy
    limit_price: Decimal = Field(gt=Decimal("0"))
    intent_at_utc: datetime
    executed_at_utc: datetime

    @field_validator(
        "capital_receipt_emitted_at_utc",
        "intent_at_utc",
        "executed_at_utc",
    )
    @classmethod
    def _utc_times(cls, value: datetime) -> datetime:
        return _require_utc(value, "application_datetime_must_be_utc")

    @model_validator(mode="after")
    def _validate_composition_law(self) -> "ApplicationCommand":
        prepared = self.prepared_data
        serial = self.serial_context
        parallel = self.parallel_input
        if (
            serial.prepared_id,
            serial.prepared_fingerprint,
            serial.prepared_schema_version,
            serial.prepared_input_fingerprint,
        ) != (
            prepared.prepared_id,
            prepared.prepared_fingerprint,
            prepared.schema_version,
            prepared.input_fingerprint,
        ):
            raise ValueError("serial_context_prepared_lineage_mismatch")
        if (
            parallel.prepared_id,
            parallel.prepared_fingerprint,
            parallel.prepared_schema_version,
        ) != (
            prepared.prepared_id,
            prepared.prepared_fingerprint,
            prepared.schema_version,
        ):
            raise ValueError("parallel_input_prepared_lineage_mismatch")
        expected_source_refs = tuple(
            sorted(
                (item.source_artifact_id, item.capture_id) for item in prepared.source_capture_refs
            )
        )
        if tuple(sorted(serial.source_capture_refs)) != expected_source_refs:
            raise ValueError("serial_context_source_lineage_mismatch")
        if (
            serial.preparation_policy_version,
            serial.alignment_policy_version,
            serial.fingerprint_policy_version,
            serial.canonicalisation_version,
            serial.derivation_versions,
        ) != (
            prepared.preparation_policy_version,
            prepared.alignment_policy_version,
            prepared.fingerprint_policy_version,
            prepared.canonicalisation_version,
            prepared.derivation_versions,
        ):
            raise ValueError("serial_context_preparation_policy_mismatch")
        stages = tuple(item.stage for item in self.serial_stage_inputs)
        expected_stages = (
            "temporal",
            "regime",
            "options_flow",
            "posture",
            "eligibility",
            "execution",
        )
        if tuple(sorted(stages)) != tuple(sorted(expected_stages)) or len(stages) != 6:
            raise ValueError("serial_stage_input_set_invalid")
        if any(
            (item.context_id, item.context_fingerprint)
            != (serial.context_id, serial.semantic_fingerprint)
            for item in self.serial_stage_inputs
        ):
            raise ValueError("serial_stage_input_context_mismatch")
        packet_ids = (
            self.prepared_packet.packet_id,
            self.serial_packet.packet_id,
            self.parallel_packet.packet_id,
        )
        if len(packet_ids) != len(set(packet_ids)):
            raise ValueError("application_packet_ids_must_be_unique")
        if self.prepared_packet.emitted_at_utc < prepared.effective_at_utc:
            raise ValueError("prepared_packet_precedes_prepared_authority")
        if (
            min(
                self.serial_packet.emitted_at_utc,
                self.parallel_packet.emitted_at_utc,
            )
            < self.prepared_packet.emitted_at_utc
        ):
            raise ValueError("owner_packet_precedes_prepared_packet")
        if self.capital_receipt_emitted_at_utc < max(
            self.serial_packet.emitted_at_utc,
            self.parallel_packet.emitted_at_utc,
        ):
            raise ValueError("capital_time_precedes_owner_packets")
        if not (self.capital_receipt_emitted_at_utc <= self.intent_at_utc <= self.executed_at_utc):
            raise ValueError("application_execution_time_order_invalid")
        if self.capital_state.effective_at_utc > self.capital_receipt_emitted_at_utc:
            raise ValueError("capital_state_is_from_future")
        if parallel.packet_lineage is not None and (
            parallel.packet_lineage.packet_id != self.prepared_packet.packet_id
        ):
            raise ValueError("parallel_input_packet_lineage_mismatch")
        return self


class ApplicationQuery(BaseModel):
    """Exact read-only M12 query; it carries no runtime execution authority."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    query_id: str = Field(min_length=1)
    envelope: ReplayEnvelope
    reproduced_output_id: str | None
    reproduced_output_fingerprint: str | None
    reproduced_reasons: tuple[str, ...] | None
    executable_versions: tuple[str, ...] | None
    isolated_execution: Literal[True]
    live_side_effects: tuple[str, ...]
    runtime_authority_promoted: Literal[False]

    @field_validator("live_side_effects")
    @classmethod
    def _no_live_side_effects(cls, value: tuple[str, ...]) -> tuple[str, ...]:
        if value:
            raise ValueError("application_query_live_side_effects_forbidden")
        return value


class ApplicationRunReceipt(BaseModel):
    """Immutable aggregation of exact owner outputs for one M00 run."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    receipt_id: str = Field(min_length=1)
    contract_version: Literal["1.0.0"] = "1.0.0"
    semantic_fingerprint: str = Field(pattern=r"^[0-9a-f]{64}$")
    command_id: str = Field(min_length=1)
    trace_id: str = Field(min_length=1)
    run_id: str = Field(min_length=1)
    scenario_id: str = Field(min_length=1)
    outcome: ApplicationOutcome
    owner_steps: tuple[str, ...] = Field(min_length=1)
    prepared_context_packet: DeskModulePacketV3
    serial_candidate: SerialCandidate
    parallel_assessment: ParallelRiskAssessment
    serial_packet: DeskModulePacketV3 | None = None
    parallel_packet: DeskModulePacketV3 | None = None
    final_risk_decision: FinalRiskDecision | None = None
    capital_decision: CapitalDeploymentDecision | None = None
    capital_receipt: CapitalDeploymentReceipt | None = None
    run_scope_id: str | None = None
    placement_intent: PlacementIntent | None = None
    execution_receipt: ExecutionReceipt | None = None
    fill_reconciliation_receipt: FillReconciliationReceipt | None = None
    portfolio_snapshot: PortfolioSnapshot | None = None
    replay_class: None = None
    live_execution_proven: Literal[False] = False
    durable_state_proven: Literal[False] = False

    @model_validator(mode="after")
    def _validate_receipt_law(self) -> "ApplicationRunReceipt":
        if (
            self.prepared_context_packet.traceid,
            self.prepared_context_packet.runid,
            self.prepared_context_packet.scenarioid,
        ) != (self.trace_id, self.run_id, self.scenario_id):
            raise ValueError("application_receipt_execution_context_mismatch")
        if self.outcome.startswith("serial_"):
            if self.serial_candidate.status == "formed":
                raise ValueError("serial_terminal_receipt_cannot_carry_formed_candidate")
            prohibited = (
                self.serial_packet,
                self.parallel_packet,
                self.final_risk_decision,
                self.capital_decision,
                self.capital_receipt,
                self.run_scope_id,
                self.placement_intent,
                self.execution_receipt,
                self.fill_reconciliation_receipt,
                self.portfolio_snapshot,
            )
            if any(value is not None for value in prohibited):
                raise ValueError("serial_terminal_receipt_carries_downstream_authority")
        elif self.outcome in {"block", "no_trade"}:
            required = (
                self.serial_packet,
                self.parallel_packet,
                self.final_risk_decision,
                self.capital_decision,
                self.capital_receipt,
            )
            if any(value is None for value in required):
                raise ValueError("capital_terminal_receipt_lineage_incomplete")
            prohibited = (
                self.run_scope_id,
                self.placement_intent,
                self.execution_receipt,
                self.fill_reconciliation_receipt,
                self.portfolio_snapshot,
            )
            if any(value is not None for value in prohibited):
                raise ValueError("capital_terminal_receipt_carries_execution_authority")
            if self.capital_decision is None or self.capital_decision.action != self.outcome:
                raise ValueError("capital_terminal_outcome_mismatch")
        else:
            required = (
                self.serial_packet,
                self.parallel_packet,
                self.final_risk_decision,
                self.capital_decision,
                self.capital_receipt,
                self.run_scope_id,
                self.placement_intent,
                self.execution_receipt,
                self.fill_reconciliation_receipt,
                self.portfolio_snapshot,
            )
            if any(value is None for value in required):
                raise ValueError("paper_run_receipt_lineage_incomplete")
            if self.capital_decision is None or self.capital_decision.action not in {
                "continue",
                "reduce",
            }:
                raise ValueError("paper_run_requires_positive_capital_action")
        material = self.model_dump(mode="python", exclude={"receipt_id", "semantic_fingerprint"})
        expected = semantic_fingerprint(material)
        if self.semantic_fingerprint != expected:
            raise ValueError("application_run_receipt_fingerprint_mismatch")
        if self.receipt_id != f"application-run-receipt:{expected[:24]}":
            raise ValueError("application_run_receipt_id_mismatch")
        return self

    @classmethod
    def create(cls, **material: Any) -> "ApplicationRunReceipt":
        provisional = cls.model_construct(
            **material,
            receipt_id="pending",
            semantic_fingerprint="0" * 64,
        )
        governed_material = provisional.model_dump(
            mode="python", exclude={"receipt_id", "semantic_fingerprint"}
        )
        fingerprint = semantic_fingerprint(governed_material)
        return cls(
            **material,
            receipt_id=f"application-run-receipt:{fingerprint[:24]}",
            semantic_fingerprint=fingerprint,
        )
