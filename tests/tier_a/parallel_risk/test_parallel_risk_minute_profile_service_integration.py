from __future__ import annotations

from datetime import UTC, datetime

from nvda_desk.contracts.options_flow import OptionsFlowContextInput
from nvda_desk.contracts.parallel_risk import ParallelRiskMinuteProfile
from nvda_desk.contracts.regime import MarketRegimeContextInput
from nvda_desk.contracts.stage_inputs import StageInputBundle
from nvda_desk.contracts.temporal import TemporalContextInput
from nvda_desk.services.parallel_risk_lane_service import ParallelRiskLaneService


def _bundle() -> StageInputBundle:
    return StageInputBundle(
        temporal=TemporalContextInput(source_time_utc=datetime(2026, 5, 18, 14, 30, tzinfo=UTC)),
        regime=MarketRegimeContextInput(vix_level=31.0),
        options_flow=OptionsFlowContextInput(spot_price=101.0, front_dte=5, next_dte=1),
    )


def test_run_bootstrap_default_result_remains_backward_compatible() -> None:
    result = ParallelRiskLaneService().run_bootstrap(
        stage_input_bundle=_bundle(),
        input_packet_id="dmp::parallel_risk::bootstrap_input::service-default",
        output_packet_id="dmp::parallel_risk::output::service-default",
    )

    assert set(result) == {"bootstrap_input_packet", "lane_packet"}


def test_run_bootstrap_can_include_optional_minute_profile_without_changing_lane_packet() -> None:
    result = ParallelRiskLaneService().run_bootstrap(
        stage_input_bundle=_bundle(),
        input_packet_id="dmp::parallel_risk::bootstrap_input::service-profile",
        output_packet_id="dmp::parallel_risk::output::service-profile",
        sourceartifactids=["source-artifact-1"],
        inputfingerprint="sha256:fixture",
        include_minute_profile=True,
    )

    assert set(result) == {"bootstrap_input_packet", "lane_packet", "minute_profile"}
    profile = result["minute_profile"]
    assert isinstance(profile, ParallelRiskMinuteProfile)
    assert profile.packet_id == "dmp::parallel_risk::output::service-profile::minute_profile"
    assert profile.risk_envelope_state == "caution"
    assert profile.lineage["parent_packet_ids"] == [
        "dmp::parallel_risk::bootstrap_input::service-profile"
    ]
    assert profile.lineage["dependency_packet_ids"] == [
        "dmp::parallel_risk::bootstrap_input::service-profile"
    ]
    assert profile.lineage["source_artifact_ids"] == ["source-artifact-1"]
    assert profile.lineage["input_fingerprint"] == "sha256:fixture"
    assert profile.authority_flags.capital_sizing_allowed is False
