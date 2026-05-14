from __future__ import annotations

from datetime import date, datetime
from enum import StrEnum

from pydantic import BaseModel, Field

from nvda_desk.domain.session_clock import SessionClockPhase
from nvda_desk.schemas.module import ModuleClass, ModuleDescriptor
from nvda_desk.schemas.options import OptionType
from nvda_desk.schemas.risk import RiskAction


class LadderOverallDecision(StrEnum):
    ACCEPT = "accept"
    ADJUST = "adjust"
    REJECT = "reject"


class LadderRungDecision(StrEnum):
    KEEP = "keep"
    ADJUST = "adjust"
    DROP = "drop"


class LadderConfidence(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class LadderRungInput(BaseModel):
    price: float = Field(gt=0)
    size_units: float = Field(gt=0)
    strike_pressure_score: float = Field(ge=0, le=1)
    fill_plausibility_score: float = Field(ge=0, le=1)


class StrategicLadderValidatorInput(BaseModel):
    descriptor: ModuleDescriptor = Field(
        default_factory=lambda: ModuleDescriptor(
            module_id="slv-v1",
            name="Strategic Ladder Validator",
            module_class=ModuleClass.EXECUTION,
            thesis="Validate a proposed entry ladder before it reaches runtime.",
        )
    )
    symbol: str = Field(default="NVDA", min_length=1)
    spot_price: float = Field(gt=0)
    distance_to_vwap_pct: float = Field(ge=-100, le=100)
    iv_hv_divergence_pct: float = Field(ge=-100, le=100)
    session_phase: SessionClockPhase
    rungs: list[LadderRungInput] = Field(min_length=1)


class LadderRungResult(BaseModel):
    price: float
    size_units: float
    decision: LadderRungDecision
    reasons: list[str]
    suggested_price: float | None = None


class StrategicLadderValidatorOutput(BaseModel):
    ladder_validity_score: float = Field(ge=0, le=1)
    overall_decision: LadderOverallDecision
    rung_decisions: list[LadderRungResult]
    reasons: list[str]
    confidence: LadderConfidence


class LadderRungMarketInput(BaseModel):
    price: float = Field(gt=0)
    size_units: float = Field(gt=0)


class LadderRungMarketContext(BaseModel):
    matched_strike: float
    strike_pressure_score: float = Field(ge=0, le=1)
    fill_plausibility_score: float = Field(ge=0, le=1)
    proximity_pct: float = Field(ge=0)
    spread_pct_of_mid: float | None = Field(default=None, ge=0)
    open_interest: int | None = Field(default=None, ge=0)
    volume: int | None = Field(default=None, ge=0)
    confidence: str


class LadderRungMarketResult(BaseModel):
    price: float
    size_units: float
    decision: LadderRungDecision
    reasons: list[str]
    market_context: LadderRungMarketContext | None = None
    suggested_price: float | None = None


class StrikeZoneSignal(BaseModel):
    strike: float
    normalized_pressure: float = Field(ge=0, le=1)
    fill_plausibility_score: float = Field(ge=0, le=1)
    spread_pct_of_mid: float | None = Field(default=None, ge=0)
    open_interest: int | None = Field(default=None, ge=0)
    volume: int | None = Field(default=None, ge=0)
    confidence: str


class SupervisoryOverlay(BaseModel):
    action: RiskAction
    reasons: list[str]
    confidence_scalar: float = Field(ge=0, le=1)
    vix_level: float = Field(ge=0, le=200)
    vvix_level: float = Field(ge=0, le=500)


class StrategicLadderValidatorMarketInput(BaseModel):
    descriptor: ModuleDescriptor = Field(
        default_factory=lambda: ModuleDescriptor(
            module_id="slv-v2-market",
            name="Strategic Ladder Validator",
            module_class=ModuleClass.EXECUTION,
            thesis="Validate a proposed NVDA ladder against persisted option-surface context.",
        )
    )
    symbol: str = Field(default="NVDA", min_length=1)
    as_of_date: date
    expiry: date | None = None
    option_type: OptionType = OptionType.PUT
    spot_price: float = Field(gt=0)
    distance_to_vwap_pct: float = Field(ge=-100, le=100)
    iv_hv_divergence_pct: float = Field(ge=-100, le=100)
    session_phase: SessionClockPhase
    entry_gate_score_floor: float = Field(default=0.65, ge=0, le=1)
    zone_score_threshold: float = Field(default=0.50, ge=0, le=1)
    distance_to_vwap_soft_limit_pct: float = Field(default=2.5, gt=0, le=100)
    rungs: list[LadderRungMarketInput] = Field(min_length=1)


class StrategicLadderValidatorMarketOutput(BaseModel):
    ladder_validity_score: float = Field(ge=0, le=1)
    overall_decision: LadderOverallDecision
    rung_decisions: list[LadderRungMarketResult]
    reasons: list[str]
    confidence: LadderConfidence
    as_of_date: date
    expiry_used: date | None = None
    option_type: OptionType
    snapshots_considered: int = Field(ge=0)
    strike_zone_signals: list[StrikeZoneSignal]
    supervisory_overlay: SupervisoryOverlay | None = None


class StrategicLadderReplayInput(BaseModel):
    descriptor: ModuleDescriptor = Field(
        default_factory=lambda: ModuleDescriptor(
            module_id="slv-v3-replay",
            name="Strategic Ladder Validator",
            module_class=ModuleClass.EXECUTION,
            thesis="Replay a proposed NVDA ladder against persisted bars and option-surface context.",
        )
    )
    symbol: str = Field(default="NVDA", min_length=1)
    as_of_date: date
    expiry: date | None = None
    option_type: OptionType = OptionType.PUT
    entry_ts: datetime
    spot_price: float = Field(gt=0)
    distance_to_vwap_pct: float = Field(ge=-100, le=100)
    iv_hv_divergence_pct: float = Field(ge=-100, le=100)
    session_phase: SessionClockPhase
    lookahead_minutes: int = Field(default=45, ge=1, le=240)
    rungs: list[LadderRungMarketInput] = Field(min_length=1)
    gross_exposure_pct: float = Field(default=0.0, ge=0, le=100)
    risk_budget_remaining_pct: float = Field(default=100.0, ge=0, le=100)
    conflict_tags: list[str] = Field(default_factory=list)
    entry_gate_score_floor: float = Field(default=0.65, ge=0, le=1)
    zone_score_threshold: float = Field(default=0.50, ge=0, le=1)
    distance_to_vwap_soft_limit_pct: float = Field(default=2.5, gt=0, le=100)
    risk_vix_caution_threshold: float = Field(default=24.0, gt=0, le=200)
    risk_vix_hot_threshold: float = Field(default=32.0, gt=0, le=200)


class LadderReplayRungOutcome(BaseModel):
    price: float
    size_units: float
    filled: bool
    fill_ts: datetime | None = None
    phase_at_fill: SessionClockPhase | None = None
    max_favorable_excursion_pct: float | None = None
    max_adverse_excursion_pct: float | None = None
    closing_return_pct: float | None = None
    outcome_label: str


class StrategicLadderReplayOutput(BaseModel):
    entry_ts: datetime
    entry_phase: SessionClockPhase
    lookahead_minutes: int = Field(ge=1)
    ladder_validity_score: float = Field(ge=0, le=1)
    replay_score: float = Field(ge=0, le=1)
    overall_decision: LadderOverallDecision
    confidence: LadderConfidence
    reasons: list[str]
    market_validation: StrategicLadderValidatorMarketOutput
    supervisory_overlay: SupervisoryOverlay
    rung_outcomes: list[LadderReplayRungOutcome]
    evaluated_bar_count: int = Field(ge=0)
