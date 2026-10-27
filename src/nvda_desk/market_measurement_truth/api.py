"""Exact controlled neutral-measurement public contract under accepted SQLite version 3."""

from __future__ import annotations

import re
import types
from collections.abc import Callable, Sequence
from dataclasses import dataclass, fields, is_dataclass
from datetime import date, datetime, timedelta
from decimal import Decimal
from math import gcd
from pathlib import Path
from typing import Protocol, get_args, get_origin, get_type_hints

from nvda_desk.raw_signal_occurrence_truth import api as raw_api


def _matches(value: object, hint: object) -> bool:
    origin = get_origin(hint)
    args = get_args(hint)
    if origin is types.UnionType:
        return any(_matches(value, item) for item in args)
    if origin is tuple:
        if type(value) is not tuple:
            return False
        if len(args) == 2 and args[1] is Ellipsis:
            return all(_matches(item, args[0]) for item in value)
        return len(value) == len(args) and all(
            _matches(v, h) for v, h in zip(value, args, strict=True)
        )
    return type(value) is hint


def _utc(value: datetime) -> None:
    if type(value) is not datetime:
        raise TypeError("a datetime is required")
    if value.tzinfo is None or value.utcoffset() != timedelta(0):
        raise ValueError("a UTC-aware instant is required")


class _Validated:
    __slots__ = ()

    def __post_init__(self) -> None:
        hints = get_type_hints(type(self))
        if not is_dataclass(self):
            raise TypeError("validation requires a declared record")
        for field in fields(self):
            value = getattr(self, field.name)
            if not _matches(value, hints[field.name]):
                raise TypeError(f"{field.name} has the wrong constructor type")
            if type(value) is str and not value:
                raise ValueError(f"{field.name} must be nonempty")
            if type(value) is datetime and not (
                field.name == "result" and isinstance(self, TemporalLocalOccurrenceV1)
            ):
                _utc(value)
            if type(value) is timedelta and value < timedelta(0):
                raise ValueError("duration must be nonnegative")
            if type(value) is Decimal and not value.is_finite():
                raise ValueError("finite Decimal required by the controlled calculation contract")
            if field.name in {"version", "history_page_size", "history_page_limit"} and value <= 0:
                raise ValueError("version/page bound must be positive")
            if type(value) is tuple and any(item in value[:i] for i, item in enumerate(value)):
                raise ValueError(f"{field.name} members must be distinct")
            if type(value) is tuple and any(type(item) is str and not item for item in value):
                raise ValueError(f"{field.name} identities must be nonempty")
            if field.name in {"raw_dependencies", "derived_dependencies"}:
                prefix, maximum = ("R", 323) if field.name == "raw_dependencies" else ("D", 209)
                if any(
                    not re.fullmatch(prefix + r"[0-9]{3}", item)
                    or not 1 <= int(item[1:]) <= maximum
                    for item in value
                ):
                    raise ValueError("dependency identities must use the admitted canonical range")
            if field.name == "derived_signal_id" and not re.fullmatch(r"D[0-9]{3}", value):
                raise ValueError("canonical D identity required")
            if field.name == "derived_signal_id" and not 1 <= int(value[1:]) <= 209:
                raise ValueError("D identity outside the admitted range")
            if field.name == "raw_signal_id" and (
                not re.fullmatch(r"R[0-9]{3}", value) or not 1 <= int(value[1:]) <= 323
            ):
                raise ValueError("canonical R identity required")
            if field.name in {
                "sha256",
                "implementation_brief_sha256",
                "definition_content_sha256",
            } and not re.fullmatch(r"[0-9a-f]{64}", value):
                raise ValueError("lowercase SHA256 required")
        if isinstance(self, OwnerAdmissionV1) and not re.fullmatch(
            r"M(?:[0-9]{2}|[1-9][0-9]{2,})", self.object_id
        ):
            raise ValueError("canonical module identity required")
        if isinstance(self, (SQLiteStorageV1, SQLiteReadStorageV1)):
            path = self.database_path
            if (
                not Path(path).is_absolute()
                or path.startswith("file:")
                or "?" in path
                or "\x00" in path
            ):
                raise ValueError("an absolute local regular-file path is required")
        if isinstance(self, RawInputLineageV1):
            p = self.projection
            if (
                self.raw_signal_id != p.raw_signal_catalogue_id.value
                or type(p.observation_occurrence_id)
                is not type(raw_api.observation_occurrence_id("id"))
                or self.observation_occurrence_id != p.observation_occurrence_id.value
                or self.projection_mapping_ref.context_id != p.projection_mapping_id
                or self.projection_mapping_ref.version != p.projection_mapping_version
            ):
                raise ValueError("lineage must preserve the exact public projection identities")


class PersistenceFailureV1(RuntimeError):
    def __init__(self, message: str, *, outcome_uncertain: bool = False) -> None:
        super().__init__(message)
        self.outcome_uncertain = outcome_uncertain


@dataclass(frozen=True, slots=True)
class VersionRefV1(_Validated):
    context_id: str
    version: int


@dataclass(frozen=True, slots=True)
class AuthorityArtifactRefV1(_Validated):
    path: str
    sha256: str


@dataclass(frozen=True, slots=True)
class OwnerAdmissionV1(_Validated):
    object_id: str
    implementation_brief_sha256: str


@dataclass(frozen=True, slots=True)
class CalculationDefinitionV1(_Validated):
    derived_signal_id: str
    calculation_definition_version: str
    kernel_id: str
    equation: str
    raw_dependencies: tuple[str, ...]
    derived_dependencies: tuple[str, ...]
    parameter_profile: str
    units: str
    result_shape: str
    authority_refs: tuple[AuthorityArtifactRefV1, ...]


@dataclass(frozen=True, slots=True)
class CalculationParameterSetV1(_Validated):
    context_id: str
    version: int
    profile: str
    subject_instrument: str
    members: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class InputSelectionPolicyVersionV1(_Validated):
    context_id: str
    version: int
    join_keys: tuple[str, ...]
    maximum_staleness: timedelta
    maximum_skew: timedelta
    temporal_basis_permissions: tuple[str, ...]
    basket_membership: tuple[str, ...]
    source_provider: str
    source_variant: str
    ingestion_sequence_scope: str
    history_page_size: int
    history_page_limit: int


@dataclass(frozen=True, slots=True)
class UnitConventionVersionV1(_Validated):
    context_id: str
    version: int
    native_units: str
    canonical_units: str
    scale: Decimal
    offset: Decimal


@dataclass(frozen=True, slots=True)
class RawInputBindingV1(_Validated):
    raw_signal_id: str
    projection_mapping_ref: VersionRefV1
    unit_convention_ref: VersionRefV1
    subject_instrument: str


@dataclass(frozen=True, slots=True)
class CalculationRequestV1(_Validated):
    derived_signal_id: str
    subject_instrument: str
    as_of_utc: datetime
    knowledge_cutoff_utc: datetime
    calculation_definition_version: str
    parameter_set_ref: VersionRefV1
    input_selection_policy_ref: VersionRefV1
    context_refs: tuple[VersionRefV1, ...]
    raw_input_bindings: tuple[RawInputBindingV1, ...]


@dataclass(frozen=True, slots=True)
class RawInputLineageV1(_Validated):
    raw_signal_id: str
    observation_occurrence_id: str
    projection_mapping_ref: VersionRefV1
    unit_convention_ref: VersionRefV1
    projection: raw_api.ProjectedRawValueV1
    canonical_value: Decimal
    event_time_utc: datetime


@dataclass(frozen=True, slots=True)
class DerivedSignalOccurrenceV1(_Validated):
    owner_object_id: str
    owner_namespace: str
    implementation_brief_sha256: str
    derived_signal_id: str
    derived_occurrence_id: str
    calculation_definition_version: str
    definition_content_sha256: str
    parameter_context_refs: tuple[VersionRefV1, ...]
    subject_instrument: str
    universe: tuple[str, ...] | None
    effective_as_of_utc: datetime
    window: str | None
    knowledge_cutoff_utc: datetime
    calculated_at_utc: datetime
    result: Decimal
    units: str
    result_shape: str
    raw_input_lineage: tuple[RawInputLineageV1, ...]
    predecessor_occurrence_ids: tuple[str, ...]
    convention_refs: tuple[VersionRefV1, ...]
    supersedes_derived_occurrence_id: str | None


@dataclass(frozen=True, slots=True)
class MemoryStorageV1(_Validated):
    pass


@dataclass(frozen=True, slots=True)
class SQLiteStorageV1(_Validated):
    database_path: str
    create: bool


@dataclass(frozen=True, slots=True)
class SQLiteReadStorageV1(_Validated):
    database_path: str


class RawProjectionReaderV1(Protocol):
    def list_projected_raw_history(
        self,
        raw_signal_catalogue_id: raw_api.RawSignalCatalogueId,
        *,
        mappings: Sequence[raw_api.RawSignalProjectionMappingV1],
        subject_instrument: str | None,
        received_at_or_before_utc: datetime | None,
        event_at_or_before_utc: datetime | None = None,
        limit: int,
        cursor: str | None,
    ) -> raw_api.ProjectedRawHistoryPageV1: ...


