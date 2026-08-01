"""Canonical M05 DMPV3 egress adapter."""

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
from nvda_desk.packets.dmp_packets import build_stage_packet

from .contracts import SerialCandidate

_SERIAL_DATASCHEMA = "urn:nvda:m05:serial-candidate:1.0.0"


def _governed_packet(value: Any, reason: str) -> DeskModulePacketV3:
    if not isinstance(value, DeskModulePacketV3):
        raise TypeError(reason)
    try:
        return DeskModulePacketV3.model_validate(value.model_dump(mode="python"))
    except (ValidationError, ValueError, TypeError) as exc:
        raise ValueError(reason) from exc


class SerialCandidatePacketAdapter:
    """Wrap one formed M05 candidate without changing its domain meaning."""

    def emit(
        self,
        candidate: SerialCandidate,
        *,
        prepared_context_packet: DeskModulePacketV3,
        execution_context: DmpV3ExecutionContext,
        packet_id: str,
        emitted_at: datetime,
        module_version: str,
        module_instance_id: str,
    ) -> DeskModulePacketV3:
        if isinstance(candidate, SerialCandidate) and (
            candidate.status != "formed" or not candidate.candidate_id
        ):
            raise ValueError("formed_serial_candidate_required")
        try:
            serial = SerialCandidate.model_validate(candidate.model_dump(mode="python"))
        except (AttributeError, ValidationError, ValueError, TypeError) as exc:
            raise ValueError("serial_candidate_contract_invalid") from exc
        if serial.status != "formed" or not serial.candidate_id:
            raise ValueError("formed_serial_candidate_required")
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
            serial.prepared_id,
            serial.prepared_fingerprint,
        ):
            raise ValueError("serial_prepared_context_mismatch")
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
            "summary_consistency", "stage_identity_and_order",
            "prepared_or_prior_stage_parentage", "material_dependency_closure",
            "stage_input_fingerprint", "domain_output_identity",
            "serial_parallel_capital_boundary",
        }
        return build_stage_packet(
            packet_id=packet_id,
            dataschema=_SERIAL_DATASCHEMA,
            data=serial,
            emitted_at=emitted_at,
            traceid=context.traceid,
            runid=context.runid,
            scenarioid=context.scenarioid,
            module_id="m05_serial_cognition",
            module_version=module_version,
            module_instance_id=module_instance_id,
            grammar_role="serial_cognition",
            stage_name="serial_candidate",
            parentids=[parent.id],
            derivedfrom=serial.serial_result_id,
            sourceartifactids=list(source_ids),
            inputfingerprint=serial.context_fingerprint,
            decisiontraceid=serial.serial_result_id,
            source_artifact_validator=lambda value: value in source_ids,
            input_fingerprint_validator=lambda value: value == serial.context_fingerprint,
            conditional_lineage_fields={"decisiontraceid"},
            owner_check_validator=lambda name, _: name in expected_checks,
            summary_headline="M05 emitted formed serial candidate",
            summary_keyflags=["formed_serial_candidate"],
            dmpextensions=extension,
        )
