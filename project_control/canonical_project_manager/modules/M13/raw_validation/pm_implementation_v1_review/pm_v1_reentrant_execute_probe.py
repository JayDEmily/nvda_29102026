"""Independent PM probe for nested/re-entrant UnitOfWork.execute sequencing."""

from __future__ import annotations

from nvda_desk.m13_state_kernel import InMemoryUnitOfWork, IdempotencyKey, TransactionCommand


def command(name: str, expected: int) -> TransactionCommand:
    return TransactionCommand(
        command_id=f"command-{name}",
        idempotency_key=IdempotencyKey(
            value=f"key-{name}",
            command_type="synthetic",
            consistency_unit_id="unit-1",
        ),
        input_fingerprint=f"fingerprint-{name}",
        expected_state_version=expected,
        policy_version="policy-v1",
    )


def main() -> None:
    boundary = InMemoryUnitOfWork(initial_state={"outer": 0, "inner": 0})

    def inner_mutation(state: dict[str, int]) -> dict[str, str]:
        state["inner"] += 1
        return {"receipt_id": "receipt-inner", "result_id": "result-inner"}

    def outer_mutation(state: dict[str, int]) -> dict[str, str]:
        state["outer"] += 1
        boundary.execute(command=command("inner", 0), mutation=inner_mutation)
        return {"receipt_id": "receipt-outer", "result_id": "result-outer"}

    boundary.execute(command=command("outer", 0), mutation=outer_mutation)
    receipts = boundary.list_receipts()

    print(f"state={boundary.snapshot_state()!r}")
    print(f"state_version={boundary.state_version}")
    print(f"committed_sequence={boundary.committed_sequence}")
    print(f"receipt_count={len(receipts)}")
    print(f"receipt_sequences={[receipt.sequence for receipt in receipts]!r}")
    print(
        "receipt_versions="
        f"{[(receipt.prior_state_version, receipt.resulting_state_version) for receipt in receipts]!r}"
    )

    assert len(receipts) != 2, (
        "a later transaction committed before the active transaction produced an admitted result"
    )
    assert len({receipt.sequence for receipt in receipts}) == len(receipts), (
        "committed receipts contain duplicate sequence authority"
    )
    assert boundary.snapshot_state() == {"outer": 1, "inner": 1}, (
        "a committed inner receipt survives while its state mutation is overwritten"
    )


if __name__ == "__main__":
    main()
