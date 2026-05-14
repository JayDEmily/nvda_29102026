"""Coordinate bounded final-risk overlay and terminal-join evaluation."""

from __future__ import annotations

from nvda_desk.contracts.execution import ExecutionExpressionOutput
from nvda_desk.contracts.risk import FinalRiskJoinReceipt
from nvda_desk.domain.final_risk.overlay import evaluate_overlay_risk
from nvda_desk.domain.final_risk.terminal_join import apply_terminal_join


class FinalRiskService:
    """Coordinate bounded final-risk helpers without absorbing domain logic."""

    def evaluate(self, expression: ExecutionExpressionOutput) -> FinalRiskJoinReceipt:
        overlay_result = evaluate_overlay_risk(expression)
        return apply_terminal_join(expression=expression, overlay_result=overlay_result)
