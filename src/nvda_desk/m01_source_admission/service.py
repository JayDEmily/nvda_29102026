"""M01 source-admission service with fail-closed identity and temporal law."""

from __future__ import annotations

import json
from collections.abc import Mapping
from datetime import UTC, datetime
from hashlib import sha256
from typing import Any

from pydantic import BaseModel, ValidationError

from .contracts import (
    CaptureIdFactory,
    CaptureReceipt,
    RawSignalBatch,
    SourceAdmissionAccepted,
    SourceAdmissionRequest,
    SourceAdmissionResult,
    SourceArtifactEnvelope,
    SourceArtifactIdFactory,
    SourceFactRequirement,
    SourceFamilyContract,
    SourceFamilyRegistry,
    SourceNonAdmission,
    SourceOutputContract,
    SourceTimeKind,
)

_FORBIDDEN_AUTHORITY_KEYS = frozenset(
    {
        "account_id",
        "api_key",
        "auth_header",
        "authorised_deployable_pct",
        "authorised_notional_usd",
        "bearer_token",
        "brokerage_order",
        "credential",
        "execution_receipt",
        "order_qty",
        "password",
        "persistence_write_path",
        "position_size",
        "private_key",
        "secret",
        "token",
        "trade_allowed",
    }
)


def _aware(value: datetime) -> bool:
    return value.tzinfo is not None and value.utcoffset() is not None


def _utc(value: datetime) -> bool:
    return _aware(value) and value.utcoffset() == UTC.utcoffset(value)


def _find_forbidden_keys(value: Any) -> tuple[str, ...]:
    found: set[str] = set()

    def visit(candidate: Any) -> None:
        if isinstance(candidate, Mapping):
            for key, nested in candidate.items():
                if isinstance(key, str) and key in _FORBIDDEN_AUTHORITY_KEYS:
                    found.add(key)
                visit(nested)
        elif isinstance(candidate, (list, tuple, set, frozenset)):
            for nested in candidate:
                visit(nested)

    visit(value)
    return tuple(sorted(found))


def _validate_source_identifier(
    contract: SourceFamilyContract,
    request: SourceAdmissionRequest,
) -> str | None:
    requirement = contract.source_identifier.requirement
    source_object_id = request.source_object_id
    if requirement is SourceFactRequirement.REQUIRED and not source_object_id:
        return "missing_required_source_identifier"
    if (
        requirement
        in {
            SourceFactRequirement.UNAVAILABLE_BY_SOURCE_DESIGN,
            SourceFactRequirement.NOT_APPLICABLE,
        }
        and source_object_id is not None
    ):
        return "source_identifier_not_applicable"
    return None


def _validate_provider_contract(
    contract: SourceFamilyContract,
    request: SourceAdmissionRequest,
) -> str | None:
    for provider in contract.providers:
        if provider.provider_id != request.provider_id:
            continue
        if request.acquisition_channel not in provider.acquisition_channels:
            return "unsupported_provider_acquisition_channel"
        return None
    return "unsupported_source_provider"


def _validate_source_time(
    contract: SourceFamilyContract,
    request: SourceAdmissionRequest,
) -> str | None:
    if contract.source_time_kind is SourceTimeKind.INSTANT:
        if request.observed_at_utc is None or request.source_date is not None:
            return "missing_or_contradictory_source_time"
        if not _utc(request.observed_at_utc):
            return "source_time_must_be_utc"
    elif contract.source_time_kind is SourceTimeKind.DATE:
        if request.source_date is None or request.observed_at_utc is not None:
            return "missing_or_contradictory_source_date"
    return None


