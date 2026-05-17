"""Coordinate the bounded co-resident parallel-risk lane."""

from __future__ import annotations

from collections.abc import Mapping
from datetime import datetime

from nvda_desk.contracts.packets import DeskModulePacketV3
from nvda_desk.contracts.parallel_risk import (
    ParallelRiskFragilityDimension,
    ParallelRiskPolicyDecision,
)
from nvda_desk.contracts.stage_inputs import StageInputBundle
from nvda_desk.risk.parallel.evaluate import (
    ParallelRiskService,
    enrich_candidate_semantics,
)

_RISK_POLICY_DECISIONS: list[ParallelRiskPolicyDecision] = []

SERIAL_RUNTIME_STAGE_KEYS = (
    "temporal",
    "regime",
    "options_flow",
    "posture",
    "eligibility",
    "execution",
)
SERIAL_RUNTIME_TEMPORAL_PACKET_PREFIX = "dmp::serial::temporal::"


class ParallelRiskLaneService:
    """Run the lawful Module 8 bootstrap path without widening downstream consumers."""

    def __init__(self):
        self._service = ParallelRiskService()

    def build_bootstrap_input_packet(
        self,
        *,
        stage_input_bundle: StageInputBundle,
        packet_id: str,
        traceid: str | None = None,
        runid: str | None = None,
        scenarioid: str | None = None,
        emitted_at: datetime | None = None,
        derivedfrom: str | None = None,
        sourceartifactids: list[str] | None = None,
        inputfingerprint: str | None = None,
        dmpextensions: dict | None = None,
    ) -> DeskModulePacketV3:
        return self._service.build_bootstrap_input_packet(
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

    def evaluate(
        self, *, bootstrap_packet: DeskModulePacketV3, output_packet_id: str
    ) -> DeskModulePacketV3:
        return self._service.evaluate(bootstrap_packet, output_packet_id=output_packet_id)

    def run_bootstrap(
        self,
        *,
        stage_input_bundle: StageInputBundle,
        input_packet_id: str,
        output_packet_id: str,
        traceid: str | None = None,
        runid: str | None = None,
        scenarioid: str | None = None,
        emitted_at: datetime | None = None,
        derivedfrom: str | None = None,
        sourceartifactids: list[str] | None = None,
        inputfingerprint: str | None = None,
        dmpextensions: dict | None = None,
    ) -> dict[str, DeskModulePacketV3]:
        bootstrap_packet = self.build_bootstrap_input_packet(
            stage_input_bundle=stage_input_bundle,
            packet_id=input_packet_id,
            traceid=traceid,
            runid=runid,
            scenarioid=scenarioid,
            emitted_at=emitted_at,
            derivedfrom=derivedfrom,
            sourceartifactids=sourceartifactids,
            inputfingerprint=inputfingerprint,
            dmpextensions=dmpextensions,
        )
        lane_packet = self.evaluate(
            bootstrap_packet=bootstrap_packet,
            output_packet_id=output_packet_id,
        )
        return {
            "bootstrap_input_packet": bootstrap_packet,
            "lane_packet": lane_packet,
        }

    def run_from_serial_runtime(self, *, receipt: Mapping[str, object]) -> dict[str, object]:
        """Run the admitted serial-runtime-to-parallel-risk boundary path."""

        temporal_stage_packet_payload = _select_temporal_stage_packet_payload(receipt)
        temporal_stage_packet_id = _extract_temporal_stage_packet_id(temporal_stage_packet_payload)
        time_token = _derive_time_token(temporal_stage_packet_id)
        bootstrap_input_packet_id = f"dmp::parallel_risk::bootstrap_input::{time_token}"
        lane_packet_id = f"dmp::parallel_risk::output::{time_token}"

        temporal_stage_packet = DeskModulePacketV3.model_validate(
            dict(temporal_stage_packet_payload)
        )
        _validate_selected_temporal_stage_packet(temporal_stage_packet)

        bootstrap_input_packet = (
            self._service.build_bootstrap_input_packet_from_temporal_stage_packet(
                temporal_stage_packet=temporal_stage_packet,
                packet_id=bootstrap_input_packet_id,
            )
        )
        lane_packet = self.evaluate(
            bootstrap_packet=bootstrap_input_packet,
            output_packet_id=lane_packet_id,
        )
        return {
            "selected_stage_packets": {"temporal": temporal_stage_packet},
            "bootstrap_input_packet": bootstrap_input_packet,
            "lane_packet": lane_packet,
        }

    def enrich_candidate_semantics(
        self,
        *,
        candidate_id: str | None = None,
        semantic_tags: list[str] | None = None,
        fragility_dimensions: list[ParallelRiskFragilityDimension] | None = None,
        risk_event_ids: list[str] | None = None,
    ):
        """Project candidate semantics without giving the lane sizing authority."""

        return enrich_candidate_semantics(
            candidate_id=candidate_id,
            semantic_tags=semantic_tags,
            fragility_dimensions=fragility_dimensions or [],
            risk_event_ids=risk_event_ids or [],
        )

    def evaluate_risk_policy(
        self,
        policy_id: str,
        *,
        candidate_id: str | None = None,
        semantic_tags: list[str] | None = None,
    ) -> ParallelRiskPolicyDecision:
        """Record one risk-gateway observation decision without capital sizing authority."""

        candidate = self.enrich_candidate_semantics(
            candidate_id=candidate_id, semantic_tags=semantic_tags
        )
        decision = ParallelRiskPolicyDecision(
            decision_id=f"{policy_id}::{candidate.candidate_id or 'no_candidate'}",
            policy_id=policy_id,
            candidate=candidate,
        )
        _RISK_POLICY_DECISIONS.append(decision)
        return decision

    def list_risk_decisions(self) -> list[ParallelRiskPolicyDecision]:
        """Return risk-gateway observation decisions recorded in this process."""

        return [decision.model_copy(deep=True) for decision in _RISK_POLICY_DECISIONS]


def _select_temporal_stage_packet_payload(receipt: Mapping[str, object]) -> Mapping[str, object]:
    stage_packets = receipt.get("stage_packets")
    if not isinstance(stage_packets, Mapping):
        raise ValueError("serial_runtime_receipt_contract_mismatch")
    if tuple(stage_packets.keys()) != SERIAL_RUNTIME_STAGE_KEYS:
        raise ValueError("serial_runtime_stage_packets_contract_mismatch")
    temporal_stage_packet_payload = stage_packets.get("temporal")
    if not isinstance(temporal_stage_packet_payload, Mapping):
        raise ValueError("serial_runtime_temporal_stage_packet_contract_mismatch")
    return temporal_stage_packet_payload


def _extract_temporal_stage_packet_id(temporal_stage_packet_payload: Mapping[str, object]) -> str:
    temporal_stage_packet_id = temporal_stage_packet_payload.get("id")
    if not isinstance(temporal_stage_packet_id, str):
        raise ValueError("serial_runtime_temporal_stage_packet_contract_mismatch")
    return temporal_stage_packet_id


def _derive_time_token(temporal_stage_packet_id: str) -> str:
    if not temporal_stage_packet_id.startswith(SERIAL_RUNTIME_TEMPORAL_PACKET_PREFIX):
        raise ValueError("serial_runtime_temporal_packet_id_contract_mismatch")
    return temporal_stage_packet_id[len(SERIAL_RUNTIME_TEMPORAL_PACKET_PREFIX) :]


def _validate_selected_temporal_stage_packet(temporal_stage_packet: DeskModulePacketV3) -> None:
    producer = temporal_stage_packet.producer
    if temporal_stage_packet.packetrole != "stage_packet":
        raise ValueError("serial_runtime_temporal_stage_packet_contract_mismatch")
    if producer.module_id != "temporal_context":
        raise ValueError("serial_runtime_temporal_stage_packet_contract_mismatch")
    if producer.grammar_role != "temporal_context":
        raise ValueError("serial_runtime_temporal_stage_packet_contract_mismatch")
    if temporal_stage_packet.dataschema != "TemporalContextOutput":
        raise ValueError("serial_runtime_temporal_stage_packet_contract_mismatch")
