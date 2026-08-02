"""Deterministic side-effect-free builder for M03 K05/K06 authority."""

from __future__ import annotations

from datetime import datetime
from typing import Mapping

from nvda_desk.contracts.prepared_data import (
    CLOSED_PREPARATION_AUTHORITIES,
    CalendarProjectionReference,
    DerivationReceipt,
    PreparedDataEnvelope,
    PreparedRuntimePayloadV1,
    SourceCaptureReference,
    prepared_envelope_fingerprint,
    prepared_input_fingerprint,
)
from nvda_desk.preparation.field_resolution import FieldResolutionReceipt


class PreparedDataBuilder:
    """Build one canonical prepared envelope from caller-owned admitted evidence."""

    def build(
        self,
        *,
        source_capture_refs: tuple[SourceCaptureReference, ...],
        input_schema_versions: Mapping[str, str],
        calendar_projection_refs: tuple[CalendarProjectionReference, ...] = (),
        schema_version: str,
        preparation_policy_version: str,
        alignment_policy_version: str,
        fingerprint_policy_version: str,
        canonicalisation_version: str,
        derivation_versions: Mapping[str, str],
        effective_at_utc: datetime,
        payload: PreparedRuntimePayloadV1,
        payload_schema_version: str,
        field_resolution_receipts: tuple[FieldResolutionReceipt, ...] = (),
        derivation_receipts: tuple[DerivationReceipt, ...] = (),
        validation_state: str = "valid",
        completeness_state: str = "complete",
        limitations: tuple[str, ...] = (),
        failed_mandatory_transformations: tuple[str, ...] = (),
        missing_optional_enrichments: tuple[str, ...] = (),
        parent_prepared_ids: tuple[str, ...] = (),
    ) -> PreparedDataEnvelope:
        """Return one deterministic prepared envelope from caller-owned evidence."""

        if not source_capture_refs:
            raise ValueError("source_capture_refs_required")
        for value, reason in (
            (schema_version, "schema_version_required"),
            (preparation_policy_version, "preparation_policy_version_required"),
            (alignment_policy_version, "alignment_policy_version_required"),
            (fingerprint_policy_version, "fingerprint_policy_version_required"),
            (canonicalisation_version, "canonicalisation_version_required"),
            (payload_schema_version, "payload_schema_version_required"),
        ):
            if not value:
                raise ValueError(reason)
        if failed_mandatory_transformations:
            raise ValueError("failed_mandatory_transformation_withholds_envelope")

        refs = tuple(
            sorted(
                (
                    SourceCaptureReference.model_validate(item.model_dump(mode="python"))
                    for item in source_capture_refs
                ),
                key=lambda item: (item.capture_id, item.source_artifact_id),
            )
        )
        projection_refs = tuple(
            sorted(
                (
                    CalendarProjectionReference.model_validate(item.model_dump(mode="python"))
                    for item in calendar_projection_refs
                ),
                key=lambda item: item.projection_id,
            )
        )
        governed_payload = PreparedRuntimePayloadV1.model_validate(
            payload.model_dump(mode="python")
        )
        schema_versions = tuple(sorted(dict(input_schema_versions).items()))
        declared_derivations = tuple(sorted(dict(derivation_versions).items()))
        resolutions = tuple(
            sorted(
                (
                    FieldResolutionReceipt.model_validate(item.model_dump(mode="python"))
                    for item in field_resolution_receipts
                ),
                key=lambda item: (item.semantic_field, item.receipt_id),
            )
        )
        derivations = tuple(
            sorted(
                (
                    DerivationReceipt.model_validate(item.model_dump(mode="python"))
                    for item in derivation_receipts
                ),
                key=lambda item: (item.semantic_field, item.derivation_id),
            )
        )
        receipt_derivations = {
            receipt.semantic_field: receipt.derivation_version for receipt in derivations
        }
        if dict(declared_derivations) != receipt_derivations:
            raise ValueError("derivation_version_or_input_provenance_mismatch")

        input_fingerprint = prepared_input_fingerprint(
            refs,
            schema_versions,
            calendar_projection_refs=projection_refs,
            fingerprint_policy_version=fingerprint_policy_version,
            canonicalisation_version=canonicalisation_version,
        )
        prepared_fingerprint = prepared_envelope_fingerprint(
            schema_version=schema_version,
            source_capture_refs=refs,
            calendar_projection_refs=projection_refs,
            input_schema_versions=schema_versions,
            preparation_policy_version=preparation_policy_version,
            alignment_policy_version=alignment_policy_version,
            fingerprint_policy_version=fingerprint_policy_version,
            canonicalisation_version=canonicalisation_version,
            derivation_versions=declared_derivations,
            effective_at_utc=effective_at_utc,
            input_fingerprint=input_fingerprint,
            validation_state=validation_state,
            completeness_state=completeness_state,
            limitations=limitations,
            failed_mandatory_transformations=failed_mandatory_transformations,
            missing_optional_enrichments=missing_optional_enrichments,
            parent_prepared_ids=parent_prepared_ids,
            payload_kind=governed_payload.kind,
            payload_schema_version=payload_schema_version,
            payload=governed_payload,
            field_resolution_receipts=resolutions,
            derivation_receipts=derivations,
        )
        return PreparedDataEnvelope(
            prepared_id=f"prepared:{prepared_fingerprint[:24]}",
            schema_version=schema_version,
            source_capture_refs=refs,
            calendar_projection_refs=projection_refs,
            input_schema_versions=schema_versions,
            preparation_policy_version=preparation_policy_version,
            alignment_policy_version=alignment_policy_version,
            fingerprint_policy_version=fingerprint_policy_version,
            canonicalisation_version=canonicalisation_version,
            derivation_versions=declared_derivations,
            effective_at_utc=effective_at_utc,
            input_fingerprint=input_fingerprint,
            prepared_fingerprint=prepared_fingerprint,
            validation_state=validation_state,
            completeness_state=completeness_state,
            limitations=limitations,
            failed_mandatory_transformations=failed_mandatory_transformations,
            missing_optional_enrichments=missing_optional_enrichments,
            parent_prepared_ids=parent_prepared_ids,
            payload_kind=governed_payload.kind,
            payload_schema_version=payload_schema_version,
            payload=governed_payload,
            field_resolution_receipts=resolutions,
            derivation_receipts=derivations,
            closed_authority_classes=CLOSED_PREPARATION_AUTHORITIES,
            foreign_authority_claimed=False,
        )
