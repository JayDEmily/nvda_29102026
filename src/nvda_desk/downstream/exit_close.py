"""Build bounded exit/close policy decisions and non-executing handoff receipts."""

from __future__ import annotations

from nvda_desk.contracts.exit_close import (
    CloseHandoffMaterial,
    ExitCloseAction,
    ExitCloseInputTrace,
    ExitClosePolicyDecision,
    ExitCloseReceipt,
    fingerprint_exit_close_replay,
)


class ExitCloseService:
    """Own bounded row 5.14 exit/close evaluation without broker execution."""

    def evaluate_policy(
        self,
        *,
        input_trace: ExitCloseInputTrace,
        requested_action: ExitCloseAction,
        trigger_ids: tuple[str, ...] = (),
        decision_id: str = "exit-close-decision",
        position_open: bool = True,
    ) -> ExitClosePolicyDecision:
        return evaluate_exit_close_policy(
            input_trace=input_trace,
            requested_action=requested_action,
            trigger_ids=trigger_ids,
            decision_id=decision_id,
            position_open=position_open,
        )

    def build_handoff(
        self,
        *,
        decision: ExitClosePolicyDecision,
        broker_boundary_mode: str = "protocol_only",
    ) -> CloseHandoffMaterial:
        return build_close_handoff(
            decision=decision,
            broker_boundary_mode=broker_boundary_mode,
        )

    def build_receipt(
        self,
        *,
        receipt_id: str,
        decision: ExitClosePolicyDecision,
        close_handoff: CloseHandoffMaterial | None = None,
    ) -> ExitCloseReceipt:
        return build_exit_close_receipt(
            receipt_id=receipt_id,
            decision=decision,
            close_handoff=close_handoff,
        )


def evaluate_exit_close_policy(
    *,
    input_trace: ExitCloseInputTrace,
    requested_action: ExitCloseAction,
    trigger_ids: tuple[str, ...] = (),
    decision_id: str = "exit-close-decision",
    position_open: bool = True,
) -> ExitClosePolicyDecision:
    """Return a bounded exit/close policy decision from admitted downstream inputs."""

    blocked_reasons: tuple[str, ...] = ()
    if not position_open:
        blocked_reasons = ("position_not_open",)
    elif requested_action in {"trim", "close"} and not trigger_ids:
        blocked_reasons = ("exit_or_close_trigger_required",)

    exit_state = "blocked"
    if not blocked_reasons:
        exit_state = {
            "hold": "hold",
            "trim": "trim_ready",
            "close": "close_ready",
        }[requested_action]

    return ExitClosePolicyDecision(
        decision_id=decision_id,
        position_id=input_trace.position_id,
        requested_action=requested_action,
        exit_state=exit_state,
        trigger_ids=trigger_ids,
        blocked_reasons=blocked_reasons,
        input_trace=input_trace,
    )


def build_close_handoff(
    *,
    decision: ExitClosePolicyDecision,
    broker_boundary_mode: str = "protocol_only",
) -> CloseHandoffMaterial:
    """Return protocol-only handoff material for trim/close-ready decisions."""

    if decision.exit_state not in {"trim_ready", "close_ready"}:
        raise ValueError("close handoff requires trim_ready or close_ready decision")
    return CloseHandoffMaterial(
        handoff_id=f"{decision.decision_id}::close-handoff",
        decision_id=decision.decision_id,
        position_id=decision.position_id,
        broker_boundary_mode=broker_boundary_mode,
        close_intent_preview={
            "position_id": decision.position_id,
            "decision_id": decision.decision_id,
            "requested_action": decision.requested_action,
            "exit_state": decision.exit_state,
            "trigger_ids": list(decision.trigger_ids),
            "close_policy_id": decision.input_trace.close_policy_id,
        },
    )


def build_exit_close_receipt(
    *,
    receipt_id: str,
    decision: ExitClosePolicyDecision,
    close_handoff: CloseHandoffMaterial | None = None,
) -> ExitCloseReceipt:
    """Return replayable exit/close receipt without live order placement."""

    fingerprint = fingerprint_exit_close_replay(
        decision=decision,
        close_handoff=close_handoff,
    )
    return ExitCloseReceipt(
        receipt_id=receipt_id,
        decision=decision,
        input_trace=decision.input_trace,
        close_handoff=close_handoff,
        emitted_output={
            "decision_id": decision.decision_id,
            "position_id": decision.position_id,
            "requested_action": decision.requested_action,
            "exit_state": decision.exit_state,
            "blocked_reasons": list(decision.blocked_reasons),
            "close_handoff_id": close_handoff.handoff_id if close_handoff else None,
        },
        position_closure_replay_fingerprint=fingerprint,
    )


def replay_exit_close_receipt(receipt: ExitCloseReceipt) -> str:
    """Recompute the replay fingerprint for a previously emitted exit/close receipt."""

    return fingerprint_exit_close_replay(
        decision=receipt.decision,
        close_handoff=receipt.close_handoff,
    )
