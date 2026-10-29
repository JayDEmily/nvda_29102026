"""Exactly two D037 R151 controlled 20d risk cases."""

from datetime import UTC, datetime, timedelta
from decimal import Decimal
from itertools import pairwise

import pytest

from nvda_desk.market_measurement_truth import api as f
from nvda_desk.raw_signal_occurrence_truth import api as r

BRIEF = "16e0fd7b73f616284842ae2ad02ed80ac51e41fd07a1e3c83645f1fa6a3c8b8d"
AUTHORITY = (
    (
        "handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md",
        "603b850802a418780109095e7ae69bcece449da79fb24140a6d50297605e927c",
    ),
    (
        "handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv",
        "67bacbcf77afa766cec220a8d4a0f9589c9568d4a1f5c5818334915adf72e549",
    ),
)
D = "D037"
K = 37
STEM = "20d"
SAMPLES = tuple(
    datetime.fromisoformat(x)
    for x in [
        "2026-09-30T13:00:00+00:00",
        "2026-10-01T13:00:00+00:00",
        "2026-10-02T13:00:00+00:00",
        "2026-10-03T13:00:00+00:00",
        "2026-10-04T13:00:00+00:00",
        "2026-10-05T13:00:00+00:00",
        "2026-10-06T13:00:00+00:00",
        "2026-10-07T13:00:00+00:00",
        "2026-10-08T13:00:00+00:00",
        "2026-10-09T13:00:00+00:00",
        "2026-10-10T13:00:00+00:00",
        "2026-10-11T13:00:00+00:00",
        "2026-10-12T13:00:00+00:00",
        "2026-10-13T13:00:00+00:00",
        "2026-10-14T13:00:00+00:00",
        "2026-10-15T13:00:00+00:00",
        "2026-10-16T13:00:00+00:00",
        "2026-10-17T13:00:00+00:00",
        "2026-10-18T13:00:00+00:00",
        "2026-10-19T13:00:00+00:00",
        "2026-10-20T13:00:00+00:00",
    ]
)
T = SAMPLES[-1]
CUTOFF = T + timedelta(seconds=1)
NOW = CUTOFF + timedelta(seconds=1)
SESSIONS = tuple(
    f.SessionFrameV1(
        f.VersionRefV1(
            "controlled-risk-"
            + (datetime(2026, 9, 30, 12, tzinfo=UTC) + timedelta(days=i)).strftime("%Y%m%d"),
            1,
        ),
        "controlled_cash",
        datetime(2026, 9, 30, 12, tzinfo=UTC) + timedelta(days=i),
        datetime(2026, 9, 30, 13, tzinfo=UTC) + timedelta(days=i),
    )
    for i in range(21)
)
MAPPING = r.RawSignalProjectionMappingV1(
    "mmt-risk-close",
    1,
    r.RawSignalCatalogueId("R151"),
    "foundation-pilot-fixture",
    "cash_quote_v1",
    ("bar", "close"),
    "price",
    (
        ("session.id", ("session", "id")),
        ("sample.kind", ("sample", "kind")),
        ("adjustment.basis", ("adjustment", "basis")),
    ),
)
UNIT = f.UnitConventionVersionV1("mmt-pilot-price", 1, "price", "price", Decimal("1"), Decimal("0"))
POLICY = f.InputSelectionPolicyVersionV1(
    "mmt-d037-selection",
    1,
    ("subject_instrument", "session"),
    timedelta(days=30),
    timedelta(0),
    ("true_instant",),
    (),
    "foundation-pilot-fixture",
    "cash_quote_v1",
    "foundation-pilot-fixture/cash_quote_v1",
    100,
    1000,
)
PARAMETER = f.CalculationParameterSetV1("mmt-d037-controlled", 1, "P_VOL_WINDOW", "NVDA", ("NVDA",))
DEFINITION = f.CalculationDefinitionV1(
    D,
    D + "-REALISED-VOL-1",
    "K05_REALIZED_RISK",
    "sqrt(sum(ln(close_i/close_(i-1))^2)/sum(trading_year_fraction_i))",
    ("R151",),
    (),
    "P_VOL_WINDOW",
    "annualised_volatility",
    "scalar_decimal",
    tuple(f.AuthorityArtifactRefV1(*ref) for ref in AUTHORITY),
)
FRAC = f.ExactRatioV1(1, 15120) if K <= 34 else f.ExactRatioV1(1, 252)
INTERVALS = tuple(f.TradingReturnIntervalV1(a, b, FRAC) for a, b in pairwise(SAMPLES))
CONTEXT = f.RealisedRiskWindowContextV1(
    f.VersionRefV1("controlled-risk-20d-calendar", 1),
    SAMPLES[0],
    SAMPLES[-1],
    SESSIONS[0].start_utc,
    SESSIONS,
    SAMPLES,
    INTERVALS,
)


def _kind(event):
    return (
        "official_close"
        if event.hour == 13
        else "session_open"
        if event.hour == 12 and event.minute == 0
        else "minute_close"
    )


