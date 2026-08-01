from __future__ import annotations

import ast
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest
from pydantic import ValidationError

from nvda_desk.contracts.eligibility import PlaybookEligibilityOutput
from nvda_desk.contracts.execution import (
    ExecutionExpressionInput,
    ExecutionExpressionOutput,
    StageLocalHandoffSurface,
)
from nvda_desk.contracts.options_flow import OptionsFlowContextInput, OptionsFlowContextOutput
from nvda_desk.contracts.posture import PermissionState
from nvda_desk.contracts.regime import MarketRegimeContextInput, MarketRegimeContextOutput
from nvda_desk.contracts.serial_spine import (
    SERIAL_SPINE_PROHIBITED_AUTHORITIES,
    SERIAL_SPINE_STAGE_ORDER,
    SERIAL_STAGE_DEPENDENCIES,
    SERIAL_STAGE_LINEAGE_TAGS,
    copy_serial_spine_contract,
    serial_spine_contract,
    validate_serial_stage_dependencies,
)
from nvda_desk.contracts.stage_inputs import StageInputBundle
from nvda_desk.contracts.temporal import TemporalContextInput, TemporalContextOutput
from nvda_desk.domain.execution.candidate_expression import evaluate_execution_expression
from nvda_desk.runtime.orchestrator import DeskRuntimeOrchestrator
from nvda_desk.services.execution_service import ExecutionService

ROOT = Path(__file__).resolve().parents[3]
SELECTED_NATIVE_FILES = (
    ROOT / "src/nvda_desk/contracts/serial_spine.py",
    ROOT / "src/nvda_desk/contracts/execution.py",
    ROOT / "src/nvda_desk/contracts/stage_inputs.py",
    ROOT / "src/nvda_desk/contracts/temporal.py",
    ROOT / "src/nvda_desk/contracts/regime.py",
    ROOT / "src/nvda_desk/contracts/options_flow.py",
    ROOT / "src/nvda_desk/contracts/posture.py",
    ROOT / "src/nvda_desk/contracts/eligibility.py",
    ROOT / "src/nvda_desk/runtime/orchestrator.py",
    ROOT / "src/nvda_desk/domain/execution/candidate_expression.py",
    ROOT / "src/nvda_desk/services/temporal_context_service.py",
    ROOT / "src/nvda_desk/services/regime_context_service.py",
    ROOT / "src/nvda_desk/services/options_flow_context_service.py",
    ROOT / "src/nvda_desk/services/posture_service.py",
    ROOT / "src/nvda_desk/services/playbook_eligibility_service.py",
    ROOT / "src/nvda_desk/services/execution_service.py",
)
PROHIBITED_IMPORT_PREFIXES = (
    "legacy_import",
    "nvda_desk.schemas.imported_modules",
    "nvda_desk.services.imported_modules",
)
PROHIBITED_DONOR_SYMBOLS = {
    "ArchetypeMatcherContractOutput",
    "ArchetypeTaggerContractOutput",
    "CompressionRegimeDetectorContractOutput",
    "ContextScannerContractBase",
    "ContextScannerContext",
    "ContextScannerPayload",
    "ContractComputationMode",
    "ContractDependencyFence",
    "ContractDependencyStatus",
    "ConvictionTierAllocatorContractOutput",
    "EngineScoreContractOutput",
    "EntryGateContractOutput",
    "EventFlagCaptureContractOutput",
    "ExecutionContextScoreContractOutput",
    "GammaPressureContractOutput",
    "IvVsRvAnalysisContractOutput",
    "LadderConstructorContractOutput",
    "MacroAdaptiveWeightingFilterContractOutput",
    "MacroSignalScoreContractOutput",
    "MarketContextSynthesisContext",
    "MarketContextSynthesisContractBase",
    "MarketContextSynthesisContractEmission",
    "MarketContextSynthesisContractService",
    "MarketContextSynthesisPayload",
    "ModelConfidenceScorerContractOutput",
    "ObvViFlowConfirmationContractOutput",
    "OptionsBehaviourClusterContractOutput",
    "PeerDivergenceContractOutput",
    "PostureEnricherContext",
    "PostureEnricherContractBase",
    "PostureEnricherPayload",
    "RunSignalScanContractOutput",
    "SignalConflictDetectorContractOutput",
    "SkewInflectionContractOutput",
    "TailHedgeInjectorContractOutput",
    "TrancheAContractBase",
    "TrancheAImportedPayload",
    "TrancheAUpstreamContext",
    "VixSpreadDetectorContractOutput",
    "VolCorridorContractOutput",
    "VolumeSpikeFilterContractOutput",
}

