from __future__ import annotations

import importlib
import math
from datetime import UTC, date, datetime, timedelta
from decimal import Decimal
from typing import Any
from zoneinfo import ZoneInfo

from nvda_desk.derived_signal_calculation_truth import api

NOW = datetime(2026, 10, 7, 1, 0, tzinfo=UTC)


def _stage1() -> Any:
    return importlib.import_module("nvda_desk.derived_signal_calculation_truth._stage1")


def _catalogue() -> Any:
    return importlib.import_module("nvda_desk.derived_signal_calculation_truth._catalogue")


def _kv(
    value: object,
    *,
    occurrence_id: str = "o1",
    at: datetime = NOW,
    received: datetime | None = None,
    subject: str = "NVDA",
    temporal_kind: str = "true_instant",
    source_timestamp_raw: str | None = None,
    metadata: tuple[tuple[str, object], ...] = (),
) -> Any:
    s1 = _stage1()
    return s1.KernelValueV1(
        value=value,
        occurrence_id=occurrence_id,
        effective_at_utc=at,
        received_ts_utc=at if received is None else received,
        subject_instrument=subject,
        source_temporal_kind=temporal_kind,
        source_timestamp_raw=source_timestamp_raw,
        metadata=metadata,
    )


def _p(profile: str, **values: object) -> api.CalculationParameterSetV1:
    if not values:
        values = {"selection_mode": "exact"}
    return api.CalculationParameterSetV1(
        context_id=f"{profile.lower()}-1",
        version=1,
        profile=profile,
        parameters=tuple(values.items()),  # type: ignore[arg-type]
    )


def _eval(
    derived_signal_id: str,
    *,
    raw: dict[str, tuple[Any, ...]] | None = None,
    derived: dict[str, tuple[Any, ...]] | None = None,
    params: api.CalculationParameterSetV1 | None = None,
    contexts: tuple[object, ...] = (),
    as_of: datetime = NOW,
    cutoff: datetime = NOW,
) -> Any:
    s1 = _stage1()
    result = s1.evaluate_stage1_kernel(
        derived_signal_id,
        raw_inputs={} if raw is None else raw,
        derived_inputs={} if derived is None else derived,
        parameter_set=_p("P_BASIC") if params is None else params,
        contexts=contexts,
        as_of_utc=as_of,
        knowledge_cutoff_utc=cutoff,
    )
    return result


def _named(value: object) -> dict[str, object]:
    assert isinstance(value, tuple)
    return {str(item[0]): item[1] for item in value}  # type: ignore[index]


def test_stage1_runtime_catalogue_is_exact_hash_bound_209_row_authority() -> None:
    cat = _catalogue()
    rows = cat.catalogue_rows()
    assert (
        cat.CATALOGUE_SHA256 == "63bc1b776fc8fa8ba82eb3c9b16916f295c9ec3d480a5a068937c2f25146f5f5"
    )
    assert len(rows) == 209
    assert tuple(row.derived_id for row in rows) == tuple(f"D{i:03d}" for i in range(1, 210))


def test_stage1_catalogue_dependency_graph_is_acyclic_and_resolves_exact_refs() -> None:
    cat = _catalogue()
    rows = cat.catalogue_rows()
    by_id = {row.derived_id: row for row in rows}
    assert cat.topological_derived_ids() == tuple(cat.topological_derived_ids())
    assert len(cat.topological_derived_ids()) == 209
    for row in rows:
        assert row.kernel_id in cat.ADMITTED_KERNEL_IDS
        assert all(dep in by_id for dep in row.derived_dependencies)
        assert all(dep.startswith("R") and 1 <= int(dep[1:]) <= 323 for dep in row.raw_dependencies)


def test_stage1_has_an_explicit_dispatch_for_every_stage1_catalogue_row() -> None:
    cat = _catalogue()
    s1 = _stage1()
    expected = {
        row.derived_id for row in cat.catalogue_rows() if row.kernel_id in s1.STAGE1_KERNEL_IDS
    }
    assert len(expected) == 174
    assert set(s1.supported_stage1_ids()) == expected


def test_k01_true_instant_conversion_and_non_instant_refusal() -> None:
    good = _eval(
        "D001",
        raw={
            "R002": (
                _kv(
                    "2026-10-07T10:15:00+11:00",
                    source_timestamp_raw="2026-10-07T10:15:00+11:00",
                ),
            ),
            "R003": (_kv("Australia/Melbourne"),),
        },
        params=_p("P_TIME", exchange_timezone="Australia/Melbourne"),
    )
    assert good is not None
    assert good.value == datetime(2026, 10, 6, 23, 15, tzinfo=UTC)

    bad = _eval(
        "D001",
        raw={
            "R002": (
                _kv(
                    "2026-10-07",
                    temporal_kind="date_only",
                    source_timestamp_raw="2026-10-07",
                ),
            ),
            "R003": (_kv("Australia/Melbourne"),),
        },
        params=_p("P_TIME", exchange_timezone="Australia/Melbourne"),
    )
    assert bad is None


def test_k01_age_market_local_session_expiry_and_event_countdown_are_exact() -> None:
    d001 = _kv(datetime(2026, 10, 7, 0, 30, tzinfo=UTC), occurrence_id="d001")
    age = _eval(
        "D002",
        raw={"R001": (_kv(Decimal("1"), received=NOW),), "R002": (_kv("ts"),)},
        derived={"D001": (d001,)},
        params=_p("P_TIME", exchange_timezone="Australia/Melbourne"),
    )
    assert age is not None
    assert _named(age.value) == {"basis": "source_event", "age_seconds": Decimal("1800")}

    receipt_age = _eval(
        "D002",
        raw={
            "R001": (_kv(Decimal("1"), received=NOW - timedelta(seconds=15)),),
            "R002": (
                _kv(
                    "receipt-only",
                    received=NOW - timedelta(seconds=15),
                    temporal_kind="receipt_only",
                ),
            ),
        },
        params=_p("P_TIME", exchange_timezone="Australia/Melbourne"),
    )
    assert receipt_age is not None
    assert _named(receipt_age.value) == {
        "basis": "collector_receipt",
        "age_seconds": Decimal("15"),
    }

    local = _eval(
        "D003",
        raw={"R004": (_kv("Australia/Melbourne"),)},
        derived={"D001": (d001,)},
        params=_p("P_TIME", exchange_timezone="Australia/Melbourne"),
    )
    assert local is not None
    assert local.value == datetime(2026, 10, 7, 11, 30, tzinfo=local.value.tzinfo)

    countdown = _eval(
        "D062",
        raw={
            "R284": (
                _kv(datetime(2026, 10, 7, 1, 30, tzinfo=UTC), occurrence_id="event-1"),
                _kv(datetime(2026, 10, 7, 2, 0, tzinfo=UTC), occurrence_id="event-2"),
            )
        },
        derived={"D001": (_kv(NOW, occurrence_id="d001-now"),)},
        params=_p("P_TIME", exchange_timezone="UTC"),
    )
    assert countdown is not None
    assert _named(countdown.value) == {"seconds": Decimal("1800"), "minutes": Decimal("30")}

    d004 = _kv("2026-10-07", occurrence_id="d004")
    dte = _eval(
        "D085",
        raw={
            "R013": (_kv("2026-10-10"),),
            "R001": (_kv(Decimal("1")),),
        },
        derived={"D004": (d004,)},
        params=_p("P_TIME", expiry_time="16:00", exchange_timezone="Australia/Melbourne"),
    )
    assert dte is not None and dte.value == 3

    tte = _eval(
        "D086",
        raw={"R013": (_kv("2026-10-08"),)},
        derived={"D001": (_kv(datetime(2026, 10, 7, 1, 0, tzinfo=UTC)),)},
        params=_p("P_TIME", expiry_time="16:00", exchange_timezone="UTC"),
    )
    assert tte is not None
    assert tte.value == Decimal(39) / Decimal(24) / Decimal(365)


