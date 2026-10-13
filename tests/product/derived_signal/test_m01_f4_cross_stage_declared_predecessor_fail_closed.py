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


def _evaluate(did: str, *, without: str | None = None) -> _stage1.KernelResultV1 | None:
    from .test_m01_f4_approved_execution_edge import NOW, case, k
    from .test_m01_f4_approved_monetary_policy import action_fixture, ev, fixture, hedge_fixture
    if did == "D178":
        c = case()
        f = dict(raw={key: (k(key, value, contract_id="option", currency="USD", unit_convention_ref=("premium", 1)),) for key, value in c["raw"].items()},
                 derived={"D133": (k("D133", c["cost"]),), "D177": (k("D177", c["utility"]),)},
                 params=c["params"], contexts=c["contexts"])
    else:
        f = hedge_fixture(fixture()) if did == "D189" else action_fixture()
    if without is not None:
        f["derived"].pop(without)
    return _stage1.evaluate_stage1_kernel(
        did, raw_inputs=f["raw"], derived_inputs=f["derived"],
        parameter_set=api.CalculationParameterSetV1("mandatory", 1, "P_RULE", tuple(f["params"].items())),
        contexts=f["contexts"], as_of_utc=NOW, knowledge_cutoff_utc=NOW,
    )


@pytest.mark.parametrize(
    "did,missing",
    [("D178", "D133"), ("D178", "D177"), ("D189", "D175"), ("D192", "D175")],
)
def test_cross_stage_kernel_refuses_missing_mandatory_declared_predecessor(did, missing):
    assert _evaluate(did) is not None  # Control: test inputs exercise an emitting branch.
    assert _evaluate(did, without=missing) is None
