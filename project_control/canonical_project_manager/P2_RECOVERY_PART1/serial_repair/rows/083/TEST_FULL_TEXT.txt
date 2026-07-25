"""Tier A transform-boundary tests for the parallel risk lane."""

from __future__ import annotations

import ast
from pathlib import Path

from nvda_desk.contracts.parallel_risk import ParallelRiskEnvelope, ParallelRiskLanePacket

ACTIVE_PARALLEL_RISK_FILES = (
    Path("src/nvda_desk/contracts/parallel_risk.py"),
    Path("src/nvda_desk/domain/parallel_risk/candidate_audit.py"),
    Path("src/nvda_desk/domain/parallel_risk/environment_assessment.py"),
    Path("src/nvda_desk/risk/parallel/evaluate.py"),
    Path("src/nvda_desk/services/parallel_risk_lane_service.py"),
)

PROHIBITED_DONOR_IMPORT_PREFIXES = (
    "legacy_import",
    "nvda_desk.schemas.parallel_risk",
    "nvda_desk.schemas.risk_lane",
    "nvda_desk.services.parallel_risk_evaluator",
)

PROHIBITED_DONOR_SYMBOLS = {
    "LegacyParallelRiskEvaluator",
    "ParallelRiskWorkbookRow",
    "RiskLaneTransformBundle",
    "ImportedRiskEnvelopeShape",
}

PROHIBITED_DOWNSTREAM_FIELDS = {
    "authorised_deployable_pct",
    "authorised_notional_usd",
    "broker_order_id",
    "open_position_id",
    "position_size",
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


def test_active_parallel_risk_files_do_not_import_donor_risk_lane_stack() -> None:
    for path in ACTIVE_PARALLEL_RISK_FILES:
        imports = _imports_for(path)
        forbidden = {
            imported
            for imported in imports
            if any(
                imported == prefix or imported.startswith(f"{prefix}.")
                for prefix in PROHIBITED_DONOR_IMPORT_PREFIXES
            )
        }
        assert (
            forbidden == set()
        ), f"{path} imports donor parallel-risk stack modules: {sorted(forbidden)}"


def test_active_parallel_risk_files_do_not_redeclare_transform_required_donor_symbols() -> None:
    declared: set[str] = set()
    for path in ACTIVE_PARALLEL_RISK_FILES:
        declared.update(_top_level_defs_for(path))

    forbidden = declared & PROHIBITED_DONOR_SYMBOLS
    assert (
        forbidden == set()
    ), f"parallel-risk native files redeclare donor symbols: {sorted(forbidden)}"


def test_parallel_risk_envelope_and_lane_packet_remain_risk_only_carriers() -> None:
    envelope_fields = set(ParallelRiskEnvelope.model_fields)
    packet_fields = set(ParallelRiskLanePacket.model_fields)

    assert envelope_fields.isdisjoint(PROHIBITED_DOWNSTREAM_FIELDS)
    assert packet_fields.isdisjoint(PROHIBITED_DOWNSTREAM_FIELDS)
    assert ParallelRiskEnvelope().decision_authority == "independent_risk_envelope_only"