def test_k01_session_phase_and_market_open_use_explicit_calendar_without_undeclared_d005_edge() -> (
    None
):
    local_weekday = datetime(2026, 10, 5, 10, 0, tzinfo=ZoneInfo("America/New_York"))
    params = _p(
        "P_TIME",
        session_phases=("overnight|20:00|04:00", "rth|09:30|16:00"),
        liquid_phases=("rth",),
        market_open_weekdays=(0, 1, 2, 3, 4),
        market_closed_dates=("2026-10-12",),
    )
    phase = _eval("D005", derived={"D003": (_kv(local_weekday),)}, params=params)
    assert phase is not None and phase.value == "rth"

    overnight = _eval(
        "D005",
        derived={
            "D003": (_kv(datetime(2026, 10, 5, 23, 30, tzinfo=ZoneInfo("America/New_York"))),)
        },
        params=params,
    )
    assert overnight is not None and overnight.value == "overnight"

    open_flag = _eval("D010", derived={"D003": (_kv(local_weekday),)}, params=params)
    assert open_flag is not None and open_flag.value is True

    weekend = datetime(2026, 10, 10, 10, 0, tzinfo=ZoneInfo("America/New_York"))
    closed_flag = _eval("D010", derived={"D003": (_kv(weekend),)}, params=params)
    assert closed_flag is not None and closed_flag.value is False


def test_k02_fixed_algebra_examples_preserve_declared_scaling() -> None:
    midpoint = _eval("D011", raw={"R034": (_kv(Decimal("100")),), "R035": (_kv(Decimal("102")),)})
    spread = _eval("D012", raw={"R034": (_kv(Decimal("100")),), "R035": (_kv(Decimal("102")),)})
    assert midpoint is not None and midpoint.value == Decimal("101")
    assert spread is not None and spread.value == Decimal("2")

    spread_pct = _eval(
        "D013",
        derived={"D011": (_kv(midpoint.value),), "D012": (_kv(spread.value),)},
    )
    assert spread_pct is not None
    assert spread_pct.value == Decimal("1.980198019801980198019801980")

    curve = _eval("D042", raw={"R247": (_kv(Decimal("0.04")),), "R249": (_kv(Decimal("0.0525")),)})
    assert curve is not None and curve.value == Decimal("1.2500")

    vol_curve = _eval("D057", raw={"R238": (_kv(Decimal("18")),), "R239": (_kv(Decimal("20")),)})
    assert vol_curve is not None
    assert _named(vol_curve.value) == {
        "point_difference": Decimal("-2"),
        "ratio": Decimal("0.9"),
    }


def test_k02_depth_reconstruction_uses_stable_event_state_not_query_order() -> None:
    t0 = NOW - timedelta(seconds=3)
    raw = {
        "R185": (
            _kv(0, occurrence_id="e2", at=t0 + timedelta(seconds=1)),
            _kv(0, occurrence_id="e1", at=t0),
            _kv(1, occurrence_id="e3", at=t0 + timedelta(seconds=2)),
        ),
        "R187": (
            _kv("update", occurrence_id="e2", at=t0 + timedelta(seconds=1)),
            _kv("insert", occurrence_id="e1", at=t0),
            _kv("insert", occurrence_id="e3", at=t0 + timedelta(seconds=2)),
        ),
        "R188": (
            _kv("bid", occurrence_id="e2", at=t0 + timedelta(seconds=1)),
            _kv("bid", occurrence_id="e1", at=t0),
            _kv("bid", occurrence_id="e3", at=t0 + timedelta(seconds=2)),
        ),
        "R189": (
            _kv(Decimal("100"), occurrence_id="e2", at=t0 + timedelta(seconds=1)),
            _kv(Decimal("100"), occurrence_id="e1", at=t0),
            _kv(Decimal("99"), occurrence_id="e3", at=t0 + timedelta(seconds=2)),
        ),
        "R190": (
            _kv(Decimal("12"), occurrence_id="e2", at=t0 + timedelta(seconds=1)),
            _kv(Decimal("10"), occurrence_id="e1", at=t0),
            _kv(Decimal("5"), occurrence_id="e3", at=t0 + timedelta(seconds=2)),
        ),
    }
    bid = _eval(
        "D134",
        raw={k: raw[k] for k in ("R185", "R187", "R188", "R190")},
        params=_p("P_BASIC", depth_levels=2),
    )
    assert bid is not None and bid.value == Decimal("17")


def test_k02_breadth_uses_component_specific_eligible_denominators() -> None:
    members = ("A", "B", "C")
    params = _p("P_BASIC", basket_membership=members)
    raw: dict[str, tuple[Any, ...]] = {
        "R037": (
            _kv(Decimal("11"), subject="A", occurrence_id="a-last"),
            _kv(Decimal("9"), subject="B", occurrence_id="b-last"),
            _kv(Decimal("12"), subject="C", occurrence_id="c-last"),
        ),
        "R043": (
            _kv(Decimal("10"), subject="A", occurrence_id="a-open"),
            _kv(Decimal("10"), subject="B", occurrence_id="b-open"),
            _kv(Decimal("10"), subject="C", occurrence_id="c-open"),
        ),
        "R137": (
            _kv(Decimal("10.5"), subject="A", occurrence_id="a-vwap"),
            _kv(Decimal("9.5"), subject="B", occurrence_id="b-vwap"),
        ),
        "R042": (
            _kv(Decimal("10"), subject="A", occurrence_id="a-close"),
            _kv(Decimal("8"), subject="B", occurrence_id="b-close"),
            _kv(Decimal("13"), subject="C", occurrence_id="c-close"),
        ),
    }
    result = _eval("D151", raw=raw, params=params)
    assert result is not None
    assert _named(result.value) == {
        "positive_return_fraction": Decimal("0.6666666666666666666666666667"),
        "above_vwap_fraction": Decimal("0.5"),
        "above_prior_close_fraction": Decimal("0.6666666666666666666666666667"),
    }


