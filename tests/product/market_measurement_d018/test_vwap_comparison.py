"""Two D018 cases with actual D017 production, including its lawful zero result."""

import importlib.util
from dataclasses import replace
from datetime import timedelta
from decimal import Decimal
from pathlib import Path

import pytest

from nvda_desk.market_measurement_truth import api as f
from nvda_desk.raw_signal_occurrence_truth import api as r

BRIEF = "1f65edb4e3050c89604c749accc5fdf39ff03e69e54eca43a50cfa496298e90e"
D017 = "b3e7b29f882d4f8ae698c8450d92ada08b3625c2effa29359f59fd50f5a3cf28"


def _literals():
    path = (
        Path(__file__).resolve().parents[3]
        / "tests/product/market_measurement_d017/test_session_vwap.py"
    )
    spec = importlib.util.spec_from_file_location("d018_vwap_literals", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _mapping():
    return r.RawSignalProjectionMappingV1(
        "mmt-provider-vwap",
        1,
        r.RawSignalCatalogueId("R137"),
        "foundation-pilot-fixture",
        "cash_quote_v1",
        ("vwap", "value"),
        "price",
        (("session", ("vwap", "session")), ("as_of", ("vwap", "as_of"))),
    )


def _admit(raw, identity, record, ids, when, sequence):
    raw.commands.admit_raw_observation_occurrence(
        r.RawObservationOccurrenceV1(
            concept_id=r.concept_id("raw_signal.raw_observation_occurrence"),
            contract_id=r.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
            observation_occurrence_id=r.observation_occurrence_id(identity),
            delivery_artifact_ref=r.delivery_artifact_ref("d018-controlled-delivery"),
            source_provider=r.provider_id("foundation-pilot-fixture"),
            native_record=record,
            received_ts_utc=when,
            ingestion_sequence=sequence,
            ingestion_sequence_scope=r.ingestion_sequence_scope(
                "foundation-pilot-fixture/cash_quote_v1"
            ),
            source_temporal_kind="true_instant",
            raw_signal_catalogue_ids=tuple(r.RawSignalCatalogueId(x) for x in ids),
            source_variant="cash_quote_v1",
            subject_instrument="NVDA",
            native_units=None,
            source_timestamp_raw=when.isoformat().replace("+00:00", "Z"),
            source_timezone_native="UTC",
        )
    )


@pytest.mark.parametrize("zero", [False, True])
def test_d018_vwap_comparison(tmp_path, zero):
    literals = _literals()
    raw = r.create_owner()
    for index, (price, size) in enumerate((("6", "2"), ("4", "3"))):
        _admit(
            raw,
            f"trade-{index}",
            {"trade": {"price": Decimal("0" if zero else price), "size": Decimal(size)}},
            ("R120", "R121"),
            literals.START + timedelta(seconds=10 * (index + 1)),
            index + 1,
        )
    context = f.WindowContextV1(
        f.VersionRefV1("controlled-vwap-session", 1), literals.START, literals.START + timedelta(hours=1), literals.START
    )
    predecessor_owner = f.create_window_owner(
        admission=f.OwnerAdmissionV1("M02", D017),
        raw_projection_reader=raw.reads,
        storage=f.MemoryStorageV1(),
        utc_now=lambda: literals.NOW,
    )
    p_request = f.WindowCalculationRequestV1(
        f.CalculationRequestV1(
            "D017",
            "NVDA",
            literals.ASOF,
            literals.CUTOFF,
            "D017-SESSION-VWAP-1",
            f.VersionRefV1("mmt-session-vwap", 1),
            f.VersionRefV1("mmt-vwap-selection", 1),
            (context.ref,),
            tuple(
                f.RawInputBindingV1(
                    rid,
                    f.VersionRefV1(literals._mapping(rid).mapping_id, 1),
                    f.VersionRefV1("mmt-pilot-price" if rid == "R120" else "mmt-trade-shares", 1),
                    "NVDA",
                )
                for rid in ("R120", "R121")
            ),
        ),
        context,
        (),
    )
    predecessor = predecessor_owner.materialise(p_request)
    assert predecessor is not None
    assert predecessor.result == (f.ExactRatioV1(0, 1) if zero else f.ExactRatioV1(24, 5))
    provider_value = Decimal("1" if zero else "4.848")
    _admit(
        raw,
        "provider",
        {
            "vwap": {
                "value": provider_value,
                "session": "controlled-vwap-session/1",
                "as_of": literals.ASOF.isoformat().replace("+00:00", "Z"),
            }
        },
        ("R137",),
        literals.ASOF,
        3,
    )
    projection = raw.reads.project_raw_value(
        r.RawSignalCatalogueId("R137"),
        r.observation_occurrence_id("provider"),
        mappings=(_mapping(),),
    )
    assert projection is not None and projection.native_value == provider_value
    assert hasattr(f, "MeasurementComparisonV1"), "admitted named comparison result is absent"
    admission = f.OwnerAdmissionV1("M02", BRIEF)
    path = str(tmp_path / "comparison.sqlite")
    owner = f.create_window_owner(
        admission=admission,
        raw_projection_reader=raw.reads,
        predecessor_reader=predecessor_owner.reads,
        storage=f.SQLiteStorageV1(path, True),
        utc_now=lambda: literals.NOW,
    )
    request = f.WindowCalculationRequestV1(
        f.CalculationRequestV1(
            "D018",
            "NVDA",
            literals.ASOF,
            literals.CUTOFF,
            "D018-VWAP-COMPARISON-1",
            f.VersionRefV1("mmt-vwap-comparison", 1),
            f.VersionRefV1("mmt-comparison-selection", 1),
            (context.ref,),
            (
                f.RawInputBindingV1(
                    "R137",
                    f.VersionRefV1("mmt-provider-vwap", 1),
                    f.VersionRefV1("mmt-pilot-price", 1),
                    "NVDA",
                ),
            ),
        ),
        context,
        (predecessor.derived_occurrence_id,),
    )
    result = owner.materialise(request)
    if zero:
        assert result is None
        assert (
            owner.reads.list_derived_history(
                derived_signal_id="D018",
                subject_instrument="NVDA",
                effective_at_or_before_utc=literals.ASOF,
                knowledge_at_or_before_utc=literals.CUTOFF,
                limit=10,
            )
            == ()
        )
        return
    assert type(result) is f.WindowMeasurementOccurrenceV1
    assert type(result.result) is f.MeasurementComparisonV1
    assert result.result == f.MeasurementComparisonV1(
        f.ExactRatioV1(6, 125), f.ExactRatioV1(100, 1)
    )
    assert result.owner_object_id == "M02" and result.implementation_brief_sha256 == BRIEF
    assert result.owner_namespace == "neutral_market_measurement_truth/window/v1"
    assert result.derived_signal_id == "D018" and result.derived_occurrence_id.startswith(
        "mmtwindow1:"
    )
    assert result.request == request and result.window_seconds == 120
    assert result.definition == f.CalculationDefinitionV1(
        "D018",
        "D018-VWAP-COMPARISON-1",
        "K02_ALGEBRA",
        "provider_vwap - D017; 10000 * difference / D017",
        ("R137",),
        ("D017",),
        "P_BASIC",
        "price / bps",
        "named_exact_comparison",
        tuple(f.AuthorityArtifactRefV1(*ref) for ref in literals.AUTHORITY),
    )
    assert result.parameter_set == f.CalculationParameterSetV1(
        "mmt-vwap-comparison", 1, "P_BASIC", "NVDA", ("NVDA",)
    )
    assert result.input_selection_policy == replace(
        predecessor.input_selection_policy, context_id="mmt-comparison-selection"
    )
    assert result.unit_conventions == (predecessor.unit_conventions[0],)
    assert result.projection_mappings == (_mapping(),) and result.predecessors == (predecessor,)
    assert result.units == "price / bps" and result.result_shape == "named_exact_comparison"
    assert result.effective_as_of_utc == literals.ASOF and result.knowledge_cutoff_utc == literals.CUTOFF
    assert result.calculated_at_utc == literals.NOW
    assert result.raw_input_lineage == (
        f.RawInputLineageV1(
            "R137",
            "provider",
            f.VersionRefV1("mmt-provider-vwap", 1),
            f.VersionRefV1("mmt-pilot-price", 1),
            projection,
            provider_value,
            literals.ASOF,
        ),
    )
    assert owner.reads.get_derived_occurrence(result.derived_occurrence_id) == result
    reader = f.create_window_reader(admission=admission, storage=f.SQLiteReadStorageV1(path))
    assert reader.get_derived_occurrence(result.derived_occurrence_id) == result
