from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True)
class CognitionRuntimeFixture:
    fixture_id: str
    market_regime_context: str
    risk_posture: str
    payload: dict[str, Any] = field(default_factory=dict)


def supportive_runtime_fixture() -> CognitionRuntimeFixture:
    return CognitionRuntimeFixture(
        fixture_id="supportive_runtime",
        market_regime_context="supportive",
        risk_posture="normal",
        payload={"options_flow": "supportive", "temporal_state": "mid_session"},
    )


def stressed_runtime_fixture() -> CognitionRuntimeFixture:
    return CognitionRuntimeFixture(
        fixture_id="stressed_runtime",
        market_regime_context="stressed",
        risk_posture="stressed",
        payload={"options_flow": "defensive", "temporal_state": "event_risk"},
    )