def test_k02_candidate_greeks_require_context_and_breakeven_returns_every_real_root() -> None:
    greeks_raw = {
        "R112": (_kv(Decimal("0.5"), occurrence_id="leg"),),
        "R115": (_kv(Decimal("0.1"), occurrence_id="leg"),),
        "R116": (_kv(Decimal("0.2"), occurrence_id="leg"),),
        "R117": (_kv(Decimal("-0.05"), occurrence_id="leg"),),
        "R016": (_kv(Decimal("100"), occurrence_id="leg"),),
    }
    assert _eval("D168", raw=greeks_raw, params=_p("P_BASIC")) is None

    candidate = api.CandidateStructureContextV1(
        context_id="candidate-straddle",
        version=1,
        candidate_identity="long-straddle",
        leg_contract_identities=("C100", "P100"),
        leg_sides=("buy", "buy"),
        leg_quantities=(Decimal("1"), Decimal("1")),
        quantity=Decimal("1"),
        premium_assumptions=(("C100", Decimal("5")), ("P100", Decimal("4"))),
        entry_assumptions=(),
        risk_capital_currency=Decimal("1000"),
    )
    breakeven = _eval(
        "D170",
        raw={
            "R014": (
                _kv(
                    Decimal("100"),
                    occurrence_id="strike-call",
                    subject="C100",
                    metadata=(("option_right", "call"),),
                ),
                _kv(
                    Decimal("100"),
                    occurrence_id="strike-put",
                    subject="P100",
                    metadata=(("option_right", "put"),),
                ),
            )
        },
        derived={
            "D087": (
                _kv(Decimal("5"), occurrence_id="mid-call", subject="C100"),
                _kv(Decimal("4"), occurrence_id="mid-put", subject="P100"),
            )
        },
        params=_p("P_BASIC"),
        contexts=(candidate,),
    )
    assert breakeven is not None
    assert breakeven.value == (Decimal("91"), Decimal("109"))


def test_k01_macro_vintage_status_preserves_realtime_period_and_ignores_future_receipts() -> None:
    t0 = NOW - timedelta(days=3)
    t1 = NOW - timedelta(days=2)
    future = NOW + timedelta(seconds=1)
    raw = {
        "R280": (
            _kv("2026-10-01", occurrence_id="v1", at=t0, received=t0, temporal_kind="date_only"),
            _kv("2026-10-02", occurrence_id="v2", at=t1, received=t1, temporal_kind="date_only"),
            _kv(
                "2026-10-03",
                occurrence_id="v3",
                at=future,
                received=future,
                temporal_kind="date_only",
            ),
        ),
        "R281": (
            _kv("2026-10-01", occurrence_id="v1", at=t0, received=t0, temporal_kind="date_only"),
            _kv("9999-12-31", occurrence_id="v2", at=t1, received=t1, temporal_kind="date_only"),
            _kv(
                "9999-12-31",
                occurrence_id="v3",
                at=future,
                received=future,
                temporal_kind="date_only",
            ),
        ),
        "R282": (
            _kv("2026-10-01T10:00:00+00:00", occurrence_id="v1", at=t0, received=t0),
            _kv("2026-10-02T10:00:00+00:00", occurrence_id="v2", at=t1, received=t1),
            _kv("2026-10-03T10:00:00+00:00", occurrence_id="v3", at=future, received=future),
        ),
    }
    result = _eval("D009", raw=raw, params=_p("P_TIME", exchange_timezone="UTC"), cutoff=NOW)
    assert result is not None
    assert _named(result.value) == {
        "status": "latest_known_at_cutoff",
        "realtime_start": "2026-10-02",
        "realtime_end": "9999-12-31",
        "last_updated": "2026-10-02T10:00:00+00:00",
        "cutoff": NOW,
    }


def test_k02_atm_straddle_requires_exact_call_put_same_expiry_without_metadata_defaults() -> None:
    valid = _eval(
        "D109",
        derived={
            "D087": (
                _kv(
                    Decimal("5"),
                    occurrence_id="call",
                    subject="C100",
                    metadata=(
                        ("right", "call"),
                        ("delta", Decimal("0.50")),
                        ("expiry", "2026-10-16"),
                    ),
                ),
                _kv(
                    Decimal("4"),
                    occurrence_id="put",
                    subject="P100",
                    metadata=(
                        ("right", "put"),
                        ("delta", Decimal("-0.50")),
                        ("expiry", "2026-10-16"),
                    ),
                ),
            )
        },
    )
    assert valid is not None and valid.value == Decimal("9")

    mismatched_expiry = _eval(
        "D109",
        derived={
            "D087": (
                _kv(
                    Decimal("5"),
                    occurrence_id="call",
                    metadata=(
                        ("right", "call"),
                        ("delta", Decimal("0.50")),
                        ("expiry", "2026-10-16"),
                    ),
                ),
                _kv(
                    Decimal("4"),
                    occurrence_id="put",
                    metadata=(
                        ("right", "put"),
                        ("delta", Decimal("-0.50")),
                        ("expiry", "2026-10-23"),
                    ),
                ),
            )
        },
    )
    assert mismatched_expiry is None

    missing_right = _eval(
        "D109",
        derived={
            "D087": (
                _kv(
                    Decimal("5"),
                    occurrence_id="call",
                    metadata=(("delta", Decimal("0.50")), ("expiry", "2026-10-16")),
                ),
                _kv(
                    Decimal("4"),
                    occurrence_id="put",
                    metadata=(("delta", Decimal("-0.50")), ("expiry", "2026-10-16")),
                ),
            )
        },
    )
    assert missing_right is None


def test_k02_open_interest_change_uses_chronological_exact_contract_history() -> None:
    t0 = NOW - timedelta(days=1)
    current = _kv(Decimal("125"), occurrence_id="new", at=NOW, subject="C100")
    prior = _kv(Decimal("100"), occurrence_id="old", at=t0, subject="C100")
    result = _eval("D123", raw={"R047": (current, prior), "R048": ()})
    assert result is not None and result.value == Decimal("25")

    mixed_contract = _eval(
        "D123",
        raw={
            "R047": (
                _kv(Decimal("125"), occurrence_id="new", at=NOW, subject="C100"),
                _kv(Decimal("100"), occurrence_id="old", at=t0, subject="C105"),
            ),
            "R048": (),
        },
    )
    assert mixed_contract is None


def test_k02_smart_direct_gap_matches_direct_venue_rows_to_smart_side_and_level() -> None:
    def field(rows: tuple[tuple[str, datetime, object, str], ...]) -> tuple[Any, ...]:
        return tuple(
            _kv(
                value,
                occurrence_id=oid,
                at=at,
                subject="NVDA",
                metadata=(("ingestion_sequence", i),),
            )
            for i, (oid, at, value, _venue) in enumerate(rows, start=1)
        )

    t0 = NOW - timedelta(seconds=1)
    smart = (
        ("sb", t0, 0, ""),
        ("sa", t0 + timedelta(microseconds=1), 0, ""),
    )
    direct = (
        ("db", t0, 0, "ARCA"),
        ("da", t0 + timedelta(microseconds=1), 0, "ARCA"),
    )
    raw = {
        "R185": field(smart),
        "R187": field(
            (("sb", t0, "insert", ""), ("sa", t0 + timedelta(microseconds=1), "insert", ""))
        ),
        "R188": field((("sb", t0, "bid", ""), ("sa", t0 + timedelta(microseconds=1), "ask", ""))),
        "R189": field(
            (
                ("sb", t0, Decimal("100"), ""),
                ("sa", t0 + timedelta(microseconds=1), Decimal("101"), ""),
            )
        ),
        "R190": field(
            (
                ("sb", t0, Decimal("10"), ""),
                ("sa", t0 + timedelta(microseconds=1), Decimal("12"), ""),
            )
        ),
        "R192": field(direct),
        "R193": field(
            (("db", t0, "ARCA", "ARCA"), ("da", t0 + timedelta(microseconds=1), "ARCA", "ARCA"))
        ),
        "R194": field(
            (("db", t0, "insert", "ARCA"), ("da", t0 + timedelta(microseconds=1), "insert", "ARCA"))
        ),
        "R195": field(
            (("db", t0, "bid", "ARCA"), ("da", t0 + timedelta(microseconds=1), "ask", "ARCA"))
        ),
        "R196": field(
            (
                ("db", t0, Decimal("99.9"), "ARCA"),
                ("da", t0 + timedelta(microseconds=1), Decimal("101.1"), "ARCA"),
            )
        ),
        "R197": field(
            (
                ("db", t0, Decimal("7"), "ARCA"),
                ("da", t0 + timedelta(microseconds=1), Decimal("8"), "ARCA"),
            )
        ),
    }
    result = _eval("D144", raw=raw)
    assert result is not None
    assert result.value == (
        ("ask:0:ARCA", (("price_difference", Decimal("-0.1")), ("depth_difference", Decimal("4")))),
        ("bid:0:ARCA", (("price_difference", Decimal("0.1")), ("depth_difference", Decimal("3")))),
    )


