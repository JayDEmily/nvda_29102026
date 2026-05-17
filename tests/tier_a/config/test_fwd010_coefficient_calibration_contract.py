from __future__ import annotations

from decimal import Decimal

from nvda_desk.config.coefficient_authority import CoefficientAuthorityService
from nvda_desk.contracts.modifiers import (
    CoefficientCalibrationOverride,
    CoefficientReplayFixturePack,
)


def test_coefficient_authority_builds_calibration_set_and_audit_packet_without_live_mutation() -> (
    None
):
    service = CoefficientAuthorityService()
    calibration = service.calibrate_from_overrides(
        owner_stage="posture",
        module_weight_overrides=[
            CoefficientCalibrationOverride(
                target_id="max_risk_per_trade",
                proposed_value=Decimal("0.20"),
                evidence_ref="walk-forward::run-1",
            )
        ],
        sub_coefficient_overrides=[],
        calibration_id="calibration-1",
    )
    audit = service.build_audit_packet(
        active_modifier_ids=["negative_gamma_stress"],
        owner_stage="posture",
        calibration=calibration,
        packet_id="audit-1",
    )
    fixture_pack = service.build_replay_fixture_pack(
        active_modifier_ids=["negative_gamma_stress"],
        owner_stage="posture",
        pack_id="fixture-pack-1",
    )

    assert calibration.calibration_id == "calibration-1"
    assert calibration.module_weight_overrides[0].target_id == "max_risk_per_trade"
    assert audit.packet_id == "audit-1"
    assert audit.calibration.calibration_id == "calibration-1"
    assert audit.replay_receipt.active_modifier_ids == ["negative_gamma_stress"]
    assert audit.live_update_allowed is False
    assert isinstance(fixture_pack, CoefficientReplayFixturePack)
    assert fixture_pack.fixture_lineage[0] == "coefficient_authority.v1"
    assert fixture_pack.capital_deployment_allowed is False
