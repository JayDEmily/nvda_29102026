"""Stage-1 own-kernel proofs with controlled Stage-2 predecessor values.

These DO NOT prove, implement or admit Stage-2 predecessor kernels.
The public refusal tests use the admitted M00 read seam without Stage-2 truth.
"""

from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest

from nvda_desk.derived_signal_calculation_truth import _stage1, api
from nvda_desk.raw_signal_occurrence_truth import api as raw

AT = datetime(2026, 10, 12, 5, tzinfo=UTC)


def _kv(did: str, value: object, suffix: str) -> _stage1.KernelValueV1:
    return _stage1.KernelValueV1(
        value=value,
        occurrence_id=f"{did}-{suffix}",
        effective_at_utc=AT,
        received_ts_utc=AT,
        subject_instrument="NVDA",
        source_temporal_kind="derived",
    )


@pytest.mark.parametrize(
    "did,stage2,extra,expected",
    [
        (
            "D097",
            (
                _kv("D096", (("expiry_day", 10), ("iv", Decimal("0.20"))), "day10"),
                _kv("D096", (("expiry_day", 20), ("iv", Decimal("0.30"))), "day20"),
            ),
            {},
            Decimal(1),
        ),
        (
            "D098",
            (
                _kv("D096", (("expiry_day", 10), ("iv", Decimal("0.20"))), "day10"),
                _kv("D096", (("expiry_day", 20), ("iv", Decimal("0.30"))), "day20"),
                _kv("D096", (("expiry_day", 30), ("iv", Decimal("0.50"))), "day30"),
            ),
            {},
            Decimal("0.1"),
        ),
        (
            "D107",
            (_kv("D096", Decimal("0.30"), "iv"),),
            {"D035": (_kv("D035", Decimal("0.10"), "hv"),)},
            Decimal(20),
        ),
        (
            "D108",
            (_kv("D096", Decimal("0.30"), "iv"),),
            {"D036": (_kv("D036", Decimal("0.15"), "hv"),)},
            Decimal(15),
        ),
    ],
)
def test_cross_stage_k02_own_kernel_exact_arithmetic(did, stage2, extra, expected):
    value = _stage1.evaluate_stage1_kernel(
        did,
        raw_inputs={},
        derived_inputs={"D096": stage2, **extra},
        parameter_set=api.CalculationParameterSetV1(
            "cross-k02", 1, "P_BASIC", (("selection_mode", "exact"),)
        ),
        contexts=(),
        as_of_utc=AT,
        knowledge_cutoff_utc=AT,
    )
    assert value is not None and value.value == expected
    assert set(value.input_occurrence_ids) == {
        x.occurrence_id for group in (stage2, *extra.values()) for x in group
    }


@pytest.mark.parametrize("did", ("D097", "D098", "D107", "D108"))
def test_public_stage1_refuses_unavailable_stage2_predecessor(did):
    m00 = raw.create_owner()
    owner = api.create_owner(
        raw_projection_reader=m00.reads,
        parameter_sets=(
            api.CalculationParameterSetV1(
                "cross-k02", 1, "P_BASIC", (("selection_mode", "exact"),)
            ),
        ),
        input_selection_policies=(
            api.InputSelectionPolicyVersionV1(
                "cross-policy",
                1,
                ("subject_instrument",),
                timedelta(days=90),
                timedelta(days=90),
                ("true_instant",),
                (),
            ),
        ),
        utc_now=lambda: AT,
    )
    request = api.CalculationRequestV1(
        did,
        "NVDA",
        AT,
        AT,
        "stage1-cross-proof",
        "cross-k02",
        1,
        "cross-policy",
        1,
        (),
    )
    assert owner.materialise(request) is None
    assert (
        owner.reads.list_derived_history(derived_signal_id=did, subject_instrument="NVDA", limit=10)
        == ()
    )


def test_cross_stage_term_structure_requires_distinct_maturities_and_history():
    bad = (
        _kv("D096", (("expiry_day", 10), ("iv", Decimal("0.20"))), "a"),
        _kv("D096", (("expiry_day", 10), ("iv", Decimal("0.25"))), "b"),
    )
    assert (
        _stage1.evaluate_stage1_kernel(
            "D097",
            raw_inputs={},
            derived_inputs={"D096": bad},
            parameter_set=api.CalculationParameterSetV1(
                "cross-k02", 1, "P_BASIC", (("selection_mode", "exact"),)
            ),
            contexts=(),
            as_of_utc=AT,
            knowledge_cutoff_utc=AT,
        )
        is None
    )
