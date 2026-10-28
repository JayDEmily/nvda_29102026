"""D138 receipt-only native-side OLS slopes over actual unchanged public D011."""

from __future__ import annotations

import hashlib
from collections.abc import Callable
from dataclasses import fields, replace
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from fractions import Fraction
from typing import cast

from nvda_desk.raw_signal_occurrence_truth import api as raw

from . import _native_codec as codec
from . import _native_source as source_module
from . import api as f
from ._catalogue import _AUTHORITY
from ._evaluation import digest
from ._record_store import RecordState
from ._selection import eligible

BRIEF = "cd2519685a80a453b839ac10a34d8488f73b8b1b87ef01a10c346e1445f5130b"
NAMESPACE = "neutral_market_measurement_truth/native-d138/v1"
PROFILE = f.VersionRefV1("native-d138-slope", 1)
T = datetime(2026, 10, 16, 1, tzinfo=UTC)
CUTOFF = T + timedelta(seconds=1)
DEFINITION = f.CalculationDefinitionV1(
    "D138", "D138-NATIVE-THREE-LEVEL-OLS-1", "K06_REGRESSION_DEPENDENCE",
    "OLS(cumulative standing depth, abs(price - actual D011 midpoint)) per native side",
    ("R185", "R187", "R188", "R189", "R190"), ("D011",), "P_REGRESSION",
    "depth per price distance", "book_slope_pair",
    tuple(f.AuthorityArtifactRefV1(*value) for value in _AUTHORITY))

# These are the unchanged admitted public D011 configurations, not a new
# predecessor profile. They also permit full nested-record validation on reopen.
_D011_BRIEF = "3ad4cdc9ffba4cf91ff9a27edf1dd3b1a9824a421514bb4b5a2cc1b9c504f233"
_PARENT_DEFINITION = f.CalculationDefinitionV1(
    "D011", "D011-MIDPOINT-1", "K02_ALGEBRA", "(R034 + R035) / 2",
    ("R034", "R035"), (), "P_BASIC", "price", "scalar_decimal",
    tuple(f.AuthorityArtifactRefV1(*value) for value in _AUTHORITY))
_PARAMETER = f.CalculationParameterSetV1("mmt-pilot-basic", 1, "P_BASIC", "NVDA", ("NVDA",))
_POLICY = f.InputSelectionPolicyVersionV1(
    "mmt-pilot-selection", 1, ("subject_instrument",), timedelta(seconds=60),
    timedelta(seconds=10), ("true_instant",), (), "foundation-pilot-fixture",
    "cash_quote_v1", "foundation-pilot-fixture/cash_quote_v1", 100, 1000)
_UNIT = f.UnitConventionVersionV1("mmt-pilot-price", 1, "price", "price", Decimal(1), Decimal(0))
_MAPS = tuple(raw.RawSignalProjectionMappingV1(
    "mmt-pilot-"+field, 1, raw.RawSignalCatalogueId(rid), "foundation-pilot-fixture",
    "cash_quote_v1", ("quote", field), "price", ())
    for rid, field in (("R034", "bid"), ("R035", "ask")))


def _parent_request() -> f.CalculationRequestV1:
    return f.CalculationRequestV1(
        "D011", "NVDA", T, CUTOFF, "D011-MIDPOINT-1",
        f.VersionRefV1("mmt-pilot-basic", 1), f.VersionRefV1("mmt-pilot-selection", 1), (),
        tuple(f.RawInputBindingV1(m.raw_signal_catalogue_id.value,
              f.VersionRefV1(m.mapping_id, 1), f.VersionRefV1("mmt-pilot-price", 1), "NVDA")
              for m in _MAPS))


def _request_check(request: f.NativeCalculationRequestV1) -> None:
    if (type(request) is not f.NativeCalculationRequestV1
        or request.derived_signal_id != "D138" or request.source_profile_ref != PROFILE
        or request.as_of_utc != T or request.knowledge_cutoff_utc != CUTOFF
        or type(request.depth_levels) is not int or request.depth_levels != 3
        or request.band is not None or request.window_seconds is not None
        or request.side is not None or request.positions
        or len(request.predecessor_occurrence_ids) != 1
        or type(request.predecessor_occurrence_ids[0]) is not str
        or not request.predecessor_occurrence_ids[0]):
        raise ValueError("unadmitted native D138 three-level request")


