from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta

from nvda_desk.domain.session_clock import SessionClockClassifier
from nvda_desk.schemas.eval import (
    BatchVariantConfig,
    FailureModeSummary,
    FailureSeverity,
    FragilityScenarioInput,
    FragilityScenarioResult,
    RankedVariantSummary,
    RegimeBucketSummary,
    StrategicLadderBatchRankingInput,
    StrategicLadderBatchRankingOutput,
    StrategicLadderFragilityInput,
    StrategicLadderFragilityOutput,
    StrategicLadderWalkForwardInput,
    StrategicLadderWalkForwardOutput,
    VolatilityBucket,
    WalkForwardWindowSummary,
)
from nvda_desk.schemas.slv import (
    LadderOverallDecision,
    LadderReplayRungOutcome,
    LadderRungMarketInput,
    StrategicLadderReplayInput,
    StrategicLadderReplayOutput,
)
from nvda_desk.services.config_surface import (
    ConfigSurfaceLookupError,
    ConfigSurfaceService,
)
from nvda_desk.services.experiment_log import ExperimentLogService
from nvda_desk.services.market_state import MarketStateService
from nvda_desk.services.slv_replay import StrategicLadderReplayService


@dataclass(frozen=True)
class _ReplayContext:
    replay_input: StrategicLadderReplayInput
    replay_output: StrategicLadderReplayOutput
    volatility_bucket: VolatilityBucket
    anchor_ts: datetime


@dataclass(frozen=True)
class _BucketAccumulator:
    count: int = 0
    pass_count: int = 0
    score_sum: float = 0.0

    def add(self, *, passed: bool, score: float) -> _BucketAccumulator:
        return _BucketAccumulator(
            count=self.count + 1,
            pass_count=self.pass_count + (1 if passed else 0),
            score_sum=self.score_sum + score,
        )


