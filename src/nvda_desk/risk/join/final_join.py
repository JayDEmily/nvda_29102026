"""Coordinate bounded final-risk joins."""

from __future__ import annotations

from nvda_desk.contracts.execution import ExecutionExpressionOutput
from nvda_desk.contracts.risk import FinalRiskJoinReceipt
from nvda_desk.domain.final_risk.overlay import evaluate_overlay_risk
from nvda_desk.domain.final_risk.terminal_join import apply_terminal_join


class FinalJoinService:
    """Own bounded final-join coordination."""

    def evaluate(self, expression: ExecutionExpressionOutput) -> FinalRiskJoinReceipt:
        return apply_terminal_join(
            expression=expression, overlay_result=evaluate_overlay_risk(expression)
        )
