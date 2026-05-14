"""Build bounded live-inventory snapshots."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from copy import deepcopy
from typing import Any

from nvda_desk.contracts.downstream import (
    DownstreamLiveInventorySnapshot,
    InventoryExposureState,
    InventoryStateReceipt,
    LiveCapitalState,
    LivePositionState,
)
from nvda_desk.persistence.receipt_ledger import ReceiptLedger
from nvda_desk.repositories.capital_state_repository import CapitalStateRepository
from nvda_desk.repositories.position_repository import PositionRepository


class DownstreamLiveInventoryService:
    """Create truthful live-inventory snapshots without injecting policy."""

    def __init__(
        self,
        *,
        position_repository: PositionRepository | None = None,
        capital_state_repository: CapitalStateRepository | None = None,
        receipt_ledger: ReceiptLedger | None = None,
    ):
        self._position_repository = position_repository
        self._capital_state_repository = capital_state_repository
        self._receipt_ledger = receipt_ledger

    def build_live_snapshot(
        self,
        live_ids: list[str] | None = None,
        *,
        inventory_id: str = "live-inventory",
        capital_snapshot_id: str | None = None,
        receipt_id: str | None = None,
    ) -> DownstreamLiveInventorySnapshot:
        """Build one inventory snapshot from repo-native state without policy decisions."""

        requested_ids = _normalise_id_list(live_ids)
        position_states = self._read_position_states(requested_ids)
        capital_state = self._read_capital_state(capital_snapshot_id)
        exposure_state = _build_exposure_state(position_states)
        receipt = None
        if receipt_id is not None:
            receipt = InventoryStateReceipt(
                receipt_id=_normalise_token(receipt_id, "receipt_id"),
                inventory_id=_normalise_token(inventory_id, "inventory_id"),
                position_ids=[state.position_id for state in position_states],
                capital_snapshot_id=capital_state.snapshot_id if capital_state else None,
            )
            if self._receipt_ledger is not None:
                self._receipt_ledger.append_receipt(
                    receipt.receipt_id,
                    "live_inventory_snapshot",
                    receipt.model_dump(),
                )
        return DownstreamLiveInventorySnapshot(
            inventory_id=_normalise_token(inventory_id, "inventory_id"),
            live_ids=[state.position_id for state in position_states] or requested_ids,
            position_states=position_states,
            capital_state=capital_state,
            exposure_state=exposure_state,
            inventory_receipt=receipt,
        )

    def reconcile_fill_evidence(
        self,
        fill_evidence: Iterable[Mapping[str, Any]],
        *,
        reconciliation_id: str,
        inventory_id: str = "live-inventory",
        capital_snapshot_id: str | None = None,
        receipt_id: str | None = None,
    ) -> DownstreamLiveInventorySnapshot:
        """Reconcile executed fill evidence into repo-native live-inventory state."""

        if self._position_repository is None:
            raise ValueError("position_repository is required for fill reconciliation")

        normalised_reconciliation_id = _normalise_token(
            reconciliation_id, "reconciliation_id"
        )
        normalised_events = [_normalise_fill_evidence_event(event) for event in fill_evidence]
        if not normalised_events:
            raise ValueError("fill_evidence must contain at least one event")
        _assert_unique_fill_evidence_ids(normalised_events)

        grouped_payloads: dict[str, dict[str, Any]] = {}
        for event in normalised_events:
            position_id = event["position_id"]
            payload = grouped_payloads.get(position_id)
            if payload is None:
                existing = self._position_repository.read_position(position_id)
                payload = deepcopy(existing) if existing is not None else {}
                payload.setdefault("fill_evidence_ids", [])
                payload.setdefault("fill_evidence", [])
                grouped_payloads[position_id] = payload

            existing_fill_ids = _normalised_existing_fill_ids(payload.get("fill_evidence_ids"))
            if event["fill_evidence_id"] in existing_fill_ids:
                raise ValueError(f"duplicate fill_evidence_id: {event['fill_evidence_id']}")

            if event.get("symbol") and not payload.get("symbol"):
                payload["symbol"] = event["symbol"]

            declared_delta = _optional_float(event.get("declared_exposure_delta"))
            if declared_delta is not None:
                current_declared = _optional_float(payload.get("declared_exposure")) or 0.0
                payload["declared_exposure"] = current_declared + declared_delta

            payload["fill_evidence_ids"].append(event["fill_evidence_id"])
            payload["fill_evidence"].append(deepcopy(event))
            payload["inventory_reconciliation_id"] = normalised_reconciliation_id

        for position_id, payload in grouped_payloads.items():
            if self._position_repository.read_position(position_id) is None:
                self._position_repository.write_position(position_id, payload)
            else:
                self._position_repository.replace_position(position_id, payload)

        reconciled_position_ids = list(grouped_payloads)
        snapshot = self.build_live_snapshot(
            live_ids=reconciled_position_ids,
            inventory_id=inventory_id,
            capital_snapshot_id=capital_snapshot_id,
        )
        normalised_receipt_id = receipt_id
        receipt = None
        if normalised_receipt_id is not None:
            receipt = InventoryStateReceipt(
                receipt_id=_normalise_token(normalised_receipt_id, "receipt_id"),
                inventory_id=_normalise_token(inventory_id, "inventory_id"),
                position_ids=reconciled_position_ids,
                capital_snapshot_id=snapshot.capital_state.snapshot_id
                if snapshot.capital_state
                else None,
            )
            if self._receipt_ledger is not None:
                receipt_payload = receipt.model_dump()
                receipt_payload.update(
                    {
                        "reconciliation_id": normalised_reconciliation_id,
                        "fill_evidence_ids": [
                            event["fill_evidence_id"] for event in normalised_events
                        ],
                    }
                )
                self._receipt_ledger.append_receipt(
                    receipt.receipt_id,
                    "live_inventory_reconciliation",
                    receipt_payload,
                )
        return snapshot.model_copy(update={"inventory_receipt": receipt})

    def _read_position_states(self, requested_ids: list[str]) -> list[LivePositionState]:
        if self._position_repository is None:
            return [LivePositionState(position_id=position_id) for position_id in requested_ids]

        if requested_ids:
            records = [
                self._position_repository.read_position_record(position_id)
                for position_id in requested_ids
            ]
            records = [record for record in records if record is not None]
        else:
            records = self._position_repository.list_position_records()

        return [
            LivePositionState(
                position_id=str(record["position_id"]),
                source_payload=deepcopy(dict(record["position"])),
            )
            for record in records
        ]

    def _read_capital_state(self, snapshot_id: str | None) -> LiveCapitalState | None:
        if self._capital_state_repository is None:
            return None
        if snapshot_id is None:
            records = self._capital_state_repository.list_snapshot_records()
            if not records:
                return None
            record = records[-1]
        else:
            record = self._capital_state_repository.read_snapshot_record(snapshot_id)
            if record is None:
                return None
        return LiveCapitalState(
            snapshot_id=str(record["snapshot_id"]),
            source_payload=deepcopy(dict(record["snapshot"])),
        )


_FILL_EVIDENCE_FORBIDDEN_KEYS = frozenset(
    {
        "broker_order_id",
        "order_submitted",
        "execution_allowed",
        "capital_deployment_receipt_id",
        "opening_authorisation",
        "placement_handoff",
    }
)


def _normalise_fill_evidence_event(event: Mapping[str, Any]) -> dict[str, Any]:
    payload = deepcopy(dict(event))
    forbidden = set(payload) & _FILL_EVIDENCE_FORBIDDEN_KEYS
    if forbidden:
        joined = ", ".join(sorted(forbidden))
        raise ValueError(f"fill evidence cannot carry placement authority keys: {joined}")
    payload["fill_evidence_id"] = _normalise_token(
        payload.get("fill_evidence_id", ""), "fill_evidence_id"
    )
    payload["position_id"] = _normalise_token(payload.get("position_id", ""), "position_id")
    if "symbol" in payload:
        symbol = _optional_text(payload["symbol"])
        if symbol is not None:
            payload["symbol"] = symbol
        else:
            payload.pop("symbol")
    declared_delta = _optional_float(payload.get("declared_exposure_delta"))
    if declared_delta is not None:
        payload["declared_exposure_delta"] = declared_delta
    return payload


def _assert_unique_fill_evidence_ids(events: list[dict[str, Any]]) -> None:
    observed: set[str] = set()
    for event in events:
        evidence_id = event["fill_evidence_id"]
        if evidence_id in observed:
            raise ValueError(f"duplicate fill_evidence_id: {evidence_id}")
        observed.add(evidence_id)


def _normalised_existing_fill_ids(values: Any) -> set[str]:
    if values is None:
        return set()
    if not isinstance(values, list):
        raise ValueError("fill_evidence_ids must be a list")
    return {_normalise_token(value, "fill_evidence_id") for value in values}


def _build_exposure_state(position_states: Iterable[LivePositionState]) -> InventoryExposureState:
    ids: list[str] = []
    exposures: dict[str, float] = {}
    for state in position_states:
        ids.append(state.position_id)
        symbol = _optional_text(state.source_payload.get("symbol"))
        declared_exposure = _optional_float(state.source_payload.get("declared_exposure"))
        if symbol and declared_exposure is not None:
            exposures[symbol] = exposures.get(symbol, 0.0) + declared_exposure
    return InventoryExposureState(
        position_count=len(ids),
        open_position_ids=ids,
        declared_exposure_by_symbol=exposures,
    )


def _normalise_id_list(values: list[str] | None) -> list[str]:
    if values is None:
        return []
    return [_normalise_token(value, "live_id") for value in values]


def _normalise_token(value: str, field_name: str) -> str:
    token = str(value).strip()
    if not token:
        raise ValueError(f"{field_name} must be non-empty")
    return token


def _optional_text(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _optional_float(value: Any) -> float | None:
    if value is None:
        return None
    if isinstance(value, bool):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None
