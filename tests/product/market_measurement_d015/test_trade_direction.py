"""Controlled D015: one public calculation test, six literal discriminating cases."""

import importlib.util
from dataclasses import replace
from datetime import timedelta
from decimal import Decimal
from pathlib import Path

import pytest

from nvda_desk.market_measurement_truth import api as f
from nvda_desk.raw_signal_occurrence_truth import api as raw_api

ROOT = Path(__file__).resolve().parents[3]
BRIEF = "84baa16665db5f8543eba3b1770dafcfb36cc5e8064b2f1837beb924713acb0d"
PREDECESSOR = "a31c482d2dc4822539ede99e955761319585af4badea93b9fc279638e1e1f393"


def _old_literals():
    path = ROOT / "tests/product/market_measurement/_support.py"
    spec = importlib.util.spec_from_file_location("d015_unchanged_midpoint_literals", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _mapping(rid):
    label, path = {
        "R120": ("price", ("trade", "price")),
        "R126": ("bid", ("quote", "bid")),
        "R127": ("ask", ("quote", "ask")),
    }[rid]
    return raw_api.RawSignalProjectionMappingV1(
        "mmt-trade-" + label,
        1,
        raw_api.RawSignalCatalogueId(rid),
        "foundation-pilot-fixture",
        "cash_quote_v1",
        path,
        "price",
        (),
    )


def _observation(rid, value, identity, at, receipt, sequence):
    mapping = _mapping(rid)
    parent, field = mapping.native_field_path
    return raw_api.RawObservationOccurrenceV1(
        concept_id=raw_api.concept_id("raw_signal.raw_observation_occurrence"),
        contract_id=raw_api.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
        observation_occurrence_id=raw_api.observation_occurrence_id(identity),
        delivery_artifact_ref=raw_api.delivery_artifact_ref("d015-controlled-delivery"),
        source_provider=raw_api.provider_id("foundation-pilot-fixture"),
        native_record={parent: {field: Decimal(value)}},
        received_ts_utc=receipt,
        ingestion_sequence=sequence,
        ingestion_sequence_scope=raw_api.ingestion_sequence_scope(
            "foundation-pilot-fixture/cash_quote_v1"
        ),
        source_temporal_kind="true_instant",
        raw_signal_catalogue_ids=(raw_api.RawSignalCatalogueId(rid),),
        source_variant="cash_quote_v1",
        subject_instrument="NVDA",
        native_units="price",
        source_timestamp_raw=at.isoformat().replace("+00:00", "Z"),
        source_timezone_native="UTC",
    )


@pytest.mark.parametrize(
    "mode,price,prior,expected",
    [
        ("above", "101", None, 1),
        ("below", "99", None, -1),
        ("tick_up", "100", "98", 1),
        ("tick_down", "100", "102", -1),
        ("unknown", "100", None, 0),
        ("post_trade_only", "101", None, None),
    ],
)
def test_d015_trade_direction(tmp_path, mode, price, prior, expected):
    literals = _old_literals()
    trade_time = literals.ASOF
    cutoff = trade_time + timedelta(seconds=10)
    clock = [cutoff + timedelta(seconds=1)]
    raw = raw_api.create_owner()
    late = mode == "post_trade_only"
    bid_at = trade_time + timedelta(seconds=5) if late else trade_time - timedelta(seconds=2)
    ask_at = trade_time + timedelta(seconds=5) if late else trade_time - timedelta(seconds=1)
    bid_received = trade_time + timedelta(seconds=5) if late else trade_time - timedelta(seconds=1)
    ask_received = trade_time + timedelta(seconds=5) if late else trade_time
    # Unchanged public D011 records and configuration: no aliasing or new D011 map.
    for side, value, event, receipt in (
        ("bid", "99", bid_at, bid_received),
        ("ask", "101", ask_at, ask_received),
    ):
        raw.commands.admit_raw_observation_occurrence(
            literals.observation(side, value=Decimal(value), event=event, receipt=receipt)
        )
    config = literals.configuration(f, raw.reads, now=lambda: clock[0])
    config["admission"] = f.OwnerAdmissionV1("M02", PREDECESSOR)
    midpoint_owner = f.create_owner(**config)
    midpoint_request = replace(
        literals.request(f),
        as_of_utc=trade_time + timedelta(seconds=5) if late else trade_time,
        knowledge_cutoff_utc=cutoff,
    )
    midpoint = midpoint_owner.materialise(midpoint_request)
    assert midpoint is not None and midpoint.result == Decimal("100")
    assert tuple(x.raw_signal_id for x in midpoint.raw_input_lineage) == ("R034", "R035")
    # These are separate controlled correspondence records, not native equivalence.
    for rid, value, identity, at, received, seq in (
        ("R120", price, "trade-current", trade_time, trade_time, 3),
        ("R126", "99", "trade-quote-bid", bid_at, bid_received, 4),
        ("R127", "101", "trade-quote-ask", ask_at, ask_received, 5),
    ):
        raw.commands.admit_raw_observation_occurrence(
            _observation(rid, value, identity, at, received, seq)
        )
    if prior is not None:
        # Beyond current-trade freshness: the admitted complete prior-price scan
        # must not lose the last different price behind the immediately equal row.
        for value, identity, age, seq in (
            (prior, "trade-prior-different", 120, 6),
            ("100", "trade-prior-equal", 1, 7),
        ):
            at = trade_time - timedelta(seconds=age)
            raw.commands.admit_raw_observation_occurrence(
                _observation("R120", value, identity, at, at, seq)
            )
    if mode == "above":
        at = trade_time + timedelta(seconds=5)
        for rid, value, seq in (("R126", "199", 8), ("R127", "201", 9)):
            raw.commands.admit_raw_observation_occurrence(
                _observation(rid, value, "post-trade-" + rid, at, at, seq)
            )
    current = raw.reads.project_raw_value(
        raw_api.RawSignalCatalogueId("R120"),
        raw_api.observation_occurrence_id("trade-current"),
        mappings=(_mapping("R120"),),
    )
    assert current is not None and current.native_value.as_tuple() == Decimal(price).as_tuple()
    # Missing new behaviour is the intended assertion after actual dependencies.
    assert hasattr(f, "create_trade_direction_owner"), (
        "admitted additive D015 trade-direction seam is absent"
    )
    owner = f.create_trade_direction_owner(
        admission=f.OwnerAdmissionV1("M02", BRIEF),
        raw_projection_reader=raw.reads,
        predecessor_reader=midpoint_owner.reads,
        storage=f.SQLiteStorageV1(str(tmp_path / "sign.sqlite"), True),
        utc_now=lambda: clock[0],
    )
    request = f.TradeDirectionRequestV1(
        f.CalculationRequestV1(
            "D015",
            "NVDA",
            cutoff,
            cutoff,
            "D015-TRADE-DIRECTION-1",
            f.VersionRefV1("mmt-trade-rule", 1),
            f.VersionRefV1("mmt-pilot-selection", 1),
            (),
            tuple(
                f.RawInputBindingV1(
                    rid,
                    f.VersionRefV1(_mapping(rid).mapping_id, 1),
                    f.VersionRefV1("mmt-pilot-price", 1),
                    "NVDA",
                )
                for rid in ("R120", "R126", "R127")
            ),
        ),
        midpoint.derived_occurrence_id,
    )
    result = owner.materialise(request)
    if expected is None:
        assert result is None
        assert (
            owner.reads.list_derived_history(
                derived_signal_id="D015",
                subject_instrument="NVDA",
                effective_at_or_before_utc=cutoff,
                knowledge_at_or_before_utc=cutoff,
                limit=10,
            )
            == ()
        )
        return
    assert type(result) is f.TradeDirectionOccurrenceV1
    assert result.result == expected and type(result.result) is int
    assert result.owner_object_id == "M02"
    assert result.owner_namespace == "neutral_market_measurement_truth/trade_direction/v1"
    assert result.implementation_brief_sha256 == BRIEF and result.derived_signal_id == "D015"
    assert result.derived_occurrence_id.startswith("mmtsign1:")
    assert result.request == request
    assert result.definition == f.CalculationDefinitionV1(
        "D015",
        "D015-TRADE-DIRECTION-1",
        "K08_RULE_BUCKET_POLICY",
        "quote_first_then_last_different_trade_else_0",
        ("R120", "R126", "R127"),
        ("D011",),
        "P_RULE",
        "sign",
        "enum_trade_sign",
        (
            f.AuthorityArtifactRefV1(
                "handoff/m01_completion/authority/"
                "NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md",
                "603b850802a418780109095e7ae69bcece449da79fb24140a6d50297605e927c",
            ),
            f.AuthorityArtifactRefV1(
                "handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv",
                "67bacbcf77afa766cec220a8d4a0f9589c9568d4a1f5c5818334915adf72e549",
            ),
        ),
    )
    assert result.parameter_set == f.CalculationParameterSetV1(
        "mmt-trade-rule", 1, "P_RULE", "NVDA", ("NVDA",)
    )
    assert result.input_selection_policy == config["input_selection_policies"][0]
    assert result.unit_conventions == config["unit_conventions"]
    assert result.projection_mappings == tuple(_mapping(rid) for rid in ("R120", "R126", "R127"))
    predecessor_reads = midpoint_owner.reads
    assert result.predecessor == f.PredecessorEvidenceV1(
        midpoint,
        predecessor_reads.get_calculation_definition(
            derived_signal_id="D011", calculation_definition_version="D011-MIDPOINT-1"
        ),
        predecessor_reads.get_parameter_set(midpoint.parameter_context_refs[0]),
        predecessor_reads.get_input_selection_policy(midpoint.parameter_context_refs[1]),
        tuple(predecessor_reads.get_unit_convention(ref) for ref in midpoint.convention_refs),
        tuple(
            predecessor_reads.get_projection_mapping(item.projection_mapping_ref)
            for item in midpoint.raw_input_lineage
        ),
    )
    assert result.units == "sign" and result.result_shape == "enum_trade_sign"
    assert result.effective_as_of_utc == result.knowledge_cutoff_utc == cutoff
    assert result.calculated_at_utc == clock[0]
    expected_ids = ("trade-current", "trade-quote-bid", "trade-quote-ask")
    if prior is not None:
        expected_ids += ("trade-prior-different",)
    assert tuple(x.observation_occurrence_id for x in result.raw_input_lineage) == expected_ids
    expected_lineage = []
    event_times = {
        "trade-current": trade_time,
        "trade-quote-bid": bid_at,
        "trade-quote-ask": ask_at,
        "trade-prior-different": trade_time - timedelta(seconds=120),
    }
    for item in result.raw_input_lineage:
        projection = raw.reads.project_raw_value(
            raw_api.RawSignalCatalogueId(item.raw_signal_id),
            raw_api.observation_occurrence_id(item.observation_occurrence_id),
            mappings=(_mapping(item.raw_signal_id),),
        )
        assert item.projection == projection
        assert item.canonical_value.as_tuple() == projection.native_value.as_tuple()
        expected_lineage.append(
            f.RawInputLineageV1(
                item.raw_signal_id,
                item.observation_occurrence_id,
                f.VersionRefV1(_mapping(item.raw_signal_id).mapping_id, 1),
                f.VersionRefV1("mmt-pilot-price", 1),
                projection,
                projection.native_value,
                event_times[item.observation_occurrence_id],
            )
        )
    assert result.raw_input_lineage == tuple(expected_lineage)
    assert owner.reads.get_derived_occurrence(result.derived_occurrence_id) == result
    if mode == "above":
        clock[0] += timedelta(seconds=3)
        assert owner.materialise(request) == result
        reader = f.create_trade_direction_reader(
            admission=f.OwnerAdmissionV1("M02", BRIEF),
            storage=f.SQLiteReadStorageV1(str(tmp_path / "sign.sqlite")),
        )
        assert reader.get_derived_occurrence(result.derived_occurrence_id) == result
