"""Exact controlled neutral-measurement public contract under accepted SQLite version 3."""

from __future__ import annotations

import re
import types
from collections.abc import Callable, Sequence
from dataclasses import dataclass, fields, is_dataclass
from datetime import datetime, timedelta
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
            if type(value) is datetime:
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


__all__ += [
    "BaselineWindowContextV1",
    "CorrelationMatrixV1",
    "IndexChangeV1",
    "MeasurementComparisonV1",
    "MeasurementWindowOwnerV1",
    "MeasurementWindowReadsV1",
    "OptionRightLineageV1",
    "OptionSkewV1",
    "ReturnAccelerationV1",
    "SessionFrameV1",
    "TermPairV1",
    "VwapDeviationV1",
    "VwapRateV1",
    "WindowCalculationRequestV1",
    "WindowContextV1",
    "WindowMeasurementOccurrenceV1",
    "create_window_owner",
    "create_window_reader",
]
