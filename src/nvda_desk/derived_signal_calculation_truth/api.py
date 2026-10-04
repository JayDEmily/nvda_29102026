"""Typed public foundation seam for Derived Signal Calculation Truth."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Protocol


def _require_non_empty_string(value: str, field_name: str) -> None:
    if type(value) is not str or not value:
        raise ValueError(f"{field_name} must be a non-empty string")


def _require_positive_version(value: int, field_name: str = "version") -> None:
    if type(value) is not int or value <= 0:
        raise ValueError(f"{field_name} must be a positive integer")


def _require_utc(value: datetime, field_name: str) -> None:
    if type(value) is not datetime:
        raise TypeError(f"{field_name} must be a datetime")
    if value.tzinfo is None or value.utcoffset() != timedelta(0):
        raise ValueError(f"{field_name} must be UTC-aware")


def _require_derived_signal_id(value: str) -> None:
    if type(value) is not str or len(value) != 4 or value[0] != "D" or not value[1:].isdigit():
        raise ValueError("derived_signal_id must be canonical DNNN form")
    if not 1 <= int(value[1:]) <= 209:
        raise ValueError("derived_signal_id must be in D001-D209")


@dataclass(frozen=True, slots=True)
class _VersionedContextV1:
    context_id: str
    version: int

    def __post_init__(self) -> None:
        _require_non_empty_string(self.context_id, "context_id")
        _require_positive_version(self.version)


@dataclass(frozen=True, slots=True)
class CalculationParameterSetV1(_VersionedContextV1):
    pass


@dataclass(frozen=True, slots=True)
class RequiredFieldPolicyV1(_VersionedContextV1):
    pass


@dataclass(frozen=True, slots=True)
class CandidateStructureContextV1(_VersionedContextV1):
    pass


@dataclass(frozen=True, slots=True)
class CandidateSetContextV1(_VersionedContextV1):
    pass


@dataclass(frozen=True, slots=True)
class LivePositionContextV1(_VersionedContextV1):
    pass


@dataclass(frozen=True, slots=True)
class OrderIntentContextV1(_VersionedContextV1):
    pass


@dataclass(frozen=True, slots=True)
class EntryStateContextV1(_VersionedContextV1):
    pass


@dataclass(frozen=True, slots=True)
class EvaluationSetV1(_VersionedContextV1):
    pass


@dataclass(frozen=True, slots=True)
class RecalculationScheduleV1(_VersionedContextV1):
    pass


@dataclass(frozen=True, slots=True)
class UnitConventionVersionV1(_VersionedContextV1):
    native_units: str
    canonical_units: str
    scale: Decimal
    offset: Decimal

    def __post_init__(self) -> None:
        _VersionedContextV1.__post_init__(self)
        _require_non_empty_string(self.native_units, "native_units")
        _require_non_empty_string(self.canonical_units, "canonical_units")
        if type(self.scale) is not Decimal or type(self.offset) is not Decimal:
            raise TypeError("scale and offset must be Decimal values")

    def convert(self, value: Decimal, *, native_units: str) -> Decimal:
        if native_units != self.native_units:
            raise ValueError("native_units does not match this unit convention")
        if type(value) is not Decimal:
            raise TypeError("value must be Decimal")
        return value * self.scale + self.offset


@dataclass(frozen=True, slots=True)
class PnLConventionVersionV1(_VersionedContextV1):
    pass


@dataclass(frozen=True, slots=True)
class OptionRevaluationConventionVersionV1(_VersionedContextV1):
    pass


@dataclass(frozen=True, slots=True)
class ExecutionCostScheduleVersionV1(_VersionedContextV1):
    pass


@dataclass(frozen=True, slots=True)
class AttributionPathContextV1(_VersionedContextV1):
    pass


@dataclass(frozen=True, slots=True)
class InputSelectionPolicyVersionV1(_VersionedContextV1):
    pass


@dataclass(frozen=True, slots=True)
class VersionRefV1:
    context_id: str
    version: int

    def __post_init__(self) -> None:
        _require_non_empty_string(self.context_id, "context_id")
        _require_positive_version(self.version)


@dataclass(frozen=True, slots=True)
class RawInputLineageV1:
    raw_signal_id: str
    observation_occurrence_id: str
    projection_mapping_id: str
    projection_mapping_version: int
    unit_convention_id: str
    unit_convention_version: int
    native_units: str
    canonical_units: str

    def __post_init__(self) -> None:
        if type(self.raw_signal_id) is not str or len(self.raw_signal_id) != 4:
            raise ValueError("raw_signal_id must be canonical RNNN form")
        _require_non_empty_string(self.observation_occurrence_id, "observation_occurrence_id")
        _require_non_empty_string(self.projection_mapping_id, "projection_mapping_id")
        _require_positive_version(self.projection_mapping_version, "projection_mapping_version")
        _require_non_empty_string(self.unit_convention_id, "unit_convention_id")
        _require_positive_version(self.unit_convention_version, "unit_convention_version")
        _require_non_empty_string(self.native_units, "native_units")
        _require_non_empty_string(self.canonical_units, "canonical_units")


type DerivedResultV1 = (
    None
    | bool
    | int
    | Decimal
    | str
    | datetime
    | tuple["DerivedResultV1", ...]
)


@dataclass(frozen=True, slots=True)
class DerivedSignalOccurrenceV1:
    derived_signal_id: str
    derived_occurrence_id: str
    calculation_definition_version: str
    parameter_context_refs: tuple[VersionRefV1, ...]
    subject_instrument: str
    universe: tuple[str, ...] | None
    effective_as_of_utc: datetime
    window: str | None
    knowledge_cutoff_utc: datetime
    calculated_at_utc: datetime
    result: DerivedResultV1
    units: str
    result_shape: str
    raw_input_lineage: tuple[RawInputLineageV1, ...]
    predecessor_occurrence_ids: tuple[str, ...]
    convention_refs: tuple[VersionRefV1, ...]
    supersedes_derived_occurrence_id: str | None = None

    def __post_init__(self) -> None:
        _require_derived_signal_id(self.derived_signal_id)
        _require_non_empty_string(self.derived_occurrence_id, "derived_occurrence_id")
        _require_non_empty_string(
            self.calculation_definition_version, "calculation_definition_version"
        )
        _require_non_empty_string(self.subject_instrument, "subject_instrument")
        _require_utc(self.effective_as_of_utc, "effective_as_of_utc")
        _require_utc(self.knowledge_cutoff_utc, "knowledge_cutoff_utc")
        _require_utc(self.calculated_at_utc, "calculated_at_utc")
        _require_non_empty_string(self.units, "units")
        _require_non_empty_string(self.result_shape, "result_shape")
        if self.window is not None and (type(self.window) is not str or not self.window):
            raise ValueError("window must be a non-empty string or absent")
        if self.universe is not None and type(self.universe) is not tuple:
            raise TypeError("universe must be a tuple or absent")
        if type(self.parameter_context_refs) is not tuple:
            raise TypeError("parameter_context_refs must be a tuple")
        if type(self.raw_input_lineage) is not tuple:
            raise TypeError("raw_input_lineage must be a tuple")
        if type(self.predecessor_occurrence_ids) is not tuple:
            raise TypeError("predecessor_occurrence_ids must be a tuple")
        if type(self.convention_refs) is not tuple:
            raise TypeError("convention_refs must be a tuple")


@dataclass(frozen=True, slots=True)
class CalculationRequestV1:
    derived_signal_id: str
    subject_instrument: str
    as_of_utc: datetime
    knowledge_cutoff_utc: datetime
    calculation_definition_version: str
    parameter_set_id: str
    parameter_set_version: int
    input_selection_policy_id: str
    input_selection_policy_version: int
    context_refs: tuple[VersionRefV1, ...]

    def __post_init__(self) -> None:
        _require_derived_signal_id(self.derived_signal_id)
        _require_non_empty_string(self.subject_instrument, "subject_instrument")
        _require_utc(self.as_of_utc, "as_of_utc")
        _require_utc(self.knowledge_cutoff_utc, "knowledge_cutoff_utc")
        _require_non_empty_string(
            self.calculation_definition_version, "calculation_definition_version"
        )
        _require_non_empty_string(self.parameter_set_id, "parameter_set_id")
        _require_positive_version(self.parameter_set_version, "parameter_set_version")
        _require_non_empty_string(self.input_selection_policy_id, "input_selection_policy_id")
        _require_positive_version(
            self.input_selection_policy_version, "input_selection_policy_version"
        )
        if type(self.context_refs) is not tuple:
            raise TypeError("context_refs must be a tuple")


class RawProjectionReaderV1(Protocol):
    def project_raw_value(self, *args: object, **kwargs: object) -> object | None: ...

    def list_projected_raw_history(self, *args: object, **kwargs: object) -> object: ...


class _PersistenceV1(Protocol):
    def append_occurrence(self, value: DerivedSignalOccurrenceV1) -> DerivedSignalOccurrenceV1: ...

    def get_occurrence(self, derived_occurrence_id: str) -> DerivedSignalOccurrenceV1 | None: ...

    def list_occurrences(
        self, *, derived_signal_id: str, subject_instrument: str, limit: int
    ) -> tuple[DerivedSignalOccurrenceV1, ...]: ...


class _MemoryPersistenceV1:
    def __init__(self) -> None:
        self._by_id: dict[str, DerivedSignalOccurrenceV1] = {}

    def append_occurrence(self, value: DerivedSignalOccurrenceV1) -> DerivedSignalOccurrenceV1:
        existing = self._by_id.get(value.derived_occurrence_id)
        if existing is not None:
            if existing != value:
                raise ValueError("derived occurrence identity already has different content")
            return existing
        self._by_id[value.derived_occurrence_id] = value
        return value

    def get_occurrence(self, derived_occurrence_id: str) -> DerivedSignalOccurrenceV1 | None:
        return self._by_id.get(derived_occurrence_id)

    def list_occurrences(
        self, *, derived_signal_id: str, subject_instrument: str, limit: int
    ) -> tuple[DerivedSignalOccurrenceV1, ...]:
        if type(limit) is not int or limit <= 0:
            raise ValueError("limit must be a positive integer")
        values = [
            value
            for value in self._by_id.values()
            if value.derived_signal_id == derived_signal_id
            and value.subject_instrument == subject_instrument
        ]
        values.sort(key=lambda value: (value.effective_as_of_utc, value.derived_occurrence_id))
        return tuple(values[:limit])


class _ReadsV1:
    __slots__ = ("_persistence",)

    def __init__(self, persistence: _PersistenceV1) -> None:
        self._persistence = persistence

    def get_derived_occurrence(
        self, derived_occurrence_id: str
    ) -> DerivedSignalOccurrenceV1 | None:
        _require_non_empty_string(derived_occurrence_id, "derived_occurrence_id")
        return self._persistence.get_occurrence(derived_occurrence_id)

    def list_derived_history(
        self, *, derived_signal_id: str, subject_instrument: str, limit: int
    ) -> tuple[DerivedSignalOccurrenceV1, ...]:
        _require_derived_signal_id(derived_signal_id)
        _require_non_empty_string(subject_instrument, "subject_instrument")
        return self._persistence.list_occurrences(
            derived_signal_id=derived_signal_id,
            subject_instrument=subject_instrument,
            limit=limit,
        )


class _OwnerV1:
    __slots__ = ("_persistence", "_raw_projection_reader", "reads")

    def __init__(
        self,
        *,
        raw_projection_reader: RawProjectionReaderV1,
        persistence: _PersistenceV1,
    ) -> None:
        self._raw_projection_reader = raw_projection_reader
        self._persistence = persistence
        self.reads = _ReadsV1(persistence)

    def materialise(self, request: CalculationRequestV1) -> DerivedSignalOccurrenceV1 | None:
        if type(request) is not CalculationRequestV1:
            raise TypeError("request must be CalculationRequestV1")
        # DS-I01 establishes the calculation/read foundation only. No D-kernel is admitted in
        # this leaf, so the sole lawful result until a later kernel leaf supplies all required
        # inputs and calculation meaning is absence.
        return None


def create_owner(
    *,
    raw_projection_reader: RawProjectionReaderV1,
    persistence: _PersistenceV1 | None = None,
) -> _OwnerV1:
    if persistence is None:
        persistence = _MemoryPersistenceV1()
    return _OwnerV1(raw_projection_reader=raw_projection_reader, persistence=persistence)


__all__ = [
    "AttributionPathContextV1",
    "CalculationParameterSetV1",
    "CalculationRequestV1",
    "CandidateSetContextV1",
    "CandidateStructureContextV1",
    "DerivedResultV1",
    "DerivedSignalOccurrenceV1",
    "EntryStateContextV1",
    "EvaluationSetV1",
    "ExecutionCostScheduleVersionV1",
    "InputSelectionPolicyVersionV1",
    "LivePositionContextV1",
    "OptionRevaluationConventionVersionV1",
    "OrderIntentContextV1",
    "PnLConventionVersionV1",
    "RawInputLineageV1",
    "RawProjectionReaderV1",
    "RecalculationScheduleV1",
    "RequiredFieldPolicyV1",
    "UnitConventionVersionV1",
    "VersionRefV1",
    "create_owner",
]