def test_k02_candidate_greeks_align_quantities_by_exact_leg_contract_not_row_order() -> None:
    candidate = api.CandidateStructureContextV1(
        context_id="candidate-greeks",
        version=1,
        candidate_identity="two-leg",
        leg_contract_identities=("C100", "P100"),
        leg_sides=("buy", "sell"),
        leg_quantities=(Decimal("2"), Decimal("3")),
        quantity=Decimal("1"),
        premium_assumptions=(),
        entry_assumptions=(),
        risk_capital_currency=Decimal("1000"),
    )

    def legs(call: Decimal, put: Decimal) -> tuple[Any, ...]:
        # Put is deliberately first and occurrence identifiers do not match candidate order.
        return (
            _kv(put, occurrence_id="z-put", subject="P100"),
            _kv(call, occurrence_id="a-call", subject="C100"),
        )

    result = _eval(
        "D168",
        raw={
            "R112": legs(Decimal("0.50"), Decimal("-0.40")),
            "R115": legs(Decimal("0.10"), Decimal("0.08")),
            "R116": legs(Decimal("0.20"), Decimal("0.15")),
            "R117": legs(Decimal("-0.05"), Decimal("-0.04")),
            "R016": legs(Decimal("100"), Decimal("100")),
        },
        contexts=(candidate,),
    )
    assert result is not None
    assert _named(result.value) == {
        "delta": Decimal("220"),
        "gamma": Decimal("-4"),
        "vega": Decimal("-5"),
        "theta": Decimal("2"),
    }


def test_k03_uses_latest_anchor_at_or_before_cutoff_and_never_looks_forward() -> None:
    current = _kv(Decimal("110"), occurrence_id="now", at=NOW)
    before = _kv(Decimal("100"), occurrence_id="before", at=NOW - timedelta(minutes=5))
    after = _kv(Decimal("50"), occurrence_id="after", at=NOW - timedelta(minutes=4, seconds=59))
    result = _eval(
        "D020",
        raw={"R143": (after, current, before)},
        params=_p("P_WINDOW", anchor_seconds=300),
    )
    assert result is not None
    assert result.value == (Decimal("110") / Decimal("100")).ln()


def test_k04_historical_zscore_midrank_percentile_and_cross_section_are_separate() -> None:
    history = tuple(
        _kv(v, occurrence_id=f"h{i}", at=NOW - timedelta(days=4 - i))
        for i, v in enumerate((Decimal("1"), Decimal("2"), Decimal("3"), Decimal("4")))
    )
    current = _kv(Decimal("5"), occurrence_id="cur", at=NOW)
    z = _eval(
        "D029",
        raw={"R144": (*history, current)},
        params=_p("P_BASELINE", minimum_sample=2, history_count=4),
    )
    assert z is not None
    expected_z = (Decimal("5") - Decimal("2.5")) / (Decimal("5") / Decimal("3")).sqrt()
    assert z.value == expected_z

    pct = _eval(
        "D106",
        raw={"R183": (*history, current)},
        params=_p("P_BASELINE", minimum_sample=2, history_count=4),
    )
    assert pct is not None and pct.value == Decimal("100")

    cross = _eval(
        "D083",
        raw={
            "R037": (
                _kv(Decimal("110"), subject="A", occurrence_id="a-now"),
                _kv(Decimal("90"), subject="B", occurrence_id="b-now"),
            ),
            "R042": (
                _kv(Decimal("100"), subject="A", occurrence_id="a-ref"),
                _kv(Decimal("100"), subject="B", occurrence_id="b-ref"),
            ),
        },
        params=_p("P_CROSS_SECTION", basket_membership=("A", "B")),
    )
    assert cross is not None
    assert cross.value > Decimal("0")


def test_k05_realised_variation_requires_full_window_and_atr_uses_true_range() -> None:
    closes = tuple(
        _kv(
            Decimal(str(v)),
            occurrence_id=f"c{i}",
            at=NOW - timedelta(days=5 - i),
        )
        for i, v in enumerate((100, 101, 102, 103, 104, 105))
    )
    rv = _eval(
        "D035",
        raw={"R151": closes},
        params=_p(
            "P_VOL_WINDOW",
            required_intervals=5,
            trading_year_fraction_per_interval=Decimal("0.003968253968253968253968253968"),
        ),
    )
    assert rv is not None and rv.value > Decimal("0")

    insufficient = _eval(
        "D035",
        raw={"R151": closes[:-1]},
        params=_p(
            "P_VOL_WINDOW",
            required_intervals=5,
            trading_year_fraction_per_interval=Decimal("0.003968253968253968253968253968"),
        ),
    )
    assert insufficient is None

    atr = _eval(
        "D039",
        raw={
            "R141": (
                _kv(Decimal("11"), occurrence_id="b1"),
                _kv(Decimal("13"), occurrence_id="b2"),
            ),
            "R142": (_kv(Decimal("9"), occurrence_id="b1"), _kv(Decimal("10"), occurrence_id="b2")),
            "R143": (
                _kv(Decimal("10"), occurrence_id="b0", at=NOW - timedelta(minutes=10)),
                _kv(Decimal("10.5"), occurrence_id="b1", at=NOW - timedelta(minutes=5)),
                _kv(Decimal("12"), occurrence_id="b2"),
            ),
        },
        params=_p("P_VOL_WINDOW", bar_count=2),
    )
    assert atr is not None and atr.value == Decimal("2.5")


