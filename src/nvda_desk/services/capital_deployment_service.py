"""Coordinate bounded capital deployment authority evaluation."""

from __future__ import annotations

from nvda_desk.capital.authority import (
    build_capital_deployment_receipt,
    evaluate_capital_deployment,
)
from nvda_desk.contracts.capital import (
    CapitalDeploymentAuthorityInput,
    CapitalDeploymentDecision,
    CapitalDeploymentReceipt,
)


class CapitalDeploymentService:
    """Coordinate capital deployment without absorbing authority logic."""

    def evaluate(
        self,
        context: CapitalDeploymentAuthorityInput,
        *,
        receipt_id: str | None = None,
    ) -> CapitalDeploymentDecision:
        """Return one capital deployment decision."""
        return evaluate_capital_deployment(context, receipt_id=receipt_id)

    def evaluate_with_receipt(
        self,
        context: CapitalDeploymentAuthorityInput,
        *,
        receipt_id: str,
    ) -> CapitalDeploymentReceipt:
        """Return one decision receipt without opening placement mechanics."""
        decision = self.evaluate(context, receipt_id=receipt_id)
        return build_capital_deployment_receipt(
            receipt_id=receipt_id,
            context=context,
            decision=decision,
        )
