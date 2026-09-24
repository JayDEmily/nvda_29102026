"""Typed public seam for the admitted Raw Signal Occurrence Truth owner."""

from collections.abc import Callable, Iterator, Mapping, Sequence
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from decimal import Decimal
from struct import pack
from typing import Literal, NoReturn, Protocol, cast


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


type NativeValueV1 = (
    None
    | bool
    | int
    | float
    | Decimal
    | str
    | bytes
    | list[NativeValueV1]
    | tuple[NativeValueV1, ...]
    | Mapping[str, NativeValueV1]
)


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


def _require_half_minute_boundary(value: datetime, field_name: str) -> None:
    _require_utc(value, field_name)
    if value.microsecond != 0 or value.second not in (0, 30):
        raise ValueError(f"{field_name} must be aligned to a nominal :00 or :30 UTC boundary")


def _intervals_overlap(
    left_start: datetime,
    left_end: datetime | None,
    right_start: datetime,
    right_end: datetime | None,
) -> bool:
    left_before_right_end = right_end is None or left_start < right_end
    right_before_left_end = left_end is None or right_start < left_end
    return left_before_right_end and right_before_left_end


def _not_implemented(unit: str) -> NoReturn:
    raise NotImplementedError(
        f"behaviour belongs to {unit} and is not implemented by the current realised boundary"
    )


def _snapshot_native_mapping(
    source: Mapping[object, object], active_container_ids: set[int]
) -> dict[str, NativeValueV1]:
    container_id = id(source)
    if container_id in active_container_ids:
        raise TypeError("native_record must be an acyclic NativeValueV1 value")
    active_container_ids.add(container_id)
    try:
        snapshot: dict[str, NativeValueV1] = {}
        for key, value in source.items():
            if type(key) is not str:
                raise TypeError("native_record mapping field names must be exact built-in strings")
            snapshot[key] = _snapshot_native_value(value, active_container_ids)
        return snapshot
    finally:
        active_container_ids.remove(container_id)


def _snapshot_native_value(value: object, active_container_ids: set[int]) -> NativeValueV1:
    if value is None:
        return None
    if type(value) is bool:
        return value
    if type(value) is int:
        return value
    if type(value) is float:
        return value
    if type(value) is Decimal:
        return value
    if type(value) is str:
        return value
    if type(value) is bytes:
        return value
    if type(value) is list:
        container_id = id(value)
        if container_id in active_container_ids:
            raise TypeError("native_record must be an acyclic NativeValueV1 value")
        active_container_ids.add(container_id)
        try:
            return [
                _snapshot_native_value(item, active_container_ids)
                for item in cast(list[object], value)
            ]
        finally:
            active_container_ids.remove(container_id)
    if type(value) is tuple:
        container_id = id(value)
        if container_id in active_container_ids:
            raise TypeError("native_record must be an acyclic NativeValueV1 value")
        active_container_ids.add(container_id)
        try:
            return tuple(
                _snapshot_native_value(item, active_container_ids)
                for item in cast(tuple[object, ...], value)
            )
        finally:
            active_container_ids.remove(container_id)
    if isinstance(value, Mapping):
        return _snapshot_native_mapping(cast(Mapping[object, object], value), active_container_ids)
    raise TypeError("native_record contains a value outside the NativeValueV1 carrier")


class _NativeRecordSnapshot(Mapping[str, NativeValueV1]):
    """Alias-safe read-only snapshot of one provider-logical native record."""

    __slots__ = ("__data",)

    def __init__(self, source: Mapping[str, NativeValueV1]) -> None:
        self.__data = _snapshot_native_mapping(cast(Mapping[object, object], source), set())

    def __getitem__(self, key: str) -> NativeValueV1:
        return _snapshot_native_value(self.__data[key], set())

    def __iter__(self) -> Iterator[str]:
        return iter(self.__data)

    def __len__(self) -> int:
        return len(self.__data)


def _native_float_exactly_equal(left: float, right: float) -> bool:
    """Compare the exact IEEE-754 representation of two native float values."""

    return pack("!d", left) == pack("!d", right)


