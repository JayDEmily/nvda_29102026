from __future__ import annotations

from datetime import UTC, datetime

from nvda_desk.contracts.options_flow import OptionsFlowContextInput
from nvda_desk.contracts.parallel_risk import FreshnessRegisterEntry, ParallelRiskMinuteProfile
from nvda_desk.contracts.regime import MarketRegimeContextInput
from nvda_desk.contracts.temporal import TemporalContextInput, TemporalEventWindow
from nvda_desk.contracts.parallel_risk import ParallelRiskPreparationPacket
from nvda_desk.domain.parallel_risk.minute_profile_assembly import assemble_parallel_risk_minute_profile


def test_minute_profile_assembly_preserves_current_envelope_and_authority_flags() -> None:
    packet = ParallelRiskPreparationPacket(
        temporal_input=TemporalContextInput(
            source_time_utc=datetime(2026, 5, 18, 14, 30, tzinfo=UTC),
            windows=[
                TemporalEventWindow(
                    event_id="event-1",
                    window_start_utc=datetime(2026, 5, 18, 14, 25, tzinfo=UTC),
                    window_end_utc=datetime(2026, 5, 18, 14, 45, tzinfo=UTC),
                    tags=["scheduled_event_window_active"],
                )
            ],
        ),
        regime_input=MarketRegimeContextInput(vix_level=31.0),
        options_flow_input=OptionsFlowContextInput(spot_price=101.0, front_dte=5, next_dte=1),
        bootstrap_source="stage_input_bundle.parallel_risk_primitives",
    )

    profile = assemble_parallel_risk_minute_profile(
        packet=packet,
        packet_id="prl-minute-assembly-1",
        symbol="NVDA",
        generated_at_utc=datetime(2026, 5, 18, 14, 30, 1, tzinfo=UTC),
        freshness_entries=[
            FreshnessRegisterEntry(
                signal_id="vix_level",
                freshness_state="fresh",
                impact_on_profile="freshness_supports_current_state_read",
            )
        ],
        parent_packet_ids=["parent-1"],
        dependency_packet_ids=["dep-1"],
        source_artifact_ids=["artifact-1"],
    )

    assert isinstance(profile, ParallelRiskMinuteProfile)
    assert profile.risk_envelope_state == "caution"
    assert profile.authority_flags.candidate_formation_allowed is False
    assert profile.authority_flags.capital_sizing_allowed is False
    assert {atom.family for atom in profile.active_risk_atoms} >= {
        "temporal_event_context",
        "market_volatility_context",
        "options_repricing_context",
    }
    assert {entry.signal_id for entry in profile.signal_snapshot} >= {
        "source_time_utc",
        "vix_level",
        "spot_price",
        "front_dte",
        "next_dte",
    }
    assert profile.lineage["parent_packet_ids"] == ["parent-1"]
    assert profile.lineage["dependency_packet_ids"] == ["dep-1"]
    assert profile.lineage["source_artifact_ids"] == ["artifact-1"]
    assert profile.lineage["forbidden_authority_keys_consumed"] == []


def test_minute_profile_assembly_contains_no_trade_action_fields() -> None:
    packet = ParallelRiskPreparationPacket(
        temporal_input=TemporalContextInput(source_time_utc=datetime(2026, 5, 18, 14, 30, tzinfo=UTC)),
    )
    profile = assemble_parallel_risk_minute_profile(
        packet=packet,
        packet_id="prl-minute-assembly-2",
        symbol="NVDA",
        generated_at_utc=datetime(2026, 5, 18, 14, 30, 1, tzinfo=UTC),
    )

    payload = profile.model_dump_json()
    for forbidden in ("buy", "sell", "fade", "chase", "hedge", "brokerage_order", "position_size"):
        assert forbidden not in payload
