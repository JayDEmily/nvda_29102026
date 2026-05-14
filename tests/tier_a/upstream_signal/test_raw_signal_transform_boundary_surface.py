from __future__ import annotations

import ast
from pathlib import Path

RAW_SIGNAL_NATIVE_FILES = (
    Path("src/nvda_desk/contracts/upstream_signal.py"),
    Path("src/nvda_desk/upstream/raw_signal_coverage.py"),
    Path("src/nvda_desk/upstream/raw_signal_ingress.py"),
    Path("src/nvda_desk/contracts/dataset_packets.py"),
)

PROHIBITED_OWNER_IMPORT_PREFIXES = (
    "legacy_import",
    "nvda_desk.schemas",
    "nvda_desk.modules",
    "nvda_desk.services",
    "nvda_desk.cognition",
    "nvda_desk.risk",
    "nvda_desk.downstream",
    "nvda_desk.repositories",
    "nvda_desk.runtime",
)

PROHIBITED_DONOR_SYMBOL_NAMES = {
    "OptionSurfaceQuery",
    "OptionSurfaceResponse",
    "OptionType",
    "OptionsSnapshot",
    "RawSignalPreparationService",
    "RawSignalSchema",
    "SignalPreparationRuntime",
}


def _module(path: Path) -> ast.Module:
    return ast.parse(path.read_text(encoding="utf-8"), filename=str(path))


def test_raw_signal_native_files_do_not_import_donor_or_runtime_owners() -> None:
    violations: list[str] = []
    for path in RAW_SIGNAL_NATIVE_FILES:
        for node in ast.walk(_module(path)):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name.startswith(PROHIBITED_OWNER_IMPORT_PREFIXES):
                        violations.append(f"{path}:{alias.name}")
            elif isinstance(node, ast.ImportFrom) and node.module:
                if node.module.startswith(PROHIBITED_OWNER_IMPORT_PREFIXES):
                    violations.append(f"{path}:{node.module}")

    assert violations == []


def test_raw_signal_native_files_do_not_recreate_donor_schema_or_preparation_symbols() -> None:
    observed_symbols: set[str] = set()
    for path in RAW_SIGNAL_NATIVE_FILES:
        for node in ast.walk(_module(path)):
            if isinstance(node, ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef):
                observed_symbols.add(node.name)

    assert observed_symbols.isdisjoint(PROHIBITED_DONOR_SYMBOL_NAMES)