def _native_values_exactly_equal(left: object, right: object) -> bool:
    """Compare only admitted NativeValueV1 values by authorised exact content."""

    left_is_mapping = isinstance(left, Mapping)
    right_is_mapping = isinstance(right, Mapping)
    if left_is_mapping or right_is_mapping:
        if not (left_is_mapping and right_is_mapping):
            return False
        left_mapping = cast(Mapping[str, object], left)
        right_mapping = cast(Mapping[str, object], right)
        if len(left_mapping) != len(right_mapping):
            return False
        if set(left_mapping) != set(right_mapping):
            return False
        return all(
            _native_values_exactly_equal(left_mapping[key], right_mapping[key])
            for key in left_mapping
        )

    if type(left) is not type(right):
        return False
    if left is None:
        return True
    if type(left) is bool:
        return left is right
    if type(left) is int:
        return left == right
    if type(left) is float:
        return _native_float_exactly_equal(left, cast(float, right))
    if type(left) is Decimal:
        return left.as_tuple() == cast(Decimal, right).as_tuple()
    if type(left) is str:
        return left == right
    if type(left) is bytes:
        return left == right
    if type(left) is list:
        left_list = cast(list[object], left)
        right_list = cast(list[object], right)
        return len(left_list) == len(right_list) and all(
            _native_values_exactly_equal(left_item, right_item)
            for left_item, right_item in zip(left_list, right_list, strict=True)
        )
    if type(left) is tuple:
        left_tuple = cast(tuple[object, ...], left)
        right_tuple = cast(tuple[object, ...], right)
        return len(left_tuple) == len(right_tuple) and all(
            _native_values_exactly_equal(left_item, right_item)
            for left_item, right_item in zip(left_tuple, right_tuple, strict=True)
        )
    raise TypeError("native comparator received a value outside the NativeValueV1 carrier")


def _observations_exactly_equal(
    left: "RawObservationOccurrenceV1", right: "RawObservationOccurrenceV1"
) -> bool:
    non_native_equal = (
        left.concept_id == right.concept_id
        and left.contract_id == right.contract_id
        and left.observation_occurrence_id == right.observation_occurrence_id
        and left.delivery_artifact_ref == right.delivery_artifact_ref
        and left.source_provider == right.source_provider
        and left.received_ts_utc == right.received_ts_utc
        and left.ingestion_sequence == right.ingestion_sequence
        and left.ingestion_sequence_scope == right.ingestion_sequence_scope
        and left.source_temporal_kind == right.source_temporal_kind
        and left.raw_signal_catalogue_ids == right.raw_signal_catalogue_ids
        and left.source_product_api == right.source_product_api
        and left.source_endpoint_callback == right.source_endpoint_callback
        and left.native_identifier == right.native_identifier
        and left.native_tick_series_identifier == right.native_tick_series_identifier
        and left.source_variant == right.source_variant
        and left.subject_instrument == right.subject_instrument
        and left.native_units == right.native_units
        and left.availability_session == right.availability_session
        and left.source_status_native == right.source_status_native
        and left.revision_vintage_native == right.revision_vintage_native
        and left.received_epoch_ns == right.received_epoch_ns
        and left.source_timestamp_raw == right.source_timestamp_raw
        and left.source_timezone_native == right.source_timezone_native
        and left.market_timezone_iana == right.market_timezone_iana
        and left.market_session_native == right.market_session_native
    )
    return non_native_equal and _native_values_exactly_equal(
        left.native_record, right.native_record
    )


def concept_id(value: str) -> _ConceptId:
    """Construct a canonical-concept identity value for a public v1 payload."""

    return _ConceptId(value)


def contract_id(value: str) -> _ContractId:
    """Construct a payload-contract identity value for a public v1 payload."""

    return _ContractId(value)


def scope_policy_id(value: str) -> _ScopePolicyId:
    return _ScopePolicyId(value)


def eligibility_policy_ref(value: str) -> _EligibilityPolicyRef:
    return _EligibilityPolicyRef(value)


def scope_policy_ref(value: str) -> _ScopePolicyRef:
    return _ScopePolicyRef(value)


def capture_occurrence_id(value: str) -> _CaptureOccurrenceId:
    return _CaptureOccurrenceId(value)


