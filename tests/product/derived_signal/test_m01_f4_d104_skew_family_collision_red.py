"""F4 D104 unresolved: current and prior skew must be corresponding measures.

The accepted catalogue lists D099 25-delta and D100 10-delta with no
selection/aggregation rule for D104's one `vol points` result. This RED
witness demonstrates that the current scalar kernel can cross families.
Do not repair by assuming a skew-family mode or inventing an aggregation.
"""

from datetime import UTC, datetime, timedelta
from decimal import Decimal

from nvda_desk.derived_signal_calculation_truth import _stage1, api

AT = datetime(2026, 10, 12, 4, tzinfo=UTC)


def _kv(value: int, oid: str, stamp: datetime) -> _stage1.KernelValueV1:
    return _stage1.KernelValueV1(
        value=Decimal(value),
        occurrence_id=oid,
        effective_at_utc=stamp,
        received_ts_utc=stamp,
        subject_instrument="NVDA",
        source_temporal_kind="derived",
        metadata=(),
    )


def test_d104_never_pairs_current_25_delta_with_prior_10_delta() -> None:
    prior = AT - timedelta(minutes=1)
    result = _stage1.evaluate_stage1_kernel(
        "D104",
        raw_inputs={},
        derived_inputs={
            "D099": (_kv(10, "a-prior99", prior), _kv(20, "z-current99", AT)),
            "D100": (_kv(30, "z-prior100", prior), _kv(40, "a-current100", AT)),
        },
        parameter_set=api.CalculationParameterSetV1(
            "skew-window",
            1,
            "P_WINDOW",
            (("anchor_seconds", 60),),
        ),
        contexts=(),
        as_of_utc=AT,
        knowledge_cutoff_utc=AT,
    )
    # Either lawful same-family change equals +10. The cross-family -10
    # is inadmissible, irrespective of the still-undefined scalar selection.
    assert result is None or result.value != Decimal(-10)