class StrategicLadderExperimentService:
    def __init__(
        self,
        classifier: SessionClockClassifier,
        market_state_service: MarketStateService,
        replay_service: StrategicLadderReplayService,
        experiment_log_service: ExperimentLogService,
        config_surface_service: ConfigSurfaceService,
    ):
        self._classifier = classifier
        self._market_state = market_state_service
        self._replay = replay_service
        self._experiment_log = experiment_log_service
        self._config_surface = config_surface_service

    def walk_forward_from_market(
        self,
        payload: StrategicLadderWalkForwardInput,
    ) -> StrategicLadderWalkForwardOutput:
        contexts = [
            self._run_replay(
                base_payload=self._apply_named_overrides(
                    payload.base_payload,
                    strategy_variant_name=payload.strategy_variant_name,
                    coefficient_group_name=payload.coefficient_group_name,
                ),
                anchor_ts=anchor_ts,
            )
            for anchor_ts in payload.anchor_timestamps
        ]
        output = self._build_walk_forward_output(
            module_id=payload.base_payload.descriptor.module_id,
            config_name=payload.config_name,
            contexts=contexts,
        )
        recorded = self._experiment_log.record(
            symbol=payload.base_payload.symbol,
            module_id=payload.base_payload.descriptor.module_id,
            experiment_type="walk_forward",
            config_name=payload.config_name,
            requested_at=payload.anchor_timestamps[-1],
            input_payload=payload,
            output_payload=output,
            ranking_score=output.average_forward_score,
        )
        return output.model_copy(update={"experiment_id": recorded.experiment_id})

    def fragility_from_market(
        self,
        payload: StrategicLadderFragilityInput,
    ) -> StrategicLadderFragilityOutput:
        scenarios = payload.scenarios or self._default_fragility_scenarios()
        configured_payload = self._apply_named_overrides(
            payload.base_payload,
            strategy_variant_name=payload.strategy_variant_name,
            coefficient_group_name=payload.coefficient_group_name,
        )
        baseline = self._run_replay(
            base_payload=configured_payload, anchor_ts=configured_payload.entry_ts
        )
        scenario_results: list[FragilityScenarioResult] = []
        failure_evidence: dict[str, list[str]] = defaultdict(list)
        drops: list[float] = []
        for scenario in scenarios:
            replay_input = self._variant_payload(
                configured_payload,
                variant=scenario,
                anchor_ts=configured_payload.entry_ts,
            )
            replay_output = self._replay.replay_from_market(replay_input)
            score_drop = max(0.0, baseline.replay_output.replay_score - replay_output.replay_score)
            drops.append(score_drop)
            scenario_result = FragilityScenarioResult(
                name=scenario.name,
                replay_score=replay_output.replay_score,
                score_drop=round(score_drop, 4),
                risk_action=replay_output.supervisory_overlay.action,
                overall_decision=replay_output.overall_decision.value,
                filled_rungs=self._filled_rung_count(replay_output.rung_outcomes),
                total_rungs=len(replay_output.rung_outcomes),
            )
            scenario_results.append(scenario_result)
            self._collect_fragility_failures(
                scenario=scenario,
                baseline=baseline.replay_output,
                scenario_output=replay_output,
                failure_evidence=failure_evidence,
            )

        fragility_score = round(sum(drops) / len(drops), 4) if drops else 0.0
        output = StrategicLadderFragilityOutput(
            module_id=payload.base_payload.descriptor.module_id,
            config_name=payload.config_name,
            baseline_replay_score=baseline.replay_output.replay_score,
            fragility_score=max(0.0, min(1.0, fragility_score)),
            worst_case_drop=round(max(drops, default=0.0), 4),
            scenario_results=scenario_results,
            failure_modes=self._failure_modes_from_evidence(
                failure_evidence, max(len(scenarios), 1)
            ),
        )
        recorded = self._experiment_log.record(
            symbol=payload.base_payload.symbol,
            module_id=payload.base_payload.descriptor.module_id,
            experiment_type="fragility",
            config_name=payload.config_name,
            requested_at=payload.base_payload.entry_ts,
            input_payload=payload,
            output_payload=output,
            ranking_score=max(0.0, min(1.0, 1.0 - output.fragility_score)),
        )
        return output.model_copy(update={"experiment_id": recorded.experiment_id})

    def batch_rank_from_market(
        self,
        payload: StrategicLadderBatchRankingInput,
    ) -> StrategicLadderBatchRankingOutput:
        ranked_variants: list[RankedVariantSummary] = []
        variants = list(payload.variants)
        for variant_name in payload.variant_names:
            variants.append(
                BatchVariantConfig(name=variant_name, strategy_variant_name=variant_name)
            )
        if not variants:
            raise ValueError("at least one explicit variant or named strategy variant is required")
        for variant in variants:
            configured_payload = self._apply_named_overrides(
                payload.base_payload,
                strategy_variant_name=variant.strategy_variant_name,
                coefficient_group_name=variant.coefficient_group_name,
            )
            walk_forward_input = StrategicLadderWalkForwardInput(
                base_payload=self._variant_payload(
                    configured_payload,
                    variant=variant,
                    anchor_ts=payload.base_payload.entry_ts,
                ),
                anchor_timestamps=[
                    anchor + timedelta(minutes=variant.entry_offset_minutes)
                    for anchor in payload.anchor_timestamps
                ],
                config_name=variant.name,
                strategy_variant_name=variant.strategy_variant_name,
                coefficient_group_name=variant.coefficient_group_name,
            )
            walk_forward_output = self.walk_forward_from_market(walk_forward_input)
            fragility_input = StrategicLadderFragilityInput(
                base_payload=self._variant_payload(
                    configured_payload,
                    variant=variant,
                    anchor_ts=payload.base_payload.entry_ts,
                ),
                config_name=variant.name,
                strategy_variant_name=variant.strategy_variant_name,
                coefficient_group_name=variant.coefficient_group_name,
            )
            fragility_output = self.fragility_from_market(fragility_input)
            ranking_score = self._ranking_score(
                average_forward_score=walk_forward_output.average_forward_score,
                pass_rate=walk_forward_output.pass_rate,
                fragility_score=fragility_output.fragility_score,
            )
            ranked_variants.append(
                RankedVariantSummary(
                    name=variant.name,
                    ranking_score=ranking_score,
                    average_forward_score=walk_forward_output.average_forward_score,
                    pass_rate=walk_forward_output.pass_rate,
                    fragility_score=fragility_output.fragility_score,
                    failure_modes=self._merge_failure_modes(
                        walk_forward_output.failure_modes,
                        fragility_output.failure_modes,
                    ),
                )
            )
        ranked_variants.sort(key=lambda item: item.ranking_score, reverse=True)
        output = StrategicLadderBatchRankingOutput(
            module_id=payload.base_payload.descriptor.module_id,
            batch_name=payload.batch_name,
            ranked_variants=ranked_variants,
        )
        recorded = self._experiment_log.record(
            symbol=payload.base_payload.symbol,
            module_id=payload.base_payload.descriptor.module_id,
            experiment_type="batch_ranking",
            config_name=payload.batch_name,
            requested_at=payload.anchor_timestamps[-1],
            input_payload=payload,
            output_payload=output,
            ranking_score=ranked_variants[0].ranking_score if ranked_variants else 0.0,
        )
        return output.model_copy(update={"experiment_id": recorded.experiment_id})

    def _build_walk_forward_output(
        self,
        *,
        module_id: str,
        config_name: str,
        contexts: Sequence[_ReplayContext],
    ) -> StrategicLadderWalkForwardOutput:
        phase_accumulators: dict[str, _BucketAccumulator] = {}
        volatility_accumulators: dict[str, _BucketAccumulator] = {}
        risk_accumulators: dict[str, _BucketAccumulator] = {}
        windows: list[WalkForwardWindowSummary] = []
        failure_evidence: dict[str, list[str]] = defaultdict(list)
        total_score = 0.0
        pass_count = 0
        for context in contexts:
            result = context.replay_output
            passed = result.overall_decision is LadderOverallDecision.ACCEPT
            total_score += result.replay_score
            pass_count += 1 if passed else 0
            phase_key = context.replay_output.entry_phase.value
            volatility_key = context.volatility_bucket
            risk_key = result.supervisory_overlay.action.value
            phase_accumulators[phase_key] = phase_accumulators.get(
                phase_key, _BucketAccumulator()
            ).add(
                passed=passed,
                score=result.replay_score,
            )
            volatility_accumulators[volatility_key] = volatility_accumulators.get(
                volatility_key, _BucketAccumulator()
            ).add(
                passed=passed,
                score=result.replay_score,
            )
            risk_accumulators[risk_key] = risk_accumulators.get(risk_key, _BucketAccumulator()).add(
                passed=passed,
                score=result.replay_score,
            )
            windows.append(
                WalkForwardWindowSummary(
                    anchor_ts=context.anchor_ts,
                    entry_phase=result.entry_phase,
                    volatility_bucket=context.volatility_bucket,
                    risk_action=result.supervisory_overlay.action,
                    pass_rate=1.0 if passed else 0.0,
                    average_score=result.replay_score,
                    filled_rungs=self._filled_rung_count(result.rung_outcomes),
                    total_rungs=len(result.rung_outcomes),
                )
            )
            self._collect_walk_forward_failures(context=context, failure_evidence=failure_evidence)

        evaluation_count = len(contexts)
        output = StrategicLadderWalkForwardOutput(
            module_id=module_id,
            config_name=config_name,
            evaluation_count=evaluation_count,
            average_forward_score=round(total_score / evaluation_count, 4),
            pass_rate=round(pass_count / evaluation_count, 4),
            windows=windows,
            phase_buckets=self._bucket_summaries(phase_accumulators),
            volatility_buckets=self._bucket_summaries(volatility_accumulators),
            risk_action_buckets=self._bucket_summaries(risk_accumulators),
            failure_modes=self._failure_modes_from_evidence(failure_evidence, evaluation_count),
        )
        return output

    def _run_replay(
        self,
        *,
        base_payload: StrategicLadderReplayInput,
        anchor_ts: datetime,
    ) -> _ReplayContext:
        replay_input = self._materialize_market_payload(
            base_payload=base_payload, anchor_ts=anchor_ts
        )
        replay_output = self._replay.replay_from_market(replay_input)
        return _ReplayContext(
            replay_input=replay_input,
            replay_output=replay_output,
            volatility_bucket=self._volatility_bucket(anchor_ts),
            anchor_ts=anchor_ts,
        )

    def _apply_named_overrides(
        self,
        base_payload: StrategicLadderReplayInput,
        *,
        strategy_variant_name: str | None,
        coefficient_group_name: str | None,
    ) -> StrategicLadderReplayInput:
        try:
            return self._config_surface.apply_replay_overrides(
                base_payload,
                strategy_variant_name=strategy_variant_name,
                coefficient_group_name=coefficient_group_name,
            )
        except ConfigSurfaceLookupError as exc:
            raise ValueError(str(exc)) from exc

    def _materialize_market_payload(
        self,
        *,
        base_payload: StrategicLadderReplayInput,
        anchor_ts: datetime,
    ) -> StrategicLadderReplayInput:
        snapshot = self._market_state.get_market_snapshot(symbol=base_payload.symbol, ts=anchor_ts)
        spot_price = base_payload.spot_price
        if snapshot.latest_bar is not None:
            spot_price = float(snapshot.latest_bar.close)
        return base_payload.model_copy(
            update={
                "entry_ts": anchor_ts.astimezone(UTC),
                "session_phase": self._classifier.classify(anchor_ts).phase,
                "spot_price": round(spot_price, 4),
                "distance_to_vwap_pct": self._distance_to_vwap_pct(
                    symbol=base_payload.symbol,
                    ts=anchor_ts,
                    fallback=base_payload.distance_to_vwap_pct,
                ),
            }
        )

    def _variant_payload(
        self,
        base_payload: StrategicLadderReplayInput,
        *,
        variant: BatchVariantConfig | FragilityScenarioInput,
        anchor_ts: datetime,
    ) -> StrategicLadderReplayInput:
        replay_input = self._materialize_market_payload(
            base_payload=base_payload, anchor_ts=anchor_ts
        )
        adjusted_rungs = [
            LadderRungMarketInput(
                price=round(rung.price * (1.0 + (variant.rung_price_shift_pct / 100.0)), 4),
                size_units=round(rung.size_units * variant.rung_size_scale, 4),
            )
            for rung in replay_input.rungs
        ]
        lookahead_minutes = replay_input.lookahead_minutes
        if isinstance(variant, BatchVariantConfig) and variant.lookahead_minutes is not None:
            lookahead_minutes = variant.lookahead_minutes
        adjusted_ts = replay_input.entry_ts + timedelta(minutes=variant.entry_offset_minutes)
        return replay_input.model_copy(
            update={
                "entry_ts": adjusted_ts,
                "session_phase": self._classifier.classify(adjusted_ts).phase,
                "distance_to_vwap_pct": round(
                    replay_input.distance_to_vwap_pct + variant.vwap_offset_pct,
                    4,
                ),
                "iv_hv_divergence_pct": round(
                    replay_input.iv_hv_divergence_pct + variant.iv_hv_divergence_offset_pct,
                    4,
                ),
                "lookahead_minutes": lookahead_minutes,
                "rungs": adjusted_rungs,
            }
        )

    def _distance_to_vwap_pct(self, *, symbol: str, ts: datetime, fallback: float) -> float:
        bars = self._market_state.get_intraday_bars(symbol=symbol, ts=ts, limit=15).bars
        if not bars:
            return fallback
        weighted_notional = 0.0
        weighted_volume = 0.0
        for bar in bars:
            typical_price = (float(bar.high) + float(bar.low) + float(bar.close)) / 3.0
            weighted_notional += typical_price * bar.volume
            weighted_volume += bar.volume
        if weighted_volume <= 0:
            return fallback
        vwap = weighted_notional / weighted_volume
        latest_close = float(bars[-1].close)
        if vwap == 0:
            return fallback
        return round(((latest_close - vwap) / vwap) * 100.0, 4)

    def _volatility_bucket(self, ts: datetime) -> VolatilityBucket:
        snapshot = self._market_state.get_market_snapshot(symbol="VIX", ts=ts)
        if snapshot.latest_bar is None:
            return "medium"
        level = float(snapshot.latest_bar.close)
        if level < 18.0:
            return "low"
        if level < 25.0:
            return "medium"
        return "high"

    def _collect_walk_forward_failures(
        self,
        *,
        context: _ReplayContext,
        failure_evidence: dict[str, list[str]],
    ) -> None:
        result = context.replay_output
        evidence = context.anchor_ts.isoformat()
        if result.supervisory_overlay.action.value == "block":
            failure_evidence["overlay_blocked"].append(evidence)
        if self._filled_rung_count(result.rung_outcomes) == 0:
            failure_evidence["no_fills"].append(evidence)
        if self._drawdown_count(result.rung_outcomes) > self._bounce_count(result.rung_outcomes):
            failure_evidence["drawdown_dominant"].append(evidence)
        if result.replay_score < 0.45:
            failure_evidence[f"phase_underperformance:{result.entry_phase.value}"].append(evidence)
        if context.volatility_bucket == "high" and result.replay_score < 0.45:
            failure_evidence["high_volatility_underperformance"].append(evidence)
        if result.market_validation.overall_decision != result.overall_decision:
            failure_evidence["overlay_decision_downgrade"].append(evidence)

    def _collect_fragility_failures(
        self,
        *,
        scenario: FragilityScenarioInput,
        baseline: StrategicLadderReplayOutput,
        scenario_output: StrategicLadderReplayOutput,
        failure_evidence: dict[str, list[str]],
    ) -> None:
        evidence = scenario.name
        score_drop = baseline.replay_score - scenario_output.replay_score
        if scenario.entry_offset_minutes != 0 and score_drop > 0.15:
            failure_evidence["timing_sensitive"].append(evidence)
        if scenario.rung_price_shift_pct != 0 and score_drop > 0.15:
            failure_evidence["price_precision_sensitive"].append(evidence)
        if scenario.vwap_offset_pct != 0 and score_drop > 0.1:
            failure_evidence["vwap_distance_sensitive"].append(evidence)
        if scenario.iv_hv_divergence_offset_pct != 0 and score_drop > 0.1:
            failure_evidence["volatility_assumption_sensitive"].append(evidence)
        if scenario_output.overall_decision is LadderOverallDecision.REJECT:
            failure_evidence["rejection_prone"].append(evidence)
        if self._filled_rung_count(scenario_output.rung_outcomes) == 0:
            failure_evidence["fragility_no_fills"].append(evidence)

    def _default_fragility_scenarios(self) -> list[FragilityScenarioInput]:
        return [
            FragilityScenarioInput(name="time_delay_5m", entry_offset_minutes=5),
            FragilityScenarioInput(name="rung_shift_up_0_5pct", rung_price_shift_pct=0.5),
            FragilityScenarioInput(name="rung_shift_down_0_5pct", rung_price_shift_pct=-0.5),
            FragilityScenarioInput(name="vwap_distance_plus_0_75pct", vwap_offset_pct=0.75),
            FragilityScenarioInput(name="iv_hv_plus_10pct", iv_hv_divergence_offset_pct=10.0),
        ]

    def _bucket_summaries(
        self, accumulators: dict[str, _BucketAccumulator]
    ) -> list[RegimeBucketSummary]:
        return [
            RegimeBucketSummary(
                bucket=bucket,
                evaluation_count=acc.count,
                pass_rate=round(acc.pass_count / acc.count, 4),
                average_score=round(acc.score_sum / acc.count, 4),
            )
            for bucket, acc in sorted(accumulators.items())
        ]

    def _failure_modes_from_evidence(
        self,
        failure_evidence: dict[str, list[str]],
        evaluation_count: int,
    ) -> list[FailureModeSummary]:
        failure_modes: list[FailureModeSummary] = []
        for code, evidence in sorted(failure_evidence.items()):
            share = len(evidence) / evaluation_count
            if share >= 0.5:
                severity: FailureSeverity = "high"
            elif share >= 0.25:
                severity = "medium"
            else:
                severity = "low"
            failure_modes.append(
                FailureModeSummary(
                    code=code,
                    occurrences=len(evidence),
                    share_of_evaluations=round(share, 4),
                    severity=severity,
                    evidence=evidence[:5],
                )
            )
        return failure_modes

    def _merge_failure_modes(
        self,
        walk_forward_modes: Sequence[FailureModeSummary],
        fragility_modes: Sequence[FailureModeSummary],
    ) -> list[FailureModeSummary]:
        merged: dict[str, tuple[int, list[str]]] = {}
        for mode in list(walk_forward_modes) + list(fragility_modes):
            count, evidence = merged.get(mode.code, (0, []))
            merged[mode.code] = (count + mode.occurrences, evidence + mode.evidence)
        return self._failure_modes_from_evidence(
            {code: evidence for code, (_, evidence) in merged.items()},
            max(len(merged), 1),
        )

    def _ranking_score(
        self,
        *,
        average_forward_score: float,
        pass_rate: float,
        fragility_score: float,
    ) -> float:
        score = (
            (average_forward_score * 0.55) + (pass_rate * 0.25) + ((1.0 - fragility_score) * 0.20)
        )
        return round(max(0.0, min(1.0, score)), 4)

    def _filled_rung_count(self, outcomes: Iterable[LadderReplayRungOutcome]) -> int:
        return sum(1 for outcome in outcomes if outcome.filled)

    def _drawdown_count(self, outcomes: Iterable[LadderReplayRungOutcome]) -> int:
        return sum(1 for outcome in outcomes if outcome.outcome_label == "drawdown")

    def _bounce_count(self, outcomes: Iterable[LadderReplayRungOutcome]) -> int:
        return sum(1 for outcome in outcomes if outcome.outcome_label == "bounce")