def observation_occurrence_id(value: str) -> _ObservationOccurrenceId:
    return _ObservationOccurrenceId(value)


def assessment_occurrence_id(value: str) -> _AssessmentOccurrenceId:
    return _AssessmentOccurrenceId(value)


def provider_id(value: str) -> _ProviderId:
    return _ProviderId(value)


def delivery_artifact_ref(value: str) -> _DeliveryArtifactRef:
    return _DeliveryArtifactRef(value)


def ingestion_sequence_scope(value: str) -> _IngestionSequenceScope:
    return _IngestionSequenceScope(value)


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
        _require_half_minute_boundary(self.activation_ts_utc, "activation_ts_utc")
        if self.deactivation_ts_utc is not None:
            _require_half_minute_boundary(self.deactivation_ts_utc, "deactivation_ts_utc")
            if self.deactivation_ts_utc <= self.activation_ts_utc:
                raise ValueError("deactivation_ts_utc must be later than activation_ts_utc")
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
        _require_half_minute_boundary(self.slot_start_utc, "slot_start_utc")
        _require_half_minute_boundary(self.slot_end_utc, "slot_end_utc")
        if self.slot_end_utc != self.slot_start_utc + timedelta(seconds=30):
            raise ValueError("slot_end_utc must be exactly 30 seconds after slot_start_utc")


@dataclass(frozen=True, slots=True)
class RawObservationOccurrenceV1:
    concept_id: _ConceptId
    contract_id: _ContractId
    observation_occurrence_id: _ObservationOccurrenceId
    delivery_artifact_ref: _DeliveryArtifactRef
    source_provider: _ProviderId
    native_record: Mapping[str, NativeValueV1]
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
        if not isinstance(self.native_record, Mapping):
            raise TypeError("native_record must be a provider-native mapping")
        object.__setattr__(self, "native_record", _NativeRecordSnapshot(self.native_record))
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
        for field_value, field_name in (
            (self.source_product_api, "source_product_api"),
            (self.source_endpoint_callback, "source_endpoint_callback"),
            (self.native_identifier, "native_identifier"),
            (self.native_tick_series_identifier, "native_tick_series_identifier"),
            (self.source_variant, "source_variant"),
            (self.subject_instrument, "subject_instrument"),
            (self.native_units, "native_units"),
            (self.availability_session, "availability_session"),
            (self.source_status_native, "source_status_native"),
            (self.revision_vintage_native, "revision_vintage_native"),
            (self.source_timestamp_raw, "source_timestamp_raw"),
            (self.source_timezone_native, "source_timezone_native"),
            (self.market_timezone_iana, "market_timezone_iana"),
            (self.market_session_native, "market_session_native"),
        ):
            _require_optional_string(field_value, field_name)


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


@dataclass(slots=True)
class _OwnerState:
    policies_by_identity: dict[tuple[_ScopePolicyId, int], CaptureScopePolicyV1] = field(
        default_factory=dict
    )
    policies_by_ref: dict[_ScopePolicyRef, CaptureScopePolicyV1] = field(default_factory=dict)
    captures_by_identity: dict[_CaptureOccurrenceId, ScheduledCaptureOccurrenceV1] = field(
        default_factory=dict
    )
    captures_by_slot: dict[tuple[_ScopePolicyRef, datetime], ScheduledCaptureOccurrenceV1] = field(
        default_factory=dict
    )
    observations_by_identity: dict[
        _ObservationOccurrenceId, RawObservationOccurrenceV1
    ] = field(default_factory=dict)
    ingestion_high_water_by_scope: dict[_IngestionSequenceScope, int] = field(
        default_factory=dict
    )
    relations_by_key: dict[
        tuple[_ObservationOccurrenceId, _CaptureOccurrenceId, _ScopePolicyRef],
        CaptureReceiptEvidenceRelationV1,
    ] = field(default_factory=dict)
    assessments_by_identity: dict[
        _AssessmentOccurrenceId, CaptureReceiptPresenceAssessmentV1
    ] = field(default_factory=dict)
    assessment_order_by_capture: dict[
        _CaptureOccurrenceId, list[_AssessmentOccurrenceId]
    ] = field(default_factory=dict)


