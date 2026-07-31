"""M03-owned deterministic field candidate resolution and receipt contracts."""

from __future__ import annotations

import json
from datetime import UTC, date, datetime
from enum import Enum
from hashlib import sha256
from math import isfinite
from typing import Any, Literal, TypeAlias

from pydantic import BaseModel, ConfigDict, Field, StrictBool, model_validator

PreparedScalar: TypeAlias = str | int | float | bool | date | datetime | None

CLOSED_FIELD_RESOLUTION_AUTHORITIES = (
    "candidate_expression",
    "risk_posture",
    "capital",
    "broker_order",
    "position_inventory",
    "exit_close",
    "lifecycle",
    "transaction",
    "replay",
)


def _canonical(value: Any) -> Any:
    if isinstance(value, BaseModel):
        return _canonical(value.model_dump(mode="python"))
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, datetime):
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("datetime_must_be_timezone_aware")
        return value.astimezone(UTC).isoformat().replace("+00:00", "Z")
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, dict):
        return {
            str(key): _canonical(item)
            for key, item in sorted(value.items(), key=lambda pair: str(pair[0]))
        }
    if isinstance(value, (tuple, list)):
        return [_canonical(item) for item in value]
    return value


def semantic_fingerprint(value: Any) -> str:
    """Return a deterministic SHA256 fingerprint for semantic material."""

    return sha256(
        json.dumps(
            _canonical(value),
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        ).encode("utf-8")
    ).hexdigest()


def _utc_aware(value: datetime) -> bool:
    return value.tzinfo is not None and value.utcoffset() is not None


def _scalar_is_valid(value: PreparedScalar) -> bool:
    return not isinstance(value, float) or isfinite(value)


def _comparison_value(value: PreparedScalar, value_type: str) -> PreparedScalar:
    """Return the exact policy-typed value used for equality comparison."""

    if value_type == "float" and isinstance(value, (int, float)) and not isinstance(value, bool):
        return float(value)
    return value


def _value_matches_type(value: PreparedScalar, value_type: str) -> bool:
    if value is None:
        return False
    if value_type == "float":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if value_type == "int":
        return isinstance(value, int) and not isinstance(value, bool)
    if value_type == "str":
        return isinstance(value, str)
    if value_type == "bool":
        return isinstance(value, bool)
    if value_type == "date":
        return isinstance(value, date) and not isinstance(value, datetime)
    if value_type == "datetime":
        return isinstance(value, datetime)
    return False


class FieldCandidate(BaseModel):
    """One source-owned candidate for a single semantic prepared field."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    candidate_id: str = Field(min_length=1)
    source_owner: str = Field(min_length=1)
    semantic_field: str = Field(min_length=1)
    candidate_state: Literal["value", "unavailable"]
    value: PreparedScalar
    value_type: Literal["float", "int", "str", "bool", "date", "datetime"]
    unit: str | None = None
    source_artifact_id: str = Field(min_length=1)
    capture_id: str = Field(min_length=1)
    contract_version: str = Field(min_length=1)
    schema_version: str = Field(min_length=1)
    effective_at_utc: datetime
    effective_to_utc: datetime | None = None
    input_fingerprint: str = Field(pattern=r"^[0-9a-f]{64}$")
    validation_state: Literal["valid", "degraded", "unavailable"]
    normalisation_operations: tuple[str, ...] = ()
    limitations: tuple[str, ...] = ()

    @model_validator(mode="after")
    def _validate_candidate(self) -> "FieldCandidate":
        if not _utc_aware(self.effective_at_utc):
            raise ValueError("effective_at_utc_must_be_timezone_aware")
        if self.effective_to_utc is not None:
            if not _utc_aware(self.effective_to_utc):
                raise ValueError("effective_to_utc_must_be_timezone_aware")
            if self.effective_to_utc <= self.effective_at_utc:
                raise ValueError("candidate_effective_interval_invalid")
        if self.capture_id in {self.source_artifact_id, self.input_fingerprint}:
            raise ValueError("capture_identity_must_remain_distinct")
        if not _scalar_is_valid(self.value):
            raise ValueError("field_candidate_value_must_be_finite")
        if self.candidate_state == "value":
            if self.validation_state == "unavailable" or not _value_matches_type(
                self.value, self.value_type
            ):
                raise ValueError("field_candidate_typed_value_required")
        elif self.value is not None or self.validation_state != "unavailable":
            raise ValueError("unavailable_candidate_must_not_claim_value")
        if len(self.normalisation_operations) != len(set(self.normalisation_operations)):
            raise ValueError("duplicate_normalisation_operation")
        return self


class FieldResolutionPolicy(BaseModel):
    """Explicit versioned owner and comparison law for one semantic field."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    policy_id: str = Field(min_length=1)
    policy_version: str = Field(min_length=1)
    output_contract_version: str = Field(min_length=1)
    semantic_field: str = Field(min_length=1)
    mandatory: StrictBool
    admitted_source_roles: tuple[str, ...] = Field(min_length=1)
    value_type: Literal["float", "int", "str", "bool", "date", "datetime"]
    unit: str | None = None
    temporal_comparison_rule: Literal["exact_effective_interval"]
    comparison_rule: Literal["exact"]
    equality_tolerance: float | None = None
    authoritative_owner: str | None = None
    fallback_owners: tuple[str, ...] = ()
    allow_degraded_candidates: StrictBool
    unresolved_consequence: Literal["withhold"]
    optional_absence_consequence: Literal["unavailable", "degraded"]

    @model_validator(mode="after")
    def _validate_policy(self) -> "FieldResolutionPolicy":
        if len(self.admitted_source_roles) != len(set(self.admitted_source_roles)):
            raise ValueError("duplicate_admitted_source_role")
        owners = tuple(
            owner
            for owner in (self.authoritative_owner, *self.fallback_owners)
            if owner is not None
        )
        if any(not owner for owner in owners):
            raise ValueError("empty_field_resolution_owner")
        if len(owners) != len(set(owners)):
            raise ValueError("duplicate_field_resolution_owner")
        if any(owner not in self.admitted_source_roles for owner in owners):
            raise ValueError("field_resolution_owner_not_admitted")
        if self.comparison_rule == "exact" and self.equality_tolerance is not None:
            raise ValueError("exact_comparison_must_not_claim_tolerance")
        return self


