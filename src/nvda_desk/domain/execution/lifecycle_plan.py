"""Pure lifecycle-plan helpers."""

from __future__ import annotations

from nvda_desk.contracts.execution import ExecutionExpressionOutput


def build_lifecycle_plan(expression: ExecutionExpressionOutput) -> dict:
    """Return one bounded lifecycle plan from the execution expression."""
    if expression.lead_playbook_id is None:
        return {"action": "stand_down", "steps": []}
    return {"action": "candidate_ready", "steps": ["prepare_candidate_review"]}