def _scope_ref_for_policy(value: CaptureScopePolicyV1) -> _ScopePolicyRef:
    return _ScopePolicyRef(f"{value.scope_policy_id.value}@{value.scope_policy_version}")


_RegisterPolicy = Callable[[CaptureScopePolicyV1], CaptureScopePolicyV1]
_RealiseCapture = Callable[
    [_ScopePolicyRef, _CaptureOccurrenceId, datetime], ScheduledCaptureOccurrenceV1
]
_ReadPolicy = Callable[[_ScopePolicyId, int], CaptureScopePolicyV1 | None]
_ReadCapture = Callable[[_CaptureOccurrenceId], ScheduledCaptureOccurrenceV1 | None]
_AdmitObservation = Callable[[RawObservationOccurrenceV1], RawObservationOccurrenceV1]
_ReadObservation = Callable[[_ObservationOccurrenceId], RawObservationOccurrenceV1 | None]
_EligibilityResolver = Callable[[RawObservationOccurrenceV1, CaptureScopePolicyV1], bool]
_DeriveRelation = Callable[
    [_ObservationOccurrenceId, _CaptureOccurrenceId, _ScopePolicyRef],
    CaptureReceiptEvidenceRelationV1 | None,
]
_AppendAssessment = Callable[
    [_AssessmentOccurrenceId, _CaptureOccurrenceId, datetime, _AssessmentOccurrenceId | None],
    CaptureReceiptPresenceAssessmentV1,
]
_ReadAssessment = Callable[[_AssessmentOccurrenceId], CaptureReceiptPresenceAssessmentV1 | None]
_ListAssessments = Callable[[_CaptureOccurrenceId], Sequence[CaptureReceiptPresenceAssessmentV1]]


class _AssessmentPersistencePort(Protocol):
    def append_assessment(
        self, value: CaptureReceiptPresenceAssessmentV1
    ) -> CaptureReceiptPresenceAssessmentV1: ...


class _CommandsV1:
    __slots__ = (
        "__admit_observation",
        "__append_assessment",
        "__derive_relation",
        "__realise_capture",
        "__register_policy",
    )

    def __init__(
        self,
        register_policy: _RegisterPolicy,
        realise_capture: _RealiseCapture,
        admit_observation: _AdmitObservation,
        derive_relation: _DeriveRelation,
        append_assessment: _AppendAssessment,
    ) -> None:
        self.__register_policy = register_policy
        self.__realise_capture = realise_capture
        self.__admit_observation = admit_observation
        self.__derive_relation = derive_relation
        self.__append_assessment = append_assessment

    def register_capture_scope_policy(self, value: CaptureScopePolicyV1) -> CaptureScopePolicyV1:
        return self.__register_policy(value)

    def realise_scheduled_capture_occurrence(
        self,
        scope_policy_ref: _ScopePolicyRef,
        capture_occurrence_id: _CaptureOccurrenceId,
        slot_start_utc: datetime,
    ) -> ScheduledCaptureOccurrenceV1:
        return self.__realise_capture(
            scope_policy_ref, capture_occurrence_id, slot_start_utc
        )

    def admit_raw_observation_occurrence(
        self, value: RawObservationOccurrenceV1
    ) -> RawObservationOccurrenceV1:
        return self.__admit_observation(value)

    def derive_capture_receipt_evidence_relation(
        self,
        observation_occurrence_ref: _ObservationOccurrenceId,
        capture_occurrence_ref: _CaptureOccurrenceId,
        scope_policy_ref: _ScopePolicyRef,
    ) -> CaptureReceiptEvidenceRelationV1 | None:
        return self.__derive_relation(
            observation_occurrence_ref, capture_occurrence_ref, scope_policy_ref
        )

    def append_capture_receipt_presence_assessment(
        self,
        assessment_occurrence_id: _AssessmentOccurrenceId,
        capture_occurrence_ref: _CaptureOccurrenceId,
        evidence_as_of_ts_utc: datetime,
        supersedes_assessment_ref: _AssessmentOccurrenceId | None,
    ) -> CaptureReceiptPresenceAssessmentV1:
        return self.__append_assessment(
            assessment_occurrence_id,
            capture_occurrence_ref,
            evidence_as_of_ts_utc,
            supersedes_assessment_ref,
        )

    def reconcile_owed_slots(
        self,
        scope_policy_ref: _ScopePolicyRef,
        slot_starts_utc: Sequence[datetime],
        capture_occurrence_ids: Sequence[_CaptureOccurrenceId],
        assessment_occurrence_ids: Sequence[_AssessmentOccurrenceId],
    ) -> Sequence[CaptureReceiptPresenceAssessmentV1]:
        _not_implemented("IWO-U05")


