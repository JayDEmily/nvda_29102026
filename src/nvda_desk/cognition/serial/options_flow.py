"""Evaluate bounded options-flow context."""

from __future__ import annotations

from nvda_desk.contracts.options_flow import OptionsFlowContextInput, OptionsFlowContextOutput
from nvda_desk.domain.options_flow.surface_state import classify_surface_state


def evaluate_options_flow_context(context: OptionsFlowContextInput) -> OptionsFlowContextOutput:
    """Return one bounded options-flow evaluation."""
    return classify_surface_state(context)
