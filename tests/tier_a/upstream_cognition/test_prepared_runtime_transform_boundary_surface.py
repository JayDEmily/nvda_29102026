from __future__ import annotations

import ast
import dataclasses
from pathlib import Path
from typing import get_type_hints

from nvda_desk.preparation.runtime_preparer import PreparedRuntimeDataset

ROOT = Path(__file__).resolve().parents[3]
SELECTED_NATIVE_FILES = (
    ROOT / "src/nvda_desk/preparation/runtime_preparer.py",
    ROOT / "src/nvda_desk/preparation/context_packet.py",
    ROOT / "src/nvda_desk/contracts/prepared_context.py",
)
PROHIBITED_IMPORT_PREFIXES = (
    "legacy_import",
    "nvda_desk.schemas.dataset",
    "nvda_desk.services.options_flow_context",
)
PROHIBITED_DONOR_SYMBOLS = {
    "EventRecord",
    "PreparedRuntimeFixturePack",
    "RealDataCognitionInputs",
    "RuntimeSnapshotSanityReport",
}
PROHIBITED_DONOR_DATASET_FIELDS = {
    "dataset_id",
    "symbol",
    "provenance",
    "events",
    "bars",
    "option_chain_snapshots",
}


def _imports_for(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    imports: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.add(node.module)
    return imports


def _defined_symbols(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    return {
        node.name for node in ast.walk(tree) if isinstance(node, (ast.ClassDef, ast.FunctionDef))
    }


def test_prepared_runtime_native_files_do_not_import_donor_dataset_or_service_surfaces() -> None:
    for path in SELECTED_NATIVE_FILES:
        imports = _imports_for(path)
        assert not {
            module for module in imports if module.startswith(PROHIBITED_IMPORT_PREFIXES)
        }, path


def test_prepared_runtime_dataset_remains_native_lean_carrier_not_donor_dataset_shape() -> None:
    assert dataclasses.is_dataclass(PreparedRuntimeDataset)
    assert not hasattr(PreparedRuntimeDataset, "model_validate")

    fields = set(get_type_hints(PreparedRuntimeDataset).keys())
    assert fields == {
        "snapshots",
        "dataset_lineage",
        "missing_optional_enrichments",
        "failed_enrichments",
    }
    assert fields.isdisjoint(PROHIBITED_DONOR_DATASET_FIELDS)


def test_prepared_runtime_native_files_do_not_redeclare_transform_required_donor_symbols() -> None:
    defined_symbols: set[str] = set()
    for path in SELECTED_NATIVE_FILES:
        defined_symbols.update(_defined_symbols(path))

    assert defined_symbols.isdisjoint(PROHIBITED_DONOR_SYMBOLS)
