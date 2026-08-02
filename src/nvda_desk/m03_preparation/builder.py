"""Deterministic M03 builder from exact M01/M02 owner evidence."""

from __future__ import annotations

import json
from datetime import date, datetime
from hashlib import sha256
from typing import Any

from pydantic import ValidationError

from nvda_desk.contracts.prepared_data import (
    CLOSED_PREPARATION_AUTHORITIES,
    CalendarProjectionReference,
    DerivationReceipt,
    PreparedDataEnvelope,
    PreparedDerivationRule,
    PreparedRuntimePayloadV1,
    SourceCaptureReference,
    prepared_envelope_fingerprint,
    prepared_input_fingerprint,
)
from nvda_desk.m01_source_admission import (
    SourceArtifactEnvelope,
    SourceDownstreamOwner,
    SourceFactRequirement,
    SourceSemanticBinding,
)
from nvda_desk.m02_financial_calendar import CalendarProjection
from nvda_desk.preparation.field_resolution import (
    FieldCandidate,
    FieldResolutionPolicy,
    FieldResolutionReceipt,
    resolve_canonical_field,
    semantic_fingerprint,
)


def _binding_value_matches(value: Any, binding: SourceSemanticBinding) -> bool:
    if value is None:
        return binding.requirement is SourceFactRequirement.OPTIONAL
    if binding.value_type == "float":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if binding.value_type == "int":
        return isinstance(value, int) and not isinstance(value, bool)
    if binding.value_type == "str":
        return isinstance(value, str)
    if binding.value_type == "bool":
        return isinstance(value, bool)
    if binding.value_type == "date":
        from datetime import date

        return isinstance(value, date) and not isinstance(value, datetime)
    if binding.value_type == "datetime":
        return isinstance(value, datetime) and value.tzinfo is not None
    return False