class FieldResolutionReceipt(BaseModel):
    """Immutable K06 evidence for one deterministic field-resolution outcome."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    receipt_id: str = Field(min_length=1)
    output_contract_version: str = Field(min_length=1)
    semantic_field: str = Field(min_length=1)
    policy_id: str = Field(min_length=1)
    policy_version: str = Field(min_length=1)
    resolution_status: Literal["selected", "degraded", "unavailable", "withheld"]
    selected_value: PreparedScalar = None
    selected_candidate_id: str | None = None
    selected_source_owner: str | None = None
    selected_source_artifact_id: str | None = None
    selected_capture_id: str | None = None
    candidate_records: tuple[FieldCandidate, ...]
    candidate_ids: tuple[str, ...]
    source_refs: tuple[tuple[str, str], ...]
    comparison_rule: Literal["exact"]
    normalisation_evidence: tuple[tuple[str, tuple[str, ...]], ...]
    equality_result: Literal["equal", "unequal", "not_applicable"]
    unit: str | None = None
    temporal_alignment_result: Literal["exact", "not_applicable"]
    resolution_reason: str = Field(min_length=1)
    rejected_candidate_ids: tuple[str, ...] = ()
    rejection_reasons: tuple[tuple[str, str], ...] = ()
    receipt_fingerprint: str = Field(pattern=r"^[0-9a-f]{64}$")
    closed_authority_classes: tuple[str, ...] = CLOSED_FIELD_RESOLUTION_AUTHORITIES
    foreign_authority_claimed: bool = False

    @model_validator(mode="after")
    def _validate_receipt(self) -> "FieldResolutionReceipt":
        expected_ids = tuple(item.candidate_id for item in self.candidate_records)
        expected_refs = tuple(
            (item.source_artifact_id, item.capture_id) for item in self.candidate_records
        )
        if self.candidate_ids != expected_ids or self.source_refs != expected_refs:
            raise ValueError("candidate_record_lineage_mismatch")
        if len(self.candidate_ids) != len(set(self.candidate_ids)):
            raise ValueError("duplicate_candidate_id_in_receipt")
        rejection_ids = tuple(item[0] for item in self.rejection_reasons)
        if rejection_ids != self.rejected_candidate_ids:
            raise ValueError("rejection_reason_lineage_mismatch")
        if self.resolution_status in {"selected", "degraded"}:
            if self.selected_candidate_id not in self.candidate_ids:
                raise ValueError("selected_candidate_missing_from_receipt_lineage")
            selected = next(
                item
                for item in self.candidate_records
                if item.candidate_id == self.selected_candidate_id
            )
            if (
                self.selected_source_owner != selected.source_owner
                or self.selected_source_artifact_id != selected.source_artifact_id
                or self.selected_capture_id != selected.capture_id
                or self.selected_value != selected.value
            ):
                raise ValueError("selected_candidate_lineage_mismatch")
        elif any(
            value is not None
            for value in (
                self.selected_value,
                self.selected_candidate_id,
                self.selected_source_owner,
                self.selected_source_artifact_id,
                self.selected_capture_id,
            )
        ):
            raise ValueError("non_selected_receipt_must_not_claim_selected_value")
        if self.closed_authority_classes != CLOSED_FIELD_RESOLUTION_AUTHORITIES:
            raise ValueError("field_resolution_foreign_authority_boundary_changed")
        if self.foreign_authority_claimed:
            raise ValueError("field_resolution_foreign_authority_claimed")
        expected = semantic_fingerprint(_receipt_material(self))
        if self.receipt_fingerprint != expected:
            raise ValueError("field_resolution_receipt_fingerprint_mismatch")
        if self.receipt_id != f"resolution:{expected[:24]}":
            raise ValueError("field_resolution_receipt_id_mismatch")
        return self


class MandatoryFieldConflictError(ValueError):
    """Raised when unequal mandatory candidates have no lawful owner rule."""


class MissingMandatoryFieldError(ValueError):
    """Raised when a mandatory semantic field has no admitted candidates."""


def _receipt_material(receipt: FieldResolutionReceipt | dict[str, Any]) -> dict[str, Any]:
    if isinstance(receipt, FieldResolutionReceipt):
        payload = receipt.model_dump(
            mode="python", exclude={"receipt_id", "receipt_fingerprint"}
        )
    else:
        payload = dict(receipt)
        payload.pop("receipt_id", None)
        payload.pop("receipt_fingerprint", None)
    return payload


def _build_receipt(
    *,
    candidates: tuple[FieldCandidate, ...],
    policy: FieldResolutionPolicy,
    status: Literal["selected", "degraded", "unavailable", "withheld"],
    selected: FieldCandidate | None,
    equality_result: Literal["equal", "unequal", "not_applicable"],
    reason: str,
    rejection_reasons: tuple[tuple[str, str], ...] = (),
) -> FieldResolutionReceipt:
    material = {
        "output_contract_version": policy.output_contract_version,
        "semantic_field": policy.semantic_field,
        "policy_id": policy.policy_id,
        "policy_version": policy.policy_version,
        "resolution_status": status,
        "selected_value": None if selected is None else selected.value,
        "selected_candidate_id": None if selected is None else selected.candidate_id,
        "selected_source_owner": None if selected is None else selected.source_owner,
        "selected_source_artifact_id": (
            None if selected is None else selected.source_artifact_id
        ),
        "selected_capture_id": None if selected is None else selected.capture_id,
        "candidate_records": candidates,
        "candidate_ids": tuple(item.candidate_id for item in candidates),
        "source_refs": tuple(
            (item.source_artifact_id, item.capture_id) for item in candidates
        ),
        "comparison_rule": policy.comparison_rule,
        "normalisation_evidence": tuple(
            (item.candidate_id, item.normalisation_operations) for item in candidates
        ),
        "equality_result": equality_result,
        "unit": policy.unit,
        "temporal_alignment_result": (
            "exact" if candidates else "not_applicable"
        ),
        "resolution_reason": reason,
        "rejected_candidate_ids": tuple(item[0] for item in rejection_reasons),
        "rejection_reasons": rejection_reasons,
        "closed_authority_classes": CLOSED_FIELD_RESOLUTION_AUTHORITIES,
        "foreign_authority_claimed": False,
    }
    fingerprint = semantic_fingerprint(material)
    return FieldResolutionReceipt(
        **material,
        receipt_id=f"resolution:{fingerprint[:24]}",
        receipt_fingerprint=fingerprint,
    )


def _validate_candidate_against_policy(
    candidate: FieldCandidate, policy: FieldResolutionPolicy
) -> None:
    if candidate.semantic_field != policy.semantic_field:
        raise ValueError("field_candidate_semantic_field_mismatch")
    if candidate.source_owner not in policy.admitted_source_roles:
        raise ValueError("field_candidate_source_role_not_admitted")
    if candidate.value_type != policy.value_type or candidate.unit != policy.unit:
        raise ValueError("field_candidate_type_or_unit_mismatch")
    if candidate.validation_state == "degraded" and not policy.allow_degraded_candidates:
        raise ValueError("degraded_field_candidate_not_admitted")


def resolve_canonical_field(
    *,
    candidates: tuple[FieldCandidate, ...],
    policy: FieldResolutionPolicy,
) -> FieldResolutionReceipt:
    """Resolve one semantic field without caller-order or downstream authority."""

    governed_policy = FieldResolutionPolicy.model_validate(
        policy.model_dump(mode="python")
    )
    ordered = tuple(
        sorted(
            (
                FieldCandidate.model_validate(item.model_dump(mode="python"))
                for item in candidates
            ),
            key=lambda item: item.candidate_id,
        )
    )
    if len(ordered) != len({item.candidate_id for item in ordered}):
        raise ValueError("duplicate_field_candidate_id")
    for candidate in ordered:
        _validate_candidate_against_policy(candidate, governed_policy)
    policy = governed_policy

    if not ordered:
        if policy.mandatory:
            raise MissingMandatoryFieldError(policy.semantic_field)
        return _build_receipt(
            candidates=ordered,
            policy=policy,
            status=policy.optional_absence_consequence,
            selected=None,
            equality_result="not_applicable",
            reason=f"optional_field_{policy.optional_absence_consequence}",
        )

    unavailable = tuple(
        item for item in ordered if item.candidate_state == "unavailable"
    )
    eligible = tuple(item for item in ordered if item.candidate_state == "value")
    unavailable_reasons = tuple(
        (item.candidate_id, "candidate_unavailable") for item in unavailable
    )
    if not eligible:
        if policy.mandatory:
            raise MissingMandatoryFieldError(policy.semantic_field)
        return _build_receipt(
            candidates=ordered,
            policy=policy,
            status=policy.optional_absence_consequence,
            selected=None,
            equality_result="not_applicable",
            reason=f"optional_field_{policy.optional_absence_consequence}",
            rejection_reasons=unavailable_reasons,
        )

    temporal_keys = {
        (item.effective_at_utc, item.effective_to_utc) for item in eligible
    }
    if len(temporal_keys) != 1:
        raise ValueError("field_candidate_temporal_applicability_mismatch")

    value_keys = {
        semantic_fingerprint(
            {
                "value_type": policy.value_type,
                "value": _comparison_value(item.value, policy.value_type),
            }
        )
        for item in eligible
    }
    if len(value_keys) == 1:
        selected = eligible[0]
        degraded = any(item.validation_state == "degraded" for item in eligible)
        return _build_receipt(
            candidates=ordered,
            policy=policy,
            status="degraded" if degraded else "selected",
            selected=selected,
            equality_result="equal",
            reason=(
                "semantically_equal_degraded_coalesced"
                if degraded
                else "semantically_equal_coalesced"
            ),
            rejection_reasons=unavailable_reasons,
        )

    owner_order = tuple(
        owner
        for owner in (policy.authoritative_owner, *policy.fallback_owners)
        if owner is not None
    )
    for owner in owner_order:
        owned = tuple(item for item in eligible if item.source_owner == owner)
        if len(owned) == 1:
            selected = owned[0]
            reason = (
                "authoritative_owner_selected"
                if owner == policy.authoritative_owner
                else "fallback_owner_selected"
            )
            rejected = unavailable_reasons + tuple(
                (item.candidate_id, f"not_selected_under_{reason}")
                for item in eligible
                if item.candidate_id != selected.candidate_id
            )
            return _build_receipt(
                candidates=ordered,
                policy=policy,
                status=(
                    "degraded" if selected.validation_state == "degraded" else "selected"
                ),
                selected=selected,
                equality_result="unequal",
                reason=reason,
                rejection_reasons=rejected,
            )
        if len(owned) > 1:
            owner_values = {
                semantic_fingerprint(
                    {
                        "value_type": policy.value_type,
                        "value": _comparison_value(item.value, policy.value_type),
                    }
                )
                for item in owned
            }
            if len(owner_values) == 1:
                selected = owned[0]
                rejected = unavailable_reasons + tuple(
                    (item.candidate_id, "outside_selected_owner")
                    for item in eligible
                    if item.source_owner != owner
                )
                return _build_receipt(
                    candidates=ordered,
                    policy=policy,
                    status=(
                        "degraded"
                        if any(item.validation_state == "degraded" for item in owned)
                        else "selected"
                    ),
                    selected=selected,
                    equality_result="unequal",
                    reason=(
                        "authoritative_owner_equal_candidates_coalesced"
                        if owner == policy.authoritative_owner
                        else "fallback_owner_equal_candidates_coalesced"
                    ),
                    rejection_reasons=rejected,
                )
            break

    if policy.mandatory:
        raise MandatoryFieldConflictError(policy.semantic_field)
    conflict_reasons = unavailable_reasons + tuple(
        (item.candidate_id, "optional_field_unresolved_conflict") for item in eligible
    )
    return _build_receipt(
        candidates=ordered,
        policy=policy,
        status=policy.unresolved_consequence,
        selected=None,
        equality_result="unequal",
        reason="optional_field_conflict_withheld",
        rejection_reasons=conflict_reasons,
    )


__all__ = [
    "CLOSED_FIELD_RESOLUTION_AUTHORITIES",
    "FieldCandidate",
    "FieldResolutionPolicy",
    "FieldResolutionReceipt",
    "MandatoryFieldConflictError",
    "MissingMandatoryFieldError",
    "PreparedScalar",
    "resolve_canonical_field",
    "semantic_fingerprint",
]