REOPENED_ROW_CASES = (
    ("FWD012-AUDIT-001", "atlas_donor_module_002", "serial_contract_descriptor"),
    ("FWD012-AUDIT-002", "atlas_donor_cognition_001", "native_transform_boundary"),
    ("FWD012-AUDIT-003", "atlas_donor_cognition_003", "bounded_state_carriers"),
    ("FWD012-AUDIT-004", "atlas_donor_cognition_004", "bounded_state_carriers"),
    ("FWD012-AUDIT-005", "atlas_donor_cognition_005", "bounded_state_carriers"),
    ("FWD012-AUDIT-006", "atlas_donor_cognition_006", "bounded_state_carriers"),
    ("FWD012-AUDIT-007", "atlas_donor_cognition_007", "bounded_state_carriers"),
    ("FWD012-AUDIT-008", "atlas_donor_cognition_010", "bounded_state_carriers"),
    ("FWD012-AUDIT-009", "atlas_donor_cognition_015", "typed_stage_input_carriage"),
    ("FWD012-AUDIT-010", "atlas_donor_cognition_017", "typed_stage_input_carriage"),
    ("FWD012-AUDIT-011", "atlas_donor_cognition_018", "stage_packet_lineage"),
    ("FWD012-AUDIT-012", "atlas_donor_cognition_019", "typed_stage_input_carriage"),
    ("FWD012-AUDIT-013", "atlas_donor_cognition_020", "typed_stage_input_carriage"),
    ("FWD012-AUDIT-014", "atlas_donor_cognition_021", "typed_stage_input_carriage"),
    ("FWD012-AUDIT-015", "atlas_donor_cognition_038", "execution_recommendation_boundary"),
    ("FWD012-AUDIT-016", "atlas_donor_cognition_039", "bounded_state_carriers"),
    ("FWD012-AUDIT-017", "atlas_donor_cognition_040", "execution_recommendation_boundary"),
    ("FWD012-AUDIT-018", "atlas_donor_cognition_041", "execution_recommendation_boundary"),
    ("FWD012-AUDIT-019", "atlas_donor_cognition_050", "stage_packet_lineage"),
    ("FWD012-AUDIT-020", "atlas_donor_cognition_052", "stage_packet_lineage"),
    ("FWD012-AUDIT-021", "atlas_donor_cognition_054", "stage_packet_lineage"),
    ("FWD012-AUDIT-022", "atlas_donor_cognition_055", "stage_packet_lineage"),
    ("FWD012-AUDIT-023", "atlas_donor_cognition_057", "native_transform_boundary"),
    ("FWD012-AUDIT-024", "atlas_donor_cognition_058", "stage_packet_lineage"),
    ("FWD012-AUDIT-025", "atlas_donor_cognition_059", "stage_packet_lineage"),
    (
        "FWD012-AUDIT-026",
        "atlas_donor_services_imported_modules_pkg_001",
        "native_transform_boundary",
    ),
    ("FWD012-AUDIT-027", "atlas_donor_legacy_extraction_001", "native_transform_boundary"),
    ("FWD012-AUDIT-028", "atlas_donor_legacy_extraction_002", "native_transform_boundary"),
    ("FWD012-AUDIT-029", "atlas_donor_legacy_extraction_005", "native_transform_boundary"),
    (
        "FWD012-AUDIT-030",
        "atlas_donor_imported_market_context_synthesis_001",
        "native_transform_boundary",
    ),
    (
        "FWD012-AUDIT-031",
        "atlas_donor_imported_market_context_synthesis_002",
        "native_transform_boundary",
    ),
    (
        "FWD012-AUDIT-032",
        "atlas_donor_imported_market_context_synthesis_003",
        "native_transform_boundary",
    ),
    (
        "FWD012-AUDIT-033",
        "atlas_donor_imported_market_context_synthesis_004",
        "native_transform_boundary",
    ),
    (
        "FWD012-AUDIT-034",
        "atlas_donor_imported_market_context_synthesis_005",
        "native_transform_boundary",
    ),
    ("FWD012-AUDIT-035", "atlas_donor_imported_posture_enrichers_002", "native_transform_boundary"),
    ("FWD012-AUDIT-036", "atlas_donor_imported_posture_enrichers_004", "native_transform_boundary"),
    ("FWD012-AUDIT-037", "atlas_donor_imported_posture_enrichers_005", "native_transform_boundary"),
    ("FWD012-AUDIT-038", "atlas_donor_imported_posture_enrichers_006", "native_transform_boundary"),
    ("FWD012-AUDIT-039", "atlas_donor_imported_posture_enrichers_007", "native_transform_boundary"),
    ("FWD012-AUDIT-040", "atlas_donor_imported_posture_enrichers_009", "native_transform_boundary"),
    ("FWD012-AUDIT-041", "atlas_donor_imported_posture_enrichers_010", "native_transform_boundary"),
    ("FWD012-AUDIT-042", "atlas_donor_imported_context_scanners_001", "native_transform_boundary"),
    ("FWD012-AUDIT-043", "atlas_donor_imported_context_scanners_002", "native_transform_boundary"),
    ("FWD012-AUDIT-044", "atlas_donor_imported_context_scanners_003", "native_transform_boundary"),
    ("FWD012-AUDIT-045", "atlas_donor_imported_context_scanners_004", "native_transform_boundary"),
    ("FWD012-AUDIT-046", "atlas_donor_imported_context_scanners_005", "native_transform_boundary"),
    ("FWD012-AUDIT-047", "atlas_donor_imported_context_scanners_006", "native_transform_boundary"),
    ("FWD012-AUDIT-048", "atlas_donor_imported_context_scanners_007", "native_transform_boundary"),
    ("FWD012-AUDIT-049", "atlas_donor_imported_context_scanners_009", "native_transform_boundary"),
    ("FWD012-AUDIT-050", "atlas_donor_imported_context_scanners_010", "native_transform_boundary"),
    ("FWD012-AUDIT-051", "atlas_donor_imported_context_scanners_011", "native_transform_boundary"),
    ("FWD012-AUDIT-052", "atlas_donor_imported_context_scanners_012", "native_transform_boundary"),
    ("FWD012-AUDIT-053", "atlas_donor_imported_tranche_a_001", "native_transform_boundary"),
    ("FWD012-AUDIT-054", "atlas_donor_imported_tranche_a_002", "native_transform_boundary"),
    ("FWD012-AUDIT-055", "atlas_donor_imported_tranche_a_003", "native_transform_boundary"),
    ("FWD012-AUDIT-056", "atlas_donor_imported_tranche_a_004", "native_transform_boundary"),
    ("FWD012-AUDIT-057", "atlas_donor_imported_tranche_a_005", "native_transform_boundary"),
    ("FWD012-AUDIT-058", "atlas_donor_imported_tranche_a_006", "native_transform_boundary"),
    ("FWD012-AUDIT-059", "atlas_donor_imported_tranche_a_008", "native_transform_boundary"),
    ("FWD012-AUDIT-060", "atlas_donor_imported_tranche_a_009", "native_transform_boundary"),
    ("FWD012-AUDIT-061", "atlas_donor_imported_tranche_a_010", "native_transform_boundary"),
    ("FWD012-AUDIT-062", "atlas_donor_imported_tranche_a_011", "native_transform_boundary"),
    ("FWD012-AUDIT-063", "atlas_donor_imported_tranche_a_012", "native_transform_boundary"),
    ("FWD012-AUDIT-064", "atlas_donor_imported_tranche_a_013", "native_transform_boundary"),
    ("FWD012-AUDIT-065", "atlas_donor_imported_tranche_a_014", "native_transform_boundary"),
    ("FWD012-AUDIT-066", "atlas_donor_imported_tranche_a_015", "native_transform_boundary"),
    ("FWD012-AUDIT-067", "atlas_donor_imported_tranche_a_016", "native_transform_boundary"),
    ("FWD012-AUDIT-068", "atlas_donor_imported_tranche_a_017", "native_transform_boundary"),
    ("FWD012-AUDIT-069", "atlas_donor_imported_tranche_a_018", "native_transform_boundary"),
    ("FWD012-AUDIT-070", "atlas_donor_imported_tranche_a_019", "native_transform_boundary"),
    ("FWD012-AUDIT-071", "atlas_donor_imported_tranche_a_020", "native_transform_boundary"),
    (
        "FWD012-AUDIT-072",
        "atlas_donor_service_imported_market_context_synthesis_001",
        "native_transform_boundary",
    ),
    (
        "FWD012-AUDIT-073",
        "atlas_donor_service_imported_market_context_synthesis_002",
        "native_transform_boundary",
    ),
    (
        "FWD012-AUDIT-074",
        "atlas_donor_service_imported_market_context_synthesis_003",
        "native_transform_boundary",
    ),
    (
        "FWD012-AUDIT-075",
        "atlas_donor_service_imported_market_context_synthesis_004",
        "native_transform_boundary",
    ),
    (
        "FWD012-AUDIT-076",
        "atlas_donor_service_imported_market_context_synthesis_005",
        "native_transform_boundary",
    ),
    (
        "FWD012-AUDIT-077",
        "atlas_donor_service_imported_market_context_synthesis_006",
        "native_transform_boundary",
    ),
    (
        "FWD012-AUDIT-078",
        "atlas_donor_service_imported_market_context_synthesis_007",
        "native_transform_boundary",
    ),
    (
        "FWD012-AUDIT-079",
        "atlas_donor_service_cognition_runtime_registry_001",
        "stage_packet_lineage",
    ),
    (
        "FWD012-AUDIT-080",
        "atlas_donor_service_cognition_runtime_registry_002",
        "runtime_contract_registry_replacement",
    ),
    (
        "FWD012-AUDIT-081",
        "atlas_donor_service_cognition_runtime_registry_003",
        "runtime_contract_registry_replacement",
    ),
    (
        "FWD012-AUDIT-082",
        "atlas_donor_service_cognition_runtime_registry_004",
        "runtime_contract_registry_replacement",
    ),
    (
        "FWD012-AUDIT-083",
        "atlas_donor_service_cognition_runtime_registry_005",
        "runtime_contract_registry_replacement",
    ),
    (
        "FWD012-AUDIT-084",
        "atlas_donor_service_cognition_runtime_registry_006",
        "runtime_contract_registry_replacement",
    ),
    (
        "FWD012-AUDIT-085",
        "atlas_donor_service_cognition_runtime_registry_007",
        "runtime_contract_registry_replacement",
    ),
    (
        "FWD012-AUDIT-086",
        "atlas_donor_service_cognition_runtime_registry_008",
        "runtime_contract_registry_replacement",
    ),
    (
        "FWD012-AUDIT-087",
        "atlas_donor_service_cognition_runtime_registry_009",
        "runtime_contract_registry_replacement",
    ),
    (
        "FWD012-AUDIT-088",
        "atlas_donor_service_cognition_runtime_registry_010",
        "runtime_contract_registry_replacement",
    ),
    (
        "FWD012-AUDIT-089",
        "atlas_donor_service_imported_posture_enrichers_001",
        "stage_packet_lineage",
    ),
    (
        "FWD012-AUDIT-090",
        "atlas_donor_service_imported_posture_enrichers_002",
        "stage_packet_lineage",
    ),
    (
        "FWD012-AUDIT-091",
        "atlas_donor_service_imported_posture_enrichers_003",
        "native_transform_boundary",
    ),
    (
        "FWD012-AUDIT-092",
        "atlas_donor_service_imported_posture_enrichers_004",
        "native_transform_boundary",
    ),
    (
        "FWD012-AUDIT-093",
        "atlas_donor_service_imported_posture_enrichers_007",
        "native_transform_boundary",
    ),
    (
        "FWD012-AUDIT-094",
        "atlas_donor_service_imported_posture_enrichers_008",
        "native_transform_boundary",
    ),
    (
        "FWD012-AUDIT-095",
        "atlas_donor_service_imported_posture_enrichers_009",
        "native_transform_boundary",
    ),
    (
        "FWD012-AUDIT-096",
        "atlas_donor_service_imported_posture_enrichers_010",
        "native_transform_boundary",
    ),
    ("FWD012-AUDIT-097", "atlas_donor_context_scanners_001", "native_transform_boundary"),
    ("FWD012-AUDIT-098", "atlas_donor_context_scanners_002", "native_transform_boundary"),
    ("FWD012-AUDIT-099", "atlas_donor_context_scanners_003", "stage_packet_lineage"),
    ("FWD012-AUDIT-100", "atlas_donor_context_scanners_004", "native_transform_boundary"),
    ("FWD012-AUDIT-101", "atlas_donor_context_scanners_005", "native_transform_boundary"),
    ("FWD012-AUDIT-102", "atlas_donor_context_scanners_006", "native_transform_boundary"),
    ("FWD012-AUDIT-103", "atlas_donor_context_scanners_007", "native_transform_boundary"),
    ("FWD012-AUDIT-104", "atlas_donor_context_scanners_008", "native_transform_boundary"),
    ("FWD012-AUDIT-105", "atlas_donor_context_scanners_009", "native_transform_boundary"),
    ("FWD012-AUDIT-106", "atlas_donor_context_scanners_010", "native_transform_boundary"),
    ("FWD012-AUDIT-107", "atlas_donor_context_scanners_011", "native_transform_boundary"),
    ("FWD012-AUDIT-108", "atlas_donor_context_scanners_013", "native_transform_boundary"),
    ("FWD012-AUDIT-109", "atlas_donor_context_scanners_014", "native_transform_boundary"),
    ("FWD012-AUDIT-110", "atlas_donor_tranche_a_service_001", "native_transform_boundary"),
    ("FWD012-AUDIT-111", "atlas_donor_tranche_a_service_002", "native_transform_boundary"),
    ("FWD012-AUDIT-112", "atlas_donor_tranche_a_service_003", "native_transform_boundary"),
    ("FWD012-AUDIT-113", "atlas_donor_tranche_a_service_004", "native_transform_boundary"),
    ("FWD012-AUDIT-114", "atlas_donor_tranche_a_service_005", "native_transform_boundary"),
    ("FWD012-AUDIT-115", "atlas_donor_tranche_a_service_006", "stage_packet_lineage"),
    ("FWD012-AUDIT-116", "atlas_donor_tranche_a_service_007", "native_transform_boundary"),
    ("FWD012-AUDIT-117", "atlas_donor_tranche_a_service_009", "native_transform_boundary"),
    ("FWD012-AUDIT-118", "atlas_donor_tranche_a_service_010", "native_transform_boundary"),
    ("FWD012-AUDIT-119", "atlas_donor_tranche_a_service_011", "native_transform_boundary"),
    ("FWD012-AUDIT-120", "atlas_donor_tranche_a_service_012", "native_transform_boundary"),
    ("FWD012-AUDIT-121", "atlas_donor_tranche_a_service_013", "native_transform_boundary"),
    ("FWD012-AUDIT-122", "atlas_donor_tranche_a_service_014", "native_transform_boundary"),
    ("FWD012-AUDIT-123", "atlas_donor_tranche_a_service_015", "native_transform_boundary"),
    ("FWD012-AUDIT-124", "atlas_donor_tranche_a_service_016", "native_transform_boundary"),
    ("FWD012-AUDIT-125", "atlas_donor_tranche_a_service_017", "native_transform_boundary"),
    ("FWD012-AUDIT-126", "atlas_donor_tranche_a_service_018", "native_transform_boundary"),
    ("FWD012-AUDIT-127", "atlas_donor_tranche_a_service_019", "native_transform_boundary"),
    ("FWD012-AUDIT-128", "atlas_donor_tranche_a_service_020", "native_transform_boundary"),
    ("FWD012-AUDIT-129", "atlas_donor_tranche_a_service_021", "native_transform_boundary"),
    ("FWD012-AUDIT-130", "atlas_donor_cognition_runtime_service_001", "runtime_service_identity"),
    ("FWD012-AUDIT-131", "atlas_donor_cognition_runtime_service_002", "runtime_service_identity"),
    ("FWD012-AUDIT-132", "atlas_donor_cognition_runtime_service_003", "runtime_service_identity"),
    ("FWD012-AUDIT-133", "atlas_donor_cognition_runtime_service_004", "runtime_service_identity"),
    ("FWD012-AUDIT-134", "atlas_donor_cognition_runtime_service_005", "runtime_service_identity"),
    ("FWD012-AUDIT-135", "atlas_donor_cognition_runtime_service_006", "runtime_service_identity"),
    ("FWD012-AUDIT-136", "atlas_donor_cognition_runtime_service_008", "runtime_service_identity"),
    ("FWD012-AUDIT-137", "atlas_donor_cognition_runtime_service_013", "stage_packet_lineage"),
    ("FWD012-AUDIT-138", "atlas_donor_cognition_runtime_service_015", "stage_packet_lineage"),
    ("FWD012-AUDIT-139", "atlas_donor_cognition_runtime_service_016", "stage_packet_lineage"),
)


