"""Two D039 public two-bar ATR cases; fixed independent arithmetic."""

from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest

from nvda_desk.market_measurement_truth import api as f
from nvda_desk.raw_signal_occurrence_truth import api as r

BRIEF = "a557c9d3572099fec9389848d94edba4b5ff17ba47bdce2e3f6e21c67e89ea5c"
T = datetime(2026, 10, 20, 12, 40, tzinfo=UTC)
CUTOFF, NOW = T + timedelta(seconds=1), T + timedelta(seconds=2)
TIMES = (T - timedelta(minutes=10), T - timedelta(minutes=5), T)
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
CONTEXT = f.WindowContextV1(
    f.VersionRefV1("controlled-atr-session", 1),
    datetime(2026, 10, 20, 12, tzinfo=UTC),
    datetime(2026, 10, 20, 13, tzinfo=UTC),
    datetime(2026, 10, 20, 12, tzinfo=UTC),
)
META = (
    ("session.id", ("session", "id")),
    ("bar.id", ("bar", "id")),
    ("bar.duration_seconds", ("bar", "duration_seconds")),
    ("adjustment.basis", ("adjustment", "basis")),
)
MAPS = tuple(
    r.RawSignalProjectionMappingV1(
        "mmt-atr-" + field,
        1,
        r.RawSignalCatalogueId(rid),
        "foundation-pilot-fixture",
        "cash_quote_v1",
        ("bar", field),
        "price",
        META,
    )
    for rid, field in (("R141", "high"), ("R142", "low"), ("R143", "close"))
)
UNIT = f.UnitConventionVersionV1("mmt-pilot-price", 1, "price", "price", Decimal("1"), Decimal("0"))
POLICY = f.InputSelectionPolicyVersionV1(
    "mmt-d039-selection",
    1,
    ("subject_instrument", "session"),
    timedelta(minutes=10),
    timedelta(0),
    ("true_instant",),
    (),
    "foundation-pilot-fixture",
    "cash_quote_v1",
    "foundation-pilot-fixture/cash_quote_v1",
    100,
    1000,
)
PARAMETER = f.CalculationParameterSetV1("mmt-d039-controlled", 1, "P_VOL_WINDOW", "NVDA", ("NVDA",))
DEFINITION = f.CalculationDefinitionV1(
    "D039",
    "D039-ATR-1",
    "K05_REALIZED_RISK",
    "mean(max(high-low,abs(high-prev_close),abs(low-prev_close))); bar_count=2; bar_seconds=300",
    ("R141", "R142", "R143"),
    (),
    "P_VOL_WINDOW",
    "price",
    "exact_ratio",
    tuple(f.AuthorityArtifactRefV1(*x) for x in AUTHORITY),
)


@pytest.mark.parametrize("refused", [False, True], ids=["success", "refusal"])
def test_d039_signal(tmp_path, refused):
    raw = r.create_owner()
    for i, (event, values) in enumerate(
        zip(TIMES, ((101, 99, 100), (110, 90, 105), (112, 99, 108)), strict=True)
    ):
        bar = {
            "id": event.isoformat().replace("+00:00", "Z"),
            "duration_seconds": 300,
            **{k: Decimal(v) for k, v in zip(("high", "low", "close"), values, strict=True)},
        }
        if refused and i == 2:
            del bar["high"]
        raw.commands.admit_raw_observation_occurrence(
            r.RawObservationOccurrenceV1(
                concept_id=r.concept_id("raw_signal.raw_observation_occurrence"),
                contract_id=r.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
                observation_occurrence_id=r.observation_occurrence_id("bar-" + str(i)),
                delivery_artifact_ref=r.delivery_artifact_ref("controlled-delivery"),
                source_provider=r.provider_id("foundation-pilot-fixture"),
                native_record={
                    "session": {"id": "controlled-atr-session/1"},
                    "adjustment": {"basis": "unadjusted"},
                    "bar": bar,
                },
                received_ts_utc=event,
                ingestion_sequence=i + 1,
                ingestion_sequence_scope=r.ingestion_sequence_scope(
                    "foundation-pilot-fixture/cash_quote_v1"
                ),
                source_temporal_kind="true_instant",
                raw_signal_catalogue_ids=tuple(
                    r.RawSignalCatalogueId(x) for x in ("R141", "R142", "R143")
                ),
                source_variant="cash_quote_v1",
                subject_instrument="NVDA",
                native_units="price",
                source_timestamp_raw=event.isoformat().replace("+00:00", "Z"),
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
        projected[mapping.mapping_id] = page.items
    assert len(projected[MAPS[2].mapping_id]) == 3
    assert len(projected[MAPS[0].mapping_id]) == (2 if refused else 3)
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
            "D039",
            "NVDA",
            T,
            CUTOFF,
            "D039-ATR-1",
            f.VersionRefV1("mmt-d039-controlled", 1),
            f.VersionRefV1("mmt-d039-selection", 1),
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
                derived_signal_id="D039",
                subject_instrument="NVDA",
                effective_at_or_before_utc=T,
                knowledge_at_or_before_utc=CUTOFF,
                limit=10,
            )
            == ()
        )
        return
    assert type(result) is f.WindowMeasurementOccurrenceV1
    assert type(result.result) is f.ExactRatioV1 and result.result == f.ExactRatioV1(33, 2)
    assert result.request == request and result.definition == DEFINITION
    assert result.parameter_set == PARAMETER and result.input_selection_policy == POLICY
    assert result.projection_mappings == MAPS and result.unit_conventions == (UNIT,)
    expected = []
    for index, event in enumerate(TIMES):
        for mapping in (MAPS[2],) if index == 0 else MAPS:
            item = next(
                p
                for p in projected[mapping.mapping_id]
                if p.observation_occurrence_id.value == "bar-" + str(index)
            )
            expected.append(
                f.RawInputLineageV1(
                    mapping.raw_signal_catalogue_id.value,
                    "bar-" + str(index),
                    f.VersionRefV1(mapping.mapping_id, 1),
                    f.VersionRefV1(UNIT.context_id, 1),
                    item,
                    item.native_value,
                    event,
                )
            )
    assert result.raw_input_lineage == tuple(expected) and result.predecessors == ()
    assert (
        result.owner_object_id == "M02"
        and result.owner_namespace == "neutral_market_measurement_truth/window/v1"
    )
    assert result.implementation_brief_sha256 == BRIEF and result.derived_signal_id == "D039"
    assert result.derived_occurrence_id.startswith("mmtwindow1:")
    assert (
        result.window_seconds == 600
        and result.units == "price"
        and result.result_shape == "exact_ratio"
    )
    assert (result.effective_as_of_utc, result.knowledge_cutoff_utc, result.calculated_at_utc) == (
        T,
        CUTOFF,
        NOW,
    )
    assert owner.reads.get_derived_occurrence(result.derived_occurrence_id) == result
    reopened = f.create_window_reader(admission=admission, storage=f.SQLiteReadStorageV1(path))
    assert reopened.get_derived_occurrence(result.derived_occurrence_id) == result
