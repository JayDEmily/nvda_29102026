from __future__ import annotations

from decimal import Decimal

import pytest

from nvda_desk.analysis.replay.walk_forward import (
    BucketAccumulator,
    ChronologyRule,
    DownstreamConsumerMode,
    FailureCollector,
    HorizonDiscoveryOutcome,
    OffsetComparisonOutcome,
    StabilityComparisonRule,
    WalkForwardHarnessAuthorityPacket,
    WalkForwardWindow,
    WalkForwardWindowMode,
    WalkForwardWindowRole,
    build_bucket_summaries,
    build_comparison_report,
    build_default_fragility_scenarios,
    build_failure_mode_summary,
    build_variant_payload,
    merge_failure_modes,
    rank_stack_summary,
    run_slv_batch_rank_from_market,
    run_slv_fragility_from_market,
    run_slv_walk_forward_from_market,
)


def test_walk_forward_contracts_reject_chronology_leakage_and_bound_vocabularies() -> None:
    assert WalkForwardWindowMode.ROLLING.value == "rolling"
    assert WalkForwardWindowRole.TRAIN.value == "train"
    assert ChronologyRule.NO_OVERLAP.value == "no_overlap"
    assert DownstreamConsumerMode.REVIEW_ONLY.value == "review_only"

    ok = WalkForwardWindow(
        window_id="wf-001",
        role=WalkForwardWindowRole.TRAIN,
        start_index=0,
        end_index=3,
    )
    later = WalkForwardWindow(
        window_id="wf-002",
        role=WalkForwardWindowRole.VALIDATION,
        start_index=4,
        end_index=5,
    )
    assert ok.precedes(later)

    with pytest.raises(ValueError, match="start_index must be <= end_index"):
        WalkForwardWindow(
            window_id="bad",
            role=WalkForwardWindowRole.TEST,
            start_index=5,
            end_index=4,
        )

    with pytest.raises(ValueError, match="chronology leakage"):
        WalkForwardHarnessAuthorityPacket(
            packet_id="pkt-001",
            dataset_id="dataset-001",
            dataset_fingerprint="a" * 64,
            windows=(ok, WalkForwardWindow("wf-overlap", WalkForwardWindowRole.TEST, 2, 6)),
        )

    with pytest.raises(ValueError, match="dataset_fingerprint"):
        WalkForwardHarnessAuthorityPacket(
            packet_id="pkt-invalid-dataset",
            dataset_id="dataset-001",
            dataset_fingerprint="not-a-sha256",
        )


def test_stability_horizon_and_comparison_reports_are_deterministic() -> None:
    rule = StabilityComparisonRule(metric_name="sharpe", maximum_degradation=Decimal("0.10"))
    outcome = OffsetComparisonOutcome(
        offset_id="off-0",
        baseline_metric=Decimal("1.00"),
        candidate_metric=Decimal("0.93"),
        rule=rule,
    )

    assert outcome.degradation == Decimal("0.07")
    assert outcome.is_stable is True

    horizon = HorizonDiscoveryOutcome(
        horizon_id="h-1",
        offset_outcomes=(outcome,),
        minimum_stable_offsets=1,
    )
    assert horizon.is_accepted is True

    report = build_comparison_report(
        report_id="cmp-1",
        stack_summaries=[
            {"stack_id": "base", "score": "0.80", "baseline_score": "0.80"},
            {"stack_id": "candidate", "score": "0.90", "baseline_score": "0.80"},
        ],
    )
    assert [summary.stack_id for summary in report.stack_summaries] == ["base", "candidate"]
    assert report.best_stack_id == "candidate"
    assert rank_stack_summary(report.stack_summaries[1]) == Decimal("0.10")


def test_slv_experiment_helpers_collect_failures_and_summaries_without_runtime_side_effects() -> (
    None
):
    accumulator = BucketAccumulator(bucket_id="opening")
    accumulator.add("candidate-a", Decimal("1.25"))
    accumulator.add("candidate-b", Decimal("0.75"))
    assert build_bucket_summaries([accumulator])[0].mean_score == Decimal("1.00")

    collector = FailureCollector(kind="walk_forward")
    collector.add("horizon", "unstable")
    collector.add("horizon", "unstable")
    collector.add("fragility", "thin_bucket")
    failure_summary = build_failure_mode_summary(collector)
    assert failure_summary.count_by_mode == {"horizon:unstable": 2, "fragility:thin_bucket": 1}
    assert (
        merge_failure_modes([failure_summary, failure_summary]).count_by_mode["horizon:unstable"]
        == 4
    )

    assert build_default_fragility_scenarios()[0].scenario_id == "baseline"
    assert build_variant_payload("variant-a", {"score": 1}) == {
        "variant_id": "variant-a",
        "payload": {"score": 1},
    }


def test_slv_market_entrypoints_return_review_only_reports() -> None:
    market_rows = [
        {"candidate_id": "a", "score": "0.10"},
        {"candidate_id": "b", "score": "0.20"},
        {"candidate_id": "c", "score": "0.15"},
    ]

    walk_forward = run_slv_walk_forward_from_market(market_rows, report_id="wf")
    fragility = run_slv_fragility_from_market(market_rows, report_id="fg")
    ranking = run_slv_batch_rank_from_market(market_rows, report_id="rk")

    assert walk_forward.consumer_mode is DownstreamConsumerMode.REVIEW_ONLY
    assert fragility.consumer_mode is DownstreamConsumerMode.REVIEW_ONLY
    assert ranking.best_stack_id == "b"
    assert [summary.stack_id for summary in ranking.stack_summaries] == ["b", "c", "a"]
