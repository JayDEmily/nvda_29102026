"""Two exact D025 public cases; controlled native roles and durable typed result."""

from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest

from nvda_desk.market_measurement_truth import api as f
from nvda_desk.raw_signal_occurrence_truth import api as r

BRIEF = "ceb90718b21be71fd55a8ecb3f5e6eb15d27ca8eb3f357b68a0f809606652227"
S = "controlled-price-session/1"
PREV = "controlled-price-session-prev/1"
START = datetime(2026, 10, 20, 12, tzinfo=UTC)
END = datetime(2026, 10, 20, 13, tzinfo=UTC)
ASOF = datetime(2026, 10, 20, 12, 40, tzinfo=UTC)
CUTOFF = ASOF + timedelta(seconds=1)
NOW = CUTOFF + timedelta(seconds=1)
CONTEXT = f.WindowContextV1(f.VersionRefV1("controlled-price-session", 1), START, END, START)
SPECS = [
    ("R039", "mmt-session-high", ("session", "high"), (("session", ("session", "id")),)),
    ("R040", "mmt-session-low", ("session", "low"), (("session", ("session", "id")),)),
    ("R037", "mmt-current-last", ("trade", "last"), (("session", ("session", "id")),)),
]
MAPPINGS = tuple(
    r.RawSignalProjectionMappingV1(
        mid,
        1,
        r.RawSignalCatalogueId(rid),
        "foundation-pilot-fixture",
        "cash_quote_v1",
        path,
        "price",
        keys,
    )
    for rid, mid, path, keys in SPECS
)
POLICY = f.InputSelectionPolicyVersionV1(
    "mmt-session-range-selection",
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
DEFINITION = f.CalculationDefinitionV1(
    "D025",
    "D025-SESSION-RANGE-1",
    "K02_ALGEBRA",
    "(last - session_low) / (session_high - session_low)",
    tuple(x[0] for x in SPECS),
    (),
    "P_BASIC",
    "dimensionless",
    "exact_ratio",
    tuple(f.AuthorityArtifactRefV1(*x) for x in AUTHORITY),
)
PARAMETER = f.CalculationParameterSetV1("mmt-session-range", 1, "P_BASIC", "NVDA", ("NVDA",))


@pytest.mark.parametrize("refused", [False, True])
def test_d025_session_range_position(tmp_path, refused):
    raw = r.create_owner()
    high, low, last = ("91", "91", "91") if refused else ("109", "91", "94")
    records = [
        (
            "snapshot",
            ASOF,
            {
                "session": {"id": S, "high": Decimal(high), "low": Decimal(low)},
                "trade": {"last": Decimal(last)},
            },
            ("R039", "R040", "R037"),
        )
    ]
    for sequence, (identity, event, native, tags) in enumerate(records, 1):
        raw.commands.admit_raw_observation_occurrence(
            r.RawObservationOccurrenceV1(
                concept_id=r.concept_id("raw_signal.raw_observation_occurrence"),
                contract_id=r.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
                observation_occurrence_id=r.observation_occurrence_id(identity),
                delivery_artifact_ref=r.delivery_artifact_ref("controlled-session-delivery"),
                source_provider=r.provider_id("foundation-pilot-fixture"),
                native_record=native,
                received_ts_utc=event,
                ingestion_sequence=sequence,
                ingestion_sequence_scope=r.ingestion_sequence_scope(
                    "foundation-pilot-fixture/cash_quote_v1"
                ),
                source_temporal_kind="true_instant",
                raw_signal_catalogue_ids=tuple(r.RawSignalCatalogueId(t) for t in tags),
                source_variant="cash_quote_v1",
                subject_instrument="NVDA",
                native_units="price",
                source_timestamp_raw=event.isoformat().replace("+00:00", "Z"),
                source_timezone_native="UTC",
            )
        )
    projections = []
    for mapping in MAPPINGS:
        page = raw.reads.list_projected_raw_history(
            mapping.raw_signal_catalogue_id,
            mappings=(mapping,),
            subject_instrument="NVDA",
            received_at_or_before_utc=CUTOFF,
            event_at_or_before_utc=ASOF,
            limit=100,
            cursor=None,
        )
        assert page.next_cursor is None and len(page.items) == 1
        item = page.items[0]
        assert item.native_field_path == mapping.native_field_path
        assert item.projection_mapping_id == mapping.mapping_id
        assert item.native_units == "price"
        assert item.selection_identity is not None
        projections.append(item)
    assert [p.native_value for p in projections] == [Decimal(high), Decimal(low), Decimal(last)]
    assert {p.observation_occurrence_id.value for p in projections} == {"snapshot"}
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
        pytest.fail(f"admitted D025 calculation unsupported after public inputs: {exc}")
    request = f.WindowCalculationRequestV1(
        f.CalculationRequestV1(
            "D025",
            "NVDA",
            ASOF,
            CUTOFF,
            DEFINITION.calculation_definition_version,
            f.VersionRefV1(PARAMETER.context_id, 1),
            f.VersionRefV1(POLICY.context_id, 1),
            (CONTEXT.ref,),
            tuple(
                f.RawInputBindingV1(
                    rid, f.VersionRefV1(mid, 1), f.VersionRefV1(UNIT.context_id, 1), "NVDA"
                )
                for rid, mid, _, _ in SPECS
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
                derived_signal_id="D025",
                subject_instrument="NVDA",
                effective_at_or_before_utc=ASOF,
                knowledge_at_or_before_utc=CUTOFF,
                limit=10,
            )
            == ()
        )
        return
    assert type(result) is f.WindowMeasurementOccurrenceV1
    assert type(result.result) is f.ExactRatioV1 and result.result == f.ExactRatioV1(1, 6)
    assert result.owner_object_id == "M02" and result.implementation_brief_sha256 == BRIEF
    assert result.owner_namespace == "neutral_market_measurement_truth/window/v1"
    assert result.derived_signal_id == "D025" and result.derived_occurrence_id.startswith(
        "mmtwindow1:"
    )
    assert result.request == request and result.predecessors == ()
    assert result.definition == DEFINITION and result.parameter_set == PARAMETER
    assert result.input_selection_policy == POLICY and result.unit_conventions == (UNIT,)
    assert result.projection_mappings == MAPPINGS
    assert result.units == "dimensionless" and result.result_shape == "exact_ratio"
    assert result.window_seconds == 2400
    assert (
        result.effective_as_of_utc == ASOF
        and result.knowledge_cutoff_utc == CUTOFF
        and result.calculated_at_utc == NOW
    )
    expected_lines = tuple(
        f.RawInputLineageV1(
            spec[0],
            p.observation_occurrence_id.value,
            f.VersionRefV1(spec[1], 1),
            f.VersionRefV1(UNIT.context_id, 1),
            p,
            p.native_value,
            datetime.fromisoformat(p.source_timestamp_raw.replace("Z", "+00:00")),
        )
        for spec, p in zip(SPECS, projections, strict=True)
    )
    assert result.raw_input_lineage == expected_lines
    assert owner.reads.get_derived_occurrence(result.derived_occurrence_id) == result
    reader = f.create_window_reader(admission=admission, storage=f.SQLiteReadStorageV1(path))
    assert reader.get_derived_occurrence(result.derived_occurrence_id) == result