def _revalidate_source_artifact(value: SourceArtifactEnvelope) -> SourceArtifactEnvelope:
    if not isinstance(value, SourceArtifactEnvelope):
        raise TypeError("typed_m01_source_artifact_required")
    try:
        payload_model = type(value.typed_payload)
        typed_payload = payload_model.model_validate(
            value.typed_payload.model_dump(mode="python")
        ).model_copy(deep=True)
        material = value.model_dump(mode="python", exclude={"typed_payload"})
        material["typed_payload"] = typed_payload
        governed = SourceArtifactEnvelope.model_validate(material)
    except (ValidationError, TypeError, ValueError) as exc:
        raise ValueError("source_artifact_contract_invalid") from exc
    try:
        captured = json.loads(governed.captured_material.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("source_artifact_evidence_mismatch") from exc
    fingerprint = sha256(governed.captured_material).hexdigest()
    if (
        governed.downstream_owner is not SourceDownstreamOwner.M03
        or governed.content_sha256 != fingerprint
        or governed.capture_receipt.content_sha256 != fingerprint
        or captured != governed.typed_payload.model_dump(mode="json")
    ):
        raise ValueError("source_artifact_evidence_mismatch")
    for binding in governed.semantic_bindings:
        if binding.payload_field not in type(governed.typed_payload).model_fields:
            raise ValueError("source_artifact_evidence_mismatch")
        bound_value = getattr(governed.typed_payload, binding.payload_field)
        if not _binding_value_matches(bound_value, binding):
            raise ValueError("source_artifact_evidence_mismatch")
    return governed


def _revalidate_projection(value: CalendarProjection) -> CalendarProjection:
    if not isinstance(value, CalendarProjection):
        raise TypeError("typed_m02_calendar_projection_required")
    try:
        return CalendarProjection.model_validate(value.model_dump(mode="python"))
    except (ValidationError, TypeError, ValueError) as exc:
        raise ValueError("calendar_projection_contract_invalid") from exc


def _source_candidate(
    artifact: SourceArtifactEnvelope,
    binding: SourceSemanticBinding,
    *,
    effective_at_utc: datetime,
) -> FieldCandidate:
    value = getattr(artifact.typed_payload, binding.payload_field)
    return FieldCandidate(
        candidate_id=f"m01:{artifact.source_artifact_id}:{binding.semantic_field}",
        source_owner=artifact.source_identifier.owner or artifact.provider_id,
        semantic_field=binding.semantic_field,
        candidate_state="unavailable" if value is None else "value",
        value=value,
        value_type=binding.value_type,
        unit=binding.unit,
        source_artifact_id=artifact.source_artifact_id,
        capture_id=artifact.capture_receipt.capture_id,
        contract_version=artifact.contract_id,
        schema_version=artifact.schema_version,
        effective_at_utc=artifact.observed_at_utc or effective_at_utc,
        input_fingerprint=artifact.content_sha256,
        validation_state=(
            ("valid" if artifact.validation_status == "admitted" else "degraded")
            if value is not None
            else "unavailable"
        ),
        limitations=artifact.limitations,
    )


def _calendar_selected_value(selected: Any) -> Any:
    value = selected.value
    if value is None:
        return None
    if selected.value_type == "datetime" and isinstance(value, str):
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if parsed.tzinfo is None or parsed.utcoffset() is None:
            raise ValueError("calendar_projection_datetime_must_be_timezone_aware")
        return parsed
    if selected.value_type == "date" and isinstance(value, str):
        return date.fromisoformat(value)
    return value


def _calendar_candidate(
    projection: CalendarProjection,
    selected: Any,
) -> FieldCandidate:
    value = _calendar_selected_value(selected)
    return FieldCandidate(
        candidate_id=f"m02:{projection.projection_id}:{selected.semantic_key}",
        source_owner="M02",
        semantic_field=selected.semantic_key,
        candidate_state="unavailable" if value is None else "value",
        value=value,
        value_type=selected.value_type,
        unit=selected.unit,
        source_artifact_id=projection.projection_id,
        capture_id=projection.snapshot_id,
        contract_version=projection.projection_policy_version,
        schema_version=projection.snapshot_version,
        effective_at_utc=projection.effective_from_utc,
        effective_to_utc=projection.effective_to_utc,
        input_fingerprint=projection.semantic_fingerprint,
        validation_state=(
            ("valid" if projection.status == "projected" else "degraded")
            if selected.value is not None
            else "unavailable"
        ),
        limitations=projection.degraded_facts,
    )


def _derive_value(rule: PreparedDerivationRule, values: tuple[Any, ...]) -> Any:
    if rule.operation == "percentage_return":
        if len(values) != 2:
            raise ValueError("percentage_return_requires_two_inputs")
        current, prior = values
        if not isinstance(current, (int, float)) or isinstance(current, bool):
            raise ValueError("derivation_input_type_mismatch")
        if not isinstance(prior, (int, float)) or isinstance(prior, bool) or prior == 0:
            raise ValueError("derivation_input_type_mismatch")
        return float(current) / float(prior) - 1.0
    if rule.operation == "difference":
        if len(values) != 2 or any(
            not isinstance(item, (int, float)) or isinstance(item, bool) for item in values
        ):
            raise ValueError("difference_requires_two_numeric_inputs")
        return values[0] - values[1]
    if rule.operation == "minutes_between":
        if len(values) != 2 or any(not isinstance(item, datetime) for item in values):
            raise ValueError("minutes_between_requires_two_datetimes")
        return int((values[1] - values[0]).total_seconds() // 60)
    raise ValueError("unsupported_prepared_derivation_operation")


class PreparedDataBuilder:
    """Build one prepared envelope only from exact M01/M02 owner evidence."""

    def build(
        self,
        *,
        source_artifacts: tuple[SourceArtifactEnvelope, ...],
        field_resolution_policies: tuple[FieldResolutionPolicy, ...],
        calendar_projections: tuple[CalendarProjection, ...] = (),
        derivation_rules: tuple[PreparedDerivationRule, ...] = (),
        schema_version: str,
        preparation_policy_version: str,
        alignment_policy_version: str,
        fingerprint_policy_version: str,
        canonicalisation_version: str,
        effective_at_utc: datetime,
        payload_schema_version: str,
        missing_optional_enrichments: tuple[str, ...] = (),
        parent_prepared_ids: tuple[str, ...] = (),
    ) -> PreparedDataEnvelope:
        """Resolve, derive and construct one canonical prepared authority object."""

        if not source_artifacts:
            raise ValueError("source_artifacts_required")
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
        if effective_at_utc.tzinfo is None or effective_at_utc.utcoffset() is None:
            raise ValueError("effective_at_utc_must_be_timezone_aware")

        artifacts = tuple(
            sorted(
                (_revalidate_source_artifact(item) for item in source_artifacts),
                key=lambda item: item.source_artifact_id,
            )
        )
        artifact_ids = {item.source_artifact_id for item in artifacts}
        if len(artifact_ids) != len(artifacts):
            raise ValueError("duplicate_source_artifact_identity")
        projections = tuple(
            sorted(
                (_revalidate_projection(item) for item in calendar_projections),
                key=lambda item: item.projection_id,
            )
        )
        if any(item.status not in {"projected", "degraded"} for item in projections):
            raise ValueError("unusable_calendar_projection")

        source_refs = tuple(
            SourceCaptureReference(
                capture_id=item.capture_receipt.capture_id,
                source_artifact_id=item.source_artifact_id,
                family_id=item.family_id,
                contract_id=item.contract_id,
                schema_version=item.schema_version,
                source_owner=item.source_identifier.owner or item.provider_id,
                effective_at_utc=item.observed_at_utc or effective_at_utc,
                source_time_utc=item.observed_at_utc,
                source_date=item.source_date,
                temporal_precision=item.source_time_precision.value,
                input_fingerprint=item.content_sha256,
                validation_state=("valid" if item.validation_status == "admitted" else "degraded"),
                limitations=item.limitations,
                semantic_fields=tuple(
                    sorted(binding.semantic_field for binding in item.semantic_bindings)
                ),
                provider_id=item.provider_id,
                acquisition_method=item.acquisition_channel,
            )
            for item in artifacts
        )

        projection_refs: list[CalendarProjectionReference] = []
        for projection in projections:
            source_refs_for_projection = tuple(
                sorted(
                    {
                        source_ref
                        for selected in projection.selected_fields
                        for source_ref in selected.source_refs
                    }
                )
            )
            foreign = tuple(
                source_id
                for source_id, _ in source_refs_for_projection
                if source_id not in artifact_ids
            )
            if foreign:
                raise ValueError(
                    "calendar_projection_source_lineage_not_admitted:" + ",".join(foreign)
                )
            projection_refs.append(
                CalendarProjectionReference(
                    projection_id=projection.projection_id,
                    snapshot_id=projection.snapshot_id,
                    snapshot_version=projection.snapshot_version,
                    projection_policy_version=projection.projection_policy_version,
                    status=projection.status,
                    semantic_fingerprint=projection.semantic_fingerprint,
                    source_refs=source_refs_for_projection,
                )
            )

        candidates_by_field: dict[str, list[FieldCandidate]] = {}
        for artifact in artifacts:
            for binding in artifact.semantic_bindings:
                candidate = _source_candidate(
                    artifact,
                    binding,
                    effective_at_utc=effective_at_utc,
                )
                candidates_by_field.setdefault(binding.semantic_field, []).append(candidate)
        for projection in projections:
            for selected in projection.selected_fields:
                if selected.semantic_key not in PreparedRuntimePayloadV1.model_fields:
                    continue
                candidate = _calendar_candidate(projection, selected)
                candidates_by_field.setdefault(selected.semantic_key, []).append(candidate)

        policies = tuple(
            sorted(
                (
                    FieldResolutionPolicy.model_validate(item.model_dump(mode="python"))
                    for item in field_resolution_policies
                ),
                key=lambda item: item.semantic_field,
            )
        )
        if len({item.semantic_field for item in policies}) != len(policies):
            raise ValueError("duplicate_prepared_field_resolution_policy")
        derivations = tuple(
            sorted(
                (
                    PreparedDerivationRule.model_validate(item.model_dump(mode="python"))
                    for item in derivation_rules
                ),
                key=lambda item: item.semantic_field,
            )
        )
        if len({item.semantic_field for item in derivations}) != len(derivations):
            raise ValueError("duplicate_prepared_derivation_rule")
        direct_fields = {item.semantic_field for item in policies}
        derived_fields = {item.semantic_field for item in derivations}
        if direct_fields & derived_fields:
            raise ValueError("prepared_field_cannot_be_direct_and_derived")
        payload_fields = set(PreparedRuntimePayloadV1.model_fields) - {"kind"}
        if any(item not in payload_fields for item in direct_fields | derived_fields):
            raise ValueError("prepared_policy_field_not_in_payload_contract")
        bound_fields = {
            binding.semantic_field
            for artifact in artifacts
            for binding in artifact.semantic_bindings
        }
        if not bound_fields <= direct_fields:
            raise ValueError("m01_semantic_binding_not_consumed_by_m03_policy")

        payload_values: dict[str, Any] = {}
        resolution_receipts: list[FieldResolutionReceipt] = []
        receipts_by_field: dict[str, FieldResolutionReceipt] = {}
        for policy in policies:
            receipt = resolve_canonical_field(
                candidates=tuple(candidates_by_field.get(policy.semantic_field, ())),
                policy=policy,
            )
            resolution_receipts.append(receipt)
            receipts_by_field[policy.semantic_field] = receipt
            if receipt.resolution_status in {"selected", "degraded"}:
                payload_values[policy.semantic_field] = receipt.selected_value

        derivation_receipts: list[DerivationReceipt] = []
        for rule in derivations:
            input_values: list[Any] = []
            input_candidate_ids: list[str] = []
            input_fingerprints: list[str] = []
            for semantic_field in rule.input_semantic_fields:
                receipt = receipts_by_field.get(semantic_field)
                if receipt is None or receipt.selected_candidate_id is None:
                    if rule.mandatory:
                        raise ValueError(f"missing_mandatory_derivation_input:{semantic_field}")
                    input_values = []
                    break
                selected = next(
                    (
                        item
                        for item in receipt.candidate_records
                        if item.candidate_id == receipt.selected_candidate_id
                    ),
                    None,
                )
                if selected is None:
                    raise ValueError("derivation_selected_candidate_missing")
                input_values.append(receipt.selected_value)
                input_candidate_ids.append(selected.candidate_id)
                input_fingerprints.append(selected.input_fingerprint)
            if not input_values:
                continue
            derived_value = _derive_value(rule, tuple(input_values))
            material = {
                "semantic_field": rule.semantic_field,
                "derivation_version": rule.derivation_version,
                "input_semantic_fields": rule.input_semantic_fields,
                "input_candidate_ids": tuple(input_candidate_ids),
                "input_fingerprints": tuple(input_fingerprints),
                "operation": rule.operation,
                "unit_alignment_policy": rule.unit_alignment_policy,
                "temporal_alignment_policy": rule.temporal_alignment_policy,
                "result_state": "derived",
                "value": derived_value,
            }
            derivation_id = f"derivation:{semantic_fingerprint(material)[:24]}"
            receipt = DerivationReceipt(derivation_id=derivation_id, **material)
            derivation_receipts.append(receipt)
            payload_values[rule.semantic_field] = derived_value

        governed_payload = PreparedRuntimePayloadV1.model_validate(payload_values)
        schema_versions = tuple(
            sorted(
                [(f"m01:{item.source_artifact_id}", item.schema_version) for item in artifacts]
                + [(f"m02:{item.projection_id}", item.snapshot_version) for item in projections]
            )
        )
        declared_derivations = tuple(
            (item.semantic_field, item.derivation_version) for item in derivations
        )
        owner_limitations = tuple(
            sorted(
                {limitation for item in source_refs for limitation in item.limitations}
                | {
                    limitation
                    for projection in projections
                    for limitation in projection.degraded_facts
                }
            )
        )
        optional_gaps = tuple(
            sorted(
                set(missing_optional_enrichments)
                | {
                    receipt.semantic_field
                    for receipt in resolution_receipts
                    if receipt.resolution_status in {"unavailable", "withheld"}
                }
            )
        )
        degraded = (
            bool(owner_limitations or optional_gaps)
            or any(item.validation_state == "degraded" for item in source_refs)
            or any(item.status == "degraded" for item in projection_refs)
        )
        validation_state = "degraded" if degraded else "valid"
        completeness_state = "degraded" if degraded else "complete"

        input_fingerprint = prepared_input_fingerprint(
            source_refs,
            schema_versions,
            calendar_projection_refs=tuple(projection_refs),
            fingerprint_policy_version=fingerprint_policy_version,
            canonicalisation_version=canonicalisation_version,
        )
        prepared_fingerprint = prepared_envelope_fingerprint(
            schema_version=schema_version,
            source_capture_refs=source_refs,
            calendar_projection_refs=tuple(projection_refs),
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
            limitations=owner_limitations,
            failed_mandatory_transformations=(),
            missing_optional_enrichments=optional_gaps,
            parent_prepared_ids=parent_prepared_ids,
            payload_kind=governed_payload.kind,
            payload_schema_version=payload_schema_version,
            payload=governed_payload,
            field_resolution_receipts=tuple(resolution_receipts),
            derivation_receipts=tuple(derivation_receipts),
        )
        return PreparedDataEnvelope(
            prepared_id=f"prepared:{prepared_fingerprint[:24]}",
            schema_version=schema_version,
            source_capture_refs=source_refs,
            calendar_projection_refs=tuple(projection_refs),
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
            limitations=owner_limitations,
            failed_mandatory_transformations=(),
            missing_optional_enrichments=optional_gaps,
            parent_prepared_ids=parent_prepared_ids,
            payload_kind=governed_payload.kind,
            payload_schema_version=payload_schema_version,
            payload=governed_payload,
            field_resolution_receipts=tuple(resolution_receipts),
            derivation_receipts=tuple(derivation_receipts),
            closed_authority_classes=CLOSED_PREPARATION_AUTHORITIES,
            foreign_authority_claimed=False,
        )
