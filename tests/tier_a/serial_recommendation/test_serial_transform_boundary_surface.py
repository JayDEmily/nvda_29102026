"""Tier A transform-boundary tests for the serial desk-cognition spine."""

from __future__ import annotations

import ast
from collections.abc import Iterable
from pathlib import Path

from nvda_desk.contracts.execution import ExecutionExpressionOutput
from nvda_desk.domain.execution.lifecycle_plan import build_lifecycle_plan

ACTIVE_SERIAL_FILES = (
    Path("src/nvda_desk/cognition/serial/__init__.py"),
    Path("src/nvda_desk/cognition/serial/eligibility.py"),
    Path("src/nvda_desk/cognition/serial/options_flow.py"),
    Path("src/nvda_desk/cognition/serial/posture.py"),
    Path("src/nvda_desk/contracts/execution.py"),
    Path("src/nvda_desk/contracts/serial_spine.py"),
    Path("src/nvda_desk/domain/execution/__init__.py"),
    Path("src/nvda_desk/domain/execution/candidate_expression.py"),
    Path("src/nvda_desk/domain/execution/lifecycle_plan.py"),
    Path("src/nvda_desk/services/execution_service.py"),
)

PROHIBITED_DONOR_IMPORT_PREFIXES = (
    "legacy_import",
    "nvda_desk.schemas.cognition",
    "nvda_desk.schemas.execution",
    "nvda_desk.services.imported_market_context_synthesis",
)

PROHIBITED_DONOR_SYMBOLS = {
    "ImportedMarketContextSynthesis",
    "LegacyCognitionExtraction",
    "LegacyExecutionRecordShape",
    "RuntimeExecutionDecisionBundle",
}

PROHIBITED_DOWNSTREAM_LIFECYCLE_TERMS = {
    "broker_order_id",
    "capital_deployment_authority",
    "open_position",
    "order_placement",
    "position_sizing",
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


def _top_level_defs_for(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    return {
        node.name
        for node in tree.body
        if isinstance(node, ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef)
    }


def _flatten_terms(value: object) -> Iterable[str]:
    if isinstance(value, dict):
        for key, child in value.items():
            yield str(key)
            yield from _flatten_terms(child)
    elif isinstance(value, (list, tuple, set)):
        for child in value:
            yield from _flatten_terms(child)
    elif value is not None:
        yield str(value)


def test_active_serial_files_do_not_import_donor_cognition_or_execution_stacks() -> None:
    for path in ACTIVE_SERIAL_FILES:
        imports = _imports_for(path)
        forbidden = {
            imported
            for imported in imports
            if any(
                imported == prefix or imported.startswith(f"{prefix}.")
                for prefix in PROHIBITED_DONOR_IMPORT_PREFIXES
            )
        }
        assert forbidden == set(), f"{path} imports donor serial stack modules: {sorted(forbidden)}"


def test_active_serial_files_do_not_redeclare_transform_required_donor_symbols() -> None:
    declared: set[str] = set()
    for path in ACTIVE_SERIAL_FILES:
        declared.update(_top_level_defs_for(path))

    forbidden = declared & PROHIBITED_DONOR_SYMBOLS
    assert forbidden == set(), f"serial native files redeclare donor symbols: {sorted(forbidden)}"


def test_serial_lifecycle_plan_remains_candidate_material_not_opening_or_capital_payload() -> None:
    plan = build_lifecycle_plan(
        ExecutionExpressionOutput(
            lead_playbook_id="playbook::demo",
            active_playbook_ids=["playbook::demo"],
        )
    )

    emitted_terms = set(_flatten_terms(plan))
    assert emitted_terms.isdisjoint(PROHIBITED_DOWNSTREAM_LIFECYCLE_TERMS)
