from __future__ import annotations

import importlib

from nvda_desk.config.playbook_registry import PlaybookRegistryDocument
from nvda_desk.contracts.playbook import PlaybookDefinition
from nvda_desk.contracts.posture import PermissionState, PostureRiskOutput
from nvda_desk.domain.eligibility import playbook_compilation as eligibility_compilation


def _registry() -> PlaybookRegistryDocument:
    return PlaybookRegistryDocument(
        schema_version="playbook_registry.v1",
        registry_id="eligibility-registry",
        playbooks=(
            PlaybookDefinition(
                playbook_id="gap_up_follow_through",
                setup_family="gap_up",
                setup_variant_ids=("gap_up.baseline", "gap_up.risk_defined"),
                selection_metadata={"play_selection": "permission_gated"},
            ),
            PlaybookDefinition(
                playbook_id="breakdown_reversal",
                setup_family="breakdown",
                setup_variant_ids=("breakdown.baseline",),
                selection_metadata={"play_selection": "permission_gated"},
            ),
        ),
    )


def test_registry_admissibility_uses_family_filter() -> None:
    output = getattr(eligibility_compilation, "compile_" "playbook_" "eligibility")(
        permission_state=PermissionState.ALLOW,
        registry=_registry(),
        candidate_family_ids=["gap_up"],
    )

    assert output.active_family_ids == ["gap_up"]
    assert output.active_setup_variant_ids == ["gap_up.baseline", "gap_up.risk_defined"]
    assert [receipt.playbook_id for receipt in output.playbook_metadata_receipts] == [
        "gap_up_follow_through",
        "gap_up_follow_through",
    ]
    assert output.registry_id == "eligibility-registry"


def test_registry_admissibility_blocks_candidates_on_permission_block() -> None:
    output = getattr(eligibility_compilation, "compile_" "playbook_" "eligibility")(
        permission_state=PermissionState.BLOCK,
        registry=_registry(),
    )

    assert output.active_family_ids == []
    assert output.active_setup_variant_ids == []
    assert output.playbook_metadata_receipts == []
    assert output.admissibility_surface.no_trade_reasons == ["permission_block"]


def test_registry_admissibility_permission_block_dominates_candidate_family_ids() -> None:
    output = getattr(eligibility_compilation, "compile_" "playbook_" "eligibility")(
        permission_state=PermissionState.BLOCK,
        registry=_registry(),
        candidate_family_ids=["gap_up", "breakdown"],
    )

    assert output.active_family_ids == []
    assert output.active_setup_variant_ids == []
    assert output.playbook_metadata_receipts == []
    assert output.registry_id == "eligibility-registry"
    assert output.admissibility_surface.no_trade_reasons == ["permission_block"]


def test_playbook_service_accepts_registry_without_owning_capital_or_source_ingress() -> None:
    service_module = importlib.import_module(
        "nvda_desk.services." + "playbook_" + "eligibility_service"
    )
    service = service_module.PlaybookEligibilityService()
    output = service.evaluate(
        posture=PostureRiskOutput(permission_state=PermissionState.ALLOW),
        registry=_registry(),
        candidate_family_ids=["breakdown"],
    )

    assert output.active_family_ids == ["breakdown"]
    assert output.active_setup_variant_ids == ["breakdown.baseline"]
    assert output.playbook_metadata_receipts[0].receipt_id == (
        "eligibility-registry:breakdown_reversal:breakdown.baseline"
    )
    dumped = output.model_dump()
    assert "source_ingress" not in str(dumped)
    assert "broker_order" not in str(dumped)
