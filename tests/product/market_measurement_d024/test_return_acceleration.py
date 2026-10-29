"""Two D024 cases using actual public fixed-horizon producers and exact five fields."""

from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest

from nvda_desk.market_measurement_truth import api as f
from nvda_desk.raw_signal_occurrence_truth import api as r

BRIEF = "7776047c140ed8e6fa76af66a772b4a8ffbf1088ce4681377243ec666ddc9885"
ASOF = datetime(2026, 10, 20, 12, 40, tzinfo=UTC)
CUTOFF = ASOF + timedelta(seconds=1)
NOW = CUTOFF + timedelta(seconds=1)
CONTEXT = f.WindowContextV1(
    f.VersionRefV1("controlled-close-session", 1),
    datetime(2026, 10, 20, 12, tzinfo=UTC),
    datetime(2026, 10, 20, 13, tzinfo=UTC),
    datetime(2026, 10, 20, 12, tzinfo=UTC),
)
MAPPING = r.RawSignalProjectionMappingV1(
    "mmt-bar-close",
    1,
    r.RawSignalCatalogueId("R143"),
    "foundation-pilot-fixture",
    "cash_quote_v1",
    ("bar", "close"),
    "price",
    (),
)
UNIT = f.UnitConventionVersionV1("mmt-pilot-price", 1, "price", "price", Decimal("1"), Decimal("0"))
POLICY = f.InputSelectionPolicyVersionV1(
    "mmt-return-acceleration-selection",
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
PRODUCERS = (
    ("D019", 60, "6affd5b55eb03007a23ae80a79bbd3d5665105d70b2e7e65c4050d29cf60c085"),
    ("D020", 300, "811906fdfb073da9b5a7ba137563953d6ff977d50bfe99b8f43adb068f20e839"),
    ("D021", 1800, "913ba660f583f8f3e564190390681e594a374e0fc2d66227bd8452b4d0cbb8cc"),
)
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
    "D024",
    "D024-RETURN-ACCELERATION-1",
    "K03_CHANGE_RETURN",
    "q1=D019/1; q5=D020/5; q30=D021/30; accel_1v5=q1-q5; accel_5v30=q5-q30",
    (),
    ("D019", "D020", "D021"),
    "P_WINDOW",
    "return/minute",
    "named_exact_acceleration",
    tuple(f.AuthorityArtifactRefV1(*x) for x in AUTHORITY),
)
PARAMETER = f.CalculationParameterSetV1("mmt-return-acceleration", 1, "P_WINDOW", "NVDA", ("NVDA",))


class _ActualReads:
    def __init__(self, readers):
        self.readers = readers

    def get_derived_occurrence(self, identity):
        found = [
            p
            for reader in self.readers
            if (p := reader.get_derived_occurrence(identity)) is not None
        ]
        assert len(found) <= 1
        return found[0] if found else None

    def list_derived_history(self, **kwargs):
        return tuple(p for reader in self.readers for p in reader.list_derived_history(**kwargs))