class MeasurementReadsV1(Protocol):
    def get_derived_occurrence(
        self,
        derived_occurrence_id: str,
    ) -> DerivedSignalOccurrenceV1 | None: ...
    def list_derived_history(
        self,
        *,
        derived_signal_id: str,
        subject_instrument: str,
        effective_at_or_before_utc: datetime,
        knowledge_at_or_before_utc: datetime,
        limit: int,
    ) -> tuple[DerivedSignalOccurrenceV1, ...]: ...
    def get_calculation_definition(
        self,
        *,
        derived_signal_id: str,
        calculation_definition_version: str,
    ) -> CalculationDefinitionV1 | None: ...
    def get_parameter_set(
        self,
        ref: VersionRefV1,
    ) -> CalculationParameterSetV1 | None: ...
    def get_input_selection_policy(
        self,
        ref: VersionRefV1,
    ) -> InputSelectionPolicyVersionV1 | None: ...
    def get_unit_convention(
        self,
        ref: VersionRefV1,
    ) -> UnitConventionVersionV1 | None: ...
    def get_projection_mapping(
        self,
        ref: VersionRefV1,
    ) -> raw_api.RawSignalProjectionMappingV1 | None: ...


class MeasurementOwnerV1(Protocol):
    @property
    def reads(self) -> MeasurementReadsV1: ...

    def materialise(
        self,
        request: CalculationRequestV1,
    ) -> DerivedSignalOccurrenceV1 | None: ...


def create_owner(
    *,
    admission: OwnerAdmissionV1,
    raw_projection_reader: RawProjectionReaderV1,
    definitions: tuple[CalculationDefinitionV1, ...],
    parameter_sets: tuple[CalculationParameterSetV1, ...],
    input_selection_policies: tuple[InputSelectionPolicyVersionV1, ...],
    unit_conventions: tuple[UnitConventionVersionV1, ...],
    raw_projection_mappings: tuple[raw_api.RawSignalProjectionMappingV1, ...],
    storage: MemoryStorageV1 | SQLiteStorageV1,
    utc_now: Callable[[], datetime],
) -> MeasurementOwnerV1:
    from ._catalogue import build_owner

    return build_owner(
        admission=admission,
        raw_projection_reader=raw_projection_reader,
        definitions=definitions,
        parameter_sets=parameter_sets,
        input_selection_policies=input_selection_policies,
        unit_conventions=unit_conventions,
        raw_projection_mappings=raw_projection_mappings,
        storage=storage,
        utc_now=utc_now,
    )


def create_reader(
    *,
    admission: OwnerAdmissionV1,
    storage: SQLiteReadStorageV1,
) -> MeasurementReadsV1:
    from ._catalogue import build_reader

    return build_reader(admission=admission, storage=storage)


@dataclass(frozen=True, slots=True)
class ExactRatioV1(_Validated):
    numerator: int
    denominator: int

    def __post_init__(self) -> None:
        _Validated.__post_init__(self)
        if (
            self.denominator <= 0
            or gcd(abs(self.numerator), self.denominator) != 1
            or (self.numerator == 0 and self.denominator != 1)
        ):
            raise ValueError("canonical reduced ratio with positive denominator required")


@dataclass(frozen=True, slots=True)
class PredecessorEvidenceV1(_Validated):
    occurrence: DerivedSignalOccurrenceV1
    definition: CalculationDefinitionV1
    parameter_set: CalculationParameterSetV1
    input_selection_policy: InputSelectionPolicyVersionV1
    unit_conventions: tuple[UnitConventionVersionV1, ...]
    projection_mappings: tuple[raw_api.RawSignalProjectionMappingV1, ...]


@dataclass(frozen=True, slots=True)
class RatioCalculationRequestV1(_Validated):
    derived_signal_id: str
    subject_instrument: str
    as_of_utc: datetime
    knowledge_cutoff_utc: datetime
    calculation_definition_version: str
    parameter_set_ref: VersionRefV1
    predecessor_occurrence_ids: tuple[str, ...]

    def __post_init__(self) -> None:
        _Validated.__post_init__(self)
        if len(self.predecessor_occurrence_ids) != 2:
            raise ValueError("exactly two explicit predecessor identities required")


@dataclass(frozen=True, slots=True)
class RatioOccurrenceV1(_Validated):
    owner_object_id: str
    owner_namespace: str
    implementation_brief_sha256: str
    derived_signal_id: str
    derived_occurrence_id: str
    calculation_definition_version: str
    definition_content_sha256: str
    parameter_context_refs: tuple[VersionRefV1, ...]
    subject_instrument: str
    universe: tuple[str, ...] | None
    effective_as_of_utc: datetime
    window: str | None
    knowledge_cutoff_utc: datetime
    calculated_at_utc: datetime
    result: ExactRatioV1
    units: str
    result_shape: str
    raw_input_lineage: tuple[RawInputLineageV1, ...]
    predecessor_occurrence_ids: tuple[str, ...]
    convention_refs: tuple[VersionRefV1, ...]
    supersedes_derived_occurrence_id: str | None
    predecessor_evidence: tuple[PredecessorEvidenceV1, ...]

    def __post_init__(self) -> None:
        _Validated.__post_init__(self)
        if (
            self.raw_input_lineage
            or self.convention_refs
            or self.universe is not None
            or self.window is not None
            or self.supersedes_derived_occurrence_id is not None
            or len(self.parameter_context_refs) != 1
            or len(self.predecessor_evidence) != 2
            or self.predecessor_occurrence_ids
            != tuple(item.occurrence.derived_occurrence_id for item in self.predecessor_evidence)
            or self.units != "percent"
            or self.result_shape != "scalar_exact_ratio"
        ):
            raise ValueError("complete exact-ratio metadata and ordered predecessor pair required")


class MeasurementRatioReadsV1(Protocol):
    def get_derived_occurrence(self, derived_occurrence_id: str) -> RatioOccurrenceV1 | None: ...
    def list_derived_history(
        self,
        *,
        derived_signal_id: str,
        subject_instrument: str,
        effective_at_or_before_utc: datetime,
        knowledge_at_or_before_utc: datetime,
        limit: int,
    ) -> tuple[RatioOccurrenceV1, ...]: ...
    def get_calculation_definition(
        self,
        *,
        derived_signal_id: str,
        calculation_definition_version: str,
    ) -> CalculationDefinitionV1 | None: ...
    def get_parameter_set(self, ref: VersionRefV1) -> CalculationParameterSetV1 | None: ...


class MeasurementRatioOwnerV1(Protocol):
    @property
    def reads(self) -> MeasurementRatioReadsV1: ...

    def materialise(self, request: RatioCalculationRequestV1) -> RatioOccurrenceV1 | None: ...


def create_ratio_owner(
    *,
    admission: OwnerAdmissionV1,
    predecessor_reader: MeasurementReadsV1,
    definitions: tuple[CalculationDefinitionV1, ...],
    parameter_sets: tuple[CalculationParameterSetV1, ...],
    storage: MemoryStorageV1 | SQLiteStorageV1,
    utc_now: Callable[[], datetime],
) -> MeasurementRatioOwnerV1:
    from ._rational import build_owner

    return build_owner(
        admission=admission,
        predecessor_reader=predecessor_reader,
        definitions=definitions,
        parameter_sets=parameter_sets,
        storage=storage,
        utc_now=utc_now,
    )


def create_ratio_reader(
    *,
    admission: OwnerAdmissionV1,
    storage: SQLiteReadStorageV1,
) -> MeasurementRatioReadsV1:
    from ._rational import build_reader

    return build_reader(admission=admission, storage=storage)


__all__ = [
    "AuthorityArtifactRefV1",
    "CalculationDefinitionV1",
    "CalculationParameterSetV1",
    "CalculationRequestV1",
    "DerivedSignalOccurrenceV1",
    "ExactRatioV1",
    "InputSelectionPolicyVersionV1",
    "MeasurementOwnerV1",
    "MeasurementRatioOwnerV1",
    "MeasurementRatioReadsV1",
    "MeasurementReadsV1",
    "MemoryStorageV1",
    "OwnerAdmissionV1",
    "PersistenceFailureV1",
    "PredecessorEvidenceV1",
    "RatioCalculationRequestV1",
    "RatioOccurrenceV1",
    "RawInputBindingV1",
    "RawInputLineageV1",
    "RawProjectionReaderV1",
    "SQLiteReadStorageV1",
    "SQLiteStorageV1",
    "UnitConventionVersionV1",
    "VersionRefV1",
    "create_owner",
    "create_ratio_owner",
    "create_ratio_reader",
    "create_reader",
]


@dataclass(frozen=True, slots=True)
class RawRatioOccurrenceV1(_Validated):
    owner_object_id: str
    owner_namespace: str
    implementation_brief_sha256: str
    derived_signal_id: str
    derived_occurrence_id: str
    calculation_definition_version: str
    definition_content_sha256: str
    parameter_context_refs: tuple[VersionRefV1, ...]
    subject_instrument: str
    universe: tuple[str, ...] | None
    effective_as_of_utc: datetime
    window: str | None
    knowledge_cutoff_utc: datetime
    calculated_at_utc: datetime
    result: ExactRatioV1
    units: str
    result_shape: str
    raw_input_lineage: tuple[RawInputLineageV1, ...]
    predecessor_occurrence_ids: tuple[str, ...]
    convention_refs: tuple[VersionRefV1, ...]
    supersedes_derived_occurrence_id: str | None

    def __post_init__(self) -> None:
        _Validated.__post_init__(self)
        units = {item.unit_convention_ref for item in self.raw_input_lineage}
        if (
            tuple(item.raw_signal_id for item in self.raw_input_lineage) != ("R033", "R036")
            or self.predecessor_occurrence_ids
            or len(self.parameter_context_refs) != 2
            or self.convention_refs
            != tuple(sorted(units, key=lambda ref: (ref.context_id, ref.version)))
            or self.universe is not None
            or self.window is not None
            or self.supersedes_derived_occurrence_id is not None
            or self.units != "-1 to 1"
            or self.result_shape != "scalar_exact_ratio"
        ):
            raise ValueError("complete ordered direct-raw ratio metadata required")


