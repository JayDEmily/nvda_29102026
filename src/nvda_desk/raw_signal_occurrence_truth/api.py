"""Typed public seam for the admitted Raw Signal Occurrence Truth owner."""

from collections.abc import Sequence
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Literal, NoReturn


@dataclass(frozen=True, slots=True)
class _OpaqueIdentity:
    value: str

    def __post_init__(self) -> None:
        if type(self.value) is not str or not self.value:
            raise ValueError("opaque identity must be a non-empty string")

    def __str__(self) -> str:
        return self.value


class _ConceptId(_OpaqueIdentity):
    __slots__ = ()


class _ContractId(_OpaqueIdentity):
    __slots__ = ()


class _ScopePolicyId(_OpaqueIdentity):
    __slots__ = ()


class _EligibilityPolicyRef(_OpaqueIdentity):
    __slots__ = ()


class _ScopePolicyRef(_OpaqueIdentity):
    __slots__ = ()


class _CaptureOccurrenceId(_OpaqueIdentity):
    __slots__ = ()


class _ObservationOccurrenceId(_OpaqueIdentity):
    __slots__ = ()


class _AssessmentOccurrenceId(_OpaqueIdentity):
    __slots__ = ()


class _ProviderId(_OpaqueIdentity):
    __slots__ = ()


class _DeliveryArtifactRef(_OpaqueIdentity):
    __slots__ = ()


class _IngestionSequenceScope(_OpaqueIdentity):
    __slots__ = ()


class RawSignalCatalogueId(_OpaqueIdentity):
    """Canonical Raw Signal catalogue identity in the admitted R001-R323 range."""

    __slots__ = ()

    def __post_init__(self) -> None:
        super().__post_init__()
        value = self.value
        if len(value) != 4 or value[0] != "R" or not value[1:].isdigit():
            raise ValueError("Raw Signal catalogue identity must be canonical RNNN form")
        number = int(value[1:])
        if not 1 <= number <= 323:
            raise ValueError("Raw Signal catalogue identity must be in R001-R323")


UnitsNotApplicable = Literal["not_applicable"]
SourceTemporalKind = Literal["true_instant", "date_only", "receipt_only"]
ReceiptRelationRole = Literal["evidences_receipt_presence_only"]
AssessmentOutcome = Literal[
    "unknown_not_established",
    "zero_received",
    "one_or_more_received",
]


_POLICY_CONCEPT = "raw_signal.capture_scope_policy"
_POLICY_CONTRACT = "nvda.raw_signal.CaptureScopePolicy.v1"
_CAPTURE_CONCEPT = "raw_signal.scheduled_capture_occurrence"
_CAPTURE_CONTRACT = "nvda.raw_signal.ScheduledCaptureOccurrence.v1"
_OBSERVATION_CONCEPT = "raw_signal.raw_observation_occurrence"
_OBSERVATION_CONTRACT = "nvda.raw_signal.RawObservationOccurrence.v1"
_RELATION_CONCEPT = "raw_signal.capture_receipt_evidence_relation"
_RELATION_CONTRACT = "nvda.raw_signal.CaptureReceiptEvidenceRelation.v1"
_ASSESSMENT_CONCEPT = "raw_signal.capture_receipt_presence_assessment"
_ASSESSMENT_CONTRACT = "nvda.raw_signal.CaptureReceiptPresenceAssessment.v1"


def _require_exact_type(value: object, expected: type[object], field_name: str) -> None:
    if type(value) is not expected:
        raise TypeError(f"{field_name} must use the {expected.__name__} identity layer")


def _require_exact_identity_value(
    value: _OpaqueIdentity,
    expected_type: type[_OpaqueIdentity],
    expected_value: str,
    field_name: str,
) -> None:
    _require_exact_type(value, expected_type, field_name)
    if value.value != expected_value:
        raise ValueError(f"{field_name} must be {expected_value!r}")


def _require_utc(value: datetime, field_name: str) -> None:
    if type(value) is not datetime:
        raise TypeError(f"{field_name} must be a datetime")
    if value.tzinfo is None or value.utcoffset() != timedelta(0):
        raise ValueError(f"{field_name} must be UTC-aware")


def _require_optional_string(value: str | None, field_name: str) -> None:
    if value is not None and type(value) is not str:
        raise TypeError(f"{field_name} must be a string or absent")


def _not_implemented(unit: str) -> NoReturn:
    raise NotImplementedError(f"behaviour belongs to {unit} and is not implemented by IWO-U01")


