"""M06-owned immutable contracts for K10 independent parallel risk."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from hashlib import sha256
from math import isfinite
from typing import Any, Final, Literal, Mapping

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from nvda_desk.contracts.prepared_data import (
    PreparedDataEnvelope,
    PreparedEventWindow,
    SourceCaptureReference,
)

RiskState = Literal["observe", "caution", "block", "unknown"]
RiskFamily = Literal[
    "concentration",
    "inventory_stress",
    "liquidity",
    "options_term_structure",
    "scheduled_event",
    "volatility",
]

CLOSED_AUTHORITY_CLASSES: Final[tuple[str, ...]] = (
    "prepared_truth",
    "packet_identity",
    "serial_candidate",
    "coefficient_modifier",
    "final_risk",
    "capital",
    "broker_order",
    "position_inventory",
    "lifecycle",
    "transaction",
    "replay",
)
EXPECTED_FAMILIES: Final[tuple[str, ...]] = (
    "concentration",
    "inventory_stress",
    "liquidity",
    "options_term_structure",
    "scheduled_event",
    "volatility",
)
SUPPORTED_EVALUATOR_POLICY_VERSION: Final[str] = "parallel-risk.compat.v1"
SUPPORTED_AGGREGATION_VERSION: Final[str] = "parallel-risk.aggregate.v1"


def _canonical(value: Any) -> Any:
    if isinstance(value, datetime):
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("datetime_must_be_timezone_aware")
        return value.astimezone(UTC).isoformat().replace("+00:00", "Z")
    if isinstance(value, BaseModel):
        return _canonical(value.model_dump(mode="python"))
    if isinstance(value, Mapping):
        return {str(key): _canonical(value[key]) for key in sorted(value)}
    if isinstance(value, (tuple, list)):
        return [_canonical(item) for item in value]
    return value


def semantic_fingerprint(value: Any) -> str:
    """Return one deterministic SHA-256 identity for governed semantic material."""

    return sha256(
        json.dumps(_canonical(value), sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


class ParallelRiskPacketLineage(BaseModel):
    """Optional admitted M04 prepared-context packet lineage consumed by M06."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    packet_id: str = Field(min_length=1)
    packet_role: Literal["prepared_context_packet"]
    packet_fingerprint: str = Field(pattern=r"^[0-9a-f]{64}$")
    parent_ids: tuple[str, ...] = ()
    dependency_ids: tuple[str, ...] = ()

    @model_validator(mode="after")
    def _validate_lineage(self) -> "ParallelRiskPacketLineage":
        if len(self.parent_ids) != len(set(self.parent_ids)):
            raise ValueError("duplicate_packet_parent_id")
        if len(self.dependency_ids) != len(set(self.dependency_ids)):
            raise ValueError("duplicate_packet_dependency_id")
        return self


