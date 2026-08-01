from __future__ import annotations

from datetime import UTC, datetime

from nvda_desk.contracts.packets import DmpV3Envelope
from nvda_desk.packets.dmp_packets import build_dmp_v3_packet


def test_dmpv3_extension_canonical_leaf_contract_surface_is_present() -> None:
    assert DmpV3Envelope is not None
    assert build_dmp_v3_packet is not None


def test_dmpv3_custom_extension_leaf_survives_canonical_merge() -> None:
    packet = build_dmp_v3_packet(
        packet_id="pkt-extension-leaf-1",
        dataschema="TemporalContextOutput",
        data={"state": "ready"},
        packetrole="stage_packet",
        module_id="temporal_context",
        grammar_role="serial_runtime",
        behaviour_class="stage_output",
        emitted_at=datetime(2026, 4, 21, 9, 55, tzinfo=UTC),
        traceid="trace-extension-leaf",
        runid="run-extension-leaf",
        dependencyids=["canonical-dependency-1"],
        dmpextensions={
            "nvda": {
                "execution_context": {"stack_id": "stack-extension-leaf"},
            },
            "custom": {"reader_hint": "preserve-me"},
        },
    )

    assert packet.dmpextensions["nvda"]["execution_context"] == {"stack_id": "stack-extension-leaf"}
    assert packet.dmpextensions["custom"] == {"reader_hint": "preserve-me"}


def test_dmpv3_extensions_cannot_replace_canonical_semantic_dependencies() -> None:
    packet = build_dmp_v3_packet(
        packet_id="pkt-semantic-dependency-guard-1",
        dataschema="TemporalContextOutput",
        data={"state": "ready"},
        packetrole="stage_packet",
        module_id="temporal_context",
        grammar_role="serial_runtime",
        behaviour_class="stage_output",
        emitted_at=datetime(2026, 4, 21, 10, 5, tzinfo=UTC),
        traceid="trace-semantic-dependency-guard",
        runid="run-semantic-dependency-guard",
        dependencyids=["canonical-dependency-1", "canonical-dependency-2"],
        dmpextensions={
            "nvda": {
                "semantic_dependencies": ["injected-dependency"],
                "execution_context": {"stack_id": "stack-semantic-dependency-guard"},
            }
        },
    )

    assert packet.lineage.dependencyids == [
        "canonical-dependency-1",
        "canonical-dependency-2",
    ]
    assert packet.dmpextensions["nvda"]["semantic_dependencies"] == [
        "canonical-dependency-1",
        "canonical-dependency-2",
    ]
    assert packet.dmpextensions["nvda"]["execution_context"] == {
        "stack_id": "stack-semantic-dependency-guard"
    }