@dataclass(frozen=True, slots=True)
class CaptureScopePolicyV1:
    concept_id: _ConceptId
    contract_id: _ContractId
    units: UnitsNotApplicable
    scope_policy_id: _ScopePolicyId
    scope_policy_version: int
    activation_ts_utc: datetime
    eligibility_policy_ref: _EligibilityPolicyRef
    deactivation_ts_utc: datetime | None = None

    def __post_init__(self) -> None:
        _require_exact_identity_value(
            self.concept_id, _ConceptId, _POLICY_CONCEPT, "concept_id"
        )
        _require_exact_identity_value(
            self.contract_id, _ContractId, _POLICY_CONTRACT, "contract_id"
        )
        if self.units != "not_applicable":
            raise ValueError("CaptureScopePolicyV1.units must be 'not_applicable'")
        _require_exact_type(self.scope_policy_id, _ScopePolicyId, "scope_policy_id")
        if type(self.scope_policy_version) is not int or self.scope_policy_version <= 0:
            raise ValueError("scope_policy_version must be a positive integer")
        _require_utc(self.activation_ts_utc, "activation_ts_utc")
        if self.deactivation_ts_utc is not None:
            _require_utc(self.deactivation_ts_utc, "deactivation_ts_utc")
        _require_exact_type(
            self.eligibility_policy_ref,
            _EligibilityPolicyRef,
            "eligibility_policy_ref",
        )


@dataclass(frozen=True, slots=True)
class ScheduledCaptureOccurrenceV1:
    concept_id: _ConceptId
    contract_id: _ContractId
    units: UnitsNotApplicable
    capture_occurrence_id: _CaptureOccurrenceId
    scope_policy_ref: _ScopePolicyRef
    slot_start_utc: datetime
    slot_end_utc: datetime

    def __post_init__(self) -> None:
        _require_exact_identity_value(
            self.concept_id, _ConceptId, _CAPTURE_CONCEPT, "concept_id"
        )
        _require_exact_identity_value(
            self.contract_id, _ContractId, _CAPTURE_CONTRACT, "contract_id"
        )
        if self.units != "not_applicable":
            raise ValueError("ScheduledCaptureOccurrenceV1.units must be 'not_applicable'")
        _require_exact_type(
            self.capture_occurrence_id, _CaptureOccurrenceId, "capture_occurrence_id"
        )
        _require_exact_type(self.scope_policy_ref, _ScopePolicyRef, "scope_policy_ref")
        _require_utc(self.slot_start_utc, "slot_start_utc")
        _require_utc(self.slot_end_utc, "slot_end_utc")