class _ReadsV1:
    __slots__ = (
        "__list_assessments",
        "__read_assessment",
        "__read_capture",
        "__read_observation",
        "__read_policy",
    )

    def __init__(
        self,
        read_policy: _ReadPolicy,
        read_capture: _ReadCapture,
        read_observation: _ReadObservation,
        read_assessment: _ReadAssessment,
        list_assessments: _ListAssessments,
    ) -> None:
        self.__read_policy = read_policy
        self.__read_capture = read_capture
        self.__read_observation = read_observation
        self.__read_assessment = read_assessment
        self.__list_assessments = list_assessments

    def get_capture_scope_policy(
        self, scope_policy_id: _ScopePolicyId, scope_policy_version: int
    ) -> CaptureScopePolicyV1 | None:
        return self.__read_policy(scope_policy_id, scope_policy_version)

    def get_scheduled_capture_occurrence(
        self, capture_occurrence_id: _CaptureOccurrenceId
    ) -> ScheduledCaptureOccurrenceV1 | None:
        return self.__read_capture(capture_occurrence_id)

    def get_raw_observation_occurrence(
        self, observation_occurrence_id: _ObservationOccurrenceId
    ) -> RawObservationOccurrenceV1 | None:
        return self.__read_observation(observation_occurrence_id)

    def get_receipt_presence_assessment(
        self, assessment_occurrence_id: _AssessmentOccurrenceId
    ) -> CaptureReceiptPresenceAssessmentV1 | None:
        return self.__read_assessment(assessment_occurrence_id)

    def list_receipt_presence_assessments(
        self, capture_occurrence_id: _CaptureOccurrenceId
    ) -> Sequence[CaptureReceiptPresenceAssessmentV1]:
        return self.__list_assessments(capture_occurrence_id)


