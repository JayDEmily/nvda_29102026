"""Translate prepared regime inputs into one bounded regime output."""

from __future__ import annotations

from nvda_desk.contracts.regime import MarketRegimeContextInput, MarketRegimeContextOutput
from nvda_desk.domain.regime.classification import classify_market_regime


class RegimeContextService:
    """Coordinate the bounded regime-context evaluation."""

    def evaluate(self, context: MarketRegimeContextInput) -> MarketRegimeContextOutput:
        return classify_market_regime(context)
