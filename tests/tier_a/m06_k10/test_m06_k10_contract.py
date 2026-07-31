"""Tier A proof for M06 K10 independent parallel-risk authority."""

from __future__ import annotations

import importlib

import pytest

from tests.support.m06_k10_contract_harness import (
    CLOSED,
    make_prepared,
    reference_evaluate,
)


def test_reference_event_caution_is_explicit() -> None:
    result = reference_evaluate(make_prepared(scheduled_event=True))
    assert result.state == "caution"
    assert "scheduled_event_window_active" in result.caution_flags


def test_reference_term_inversion_is_explicit() -> None:
    result = reference_evaluate(make_prepared(front_dte=12, next_dte=5))
    assert "front_term_structure_backwardation" in result.caution_flags


def test_reference_vix_block_dominates() -> None:
    result = reference_evaluate(make_prepared(vix_level=55.0, scheduled_event=True))
    assert result.state == "block"
    assert result.hard_blocks == ("vix_block_threshold_reached",)


def test_reference_unknown_is_not_safe() -> None:
    result = reference_evaluate(make_prepared(vix_level=None, front_dte=None, next_dte=None))
    assert result.state == "unknown"
    assert result.unknown_families == ("options_term_structure", "volatility")


def test_reference_is_deterministic_and_stateless() -> None:
    prepared = make_prepared(vix_level=34.0)
    first = reference_evaluate(prepared)
    second = reference_evaluate(prepared)
    assert first == second
    assert first.semantic_fingerprint == second.semantic_fingerprint


def test_reference_closes_foreign_authority() -> None:
    result = reference_evaluate(make_prepared())
    assert result.closed_authority_classes == CLOSED
    assert result.foreign_authority_claimed is False


@pytest.mark.parametrize(
    ("mutant", "error"),
    [
        ("generic_mapping", "typed_prepared_envelope_required"),
        ("forged_prepared", "prepared_fingerprint_mismatch"),
        ("missing_policy", "policy_version_required"),
        ("missing_thresholds", "threshold_authority_required"),
        ("missing_threshold_refs", "threshold_authority_required"),
        ("reversed_thresholds", "threshold_order_invalid"),
        ("global_state_leak", None),
    ],
)
def test_named_mutants_are_killed(mutant: str, error: str | None) -> None:
    prepared = make_prepared(vix_level=34.0)
    if mutant == "generic_mapping":
        with pytest.raises(TypeError, match=error):
            reference_evaluate(prepared.model_dump(mode="python"))
    elif mutant == "forged_prepared":
        forged = prepared.model_copy(update={"prepared_fingerprint": "0" * 64})
        with pytest.raises(ValueError, match=error):
            reference_evaluate(forged)
    elif mutant == "missing_policy":
        with pytest.raises(ValueError, match=error):
            reference_evaluate(prepared, policy_version="")
    elif mutant == "missing_thresholds":
        with pytest.raises(ValueError, match=error):
            reference_evaluate(prepared, caution_threshold=None)
    elif mutant == "missing_threshold_refs":
        with pytest.raises(ValueError, match=error):
            reference_evaluate(prepared, threshold_authority_refs=())
    elif mutant == "reversed_thresholds":
        with pytest.raises(ValueError, match=error):
            reference_evaluate(prepared, caution_threshold=50.0, block_threshold=30.0)
    else:
        assert reference_evaluate(prepared) == reference_evaluate(prepared)


def _production():
    return importlib.import_module("nvda_desk.m06_parallel_risk")


def _build_production_input():
    m = _production()
    return m.ParallelRiskInput.from_prepared(
        make_prepared(vix_level=34.0),
        evaluator_policy_version="parallel-risk.compat.v1",
        aggregation_version="parallel-risk.aggregate.v1",
        threshold_authority_refs=(
            "m07:risk_vix_caution_threshold:v1",
            "m07:risk_vix_hot_threshold:v1",
        ),
        vix_caution_threshold=30.0,
        vix_block_threshold=50.0,
    )


def test_production_public_contracts_exist() -> None:
    m = _production()
    assert m.ParallelRiskInput and m.ParallelRiskObservation
    assert m.ParallelRiskAssessment and m.ParallelRiskEvaluator


def test_production_input_preserves_prepared_lineage() -> None:
    risk_input = _build_production_input()
    prepared = make_prepared(vix_level=34.0)
    assert risk_input.prepared_id == prepared.prepared_id
    assert risk_input.prepared_fingerprint == prepared.prepared_fingerprint


def test_production_evaluator_returns_typed_assessment() -> None:
    m = _production()
    result = m.ParallelRiskEvaluator().evaluate(_build_production_input())
    assert isinstance(result, m.ParallelRiskAssessment)
    assert result.state == "caution"


def test_production_block_dominates_caution() -> None:
    m = _production()
    risk_input = m.ParallelRiskInput.from_prepared(
        make_prepared(vix_level=55.0, scheduled_event=True),
        evaluator_policy_version="parallel-risk.compat.v1",
        aggregation_version="parallel-risk.aggregate.v1",
        threshold_authority_refs=("m07:caution:v1", "m07:block:v1"),
        vix_caution_threshold=30.0,
        vix_block_threshold=50.0,
    )
    assert m.ParallelRiskEvaluator().evaluate(risk_input).state == "block"


def test_production_unknown_remains_explicit() -> None:
    m = _production()
    risk_input = m.ParallelRiskInput.from_prepared(
        make_prepared(vix_level=None, front_dte=None, next_dte=None),
        evaluator_policy_version="parallel-risk.compat.v1",
        aggregation_version="parallel-risk.aggregate.v1",
        threshold_authority_refs=("m07:caution:v1", "m07:block:v1"),
        vix_caution_threshold=30.0,
        vix_block_threshold=50.0,
    )
    result = m.ParallelRiskEvaluator().evaluate(risk_input)
    assert result.state == "unknown"
    assert result.unknown_families == ("options_term_structure", "volatility")


def test_production_revalidates_copied_prepared_authority() -> None:
    m = _production()
    forged = make_prepared().model_copy(update={"prepared_fingerprint": "0" * 64})
    with pytest.raises(ValueError, match="prepared_fingerprint_mismatch"):
        m.ParallelRiskInput.from_prepared(
            forged,
            evaluator_policy_version="parallel-risk.compat.v1",
            aggregation_version="parallel-risk.aggregate.v1",
            threshold_authority_refs=("m07:caution:v1", "m07:block:v1"),
            vix_caution_threshold=30.0,
            vix_block_threshold=50.0,
        )


def test_production_is_deterministic_and_foreign_authority_closed() -> None:
    m = _production()
    evaluator = m.ParallelRiskEvaluator()
    risk_input = _build_production_input()
    first = evaluator.evaluate(risk_input)
    second = evaluator.evaluate(risk_input)
    assert first == second
    assert first.foreign_authority_claimed is False
    assert "capital" in first.closed_authority_classes
