"""Bounded parallel-risk coordination helpers."""

from __future__ import annotations

from nvda_desk.contracts.packets import DeskModulePacketV3
from nvda_desk.contracts.parallel_risk import (
    PARALLEL_RISK_BOOTSTRAP_INPUT_DATASCHEMA,
    PARALLEL_RISK_FORBIDDEN_AUTHORITY_KEYS,
    SERIAL_RUNTIME_TEMPORAL_BOOTSTRAP_SOURCE,
    STAGE_INPUT_BUNDLE_PARALLEL_RISK_PRIMITIVES_SOURCE,
    STAGE_INPUT_BUNDLE_TEMPORAL_BOOTSTRAP_SOURCE,
    ParallelRiskFragilityDimension,
    ParallelRiskInputTrace,
    ParallelRiskLanePacket,
    ParallelRiskPreparationPacket,
    build_parallel_risk_bootstrap_input_packet,
    build_parallel_risk_bootstrap_input_packet_from_temporal_stage_packet,
    build_parallel_risk_lane_output_packet,
)
from nvda_desk.contracts.stage_inputs import StageInputBundle
from nvda_desk.domain.parallel_risk.candidate_audit import audit_candidate
from nvda_desk.domain.parallel_risk.environment_assessment import (
    assess_environment,
    assess_risk_envelope,
)

# This module retains the old bootstrap-packet evaluator only as compatibility
# evidence. Canonical M06 authority is nvda_desk.m06_parallel_risk and its
# DMPV3 egress adapter; this module must not feed canonical M09 ingress.
CANONICAL_M06_ROUTE = False
COMPATIBILITY_SCOPE = "legacy_parallel_risk_bootstrap_specimen"


class ParallelRiskService:
    """Coordinate the bounded Module 8 bootstrap path only."""

    def build_bootstrap_input_packet(
        self,
        *,
        stage_input_bundle: StageInputBundle,
        packet_id: str,
        traceid: str | None = None,
        runid: str | None = None,
        scenarioid: str | None = None,
        emitted_at=None,
        derivedfrom: str | None = None,
        sourceartifactids: list[str] | None = None,
        inputfingerprint: str | None = None,
        dmpextensions: dict | None = None,
    ) -> DeskModulePacketV3:
        return build_parallel_risk_bootstrap_input_packet(
            stage_input_bundle=stage_input_bundle,
            packet_id=packet_id,
            traceid=traceid,
            runid=runid,
            scenarioid=scenarioid,
            emitted_at=emitted_at,
            derivedfrom=derivedfrom,
            sourceartifactids=sourceartifactids,
            inputfingerprint=inputfingerprint,
            dmpextensions=dmpextensions,
        )

    def build_bootstrap_input_packet_from_temporal_stage_packet(
        self,
        *,
        temporal_stage_packet: DeskModulePacketV3,
        packet_id: str,
        traceid: str | None = None,
        runid: str | None = None,
        scenarioid: str | None = None,
        emitted_at=None,
        derivedfrom: str | None = None,
        sourceartifactids: list[str] | None = None,
        inputfingerprint: str | None = None,
        dmpextensions: dict | None = None,
    ) -> DeskModulePacketV3:
        return build_parallel_risk_bootstrap_input_packet_from_temporal_stage_packet(
            temporal_stage_packet=temporal_stage_packet,
            packet_id=packet_id,
            traceid=traceid,
            runid=runid,
            scenarioid=scenarioid,
            emitted_at=emitted_at,
            derivedfrom=derivedfrom,
            sourceartifactids=sourceartifactids,
            inputfingerprint=inputfingerprint,
            dmpextensions=dmpextensions,
        )

    def evaluate(
        self, preparation_packet: DeskModulePacketV3, *, output_packet_id: str
    ) -> DeskModulePacketV3:
        return evaluate_parallel_risk(
            preparation_packet=preparation_packet, output_packet_id=output_packet_id
        )


def evaluate_parallel_risk(
    *, preparation_packet: DeskModulePacketV3, output_packet_id: str
) -> DeskModulePacketV3:
    _validate_parallel_risk_packet_authority(preparation_packet)
    payload = _coerce_preparation_payload(preparation_packet)
    environment = assess_environment(payload)
    risk_envelope = assess_risk_envelope(payload)
    lane_payload = ParallelRiskLanePacket(
        environment_assessment=environment,
        risk_envelope=risk_envelope,
        input_trace=_build_input_trace(preparation_packet=preparation_packet, payload=payload),
        invariant_reads=list(payload.invariant_reads),
        stage_read_state=[record.model_copy(deep=True) for record in payload.stage_read_state],
        notes=[
            "stage_a_bootstrap_complete",
            "stage_b_reserved_without_lawful_upstream_packets",
            "stage_c_reserved_without_lawful_upstream_packets",
        ],
    )
    return build_parallel_risk_lane_output_packet(
        packet_id=output_packet_id,
        payload=lane_payload,
        emitted_at=preparation_packet.emitted_at,
        traceid=preparation_packet.traceid,
        runid=preparation_packet.runid,
        scenarioid=preparation_packet.scenarioid,
        parentids=[preparation_packet.packet_id],
        dependencyids=[preparation_packet.packet_id],
        derivedfrom=preparation_packet.lineage.derivedfrom,
        sourceartifactids=list(preparation_packet.lineage.sourceartifactids),
        inputfingerprint=preparation_packet.lineage.inputfingerprint,
        dmpextensions=dict(preparation_packet.dmpextensions),
    )