@pytest.mark.parametrize("missing_thirty", [False, True])
def test_d024_return_acceleration(tmp_path, missing_thirty):
    raw = r.create_owner()
    rows = [("current", 0, "120"), ("one", 60, "110"), ("five", 300, "100")]
    if not missing_thirty:
        rows.append(("thirty", 1800, "80"))
    for sequence, (identity, age, price) in enumerate(rows, 1):
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
        mappings=(MAPPING,),
        subject_instrument="NVDA",
        received_at_or_before_utc=CUTOFF,
        event_at_or_before_utc=ASOF,
        limit=100,
        cursor=None,
    )
    assert {x.observation_occurrence_id.value for x in page.items} == {
        x[0] for x in rows
    } and page.next_cursor is None
    predecessors, readers = [], []
    for identity, seconds, brief in PRODUCERS:
        producer = f.create_window_owner(
            admission=f.OwnerAdmissionV1("M02", brief),
            raw_projection_reader=raw.reads,
            storage=f.MemoryStorageV1(),
            utc_now=lambda: NOW,
        )
        req = f.WindowCalculationRequestV1(
            f.CalculationRequestV1(
                identity,
                "NVDA",
                ASOF,
                CUTOFF,
                identity + "-LOG-RETURN-1",
                f.VersionRefV1(f"mmt-log-{seconds}s-50d-half-even", 1),
                f.VersionRefV1("mmt-close-selection", 1),
                (CONTEXT.ref,),
                (
                    f.RawInputBindingV1(
                        "R143",
                        f.VersionRefV1("mmt-bar-close", 1),
                        f.VersionRefV1("mmt-pilot-price", 1),
                        "NVDA",
                    ),
                ),
            ),
            CONTEXT,
            (),
        )
        p = producer.materialise(req)
        readers.append(producer.reads)
        if missing_thirty and identity == "D021":
            assert p is None
        else:
            assert type(p) is f.WindowMeasurementOccurrenceV1 and p.derived_signal_id == identity
            predecessors.append(p)
    assert [p.derived_signal_id for p in predecessors] == (
        ["D019", "D020"] if missing_thirty else ["D019", "D020", "D021"]
    )
    reads = _ActualReads(readers)
    admission = f.OwnerAdmissionV1("M02", BRIEF)
    path = str(tmp_path / "acceleration.sqlite")
    try:
        owner = f.create_window_owner(
            admission=admission,
            raw_projection_reader=raw.reads,
            predecessor_reader=reads,
            storage=f.SQLiteStorageV1(path, True),
            utc_now=lambda: NOW,
        )
    except ValueError as exc:
        pytest.fail(f"admitted D024 unsupported after actual compatible producers: {exc}")
    request = f.WindowCalculationRequestV1(
        f.CalculationRequestV1(
            "D024",
            "NVDA",
            ASOF,
            CUTOFF,
            DEFINITION.calculation_definition_version,
            f.VersionRefV1(PARAMETER.context_id, 1),
            f.VersionRefV1(POLICY.context_id, 1),
            (CONTEXT.ref,),
            (),
        ),
        CONTEXT,
        tuple(p.derived_occurrence_id for p in predecessors),
    )
    result = owner.materialise(request)
    if missing_thirty:
        assert result is None
        assert (
            owner.reads.list_derived_history(
                derived_signal_id="D024",
                subject_instrument="NVDA",
                effective_at_or_before_utc=ASOF,
                knowledge_at_or_before_utc=CUTOFF,
                limit=10,
            )
            == ()
        )
        return
    assert type(result) is f.WindowMeasurementOccurrenceV1
    expected = f.ReturnAccelerationV1(
        f.ExactRatioV1(
            87011376989629766167765901873749540976783972605843,
            1000000000000000000000000000000000000000000000000000,
        ),
        f.ExactRatioV1(
            18232155679395462621171802515451463319738933791449,
            500000000000000000000000000000000000000000000000000,
        ),
        f.ExactRatioV1(
            40546510810816438197801311546434913657199042346249,
            3000000000000000000000000000000000000000000000000000,
        ),
        f.ExactRatioV1(
            10109413126167768185084459368569322867461221004589,
            200000000000000000000000000000000000000000000000000,
        ),
        f.ExactRatioV1(
            13769284653111267505845900709254773252246912080489,
            600000000000000000000000000000000000000000000000000,
        ),
    )
    assert type(result.result) is f.ReturnAccelerationV1 and result.result == expected
    assert (
        result.owner_object_id == "M02"
        and result.owner_namespace == "neutral_market_measurement_truth/window/v1"
    )
    assert (
        result.implementation_brief_sha256 == BRIEF
        and result.derived_signal_id == "D024"
        and result.derived_occurrence_id.startswith("mmtwindow1:")
    )
    assert (
        result.request == request
        and result.definition == DEFINITION
        and result.parameter_set == PARAMETER
    )
    assert (
        result.input_selection_policy == POLICY
        and result.unit_conventions == (UNIT,)
        and result.projection_mappings == (MAPPING,)
    )
    assert result.predecessors == tuple(predecessors)
    assert result.raw_input_lineage == (
        predecessors[0].raw_input_lineage[0],
        *(p.raw_input_lineage[1] for p in predecessors),
    )
    assert [
        (line.observation_occurrence_id, line.canonical_value, line.event_time_utc)
        for line in result.raw_input_lineage
    ] == [
        ("current", Decimal("120"), ASOF),
        ("one", Decimal("110"), ASOF - timedelta(seconds=60)),
        ("five", Decimal("100"), ASOF - timedelta(seconds=300)),
        ("thirty", Decimal("80"), ASOF - timedelta(seconds=1800)),
    ]
    assert (
        result.window_seconds == 1800
        and result.units == "return/minute"
        and result.result_shape == "named_exact_acceleration"
    )
    assert (
        result.effective_as_of_utc == ASOF
        and result.knowledge_cutoff_utc == CUTOFF
        and result.calculated_at_utc == NOW
    )
    assert owner.reads.get_derived_occurrence(result.derived_occurrence_id) == result
    reader = f.create_window_reader(admission=admission, storage=f.SQLiteReadStorageV1(path))
    assert reader.get_derived_occurrence(result.derived_occurrence_id) == result
