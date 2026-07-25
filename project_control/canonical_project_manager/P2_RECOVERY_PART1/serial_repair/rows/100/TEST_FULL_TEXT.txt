from __future__ import annotations

import pytest
from pydantic import ValidationError

from nvda_desk.contracts.exit_close import (
    CloseHandoffMaterial,
    ExitCloseInputTrace,
    ExitClosePolicyDecision,
    ExitCloseReceipt,
    find_forbidden_exit_close_authority_keys,
)
from nvda_desk.downstream.exit_close import (
    ExitCloseService,
    build_close_handoff,
    build_exit_close_receipt,
    evaluate_exit_close_policy,
    replay_exit_close_receipt,
)


def _trace() -> ExitCloseInputTrace:
    return ExitCloseInputTrace(
        live_inventory_receipt_id="inventory-receipt-001",
        position_id="position-001",
        playbook_metadata_receipt_ids=("registry:playbook:variant",),
        placement_readiness_id="placement-readiness-001",
        capital_deployment_receipt_id="capital-receipt-001",
        parallel_risk_packet_id="parallel-risk-001",
        close_policy_id="close-policy-bounded-v1",
        context={"source": "test", "risk_state": "reduce_exposure"},
    )


def test_exit_close_trace_rejects_hidden_authority_keys() -> None:
    with pytest.raises(ValidationError, match="forbidden authority keys"):
        ExitCloseInputTrace(
            live_inventory_receipt_id="inventory-receipt-001",
            position_id="position-001",
            placement_readiness_id="placement-readiness-001",
            capital_deployment_receipt_id="capital-receipt-001",
            parallel_risk_packet_id="parallel-risk-001",
            close_policy_id="close-policy-bounded-v1",
            context={"nested": {"order_execution": "not allowed"}},
        )


def test_forbidden_exit_close_authority_key_searches_nested_payloads() -> None:
    assert find_forbidden_exit_close_authority_keys(
        {"safe": [{"live_order_placement": True}, {"broker_order_id": "abc"}]}
    ) == ["broker_order_id", "live_order_placement"]


def test_exit_close_policy_consumes_downstream_trace_without_execution() -> None:
    decision = evaluate_exit_close_policy(
        input_trace=_trace(),
        requested_action="close",
        trigger_ids=("trailing-stop-hit",),
        decision_id="decision-001",
    )

    assert decision.exit_state == "close_ready"
    assert decision.position_id == "position-001"
    assert decision.input_trace.live_inventory_receipt_id == "inventory-receipt-001"
    assert decision.input_trace.capital_deployment_receipt_id == "capital-receipt-001"
    assert decision.input_trace.placement_readiness_id == "placement-readiness-001"
    assert decision.broker_execution_opened is False
    assert decision.live_inventory_mutated is False
    assert decision.capital_sizing_recomputed is False


def test_exit_close_policy_blocks_closed_position_and_missing_close_trigger() -> None:
    closed_position = evaluate_exit_close_policy(
        input_trace=_trace(),
        requested_action="close",
        trigger_ids=("exit-signal",),
        position_open=False,
    )
    assert closed_position.exit_state == "blocked"
    assert "position_not_open" in closed_position.blocked_reasons

    missing_trigger = evaluate_exit_close_policy(
        input_trace=_trace(),
        requested_action="trim",
        trigger_ids=(),
    )
    assert missing_trigger.exit_state == "blocked"
    assert "exit_or_close_trigger_required" in missing_trigger.blocked_reasons


def test_exit_close_policy_rejects_inconsistent_unblocked_state() -> None:
    with pytest.raises(ValidationError, match="exit_state must match requested_action"):
        ExitClosePolicyDecision(
            decision_id="decision-inconsistent",
            position_id="position-001",
            requested_action="close",
            exit_state="trim_ready",
            trigger_ids=("time-stop",),
            input_trace=_trace(),
        )


def test_exit_close_decision_rejects_boundary_mutation_flags() -> None:
    with pytest.raises(ValidationError, match="must not open broker execution"):
        ExitClosePolicyDecision(
            decision_id="decision-001",
            position_id="position-001",
            requested_action="hold",
            exit_state="hold",
            input_trace=_trace(),
            broker_execution_opened=True,
        )


def test_close_handoff_is_protocol_only_and_non_executing() -> None:
    decision = evaluate_exit_close_policy(
        input_trace=_trace(),
        requested_action="trim",
        trigger_ids=("profit-take-band",),
        decision_id="decision-002",
    )

    handoff = build_close_handoff(decision=decision)

    assert handoff.broker_boundary_mode == "protocol_only"
    assert handoff.broker_protocol_only is True
    assert handoff.execution_allowed is False
    assert handoff.live_order_placement_opened is False
    assert handoff.close_intent_preview["requested_action"] == "trim"

    with pytest.raises(ValidationError, match="protocol_only"):
        CloseHandoffMaterial(
            handoff_id="bad-handoff",
            decision_id="decision-002",
            position_id="position-001",
            broker_boundary_mode="live_broker_adapter",
        )


