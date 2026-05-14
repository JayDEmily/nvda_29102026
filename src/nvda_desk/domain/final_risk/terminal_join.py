"""Pure terminal-risk join helpers."""

from __future__ import annotations

from nvda_desk.contracts.execution import ExecutionExpressionOutput
from nvda_desk.contracts.risk import FinalRiskJoinReceipt


def apply_terminal_join(
    *, expression: ExecutionExpressionOutput, overlay_result: dict
) -> FinalRiskJoinReceipt:
    """Return one bounded final-join receipt from execution output and overlay result."""
    reasons = list(overlay_result.get("reasons", []))
    if overlay_result.get("action") == "stand_down":
        return FinalRiskJoinReceipt(action="stand_down", confidence_scalar=0.0, reasons=reasons)
    confidence = 1.0 if expression.lead_playbook_id else 0.0
    return FinalRiskJoinReceipt(action="proceed", confidence_scalar=confidence, reasons=reasons)