def _source_time() -> datetime:
    return datetime(2026, 5, 19, 13, 31, 45, tzinfo=UTC)


def _stage_input_bundle(audit_row_id: str, atlas_record_id: str) -> StageInputBundle:
    source_time_utc = _source_time()
    return StageInputBundle(
        temporal=TemporalContextInput(
            source_time_raw="2026-05-19T09:31:45-04:00",
            source_time_kind="timestamp",
            source_timezone_raw="America/New_York",
            source_time_utc=source_time_utc,
            captured_at_utc=source_time_utc + timedelta(seconds=3),
            persisted_at_utc=source_time_utc + timedelta(seconds=8),
            source_provider="fwd012_source",
            source_channel="serial_stage_ingress",
            time_granularity="timestamp",
            next_event_time_utc=source_time_utc + timedelta(minutes=45),
            windows=[
                {
                    "event_id": audit_row_id,
                    "window_start_utc": source_time_utc - timedelta(minutes=5),
                    "window_end_utc": source_time_utc + timedelta(minutes=20),
                    "tags": [atlas_record_id],
                }
            ],
        ),
        regime=MarketRegimeContextInput(
            nvda_return_pct=0.045,
            nq_return_pct=0.018,
            vix_level=23.5,
        ),
        options_flow=OptionsFlowContextInput(spot_price=104.0, front_dte=1, next_dte=7),
    )


