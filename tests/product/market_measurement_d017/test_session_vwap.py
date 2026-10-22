"""Two exact D017 public-path cases, with visible session-selection decoy."""

from datetime import UTC, datetime, timedelta
from decimal import Decimal
from typing import get_args, get_type_hints

import pytest

from nvda_desk.market_measurement_truth import api as f
from nvda_desk.raw_signal_occurrence_truth import api as r

BRIEF = "b3e7b29f882d4f8ae698c8450d92ada08b3625c2effa29359f59fd50f5a3cf28"
START = datetime(2026, 10, 20, 12, tzinfo=UTC)
ASOF = START + timedelta(seconds=120)
CUTOFF = ASOF + timedelta(seconds=1)
NOW = CUTOFF + timedelta(seconds=1)
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


def _mapping(rid):
    price = rid == "R120"
    return r.RawSignalProjectionMappingV1(
        "mmt-trade-price" if price else "mmt-trade-size",
        1,
        r.RawSignalCatalogueId(rid),
        "foundation-pilot-fixture",
        "cash_quote_v1",
        ("trade", "price" if price else "size"),
        "price" if price else "shares",
        (),
    )


@pytest.mark.parametrize("missing_size", [False, True])
def test_d017_session_vwap(tmp_path, missing_size):
    raw = r.create_owner()
    for identity, age, price, size, sequence in (
        ("outside", -20, "100", "100", 1),
        ("trade-a", 10, "6", "2", 2),
        ("trade-b", 20, "4", "3", 3),
    ):
        event = START + timedelta(seconds=age)
        include_size = not (missing_size and identity == "trade-b")
        fields = {"price": Decimal(price)}
        if include_size:
            fields["size"] = Decimal(size)
        raw.commands.admit_raw_observation_occurrence(
            r.RawObservationOccurrenceV1(
                concept_id=r.concept_id("raw_signal.raw_observation_occurrence"),
                contract_id=r.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
                observation_occurrence_id=r.observation_occurrence_id(identity),
                delivery_artifact_ref=r.delivery_artifact_ref("d017-controlled-delivery"),
                source_provider=r.provider_id("foundation-pilot-fixture"),
                native_record={"trade": fields},
                received_ts_utc=event,
                ingestion_sequence=sequence,
                ingestion_sequence_scope=r.ingestion_sequence_scope(
                    "foundation-pilot-fixture/cash_quote_v1"
                ),
                source_temporal_kind="true_instant",
                raw_signal_catalogue_ids=tuple(
                    r.RawSignalCatalogueId(x)
                    for x in (("R120", "R121") if include_size else ("R120",))
                ),
                source_variant="cash_quote_v1",
                subject_instrument="NVDA",
                native_units=None,
                source_timestamp_raw=event.isoformat().replace("+00:00", "Z"),
                source_timezone_native="UTC",
            )
        )
    # The decoy is actually present in both histories; exclusion must be by session.
    for rid in ("R120", "R121"):
        page = raw.reads.list_projected_raw_history(
            r.RawSignalCatalogueId(rid),
            mappings=(_mapping(rid),),
            subject_instrument="NVDA",
            received_at_or_before_utc=CUTOFF,
            event_at_or_before_utc=ASOF,
            limit=100,
            cursor=None,
        )
        assert "outside" in {x.observation_occurrence_id.value for x in page.items}
        assert page.next_cursor is None
    second_price = raw.reads.project_raw_value(
        r.RawSignalCatalogueId("R120"),
        r.observation_occurrence_id("trade-b"),
        mappings=(_mapping("R120"),),
    )
    second_size = raw.reads.project_raw_value(
        r.RawSignalCatalogueId("R121"),
        r.observation_occurrence_id("trade-b"),
        mappings=(_mapping("R121"),),
    )
    assert second_price is not None and second_price.native_value == Decimal("4")
    assert (second_size is None) == missing_size
    assert f.ExactRatioV1 in get_args(get_type_hints(f.WindowMeasurementOccurrenceV1)["result"]), (
        "admitted exact window result capability is absent"
    )
    context = f.WindowContextV1(
        f.VersionRefV1("controlled-vwap-session", 1),
        START,
        START + timedelta(hours=1),
        START,
    )
    request = f.WindowCalculationRequestV1(
        f.CalculationRequestV1(
            "D017",
            "NVDA",
            ASOF,
            CUTOFF,
            "D017-SESSION-VWAP-1",
            f.VersionRefV1("mmt-session-vwap", 1),
            f.VersionRefV1("mmt-vwap-selection", 1),
            (context.ref,),
            tuple(
                f.RawInputBindingV1(
                    rid,
                    f.VersionRefV1(_mapping(rid).mapping_id, 1),
                    f.VersionRefV1("mmt-pilot-price" if rid == "R120" else "mmt-trade-shares", 1),
                    "NVDA",
                )
                for rid in ("R120", "R121")
            ),
        ),
        context,
        (),
    )
    admission = f.OwnerAdmissionV1("M02", BRIEF)
    path = str(tmp_path / "vwap.sqlite")
    owner = f.create_window_owner(
        admission=admission,
        raw_projection_reader=raw.reads,
        predecessor_reader=None,
        storage=f.SQLiteStorageV1(path, True),
        utc_now=lambda: NOW,
    )
    result = owner.materialise(request)
    if missing_size:
        assert result is None
        assert (
            owner.reads.list_derived_history(
                derived_signal_id="D017",
                subject_instrument="NVDA",
                effective_at_or_before_utc=ASOF,
                knowledge_at_or_before_utc=CUTOFF,
                limit=10,
            )
            == ()
        )
        return
    assert type(result) is f.WindowMeasurementOccurrenceV1
    assert type(result.result) is f.ExactRatioV1 and result.result == f.ExactRatioV1(24, 5)
    assert result.owner_object_id == "M02" and result.implementation_brief_sha256 == BRIEF
    assert result.owner_namespace == "neutral_market_measurement_truth/window/v1"
    assert result.derived_signal_id == "D017" and result.derived_occurrence_id.startswith(
        "mmtwindow1:"
    )
    assert result.request == request and result.window_seconds == 120
    assert result.definition == f.CalculationDefinitionV1(
        "D017",
        "D017-SESSION-VWAP-1",
        "K02_ALGEBRA",
        "sum(price * size) / sum(size)",
        ("R120", "R121"),
        (),
        "P_BASIC",
        "price",
        "scalar_exact_ratio",
        tuple(f.AuthorityArtifactRefV1(*ref) for ref in AUTHORITY),
    )
    assert result.parameter_set == f.CalculationParameterSetV1(
        "mmt-session-vwap",
        1,
        "P_BASIC",
        "NVDA",
        ("NVDA",),
    )
    assert result.input_selection_policy == f.InputSelectionPolicyVersionV1(
        "mmt-vwap-selection",
        1,
        ("subject_instrument",),
        timedelta(hours=1),
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
            "mmt-pilot-price", 1, "price", "price", Decimal("1"), Decimal("0")
        ),
        f.UnitConventionVersionV1(
            "mmt-trade-shares", 1, "shares", "shares", Decimal("1"), Decimal("0")
        ),
    )
    assert result.projection_mappings == tuple(_mapping(rid) for rid in ("R120", "R121"))
    assert result.predecessors == ()
    assert result.units == "price" and result.result_shape == "scalar_exact_ratio"
    assert result.effective_as_of_utc == ASOF and result.knowledge_cutoff_utc == CUTOFF
    assert result.calculated_at_utc == NOW
    expected = []
    for identity, seconds in (("trade-a", 10), ("trade-b", 20)):
        for rid, unit in (("R120", "mmt-pilot-price"), ("R121", "mmt-trade-shares")):
            mapping = _mapping(rid)
            projection = raw.reads.project_raw_value(
                r.RawSignalCatalogueId(rid),
                r.observation_occurrence_id(identity),
                mappings=(mapping,),
            )
            expected.append(
                f.RawInputLineageV1(
                    rid,
                    identity,
                    f.VersionRefV1(mapping.mapping_id, 1),
                    f.VersionRefV1(unit, 1),
                    projection,
                    projection.native_value,
                    START + timedelta(seconds=seconds),
                )
            )
    assert result.raw_input_lineage == tuple(expected)
    assert owner.reads.get_derived_occurrence(result.derived_occurrence_id) == result
    reader = f.create_window_reader(admission=admission, storage=f.SQLiteReadStorageV1(path))
    assert reader.get_derived_occurrence(result.derived_occurrence_id) == result