def test_close_handoff_requires_trim_or_close_ready_decision() -> None:
    decision = evaluate_exit_close_policy(
        input_trace=_trace(),
        requested_action="hold",
        decision_id="decision-hold",
    )

    with pytest.raises(ValueError, match="trim_ready or close_ready"):
        build_close_handoff(decision=decision)


def test_close_handoff_rejects_live_order_placement_flag() -> None:
    with pytest.raises(ValidationError, match="non-executing protocol-only"):
        CloseHandoffMaterial(
            handoff_id="bad-handoff-live-order",
            decision_id="decision-003",
            position_id="position-001",
            live_order_placement_opened=True,
        )


def test_close_handoff_rejects_hidden_broker_payloads() -> None:
    with pytest.raises(ValidationError, match="forbidden authority keys"):
        CloseHandoffMaterial(
            handoff_id="bad-handoff",
            decision_id="decision-003",
            position_id="position-001",
            close_intent_preview={"nested": {"broker_execution": True}},
        )


def test_exit_close_receipt_is_replayable_and_copy_safe() -> None:
    decision = evaluate_exit_close_policy(
        input_trace=_trace(),
        requested_action="close",
        trigger_ids=("time-stop",),
        decision_id="decision-004",
    )
    handoff = build_close_handoff(decision=decision)
    receipt = build_exit_close_receipt(
        receipt_id="exit-close-receipt-001",
        decision=decision,
        close_handoff=handoff,
    )

    assert receipt.broker_execution_opened is False
    assert receipt.live_inventory_mutated is False
    assert receipt.position_closure_replay_fingerprint == replay_exit_close_receipt(receipt)

    copied = receipt.model_copy(deep=True)
    copied.emitted_output["exit_state"] = "mutated"
    assert receipt.emitted_output["exit_state"] == "close_ready"


def test_exit_close_receipt_rejects_hidden_emitted_output_authority() -> None:
    decision = evaluate_exit_close_policy(
        input_trace=_trace(),
        requested_action="hold",
        decision_id="decision-005",
    )
    with pytest.raises(ValidationError, match="forbidden authority keys"):
        ExitCloseReceipt(
            receipt_id="bad-receipt",
            decision=decision,
            input_trace=decision.input_trace,
            emitted_output={"capital_sizing": "not allowed"},
            position_closure_replay_fingerprint="abc",
        )


def test_exit_close_receipt_rejects_input_trace_mismatch() -> None:
    decision = evaluate_exit_close_policy(
        input_trace=_trace(),
        requested_action="hold",
        decision_id="decision-trace-mismatch",
    )
    mismatched_trace = _trace().model_copy(update={"position_id": "position-002"})

    with pytest.raises(ValidationError, match="input_trace must match decision input_trace"):
        ExitCloseReceipt(
            receipt_id="bad-receipt-trace-mismatch",
            decision=decision,
            input_trace=mismatched_trace,
            position_closure_replay_fingerprint="abc",
        )


def test_exit_close_receipt_rejects_live_inventory_mutation_flag() -> None:
    decision = evaluate_exit_close_policy(
        input_trace=_trace(),
        requested_action="hold",
        decision_id="decision-live-inventory-mutation",
    )

    with pytest.raises(ValidationError, match="must not mutate live inventory"):
        ExitCloseReceipt(
            receipt_id="bad-receipt-live-inventory-mutation",
            decision=decision,
            input_trace=decision.input_trace,
            position_closure_replay_fingerprint="abc",
            live_inventory_mutated=True,
        )


def test_exit_close_replay_fingerprint_changes_when_handoff_material_changes() -> None:
    decision = evaluate_exit_close_policy(
        input_trace=_trace(),
        requested_action="close",
        trigger_ids=("time-stop",),
        decision_id="decision-replay-material",
    )
    handoff = build_close_handoff(decision=decision)
    changed_handoff = handoff.model_copy(
        update={
            "close_intent_preview": {
                **handoff.close_intent_preview,
                "trigger_ids": ["different-trigger"],
            }
        },
        deep=True,
    )

    assert replay_exit_close_receipt(
        build_exit_close_receipt(
            receipt_id="exit-close-receipt-replay-a",
            decision=decision,
            close_handoff=handoff,
        )
    ) != replay_exit_close_receipt(
        build_exit_close_receipt(
            receipt_id="exit-close-receipt-replay-b",
            decision=decision,
            close_handoff=changed_handoff,
        )
    )


def test_exit_close_service_wrapper_emits_receipt_without_opening_orders() -> None:
    service = ExitCloseService()
    decision = service.evaluate_policy(
        input_trace=_trace(),
        requested_action="close",
        trigger_ids=("manual-review-approved",),
        decision_id="decision-006",
    )
    handoff = service.build_handoff(decision=decision)
    receipt = service.build_receipt(
        receipt_id="exit-close-receipt-006",
        decision=decision,
        close_handoff=handoff,
    )

    assert receipt.close_handoff is not None
    assert receipt.close_handoff.execution_allowed is False
    assert receipt.position_closure_replay_fingerprint == replay_exit_close_receipt(receipt)
