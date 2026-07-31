"""Reference and false-positive subjects for the bounded M01 admission contract."""

from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import date, datetime
from hashlib import sha256
from typing import Any, Callable

from pydantic import BaseModel, ConfigDict, Field


class FixtureSignalPayload(BaseModel):
    """Typed fixture payload used only by the M01 public-seam proof."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    symbol: str = Field(min_length=1)
    value: float


@dataclass(frozen=True)
class FamilyContract:
    family_id: str = "market_snapshot"
    contract_id: str = "market_snapshot.v1"
    schema_version: str = "1.0.0"
    source_identifier_required: bool = True
    source_time_kind: str = "instant"
    downstream_owner: str = "M03"
    provider_id: str = "recorded-provider"
    acquisition_channels: tuple[str, ...] = ("recorded_api_response",)


@dataclass(frozen=True)
class AdmissionCase:
    contract: FamilyContract
    provider_id: str
    acquisition_channel: str
    source_object_id: str | None
    observed_at_utc: datetime | None
    source_date: date | None
    captured_at_utc: datetime
    captured_material: bytes
    typed_payload: BaseModel
    family_id: str
    contract_id: str
    schema_version: str


@dataclass(frozen=True)
class AcceptedAdmission:
    source_object_id: str | None
    capture_id: str
    content_sha256: str
    observed_at_utc: datetime | None
    source_date: date | None
    time_precision: str
    downstream_owner: str
    typed_payload: BaseModel


@dataclass(frozen=True)
class RejectedAdmission:
    reason: str


class ReferenceSubject:
    """Small reference subject implementing only the admitted proof proposition."""

    def admit(
        self,
        case: AdmissionCase,
        *,
        capture_id_factory: Callable[[str], str],
    ) -> AcceptedAdmission | RejectedAdmission:
        contract = case.contract
        if (
            case.family_id != contract.family_id
            or case.contract_id != contract.contract_id
            or case.schema_version != contract.schema_version
        ):
            return RejectedAdmission("unsupported_family_contract_or_version")
        if not isinstance(case.typed_payload, FixtureSignalPayload):
            return RejectedAdmission("typed_payload_contract_mismatch")
        if case.provider_id != contract.provider_id:
            return RejectedAdmission("unsupported_source_provider")
        if case.acquisition_channel not in contract.acquisition_channels:
            return RejectedAdmission("unsupported_provider_acquisition_channel")
        if contract.source_identifier_required and not case.source_object_id:
            return RejectedAdmission("missing_required_source_identifier")
        if contract.source_time_kind == "instant":
            if case.observed_at_utc is None or case.source_date is not None:
                return RejectedAdmission("missing_or_contradictory_source_time")
            if case.observed_at_utc.tzinfo is None:
                return RejectedAdmission("source_time_must_be_timezone_aware")
            precision = "instant"
        elif contract.source_time_kind == "date":
            if case.source_date is None or case.observed_at_utc is not None:
                return RejectedAdmission("missing_or_contradictory_source_date")
            precision = "date"
        else:
            return RejectedAdmission("unsupported_source_time_kind")
        if case.captured_at_utc.tzinfo is None:
            return RejectedAdmission("capture_time_must_be_timezone_aware")
        fingerprint = sha256(case.captured_material).hexdigest()
        capture_id = capture_id_factory(fingerprint)
        if not capture_id or capture_id in {case.source_object_id, fingerprint}:
            return RejectedAdmission("invalid_repository_capture_identity")
        return AcceptedAdmission(
            source_object_id=case.source_object_id,
            capture_id=capture_id,
            content_sha256=fingerprint,
            observed_at_utc=case.observed_at_utc,
            source_date=case.source_date,
            time_precision=precision,
            downstream_owner=contract.downstream_owner,
            typed_payload=case.typed_payload,
        )


class CaptureIdentityAsSourceMutant(ReferenceSubject):
    def admit(self, case: AdmissionCase, *, capture_id_factory: Callable[[str], str]):
        fingerprint = sha256(case.captured_material).hexdigest()
        capture_id = capture_id_factory(fingerprint)
        return super().admit(
            replace(case, source_object_id=case.source_object_id or capture_id),
            capture_id_factory=capture_id_factory,
        )


class ShapeGuessMutant(ReferenceSubject):
    def admit(self, case: AdmissionCase, *, capture_id_factory: Callable[[str], str]):
        if isinstance(case.typed_payload, BaseModel):
            case = replace(
                case,
                family_id=case.contract.family_id,
                contract_id=case.contract.contract_id,
                schema_version=case.contract.schema_version,
            )
        return super().admit(case, capture_id_factory=capture_id_factory)


class ProviderSubstitutionMutant(ReferenceSubject):
    def admit(self, case: AdmissionCase, *, capture_id_factory: Callable[[str], str]):
        case = replace(case, provider_id=case.contract.provider_id)
        return super().admit(case, capture_id_factory=capture_id_factory)


class CaptureTimeAsSourceTimeMutant(ReferenceSubject):
    def admit(self, case: AdmissionCase, *, capture_id_factory: Callable[[str], str]):
        if case.contract.source_time_kind == "instant" and case.observed_at_utc is None:
            case = replace(case, observed_at_utc=case.captured_at_utc)
        return super().admit(case, capture_id_factory=capture_id_factory)


class HashAsCaptureIdentityMutant(ReferenceSubject):
    def admit(self, case: AdmissionCase, *, capture_id_factory: Callable[[str], str]):
        fingerprint = sha256(case.captured_material).hexdigest()
        return AcceptedAdmission(
            source_object_id=case.source_object_id,
            capture_id=fingerprint,
            content_sha256=fingerprint,
            observed_at_utc=case.observed_at_utc,
            source_date=case.source_date,
            time_precision=case.contract.source_time_kind,
            downstream_owner=case.contract.downstream_owner,
            typed_payload=case.typed_payload,
        )


MUTANTS: dict[str, type[ReferenceSubject]] = {
    "capture_identity_as_source": CaptureIdentityAsSourceMutant,
    "shape_guess": ShapeGuessMutant,
    "provider_substitution": ProviderSubstitutionMutant,
    "capture_time_as_source_time": CaptureTimeAsSourceTimeMutant,
    "hash_as_capture_identity": HashAsCaptureIdentityMutant,
}


def valid_case(*, source_time_kind: str = "instant") -> AdmissionCase:
    from datetime import UTC

    contract = FamilyContract(source_time_kind=source_time_kind)
    observed = datetime(2026, 7, 31, 1, 15, tzinfo=UTC) if source_time_kind == "instant" else None
    source_date = date(2026, 7, 31) if source_time_kind == "date" else None
    return AdmissionCase(
        contract=contract,
        provider_id="recorded-provider",
        acquisition_channel="recorded_api_response",
        source_object_id="provider-observation-17",
        observed_at_utc=observed,
        source_date=source_date,
        captured_at_utc=datetime(2026, 7, 31, 1, 16, tzinfo=UTC),
        captured_material=b'{"symbol":"NVDA","value":121.5}',
        typed_payload=FixtureSignalPayload(symbol="NVDA", value=121.5),
        family_id=contract.family_id,
        contract_id=contract.contract_id,
        schema_version=contract.schema_version,
    )


def capture_id_factory(_: str) -> str:
    return "capture::m01::0001"


def production_api() -> dict[str, Any]:
    from nvda_desk import m01_source_admission as api

    return {name: getattr(api, name) for name in api.__all__}
