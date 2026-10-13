"""Controlled Stage-1 own-kernel arithmetic for Stage-2-dependent rows only.

The controlled predecessor values are not Stage-2 implementation or public integration.
"""

from datetime import UTC, datetime
from decimal import Decimal as D

import pytest

from nvda_desk.derived_signal_calculation_truth import _catalogue, _stage1, api

NOW = datetime(2026, 10, 12, 6, tzinfo=UTC)


def _k(did: str, value: object, *, metadata=()) -> _stage1.KernelValueV1:
    return _stage1.KernelValueV1(
        value=value,
        occurrence_id=f"{did}-case",
        effective_at_utc=NOW,
        received_ts_utc=NOW,
        subject_instrument="NVDA",
        source_temporal_kind="derived",
        metadata=metadata,
    )


def _ev(did: str, derived=None, raw=None, *, params=(), contexts=()):
    row = _catalogue.catalogue_row(did)
    inputs = {k: (_k(k, v),) for k, v in (derived or {}).items()}
    raw_inputs = {k: (_k(k, v),) for k, v in (raw or {}).items()}
    p = api.CalculationParameterSetV1(
        f"cross-{did}",
        1,
        row.parameter_profiles[0],
        tuple(params) or (("selection_mode", "exact"),),
    )
    return _stage1.evaluate_stage1_kernel(
        did,
        raw_inputs=raw_inputs,
        derived_inputs=inputs,
        parameter_set=p,
        contexts=contexts,
        as_of_utc=NOW,
        knowledge_cutoff_utc=NOW,
    )


@pytest.mark.parametrize(
    "did,derived,raw,params,expected",
    [
        (
            "D128",
            {"D125": (("gamma_exposure", D(20)), ("spot_distance", D(2))), "D089": D(1)},
            {},
            (("spot_distance_boundaries", (D(0), D(5), D(10))),),
            (("shares", (D(1), D(0))), ("hhi", D(1))),
        ),
        (
            "D166",
            {"D159": D("0.8"), "D165": D("0.9")},
            {},
            (("minimum_identifiability", D("0.7")), ("minimum_utility", D("0.8"))),
            True,
        ),
        ("D175", {}, {}, (), D(50)),
        ("D176", {}, {}, (), 5),
        ("D178", {}, {}, (), D("5.5")),
        ("D189", {}, {}, (), (("delta", D(-10)), ("gamma", D(0)), ("vega", D(0)), ("theta", D(0)))),
        (
            "D191",
            {
                "D133": (("expected_fill_price", D(5)),),
                "D164": (
                    ("commissions", D(3)),
                    ("fees", D(1)),
                    ("multi_leg_incremental_cost", D(2)),
                ),
            },
            {"R034": D(4), "R035": D(6)},
            (("liquidation_quantity", D(2)), ("multiplier", D(100))),
            D(994),
        ),
        (
            "D199",
            {
                "D194": D(10),
                "D195": D(10),
                "D196": D(10),
                "D197": D(10),
                "D198": D(10),
                "D193": D(2),
            },
            {"R216": D(100), "R215": D(0)},
            (),
            D(50),
        ),
        (
            "D208",
            {"D202": D(8), "D207": D(2)},
            {},
            (("classification_thresholds", ("informative|5|3",)),),
            "informative",
        ),
    ],
)
def test_stage1_cross_stage_rule_algebra_numeric_and_lineage(
    did,
    derived,
    raw,
    params,
    expected,
):
    if did in {"D175", "D176", "D178", "D189"}:
        from .test_m01_f4_approved_execution_edge import case, evaluate
        from .test_m01_f4_approved_monetary_policy import budget, ev, fixture, hedge_fixture, kv

        if did == "D178":
            c = case(edge=D(40))
            result = evaluate(c)
            expected_ids = {"D133", "D177", *c["raw"]}
            assert result is not None and result.value == expected
        else:
            f = fixture((D(15), D(4), D(5), D(2))) if did == "D189" else fixture()
            if did == "D175":
                f["params"]["capital_fraction"] = D(".005")
            elif did == "D176":
                f["params"]["capital_fraction"] = D(".01")
                b = budget(f)
                f["raw"] = {}
                f["derived"] = {
                    "D175": (kv("D175", b),),
                    **{x: (kv(x, D(1)),) for x in ("D165", "D163", "D132")},
                }
                f["params"].update(
                    risk_per_unit=D(5),
                    uncertainty_multiplier=D(2),
                    liquidity_multiplier=D(2),
                    risk_per_unit_currency="USD",
                    risk_per_unit_definition="GREEK_SHOCK_ENVELOPE_V1",
                )
            else:
                f = hedge_fixture(f)
                f["params"]["target_bands"] = tuple(
                    name + "|0|10" for name in ("delta", "gamma", "vega", "theta")
                )
            result = ev(did, f)
            expected_ids = {
                v.occurrence_id
                for values in (*f["derived"].values(), *f["raw"].values())
                for v in values
            }
            assert result is not None
            value = (
                dict(result.value)["maximum_currency"]
                if did == "D175"
                else dict(result.value)["adjustment"]
                if did == "D189"
                else result.value
            )
            assert value == expected
        assert set(result.input_occurrence_ids) == expected_ids
    else:
        result = _ev(did, derived, raw, params=params)
        assert result is not None and result.value == expected
        assert set(result.input_occurrence_ids) == {f"{key}-case" for key in (*derived, *raw)}


def test_d164_exact_versioned_execution_schedule() -> None:
    schedule = api.ExecutionCostScheduleVersionV1(
        "schedule",
        1,
        (("fixed", D(1)),),
        (("exchange", D(2)),),
        (("multi", D(3)),),
        "USD",
    )
    result = _ev(
        "D164",
        {"D133": (("expected_slippage_currency", D(4)), ("currency", "USD"))},
        contexts=(schedule,),
    )
    assert result is not None and dict(result.value)["total"] == D(10)
    assert result.input_occurrence_ids == ("D133-case",)
    assert (
        _ev("D164", {"D133": (("expected_slippage_currency", D(4)), ("currency", "USD"))}) is None
    )