class MeasurementRawRatioReadsV1(Protocol):
    def get_derived_occurrence(self, derived_occurrence_id: str) -> RawRatioOccurrenceV1 | None: ...
    def list_derived_history(
        self,
        *,
        derived_signal_id: str,
        subject_instrument: str,
        effective_at_or_before_utc: datetime,
        knowledge_at_or_before_utc: datetime,
        limit: int,
    ) -> tuple[RawRatioOccurrenceV1, ...]: ...
    def get_calculation_definition(
        self,
        *,
        derived_signal_id: str,
        calculation_definition_version: str,
    ) -> CalculationDefinitionV1 | None: ...
    def get_parameter_set(self, ref: VersionRefV1) -> CalculationParameterSetV1 | None: ...
    def get_input_selection_policy(
        self, ref: VersionRefV1
    ) -> InputSelectionPolicyVersionV1 | None: ...
    def get_unit_convention(self, ref: VersionRefV1) -> UnitConventionVersionV1 | None: ...
    def get_projection_mapping(
        self, ref: VersionRefV1
    ) -> raw_api.RawSignalProjectionMappingV1 | None: ...


class MeasurementRawRatioOwnerV1(Protocol):
    @property
    def reads(self) -> MeasurementRawRatioReadsV1: ...

    def materialise(self, request: CalculationRequestV1) -> RawRatioOccurrenceV1 | None: ...


def create_raw_ratio_owner(
    *,
    admission: OwnerAdmissionV1,
    raw_projection_reader: RawProjectionReaderV1,
    definitions: tuple[CalculationDefinitionV1, ...],
    parameter_sets: tuple[CalculationParameterSetV1, ...],
    input_selection_policies: tuple[InputSelectionPolicyVersionV1, ...],
    unit_conventions: tuple[UnitConventionVersionV1, ...],
    raw_projection_mappings: tuple[raw_api.RawSignalProjectionMappingV1, ...],
    storage: MemoryStorageV1 | SQLiteStorageV1,
    utc_now: Callable[[], datetime],
) -> MeasurementRawRatioOwnerV1:
    from ._raw_rational import build_owner

    return build_owner(
        admission=admission,
        raw_projection_reader=raw_projection_reader,
        definitions=definitions,
        parameter_sets=parameter_sets,
        input_selection_policies=input_selection_policies,
        unit_conventions=unit_conventions,
        raw_projection_mappings=raw_projection_mappings,
        storage=storage,
        utc_now=utc_now,
    )


def create_raw_ratio_reader(
    *,
    admission: OwnerAdmissionV1,
    storage: SQLiteReadStorageV1,
) -> MeasurementRawRatioReadsV1:
    from ._raw_rational import build_reader

    return build_reader(admission=admission, storage=storage)


__all__ += [
    "MeasurementRawRatioOwnerV1",
    "MeasurementRawRatioReadsV1",
    "RawRatioOccurrenceV1",
    "create_raw_ratio_owner",
    "create_raw_ratio_reader",
]


@dataclass(frozen=True, slots=True)
class TradeDirectionRequestV1(_Validated):
    calculation: CalculationRequestV1
    midpoint_occurrence_id: str


@dataclass(frozen=True, slots=True)
class TradeDirectionOccurrenceV1(_Validated):
    owner_object_id: str
    owner_namespace: str
    implementation_brief_sha256: str
    derived_signal_id: str
    derived_occurrence_id: str
    request: TradeDirectionRequestV1
    definition: CalculationDefinitionV1
    parameter_set: CalculationParameterSetV1
    input_selection_policy: InputSelectionPolicyVersionV1
    unit_conventions: tuple[UnitConventionVersionV1, ...]
    projection_mappings: tuple[raw_api.RawSignalProjectionMappingV1, ...]
    raw_input_lineage: tuple[RawInputLineageV1, ...]
    predecessor: PredecessorEvidenceV1
    result: int
    units: str
    result_shape: str
    effective_as_of_utc: datetime
    knowledge_cutoff_utc: datetime
    calculated_at_utc: datetime

    def __post_init__(self) -> None:
        _Validated.__post_init__(self)
        if self.result not in (-1, 0, 1):
            raise ValueError("trade direction must be -1, 0 or +1")


class MeasurementTradeDirectionReadsV1(Protocol):
    def get_derived_occurrence(
        self, derived_occurrence_id: str
    ) -> TradeDirectionOccurrenceV1 | None: ...
    def list_derived_history(
        self,
        *,
        derived_signal_id: str,
        subject_instrument: str,
        effective_at_or_before_utc: datetime,
        knowledge_at_or_before_utc: datetime,
        limit: int,
    ) -> tuple[TradeDirectionOccurrenceV1, ...]: ...


class MeasurementTradeDirectionOwnerV1(Protocol):
    @property
    def reads(self) -> MeasurementTradeDirectionReadsV1: ...
    def materialise(
        self, request: TradeDirectionRequestV1
    ) -> TradeDirectionOccurrenceV1 | None: ...


def create_trade_direction_owner(
    *,
    admission: OwnerAdmissionV1,
    raw_projection_reader: RawProjectionReaderV1,
    predecessor_reader: MeasurementReadsV1,
    storage: MemoryStorageV1 | SQLiteStorageV1,
    utc_now: Callable[[], datetime],
) -> MeasurementTradeDirectionOwnerV1:
    from ._trade_direction import build_owner

    return build_owner(
        admission=admission,
        raw_projection_reader=raw_projection_reader,
        predecessor_reader=predecessor_reader,
        storage=storage,
        utc_now=utc_now,
    )


def create_trade_direction_reader(
    *, admission: OwnerAdmissionV1, storage: SQLiteReadStorageV1
) -> MeasurementTradeDirectionReadsV1:
    from ._trade_direction import build_reader

    return build_reader(admission=admission, storage=storage)


__all__ += [
    "MeasurementTradeDirectionOwnerV1",
    "MeasurementTradeDirectionReadsV1",
    "TradeDirectionOccurrenceV1",
    "TradeDirectionRequestV1",
    "create_trade_direction_owner",
    "create_trade_direction_reader",
]


@dataclass(frozen=True, slots=True)
class MeasurementComparisonV1(_Validated):
    price_difference: ExactRatioV1
    bps_difference: ExactRatioV1


@dataclass(frozen=True, slots=True)
class ReturnAccelerationV1(_Validated):
    q1: ExactRatioV1
    q5: ExactRatioV1
    q30: ExactRatioV1
    accel_1v5: ExactRatioV1
    accel_5v30: ExactRatioV1


@dataclass(frozen=True, slots=True)
class VwapRateV1(_Validated):
    price_per_minute: ExactRatioV1
    percent_per_minute: ExactRatioV1


@dataclass(frozen=True, slots=True)
class VwapDeviationV1(_Validated):
    price_difference: ExactRatioV1
    percent_difference: ExactRatioV1


@dataclass(frozen=True, slots=True)
class IndexChangeV1(_Validated):
    point_change: ExactRatioV1
    percent_change: ExactRatioV1


@dataclass(frozen=True, slots=True)
class TermPairV1(_Validated):
    point_difference: ExactRatioV1
    ratio: ExactRatioV1


@dataclass(frozen=True, slots=True)
class WindowContextV1(_Validated):
    ref: VersionRefV1
    session_start_utc: datetime
    session_end_utc: datetime
    history_complete_from_utc: datetime


@dataclass(frozen=True, slots=True)
class SessionFrameV1(_Validated):
    ref: VersionRefV1
    session_type: str
    start_utc: datetime
    end_utc: datetime


@dataclass(frozen=True, slots=True)
class BaselineWindowContextV1(_Validated):
    ref: VersionRefV1
    session_start_utc: datetime
    session_end_utc: datetime
    history_complete_from_utc: datetime
    sessions: tuple[SessionFrameV1, ...]
    prior_session_count: int
    bucket_offset_seconds: int


@dataclass(frozen=True, slots=True)
class TradingReturnIntervalV1(_Validated):
    start_utc: datetime
    end_utc: datetime
    trading_year_fraction: ExactRatioV1


@dataclass(frozen=True, slots=True)
class RealisedRiskWindowContextV1(_Validated):
    ref: VersionRefV1
    session_start_utc: datetime
    session_end_utc: datetime
    history_complete_from_utc: datetime
    sessions: tuple[SessionFrameV1, ...]
    sample_instants_utc: tuple[datetime, ...]
    intervals: tuple[TradingReturnIntervalV1, ...]


@dataclass(frozen=True, slots=True)
class WindowCalculationRequestV1(_Validated):
    calculation: CalculationRequestV1
    context: WindowContextV1 | BaselineWindowContextV1 | RealisedRiskWindowContextV1
    predecessor_occurrence_ids: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class CorrelationMatrixV1:
    members: tuple[str, ...]
    rows: tuple[tuple[Decimal, ...], ...]

    def __post_init__(self) -> None:
        if (
            type(self.members) is not tuple
            or len(self.members) < 2
            or any(type(member) is not str or not member for member in self.members)
            or len(set(self.members)) != len(self.members)
            or type(self.rows) is not tuple
            or len(self.rows) != len(self.members)
        ):
            raise ValueError("exact ordered correlation member set required")
        for i, row in enumerate(self.rows):
            if type(row) is not tuple or len(row) != len(self.members):
                raise ValueError("square correlation matrix required")
            for j, entry in enumerate(row):
                if (
                    type(entry) is not Decimal
                    or not entry.is_finite()
                    or not Decimal("-1") <= entry <= Decimal("1")
                    or (i == j and entry != 1)
                ):
                    raise ValueError("finite bounded correlation entry required")
        if any(self.rows[i][j] != self.rows[j][i] for i in range(len(self.rows))
               for j in range(i)):
            raise ValueError("symmetric correlation matrix required")


