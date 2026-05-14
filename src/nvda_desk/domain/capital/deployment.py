"""Pure capital deployment decision helpers."""

from __future__ import annotations

from nvda_desk.capital.authority import evaluate_capital_deployment
from nvda_desk.contracts.capital import CapitalDeploymentAuthorityInput


def compute_deployment_plan(
    context: CapitalDeploymentAuthorityInput,
    *,
    receipt_id: str | None = None,
) -> dict:
    """Return one serialisable downstream capital deployment plan."""
    decision = evaluate_capital_deployment(context, receipt_id=receipt_id)
    return decision.model_dump(mode="json")
