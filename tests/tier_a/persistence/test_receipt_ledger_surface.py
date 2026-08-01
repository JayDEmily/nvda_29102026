from __future__ import annotations

from datetime import datetime

import pytest

from nvda_desk.persistence.receipt_ledger import ReceiptLedger


def test_receipt_ledger_is_append_only_id_unique_and_copy_safe() -> None:
    ledger = ReceiptLedger()
    payload = {"receipt_path": "var/audit/example.json", "counts": {"passed": 1}}

    ledger.append_receipt("receipt-1", "proof", payload)
    ledger.append_receipt("receipt-2", "proof", {"receipt_path": "var/audit/second.json"})
    payload["counts"]["passed"] = 999
    listed = ledger.list_receipts()
    listed[0]["payload"]["counts"]["passed"] = 0

    assert ledger.list_receipts() == [
        {
            "receipt_id": "receipt-1",
            "receipt_kind": "proof",
            "payload": {"receipt_path": "var/audit/example.json", "counts": {"passed": 1}},
        },
        {
            "receipt_id": "receipt-2",
            "receipt_kind": "proof",
            "payload": {"receipt_path": "var/audit/second.json"},
        },
    ]
    with pytest.raises(ValueError, match="duplicate receipt_id"):
        ledger.append_receipt("receipt-1", "proof", {"receipt_path": "var/audit/duplicate.json"})


def test_receipt_ledger_read_receipt_returns_copy_or_none() -> None:
    ledger = ReceiptLedger()
    ledger.append_receipt("receipt-1", "checkpoint", {"checkpoint": "ready"})

    readback = ledger.read_receipt("receipt-1")
    assert readback == {
        "receipt_id": "receipt-1",
        "receipt_kind": "checkpoint",
        "payload": {"checkpoint": "ready"},
    }
    assert readback is not None
    readback["payload"]["checkpoint"] = "mutated"

    assert ledger.read_receipt("receipt-1") == {
        "receipt_id": "receipt-1",
        "receipt_kind": "checkpoint",
        "payload": {"checkpoint": "ready"},
    }
    assert ledger.read_receipt("missing") is None


def test_receipt_ledger_rejects_empty_ids_and_non_json_payloads() -> None:
    ledger = ReceiptLedger()

    with pytest.raises(ValueError, match="receipt_id must be non-empty"):
        ledger.append_receipt(" ", "proof", {"ok": True})
    with pytest.raises(ValueError, match="receipt_kind must be non-empty"):
        ledger.append_receipt("receipt-1", " ", {"ok": True})
    with pytest.raises(TypeError, match="JSON-serialisable"):
        ledger.append_receipt("receipt-1", "proof", {"not_json": datetime(2026, 5, 9)})


def test_receipt_ledger_normalises_ids_and_rejects_duplicate_after_normalisation() -> None:
    ledger = ReceiptLedger()

    ledger.append_receipt(" receipt-1 ", " proof ", {"ok": True})

    assert ledger.read_receipt("receipt-1") == {
        "receipt_id": "receipt-1",
        "receipt_kind": "proof",
        "payload": {"ok": True},
    }
    with pytest.raises(ValueError, match="duplicate receipt_id: receipt-1"):
        ledger.append_receipt("receipt-1", "proof", {"ok": False})


def test_receipt_ledger_lists_receipts_by_kind_copy_safely() -> None:
    ledger = ReceiptLedger()
    ledger.append_receipt("receipt-1", "live_inventory_reconciliation", {"position_ids": ["pos-1"]})
    ledger.append_receipt("receipt-2", "proof", {"passed": True})
    ledger.append_receipt(
        "receipt-3", " live_inventory_reconciliation ", {"position_ids": ["pos-2"]}
    )

    inventory_receipts = ledger.list_receipts_by_kind(" live_inventory_reconciliation ")
    inventory_receipts[0]["payload"]["position_ids"].append("mutated")

    assert ledger.list_receipts_by_kind("live_inventory_reconciliation") == [
        {
            "receipt_id": "receipt-1",
            "receipt_kind": "live_inventory_reconciliation",
            "payload": {"position_ids": ["pos-1"]},
        },
        {
            "receipt_id": "receipt-3",
            "receipt_kind": "live_inventory_reconciliation",
            "payload": {"position_ids": ["pos-2"]},
        },
    ]
    assert ledger.list_receipts_by_kind("proof") == [
        {"receipt_id": "receipt-2", "receipt_kind": "proof", "payload": {"passed": True}}
    ]
