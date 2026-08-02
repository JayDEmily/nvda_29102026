from __future__ import annotations

from datetime import UTC, datetime

from tests.support.dmpv3_current_builder import current_packet_kwargs

from nvda_desk.contracts.packets import DeskModulePacketV3
from nvda_desk.packets.dmp_packets import (
    DmpPacketBuilder,
    build_parallel_risk_packet,
    build_stage_packet,
)


def test_parallel_risk_packet_builder_surface_is_present() -> None:
    assert DmpPacketBuilder is not None
    assert build_stage_packet is not None
    assert build_parallel_risk_packet is not None


def test_stage_packet_builder_preserves_explicit_stage_carriage_metadata() -> None:
    authority = current_packet_kwargs(
        role="stage_packet",
        packet_id="stage-1",
        emitted_at=datetime(2026, 4, 21, 9, 31, tzinfo=UTC),
        parentids=["prepared-context-1"],
        derivedfrom="temporal_from_declared_stage_inputs",
        sourceartifactids=["bundle-input-1"],
    )
    packet = build_stage_packet(
        packet_id="stage-1",
        dataschema="TemporalContextOutput",
        data={"session_state": "opening"},
        module_id="temporal_context",
        grammar_role="temporal_context",
        stage_name="temporal",
        summary_headline="session_state=opening",
        **authority,
    )

    assert packet.packetrole == "stage_packet"
    assert packet.producer.module_id == "temporal_context"
    assert packet.producer.grammar_role == "temporal_context"
    assert packet.producer.stage_name == "temporal"
    assert packet.lineage.derivedfrom == "temporal_from_declared_stage_inputs"
    assert packet.lineage.sourceartifactids == ["bundle-input-1"]
    assert packet.lineage.inputfingerprint == authority["inputfingerprint"]
    assert packet.summary.headline == "session_state=opening"
    assert packet.validation.status == "valid"


def test_parallel_risk_packet_builder_emits_stable_parallel_risk_carriage() -> None:
    packet = build_parallel_risk_packet(
        packet_id="risk-1",
        dataschema="ParallelRiskLanePacket",
        data={"risk_state": "caution"},
        summary_headline="parallel risk emitted",
        **current_packet_kwargs(
            role="parallel_risk_packet",
            packet_id="risk-1",
            emitted_at=datetime(2026, 4, 21, 9, 45, tzinfo=UTC),
            parentids=["stage-1"],
            dependencyids=["stage-1", "stage-2"],
            derivedfrom="parallel-risk-from-stages",
            sourceartifactids=["bundle-input-1"],
        ),
    )

    assert packet.packetrole == "parallel_risk_packet"
    assert packet.producer.module_id == "parallel_risk_lane"
    assert packet.producer.grammar_role == "parallel_risk_lane"
    assert packet.producer.behaviour_class == "module_output"
    assert packet.lineage.dependencyids == ["stage-1", "stage-2"]
    assert packet.validation.status == "valid"
    assert packet.summary.headline == "parallel risk emitted"

    reparsed = DeskModulePacketV3.model_validate(packet.model_dump())
    assert reparsed == packet
