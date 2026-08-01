"""Canonical M06 DMPV3 egress adapter."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import ValidationError

from nvda_desk.contracts.packets import (
    DeskModulePacketV3,
    DmpV3ExecutionContext,
    PreparedContextIdentity,
    dmp_v3_carriage_fingerprint,
)
from nvda_desk.packets.dmp_packets import build_parallel_risk_packet

from .contracts import ParallelRiskAssessment

_PARALLEL_DATASCHEMA = "urn:nvda:m06:parallel-risk-assessment:1.0.0"


def _governed_packet(value: Any, reason: str) -> DeskModulePacketV3:
    if not isinstance(value, DeskModulePacketV3):
        raise TypeError(reason)
    try:
        return DeskModulePacketV3.model_validate(value.model_dump(mode="python"))
    except (ValidationError, ValueError, TypeError) as exc:
        raise ValueError(reason) from exc


class ParallelRiskPacketAdapter:
    """Wrap one immutable M06 assessment without changing risk meaning."""

    def emit(
        self,
        assessment: ParallelRiskAssessment,
        *,
        prepared_context_packet: DeskModulePacketV3,
        execution_context: DmpV3ExecutionContext,
        packet_id: str,
        emitted_at: datetime,
        module_version: str,
        module_instance_id: str,
    ) -> DeskModulePacketV3:
        try:
            risk = ParallelRiskAssessment.model_validate(assessment.model_dump(mode="python"))
        except (AttributeError, ValidationError, ValueError, TypeError) as exc:
            raise ValueError("parallel_risk_assessment_contract_invalid") from exc
        parent = _governed_packet(
            prepared_context_packet,
            "prepared_context_packet_contract_invalid",
        )
        context = DmpV3ExecutionContext.model_validate(execution_context.model_dump())
        if parent.packetrole != "prepared_context_packet":
            raise ValueError("prepared_context_packet_role_invalid")
        if parent.validation.status != "valid":
            raise ValueError("prepared_context_packet_must_be_valid")
        if (parent.traceid, parent.runid, parent.scenarioid) != (
            context.traceid,
            context.runid,
            context.scenarioid,
        ):
            raise ValueError("prepared_packet_execution_context_mismatch")
        try:
            prepared = PreparedContextIdentity.model_validate(parent.data)
        except (ValidationError, ValueError, TypeError) as exc:
            raise ValueError("prepared_context_identity_invalid") from exc
        if (prepared.prepared_id, prepared.prepared_fingerprint) != (
            risk.prepared_id,
            risk.prepared_fingerprint,
        ):
            raise ValueError("parallel_prepared_context_mismatch")
        source_ids = tuple(parent.lineage.sourceartifactids)
        extension = {
            "nvda": {
                "prepared_context": {
                    "packet_id": parent.id,
                    "carriage_fingerprint": dmp_v3_carriage_fingerprint(parent),
                    "prepared_id": prepared.prepared_id,
                    "prepared_fingerprint": prepared.prepared_fingerprint,
                }
            }
        }
        expected_checks = {
            "producer_identity", "role_schema_consistency", "execution_context_ownership",
            "typed_payload", "lineage_profile", "authority_boundary", "extension_bounds",
            "summary_consistency", "parallel_lane_identity", "lawful_input_boundary",
            "material_dependency_closure", "risk_input_fingerprint", "risk_output_identity",
            "serial_candidate_and_capital_separation",
        }
        return build_parallel_risk_packet(
            packet_id=packet_id,
            dataschema=_PARALLEL_DATASCHEMA,
            data=risk,
            emitted_at=emitted_at,
            traceid=context.traceid,
            runid=context.runid,
            scenarioid=context.scenarioid,
            module_id="m06_parallel_risk",
            module_version=module_version,
            module_instance_id=module_instance_id,
            parentids=[parent.id],
            derivedfrom=risk.assessment_id,
            sourceartifactids=list(source_ids),
            inputfingerprint=risk.input_fingerprint,
            decisiontraceid=risk.assessment_id,
            source_artifact_validator=lambda value: value in source_ids,
            input_fingerprint_validator=lambda value: value == risk.input_fingerprint,
            conditional_lineage_fields={"decisiontraceid"},
            owner_check_validator=lambda name, _: name in expected_checks,
            summary_headline="M06 emitted parallel risk assessment",
            summary_keyflags=[risk.state],
            dmpextensions=extension,
        )
