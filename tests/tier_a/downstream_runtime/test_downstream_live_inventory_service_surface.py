from __future__ import annotations

import ast
import importlib
from pathlib import Path

import pytest

from nvda_desk.downstream.live_inventory import DownstreamLiveInventoryService
from nvda_desk.services.downstream_live_inventory_service import (
    DownstreamLiveInventoryService as WorkbookDownstreamLiveInventoryService,
)
from nvda_desk.persistence.receipt_ledger import ReceiptLedger
from nvda_desk.repositories.capital_state_repository import CapitalStateRepository
from nvda_desk.repositories.position_repository import PositionRepository


def _require_module(module_path: str):
    try:
        return importlib.import_module(module_path)
    except ModuleNotFoundError as exc:
        pytest.fail(f"Required module is not implemented: {module_path} ({exc})")


def _require_attr(module, attr_name: str):
    if not hasattr(module, attr_name):
        pytest.fail(f"Required attribute is not implemented: {module.__name__}.{attr_name}")
    return getattr(module, attr_name)


def test_downstream_live_inventory_service_surface_is_present() -> None:
    live_inventory = _require_module("nvda_desk.downstream.live_inventory")
    assert live_inventory.__name__ == "nvda_desk.downstream.live_inventory"
    assert _require_attr(live_inventory, "DownstreamLiveInventoryService") is getattr(live_inventory, "DownstreamLiveInventoryService")


def test_live_inventory_snapshot_reads_position_and_capital_state_copy_safely() -> None:
    positions = PositionRepository()
    capital = CapitalStateRepository()
    positions.write_position(
        "pos-1",
        {"symbol": "NVDA", "declared_exposure": 12.5, "metadata": {"source": "fill"}},
    )
    capital.write_snapshot("cap-1", {"cash": 1000.0, "metadata": {"source": "ledger"}})

    snapshot = DownstreamLiveInventoryService(
        position_repository=positions,
        capital_state_repository=capital,
    ).build_live_snapshot(receipt_id="inv-r1")

    assert snapshot.live_ids == ["pos-1"]
    assert snapshot.position_states[0].position_id == "pos-1"
    assert snapshot.position_states[0].source_payload["metadata"] == {"source": "fill"}
    assert snapshot.capital_state is not None
    assert snapshot.capital_state.snapshot_id == "cap-1"
    assert snapshot.exposure_state.position_count == 1
    assert snapshot.exposure_state.declared_exposure_by_symbol == {"NVDA": 12.5}
    assert snapshot.inventory_receipt is not None
    assert snapshot.inventory_receipt.position_ids == ["pos-1"]
    assert snapshot.inventory_receipt.capital_snapshot_id == "cap-1"

    snapshot.position_states[0].source_payload["metadata"]["source"] = "mutated"
    assert positions.read_position("pos-1") == {
        "symbol": "NVDA",
        "declared_exposure": 12.5,
        "metadata": {"source": "fill"},
    }


def test_live_inventory_receipt_write_is_explicit_and_append_only() -> None:
    positions = PositionRepository()
    receipts = ReceiptLedger()
    positions.write_position("pos-1", {"symbol": "NVDA", "declared_exposure": 1.5})

    service = DownstreamLiveInventoryService(
        position_repository=positions,
        receipt_ledger=receipts,
    )
    snapshot = service.build_live_snapshot(receipt_id="inv-r1")

    stored = receipts.read_receipt("inv-r1")
    assert stored is not None
    assert stored["receipt_kind"] == "live_inventory_snapshot"
    assert stored["payload"] == snapshot.inventory_receipt.model_dump()
    with pytest.raises(ValueError, match="duplicate receipt_id"):
        service.build_live_snapshot(receipt_id="inv-r1")


def test_live_inventory_does_not_invent_undeclared_exposure() -> None:
    positions = PositionRepository()
    positions.write_position("pos-1", {"symbol": "NVDA", "quantity": 100})

    snapshot = DownstreamLiveInventoryService(position_repository=positions).build_live_snapshot()

    assert snapshot.exposure_state.open_position_ids == ["pos-1"]
    assert snapshot.exposure_state.declared_exposure_by_symbol == {}


