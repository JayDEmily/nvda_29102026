"""Minimum truthful public-seam proof for M01 source admission."""

from __future__ import annotations

from dataclasses import replace
from datetime import UTC, date, datetime, timedelta, timezone

import pytest
from pydantic import BaseModel, ConfigDict, Field
from tests.support.m01_source_admission_contract_harness import (
    MUTANTS,
    AcceptedAdmission,
    ReferenceSubject,
    RejectedAdmission,
    capture_id_factory,
    production_api,
    valid_case,
)


class MarketSnapshotPayload(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    symbol: str = Field(min_length=1)
    value: float


class NestedAuthorityPayload(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    symbol: str = Field(min_length=1)
    metadata: dict[str, object]


def test_reference_subject_admits_complete_source_and_capture_facts() -> None:
    case = valid_case()
    result = ReferenceSubject().admit(case, capture_id_factory=capture_id_factory)

    assert isinstance(result, AcceptedAdmission)
    assert result.source_object_id == "provider-observation-17"
    assert result.capture_id == "capture::m01::0001"
    assert result.capture_id != result.source_object_id
    assert result.content_sha256 != result.capture_id
    assert result.observed_at_utc == case.observed_at_utc
    assert result.time_precision == "instant"
    assert result.downstream_owner == "M03"


def test_reference_subject_preserves_date_only_source_truth() -> None:
    case = valid_case(source_time_kind="date")
    result = ReferenceSubject().admit(case, capture_id_factory=capture_id_factory)

    assert isinstance(result, AcceptedAdmission)
    assert result.source_date == date(2026, 7, 31)
    assert result.observed_at_utc is None
    assert result.time_precision == "date"


def test_reference_subject_fails_closed_when_required_source_identity_is_absent() -> None:
    result = ReferenceSubject().admit(
        replace(valid_case(), source_object_id=None),
        capture_id_factory=capture_id_factory,
    )

    assert result == RejectedAdmission("missing_required_source_identifier")


def test_reference_subject_rejects_unsupported_contract_instead_of_shape_guessing() -> None:
    result = ReferenceSubject().admit(
        replace(valid_case(), family_id="unknown_family"),
        capture_id_factory=capture_id_factory,
    )

    assert result == RejectedAdmission("unsupported_family_contract_or_version")


@pytest.mark.parametrize("mutant_name", tuple(MUTANTS))
def test_each_false_positive_mutant_is_killed(mutant_name: str) -> None:
    case = valid_case()
    if mutant_name == "capture_identity_as_source":
        case = replace(case, source_object_id=None)
        expected_reason = "missing_required_source_identifier"
    elif mutant_name == "shape_guess":
        case = replace(case, family_id="unknown_family")
        expected_reason = "unsupported_family_contract_or_version"
    elif mutant_name == "provider_substitution":
        case = replace(case, provider_id="unregistered-provider")
        expected_reason = "unsupported_source_provider"
    elif mutant_name == "capture_time_as_source_time":
        case = replace(case, observed_at_utc=None)
        expected_reason = "missing_or_contradictory_source_time"
    else:
        expected_reason = "invalid_repository_capture_identity"

    factory = (
        (lambda fingerprint: fingerprint)
        if mutant_name == "hash_as_capture_identity"
        else capture_id_factory
    )
    reference = ReferenceSubject().admit(case, capture_id_factory=factory)
    mutant = MUTANTS[mutant_name]().admit(case, capture_id_factory=factory)

    assert reference == RejectedAdmission(expected_reason)
    assert mutant != reference


def _production_fixture():
    api = production_api()
    source_identifier = api["SourceIdentifierContract"](
        requirement=api["SourceFactRequirement"].REQUIRED,
        owner="recorded-provider",
        namespace="recorded-provider/market-observation",
        uniqueness_scope="recorded-provider/market-observation",
        stability_rule="stable_for_source_object_lifetime",
        generation_rule="issued_by_upstream_provider",
    )
    contract = api["SourceFamilyContract"](
        family_id="market_snapshot",
        contract_id="market_snapshot.v1",
        schema_version="1.0.0",
        payload_model=MarketSnapshotPayload,
        providers=(
            api["SourceProviderContract"](
                provider_id="recorded-provider",
                acquisition_channels=("recorded_api_response",),
            ),
        ),
        source_identifier=source_identifier,
        source_time_kind=api["SourceTimeKind"].INSTANT,
        downstream_owner=api["SourceDownstreamOwner"].M03,
        output_contract=api["SourceOutputContract"].RAW_SIGNAL_BATCH,
        signal_family_id="market_snapshot",
    )
    registry = api["SourceFamilyRegistry"].build([contract])
    service = api["SourceAdmissionService"](
        registry=registry,
        capture_id_factory=lambda _: "capture::m01::0001",
    )
    request = api["SourceAdmissionRequest"](
        family_id="market_snapshot",
        contract_id="market_snapshot.v1",
        schema_version="1.0.0",
        provider_id="recorded-provider",
        acquisition_channel="recorded_api_response",
        source_object_id="provider-observation-17",
        observed_at_utc=datetime(2026, 7, 31, 1, 15, tzinfo=UTC),
        captured_at_utc=datetime(2026, 7, 31, 1, 16, tzinfo=UTC),
        captured_material=b'{"symbol":"NVDA","value":121.5}',
        typed_payload=MarketSnapshotPayload(symbol="NVDA", value=121.5),
    )
    return api, service, request


def test_production_public_seam_admits_complete_source_artifact() -> None:
    api, service, request = _production_fixture()
    result = service.admit(request)

    assert isinstance(result, api["SourceAdmissionAccepted"])
    envelope = result.source_artifact
    assert envelope.source_object_id == "provider-observation-17"
    assert envelope.capture_receipt.capture_id == "capture::m01::0001"
    assert envelope.capture_receipt.capture_id != envelope.source_object_id
    assert envelope.capture_receipt.durability_status == "volatile_alpha"
    assert envelope.source_identifier.owner == "recorded-provider"
    assert envelope.source_identifier.namespace == "recorded-provider/market-observation"
    assert envelope.source_time_precision == "instant"
    assert envelope.validation_status == "admitted"
    assert result.raw_signal_batch is not None
    assert result.raw_signal_batch.capture_id == envelope.capture_receipt.capture_id
    assert result.raw_signal_batch.source_object_id == envelope.source_object_id
    assert result.raw_signal_batch.provider_id == "recorded-provider"
    assert result.raw_signal_batch.source_identifier == envelope.source_identifier


def test_production_public_seam_rejects_missing_required_source_identity() -> None:
    api, service, request = _production_fixture()
    result = service.admit(request.model_copy(update={"source_object_id": None}))

    assert isinstance(result, api["SourceNonAdmission"])
    assert result.reason == "missing_required_source_identifier"
    assert result.capture_receipt is None


def test_production_public_seam_rejects_unsupported_family_without_shape_guessing() -> None:
    api, service, request = _production_fixture()
    result = service.admit(request.model_copy(update={"family_id": "unknown_family"}))

    assert isinstance(result, api["SourceNonAdmission"])
    assert result.reason == "unsupported_family_contract_or_version"


def test_production_public_seam_rejects_unregistered_provider_substitution() -> None:
    api, service, request = _production_fixture()
    result = service.admit(request.model_copy(update={"provider_id": "unregistered-provider"}))

    assert isinstance(result, api["SourceNonAdmission"])
    assert result.reason == "unsupported_source_provider"


def test_production_public_seam_rejects_unregistered_provider_channel() -> None:
    api, service, request = _production_fixture()
    result = service.admit(request.model_copy(update={"acquisition_channel": "live_api"}))

    assert isinstance(result, api["SourceNonAdmission"])
    assert result.reason == "unsupported_provider_acquisition_channel"


def test_production_public_seam_requires_utc_source_and_capture_instants() -> None:
    api, service, request = _production_fixture()
    non_utc = timezone(timedelta(hours=10))

    source_result = service.admit(
        request.model_copy(update={"observed_at_utc": request.observed_at_utc.astimezone(non_utc)})
    )
    capture_result = service.admit(
        request.model_copy(update={"captured_at_utc": request.captured_at_utc.astimezone(non_utc)})
    )

    assert isinstance(source_result, api["SourceNonAdmission"])
    assert source_result.reason == "source_time_must_be_utc"
    assert isinstance(capture_result, api["SourceNonAdmission"])
    assert capture_result.reason == "capture_time_must_be_utc"


def test_production_public_seam_preserves_date_only_truth_without_fabricated_instant() -> None:
    api = production_api()
    contract = api["SourceFamilyContract"](
        family_id="calendar_reference",
        contract_id="calendar_reference.v1",
        schema_version="1.0.0",
        payload_model=MarketSnapshotPayload,
        providers=(
            api["SourceProviderContract"](
                provider_id="checked-reference",
                acquisition_channels=("checked_in_reference",),
            ),
        ),
        source_identifier=api["SourceIdentifierContract"](
            requirement=api["SourceFactRequirement"].REQUIRED,
            owner="checked-reference",
            namespace="checked-reference/calendar-bundle",
            uniqueness_scope="checked-reference/calendar-bundle",
            stability_rule="stable_for_reference_bundle_lifetime",
            generation_rule="issued_by_reference_source",
        ),
        source_time_kind=api["SourceTimeKind"].DATE,
        downstream_owner=api["SourceDownstreamOwner"].M02,
        output_contract=api["SourceOutputContract"].SOURCE_ARTIFACT,
    )
    service = api["SourceAdmissionService"](
        registry=api["SourceFamilyRegistry"].build([contract]),
        capture_id_factory=lambda _: "capture::m01::calendar-1",
    )
    request = api["SourceAdmissionRequest"](
        family_id="calendar_reference",
        contract_id="calendar_reference.v1",
        schema_version="1.0.0",
        provider_id="checked-reference",
        acquisition_channel="checked_in_reference",
        source_object_id="calendar-bundle-1",
        source_date=date(2026, 7, 31),
        captured_at_utc=datetime(2026, 7, 31, 1, 16, tzinfo=UTC),
        captured_material=b'{"symbol":"NVDA","value":0.0}',
        typed_payload=MarketSnapshotPayload(symbol="NVDA", value=0.0),
    )

    result = service.admit(request)

    assert isinstance(result, api["SourceAdmissionAccepted"])
    assert result.source_artifact.source_date == date(2026, 7, 31)
    assert result.source_artifact.observed_at_utc is None
    assert result.source_artifact.source_time_precision == "date"
    assert result.raw_signal_batch is None


def test_production_public_seam_rejects_hash_as_repository_capture_identity() -> None:
    api, _, request = _production_fixture()
    from hashlib import sha256

    service = api["SourceAdmissionService"](
        registry=api["SourceFamilyRegistry"].build(
            [
                api["SourceFamilyContract"](
                    family_id="market_snapshot",
                    contract_id="market_snapshot.v1",
                    schema_version="1.0.0",
                    payload_model=MarketSnapshotPayload,
                    providers=(
                        api["SourceProviderContract"](
                            provider_id="recorded-provider",
                            acquisition_channels=("recorded_api_response",),
                        ),
                    ),
                    source_identifier=api["SourceIdentifierContract"](
                        requirement=api["SourceFactRequirement"].REQUIRED,
                        owner="recorded-provider",
                        namespace="recorded-provider/market-observation",
                        uniqueness_scope="recorded-provider/market-observation",
                        stability_rule="stable_for_source_object_lifetime",
                        generation_rule="issued_by_upstream_provider",
                    ),
                    source_time_kind=api["SourceTimeKind"].INSTANT,
                    downstream_owner=api["SourceDownstreamOwner"].M03,
                    output_contract=api["SourceOutputContract"].RAW_SIGNAL_BATCH,
                    signal_family_id="market_snapshot",
                )
            ]
        ),
        capture_id_factory=lambda fingerprint: fingerprint,
    )
    result = service.admit(request)

    assert isinstance(result, api["SourceNonAdmission"])
    assert result.reason == "invalid_repository_capture_identity"
    assert result.content_sha256 == sha256(request.captured_material).hexdigest()


def test_production_public_seam_rejects_nested_credential_authority() -> None:
    api = production_api()
    contract = api["SourceFamilyContract"](
        family_id="market_snapshot",
        contract_id="market_snapshot.v1",
        schema_version="1.0.0",
        payload_model=NestedAuthorityPayload,
        providers=(
            api["SourceProviderContract"](
                provider_id="recorded-provider",
                acquisition_channels=("recorded_api_response",),
            ),
        ),
        source_identifier=api["SourceIdentifierContract"](
            requirement=api["SourceFactRequirement"].REQUIRED,
            owner="recorded-provider",
            namespace="recorded-provider/market-observation",
            uniqueness_scope="recorded-provider/market-observation",
            stability_rule="stable_for_source_object_lifetime",
            generation_rule="issued_by_upstream_provider",
        ),
        source_time_kind=api["SourceTimeKind"].INSTANT,
        downstream_owner=api["SourceDownstreamOwner"].M03,
        output_contract=api["SourceOutputContract"].RAW_SIGNAL_BATCH,
        signal_family_id="market_snapshot",
    )
    service = api["SourceAdmissionService"](
        registry=api["SourceFamilyRegistry"].build([contract]),
        capture_id_factory=lambda _: "capture::m01::0001",
    )
    request = api["SourceAdmissionRequest"](
        family_id="market_snapshot",
        contract_id="market_snapshot.v1",
        schema_version="1.0.0",
        provider_id="recorded-provider",
        acquisition_channel="recorded_api_response",
        source_object_id="provider-observation-17",
        observed_at_utc=datetime(2026, 7, 31, 1, 15, tzinfo=UTC),
        captured_at_utc=datetime(2026, 7, 31, 1, 16, tzinfo=UTC),
        captured_material=(b'{"symbol":"NVDA","metadata":{"credential":"must-not-cross"}}'),
        typed_payload=NestedAuthorityPayload(
            symbol="NVDA",
            metadata={"credential": "must-not-cross"},
        ),
    )

    result = service.admit(request)

    assert isinstance(result, api["SourceNonAdmission"])
    assert result.reason == "forbidden_source_payload_authority:credential"
