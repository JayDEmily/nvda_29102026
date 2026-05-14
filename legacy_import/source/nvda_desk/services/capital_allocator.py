from __future__ import annotations

from nvda_desk.schemas.allocation import (
    ModuleCapitalAllocation,
    ModuleRegimeCapitalAllocationInput,
    ModuleRegimeCapitalAllocationOutput,
)
from nvda_desk.schemas.eval import ExperimentRunPayload
from nvda_desk.services.config_surface import (
    ConfigSurfaceLookupError,
    ConfigSurfaceService,
)
from nvda_desk.services.experiment_log import ExperimentLogService


class CapitalAllocatorService:
    def __init__(
        self,
        experiment_log_service: ExperimentLogService,
        config_surface_service: ConfigSurfaceService,
    ):
        self._experiment_log = experiment_log_service
        self._config_surface = config_surface_service

    def allocate(
        self, payload: ModuleRegimeCapitalAllocationInput
    ) -> ModuleRegimeCapitalAllocationOutput:
        caution_threshold, hot_threshold = self._config_surface.reserve_vix_thresholds(
            coefficient_group_name=payload.coefficient_group_name
        )
        reserve_pct = self._reserve_pct(
            vix_level=payload.vix_level,
            vvix_level=payload.vvix_level,
            caution_threshold=caution_threshold,
            hot_threshold=hot_threshold,
        )
        deployable_pct = max(0.0, 100.0 - reserve_pct)
        scored_candidates: list[tuple[str, str, float, float, list[str], float, float, float]] = []
        for candidate in payload.candidates:
            walk_forward = self._experiment_log.latest_run(
                module_id=candidate.module_id,
                experiment_type="walk_forward",
            )
            fragility = self._experiment_log.latest_run(
                module_id=candidate.module_id,
                experiment_type="fragility",
            )
            quality_score, regime_fit_score, reasons = self._candidate_score(
                walk_forward=walk_forward,
                fragility=fragility,
                requested_phase=payload.session_phase.value,
                requested_volatility_bucket=self._volatility_bucket(payload.vix_level),
            )
            effective_weight = candidate.base_weight
            if candidate.config_key is not None:
                try:
                    config_weight = self._config_surface.effective_weight(
                        config_key=candidate.config_key,
                        strategy_variant_name=payload.strategy_variant_name,
                    )
                except ConfigSurfaceLookupError:
                    config_weight = None
                    reasons.append("config_weight_key_unknown")
                else:
                    if config_weight is not None:
                        effective_weight = config_weight
                        if payload.strategy_variant_name is not None:
                            reasons.append("variant_weight_override_applied")
                        else:
                            reasons.append("registry_weight_applied")
            scored_candidates.append(
                (
                    candidate.module_id,
                    candidate.module_name,
                    quality_score * effective_weight,
                    regime_fit_score,
                    reasons,
                    candidate.min_allocation_pct,
                    candidate.max_allocation_pct,
                    effective_weight,
                )
            )
        total_weight = sum(item[2] for item in scored_candidates)
        allocations: list[ModuleCapitalAllocation] = []
        for (
            module_id,
            module_name,
            weighted_score,
            regime_fit_score,
            reasons,
            min_pct,
            max_pct,
            _,
        ) in scored_candidates:
            if total_weight <= 0:
                allocation_pct = 0.0
            else:
                raw_pct = deployable_pct * (weighted_score / total_weight)
                allocation_pct = min(max(raw_pct, min_pct), max_pct)
            allocations.append(
                ModuleCapitalAllocation(
                    module_id=module_id,
                    module_name=module_name,
                    allocation_pct=round(allocation_pct, 4),
                    allocated_capital=round(payload.total_capital * (allocation_pct / 100.0), 4),
                    quality_score=round(min(weighted_score, 1.0), 4),
                    regime_fit_score=round(regime_fit_score, 4),
                    reasons=reasons,
                )
            )
        allocated_pct = sum(item.allocation_pct for item in allocations)
        cash_reserve_pct = round(max(0.0, 100.0 - allocated_pct), 4)
        return ModuleRegimeCapitalAllocationOutput(
            requested_at=payload.requested_at,
            total_capital=payload.total_capital,
            cash_reserve_pct=cash_reserve_pct,
            cash_reserve_capital=round(payload.total_capital * (cash_reserve_pct / 100.0), 4),
            allocations=allocations,
        )

    def _candidate_score(
        self,
        *,
        walk_forward: ExperimentRunPayload | None,
        fragility: ExperimentRunPayload | None,
        requested_phase: str,
        requested_volatility_bucket: str,
    ) -> tuple[float, float, list[str]]:
        reasons: list[str] = []
        if walk_forward is None:
            return 0.0, 0.0, ["no_walk_forward_experiment"]
        if fragility is None:
            return 0.0, 0.0, ["no_fragility_experiment"]

        walk_output = walk_forward.output_payload
        average_score = float(walk_output.get("average_forward_score", 0.0))
        pass_rate = float(walk_output.get("pass_rate", 0.0))
        fragility_score = float(fragility.output_payload.get("fragility_score", 1.0))
        phase_fit = self._bucket_score(walk_output.get("phase_buckets", []), requested_phase)
        volatility_fit = self._bucket_score(
            walk_output.get("volatility_buckets", []),
            requested_volatility_bucket,
        )
        regime_fit_score = (phase_fit * 0.6) + (volatility_fit * 0.4)
        quality = (
            average_score
            * max(pass_rate, 0.05)
            * max(1.0 - fragility_score, 0.05)
            * max(regime_fit_score, 0.05)
        )
        if phase_fit < 0.4:
            reasons.append("phase_fit_weak")
        if volatility_fit < 0.4:
            reasons.append("volatility_fit_weak")
        if fragility_score > 0.4:
            reasons.append("fragility_elevated")
        if average_score < 0.45:
            reasons.append("average_forward_score_below_floor")
        if pass_rate < 0.4:
            reasons.append("pass_rate_below_floor")
        if not reasons:
            reasons.append("allocation_within_current_regime_tolerances")
        return quality, regime_fit_score, reasons

    def _bucket_score(self, buckets: object, bucket_name: str) -> float:
        if not isinstance(buckets, list):
            return 0.0
        for bucket in buckets:
            if isinstance(bucket, dict) and bucket.get("bucket") == bucket_name:
                return float(bucket.get("average_score", 0.0))
        return 0.0

    def _reserve_pct(
        self,
        *,
        vix_level: float,
        vvix_level: float,
        caution_threshold: float,
        hot_threshold: float,
    ) -> float:
        if vix_level >= hot_threshold or vvix_level >= 110.0:
            return 40.0
        if vix_level >= caution_threshold or vvix_level >= 95.0:
            return 20.0
        return 5.0

    def _volatility_bucket(self, vix_level: float) -> str:
        if vix_level < 18.0:
            return "low"
        if vix_level < 25.0:
            return "medium"
        return "high"