def _parent_check(parent: f.DerivedSignalOccurrenceV1, identity: str, now: datetime) -> None:
    if type(parent) is not f.DerivedSignalOccurrenceV1:
        raise TypeError("actual public D011 record required")
    f._Validated.__post_init__(parent)
    request = _parent_request()
    if (parent.derived_occurrence_id != identity or parent.owner_object_id != "M02"
        or parent.owner_namespace != "neutral_market_measurement_truth/v1"
        or parent.implementation_brief_sha256 != _D011_BRIEF
        or parent.derived_signal_id != "D011"
        or parent.calculation_definition_version != "D011-MIDPOINT-1"
        or parent.definition_content_sha256 != digest(_PARENT_DEFINITION)
        or parent.parameter_context_refs != (request.parameter_set_ref, request.input_selection_policy_ref)
        or parent.subject_instrument != "NVDA" or parent.universe is not None
        or parent.effective_as_of_utc != T or parent.knowledge_cutoff_utc != CUTOFF
        or not CUTOFF <= parent.calculated_at_utc <= now
        or parent.window is not None or parent.predecessor_occurrence_ids
        or parent.convention_refs != (f.VersionRefV1("mmt-pilot-price", 1),)
        or parent.supersedes_derived_occurrence_id is not None
        or parent.units != "price" or parent.result_shape != "scalar_decimal"
        or type(parent.result) is not Decimal or parent.result != Decimal(100)
        or len(parent.raw_input_lineage) != 2):
        raise ValueError("D011 exact admitted context mismatch")
    for line, mapping, binding in zip(parent.raw_input_lineage, _MAPS,
                                       request.raw_input_bindings, strict=True):
        f._Validated.__post_init__(line)
        if (line.raw_signal_id != binding.raw_signal_id
            or line.projection_mapping_ref != binding.projection_mapping_ref
            or line.unit_convention_ref != binding.unit_convention_ref
            or eligible(line.projection, mapping, _POLICY, request) != line.event_time_utc
            or codec.canonical(line.canonical_value) != codec.canonical(line.projection.native_value)):
            raise ValueError("D011 exact public lineage mismatch")
    first, second = parent.raw_input_lineage
    if (abs(first.event_time_utc-second.event_time_utc) > _POLICY.maximum_skew
        or (Fraction(first.canonical_value)+Fraction(second.canonical_value))/2 != Fraction(parent.result)):
        raise ValueError("D011 midpoint or source skew mismatch")
    payload = dict(owner_object_id="M02", owner_namespace=parent.owner_namespace,
        implementation_brief_sha256=_D011_BRIEF, request=request,
        definition_content_sha256=digest(_PARENT_DEFINITION), parameter_set=_PARAMETER,
        input_selection_policy=_POLICY, unit_conventions=(_UNIT,), projection_mappings=_MAPS,
        raw_input_lineage=parent.raw_input_lineage)
    if parent.derived_occurrence_id != "mmt1:"+digest(payload):
        raise ValueError("D011 full semantic identity mismatch")