@dataclass(frozen=True, slots=True)
class OptionRightLineageV1(_Validated):
    raw_signal_id: str
    observation_occurrence_id: str
    projection_mapping_ref: VersionRefV1
    projection_mapping: raw_api.RawSignalProjectionMappingV1
    projection: raw_api.ProjectedRawValueV1
    native_value: str
    canonical_value: str
    units: str
    event_time_utc: datetime

    def __post_init__(self) -> None:
        _Validated.__post_init__(self)
        if (self.raw_signal_id != "R015" or self.units != "option_right"
            or self.native_value not in ("C", "P")
            or self.canonical_value != self.native_value
            or self.projection.native_value != self.native_value
            or self.projection.raw_signal_catalogue_id.value != "R015"
            or self.projection.observation_occurrence_id.value != self.observation_occurrence_id
            or self.projection.projection_mapping_id != self.projection_mapping.mapping_id
            or self.projection_mapping_ref != VersionRefV1(
                self.projection_mapping.mapping_id, self.projection_mapping.version
            )):
            raise ValueError("exact native R015 categorical lineage required")


@dataclass(frozen=True, slots=True)
class OptionSkewV1(_Validated):
    value: ExactRatioV1
    native_right_lineage: tuple[OptionRightLineageV1, ...]

    def __post_init__(self) -> None:
        _Validated.__post_init__(self)
        if len(self.native_right_lineage) != 2:
            raise ValueError("call and put native right lineage required")


@dataclass(frozen=True, slots=True)
class OIConcentrationV1(_Validated):
    group_keys: tuple[tuple[str, str], ...]
    shares: tuple[ExactRatioV1, ...]
    hhi: ExactRatioV1

    def __post_init__(self) -> None:
        _Validated.__post_init__(self)
        from fractions import Fraction

        if (not self.group_keys or len(self.group_keys) != len(self.shares)
            or tuple(sorted(self.group_keys)) != self.group_keys
            or len(set(self.group_keys)) != len(self.group_keys)
            or any(len(key) != 2 or any(type(part) is not str or not part for part in key)
                   for key in self.group_keys)):
            raise ValueError("exact ordered strike/expiry groups required")
        fractions = tuple(Fraction(share.numerator, share.denominator)
                          for share in self.shares)
        hhi = Fraction(self.hhi.numerator, self.hhi.denominator)
        if (any(not 0 <= share <= 1 for share in fractions)
            or sum(fractions) != 1 or sum((share * share for share in fractions),
                                          Fraction()) != hhi):
            raise ValueError("shares and HHI must be exact and consistent")


@dataclass(frozen=True, slots=True)
class WindowMeasurementOccurrenceV1(_Validated):
    owner_object_id: str
    owner_namespace: str
    implementation_brief_sha256: str
    derived_signal_id: str
    derived_occurrence_id: str
    request: WindowCalculationRequestV1
    definition: CalculationDefinitionV1
    parameter_set: CalculationParameterSetV1
    input_selection_policy: InputSelectionPolicyVersionV1
    unit_conventions: tuple[UnitConventionVersionV1, ...]
    projection_mappings: tuple[raw_api.RawSignalProjectionMappingV1, ...]
    raw_input_lineage: tuple[RawInputLineageV1, ...]
    predecessors: tuple[TradeDirectionOccurrenceV1 | WindowMeasurementOccurrenceV1, ...]
    window_seconds: int
    result: (
        Decimal
        | CorrelationMatrixV1
        | OptionSkewV1
        | OIConcentrationV1
        | ExactRatioV1
        | IndexChangeV1
        | TermPairV1
        | MeasurementComparisonV1
        | ReturnAccelerationV1
        | VwapDeviationV1
        | VwapRateV1
    )
    units: str
    result_shape: str
    effective_as_of_utc: datetime
    knowledge_cutoff_utc: datetime
    calculated_at_utc: datetime


@dataclass(frozen=True, slots=True)
class BookEventSelectionV1(_Validated):
    ref: VersionRefV1
    provider: str
    variant: str
    generation: str
    history_complete_from_utc: datetime
    maximum_events: int


@dataclass(frozen=True, slots=True)
class BookRawLineageV1(_Validated):
    raw_signal_id: str
    observation_occurrence_id: str
    projection_mapping_ref: VersionRefV1
    unit_convention_ref: VersionRefV1
    projection: raw_api.ProjectedRawValueV1
    canonical_value: int | Decimal
    event_time_utc: datetime

    def __post_init__(self) -> None:
        _Validated.__post_init__(self)
        expected = int if self.raw_signal_id in ("R185", "R187", "R188") else Decimal
        if type(self.canonical_value) is not expected:
            raise TypeError("book native role type mismatch")


@dataclass(frozen=True, slots=True)
class BookRowV1(_Validated):
    side: int
    position: int
    price: Decimal
    size: Decimal


@dataclass(frozen=True, slots=True)
class BookDepthRequestV1(_Validated):
    calculation: CalculationRequestV1
    selection: BookEventSelectionV1
    predecessor_occurrence_id: str
    band: Decimal


@dataclass(frozen=True, slots=True)
class BookDepthOccurrenceV1(_Validated):
    owner_object_id: str
    owner_namespace: str
    implementation_brief_sha256: str
    derived_signal_id: str
    derived_occurrence_id: str
    request: BookDepthRequestV1
    definition: CalculationDefinitionV1
    parameter_set: CalculationParameterSetV1
    unit_conventions: tuple[UnitConventionVersionV1, ...]
    projection_mappings: tuple[raw_api.RawSignalProjectionMappingV1, ...]
    raw_input_lineage: tuple[BookRawLineageV1, ...]
    predecessor: WindowMeasurementOccurrenceV1
    standing_rows: tuple[BookRowV1, ...]
    result: Decimal
    units: str
    result_shape: str
    effective_as_of_utc: datetime
    knowledge_cutoff_utc: datetime
    calculated_at_utc: datetime


@dataclass(frozen=True, slots=True)
class BookSlopePairV1(_Validated):
    bid: ExactRatioV1
    ask: ExactRatioV1


@dataclass(frozen=True, slots=True)
class BookSlopeRequestV1(_Validated):
    calculation: CalculationRequestV1
    selection: BookEventSelectionV1
    predecessor_occurrence_id: str
    depth_levels: int


@dataclass(frozen=True, slots=True)
class BookSlopeOccurrenceV1(_Validated):
    owner_object_id: str
    owner_namespace: str
    implementation_brief_sha256: str
    derived_signal_id: str
    derived_occurrence_id: str
    request: BookSlopeRequestV1
    definition: CalculationDefinitionV1
    parameter_set: CalculationParameterSetV1
    unit_conventions: tuple[UnitConventionVersionV1, ...]
    projection_mappings: tuple[raw_api.RawSignalProjectionMappingV1, ...]
    raw_input_lineage: tuple[BookRawLineageV1, ...]
    predecessor: DerivedSignalOccurrenceV1
    standing_rows: tuple[BookRowV1, ...]
    result: BookSlopePairV1
    units: str
    result_shape: str
    effective_as_of_utc: datetime
    knowledge_cutoff_utc: datetime
    calculated_at_utc: datetime


@dataclass(frozen=True, slots=True)
class BookRateRawLineageV1(_Validated):
    raw_signal_id: str
    observation_occurrence_id: str
    projection_mapping_ref: VersionRefV1
    unit_convention_ref: VersionRefV1
    projection: raw_api.ProjectedRawValueV1
    canonical_value: datetime | int | Decimal
    event_time_utc: datetime

    def __post_init__(self) -> None:
        _Validated.__post_init__(self)
        expected = {
            "R001": datetime, "R185": int, "R187": int, "R188": int, "R190": Decimal,
        }.get(self.raw_signal_id)
        if expected is None or type(self.canonical_value) is not expected:
            raise TypeError("exact receipt-book native role type required")


@dataclass(frozen=True, slots=True)
class BookRatePairV1(_Validated):
    count_per_second: ExactRatioV1
    size_per_second: ExactRatioV1


@dataclass(frozen=True, slots=True)
class BookRateRequestV1(_Validated):
    calculation: CalculationRequestV1
    selection: BookEventSelectionV1
    window_seconds: int
    side: int
    positions: tuple[int, ...]


@dataclass(frozen=True, slots=True)
class BookRateOccurrenceV1(_Validated):
    owner_object_id: str
    owner_namespace: str
    implementation_brief_sha256: str
    derived_signal_id: str
    derived_occurrence_id: str
    request: BookRateRequestV1
    definition: CalculationDefinitionV1
    parameter_set: CalculationParameterSetV1
    selection: BookEventSelectionV1
    unit_conventions: tuple[UnitConventionVersionV1, ...]
    projection_mappings: tuple[raw_api.RawSignalProjectionMappingV1, ...]
    raw_input_lineage: tuple[BookRateRawLineageV1, ...]
    standing_rows: tuple[SmartSizeRowV1, ...]
    selected_event_ids: tuple[str, ...]
    result: BookRatePairV1
    units: str
    result_shape: str
    effective_as_of_utc: datetime
    knowledge_cutoff_utc: datetime
    calculated_at_utc: datetime


@dataclass(frozen=True, slots=True)
class SmartSizeRowV1(_Validated):
    side: int
    position: int
    size: Decimal


