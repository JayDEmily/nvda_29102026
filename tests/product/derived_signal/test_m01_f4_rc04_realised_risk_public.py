"""F4 RC04 K05: public M00 realised-risk and bar true-range evidence.

The time-grid parameters are immutable supplied policy.  For named daily
horizons the fixtures use six/eleven/twenty-one genuine successive weekday
close instants, rather than inferring five days from five adjacent samples.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest

from nvda_desk.derived_signal_calculation_truth import api
from nvda_desk.raw_signal_occurrence_truth import api as raw

NOW = datetime(2026, 10, 10, 4, tzinfo=UTC)
DAY_END = datetime(2026, 10, 9, 20, tzinfo=UTC)
ONE = Decimal(1)
BASE = Decimal(100)
GROWTH = Decimal("1.1")


def _weekdays(count: int) -> tuple[datetime, ...]:
    dates: list[datetime] = []
    cursor = DAY_END
    while len(dates) < count:
        if cursor.weekday() < 5:
            dates.append(cursor)
        cursor -= timedelta(days=1)
    return tuple(reversed(dates))


def _instants(did: str) -> tuple[datetime, ...]:
    if did in ("D035", "D036", "D037"):
        return _weekdays({"D035": 6, "D036": 11, "D037": 21}[did])
    seconds = {"D032": 150, "D033": 900, "D034": 3600, "D038": 60}[did]
    count = 4 if did == "D038" else 3
    return tuple(
        NOW - timedelta(seconds=5 + seconds * (count - 1 - i))
        for i in range(count)
    )


def _record(
    m00: object, rid: str, oid: str, value: Decimal,
    timestamp: datetime, sequence: int, *,
    subject: str = "NVDA", received: datetime | None = None,
) -> None:
    m00.commands.admit_raw_observation_occurrence(
        raw.RawObservationOccurrenceV1(
            concept_id=raw.concept_id("raw_signal.raw_observation_occurrence"),
            contract_id=raw.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
            observation_occurrence_id=raw.observation_occurrence_id(oid),
            delivery_artifact_ref=raw.delivery_artifact_ref("rc04-risk-" + oid),
            source_provider=raw.provider_id("controlled-rc04-risk"),
            native_record={"metric": {rid: value}},
            received_ts_utc=timestamp if received is None else received,
            ingestion_sequence=sequence,
            ingestion_sequence_scope=raw.ingestion_sequence_scope("rc04:risk"),
            source_temporal_kind="true_instant",
            source_timestamp_raw=timestamp.isoformat(),
            source_timezone_native="UTC",
            raw_signal_catalogue_ids=(raw.RawSignalCatalogueId(rid),),
            source_variant="metric",
            subject_instrument=subject,
            native_units="canonical",
            revision_vintage_native="v1",
        )
    )


def _public(
    did: str,
    *,
    missing_index: int | None = None,
    wrong_subject_index: int | None = None,
    future_index: int | None = None,
    extra_d039_bar: bool = False,
    omit_bar_field: tuple[int, str] | None = None,
) -> tuple[api.DerivedSignalCalculationOwnerV1, api.CalculationRequestV1, tuple[datetime, ...]]:
    m00 = raw.create_owner()
    bar_total = 4 if extra_d039_bar else 3
    stamps = _instants(did) if did != "D039" else tuple(
        NOW - timedelta(minutes=5 * (bar_total - 1 - i)) for i in range(bar_total)
    )
    source_ids = (
        ("R141", "R142", "R143") if did == "D039" else
        ("R151", "R149", "R150") if did == "D038" else
        ("R151",)
    )
    seq = 0
    for i, ts in enumerate(stamps):
        if missing_index == i:
            continue
        if did == "D039":
            # Bar 0 is the previous close. Bars 1 and 2 have native
            # highs/lows with exact same-occurrence identity.
            if extra_d039_bar:
                obs = (
                    {"R143": Decimal(90)},
                    {"R141": Decimal(106), "R142": Decimal(94), "R143": Decimal(100)},
                    {"R141": Decimal(112), "R142": Decimal(95), "R143": Decimal(105)},
                    {"R141": Decimal(120), "R142": Decimal(100), "R143": Decimal(108)},
                )[i].copy()
            else:
                obs = (
                    {"R143": Decimal(100)}
                    if i == 0 else
                    ({"R141": Decimal(110), "R142": Decimal(90), "R143": Decimal(105)}
                     if i == 1 else
                     {"R141": Decimal(112), "R142": Decimal(99), "R143": Decimal(108)})
                ).copy()
            if omit_bar_field is not None and i == omit_bar_field[0]:
                obs.pop(omit_bar_field[1], None)
        else:
            price = (BASE * GROWTH ** i) if did != "D038" else (
                Decimal(100), Decimal(105), Decimal(90), Decimal(110)
            )[i]
            obs = (
                {"R151": price, "R149": price + 2, "R150": price - 2}
                if did == "D038" else {"R151": price}
            )
        seq += 1
        m00.commands.admit_raw_observation_occurrence(
            raw.RawObservationOccurrenceV1(
                concept_id=raw.concept_id("raw_signal.raw_observation_occurrence"),
                contract_id=raw.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
                observation_occurrence_id=raw.observation_occurrence_id(f"rc04-risk-{i}"),
                delivery_artifact_ref=raw.delivery_artifact_ref(f"rc04-risk-{i}"),
                source_provider=raw.provider_id("controlled-rc04-risk"),
                native_record={"metric": obs},
                received_ts_utc=NOW + timedelta(seconds=2) if future_index == i else ts,
                ingestion_sequence=seq,
                ingestion_sequence_scope=raw.ingestion_sequence_scope("rc04:risk"),
                source_temporal_kind="true_instant",
                source_timestamp_raw=ts.isoformat(),
                source_timezone_native="UTC",
                raw_signal_catalogue_ids=tuple(raw.RawSignalCatalogueId(r) for r in obs),
                source_variant="metric",
                subject_instrument="AMD" if wrong_subject_index == i else "NVDA",
                native_units="canonical",
                revision_vintage_native="v1",
            )
        )
    values: tuple[tuple[str, object], ...]
    if did == "D039":
        values = (("bar_count", 2),)
    else:
        minutes = {"D032": Decimal("2.5"), "D033": Decimal(15),
                   "D034": Decimal(60)}
        if did == "D038":
            values = (
                ("required_intervals", len(stamps) - 1),
                ("required_sample_instants_utc", stamps),
            )
        else:
            dt = (
                ONE / Decimal(252)
                if did in ("D035", "D036", "D037")
                else minutes[did] / (Decimal(252) * Decimal(390))
            )
            values = (
                ("required_intervals", len(stamps) - 1),
                ("required_sample_instants_utc", stamps),
                ("trading_year_fraction_per_interval", dt),
            )
    owner = api.create_owner(
        raw_projection_reader=m00.reads,
        raw_projection_mappings=tuple(
            raw.RawSignalProjectionMappingV1(
                "rc04-risk-map-" + key, 1,
                raw.RawSignalCatalogueId(key),
                "controlled-rc04-risk", "metric",
                ("metric", key), "canonical",
            ) for key in source_ids
        ),
        parameter_sets=(
            api.CalculationParameterSetV1(
                "rc04-risk", 1, "P_VOL_WINDOW", values
            ),
        ),
        input_selection_policies=(
            api.InputSelectionPolicyVersionV1(
                "rc04-risk-select", 1, ("subject_instrument",),
                timedelta(days=50), timedelta(days=50),
                ("true_instant",), (),
            ),
        ),
        unit_conventions=(
            api.UnitConventionVersionV1(
                "rc04-risk-unit", 1, "canonical", "canonical",
                Decimal(1), Decimal(0),
            ),
        ),
        contexts=(), utc_now=lambda: NOW,
    )
    req = api.CalculationRequestV1(
        did, "NVDA", NOW, NOW,
        "rc04-risk-public", "rc04-risk", 1,
        "rc04-risk-select", 1, (),
        raw_input_bindings=tuple(
            api.RawInputBindingV1(
                rid, api.VersionRefV1("rc04-risk-map-" + rid, 1),
                api.VersionRefV1("rc04-risk-unit", 1), "NVDA", None,
            ) for rid in source_ids
        ),
    )
    return owner, req, stamps


@pytest.mark.parametrize("did", ("D032", "D033", "D034", "D035", "D036", "D037"))
def test_rc04_public_realised_volatility_named_complete_window(
    did: str,
) -> None:
    owner, req, instants = _public(did)
    result = owner.materialise(req)
    assert result is not None
    intervals = len(instants) - 1
    year_fraction = (
        ONE / Decimal(252)
        if did in ("D035", "D036", "D037")
        else {"D032": Decimal("2.5"), "D033": Decimal(15),
              "D034": Decimal(60)}[did] / (Decimal(252) * Decimal(390))
    )
    prices = tuple(BASE * GROWTH ** i for i in range(len(instants)))
    returns = tuple(
        (prices[i] / prices[i - 1]).ln()
        for i in range(1, len(prices))
    )
    expected = (
        sum((rate * rate for rate in returns), Decimal(0))
        / (year_fraction * Decimal(intervals))
    ).sqrt()
    assert result.result == expected
    assert {r.observation_occurrence_id for r in result.raw_input_lineage} == {
        f"rc04-risk-{i}" for i in range(len(instants))
    }
    assert owner.materialise(req) == result


@pytest.mark.parametrize("did", ("D032", "D033", "D034", "D035", "D036", "D037"))
def test_rc04_public_named_window_missing_required_calendar_sample_refuses(
    did: str,
) -> None:
    _, _, original = _public(did)
    owner, req, _ = _public(did, missing_index=len(original) // 2)
    assert owner.materialise(req) is None


def test_rc04_public_d038_bipower_jump_variation_with_required_native_inputs() -> None:
    owner, req, _ = _public("D038")
    out = owner.materialise(req)
    assert out is not None
    prices = (Decimal(100), Decimal(105), Decimal(90), Decimal(110))
    rs = tuple((prices[i] / prices[i - 1]).ln() for i in range(1, len(prices)))
    rv = sum((r * r for r in rs), Decimal(0))
    bv = Decimal(str(3.141592653589793)) / Decimal(2) * sum(
        (abs(rs[i]) * abs(rs[i - 1]) for i in range(1, len(rs))), Decimal(0)
    )
    assert out.result == max(rv - bv, Decimal(0))
    assert {r.raw_signal_id for r in out.raw_input_lineage} == {
        "R149", "R150", "R151"
    }
    assert owner.materialise(req) == out


def test_rc04_public_d039_true_range_uses_previous_close_and_two_bar_mean() -> None:
    owner, req, _ = _public("D039")
    out = owner.materialise(req)
    assert out is not None and out.result == Decimal("16.5")
    assert {r.raw_signal_id for r in out.raw_input_lineage} == {
        "R141", "R142", "R143"
    }
    assert owner.materialise(req) == out


@pytest.mark.parametrize("did", ("D035", "D038", "D039"))
def test_rc04_public_required_window_wrong_subject_or_missing_refuses(
    did: str,
) -> None:
    owner, req, stamps = _public(did, wrong_subject_index=len(_instants(did)) // 2
                                if did != "D039" else 1)
    assert owner.materialise(req) is None
    owner, req, stamps = _public(did, missing_index=len(stamps) - 1)
    assert owner.materialise(req) is None


def test_rc04_public_d035_future_received_calendar_sample_not_visible() -> None:
    owner, req, _ = _public("D035", future_index=2)
    assert owner.materialise(req) is None


def test_rc04_public_d039_must_not_skip_incomplete_bar_in_latest_window() -> None:
    owner, req, _ = _public(
        "D039", extra_d039_bar=True, omit_bar_field=(2, "R141"),
    )
    # The last two bars are bar 2 and bar 3. Missing bar-2 high cannot
    # be repaired by silently drawing older complete bar 1 into the window.
    assert owner.materialise(req) is None


def test_rc04_public_d039_four_bar_control_true_range() -> None:
    owner, req, _ = _public("D039", extra_d039_bar=True)
    result = owner.materialise(req)
    # bar2 previous close=100 -> max(112-95,12,5)=17;
    # bar3 previous close=105 -> max(120-100,15,5)=20.
    assert result is not None and result.result == Decimal("18.5")
    assert owner.materialise(req) == result
