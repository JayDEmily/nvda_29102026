"""Exactly two D026 public cases with independent exact oracles."""

from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest

from nvda_desk.market_measurement_truth import api as f
from nvda_desk.raw_signal_occurrence_truth import api as r

BRIEF = "a2f3fc76cd2cc846fd4885d4f3d3df7a1a3e5c7370700a613ecb0706c853412f"
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


T = datetime(2026, 10, 20, 12, 40, tzinfo=UTC)
CUTOFF, NOW = T + timedelta(seconds=1), T + timedelta(seconds=2)
S = "controlled-price-session/1"
CONTEXT = f.WindowContextV1(
    f.VersionRefV1("controlled-price-session", 1),
    datetime(2026, 10, 20, 12, tzinfo=UTC),
    datetime(2026, 10, 20, 13, tzinfo=UTC),
    datetime(2026, 10, 20, 12, tzinfo=UTC),
)
VWAP = r.RawSignalProjectionMappingV1(
    "mmt-session-provider-vwap",
    1,
    r.RawSignalCatalogueId("R137"),
    "foundation-pilot-fixture",
    "cash_quote_v1",
    ("vwap", "value"),
    "price",
    (("session", ("vwap", "session")), ("as_of", ("vwap", "as_of")), ("basis", ("vwap", "basis"))),
)
LAST = r.RawSignalProjectionMappingV1(
    "mmt-current-last",
    1,
    r.RawSignalCatalogueId("R037"),
    "foundation-pilot-fixture",
    "cash_quote_v1",
    ("trade", "last"),
    "price",
    (("session", ("session", "id")),),
)
MAPPINGS = (LAST, VWAP)
POLICY = f.InputSelectionPolicyVersionV1(
    "mmt-vwap-deviation-selection",
    1,
    ("subject_instrument", "session"),
    timedelta(seconds=60),
    timedelta(0),
    ("true_instant",),
    (),
    "foundation-pilot-fixture",
    "cash_quote_v1",
    "foundation-pilot-fixture/cash_quote_v1",
    100,
    1000,
)
UNIT = f.UnitConventionVersionV1("mmt-pilot-price", 1, "price", "price", Decimal("1"), Decimal("0"))
DEFINITION = f.CalculationDefinitionV1(
    "D026",
    "D026-VWAP-DEVIATION-1",
    "K03_CHANGE_RETURN",
    "last-vwap; 100*(last/vwap-1)",
    ("R037", "R137"),
    (),
    "P_WINDOW",
    "price / percent",
    "named_exact_vwap_deviation",
    tuple(f.AuthorityArtifactRefV1(*x) for x in AUTHORITY),
)
PARAMETER = f.CalculationParameterSetV1("mmt-vwap-deviation", 1, "P_WINDOW", "NVDA", ("NVDA",))


@pytest.mark.parametrize("refused", [False, True])
def test_d026_vwap_deviation(tmp_path, refused):
    raw = r.create_owner()
    _admit(
        raw,
        "last",
        T,
        {"trade": {"last": Decimal("101")}, "session": {"id": S}},
        ("R037",),
        "price",
        1,
    )
    _admit(
        raw,
        "vwap",
        T,
        {
            "vwap": {
                "value": Decimal("0" if refused else "120"),
                "session": S,
                "as_of": T.isoformat().replace("+00:00", "Z"),
                "basis": "cumulative_session",
            }
        },
        ("R137",),
        "price",
        2,
    )
    projected = (*_page(raw, LAST, CUTOFF, T), *_page(raw, VWAP, CUTOFF, T))
    assert [p.native_value for p in projected] == [
        Decimal("101"),
        Decimal("0" if refused else "120"),
    ]
    selected_ids = ("last", "vwap")

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
        pytest.fail(f"admitted D026 unsupported after lawful public source setup: {exc}")
    request = f.WindowCalculationRequestV1(
        f.CalculationRequestV1(
            "D026",
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
                for m in MAPPINGS
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
                derived_signal_id="D026",
                subject_instrument="NVDA",
                effective_at_or_before_utc=T,
                knowledge_at_or_before_utc=CUTOFF,
                limit=10,
            )
            == ()
        )
        return
    expected = f.VwapDeviationV1(f.ExactRatioV1(-19, 1), f.ExactRatioV1(-95, 6))
    by_id = {p.observation_occurrence_id.value: p for p in projected}
    lines = tuple(
        f.RawInputLineageV1(
            p.raw_signal_catalogue_id.value,
            identity,
            f.VersionRefV1(p.projection_mapping_id, 1),
            f.VersionRefV1(UNIT.context_id, 1),
            p,
            p.native_value,
            datetime.fromisoformat(p.source_timestamp_raw.replace("Z", "+00:00")),
        )
        for identity in selected_ids
        for p in (by_id[identity],)
    )
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
        MAPPINGS,
        lines,
        expected,
        2400,
        "price / percent",
        "named_exact_vwap_deviation",
        NOW,
    )
