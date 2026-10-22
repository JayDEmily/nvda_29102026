"""Exactly two D028 controlled baseline cases."""

from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest

from nvda_desk.market_measurement_truth import api as f
from nvda_desk.raw_signal_occurrence_truth import api as r

BRIEF = "c0c2788a727681d87f7b971d242f263d0f04657c896cc113bcf8a57126e684a9"
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


def _admit(raw, identity, event, native, tags, units, sequence, receipt=None):
    raw.commands.admit_raw_observation_occurrence(
        r.RawObservationOccurrenceV1(
            concept_id=r.concept_id("raw_signal.raw_observation_occurrence"),
            contract_id=r.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
            observation_occurrence_id=r.observation_occurrence_id(identity),
            delivery_artifact_ref=r.delivery_artifact_ref("controlled-delivery"),
            source_provider=r.provider_id("foundation-pilot-fixture"),
            native_record=native,
            received_ts_utc=receipt or event,
            ingestion_sequence=sequence,
            ingestion_sequence_scope=r.ingestion_sequence_scope(
                "foundation-pilot-fixture/cash_quote_v1"
            ),
            source_temporal_kind="true_instant",
            raw_signal_catalogue_ids=tuple(r.RawSignalCatalogueId(t) for t in tags),
            source_variant="cash_quote_v1",
            subject_instrument="NVDA",
            native_units=units,
            source_timestamp_raw=event.isoformat().replace("+00:00", "Z"),
            source_timezone_native="UTC",
        )
    )


def _page(raw, mapping, cutoff, event):
    page = raw.reads.list_projected_raw_history(
        mapping.raw_signal_catalogue_id,
        mappings=(mapping,),
        subject_instrument="NVDA",
        received_at_or_before_utc=cutoff,
        event_at_or_before_utc=event,
        limit=100,
        cursor=None,
    )
    assert page.next_cursor is None
    return page.items


def _assert_result(
    result,
    owner,
    admission,
    path,
    request,
    definition,
    parameter,
    policy,
    unit,
    mappings,
    expected_lines,
    expected,
    seconds,
    units,
    shape,
    now,
):
    assert type(result) is f.WindowMeasurementOccurrenceV1
    if type(expected) is Decimal:
        assert type(result.result) is Decimal and result.result.as_tuple() == expected.as_tuple()
    else:
        assert type(result.result) is type(expected) and result.result == expected
    assert result.owner_object_id == "M02" and result.implementation_brief_sha256 == BRIEF
    assert result.owner_namespace == "neutral_market_measurement_truth/window/v1"
    assert (
        result.derived_signal_id == request.calculation.derived_signal_id
        and result.derived_occurrence_id.startswith("mmtwindow1:")
    )
    assert (
        result.request == request
        and result.definition == definition
        and result.parameter_set == parameter
    )
    assert (
        result.input_selection_policy == policy
        and result.unit_conventions == (unit,)
        and result.projection_mappings == mappings
    )
    assert result.raw_input_lineage == expected_lines and result.predecessors == ()
    assert (
        result.window_seconds == seconds and result.units == units and result.result_shape == shape
    )
    assert (
        result.effective_as_of_utc == request.calculation.as_of_utc
        and result.knowledge_cutoff_utc == request.calculation.knowledge_cutoff_utc
        and result.calculated_at_utc == now
    )
    assert owner.reads.get_derived_occurrence(result.derived_occurrence_id) == result
    reader = f.create_window_reader(admission=admission, storage=f.SQLiteReadStorageV1(path))
    assert reader.get_derived_occurrence(result.derived_occurrence_id) == result


