"""D105 complete synthetic 365-prior-daily comparable-IV rank owner."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import replace
from datetime import datetime, timedelta
from decimal import Decimal
from fractions import Fraction
from typing import cast

from nvda_desk.raw_signal_occurrence_truth import api as r

from . import api as f
from ._catalogue import _AUTHORITY
from ._evaluation import canonical
from ._option_scalars import T
from ._option_skew import source_event
from ._record_store import RecordState
from ._selection import eligible
from ._vwap_returns import history
from ._window import NAMESPACE, _decode, _identity, _Reads

BRIEF = "b450ae7bc14068908d3a5cf8df8523ed74a275c818d120c8bdb108ef62b73211"
SUBJECT = "NVDA_30D_ATM_CONTROLLED"
PROVIDER, VARIANT = "foundation-controlled-iv-history", "daily_constant_maturity_iv_v1"
ANCHORS = (T, *(T - timedelta(days=k) for k in range(365, 0, -1)))
MAPPING = r.RawSignalProjectionMappingV1(
    "mmt-r183-comparable-iv", 1, r.RawSignalCatalogueId("R183"), PROVIDER, VARIANT,
    ("iv", "close"), "annualised_decimal_volatility",
    (("series.id", ("series", "id")), ("underlying.id", ("underlying", "id")),
     ("tenor.days", ("tenor", "days")), ("measure.kind", ("measure", "kind")),
     ("model.convention", ("model", "convention")),
     ("period.close_utc", ("period", "close_utc"))),
)
UNIT = f.UnitConventionVersionV1(
    "mmt-comparable-iv", 1, "annualised_decimal_volatility",
    "annualised_decimal_volatility", Decimal(1), Decimal(0),
)
CONTEXT = f.WindowContextV1(
    f.VersionRefV1("controlled-comparable-iv-year", 1),
    T - timedelta(days=365), T + timedelta(seconds=1), T - timedelta(days=365),
)
POLICY = f.InputSelectionPolicyVersionV1(
    "mmt-d105-selection", 1,
    ("subject_instrument", "series.id", "tenor.days", "measure.kind", "model.convention"),
    timedelta(days=365), timedelta(0), ("true_instant",), (),
    PROVIDER, VARIANT, PROVIDER + "/" + VARIANT, 100, 1000,
)
PARAMETER = f.CalculationParameterSetV1("mmt-d105-controlled", 1, "P_BASELINE",
                                         SUBJECT, (SUBJECT,))
DEFINITION = f.CalculationDefinitionV1(
    "D105", "D105-PRIOR-YEAR-IV-RANK-1", "K04_STANDARDISE_RANK",
    "100*(current-min(prior365))/(max(prior365)-min(prior365))", ("R183",), (),
    "P_BASELINE", "iv_rank_points", "exact_ratio",
    tuple(f.AuthorityArtifactRefV1(*x) for x in _AUTHORITY),
)


def request_check(request: f.WindowCalculationRequestV1, now: datetime) -> None:
    expected = f.CalculationRequestV1(
        "D105", SUBJECT, T, T + timedelta(seconds=1),
        DEFINITION.calculation_definition_version,
        f.VersionRefV1(PARAMETER.context_id, 1), f.VersionRefV1(POLICY.context_id, 1),
        (CONTEXT.ref,), (f.RawInputBindingV1(
            "R183", f.VersionRefV1(MAPPING.mapping_id, 1),
            f.VersionRefV1(UNIT.context_id, 1), SUBJECT,
        ),),
    )
    if (canonical(request.calculation) != canonical(expected) or request.context != CONTEXT
        or request.predecessor_occurrence_ids or now < expected.knowledge_cutoff_utc):
        raise ValueError("incompatible complete comparable-IV year request")


def identity(item: r.ProjectedRawValueV1) -> r.RawSelectionIdentityV1:
    if type(item.source_timestamp_raw) is not str:
        raise ValueError("exact comparable-IV close timestamp required")
    return r.RawSelectionIdentityV1((
        ("series.id", SUBJECT), ("underlying.id", "NVDA"),
        ("tenor.days", "30"), ("measure.kind", "atm_constant_maturity"),
        ("model.convention", "controlled-comparable-iv/1"),
        ("period.close_utc", item.source_timestamp_raw),
    ))


def candidate(item: r.ProjectedRawValueV1, c: f.CalculationRequestV1,
              anchor: datetime) -> bool:
    return (type(item) is r.ProjectedRawValueV1
            and item.selection_identity == identity(item)
            and source_event(item) == anchor
            and eligible(replace(item, selection_identity=None), MAPPING, POLICY, c) == anchor)


def choose(items: tuple[r.ProjectedRawValueV1, ...]) -> r.ProjectedRawValueV1:
    if not items:
        raise ValueError("missing required prior daily comparable-IV anchor")
    def rank(item: r.ProjectedRawValueV1) -> tuple[datetime, datetime, int]:
        return source_event(item), item.received_ts_utc, item.ingestion_sequence
    selected = max(items, key=rank)
    if sum(rank(item) == rank(selected) for item in items) != 1:
        raise ValueError("ambiguous exact comparable-IV daily role")
    return selected


def line(item: r.ProjectedRawValueV1, c: f.CalculationRequestV1,
         anchor: datetime) -> f.RawInputLineageV1:
    if (not candidate(item, c, anchor) or item.received_ts_utc != anchor
        or type(item.native_value) is not Decimal or item.native_value < 0):
        raise ValueError("exact nonnegative comparable-IV daily source required")
    return f.RawInputLineageV1(
        "R183", item.observation_occurrence_id.value,
        f.VersionRefV1(MAPPING.mapping_id, 1), f.VersionRefV1(UNIT.context_id, 1),
        item, cast(Decimal, item.native_value), anchor,
    )


def produce(request: f.WindowCalculationRequestV1,
            lines: tuple[f.RawInputLineageV1, ...], now: datetime
            ) -> f.WindowMeasurementOccurrenceV1:
    request_check(request, now)
    if len(lines) != 366:
        raise ValueError("current plus complete365 prior daily anchors required")
    for actual, anchor in zip(lines, ANCHORS, strict=True):
        if (type(actual) is not f.RawInputLineageV1
            or canonical(actual) != canonical(line(actual.projection, request.calculation,
                                                    anchor))):
            raise ValueError("comparable-IV anchor/source/order mismatch")
    current = Fraction(lines[0].canonical_value)
    prior = tuple(Fraction(x.canonical_value) for x in lines[1:])
    low, high = min(prior), max(prior)
    if low == high:
        raise ValueError("zero prior-year IV range")
    rank = 100 * (current - low) / (high - low)
    value = f.WindowMeasurementOccurrenceV1(
        "M02", NAMESPACE, BRIEF, "D105", "pending", request, DEFINITION,
        PARAMETER, POLICY, (UNIT,), (MAPPING,), lines, (), 31536000,
        f.ExactRatioV1(rank.numerator, rank.denominator),
        "iv_rank_points", "exact_ratio", T, request.calculation.knowledge_cutoff_utc, now,
    )
    return replace(value, derived_occurrence_id=_identity(value))


def validate(value: f.WindowMeasurementOccurrenceV1) -> None:
    if type(value) is not f.WindowMeasurementOccurrenceV1:
        raise TypeError("exact prior-year IV rank occurrence required")
    f._Validated.__post_init__(value)
    if canonical(value) != canonical(produce(value.request, value.raw_input_lineage,
                                             value.calculated_at_utc)):
        raise ValueError("prior-year rank/source/identity mismatch")


class _Owner:
    def __init__(self, state: RecordState, raw: f.RawProjectionReaderV1,
                 now: Callable[[], datetime]) -> None:
        self.state, self.raw, self.now = state, raw, now
        self.reads = _Reads(state)

    def materialise(self, request: f.WindowCalculationRequestV1
                    ) -> f.WindowMeasurementOccurrenceV1 | None:
        if type(request) is not f.WindowCalculationRequestV1:
            raise TypeError("exact prior-year rank request required")
        now = self.now()
        f._utc(now)
        try:
            request_check(request, now)
            items = tuple(history(self.raw, request.calculation, MAPPING, POLICY))
            lines = tuple(line(choose(tuple(item for item in items
                                      if candidate(item, request.calculation, anchor))),
                               request.calculation, anchor) for anchor in ANCHORS)
            result = produce(request, lines, now)
        except (TypeError, ValueError, ArithmeticError):
            return None
        return cast(f.WindowMeasurementOccurrenceV1, self.state.append(result))


def build_owner(
    admission: f.OwnerAdmissionV1, raw: f.RawProjectionReaderV1,
    predecessor: f.MeasurementTradeDirectionReadsV1 | f.MeasurementWindowReadsV1 | None,
    storage: f.MemoryStorageV1 | f.SQLiteStorageV1, now: Callable[[], datetime],
) -> f.MeasurementWindowOwnerV1:
    if admission != f.OwnerAdmissionV1("M02", BRIEF):
        raise ValueError("exact D105 admission required")
    if type(storage) not in (f.MemoryStorageV1, f.SQLiteStorageV1) or not callable(now):
        raise TypeError("exact storage/clock required")
    return _Owner(RecordState(storage, _decode, validate), raw, now)
