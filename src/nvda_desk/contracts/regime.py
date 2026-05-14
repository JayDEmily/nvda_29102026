"""Regime ingress and output contracts for the bounded runtime rebuild."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class MarketRegimeContextInput(BaseModel):
    """Typed regime input with explicit completeness state."""

    model_config = ConfigDict(extra="forbid")
    nvda_return_pct: float | None = None
    nq_return_pct: float | None = None
    vix_level: float | None = None
    missing_fields: list[str] = Field(default_factory=list)


class MarketRegimeContextOutput(BaseModel):
    """Typed regime output from the bounded regime stage."""

    model_config = ConfigDict(extra="forbid")
    volatility_regime: str = "unknown"
    cross_asset_pressure_score: float = 0.0
    vix_level: float | None = None
    reasons: list[str] = Field(default_factory=list)
