"""Fixed controlled R151 realised-volatility profiles over exact risk grids."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import replace
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from fractions import Fraction
from itertools import pairwise
from typing import cast

from nvda_desk.raw_signal_occurrence_truth import api as r

from . import api as f
from ._catalogue import _AUTHORITY
from ._evaluation import canonical
from ._log_return import _logarithm
from ._numeric_bounds import sqrt_ratio_50
from ._record_store import RecordState
from ._selection import eligible
from ._vwap_returns import chosen, history
from ._window import NAMESPACE, _decode, _identity, _Reads

# Each ID is admitted only by its immutable exact brief and generation.
BRIEFS: dict[str, str] = {
    "D033": "1e5dbfd27a61e9bea69e850c2913d60026366465fff2b264d5678becc3dfd183",
    "D032": "9201aaf3b34965acb6ee2e5ad5d0b7e5d5a002a6572b18c0b85c5c71a5022ddd",
}

_PROFILE: dict[str, tuple[str, datetime, int, timedelta]] = {
    "D032": ("5m", datetime(2026, 10, 20, 12, 35, tzinfo=UTC), 6, timedelta(minutes=1)),
    "D033": ("30m", datetime(2026, 10, 20, 12, 10, tzinfo=UTC), 31, timedelta(minutes=1)),
    "D034": ("session", datetime(2026, 10, 20, 12, tzinfo=UTC), 61, timedelta(minutes=1)),
    "D035": ("5d", datetime(2026, 10, 15, 13, tzinfo=UTC), 6, timedelta(days=1)),
    "D036": ("10d", datetime(2026, 10, 10, 13, tzinfo=UTC), 11, timedelta(days=1)),
}


def configuration(
    identity: str,
) -> tuple[
    f.CalculationDefinitionV1,
    f.CalculationParameterSetV1,
    f.InputSelectionPolicyVersionV1,
    r.RawSignalProjectionMappingV1,
    f.UnitConventionVersionV1,
    f.RealisedRiskWindowContextV1,
]:
    if identity not in BRIEFS:
        raise ValueError("unadmitted controlled risk profile")
    stem, start, count, step = _PROFILE[identity]
    samples = tuple(start + i * step for i in range(count))
    sessions = tuple(
        f.SessionFrameV1(
            f.VersionRefV1("controlled-risk-" + day.strftime("%Y%m%d"), 1),
            "controlled_cash", day, day + timedelta(hours=1),
        )
        for day in (
            datetime(2026, 10, 10, 12, tzinfo=UTC) + timedelta(days=i)
            for i in range(11)
        )
    )
    fraction = f.ExactRatioV1(1, 15120 if identity in {"D032", "D033", "D034"} else 252)
    intervals = tuple(
        f.TradingReturnIntervalV1(a, b, fraction)
        for a, b in pairwise(samples)
    )
    context = f.RealisedRiskWindowContextV1(
        f.VersionRefV1("controlled-risk-calendar", 1),
        samples[0], samples[-1], sessions[0].start_utc,
        sessions, samples, intervals,
    )
    name = "mmt-realised-vol-" + stem
    definition = f.CalculationDefinitionV1(
        identity, identity + "-REALISED-VOL-1", "K05_REALIZED_RISK",
        "sqrt(sum(ln(close_i/close_(i-1))^2)/sum(trading_year_fraction_i))",
        ("R151",), (), "P_VOL_WINDOW", "annualised_volatility", "scalar_decimal",
        tuple(f.AuthorityArtifactRefV1(*ref) for ref in _AUTHORITY),
    )
    parameter = f.CalculationParameterSetV1(name + "-50d", 1, "P_VOL_WINDOW", "NVDA", ("NVDA",))
    policy = f.InputSelectionPolicyVersionV1(
        name + "-selection", 1, ("subject_instrument", "session"),
        timedelta(days=30), timedelta(0), ("true_instant",), (),
        "foundation-pilot-fixture", "cash_quote_v1", "foundation-pilot-fixture/cash_quote_v1",
        100, 1000,
    )
    mapping = r.RawSignalProjectionMappingV1(
        "mmt-risk-close", 1, r.RawSignalCatalogueId("R151"),
        "foundation-pilot-fixture", "cash_quote_v1", ("bar", "close"), "price",
        (
            ("session.id", ("session", "id")),
            ("sample.kind", ("sample", "kind")),
            ("adjustment.basis", ("adjustment", "basis")),
        ),
    )
    unit = f.UnitConventionVersionV1(
        "mmt-pilot-price", 1, "price", "price", Decimal("1"), Decimal("0")
    )
    return definition, parameter, policy, mapping, unit, context


def request_check(request: f.WindowCalculationRequestV1, now: datetime) -> None:
    c = request.calculation
    d, p, policy, m, u, context = configuration(c.derived_signal_id)
    expected = f.CalculationRequestV1(
        c.derived_signal_id, "NVDA", c.as_of_utc, c.knowledge_cutoff_utc,
        d.calculation_definition_version,
        f.VersionRefV1(p.context_id, 1), f.VersionRefV1(policy.context_id, 1),
        (context.ref,),
        (f.RawInputBindingV1("R151", f.VersionRefV1(m.mapping_id, 1),
                             f.VersionRefV1(u.context_id, 1), "NVDA"),),
    )
    if (
        canonical(c) != canonical(expected)
        or request.context != context
        or request.predecessor_occurrence_ids
        or c.as_of_utc != context.sample_instants_utc[-1]
        or not c.as_of_utc <= c.knowledge_cutoff_utc <= now
        or len(context.intervals) != len(context.sample_instants_utc) - 1
        or context.history_complete_from_utc > context.sample_instants_utc[0]
    ):
        raise ValueError("incompatible fixed realised-risk request")
    for interval, a, b in zip(
        context.intervals,
        context.sample_instants_utc[:-1],
        context.sample_instants_utc[1:],
        strict=True,
    ):
        if interval.start_utc != a or interval.end_utc != b or not a < b:
            raise ValueError("incomplete or mismatched exact risk grid")
        if interval.trading_year_fraction.numerator <= 0:
            raise ValueError("nonpositive exact trading-time year fraction")
    if context.sessions != configuration(c.derived_signal_id)[-1].sessions:
        raise ValueError("unadmitted trading calendar")


def line(
    item: r.ProjectedRawValueV1, c: f.CalculationRequestV1,
    m: r.RawSignalProjectionMappingV1, u: f.UnitConventionVersionV1,
    policy: f.InputSelectionPolicyVersionV1, event: datetime,
) -> f.RawInputLineageV1:
    actual = eligible(replace(item, selection_identity=None), m, policy, c)
    kind = (
        "official_close" if event.hour == 13
        else "session_open" if event.hour == 12 and event.minute == 0
        else "minute_close"
    )
    expected = r.RawSelectionIdentityV1((
        ("session.id", "controlled-risk-" + event.strftime("%Y%m%d") + "/1"),
        ("sample.kind", kind), ("adjustment.basis", "unadjusted"),
    ))
    if (
        actual != event or item.selection_identity != expected
        or type(item.native_value) is not Decimal or item.native_value <= 0
    ):
        raise ValueError("missing exact compatible close")
    return f.RawInputLineageV1(
        "R151", item.observation_occurrence_id.value,
        f.VersionRefV1(m.mapping_id, 1), f.VersionRefV1(u.context_id, 1),
        item, item.native_value, event,
    )


def produce(
    request: f.WindowCalculationRequestV1,
    lines: tuple[f.RawInputLineageV1, ...], now: datetime,
) -> f.WindowMeasurementOccurrenceV1:
    request_check(request, now)
    c = request.calculation
    d, p, policy, m, u, context = configuration(c.derived_signal_id)
    if len(lines) != len(context.sample_instants_utc):
        raise ValueError("incomplete exact risk sample grid")
    for actual, event in zip(lines, context.sample_instants_utc, strict=True):
        if canonical(actual) != canonical(line(actual.projection, c, m, u, policy, event)):
            raise ValueError("selected risk lineage mismatch")
    squared = Fraction(0)
    for old, new in pairwise(lines):
        ratio_log = _logarithm(new.canonical_value, old.canonical_value)
        squared += Fraction(ratio_log) ** 2
    year_fraction = sum(
        (Fraction(x.trading_year_fraction.numerator, x.trading_year_fraction.denominator)
         for x in context.intervals), Fraction(0)
    )
    if year_fraction <= 0:
        raise ValueError("invalid trading-time denominator")
    result = sqrt_ratio_50(squared / year_fraction)
    value = f.WindowMeasurementOccurrenceV1(
        "M02", NAMESPACE, BRIEFS[c.derived_signal_id], c.derived_signal_id,
        "pending", request, d, p, policy, (u,), (m,), lines, (),
        int((context.session_end_utc - context.session_start_utc).total_seconds()),
        result, "annualised_volatility", "scalar_decimal",
        c.as_of_utc, c.knowledge_cutoff_utc, now,
    )
    return replace(value, derived_occurrence_id=_identity(value))


def validate(value: f.WindowMeasurementOccurrenceV1) -> None:
    if type(value) is not f.WindowMeasurementOccurrenceV1:
        raise TypeError("exact risk occurrence required")
    f._Validated.__post_init__(value)
    if canonical(value) != canonical(produce(value.request, value.raw_input_lineage,
                                            value.calculated_at_utc)):
        raise ValueError("realised risk calculation mismatch")


def validator(admission: f.OwnerAdmissionV1) -> Callable[[f.WindowMeasurementOccurrenceV1], None]:
    def check(value: f.WindowMeasurementOccurrenceV1) -> None:
        validate(value)
        if value.implementation_brief_sha256 != admission.implementation_brief_sha256:
            raise ValueError("wrong risk admission")
    return check


class _Owner:
    def __init__(
        self, admission: f.OwnerAdmissionV1, state: RecordState,
        raw: f.RawProjectionReaderV1, now: Callable[[], datetime],
    ) -> None:
        self.admission, self.state, self.raw, self.now = admission, state, raw, now
        self.reads = _Reads(state)

    def materialise(
        self, request: f.WindowCalculationRequestV1
    ) -> f.WindowMeasurementOccurrenceV1 | None:
        if type(request) is not f.WindowCalculationRequestV1:
            raise TypeError("exact risk request")
        now = self.now()
        f._utc(now)
        try:
            request_check(request, now)
            c = request.calculation
            if BRIEFS[c.derived_signal_id] != self.admission.implementation_brief_sha256:
                return None
            _, _, policy, m, u, context = configuration(c.derived_signal_id)
            items = history(self.raw, c, m, policy)
            selected = []
            for event in context.sample_instants_utc:
                candidates = []
                for item in items:
                    try:
                        candidates.append(line(item, c, m, u, policy, event))
                    except (TypeError, ValueError):
                        continue
                selected.append(chosen(tuple(candidates)))
            value = produce(request, tuple(selected), now)
        except (TypeError, ValueError, ArithmeticError):
            return None
        return cast(f.WindowMeasurementOccurrenceV1, self.state.append(value))


def build_owner(
    admission: f.OwnerAdmissionV1, raw: f.RawProjectionReaderV1,
    predecessor: f.MeasurementTradeDirectionReadsV1 | f.MeasurementWindowReadsV1 | None,
    storage: f.MemoryStorageV1 | f.SQLiteStorageV1, now: Callable[[], datetime],
) -> f.MeasurementWindowOwnerV1:
    if (
        type(admission) is not f.OwnerAdmissionV1 or admission.object_id != "M02"
        or admission.implementation_brief_sha256 not in BRIEFS.values()
    ):
        raise ValueError("exact realised risk admission")
    if (
        predecessor is not None or type(storage) not in (f.MemoryStorageV1, f.SQLiteStorageV1)
        or not callable(now) or not callable(getattr(raw, "list_projected_raw_history", None))
    ):
        raise TypeError("risk source must be public M00 only")
    return _Owner(admission, RecordState(storage, _decode, validator(admission)), raw, now)