def test_k06_shared_ols_model_produces_coherent_coefficients_and_residual() -> None:
    xs = [
        (Decimal("1"), Decimal("0"), Decimal("1")),
        (Decimal("0"), Decimal("1"), Decimal("1")),
        (Decimal("1"), Decimal("1"), Decimal("0")),
        (Decimal("2"), Decimal("1"), Decimal("1")),
        (Decimal("1"), Decimal("2"), Decimal("2")),
    ]
    rows: dict[str, list[Any]] = {key: [] for key in ("D075", "D071", "D076", "D077")}
    for i, (m, tech, semi) in enumerate(xs):
        at = NOW - timedelta(days=len(xs) - i)
        y = Decimal("2") + Decimal("3") * m + Decimal("4") * tech + Decimal("5") * semi
        rows["D075"].append(_kv(y, occurrence_id=f"y{i}", at=at))
        rows["D071"].append(_kv(m, occurrence_id=f"m{i}", at=at))
        rows["D076"].append(_kv(tech, occurrence_id=f"t{i}", at=at))
        rows["D077"].append(_kv(semi, occurrence_id=f"s{i}", at=at))
    d = {key: tuple(value) for key, value in rows.items()}
    p = _p("P_REGRESSION", minimum_sample=5)
    b_market = _eval("D079", derived=d, params=p)
    b_tech = _eval("D080", derived=d, params=p)
    b_semi = _eval("D081", derived=d, params=p)
    assert b_market is not None and abs(b_market.value - Decimal("3")) < Decimal("1e-20")
    assert b_tech is not None and abs(b_tech.value - Decimal("4")) < Decimal("1e-20")
    assert b_semi is not None and abs(b_semi.value - Decimal("5")) < Decimal("1e-20")

    current = {
        "D075": (_kv(Decimal("21"), occurrence_id="yc"),),
        "D071": (_kv(Decimal("1"), occurrence_id="mc"),),
        "D076": (_kv(Decimal("1"), occurrence_id="tc"),),
        "D077": (_kv(Decimal("1"), occurrence_id="sc"),),
        "D079": (_kv(b_market.value, occurrence_id="bm"),),
        "D080": (_kv(b_tech.value, occurrence_id="bt"),),
        "D081": (_kv(b_semi.value, occurrence_id="bs"),),
    }
    # History plus current factors lets D078 reconstruct the same accepted model identity.
    for key in ("D075", "D071", "D076", "D077"):
        current[key] = (*d[key], *current[key])
    residual = _eval("D078", derived=current, params=p)
    assert residual is not None and abs(residual.value - Decimal("7")) < Decimal("1e-20")


def test_k06_book_slope_and_partial_correlation_have_explicit_ridge_semantics() -> None:
    slope = _eval(
        "D138",
        raw={
            "R189": (
                _kv(Decimal("99"), occurrence_id="b1"),
                _kv(Decimal("98"), occurrence_id="b2"),
                _kv(Decimal("101"), occurrence_id="a1"),
                _kv(Decimal("102"), occurrence_id="a2"),
            ),
            "R190": (
                _kv(Decimal("10"), occurrence_id="b1"),
                _kv(Decimal("20"), occurrence_id="b2"),
                _kv(Decimal("8"), occurrence_id="a1"),
                _kv(Decimal("18"), occurrence_id="a2"),
            ),
            "R188": (
                _kv("bid", occurrence_id="b1"),
                _kv("bid", occurrence_id="b2"),
                _kv("ask", occurrence_id="a1"),
                _kv("ask", occurrence_id="a2"),
            ),
        },
        derived={"D011": (_kv(Decimal("100")),)},
        params=_p("P_REGRESSION", ridge_coefficient=Decimal("0.1")),
    )
    assert slope is not None
    named = _named(slope.value)
    assert named["bid_slope"] == Decimal("20")
    assert named["ask_slope"] == Decimal("18")


def test_k07_all_authorised_scalar_extractors_are_implemented_without_implicit_scalarisation() -> (
    None
):
    s1 = _stage1()
    structured = (
        ("a", Decimal("3")),
        ("b", Decimal("4")),
        ("probabilities", (("up", Decimal("0.7")), ("down", Decimal("0.3")))),
        ("matrix", ((Decimal("1"), Decimal("2")), (Decimal("3"), Decimal("4")))),
        ("distribution", ((Decimal("-1"), Decimal("0.25")), (Decimal("1"), Decimal("0.75")))),
    )
    assert s1.extract_scalar(structured, "component", ("a",)) == Decimal("3")
    assert s1.extract_scalar(
        structured, "weighted_component_sum", ("a", Decimal("2"), "b", Decimal("-1"))
    ) == Decimal("2")
    assert s1.extract_scalar(structured, "class_probability", ("up",)) == Decimal("0.7")
    assert s1.extract_scalar(structured, "probability_margin", ()) == Decimal("0.4")
    entropy = s1.extract_scalar(structured, "normalised_entropy", ())
    assert Decimal("0") < entropy < Decimal("1")
    assert s1.extract_scalar(structured, "distribution_cdf", (Decimal("0"),)) == Decimal("0.25")
    assert s1.extract_scalar(structured, "upper_tail", (Decimal("0"),)) == Decimal("0.75")
    assert s1.extract_scalar(structured, "matrix_entry", (0, 1)) == Decimal("2")
    assert s1.extract_scalar(structured, "row_l2", (0,)) == Decimal(str(math.sqrt(5)))
    assert s1.extract_scalar(structured, "frobenius", ()) == Decimal(str(math.sqrt(30)))


def test_k07_score_schema_controls_transform_orientation_weight_and_missing_feature_refusal() -> (
    None
):
    feature_type = getattr(api, "ScoreFeatureV1", None)
    assert feature_type is not None
    features = (
        feature_type(
            signal_id="D020",
            extractor="component",
            extractor_arguments=("value",),
            transform="bounded_ratio",
            transform_scale=Decimal("2"),
            orientation=1,
            weight=Decimal("0.75"),
            clip_min=None,
            clip_max=None,
            baseline_values=(),
        ),
        feature_type(
            signal_id="D021",
            extractor="component",
            extractor_arguments=("value",),
            transform="identity",
            transform_scale=None,
            orientation=-1,
            weight=Decimal("0.25"),
            clip_min=None,
            clip_max=None,
            baseline_values=(),
        ),
    )
    params = api.CalculationParameterSetV1(
        context_id="score",
        version=1,
        profile="P_SCORE",
        parameters=(("intercept", Decimal("0")), ("bounded_output", False)),
        score_features=features,
    )
    result = _eval(
        "D040",
        derived={
            "D020": (_kv((("value", Decimal("2")),)),),
            "D021": (_kv((("value", Decimal("1")),)),),
            "D027": (_kv((("value", Decimal("99")),)),),
            "D024": (_kv((("value", Decimal("99")),)),),
        },
        params=params,
    )
    assert result is not None and result.value == Decimal("0.125")

    missing = _eval(
        "D040",
        derived={"D020": (_kv((("value", Decimal("2")),)),)},
        params=params,
    )
    assert missing is None


def test_k08_required_field_completeness_and_trade_sign_never_guess() -> None:
    policy = api.RequiredFieldPolicyV1(
        context_id="required",
        version=1,
        requirements=("R001", "R002", "R003"),
    )
    completeness = _eval(
        "D007",
        raw={"R001": (_kv(1),), "R003": (_kv(1),)},
        params=_p("P_RULE", rule="required_field_completeness"),
        contexts=(policy,),
    )
    assert completeness is not None and completeness.value == Decimal(
        "0.6666666666666666666666666667"
    )

    midpoint = _kv(Decimal("100"), occurrence_id="mid")
    buyer = _eval(
        "D015",
        raw={
            "R120": (_kv(Decimal("101")),),
            "R126": (_kv(Decimal("1")),),
            "R127": (_kv(Decimal("1")),),
        },
        derived={"D011": (midpoint,)},
        params=_p("P_RULE", rule="trade_sign"),
    )
    assert buyer is not None and buyer.value == 1

    unknown = _eval(
        "D015",
        raw={
            "R120": (_kv(Decimal("100")),),
            "R126": (_kv(Decimal("1")),),
            "R127": (_kv(Decimal("1")),),
        },
        derived={"D011": (midpoint,)},
        params=_p("P_RULE", rule="trade_sign"),
    )
    assert unknown is not None and unknown.value == 0


