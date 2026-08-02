from __future__ import annotations

from datetime import UTC, datetime

from tests.support.dmpv3_current_builder import current_packet_kwargs

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
        dmpextensions={
            "nvda": {
                "execution_context": {"stack_id": "stack-extension-leaf"},
            },
            "custom": {"reader_hint": "preserve-me"},
        },
        **current_packet_kwargs(
            role="stage_packet",
            packet_id="pkt-extension-leaf-1",
            emitted_at=datetime(2026, 4, 21, 9, 55, tzinfo=UTC),
            dependencyids=["canonical-dependency-1"],
        ),
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
        dmpextensions={
            "nvda": {
                "semantic_dependencies": ["injected-dependency"],
                "execution_context": {"stack_id": "stack-semantic-dependency-guard"},
            }
        },
        **current_packet_kwargs(
            role="stage_packet",
            packet_id="pkt-semantic-dependency-guard-1",
            emitted_at=datetime(2026, 4, 21, 10, 5, tzinfo=UTC),
            dependencyids=["canonical-dependency-1", "canonical-dependency-2"],
        ),
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
