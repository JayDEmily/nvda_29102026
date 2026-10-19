"""Additive exact D013 service; original v1 arithmetic and validators are reused unchanged."""

from __future__ import annotations

import hashlib
import json
import re
from collections.abc import Callable
from dataclasses import dataclass, field, fields, is_dataclass, replace
from datetime import datetime
from decimal import Decimal
from math import gcd
from typing import TYPE_CHECKING, Any, get_args, get_origin, get_type_hints

from . import api as f
from ._catalogue import _AUTHORITY, _Configuration, _expected, _key
from ._catalogue import _Memory as _OriginalMemory
from ._evaluation import canonical as original_canonical
from ._evaluation import tagged as original_tagged
from ._evaluation import untagged as original_untagged
from ._sqlite import _validate_occurrence as validate_original_occurrence

if TYPE_CHECKING:
    from ._rational_sqlite import _SQLiteState

BRIEF = "1f53d9c21c6eb4b90213137c4699a0688f994cd0ed55e54082268d8477abc148"
NAMESPACE = "neutral_market_measurement_truth/exact_ratio/v1"
_PREDECESSOR = f.OwnerAdmissionV1(
    "M02", "a31c482d2dc4822539ede99e955761319585af4badea93b9fc279638e1e1f393"
)


def _integer_text(value: int) -> str:
    if not value:
        return "0"
    sign = "-" if value < 0 else ""
    value = abs(value)
    digits = []
    while value:
        value, digit = divmod(value, 10)
        digits.append(chr(48 + digit))
    return sign + "".join(reversed(digits))


def _integer(value: Any) -> int:
    if type(value) is not str or not re.fullmatch(r"(?:0|-?[1-9][0-9]*)", value):
        raise ValueError("canonical exact integer text required")
    negative = value.startswith("-")
    number = 0
    for char in value[1:] if negative else value:
        number = number * 10 + ord(char) - 48
    return -number if negative else number


def tagged(value: Any) -> Any:
    if type(value) is f.ExactRatioV1:
        return dict(
            kind="exact_ratio",
            numerator=_integer_text(value.numerator),
            denominator=_integer_text(value.denominator),
        )
    if is_dataclass(value) and not isinstance(value, type):
        # Preserve v1 opaque identity tags before generic dataclass traversal.
        if type(value).__module__ != f.__name__:
            return original_tagged(value)
        return {item.name: tagged(getattr(value, item.name)) for item in fields(value)}
    if type(value) is tuple:
        return [tagged(item) for item in value]
    if type(value) is dict:
        return {key: tagged(item) for key, item in value.items()}
    return original_tagged(value)


def canonical(value: Any) -> bytes:
    return json.dumps(
        tagged(value), sort_keys=True, ensure_ascii=True, separators=(",", ":"), allow_nan=False
    ).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def untagged(value: Any, hint: Any) -> Any:
    if hint is f.ExactRatioV1:
        if type(value) is not dict or set(value) != {"kind", "numerator", "denominator"}:
            raise ValueError("exact ratio tag required")
        if value["kind"] != "exact_ratio":
            raise ValueError("wrong exact ratio tag")
        return f.ExactRatioV1(_integer(value["numerator"]), _integer(value["denominator"]))
    if get_origin(hint) is tuple:
        if type(value) is not list:
            raise TypeError("stored tuple must be an array")
        args = get_args(hint)
        if len(args) == 2 and args[1] is Ellipsis:
            return tuple(untagged(item, args[0]) for item in value)
        if len(value) != len(args):
            raise ValueError("stored tuple arity mismatch")
        return tuple(untagged(item, cls) for item, cls in zip(value, args, strict=True))
    if hint in (f.PredecessorEvidenceV1, f.RatioCalculationRequestV1, f.RatioOccurrenceV1):
        hints = get_type_hints(hint)
        if type(value) is not dict or set(value) != set(hints):
            raise ValueError("incomplete or extra exact-ratio record fields")
        return hint(**{key: untagged(value[key], cls) for key, cls in hints.items()})
    return original_untagged(value, hint)


def decode(payload: bytes, cls: Any) -> Any:
    value = untagged(json.loads(payload), cls)
    if canonical(value) != payload:
        raise ValueError("noncanonical or lossy exact-ratio representation")
    return value


