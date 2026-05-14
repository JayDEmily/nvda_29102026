"""Durable receipt-ledger primitives for bounded audit and checkpoint truth."""

from __future__ import annotations

import json
from copy import deepcopy
from typing import Any, Mapping


class ReceiptLedger:
    """Append-only receipt ledger with duplicate-id protection and copy-on-read."""

    def __init__(self):
        self._receipts: list[dict[str, Any]] = []
        self._receipt_ids: set[str] = set()

    def append_receipt(
        self, receipt_id: str, receipt_kind: str, payload: Mapping[str, Any]
    ) -> None:
        """Append one JSON-serialisable receipt payload by stable identifier."""

        normalised_id = _normalise_token(receipt_id, "receipt_id")
        normalised_kind = _normalise_token(receipt_kind, "receipt_kind")
        if normalised_id in self._receipt_ids:
            raise ValueError(f"duplicate receipt_id: {normalised_id}")

        stored_payload = deepcopy(dict(payload))
        _assert_json_serialisable(stored_payload)
        self._receipt_ids.add(normalised_id)
        self._receipts.append(
            {
                "receipt_id": normalised_id,
                "receipt_kind": normalised_kind,
                "payload": stored_payload,
            }
        )

    def read_receipt(self, receipt_id: str) -> dict[str, Any] | None:
        """Return one stored receipt by identifier, if present."""

        normalised_id = _normalise_token(receipt_id, "receipt_id")
        for receipt in self._receipts:
            if receipt["receipt_id"] == normalised_id:
                return deepcopy(receipt)
        return None

    def list_receipts(self) -> list[dict[str, Any]]:
        """Return stored receipts in append order."""

        return deepcopy(self._receipts)

    def list_receipts_by_kind(self, receipt_kind: str) -> list[dict[str, Any]]:
        """Return stored receipts of one kind in append order."""

        normalised_kind = _normalise_token(receipt_kind, "receipt_kind")
        return deepcopy(
            [
                receipt
                for receipt in self._receipts
                if receipt["receipt_kind"] == normalised_kind
            ]
        )


def _normalise_token(value: str, field_name: str) -> str:
    token = str(value).strip()
    if not token:
        raise ValueError(f"{field_name} must be non-empty")
    return token


def _assert_json_serialisable(payload: Mapping[str, Any]) -> None:
    try:
        json.dumps(payload, sort_keys=True)
    except TypeError as exc:
        raise TypeError("receipt payload must be JSON-serialisable") from exc