@dataclass(frozen=True, slots=True)
class RawObservationOccurrenceV1:
    concept_id: _ConceptId
    contract_id: _ContractId
    observation_occurrence_id: _ObservationOccurrenceId
    delivery_artifact_ref: _DeliveryArtifactRef
    source_provider: _ProviderId
    native_record: dict[str, object]
    received_ts_utc: datetime
    ingestion_sequence: int
    ingestion_sequence_scope: _IngestionSequenceScope
    source_temporal_kind: SourceTemporalKind
    raw_signal_catalogue_ids: tuple[RawSignalCatalogueId, ...] | None = None
    source_product_api: str | None = None
    source_endpoint_callback: str | None = None
    native_identifier: str | None = None
    native_tick_series_identifier: str | None = None
    source_variant: str | None = None
    subject_instrument: str | None = None
    native_units: str | None = None
    availability_session: str | None = None
    source_status_native: str | None = None
    revision_vintage_native: str | None = None
    received_epoch_ns: int | None = None
    source_timestamp_raw: str | None = None
    source_timezone_native: str | None = None
    market_timezone_iana: str | None = None
    market_session_native: str | None = None

    def __post_init__(self) -> None:
        _require_exact_identity_value(
            self.concept_id, _ConceptId, _OBSERVATION_CONCEPT, "concept_id"
        )
        _require_exact_identity_value(
            self.contract_id, _ContractId, _OBSERVATION_CONTRACT, "contract_id"
        )
        _require_exact_type(
            self.observation_occurrence_id,
            _ObservationOccurrenceId,
            "observation_occurrence_id",
        )
        _require_exact_type(
            self.delivery_artifact_ref, _DeliveryArtifactRef, "delivery_artifact_ref"
        )
        _require_exact_type(self.source_provider, _ProviderId, "source_provider")
        if self.raw_signal_catalogue_ids is not None:
            if type(self.raw_signal_catalogue_ids) is not tuple:
                raise TypeError("raw_signal_catalogue_ids must be a tuple or absent")
            if not self.raw_signal_catalogue_ids:
                raise ValueError("raw_signal_catalogue_ids uses absence, not an empty tuple")
            if any(
                type(item) is not RawSignalCatalogueId
                for item in self.raw_signal_catalogue_ids
            ):
                raise TypeError("raw_signal_catalogue_ids must contain RawSignalCatalogueId values")
            if len(set(self.raw_signal_catalogue_ids)) != len(self.raw_signal_catalogue_ids):
                raise ValueError("raw_signal_catalogue_ids must not contain duplicates")
        if type(self.native_record) is not dict:
            raise TypeError("native_record must be a provider-native mapping")
        _require_utc(self.received_ts_utc, "received_ts_utc")
        if self.received_epoch_ns is not None and type(self.received_epoch_ns) is not int:
            raise TypeError("received_epoch_ns must be an integer or absent")
        if type(self.ingestion_sequence) is not int:
            raise TypeError("ingestion_sequence must be an integer")
        _require_exact_type(
            self.ingestion_sequence_scope,
            _IngestionSequenceScope,
            "ingestion_sequence_scope",
        )
        if self.source_temporal_kind not in ("true_instant", "date_only", "receipt_only"):
            raise ValueError("source_temporal_kind is outside the v1 contract")
        if self.source_temporal_kind == "receipt_only":
            if self.source_timestamp_raw is not None:
                raise ValueError("receipt_only must not fabricate a source timestamp")
        elif self.source_timestamp_raw is None:
            raise ValueError(f"{self.source_temporal_kind} requires source_timestamp_raw")
        for field_name in (
            "source_product_api",
            "source_endpoint_callback",
            "native_identifier",
            "native_tick_series_identifier",
            "source_variant",
            "subject_instrument",
            "native_units",
            "availability_session",
            "source_status_native",
            "revision_vintage_native",
            "source_timestamp_raw",
            "source_timezone_native",
            "market_timezone_iana",
            "market_session_native",
        ):
            _require_optional_string(getattr(self, field_name), field_name)


@dataclass(frozen=True, slots=True)
class CaptureReceiptEvidenceRelationV1:
    concept_id: _ConceptId
    contract_id: _ContractId
    units: UnitsNotApplicable
    observation_occurrence_ref: _ObservationOccurrenceId
    capture_occurrence_ref: _CaptureOccurrenceId
    scope_policy_ref: _ScopePolicyRef
    received_ts_utc: datetime
    relation_role: ReceiptRelationRole

    def __post_init__(self) -> None:
        _require_exact_identity_value(
            self.concept_id, _ConceptId, _RELATION_CONCEPT, "concept_id"
        )
        _require_exact_identity_value(
            self.contract_id, _ContractId, _RELATION_CONTRACT, "contract_id"
        )
        if self.units != "not_applicable":
            raise ValueError("CaptureReceiptEvidenceRelationV1.units must be 'not_applicable'")
        _require_exact_type(
            self.observation_occurrence_ref,
            _ObservationOccurrenceId,
            "observation_occurrence_ref",
        )
        _require_exact_type(
            self.capture_occurrence_ref, _CaptureOccurrenceId, "capture_occurrence_ref"
        )
        _require_exact_type(self.scope_policy_ref, _ScopePolicyRef, "scope_policy_ref")
        _require_utc(self.received_ts_utc, "received_ts_utc")
        if self.relation_role != "evidences_receipt_presence_only":
            raise ValueError("relation_role is outside the v1 contract")


@dataclass(frozen=True, slots=True)
class CaptureReceiptPresenceAssessmentV1:
    concept_id: _ConceptId
    contract_id: _ContractId
    units: UnitsNotApplicable
    assessment_occurrence_id: _AssessmentOccurrenceId
    capture_occurrence_ref: _CaptureOccurrenceId
    outcome: AssessmentOutcome
    evidence_as_of_ts_utc: datetime
    supersedes_assessment_ref: _AssessmentOccurrenceId | None = None

    def __post_init__(self) -> None:
        _require_exact_identity_value(
            self.concept_id, _ConceptId, _ASSESSMENT_CONCEPT, "concept_id"
        )
        _require_exact_identity_value(
            self.contract_id, _ContractId, _ASSESSMENT_CONTRACT, "contract_id"
        )
        if self.units != "not_applicable":
            raise ValueError(
                "CaptureReceiptPresenceAssessmentV1.units must be 'not_applicable'"
            )
        _require_exact_type(
            self.assessment_occurrence_id,
            _AssessmentOccurrenceId,
            "assessment_occurrence_id",
        )
        _require_exact_type(
            self.capture_occurrence_ref, _CaptureOccurrenceId, "capture_occurrence_ref"
        )
        if self.outcome not in (
            "unknown_not_established",
            "zero_received",
            "one_or_more_received",
        ):
            raise ValueError("outcome is outside the v1 contract")
        _require_utc(self.evidence_as_of_ts_utc, "evidence_as_of_ts_utc")
        if self.supersedes_assessment_ref is not None:
            _require_exact_type(
                self.supersedes_assessment_ref,
                _AssessmentOccurrenceId,
                "supersedes_assessment_ref",
            )


