from __future__ import annotations

import importlib

import pytest
from pydantic import ValidationError

from nvda_desk.contracts.downstream import (
    DownstreamLiveInventorySnapshot,
    InventoryExposureState,
    InventoryStateReceipt,
    LiveCapitalState,
    LivePositionState,
)


def _require_module(module_path: str):
    try:
        return importlib.import_module(module_path)
    except ModuleNotFoundError as exc:
        pytest.fail(f"Required module is not implemented: {module_path} ({exc})")


def _require_attr(module, attr_name: str):
    if not hasattr(module, attr_name):
        pytest.fail(f"Required attribute is not implemented: {module.__name__}.{attr_name}")
    return getattr(module, attr_name)


def test_downstream_contract_models_are_present() -> None:
    contracts = _require_module("nvda_desk.contracts.downstream")
    assert contracts.__name__ == "nvda_desk.contracts.downstream"

    assert _require_attr(contracts, "DownstreamStateReadResult") is getattr(
        contracts, "DownstreamStateReadResult"
    )
    assert _require_attr(contracts, "DownstreamStateSnapshot") is getattr(
        contracts, "DownstreamStateSnapshot"
    )
    assert _require_attr(contracts, "DownstreamArchitectureReceipt") is getattr(
        contracts, "DownstreamArchitectureReceipt"
    )
    assert _require_attr(contracts, "DownstreamOpeningSnapshot") is getattr(
        contracts, "DownstreamOpeningSnapshot"
    )
    assert _require_attr(contracts, "DownstreamLiveInventorySnapshot") is getattr(
        contracts, "DownstreamLiveInventorySnapshot"
    )
    assert _require_attr(contracts, "LivePositionState") is getattr(contracts, "LivePositionState")
    assert _require_attr(contracts, "LiveCapitalState") is getattr(contracts, "LiveCapitalState")
    assert _require_attr(contracts, "InventoryExposureState") is getattr(
        contracts, "InventoryExposureState"
    )
    assert _require_attr(contracts, "InventoryStateReceipt") is getattr(
        contracts, "InventoryStateReceipt"
    )


def test_live_inventory_contract_forbids_hidden_authority_fields() -> None:
    with pytest.raises(ValidationError):
        DownstreamLiveInventorySnapshot(
            live_ids=["pos-1"],
            broker_order_id="hidden-broker-authority",
        )


def test_live_inventory_contract_carries_position_capital_exposure_and_receipt() -> None:
    snapshot = DownstreamLiveInventorySnapshot(
        inventory_id="inventory-1",
        live_ids=["pos-1"],
        position_states=[LivePositionState(position_id="pos-1", source_payload={"symbol": "NVDA"})],
        capital_state=LiveCapitalState(snapshot_id="cap-1", source_payload={"cash": 1000}),
        exposure_state=InventoryExposureState(
            position_count=1,
            open_position_ids=["pos-1"],
            declared_exposure_by_symbol={"NVDA": 12.5},
        ),
        inventory_receipt=InventoryStateReceipt(
            receipt_id="receipt-1",
            inventory_id="inventory-1",
            position_ids=["pos-1"],
            capital_snapshot_id="cap-1",
        ),
    )

    assert snapshot.policy_freeze_state == "architecture_only_no_policy"
    assert snapshot.capital_state is not None
    assert snapshot.exposure_state.declared_exposure_by_symbol == {"NVDA": 12.5}


def test_inventory_state_receipt_rejects_broker_or_execution_authority_fields() -> None:
    with pytest.raises(ValidationError):
        InventoryStateReceipt(
            receipt_id="receipt-1",
            inventory_id="inventory-1",
            broker_order_id="hidden-broker-authority",
        )


def test_live_inventory_contracts_detach_nested_caller_owned_payload_state() -> None:
    position_payload = {"symbol": "NVDA", "metadata": {"source": "fill"}}
    capital_payload = {"cash": 1000.0, "metadata": {"source": "ledger"}}
    position_state = LivePositionState(position_id="pos-1", source_payload=position_payload)
    capital_state = LiveCapitalState(snapshot_id="cap-1", source_payload=capital_payload)
    snapshot = DownstreamLiveInventorySnapshot(
        inventory_id="inventory-1",
        live_ids=["pos-1"],
        position_states=[position_state],
        capital_state=capital_state,
    )

    position_payload["metadata"]["source"] = "caller-mutated"
    capital_payload["metadata"]["source"] = "caller-mutated"
    position_state.source_payload["metadata"]["source"] = "state-mutated"
    capital_state.source_payload["metadata"]["source"] = "state-mutated"

    assert snapshot.position_states[0].source_payload == {
        "symbol": "NVDA",
        "metadata": {"source": "fill"},
    }
    assert snapshot.capital_state is not None
    assert snapshot.capital_state.source_payload == {
        "cash": 1000.0,
        "metadata": {"source": "ledger"},
    }
