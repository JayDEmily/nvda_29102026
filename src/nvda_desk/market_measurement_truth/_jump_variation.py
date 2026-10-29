"""Approved D038 jump variation over exact public co-occurring historical bars."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import replace
from datetime import UTC, datetime, timedelta
from decimal import ROUND_HALF_EVEN, Context, Decimal, localcontext
from fractions import Fraction
from itertools import pairwise
from typing import cast

from nvda_desk.raw_signal_occurrence_truth import api as r

from . import api as f
from ._catalogue import _AUTHORITY as AUTHORITY
from ._evaluation import canonical
from ._log_return import _series
from ._record_store import RecordState
from ._selection import eligible
from ._vwap_returns import chosen, history
from ._window import NAMESPACE, _decode, _identity, _Reads

BRIEF = "4bd92bd883c5fc4ab63d4cb8988783d53994b25ca88ab91a2976bda13bdaee9c"
T = datetime(2026, 10, 20, 12, 40, tzinfo=UTC)
CUTOFF, NOW = T + timedelta(seconds=1), T + timedelta(seconds=2)
TIMES = tuple(T - timedelta(minutes=i) for i in (3, 2, 1, 0))
CONTEXT = f.WindowContextV1(
    f.VersionRefV1("controlled-jump-3m-grid", 1),
    datetime(2026, 10, 20, 12, tzinfo=UTC),
    datetime(2026, 10, 20, 13, tzinfo=UTC),
    TIMES[0],
)
PROVIDER, VARIANT = "foundation-controlled-jump", "trades_history_1m_v1"
META = (
    ("bar.end_utc", ("bar", "end_utc")),
    ("bar.id", ("bar", "id")),
    ("bar.duration_seconds", ("bar", "duration_seconds")),
    ("session.id", ("session", "id")),
    ("bar.series", ("bar", "series")),
    ("bar.adjustment_basis", ("bar", "adjustment_basis")),
)
MAPS = tuple(
    r.RawSignalProjectionMappingV1(
        "mmt-d038-" + field,
        1,
        r.RawSignalCatalogueId(rid),
        PROVIDER,
        VARIANT,
        ("bar", field),
        "price",
        META,
    )
    for rid, field in (("R151", "close"), ("R149", "high"), ("R150", "low"))
)
UNIT = f.UnitConventionVersionV1("mmt-d038-price", 1, "price", "price", Decimal("1"), Decimal("0"))
POLICY = f.InputSelectionPolicyVersionV1(
    "mmt-d038-selection",
    1,
    ("subject_instrument", "session.id"),
    timedelta(minutes=3),
    timedelta(0),
    ("true_instant",),
    (),
    PROVIDER,
    VARIANT,
    PROVIDER + "/" + VARIANT,
    100,
    1000,
)
PARAMETER = f.CalculationParameterSetV1(
    "mmt-d038-jump-3m-50d-half-even", 1, "P_VOL_WINDOW", "NVDA", ("NVDA",)
)
DEFINITION = f.CalculationDefinitionV1(
    "D038",
    "D038-JUMP-VARIATION-1",
    "K05_REALIZED_RISK",
    "max(sum(r_i^2)-(pi/2)*sum(abs(r_i)*abs(r_(i-1))),0); r_i=ln(P_i/P_(i-1))",
    ("R151", "R149", "R150"),
    (),
    "P_VOL_WINDOW",
    "variance",
    "scalar_decimal",
    tuple(f.AuthorityArtifactRefV1(*x) for x in AUTHORITY),
)

Interval = tuple[Fraction, Fraction]


def log_bounds(ratio: Fraction, terms: int) -> Interval:
    if ratio <= 0:
        raise ValueError("positive price ratio required")
    power = ratio.numerator.bit_length() - ratio.denominator.bit_length()
    reduced = ratio / Fraction(2) ** power
    if reduced < 1:
        reduced *= 2
        power -= 1
    elif reduced >= 2:
        reduced /= 2
        power += 1
    low, high = _series((reduced - 1) / (reduced + 1), terms)
    two_low, two_high = _series(Fraction(1, 3), terms)
    return (
        low + power * (two_low if power >= 0 else two_high),
        high + power * (two_high if power >= 0 else two_low),
    )


def atan_bounds(value: Fraction, terms: int) -> Interval:
    partial = Fraction(0)
    power = value
    square = value * value
    sign = 1
    for index in range(terms):
        partial += sign * power / (2 * index + 1)
        power *= square
        sign = -sign
    following = partial + sign * power / (2 * terms + 1)
    return min(partial, following), max(partial, following)


def pi_bounds(terms: int) -> Interval:
    a, b = atan_bounds(Fraction(1, 5), terms)
    c, d = atan_bounds(Fraction(1, 239), terms)
    return 16 * a - 4 * d, 16 * b - 4 * c


def absolute(bounds: Interval) -> Interval:
    low, high = bounds
    if low >= 0:
        return bounds
    if high <= 0:
        return -high, -low
    return Fraction(0), max(-low, high)


def multiply(left: Interval, right: Interval) -> Interval:
    products = tuple(a * b for a in left for b in right)
    return min(products), max(products)


def round_50(value: Fraction) -> Decimal:
    with localcontext(Context(prec=50, rounding=ROUND_HALF_EVEN)) as context:
        return context.divide(Decimal(value.numerator), Decimal(value.denominator))


def jump_variation(closes: tuple[Fraction, ...]) -> Decimal:
    for terms in range(32, 513, 32):
        returns = tuple(
            absolute(log_bounds(current / previous, terms))
            for previous, current in pairwise(closes)
        )
        rv_low = sum((low * low for low, _ in returns), Fraction(0))
        rv_high = sum((high * high for _, high in returns), Fraction(0))
        products = tuple(multiply(a, b) for a, b in pairwise(returns))
        adjacent = (
            sum((low for low, _ in products), Fraction(0)),
            sum((high for _, high in products), Fraction(0)),
        )
        pi_low, pi_high = pi_bounds(terms)
        bv_low, bv_high = multiply((pi_low / 2, pi_high / 2), adjacent)
        low = max(Fraction(0), rv_low - bv_high)
        high = max(Fraction(0), rv_high - bv_low)
        rounded = round_50(low)
        if rounded == round_50(high):
            return rounded
    raise ValueError("jump interval does not certify fifty-digit rounding")


def request_check(request: f.WindowCalculationRequestV1, now: datetime) -> None:
    c = request.calculation
    expected = f.CalculationRequestV1(
        "D038",
        "NVDA",
        T,
        CUTOFF,
        DEFINITION.calculation_definition_version,
        f.VersionRefV1(PARAMETER.context_id, 1),
        f.VersionRefV1(POLICY.context_id, 1),
        (CONTEXT.ref,),
        tuple(
            f.RawInputBindingV1(
                m.raw_signal_catalogue_id.value,
                f.VersionRefV1(m.mapping_id, 1),
                f.VersionRefV1(UNIT.context_id, 1),
                "NVDA",
            )
            for m in MAPS
        ),
    )
    if (
        canonical(c) != canonical(expected)
        or request.context != CONTEXT
        or request.predecessor_occurrence_ids
        or now != NOW
    ):
        raise ValueError("incompatible fixed jump request")


def line(
    item: r.ProjectedRawValueV1,
    c: f.CalculationRequestV1,
    mapping: r.RawSignalProjectionMappingV1,
    event: datetime,
) -> f.RawInputLineageV1:
    actual = eligible(replace(item, selection_identity=None), mapping, POLICY, c)
    stamp = event.isoformat().replace("+00:00", "Z")
    expected = r.RawSelectionIdentityV1(
        (
            ("bar.end_utc", stamp),
            ("bar.id", stamp),
            ("bar.duration_seconds", 60),
            ("session.id", "controlled_cash_20261020"),
            ("bar.series", "TRADES"),
            ("bar.adjustment_basis", "controlled_unadjusted/1"),
        )
    )
    if (
        actual != event
        or item.selection_identity != expected
        or type(item.native_value) is not Decimal
        or (mapping == MAPS[0] and item.native_value <= 0)
    ):
        raise ValueError("incompatible jump source role")
    return f.RawInputLineageV1(
        mapping.raw_signal_catalogue_id.value,
        item.observation_occurrence_id.value,
        f.VersionRefV1(mapping.mapping_id, 1),
        f.VersionRefV1(UNIT.context_id, 1),
        item,
        item.native_value,
        event,
    )


def produce(
    request: f.WindowCalculationRequestV1,
    lines: tuple[f.RawInputLineageV1, ...],
    now: datetime,
) -> f.WindowMeasurementOccurrenceV1:
    request_check(request, now)
    if len(lines) != 12:
        raise ValueError("four complete co-occurring bars required")
    roles = tuple((mapping, event) for event in TIMES for mapping in MAPS)
    for actual, (mapping, event) in zip(lines, roles, strict=True):
        if canonical(actual) != canonical(
            line(actual.projection, request.calculation, mapping, event)
        ):
            raise ValueError("jump immutable lineage mismatch")
    closes = []
    for offset in range(0, 12, 3):
        group = lines[offset : offset + 3]
        if len({v.observation_occurrence_id for v in group}) != 1:
            raise ValueError("bar roles must co-occur")
        close, high, low = (Fraction(v.canonical_value) for v in group)
        if not low <= close <= high:
            raise ValueError("inconsistent bar envelope")
        closes.append(close)
    c = request.calculation
    value = f.WindowMeasurementOccurrenceV1(
        "M02",
        NAMESPACE,
        BRIEF,
        "D038",
        "pending",
        request,
        DEFINITION,
        PARAMETER,
        POLICY,
        (UNIT,),
        MAPS,
        lines,
        (),
        180,
        jump_variation(tuple(closes)),
        "variance",
        "scalar_decimal",
        c.as_of_utc,
        c.knowledge_cutoff_utc,
        now,
    )
    return replace(value, derived_occurrence_id=_identity(value))


def validator(admission: f.OwnerAdmissionV1) -> Callable[[f.WindowMeasurementOccurrenceV1], None]:
    def check(value: f.WindowMeasurementOccurrenceV1) -> None:
        if type(value) is not f.WindowMeasurementOccurrenceV1:
            raise TypeError("exact jump occurrence")
        f._Validated.__post_init__(value)
        if admission != f.OwnerAdmissionV1("M02", BRIEF) or canonical(value) != canonical(
            produce(value.request, value.raw_input_lineage, value.calculated_at_utc)
        ):
            raise ValueError("jump immutable calculation mismatch")

    return check


class _Owner:
    def __init__(
        self,
        admission: f.OwnerAdmissionV1,
        state: RecordState,
        raw: f.RawProjectionReaderV1,
        now: Callable[[], datetime],
    ) -> None:
        self.admission, self.state, self.raw, self.now = admission, state, raw, now
        self.reads = _Reads(state)

    def materialise(
        self, request: f.WindowCalculationRequestV1
    ) -> f.WindowMeasurementOccurrenceV1 | None:
        if type(request) is not f.WindowCalculationRequestV1:
            raise TypeError("exact jump request")
        now = self.now()
        f._utc(now)
        try:
            request_check(request, now)
            c = request.calculation
            histories = {m.mapping_id: history(self.raw, c, m, POLICY) for m in MAPS}
            selected = []
            # Fix required close positions before attempting each bar's co-fields.
            for event in TIMES:
                mappings = MAPS
                close_candidates = []
                for item in histories[MAPS[0].mapping_id]:
                    try:
                        close_candidates.append(line(item, c, MAPS[0], event))
                    except (TypeError, ValueError):
                        continue
                close = chosen(tuple(close_candidates))
                for mapping in mappings:
                    matches = []
                    for item in histories[mapping.mapping_id]:
                        if item.observation_occurrence_id.value != close.observation_occurrence_id:
                            continue
                        try:
                            matches.append(line(item, c, mapping, event))
                        except (TypeError, ValueError):
                            continue
                    selected.append(chosen(tuple(matches)))
            value = produce(request, tuple(selected), now)
        except (TypeError, ValueError, ArithmeticError):
            return None
        return cast(f.WindowMeasurementOccurrenceV1, self.state.append(value))


def build_owner(
    admission: f.OwnerAdmissionV1,
    raw: f.RawProjectionReaderV1,
    predecessor: f.MeasurementTradeDirectionReadsV1 | f.MeasurementWindowReadsV1 | None,
    storage: f.MemoryStorageV1 | f.SQLiteStorageV1,
    now: Callable[[], datetime],
) -> f.MeasurementWindowOwnerV1:
    if type(admission) is not f.OwnerAdmissionV1 or admission != f.OwnerAdmissionV1("M02", BRIEF):
        raise ValueError("exact jump admission")
    if (
        predecessor is not None
        or type(storage) not in (f.MemoryStorageV1, f.SQLiteStorageV1)
        or not callable(now)
        or not callable(getattr(raw, "list_projected_raw_history", None))
    ):
        raise TypeError("jump requires public M00 only")
    return _Owner(admission, RecordState(storage, _decode, validator(admission)), raw, now)