def test_k08_bucket_and_concentration_rules_use_absolute_gamma_and_canonical_hhi() -> None:
    bucket = _eval(
        "D091",
        raw={"R112": (_kv(Decimal("-0.25")),)},
        params=_p(
            "P_RULE",
            delta_bucket_boundaries=(Decimal("0"), Decimal("0.15"), Decimal("0.35"), Decimal("1")),
            delta_bucket_labels=("wing", "25d", "core"),
        ),
    )
    assert bucket is not None and bucket.value == "25d"

    oi = _eval(
        "D124",
        raw={
            "R047": (
                _kv(Decimal("30"), occurrence_id="a"),
                _kv(Decimal("70"), occurrence_id="b"),
            ),
            "R048": (),
        },
        params=_p("P_RULE", grouping="occurrence"),
    )
    assert oi is not None
    named = _named(oi.value)
    assert named["hhi"] == Decimal("0.58")

    gamma = _eval(
        "D128",
        derived={
            "D125": (
                _kv(
                    (("gamma_exposure", Decimal("-30")), ("spot_distance", Decimal("1"))),
                    occurrence_id="g1",
                ),
                _kv(
                    (("gamma_exposure", Decimal("70")), ("spot_distance", Decimal("5"))),
                    occurrence_id="g2",
                ),
            ),
            "D089": (_kv(Decimal("1")),),
        },
        params=_p("P_RULE", spot_distance_boundaries=(Decimal("0"), Decimal("2"), Decimal("10"))),
    )
    assert gamma is not None
    assert _named(gamma.value)["hhi"] == Decimal("0.58")


def test_k08_l2_insert_delete_replenishment_and_resilience_use_reconstructed_state() -> None:
    s1 = _stage1()
    assert callable(s1.reconstruct_book)
    events = (
        s1.BookEventV1(
            "e1", NOW - timedelta(seconds=4), 0, "insert", "bid", Decimal("100"), Decimal("10"), "X"
        ),
        s1.BookEventV1(
            "e2", NOW - timedelta(seconds=3), 0, "update", "bid", Decimal("100"), Decimal("4"), "X"
        ),
        s1.BookEventV1(
            "e3", NOW - timedelta(seconds=2), 0, "update", "bid", Decimal("100"), Decimal("10"), "X"
        ),
        s1.BookEventV1(
            "e4", NOW - timedelta(seconds=1), 0, "delete", "bid", Decimal("100"), Decimal("0"), "X"
        ),
    )
    reconstructed = s1.reconstruct_book(events)
    assert reconstructed[0].inserted_size == Decimal("10")
    assert reconstructed[1].depleted_size == Decimal("6")
    assert reconstructed[2].restored_size == Decimal("6")
    assert reconstructed[3].removed_size == Decimal("10")

    same_time = NOW - timedelta(seconds=10)
    out_of_query_order = (
        s1.BookEventV1(
            "late-update",
            same_time,
            0,
            "update",
            "bid",
            Decimal("100"),
            Decimal("4"),
            "X",
            ingestion_sequence=2,
        ),
        s1.BookEventV1(
            "early-insert",
            same_time,
            0,
            "insert",
            "bid",
            Decimal("100"),
            Decimal("10"),
            "X",
            ingestion_sequence=1,
        ),
    )
    ordered = s1.reconstruct_book(out_of_query_order)
    assert tuple(item.event.occurrence_id for item in ordered) == ("early-insert", "late-update")
    assert ordered[-1].resulting_size == Decimal("4")


def test_k08_resilience_requires_joint_depth_and_spread_recovery() -> None:
    def event_field(values: tuple[tuple[str, datetime, object], ...]) -> tuple[Any, ...]:
        return tuple(_kv(value, occurrence_id=oid, at=at) for oid, at, value in values)

    t0 = NOW - timedelta(seconds=4)
    t1 = NOW - timedelta(seconds=3)
    t2 = NOW - timedelta(seconds=2)
    rows = (
        ("bid-insert", t0, 0, "insert", "bid", Decimal("100"), Decimal("10")),
        ("ask-insert", t0, 0, "insert", "ask", Decimal("101"), Decimal("10")),
        ("bid-shock", t1, 0, "update", "bid", Decimal("100"), Decimal("2")),
        ("bid-recover", t2, 0, "update", "bid", Decimal("100"), Decimal("8")),
    )
    raw = {
        "R185": event_field(tuple((oid, at, pos) for oid, at, pos, *_ in rows)),
        "R187": event_field(tuple((oid, at, op) for oid, at, _, op, *_ in rows)),
        "R188": event_field(tuple((oid, at, side) for oid, at, _, _, side, *_ in rows)),
        "R189": event_field(tuple((oid, at, price) for oid, at, *_, price, _ in rows)),
        "R190": event_field(tuple((oid, at, size) for oid, at, *_, size in rows)),
        "R034": (_kv(Decimal("100"), occurrence_id="best-bid", at=t0),),
        "R035": (_kv(Decimal("101"), occurrence_id="best-ask", at=t0),),
    }
    result = _eval(
        "D142",
        raw=raw,
        params=_p(
            "P_RULE",
            depth_levels=1,
            shock_depth_fraction=Decimal("0.7"),
            shock_spread_multiple=Decimal("2"),
            recovery_depth_fraction=Decimal("0.8"),
            recovery_spread_multiple=Decimal("1.2"),
        ),
    )
    assert result is not None
    values = _named(result.value)
    assert values["seconds"] == Decimal("1")
    assert values["recovered_depth"] == Decimal("18")
    assert values["recovered_spread"] == Decimal("1")


def test_k08_candidate_selection_risk_size_limit_and_action_precedence_are_deterministic() -> None:
    candidate_type = api.CandidateSetContextV1
    candidate_set = candidate_type(
        context_id="cset",
        version=1,
        candidate_identities=("A", "B"),
        eligibility_classes=(("A", "directional"), ("B", "directional")),
        neighbour_relations=(("A", "B"), ("B", "A")),
    )
    selection = _eval(
        "D167",
        derived={
            "D166": (
                _kv((("candidate", "A"), ("value", True)), occurrence_id="a166"),
                _kv((("candidate", "B"), ("value", True)), occurrence_id="b166"),
            ),
            "D165": (
                _kv((("candidate", "A"), ("value", Decimal("5"))), occurrence_id="a165"),
                _kv((("candidate", "B"), ("value", Decimal("5"))), occurrence_id="b165"),
            ),
        },
        params=_p("P_RULE", rule="candidate_selection"),
        contexts=(candidate_set,),
    )
    assert selection is not None and selection.value == "A"

    action = _eval(
        "D192",
        derived={
            "D187": (_kv(True),),
            "D188": (_kv((("expected_currency_PnL", Decimal("100")),)),),
            "D189": (_kv((("delta", Decimal("0")),)),),
            "D190": (_kv(Decimal("1000")),),
            "D191": (_kv(Decimal("1000")),),
            "D175": (_kv(Decimal("1000")),),
        },
        params=_p(
            "P_RULE",
            mandatory_exit_on_invalidation=True,
            modify_minimum=Decimal("1"),
            exit_margin_currency=Decimal("1"),
        ),
    )
    assert action is not None and action.value == "exit"


