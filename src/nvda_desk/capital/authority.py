"""Bounded downstream capital deployment authority helpers."""

from __future__ import annotations

from nvda_desk.contracts.capital import (
    CapitalDeploymentAuthorityAction,
    CapitalDeploymentAuthorityInput,
    CapitalDeploymentDecision,
    CapitalDeploymentInputTrace,
    CapitalDeploymentReceipt,
)

_CONSUMED_INPUTS = (
    "serial_candidate",
    "downstream_pre_deployment_result",
    "parallel_risk_envelope",
    "final_risk_product",
    "capital_state",
    "bounded_deployment_policy",
    "coefficient_modifier_authority",
    "temporal_context",
)


class CapitalDeploymentAuthorityService:
    """Own bounded downstream capital-deployment authority evaluation."""

    def evaluate(
        self,
        context: CapitalDeploymentAuthorityInput,
        *,
        receipt_id: str | None = None,
    ) -> CapitalDeploymentDecision:
        """Return one bounded downstream capital deployment decision."""
        return evaluate_capital_deployment(context, receipt_id=receipt_id)

    def evaluate_with_receipt(
        self,
        context: CapitalDeploymentAuthorityInput,
        *,
        receipt_id: str,
    ) -> CapitalDeploymentReceipt:
        """Return one receipt tying the decision to its consumed inputs."""
        decision = self.evaluate(context, receipt_id=receipt_id)
        return build_capital_deployment_receipt(
            receipt_id=receipt_id,
            context=context,
            decision=decision,
        )


def _bounded_deployable_pct(context: CapitalDeploymentAuthorityInput) -> float:
    """Return the deployment percentage allowed by downstream risk and policy bounds."""
    return min(context.requested_deployable_pct, context.max_deployable_pct)


def _authorised_notional(context: CapitalDeploymentAuthorityInput, deployable_pct: float) -> float:
    """Return authorised notional from explicit capital state and bounded percentage."""
    return round(context.available_capital_usd * (deployable_pct / 100.0), 2)


def _input_trace(context: CapitalDeploymentAuthorityInput) -> CapitalDeploymentInputTrace:
    """Return the explicit input trace consumed by capital deployment authority."""
    return CapitalDeploymentInputTrace(
        serial_candidate_id=context.serial_candidate_id,
        downstream_pre_deployment_receipt_id=context.downstream_pre_deployment_receipt_id,
        parallel_risk_packet_id=context.parallel_risk_packet_id,
        final_risk_receipt_id=context.final_risk_receipt_id,
        capital_state_snapshot_id=context.capital_state_snapshot_id,
        bounded_policy_id=context.bounded_policy_id,
        consumed_inputs=list(_CONSUMED_INPUTS),
    )


def _decision(
    context: CapitalDeploymentAuthorityInput,
    *,
    action: CapitalDeploymentAuthorityAction,
    deployable_pct: float = 0.0,
    notional_usd: float = 0.0,
    rationale: list[str],
    receipt_id: str | None = None,
) -> CapitalDeploymentDecision:
    """Return an auditable decision carrying the closed Sequence 9 action vocabulary."""
    return CapitalDeploymentDecision(
        action=action,
        authorised_deployable_pct=deployable_pct,
        authorised_notional_usd=notional_usd,
        consumed_inputs=list(_CONSUMED_INPUTS),
        rationale=rationale,
        input_trace=_input_trace(context),
        capital_deployment_receipt_id=receipt_id,
    )


def evaluate_capital_deployment(
    context: CapitalDeploymentAuthorityInput,
    *,
    receipt_id: str | None = None,
) -> CapitalDeploymentDecision:
    """Return one bounded downstream capital deployment decision.

    Precedence is deterministic: downstream pre-deployment blocks dominate,
    parallel/final risk hard blocks dominate, serial ineligibility produces
    no-trade, risk or coefficient compression reduces deployment, temporal
    elevated event risk reduces deployment, and only a clean bounded context
    continues. Serial confidence is deliberately not used for sizing.
    """
    if not context.downstream_pre_deployment_allowed:
        return _decision(
            context,
            action=CapitalDeploymentAuthorityAction.BLOCK,
            rationale=["downstream_pre_deployment_blocked_candidate"],
            receipt_id=receipt_id,
        )

    if (
        context.final_risk_action != "proceed"
        or context.parallel_risk_envelope_state == "block"
        or bool(context.parallel_risk_hard_blocks)
    ):
        return _decision(
            context,
            action=CapitalDeploymentAuthorityAction.BLOCK,
            rationale=["parallel_or_final_risk_block_dominates"],
            receipt_id=receipt_id,
        )

    if not context.serial_candidate_eligible:
        return _decision(
            context,
            action=CapitalDeploymentAuthorityAction.NO_TRADE,
            rationale=["serial_candidate_not_eligible"],
            receipt_id=receipt_id,
        )

    deployable_pct = _bounded_deployable_pct(context)
    authorised = _authorised_notional(context, deployable_pct)

    if deployable_pct <= 0.0 or authorised <= 0.0:
        return _decision(
            context,
            action=CapitalDeploymentAuthorityAction.NO_TRADE,
            rationale=["no_positive_downstream_deployment_authorised"],
            receipt_id=receipt_id,
        )

    if deployable_pct < context.requested_deployable_pct:
        return _decision(
            context,
            action=CapitalDeploymentAuthorityAction.REDUCE,
            deployable_pct=deployable_pct,
            notional_usd=authorised,
            rationale=["parallel_risk_envelope_reduced_requested_deployment"],
            receipt_id=receipt_id,
        )

    if deployable_pct < context.coefficient_min_deployable_floor_pct:
        return _decision(
            context,
            action=CapitalDeploymentAuthorityAction.REDUCE,
            deployable_pct=deployable_pct,
            notional_usd=authorised,
            rationale=["coefficient_floor_not_satisfied"],
            receipt_id=receipt_id,
        )

    if context.parallel_risk_caution_flags or context.parallel_risk_envelope_state in {
        "tight",
        "caution",
    }:
        return _decision(
            context,
            action=CapitalDeploymentAuthorityAction.REDUCE,
            deployable_pct=deployable_pct,
            notional_usd=authorised,
            rationale=["parallel_risk_caution_requires_reduction"],
            receipt_id=receipt_id,
        )

    if context.temporal_event_window_active and context.temporal_event_risk == "elevated":
        return _decision(
            context,
            action=CapitalDeploymentAuthorityAction.REDUCE,
            deployable_pct=deployable_pct,
            notional_usd=authorised,
            rationale=["temporal_event_window_elevated_risk"],
            receipt_id=receipt_id,
        )

    return _decision(
        context,
        action=CapitalDeploymentAuthorityAction.CONTINUE,
        deployable_pct=deployable_pct,
        notional_usd=authorised,
        rationale=["serial_parallel_coefficient_and_temporal_inputs_allow_continuation"],
        receipt_id=receipt_id,
    )


def build_capital_deployment_receipt(
    *,
    receipt_id: str,
    context: CapitalDeploymentAuthorityInput,
    decision: CapitalDeploymentDecision,
) -> CapitalDeploymentReceipt:
    """Return a receipt without opening placement mechanics or broker execution."""
    trace = decision.input_trace or _input_trace(context)
    return CapitalDeploymentReceipt(
        receipt_id=receipt_id,
        decision=decision,
        input_trace=trace,
        emitted_output={
            "action": decision.action.value,
            "authorised_deployable_pct": decision.authorised_deployable_pct,
            "authorised_notional_usd": decision.authorised_notional_usd,
            "rationale": list(decision.rationale),
        },
        placement_authority_opened=False,
    )
