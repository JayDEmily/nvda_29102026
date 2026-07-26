"""Independent PM probe for AtomicReceipt scope and version self-consistency."""

from __future__ import annotations

from nvda_desk.m13_state_kernel import AtomicReceipt, IdempotencyKey


def main() -> None:
    key = IdempotencyKey(
        value="key-1",
        command_type="command-a",
        consistency_unit_id="unit-a",
    )
    receipt = AtomicReceipt(
        receipt_id="receipt-1",
        result_id="result-1",
        command_id="command-1",
        command_type="command-b",
        consistency_unit_id="unit-b",
        idempotency_key=key,
        input_fingerprint="fingerprint-1",
        policy_version="policy-v1",
        prior_state_version=0,
        resulting_state_version=1.0,
        sequence=1,
    )
    print(f"receipt={receipt!r}")
    print(f"scope_matches={receipt.command_type == key.command_type and receipt.consistency_unit_id == key.consistency_unit_id}")
    print(f"resulting_version_type={type(receipt.resulting_state_version).__name__}")
    assert receipt.command_type == key.command_type, "receipt command type is not bound to its idempotency scope"
    assert receipt.consistency_unit_id == key.consistency_unit_id, "receipt consistency unit is not bound to its idempotency scope"
    assert type(receipt.resulting_state_version) is int, "resulting state version accepted a non-integer value"


if __name__ == "__main__":
    main()
