"""Pure market-regime classification helpers."""

from __future__ import annotations

from nvda_desk.contracts.regime import MarketRegimeContextInput, MarketRegimeContextOutput

MARKET_REGIME_POLICY_VERSION = "market-regime.cross-asset.v1"


def classify_market_regime(context: MarketRegimeContextInput) -> MarketRegimeContextOutput:
    """Return one bounded regime classification from cross-asset inputs."""

    reasons: list[str] = []
    missing_fields = set(context.missing_fields)
    if context.nvda_return_pct is None:
        missing_fields.add("nvda_return_pct")
    if context.nq_return_pct is None:
        missing_fields.add("nq_return_pct")
    if context.vix_level is None:
        missing_fields.add("vix_level")

    score = 0.0
    if context.nvda_return_pct is not None and context.nq_return_pct is not None:
        score = abs(context.nvda_return_pct - context.nq_return_pct)
    else:
        reasons.append("cross_asset_returns_incomplete")

    if context.vix_level is None:
        reasons.append("vix_level_missing")
        regime = "unknown"
    elif context.vix_level >= 30:
        regime = "high_volatility"
        reasons.append("vix_ge_30")
    elif context.nvda_return_pct is not None and context.nq_return_pct is not None and score >= 2.0:
        regime = "divergent"
        reasons.append("dispersion_ge_2pct")
    elif context.nvda_return_pct is not None and context.nq_return_pct is not None:
        regime = "normal"
        reasons.append("bounded_cross_asset_state")
    else:
        regime = "unknown"
        reasons.append("insufficient_regime_inputs")

    for field_name in sorted(missing_fields):
        token = f"missing_{field_name}"
        if token not in reasons:
            reasons.append(token)

    return MarketRegimeContextOutput(
        regime_policy_version=MARKET_REGIME_POLICY_VERSION,
        volatility_regime=regime,
        cross_asset_pressure_score=round(score, 3),
        vix_level=context.vix_level,
        reasons=reasons,
    )