@dataclass(frozen=True, slots=True)
class SmartDepthRequestV1(_Validated):
    calculation: CalculationRequestV1
    selection: BookEventSelectionV1
    depth_levels: int


@dataclass(frozen=True, slots=True)
class SmartDepthOccurrenceV1(_Validated):
    owner_object_id: str
    owner_namespace: str
    implementation_brief_sha256: str
    derived_signal_id: str
    derived_occurrence_id: str
    request: SmartDepthRequestV1
    definition: CalculationDefinitionV1
    parameter_set: CalculationParameterSetV1
    unit_conventions: tuple[UnitConventionVersionV1, ...]
    projection_mappings: tuple[raw_api.RawSignalProjectionMappingV1, ...]
    raw_input_lineage: tuple[BookRawLineageV1, ...]
    standing_rows: tuple[SmartSizeRowV1, ...]
    result: Decimal
    units: str
    result_shape: str
    effective_as_of_utc: datetime
    knowledge_cutoff_utc: datetime
    calculated_at_utc: datetime


@dataclass(frozen=True, slots=True)
class SmartDepthPairV1(_Validated):
    bid_levels: int
    ask_levels: int

    def __post_init__(self) -> None:
        _Validated.__post_init__(self)
        if self.bid_levels <= 0 or self.ask_levels <= 0:
            raise ValueError("positive bid and ask depth levels required")


@dataclass(frozen=True, slots=True)
class SmartImbalanceRequestV1(_Validated):
    calculation: CalculationRequestV1
    predecessor_occurrence_ids: tuple[str, str]
    requested_depth_levels: SmartDepthPairV1


@dataclass(frozen=True, slots=True)
class SmartImbalanceOccurrenceV1(_Validated):
    owner_object_id: str
    owner_namespace: str
    implementation_brief_sha256: str
    derived_signal_id: str
    derived_occurrence_id: str
    request: SmartImbalanceRequestV1
    definition: CalculationDefinitionV1
    parameter_set: CalculationParameterSetV1
    predecessors: tuple[SmartDepthOccurrenceV1, SmartDepthOccurrenceV1]
    result: ExactRatioV1
    units: str
    result_shape: str
    effective_as_of_utc: datetime
    knowledge_cutoff_utc: datetime
    calculated_at_utc: datetime


class MeasurementSmartImbalanceReadsV1(Protocol):
    def get_derived_occurrence(self, derived_occurrence_id: str
                               ) -> SmartImbalanceOccurrenceV1 | None: ...
    def list_derived_history(
        self, *, derived_signal_id: str, subject_instrument: str,
        effective_at_or_before_utc: datetime, knowledge_at_or_before_utc: datetime,
        limit: int,
    ) -> tuple[SmartImbalanceOccurrenceV1, ...]: ...


class MeasurementSmartImbalanceOwnerV1(Protocol):
    @property
    def reads(self) -> MeasurementSmartImbalanceReadsV1: ...
    def materialise(self, request: SmartImbalanceRequestV1
                    ) -> SmartImbalanceOccurrenceV1 | None: ...


def create_smart_imbalance_owner(
    *, admission: OwnerAdmissionV1, bid_reader: MeasurementSmartDepthReadsV1,
    ask_reader: MeasurementSmartDepthReadsV1,
    storage: MemoryStorageV1 | SQLiteStorageV1, utc_now: Callable[[], datetime],
) -> MeasurementSmartImbalanceOwnerV1:
    from ._smart_imbalance import build_owner
    return build_owner(admission, bid_reader, ask_reader, storage, utc_now)


def create_smart_imbalance_reader(
    *, admission: OwnerAdmissionV1, storage: SQLiteReadStorageV1,
) -> MeasurementSmartImbalanceReadsV1:
    from ._smart_imbalance import build_reader
    return build_reader(admission, storage)


class MeasurementSmartDepthReadsV1(Protocol):
    def get_derived_occurrence(self, derived_occurrence_id: str
                               ) -> SmartDepthOccurrenceV1 | None: ...
    def list_derived_history(
        self, *, derived_signal_id: str, subject_instrument: str,
        effective_at_or_before_utc: datetime, knowledge_at_or_before_utc: datetime,
        limit: int,
    ) -> tuple[SmartDepthOccurrenceV1, ...]: ...


class MeasurementSmartDepthOwnerV1(Protocol):
    @property
    def reads(self) -> MeasurementSmartDepthReadsV1: ...
    def materialise(self, request: SmartDepthRequestV1) -> SmartDepthOccurrenceV1 | None: ...


def create_smart_depth_owner(
    *, admission: OwnerAdmissionV1, raw_projection_reader: RawProjectionReaderV1,
    storage: MemoryStorageV1 | SQLiteStorageV1, utc_now: Callable[[], datetime],
) -> MeasurementSmartDepthOwnerV1:
    from ._smart_depth import build_owner
    return build_owner(admission, raw_projection_reader, storage, utc_now)


def create_smart_depth_reader(
    *, admission: OwnerAdmissionV1, storage: SQLiteReadStorageV1,
) -> MeasurementSmartDepthReadsV1:
    from ._smart_depth import build_reader
    return build_reader(admission, storage)


def create_smart_ask_owner(
    *, admission: OwnerAdmissionV1, raw_projection_reader: RawProjectionReaderV1,
    storage: MemoryStorageV1 | SQLiteStorageV1, utc_now: Callable[[], datetime],
) -> MeasurementSmartDepthOwnerV1:
    from ._smart_ask import build_owner
    return build_owner(admission, raw_projection_reader, storage, utc_now)


def create_smart_ask_reader(
    *, admission: OwnerAdmissionV1, storage: SQLiteReadStorageV1,
) -> MeasurementSmartDepthReadsV1:
    from ._smart_ask import build_reader
    return build_reader(admission, storage)


class MeasurementBookDepthReadsV1(Protocol):
    def get_derived_occurrence(self, derived_occurrence_id: str
                               ) -> BookDepthOccurrenceV1 | None: ...
    def list_derived_history(
        self, *, derived_signal_id: str, subject_instrument: str,
        effective_at_or_before_utc: datetime, knowledge_at_or_before_utc: datetime,
        limit: int,
    ) -> tuple[BookDepthOccurrenceV1, ...]: ...


class MeasurementBookDepthOwnerV1(Protocol):
    @property
    def reads(self) -> MeasurementBookDepthReadsV1: ...
    def materialise(self, request: BookDepthRequestV1) -> BookDepthOccurrenceV1 | None: ...


def create_book_depth_owner(
    *, admission: OwnerAdmissionV1, raw_projection_reader: RawProjectionReaderV1,
    predecessor_reader: MeasurementWindowReadsV1,
    storage: MemoryStorageV1 | SQLiteStorageV1, utc_now: Callable[[], datetime],
) -> MeasurementBookDepthOwnerV1:
    from ._book_depth import build_owner
    return build_owner(admission, raw_projection_reader, predecessor_reader, storage, utc_now)


def create_book_depth_reader(
    *, admission: OwnerAdmissionV1, storage: SQLiteReadStorageV1,
) -> MeasurementBookDepthReadsV1:
    from ._book_depth import build_reader
    return build_reader(admission, storage)


class MeasurementBookSlopeReadsV1(Protocol):
    def get_derived_occurrence(self, derived_occurrence_id: str
                               ) -> BookSlopeOccurrenceV1 | None: ...
    def list_derived_history(
        self, *, derived_signal_id: str, subject_instrument: str,
        effective_at_or_before_utc: datetime, knowledge_at_or_before_utc: datetime,
        limit: int,
    ) -> tuple[BookSlopeOccurrenceV1, ...]: ...


class MeasurementBookSlopeOwnerV1(Protocol):
    @property
    def reads(self) -> MeasurementBookSlopeReadsV1: ...
    def materialise(self, request: BookSlopeRequestV1) -> BookSlopeOccurrenceV1 | None: ...


def create_book_slope_owner(
    *, admission: OwnerAdmissionV1, raw_projection_reader: RawProjectionReaderV1,
    predecessor_reader: MeasurementReadsV1,
    storage: MemoryStorageV1 | SQLiteStorageV1, utc_now: Callable[[], datetime],
) -> MeasurementBookSlopeOwnerV1:
    from ._book_slope import build_owner
    return build_owner(admission, raw_projection_reader, predecessor_reader, storage, utc_now)


def create_book_slope_reader(
    *, admission: OwnerAdmissionV1, storage: SQLiteReadStorageV1,
) -> MeasurementBookSlopeReadsV1:
    from ._book_slope import build_reader
    return build_reader(admission, storage)


class MeasurementBookRateReadsV1(Protocol):
    def get_derived_occurrence(self, derived_occurrence_id: str
                               ) -> BookRateOccurrenceV1 | None: ...
    def list_derived_history(
        self, *, derived_signal_id: str, subject_instrument: str,
        effective_at_or_before_utc: datetime, knowledge_at_or_before_utc: datetime,
        limit: int,
    ) -> tuple[BookRateOccurrenceV1, ...]: ...


class MeasurementBookRateOwnerV1(Protocol):
    @property
    def reads(self) -> MeasurementBookRateReadsV1: ...
    def materialise(self, request: BookRateRequestV1) -> BookRateOccurrenceV1 | None: ...


def create_book_insert_rate_owner(
    *, admission: OwnerAdmissionV1, raw_projection_reader: RawProjectionReaderV1,
    storage: MemoryStorageV1 | SQLiteStorageV1, utc_now: Callable[[], datetime],
) -> MeasurementBookRateOwnerV1:
    from ._book_insert_rate import build_owner
    return build_owner(admission, raw_projection_reader, storage, utc_now)