def test_k16_state_vector_is_ordered_schema_assembly_without_hidden_weighting() -> None:
    params = _p(
        "P_STATE_VECTOR",
        component_order=("D150", "D084", "D061"),
    )
    result = _eval(
        "D155",
        derived={
            "D150": (_kv(Decimal("1"), occurrence_id="a"),),
            "D084": (_kv(Decimal("2"), occurrence_id="b"),),
            "D061": (_kv(Decimal("3"), occurrence_id="c"),),
        },
        params=params,
    )
    assert result is not None
    assert result.value == (
        ("D150", Decimal("1"), "a"),
        ("D084", Decimal("2"), "b"),
        ("D061", Decimal("3"), "c"),
    )


def test_k17_ofi_uses_adjacent_states_without_strict_length_pairing_bug() -> None:
    states = (
        _kv(
            (
                ("bid_price", Decimal("100")),
                ("bid_size", Decimal("10")),
                ("ask_price", Decimal("101")),
                ("ask_size", Decimal("8")),
            ),
            occurrence_id="s1",
            at=NOW - timedelta(seconds=2),
        ),
        _kv(
            (
                ("bid_price", Decimal("100")),
                ("bid_size", Decimal("12")),
                ("ask_price", Decimal("101")),
                ("ask_size", Decimal("7")),
            ),
            occurrence_id="s2",
            at=NOW - timedelta(seconds=1),
        ),
        _kv(
            (
                ("bid_price", Decimal("101")),
                ("bid_size", Decimal("5")),
                ("ask_price", Decimal("102")),
                ("ask_size", Decimal("9")),
            ),
            occurrence_id="s3",
            at=NOW,
        ),
    )
    result = _eval(
        "D145",
        raw={"__book_states__": states},
        params=_p("P_OFI", window_seconds=5),
    )
    assert result is not None and result.value == Decimal("15")


def test_graph_materialise_recurses_topologically_and_preserves_ultimate_raw_lineage() -> None:
    raw_api = importlib.import_module("nvda_desk.raw_signal_occurrence_truth.api")
    projected_type = raw_api.ProjectedRawValueV1
    page_type = raw_api.ProjectedRawHistoryPageV1

    values = {
        "R034": projected_type(
            raw_signal_catalogue_id=raw_api.RawSignalCatalogueId("R034"),
            observation_occurrence_id=raw_api.observation_occurrence_id("bid"),
            projection_mapping_id="m-bid",
            projection_mapping_version=1,
            source_provider="p",
            source_variant="snapshot",
            native_field_path=("bid",),
            native_value=Decimal("100"),
            native_units="price",
            subject_instrument="NVDA",
            source_temporal_kind="true_instant",
            source_timestamp_raw=NOW.isoformat(),
            source_timezone_native="UTC",
            received_ts_utc=NOW,
            ingestion_sequence=1,
            ingestion_sequence_scope=raw_api.ingestion_sequence_scope("p:snapshot"),
            revision_vintage_native=None,
        ),
        "R035": projected_type(
            raw_signal_catalogue_id=raw_api.RawSignalCatalogueId("R035"),
            observation_occurrence_id=raw_api.observation_occurrence_id("ask"),
            projection_mapping_id="m-ask",
            projection_mapping_version=1,
            source_provider="p",
            source_variant="snapshot",
            native_field_path=("ask",),
            native_value=Decimal("102"),
            native_units="price",
            subject_instrument="NVDA",
            source_temporal_kind="true_instant",
            source_timestamp_raw=NOW.isoformat(),
            source_timezone_native="UTC",
            received_ts_utc=NOW,
            ingestion_sequence=2,
            ingestion_sequence_scope=raw_api.ingestion_sequence_scope("p:snapshot"),
            revision_vintage_native=None,
        ),
    }

    class Reader:
        def list_projected_raw_history(self, raw_signal_catalogue_id: Any, **kwargs: Any) -> Any:
            item = values.get(raw_signal_catalogue_id.value)
            return page_type(items=() if item is None else (item,), next_cursor=None)

        def project_raw_value(self, *args: object, **kwargs: object) -> object | None:
            return None

    binding_type = getattr(api, "RawInputBindingV1", None)
    profile_ref_type = getattr(api, "ParameterProfileRefV1", None)
    assert binding_type is not None and profile_ref_type is not None

    p_basic = _p("P_BASIC", selection_mode="exact")
    selection = api.InputSelectionPolicyVersionV1(
        context_id="selection",
        version=1,
        join_keys=("subject_instrument",),
        maximum_staleness=timedelta(minutes=1),
        maximum_skew=timedelta(seconds=10),
        temporal_basis_permissions=("true_instant",),
        basket_membership=(),
    )
    unit = api.UnitConventionVersionV1(
        context_id="unit-price",
        version=1,
        native_units="price",
        canonical_units="price",
        scale=Decimal("1"),
        offset=Decimal("0"),
    )
    mappings = (
        raw_api.RawSignalProjectionMappingV1(
            mapping_id="m-bid",
            version=1,
            raw_signal_catalogue_id=raw_api.RawSignalCatalogueId("R034"),
            source_provider="p",
            source_variant="snapshot",
            native_field_path=("bid",),
            native_units="price",
        ),
        raw_api.RawSignalProjectionMappingV1(
            mapping_id="m-ask",
            version=1,
            raw_signal_catalogue_id=raw_api.RawSignalCatalogueId("R035"),
            source_provider="p",
            source_variant="snapshot",
            native_field_path=("ask",),
            native_units="price",
        ),
    )
    owner = api.create_owner(
        raw_projection_reader=Reader(),
        raw_projection_mappings=mappings,
        parameter_sets=(p_basic,),
        input_selection_policies=(selection,),
        unit_conventions=(unit,),
        contexts=(),
        utc_now=lambda: NOW,
    )
    request = api.CalculationRequestV1(
        derived_signal_id="D013",
        subject_instrument="NVDA",
        as_of_utc=NOW,
        knowledge_cutoff_utc=NOW,
        calculation_definition_version="calc-v1",
        parameter_set_id=p_basic.context_id,
        parameter_set_version=1,
        input_selection_policy_id=selection.context_id,
        input_selection_policy_version=1,
        context_refs=(),
        parameter_profile_refs=(profile_ref_type("P_BASIC", p_basic.context_id, 1),),
        raw_input_bindings=(
            binding_type(
                "R034", api.VersionRefV1("m-bid", 1), api.VersionRefV1(unit.context_id, 1), "NVDA"
            ),
            binding_type(
                "R035", api.VersionRefV1("m-ask", 1), api.VersionRefV1(unit.context_id, 1), "NVDA"
            ),
        ),
    )
    occurrence = owner.materialise(request)
    assert occurrence is not None
    assert occurrence.derived_signal_id == "D013"
    assert occurrence.result == Decimal("1.980198019801980198019801980")
    assert len(occurrence.predecessor_occurrence_ids) == 2
    assert {line.raw_signal_id for line in occurrence.raw_input_lineage} == {"R034", "R035"}