def enrich_market_translation(*, preparation_packet: DeskModulePacketV3) -> dict:
    del preparation_packet
    raise NotImplementedError(
        "Stage B market translation remains reserved because the accepted baseline does not expose lawful native upstream packet inputs for it."
    )


def enrich_candidate_semantics(
    *,
    candidate_id: str | None = None,
    semantic_tags: list[str] | None = None,
    fragility_dimensions: list[ParallelRiskFragilityDimension] | None = None,
    risk_event_ids: list[str] | None = None,
):
    """Return bounded Stage C candidate semantics without capital or arbitration authority."""

    return audit_candidate(
        candidate_id=candidate_id,
        semantic_tags=semantic_tags,
        fragility_dimensions=fragility_dimensions or [],
        risk_event_ids=risk_event_ids or [],
    )


def preview_candidate_audit(
    *,
    candidate_id: str | None = None,
    semantic_tags: list[str] | None = None,
    fragility_dimensions: list[ParallelRiskFragilityDimension] | None = None,
):
    """Return the bounded candidate-audit surface without widening the live bootstrap path."""

    return audit_candidate(
        candidate_id=candidate_id,
        semantic_tags=semantic_tags,
        fragility_dimensions=fragility_dimensions or [],
    )


def _coerce_preparation_payload(
    preparation_packet: DeskModulePacketV3,
) -> ParallelRiskPreparationPacket:
    if preparation_packet.dataschema != PARALLEL_RISK_BOOTSTRAP_INPUT_DATASCHEMA:
        raise ValueError(
            f"parallel risk bootstrap input packet requires dataschema {PARALLEL_RISK_BOOTSTRAP_INPUT_DATASCHEMA}, got {preparation_packet.dataschema}"
        )
    return ParallelRiskPreparationPacket.model_validate(preparation_packet.data)


def _validate_parallel_risk_packet_authority(preparation_packet: DeskModulePacketV3) -> None:
    """Reject spoofed or authority-smuggling bootstrap packets before evaluation."""

    if preparation_packet.packetrole != "diagnostic_packet":
        raise ValueError("parallel_risk_bootstrap_packetrole_mismatch")
    if preparation_packet.producer.module_id != "parallel_risk_lane_bootstrap_adapter":
        raise ValueError("parallel_risk_bootstrap_producer_mismatch")
    if preparation_packet.producer.grammar_role != "parallel_risk_lane":
        raise ValueError("parallel_risk_bootstrap_producer_mismatch")
    if (
        preparation_packet.producer.behaviour_class != "non_binding_compatibility_diagnostic"
        or "non_binding_compatibility" not in preparation_packet.summary.keyflags
    ):
        raise ValueError("parallel_risk_bootstrap_binding_status_mismatch")

    forbidden_key_paths = _find_forbidden_authority_key_paths(preparation_packet.dmpextensions)
    if forbidden_key_paths:
        raise ValueError("parallel_risk_hidden_authority_key_rejected")


def _build_input_trace(
    *, preparation_packet: DeskModulePacketV3, payload: ParallelRiskPreparationPacket
) -> ParallelRiskInputTrace:
    admitted_inputs = _admitted_semantic_inputs(payload.bootstrap_source)
    selected_stage_packet_ids = []
    if payload.bootstrap_source == SERIAL_RUNTIME_TEMPORAL_BOOTSTRAP_SOURCE:
        selected_stage_packet_ids = list(preparation_packet.lineage.parentids)
        if preparation_packet.lineage.parentids != preparation_packet.lineage.dependencyids:
            raise ValueError("parallel_risk_temporal_stage_lineage_mismatch")
        if len(selected_stage_packet_ids) != 1 or not selected_stage_packet_ids[0].startswith(
            "dmp::serial::temporal::"
        ):
            raise ValueError("parallel_risk_temporal_stage_lineage_mismatch")

    return ParallelRiskInputTrace(
        bootstrap_input_packet_id=preparation_packet.packet_id,
        bootstrap_source=payload.bootstrap_source,
        admitted_semantic_inputs=admitted_inputs,
        parent_packet_ids=list(preparation_packet.lineage.parentids),
        dependency_packet_ids=list(preparation_packet.lineage.dependencyids),
        selected_stage_packet_ids=selected_stage_packet_ids,
    )


def _admitted_semantic_inputs(bootstrap_source: str) -> list[str]:
    if bootstrap_source == STAGE_INPUT_BUNDLE_PARALLEL_RISK_PRIMITIVES_SOURCE:
        return ["temporal_input", "regime_input", "options_flow_input"]
    if bootstrap_source in {
        SERIAL_RUNTIME_TEMPORAL_BOOTSTRAP_SOURCE,
        STAGE_INPUT_BUNDLE_TEMPORAL_BOOTSTRAP_SOURCE,
    }:
        return ["temporal_input"]
    raise ValueError("parallel_risk_bootstrap_source_not_admitted")


def _find_forbidden_authority_key_paths(value: object, *, prefix: str = "") -> list[str]:
    if isinstance(value, dict):
        paths: list[str] = []
        for key, nested in value.items():
            key_text = str(key)
            path = f"{prefix}.{key_text}" if prefix else key_text
            if key_text in PARALLEL_RISK_FORBIDDEN_AUTHORITY_KEYS:
                paths.append(path)
            paths.extend(_find_forbidden_authority_key_paths(nested, prefix=path))
        return paths
    if isinstance(value, (list, tuple)):
        paths = []
        for index, nested in enumerate(value):
            path = f"{prefix}[{index}]" if prefix else f"[{index}]"
            paths.extend(_find_forbidden_authority_key_paths(nested, prefix=path))
        return paths
    return []
