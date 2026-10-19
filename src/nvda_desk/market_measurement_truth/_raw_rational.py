"""Fixed controlled D014 direct-raw ratio; old owners and codecs remain unchanged."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field, replace
from datetime import datetime, timedelta
from decimal import Decimal
from math import gcd
from typing import Protocol

from nvda_desk.raw_signal_occurrence_truth import api as raw_api

from . import api as f
from ._catalogue import _AUTHORITY, _Configuration, _key
from ._rational import canonical, digest, untagged
from ._selection import eligible, select

BRIEF = "c23ea315c94b478c568f105e94891a03af62393792a1478c33027a0371738bb8"
NAMESPACE = "neutral_market_measurement_truth/raw_exact_ratio/v1"


def admission_check(admission: f.OwnerAdmissionV1) -> None:
    if type(admission) is not f.OwnerAdmissionV1:
        raise TypeError("exact owner admission required")
    if admission.object_id != "M02" or admission.implementation_brief_sha256 != BRIEF:
        raise ValueError("exact D014 implementation admission required")


def expected_definition(value: f.CalculationDefinitionV1) -> f.CalculationDefinitionV1:
    if value.derived_signal_id != "D014" or value.calculation_definition_version not in (
        "D014-SIZE-IMBALANCE-1",
        "D014-SIZE-IMBALANCE-2",
    ):
        raise ValueError("unadmitted D014 definition")
    return f.CalculationDefinitionV1(
        "D014",
        value.calculation_definition_version,
        "K02_ALGEBRA",
        "(R033 - R036) / (R033 + R036)",
        ("R033", "R036"),
        (),
        "P_BASIC",
        "-1 to 1",
        "scalar_exact_ratio",
        tuple(f.AuthorityArtifactRefV1(*ref) for ref in _AUTHORITY),
    )


def expected_configuration(value: _Configuration) -> _Configuration:
    if type(value.version) is not int or value.version not in (1, 2):
        raise ValueError("unadmitted D014 configuration version")
    version = value.version
    if isinstance(value, f.CalculationParameterSetV1):
        return f.CalculationParameterSetV1("mmt-size-basic", version, "P_BASIC", "NVDA", ("NVDA",))
    if isinstance(value, f.InputSelectionPolicyVersionV1):
        return f.InputSelectionPolicyVersionV1(
            "mmt-size-selection",
            version,
            ("subject_instrument",),
            timedelta(seconds=60),
            timedelta(seconds=10),
            ("true_instant",),
            (),
            "foundation-size-fixture",
            "cash_size_v1",
            "foundation-size-fixture/cash_size_v1",
            100,
            1000,
        )
    if isinstance(value, f.UnitConventionVersionV1):
        return f.UnitConventionVersionV1(
            "mmt-size-shares", version, "shares", "shares", Decimal("1"), Decimal("0")
        )
    if value.mapping_id not in ("mmt-size-bid", "mmt-size-ask"):
        raise ValueError("unadmitted D014 projection mapping")
    bid = value.mapping_id == "mmt-size-bid"
    return raw_api.RawSignalProjectionMappingV1(
        value.mapping_id,
        version,
        raw_api.RawSignalCatalogueId("R033" if bid else "R036"),
        "foundation-size-fixture",
        "cash_size_v1",
        ("quote", "bid_size" if bid else "ask_size"),
        "shares",
        (),
    )


def exact_ratio(bid: Decimal, ask: Decimal) -> f.ExactRatioV1 | None:
    """Signed fixed difference/sum of aligned integer coefficients, without rounding."""
    try:
        if not bid.is_finite() or not ask.is_finite():
            return None

        def coefficient(value: Decimal) -> tuple[int, int]:
            sign, digits, exponent = value.as_tuple()
            number = 0
            for digit in digits:
                number = number * 10 + digit
            return (-number if sign else number), int(exponent)

        a, ae = coefficient(bid)
        b, be = coefficient(ask)
        exponent = min(ae, be)
        a *= 10 ** (ae - exponent)
        b *= 10 ** (be - exponent)
        numerator, denominator = a - b, a + b
        if denominator == 0:
            return None
        if denominator < 0:
            numerator, denominator = -numerator, -denominator
        common = gcd(abs(numerator), denominator)
        return f.ExactRatioV1(numerator // common, denominator // common)
    except (ArithmeticError, ValueError, MemoryError):
        return None


@dataclass
class _Memory:
    definitions: dict[tuple[str, str], f.CalculationDefinitionV1] = field(default_factory=dict)
    configuration: dict[tuple[str, str, int], _Configuration] = field(default_factory=dict)
    occurrences: dict[str, f.RawRatioOccurrenceV1] = field(default_factory=dict)
    logical: dict[str, bytes] = field(default_factory=dict)

    def snapshot(self) -> _Memory:
        return self

    def append(self, occurrence: f.RawRatioOccurrenceV1, logical: bytes) -> f.RawRatioOccurrenceV1:
        validate_occurrence(self, occurrence, logical)
        old = self.occurrences.get(occurrence.derived_occurrence_id)
        if old is not None:
            if self.logical[old.derived_occurrence_id] != logical or canonical(old) != canonical(
                replace(occurrence, calculated_at_utc=old.calculated_at_utc)
            ):
                raise f.PersistenceFailureV1("immutable raw-ratio occurrence conflict")
            return old
        self.occurrences[occurrence.derived_occurrence_id] = occurrence
        self.logical[occurrence.derived_occurrence_id] = logical
        return occurrence


class _Storage(Protocol):
    def snapshot(self) -> _Memory: ...
    def append(
        self, occurrence: f.RawRatioOccurrenceV1, logical: bytes
    ) -> f.RawRatioOccurrenceV1: ...


def context(
    state: _Memory,
    request: f.CalculationRequestV1,
    now: datetime,
) -> (
    tuple[
        f.CalculationDefinitionV1,
        f.CalculationParameterSetV1,
        f.InputSelectionPolicyVersionV1,
        tuple[raw_api.RawSignalProjectionMappingV1, ...],
        tuple[f.UnitConventionVersionV1, ...],
    ]
    | None
):
    if (
        request.derived_signal_id != "D014"
        or request.subject_instrument != "NVDA"
        or request.context_refs
        or not request.as_of_utc <= request.knowledge_cutoff_utc <= now
        or tuple(item.raw_signal_id for item in request.raw_input_bindings) != ("R033", "R036")
    ):
        return None
    definition = state.definitions.get(("D014", request.calculation_definition_version))
    parameter = state.configuration.get(
        ("parameter", request.parameter_set_ref.context_id, request.parameter_set_ref.version)
    )
    policy = state.configuration.get(
        (
            "selection",
            request.input_selection_policy_ref.context_id,
            request.input_selection_policy_ref.version,
        )
    )
    if (
        definition is None
        or not isinstance(parameter, f.CalculationParameterSetV1)
        or not isinstance(policy, f.InputSelectionPolicyVersionV1)
    ):
        return None
    mappings = []
    units = {}
    for binding in request.raw_input_bindings:
        mapping = state.configuration.get(
            (
                "raw_mapping",
                binding.projection_mapping_ref.context_id,
                binding.projection_mapping_ref.version,
            )
        )
        unit = state.configuration.get(
            ("unit", binding.unit_convention_ref.context_id, binding.unit_convention_ref.version)
        )
        if (
            not isinstance(mapping, raw_api.RawSignalProjectionMappingV1)
            or not isinstance(unit, f.UnitConventionVersionV1)
            or mapping.raw_signal_catalogue_id.value != binding.raw_signal_id
            or binding.subject_instrument != "NVDA"
        ):
            return None
        mappings.append(mapping)
        units[(unit.context_id, unit.version)] = unit
    return (
        definition,
        parameter,
        policy,
        tuple(mappings),
        tuple(units[key] for key in sorted(units)),
    )


def produce(
    state: _Memory,
    request: f.CalculationRequestV1,
    lineage: tuple[f.RawInputLineageV1, ...],
    now: datetime,
) -> tuple[f.RawRatioOccurrenceV1, bytes] | None:
    selected = context(state, request, now)
    if selected is None or len(lineage) != 2:
        return None
    definition, parameter, policy, mappings, units = selected
    for binding, mapping, item in zip(request.raw_input_bindings, mappings, lineage, strict=True):
        when = eligible(item.projection, mapping, policy, request)
        if (
            when is None
            or when != item.event_time_utc
            or item.raw_signal_id != binding.raw_signal_id
            or item.projection_mapping_ref != binding.projection_mapping_ref
            or item.unit_convention_ref != binding.unit_convention_ref
            or canonical(item.canonical_value) != canonical(item.projection.native_value)
        ):
            return None
    if abs(lineage[0].event_time_utc - lineage[1].event_time_utc) > policy.maximum_skew:
        return None
    value = exact_ratio(lineage[0].canonical_value, lineage[1].canonical_value)
    if value is None:
        return None
    payload = dict(
        owner_object_id="M02",
        owner_namespace=NAMESPACE,
        implementation_brief_sha256=BRIEF,
        request=request,
        definition_content_sha256=digest(definition),
        parameter_set=parameter,
        input_selection_policy=policy,
        unit_conventions=units,
        projection_mappings=mappings,
        raw_input_lineage=lineage,
    )
    occurrence = f.RawRatioOccurrenceV1(
        "M02",
        NAMESPACE,
        BRIEF,
        "D014",
        "mmtraw1:" + digest(payload),
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
        "-1 to 1",
        "scalar_exact_ratio",
        lineage,
        (),
        tuple(f.VersionRefV1(unit.context_id, unit.version) for unit in units),
        None,
    )
    return occurrence, canonical(payload)


def validate_occurrence(state: _Memory, occurrence: f.RawRatioOccurrenceV1, logical: bytes) -> None:
    import json

    document = json.loads(logical)
    request = untagged(document["request"], f.CalculationRequestV1)
    expected = produce(state, request, occurrence.raw_input_lineage, occurrence.calculated_at_utc)
    if (
        expected is None
        or canonical(expected[0]) != canonical(occurrence)
        or expected[1] != logical
    ):
        raise ValueError("complete raw-ratio occurrence disagrees with immutable logical content")


class _Reads:
    def __init__(self, state: _Storage) -> None:
        self._state = state

    def get_derived_occurrence(self, derived_occurrence_id: str) -> f.RawRatioOccurrenceV1 | None:
        if type(derived_occurrence_id) is not str:
            raise TypeError("exact string occurrence identity required")
        if not derived_occurrence_id:
            raise ValueError("nonempty occurrence identity required")
        return self._state.snapshot().occurrences.get(derived_occurrence_id)

    def list_derived_history(
        self,
        *,
        derived_signal_id: str,
        subject_instrument: str,
        effective_at_or_before_utc: datetime,
        knowledge_at_or_before_utc: datetime,
        limit: int,
    ) -> tuple[f.RawRatioOccurrenceV1, ...]:
        if (
            type(derived_signal_id) is not str
            or type(subject_instrument) is not str
            or type(limit) is not int
        ):
            raise TypeError("exact history argument types required")
        if not derived_signal_id or not subject_instrument or not 1 <= limit <= 1000:
            raise ValueError("invalid history bound or identity")
        f._utc(effective_at_or_before_utc)
        f._utc(knowledge_at_or_before_utc)
        return tuple(
            sorted(
                (
                    item
                    for item in self._state.snapshot().occurrences.values()
                    if item.derived_signal_id == derived_signal_id
                    and item.subject_instrument == subject_instrument
                    and item.effective_as_of_utc <= effective_at_or_before_utc
                    and item.knowledge_cutoff_utc <= knowledge_at_or_before_utc
                ),
                key=lambda item: (
                    item.effective_as_of_utc,
                    item.knowledge_cutoff_utc,
                    item.derived_occurrence_id,
                ),
                reverse=True,
            )
        )[:limit]

    def get_calculation_definition(
        self,
        *,
        derived_signal_id: str,
        calculation_definition_version: str,
    ) -> f.CalculationDefinitionV1 | None:
        if type(derived_signal_id) is not str or type(calculation_definition_version) is not str:
            raise TypeError("exact definition identity types required")
        if not derived_signal_id or not calculation_definition_version:
            raise ValueError("nonempty definition identities required")
        return self._state.snapshot().definitions.get(
            (derived_signal_id, calculation_definition_version)
        )

    def _configuration(self, kind: str, ref: f.VersionRefV1) -> _Configuration | None:
        if type(ref) is not f.VersionRefV1:
            raise TypeError("exact version reference required")
        return self._state.snapshot().configuration.get((kind, ref.context_id, ref.version))

    def get_parameter_set(self, ref: f.VersionRefV1) -> f.CalculationParameterSetV1 | None:
        value = self._configuration("parameter", ref)
        return value if isinstance(value, f.CalculationParameterSetV1) else None

    def get_input_selection_policy(
        self, ref: f.VersionRefV1
    ) -> f.InputSelectionPolicyVersionV1 | None:
        value = self._configuration("selection", ref)
        return value if isinstance(value, f.InputSelectionPolicyVersionV1) else None

    def get_unit_convention(self, ref: f.VersionRefV1) -> f.UnitConventionVersionV1 | None:
        value = self._configuration("unit", ref)
        return value if isinstance(value, f.UnitConventionVersionV1) else None

    def get_projection_mapping(
        self, ref: f.VersionRefV1
    ) -> raw_api.RawSignalProjectionMappingV1 | None:
        value = self._configuration("raw_mapping", ref)
        return value if isinstance(value, raw_api.RawSignalProjectionMappingV1) else None


class _Owner:
    def __init__(
        self, reader: f.RawProjectionReaderV1, state: _Storage, clock: Callable[[], datetime]
    ) -> None:
        self._reader, self._state, self._clock = reader, state, clock
        self._reads = _Reads(state)

    @property
    def reads(self) -> f.MeasurementRawRatioReadsV1:
        return self._reads

    def materialise(self, request: f.CalculationRequestV1) -> f.RawRatioOccurrenceV1 | None:
        if type(request) is not f.CalculationRequestV1:
            raise TypeError("exact calculation request required")
        now = self._clock()
        f._utc(now)
        state = self._state.snapshot()
        selected_context = context(state, request, now)
        if selected_context is None:
            return None
        _, _, policy, mappings, _ = selected_context
        lineage = []
        for binding, mapping in zip(request.raw_input_bindings, mappings, strict=True):
            selected = select(self._reader, mapping, policy, request)
            if selected is None:
                return None
            projected, event = selected
            native = projected.native_value
            if not isinstance(native, Decimal):
                return None
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
        result = produce(state, request, tuple(lineage), now)
        return None if result is None else self._state.append(*result)


def _register(
    state: _Memory, records: tuple[_Configuration, ...], cls: type[_Configuration]
) -> None:
    if type(records) is not tuple or any(type(record) is not cls for record in records):
        raise TypeError("exact tuple of configuration records required")
    for record in records:
        if canonical(record) != canonical(expected_configuration(record)):
            raise ValueError("unadmitted D014 configuration content")
        state.configuration[_key(record)] = record


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
) -> f.MeasurementRawRatioOwnerV1:
    admission_check(admission)
    if not callable(utc_now) or not callable(
        getattr(raw_projection_reader, "list_projected_raw_history", None)
    ):
        raise TypeError("declared public raw reader and UTC clock required")
    if type(definitions) is not tuple or any(
        type(value) is not f.CalculationDefinitionV1 for value in definitions
    ):
        raise TypeError("exact tuple of definitions required")
    state = _Memory()
    for definition in definitions:
        if canonical(definition) != canonical(expected_definition(definition)):
            raise ValueError("unadmitted D014 definition content")
        state.definitions[
            (definition.derived_signal_id, definition.calculation_definition_version)
        ] = definition
    _register(state, parameter_sets, f.CalculationParameterSetV1)
    _register(state, input_selection_policies, f.InputSelectionPolicyVersionV1)
    _register(state, unit_conventions, f.UnitConventionVersionV1)
    _register(state, raw_projection_mappings, raw_api.RawSignalProjectionMappingV1)
    if type(storage) is f.MemoryStorageV1:
        return _Owner(raw_projection_reader, state, utc_now)
    if type(storage) is f.SQLiteStorageV1:
        from ._raw_rational_sqlite import create_state

        return _Owner(raw_projection_reader, create_state(storage, admission, state), utc_now)
    raise TypeError("declared memory or SQLite writer storage required")


def build_reader(
    *, admission: f.OwnerAdmissionV1, storage: f.SQLiteReadStorageV1
) -> f.MeasurementRawRatioReadsV1:
    admission_check(admission)
    if type(storage) is not f.SQLiteReadStorageV1:
        raise TypeError("declared readonly SQLite storage required")
    from ._raw_rational_sqlite import _SQLiteState

    state = _SQLiteState(storage.database_path, admission)
    state.snapshot()
    return _Reads(state)
