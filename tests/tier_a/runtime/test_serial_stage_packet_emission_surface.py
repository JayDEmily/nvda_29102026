from __future__ import annotations

from datetime import UTC, datetime

from nvda_desk.contracts.options_flow import OptionsFlowContextInput
from nvda_desk.contracts.regime import MarketRegimeContextInput
from nvda_desk.contracts.stage_inputs import StageInputBundle
from nvda_desk.contracts.temporal import TemporalContextInput
from nvda_desk.runtime.orchestrator import DeskRuntimeOrchestrator


def test_serial_stage_packet_emission_preserves_order_stage_ownership_and_truthful_dependencies() -> (
    None
):
    source_time_utc = datetime(2026, 4, 21, 13, 31, tzinfo=UTC)
    receipt = DeskRuntimeOrchestrator().run_once(
        StageInputBundle(
            temporal=TemporalContextInput(
                source_time_utc=source_time_utc,
                source_timezone_raw="America/New_York",
            ),
            regime=MarketRegimeContextInput(
                nvda_return_pct=0.1,
                nq_return_pct=0.05,
                vix_level=20.0,
            ),
            options_flow=OptionsFlowContextInput(spot_price=101.0, front_dte=1, next_dte=5),
        )
    )

    assert receipt["serial_spine_contract"]["architecture_row"] == "5.7 Serial desk-cognition spine"
    assert receipt["serial_spine_contract"]["stage_order"] == receipt["stage_order"]
    assert (
        "capital_deployment_authority" in receipt["serial_spine_contract"]["prohibited_authorities"]
    )
    assert "live_position_management" in receipt["serial_spine_contract"]["prohibited_authorities"]
    assert receipt["stage_local_handoff"]["lineage_tags"] == [
        "serial_spine_candidate_formation",
        "before_independent_lane",
        "pre_capital_deployment",
        "no_live_inventory_authority",
    ]

    stage_packets = receipt["stage_packets"]
    stage_packet_ids = receipt["stage_packet_ids"]

    assert stage_packets["temporal"]["packetrole"] == "stage_packet"
    assert stage_packets["temporal"]["data"]["source_timezone_raw"] == "America/New_York"
    assert stage_packets["temporal"]["data"]["session_state"] == "opening"
    assert stage_packets["temporal"]["producer"]["module_id"] == "temporal_context"
    assert stage_packets["temporal"]["producer"]["grammar_role"] == "temporal_context"
    assert stage_packets["temporal"]["lineage"]["parentids"] == []
    assert stage_packets["temporal"]["lineage"]["dependencyids"] == []
    assert (
        stage_packets["temporal"]["lineage"]["derivedfrom"] == "temporal_from_declared_stage_inputs"
    )

    assert stage_packets["regime"]["producer"]["module_id"] == "market_regime_context"
    assert stage_packets["regime"]["producer"]["grammar_role"] == "market_regime_context"
    assert stage_packets["regime"]["lineage"]["parentids"] == [stage_packet_ids["temporal"]]
    assert stage_packets["regime"]["lineage"]["dependencyids"] == []

    assert stage_packets["options_flow"]["producer"]["module_id"] == "options_flow_context"
    assert stage_packets["options_flow"]["producer"]["grammar_role"] == "options_flow_context"
    assert stage_packets["options_flow"]["lineage"]["parentids"] == [stage_packet_ids["regime"]]
    assert stage_packets["options_flow"]["lineage"]["dependencyids"] == []

    assert stage_packets["posture"]["producer"]["module_id"] == "posture_risk_permission"
    assert stage_packets["posture"]["producer"]["grammar_role"] == "posture_risk_permission"
    assert stage_packets["posture"]["lineage"]["parentids"] == [stage_packet_ids["options_flow"]]
    assert stage_packets["posture"]["lineage"]["dependencyids"] == [stage_packet_ids["regime"]]
    assert stage_packets["posture"]["lineage"]["derivedfrom"] == "posture_from_regime"

    assert stage_packets["eligibility"]["producer"]["module_id"] == "playbook_eligibility"
    assert stage_packets["eligibility"]["producer"]["grammar_role"] == "playbook_eligibility"
    assert stage_packets["eligibility"]["lineage"]["parentids"] == [stage_packet_ids["posture"]]
    assert stage_packets["eligibility"]["lineage"]["dependencyids"] == [stage_packet_ids["posture"]]
    assert stage_packets["eligibility"]["lineage"]["derivedfrom"] == "eligibility_from_posture"

    assert stage_packets["execution"]["producer"]["module_id"] == "expression_execution"
    assert stage_packets["execution"]["producer"]["grammar_role"] == "expression_execution"
    assert stage_packets["execution"]["lineage"]["parentids"] == [stage_packet_ids["eligibility"]]
    assert stage_packets["execution"]["lineage"]["dependencyids"] == [
        stage_packet_ids["temporal"],
        stage_packet_ids["regime"],
        stage_packet_ids["options_flow"],
        stage_packet_ids["posture"],
        stage_packet_ids["eligibility"],
    ]
    assert (
        stage_packets["execution"]["lineage"]["derivedfrom"]
        == "execution_from_temporal+regime+options_flow+posture+eligibility"
    )
    assert stage_packets["execution"]["summary"]["headline"] == "lead_playbook_id=none"
    assert stage_packets["execution"]["validation"]["status"] == "valid"

    fingerprints = {
        stage_packets[stage_name]["lineage"]["inputfingerprint"]
        for stage_name in receipt["stage_order"]
    }
    assert len(fingerprints) == 1
    for stage_name in receipt["stage_order"]:
        assert stage_packets[stage_name]["time"] != source_time_utc.isoformat().replace(
            "+00:00", "Z"
        )


def test_serial_runtime_mapping_fallback_ignores_extra_trading_authority_keys() -> None:
    receipt = DeskRuntimeOrchestrator().run_once(
        {
            "temporal": {"source_timezone_raw": "America/New_York"},
            "capital": {"authorised_notional_usd": 1000.0},
            "live_inventory": {"position_id": "NVDA-LIVE"},
        }
    )

    assert receipt["executed_stages"] == ["temporal"]
    assert "capital" not in receipt["executed_stages"]
    assert "live_inventory" not in receipt["executed_stages"]
    assert receipt["missing_stages"] == [
        "regime",
        "options_flow",
        "posture",
        "eligibility",
        "execution",
    ]
    assert "stage_packets" not in receipt