def _admission(value: f.OwnerAdmissionV1) -> None:
    if type(value) is not f.OwnerAdmissionV1:
        raise TypeError("exact owner admission required")
    if value.object_id != "M02" or value.implementation_brief_sha256 != BRIEF:
        raise ValueError("exact D013 implementation admission required")


def expected_definition(value: f.CalculationDefinitionV1) -> f.CalculationDefinitionV1:
    if type(value) is not f.CalculationDefinitionV1:
        raise TypeError("exact definition required")
    if value.derived_signal_id != "D013" or value.calculation_definition_version not in (
        "D013-RELATIVE-SPREAD-1",
        "D013-RELATIVE-SPREAD-2",
    ):
        raise ValueError("unadmitted D013 definition")
    return f.CalculationDefinitionV1(
        "D013",
        value.calculation_definition_version,
        "K02_ALGEBRA",
        "100 * D012 / D011",
        (),
        ("D011", "D012"),
        "P_BASIC",
        "percent",
        "scalar_exact_ratio",
        tuple(f.AuthorityArtifactRefV1(*ref) for ref in _AUTHORITY),
    )


def expected_parameter(value: f.CalculationParameterSetV1) -> f.CalculationParameterSetV1:
    if type(value) is not f.CalculationParameterSetV1:
        raise TypeError("exact parameter record required")
    return _expected(value, _PREDECESSOR)


def validate_evidence(value: f.PredecessorEvidenceV1, now: datetime) -> None:
    if type(value) is not f.PredecessorEvidenceV1:
        raise TypeError("complete predecessor evidence required")
    # Exact recursive typed/canonical reconstruction; never normalise invalid
    # transient fields or treat Decimal numeric equality as representation identity.
    decode(canonical(value), f.PredecessorEvidenceV1)
    occurrence = value.occurrence
    if occurrence.calculated_at_utc > now:
        raise ValueError("predecessor calculated after this calculation clock")
    records = (
        value.definition,
        value.parameter_set,
        value.input_selection_policy,
        *value.unit_conventions,
        *value.projection_mappings,
    )
    for record in records:
        if original_canonical(record) != original_canonical(_expected(record, _PREDECESSOR)):
            raise ValueError("unadmitted predecessor configuration")
    if len(occurrence.parameter_context_refs) != 2 or len(occurrence.raw_input_lineage) != 2:
        raise ValueError("incomplete predecessor configuration/lineage references")
    state = _OriginalMemory()
    state.definitions[
        (value.definition.derived_signal_id, value.definition.calculation_definition_version)
    ] = value.definition
    configurations: tuple[_Configuration, ...] = (
        value.parameter_set,
        value.input_selection_policy,
        *value.unit_conventions,
        *value.projection_mappings,
    )
    for configuration in configurations:
        key = _key(configuration)
        if key in state.configuration and original_canonical(state.configuration[key]) != (
            original_canonical(configuration)
        ):
            raise ValueError("ambiguous predecessor configuration")
        state.configuration[key] = configuration
    request = f.CalculationRequestV1(
        occurrence.derived_signal_id,
        occurrence.subject_instrument,
        occurrence.effective_as_of_utc,
        occurrence.knowledge_cutoff_utc,
        occurrence.calculation_definition_version,
        occurrence.parameter_context_refs[0],
        occurrence.parameter_context_refs[1],
        (),
        tuple(
            f.RawInputBindingV1(
                item.raw_signal_id, item.projection_mapping_ref, item.unit_convention_ref, "NVDA"
            )
            for item in occurrence.raw_input_lineage
        ),
    )
    logical = dict(
        owner_object_id="M02",
        owner_namespace="neutral_market_measurement_truth/v1",
        implementation_brief_sha256=_PREDECESSOR.implementation_brief_sha256,
        request=request,
        definition_content_sha256=hashlib.sha256(original_canonical(value.definition)).hexdigest(),
        parameter_set=value.parameter_set,
        input_selection_policy=value.input_selection_policy,
        unit_conventions=value.unit_conventions,
        projection_mappings=value.projection_mappings,
        raw_input_lineage=occurrence.raw_input_lineage,
    )
    # Reuse the one v1 identity/equation/content validator, with no SQL access to
    # a predecessor store and no competing midpoint/spread implementation.
    validate_original_occurrence(state, occurrence, original_canonical(logical), _PREDECESSOR)


