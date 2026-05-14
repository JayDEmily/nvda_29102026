"""Translate prepared options-flow inputs into one bounded options-flow output."""

from __future__ import annotations

from nvda_desk.contracts.options_flow import OptionsFlowContextInput, OptionsFlowContextOutput
from nvda_desk.domain.options_flow.surface_state import classify_surface_state


class OptionsFlowContextService:
    """Coordinate the bounded options-flow evaluation."""

    def evaluate(self, context: OptionsFlowContextInput) -> OptionsFlowContextOutput:
        return classify_surface_state(context)