def _slope(rows: tuple[f.NativeBookRowV1, ...], midpoint: Fraction, side: int) -> f.ExactRatioV1:
    selected = tuple(row for row in rows if row.side == side)
    if (tuple(row.position for row in selected) != (0, 1, 2)
        or any(row.price is None or row.price <= 0 for row in selected)):
        raise ValueError("complete priced three-level native book required")
    prices = tuple(Fraction(cast(Decimal, row.price)) for row in selected)
    if (any(price >= midpoint for price in prices) if side == 1
        else any(price <= midpoint for price in prices)):
        raise ValueError("native side lies on wrong midpoint side")
    if any((prices[i] <= prices[i+1]) if side == 1 else (prices[i] >= prices[i+1])
           for i in range(2)):
        raise ValueError("native bid/ask price ladder mismatch")
    xs = tuple(abs(price-midpoint) for price in prices)
    cumulative = []
    total = Fraction(0)
    for row in selected:
        total += Fraction(row.size)
        cumulative.append(total)
    n = len(xs)
    numerator = n*sum((x*y for x, y in zip(xs, cumulative, strict=True)), Fraction(0)) \
        - sum(xs)*sum(cumulative)
    denominator = n*sum((x*x for x in xs), Fraction(0))-sum(xs)**2
    if denominator <= 0:
        raise ValueError("degenerate OLS distance")
    answer = numerator/denominator
    return f.ExactRatioV1(answer.numerator, answer.denominator)


def _identity(value: f.NativeMeasurementOccurrenceV1) -> str:
    payload = {field.name: getattr(value, field.name) for field in fields(value)
               if field.name not in ("derived_occurrence_id", "calculated_at_utc")}
    return "mmtnative-d138:"+hashlib.sha256(codec.canonical(payload)).hexdigest()


def _produce(request: f.NativeCalculationRequestV1, source: f.NativeSourceSnapshotV1,
             parent: f.DerivedSignalOccurrenceV1, now: datetime) -> f.NativeMeasurementOccurrenceV1:
    _request_check(request)
    f._utc(now)
    if now < CUTOFF:
        raise ValueError("calculation precedes knowledge cutoff")
    _parent_check(parent, request.predecessor_occurrence_ids[0], now)
    source_module._validate(source)
    if (source.request != f.NativeSourceRequestV1(PROFILE, T, CUTOFF)
        or source.profile.ref != PROFILE or source.profile.subject_instrument != parent.subject_instrument
        or source.calculated_at_utc > now or len(source.standing_rows) != 6):
        raise ValueError("D138 exact native source context mismatch")
    midpoint = Fraction(parent.result)
    result = f.BookSlopePairV1(_slope(source.standing_rows, midpoint, 1),
                               _slope(source.standing_rows, midpoint, 0))
    value = f.NativeMeasurementOccurrenceV1(
        "M02", NAMESPACE, BRIEF, "D138", "pending", request, DEFINITION, source, None, (parent,),
        tuple(row.observation_occurrence_id for row in source.standing_rows), result,
        DEFINITION.units, DEFINITION.result_shape, T, CUTOFF, now)
    return replace(value, derived_occurrence_id=_identity(value))


def _validate(value: f.NativeMeasurementOccurrenceV1) -> None:
    if type(value) is not f.NativeMeasurementOccurrenceV1:
        raise TypeError("exact native D138 occurrence required")
    f._Validated.__post_init__(value)
    if (value.owner_object_id != "M02" or value.owner_namespace != NAMESPACE
        or value.implementation_brief_sha256 != BRIEF or value.derived_signal_id != "D138"
        or value.definition != DEFINITION or value.source is None
        or value.quote_assembly is not None or len(value.predecessors) != 1
        or type(value.predecessors[0]) is not f.DerivedSignalOccurrenceV1
        or type(value.result) is not f.BookSlopePairV1
        or codec.canonical(value) != codec.canonical(_produce(value.request, value.source,
             cast(f.DerivedSignalOccurrenceV1, value.predecessors[0]), value.calculated_at_utc))):
        raise ValueError("D138 full source/predecessor/result identity mismatch")