class _CommandsV1:
    def register_capture_scope_policy(
        self, value: CaptureScopePolicyV1
    ) -> CaptureScopePolicyV1:
        _not_implemented("IWO-U02")

    def realise_scheduled_capture_occurrence(
        self,
        scope_policy_ref: _ScopePolicyRef,
        capture_occurrence_id: _CaptureOccurrenceId,
        slot_start_utc: datetime,
    ) -> ScheduledCaptureOccurrenceV1:
        _not_implemented("IWO-U02")

    def admit_raw_observation_occurrence(
        self, value: RawObservationOccurrenceV1
    ) -> RawObservationOccurrenceV1:
        _not_implemented("IWO-U03")

    def derive_capture_receipt_evidence_relation(
        self,
        observation_occurrence_ref: _ObservationOccurrenceId,
        capture_occurrence_ref: _CaptureOccurrenceId,
        scope_policy_ref: _ScopePolicyRef,
    ) -> CaptureReceiptEvidenceRelationV1 | None:
        _not_implemented("IWO-U04")

    def append_capture_receipt_presence_assessment(
        self,
        assessment_occurrence_id: _AssessmentOccurrenceId,
        capture_occurrence_ref: _CaptureOccurrenceId,
        evidence_as_of_ts_utc: datetime,
        supersedes_assessment_ref: _AssessmentOccurrenceId | None,
    ) -> CaptureReceiptPresenceAssessmentV1:
        _not_implemented("IWO-U04")

    def reconcile_owed_slots(
        self,
        scope_policy_ref: _ScopePolicyRef,
        slot_starts_utc: Sequence[datetime],
        capture_occurrence_ids: Sequence[_CaptureOccurrenceId],
        assessment_occurrence_ids: Sequence[_AssessmentOccurrenceId],
    ) -> Sequence[CaptureReceiptPresenceAssessmentV1]:
        _not_implemented("IWO-U05")


class _ReadsV1:
    def get_capture_scope_policy(
        self, scope_policy_id: _ScopePolicyId, scope_policy_version: int
    ) -> CaptureScopePolicyV1 | None:
        _not_implemented("IWO-U02")

    def get_scheduled_capture_occurrence(
        self, capture_occurrence_id: _CaptureOccurrenceId
    ) -> ScheduledCaptureOccurrenceV1 | None:
        _not_implemented("IWO-U02")

    def get_raw_observation_occurrence(
        self, observation_occurrence_id: _ObservationOccurrenceId
    ) -> RawObservationOccurrenceV1 | None:
        _not_implemented("IWO-U03")

    def get_receipt_presence_assessment(
        self, assessment_occurrence_id: _AssessmentOccurrenceId
    ) -> CaptureReceiptPresenceAssessmentV1 | None:
        _not_implemented("IWO-U04")

    def list_receipt_presence_assessments(
        self, capture_occurrence_id: _CaptureOccurrenceId
    ) -> Sequence[CaptureReceiptPresenceAssessmentV1]:
        _not_implemented("IWO-U04")


@dataclass(frozen=True, slots=True)
class _OwnerV1:
    commands: _CommandsV1
    reads: _ReadsV1


def create_owner() -> _OwnerV1:
    """Construct the admitted owner boundary without implementing later-unit behaviour."""

    return _OwnerV1(commands=_CommandsV1(), reads=_ReadsV1())


__all__ = [
    "CaptureReceiptEvidenceRelationV1",
    "CaptureReceiptPresenceAssessmentV1",
    "CaptureScopePolicyV1",
    "RawObservationOccurrenceV1",
    "RawSignalCatalogueId",
    "ScheduledCaptureOccurrenceV1",
    "create_owner",
]
