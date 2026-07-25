"""Tier A transform-boundary tests for live position/inventory architecture."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest
from pydantic import ValidationError

from nvda_desk.contracts.downstream import LiveCapitalState, LivePositionState
from nvda_desk.downstream.live_inventory import DownstreamLiveInventoryService
from nvda_desk.repositories.position_repository import PositionRepository

ACTIVE_LIVE_INVENTORY_FILES = (
    Path("src/nvda_desk/contracts/downstream.py"),
    Path("src/nvda_desk/downstream/live_inventory.py"),
    Path("src/nvda_desk/domain/downstream/live_inventory.py"),
    Path("src/nvda_desk/services/downstream_live_inventory_service.py"),
    Path("src/nvda_desk/repositories/position_repository.py"),
    Path("src/nvda_desk/repositories/capital_state_repository.py"),
)

PROHIBITED_DONOR_IMPORT_PREFIXES = (
    "legacy_import",
    "nvda_desk.schemas.import_registry",
    "nvda_desk.schemas.review",
    "nvda_desk.schemas.cognition",
    "nvda_desk.schemas.imported_modules.execution_lifecycle",
    "nvda_desk.schemas.imported_modules.posture_enrichers",
    "nvda_desk.services.imported_modules.execution_lifecycle",
    "nvda_desk.services.imported_modules.posture_enrichers",
    "nvda_desk.services.module_evaluators",
    "nvda_desk.services.options_flow_history",
    "nvda_desk.services.slv_replay",
    "nvda_desk.services.slv_experiments",
    "nvda_desk.services.cognition_runtime",
)

PROHIBITED_DONOR_SYMBOLS = {
    "ArchitectureRole",
    "CandidateComparisonContext",
    "CandidateGovernanceSurface",
    "DeskCognitionRuntime",
    "ExecutionLifecycleService",
    "FillBiasAdjusterContractOutput",
    "FillFeedbackRouterContractOutput",
    "LadderReplayRungOutcome",
    "OptionsFlowHistoryWriteResult",
    "PostureRiskInput",
    "ReviewGovernanceSurface",
    "StrategicLadderExperimentService",
    "StrategicLadderValidatorOutput",
    "StrategicLadderValidatorService",
}

DONOR_TRANSFORM_PAYLOAD_KEYS = {
    "adjudication_disposition",
    "candidate_shape",
    "champion_candidate_id",
    "comparison_outcome",
    "execution_context_score",
    "fill_bias_adjuster",
    "fill_feedback_router",
    "FillBiasAdjusterContractOutput",
    "FillFeedbackRouterContractOutput",
    "LadderReplayRungOutcome",
    "override_disposition",
    "PostureRiskInput",
    "risk_budget_remaining_pct",
    "shadow_challenger_ids",
    "StrategicLadderValidatorOutput",
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


def test_live_inventory_files_do_not_import_transform_required_donor_stacks() -> None:
    for path in ACTIVE_LIVE_INVENTORY_FILES:
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
        ), f"{path} imports transform-required donor stacks: {sorted(forbidden)}"


def test_live_inventory_files_do_not_redeclare_transform_required_donor_symbols() -> None:
    declared: set[str] = set()
    for path in ACTIVE_LIVE_INVENTORY_FILES:
        declared.update(_top_level_defs_for(path))

    forbidden = declared & PROHIBITED_DONOR_SYMBOLS
    assert forbidden == set(), f"live-inventory files redeclare donor symbols: {sorted(forbidden)}"


@pytest.mark.parametrize(
    ("model_type", "identity_field"),
    (
        (LivePositionState, {"position_id": "pos-1"}),
        (LiveCapitalState, {"snapshot_id": "cap-1"}),
    ),
)
def test_live_inventory_contracts_reject_transform_required_donor_payload_keys(
    model_type, identity_field: dict[str, str]
) -> None:
    donor_payload = {
        "symbol": "NVDA",
        "metadata": {
            "candidate_shape": "shadow_challenger",
            "FillBiasAdjusterContractOutput": {"execution_context_score": 0.8},
        },
    }

    with pytest.raises(ValidationError, match="transform-required donor"):
        model_type(**identity_field, source_payload=donor_payload)


def test_live_inventory_snapshot_builder_rejects_repository_donor_transform_payloads() -> None:
    positions = PositionRepository()
    positions.write_position(
        "pos-1",
        {
            "symbol": "NVDA",
            "declared_exposure": 1.0,
            "metadata": {"fill_feedback_router": {"status": "donor-shape"}},
        },
    )

    with pytest.raises(ValidationError, match="transform-required donor"):
        DownstreamLiveInventoryService(position_repository=positions).build_live_snapshot()


def test_live_inventory_transform_guard_list_covers_row037_donor_payload_markers() -> None:
    assert {
        "candidate_shape",
        "FillBiasAdjusterContractOutput",
        "fill_feedback_router",
        "StrategicLadderValidatorOutput",
    }.issubset(DONOR_TRANSFORM_PAYLOAD_KEYS)
