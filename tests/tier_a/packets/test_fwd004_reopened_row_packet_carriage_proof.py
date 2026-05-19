from __future__ import annotations

from datetime import UTC, datetime

import pytest

from nvda_desk.contracts.packets import DeskModulePacketV3, DmpV3Envelope
from nvda_desk.packets.dmp_packets import DmpPacketBuilder, build_dmp_v3_packet
from nvda_desk.persistence.execution_records import ExecutionRecordsRepository
from nvda_desk.repositories.position_repository import PositionRepository
from nvda_desk.review.packet_service import ReviewPacketService


REOPENED_ROW_CASES = (
    ("FWD004-AUDIT-001", "atlas_donor_dmp_envelope_001", "dependency_light_seam"),
    ("FWD004-AUDIT-002", "atlas_donor_dmp_envelope_002", "contract_primitives"),
    ("FWD004-AUDIT-003", "atlas_donor_dmp_envelope_003", "contract_primitives"),
    ("FWD004-AUDIT-004", "atlas_donor_dmp_envelope_004", "contract_primitives"),
    ("FWD004-AUDIT-005", "atlas_donor_dmp_envelope_005", "contract_primitives"),
    ("FWD004-AUDIT-006", "atlas_donor_dmp_envelope_006", "contract_primitives"),
    ("FWD004-AUDIT-007", "atlas_donor_dmp_envelope_007", "extension_merge_guard"),
    ("FWD004-AUDIT-008", "atlas_donor_dmp_envelope_008", "outer_envelope_wrapper"),
    ("FWD004-AUDIT-009", "atlas_donor_dmp_envelope_009", "outer_envelope_wrapper"),
    ("FWD004-AUDIT-010", "atlas_donor_dmp_envelope_010", "default_degradation"),
    ("FWD004-AUDIT-011", "atlas_donor_dmp_001", "typed_wrapper_projection"),
    ("FWD004-AUDIT-012", "atlas_donor_dmp_002", "payload_family_carriage"),
    ("FWD004-AUDIT-013", "atlas_donor_dmp_003", "contract_primitives"),
    ("FWD004-AUDIT-014", "atlas_donor_dmp_004", "contract_primitives"),
    ("FWD004-AUDIT-015", "atlas_donor_dmp_005", "contract_primitives"),
    ("FWD004-AUDIT-016", "atlas_donor_dmp_006", "contract_primitives"),
    ("FWD004-AUDIT-017", "atlas_donor_dmp_007", "contract_primitives"),
    ("FWD004-AUDIT-018", "atlas_donor_dmp_008", "payload_family_carriage"),
    ("FWD004-AUDIT-019", "atlas_donor_dmp_009", "payload_family_carriage"),
    ("FWD004-AUDIT-020", "atlas_donor_dmp_010", "payload_family_carriage"),
    ("FWD004-AUDIT-021", "atlas_donor_dmp_011", "payload_family_carriage"),
    ("FWD004-AUDIT-022", "atlas_donor_dmp_012", "typed_wrapper_projection"),
    ("FWD004-AUDIT-023", "atlas_donor_dmp_013", "typed_wrapper_projection"),
    ("FWD004-AUDIT-024", "atlas_donor_dmp_014", "typed_wrapper_projection"),
    ("FWD004-AUDIT-025", "atlas_donor_dmp_015", "typed_wrapper_projection"),
    ("FWD004-AUDIT-026", "atlas_donor_dmp_016", "typed_wrapper_projection"),
    ("FWD004-AUDIT-027", "atlas_donor_dmp_017", "typed_wrapper_projection"),
    ("FWD004-AUDIT-028", "atlas_donor_dmp_018", "builder_default_surface"),
    ("FWD004-AUDIT-030", "atlas_donor_temporal_surface_010", "stage_payload_carriage"),
    ("FWD004-AUDIT-031", "atlas_donor_parallel_risk_001", "parallel_risk_packet"),
    ("FWD004-AUDIT-036", "atlas_donor_cognition_014", "stage_payload_carriage"),
    ("FWD004-AUDIT-037", "atlas_donor_cognition_022", "stage_payload_carriage"),
    ("FWD004-AUDIT-039", "atlas_donor_cognition_028", "stage_payload_carriage"),
    ("FWD004-AUDIT-043", "atlas_donor_domain_temporal_state_008", "stage_payload_carriage"),
    ("FWD004-AUDIT-044", "atlas_donor_config_models_019", "reference_payload_carriage"),
    ("FWD004-AUDIT-045", "atlas_donor_config_models_022", "reference_payload_carriage"),
    ("FWD004-AUDIT-046", "atlas_donor_config_models_024", "reference_payload_carriage"),
    ("FWD004-AUDIT-047", "atlas_donor_config_models_027", "reference_payload_carriage"),
    ("FWD004-AUDIT-048", "atlas_donor_config_models_029", "reference_payload_carriage"),
    ("FWD004-AUDIT-049", "atlas_donor_config_models_031", "reference_payload_carriage"),
    ("FWD004-AUDIT-050", "atlas_donor_service_financial_calendar_reference_001", "reference_payload_carriage"),
    ("FWD004-AUDIT-052", "atlas_donor_service_carry_handoff_004", "stage_payload_carriage"),
    ("FWD004-AUDIT-053", "atlas_donor_service_carry_handoff_005", "stage_payload_carriage"),
    ("FWD004-AUDIT-054", "atlas_donor_service_carry_market_004", "stage_payload_carriage"),
    ("FWD004-AUDIT-056", "atlas_donor_service_review_packets_002", "review_service_identity"),
    ("FWD004-AUDIT-057", "atlas_donor_service_review_packets_003", "module_health_packet"),
    ("FWD004-AUDIT-058", "atlas_donor_service_review_packets_004", "review_safe_rendering"),
    ("FWD004-AUDIT-059", "atlas_donor_service_review_packets_005", "review_safe_rendering"),
    ("FWD004-AUDIT-060", "atlas_donor_service_review_packets_006", "review_safe_rendering"),
    ("FWD004-AUDIT-061", "atlas_donor_service_review_packets_007", "review_safe_rendering"),
    ("FWD004-AUDIT-062", "atlas_donor_service_review_packets_008", "daily_review_packet"),
    ("FWD004-AUDIT-063", "atlas_donor_service_review_packets_009", "daily_review_packet"),
    ("FWD004-AUDIT-064", "atlas_donor_service_review_packets_010", "review_service_identity"),
    ("FWD004-AUDIT-065", "atlas_donor_service_review_packets_011", "module_health_packet"),
    ("FWD004-AUDIT-066", "atlas_donor_service_review_packets_012", "module_health_packet"),
    ("FWD004-AUDIT-067", "atlas_donor_service_review_packets_013", "module_health_packet"),
    ("FWD004-AUDIT-068", "atlas_donor_service_review_packets_014", "module_health_packet"),
    ("FWD004-AUDIT-072", "atlas_donor_posture_risk_003", "stage_payload_carriage"),
    ("FWD004-AUDIT-073", "atlas_donor_cognition_runtime_service_011", "parallel_risk_packet"),
)


