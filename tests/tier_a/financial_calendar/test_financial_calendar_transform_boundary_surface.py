from __future__ import annotations

import ast
from pathlib import Path

FINANCIAL_CALENDAR_NATIVE_FILES = (
    Path("src/nvda_desk/contracts/reference_data.py"),
    Path("src/nvda_desk/calendar/reference/importer.py"),
    Path("src/nvda_desk/calendar/reference/projection.py"),
    Path("src/nvda_desk/calendar/operational/events.py"),
    Path("src/nvda_desk/adapters/ingress/calendar_feed.py"),
)

PROHIBITED_OWNER_IMPORT_PREFIXES = (
    "legacy_import",
    "nvda_desk.services.event_store",
    "nvda_desk.services.event_ingestion",
    "nvda_desk.cognition",
    "nvda_desk.risk",
    "nvda_desk.downstream",
    "nvda_desk.broker",
    "nvda_desk.runtime",
)

PROHIBITED_DONOR_SYMBOL_NAMES = {
    "EventStoreService",
    "EventIngestionService",
    "EventStoreQuery",
    "LiveEventStore",
    "normalise_event_ingestion",
    "build_live_event_snapshot",
}


def _module(path: Path) -> ast.Module:
    return ast.parse(path.read_text(encoding="utf-8"), filename=str(path))


def test_financial_calendar_native_files_do_not_import_donor_event_services_or_runtime_owners() -> None:
    violations: list[str] = []
    for path in FINANCIAL_CALENDAR_NATIVE_FILES:
        for node in ast.walk(_module(path)):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name.startswith(PROHIBITED_OWNER_IMPORT_PREFIXES):
                        violations.append(f"{path}:{alias.name}")
            elif isinstance(node, ast.ImportFrom) and node.module:
                if node.module.startswith(PROHIBITED_OWNER_IMPORT_PREFIXES):
                    violations.append(f"{path}:{node.module}")

    assert violations == []


def test_financial_calendar_native_files_do_not_recreate_donor_event_service_symbols() -> None:
    observed_symbols: set[str] = set()
    for path in FINANCIAL_CALENDAR_NATIVE_FILES:
        for node in ast.walk(_module(path)):
            if isinstance(node, ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef):
                observed_symbols.add(node.name)

    assert observed_symbols.isdisjoint(PROHIBITED_DONOR_SYMBOL_NAMES)
