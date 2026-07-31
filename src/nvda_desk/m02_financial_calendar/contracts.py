"""M02-owned immutable contracts for K04 financial-calendar authority."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from enum import StrEnum
from hashlib import sha256
from math import isfinite
from typing import Any, Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    StrictBool,
    field_validator,
    model_validator,
)

JsonScalar = str | int | float | bool | None
CompletenessState = Literal["complete", "unknown", "unavailable"]
ProjectionStatus = Literal["projected", "degraded", "withheld", "rejected"]

CLOSED_AUTHORITY_CLASSES: tuple[str, ...] = (
    "candidate_formation",
    "risk_permission",
    "capital",
    "broker_order",
    "position_inventory",
    "lifecycle",
    "review",
    "replay",
    "transaction",
)


class FinancialCalendarLayer(StrEnum):
    """The exact four semantic calendar layers admitted by N02 and K04."""

    MARKET_SESSION_REFERENCE = "market_session_reference"
    FINANCIAL_EVENT_REFERENCE = "financial_event_reference"
    OPERATIONAL_CALENDAR_STATE = "operational_calendar_state"
    DERIVED_RUNTIME_CALENDAR_CONTEXT = "derived_runtime_calendar_context"


def _is_utc(value: datetime) -> bool:
    return (
        value.tzinfo is not None
        and value.utcoffset() is not None
        and value.utcoffset() == UTC.utcoffset(value)
    )


def _non_empty(value: str, *, reason: str) -> str:
    if not value.strip():
        raise ValueError(reason)
    return value


def _validate_scalar(value: JsonScalar, *, reason: str) -> JsonScalar:
    if isinstance(value, float) and not isfinite(value):
        raise ValueError(reason)
    return value


def _canonical_json(material: Any) -> str:
    return json.dumps(
        material,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    )


class CalendarFactCandidate(BaseModel):
    """One immutable owner-issued calendar fact from exactly one K04 layer."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    candidate_id: str = Field(min_length=1)
    layer: FinancialCalendarLayer
    fact_family: str = Field(min_length=1)
    semantic_key: str = Field(min_length=1)
    value: JsonScalar
    value_type: str = Field(min_length=1)
    unit: str | None = None
    effective_from_utc: datetime
    effective_to_utc: datetime | None = None
    source_artifact_id: str = Field(min_length=1)
    source_version: str = Field(min_length=1)
    contract_version: str = Field(min_length=1)
    owner_id: str = Field(min_length=1)
    validation_state: Literal["valid", "unavailable", "cancelled"]
    observed_at_utc: datetime | None = None
    capture_id: str | None = None
    captured_at_utc: datetime | None = None
    supersedes_candidate_id: str | None = None
    supersession_reason: str | None = None
    supersession_status: Literal["applied"] | None = None

    @field_validator("value")
    @classmethod
    def _value_is_finite(cls, value: JsonScalar) -> JsonScalar:
        return _validate_scalar(value, reason="calendar_value_must_be_finite")

    @field_validator(
        "effective_from_utc",
        "effective_to_utc",
        "observed_at_utc",
        "captured_at_utc",
    )
    @classmethod
    def _times_are_utc(cls, value: datetime | None) -> datetime | None:
        if value is not None and not _is_utc(value):
            raise ValueError("calendar_effective_time_must_be_utc")
        return value

    @model_validator(mode="after")
    def _candidate_law(self) -> "CalendarFactCandidate":
        for value, reason in (
            (self.candidate_id, "candidate_id_required"),
            (self.fact_family, "fact_family_required"),
            (self.semantic_key, "semantic_key_required"),
            (self.value_type, "value_type_required"),
            (self.source_artifact_id, "source_artifact_id_required"),
            (self.source_version, "source_version_required"),
            (self.contract_version, "contract_version_required"),
            (self.owner_id, "owner_id_required"),
        ):
            _non_empty(value, reason=reason)
        if (
            self.effective_to_utc is not None
            and self.effective_to_utc <= self.effective_from_utc
        ):
            raise ValueError("calendar_effective_interval_invalid")
        if (self.capture_id is None) != (self.captured_at_utc is None):
            raise ValueError("capture_identity_time_mismatch")
        if self.capture_id is not None:
            _non_empty(self.capture_id, reason="capture_id_required")
        supersession_parts = (
            self.supersedes_candidate_id,
            self.supersession_reason,
            self.supersession_status,
        )
        if any(supersession_parts) and not all(supersession_parts):
            raise ValueError("supersession_identity_reason_status_mismatch")
        if self.supersedes_candidate_id == self.candidate_id:
            raise ValueError("candidate_cannot_supersede_itself")
        if self.supersedes_candidate_id is not None and self.validation_state != "valid":
            raise ValueError("applied_supersession_candidate_must_be_valid")
        return self


