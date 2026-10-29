"""Exactly two D020 cases: independent rounded oracle and missing 300s anchor."""

from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest

from nvda_desk.market_measurement_truth import api as f
from nvda_desk.raw_signal_occurrence_truth import api as r

BRIEF = "811906fdfb073da9b5a7ba137563953d6ff977d50bfe99b8f43adb068f20e839"
ASOF = datetime(2026, 10, 20, 12, 10, tzinfo=UTC)
CUTOFF = ASOF + timedelta(seconds=1)
NOW = CUTOFF + timedelta(seconds=1)
EXPECTED = Decimal("0.18232155679395462621171802515451463319738933791449")
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


def _mapping():
    return r.RawSignalProjectionMappingV1(
        "mmt-bar-close",
        1,
        r.RawSignalCatalogueId("R143"),
        "foundation-pilot-fixture",
        "cash_quote_v1",
        ("bar", "close"),
        "price",
        (),
    )


@pytest.mark.parametrize("missing_reference", [False, True])
def test_d020_five_minute_log_return(tmp_path, missing_reference):
    raw = r.create_owner()
    records = [("current", 0, "120"), ("post-anchor", 60, "110")]
    if not missing_reference:
        records.append(("reference", 300, "100"))
    for sequence, (identity, age, price) in enumerate(records, 1):
        event = ASOF - timedelta(seconds=age)
        raw.commands.admit_raw_observation_occurrence(
            r.RawObservationOccurrenceV1(
                concept_id=r.concept_id("raw_signal.raw_observation_occurrence"),
                contract_id=r.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
                observation_occurrence_id=r.observation_occurrence_id(identity),
                delivery_artifact_ref=r.delivery_artifact_ref("controlled-close-delivery"),
                source_provider=r.provider_id("foundation-pilot-fixture"),
                native_record={"bar": {"close": Decimal(price)}},
                received_ts_utc=event,
                ingestion_sequence=sequence,
                ingestion_sequence_scope=r.ingestion_sequence_scope(
                    "foundation-pilot-fixture/cash_quote_v1"
                ),
                source_temporal_kind="true_instant",
                raw_signal_catalogue_ids=(r.RawSignalCatalogueId("R143"),),
                source_variant="cash_quote_v1",
                subject_instrument="NVDA",
                native_units="price",
                source_timestamp_raw=event.isoformat().replace("+00:00", "Z"),
                source_timezone_native="UTC",
            )
        )
    page = raw.reads.list_projected_raw_history(
        r.RawSignalCatalogueId("R143"),
        mappings=(_mapping(),),
        subject_instrument="NVDA",
        received_at_or_before_utc=CUTOFF,
        event_at_or_before_utc=ASOF,
        limit=100,
        cursor=None,
    )
    ids = {item.observation_occurrence_id.value for item in page.items}
    assert ids == (
        {"current", "post-anchor"} if missing_reference else {"current", "post-anchor", "reference"}
    )
    assert page.next_cursor is None
    admission = f.OwnerAdmissionV1("M02", BRIEF)
    path = str(tmp_path / "return.sqlite")
    try:
        owner = f.create_window_owner(
            admission=admission,
            raw_projection_reader=raw.reads,
            storage=f.SQLiteStorageV1(path, True),
            utc_now=lambda: NOW,
        )
    except ValueError as exc:
        pytest.fail(f"admitted D020 calculation is unsupported: {exc}")
    context = f.WindowContextV1(
        f.VersionRefV1("controlled-close-session", 1),
        ASOF - timedelta(minutes=10),
        ASOF + timedelta(minutes=50),
        ASOF - timedelta(minutes=10),
    )
    request = f.WindowCalculationRequestV1(
        f.CalculationRequestV1(
            "D020",
            "NVDA",
            ASOF,
            CUTOFF,
            "D020-LOG-RETURN-1",
            f.VersionRefV1("mmt-log-300s-50d-half-even", 1),
            f.VersionRefV1("mmt-close-selection", 1),
            (context.ref,),
            (
                f.RawInputBindingV1(
                    "R143",
                    f.VersionRefV1("mmt-bar-close", 1),
                    f.VersionRefV1("mmt-pilot-price", 1),
                    "NVDA",
                ),
            ),
        ),
        context,
        (),
    )
    result = owner.materialise(request)
    if missing_reference:
        assert result is None
        assert (
            owner.reads.list_derived_history(
                derived_signal_id="D020",
                subject_instrument="NVDA",
                effective_at_or_before_utc=ASOF,
                knowledge_at_or_before_utc=CUTOFF,
                limit=10,
            )
            == ()
        )
        return
    assert type(result) is f.WindowMeasurementOccurrenceV1
    assert type(result.result) is Decimal and result.result.as_tuple() == EXPECTED.as_tuple()
    assert result.owner_object_id == "M02" and result.implementation_brief_sha256 == BRIEF
    assert result.owner_namespace == "neutral_market_measurement_truth/window/v1"
    assert result.derived_signal_id == "D020" and result.derived_occurrence_id.startswith(
        "mmtwindow1:"
    )
    assert result.request == request and result.window_seconds == 300
    assert result.definition == f.CalculationDefinitionV1(
        "D020",
        "D020-LOG-RETURN-1",
        "K03_CHANGE_RETURN",
        "ln(close_t / close_reference)",
        ("R143",),
        (),
        "P_WINDOW",
        "return",
        "scalar_decimal",
        tuple(f.AuthorityArtifactRefV1(*ref) for ref in AUTHORITY),
    )
    assert result.parameter_set == f.CalculationParameterSetV1(
        "mmt-log-300s-50d-half-even",
        1,
        "P_WINDOW",
        "NVDA",
        ("NVDA",),
    )
    assert result.input_selection_policy == f.InputSelectionPolicyVersionV1(
        "mmt-close-selection",
        1,
        ("subject_instrument",),
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
    assert result.unit_conventions == (
        f.UnitConventionVersionV1(
            "mmt-pilot-price",
            1,
            "price",
            "price",
            Decimal("1"),
            Decimal("0"),
        ),
    )
    assert result.projection_mappings == (_mapping(),) and result.predecessors == ()
    assert result.units == "return" and result.result_shape == "scalar_decimal"
    assert result.effective_as_of_utc == ASOF and result.knowledge_cutoff_utc == CUTOFF
    assert result.calculated_at_utc == NOW
    expected_lines = []
    for identity, seconds, price in (("current", 0, "120"), ("reference", 300, "100")):
        projection = raw.reads.project_raw_value(
            r.RawSignalCatalogueId("R143"),
            r.observation_occurrence_id(identity),
            mappings=(_mapping(),),
        )
        assert projection.native_value == Decimal(price)
        expected_lines.append(
            f.RawInputLineageV1(
                "R143",
                identity,
                f.VersionRefV1("mmt-bar-close", 1),
                f.VersionRefV1("mmt-pilot-price", 1),
                projection,
                Decimal(price),
                ASOF - timedelta(seconds=seconds),
            )
        )
    assert result.raw_input_lineage == tuple(expected_lines)
    assert owner.reads.get_derived_occurrence(result.derived_occurrence_id) == result
    reader = f.create_window_reader(admission=admission, storage=f.SQLiteReadStorageV1(path))
    assert reader.get_derived_occurrence(result.derived_occurrence_id) == result