class ParallelRiskInput(BaseModel):
    """Immutable projection of exact M03 authority for one K10 evaluation."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    input_id: str = Field(min_length=1)
    contract_version: Literal["1.0.0"] = "1.0.0"
    schema_version: Literal["1.0.0"] = "1.0.0"
    evaluator_version: Literal["m06.parallel-risk-evaluator.v1"] = (
        "m06.parallel-risk-evaluator.v1"
    )
    evaluator_policy_version: Literal["parallel-risk.compat.v1"]
    aggregation_version: Literal["parallel-risk.aggregate.v1"]
    prepared_id: str = Field(min_length=1)
    prepared_fingerprint: str = Field(pattern=r"^[0-9a-f]{64}$")
    prepared_schema_version: str = Field(min_length=1)
    preparation_policy_version: str = Field(min_length=1)
    alignment_policy_version: str = Field(min_length=1)
    fingerprint_policy_version: str = Field(min_length=1)
    canonicalisation_version: str = Field(min_length=1)
    effective_at_utc: datetime
    source_capture_refs: tuple[SourceCaptureReference, ...] = Field(min_length=1)
    prepared_validation_state: Literal["valid", "degraded"]
    prepared_completeness_state: Literal["complete", "degraded"]
    prepared_limitations: tuple[str, ...]
    missing_optional_enrichments: tuple[str, ...]
    packet_lineage: ParallelRiskPacketLineage | None = None
    windows: tuple[PreparedEventWindow, ...] = ()
    front_dte: int | None = None
    next_dte: int | None = None
    vix_level: float | None = None
    threshold_authority_refs: tuple[str, ...] = Field(min_length=1)
    vix_caution_threshold: float
    vix_block_threshold: float
    input_fingerprint: str = Field(pattern=r"^[0-9a-f]{64}$")
    closed_authority_classes: tuple[str, ...] = CLOSED_AUTHORITY_CLASSES
    foreign_authority_claimed: bool = False

    @field_validator("source_capture_refs", mode="before")
    @classmethod
    def _revalidate_source_refs(cls, value: Any) -> tuple[SourceCaptureReference, ...]:
        return tuple(
            sorted(
                (
                    SourceCaptureReference.model_validate(
                        item.model_dump(mode="python")
                        if isinstance(item, BaseModel)
                        else item
                    )
                    for item in value
                ),
                key=lambda item: (item.capture_id, item.source_artifact_id),
            )
        )

    @field_validator("windows", mode="before")
    @classmethod
    def _revalidate_windows(cls, value: Any) -> tuple[PreparedEventWindow, ...]:
        return tuple(
            sorted(
                (
                    PreparedEventWindow.model_validate(
                        item.model_dump(mode="python")
                        if isinstance(item, BaseModel)
                        else item
                    )
                    for item in value
                ),
                key=lambda item: (item.window_start_utc, item.event_id),
            )
        )

    @field_validator(
        "threshold_authority_refs",
        "prepared_limitations",
        "missing_optional_enrichments",
        mode="before",
    )
    @classmethod
    def _normalise_string_sets(cls, value: Any) -> tuple[str, ...]:
        return tuple(sorted(str(item) for item in value))

    @field_validator("packet_lineage", mode="before")
    @classmethod
    def _revalidate_packet_lineage(cls, value: Any) -> ParallelRiskPacketLineage | None:
        if value is None:
            return None
        return ParallelRiskPacketLineage.model_validate(
            value.model_dump(mode="python") if isinstance(value, BaseModel) else value
        )

    @model_validator(mode="after")
    def _validate_input(self) -> "ParallelRiskInput":
        if self.effective_at_utc.tzinfo is None or self.effective_at_utc.utcoffset() is None:
            raise ValueError("effective_at_utc_must_be_timezone_aware")
        if self.closed_authority_classes != CLOSED_AUTHORITY_CLASSES:
            raise ValueError("parallel_risk_input_foreign_authority_boundary_changed")
        if self.foreign_authority_claimed:
            raise ValueError("parallel_risk_input_foreign_authority_claimed")
        if len(self.threshold_authority_refs) != 2:
            raise ValueError("exact_two_threshold_authority_refs_required")
        if len(self.threshold_authority_refs) != len(set(self.threshold_authority_refs)):
            raise ValueError("duplicate_threshold_authority_ref")
        if not all(item.startswith("m07:") for item in self.threshold_authority_refs):
            raise ValueError("threshold_authority_must_be_m07_owned")
        if self.prepared_validation_state == "valid" and (
            self.prepared_completeness_state != "complete"
            or self.prepared_limitations
            or self.missing_optional_enrichments
        ):
            raise ValueError("valid_prepared_projection_must_be_complete")
        if self.prepared_validation_state == "degraded" and (
            self.prepared_completeness_state != "degraded"
            or not (self.prepared_limitations or self.missing_optional_enrichments)
        ):
            raise ValueError("degraded_prepared_projection_requires_explicit_gap")
        if not all(isfinite(value) for value in (self.vix_caution_threshold, self.vix_block_threshold)):
            raise ValueError("vix_threshold_must_be_finite")
        if self.vix_caution_threshold < 0 or self.vix_block_threshold < 0:
            raise ValueError("vix_threshold_must_be_nonnegative")
        if self.vix_level is not None and (not isfinite(self.vix_level) or self.vix_level < 0):
            raise ValueError("vix_level_must_be_nonnegative_finite")
        if any(value is not None and value < 0 for value in (self.front_dte, self.next_dte)):
            raise ValueError("options_dte_must_be_nonnegative")
        if self.vix_caution_threshold >= self.vix_block_threshold:
            raise ValueError("threshold_order_invalid")
        expected = parallel_risk_input_fingerprint(self)
        if self.input_fingerprint != expected:
            raise ValueError("parallel_risk_input_fingerprint_mismatch")
        if self.input_id != f"parallel-risk-input:{expected[:24]}":
            raise ValueError("parallel_risk_input_id_mismatch")
        return self

    @classmethod
    def from_prepared(
        cls,
        prepared: PreparedDataEnvelope,
        *,
        evaluator_policy_version: str,
        aggregation_version: str,
        threshold_authority_refs: tuple[str, ...],
        vix_caution_threshold: float,
        vix_block_threshold: float,
        packet_lineage: ParallelRiskPacketLineage | None = None,
    ) -> "ParallelRiskInput":
        """Project one revalidated M03 envelope into the bounded K10 input."""

        if not isinstance(prepared, PreparedDataEnvelope):
            raise TypeError("typed_prepared_envelope_required")
        governed = PreparedDataEnvelope.model_validate(prepared.model_dump(mode="python"))
        if evaluator_policy_version != SUPPORTED_EVALUATOR_POLICY_VERSION:
            raise ValueError("unsupported_evaluator_policy_version")
        if aggregation_version != SUPPORTED_AGGREGATION_VERSION:
            raise ValueError("unsupported_aggregation_version")
        if not threshold_authority_refs:
            raise ValueError("threshold_authority_refs_required")
        lineage = None
        if packet_lineage is not None:
            lineage = ParallelRiskPacketLineage.model_validate(
                packet_lineage.model_dump(mode="python")
            )
        payload: dict[str, Any] = {
            "input_id": "pending",
            "evaluator_policy_version": evaluator_policy_version,
            "aggregation_version": aggregation_version,
            "prepared_id": governed.prepared_id,
            "prepared_fingerprint": governed.prepared_fingerprint,
            "prepared_schema_version": governed.schema_version,
            "preparation_policy_version": governed.preparation_policy_version,
            "alignment_policy_version": governed.alignment_policy_version,
            "fingerprint_policy_version": governed.fingerprint_policy_version,
            "canonicalisation_version": governed.canonicalisation_version,
            "effective_at_utc": governed.effective_at_utc,
            "source_capture_refs": tuple(
                sorted(
                    governed.source_capture_refs,
                    key=lambda item: (item.capture_id, item.source_artifact_id),
                )
            ),
            "prepared_validation_state": governed.validation_state,
            "prepared_completeness_state": governed.completeness_state,
            "prepared_limitations": governed.limitations,
            "missing_optional_enrichments": governed.missing_optional_enrichments,
            "packet_lineage": lineage,
            "windows": tuple(
                sorted(
                    governed.payload.windows,
                    key=lambda item: (item.window_start_utc, item.event_id),
                )
            ),
            "front_dte": governed.payload.front_dte,
            "next_dte": governed.payload.next_dte,
            "vix_level": governed.payload.vix_level,
            "threshold_authority_refs": tuple(sorted(threshold_authority_refs)),
            "vix_caution_threshold": vix_caution_threshold,
            "vix_block_threshold": vix_block_threshold,
            "input_fingerprint": "0" * 64,
            "closed_authority_classes": CLOSED_AUTHORITY_CLASSES,
            "foreign_authority_claimed": False,
        }
        provisional = cls.model_construct(**payload)
        fp = parallel_risk_input_fingerprint(provisional)
        payload["input_fingerprint"] = fp
        payload["input_id"] = f"parallel-risk-input:{fp[:24]}"
        return cls.model_validate(payload)


class ParallelRiskObservation(BaseModel):
    """Immutable typed result for one admitted M06 environmental-risk family."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    observation_id: str = Field(min_length=1)
    family: RiskFamily
    state: RiskState
    reason: str = Field(min_length=1)
    source_fields: tuple[str, ...] = Field(min_length=1)
    source_references: tuple[str, ...] = Field(min_length=1)
    limitation: str | None = None
    semantic_fingerprint: str = Field(pattern=r"^[0-9a-f]{64}$")

    @model_validator(mode="after")
    def _validate_observation(self) -> "ParallelRiskObservation":
        if len(self.source_fields) != len(set(self.source_fields)):
            raise ValueError("duplicate_observation_source_field")
        if len(self.source_references) != len(set(self.source_references)):
            raise ValueError("duplicate_observation_source_reference")
        if self.state == "unknown" and not self.limitation:
            raise ValueError("unknown_observation_requires_limitation")
        if self.state != "unknown" and self.limitation:
            raise ValueError("known_observation_must_not_claim_unknown_limitation")
        expected = parallel_risk_observation_fingerprint(self)
        if self.semantic_fingerprint != expected:
            raise ValueError("parallel_risk_observation_fingerprint_mismatch")
        if self.observation_id != f"parallel-risk-observation:{expected[:24]}":
            raise ValueError("parallel_risk_observation_id_mismatch")
        return self


