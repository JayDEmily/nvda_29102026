"""Canonical M11 portfolio lifecycle service."""

from __future__ import annotations

from copy import deepcopy
from datetime import UTC, datetime
from decimal import Decimal
from typing import Any, Literal

from nvda_desk.m10_execution_gateway.contracts import ExecutionReceipt, semantic_fingerprint
from nvda_desk.m13_state_kernel.contracts import IdempotencyKey, TransactionCommand
from nvda_desk.m13_state_kernel.in_memory import InMemoryUnitOfWork

from .contracts import (
    CloseReceipt,
    FillReconciliationReceipt,
    LifecycleDecision,
    PortfolioSnapshot,
    PositionState,
)


class PortfolioLifecycleService:
    """Own one non-durable canonical NVDA portfolio state."""

    def __init__(self) -> None:
        self._uow = InMemoryUnitOfWork(initial_state={"positions": {}})
        self._fill_receipts: dict[str, FillReconciliationReceipt] = {}
        self._close_receipts: dict[str, CloseReceipt] = {}
        self._last_transition_at = datetime(1970, 1, 1, tzinfo=UTC)

    @property
    def durability(self) -> str:
        return self._uow.durability

    def snapshot(self) -> PortfolioSnapshot:
        return deepcopy(self._build_snapshot(as_of=self._last_transition_at))

    def reconcile_fill(self, receipt: ExecutionReceipt) -> FillReconciliationReceipt:
        try:
            receipt = ExecutionReceipt.model_validate(receipt.model_dump(mode="python"))
        except Exception as exc:
            raise ValueError("execution_receipt_contract_invalid") from exc
        if receipt.status != "filled":
            raise ValueError("execution_receipt_not_filled")
        previous = self._fill_receipts.get(receipt.receipt_id)
        if previous is not None:
            if previous.execution_receipt_fingerprint != receipt.semantic_fingerprint:
                raise ValueError("conflicting_execution_receipt_replay")
            return FillReconciliationReceipt.model_validate(
                {**previous.model_dump(mode="python"), "duplicate_replay": True}
            )

        current = self._current_position()
        if current is not None and receipt.executed_at_utc < current.updated_at_utc:
            raise ValueError("fill_precedes_current_position_update")
        next_version = self._uow.state_version + 1
        position = self._position_after_fill(current, receipt, next_version)
        preview = self._preview_snapshot(
            position=position, version=next_version, as_of=receipt.executed_at_utc
        )
        material = {
            "execution_receipt_id": receipt.receipt_id,
            "execution_receipt_fingerprint": receipt.semantic_fingerprint,
            "fill_id": receipt.fill_id,
            "snapshot_fingerprint": preview.semantic_fingerprint,
            "state_version": next_version,
        }
        result_fp = semantic_fingerprint(material)
        result_id = f"fill-result:{result_fp[:24]}"
        atomic_receipt_id = f"m13:m11-fill:{result_fp[:24]}"
        command = TransactionCommand(
            command_id=f"m11.reconcile:{receipt.receipt_id}",
            idempotency_key=IdempotencyKey(
                receipt.receipt_id, "m11.reconcile_fill", "portfolio:NVDA"
            ),
            input_fingerprint=receipt.semantic_fingerprint,
            expected_state_version=self._uow.state_version,
            policy_version="m11.fill-reconciliation.v1",
        )

        def mutation(state: dict[str, Any]):
            state["positions"] = {position.position_id: position.model_dump(mode="python")}
            return {"receipt_id": atomic_receipt_id, "result_id": result_id}

        atomic = self._uow.execute(command=command, mutation=mutation)
        self._last_transition_at = receipt.executed_at_utc
        snapshot = self._build_snapshot(as_of=receipt.executed_at_utc)
        payload = {
            "execution_receipt_id": receipt.receipt_id,
            "execution_receipt_fingerprint": receipt.semantic_fingerprint,
            "fill_id": receipt.fill_id,
            "snapshot": snapshot,
            "snapshot_id": snapshot.snapshot_id,
            "snapshot_fingerprint": snapshot.semantic_fingerprint,
            "atomic_receipt_id": atomic.receipt_id,
            "atomic_command_id": atomic.command_id,
            "atomic_prior_state_version": atomic.prior_state_version,
            "atomic_resulting_state_version": atomic.resulting_state_version,
            "atomic_sequence": atomic.sequence,
            "durability": "non_durable_in_memory",
        }
        fp = semantic_fingerprint(payload)
        result = FillReconciliationReceipt.model_validate(
            {**payload, "receipt_id": f"fill-reconciliation:{fp[:24]}", "semantic_fingerprint": fp}
        )
        self._fill_receipts[receipt.receipt_id] = result
        return deepcopy(result)

    def decide_lifecycle(
        self,
        *,
        snapshot: PortfolioSnapshot,
        position_id: str,
        action: Literal["hold", "trim", "close"],
        quantity: Decimal | None,
        reasons: tuple[str, ...],
        decided_at_utc: datetime,
    ) -> LifecycleDecision:
        try:
            snapshot = PortfolioSnapshot.model_validate(snapshot.model_dump(mode="python"))
        except Exception as exc:
            raise ValueError("portfolio_snapshot_contract_invalid") from exc
        if decided_at_utc.tzinfo is None or decided_at_utc.utcoffset() != UTC.utcoffset(
            decided_at_utc
        ):
            raise ValueError("lifecycle_decision_time_must_be_utc")
        if decided_at_utc < snapshot.as_of_utc:
            raise ValueError("lifecycle_decision_precedes_snapshot")
        positions = {p.position_id: p for p in snapshot.positions}
        if position_id not in positions:
            raise ValueError("position_not_in_snapshot")
        position = positions[position_id]
        payload = {
            "contract_version": "1.0.0",
            "policy_version": "m11.lifecycle.v1",
            "snapshot_id": snapshot.snapshot_id,
            "snapshot_fingerprint": snapshot.semantic_fingerprint,
            "snapshot_state_version": snapshot.state_version,
            "position_id": position.position_id,
            "position_fingerprint": position.semantic_fingerprint,
            "position_quantity": position.quantity,
            "action": action,
            "quantity": quantity,
            "reasons": reasons,
            "decided_at_utc": decided_at_utc,
            "broker_execution_allowed": False,
            "capital_recomputation_allowed": False,
        }
        fp = semantic_fingerprint(payload)
        return LifecycleDecision.model_validate(
            {**payload, "decision_id": f"lifecycle-decision:{fp[:24]}", "semantic_fingerprint": fp}
        )

    def apply_lifecycle(self, decision: LifecycleDecision) -> CloseReceipt:
        try:
            decision = LifecycleDecision.model_validate(decision.model_dump(mode="python"))
        except Exception as exc:
            raise ValueError("lifecycle_decision_contract_invalid") from exc
        if decision.action == "hold":
            raise ValueError("hold_is_non_mutating")
        previous = self._close_receipts.get(decision.decision_id)
        if previous is not None:
            if previous.decision_fingerprint != decision.semantic_fingerprint:
                raise ValueError("conflicting_lifecycle_decision_replay")
            return CloseReceipt.model_validate(
                {**previous.model_dump(mode="python"), "duplicate_replay": True}
            )
        current_snapshot = self.snapshot()
        if (
            current_snapshot.snapshot_id,
            current_snapshot.semantic_fingerprint,
            current_snapshot.state_version,
        ) != (decision.snapshot_id, decision.snapshot_fingerprint, decision.snapshot_state_version):
            raise ValueError("stale_lifecycle_snapshot")
        current = self._current_position()
        if current is None or current.semantic_fingerprint != decision.position_fingerprint:
            raise ValueError("stale_lifecycle_position")
        next_version = self._uow.state_version + 1
        resulting = None
        if decision.action == "trim":
            assert decision.quantity is not None
            remaining = current.quantity - decision.quantity
            resulting = self._build_position(
                quantity=remaining,
                cost_basis=current.average_cost * remaining,
                fill_ids=current.fill_ids,
                execution_receipt_ids=current.execution_receipt_ids,
                execution_receipt_fingerprints=current.execution_receipt_fingerprints,
                opened_at=current.opened_at_utc,
                updated_at=decision.decided_at_utc,
                state_version=next_version,
            )
        preview = self._preview_snapshot(
            position=resulting, version=next_version, as_of=decision.decided_at_utc
        )
        material = {
            "decision_fingerprint": decision.semantic_fingerprint,
            "snapshot_fingerprint": preview.semantic_fingerprint,
            "state_version": next_version,
        }
        result_fp = semantic_fingerprint(material)
        atomic_receipt_id = f"m13:m11-close:{result_fp[:24]}"
        command = TransactionCommand(
            command_id=f"m11.lifecycle:{decision.decision_id}",
            idempotency_key=IdempotencyKey(
                decision.decision_id, "m11.apply_lifecycle", "portfolio:NVDA"
            ),
            input_fingerprint=decision.semantic_fingerprint,
            expected_state_version=self._uow.state_version,
            policy_version=decision.policy_version,
        )

        def mutation(state: dict[str, Any]):
            state["positions"] = (
                {}
                if resulting is None
                else {resulting.position_id: resulting.model_dump(mode="python")}
            )
            return {
                "receipt_id": atomic_receipt_id,
                "result_id": f"lifecycle-result:{result_fp[:24]}",
            }

        atomic = self._uow.execute(command=command, mutation=mutation)
        self._last_transition_at = decision.decided_at_utc
        snapshot = self._build_snapshot(as_of=decision.decided_at_utc)
        payload = {
            "decision": decision,
            "decision_id": decision.decision_id,
            "decision_fingerprint": decision.semantic_fingerprint,
            "prior_position": current,
            "resulting_position": resulting,
            "snapshot": snapshot,
            "atomic_receipt_id": atomic.receipt_id,
            "atomic_command_id": atomic.command_id,
            "atomic_prior_state_version": atomic.prior_state_version,
            "atomic_resulting_state_version": atomic.resulting_state_version,
            "atomic_sequence": atomic.sequence,
            "durability": "non_durable_in_memory",
        }
        fp = semantic_fingerprint(payload)
        result = CloseReceipt.model_validate(
            {**payload, "receipt_id": f"close-receipt:{fp[:24]}", "semantic_fingerprint": fp}
        )
        self._close_receipts[decision.decision_id] = result
        return deepcopy(result)

    def _current_position(self) -> PositionState | None:
        state = self._uow.snapshot_state()
        raw = state.get("positions", {}).get("position:NVDA:long")
        return None if raw is None else PositionState.model_validate(raw)

    def _position_after_fill(
        self, current: PositionState | None, receipt: ExecutionReceipt, version: int
    ) -> PositionState:
        if current is None:
            return self._build_position(
                quantity=receipt.executed_quantity,
                cost_basis=receipt.executed_notional,
                fill_ids=(receipt.fill_id,),
                execution_receipt_ids=(receipt.receipt_id,),
                execution_receipt_fingerprints=(receipt.semantic_fingerprint,),
                opened_at=receipt.executed_at_utc,
                updated_at=receipt.executed_at_utc,
                state_version=version,
            )
        if receipt.fill_id in current.fill_ids:
            raise ValueError("duplicate_fill_id")
        return self._build_position(
            quantity=current.quantity + receipt.executed_quantity,
            cost_basis=current.cost_basis + receipt.executed_notional,
            fill_ids=current.fill_ids + (receipt.fill_id,),
            execution_receipt_ids=current.execution_receipt_ids + (receipt.receipt_id,),
            execution_receipt_fingerprints=current.execution_receipt_fingerprints
            + (receipt.semantic_fingerprint,),
            opened_at=current.opened_at_utc,
            updated_at=receipt.executed_at_utc,
            state_version=version,
        )

    @staticmethod
    def _build_position(
        *,
        quantity: Decimal,
        cost_basis: Decimal,
        fill_ids: tuple[str, ...],
        execution_receipt_ids: tuple[str, ...],
        execution_receipt_fingerprints: tuple[str, ...],
        opened_at: datetime,
        updated_at: datetime,
        state_version: int,
    ) -> PositionState:
        payload = {
            "quantity": quantity,
            "average_cost": cost_basis / quantity,
            "cost_basis": cost_basis,
            "fill_ids": fill_ids,
            "execution_receipt_ids": execution_receipt_ids,
            "execution_receipt_fingerprints": execution_receipt_fingerprints,
            "opened_at_utc": opened_at,
            "updated_at_utc": updated_at,
            "state_version": state_version,
        }
        fp = semantic_fingerprint(
            {
                "position_id": "position:NVDA:long",
                "contract_version": "1.0.0",
                "symbol": "NVDA",
                "side": "long",
                **payload,
                "paper_only": True,
                "live_account_truth": False,
                "durable_commit_proven": False,
            }
        )
        return PositionState.model_validate({**payload, "semantic_fingerprint": fp})

    def _preview_snapshot(
        self, *, position: PositionState | None, version: int, as_of: datetime
    ) -> PortfolioSnapshot:
        positions = () if position is None else (position,)
        payload = {
            "contract_version": "1.0.0",
            "portfolio_id": "portfolio:NVDA",
            "positions": positions,
            "position_ids": tuple(p.position_id for p in positions),
            "state_version": version,
            "as_of_utc": as_of,
            "durability": "non_durable_in_memory",
            "live_account_truth": False,
        }
        fp = semantic_fingerprint(payload)
        return PortfolioSnapshot.model_validate(
            {**payload, "snapshot_id": f"portfolio-snapshot:{fp[:24]}", "semantic_fingerprint": fp}
        )

    def _build_snapshot(self, *, as_of: datetime) -> PortfolioSnapshot:
        position = self._current_position()
        return self._preview_snapshot(
            position=position, version=self._uow.state_version, as_of=as_of
        )
