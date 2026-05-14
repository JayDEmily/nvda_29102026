from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field

from nvda_desk.domain.session_clock import SessionClockPhase
from nvda_desk.schemas.risk import RiskAction
from nvda_desk.schemas.slv import StrategicLadderReplayInput

EvalVerdict = Literal["pass", "fail", "review"]
ExperimentType = Literal["walk_forward", "fragility", "batch_ranking"]
FailureSeverity = Literal["low", "medium", "high"]
VolatilityBucket = Literal["low", "medium", "high"]


class EvaluationRunPayload(BaseModel):
    evaluation_id: int
    created_at: datetime
    symbol: str
    module_id: str = Field(min_length=1)
    module_name: str = Field(min_length=1)
    module_class: str = Field(min_length=1)
    verdict: EvalVerdict
    score: float = Field(ge=0, le=1)
    requested_at: datetime
    input_payload: dict[str, Any]
    output_payload: dict[str, Any]


class EvaluationRunListResponse(BaseModel):
    evaluations: list[EvaluationRunPayload]


class FailureModeSummary(BaseModel):
    code: str = Field(min_length=1)
    occurrences: int = Field(ge=1)
    share_of_evaluations: float = Field(ge=0, le=1)
    severity: FailureSeverity
    evidence: list[str] = Field(default_factory=list)


class WalkForwardWindowSummary(BaseModel):
    anchor_ts: datetime
    entry_phase: SessionClockPhase
    volatility_bucket: VolatilityBucket
    risk_action: RiskAction
    evaluation_count: int = Field(default=1, ge=1)
    pass_rate: float = Field(ge=0, le=1)
    average_score: float = Field(ge=0, le=1)
    filled_rungs: int = Field(ge=0)
    total_rungs: int = Field(ge=0)


class RegimeBucketSummary(BaseModel):
    bucket: str = Field(min_length=1)
    evaluation_count: int = Field(ge=1)
    pass_rate: float = Field(ge=0, le=1)
    average_score: float = Field(ge=0, le=1)


class StrategicLadderWalkForwardInput(BaseModel):
    base_payload: StrategicLadderReplayInput
    anchor_timestamps: list[datetime] = Field(min_length=3, max_length=24)
    config_name: str = Field(default="default", min_length=1)
    strategy_variant_name: str | None = Field(default=None, min_length=1)
    coefficient_group_name: str | None = Field(default=None, min_length=1)


class StrategicLadderWalkForwardOutput(BaseModel):
    experiment_id: int | None = None
    module_id: str = Field(min_length=1)
    config_name: str = Field(min_length=1)
    evaluation_count: int = Field(ge=1)
    average_forward_score: float = Field(ge=0, le=1)
    pass_rate: float = Field(ge=0, le=1)
    windows: list[WalkForwardWindowSummary]
    phase_buckets: list[RegimeBucketSummary]
    volatility_buckets: list[RegimeBucketSummary]
    risk_action_buckets: list[RegimeBucketSummary]
    failure_modes: list[FailureModeSummary]


class FragilityScenarioInput(BaseModel):
    name: str = Field(min_length=1)
    entry_offset_minutes: int = Field(default=0, ge=-30, le=30)
    rung_price_shift_pct: float = Field(default=0.0, ge=-5.0, le=5.0)
    rung_size_scale: float = Field(default=1.0, gt=0, le=3.0)
    vwap_offset_pct: float = Field(default=0.0, ge=-5.0, le=5.0)
    iv_hv_divergence_offset_pct: float = Field(default=0.0, ge=-50.0, le=50.0)


class FragilityScenarioResult(BaseModel):
    name: str
    replay_score: float = Field(ge=0, le=1)
    score_drop: float = Field(ge=0, le=1)
    risk_action: RiskAction
    overall_decision: str
    filled_rungs: int = Field(ge=0)
    total_rungs: int = Field(ge=0)


class StrategicLadderFragilityInput(BaseModel):
    base_payload: StrategicLadderReplayInput
    scenarios: list[FragilityScenarioInput] = Field(default_factory=list, max_length=12)
    config_name: str = Field(default="default", min_length=1)
    strategy_variant_name: str | None = Field(default=None, min_length=1)
    coefficient_group_name: str | None = Field(default=None, min_length=1)


class StrategicLadderFragilityOutput(BaseModel):
    experiment_id: int | None = None
    module_id: str = Field(min_length=1)
    config_name: str = Field(min_length=1)
    baseline_replay_score: float = Field(ge=0, le=1)
    fragility_score: float = Field(ge=0, le=1)
    worst_case_drop: float = Field(ge=0, le=1)
    scenario_results: list[FragilityScenarioResult]
    failure_modes: list[FailureModeSummary]


class BatchVariantConfig(BaseModel):
    name: str = Field(min_length=1)
    entry_offset_minutes: int = Field(default=0, ge=-30, le=30)
    rung_price_shift_pct: float = Field(default=0.0, ge=-5.0, le=5.0)
    rung_size_scale: float = Field(default=1.0, gt=0, le=3.0)
    vwap_offset_pct: float = Field(default=0.0, ge=-5.0, le=5.0)
    iv_hv_divergence_offset_pct: float = Field(default=0.0, ge=-50.0, le=50.0)
    lookahead_minutes: int | None = Field(default=None, ge=1, le=240)
    strategy_variant_name: str | None = Field(default=None, min_length=1)
    coefficient_group_name: str | None = Field(default=None, min_length=1)


class StrategicLadderBatchRankingInput(BaseModel):
    base_payload: StrategicLadderReplayInput
    anchor_timestamps: list[datetime] = Field(min_length=3, max_length=24)
    variants: list[BatchVariantConfig] = Field(default_factory=list, max_length=12)
    batch_name: str = Field(default="default-batch", min_length=1)
    variant_names: list[str] = Field(default_factory=list, max_length=12)


class RankedVariantSummary(BaseModel):
    name: str = Field(min_length=1)
    ranking_score: float = Field(ge=0, le=1)
    average_forward_score: float = Field(ge=0, le=1)
    pass_rate: float = Field(ge=0, le=1)
    fragility_score: float = Field(ge=0, le=1)
    failure_modes: list[FailureModeSummary]


class StrategicLadderBatchRankingOutput(BaseModel):
    experiment_id: int | None = None
    module_id: str = Field(min_length=1)
    batch_name: str = Field(min_length=1)
    ranked_variants: list[RankedVariantSummary]


class ExperimentRunPayload(BaseModel):
    experiment_id: int
    created_at: datetime
    symbol: str
    module_id: str = Field(min_length=1)
    experiment_type: ExperimentType
    config_name: str = Field(min_length=1)
    requested_at: datetime
    ranking_score: float | None = Field(default=None, ge=0, le=1)
    input_payload: dict[str, Any]
    output_payload: dict[str, Any]


class ExperimentRunListResponse(BaseModel):
    experiments: list[ExperimentRunPayload]
