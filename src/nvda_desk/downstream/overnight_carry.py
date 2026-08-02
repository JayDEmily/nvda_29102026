from __future__ import annotations

from copy import deepcopy
from typing import Any, Literal, Mapping

from pydantic import BaseModel, ConfigDict, Field, model_validator

from nvda_desk.contracts.exit_close import ExitClosePolicyDecision

CarryAction = Literal["hold", "trim", "close"]
CarryRecommendation = Literal["hold", "trim", "close"]
OVERNIGHT_CARRY_POLICY_VERSION = "overnight-carry.market.v1"


class CarryHandoffPacket(BaseModel):
    model_config = ConfigDict(extra="forbid")

    handoff_id: str
    decision_id: str
    position_id: str
    horizon: str
    allowed_actions: tuple[CarryAction, ...]
    next_session_open_utc: str | None = None
    source_exit_state: str
    execution_allowed: bool = False

    @model_validator(mode="after")
    def _validate_reporting_only(self) -> "CarryHandoffPacket":
        if self.execution_allowed:
            raise ValueError("carry handoff must not permit execution")
        return self


class OvernightCarryEvaluation(BaseModel):
    model_config = ConfigDict(extra="forbid")

    evaluation_id: str
    policy_version: str = Field(min_length=1)
    symbol: str
    recommendation: CarryRecommendation
    handoff_id: str
    latest_close: float | None = None
    session_vwap: float | None = None
    close_distance_to_vwap_pct: float | None = None
    scalar_context: dict[str, float] = Field(default_factory=dict)
    reasons: tuple[str, ...] = Field(default_factory=tuple)
    execution_allowed: bool = False


class OvernightCarryReplayResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    replay_id: str
    evaluation_id: str
    next_session_source_id: str = Field(min_length=1)
    recommendation: CarryRecommendation
    path_summary: dict[str, float | None]
    comparator_summary: str
    runtime_mutated: bool = False


class CarryHandoffService:
    def build_carry_handoff(
        self,
        *,
        decision: ExitClosePolicyDecision,
        horizon: str,
        lifecycle_ceiling: CarryAction = "close",
        next_session_open_utc: str | None = None,
        configured_next_session_open_utc: str | None = None,
    ) -> CarryHandoffPacket:
        allowed = _actions_for_decision(decision)
        allowed = _limit_actions(allowed, lifecycle_ceiling)
        return CarryHandoffPacket(
            handoff_id=f"{decision.decision_id}::carry::{horizon}",
            decision_id=decision.decision_id,
            position_id=decision.position_id,
            horizon=horizon,
            allowed_actions=allowed,
            next_session_open_utc=next_session_open_utc or configured_next_session_open_utc,
            source_exit_state=decision.exit_state,
        )


class OvernightCarryMarketService:
    def evaluate_from_market(
        self,
        *,
        evaluation_id: str,
        market_state: Mapping[str, Any],
        handoff: CarryHandoffPacket,
    ) -> OvernightCarryEvaluation:
        state = deepcopy(dict(market_state))
        symbol = str(state.get("symbol") or "NVDA").strip().upper()
        latest_close = _optional_float(state.get("latest_close"))
        session_vwap = _optional_float(state.get("session_vwap") or state.get("vwap"))
        distance = _distance_to_vwap_pct(latest_close, session_vwap)
        scalar_context = {
            key: value
            for key in ("vix_close", "vvix_close")
            if (value := _optional_float(state.get(key))) is not None
        }
        raw_action: CarryAction = "hold"
        reasons: list[str] = []
        if distance is not None and distance >= 4.0:
            raw_action = "trim"
            reasons.append("close_above_vwap_threshold")
        if scalar_context.get("vix_close", 0.0) >= 30.0:
            raw_action = "close"
            reasons.append("elevated_vix")
        recommendation = _cap_action(raw_action, handoff.allowed_actions)
        if recommendation != raw_action:
            reasons.append("capped_by_close_state_handoff")
        return OvernightCarryEvaluation(
            evaluation_id=evaluation_id,
            policy_version=OVERNIGHT_CARRY_POLICY_VERSION,
            symbol=symbol,
            recommendation=recommendation,
            handoff_id=handoff.handoff_id,
            latest_close=latest_close,
            session_vwap=session_vwap,
            close_distance_to_vwap_pct=distance,
            scalar_context=scalar_context,
            reasons=tuple(reasons),
        )


class OvernightCarryReplayService:
    def __init__(self) -> None:
        self._evaluations: dict[str, OvernightCarryEvaluation] = {}

    def record_evaluation(self, evaluation: OvernightCarryEvaluation) -> OvernightCarryEvaluation:
        if evaluation.evaluation_id in self._evaluations:
            raise ValueError(f"duplicate evaluation_id: {evaluation.evaluation_id}")
        self._evaluations[evaluation.evaluation_id] = evaluation.model_copy(deep=True)
        return evaluation.model_copy(deep=True)

    def replay_evaluation(
        self,
        *,
        replay_id: str,
        evaluation: OvernightCarryEvaluation,
        next_session_source_id: str,
        next_session_reference: Mapping[str, Any],
    ) -> OvernightCarryReplayResult:
        governed_next_session_source_id = next_session_source_id.strip()
        if not governed_next_session_source_id:
            raise ValueError("next_session_source_id_required")
        latest_close = evaluation.latest_close
        open_price = _optional_float(next_session_reference.get("open_price"))
        close_price = _optional_float(next_session_reference.get("close_price"))
        path_summary = {
            "open_gap_pct": _pct_change(latest_close, open_price),
            "close_to_close_pct": _pct_change(latest_close, close_price),
        }
        return OvernightCarryReplayResult(
            replay_id=replay_id,
            evaluation_id=evaluation.evaluation_id,
            next_session_source_id=governed_next_session_source_id,
            recommendation=evaluation.recommendation,
            path_summary=path_summary,
            comparator_summary=f"{evaluation.recommendation}:{path_summary['open_gap_pct']}:{path_summary['close_to_close_pct']}",
        )

    def list_evaluations(self) -> tuple[OvernightCarryEvaluation, ...]:
        return tuple(evaluation.model_copy(deep=True) for evaluation in self._evaluations.values())


def _actions_for_decision(decision: ExitClosePolicyDecision) -> tuple[CarryAction, ...]:
    if decision.exit_state == "blocked":
        return ("hold",)
    if decision.requested_action == "hold":
        return ("hold",)
    if decision.requested_action == "trim":
        return ("hold", "trim")
    return ("hold", "trim", "close")


def _limit_actions(
    actions: tuple[CarryAction, ...], ceiling: CarryAction
) -> tuple[CarryAction, ...]:
    order = {"hold": 0, "trim": 1, "close": 2}
    max_rank = order[ceiling]
    return tuple(action for action in actions if order[action] <= max_rank)


def _cap_action(action: CarryAction, allowed: tuple[CarryAction, ...]) -> CarryAction:
    if action in allowed:
        return action
    order = {"hold": 0, "trim": 1, "close": 2}
    return max(allowed, key=lambda item: order[item])


def _optional_float(value: Any) -> float | None:
    if value is None or isinstance(value, bool):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _distance_to_vwap_pct(close: float | None, vwap: float | None) -> float | None:
    if close is None or vwap in (None, 0):
        return None
    return round(((close - vwap) / vwap) * 100.0, 4)


def _pct_change(base: float | None, value: float | None) -> float | None:
    if base in (None, 0) or value is None:
        return None
    return round(((value - base) / base) * 100.0, 4)
