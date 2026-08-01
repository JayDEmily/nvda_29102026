from __future__ import annotations

from copy import deepcopy
from datetime import UTC, datetime
from pathlib import Path

import pytest
import yaml
from pydantic import ValidationError

from nvda_desk.config.parallel_risk_lane_profile import ParallelRiskLaneProfileService
from nvda_desk.contracts.options_flow import OptionsFlowContextInput
from nvda_desk.contracts.parallel_risk import (
    ParallelRiskPreparationPacket,
    parallel_risk_lane_profile_config_from_dict,
)
from nvda_desk.contracts.regime import MarketRegimeContextInput
from nvda_desk.contracts.temporal import TemporalContextInput
from nvda_desk.domain.parallel_risk.environment_assessment import assess_risk_envelope

CONFIG = Path("config/parallel_risk_lane_profile.v1.yaml")


def _packet(vix_level: float) -> ParallelRiskPreparationPacket:
    return ParallelRiskPreparationPacket(
        temporal_input=TemporalContextInput(
            source_time_utc=datetime(2026, 5, 18, 14, 30, tzinfo=UTC)
        ),
        regime_input=MarketRegimeContextInput(vix_level=vix_level),
        options_flow_input=OptionsFlowContextInput(),
    )


def _payload() -> dict:
    return yaml.safe_load(CONFIG.read_text(encoding="utf-8"))


def test_parallel_risk_lane_profile_config_loads_and_preserves_compatibility() -> None:
    config = ParallelRiskLaneProfileService(CONFIG).load_config()
    policy = config.vix_threshold_policy

    assert policy.mode == "compatibility_legacy_30_50"
    assert policy.caution_threshold == 30.0
    assert policy.block_threshold == 50.0
    assert policy.hidden_coefficient_mutation_allowed is False
    assert policy.authority_flags.capital_sizing_allowed is False
    assert policy.coefficient_authority_refs == [
        "config/coefficient_authority.v1.yaml#risk_vix_caution_threshold",
        "config/coefficient_authority.v1.yaml#risk_vix_hot_threshold",
    ]

    caution_envelope = assess_risk_envelope(_packet(30.0), vix_threshold_policy=policy)
    block_envelope = assess_risk_envelope(_packet(50.0), vix_threshold_policy=policy)
    assert caution_envelope.envelope_state == "caution"
    assert block_envelope.envelope_state == "block"


def test_parallel_risk_lane_profile_invalid_threshold_config_fails() -> None:
    payload = _payload()
    payload["vix_threshold_policy"]["caution_threshold"] = 55.0
    payload["vix_threshold_policy"]["block_threshold"] = 50.0

    with pytest.raises(ValidationError):
        parallel_risk_lane_profile_config_from_dict(payload)


def test_parallel_risk_lane_profile_migration_path_is_explicit_for_governed_config() -> None:
    payload = _payload()
    policy = payload["vix_threshold_policy"]
    policy["mode"] = "governed_config"
    policy["policy_id"] = "prl_vix_governed_test_policy"
    policy["caution_threshold"] = 25.0
    policy["block_threshold"] = 45.0
    policy["migration_status"] = "explicit_governed_test_migration"

    config = parallel_risk_lane_profile_config_from_dict(payload)
    envelope = assess_risk_envelope(_packet(25.0), vix_threshold_policy=config.vix_threshold_policy)

    assert config.vix_threshold_policy.mode == "governed_config"
    assert config.vix_threshold_policy.migration_status == "explicit_governed_test_migration"
    assert envelope.envelope_state == "caution"
    assert "vix_elevated" in envelope.caution_flags


def test_parallel_risk_lane_profile_hidden_coefficient_mutation_fails() -> None:
    payload = _payload()
    payload["vix_threshold_policy"]["hidden_coefficient_mutation_allowed"] = True

    with pytest.raises(ValidationError):
        parallel_risk_lane_profile_config_from_dict(payload)


def test_parallel_risk_lane_profile_no_authority_widening() -> None:
    payload = _payload()
    config = parallel_risk_lane_profile_config_from_dict(payload)
    authority = config.vix_threshold_policy.authority_flags

    assert authority.candidate_formation_allowed is False
    assert authority.playbook_selection_allowed is False
    assert authority.capital_sizing_allowed is False
    assert authority.broker_execution_allowed is False
    assert authority.direct_workbook_runtime_read_allowed is False

    mutated = deepcopy(payload)
    mutated["vix_threshold_policy"]["authority_flags"] = {"broker_execution_allowed": True}
    with pytest.raises(ValidationError):
        parallel_risk_lane_profile_config_from_dict(mutated)
