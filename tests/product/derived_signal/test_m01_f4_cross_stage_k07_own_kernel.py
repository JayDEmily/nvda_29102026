"""Provider-independent Stage-1 K07 own-kernel proof with stage-2 values controlled.

No positive observation from this fixture is a claimed Stage-2 implementation.
"""

from datetime import UTC, datetime
from decimal import Decimal

import pytest

from nvda_desk.derived_signal_calculation_truth import _catalogue, _stage1, api

AT = datetime(2026, 10, 12, 5, tzinfo=UTC)


def _v(identity: str, value: object) -> _stage1.KernelValueV1:
    return _stage1.KernelValueV1(
        value=value,
        occurrence_id=f"{identity}-fixture",
        effective_at_utc=AT,
        received_ts_utc=AT,
        subject_instrument="NVDA",
        source_temporal_kind="derived",
    )


@pytest.mark.parametrize(
    "identity",
    ("D158", "D159", "D163", "D171", "D172", "D187", "D200", "D207"),
)
def test_cross_stage_score_uses_its_own_declared_feature_and_provenance(identity: str) -> None:
    row = _catalogue.catalogue_row(identity)
    chosen = row.derived_dependencies[0]
    score = api.CalculationParameterSetV1(
        "cross-score",
        1,
        "P_SCORE",
        (("intercept", Decimal("0.25")),),
        score_features=(
            api.ScoreFeatureV1(
                chosen,
                "component",
                (),
                "identity",
                None,
                1,
                Decimal(1),
                None,
                None,
                (),
            ),
        ),
    )
    selected = _v(chosen, Decimal("4.5"))
    result = _stage1.evaluate_stage1_kernel(
        identity,
        raw_inputs={},
        derived_inputs={chosen: (selected,)},
        parameter_set=score,
        contexts=(),
        as_of_utc=AT,
        knowledge_cutoff_utc=AT,
    )
    expected = Decimal("4.75")
    if row.units == "0-1":
        expected = Decimal(1) / (Decimal(1) + (-expected).exp())
    assert result is not None and result.value == expected
    assert result.input_occurrence_ids == (selected.occurrence_id,)
    missing = _stage1.evaluate_stage1_kernel(
        identity,
        raw_inputs={},
        derived_inputs={},
        parameter_set=score,
        contexts=(),
        as_of_utc=AT,
        knowledge_cutoff_utc=AT,
    )
    assert missing is None


def test_cross_stage_d157_requires_versioned_partial_matrix() -> None:
    state = _v("D155", Decimal(4))
    matrix = _v("D156", (("partial_correlation_matrix", ((Decimal(1),),)),))
    param = api.CalculationParameterSetV1(
        "cross-matrix",
        1,
        "P_SCORE",
        (("intercept", Decimal(0)),),
        score_features=(
            api.ScoreFeatureV1(
                "D155",
                "component",
                (),
                "identity",
                None,
                1,
                Decimal(1),
                None,
                None,
                (),
            ),
        ),
    )
    result = _stage1.evaluate_stage1_kernel(
        "D157",
        raw_inputs={},
        derived_inputs={"D155": (state,), "D156": (matrix,)},
        parameter_set=param,
        contexts=(),
        as_of_utc=AT,
        knowledge_cutoff_utc=AT,
    )
    assert result is not None and result.value == Decimal(0)
    assert set(result.input_occurrence_ids) == {state.occurrence_id, matrix.occurrence_id}
    assert (
        _stage1.evaluate_stage1_kernel(
            "D157",
            raw_inputs={},
            derived_inputs={"D155": (state,)},
            parameter_set=param,
            contexts=(),
            as_of_utc=AT,
            knowledge_cutoff_utc=AT,
        )
        is None
    )