def _captured_material_matches_payload(
    captured_material: bytes,
    typed_payload: BaseModel,
) -> bool:
    try:
        decoded = json.loads(captured_material.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return False
    return decoded == typed_payload.model_dump(mode="json")


class SourceAdmissionService:
    """Admit one offline source artefact under an exact registered contract."""

    def __init__(
        self,
        *,
        registry: SourceFamilyRegistry,
        capture_id_factory: CaptureIdFactory,
        source_artifact_id_factory: SourceArtifactIdFactory,
    ) -> None:
        self._registry = registry
        self._capture_id_factory = capture_id_factory
        self._source_artifact_id_factory = source_artifact_id_factory

    def admit(self, request: SourceAdmissionRequest) -> SourceAdmissionResult:
        fingerprint = sha256(request.captured_material).hexdigest()
        contract = self._registry.resolve(
            family_id=request.family_id,
            contract_id=request.contract_id,
            schema_version=request.schema_version,
        )
        if contract is None:
            return SourceNonAdmission(
                reason="unsupported_family_contract_or_version",
                content_sha256=fingerprint,
            )
        try:
            typed_payload = contract.payload_model.model_validate(request.typed_payload)
        except (ValidationError, TypeError, ValueError):
            return SourceNonAdmission(
                reason="typed_payload_contract_mismatch",
                content_sha256=fingerprint,
            )
        provider_error = _validate_provider_contract(contract, request)
        if provider_error is not None:
            return SourceNonAdmission(reason=provider_error, content_sha256=fingerprint)
        identifier_error = _validate_source_identifier(contract, request)
        if identifier_error is not None:
            return SourceNonAdmission(reason=identifier_error, content_sha256=fingerprint)
        time_error = _validate_source_time(contract, request)
        if time_error is not None:
            return SourceNonAdmission(reason=time_error, content_sha256=fingerprint)
        if not _utc(request.captured_at_utc):
            return SourceNonAdmission(
                reason="capture_time_must_be_utc",
                content_sha256=fingerprint,
            )
        if not _captured_material_matches_payload(
            request.captured_material,
            typed_payload,
        ):
            return SourceNonAdmission(
                reason="captured_material_typed_payload_mismatch",
                content_sha256=fingerprint,
            )
        forbidden = _find_forbidden_keys(typed_payload.model_dump(mode="python"))
        if forbidden:
            return SourceNonAdmission(
                reason="forbidden_source_payload_authority:" + ",".join(forbidden),
                content_sha256=fingerprint,
            )
        unsupported_limitations = set(request.declared_limitations).difference(
            contract.permitted_limitations
        )
        if unsupported_limitations:
            return SourceNonAdmission(
                reason="unsupported_source_limitation:" + ",".join(sorted(unsupported_limitations)),
                content_sha256=fingerprint,
            )

        capture_id = self._capture_id_factory(fingerprint)
        if (
            not isinstance(capture_id, str)
            or not capture_id
            or capture_id.strip() != capture_id
            or any(character.isspace() for character in capture_id)
            or capture_id in {request.source_object_id, fingerprint}
        ):
            return SourceNonAdmission(
                reason="invalid_repository_capture_identity",
                content_sha256=fingerprint,
            )

        source_artifact_id = self._source_artifact_id_factory(
            contract.family_id,
            contract.contract_id,
            request.source_object_id,
            fingerprint,
        )
        if (
            not isinstance(source_artifact_id, str)
            or not source_artifact_id
            or source_artifact_id.strip() != source_artifact_id
            or any(character.isspace() for character in source_artifact_id)
            or source_artifact_id in {request.source_object_id, capture_id, fingerprint}
        ):
            return SourceNonAdmission(
                reason="invalid_repository_source_artifact_identity",
                content_sha256=fingerprint,
            )

        receipt = CaptureReceipt(
            capture_id=capture_id,
            content_sha256=fingerprint,
            captured_at_utc=request.captured_at_utc,
        )
        validation_status = "degraded" if request.declared_limitations else "admitted"
        payload_copy = typed_payload.model_copy(deep=True)
        envelope = SourceArtifactEnvelope(
            source_artifact_id=source_artifact_id,
            family_id=contract.family_id,
            contract_id=contract.contract_id,
            schema_version=contract.schema_version,
            provider_id=request.provider_id,
            acquisition_channel=request.acquisition_channel,
            source_identifier=contract.source_identifier,
            source_object_id=request.source_object_id,
            observed_at_utc=request.observed_at_utc,
            source_date=request.source_date,
            source_time_raw=request.source_time_raw,
            source_timezone_raw=request.source_timezone_raw,
            source_time_precision=contract.source_time_kind,
            capture_receipt=receipt,
            captured_material=bytes(request.captured_material),
            content_sha256=fingerprint,
            validation_status=validation_status,
            validation_results=(
                "family_contract",
                "typed_payload",
                "source_identity",
                "source_time",
                "captured_material",
                "authority_boundary",
                "capture_identity",
            ),
            limitations=request.declared_limitations,
            downstream_owner=contract.downstream_owner,
            typed_payload=payload_copy,
        )

        batch = None
        if contract.output_contract is SourceOutputContract.RAW_SIGNAL_BATCH:
            batch = RawSignalBatch(
                signal_family_id=contract.signal_family_id or "",
                source_object_id=request.source_object_id,
                capture_id=capture_id,
                source_artifact_id=source_artifact_id,
                contract_id=contract.contract_id,
                schema_version=contract.schema_version,
                provider_id=request.provider_id,
                acquisition_channel=request.acquisition_channel,
                source_identifier=contract.source_identifier,
                observed_at_utc=request.observed_at_utc,
                source_date=request.source_date,
                payload=payload_copy.model_copy(deep=True),
            )
        return SourceAdmissionAccepted(source_artifact=envelope, raw_signal_batch=batch)
