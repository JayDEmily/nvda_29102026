"""Two new D042 public controlled macro cases."""

from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest

from nvda_desk.market_measurement_truth import api as f
from nvda_desk.raw_signal_occurrence_truth import api as r

BRIEF = "fd69f8a6f1c9f015ac2c01351c93fe9ea91d94730e1c0a43b47865a616e14bd3"
D, DAYS = "D042", 0
T = datetime(2026, 10, 20, 13, tzinfo=UTC)
CUTOFF, NOW = T + timedelta(seconds=1), T + timedelta(seconds=2)
RAW = ("R247", "R249")
SERIES = (
    ("DGS2", "rate_fraction", "not_applicable"),
    ("DGS10", "rate_fraction", "not_applicable"),
)
CONTEXT = f.WindowContextV1(
    f.VersionRefV1("controlled-macro-history", 1),
    T - timedelta(days=30),
    T + timedelta(seconds=1),
    T - timedelta(days=30),
)
META = (
    ("metric.series", ("metric", "series")),
    ("metric.measurement_date", ("metric", "measurement_date")),
    ("metric.method", ("metric", "method")),
    ("metric.quote_orientation", ("metric", "quote_orientation")),
)
MAPS = tuple(
    r.RawSignalProjectionMappingV1(
        "mmt-macro-" + rid.lower(),
        1,
        r.RawSignalCatalogueId(rid),
        "foundation-controlled-macro",
        "macro_snapshot_v1",
        ("metric", "value"),
        spec[1],
        META,
    )
    for rid, spec in zip(RAW, SERIES, strict=True)
)
UNITS = tuple(
    f.UnitConventionVersionV1(
        "mmt-macro-" + rid.lower() + "-units", 1, spec[1], spec[1], Decimal("1"), Decimal("0")
    )
    for rid, spec in zip(RAW, SERIES, strict=True)
)
POLICY = f.InputSelectionPolicyVersionV1(
    "mmt-d042-selection",
    1,
    ("subject_instrument", "metric.series"),
    timedelta(days=30),
    timedelta(0),
    ("true_instant",),
    (),
    "foundation-controlled-macro",
    "macro_snapshot_v1",
    "foundation-controlled-macro/macro_snapshot_v1",
    100,
    1000,
)
PARAMETER = f.CalculationParameterSetV1("mmt-d042-controlled", 1, "P_BASIC", "NVDA", ("NVDA",))
DEFINITION = f.CalculationDefinitionV1(
    D,
    D + "-RATE-SLOPE-1",
    "K02_ALGEBRA",
    "100*(second-first)",
    RAW,
    (),
    "P_BASIC",
    "percentage_points",
    "scalar_decimal",
    (
        f.AuthorityArtifactRefV1(
            "handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md",
            "603b850802a418780109095e7ae69bcece449da79fb24140a6d50297605e927c",
        ),
        f.AuthorityArtifactRefV1(
            "handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv",
            "67bacbcf77afa766cec220a8d4a0f9589c9568d4a1f5c5818334915adf72e549",
        ),
    ),
)


@pytest.mark.parametrize("refused", [False, True], ids=["success", "refusal"])
def test_d042_signal(tmp_path, refused):
    raw = r.create_owner()
    values = [".0425", ".0390"]
    records = [(0, T, values[0]), (1, T, values[1])]

    for i, (role, event, value) in enumerate(records):
        series, unit, orientation = SERIES[role]
        metric = {
            "value": Decimal(value),
            "series": series,
            "measurement_date": event.date().isoformat(),
            "method": "controlled_snapshot/1",
            "quote_orientation": orientation,
        }
        receipt = event
        if refused and i == 0:
            receipt = CUTOFF + timedelta(seconds=1)
        if receipt < event:
            receipt = event
        raw.commands.admit_raw_observation_occurrence(
            r.RawObservationOccurrenceV1(
                concept_id=r.concept_id("raw_signal.raw_observation_occurrence"),
                contract_id=r.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
                observation_occurrence_id=r.observation_occurrence_id("record-" + str(i)),
                delivery_artifact_ref=r.delivery_artifact_ref("controlled-delivery"),
                source_provider=r.provider_id("foundation-controlled-macro"),
                native_record={"metric": metric},
                received_ts_utc=receipt,
                ingestion_sequence=i + 1,
                ingestion_sequence_scope=r.ingestion_sequence_scope(
                    "foundation-controlled-macro/macro_snapshot_v1"
                ),
                source_temporal_kind="true_instant",
                raw_signal_catalogue_ids=(r.RawSignalCatalogueId(RAW[role]),),
                source_variant="macro_snapshot_v1",
                subject_instrument="NVDA",
                native_units=unit,
                source_timestamp_raw=event.isoformat().replace("+00:00", "Z"),
                source_timezone_native="UTC",
            )
        )
    # Direct public projection establishes actual inputs, including late-received negatives.
    projected = {}
    for mapping in MAPS:
        page = raw.reads.list_projected_raw_history(
            mapping.raw_signal_catalogue_id,
            mappings=(mapping,),
            subject_instrument="NVDA",
            received_at_or_before_utc=CUTOFF + timedelta(seconds=1),
            event_at_or_before_utc=T,
            limit=100,
            cursor=None,
        )
        assert page.next_cursor is None
        projected.update({p.observation_occurrence_id.value: p for p in page.items})
    assert len(projected) == len(records)
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
            D,
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
                    f.VersionRefV1(u.context_id, 1),
                    "NVDA",
                )
                for m, u in zip(MAPS, UNITS, strict=True)
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
    expected_value = Decimal("-0.35")
    assert type(result.result) is type(expected_value) and result.result == expected_value
    assert result.result.as_tuple() == expected_value.as_tuple()
    assert result.request == request and result.definition == DEFINITION
    assert result.parameter_set == PARAMETER and result.input_selection_policy == POLICY
    assert result.projection_mappings == MAPS and result.unit_conventions == UNITS
    expected_lines = []
    for i, (role, event, _) in enumerate(records[:2]):
        mapping, unit = MAPS[role], UNITS[role]
        item = projected["record-" + str(i)]
        expected_lines.append(
            f.RawInputLineageV1(
                RAW[role],
                "record-" + str(i),
                f.VersionRefV1(mapping.mapping_id, 1),
                f.VersionRefV1(unit.context_id, 1),
                item,
                item.native_value,
                event,
            )
        )
    assert result.raw_input_lineage == tuple(expected_lines) and result.predecessors == ()
    assert (
        result.owner_object_id == "M02"
        and result.owner_namespace == "neutral_market_measurement_truth/window/v1"
    )
    assert result.implementation_brief_sha256 == BRIEF and result.derived_signal_id == D
    assert result.derived_occurrence_id.startswith("mmtwindow1:")
    assert (
        result.window_seconds == DAYS * 86400
        and result.units == "percentage_points"
        and result.result_shape == "scalar_decimal"
    )
    assert (result.effective_as_of_utc, result.knowledge_cutoff_utc, result.calculated_at_utc) == (
        T,
        CUTOFF,
        NOW,
    )
    assert owner.reads.get_derived_occurrence(result.derived_occurrence_id) == result
    reader = f.create_window_reader(admission=admission, storage=f.SQLiteReadStorageV1(path))
    assert reader.get_derived_occurrence(result.derived_occurrence_id) == result
