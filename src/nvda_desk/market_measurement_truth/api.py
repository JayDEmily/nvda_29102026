"""Exact controlled neutral-measurement public contract under accepted SQLite version 3."""

from __future__ import annotations

import re
import types
from collections.abc import Callable, Sequence
from dataclasses import dataclass, fields, is_dataclass
from datetime import datetime, timedelta
from decimal import Decimal
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


__all__ = [
    "AuthorityArtifactRefV1",
    "CalculationDefinitionV1",
    "CalculationParameterSetV1",
    "CalculationRequestV1",
    "DerivedSignalOccurrenceV1",
    "InputSelectionPolicyVersionV1",
    "MeasurementOwnerV1",
    "MeasurementReadsV1",
    "MemoryStorageV1",
    "OwnerAdmissionV1",
    "PersistenceFailureV1",
    "RawInputBindingV1",
    "RawInputLineageV1",
    "RawProjectionReaderV1",
    "SQLiteReadStorageV1",
    "SQLiteStorageV1",
    "UnitConventionVersionV1",
    "VersionRefV1",
    "create_owner",
    "create_reader",
]