def _receipt(audit_row_id: str, atlas_record_id: str) -> dict[str, object]:
    return DeskRuntimeOrchestrator().run_once(_stage_input_bundle(audit_row_id, atlas_record_id))


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


@pytest.mark.parametrize(("audit_row_id", "atlas_record_id", "behaviour"), REOPENED_ROW_CASES)
def test_fwd012_reopened_rows_have_real_serial_desk_cognition_spine_behaviour(
    audit_row_id: str, atlas_record_id: str, behaviour: str
) -> None:
    assert audit_row_id.startswith("FWD012-AUDIT-")
    assert atlas_record_id.startswith("atlas_donor_")

    if behaviour == "serial_contract_descriptor":
        contract = serial_spine_contract()
        copied = copy_serial_spine_contract()
        copied["stage_order"].append("capital_deployment_authority")
        assert serial_spine_contract()["stage_order"] == list(SERIAL_SPINE_STAGE_ORDER)
        assert contract["architecture_row"] == "5.7 Serial desk-cognition spine"
        assert contract["owner"] == "serial desk-cognition authority"
        assert (
            contract["purpose"] == "ordered candidate formation through six serial runtime stages"
        )
        assert contract["stage_dependencies"] == {
            stage_name: list(dependencies)
            for stage_name, dependencies in validate_serial_stage_dependencies(
                SERIAL_SPINE_STAGE_ORDER, SERIAL_STAGE_DEPENDENCIES
            ).items()
        }
        assert "capital_deployment_authority" in contract["prohibited_authorities"]
        assert contract["boundary"].startswith("forms candidate material only")
        return

    receipt = _receipt(audit_row_id, atlas_record_id)
    stage_outputs = receipt["stage_outputs"]
    stage_packets = receipt["stage_packets"]
    stage_packet_ids = receipt["stage_packet_ids"]

    if behaviour == "bounded_state_carriers":
        assert tuple(receipt["stage_order"]) == SERIAL_SPINE_STAGE_ORDER
        assert set(SERIAL_SPINE_PROHIBITED_AUTHORITIES) <= set(
            receipt["serial_spine_contract"]["prohibited_authorities"]
        )
        assert set(stage_outputs["options_flow"]) >= {
            "term_structure_state",
            "skew_state",
            "gamma_state",
        }
        assert stage_outputs["posture"]["permission_state"] in {
            PermissionState.ALLOW.value,
            PermissionState.DERISK.value,
            PermissionState.BLOCK.value,
        }
        assert "lead_playbook_id" in stage_outputs["execution"]
        assert "authorised_notional_usd" not in stage_outputs["execution"]
        return

    if behaviour == "typed_stage_input_carriage":
        assert isinstance(_stage_input_bundle(audit_row_id, atlas_record_id), StageInputBundle)
        with pytest.raises(ValidationError):
            StageInputBundle.model_validate(
                {
                    "temporal": {"source_time_utc": _source_time()},
                    "regime": {},
                    "options_flow": {},
                    "capital_deployment_authority": {"authorised_notional_usd": 1.0},
                }
            )
        assert (
            TemporalContextOutput.model_validate(stage_outputs["temporal"]).source_provider
            == "fwd012_source"
        )
        assert MarketRegimeContextOutput.model_validate(stage_outputs["regime"]).vix_level == 23.5
        assert isinstance(
            OptionsFlowContextOutput.model_validate(stage_outputs["options_flow"]),
            OptionsFlowContextOutput,
        )
        return

    if behaviour == "execution_recommendation_boundary":
        execution_input = ExecutionExpressionInput(
            temporal=stage_outputs["temporal"],
            regime=stage_outputs["regime"],
            options_flow=stage_outputs["options_flow"],
            posture=stage_outputs["posture"],
            eligibility=stage_outputs["eligibility"],
        )
        expression = evaluate_execution_expression(
            execution_input=execution_input,
            eligibility_output=PlaybookEligibilityOutput.model_validate(
                stage_outputs["eligibility"]
            ),
        )
        service_result = ExecutionService().evaluate(
            execution_input=execution_input,
            eligibility_output=PlaybookEligibilityOutput.model_validate(
                stage_outputs["eligibility"]
            ),
        )
        assert isinstance(expression, ExecutionExpressionOutput)
        assert service_result["expression"].final_risk_join == expression.final_risk_join
        with pytest.raises(ValidationError):
            ExecutionExpressionOutput(authorised_notional_usd=1000.0)
        handoff = StageLocalHandoffSurface.model_validate(receipt["stage_local_handoff"])
        assert handoff.lineage_tags == list(SERIAL_STAGE_LINEAGE_TAGS)
        assert "pre_capital_deployment" in handoff.lineage_tags
        return

    if behaviour == "stage_packet_lineage":
        assert receipt["executed_stages"] == list(SERIAL_SPINE_STAGE_ORDER)
        assert receipt["missing_stages"] == []
        expected_modules = {
            "temporal": "temporal_context",
            "regime": "market_regime_context",
            "options_flow": "options_flow_context",
            "posture": "posture_risk_permission",
            "eligibility": "playbook_eligibility",
            "execution": "expression_execution",
        }
        expected_schemas = {
            "temporal": "TemporalContextOutput",
            "regime": "MarketRegimeContextOutput",
            "options_flow": "OptionsFlowContextOutput",
            "posture": "PostureRiskOutput",
            "eligibility": "PlaybookEligibilityOutput",
            "execution": "ExecutionExpressionOutput",
        }
        fingerprints = set()
        previous_id: str | None = None
        for stage_name in SERIAL_SPINE_STAGE_ORDER:
            packet = stage_packets[stage_name]
            fingerprints.add(packet["lineage"]["inputfingerprint"])
            assert packet["packetrole"] == "stage_packet"
            assert packet["producer"]["module_id"] == expected_modules[stage_name]
            assert packet["producer"]["grammar_role"] == expected_modules[stage_name]
            assert packet["producer"]["stage_name"] == stage_name
            assert packet["producer"]["module_version"] == "native"
            assert packet["dataschema"] == expected_schemas[stage_name]
            assert (
                packet["dmpextensions"]["nvda"]["schema_identifiers"]["output_model_name"]
                == expected_schemas[stage_name]
            )
            assert packet["validation"]["status"] == "valid"
            assert packet["lineage"]["parentids"] == ([] if previous_id is None else [previous_id])
            assert packet["lineage"]["dependencyids"] == [
                stage_packet_ids[name] for name in SERIAL_STAGE_DEPENDENCIES[stage_name]
            ]
            previous_id = stage_packet_ids[stage_name]
        assert len(fingerprints) == 1
        assert stage_packets["execution"]["lineage"]["derivedfrom"] == (
            "execution_from_temporal+regime+options_flow+posture+eligibility"
        )
        assert stage_packets["execution"]["summary"]["headline"] == "lead_playbook_id=none"
        return

    if behaviour == "native_transform_boundary":
        for path in SELECTED_NATIVE_FILES:
            imports = _imports_for(path)
            for prohibited_prefix in PROHIBITED_IMPORT_PREFIXES:
                assert not any(
                    imported == prohibited_prefix or imported.startswith(f"{prohibited_prefix}.")
                    for imported in imports
                ), f"{path} imports prohibited donor module prefix {prohibited_prefix}"
            assert _defined_symbols(path).isdisjoint(PROHIBITED_DONOR_SYMBOLS)
        assert receipt["serial_spine_contract"]["owner"] == "serial desk-cognition authority"
        assert all(
            stage_packets[stage_name]["producer"]["module_version"] == "native"
            for stage_name in SERIAL_SPINE_STAGE_ORDER
        )
        return

    if behaviour == "runtime_contract_registry_replacement":
        metadata = DeskRuntimeOrchestrator._stage_packet_metadata
        assert tuple(metadata) == SERIAL_SPINE_STAGE_ORDER
        assert set(metadata) == set(receipt["serial_spine_contract"]["stage_output_schemas"])
        for stage_name, stage_metadata in metadata.items():
            assert (
                stage_metadata["dataschema"]
                == receipt["serial_spine_contract"]["stage_output_schemas"][stage_name]
            )
            assert stage_metadata["module_id"] == stage_packets[stage_name]["producer"]["module_id"]
            assert (
                stage_metadata["grammar_role"]
                == stage_packets[stage_name]["producer"]["grammar_role"]
            )
        assert receipt["stage_dependencies"] == {
            stage_name: list(dependencies)
            for stage_name, dependencies in SERIAL_STAGE_DEPENDENCIES.items()
        }
        return

    if behaviour == "runtime_service_identity":
        orchestrator = DeskRuntimeOrchestrator()
        assert orchestrator.stage_sequence() == SERIAL_SPINE_STAGE_ORDER
        assert receipt["stage_packets"]["temporal"]["traceid"].startswith("trace::serial_runtime::")
        assert receipt["stage_packets"]["temporal"]["runid"].startswith("run::serial_runtime::")
        assert receipt["stage_packets"]["temporal"]["scenarioid"] == "live"
        assert receipt["serial_spine_contract"]["lineage_tags"] == list(SERIAL_STAGE_LINEAGE_TAGS)
        assert "runtime_live_inventory" not in receipt
        assert "capital_deployment_authority" not in receipt["executed_stages"]
        return

    raise AssertionError(f"Unhandled FWD-012 behaviour bucket: {behaviour}")
