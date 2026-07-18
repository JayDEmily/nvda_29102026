from __future__ import annotations

from datetime import datetime, timezone

import pytest

from nvda_desk.config.playbook_registry import PlaybookRegistryDocument
from nvda_desk.contracts.options_flow import OptionsFlowContextInput
from nvda_desk.contracts.playbook import PlaybookDefinition
from nvda_desk.contracts.posture import PermissionState, PostureRiskOutput
from nvda_desk.contracts.regime import MarketRegimeContextInput
from nvda_desk.contracts.stage_inputs import StageInputBundle
from nvda_desk.contracts.temporal import TemporalContextInput
from nvda_desk.runtime.orchestrator import DeskRuntimeOrchestrator
from nvda_desk.services.parallel_risk_lane_service import ParallelRiskLaneService
from nvda_desk.services.playbook_eligibility_service import PlaybookEligibilityService


def _bundle() -> StageInputBundle:
    return StageInputBundle(
        temporal=TemporalContextInput(
            source_time_utc=datetime(2026, 4, 21, 13, 31, tzinfo=timezone.utc)
        ),
        regime=MarketRegimeContextInput(
            nvda_return_pct=0.1,
            nq_return_pct=0.05,
            vix_level=20.0,
        ),
        options_flow=OptionsFlowContextInput(spot_price=101.0, front_dte=1, next_dte=5),
    )


def test_c017_parallel_risk_bootstrap_rejects_missing_upstream_identity_and_lineage() -> None:
    with pytest.raises(
        ValueError, match="traceid|runid|scenarioid|derivedfrom|sourceartifactids|inputfingerprint"
    ):
        ParallelRiskLaneService().run_bootstrap(
            stage_input_bundle=_bundle(),
            input_packet_id="risk-input-1",
            output_packet_id="risk-output-1",
        )


def test_c020_c035_parallel_risk_policy_state_is_instance_owned_not_module_global() -> None:
    first = ParallelRiskLaneService()
    second = ParallelRiskLaneService()
    first.evaluate_risk_policy("policy-v1", candidate_id="candidate-1")

    assert [item.decision_id for item in first.list_risk_decisions()] == ["policy-v1::candidate-1"]
    assert second.list_risk_decisions() == []


def test_c025_c027_temporal_and_regime_outputs_carry_the_policy_versions_that_define_them() -> None:
    receipt = DeskRuntimeOrchestrator().run_once(_bundle())
    temporal = receipt["stage_outputs"]["temporal"]
    regime = receipt["stage_outputs"]["regime"]

    assert temporal["temporal_policy_version"]
    assert regime["regime_policy_version"]


def test_c031_governed_run_once_rejects_structurally_invalid_stage_mapping() -> None:
    with pytest.raises((ValueError, TypeError), match="stage|bundle|input|contract"):
        DeskRuntimeOrchestrator().run_once({"temporal": {"present": True}})


def test_c032_playbook_registry_substitution_does_not_require_consumer_changes() -> None:
    registry = PlaybookRegistryDocument(
        registry_id="registry-v1",
        playbooks=(
            PlaybookDefinition(
                playbook_id="strategy-a",
                setup_family="family-a",
                setup_variant_ids=("family-a.base",),
            ),
            PlaybookDefinition(
                playbook_id="strategy-b",
                setup_family="family-b",
                setup_variant_ids=("family-b.base",),
            ),
        ),
    )
    output = PlaybookEligibilityService().evaluate(
        posture=PostureRiskOutput(permission_state=PermissionState.ALLOW),
        registry=registry,
        candidate_family_ids=["family-b"],
    )

    assert output.registry_id == "registry-v1"
    assert output.active_family_ids == ["family-b"]
    assert [receipt.playbook_id for receipt in output.playbook_metadata_receipts] == ["strategy-b"]


def test_c033_orchestrator_receives_candidate_families_and_registry_as_owned_inputs() -> None:
    signature_fields = set(DeskRuntimeOrchestrator.run_once.__annotations__)
    assert "candidate_family_ids" in signature_fields
    assert "playbook_registry" in signature_fields