class ParallelRiskAssessment(BaseModel):
    """Immutable K10 aggregate and terminal-join contribution."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    assessment_id: str = Field(min_length=1)
    contract_version: Literal["1.0.0"] = "1.0.0"
    schema_version: Literal["1.0.0"] = "1.0.0"
    input_id: str = Field(min_length=1)
    input_fingerprint: str = Field(pattern=r"^[0-9a-f]{64}$")
    prepared_id: str = Field(min_length=1)
    prepared_fingerprint: str = Field(pattern=r"^[0-9a-f]{64}$")
    evaluator_version: str = Field(min_length=1)
    evaluator_policy_version: Literal["parallel-risk.compat.v1"]
    aggregation_version: Literal["parallel-risk.aggregate.v1"]
    state: RiskState
    observations: tuple[ParallelRiskObservation, ...] = Field(min_length=1)
    caution_flags: tuple[str, ...]
    hard_blocks: tuple[str, ...]
    unknown_families: tuple[str, ...]
    prepared_limitations: tuple[str, ...]
    missing_optional_enrichments: tuple[str, ...]
    limitations: tuple[str, ...]
    semantic_fingerprint: str = Field(pattern=r"^[0-9a-f]{64}$")
    closed_authority_classes: tuple[str, ...] = CLOSED_AUTHORITY_CLASSES
    foreign_authority_claimed: bool = False

    @field_validator("observations", mode="before")
    @classmethod
    def _revalidate_observations(cls, value: Any) -> tuple[ParallelRiskObservation, ...]:
        return tuple(
            ParallelRiskObservation.model_validate(
                item.model_dump(mode="python") if isinstance(item, BaseModel) else item
            )
            for item in value
        )

    @model_validator(mode="after")
    def _validate_assessment(self) -> "ParallelRiskAssessment":
        if self.closed_authority_classes != CLOSED_AUTHORITY_CLASSES:
            raise ValueError("parallel_risk_assessment_foreign_authority_boundary_changed")
        if self.foreign_authority_claimed:
            raise ValueError("parallel_risk_assessment_foreign_authority_claimed")
        families = tuple(item.family for item in self.observations)
        if families != EXPECTED_FAMILIES:
            raise ValueError("parallel_risk_observation_family_order_or_completeness_invalid")
        expected_cautions = tuple(item.reason for item in self.observations if item.state == "caution")
        expected_blocks = tuple(item.reason for item in self.observations if item.state == "block")
        expected_unknown = tuple(item.family for item in self.observations if item.state == "unknown")
        expected_limitations = tuple(
            sorted(
                {item.limitation for item in self.observations if item.limitation}
                | set(self.prepared_limitations)
                | set(self.missing_optional_enrichments)
            )
        )
        if self.caution_flags != expected_cautions:
            raise ValueError("parallel_risk_caution_lineage_mismatch")
        if self.hard_blocks != expected_blocks:
            raise ValueError("parallel_risk_block_lineage_mismatch")
        if self.unknown_families != expected_unknown:
            raise ValueError("parallel_risk_unknown_lineage_mismatch")
        if self.limitations != expected_limitations:
            raise ValueError("parallel_risk_limitation_lineage_mismatch")
        expected_state: RiskState = (
            "block"
            if expected_blocks
            else "caution"
            if expected_cautions
            else "unknown"
            if expected_unknown
            else "observe"
        )
        if self.state != expected_state:
            raise ValueError("parallel_risk_aggregate_state_mismatch")
        expected = parallel_risk_assessment_fingerprint(self)
        if self.semantic_fingerprint != expected:
            raise ValueError("parallel_risk_assessment_fingerprint_mismatch")
        if self.assessment_id != f"parallel-risk-assessment:{expected[:24]}":
            raise ValueError("parallel_risk_assessment_id_mismatch")
        return self


def parallel_risk_input_fingerprint(value: ParallelRiskInput) -> str:
    data = value.model_dump(mode="python", exclude={"input_id", "input_fingerprint"})
    return semantic_fingerprint(data)


def parallel_risk_observation_fingerprint(value: ParallelRiskObservation) -> str:
    data = value.model_dump(
        mode="python", exclude={"observation_id", "semantic_fingerprint"}
    )
    return semantic_fingerprint(data)


def parallel_risk_assessment_fingerprint(value: ParallelRiskAssessment) -> str:
    data = value.model_dump(
        mode="python", exclude={"assessment_id", "semantic_fingerprint"}
    )
    return semantic_fingerprint(data)


__all__ = [
    "CLOSED_AUTHORITY_CLASSES",
    "EXPECTED_FAMILIES",
    "SUPPORTED_AGGREGATION_VERSION",
    "SUPPORTED_EVALUATOR_POLICY_VERSION",
    "ParallelRiskAssessment",
    "ParallelRiskInput",
    "ParallelRiskObservation",
    "ParallelRiskPacketLineage",
    "semantic_fingerprint",
]
