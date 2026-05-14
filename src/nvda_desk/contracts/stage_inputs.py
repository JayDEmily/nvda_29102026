"""Typed ingress bundle admitted at the preparation-to-serial seam."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from nvda_desk.contracts.options_flow import OptionsFlowContextInput
from nvda_desk.contracts.regime import MarketRegimeContextInput
from nvda_desk.contracts.temporal import TemporalContextInput


class StageInputBundle(BaseModel):
    """Typed stage-input bundle emitted by cognition ingress."""

    model_config = ConfigDict(extra="forbid")
    temporal: TemporalContextInput
    regime: MarketRegimeContextInput
    options_flow: OptionsFlowContextInput

    def as_mapping(self) -> dict[str, object]:
        """Return a stage-name keyed mapping over the typed input carriers."""

        return {
            "temporal": self.temporal,
            "regime": self.regime,
            "options_flow": self.options_flow,
        }
