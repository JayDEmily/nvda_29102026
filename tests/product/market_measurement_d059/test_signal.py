"""Exactly two authority-derived D059 volatility relationship cases through public M00/M02."""

from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest

from nvda_desk.market_measurement_truth import api as f
from nvda_desk.raw_signal_occurrence_truth import api as r

D = "D059"
BRIEF = "1ce887da55b8afa021484defce4f39bf96a2b597573781fb32ba5435b4abcb26"
RAW = ("R236", "R240")
SERIES = ("VIX", "VIX3M")
T = datetime(2026, 10, 20, 13, tzinfo=UTC)
CUTOFF, NOW = T + timedelta(seconds=1), T + timedelta(seconds=2)
CONTEXT = f.WindowContextV1(
    f.VersionRefV1("controlled-volatility-terms", 1),
    T - timedelta(seconds=60),
    T + timedelta(seconds=1),
    T - timedelta(seconds=60),
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
        "index_points",
        META,
    )
    for rid in RAW
)
UNITS = tuple(
    f.UnitConventionVersionV1(
        "mmt-macro-" + rid.lower() + "-units",
        1,
        "index_points",
        "index_points",
        Decimal("1"),
        Decimal("0"),
    )
    for rid in RAW
)
POLICY = f.InputSelectionPolicyVersionV1(
    "mmt-d059-selection",
    1,
    ("subject_instrument", "metric.series"),
    timedelta(seconds=60),
    timedelta(0),
    ("true_instant",),
    (),
    "foundation-controlled-macro",
    "macro_snapshot_v1",
    "foundation-controlled-macro/macro_snapshot_v1",
    100,
    1000,
)
PARAMETER = f.CalculationParameterSetV1("mmt-d059-controlled", 1, "P_BASIC", "NVDA", ("NVDA",))
DEFINITION = f.CalculationDefinitionV1(
    D,
    "D059-TERM-PAIR-1",
    "K02_ALGEBRA",
    "first-second; first/second",
    RAW,
    (),
    "P_BASIC",
    "index_points / ratio",
    "named_exact_term_pair",
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
def test_d059_signal(tmp_path, refused):
    raw = r.create_owner()
    # A single declared scenario per branch; these records are source setup, not probes.
    records = [(0, T, "25"), (1, T, "30")]
    if refused:
        # Same event/receipt instant: older positive loses by ingestion rank only.
        # A forbidden zero-skipping fallback would still satisfy zero skew.
        records = [(1, T, "30"), (0, T, "25"), (1, T, "0")]
    for index, (role, event, value) in enumerate(records):
        raw.commands.admit_raw_observation_occurrence(
            r.RawObservationOccurrenceV1(
                concept_id=r.concept_id("raw_signal.raw_observation_occurrence"),
                contract_id=r.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
                observation_occurrence_id=r.observation_occurrence_id("d059-raw-" + str(index)),
                delivery_artifact_ref=r.delivery_artifact_ref("d059-delivery"),
                source_provider=r.provider_id("foundation-controlled-macro"),
                native_record={
                    "metric": {
                        "value": Decimal(value),
                        "series": SERIES[role],
                        "measurement_date": event.date().isoformat(),
                        "method": "controlled_snapshot/1",
                        "quote_orientation": "not_applicable",
                    }
                },
                received_ts_utc=event,
                ingestion_sequence=index + 1,
                ingestion_sequence_scope=r.ingestion_sequence_scope(
                    "foundation-controlled-macro/macro_snapshot_v1"
                ),
                source_temporal_kind="true_instant",
                raw_signal_catalogue_ids=(r.RawSignalCatalogueId(RAW[role]),),
                source_variant="macro_snapshot_v1",
                subject_instrument="NVDA",
                native_units="index_points",
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
        projected.update({p.observation_occurrence_id.value: p for p in page.items})
    assert len(projected) == len(records)
    for index, (role, event, value) in enumerate(records):
        actual = projected["d059-raw-" + str(index)]
        assert actual.native_value == Decimal(value)
        assert actual.raw_signal_catalogue_id == r.RawSignalCatalogueId(RAW[role])
        assert actual.source_timestamp_raw == event.isoformat().replace("+00:00", "Z")
        assert actual.received_ts_utc == event
        assert actual.selection_identity == r.RawSelectionIdentityV1(
            (
                ("metric.series", SERIES[role]),
                ("metric.measurement_date", event.date().isoformat()),
                ("metric.method", "controlled_snapshot/1"),
                ("metric.quote_orientation", "not_applicable"),
            )
        )
    if refused:
        assert projected["d059-raw-2"].native_value == Decimal("0")
        assert projected["d059-raw-0"].native_value == Decimal("30")
        assert (
            projected["d059-raw-2"].ingestion_sequence > projected["d059-raw-0"].ingestion_sequence
        )
        assert records[0][1] == records[1][1] == records[2][1] == T
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
    # Explicit public actions keep source admission/selection independent from materialisation.
    result = owner.materialise(request)
    history_args = dict(
        derived_signal_id=D,
        subject_instrument="NVDA",
        effective_at_or_before_utc=T,
        knowledge_at_or_before_utc=CUTOFF,
        limit=10,
    )
    reader = f.create_window_reader(admission=admission, storage=f.SQLiteReadStorageV1(path))
    if refused:
        assert result is None
        assert owner.reads.list_derived_history(**history_args) == ()
        assert reader.list_derived_history(**history_args) == ()
        return
    assert type(result) is f.WindowMeasurementOccurrenceV1
    expected = f.TermPairV1(f.ExactRatioV1(-5, 1), f.ExactRatioV1(5, 6))
    assert type(result.result) is type(expected) and result.result == expected
    assert result.request == request and result.definition == DEFINITION
    assert result.parameter_set == PARAMETER and result.input_selection_policy == POLICY
    assert result.projection_mappings == MAPS and result.unit_conventions == UNITS
    assert result.raw_input_lineage == tuple(
        f.RawInputLineageV1(
            RAW[role],
            "d059-raw-" + str(index),
            f.VersionRefV1(MAPS[role].mapping_id, 1),
            f.VersionRefV1(UNITS[role].context_id, 1),
            projected["d059-raw-" + str(index)],
            Decimal(value),
            event,
        )
        for index, (role, event, value) in enumerate(records[:2])
    )
    assert result.predecessors == () and result.window_seconds == 0
    assert result.owner_object_id == "M02"
    assert result.owner_namespace == "neutral_market_measurement_truth/window/v1"
    assert result.implementation_brief_sha256 == BRIEF and result.derived_signal_id == D
    assert result.units == "index_points / ratio" and result.result_shape == "named_exact_term_pair"
    assert result.derived_occurrence_id.startswith("mmtwindow1:")
    assert (result.effective_as_of_utc, result.knowledge_cutoff_utc, result.calculated_at_utc) == (
        T,
        CUTOFF,
        NOW,
    )
    assert owner.reads.get_derived_occurrence(result.derived_occurrence_id) == result
    assert reader.get_derived_occurrence(result.derived_occurrence_id) == result
    assert reader.list_derived_history(**history_args) == (result,)
