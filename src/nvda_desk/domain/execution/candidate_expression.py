"""Pure execution-expression helpers."""

from __future__ import annotations

from nvda_desk.contracts.eligibility import PlaybookEligibilityOutput
from nvda_desk.contracts.execution import ExecutionExpressionInput, ExecutionExpressionOutput


def evaluate_execution_expression(
    *,
    execution_input: ExecutionExpressionInput,
    eligibility_output: PlaybookEligibilityOutput,
    candidate_id: str | None = None,
) -> ExecutionExpressionOutput:
    """Return one bounded execution expression from eligibility and prior stage inputs."""
    lead_playbook_id = (
        eligibility_output.active_family_ids[0] if eligibility_output.active_family_ids else None
    )
    if lead_playbook_id is None and candidate_id is not None:
        raise ValueError("candidate_id cannot be supplied when no eligible playbook is selected")
    if lead_playbook_id is not None and not candidate_id:
        raise ValueError("candidate_id must be supplied for a formed execution expression")
    return ExecutionExpressionOutput(
        candidate_id=candidate_id,
        lead_playbook_id=lead_playbook_id,
        scaling_plan=["enter" if lead_playbook_id else "stand_down"],
        final_risk_join={"ready": lead_playbook_id is not None},
        active_playbook_ids=list(eligibility_output.active_family_ids),
    )
