"""M03 K05 prepared-data envelope, payload and derivation contracts."""

from __future__ import annotations

from datetime import date, datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from nvda_desk.preparation.field_resolution import (
    FieldResolutionReceipt,
    PreparedScalar,
    semantic_fingerprint,
)

CLOSED_PREPARATION_AUTHORITIES = (
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


def _utc_aware(value: datetime) -> bool:
    return value.tzinfo is not None and value.utcoffset() is not None


def _sorted_pairs(value: Any) -> tuple[tuple[str, str], ...]:
    if isinstance(value, dict):
        pairs = tuple(value.items())
    else:
        pairs = tuple(tuple(item) for item in value)
    if any(len(item) != 2 or not item[0] or not item[1] for item in pairs):
        raise ValueError("version_mapping_entries_must_be_named")
    if len({item[0] for item in pairs}) != len(pairs):
        raise ValueError("duplicate_version_mapping_key")
    return tuple(sorted((str(key), str(version)) for key, version in pairs))


def _prepared_values_equal(left: PreparedScalar, right: PreparedScalar) -> bool:
    """Compare governed scalar facts without conflating booleans and numbers."""

    if isinstance(left, bool) or isinstance(right, bool):
        return type(left) is type(right) and left == right
    if isinstance(left, (int, float)) and isinstance(right, (int, float)):
        return float(left) == float(right)
    return left == right


class SourceCaptureReference(BaseModel):
    """Admitted source artefact and repository capture identity carried into M03."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    capture_id: str = Field(min_length=1)
    source_artifact_id: str = Field(min_length=1)
    family_id: str = Field(min_length=1)
    contract_id: str = Field(min_length=1)
    schema_version: str = Field(min_length=1)
    source_owner: str = Field(min_length=1)
    effective_at_utc: datetime
    source_time_utc: datetime | None = None
    source_date: date | None = None
    temporal_precision: Literal["instant", "date"]
    input_fingerprint: str = Field(pattern=r"^[0-9a-f]{64}$")
    validation_state: Literal["valid", "degraded"]
    limitations: tuple[str, ...]
    semantic_fields: tuple[str, ...] = Field(min_length=1)
    provider_id: str | None = None
    acquisition_method: str | None = None

    @model_validator(mode="after")
    def _validate_reference(self) -> "SourceCaptureReference":
        if not _utc_aware(self.effective_at_utc):
            raise ValueError("effective_at_utc_must_be_timezone_aware")
        if self.capture_id in {self.source_artifact_id, self.input_fingerprint}:
            raise ValueError("capture_identity_must_remain_distinct")
        if self.temporal_precision == "instant":
            if self.source_time_utc is None or self.source_date is not None:
                raise ValueError("instant_source_temporal_fact_required")
            if not _utc_aware(self.source_time_utc):
                raise ValueError("source_time_utc_must_be_timezone_aware")
        elif self.source_date is None or self.source_time_utc is not None:
            raise ValueError("date_source_temporal_fact_required")
        if len(self.semantic_fields) != len(set(self.semantic_fields)):
            raise ValueError("duplicate_source_semantic_field")
        if (self.provider_id is None) != (self.acquisition_method is None):
            raise ValueError("provider_acquisition_facts_must_be_paired")
        return self


class PreparedEventWindow(BaseModel):
    """Typed event-window member admitted into the prepared runtime payload."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    event_id: str = Field(min_length=1)
    window_start_utc: datetime
    window_end_utc: datetime
    tags: tuple[str, ...] = ()

    @model_validator(mode="after")
    def _validate_window(self) -> "PreparedEventWindow":
        if not _utc_aware(self.window_start_utc) or not _utc_aware(self.window_end_utc):
            raise ValueError("prepared_event_window_must_be_timezone_aware")
        if self.window_end_utc < self.window_start_utc:
            raise ValueError("prepared_event_window_end_before_start")
        return self


class PreparedRuntimePayloadV1(BaseModel):
    """Tagged typed alpha payload for the bounded M03 prepared runtime seam."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    kind: Literal["prepared_runtime_v1"] = "prepared_runtime_v1"
    source_time_utc: datetime | None = None
    source_date: date | None = None
    runtime_bar_time_utc: datetime | None = None
    spot_price: float | None = None
    market_spot_price: float | None = None
    options_spot_price: float | None = None
    front_dte: int | None = None
    next_dte: int | None = None
    windows: tuple[PreparedEventWindow, ...] = ()
    next_event_time_utc: datetime | None = None
    prior_close: float | None = None
    previous_close: float | None = None
    reference_close: float | None = None
    nvda_return_pct: float | None = None
    nq_return_pct: float | None = None
    vix_level: float | None = None
    window_count: int | None = None
    has_windows: bool | None = None
    minutes_to_next_event: int | None = None
    front_to_next_dte_spread: int | None = None

    @model_validator(mode="after")
    def _validate_temporal_fields(self) -> "PreparedRuntimePayloadV1":
        for value in (
            self.source_time_utc,
            self.runtime_bar_time_utc,
            self.next_event_time_utc,
        ):
            if value is not None and not _utc_aware(value):
                raise ValueError("prepared_payload_datetime_must_be_timezone_aware")
        return self


class DerivationReceipt(BaseModel):
    """Immutable evidence for one material deterministic prepared-field derivation."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    derivation_id: str = Field(min_length=1)
    semantic_field: str = Field(min_length=1)
    derivation_version: str = Field(min_length=1)
    input_semantic_fields: tuple[str, ...] = Field(min_length=1)
    input_candidate_ids: tuple[str, ...] = Field(min_length=1)
    input_fingerprints: tuple[str, ...] = Field(min_length=1)
    operation: str = Field(min_length=1)
    unit_alignment_policy: str = Field(min_length=1)
    temporal_alignment_policy: str = Field(min_length=1)
    result_state: Literal["derived", "missing", "failed"]
    value: PreparedScalar
    receipt_fingerprint: str | None = Field(
        default=None, pattern=r"^[0-9a-f]{64}$"
    )

    @model_validator(mode="after")
    def _validate_derivation(self) -> "DerivationReceipt":
        if len(self.input_candidate_ids) != len(set(self.input_candidate_ids)):
            raise ValueError("duplicate_derivation_input_candidate_id")
        if len(self.input_semantic_fields) != len(self.input_candidate_ids):
            raise ValueError("derivation_input_semantic_lineage_mismatch")
        if len(self.input_fingerprints) != len(self.input_candidate_ids):
            raise ValueError("derivation_input_fingerprint_lineage_mismatch")
        if any(
            len(item) != 64
            or any(character not in "0123456789abcdef" for character in item)
            for item in self.input_fingerprints
        ):
            raise ValueError("derivation_input_fingerprint_invalid")
        if self.result_state == "derived" and self.value is None:
            raise ValueError("derived_result_value_required")
        if self.result_state != "derived" and self.value is not None:
            raise ValueError("non_derived_result_must_not_claim_value")
        expected = semantic_fingerprint(
            self.model_dump(mode="python", exclude={"receipt_fingerprint"})
        )
        if self.receipt_fingerprint is None:
            object.__setattr__(self, "receipt_fingerprint", expected)
        elif self.receipt_fingerprint != expected:
            raise ValueError("derivation_receipt_fingerprint_mismatch")
        return self


class PreparedDataEnvelope(BaseModel):
    """Immutable K05 authority envelope for one tagged prepared runtime payload."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    prepared_id: str = Field(min_length=1)
    schema_version: str = Field(min_length=1)
    source_capture_refs: tuple[SourceCaptureReference, ...] = Field(min_length=1)
    input_schema_versions: tuple[tuple[str, str], ...] = Field(min_length=1)
    preparation_policy_version: str = Field(min_length=1)
    alignment_policy_version: str = Field(min_length=1)
    fingerprint_policy_version: str = Field(min_length=1)
    canonicalisation_version: str = Field(min_length=1)
    derivation_versions: tuple[tuple[str, str], ...]
    effective_at_utc: datetime
    input_fingerprint: str = Field(pattern=r"^[0-9a-f]{64}$")
    prepared_fingerprint: str = Field(pattern=r"^[0-9a-f]{64}$")
    validation_state: Literal["valid", "degraded"]
    completeness_state: Literal["complete", "degraded"]
    limitations: tuple[str, ...]
    failed_mandatory_transformations: tuple[str, ...]
    missing_optional_enrichments: tuple[str, ...]
    parent_prepared_ids: tuple[str, ...]
    payload_kind: Literal["prepared_runtime_v1"]
    payload_schema_version: Literal["1.0.0"]
    payload: PreparedRuntimePayloadV1
    field_resolution_receipts: tuple[FieldResolutionReceipt, ...] = ()
    derivation_receipts: tuple[DerivationReceipt, ...] = ()
    closed_authority_classes: tuple[str, ...] = CLOSED_PREPARATION_AUTHORITIES
    foreign_authority_claimed: bool = False

    @field_validator("input_schema_versions", "derivation_versions", mode="before")
    @classmethod
    def _normalise_version_pairs(cls, value: Any) -> tuple[tuple[str, str], ...]:
        return _sorted_pairs(value)

    @model_validator(mode="after")
    def _validate_envelope(self) -> "PreparedDataEnvelope":
        if not _utc_aware(self.effective_at_utc):
            raise ValueError("effective_at_utc_must_be_timezone_aware")
        if self.payload_kind != self.payload.kind:
            raise ValueError("payload_kind_must_match_tagged_typed_payload")
        if self.closed_authority_classes != CLOSED_PREPARATION_AUTHORITIES:
            raise ValueError("prepared_data_foreign_authority_boundary_changed")
        if self.foreign_authority_claimed:
            raise ValueError("prepared_data_foreign_authority_claimed")
        if self.failed_mandatory_transformations:
            raise ValueError("failed_mandatory_transformation_withholds_envelope")
        if self.validation_state == "valid" and (
            self.completeness_state != "complete"
            or self.limitations
            or self.missing_optional_enrichments
        ):
            raise ValueError("valid_envelope_must_be_complete_without_gaps")
        if self.validation_state == "degraded" and (
            self.completeness_state != "degraded"
            or not (self.limitations or self.missing_optional_enrichments)
        ):
            raise ValueError("degraded_envelope_requires_explicit_gap")
        if len(self.parent_prepared_ids) != len(set(self.parent_prepared_ids)):
            raise ValueError("duplicate_parent_prepared_identity")
        receipt_ids = tuple(item.receipt_id for item in self.field_resolution_receipts)
        if len(receipt_ids) != len(set(receipt_ids)):
            raise ValueError("duplicate_field_resolution_receipt")

        degraded_sources = tuple(
            item for item in self.source_capture_refs if item.validation_state == "degraded"
        )
        if degraded_sources and self.validation_state != "degraded":
            raise ValueError("degraded_source_cannot_form_valid_envelope")
        degraded_limitations = {
            limitation for item in degraded_sources for limitation in item.limitations
        }
        if not degraded_limitations <= set(self.limitations):
            raise ValueError("degraded_source_limitations_not_preserved")

        receipts_by_field: dict[str, list[FieldResolutionReceipt]] = {}
        for receipt in self.field_resolution_receipts:
            receipts_by_field.setdefault(receipt.semantic_field, []).append(receipt)
        if any(len(items) != 1 for items in receipts_by_field.values()):
            raise ValueError("duplicate_field_resolution_semantic_field")

        payload_fields = set(PreparedRuntimePayloadV1.model_fields) - {"kind"}
        source_refs_by_field: dict[str, set[tuple[str, str]]] = {}
        for source in self.source_capture_refs:
            for semantic_field in source.semantic_fields:
                if semantic_field in payload_fields:
                    source_refs_by_field.setdefault(semantic_field, set()).add(
                        (source.source_artifact_id, source.capture_id)
                    )
        for semantic_field, contributing_refs in source_refs_by_field.items():
            if len(contributing_refs) <= 1:
                continue
            receipts = receipts_by_field.get(semantic_field, [])
            if len(receipts) != 1 or set(receipts[0].source_refs) != contributing_refs:
                raise ValueError("competing_payload_sources_require_resolution")

        for receipt in self.field_resolution_receipts:
            if receipt.semantic_field not in payload_fields:
                raise ValueError("resolution_receipt_semantic_field_not_in_payload")
            payload_value = getattr(self.payload, receipt.semantic_field)
            if receipt.resolution_status in {"selected", "degraded"}:
                if not _prepared_values_equal(receipt.selected_value, payload_value):
                    raise ValueError("resolution_receipt_payload_value_mismatch")
            elif payload_value is not None:
                raise ValueError("unresolved_receipt_cannot_coexist_with_payload_value")

        for receipt in self.derivation_receipts:
            if receipt.semantic_field not in payload_fields:
                raise ValueError("derivation_receipt_semantic_field_not_in_payload")
            payload_value = getattr(self.payload, receipt.semantic_field)
            if receipt.result_state == "derived":
                if not _prepared_values_equal(receipt.value, payload_value):
                    raise ValueError("derivation_receipt_payload_value_mismatch")
            elif payload_value is not None:
                raise ValueError("non_derived_receipt_cannot_coexist_with_payload_value")

        expected_input = prepared_input_fingerprint(
            self.source_capture_refs,
            self.input_schema_versions,
            fingerprint_policy_version=self.fingerprint_policy_version,
            canonicalisation_version=self.canonicalisation_version,
        )
        if self.input_fingerprint != expected_input:
            raise ValueError("input_fingerprint_mismatch")

        declared_derivations = dict(self.derivation_versions)
        receipt_derivations = {
            receipt.semantic_field: receipt.derivation_version
            for receipt in self.derivation_receipts
        }
        if declared_derivations != receipt_derivations:
            raise ValueError("derivation_version_or_input_provenance_mismatch")

        expected_prepared = prepared_envelope_fingerprint(
            schema_version=self.schema_version,
            source_capture_refs=self.source_capture_refs,
            input_schema_versions=self.input_schema_versions,
            preparation_policy_version=self.preparation_policy_version,
            alignment_policy_version=self.alignment_policy_version,
            fingerprint_policy_version=self.fingerprint_policy_version,
            canonicalisation_version=self.canonicalisation_version,
            derivation_versions=self.derivation_versions,
            effective_at_utc=self.effective_at_utc,
            input_fingerprint=self.input_fingerprint,
            validation_state=self.validation_state,
            completeness_state=self.completeness_state,
            limitations=self.limitations,
            failed_mandatory_transformations=self.failed_mandatory_transformations,
            missing_optional_enrichments=self.missing_optional_enrichments,
            parent_prepared_ids=self.parent_prepared_ids,
            payload_kind=self.payload_kind,
            payload_schema_version=self.payload_schema_version,
            payload=self.payload,
            field_resolution_receipts=self.field_resolution_receipts,
            derivation_receipts=self.derivation_receipts,
            closed_authority_classes=self.closed_authority_classes,
            foreign_authority_claimed=self.foreign_authority_claimed,
        )
        if self.prepared_fingerprint != expected_prepared:
            raise ValueError("prepared_fingerprint_mismatch")
        if self.prepared_id != f"prepared:{expected_prepared[:24]}":
            raise ValueError("prepared_id_must_derive_from_prepared_fingerprint")
        return self


def _sorted_source_refs(
    refs: tuple[SourceCaptureReference, ...],
) -> tuple[SourceCaptureReference, ...]:
    return tuple(
        sorted(refs, key=lambda item: (item.capture_id, item.source_artifact_id))
    )


def prepared_input_fingerprint(
    source_capture_refs: tuple[SourceCaptureReference, ...],
    input_schema_versions: tuple[tuple[str, str], ...] | dict[str, str],
    *,
    fingerprint_policy_version: str,
    canonicalisation_version: str,
) -> str:
    """Fingerprint exact admitted source/capture inputs and schema versions."""

    return semantic_fingerprint(
        {
            "fingerprint_policy_version": fingerprint_policy_version,
            "canonicalisation_version": canonicalisation_version,
            "source_capture_refs": [
                item.model_dump(mode="python")
                for item in _sorted_source_refs(source_capture_refs)
            ],
            "input_schema_versions": _sorted_pairs(input_schema_versions),
        }
    )


def prepared_envelope_fingerprint(
    *,
    schema_version: str,
    source_capture_refs: tuple[SourceCaptureReference, ...],
    input_schema_versions: tuple[tuple[str, str], ...],
    preparation_policy_version: str,
    alignment_policy_version: str,
    fingerprint_policy_version: str,
    canonicalisation_version: str,
    derivation_versions: tuple[tuple[str, str], ...],
    effective_at_utc: datetime,
    input_fingerprint: str,
    validation_state: str,
    completeness_state: str,
    limitations: tuple[str, ...],
    failed_mandatory_transformations: tuple[str, ...],
    missing_optional_enrichments: tuple[str, ...],
    parent_prepared_ids: tuple[str, ...],
    payload_kind: str,
    payload_schema_version: str,
    payload: PreparedRuntimePayloadV1,
    field_resolution_receipts: tuple[FieldResolutionReceipt, ...],
    derivation_receipts: tuple[DerivationReceipt, ...],
    closed_authority_classes: tuple[str, ...] = CLOSED_PREPARATION_AUTHORITIES,
    foreign_authority_claimed: bool = False,
) -> str:
    """Fingerprint one complete semantic prepared-data authority object."""

    return semantic_fingerprint(
        {
            "schema_version": schema_version,
            "source_capture_refs": [
                item.model_dump(mode="python")
                for item in _sorted_source_refs(source_capture_refs)
            ],
            "input_schema_versions": _sorted_pairs(input_schema_versions),
            "preparation_policy_version": preparation_policy_version,
            "alignment_policy_version": alignment_policy_version,
            "fingerprint_policy_version": fingerprint_policy_version,
            "canonicalisation_version": canonicalisation_version,
            "derivation_versions": _sorted_pairs(derivation_versions),
            "effective_at_utc": effective_at_utc,
            "input_fingerprint": input_fingerprint,
            "validation_state": validation_state,
            "completeness_state": completeness_state,
            "limitations": limitations,
            "failed_mandatory_transformations": failed_mandatory_transformations,
            "missing_optional_enrichments": missing_optional_enrichments,
            "parent_prepared_ids": parent_prepared_ids,
            "payload_kind": payload_kind,
            "payload_schema_version": payload_schema_version,
            "payload": payload,
            "field_resolution_receipts": tuple(
                sorted(
                    field_resolution_receipts,
                    key=lambda item: (item.semantic_field, item.receipt_id),
                )
            ),
            "derivation_receipts": tuple(
                sorted(
                    derivation_receipts,
                    key=lambda item: (item.semantic_field, item.derivation_id),
                )
            ),
            "closed_authority_classes": closed_authority_classes,
            "foreign_authority_claimed": foreign_authority_claimed,
        }
    )


__all__ = [
    "CLOSED_PREPARATION_AUTHORITIES",
    "DerivationReceipt",
    "PreparedDataEnvelope",
    "PreparedEventWindow",
    "PreparedRuntimePayloadV1",
    "SourceCaptureReference",
    "prepared_envelope_fingerprint",
    "prepared_input_fingerprint",
]
