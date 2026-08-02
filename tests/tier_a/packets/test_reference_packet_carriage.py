from __future__ import annotations

from datetime import UTC, datetime

import pytest
from tests.support.dmpv3_current_builder import current_packet_kwargs

from nvda_desk.contracts.packets import (
    DeskModulePacketV3,
    DmpV3Envelope,
    PreparedContextIdentity,
)
from nvda_desk.packets.dmp_packets import DmpPacketBuilder, build_reference_packet
from nvda_desk.schemas.dmp import DmpV3Packet, build_dmp_v3_packet
from nvda_desk.schemas.dmp_envelope import build_dmp_v3_envelope_kwargs


def test_reference_packet_builder_surface_is_present() -> None:
    assert DmpPacketBuilder is not None
    assert build_reference_packet is not None
    assert build_dmp_v3_packet is not None
    assert build_dmp_v3_envelope_kwargs is not None


def test_reference_packet_contract_surface_is_present() -> None:
    assert DmpV3Envelope is not None
    assert DmpV3Packet is not None
    assert DeskModulePacketV3 is not None


def test_reference_packet_builder_rejects_missing_context_then_emits_with_owner_facts() -> None:
    with pytest.raises(ValueError, match="traceid must be a caller-owned governed identity"):
        build_reference_packet(
            packet_id="ref-missing-context",
            dataschema="ImportedReferenceBundle",
            data={"bundle_id": "calendar-1"},
            emitted_at=datetime(2026, 4, 21, 0, 0, tzinfo=UTC),
            sourceartifactids=["calendar-bundle-1"],
        )

    packet = build_reference_packet(
        packet_id="ref-1",
        dataschema="ImportedReferenceBundle",
        data={"bundle_id": "calendar-1"},
        **current_packet_kwargs(
            role="reference_packet",
            packet_id="ref-1",
            emitted_at=datetime(2026, 4, 21, 0, 0, tzinfo=UTC),
            sourceartifactids=["calendar-bundle-1"],
        ),
    )

    assert packet.specversion == "1.0"
    assert packet.dmpversion == "3.0.0"
    assert packet.id == "ref-1"
    assert packet.packetrole == "reference_packet"
    assert packet.producer.module_id == "reference_data"
    assert packet.producer.grammar_role == "reference_data"
    assert packet.producer.behaviour_class == "module_output"
    assert packet.validation.status == "valid"
    assert packet.validation.violations == []
    assert packet.lineage.sourceartifactids == ["calendar-bundle-1"]
    assert packet.summary.headline == "reference_data emitted reference_packet"
    assert packet.summary.humanstate == "valid"
    assert packet.dmpextensions["nvda"]["schema_identifiers"]["payload_model_name"] == "dict"
    assert packet.dmpextensions["nvda"]["semantic_dependencies"] == []

    reparsed = DeskModulePacketV3.model_validate(packet.model_dump())
    assert reparsed == packet


def test_generic_packet_builder_preserves_explicit_lineage_and_extensions() -> None:
    packet = build_dmp_v3_packet(
        packet_id="pkt-1",
        dataschema="TemporalContextOutput",
        data={"state": "ready"},
        packetrole="stage_packet",
        module_id="temporal_context",
        grammar_role="serial_runtime",
        behaviour_class="stage_output",
        stage_name="temporal_context",
        summary_headline="temporal stage emitted",
        summary_keyflags=["aligned"],
        dmpextensions={
            "nvda": {
                "semantic_dependencies": ["dep-1", "dep-2"],
                "execution_context": {"stack_id": "stack-1"},
            }
        },
        **current_packet_kwargs(
            role="stage_packet",
            packet_id="pkt-1",
            emitted_at=datetime(2026, 4, 21, 9, 30, tzinfo=UTC),
            parentids=["parent-1"],
            dependencyids=["dep-1", "dep-2"],
        ),
    )

    assert packet.validation.status == "valid"
    assert packet.lineage.parentids == ["parent-1"]
    assert packet.lineage.dependencyids == ["dep-1", "dep-2"]
    assert packet.producer.stage_name == "temporal_context"
    assert packet.summary.headline == "temporal stage emitted"
    assert packet.summary.keyflags == ["aligned"]
    assert packet.dmpextensions["nvda"]["execution_context"]["stack_id"] == "stack-1"
    assert packet.dmpextensions["nvda"]["schema_identifiers"]["payload_model_name"] == "dict"


def test_prepared_context_and_review_packet_builders_emit_bounded_roles() -> None:
    builder = DmpPacketBuilder
    emitted_at = datetime(2026, 4, 21, 10, 0, tzinfo=UTC)

    prepared_packet = builder.build_prepared_context_packet(
        packet_id="prepared-context-builder-1",
        data=PreparedContextIdentity(
            prepared_id="prepared:builder-1",
            prepared_fingerprint="a" * 64,
            schema_version="1.0.0",
            preparation_policy_version="prepare.1.0.0",
        ),
        **current_packet_kwargs(
            role="prepared_context_packet",
            packet_id="prepared-context-builder-1",
            emitted_at=emitted_at,
            derivedfrom="prepared:builder-1",
        ),
    )
    review_packet = builder.build_review_explanation_packet(
        packet_id="review-explanation-1",
        data={"summary": "deterministic review only"},
        **current_packet_kwargs(
            role="review_explanation_packet",
            packet_id="review-explanation-1",
            emitted_at=emitted_at,
            parentids=[prepared_packet.id],
        ),
    )

    assert prepared_packet.packetrole == "prepared_context_packet"
    assert prepared_packet.producer.stage_name == "runtime_context_preparation"
    assert prepared_packet.producer.behaviour_class == "preparation_output"
    assert review_packet.packetrole == "review_explanation_packet"
    assert review_packet.producer.behaviour_class == "review_only_output"
    assert review_packet.lineage.parentids == ["prepared-context-builder-1"]


def test_dmpv3_extensions_cannot_replace_canonical_schema_identifiers() -> None:
    packet = build_dmp_v3_packet(
        packet_id="pkt-extension-guard-1",
        dataschema="TemporalContextOutput",
        data={"state": "ready"},
        packetrole="stage_packet",
        module_id="temporal_context",
        grammar_role="serial_runtime",
        behaviour_class="stage_output",
        stage_name="temporal_context",
        dmpextensions={
            "nvda": {
                "schema_identifiers": {
                    "payload_model_name": "InjectedPayload",
                    "payload_module_path": "not.canonical",
                    "output_model_name": "InjectedEnvelope",
                },
                "execution_context": {"stack_id": "stack-extension-guard"},
            }
        },
        **current_packet_kwargs(
            role="stage_packet",
            packet_id="pkt-extension-guard-1",
            emitted_at=datetime(2026, 4, 21, 9, 45, tzinfo=UTC),
        ),
    )

    schema_identifiers = packet.dmpextensions["nvda"]["schema_identifiers"]
    assert schema_identifiers["payload_model_name"] == "dict"
    assert schema_identifiers["payload_module_path"] == "builtins"
    assert schema_identifiers["output_model_name"] == "dict"
    assert packet.dmpextensions["nvda"]["execution_context"]["stack_id"] == "stack-extension-guard"
