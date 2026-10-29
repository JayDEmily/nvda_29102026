"""Five controlled D016 cases; actual M00 -> D011 -> D015 -> window aggregate."""

import importlib.util
from dataclasses import replace
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from pathlib import Path

import pytest

from nvda_desk.market_measurement_truth import api as f
from nvda_desk.raw_signal_occurrence_truth import api as r

ROOT = Path(__file__).resolve().parents[3]
BRIEF = "bcf43f272179b7291a9851a5a1731efc7a90fb156d92de7108e41683045dae01"
SIGN_BRIEF = "84baa16665db5f8543eba3b1770dafcfb36cc5e8064b2f1837beb924713acb0d"
MID_BRIEF = "a31c482d2dc4822539ede99e955761319585af4badea93b9fc279638e1e1f393"


def _literals():
    spec = importlib.util.spec_from_file_location(
        "d016_midpoint_literals", ROOT / "tests/product/market_measurement/_support.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _mapping(rid):
    label, path, units = {
        "R120": ("price", ("trade", "price"), "price"),
        "R121": ("size", ("trade", "size"), "shares"),
        "R126": ("bid", ("quote", "bid"), "price"),
        "R127": ("ask", ("quote", "ask"), "price"),
    }[rid]
    return r.RawSignalProjectionMappingV1(
        "mmt-trade-" + label,
        1,
        r.RawSignalCatalogueId(rid),
        "foundation-pilot-fixture",
        "cash_quote_v1",
        path,
        units,
        (),
    )


@pytest.mark.parametrize(
    "seconds,unknown,expected,selected",
    [
        (1, False, "2", ("A",)),
        (5, False, "-1", ("A", "B")),
        (60, False, "3", ("A", "B", "C")),
        (300, False, "-4", ("A", "B", "C", "D")),
        (1, True, None, ("A",)),
    ],
)
def test_d016_signed_trade_volume(tmp_path, seconds, unknown, expected, selected):
    literals = _literals()
    asof = datetime(2026, 10, 20, 12, 0, 10, tzinfo=UTC)
    cutoff = asof + timedelta(seconds=1)
    now = cutoff + timedelta(seconds=1)
    raw = r.create_owner()
    config = literals.configuration(f, raw.reads, now=lambda: now)
    config["admission"] = f.OwnerAdmissionV1("M02", MID_BRIEF)
    midpoint_owner = f.create_owner(**config)
    sign_owner = f.create_trade_direction_owner(
        admission=f.OwnerAdmissionV1("M02", SIGN_BRIEF),
        raw_projection_reader=raw.reads,
        predecessor_reader=midpoint_owner.reads,
        storage=f.MemoryStorageV1(),
        utc_now=lambda: now,
    )
    signs = {}
    # Oldest first. Unknown A is first in this separate case: no different prior price.
    trades = (
        [("A", 0.5, "100", "2", 0)]
        if unknown
        else [
            ("D", 120, "99", "7", -1),
            ("C", 30, "101", "4", 1),
            ("B", 3, "99", "3", -1),
            ("A", 0.5, "101", "2", 1),
        ]
    )
    for index, (identity, age, price, size, expected_sign) in enumerate(trades):
        event = asof - timedelta(seconds=age)
        for side, value, rid in (("bid", "99", "R126"), ("ask", "101", "R127")):
            quote = literals.observation(
                side,
                identity=identity + "-old-" + side,
                value=Decimal(value),
                event=event,
                receipt=event,
                sequence=index * 5 + (1 if side == "bid" else 2),
            )
            raw.commands.admit_raw_observation_occurrence(quote)
            raw.commands.admit_raw_observation_occurrence(
                replace(
                    quote,
                    observation_occurrence_id=r.observation_occurrence_id(identity + "-" + rid),
                    raw_signal_catalogue_ids=(r.RawSignalCatalogueId(rid),),
                )
            )
        midpoint = midpoint_owner.materialise(
            literals.request(
                f,
                as_of_utc=event,
                knowledge_cutoff_utc=cutoff,
            )
        )
        assert midpoint is not None and midpoint.result == Decimal("100")
        # One native trade occurrence, two explicit field mappings with distinct units.
        trade = replace(
            literals.observation("bid", event=event, receipt=event),
            observation_occurrence_id=r.observation_occurrence_id(identity),
            native_record={"trade": {"price": Decimal(price), "size": Decimal(size)}},
            raw_signal_catalogue_ids=(
                r.RawSignalCatalogueId("R120"),
                r.RawSignalCatalogueId("R121"),
            ),
            ingestion_sequence=index * 5 + 3,
            native_units=None,
        )
        raw.commands.admit_raw_observation_occurrence(trade)
        sign_request = f.TradeDirectionRequestV1(
            f.CalculationRequestV1(
                "D015",
                "NVDA",
                event,
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
        signs[identity] = sign_owner.materialise(sign_request)
        assert signs[identity] is not None and signs[identity].result == expected_sign
        assert signs[identity].raw_input_lineage[0].observation_occurrence_id == identity
    assert hasattr(f, "create_window_owner"), "admitted M02 window calculation capability is absent"
    admission = f.OwnerAdmissionV1("M02", BRIEF)
    path = str(tmp_path / "measurements.sqlite")
    owner = f.create_window_owner(
        admission=admission,
        raw_projection_reader=raw.reads,
        predecessor_reader=sign_owner.reads,
        storage=f.SQLiteStorageV1(path, True),
        utc_now=lambda: now,
    )
    context = f.WindowContextV1(
        f.VersionRefV1("controlled-trade-session", 1),
        asof - timedelta(seconds=600),
        asof + timedelta(seconds=600),
        asof - timedelta(seconds=600),
    )
    calculation = f.CalculationRequestV1(
        "D016",
        "NVDA",
        asof,
        cutoff,
        "D016-SIGNED-VOLUME-1",
        f.VersionRefV1(f"mmt-signed-volume-{seconds}s", 1),
        f.VersionRefV1("mmt-trade-window", 1),
        (context.ref,),
        (
            f.RawInputBindingV1(
                "R121",
                f.VersionRefV1("mmt-trade-size", 1),
                f.VersionRefV1("mmt-trade-shares", 1),
                "NVDA",
            ),
        ),
    )
    request = f.WindowCalculationRequestV1(
        calculation,
        context,
        tuple(signs[key].derived_occurrence_id for key in selected),
    )
    result = owner.materialise(request)
    if expected is None:
        assert result is None
        assert (
            owner.reads.list_derived_history(
                derived_signal_id="D016",
                subject_instrument="NVDA",
                effective_at_or_before_utc=asof,
                knowledge_at_or_before_utc=cutoff,
                limit=10,
            )
            == ()
        )
        return
    assert type(result) is f.WindowMeasurementOccurrenceV1
    assert (
        type(result.result) is Decimal and result.result.as_tuple() == Decimal(expected).as_tuple()
    )
    assert result.owner_object_id == "M02" and result.implementation_brief_sha256 == BRIEF
    assert result.owner_namespace == "neutral_market_measurement_truth/window/v1"
    assert result.derived_signal_id == "D016" and result.derived_occurrence_id.startswith(
        "mmtwindow1:"
    )
    assert result.request == request and result.window_seconds == seconds
    assert result.definition == f.CalculationDefinitionV1(
        "D016",
        "D016-SIGNED-VOLUME-1",
        "K08_RULE_BUCKET_POLICY",
        "sum(matched_sign * size)",
        ("R121",),
        ("D015",),
        "P_RULE",
        "shares",
        "scalar_decimal",
        tuple(f.AuthorityArtifactRefV1(*item) for item in literals.AUTHORITY),
    )
    assert result.parameter_set == f.CalculationParameterSetV1(
        f"mmt-signed-volume-{seconds}s",
        1,
        "P_RULE",
        "NVDA",
        ("NVDA",),
    )
    assert result.input_selection_policy == replace(
        config["input_selection_policies"][0],
        context_id="mmt-trade-window",
        maximum_staleness=timedelta(seconds=300),
        maximum_skew=timedelta(0),
    )
    assert result.unit_conventions == (
        f.UnitConventionVersionV1(
            "mmt-trade-shares",
            1,
            "shares",
            "shares",
            Decimal("1"),
            Decimal("0"),
        ),
    )
    assert result.projection_mappings == (_mapping("R121"),)
    assert result.predecessors == tuple(signs[key] for key in selected)
    assert result.units == "shares" and result.result_shape == "scalar_decimal"
    assert result.effective_as_of_utc == asof and result.knowledge_cutoff_utc == cutoff
    assert result.calculated_at_utc == now
    assert tuple(item.observation_occurrence_id for item in result.raw_input_lineage) == selected
    for line, key in zip(result.raw_input_lineage, selected, strict=True):
        projection = raw.reads.project_raw_value(
            r.RawSignalCatalogueId("R121"),
            r.observation_occurrence_id(key),
            mappings=(_mapping("R121"),),
        )
        assert line == f.RawInputLineageV1(
            "R121",
            key,
            f.VersionRefV1("mmt-trade-size", 1),
            f.VersionRefV1("mmt-trade-shares", 1),
            projection,
            projection.native_value,
            signs[key].raw_input_lineage[0].event_time_utc,
        )
    assert owner.reads.get_derived_occurrence(result.derived_occurrence_id) == result
    reader = f.create_window_reader(admission=admission, storage=f.SQLiteReadStorageV1(path))
    assert reader.get_derived_occurrence(result.derived_occurrence_id) == result
