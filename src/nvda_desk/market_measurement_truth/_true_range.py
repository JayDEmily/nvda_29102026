"""Controlled D039 two-bar true range over co-occurring public OHLC."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import replace
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from fractions import Fraction
from typing import cast

from nvda_desk.raw_signal_occurrence_truth import api as r

from . import api as f
from ._catalogue import _AUTHORITY
from ._evaluation import canonical
from ._record_store import RecordState
from ._selection import eligible
from ._vwap_returns import chosen, history
from ._window import NAMESPACE, _decode, _identity, _Reads

BRIEF = "a557c9d3572099fec9389848d94edba4b5ff17ba47bdce2e3f6e21c67e89ea5c"
T = datetime(2026, 10, 20, 12, 40, tzinfo=UTC)
TIMES = (T - timedelta(minutes=10), T - timedelta(minutes=5), T)
S = "controlled-atr-session/1"
CONTEXT = f.WindowContextV1(
    f.VersionRefV1("controlled-atr-session", 1),
    datetime(2026, 10, 20, 12, tzinfo=UTC),
    datetime(2026, 10, 20, 13, tzinfo=UTC),
    datetime(2026, 10, 20, 12, tzinfo=UTC),
)
META = (
    ("session.id", ("session", "id")),
    ("bar.id", ("bar", "id")),
    ("bar.duration_seconds", ("bar", "duration_seconds")),
    ("adjustment.basis", ("adjustment", "basis")),
)
MAPS = tuple(
    r.RawSignalProjectionMappingV1(
        "mmt-atr-" + field,
        1,
        r.RawSignalCatalogueId(rid),
        "foundation-pilot-fixture",
        "cash_quote_v1",
        ("bar", field),
        "price",
        META,
    )
    for rid, field in (("R141", "high"), ("R142", "low"), ("R143", "close"))
)
UNIT = f.UnitConventionVersionV1("mmt-pilot-price", 1, "price", "price", Decimal("1"), Decimal("0"))
POLICY = f.InputSelectionPolicyVersionV1(
    "mmt-d039-selection",
    1,
    ("subject_instrument", "session"),
    timedelta(minutes=10),
    timedelta(0),
    ("true_instant",),
    (),
    "foundation-pilot-fixture",
    "cash_quote_v1",
    "foundation-pilot-fixture/cash_quote_v1",
    100,
    1000,
)
PARAMETER = f.CalculationParameterSetV1("mmt-d039-controlled", 1, "P_VOL_WINDOW", "NVDA", ("NVDA",))
DEFINITION = f.CalculationDefinitionV1(
    "D039",
    "D039-ATR-1",
    "K05_REALIZED_RISK",
    "mean(max(high-low,abs(high-prev_close),abs(low-prev_close))); bar_count=2; bar_seconds=300",
    ("R141", "R142", "R143"),
    (),
    "P_VOL_WINDOW",
    "price",
    "exact_ratio",
    tuple(f.AuthorityArtifactRefV1(*x) for x in _AUTHORITY),
)


def request_check(request: f.WindowCalculationRequestV1, now: datetime) -> None:
    c = request.calculation
    expected = f.CalculationRequestV1(
        "D039",
        "NVDA",
        T,
        c.knowledge_cutoff_utc,
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
        or not T <= c.knowledge_cutoff_utc <= now
    ):
        raise ValueError("incompatible fixed two-bar ATR request")


def line(
    item: r.ProjectedRawValueV1,
    c: f.CalculationRequestV1,
    mapping: r.RawSignalProjectionMappingV1,
    event: datetime,
) -> f.RawInputLineageV1:
    actual = eligible(replace(item, selection_identity=None), mapping, POLICY, c)
    expected = r.RawSelectionIdentityV1(
        (
            ("session.id", S),
            ("bar.id", event.isoformat().replace("+00:00", "Z")),
            ("bar.duration_seconds", 300),
            ("adjustment.basis", "unadjusted"),
        )
    )
    if (
        actual != event
        or item.selection_identity != expected
        or type(item.native_value) is not Decimal
        or item.native_value <= 0
    ):
        raise ValueError("incompatible exact OHLC bar")
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
    request: f.WindowCalculationRequestV1, lines: tuple[f.RawInputLineageV1, ...], now: datetime
) -> f.WindowMeasurementOccurrenceV1:
    request_check(request, now)
    if len(lines) != 7:
        raise ValueError("one previous close and two complete OHLC bars required")
    roles = ((MAPS[2], TIMES[0]), *((m, event) for event in TIMES[1:] for m in MAPS))
    for actual, (mapping, event) in zip(lines, roles, strict=True):
        if canonical(actual) != canonical(
            line(actual.projection, request.calculation, mapping, event)
        ):
            raise ValueError("ATR lineage mismatch")
    previous = Fraction(lines[0].canonical_value)
    total = Fraction(0)
    for offset in (1, 4):
        group = lines[offset : offset + 3]
        if len({v.observation_occurrence_id for v in group}) != 1:
            raise ValueError("OHLC must co-occur on the selected bar")
        high, low, close = (Fraction(v.canonical_value) for v in group)
        if not low <= close <= high:
            raise ValueError("inconsistent OHLC")
        total += max(high - low, abs(high - previous), abs(low - previous))
        previous = close
    result = total / 2
    c = request.calculation
    value = f.WindowMeasurementOccurrenceV1(
        "M02",
        NAMESPACE,
        BRIEF,
        "D039",
        "pending",
        request,
        DEFINITION,
        PARAMETER,
        POLICY,
        (UNIT,),
        MAPS,
        lines,
        (),
        600,
        f.ExactRatioV1(result.numerator, result.denominator),
        "price",
        "exact_ratio",
        c.as_of_utc,
        c.knowledge_cutoff_utc,
        now,
    )
    return replace(value, derived_occurrence_id=_identity(value))


def validator(admission: f.OwnerAdmissionV1) -> Callable[[f.WindowMeasurementOccurrenceV1], None]:
    def check(value: f.WindowMeasurementOccurrenceV1) -> None:
        if type(value) is not f.WindowMeasurementOccurrenceV1:
            raise TypeError("exact ATR occurrence")
        f._Validated.__post_init__(value)
        if admission != f.OwnerAdmissionV1("M02", BRIEF) or canonical(value) != canonical(
            produce(value.request, value.raw_input_lineage, value.calculated_at_utc)
        ):
            raise ValueError("ATR immutable calculation mismatch")

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
            raise TypeError("exact ATR request")
        now = self.now()
        f._utc(now)
        try:
            request_check(request, now)
            c = request.calculation
            histories = {m.mapping_id: history(self.raw, c, m, POLICY) for m in MAPS}
            selected = []
            # Fix required close positions before attempting each bar's co-fields.
            for index, event in enumerate(TIMES):
                mappings = (MAPS[2],) if index == 0 else MAPS
                close_candidates = []
                for item in histories[MAPS[2].mapping_id]:
                    try:
                        close_candidates.append(line(item, c, MAPS[2], event))
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
        raise ValueError("exact ATR admission")
    if (
        predecessor is not None
        or type(storage) not in (f.MemoryStorageV1, f.SQLiteStorageV1)
        or not callable(now)
        or not callable(getattr(raw, "list_projected_raw_history", None))
    ):
        raise TypeError("ATR requires public M00 only")
    return _Owner(admission, RecordState(storage, _decode, validator(admission)), raw, now)