class CalendarFieldResolutionPolicy(BaseModel):
    """Versioned M02 comparison and absence policy for one semantic field."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    policy_id: str = Field(min_length=1)
    policy_version: str = Field(min_length=1)
    semantic_key: str = Field(min_length=1)
    mandatory: StrictBool
    allow_reference_only_degraded: StrictBool = False


class SelectedCalendarField(BaseModel):
    """One selected K04 field with complete contributing lineage."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    semantic_key: str = Field(min_length=1)
    value: JsonScalar
    candidate_ids: tuple[str, ...] = Field(min_length=1)
    source_refs: tuple[tuple[str, str], ...] = Field(min_length=1)
    layers: tuple[FinancialCalendarLayer, ...] = Field(min_length=1)

    @model_validator(mode="after")
    def _lineage_is_unique(self) -> "SelectedCalendarField":
        if len(self.candidate_ids) != len(set(self.candidate_ids)):
            raise ValueError("duplicate_selected_candidate_id")
        if len(self.source_refs) != len(set(self.source_refs)):
            raise ValueError("duplicate_selected_source_ref")
        return self


def candidate_material(candidate: CalendarFactCandidate) -> dict[str, Any]:
    """Return canonical semantic material for one candidate."""

    return {
        "candidate_id": candidate.candidate_id,
        "layer": candidate.layer.value,
        "fact_family": candidate.fact_family,
        "semantic_key": candidate.semantic_key,
        "value": candidate.value,
        "value_type": candidate.value_type,
        "unit": candidate.unit,
        "effective_from_utc": candidate.effective_from_utc.isoformat(),
        "effective_to_utc": (
            candidate.effective_to_utc.isoformat()
            if candidate.effective_to_utc is not None
            else None
        ),
        "source_artifact_id": candidate.source_artifact_id,
        "source_version": candidate.source_version,
        "contract_version": candidate.contract_version,
        "owner_id": candidate.owner_id,
        "validation_state": candidate.validation_state,
        "observed_at_utc": (
            candidate.observed_at_utc.isoformat()
            if candidate.observed_at_utc is not None
            else None
        ),
        "capture_id": candidate.capture_id,
        "captured_at_utc": (
            candidate.captured_at_utc.isoformat()
            if candidate.captured_at_utc is not None
            else None
        ),
        "supersedes_candidate_id": candidate.supersedes_candidate_id,
        "supersession_reason": candidate.supersession_reason,
        "supersession_status": candidate.supersession_status,
    }


class ReferenceBundleSelection(BaseModel):
    """One selected immutable calendar-reference bundle identity/version."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    bundle_id: str = Field(min_length=1)
    bundle_version: str = Field(min_length=1)


class AppliedSupersession(BaseModel):
    """One explicit operational supersession preserved by snapshot/projection."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    superseding_candidate_id: str = Field(min_length=1)
    superseded_candidate_id: str = Field(min_length=1)
    reason: str = Field(min_length=1)
    status: Literal["applied"]


