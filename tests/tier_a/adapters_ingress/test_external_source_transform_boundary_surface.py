from __future__ import annotations

import ast
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
ROW_5_1_FILES = [
    REPO_ROOT / "src/nvda_desk/contracts/external_source.py",
    REPO_ROOT / "src/nvda_desk/adapters/ingress/calendar_feed.py",
    REPO_ROOT / "src/nvda_desk/adapters/ingress/market_snapshot_feed.py",
    REPO_ROOT / "src/nvda_desk/adapters/ingress/options_surface_feed.py",
]
FORBIDDEN_CLIENT_IMPORT_ROOTS = {
    "aiohttp",
    "httpx",
    "ibapi",
    "openai",
    "requests",
    "websocket",
}
FORBIDDEN_DOMAIN_IMPORT_PREFIXES = (
    "nvda_desk.capital",
    "nvda_desk.downstream",
    "nvda_desk.repositories",
    "nvda_desk.risk",
    "nvda_desk.runtime",
)
FORBIDDEN_DONOR_AUTHORITY_NAMES = {
    "AllocationDecision",
    "AllocationEngine",
    "BrokerClient",
    "ExecutionClient",
    "LiveOrderGateway",
    "OvernightRiskAllocator",
    "PositionSizer",
}


def _imported_modules(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    imported: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module)
    return imported


def test_external_source_transform_boundary_does_not_import_live_client_libraries() -> None:
    imported_roots: set[str] = set()
    for path in ROW_5_1_FILES:
        imported_roots.update(
            module.split(".", maxsplit=1)[0] for module in _imported_modules(path)
        )

    assert imported_roots.isdisjoint(FORBIDDEN_CLIENT_IMPORT_ROOTS) is True


def test_external_source_transform_boundary_does_not_import_decision_or_persistence_owners() -> (
    None
):
    imported_modules: set[str] = set()
    for path in ROW_5_1_FILES:
        imported_modules.update(_imported_modules(path))

    for module in imported_modules:
        assert not module.startswith(FORBIDDEN_DOMAIN_IMPORT_PREFIXES), module


def test_external_source_transform_boundary_does_not_define_donor_authority_classes() -> None:
    defined_names: set[str] = set()
    for path in ROW_5_1_FILES:
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
                defined_names.add(node.name)

    assert defined_names.isdisjoint(FORBIDDEN_DONOR_AUTHORITY_NAMES) is True
