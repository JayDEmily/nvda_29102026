from __future__ import annotations

from typing import Any, Mapping

from pydantic import BaseModel, ConfigDict, Field


class StrategicLadderReplayContext(BaseModel):
    model_config = ConfigDict(extra="forbid")

    context_id: str
    market_state: dict[str, Any]
    overlay_state: dict[str, Any] = Field(default_factory=dict)
    percent_change: float | None = None
    distance_to_vwap_pct: float | None = None


class StrategicLadderReplayResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    run_id: str
    contexts: tuple[StrategicLadderReplayContext, ...]
    average_percent_change: float | None = None
    runtime_authority_mutated: bool = False


class StrategicLadderWalkForwardOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    output_id: str
    run_count: int = Field(ge=0)
    context_count: int = Field(ge=0)
    runtime_authority_mutated: bool = False


class StrategicLadderReplayService:
    def build_replay_context(
        self,
        *,
        context_id: str,
        market_state: Mapping[str, Any],
        overlay_state: Mapping[str, Any] | None = None,
    ) -> StrategicLadderReplayContext:
        state = dict(market_state)
        previous_close = _optional_float(state.get("previous_close"))
        latest_close = _optional_float(state.get("latest_close"))
        vwap = _optional_float(state.get("vwap") or state.get("session_vwap"))
        return StrategicLadderReplayContext(
            context_id=context_id,
            market_state=state,
            overlay_state=dict(overlay_state or {}),
            percent_change=_pct_change(previous_close, latest_close),
            distance_to_vwap_pct=_pct_distance(latest_close, vwap),
        )

    def run_replay(
        self, *, run_id: str, contexts: tuple[StrategicLadderReplayContext, ...]
    ) -> StrategicLadderReplayResult:
        values = [
            context.percent_change for context in contexts if context.percent_change is not None
        ]
        average = round(sum(values) / len(values), 4) if values else None
        return StrategicLadderReplayResult(
            run_id=run_id,
            contexts=tuple(context.model_copy(deep=True) for context in contexts),
            average_percent_change=average,
        )

    def build_walk_forward_output(
        self,
        *,
        output_id: str,
        replay_results: tuple[StrategicLadderReplayResult, ...],
    ) -> StrategicLadderWalkForwardOutput:
        return StrategicLadderWalkForwardOutput(
            output_id=output_id,
            run_count=len(replay_results),
            context_count=sum(len(result.contexts) for result in replay_results),
        )


def _optional_float(value: Any) -> float | None:
    if value is None or isinstance(value, bool):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _pct_change(base: float | None, value: float | None) -> float | None:
    if base in (None, 0) or value is None:
        return None
    return round(((value - base) / base) * 100.0, 4)


def _pct_distance(value: float | None, base: float | None) -> float | None:
    if base in (None, 0) or value is None:
        return None
    return round(((value - base) / base) * 100.0, 4)