def snapshot_fingerprint(
    *,
    snapshot_id: str,
    snapshot_version: str,
    schema_version: str,
    scope: str,
    effective_from_utc: datetime,
    effective_to_utc: datetime,
    as_of_utc: datetime,
    market_session_reference: tuple[CalendarFactCandidate, ...],
    financial_event_reference: tuple[CalendarFactCandidate, ...],
    operational_calendar_state: tuple[CalendarFactCandidate, ...],
    derived_runtime_calendar_context: tuple[CalendarFactCandidate, ...],
    session_completeness: CompletenessState,
    event_completeness: CompletenessState,
    operational_completeness: CompletenessState,
    selected_reference_bundles: tuple[ReferenceBundleSelection, ...],
    unresolved_conflicts: tuple[str, ...],
    applied_supersessions: tuple[AppliedSupersession, ...],
    projection_policy_version: str | None,
    canonicalisation_version: str,
) -> str:
    """Compute order-independent semantic identity for one K04 snapshot."""

    material = {
        "snapshot_id": snapshot_id,
        "snapshot_version": snapshot_version,
        "schema_version": schema_version,
        "scope": scope,
        "effective_from_utc": effective_from_utc.isoformat(),
        "effective_to_utc": effective_to_utc.isoformat(),
        "as_of_utc": as_of_utc.isoformat(),
        "layers": {
            layer_name: [
                candidate_material(candidate)
                for candidate in sorted(
                    candidates,
                    key=lambda item: (item.semantic_key, item.candidate_id),
                )
            ]
            for layer_name, candidates in (
                ("market_session_reference", market_session_reference),
                ("financial_event_reference", financial_event_reference),
                ("operational_calendar_state", operational_calendar_state),
                ("derived_runtime_calendar_context", derived_runtime_calendar_context),
            )
        },
        "session_completeness": session_completeness,
        "event_completeness": event_completeness,
        "operational_completeness": operational_completeness,
        "selected_reference_bundles": [
            item.model_dump(mode="json") for item in selected_reference_bundles
        ],
        "unresolved_conflicts": unresolved_conflicts,
        "applied_supersessions": [
            item.model_dump(mode="json") for item in applied_supersessions
        ],
        "projection_policy_version": projection_policy_version,
        "canonicalisation_version": canonicalisation_version,
    }
    return sha256(_canonical_json(material).encode("utf-8")).hexdigest()