def create_book_insert_rate_reader(
    *, admission: OwnerAdmissionV1, storage: SQLiteReadStorageV1,
) -> MeasurementBookRateReadsV1:
    from ._book_insert_rate import build_reader
    return build_reader(admission, storage)


def create_microprice_owner(
    *, admission: OwnerAdmissionV1, raw_projection_reader: RawProjectionReaderV1,
    storage: MemoryStorageV1 | SQLiteStorageV1, utc_now: Callable[[], datetime],
) -> MeasurementWindowOwnerV1:
    from ._microprice import build_owner
    return build_owner(admission, raw_projection_reader, storage, utc_now)


def create_microprice_reader(
    *, admission: OwnerAdmissionV1, storage: SQLiteReadStorageV1,
) -> MeasurementWindowReadsV1:
    from ._microprice import build_reader
    return build_reader(admission, storage)


@dataclass(frozen=True, slots=True)
class TemporalRawLineageV1(_Validated):
    raw_signal_id: str
    observation_occurrence_id: str
    projection_mapping_ref: VersionRefV1
    unit_convention_ref: VersionRefV1
    projection: raw_api.ProjectedRawValueV1
    canonical_value: str
    event_time_utc: datetime


@dataclass(frozen=True, slots=True)
class TemporalOccurrenceV1(_Validated):
    owner_object_id: str
    owner_namespace: str
    implementation_brief_sha256: str
    derived_signal_id: str
    derived_occurrence_id: str
    request: CalculationRequestV1
    definition: CalculationDefinitionV1
    parameter_set: CalculationParameterSetV1
    input_selection_policy: InputSelectionPolicyVersionV1
    unit_conventions: tuple[UnitConventionVersionV1, ...]
    projection_mappings: tuple[raw_api.RawSignalProjectionMappingV1, ...]
    raw_input_lineage: tuple[TemporalRawLineageV1, ...]
    predecessor_occurrence_ids: tuple[str, ...]
    result: datetime
    units: str
    result_shape: str
    effective_as_of_utc: datetime
    knowledge_cutoff_utc: datetime
    calculated_at_utc: datetime


@dataclass(frozen=True, slots=True)
class TemporalAgeRequestV1(_Validated):
    calculation: CalculationRequestV1
    predecessor_occurrence_ids: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class TemporalAgeV1(_Validated):
    basis: str
    age_seconds: Decimal

    def __post_init__(self) -> None:
        _Validated.__post_init__(self)
        if self.basis not in ("source_event", "collector_receipt") or self.age_seconds < 0:
            raise ValueError("exact nonnegative source/receipt age required")


@dataclass(frozen=True, slots=True)
class TemporalAgeRawLineageV1(_Validated):
    raw_signal_id: str
    observation_occurrence_id: str
    projection_mapping_ref: VersionRefV1
    unit_convention_ref: VersionRefV1
    projection: raw_api.ProjectedRawValueV1
    canonical_value: str
    selected_time_utc: datetime
    time_basis: str


@dataclass(frozen=True, slots=True)
class TemporalAgeOccurrenceV1(_Validated):
    owner_object_id: str
    owner_namespace: str
    implementation_brief_sha256: str
    derived_signal_id: str
    derived_occurrence_id: str
    request: TemporalAgeRequestV1
    definition: CalculationDefinitionV1
    parameter_set: CalculationParameterSetV1
    input_selection_policy: InputSelectionPolicyVersionV1
    unit_conventions: tuple[UnitConventionVersionV1, ...]
    projection_mappings: tuple[raw_api.RawSignalProjectionMappingV1, ...]
    raw_input_lineage: tuple[TemporalAgeRawLineageV1, ...]
    predecessors: tuple[TemporalOccurrenceV1, ...]
    result: TemporalAgeV1
    units: str
    result_shape: str
    effective_as_of_utc: datetime
    knowledge_cutoff_utc: datetime
    calculated_at_utc: datetime


@dataclass(frozen=True, slots=True)
class TemporalLocalRequestV1(_Validated):
    calculation: CalculationRequestV1
    predecessor_occurrence_id: str


@dataclass(frozen=True, slots=True)
class TemporalLocalRawLineageV1(_Validated):
    raw_signal_id: str
    observation_occurrence_id: str
    projection_mapping_ref: VersionRefV1
    unit_convention_ref: VersionRefV1
    projection: raw_api.ProjectedRawValueV1
    canonical_value: str
    event_time_utc: datetime


@dataclass(frozen=True, slots=True)
class TemporalLocalOccurrenceV1(_Validated):
    owner_object_id: str
    owner_namespace: str
    implementation_brief_sha256: str
    derived_signal_id: str
    derived_occurrence_id: str
    request: TemporalLocalRequestV1
    definition: CalculationDefinitionV1
    parameter_set: CalculationParameterSetV1
    input_selection_policy: InputSelectionPolicyVersionV1
    unit_convention: UnitConventionVersionV1
    projection_mapping: raw_api.RawSignalProjectionMappingV1
    raw_input_lineage: TemporalLocalRawLineageV1
    predecessor: TemporalOccurrenceV1
    zone_policy_ref: VersionRefV1
    result: datetime
    units: str
    result_shape: str
    effective_as_of_utc: datetime
    knowledge_cutoff_utc: datetime
    calculated_at_utc: datetime

    def __post_init__(self) -> None:
        _Validated.__post_init__(self)
        if self.result.tzinfo is None or self.result.utcoffset() is None:
            raise ValueError("aware local datetime required")


@dataclass(frozen=True, slots=True)
class CalendarIntervalV1(_Validated):
    start_utc: datetime
    end_utc: datetime
    session_id: str
    trading_date: date | None

    def __post_init__(self) -> None:
        _Validated.__post_init__(self)
        if self.end_utc <= self.start_utc:
            raise ValueError("calendar interval must be positive")
        if (self.session_id == "closed") != (self.trading_date is None):
            raise ValueError("closed interval cannot assign a trading date")


@dataclass(frozen=True, slots=True)
class CalendarPolicyV1(_Validated):
    ref: VersionRefV1
    iana_zone: str
    coverage_start_utc: datetime
    coverage_end_utc: datetime
    intervals: tuple[CalendarIntervalV1, ...]

    def __post_init__(self) -> None:
        _Validated.__post_init__(self)
        if (not self.intervals or self.coverage_end_utc <= self.coverage_start_utc
            or self.intervals[0].start_utc != self.coverage_start_utc
            or self.intervals[-1].end_utc != self.coverage_end_utc
            or any(a.end_utc != b.start_utc for a, b in zip(
                self.intervals, self.intervals[1:], strict=False,
            ))):
            raise ValueError("calendar coverage must be ordered, complete and nonoverlapping")


@dataclass(frozen=True, slots=True)
class TemporalDateRequestV1(_Validated):
    calculation: CalculationRequestV1
    predecessor_occurrence_id: str
    calendar_policy: CalendarPolicyV1


@dataclass(frozen=True, slots=True)
class TemporalCalendarRawLineageV1(_Validated):
    raw_signal_id: str
    observation_occurrence_id: str
    projection_mapping_ref: VersionRefV1
    unit_convention_ref: VersionRefV1
    projection: raw_api.ProjectedRawValueV1
    canonical_value: str
    event_time_utc: datetime


@dataclass(frozen=True, slots=True)
class TemporalDateOccurrenceV1(_Validated):
    owner_object_id: str
    owner_namespace: str
    implementation_brief_sha256: str
    derived_signal_id: str
    derived_occurrence_id: str
    request: TemporalDateRequestV1
    definition: CalculationDefinitionV1
    parameter_set: CalculationParameterSetV1
    input_selection_policy: InputSelectionPolicyVersionV1
    unit_conventions: tuple[UnitConventionVersionV1, ...]
    projection_mappings: tuple[raw_api.RawSignalProjectionMappingV1, ...]
    raw_input_lineage: tuple[TemporalCalendarRawLineageV1, ...]
    predecessor: TemporalLocalOccurrenceV1
    calendar_policy: CalendarPolicyV1
    result: date
    units: str
    result_shape: str
    effective_as_of_utc: datetime
    knowledge_cutoff_utc: datetime
    calculated_at_utc: datetime


@dataclass(frozen=True, slots=True)
class PhaseIntervalV1(_Validated):
    start_utc: datetime
    end_utc: datetime
    phase: str

    def __post_init__(self) -> None:
        _Validated.__post_init__(self)
        if self.end_utc <= self.start_utc:
            raise ValueError("phase interval must be positive")


@dataclass(frozen=True, slots=True)
class PhasePolicyV1(_Validated):
    ref: VersionRefV1
    calendar_ref: VersionRefV1
    iana_zone: str
    intervals: tuple[PhaseIntervalV1, ...]

    def __post_init__(self) -> None:
        _Validated.__post_init__(self)
        if (not self.intervals or any(a.end_utc > b.start_utc for a, b in zip(
            self.intervals, self.intervals[1:], strict=False,
        ))):
            raise ValueError("ordered nonoverlapping phase schedule required")


@dataclass(frozen=True, slots=True)
class TemporalPhaseRequestV1(_Validated):
    calculation: CalculationRequestV1
    predecessor_occurrence_id: str
    calendar_policy: CalendarPolicyV1
    phase_policy: PhasePolicyV1