def _admit(raw, identity, event, value, seq):
    native = {
        "session": {"id": "controlled-risk-" + event.strftime("%Y%m%d") + "/1"},
        "sample": {"kind": _kind(event)},
        "adjustment": {"basis": "unadjusted"},
        "bar": {"close": Decimal(value)},
    }
    raw.commands.admit_raw_observation_occurrence(
        r.RawObservationOccurrenceV1(
            concept_id=r.concept_id("raw_signal.raw_observation_occurrence"),
            contract_id=r.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
            observation_occurrence_id=r.observation_occurrence_id(identity),
            delivery_artifact_ref=r.delivery_artifact_ref("controlled-delivery"),
            source_provider=r.provider_id("foundation-pilot-fixture"),
            native_record=native,
            received_ts_utc=event,
            ingestion_sequence=seq,
            ingestion_sequence_scope=r.ingestion_sequence_scope(
                "foundation-pilot-fixture/cash_quote_v1"
            ),
            source_temporal_kind="true_instant",
            raw_signal_catalogue_ids=(r.RawSignalCatalogueId("R151"),),
            source_variant="cash_quote_v1",
            subject_instrument="NVDA",
            native_units="price",
            source_timestamp_raw=event.isoformat().replace("+00:00", "Z"),
            source_timezone_native="UTC",
        )
    )


def _page(raw, cutoff, asof):
    page = raw.reads.list_projected_raw_history(
        r.RawSignalCatalogueId("R151"),
        mappings=(MAPPING,),
        subject_instrument="NVDA",
        received_at_or_before_utc=cutoff,
        event_at_or_before_utc=asof,
        limit=100,
        cursor=None,
    )
    assert page.next_cursor is None
    return page.items


@pytest.mark.parametrize("refused", [False, True], ids=["success", "refusal"])
def test_d037_signal(tmp_path, refused):
    raw = r.create_owner()
    missing = tuple(range(10))
    for i, event in enumerate(SAMPLES):
        if refused and i in missing:
            continue
        _admit(raw, "sample-" + str(i), event, "110" if i == len(SAMPLES) - 1 else "100", i + 1)
    projected = _page(raw, CUTOFF, T)
    assert len(projected) == len(SAMPLES) - len(missing if refused else ())
    admission = f.OwnerAdmissionV1("M02", BRIEF)
    path = str(tmp_path / "m02.sqlite")
    try:
        owner = f.create_window_owner(
            admission=admission,
            raw_projection_reader=raw.reads,
            storage=f.SQLiteStorageV1(path, True),
            utc_now=lambda: NOW,
        )
    except ValueError as exc:
        pytest.fail(f"admitted {D} unsupported after lawful public R151 setup: {exc}")
    request = f.WindowCalculationRequestV1(
        f.CalculationRequestV1(
            D,
            "NVDA",
            T,
            CUTOFF,
            DEFINITION.calculation_definition_version,
            f.VersionRefV1(PARAMETER.context_id, 1),
            f.VersionRefV1(POLICY.context_id, 1),
            (CONTEXT.ref,),
            (
                f.RawInputBindingV1(
                    "R151",
                    f.VersionRefV1(MAPPING.mapping_id, 1),
                    f.VersionRefV1(UNIT.context_id, 1),
                    "NVDA",
                ),
            ),
        ),
        CONTEXT,
        (),
    )
    result = owner.materialise(request)
    if refused:
        assert result is None
        assert (
            owner.reads.list_derived_history(
                derived_signal_id=D,
                subject_instrument="NVDA",
                effective_at_or_before_utc=T,
                knowledge_at_or_before_utc=CUTOFF,
                limit=10,
            )
            == ()
        )
        return
    assert type(result) is f.WindowMeasurementOccurrenceV1
    expected = Decimal("0.33831757671837337403929019188671516632423102188566")
    assert type(result.result) is Decimal and result.result.as_tuple() == expected.as_tuple()
    assert (
        result.owner_object_id == "M02"
        and result.owner_namespace == "neutral_market_measurement_truth/window/v1"
    )
    assert result.implementation_brief_sha256 == BRIEF and result.derived_signal_id == D
    assert result.derived_occurrence_id.startswith("mmtwindow1:")
    assert result.request == request and result.definition == DEFINITION
    assert result.parameter_set == PARAMETER and result.input_selection_policy == POLICY
    assert result.unit_conventions == (UNIT,) and result.projection_mappings == (MAPPING,)
    by_id = {p.observation_occurrence_id.value: p for p in projected}
    lines = tuple(
        f.RawInputLineageV1(
            "R151",
            "sample-" + str(i),
            f.VersionRefV1(MAPPING.mapping_id, 1),
            f.VersionRefV1(UNIT.context_id, 1),
            by_id["sample-" + str(i)],
            by_id["sample-" + str(i)].native_value,
            event,
        )
        for i, event in enumerate(SAMPLES)
    )
    assert result.raw_input_lineage == lines and result.predecessors == ()
    assert result.window_seconds == 1728000 and result.units == "annualised_volatility"
    assert result.result_shape == "scalar_decimal"
    assert result.effective_as_of_utc == T and result.knowledge_cutoff_utc == CUTOFF
    assert result.calculated_at_utc == NOW
    assert owner.reads.get_derived_occurrence(result.derived_occurrence_id) == result
    reader = f.create_window_reader(admission=admission, storage=f.SQLiteReadStorageV1(path))
    assert reader.get_derived_occurrence(result.derived_occurrence_id) == result