class FinancialCalendarSnapshot(BaseModel):
    """Immutable, versioned M02 authority snapshot binding exactly four layers."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    snapshot_id: str = Field(min_length=1)
    snapshot_version: str = Field(min_length=1)
    schema_version: str = Field(min_length=1)
    scope: str = Field(min_length=1)
    effective_from_utc: datetime
    effective_to_utc: datetime
    as_of_utc: datetime
    market_session_reference: tuple[CalendarFactCandidate, ...]
    financial_event_reference: tuple[CalendarFactCandidate, ...]
    operational_calendar_state: tuple[CalendarFactCandidate, ...]
    derived_runtime_calendar_context: tuple[CalendarFactCandidate, ...]
    session_completeness: CompletenessState
    event_completeness: CompletenessState
    operational_completeness: CompletenessState
    selected_reference_bundles: tuple[ReferenceBundleSelection, ...]
    unresolved_conflicts: tuple[str, ...] = ()
    applied_supersessions: tuple[AppliedSupersession, ...] = ()
    projection_policy_version: str | None = None
    canonicalisation_version: str = Field(min_length=1)
    semantic_fingerprint: str = Field(min_length=1)

    @field_validator("effective_from_utc", "effective_to_utc", "as_of_utc")
    @classmethod
    def _times_are_utc(cls, value: datetime) -> datetime:
        if not _is_utc(value):
            raise ValueError("snapshot_time_must_be_utc")
        return value

    @model_validator(mode="after")
    def _snapshot_law(self) -> "FinancialCalendarSnapshot":
        if self.effective_to_utc <= self.effective_from_utc:
            raise ValueError("snapshot_effective_interval_invalid")
        collections = (
            (FinancialCalendarLayer.MARKET_SESSION_REFERENCE, self.market_session_reference),
            (FinancialCalendarLayer.FINANCIAL_EVENT_REFERENCE, self.financial_event_reference),
            (FinancialCalendarLayer.OPERATIONAL_CALENDAR_STATE, self.operational_calendar_state),
            (
                FinancialCalendarLayer.DERIVED_RUNTIME_CALENDAR_CONTEXT,
                self.derived_runtime_calendar_context,
            ),
        )
        all_candidates: list[CalendarFactCandidate] = []
        for expected_layer, candidates in collections:
            for candidate in candidates:
                if candidate.layer != expected_layer:
                    raise ValueError("candidate_layer_collection_mismatch")
                all_candidates.append(candidate)
        identities = [candidate.candidate_id for candidate in all_candidates]
        if len(identities) != len(set(identities)):
            raise ValueError("duplicate_calendar_candidate_id")
        has_reference_facts = (
            self.market_session_reference or self.financial_event_reference
        )
        if has_reference_facts and not self.selected_reference_bundles:
            raise ValueError("selected_reference_bundle_required")
        bundle_ids = [
            (item.bundle_id, item.bundle_version) for item in self.selected_reference_bundles
        ]
        if len(bundle_ids) != len(set(bundle_ids)):
            raise ValueError("duplicate_selected_reference_bundle")
        if self.derived_runtime_calendar_context and not self.projection_policy_version:
            raise ValueError("derived_calendar_projection_policy_required")
        candidate_by_id = {item.candidate_id: item for item in all_candidates}
        declared_decisions = {
            (
                decision.superseding_candidate_id,
                decision.superseded_candidate_id,
                decision.reason,
                decision.status,
            )
            for decision in self.applied_supersessions
        }
        if len(declared_decisions) != len(self.applied_supersessions):
            raise ValueError("duplicate_applied_supersession_decision")
        for decision in self.applied_supersessions:
            winner = candidate_by_id.get(decision.superseding_candidate_id)
            target = candidate_by_id.get(decision.superseded_candidate_id)
            if (
                winner is None
                or target is None
                or winner.layer != FinancialCalendarLayer.OPERATIONAL_CALENDAR_STATE
                or winner.supersedes_candidate_id != target.candidate_id
                or winner.supersession_reason != decision.reason
                or winner.supersession_status != decision.status
            ):
                raise ValueError("applied_supersession_authority_mismatch")
        claimed_decisions = {
            (
                candidate.candidate_id,
                candidate.supersedes_candidate_id,
                candidate.supersession_reason,
                candidate.supersession_status,
            )
            for candidate in self.operational_calendar_state
            if candidate.supersedes_candidate_id is not None
        }
        if claimed_decisions != declared_decisions:
            raise ValueError("applied_supersession_set_mismatch")
        expected = snapshot_fingerprint(
            snapshot_id=self.snapshot_id,
            snapshot_version=self.snapshot_version,
            schema_version=self.schema_version,
            scope=self.scope,
            effective_from_utc=self.effective_from_utc,
            effective_to_utc=self.effective_to_utc,
            as_of_utc=self.as_of_utc,
            market_session_reference=self.market_session_reference,
            financial_event_reference=self.financial_event_reference,
            operational_calendar_state=self.operational_calendar_state,
            derived_runtime_calendar_context=self.derived_runtime_calendar_context,
            session_completeness=self.session_completeness,
            event_completeness=self.event_completeness,
            operational_completeness=self.operational_completeness,
            selected_reference_bundles=self.selected_reference_bundles,
            unresolved_conflicts=self.unresolved_conflicts,
            applied_supersessions=self.applied_supersessions,
            projection_policy_version=self.projection_policy_version,
            canonicalisation_version=self.canonicalisation_version,
        )
        if self.semantic_fingerprint != expected:
            raise ValueError("snapshot_fingerprint_mismatch")
        return self


def projection_fingerprint(
    *,
    projection_id: str,
    projection_policy_version: str,
    canonicalisation_version: str,
    snapshot_id: str,
    snapshot_version: str,
    snapshot_fingerprint_value: str,
    scope: str,
    effective_from_utc: datetime,
    effective_to_utc: datetime,
    as_of_utc: datetime,
    status: ProjectionStatus,
    selected_fields: tuple[SelectedCalendarField, ...],
    unresolved_conflicts: tuple[str, ...],
    missing_mandatory_authority: tuple[str, ...],
    degraded_facts: tuple[str, ...],
    applied_supersessions: tuple[AppliedSupersession, ...],
    closed_authority_classes: tuple[str, ...] = CLOSED_AUTHORITY_CLASSES,
) -> str:
    """Compute deterministic semantic identity for one K04 projection."""

    material = {
        "projection_id": projection_id,
        "projection_policy_version": projection_policy_version,
        "canonicalisation_version": canonicalisation_version,
        "snapshot_id": snapshot_id,
        "snapshot_version": snapshot_version,
        "snapshot_fingerprint": snapshot_fingerprint_value,
        "scope": scope,
        "effective_from_utc": effective_from_utc.isoformat(),
        "effective_to_utc": effective_to_utc.isoformat(),
        "as_of_utc": as_of_utc.isoformat(),
        "status": status,
        "selected_fields": [item.model_dump(mode="json") for item in selected_fields],
        "unresolved_conflicts": unresolved_conflicts,
        "missing_mandatory_authority": missing_mandatory_authority,
        "degraded_facts": degraded_facts,
        "applied_supersessions": [
            item.model_dump(mode="json") for item in applied_supersessions
        ],
        "closed_authority_classes": closed_authority_classes,
    }
    return sha256(_canonical_json(material).encode("utf-8")).hexdigest()


class CalendarProjection(BaseModel):
    """Deterministic side-effect-free K04 projection with closed authority."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    projection_id: str = Field(min_length=1)
    projection_policy_version: str = Field(min_length=1)
    canonicalisation_version: str = Field(min_length=1)
    snapshot_id: str
    snapshot_version: str
    snapshot_fingerprint: str
    scope: str
    effective_from_utc: datetime
    effective_to_utc: datetime
    as_of_utc: datetime
    status: ProjectionStatus
    selected_fields: tuple[SelectedCalendarField, ...] = ()
    unresolved_conflicts: tuple[str, ...] = ()
    missing_mandatory_authority: tuple[str, ...] = ()
    degraded_facts: tuple[str, ...] = ()
    applied_supersessions: tuple[AppliedSupersession, ...] = ()
    semantic_fingerprint: str = Field(min_length=1)
    closed_authority_classes: tuple[str, ...] = CLOSED_AUTHORITY_CLASSES
    foreign_authority_claimed: StrictBool = False

    @model_validator(mode="after")
    def _closed_authority_law(self) -> "CalendarProjection":
        if self.closed_authority_classes != CLOSED_AUTHORITY_CLASSES:
            raise ValueError("calendar_projection_authority_boundary_mismatch")
        if self.foreign_authority_claimed:
            raise ValueError("calendar_projection_foreign_authority_forbidden")
        expected = projection_fingerprint(
            projection_id=self.projection_id,
            projection_policy_version=self.projection_policy_version,
            canonicalisation_version=self.canonicalisation_version,
            snapshot_id=self.snapshot_id,
            snapshot_version=self.snapshot_version,
            snapshot_fingerprint_value=self.snapshot_fingerprint,
            scope=self.scope,
            effective_from_utc=self.effective_from_utc,
            effective_to_utc=self.effective_to_utc,
            as_of_utc=self.as_of_utc,
            status=self.status,
            selected_fields=self.selected_fields,
            unresolved_conflicts=self.unresolved_conflicts,
            missing_mandatory_authority=self.missing_mandatory_authority,
            degraded_facts=self.degraded_facts,
            applied_supersessions=self.applied_supersessions,
            closed_authority_classes=self.closed_authority_classes,
        )
        if self.semantic_fingerprint != expected:
            raise ValueError("projection_fingerprint_mismatch")
        return self