def capture(reader: f.MeasurementReadsV1, identity: str) -> f.PredecessorEvidenceV1 | None:
    occurrence = reader.get_derived_occurrence(identity)
    if type(occurrence) is not f.DerivedSignalOccurrenceV1:
        return None
    if occurrence.derived_occurrence_id != identity:
        return None
    if len(occurrence.parameter_context_refs) != 2:
        return None
    definition = reader.get_calculation_definition(
        derived_signal_id=occurrence.derived_signal_id,
        calculation_definition_version=occurrence.calculation_definition_version,
    )
    parameter = reader.get_parameter_set(occurrence.parameter_context_refs[0])
    selection = reader.get_input_selection_policy(occurrence.parameter_context_refs[1])
    if definition is None or parameter is None or selection is None:
        return None
    units = []
    for ref in occurrence.convention_refs:
        unit = reader.get_unit_convention(ref)
        if unit is None:
            return None
        units.append(unit)
    mappings = []
    for item in occurrence.raw_input_lineage:
        mapping = reader.get_projection_mapping(item.projection_mapping_ref)
        if mapping is None:
            return None
        mappings.append(mapping)
    return f.PredecessorEvidenceV1(
        occurrence,
        definition,
        parameter,
        selection,
        tuple(units),
        tuple(mappings),
    )