@dataclass(frozen=True, slots=True)
class TemporalPhaseOccurrenceV1(_Validated):
    owner_object_id: str
    owner_namespace: str
    implementation_brief_sha256: str
    derived_signal_id: str
    derived_occurrence_id: str
    request: TemporalPhaseRequestV1
    definition: CalculationDefinitionV1
    parameter_set: CalculationParameterSetV1
    input_selection_policy: InputSelectionPolicyVersionV1
    unit_conventions: tuple[UnitConventionVersionV1, ...]
    projection_mappings: tuple[raw_api.RawSignalProjectionMappingV1, ...]
    raw_input_lineage: tuple[TemporalCalendarRawLineageV1, ...]
    predecessor: TemporalLocalOccurrenceV1
    calendar_policy: CalendarPolicyV1
    phase_policy: PhasePolicyV1
    result: str
    units: str
    result_shape: str
    effective_as_of_utc: datetime
    knowledge_cutoff_utc: datetime
    calculated_at_utc: datetime


@dataclass(frozen=True, slots=True)
class VintageStatusRequestV1(_Validated):
    calculation: CalculationRequestV1
    series_id: str
    reference_period: str


@dataclass(frozen=True, slots=True)
class VintageRawLineageV1(_Validated):
    raw_signal_id: str
    observation_occurrence_id: str
    projection_mapping_ref: VersionRefV1
    unit_convention_ref: VersionRefV1
    projection: raw_api.ProjectedRawValueV1
    canonical_value: date | datetime
    publication_ordinal: int
    publication_timestamp_utc: datetime


@dataclass(frozen=True, slots=True)
class VintageStatusOccurrenceV1(_Validated):
    owner_object_id: str
    owner_namespace: str
    implementation_brief_sha256: str
    derived_signal_id: str
    derived_occurrence_id: str
    request: VintageStatusRequestV1
    definition: CalculationDefinitionV1
    parameter_set: CalculationParameterSetV1
    input_selection_policy: InputSelectionPolicyVersionV1
    unit_conventions: tuple[UnitConventionVersionV1, ...]
    projection_mappings: tuple[raw_api.RawSignalProjectionMappingV1, ...]
    raw_input_lineage: tuple[VintageRawLineageV1, ...]
    visible_vintage_ids: tuple[str, ...]
    vintage_id: str
    publication_ordinal: int
    publication_timestamp_utc: datetime
    realtime_start: date
    realtime_end: date
    last_updated_utc: datetime
    result: str
    units: str
    result_shape: str
    effective_as_of_utc: datetime
    knowledge_cutoff_utc: datetime
    calculated_at_utc: datetime


class MeasurementVintageReadsV1(Protocol):
    def get_derived_occurrence(self, derived_occurrence_id: str
                               ) -> VintageStatusOccurrenceV1 | None: ...
    def list_derived_history(
        self, *, derived_signal_id: str, subject_instrument: str,
        effective_at_or_before_utc: datetime, knowledge_at_or_before_utc: datetime, limit: int,
    ) -> tuple[VintageStatusOccurrenceV1, ...]: ...


class MeasurementVintageOwnerV1(Protocol):
    @property
    def reads(self) -> MeasurementVintageReadsV1: ...
    def materialise_vintage_statuses(self, request: VintageStatusRequestV1
                                    ) -> tuple[VintageStatusOccurrenceV1, ...] | None: ...


def create_vintage_owner(
    *, admission: OwnerAdmissionV1, raw_projection_reader: RawProjectionReaderV1,
    storage: MemoryStorageV1 | SQLiteStorageV1, utc_now: Callable[[], datetime],
) -> MeasurementVintageOwnerV1:
    from ._vintage import build_owner

    return build_owner(admission, raw_projection_reader, storage, utc_now)


def create_vintage_reader(
    *, admission: OwnerAdmissionV1, storage: SQLiteReadStorageV1,
) -> MeasurementVintageReadsV1:
    from ._vintage import build_reader

    return build_reader(admission, storage)


class MeasurementTemporalPhaseReadsV1(Protocol):
    def get_derived_occurrence(self, derived_occurrence_id: str
                               ) -> TemporalPhaseOccurrenceV1 | None: ...
    def list_derived_history(
        self, *, derived_signal_id: str, subject_instrument: str,
        effective_at_or_before_utc: datetime, knowledge_at_or_before_utc: datetime, limit: int,
    ) -> tuple[TemporalPhaseOccurrenceV1, ...]: ...


class MeasurementTemporalPhaseOwnerV1(Protocol):
    @property
    def reads(self) -> MeasurementTemporalPhaseReadsV1: ...
    def materialise(self, request: TemporalPhaseRequestV1
                    ) -> TemporalPhaseOccurrenceV1 | None: ...


def create_temporal_phase_owner(
    *, admission: OwnerAdmissionV1, raw_projection_reader: RawProjectionReaderV1,
    predecessor_reader: MeasurementTemporalLocalReadsV1,
    storage: MemoryStorageV1 | SQLiteStorageV1, utc_now: Callable[[], datetime],
) -> MeasurementTemporalPhaseOwnerV1:
    from ._temporal_phase import build_owner

    return build_owner(admission, raw_projection_reader, predecessor_reader, storage, utc_now)


def create_temporal_phase_reader(
    *, admission: OwnerAdmissionV1, storage: SQLiteReadStorageV1,
) -> MeasurementTemporalPhaseReadsV1:
    from ._temporal_phase import build_reader

    return build_reader(admission, storage)


class MeasurementTemporalDateReadsV1(Protocol):
    def get_derived_occurrence(self, derived_occurrence_id: str
                               ) -> TemporalDateOccurrenceV1 | None: ...
    def list_derived_history(
        self, *, derived_signal_id: str, subject_instrument: str,
        effective_at_or_before_utc: datetime, knowledge_at_or_before_utc: datetime, limit: int,
    ) -> tuple[TemporalDateOccurrenceV1, ...]: ...


class MeasurementTemporalDateOwnerV1(Protocol):
    @property
    def reads(self) -> MeasurementTemporalDateReadsV1: ...
    def materialise(self, request: TemporalDateRequestV1
                    ) -> TemporalDateOccurrenceV1 | None: ...


def create_temporal_date_owner(
    *, admission: OwnerAdmissionV1, raw_projection_reader: RawProjectionReaderV1,
    predecessor_reader: MeasurementTemporalLocalReadsV1,
    storage: MemoryStorageV1 | SQLiteStorageV1, utc_now: Callable[[], datetime],
) -> MeasurementTemporalDateOwnerV1:
    from ._temporal_date import build_owner

    return build_owner(admission, raw_projection_reader, predecessor_reader, storage, utc_now)


def create_temporal_date_reader(
    *, admission: OwnerAdmissionV1, storage: SQLiteReadStorageV1,
) -> MeasurementTemporalDateReadsV1:
    from ._temporal_date import build_reader

    return build_reader(admission, storage)


class MeasurementTemporalLocalReadsV1(Protocol):
    def get_derived_occurrence(self, derived_occurrence_id: str
                               ) -> TemporalLocalOccurrenceV1 | None: ...
    def list_derived_history(
        self, *, derived_signal_id: str, subject_instrument: str,
        effective_at_or_before_utc: datetime, knowledge_at_or_before_utc: datetime, limit: int,
    ) -> tuple[TemporalLocalOccurrenceV1, ...]: ...


class MeasurementTemporalLocalOwnerV1(Protocol):
    @property
    def reads(self) -> MeasurementTemporalLocalReadsV1: ...
    def materialise(self, request: TemporalLocalRequestV1
                    ) -> TemporalLocalOccurrenceV1 | None: ...


def create_temporal_local_owner(
    *, admission: OwnerAdmissionV1, raw_projection_reader: RawProjectionReaderV1,
    predecessor_reader: MeasurementTemporalReadsV1,
    storage: MemoryStorageV1 | SQLiteStorageV1, utc_now: Callable[[], datetime],
) -> MeasurementTemporalLocalOwnerV1:
    from ._temporal_local import build_owner

    return build_owner(admission, raw_projection_reader, predecessor_reader, storage, utc_now)


def create_temporal_local_reader(
    *, admission: OwnerAdmissionV1, storage: SQLiteReadStorageV1,
) -> MeasurementTemporalLocalReadsV1:
    from ._temporal_local import build_reader

    return build_reader(admission, storage)


class MeasurementTemporalAgeReadsV1(Protocol):
    def get_derived_occurrence(self, derived_occurrence_id: str
                               ) -> TemporalAgeOccurrenceV1 | None: ...
    def list_derived_history(
        self, *, derived_signal_id: str, subject_instrument: str,
        effective_at_or_before_utc: datetime, knowledge_at_or_before_utc: datetime, limit: int,
    ) -> tuple[TemporalAgeOccurrenceV1, ...]: ...


class MeasurementTemporalAgeOwnerV1(Protocol):
    @property
    def reads(self) -> MeasurementTemporalAgeReadsV1: ...
    def materialise(self, request: TemporalAgeRequestV1
                    ) -> TemporalAgeOccurrenceV1 | None: ...


def create_temporal_age_owner(
    *, admission: OwnerAdmissionV1, raw_projection_reader: RawProjectionReaderV1,
    predecessor_reader: MeasurementTemporalReadsV1,
    storage: MemoryStorageV1 | SQLiteStorageV1, utc_now: Callable[[], datetime],
) -> MeasurementTemporalAgeOwnerV1:
    from ._temporal_age import build_owner

    return build_owner(admission, raw_projection_reader, predecessor_reader, storage, utc_now)


def create_temporal_age_reader(
    *, admission: OwnerAdmissionV1, storage: SQLiteReadStorageV1,
) -> MeasurementTemporalAgeReadsV1:
    from ._temporal_age import build_reader

    return build_reader(admission, storage)


