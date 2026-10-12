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
        (
            "D175",
            {"D162": D(80), "D174": D(70)},
            {"R205": D(100), "R206": D(50), "R209": D(90), "R208": D(60)},
            (),
            D(50),
        ),
        (
            "D176",
            {"D175": D(100), "D165": D(20), "D163": D(2), "D132": D(4)},
            {},
            (
                ("risk_per_unit", D(5)),
                ("uncertainty_multiplier", D(2)),
                ("liquidity_multiplier", D(2)),
            ),
            5,
        ),
        (
            "D178",
            {"D133": D(4), "D177": D(2)},
            {"R034": D(4), "R035": D(6), "R189": D(5), "R190": D(8)},
            (("allowed_execution_cost_per_unit", D("0.5")), ("side", "buy")),
            D("5.5"),
        ),
        (
            "D189",
            {"D181": D(15), "D182": D(4), "D183": D(5), "D184": D(2), "D175": D(30)},
            {},
            (("target_bands", ("delta|0|10", "gamma|0|10")),),
            (("delta", D(-10)), ("gamma", D(0))),
        ),
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
    result = _ev("D164", {"D133": D(4)}, contexts=(schedule,))
    assert result is not None and dict(result.value)["total"] == D(10)
    assert result.input_occurrence_ids == ("D133-case",)
    assert _ev("D164", {"D133": D(4)}) is None