class _Reads:
    def __init__(self, state: RecordState) -> None:
        self.state = state

    def get_derived_occurrence(self, derived_occurrence_id: str) -> f.NativeMeasurementOccurrenceV1 | None:
        if type(derived_occurrence_id) is not str or not derived_occurrence_id:
            raise ValueError("nonempty D138 identity required")
        return next((v for v in self.state.all() if v.derived_occurrence_id == derived_occurrence_id), None)

    def list_derived_history(self, *, derived_signal_id: str, subject_instrument: str,
        effective_at_or_before_utc: datetime, knowledge_at_or_before_utc: datetime,
        limit: int) -> tuple[f.NativeMeasurementOccurrenceV1, ...]:
        f._utc(effective_at_or_before_utc)
        f._utc(knowledge_at_or_before_utc)
        if (derived_signal_id != "D138" or type(subject_instrument) is not str
            or not subject_instrument or type(limit) is not int or limit <= 0):
            raise ValueError("bounded native D138 history request required")
        rows = (v for v in self.state.all() if v.source is not None
                and v.source.profile.subject_instrument == subject_instrument
                and v.effective_as_of_utc <= effective_at_or_before_utc
                and v.knowledge_cutoff_utc <= knowledge_at_or_before_utc)
        return tuple(sorted(rows, key=lambda v: (v.effective_as_of_utc,
            v.knowledge_cutoff_utc, v.derived_occurrence_id), reverse=True))[:limit]


class _Owner:
    def __init__(self, raw_reader: f.NativeRawReaderV1, predecessor_reader: f.MeasurementReadsV1,
                 state: RecordState, utc_now: Callable[[], datetime]) -> None:
        self.raw_reader, self.predecessor_reader = raw_reader, predecessor_reader
        self.state, self.utc_now = state, utc_now
        self.reads = _Reads(state)

    def materialise(self, request: f.NativeCalculationRequestV1) -> f.NativeMeasurementOccurrenceV1 | None:
        _request_check(request)
        now = self.utc_now()
        f._utc(now)
        if now < CUTOFF:
            raise ValueError("calculation precedes knowledge cutoff")
        parent = self.predecessor_reader.get_derived_occurrence(request.predecessor_occurrence_ids[0])
        if type(parent) is not f.DerivedSignalOccurrenceV1:
            return None
        source = source_module.build_owner(f.OwnerAdmissionV1("M02", source_module.BRIEF),
            self.raw_reader, f.MemoryStorageV1(), lambda: now).materialise(
                f.NativeSourceRequestV1(PROFILE, T, CUTOFF))
        if source is None:
            return None
        try:
            value = _produce(request, source, parent, now)
        except (ValueError, TypeError, ArithmeticError):
            return None
        return cast(f.NativeMeasurementOccurrenceV1, self.state.append(value))


def _state(storage: f.MemoryStorageV1 | f.SQLiteStorageV1 | f.SQLiteReadStorageV1) -> RecordState:
    return RecordState(storage, lambda payload: codec.decode(payload, f.NativeMeasurementOccurrenceV1),
                       _validate, encode=codec.canonical)


def build_owner(admission: f.OwnerAdmissionV1, raw_reader: f.NativeRawReaderV1,
                predecessor_reader: f.MeasurementReadsV1, storage: f.MemoryStorageV1 | f.SQLiteStorageV1,
                utc_now: Callable[[], datetime]) -> f.NativeMeasurementOwnerV1:
    if (type(admission) is not f.OwnerAdmissionV1 or admission.object_id != "M02"
        or admission.implementation_brief_sha256 != BRIEF
        or type(storage) not in (f.MemoryStorageV1, f.SQLiteStorageV1) or not callable(utc_now)
        or not callable(getattr(raw_reader, "list_projected_raw_history", None))
        or not callable(getattr(raw_reader, "list_raw_observation_history", None))
        or not callable(getattr(predecessor_reader, "get_derived_occurrence", None))):
        raise ValueError("native D138 admission/public source/predecessor mismatch")
    return _Owner(raw_reader, predecessor_reader, _state(storage), utc_now)


def build_reader(admission: f.OwnerAdmissionV1,
                 storage: f.SQLiteReadStorageV1) -> f.NativeMeasurementReadsV1:
    if (type(admission) is not f.OwnerAdmissionV1 or admission.object_id != "M02"
        or admission.implementation_brief_sha256 != BRIEF or type(storage) is not f.SQLiteReadStorageV1):
        raise ValueError("native D138 read-only admission mismatch")
    return _Reads(_state(storage))