@pytest.mark.parametrize(("audit_row_id", "atlas_record_id", "behaviour"), REOPENED_ROW_CASES)
def test_fwd004_reopened_rows_have_real_packet_carriage_behaviour(
    audit_row_id: str, atlas_record_id: str, behaviour: str
) -> None:
    assert atlas_record_id
    emitted_at = datetime(2026, 5, 19, 10, 0, tzinfo=UTC)

    if behaviour == "dependency_light_seam":
        packet = build_dmp_v3_packet(
            packet_id=audit_row_id,
            dataschema="nvda.test.DependencyLightPayload.v1",
            data={"atlas_record_id": atlas_record_id},
            packetrole="stage_packet",
            module_id="fwd004_packet_surface",
            grammar_role="serial_runtime",
            behaviour_class="stage_output",
            emitted_at=emitted_at,
            traceid=f"trace::{audit_row_id}",
            runid=f"run::{audit_row_id}",
        )
        assert isinstance(packet, DeskModulePacketV3)
        assert packet.id == audit_row_id
        assert packet.data == {"atlas_record_id": atlas_record_id}
        assert packet.source == "urn:nvda:producer:fwd004_packet_surface"
        assert packet.type == "urn:nvda:packet:stage_packet"
        return

    if behaviour == "contract_primitives":
        packet = build_dmp_v3_packet(
            packet_id=audit_row_id,
            dataschema="nvda.test.ContractPrimitivePayload.v1",
            data={"atlas_record_id": atlas_record_id},
            packetrole="stage_packet",
            module_id="fwd004_packet_surface",
            grammar_role="serial_runtime",
            behaviour_class="stage_output",
            emitted_at=emitted_at,
            traceid=f"trace::{audit_row_id}",
            runid=f"run::{audit_row_id}",
            parentids=["parent-a"],
            dependencyids=["dependency-a"],
            summary_headline="primitive packet emitted",
            summary_keyflags=["primitive"],
        )
        assert packet.producer.module_id == "fwd004_packet_surface"
        assert packet.producer.grammar_role == "serial_runtime"
        assert packet.producer.behaviour_class == "stage_output"
        assert packet.lineage.parentids == ["parent-a"]
        assert packet.lineage.dependencyids == ["dependency-a"]
        assert packet.validation.status == "valid"
        assert packet.summary.headline == "primitive packet emitted"
        assert packet.summary.keyflags == ["primitive"]
        return

    if behaviour == "extension_merge_guard":
        packet = build_dmp_v3_packet(
            packet_id=audit_row_id,
            dataschema="nvda.test.ExtensionPayload.v1",
            data={"atlas_record_id": atlas_record_id},
            packetrole="stage_packet",
            module_id="fwd004_packet_surface",
            grammar_role="serial_runtime",
            behaviour_class="stage_output",
            emitted_at=emitted_at,
            traceid=f"trace::{audit_row_id}",
            runid=f"run::{audit_row_id}",
            dependencyids=["canonical-dependency"],
            dmpextensions={
                "nvda": {
                    "schema_identifiers": {"payload_model_name": "Injected"},
                    "semantic_dependencies": ["injected"],
                    "custom_leaf": {"preserved": True},
                },
                "custom": {"leaf": "preserved"},
            },
        )
        assert packet.dmpextensions["nvda"]["schema_identifiers"]["payload_model_name"] == "dict"
        assert packet.dmpextensions["nvda"]["semantic_dependencies"] == ["canonical-dependency"]
        assert packet.dmpextensions["nvda"]["custom_leaf"] == {"preserved": True}
        assert packet.dmpextensions["custom"] == {"leaf": "preserved"}
        return

    if behaviour == "outer_envelope_wrapper":
        packet = build_dmp_v3_packet(
            packet_id=audit_row_id,
            dataschema="nvda.test.EnvelopePayload.v1",
            data={"atlas_record_id": atlas_record_id},
            packetrole="stage_packet",
            module_id="fwd004_packet_surface",
            grammar_role="serial_runtime",
            behaviour_class="stage_output",
            emitted_at=emitted_at,
            traceid=f"trace::{audit_row_id}",
            runid=f"run::{audit_row_id}",
        )
        assert isinstance(packet, DmpV3Envelope)
        assert packet.specversion == "1.0"
        assert packet.dmpversion == "3.0.0"
        assert packet.datacontenttype == "application/json"
        assert packet.packet_id == audit_row_id
        assert packet.emitted_at == emitted_at
        return

    if behaviour == "default_degradation":
        packet = DmpPacketBuilder.build_reference_packet(
            packet_id=audit_row_id,
            dataschema="nvda.test.DefaultedReferencePayload.v1",
            data={"atlas_record_id": atlas_record_id},
            emitted_at=emitted_at,
        )
        assert packet.traceid == f"trace::{audit_row_id}"
        assert packet.runid == f"run::{audit_row_id}"
        assert packet.validation.status == "degraded"
        assert packet.validation.violations == [
            "traceid_defaulted_from_packet_id",
            "runid_defaulted_from_packet_id",
        ]
        assert set(packet.summary.keyflags) >= set(packet.validation.violations)
        return

    if behaviour == "typed_wrapper_projection":
        packet = build_dmp_v3_packet(
            packet_id=audit_row_id,
            dataschema="nvda.test.TypedWrapperPayload.v1",
            data={"atlas_record_id": atlas_record_id},
            packetrole="stage_packet",
            module_id="fwd004_packet_surface",
            grammar_role="serial_runtime",
            behaviour_class="stage_output",
            emitted_at=emitted_at,
            traceid=f"trace::{audit_row_id}",
            runid=f"run::{audit_row_id}",
        )
        reparsed = DeskModulePacketV3.model_validate(packet.model_dump())
        assert reparsed == packet
        assert reparsed.packet_id == audit_row_id
        assert reparsed.emitted_at == emitted_at
        return

    if behaviour == "payload_family_carriage":
        payload = {"atlas_record_id": atlas_record_id, "payload_family": "admitted"}
        packet = build_dmp_v3_packet(
            packet_id=audit_row_id,
            dataschema="nvda.test.AdmittedPayloadFamily.v1",
            data=payload,
            packetrole="stage_packet",
            module_id="payload_family_surface",
            grammar_role="serial_runtime",
            behaviour_class="stage_output",
            emitted_at=emitted_at,
            traceid=f"trace::{audit_row_id}",
            runid=f"run::{audit_row_id}",
        )
        assert packet.data == payload
        assert packet.dataschema == "nvda.test.AdmittedPayloadFamily.v1"
        assert packet.dmpextensions["nvda"]["schema_identifiers"] == {
            "payload_model_name": "dict",
            "payload_module_path": "builtins",
            "output_model_name": "dict",
        }
        return

    if behaviour == "builder_default_surface":
        packet = DmpPacketBuilder.build_dmp_v3_packet(
            packet_id=audit_row_id,
            dataschema="nvda.test.BuilderDefaultPayload.v1",
            data={"atlas_record_id": atlas_record_id},
            packetrole="stage_packet",
            module_id="builder_default_surface",
            grammar_role="serial_runtime",
            behaviour_class="stage_output",
            emitted_at=emitted_at,
            traceid=f"trace::{audit_row_id}",
            runid=f"run::{audit_row_id}",
        )
        assert packet.producer.module_version == "native"
        assert packet.producer.module_instance_id == "builder_default_surface::default"
        assert packet.summary.headline == "builder_default_surface emitted stage_packet"
        assert packet.summary.humanstate == "valid"
        return

    if behaviour == "stage_payload_carriage":
        packet = DmpPacketBuilder.build_stage_packet(
            packet_id=audit_row_id,
            dataschema="nvda.test.StagePayload.v1",
            data={"atlas_record_id": atlas_record_id, "stage": "carried"},
            emitted_at=emitted_at,
            traceid=f"trace::{audit_row_id}",
            runid=f"run::{audit_row_id}",
            module_id="serial_stage_surface",
            stage_name="fwd004_stage_surface",
            dependencyids=["upstream-packet"],
        )
        assert packet.packetrole == "stage_packet"
        assert packet.producer.stage_name == "fwd004_stage_surface"
        assert packet.producer.behaviour_class == "stage_output"
        assert packet.lineage.dependencyids == ["upstream-packet"]
        assert packet.dmpextensions["nvda"]["semantic_dependencies"] == ["upstream-packet"]
        return

    if behaviour == "parallel_risk_packet":
        packet = DmpPacketBuilder.build_parallel_risk_packet(
            packet_id=audit_row_id,
            dataschema="nvda.test.ParallelRiskPayload.v1",
            data={"atlas_record_id": atlas_record_id, "lane": "parallel_risk"},
            emitted_at=emitted_at,
            traceid=f"trace::{audit_row_id}",
            runid=f"run::{audit_row_id}",
            dependencyids=["temporal-input"],
        )
        assert packet.packetrole == "parallel_risk_packet"
        assert packet.producer.module_id == "parallel_risk_lane"
        assert packet.producer.grammar_role == "parallel_risk_lane"
        assert packet.producer.behaviour_class == "module_output"
        assert packet.lineage.dependencyids == ["temporal-input"]
        return

    if behaviour == "reference_payload_carriage":
        packet = DmpPacketBuilder.build_reference_packet(
            packet_id=audit_row_id,
            dataschema="nvda.test.ReferencePayload.v1",
            data={"atlas_record_id": atlas_record_id, "reference": "carried"},
            emitted_at=emitted_at,
            traceid=f"trace::{audit_row_id}",
            runid=f"run::{audit_row_id}",
            sourceartifactids=["reference-source-artifact"],
        )
        assert packet.packetrole == "reference_packet"
        assert packet.producer.grammar_role == "reference_data"
        assert packet.producer.behaviour_class == "module_output"
        assert packet.lineage.sourceartifactids == ["reference-source-artifact"]
        return

    if behaviour == "review_service_identity":
        service = _review_service()
        health = service.build_module_health_packet(packet_id=audit_row_id)
        module_ids = [summary.module_id for summary in health.module_summaries]
        assert module_ids == ["module-a", "module-b"]
        assert service.daily_pnl_service is not None
        return

    if behaviour == "module_health_packet":
        service = _review_service()
        health = service.build_module_health_packet(packet_id=audit_row_id)
        module_a = health.module_summaries[0]
        assert health.packet_id == audit_row_id
        assert module_a.module_id == "module-a"
        assert module_a.order_event_count == 1
        assert module_a.fill_event_count == 1
        assert module_a.record_count == 2
        assert health.position_snapshot_count == 1
        assert health.rendering_authority_mutated is False
        return

    if behaviour == "review_safe_rendering":
        service = _review_service()
        rendering = service.render_review_safe_packet(
            packet_id=audit_row_id,
            packet_kind="review_surface",
            payload={
                "atlas_record_id": atlas_record_id,
                "safe_evidence": {"retained": True},
                "order_submitted": True,
                "nested": {"execution_allowed": True, "safe_nested": "retained"},
            },
        )
        assert rendering.packet_id == audit_row_id
        assert rendering.packet_kind == "review_surface"
        assert rendering.review_safe_payload["atlas_record_id"] == atlas_record_id
        assert rendering.review_safe_payload["safe_evidence"] == {"retained": True}
        assert "order_submitted" not in rendering.review_safe_payload
        assert rendering.review_safe_payload["nested"] == {"safe_nested": "retained"}
        assert rendering.redacted_keys == ("execution_allowed", "order_submitted")
        assert rendering.runtime_authority_mutated is False
        return

    if behaviour == "daily_review_packet":
        service = _review_service()
        rendering = service.render_review_safe_packet(
            packet_id=f"{audit_row_id}::rendering",
            packet_kind="promotion_evidence",
            payload={"atlas_record_id": atlas_record_id, "safe": True},
        )
        daily = service.build_daily_review_packet(
            packet_id=audit_row_id,
            symbol="nvda",
            trade_date="2026-05-19",
            renderings=(rendering,),
        )
        assert daily.packet_id == audit_row_id
        assert daily.symbol == "NVDA"
        assert daily.daily_pnl.report_id == f"{audit_row_id}::pnl-fallback"
        assert daily.daily_pnl.context == {"fallback": True}
        assert daily.module_health.packet_id == f"{audit_row_id}::module-health"
        assert daily.renderings == (rendering,)
        assert daily.rendering_authority_mutated is False
        return

    raise AssertionError(f"Unhandled FWD-004 reopened row behaviour: {behaviour}")


def _review_service() -> ReviewPacketService:
    execution_records = ExecutionRecordsRepository()
    execution_records.append_record({"module_id": "module-a", "record_type": "order_event"})
    execution_records.append_record({"module_id": "module-a", "record_type": "fill_event"})
    positions = PositionRepository()
    positions.write_position("pos-1", {"symbol": "NVDA"})
    return ReviewPacketService(
        execution_records=execution_records,
        position_repository=positions,
        active_module_ids=("module-a", "module-b"),
    )
