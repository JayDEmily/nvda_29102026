"""Pure overlay-risk evaluation helpers."""

from __future__ import annotations

from nvda_desk.contracts.execution import ExecutionExpressionOutput


def evaluate_overlay_risk(expression: ExecutionExpressionOutput) -> dict:
    """Return one bounded overlay-risk surface from execution output."""
    lead_playbook_id = expression.lead_playbook_id
    if lead_playbook_id is None:
        return {"action": "stand_down", "reasons": ["no_lead_playbook"]}
    return {"action": "continue", "reasons": ["lead_playbook_present"]}