def test_public_seam_refuses_raw_inputs_from_another_subject() -> None:
    raw_api = importlib.import_module("nvda_desk.raw_signal_occurrence_truth.api")
    projected_type = raw_api.ProjectedRawValueV1
    page_type = raw_api.ProjectedRawHistoryPageV1

    values = {
        "R034": projected_type(
            raw_signal_catalogue_id=raw_api.RawSignalCatalogueId("R034"),
            observation_occurrence_id=raw_api.observation_occurrence_id("aapl-bid"),
            projection_mapping_id="m-bid",
            projection_mapping_version=1,
            source_provider="p",
            source_variant="snapshot",
            native_field_path=("bid",),
            native_value=Decimal("100"),
            native_units="price",
            subject_instrument="AAPL",
            source_temporal_kind="true_instant",
            source_timestamp_raw=NOW.isoformat(),
            source_timezone_native="UTC",
            received_ts_utc=NOW,
            ingestion_sequence=1,
            ingestion_sequence_scope=raw_api.ingestion_sequence_scope("p:snapshot"),
            revision_vintage_native=None,
        ),
        "R035": projected_type(
            raw_signal_catalogue_id=raw_api.RawSignalCatalogueId("R035"),
            observation_occurrence_id=raw_api.observation_occurrence_id("aapl-ask"),
            projection_mapping_id="m-ask",
            projection_mapping_version=1,
            source_provider="p",
            source_variant="snapshot",
            native_field_path=("ask",),
            native_value=Decimal("102"),
            native_units="price",
            subject_instrument="AAPL",
            source_temporal_kind="true_instant",
            source_timestamp_raw=NOW.isoformat(),
            source_timezone_native="UTC",
            received_ts_utc=NOW,
            ingestion_sequence=2,
            ingestion_sequence_scope=raw_api.ingestion_sequence_scope("p:snapshot"),
            revision_vintage_native=None,
        ),
    }

    class Reader:
        def list_projected_raw_history(self, raw_signal_catalogue_id: Any, **kwargs: Any) -> Any:
            item = values.get(raw_signal_catalogue_id.value)
            return page_type(items=() if item is None else (item,), next_cursor=None)

        def project_raw_value(self, *args: object, **kwargs: object) -> object | None:
            return None

    p_basic = _p("P_BASIC", selection_mode="exact")
    selection = api.InputSelectionPolicyVersionV1(
        context_id="selection-subject-match",
        version=1,
        join_keys=("subject_instrument",),
        maximum_staleness=timedelta(minutes=1),
        maximum_skew=timedelta(seconds=10),
        temporal_basis_permissions=("true_instant",),
        basket_membership=(),
    )
    unit = api.UnitConventionVersionV1(
        context_id="unit-price-subject-match",
        version=1,
        native_units="price",
        canonical_units="price",
        scale=Decimal("1"),
        offset=Decimal("0"),
    )
    mappings = (
        raw_api.RawSignalProjectionMappingV1(
            mapping_id="m-bid",
            version=1,
            raw_signal_catalogue_id=raw_api.RawSignalCatalogueId("R034"),
            source_provider="p",
            source_variant="snapshot",
            native_field_path=("bid",),
            native_units="price",
        ),
        raw_api.RawSignalProjectionMappingV1(
            mapping_id="m-ask",
            version=1,
            raw_signal_catalogue_id=raw_api.RawSignalCatalogueId("R035"),
            source_provider="p",
            source_variant="snapshot",
            native_field_path=("ask",),
            native_units="price",
        ),
    )
    owner = api.create_owner(
        raw_projection_reader=Reader(),
        raw_projection_mappings=mappings,
        parameter_sets=(p_basic,),
        input_selection_policies=(selection,),
        unit_conventions=(unit,),
        contexts=(),
        utc_now=lambda: NOW,
    )
    profile_ref = api.ParameterProfileRefV1("P_BASIC", p_basic.context_id, 1)

    def request(binding_subject: str) -> api.CalculationRequestV1:
        return api.CalculationRequestV1(
            derived_signal_id="D011",
            subject_instrument="NVDA",
            as_of_utc=NOW,
            knowledge_cutoff_utc=NOW,
            calculation_definition_version="calc-v1",
            parameter_set_id=p_basic.context_id,
            parameter_set_version=1,
            input_selection_policy_id=selection.context_id,
            input_selection_policy_version=1,
            context_refs=(),
            parameter_profile_refs=(profile_ref,),
            raw_input_bindings=(
                api.RawInputBindingV1(
                    "R034",
                    api.VersionRefV1("m-bid", 1),
                    api.VersionRefV1(unit.context_id, 1),
                    binding_subject,
                ),
                api.RawInputBindingV1(
                    "R035",
                    api.VersionRefV1("m-ask", 1),
                    api.VersionRefV1(unit.context_id, 1),
                    binding_subject,
                ),
            ),
        )

    # Reviewer witness: request NVDA while both binding and projected observations are AAPL.
    assert owner.materialise(request("AAPL")) is None
    # The projection reader is an external seam: a mismatched returned observation must also fail closed.
    assert owner.materialise(request("NVDA")) is None

def test_graph_refuses_future_raw_inputs_and_incompatible_stored_predecessor_versions() -> None:
    s1 = _stage1()
    assert callable(s1.select_eligible_values)
    future = _kv(Decimal("1"), at=NOW + timedelta(seconds=1))
    past = _kv(Decimal("2"), at=NOW - timedelta(seconds=1))
    selected = s1.select_eligible_values(
        (future, past),
        as_of_utc=NOW,
        knowledge_cutoff_utc=NOW,
        maximum_staleness=timedelta(minutes=1),
        temporal_basis_permissions=("true_instant",),
    )
    assert tuple(item.value for item in selected) == (Decimal("2"),)


def test_occurrence_identity_is_idempotent_and_changed_inputs_append_new_truth() -> None:
    s1 = _stage1()
    one = s1.occurrence_identity(
        "D011",
        calculation_definition_version="calc-v1",
        subject_instrument="NVDA",
        effective_as_of_utc=NOW,
        knowledge_cutoff_utc=NOW,
        input_occurrence_ids=("a", "b"),
        version_keys=(("p", 1),),
    )
    same = s1.occurrence_identity(
        "D011",
        calculation_definition_version="calc-v1",
        subject_instrument="NVDA",
        effective_as_of_utc=NOW,
        knowledge_cutoff_utc=NOW,
        input_occurrence_ids=("a", "b"),
        version_keys=(("p", 1),),
    )
    changed = s1.occurrence_identity(
        "D011",
        calculation_definition_version="calc-v1",
        subject_instrument="NVDA",
        effective_as_of_utc=NOW,
        knowledge_cutoff_utc=NOW,
        input_occurrence_ids=("a", "c"),
        version_keys=(("p", 1),),
    )
    assert one == same
    assert one != changed


def test_structured_result_carrier_and_postgres_codec_round_trip_nested_stage1_values() -> None:
    pg = importlib.import_module("nvda_desk.derived_signal_calculation_truth._postgres")
    value = (
        ("scalar", Decimal("1.25")),
        ("vector", (Decimal("1"), Decimal("2"))),
        ("matrix", ((Decimal("1"), Decimal("2")), (Decimal("3"), Decimal("4")))),
        ("stamp", NOW),
        ("local_stamp", datetime(2026, 10, 7, 12, 0, tzinfo=ZoneInfo("Australia/Melbourne"))),
        ("trading_date", date(2026, 10, 7)),
    )
    encoded = pg._encode_value(value)
    assert pg._decode_value(encoded) == value