class MeasurementTemporalReadsV1(Protocol):
    def get_derived_occurrence(self, derived_occurrence_id: str) -> TemporalOccurrenceV1 | None: ...
    def list_derived_history(
        self, *, derived_signal_id: str, subject_instrument: str,
        effective_at_or_before_utc: datetime, knowledge_at_or_before_utc: datetime, limit: int,
    ) -> tuple[TemporalOccurrenceV1, ...]: ...


class MeasurementTemporalOwnerV1(Protocol):
    @property
    def reads(self) -> MeasurementTemporalReadsV1: ...
    def materialise(self, request: CalculationRequestV1) -> TemporalOccurrenceV1 | None: ...


def create_temporal_owner(
    *, admission: OwnerAdmissionV1, raw_projection_reader: RawProjectionReaderV1,
    storage: MemoryStorageV1 | SQLiteStorageV1, utc_now: Callable[[], datetime],
) -> MeasurementTemporalOwnerV1:
    from ._temporal import build_owner

    return build_owner(admission, raw_projection_reader, storage, utc_now)


def create_temporal_reader(
    *, admission: OwnerAdmissionV1, storage: SQLiteReadStorageV1,
) -> MeasurementTemporalReadsV1:
    from ._temporal import build_reader

    return build_reader(admission, storage)


class MeasurementWindowReadsV1(Protocol):
    def get_derived_occurrence(
        self, derived_occurrence_id: str
    ) -> WindowMeasurementOccurrenceV1 | None: ...
    def list_derived_history(
        self,
        *,
        derived_signal_id: str,
        subject_instrument: str,
        effective_at_or_before_utc: datetime,
        knowledge_at_or_before_utc: datetime,
        limit: int,
    ) -> tuple[WindowMeasurementOccurrenceV1, ...]: ...


class MeasurementWindowOwnerV1(Protocol):
    @property
    def reads(self) -> MeasurementWindowReadsV1: ...
    def materialise(
        self, request: WindowCalculationRequestV1
    ) -> WindowMeasurementOccurrenceV1 | None: ...


def create_window_owner(
    *,
    admission: OwnerAdmissionV1,
    raw_projection_reader: RawProjectionReaderV1,
    predecessor_reader: MeasurementTradeDirectionReadsV1 | MeasurementWindowReadsV1 | None = None,
    storage: MemoryStorageV1 | SQLiteStorageV1,
    utc_now: Callable[[], datetime],
) -> MeasurementWindowOwnerV1:
    from ._window import build_owner

    return build_owner(admission, raw_projection_reader, predecessor_reader, storage, utc_now)


def create_window_reader(
    *,
    admission: OwnerAdmissionV1,
    storage: SQLiteReadStorageV1,
) -> MeasurementWindowReadsV1:
    from ._window import build_reader

    return build_reader(admission, storage)


@dataclass(frozen=True, slots=True)
class DeliveredModePolicyV1(_Validated):
    ref: VersionRefV1
    requested_mode: str
    live_delivered_code: int
    generation_id: str


@dataclass(frozen=True, slots=True)
class MarketStatePolicyV1(_Validated):
    ref: VersionRefV1
    calendar_ref: VersionRefV1
    open_dates: tuple[date, ...]
    closed_dates: tuple[date, ...]

    def __post_init__(self) -> None:
        _Validated.__post_init__(self)
        if set(self.open_dates) & set(self.closed_dates):
            raise ValueError("market date cannot be both open and closed")


@dataclass(frozen=True, slots=True)
class MarketModeRawLineageV1(_Validated):
    raw_signal_id: str
    observation_occurrence_id: str
    projection_mapping_ref: VersionRefV1
    unit_convention_ref: VersionRefV1
    projection: raw_api.ProjectedRawValueV1
    canonical_value: int
    event_time_utc: datetime


@dataclass(frozen=True, slots=True)
class MarketOpenRequestV1(_Validated):
    calculation: CalculationRequestV1
    predecessor_occurrence_id: str
    mode_policy: DeliveredModePolicyV1
    calendar_policy: CalendarPolicyV1
    phase_policy: PhasePolicyV1
    market_state_policy: MarketStatePolicyV1
    liquid_phases: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class MarketOpenOccurrenceV1(_Validated):
    owner_object_id: str
    owner_namespace: str
    implementation_brief_sha256: str
    derived_signal_id: str
    derived_occurrence_id: str
    request: MarketOpenRequestV1
    definition: CalculationDefinitionV1
    parameter_set: CalculationParameterSetV1
    input_selection_policy: InputSelectionPolicyVersionV1
    unit_conventions: tuple[UnitConventionVersionV1, ...]
    projection_mappings: tuple[raw_api.RawSignalProjectionMappingV1, ...]
    delivered_mode_lineage: MarketModeRawLineageV1
    calendar_lineage: tuple[TemporalCalendarRawLineageV1, ...]
    predecessor: TemporalLocalOccurrenceV1
    mode_policy: DeliveredModePolicyV1
    calendar_policy: CalendarPolicyV1
    phase_policy: PhasePolicyV1
    market_state_policy: MarketStatePolicyV1
    liquid_phases: tuple[str, ...]
    result: bool
    units: str
    result_shape: str
    effective_as_of_utc: datetime
    knowledge_cutoff_utc: datetime
    calculated_at_utc: datetime


class MeasurementMarketOpenReadsV1(Protocol):
    def get_derived_occurrence(self, derived_occurrence_id: str
                               ) -> MarketOpenOccurrenceV1 | None: ...
    def list_derived_history(
        self, *, derived_signal_id: str, subject_instrument: str,
        effective_at_or_before_utc: datetime, knowledge_at_or_before_utc: datetime, limit: int,
    ) -> tuple[MarketOpenOccurrenceV1, ...]: ...


class MeasurementMarketOpenOwnerV1(Protocol):
    @property
    def reads(self) -> MeasurementMarketOpenReadsV1: ...
    def materialise(self, request: MarketOpenRequestV1
                    ) -> MarketOpenOccurrenceV1 | None: ...


def create_market_open_owner(
    *, admission: OwnerAdmissionV1, raw_projection_reader: RawProjectionReaderV1,
    predecessor_reader: MeasurementTemporalLocalReadsV1,
    storage: MemoryStorageV1 | SQLiteStorageV1, utc_now: Callable[[], datetime],
) -> MeasurementMarketOpenOwnerV1:
    from ._market_open import build_owner

    return build_owner(admission, raw_projection_reader, predecessor_reader, storage, utc_now)


def create_market_open_reader(
    *, admission: OwnerAdmissionV1, storage: SQLiteReadStorageV1,
) -> MeasurementMarketOpenReadsV1:
    from ._market_open import build_reader

    return build_reader(admission, storage)


__all__ += [
    "BaselineWindowContextV1",
    "CalendarIntervalV1",
    "CalendarPolicyV1",
    "CorrelationMatrixV1",
    "DeliveredModePolicyV1",
    "IndexChangeV1",
    "MarketModeRawLineageV1",
    "MarketOpenOccurrenceV1",
    "MarketOpenRequestV1",
    "MarketStatePolicyV1",
    "MeasurementComparisonV1",
    "MeasurementMarketOpenOwnerV1",
    "MeasurementMarketOpenReadsV1",
    "MeasurementTemporalAgeOwnerV1",
    "MeasurementTemporalAgeReadsV1",
    "MeasurementTemporalDateOwnerV1",
    "MeasurementTemporalDateReadsV1",
    "MeasurementTemporalLocalOwnerV1",
    "MeasurementTemporalLocalReadsV1",
    "MeasurementTemporalOwnerV1",
    "MeasurementTemporalPhaseOwnerV1",
    "MeasurementTemporalPhaseReadsV1",
    "MeasurementTemporalReadsV1",
    "MeasurementVintageOwnerV1",
    "MeasurementVintageReadsV1",
    "MeasurementWindowOwnerV1",
    "MeasurementWindowReadsV1",
    "OIConcentrationV1",
    "OptionRightLineageV1",
    "OptionSkewV1",
    "PhaseIntervalV1",
    "PhasePolicyV1",
    "ReturnAccelerationV1",
    "SessionFrameV1",
    "TemporalAgeOccurrenceV1",
    "TemporalAgeRawLineageV1",
    "TemporalAgeRequestV1",
    "TemporalAgeV1",
    "TemporalCalendarRawLineageV1",
    "TemporalDateOccurrenceV1",
    "TemporalDateRequestV1",
    "TemporalLocalOccurrenceV1",
    "TemporalLocalRawLineageV1",
    "TemporalLocalRequestV1",
    "TemporalOccurrenceV1",
    "TemporalPhaseOccurrenceV1",
    "TemporalPhaseRequestV1",
    "TemporalRawLineageV1",
    "TermPairV1",
    "VintageRawLineageV1",
    "VintageStatusOccurrenceV1",
    "VintageStatusRequestV1",
    "VwapDeviationV1",
    "VwapRateV1",
    "WindowCalculationRequestV1",
    "WindowContextV1",
    "WindowMeasurementOccurrenceV1",
    "create_market_open_owner",
    "create_market_open_reader",
    "create_temporal_age_owner",
    "create_temporal_age_reader",
    "create_temporal_date_owner",
    "create_temporal_date_reader",
    "create_temporal_local_owner",
    "create_temporal_local_reader",
    "create_temporal_owner",
    "create_temporal_phase_owner",
    "create_temporal_phase_reader",
    "create_temporal_reader",
    "create_vintage_owner",
    "create_vintage_reader",
    "create_window_owner",
    "create_window_reader",
]
