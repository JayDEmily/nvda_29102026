"""Bounded Stage-1 own-kernel absence proofs, independent of unresolved risk mathematics.

These tests establish only mandatory-dependency refusal for D178/D189/D192.
They do not establish D133/D177 cost conversion, D175 exposure-risk clipping,
D175 breach detection, or Stage-2/public reachability.
"""

from datetime import UTC, datetime
from decimal import Decimal

import pytest

from nvda_desk.derived_signal_calculation_truth import _stage1, api

AT = datetime(2026, 10, 12, 10, tzinfo=UTC)


def _value(did: str, datum: object) -> _stage1.KernelValueV1:
    return _stage1.KernelValueV1(
        value=datum,
        occurrence_id=f"{did}-mandatory-probe",
        effective_at_utc=AT,
        received_ts_utc=AT,
        subject_instrument="NVDA",
        source_temporal_kind="derived",
    )


_CASES = {
    "D178": (
        {"D133": Decimal(4), "D177": Decimal(2)},
        {"R034": Decimal(4), "R035": Decimal(6), "R189": Decimal(5), "R190": Decimal(8)},
        (("allowed_execution_cost_per_unit", Decimal("0.5")), ("side", "buy")),
        "P_RULE",
    ),
    "D189": (
        {
            "D181": Decimal(15),
            "D182": Decimal(4),
            "D183": Decimal(5),
            "D184": Decimal(2),
            "D175": Decimal(30),
        },
        {},
        (("target_bands", ("delta|0|10", "gamma|0|10")),),
        "P_RULE",
    ),
    "D192": (
        {
            "D187": False,
            "D188": (("expected_currency_PnL", Decimal(10)),),
            "D189": (("delta", Decimal(0)),),
            "D190": Decimal(0),
            "D191": Decimal(5),
            "D175": Decimal(30),
        },
        {},
        (("mandatory_exit_on_invalidation", True), ("mandatory_hedge_on_risk", True)),
        "P_RULE",
    ),
}


def _evaluate(did: str, *, without: str | None = None) -> _stage1.KernelResultV1 | None:
    derived, raw, params, profile = _CASES[did]
    return _stage1.evaluate_stage1_kernel(
        did,
        raw_inputs={k: (_value(k, v),) for k, v in raw.items()},
        derived_inputs={k: (_value(k, v),) for k, v in derived.items() if k != without},
        parameter_set=api.CalculationParameterSetV1(f"absent-{did}", 1, profile, params),
        contexts=(),
        as_of_utc=AT,
        knowledge_cutoff_utc=AT,
    )


@pytest.mark.parametrize(
    "did,missing",
    [("D178", "D133"), ("D178", "D177"), ("D189", "D175"), ("D192", "D175")],
)
def test_cross_stage_kernel_refuses_missing_mandatory_declared_predecessor(did, missing):
    assert _evaluate(did) is not None  # Control: test inputs exercise an emitting branch.
    assert _evaluate(did, without=missing) is None
