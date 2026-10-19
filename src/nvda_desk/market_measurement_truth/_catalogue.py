"""Controlled D011 registrations, owning service and explicit component memory state."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field, replace
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Any, cast

from nvda_desk.raw_signal_occurrence_truth import api as raw_api

from . import api as f
from ._evaluation import canonical, digest, midpoint
from ._selection import select

NAMESPACE = "neutral_market_measurement_truth/v1"
_AUTHORITY = (
    (
        "handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md",
        "603b850802a418780109095e7ae69bcece449da79fb24140a6d50297605e927c",
    ),
    (
        "handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv",
        "67bacbcf77afa766cec220a8d4a0f9589c9568d4a1f5c5818334915adf72e549",
    ),
)
_PROVIDER = "foundation-pilot-fixture"
_SCOPE = _PROVIDER + "/cash_quote_v1"
type _Configuration = (
    f.CalculationParameterSetV1
    | f.InputSelectionPolicyVersionV1
    | f.UnitConventionVersionV1
    | raw_api.RawSignalProjectionMappingV1
)


def _expected(value: Any) -> Any:
    if type(value) is f.CalculationDefinitionV1:
        if value.calculation_definition_version not in {"D011-MIDPOINT-1", "D011-MIDPOINT-2"}:
            raise ValueError("unadmitted definition version")
        return f.CalculationDefinitionV1(
            "D011",
            value.calculation_definition_version,
            "K02_ALGEBRA",
            "(R034 + R035) / 2",
            ("R034", "R035"),
            (),
            "P_BASIC",
            "price",
            "scalar_decimal",
            tuple(f.AuthorityArtifactRefV1(*ref) for ref in _AUTHORITY),
        )
    if value.version not in (1, 2):
        raise ValueError("unadmitted controlled configuration version")
    version = value.version
    if type(value) is f.CalculationParameterSetV1:
        return f.CalculationParameterSetV1("mmt-pilot-basic", version, "P_BASIC", "NVDA", ("NVDA",))
    if type(value) is f.InputSelectionPolicyVersionV1:
        return f.InputSelectionPolicyVersionV1(
            "mmt-pilot-selection",
            version,
            ("subject_instrument",),
            timedelta(seconds=60),
            timedelta(seconds=10),
            ("true_instant",),
            (),
            _PROVIDER,
            "cash_quote_v1",
            _SCOPE,
            100,
            1000,
        )
    if type(value) is f.UnitConventionVersionV1:
        return f.UnitConventionVersionV1(
            "mmt-pilot-price", version, "price", "price", Decimal("1"), Decimal("0")
        )
    if type(value) is raw_api.RawSignalProjectionMappingV1:
        if value.mapping_id not in {"mmt-pilot-bid", "mmt-pilot-ask"}:
            raise ValueError("unadmitted raw mapping")
        side = "bid" if value.mapping_id == "mmt-pilot-bid" else "ask"
        return raw_api.RawSignalProjectionMappingV1(
            value.mapping_id,
            version,
            raw_api.RawSignalCatalogueId("R034" if side == "bid" else "R035"),
            _PROVIDER,
            "cash_quote_v1",
            ("quote", side),
            "price",
            (),
        )
    raise TypeError("unexpected configuration record")


def _kind(value: _Configuration) -> str:
    return {
        f.CalculationParameterSetV1: "parameter",
        f.InputSelectionPolicyVersionV1: "selection",
        f.UnitConventionVersionV1: "unit",
        raw_api.RawSignalProjectionMappingV1: "raw_mapping",
    }[type(value)]


def _key(value: _Configuration) -> tuple[str, str, int]:
    return (
        _kind(value),
        value.mapping_id
        if isinstance(value, raw_api.RawSignalProjectionMappingV1)
        else value.context_id,
        value.version,
    )


@dataclass
class _Memory:
    definitions: dict[tuple[str, str], f.CalculationDefinitionV1] = field(default_factory=dict)
    configuration: dict[tuple[str, str, int], _Configuration] = field(default_factory=dict)
    occurrences: dict[str, f.DerivedSignalOccurrenceV1] = field(default_factory=dict)
    logical: dict[str, bytes] = field(default_factory=dict)

    def append(
        self, occurrence: f.DerivedSignalOccurrenceV1, payload: bytes
    ) -> f.DerivedSignalOccurrenceV1:
        existing = self.occurrences.get(occurrence.derived_occurrence_id)
        if existing is not None:
            if self.logical[occurrence.derived_occurrence_id] != payload or canonical(
                existing
            ) != canonical(replace(occurrence, calculated_at_utc=existing.calculated_at_utc)):
                raise f.PersistenceFailureV1("immutable occurrence identity conflict")
            return existing
        self.occurrences[occurrence.derived_occurrence_id] = occurrence
        self.logical[occurrence.derived_occurrence_id] = payload
        return occurrence


class _Reads:
    def __init__(self, state: _Memory) -> None:
        self._state = state

    def get_derived_occurrence(
        self, derived_occurrence_id: str
    ) -> f.DerivedSignalOccurrenceV1 | None:
        if type(derived_occurrence_id) is not str:
            raise TypeError("occurrence ID must be a string")
        if not derived_occurrence_id:
            raise ValueError("occurrence ID must be nonempty")
        return self._state.occurrences.get(derived_occurrence_id)

    def list_derived_history(
        self,
        *,
        derived_signal_id: str,
        subject_instrument: str,
        effective_at_or_before_utc: datetime,
        knowledge_at_or_before_utc: datetime,
        limit: int,
    ) -> tuple[f.DerivedSignalOccurrenceV1, ...]:
        f._utc(effective_at_or_before_utc)
        f._utc(knowledge_at_or_before_utc)
        if type(limit) is not int:
            raise TypeError("history limit must be an exact integer")
        if not 1 <= limit <= 1000:
            raise ValueError("history limit must be in 1..1000")
        if type(derived_signal_id) is not str or type(subject_instrument) is not str:
            raise TypeError("history IDs must be strings")
        if not derived_signal_id or not subject_instrument:
            raise ValueError("history IDs must be nonempty")
        return tuple(
            sorted(
                (
                    v
                    for v in self._state.occurrences.values()
                    if v.derived_signal_id == derived_signal_id
                    and v.subject_instrument == subject_instrument
                    and v.effective_as_of_utc <= effective_at_or_before_utc
                    and v.knowledge_cutoff_utc <= knowledge_at_or_before_utc
                ),
                key=lambda v: (
                    v.effective_as_of_utc,
                    v.knowledge_cutoff_utc,
                    v.derived_occurrence_id,
                ),
                reverse=True,
            )[:limit]
        )

    def get_calculation_definition(
        self, *, derived_signal_id: str, calculation_definition_version: str
    ) -> f.CalculationDefinitionV1 | None:
        return self._state.definitions.get((derived_signal_id, calculation_definition_version))

    def get_parameter_set(self, ref: f.VersionRefV1) -> f.CalculationParameterSetV1 | None:
        return cast(f.CalculationParameterSetV1 | None, self._configuration("parameter", ref))

    def get_input_selection_policy(
        self, ref: f.VersionRefV1
    ) -> f.InputSelectionPolicyVersionV1 | None:
        return cast(f.InputSelectionPolicyVersionV1 | None, self._configuration("selection", ref))

    def get_unit_convention(self, ref: f.VersionRefV1) -> f.UnitConventionVersionV1 | None:
        return cast(f.UnitConventionVersionV1 | None, self._configuration("unit", ref))

    def get_projection_mapping(
        self, ref: f.VersionRefV1
    ) -> raw_api.RawSignalProjectionMappingV1 | None:
        return cast(
            raw_api.RawSignalProjectionMappingV1 | None, self._configuration("raw_mapping", ref)
        )

    def _configuration(self, kind: str, ref: f.VersionRefV1) -> _Configuration | None:
        if type(ref) is not f.VersionRefV1:
            raise TypeError("an exact version reference is required")
        return self._state.configuration.get((kind, ref.context_id, ref.version))


class _Owner:
    def __init__(
        self,
        admission: f.OwnerAdmissionV1,
        reader: f.RawProjectionReaderV1,
        state: _Memory,
        now: Callable[[], datetime],
    ) -> None:
        self._admission, self._raw, self._state, self._now = admission, reader, state, now
        self._reads = _Reads(state)

    @property
    def reads(self) -> f.MeasurementReadsV1:
        return self._reads

    def materialise(self, request: f.CalculationRequestV1) -> f.DerivedSignalOccurrenceV1 | None:
        if type(request) is not f.CalculationRequestV1:
            raise TypeError("an exact calculation request is required")
        now = self._now()
        f._utc(now)
        if (
            request.derived_signal_id != "D011"
            or request.subject_instrument != "NVDA"
            or request.context_refs
            or not request.as_of_utc <= request.knowledge_cutoff_utc <= now
            or tuple(b.raw_signal_id for b in request.raw_input_bindings) != ("R034", "R035")
        ):
            return None
        definition = self._state.definitions.get(("D011", request.calculation_definition_version))
        parameter = self._state.configuration.get(
            ("parameter", request.parameter_set_ref.context_id, request.parameter_set_ref.version)
        )
        selection = self._state.configuration.get(
            (
                "selection",
                request.input_selection_policy_ref.context_id,
                request.input_selection_policy_ref.version,
            )
        )
        if (
            definition is None
            or type(parameter) is not f.CalculationParameterSetV1
            or type(selection) is not f.InputSelectionPolicyVersionV1
        ):
            return None
        lineage = []
        mappings = []
        units = {}
        for binding in request.raw_input_bindings:
            mapping = self._state.configuration.get(
                (
                    "raw_mapping",
                    binding.projection_mapping_ref.context_id,
                    binding.projection_mapping_ref.version,
                )
            )
            unit = self._state.configuration.get(
                (
                    "unit",
                    binding.unit_convention_ref.context_id,
                    binding.unit_convention_ref.version,
                )
            )
            if (
                type(mapping) is not raw_api.RawSignalProjectionMappingV1
                or type(unit) is not f.UnitConventionVersionV1
                or mapping.raw_signal_catalogue_id.value != binding.raw_signal_id
                or binding.subject_instrument != "NVDA"
            ):
                return None
            selected = select(self._raw, mapping, selection, request)
            if selected is None:
                return None
            projected, event = selected
            native = cast(Decimal, projected.native_value)
            lineage.append(
                f.RawInputLineageV1(
                    binding.raw_signal_id,
                    projected.observation_occurrence_id.value,
                    binding.projection_mapping_ref,
                    binding.unit_convention_ref,
                    projected,
                    native,
                    event,
                )
            )
            mappings.append(mapping)
            units[(unit.context_id, unit.version)] = unit
        if abs(lineage[0].event_time_utc - lineage[1].event_time_utc) > selection.maximum_skew:
            return None
        value = midpoint(lineage[0].canonical_value, lineage[1].canonical_value)
        if value is None:
            return None
        convention_snapshots = tuple(units[key] for key in sorted(units))
        payload = dict(
            owner_object_id=self._admission.object_id,
            owner_namespace=NAMESPACE,
            implementation_brief_sha256=self._admission.implementation_brief_sha256,
            request=request,
            definition_content_sha256=digest(definition),
            parameter_set=parameter,
            input_selection_policy=selection,
            unit_conventions=convention_snapshots,
            projection_mappings=tuple(mappings),
            raw_input_lineage=tuple(lineage),
        )
        occurrence = f.DerivedSignalOccurrenceV1(
            self._admission.object_id,
            NAMESPACE,
            self._admission.implementation_brief_sha256,
            "D011",
            "mmt1:" + digest(payload),
            definition.calculation_definition_version,
            digest(definition),
            (request.parameter_set_ref, request.input_selection_policy_ref),
            "NVDA",
            None,
            request.as_of_utc,
            None,
            request.knowledge_cutoff_utc,
            now,
            value,
            "price",
            "scalar_decimal",
            tuple(lineage),
            (),
            tuple(f.VersionRefV1(u.context_id, u.version) for u in convention_snapshots),
            None,
        )
        return self._state.append(occurrence, canonical(payload))


def build_owner(
    *,
    admission: f.OwnerAdmissionV1,
    raw_projection_reader: f.RawProjectionReaderV1,
    definitions: tuple[f.CalculationDefinitionV1, ...],
    parameter_sets: tuple[f.CalculationParameterSetV1, ...],
    input_selection_policies: tuple[f.InputSelectionPolicyVersionV1, ...],
    unit_conventions: tuple[f.UnitConventionVersionV1, ...],
    raw_projection_mappings: tuple[raw_api.RawSignalProjectionMappingV1, ...],
    storage: f.MemoryStorageV1 | f.SQLiteStorageV1,
    utc_now: Callable[[], datetime],
) -> f.MeasurementOwnerV1:
    if type(admission) is not f.OwnerAdmissionV1 or not callable(utc_now):
        raise TypeError("exact admission and UTC clock are required")
    if not callable(getattr(raw_projection_reader, "list_projected_raw_history", None)):
        raise TypeError("declared M00 projection reader required")
    state = _Memory()
    groups = (
        (definitions, f.CalculationDefinitionV1),
        (parameter_sets, f.CalculationParameterSetV1),
        (input_selection_policies, f.InputSelectionPolicyVersionV1),
        (unit_conventions, f.UnitConventionVersionV1),
        (raw_projection_mappings, raw_api.RawSignalProjectionMappingV1),
    )
    for records, cls in groups:
        if type(records) is not tuple or any(type(record) is not cls for record in records):
            raise TypeError("exact tuple of declared registration records required")
        for record in records:
            if canonical(record) != canonical(_expected(record)):
                raise ValueError("configuration is outside the accepted controlled D011 payload")
            if isinstance(record, f.CalculationDefinitionV1):
                state.definitions[
                    (record.derived_signal_id, record.calculation_definition_version)
                ] = record
            else:
                state.configuration[_key(record)] = record
    if type(storage) is f.SQLiteStorageV1:
        raise NotImplementedError("G5.2 SQLite durability unit")
    if type(storage) is not f.MemoryStorageV1:
        raise TypeError("explicit writer storage required")
    return _Owner(admission, raw_projection_reader, state, utc_now)


def build_reader(
    *, admission: f.OwnerAdmissionV1, storage: f.SQLiteReadStorageV1
) -> f.MeasurementReadsV1:
    raise NotImplementedError("G5.2 SQLite durability unit")
