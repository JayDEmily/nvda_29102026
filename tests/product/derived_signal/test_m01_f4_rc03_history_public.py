"""F4 RC03 public M00 history and exact-subject anchor proof (D019-D023, D026).

Every value is admitted as a native M00 observation.  No kernel values,
persistence objects, or derived results are directly injected.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest

from nvda_desk.derived_signal_calculation_truth import api
from nvda_desk.raw_signal_occurrence_truth import api as raw

NOW = datetime(2026, 10, 10, 4, tzinfo=UTC)
ANCHORS = (("D019", 60), ("D020", 300), ("D021", 1800))


def _record(
    m00: object,
    rid: str,
    oid: str,
    value: Decimal,
    stamp: datetime,
    seq: int,
    *,
    subject: str = "NVDA",
    received: datetime | None = None,
) -> None:
    recv = stamp if received is None else received
    m00.commands.admit_raw_observation_occurrence(
        raw.RawObservationOccurrenceV1(
            concept_id=raw.concept_id("raw_signal.raw_observation_occurrence"),
            contract_id=raw.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
            observation_occurrence_id=raw.observation_occurrence_id(oid),
            delivery_artifact_ref=raw.delivery_artifact_ref("rc03-" + oid),
            source_provider=raw.provider_id("controlled-rc03"),
            native_record={"metrics": {rid: value}},
            received_ts_utc=recv,
            ingestion_sequence=seq,
            ingestion_sequence_scope=raw.ingestion_sequence_scope("controlled-rc03:metrics"),
            source_temporal_kind="true_instant",
            source_timestamp_raw=stamp.isoformat(),
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
    events: tuple[tuple[str, str, Decimal, datetime, str], ...],
    *,
    anchor: int | None = None,
    omitted: str | None = None,
    parameter: tuple[str, int | None] | None = None,
) -> tuple[api.DerivedSignalCalculationOwnerV1, api.CalculationRequestV1]:
    m00 = raw.create_owner()
    for i, (rid, oid, value, instant, subject) in enumerate(events, 1):
        _record(m00, rid, oid, value, instant, i, subject=subject)
    raw_ids = tuple(dict.fromkeys(rid for rid, *_ in events if rid != omitted))
    mappings = tuple(
        raw.RawSignalProjectionMappingV1(
            "rc03-map-" + rid,
            1,
            raw.RawSignalCatalogueId(rid),
            "controlled-rc03",
            "metric",
            ("metrics", rid),
            "canonical",
        )
        for rid in raw_ids
    )
    owner = api.create_owner(
        raw_projection_reader=m00.reads,
        raw_projection_mappings=mappings,
        parameter_sets=(
            api.CalculationParameterSetV1(
                "rc03-window",
                1,
                "P_WINDOW",
                (("window_seconds", 3600),)
                if anchor is None and parameter is None
                else ((("anchor_seconds", anchor) if parameter is None else parameter),),
            ),
        ),
        input_selection_policies=(
            api.InputSelectionPolicyVersionV1(
                "rc03-subject",
                1,
                ("subject_instrument",),
                timedelta(seconds=15),
                timedelta(seconds=15),
                ("true_instant",),
                (),
            ),
        ),
        unit_conventions=(
            api.UnitConventionVersionV1(
                "rc03-unit",
                1,
                "canonical",
                "canonical",
                Decimal(1),
                Decimal(0),
            ),
        ),
        contexts=(),
        utc_now=lambda: NOW,
    )
    req = api.CalculationRequestV1(
        did,
        "NVDA",
        NOW,
        NOW,
        "rc03-public",
        "rc03-window",
        1,
        "rc03-subject",
        1,
        (),
        raw_input_bindings=tuple(
            api.RawInputBindingV1(
                rid,
                api.VersionRefV1("rc03-map-" + rid, 1),
                api.VersionRefV1("rc03-unit", 1),
                "NVDA",
                None,
            )
            for rid in raw_ids
        ),
    )
    return owner, req


def _anchored_events(
    seconds: int,
    *,
    missing_anchor: bool = False,
    late_reference: bool = False,
) -> tuple[tuple[str, str, Decimal, datetime, str], ...]:
    end = NOW - timedelta(seconds=2)
    events = [
        ("R143", "current", Decimal(120), end, "NVDA"),
        ("R143", "distractor", Decimal(999), end - timedelta(seconds=seconds // 2), "NVDA"),
        ("R143", "other-subject", Decimal(1), end - timedelta(seconds=seconds), "AMD"),
    ]
    if not missing_anchor:
        ref_at = end - timedelta(seconds=seconds)
        if late_reference:
            ref_at = end + timedelta(seconds=1)
        events.append(("R143", "correct-anchor", Decimal(100), ref_at, "NVDA"))
    return tuple(events)


@pytest.mark.parametrize(("did", "seconds"), ANCHORS)
def test_rc03_exact_historical_anchor_public_value_lineage_and_repeat(
    did: str,
    seconds: int,
) -> None:
    owner, request = _public(did, _anchored_events(seconds), anchor=seconds)
    result = owner.materialise(request)
    assert result is not None
    assert result.result == (Decimal(120) / Decimal(100)).ln()
    assert {x.observation_occurrence_id for x in result.raw_input_lineage} == {
        "current",
        "distractor",
        "correct-anchor",
    }
    assert all(x.raw_signal_id == "R143" for x in result.raw_input_lineage)
    assert result.predecessor_occurrence_ids == ()
    assert owner.materialise(request) == result


@pytest.mark.parametrize(("did", "seconds"), ANCHORS)
def test_rc03_anchored_history_missing_past_and_late_reference_refused(
    did: str,
    seconds: int,
) -> None:
    owner, request = _public(did, _anchored_events(seconds, missing_anchor=True), anchor=seconds)
    assert owner.materialise(request) is None
    owner, request = _public(did, _anchored_events(seconds, late_reference=True), anchor=seconds)
    assert owner.materialise(request) is None


@pytest.mark.parametrize(
    ("did", "source", "reference", "expected"),
    (
        ("D022", "R043", Decimal(100), (Decimal(120) / Decimal(100)).ln()),
        ("D023", "R042", Decimal(80), (Decimal(120) / Decimal(80)).ln()),
        (
            "D026",
            "R137",
            Decimal(100),
            (
                ("price_difference", Decimal(20)),
                ("percent_difference", Decimal(20)),
            ),
        ),
    ),
)
def test_rc03_same_subject_scalar_public_result_and_refusal(
    did: str,
    source: str,
    reference: Decimal,
    expected: object,
) -> None:
    events = (
        ("R037", "latest", Decimal(120), NOW - timedelta(seconds=2), "NVDA"),
        (source, "reference", reference, NOW - timedelta(seconds=3), "NVDA"),
        (source, "cross-subject", Decimal(999), NOW - timedelta(seconds=1), "AMD"),
    )
    owner, request = _public(did, events)
    out = owner.materialise(request)
    assert out is not None and out.result == expected
    assert {x.observation_occurrence_id for x in out.raw_input_lineage} == {
        "latest",
        "reference",
    }
    assert owner.materialise(request) == out

    owner, request = _public(did, events, omitted=source)
    assert owner.materialise(request) is None
    wrong_subject = tuple(
        (rid, oid, value, ts, "AMD" if oid == "reference" else sub)
        for rid, oid, value, ts, sub in events
    )
    owner, request = _public(did, wrong_subject)
    assert owner.materialise(request) is None


# Every remaining RC03 raw-history row is independently exercised using its
# authoritative fixed/parameterised horizon and output family.
OTHER_HISTORY = (
    ("D027", "R137", 300, None, "vwap_rate"),
    ("D044", "R252", 300, None, "basis_points"),
    ("D045", "R249", 300, None, "basis_points"),
    ("D046", "R255", 300, None, "basis_points"),
    ("D048", "R245", 300, None, "percent"),
    ("D049", "R274", 300, None, "percent"),
    ("D050", "R275", 300, None, "percent"),
    ("D051", "R276", 300, None, "percent"),
    ("D052", "R236", 300, None, "point_and_percent"),
    ("D053", "R237", 300, None, "point_and_percent"),
    ("D054", "R238", 300, None, "point_and_percent"),
    ("D055", "R239", 300, None, "point_and_percent"),
    ("D056", "R240", 300, None, "point_and_percent"),
    ("D066", "R270", None, 1, "log"),
    ("D067", "R271", None, 1, "log"),
    ("D068", "R272", None, 1, "log"),
    ("D069", "R273", None, 1, "log"),
)


@pytest.mark.parametrize(("did", "rid", "seconds", "days", "family"), OTHER_HISTORY)
def test_rc03_public_history_all_named_k03_rows_exact_value_and_refusal(
    did: str,
    rid: str,
    seconds: int | None,
    days: int | None,
    family: str,
) -> None:
    anchor = timedelta(seconds=seconds) if seconds is not None else timedelta(days=days or 0)
    end = NOW - timedelta(seconds=2)
    current = Decimal("1.2") if family == "basis_points" else Decimal(120)
    prior = Decimal("1.1") if family == "basis_points" else Decimal(100)
    events = (
        (rid, "hist-current", current, end, "NVDA"),
        (rid, "hist-anchor", prior, end - anchor, "NVDA"),
        (rid, "hist-near", Decimal(999), end - anchor / 2, "NVDA"),
        (rid, "hist-other", Decimal(999), end - timedelta(seconds=1), "AMD"),
    )
    # The other rows are explicitly parameterised; D066-D069 use the fixed
    # official daily reference, not a guessed trading-session substitute.
    params = ("anchor_seconds", seconds) if seconds is not None else ("anchor_days", days)
    owner, request = _public(did, events, parameter=params)
    out = owner.materialise(request)
    if family == "vwap_rate":
        expected = (
            ("price_per_minute", Decimal(20) / Decimal(5)),
            ("percent_per_minute", Decimal(4)),
        )
    elif family == "basis_points":
        expected = Decimal(1000)
    elif family == "percent":
        expected = Decimal(20)
    elif family == "point_and_percent":
        expected = (
            ("point_change", Decimal(20)),
            ("percent_change", Decimal(20)),
        )
    else:
        expected = (Decimal(120) / Decimal(100)).ln()
    assert out is not None and out.result == expected
    assert {x.observation_occurrence_id for x in out.raw_input_lineage} == {
        "hist-current",
        "hist-anchor",
        "hist-near",
    }
    assert out.predecessor_occurrence_ids == ()
    assert owner.materialise(request) == out

    # The tempting nearer observation is not an admissible anchor.
    invalid = tuple(event for event in events if event[1] != "hist-anchor")
    owner, request = _public(did, invalid, parameter=params)
    assert owner.materialise(request) is None


def test_rc03_public_d024_uses_three_distinct_fixed_predecessor_anchors() -> None:
    end = NOW - timedelta(seconds=2)
    events = (
        ("R143", "compound-current", Decimal(120), end, "NVDA"),
        ("R143", "compound-1m", Decimal(110), end - timedelta(seconds=60), "NVDA"),
        ("R143", "compound-5m", Decimal(100), end - timedelta(seconds=300), "NVDA"),
        ("R143", "compound-30m", Decimal(80), end - timedelta(seconds=1800), "NVDA"),
    )
    owner, request = _public("D024", events)
    out = owner.materialise(request)
    assert out is not None
    q1 = (Decimal(120) / Decimal(110)).ln()
    q5 = (Decimal(120) / Decimal(100)).ln() / Decimal(5)
    q30 = (Decimal(120) / Decimal(80)).ln() / Decimal(30)
    assert out.result == (
        ("q1", q1),
        ("q5", q5),
        ("q30", q30),
        ("accel_1v5", q1 - q5),
        ("accel_5v30", q5 - q30),
    )
    assert {
        owner.reads.get_derived_occurrence(ref).derived_signal_id
        for ref in out.predecessor_occurrence_ids
    } == {"D019", "D020", "D021"}
    assert {r.observation_occurrence_id for r in out.raw_input_lineage} == {
        "compound-current",
        "compound-1m",
        "compound-5m",
        "compound-30m",
    }
    assert owner.materialise(request) == out


def test_rc03_public_d024_refuses_absent_thirty_minute_predecessor_history() -> None:
    end = NOW - timedelta(seconds=2)
    events = (
        ("R143", "short-current", Decimal(120), end, "NVDA"),
        ("R143", "short-1m", Decimal(110), end - timedelta(seconds=60), "NVDA"),
        ("R143", "short-5m", Decimal(100), end - timedelta(seconds=300), "NVDA"),
    )
    owner, request = _public("D024", events)
    # D024 may not invent its D021 thirty-minute predecessor from a shorter history.
    assert owner.materialise(request) is None


def test_rc03_public_history_ignores_future_received_competitor_at_cutoff() -> None:
    events = (
        *_anchored_events(60),
        ("R143", "future-quote", Decimal(800), NOW + timedelta(seconds=2), "NVDA"),
    )
    owner, request = _public("D019", events, anchor=60)
    out = owner.materialise(request)
    assert out is not None and out.result == (Decimal(120) / Decimal(100)).ln()
    assert "future-quote" not in {x.observation_occurrence_id for x in out.raw_input_lineage}
