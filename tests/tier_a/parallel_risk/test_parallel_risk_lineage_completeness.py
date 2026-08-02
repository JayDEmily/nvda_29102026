from __future__ import annotations

from datetime import UTC, datetime

from tests.support.dmpv3_current_builder import parallel_risk_compatibility_authority

from nvda_desk.contracts.options_flow import OptionsFlowContextInput
from nvda_desk.contracts.parallel_risk import (
    EventProximityRegisterEntry,
    FreshnessRegisterEntry,
    ParallelRiskPreparationPacket,
)
from nvda_desk.contracts.regime import MarketRegimeContextInput
from nvda_desk.contracts.temporal import TemporalContextInput
from nvda_desk.domain.parallel_risk.minute_profile_assembly import (
    assemble_parallel_risk_minute_profile,
)


def test_minute_profile_lineage_preserves_packet_ids_source_refs_and_forbidden_authority_trace() -> (
    None
):
    packet = ParallelRiskPreparationPacket(
        temporal_input=TemporalContextInput(
            source_time_utc=datetime(2026, 5, 18, 14, 30, tzinfo=UTC)
        ),
        regime_input=MarketRegimeContextInput(vix_level=31.0),
        options_flow_input=OptionsFlowContextInput(spot_price=101.0, front_dte=5, next_dte=1),
        bootstrap_source="stage_input_bundle.parallel_risk_primitives",
    )
    profile = assemble_parallel_risk_minute_profile(
        packet=packet,
        packet_id="profile-lineage",
        symbol="NVDA",
        generated_at_utc=datetime(2026, 5, 18, 14, 30, 1, tzinfo=UTC),
        freshness_entries=[
            FreshnessRegisterEntry(
                signal_id="vix_level",
                freshness_state="fresh",
                impact_on_profile="freshness_supports_current_state_read",
                source_refs=["market-data-lineage:vix"],
            )
        ],
        event_proximity_entries=[
            EventProximityRegisterEntry(
                event_id="earnings-nvda",
                event_type="earnings",
                risk_interpretation="event_proximity_state_of_play_only",
                runtime_tags=["scheduled_event_window_active"],
                source_refs=["calendar-lineage:earnings-nvda"],
            )
        ],
        parent_packet_ids=["parent-packet"],
        dependency_packet_ids=["dependency-packet"],
        source_artifact_ids=["source-artifact"],
        input_fingerprint="sha256:fixture",
    )

    assert profile.lineage["bootstrap_source"] == "stage_input_bundle.parallel_risk_primitives"
    assert profile.lineage["parent_packet_ids"] == ["parent-packet"]
    assert profile.lineage["dependency_packet_ids"] == ["dependency-packet"]
    assert profile.lineage["source_artifact_ids"] == ["source-artifact"]
    assert profile.lineage["input_fingerprint"] == "sha256:fixture"
    assert profile.lineage["forbidden_authority_keys_consumed"] == []
    assert profile.lineage["admitted_semantic_inputs"] == [
        "temporal_input",
        "regime_input",
        "options_flow_input",
    ]

    assert {"source-artifact"} <= set().union(
        *(set(entry.lineage_refs) for entry in profile.signal_snapshot)
    )
    assert {"market-data-lineage:vix", "calendar-lineage:earnings-nvda"} <= set().union(
        *(set(atom.source_refs) for atom in profile.active_risk_atoms)
    )
    assert all(family.dominant_atoms for family in profile.risk_family_states)


def test_service_optional_profile_carries_lineage_without_hidden_authority() -> None:
    from nvda_desk.contracts.stage_inputs import StageInputBundle
    from nvda_desk.services.parallel_risk_lane_service import ParallelRiskLaneService

    result = ParallelRiskLaneService().run_bootstrap(
        stage_input_bundle=StageInputBundle(
            temporal=TemporalContextInput(
                source_time_utc=datetime(2026, 5, 18, 14, 30, tzinfo=UTC)
            ),
            regime=MarketRegimeContextInput(vix_level=31.0),
            options_flow=OptionsFlowContextInput(spot_price=101.0, front_dte=5, next_dte=1),
        ),
        input_packet_id="dmp::parallel_risk::bootstrap_input::lineage-service",
        output_packet_id="dmp::parallel_risk::output::lineage-service",
        **parallel_risk_compatibility_authority(
            "lineage-service",
            sourceartifactids=["service-source-artifact"],
            inputfingerprint="sha256:service-fixture",
        ),
        include_minute_profile=True,
    )

    profile = result["minute_profile"]
    assert profile.lineage["source_artifact_ids"] == ["service-source-artifact"]
    assert profile.lineage["input_fingerprint"] == "sha256:service-fixture"
    assert profile.lineage["forbidden_authority_keys_consumed"] == []
    assert profile.authority_flags.direct_workbook_runtime_read_allowed is False
    assert profile.authority_flags.capital_sizing_allowed is False