def _build_owner_facets(
    *,
    eligibility_resolver: _EligibilityResolver | None,
    persistence_port: _AssessmentPersistencePort | None,
) -> tuple[_CommandsV1, _ReadsV1]:
    state = _OwnerState()

    def register_policy(value: CaptureScopePolicyV1) -> CaptureScopePolicyV1:
        if type(value) is not CaptureScopePolicyV1:
            raise TypeError("value must be CaptureScopePolicyV1")

        identity_key = (value.scope_policy_id, value.scope_policy_version)
        existing = state.policies_by_identity.get(identity_key)
        if existing is not None:
            if existing != value:
                raise ValueError(
                    "policy identity/version is already registered with different content"
                )
            return existing

        for admitted in state.policies_by_identity.values():
            if _intervals_overlap(
                value.activation_ts_utc,
                value.deactivation_ts_utc,
                admitted.activation_ts_utc,
                admitted.deactivation_ts_utc,
            ):
                raise ValueError("capture-scope policy active intervals must not overlap")

        scope_ref = _scope_ref_for_policy(value)
        if scope_ref in state.policies_by_ref:
            raise ValueError("scope policy reference is already registered")

        state.policies_by_identity[identity_key] = value
        state.policies_by_ref[scope_ref] = value
        return value

    def realise_capture(
        scope_policy_ref: _ScopePolicyRef,
        capture_occurrence_id: _CaptureOccurrenceId,
        slot_start_utc: datetime,
    ) -> ScheduledCaptureOccurrenceV1:
        _require_exact_type(scope_policy_ref, _ScopePolicyRef, "scope_policy_ref")
        _require_exact_type(
            capture_occurrence_id, _CaptureOccurrenceId, "capture_occurrence_id"
        )
        _require_half_minute_boundary(slot_start_utc, "slot_start_utc")

        policy = state.policies_by_ref.get(scope_policy_ref)
        if policy is None:
            raise KeyError("scope_policy_ref is not registered")
        if slot_start_utc < policy.activation_ts_utc:
            raise ValueError("slot_start_utc is before policy activation")
        if policy.deactivation_ts_utc is not None and slot_start_utc >= policy.deactivation_ts_utc:
            raise ValueError("slot_start_utc is at or after policy deactivation")

        slot_key = (scope_policy_ref, slot_start_utc)
        existing_for_slot = state.captures_by_slot.get(slot_key)
        if existing_for_slot is not None:
            if existing_for_slot.capture_occurrence_id != capture_occurrence_id:
                raise ValueError(
                    "owed slot is already realised under a different capture identity"
                )
            return existing_for_slot

        existing_for_identity = state.captures_by_identity.get(capture_occurrence_id)
        if existing_for_identity is not None:
            raise ValueError(
                "capture occurrence identity is already bound to a different owed slot"
            )

        value = ScheduledCaptureOccurrenceV1(
            concept_id=_ConceptId(_CAPTURE_CONCEPT),
            contract_id=_ContractId(_CAPTURE_CONTRACT),
            units="not_applicable",
            capture_occurrence_id=capture_occurrence_id,
            scope_policy_ref=scope_policy_ref,
            slot_start_utc=slot_start_utc,
            slot_end_utc=slot_start_utc + timedelta(seconds=30),
        )
        state.captures_by_identity[capture_occurrence_id] = value
        state.captures_by_slot[slot_key] = value
        return value

    def read_policy(
        scope_policy_id: _ScopePolicyId, scope_policy_version: int
    ) -> CaptureScopePolicyV1 | None:
        _require_exact_type(scope_policy_id, _ScopePolicyId, "scope_policy_id")
        if type(scope_policy_version) is not int or scope_policy_version <= 0:
            raise ValueError("scope_policy_version must be a positive integer")
        return state.policies_by_identity.get((scope_policy_id, scope_policy_version))

    def read_capture(
        capture_occurrence_id: _CaptureOccurrenceId,
    ) -> ScheduledCaptureOccurrenceV1 | None:
        _require_exact_type(
            capture_occurrence_id, _CaptureOccurrenceId, "capture_occurrence_id"
        )
        return state.captures_by_identity.get(capture_occurrence_id)

    def admit_observation(value: RawObservationOccurrenceV1) -> RawObservationOccurrenceV1:
        if type(value) is not RawObservationOccurrenceV1:
            raise TypeError("value must be RawObservationOccurrenceV1")

        existing = state.observations_by_identity.get(value.observation_occurrence_id)
        if existing is not None:
            if not _observations_exactly_equal(existing, value):
                raise ValueError(
                    "observation occurrence identity is already admitted with different content"
                )
            return existing

        previous_high_water = state.ingestion_high_water_by_scope.get(
            value.ingestion_sequence_scope
        )
        if previous_high_water is not None and value.ingestion_sequence < previous_high_water:
            raise ValueError(
                "ingestion_sequence must not decrease within one ingestion_sequence_scope"
            )

        state.observations_by_identity[value.observation_occurrence_id] = value
        if previous_high_water is None or value.ingestion_sequence > previous_high_water:
            state.ingestion_high_water_by_scope[value.ingestion_sequence_scope] = (
                value.ingestion_sequence
            )
        return value

    def read_observation(
        observation_occurrence_id: _ObservationOccurrenceId,
    ) -> RawObservationOccurrenceV1 | None:
        _require_exact_type(
            observation_occurrence_id,
            _ObservationOccurrenceId,
            "observation_occurrence_id",
        )
        return state.observations_by_identity.get(observation_occurrence_id)

    def derive_relation(
        observation_occurrence_ref: _ObservationOccurrenceId,
        capture_occurrence_ref: _CaptureOccurrenceId,
        scope_policy_ref: _ScopePolicyRef,
    ) -> CaptureReceiptEvidenceRelationV1 | None:
        _require_exact_type(
            observation_occurrence_ref,
            _ObservationOccurrenceId,
            "observation_occurrence_ref",
        )
        _require_exact_type(
            capture_occurrence_ref, _CaptureOccurrenceId, "capture_occurrence_ref"
        )
        _require_exact_type(scope_policy_ref, _ScopePolicyRef, "scope_policy_ref")

        observed = state.observations_by_identity.get(observation_occurrence_ref)
        if observed is None:
            raise KeyError("observation_occurrence_ref is not admitted")
        capture = state.captures_by_identity.get(capture_occurrence_ref)
        if capture is None:
            raise KeyError("capture_occurrence_ref is not realised")
        if scope_policy_ref != capture.scope_policy_ref:
            raise ValueError("scope_policy_ref does not match the capture effective policy")
        effective_policy = state.policies_by_ref.get(capture.scope_policy_ref)
        if effective_policy is None:
            raise KeyError("capture effective scope policy is not registered")

        relation_key = (
            observation_occurrence_ref,
            capture_occurrence_ref,
            scope_policy_ref,
        )
        existing = state.relations_by_key.get(relation_key)
        if existing is not None:
            return existing

        if not (capture.slot_start_utc <= observed.received_ts_utc < capture.slot_end_utc):
            return None
        if eligibility_resolver is None:
            raise ValueError(
                "receipt-evidence derivation requires an admitted eligibility resolver"
            )
        eligible = eligibility_resolver(observed, effective_policy)
        if type(eligible) is not bool:
            raise TypeError("eligibility resolver must return an exact bool")
        if not eligible:
            return None

        relation = CaptureReceiptEvidenceRelationV1(
            concept_id=_ConceptId(_RELATION_CONCEPT),
            contract_id=_ContractId(_RELATION_CONTRACT),
            units="not_applicable",
            observation_occurrence_ref=observed.observation_occurrence_id,
            capture_occurrence_ref=capture.capture_occurrence_id,
            scope_policy_ref=capture.scope_policy_ref,
            received_ts_utc=observed.received_ts_utc,
            relation_role="evidences_receipt_presence_only",
        )
        state.relations_by_key[relation_key] = relation
        return relation

    def append_assessment(
        assessment_occurrence_id: _AssessmentOccurrenceId,
        capture_occurrence_ref: _CaptureOccurrenceId,
        evidence_as_of_ts_utc: datetime,
        supersedes_assessment_ref: _AssessmentOccurrenceId | None,
    ) -> CaptureReceiptPresenceAssessmentV1:
        _require_exact_type(
            assessment_occurrence_id,
            _AssessmentOccurrenceId,
            "assessment_occurrence_id",
        )
        _require_exact_type(
            capture_occurrence_ref, _CaptureOccurrenceId, "capture_occurrence_ref"
        )
        _require_utc(evidence_as_of_ts_utc, "evidence_as_of_ts_utc")
        if supersedes_assessment_ref is not None:
            _require_exact_type(
                supersedes_assessment_ref,
                _AssessmentOccurrenceId,
                "supersedes_assessment_ref",
            )

        capture = state.captures_by_identity.get(capture_occurrence_ref)
        if capture is None:
            raise KeyError("capture_occurrence_ref is not realised")
        effective_policy = state.policies_by_ref.get(capture.scope_policy_ref)
        if effective_policy is None:
            raise KeyError("capture effective scope policy is not registered")

        existing = state.assessments_by_identity.get(assessment_occurrence_id)
        if existing is not None:
            if (
                existing.capture_occurrence_ref != capture.capture_occurrence_id
                or existing.evidence_as_of_ts_utc != evidence_as_of_ts_utc
                or existing.supersedes_assessment_ref != supersedes_assessment_ref
            ):
                raise ValueError(
                    "assessment occurrence identity is already appended with different content"
                )
            return existing

        eligible_visible_observation = False
        for observed in state.observations_by_identity.values():
            if not (
                capture.slot_start_utc
                <= observed.received_ts_utc
                < capture.slot_end_utc
            ):
                continue
            if eligibility_resolver is None:
                raise ValueError(
                    "assessment derivation requires an admitted eligibility resolver "
                    "for in-slot observation evidence"
                )
            eligible = eligibility_resolver(observed, effective_policy)
            if type(eligible) is not bool:
                raise TypeError("eligibility resolver must return an exact bool")
            if eligible:
                eligible_visible_observation = True
                break

        outcome: AssessmentOutcome = (
            "one_or_more_received"
            if eligible_visible_observation
            else "zero_received"
        )
        candidate = CaptureReceiptPresenceAssessmentV1(
            concept_id=_ConceptId(_ASSESSMENT_CONCEPT),
            contract_id=_ContractId(_ASSESSMENT_CONTRACT),
            units="not_applicable",
            assessment_occurrence_id=assessment_occurrence_id,
            capture_occurrence_ref=capture.capture_occurrence_id,
            outcome=outcome,
            evidence_as_of_ts_utc=evidence_as_of_ts_utc,
            supersedes_assessment_ref=supersedes_assessment_ref,
        )

        chain = state.assessment_order_by_capture.get(capture_occurrence_ref, [])
        if not chain:
            if supersedes_assessment_ref is not None:
                raise ValueError("first assessment cannot supersede a prior assessment")
        else:
            immediate_predecessor = chain[-1]
            if supersedes_assessment_ref != immediate_predecessor:
                raise ValueError(
                    "assessment must supersede the immediately prior current assessment"
                )

        if persistence_port is not None:
            persistence_port.append_assessment(candidate)
        state.assessments_by_identity[assessment_occurrence_id] = candidate
        state.assessment_order_by_capture.setdefault(capture_occurrence_ref, []).append(
            assessment_occurrence_id
        )
        return candidate

    def read_assessment(
        assessment_occurrence_id: _AssessmentOccurrenceId,
    ) -> CaptureReceiptPresenceAssessmentV1 | None:
        _require_exact_type(
            assessment_occurrence_id,
            _AssessmentOccurrenceId,
            "assessment_occurrence_id",
        )
        return state.assessments_by_identity.get(assessment_occurrence_id)

    def list_assessments(
        capture_occurrence_id: _CaptureOccurrenceId,
    ) -> Sequence[CaptureReceiptPresenceAssessmentV1]:
        _require_exact_type(
            capture_occurrence_id, _CaptureOccurrenceId, "capture_occurrence_id"
        )
        if capture_occurrence_id not in state.captures_by_identity:
            raise KeyError("capture_occurrence_id is not realised")
        return tuple(
            state.assessments_by_identity[assessment_id]
            for assessment_id in state.assessment_order_by_capture.get(
                capture_occurrence_id, ()
            )
        )

    return (
        _CommandsV1(
            register_policy=register_policy,
            realise_capture=realise_capture,
            admit_observation=admit_observation,
            derive_relation=derive_relation,
            append_assessment=append_assessment,
        ),
        _ReadsV1(
            read_policy=read_policy,
            read_capture=read_capture,
            read_observation=read_observation,
            read_assessment=read_assessment,
            list_assessments=list_assessments,
        ),
    )


@dataclass(frozen=True, slots=True)
class _OwnerV1:
    commands: _CommandsV1
    reads: _ReadsV1


def create_owner(
    *,
    eligibility_resolver: _EligibilityResolver | None = None,
    persistence_port: _AssessmentPersistencePort | None = None,
) -> _OwnerV1:
    """Construct the admitted owner boundary through IWO-U04 semantics."""

    commands, reads = _build_owner_facets(
        eligibility_resolver=eligibility_resolver,
        persistence_port=persistence_port,
    )
    return _OwnerV1(commands=commands, reads=reads)


__all__ = [
    "CaptureReceiptEvidenceRelationV1",
    "CaptureReceiptPresenceAssessmentV1",
    "CaptureScopePolicyV1",
    "NativeValueV1",
    "RawObservationOccurrenceV1",
    "RawSignalCatalogueId",
    "ScheduledCaptureOccurrenceV1",
    "assessment_occurrence_id",
    "capture_occurrence_id",
    "concept_id",
    "contract_id",
    "create_owner",
    "delivery_artifact_ref",
    "eligibility_policy_ref",
    "ingestion_sequence_scope",
    "observation_occurrence_id",
    "provider_id",
    "scope_policy_id",
    "scope_policy_ref",
]