def test_live_inventory_module_does_not_import_broker_or_candidate_authority() -> None:
    source = Path("src/nvda_desk/downstream/live_inventory.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module)

    forbidden_roots = (
        "nvda_desk.adapters.egress",
        "nvda_desk.domain.execution",
        "nvda_desk.cognition.serial",
        "nvda_desk.ingress.raw_bundle_loader",
    )
    assert not any(
        module == root or module.startswith(root + ".")
        for module in imported
        for root in forbidden_roots
    )


def test_live_inventory_rejects_empty_live_inventory_identifiers() -> None:
    service = DownstreamLiveInventoryService()

    with pytest.raises(ValueError, match="live_id must be non-empty"):
        service.build_live_snapshot(live_ids=["  "])

    with pytest.raises(ValueError, match="inventory_id must be non-empty"):
        service.build_live_snapshot(inventory_id="  ")

    with pytest.raises(ValueError, match="receipt_id must be non-empty"):
        service.build_live_snapshot(receipt_id="  ")


def test_live_inventory_requested_ids_are_normalised_before_repository_read() -> None:
    positions = PositionRepository()
    positions.write_position("pos-1", {"symbol": "NVDA", "declared_exposure": 2.5})

    snapshot = DownstreamLiveInventoryService(position_repository=positions).build_live_snapshot(
        live_ids=[" pos-1 "]
    )

    assert snapshot.live_ids == ["pos-1"]
    assert snapshot.position_states[0].position_id == "pos-1"
    assert snapshot.exposure_state.declared_exposure_by_symbol == {"NVDA": 2.5}


def test_live_inventory_reads_requested_capital_snapshot_not_latest_snapshot() -> None:
    positions = PositionRepository()
    capital = CapitalStateRepository()
    positions.write_position("pos-1", {"symbol": "NVDA", "declared_exposure": 1.0})
    capital.write_snapshot("cap-1", {"cash": 1000.0})
    capital.write_snapshot("cap-2", {"cash": 900.0})

    snapshot = DownstreamLiveInventoryService(
        position_repository=positions,
        capital_state_repository=capital,
    ).build_live_snapshot(capital_snapshot_id=" cap-1 ")

    assert snapshot.capital_state is not None
    assert snapshot.capital_state.snapshot_id == "cap-1"
    assert snapshot.capital_state.source_payload == {"cash": 1000.0}


def test_workbook_live_inventory_wrapper_preserves_bounded_readback_inputs() -> None:
    positions = PositionRepository()
    capital = CapitalStateRepository()
    receipts = ReceiptLedger()
    positions.write_position("pos-1", {"symbol": "NVDA", "declared_exposure": 3.0})
    capital.write_snapshot("cap-older", {"cash": 1000.0})
    capital.write_snapshot("cap-selected", {"cash": 900.0})

    snapshot = WorkbookDownstreamLiveInventoryService(
        position_repository=positions,
        capital_state_repository=capital,
        receipt_ledger=receipts,
    ).build_live_snapshot(
        live_ids=[" pos-1 "],
        inventory_id=" inv-1 ",
        capital_snapshot_id=" cap-selected ",
        receipt_id=" receipt-1 ",
    )

    assert snapshot.inventory_id == "inv-1"
    assert snapshot.live_ids == ["pos-1"]
    assert snapshot.capital_state is not None
    assert snapshot.capital_state.snapshot_id == "cap-selected"
    assert snapshot.inventory_receipt is not None
    assert snapshot.inventory_receipt.receipt_id == "receipt-1"
    assert snapshot.inventory_receipt.inventory_id == "inv-1"
    assert snapshot.inventory_receipt.capital_snapshot_id == "cap-selected"
    stored = receipts.read_receipt("receipt-1")
    assert stored is not None
    assert stored["payload"] == snapshot.inventory_receipt.model_dump()


def test_live_inventory_reconciles_executed_fill_evidence_into_position_state() -> None:
    positions = PositionRepository()
    receipts = ReceiptLedger()
    service = DownstreamLiveInventoryService(
        position_repository=positions,
        receipt_ledger=receipts,
    )

    snapshot = service.reconcile_fill_evidence(
        [
            {
                "fill_evidence_id": "fill-1",
                "position_id": " pos-1 ",
                "symbol": "NVDA",
                "declared_exposure_delta": 12.5,
                "filled_quantity": 5,
                "source": "execution_event_repository",
            },
            {
                "fill_evidence_id": "fill-2",
                "position_id": "pos-1",
                "symbol": "NVDA",
                "declared_exposure_delta": -2.5,
                "filled_quantity": -1,
                "source": "execution_event_repository",
            },
        ],
        reconciliation_id=" recon-1 ",
        inventory_id=" inv-reconciled ",
        receipt_id=" receipt-recon-1 ",
    )

    assert snapshot.inventory_id == "inv-reconciled"
    assert snapshot.live_ids == ["pos-1"]
    assert snapshot.exposure_state.declared_exposure_by_symbol == {"NVDA": 10.0}
    assert positions.read_position("pos-1") == {
        "symbol": "NVDA",
        "declared_exposure": 10.0,
        "fill_evidence_ids": ["fill-1", "fill-2"],
        "fill_evidence": [
            {
                "fill_evidence_id": "fill-1",
                "position_id": "pos-1",
                "symbol": "NVDA",
                "declared_exposure_delta": 12.5,
                "filled_quantity": 5,
                "source": "execution_event_repository",
            },
            {
                "fill_evidence_id": "fill-2",
                "position_id": "pos-1",
                "symbol": "NVDA",
                "declared_exposure_delta": -2.5,
                "filled_quantity": -1,
                "source": "execution_event_repository",
            },
        ],
        "inventory_reconciliation_id": "recon-1",
    }
    assert snapshot.inventory_receipt is not None
    assert snapshot.inventory_receipt.receipt_id == "receipt-recon-1"
    assert snapshot.inventory_receipt.position_ids == ["pos-1"]
    stored = receipts.read_receipt("receipt-recon-1")
    assert stored is not None
    assert stored["receipt_kind"] == "live_inventory_reconciliation"
    assert stored["payload"]["reconciliation_id"] == "recon-1"
    assert stored["payload"]["fill_evidence_ids"] == ["fill-1", "fill-2"]


def test_live_inventory_reconciliation_requires_explicit_fill_evidence_identity() -> None:
    service = DownstreamLiveInventoryService(position_repository=PositionRepository())

    with pytest.raises(ValueError, match="fill_evidence_id must be non-empty"):
        service.reconcile_fill_evidence(
            [{"fill_evidence_id": "  ", "position_id": "pos-1"}],
            reconciliation_id="recon-1",
        )

    with pytest.raises(ValueError, match="position_id must be non-empty"):
        service.reconcile_fill_evidence(
            [{"fill_evidence_id": "fill-1", "position_id": "  "}],
            reconciliation_id="recon-1",
        )


def test_live_inventory_reconciliation_rejects_placement_authority_keys() -> None:
    service = DownstreamLiveInventoryService(position_repository=PositionRepository())

    with pytest.raises(ValueError, match="placement authority keys: broker_order_id"):
        service.reconcile_fill_evidence(
            [
                {
                    "fill_evidence_id": "fill-1",
                    "position_id": "pos-1",
                    "broker_order_id": "broker-1",
                }
            ],
            reconciliation_id="recon-1",
        )

def test_live_inventory_reconciliation_rejects_empty_fill_evidence() -> None:
    service = DownstreamLiveInventoryService(position_repository=PositionRepository())

    with pytest.raises(ValueError, match="fill_evidence must contain at least one event"):
        service.reconcile_fill_evidence([], reconciliation_id="recon-1")


def test_live_inventory_reconciliation_rejects_duplicate_fill_evidence_identity_before_mutation() -> None:
    positions = PositionRepository()
    service = DownstreamLiveInventoryService(position_repository=positions)

    with pytest.raises(ValueError, match="duplicate fill_evidence_id: fill-1"):
        service.reconcile_fill_evidence(
            [
                {
                    "fill_evidence_id": "fill-1",
                    "position_id": "pos-1",
                    "symbol": "NVDA",
                    "declared_exposure_delta": 1.0,
                },
                {
                    "fill_evidence_id": " fill-1 ",
                    "position_id": "pos-1",
                    "symbol": "NVDA",
                    "declared_exposure_delta": 99.0,
                },
            ],
            reconciliation_id="recon-1",
        )

    assert positions.read_position("pos-1") is None


def test_live_inventory_reconciliation_rejects_replayed_fill_evidence_identity_without_double_counting() -> None:
    positions = PositionRepository()
    positions.write_position(
        "pos-1",
        {
            "symbol": "NVDA",
            "declared_exposure": 10.0,
            "fill_evidence_ids": ["fill-1"],
            "fill_evidence": [{"fill_evidence_id": "fill-1", "position_id": "pos-1"}],
        },
    )
    service = DownstreamLiveInventoryService(position_repository=positions)

    with pytest.raises(ValueError, match="duplicate fill_evidence_id: fill-1"):
        service.reconcile_fill_evidence(
            [
                {
                    "fill_evidence_id": "fill-1",
                    "position_id": "pos-1",
                    "symbol": "NVDA",
                    "declared_exposure_delta": 99.0,
                }
            ],
            reconciliation_id="recon-2",
        )

    assert positions.read_position("pos-1") == {
        "symbol": "NVDA",
        "declared_exposure": 10.0,
        "fill_evidence_ids": ["fill-1"],
        "fill_evidence": [{"fill_evidence_id": "fill-1", "position_id": "pos-1"}],
    }
