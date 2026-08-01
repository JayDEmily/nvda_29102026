"""M10 execution-port protocol and offline paper adapter."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Protocol, runtime_checkable

from nvda_desk.m13_state_kernel import IdempotencyKey, InMemoryUnitOfWork, TransactionCommand

from .contracts import (
    PAPER_PORT_VERSION,
    ExecutionEvent,
    ExecutionReceipt,
    PlacementIntent,
    semantic_fingerprint,
)


def _utc(value: datetime) -> datetime:
    if value.tzinfo is None or value.utcoffset() != UTC.utcoffset(value):
        raise ValueError("execution_time_must_be_utc")
    return value


def _build_event(**payload) -> ExecutionEvent:
    material = {
        **payload,
        "contract_version": "1.0.0",
        "paper_only": True,
        "network_execution_proven": False,
        "position_mutation_proven": False,
        "lifecycle_mutation_proven": False,
    }
    fp = semantic_fingerprint(material)
    return ExecutionEvent.model_validate(
        {**material, "event_id": f"execution-event:{fp[:24]}", "semantic_fingerprint": fp}
    )


def _build_receipt(**payload) -> ExecutionReceipt:
    material = {
        **payload,
        "contract_version": "1.0.0",
        "status": "filled",
        "durability": "non_durable_in_memory",
        "paper_only": True,
        "live_execution_proven": False,
        "network_execution_proven": False,
        "position_mutation_proven": False,
        "lifecycle_mutation_proven": False,
        "durable_commit_proven": False,
    }
    fp = semantic_fingerprint(material)
    rid = f"execution-receipt:{fp[:24]}"
    return ExecutionReceipt.model_validate(
        {**material, "receipt_id": rid, "transaction_receipt_id": rid, "semantic_fingerprint": fp}
    )


@runtime_checkable
class ExecutionPort(Protocol):
    """Provider-substitutable M10 submission and evidence-read boundary."""

    adapter_mode: str
    durability: str

    def submit(self, intent: PlacementIntent, *, executed_at_utc: datetime) -> ExecutionReceipt: ...
    def list_events(self) -> tuple[ExecutionEvent, ...]: ...
    def list_receipts(self) -> tuple[ExecutionReceipt, ...]: ...


class PaperExecutionPort:
    """Explicitly offline and non-durable paper execution adapter."""

    adapter_mode = "paper"
    durability = "non_durable_in_memory"
    port_version = PAPER_PORT_VERSION

    def __init__(self, *, port_id: str = "m10.paper-port.alpha") -> None:
        if not port_id.strip():
            raise ValueError("port_id_required")
        self.port_id = port_id
        self.port_fingerprint = semantic_fingerprint(
            {
                "port_id": port_id,
                "port_version": self.port_version,
                "adapter_mode": self.adapter_mode,
                "durability": self.durability,
            }
        )
        self._uow = InMemoryUnitOfWork(initial_state={"events": [], "receipts": {}})

    def submit(self, intent: PlacementIntent, *, executed_at_utc: datetime) -> ExecutionReceipt:
        try:
            intent = PlacementIntent.model_validate(intent.model_dump(mode="python"))
        except Exception as exc:
            raise ValueError("placement_intent_contract_invalid") from exc
        executed_at_utc = _utc(executed_at_utc)
        if executed_at_utc < intent.intent_at_utc:
            raise ValueError("execution_precedes_placement_intent")

        prior = self._uow.state_version
        resulting = prior + 1
        sequence = self._uow.committed_sequence + 1
        order_id = f"paper-order:{semantic_fingerprint({'intent_id': intent.intent_id, 'port_id': self.port_id})[:24]}"
        fill_id = f"paper-fill:{semantic_fingerprint({'order_id': order_id, 'intent_id': intent.intent_id})[:24]}"
        common = {
            "intent": intent,
            "intent_id": intent.intent_id,
            "intent_fingerprint": intent.semantic_fingerprint,
            "port_id": self.port_id,
            "port_version": self.port_version,
            "port_fingerprint": self.port_fingerprint,
            "order_id": order_id,
            "quantity": intent.quantity,
            "price": intent.limit_price,
            "notional": intent.planned_notional,
            "occurred_at_utc": executed_at_utc,
        }
        order = _build_event(**common, sequence=1, event_type="order_accepted", fill_id=None)
        fill = _build_event(**common, sequence=2, event_type="fill_recorded", fill_id=fill_id)
        command_id = f"m10.execute:{intent.intent_id}"
        receipt = _build_receipt(
            intent=intent,
            intent_id=intent.intent_id,
            intent_fingerprint=intent.semantic_fingerprint,
            port_id=self.port_id,
            port_version=self.port_version,
            port_fingerprint=self.port_fingerprint,
            order_event=order,
            fill_event=fill,
            order_event_id=order.event_id,
            order_event_fingerprint=order.semantic_fingerprint,
            fill_event_id=fill.event_id,
            fill_event_fingerprint=fill.semantic_fingerprint,
            order_id=order_id,
            fill_id=fill_id,
            executed_quantity=intent.quantity,
            executed_price=intent.limit_price,
            executed_notional=intent.planned_notional,
            executed_at_utc=executed_at_utc,
            transaction_command_id=command_id,
            transaction_command_type="m10.paper_execute",
            transaction_consistency_unit_id=self.port_id,
            transaction_input_fingerprint=intent.semantic_fingerprint,
            transaction_policy_version=self.port_version,
            transaction_prior_state_version=prior,
            transaction_resulting_state_version=resulting,
            transaction_sequence=sequence,
        )
        command = TransactionCommand(
            command_id=command_id,
            idempotency_key=IdempotencyKey(
                value=intent.intent_id,
                command_type="m10.paper_execute",
                consistency_unit_id=self.port_id,
            ),
            input_fingerprint=intent.semantic_fingerprint,
            expected_state_version=prior,
            policy_version=self.port_version,
        )

        def mutation(state):
            state["events"].extend(
                (order.model_dump(mode="python"), fill.model_dump(mode="python"))
            )
            state["receipts"][intent.intent_id] = receipt.model_dump(mode="python")
            return {"receipt_id": receipt.receipt_id, "result_id": receipt.receipt_id}

        atomic = self._uow.execute(command=command, mutation=mutation)
        if not atomic.duplicate_replay and (
            atomic.receipt_id,
            atomic.result_id,
            atomic.command_id,
            atomic.command_type,
            atomic.consistency_unit_id,
            atomic.idempotency_key.value,
            atomic.idempotency_key.command_type,
            atomic.idempotency_key.consistency_unit_id,
            atomic.input_fingerprint,
            atomic.policy_version,
            atomic.prior_state_version,
            atomic.resulting_state_version,
            atomic.sequence,
        ) != (
            receipt.receipt_id,
            receipt.receipt_id,
            command_id,
            "m10.paper_execute",
            self.port_id,
            intent.intent_id,
            "m10.paper_execute",
            self.port_id,
            intent.semantic_fingerprint,
            self.port_version,
            receipt.transaction_prior_state_version,
            receipt.transaction_resulting_state_version,
            receipt.transaction_sequence,
        ):
            raise RuntimeError("m13_atomic_receipt_mismatch")
        stored = self._uow.snapshot_state()["receipts"].get(intent.intent_id)
        if stored is None:
            raise RuntimeError("committed_execution_receipt_missing")
        return ExecutionReceipt.model_validate(stored)

    def list_events(self) -> tuple[ExecutionEvent, ...]:
        return tuple(
            ExecutionEvent.model_validate(item) for item in self._uow.snapshot_state()["events"]
        )

    def list_receipts(self) -> tuple[ExecutionReceipt, ...]:
        values = self._uow.snapshot_state()["receipts"].values()
        return tuple(
            sorted(
                (ExecutionReceipt.model_validate(item) for item in values),
                key=lambda item: item.receipt_id,
            )
        )
