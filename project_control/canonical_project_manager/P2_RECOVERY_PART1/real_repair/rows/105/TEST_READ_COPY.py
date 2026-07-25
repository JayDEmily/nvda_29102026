"""Tier A authority-boundary tests for live position/inventory architecture."""

from __future__ import annotations

import ast
import inspect
from pathlib import Path

from nvda_desk.contracts.downstream import (
    DownstreamLiveInventorySnapshot,
    InventoryExposureState,
    InventoryStateReceipt,
    LiveCapitalState,
    LivePositionState,
)
from nvda_desk.downstream.live_inventory import DownstreamLiveInventoryService

ACTIVE_LIVE_INVENTORY_FILES = (
    Path("src/nvda_desk/downstream/live_inventory.py"),
    Path("src/nvda_desk/domain/downstream/live_inventory.py"),
    Path("src/nvda_desk/services/downstream_live_inventory_service.py"),
    Path("src/nvda_desk/repositories/position_repository.py"),
    Path("src/nvda_desk/repositories/capital_state_repository.py"),
)

PROHIBITED_AUTHORITY_IMPORT_PREFIXES = (
    "nvda_desk.adapters.egress",
    "nvda_desk.capital",
    "nvda_desk.domain.capital",
    "nvda_desk.domain.downstream.opening",
    "nvda_desk.downstream.exit_close",
    "nvda_desk.downstream.opening",
    "nvda_desk.services.capital_deployment_service",
    "nvda_desk.services.downstream_opening_service",
    "nvda_desk.services.exit_close_service",
)

PROHIBITED_AUTHORITY_FIELDS = {
    "authorised_deployable_pct",
    "authorised_notional_usd",
    "broker_order_id",
    "capital_deployment_receipt_id",
    "execution_allowed",
    "immediate_opening_slice_pct",
    "opening_authorisation",
    "order_intent_preview",
    "placement_handoff",
    "readiness_state",
}

PROHIBITED_BUILD_PARAMETERS = {
    "authorised_deployable_pct",
    "broker_order_id",
    "capital_deployment_receipt_id",
    "execution_allowed",
    "order_intent_preview",
    "placement_handoff",
    "readiness_id",
}


def _imports_for(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    imports: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.add(node.module)
    return imports


def test_live_inventory_files_do_not_import_capital_opening_broker_or_exit_authority() -> None:
    for path in ACTIVE_LIVE_INVENTORY_FILES:
        imports = _imports_for(path)
        forbidden = {
            imported
            for imported in imports
            if any(
                imported == prefix or imported.startswith(f"{prefix}.")
                for prefix in PROHIBITED_AUTHORITY_IMPORT_PREFIXES
            )
        }
        assert (
            forbidden == set()
        ), f"{path} imports non-inventory authority modules: {sorted(forbidden)}"


def test_live_inventory_contract_fields_remain_inventory_only() -> None:
    inventory_contracts = (
        LivePositionState,
        LiveCapitalState,
        InventoryExposureState,
        InventoryStateReceipt,
        DownstreamLiveInventorySnapshot,
    )
    exposed_fields = set().union(*(contract.model_fields for contract in inventory_contracts))

    assert exposed_fields.isdisjoint(PROHIBITED_AUTHORITY_FIELDS)
    assert DownstreamLiveInventorySnapshot().policy_freeze_state == "architecture_only_no_policy"


def test_live_inventory_snapshot_builder_accepts_inventory_readback_inputs_only() -> None:
    signature = inspect.signature(DownstreamLiveInventoryService.build_live_snapshot)
    parameter_names = set(signature.parameters)

    assert parameter_names.isdisjoint(PROHIBITED_BUILD_PARAMETERS)
    assert {"self", "live_ids", "inventory_id", "capital_snapshot_id", "receipt_id"}.issubset(
        parameter_names
    )

def test_live_inventory_reconciliation_accepts_fill_evidence_inputs_only() -> None:
    signature = inspect.signature(DownstreamLiveInventoryService.reconcile_fill_evidence)
    parameter_names = set(signature.parameters)

    assert parameter_names.isdisjoint(PROHIBITED_BUILD_PARAMETERS)
    assert {
        "self",
        "fill_evidence",
        "reconciliation_id",
        "inventory_id",
        "capital_snapshot_id",
        "receipt_id",
    }.issubset(parameter_names)
