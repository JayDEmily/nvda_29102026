"""Two approved D038 public jump-variation cases; independent fixed oracle."""

from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest

from nvda_desk.market_measurement_truth import api as f
from nvda_desk.raw_signal_occurrence_truth import api as r

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


@pytest.mark.parametrize("refused", [False, True], ids=["success", "refusal"])
def test_d038_signal(tmp_path, refused):
    raw = r.create_owner()
    records = [
        ("bar-" + str(i), event, event + timedelta(microseconds=500000), close, high, low, False)
        for i, (event, (close, high, low)) in enumerate(
            zip(
                TIMES,
                (
                    ("100", "101", "99"),
                    ("110", "111", "109"),
                    ("111.1", "112.1", "110.1"),
                    ("122.21", "123.21", "121.21"),
                ),
                strict=True,
            )
        )
    ]
    if refused:
        records.insert(2, ("older-complete", TIMES[2], TIMES[2], "111.1", "112.1", "110.1", False))
        current = records[3]
        records[3] = (*current[:-1], True)
    for sequence, (identity, event, receipt, close, high, low, missing_high) in enumerate(
        records, 1
    ):
        stamp = event.isoformat().replace("+00:00", "Z")
        bar = {
            "close": Decimal(close),
            "high": Decimal(high),
            "low": Decimal(low),
            "id": stamp,
            "end_utc": stamp,
            "duration_seconds": 60,
            "series": "TRADES",
            "adjustment_basis": "controlled_unadjusted/1",
        }
        if missing_high:
            del bar["high"]
        raw.commands.admit_raw_observation_occurrence(
            r.RawObservationOccurrenceV1(
                concept_id=r.concept_id("raw_signal.raw_observation_occurrence"),
                contract_id=r.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
                observation_occurrence_id=r.observation_occurrence_id(identity),
                delivery_artifact_ref=r.delivery_artifact_ref("controlled-delivery"),
                source_provider=r.provider_id(PROVIDER),
                native_record={"session": {"id": "controlled_cash_20261020"}, "bar": bar},
                received_ts_utc=receipt,
                ingestion_sequence=sequence,
                ingestion_sequence_scope=r.ingestion_sequence_scope(PROVIDER + "/" + VARIANT),
                source_temporal_kind="true_instant",
                raw_signal_catalogue_ids=tuple(
                    r.RawSignalCatalogueId(x) for x in ("R151", "R149", "R150")
                ),
                source_variant=VARIANT,
                subject_instrument="NVDA",
                native_units="price",
                source_timestamp_raw=stamp,
                source_timezone_native="UTC",
            )
        )
    projected = {}
    for mapping in MAPS:
        page = raw.reads.list_projected_raw_history(
            mapping.raw_signal_catalogue_id,
            mappings=(mapping,),
            subject_instrument="NVDA",
            received_at_or_before_utc=CUTOFF,
            event_at_or_before_utc=T,
            limit=100,
            cursor=None,
        )
        assert page.next_cursor is None
        projected[mapping.mapping_id] = {p.observation_occurrence_id.value: p for p in page.items}
    assert len(projected[MAPS[0].mapping_id]) == (5 if refused else 4)
    if refused:
        assert "bar-2" in projected[MAPS[0].mapping_id]
        assert "bar-2" in projected[MAPS[2].mapping_id]
        assert "bar-2" not in projected[MAPS[1].mapping_id]
        assert "older-complete" in projected[MAPS[1].mapping_id]
        assert (
            projected[MAPS[0].mapping_id]["bar-2"].received_ts_utc
            > projected[MAPS[0].mapping_id]["older-complete"].received_ts_utc
        )
    admission = f.OwnerAdmissionV1("M02", BRIEF)
    path = str(tmp_path / "m02.sqlite")
    owner = f.create_window_owner(
        admission=admission,
        raw_projection_reader=raw.reads,
        storage=f.SQLiteStorageV1(path, True),
        utc_now=lambda: NOW,
    )
    request = f.WindowCalculationRequestV1(
        f.CalculationRequestV1(
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
        ),
        CONTEXT,
        (),
    )
    result = owner.materialise(request)
    if refused:
        assert result is None
        assert (
            owner.reads.list_derived_history(
                derived_signal_id="D038",
                subject_instrument="NVDA",
                effective_at_or_before_utc=T,
                knowledge_at_or_before_utc=CUTOFF,
                limit=10,
            )
            == ()
        )
        return
    assert type(result) is f.WindowMeasurementOccurrenceV1
    expected_value = Decimal("0.015287684447969835944626693447037281426366216225509")
    assert type(result.result) is Decimal and result.result.as_tuple() == expected_value.as_tuple()
    assert result.request == request and result.definition == DEFINITION
    assert result.parameter_set == PARAMETER and result.input_selection_policy == POLICY
    assert result.unit_conventions == (UNIT,) and result.projection_mappings == MAPS
    expected_lines = []
    for i, event in enumerate(TIMES):
        for mapping in MAPS:
            item = projected[mapping.mapping_id]["bar-" + str(i)]
            expected_lines.append(
                f.RawInputLineageV1(
                    mapping.raw_signal_catalogue_id.value,
                    "bar-" + str(i),
                    f.VersionRefV1(mapping.mapping_id, 1),
                    f.VersionRefV1(UNIT.context_id, 1),
                    item,
                    item.native_value,
                    event,
                )
            )
    assert result.raw_input_lineage == tuple(expected_lines) and result.predecessors == ()
    assert result.owner_object_id == "M02"
    assert result.owner_namespace == "neutral_market_measurement_truth/window/v1"
    assert result.implementation_brief_sha256 == BRIEF and result.derived_signal_id == "D038"
    assert result.derived_occurrence_id.startswith("mmtwindow1:")
    assert result.window_seconds == 180 and result.units == "variance"
    assert result.result_shape == "scalar_decimal"
    assert (result.effective_as_of_utc, result.knowledge_cutoff_utc, result.calculated_at_utc) == (
        T,
        CUTOFF,
        NOW,
    )
    assert owner.reads.get_derived_occurrence(result.derived_occurrence_id) == result
    reader = f.create_window_reader(admission=admission, storage=f.SQLiteReadStorageV1(path))
    assert reader.get_derived_occurrence(result.derived_occurrence_id) == result