T = datetime(2026, 10, 20, 12, 30, tzinfo=UTC)
CUTOFF, NOW = T + timedelta(seconds=1), T + timedelta(seconds=2)
DATES = tuple(datetime(2026, 9, 29, 12, tzinfo=UTC) + timedelta(days=i) for i in range(22))
N = 2
MAPPING = r.RawSignalProjectionMappingV1(
    "mmt-session-volume",
    1,
    r.RawSignalCatalogueId("R041"),
    "foundation-pilot-fixture",
    "cash_quote_v1",
    ("session", "volume"),
    "shares",
    (
        ("session.id", ("session", "id")),
        ("counter.generation", ("counter", "generation")),
        ("counter.basis", ("counter", "basis")),
        ("counter.complete_from_open", ("counter", "complete_from_open")),
    ),
)
UNIT = f.UnitConventionVersionV1("mmt-shares", 1, "shares", "shares", Decimal("1"), Decimal("0"))
POLICY = f.InputSelectionPolicyVersionV1(
    "mmt-relative-volume-2sessions-selection",
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
PARAMETER = f.CalculationParameterSetV1(
    "mmt-relative-volume-2sessions", 1, "P_BASELINE", "NVDA", ("NVDA",)
)
DEFINITION = f.CalculationDefinitionV1(
    "D028",
    "D028-RELATIVE-VOLUME-1",
    "K04_RELATIVE_ACTIVITY",
    "current / mean(prior_same_fraction)",
    ("R041",),
    (),
    "P_BASELINE",
    "multiple",
    "exact_ratio",
    tuple(
        f.AuthorityArtifactRefV1(*x)
        for x in AUTHORITY
        + (
            (
                "handoff/m01_completion/authority/D028_OWNER_APPROVED_RAW_VOLUME_BASELINE_AMENDMENT_20261017.md",
                "115edc89241c9973793f2c74bdc2f4f946a42fe38217b2462c2cab932fa1837c",
            ),
        )
    ),
)


@pytest.mark.parametrize("refused", [False, True])
def test_d028_relative_volume(tmp_path, refused):
    raw = r.create_owner()
    required = DATES[-N - 1 : -1]
    rows = [("current", DATES[-1], T, "30", True, "minute-ending-1230/1", None)]
    for i, start in enumerate(required):
        event = start + timedelta(minutes=30)
        value = str(10 + 10 * i)
        complete = True
        bucket = "minute-ending-1230/1"
        receipt = None
        if refused and i == 1:
            complete = False
        rows.append(("prior-" + str(i), start, event, value, complete, bucket, receipt))
    rows.extend(
        (
            (
                "wrong-fraction",
                DATES[-2],
                DATES[-2] + timedelta(minutes=31),
                "999",
                True,
                "minute-ending-1231/1",
                None,
            ),
            (
                "older",
                DATES[-4],
                DATES[-4] + timedelta(minutes=30),
                "999",
                True,
                "minute-ending-1230/1",
                None,
            ),
        )
    )
    for seq, (identity, start, event, value, complete, bucket, receipt) in enumerate(rows, 1):
        session = "controlled-volume-" + start.strftime("%Y%m%d") + "/1"
        native = {
            "session": {"id": session, "volume": Decimal(value)},
            "counter": {
                "generation": "counter-" + start.strftime("%Y%m%d") + "/1",
                "basis": "cash_shares_unadjusted",
                "complete_from_open": complete,
            },
        }
        _admit(raw, identity, event, native, ("R041",), "shares", seq, receipt)
    projected = _page(raw, MAPPING, CUTOFF, T)
    assert len(projected) == len(rows)
    assert all(p.selection_identity is not None for p in projected)
    admission = f.OwnerAdmissionV1("M02", BRIEF)
    path = str(tmp_path / "result.sqlite")
    try:
        owner = f.create_window_owner(
            admission=admission,
            raw_projection_reader=raw.reads,
            storage=f.SQLiteStorageV1(path, True),
            utc_now=lambda: NOW,
        )
    except ValueError as exc:
        pytest.fail(f"admitted D028 unsupported after lawful public raw setup: {exc}")
    context = f.BaselineWindowContextV1(
        f.VersionRefV1("controlled-volume-calendar", 1),
        DATES[-1],
        DATES[-1] + timedelta(hours=1),
        DATES[0],
        tuple(
            f.SessionFrameV1(
                f.VersionRefV1("controlled-volume-" + d.strftime("%Y%m%d"), 1),
                "controlled_cash",
                d,
                d + timedelta(hours=1),
            )
            for d in DATES
        ),
        N,
        1800,
    )
    request = f.WindowCalculationRequestV1(
        f.CalculationRequestV1(
            "D028",
            "NVDA",
            T,
            CUTOFF,
            DEFINITION.calculation_definition_version,
            f.VersionRefV1(PARAMETER.context_id, 1),
            f.VersionRefV1(POLICY.context_id, 1),
            (context.ref,),
            (
                f.RawInputBindingV1(
                    "R041",
                    f.VersionRefV1(MAPPING.mapping_id, 1),
                    f.VersionRefV1(UNIT.context_id, 1),
                    "NVDA",
                ),
            ),
        ),
        context,
        (),
    )
    result = owner.materialise(request)
    if refused:
        assert result is None
        assert (
            owner.reads.list_derived_history(
                derived_signal_id="D028",
                subject_instrument="NVDA",
                effective_at_or_before_utc=T,
                knowledge_at_or_before_utc=CUTOFF,
                limit=10,
            )
            == ()
        )
        return
    by_id = {p.observation_occurrence_id.value: p for p in projected}
    lines = tuple(
        f.RawInputLineageV1(
            "R041",
            identity,
            f.VersionRefV1(MAPPING.mapping_id, 1),
            f.VersionRefV1(UNIT.context_id, 1),
            p,
            p.native_value,
            datetime.fromisoformat(p.source_timestamp_raw.replace("Z", "+00:00")),
        )
        for identity in ("current", *("prior-" + str(i) for i in range(N)))
        for p in (by_id[identity],)
    )
    expected = f.ExactRatioV1(2, 1)
    _assert_result(
        result,
        owner,
        admission,
        path,
        request,
        DEFINITION,
        PARAMETER,
        POLICY,
        UNIT,
        (MAPPING,),
        lines,
        expected,
        1800,
        "multiple",
        "exact_ratio",
        NOW,
    )