def _ratio(midpoint: Decimal, spread: Decimal) -> f.ExactRatioV1 | None:
    try:
        parts = []
        for value in (midpoint, spread):
            sign, digits, exponent = value.as_tuple()
            coefficient = 0
            for digit in digits:
                coefficient = coefficient * 10 + digit
            parts.append((-coefficient if sign else coefficient, int(exponent)))
        (denominator, de), (numerator, ne) = parts
        if denominator == 0:
            return None
        numerator *= 100
        if ne >= de:
            numerator *= 10 ** (ne - de)
        else:
            denominator *= 10 ** (de - ne)
        if denominator < 0:
            numerator, denominator = -numerator, -denominator
        divisor = gcd(abs(numerator), denominator)
        return f.ExactRatioV1(numerator // divisor, denominator // divisor)
    except (ArithmeticError, MemoryError, ValueError):
        return None


def evaluate(
    request: f.RatioCalculationRequestV1,
    definition: f.CalculationDefinitionV1,
    parameter: f.CalculationParameterSetV1,
    evidence: tuple[f.PredecessorEvidenceV1, ...],
    now: datetime,
) -> tuple[f.RatioOccurrenceV1, bytes] | None:
    if (
        request.derived_signal_id != "D013"
        or request.subject_instrument != "NVDA"
        or not request.as_of_utc <= request.knowledge_cutoff_utc <= now
        or len(evidence) != 2
        or tuple(item.occurrence.derived_signal_id for item in evidence) != ("D011", "D012")
        or tuple(item.occurrence.derived_occurrence_id for item in evidence)
        != (request.predecessor_occurrence_ids)
    ):
        return None
    for item in evidence:
        validate_evidence(item, now)
        occurrence = item.occurrence
        if (
            occurrence.subject_instrument != request.subject_instrument
            or occurrence.effective_as_of_utc != request.as_of_utc
            or occurrence.knowledge_cutoff_utc != request.knowledge_cutoff_utc
            or occurrence.parameter_context_refs[0] != request.parameter_set_ref
            or canonical(item.parameter_set) != canonical(parameter)
        ):
            return None
    first, second = evidence
    if any(
        canonical(left) != canonical(right)
        for left, right in (
            (first.parameter_set, second.parameter_set),
            (first.input_selection_policy, second.input_selection_policy),
            (first.unit_conventions, second.unit_conventions),
            (first.projection_mappings, second.projection_mappings),
            (first.occurrence.raw_input_lineage, second.occurrence.raw_input_lineage),
        )
    ):
        return None
    value = _ratio(first.occurrence.result, second.occurrence.result)
    if value is None:
        return None
    logical = dict(
        owner_object_id="M02",
        owner_namespace=NAMESPACE,
        implementation_brief_sha256=BRIEF,
        request=request,
        definition_content_sha256=digest(definition),
        parameter_set=parameter,
        predecessor_evidence=evidence,
    )
    ratio_occurrence = f.RatioOccurrenceV1(
        "M02",
        NAMESPACE,
        BRIEF,
        "D013",
        "mmtr1:" + digest(logical),
        definition.calculation_definition_version,
        digest(definition),
        (request.parameter_set_ref,),
        "NVDA",
        None,
        request.as_of_utc,
        None,
        request.knowledge_cutoff_utc,
        now,
        value,
        "percent",
        "scalar_exact_ratio",
        (),
        request.predecessor_occurrence_ids,
        (),
        None,
        evidence,
    )
    return ratio_occurrence, canonical(logical)


@dataclass
class _Memory:
    definitions: dict[tuple[str, str], f.CalculationDefinitionV1] = field(default_factory=dict)
    parameters: dict[tuple[str, int], f.CalculationParameterSetV1] = field(default_factory=dict)
    occurrences: dict[str, f.RatioOccurrenceV1] = field(default_factory=dict)
    logical: dict[str, bytes] = field(default_factory=dict)

    def append(self, occurrence: f.RatioOccurrenceV1, logical: bytes) -> f.RatioOccurrenceV1:
        old = self.occurrences.get(occurrence.derived_occurrence_id)
        if old is not None:
            if self.logical[old.derived_occurrence_id] != logical or canonical(old) != canonical(
                replace(occurrence, calculated_at_utc=old.calculated_at_utc)
            ):
                raise f.PersistenceFailureV1("immutable exact-ratio occurrence conflict")
            return old
        self.occurrences[occurrence.derived_occurrence_id] = occurrence
        self.logical[occurrence.derived_occurrence_id] = logical
        return occurrence


def validate_occurrence(
    state: _Memory,
    occurrence: f.RatioOccurrenceV1,
    logical: bytes,
) -> None:
    if type(occurrence) is not f.RatioOccurrenceV1:
        raise TypeError("exact stored ratio occurrence required")
    document = json.loads(logical)
    request = untagged(document["request"], f.RatioCalculationRequestV1)
    definition = state.definitions[
        (request.derived_signal_id, request.calculation_definition_version)
    ]
    parameter = state.parameters[
        (request.parameter_set_ref.context_id, request.parameter_set_ref.version)
    ]
    expected = evaluate(
        request,
        definition,
        parameter,
        occurrence.predecessor_evidence,
        occurrence.calculated_at_utc,
    )
    if (
        expected is None
        or canonical(expected[0]) != canonical(occurrence)
        or expected[1] != logical
    ):
        raise ValueError("stored ratio identity/equation/metadata/evidence mismatch")


class _Reads:
    def __init__(self, state: _Memory | _SQLiteState) -> None:
        self._state = state

    def get_derived_occurrence(self, derived_occurrence_id: str) -> f.RatioOccurrenceV1 | None:
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
    ) -> tuple[f.RatioOccurrenceV1, ...]:
        f._utc(effective_at_or_before_utc)
        f._utc(knowledge_at_or_before_utc)
        if type(limit) is not int:
            raise TypeError("history limit must be an exact integer")
        if not 1 <= limit <= 1000:
            raise ValueError("history limit must be in 1..1000")
        if type(derived_signal_id) is not str or type(subject_instrument) is not str:
            raise TypeError("history identities must be strings")
        if not derived_signal_id or not subject_instrument:
            raise ValueError("history identities must be nonempty")
        return tuple(
            sorted(
                (
                    item
                    for item in self._state.occurrences.values()
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
            )[:limit]
        )

    def get_calculation_definition(
        self,
        *,
        derived_signal_id: str,
        calculation_definition_version: str,
    ) -> f.CalculationDefinitionV1 | None:
        if type(derived_signal_id) is not str or type(calculation_definition_version) is not str:
            raise TypeError("definition identities must be strings")
        if not derived_signal_id or not calculation_definition_version:
            raise ValueError("definition identities must be nonempty")
        return self._state.definitions.get((derived_signal_id, calculation_definition_version))

    def get_parameter_set(self, ref: f.VersionRefV1) -> f.CalculationParameterSetV1 | None:
        if type(ref) is not f.VersionRefV1:
            raise TypeError("exact parameter reference required")
        return self._state.parameters.get((ref.context_id, ref.version))


class _Owner:
    def __init__(
        self,
        reader: f.MeasurementReadsV1,
        state: _Memory | _SQLiteState,
        clock: Callable[[], datetime],
    ) -> None:
        self._reader, self._state, self._clock = reader, state, clock
        self._reads = _Reads(state)

    @property
    def reads(self) -> f.MeasurementRatioReadsV1:
        return self._reads

    def materialise(self, request: f.RatioCalculationRequestV1) -> f.RatioOccurrenceV1 | None:
        if type(request) is not f.RatioCalculationRequestV1:
            raise TypeError("exact ratio request required")
        now = self._clock()
        f._utc(now)
        if (
            request.derived_signal_id != "D013"
            or request.subject_instrument != "NVDA"
            or not request.as_of_utc <= request.knowledge_cutoff_utc <= now
        ):
            return None
        definition = self._state.definitions.get(
            (request.derived_signal_id, request.calculation_definition_version)
        )
        parameter = self._state.parameters.get(
            (request.parameter_set_ref.context_id, request.parameter_set_ref.version)
        )
        if definition is None or parameter is None:
            return None
        try:
            captures = tuple(
                capture(self._reader, identity) for identity in request.predecessor_occurrence_ids
            )
            if any(item is None for item in captures):
                return None
            evidence = tuple(item for item in captures if item is not None)
            result = evaluate(request, definition, parameter, evidence, now)
        except (TypeError, ValueError, KeyError, AttributeError, ArithmeticError, MemoryError):
            return None
        if result is None:
            return None
        return self._state.append(*result)


def build_owner(
    *,
    admission: f.OwnerAdmissionV1,
    predecessor_reader: f.MeasurementReadsV1,
    definitions: tuple[f.CalculationDefinitionV1, ...],
    parameter_sets: tuple[f.CalculationParameterSetV1, ...],
    storage: f.MemoryStorageV1 | f.SQLiteStorageV1,
    utc_now: Callable[[], datetime],
) -> f.MeasurementRatioOwnerV1:
    _admission(admission)
    if not callable(utc_now):
        raise TypeError("UTC clock required")
    for method in (
        "get_derived_occurrence",
        "get_calculation_definition",
        "get_parameter_set",
        "get_input_selection_policy",
        "get_unit_convention",
        "get_projection_mapping",
    ):
        if not callable(getattr(predecessor_reader, method, None)):
            raise TypeError("declared complete v1 predecessor read facet required")
    state = _Memory()
    for records, cls in (
        (definitions, f.CalculationDefinitionV1),
        (parameter_sets, f.CalculationParameterSetV1),
    ):
        if type(records) is not tuple or any(type(value) is not cls for value in records):
            raise TypeError("exact tuple of registration records required")
    for definition in definitions:
        if canonical(definition) != canonical(expected_definition(definition)):
            raise ValueError("unsupported exact-ratio definition payload")
        state.definitions[
            (definition.derived_signal_id, definition.calculation_definition_version)
        ] = definition
    for parameter in parameter_sets:
        if canonical(parameter) != canonical(expected_parameter(parameter)):
            raise ValueError("unsupported exact-ratio parameter payload")
        state.parameters[(parameter.context_id, parameter.version)] = parameter
    if type(storage) is f.SQLiteStorageV1:
        from ._rational_sqlite import create_state

        return _Owner(predecessor_reader, create_state(storage, admission, state), utc_now)
    if type(storage) is not f.MemoryStorageV1:
        raise TypeError("explicit ratio writer storage required")
    return _Owner(predecessor_reader, state, utc_now)


def build_reader(
    *,
    admission: f.OwnerAdmissionV1,
    storage: f.SQLiteReadStorageV1,
) -> f.MeasurementRatioReadsV1:
    _admission(admission)
    if type(storage) is not f.SQLiteReadStorageV1:
        raise TypeError("exact read-only storage required")
    from ._rational_sqlite import _SQLiteState

    state = _SQLiteState(storage.database_path, admission)
    state.snapshot()
    return _Reads(state)
