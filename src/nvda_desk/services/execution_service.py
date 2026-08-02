"""Coordinate bounded execution-expression and lifecycle-plan creation."""

from __future__ import annotations

from nvda_desk.contracts.eligibility import PlaybookEligibilityOutput
from nvda_desk.contracts.execution import ExecutionExpressionInput
from nvda_desk.domain.execution.candidate_expression import evaluate_execution_expression
from nvda_desk.domain.execution.lifecycle_plan import build_lifecycle_plan


class ExecutionService:
    """Coordinate execution helpers without absorbing execution domain logic."""

    def evaluate(
        self,
        *,
        execution_input: ExecutionExpressionInput,
        eligibility_output: PlaybookEligibilityOutput,
        candidate_id: str | None = None,
    ) -> dict:
        expression = evaluate_execution_expression(
            execution_input=execution_input,
            eligibility_output=eligibility_output,
            candidate_id=candidate_id,
        )
        return {
            "expression": expression,
            "lifecycle_plan": build_lifecycle_plan(expression),
        }
