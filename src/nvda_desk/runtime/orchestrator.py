"""Run one bounded deterministic serial-runtime pass over admitted stage inputs."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping
from datetime import UTC, datetime
from typing import Any

from pydantic import ValidationError

from nvda_desk.contracts.downstream import DownstreamLiveInventorySnapshot
from nvda_desk.contracts.execution import ExecutionExpressionInput, StageLocalHandoffSurface
from nvda_desk.contracts.serial_spine import (
    SERIAL_SPINE_STAGE_ORDER,
    SERIAL_STAGE_DEPENDENCIES,
    SERIAL_STAGE_LINEAGE_TAGS,
    copy_serial_spine_contract,
    validate_serial_stage_dependencies,
)
from nvda_desk.contracts.stage_inputs import StageInputBundle
from nvda_desk.domain.execution.candidate_expression import evaluate_execution_expression
from nvda_desk.packets.dmp_packets import build_stage_packet
from nvda_desk.services.options_flow_context_service import OptionsFlowContextService
from nvda_desk.services.playbook_eligibility_service import PlaybookEligibilityService
from nvda_desk.services.posture_service import PostureService
from nvda_desk.services.regime_context_service import RegimeContextService
from nvda_desk.services.temporal_context_service import TemporalContextService


class DeskRuntimeOrchestrator:
    """Legacy pre-M00 serial specimen; not the canonical M05/M06-to-M09 route."""

    canonical_runtime_route: bool = False
    compatibility_scope: str = "legacy_pre_m00_serial_runtime_specimen"

    stage_order: tuple[str, ...] = SERIAL_SPINE_STAGE_ORDER

    _stage_dependencies: dict[str, tuple[str, ...]] = validate_serial_stage_dependencies(
        SERIAL_SPINE_STAGE_ORDER, SERIAL_STAGE_DEPENDENCIES
    )

    _stage_packet_metadata: dict[str, dict[str, str]] = {
        "temporal": {
            "module_id": "temporal_context",
            "grammar_role": "temporal_context",
            "dataschema": "TemporalContextOutput",
        },
        "regime": {
            "module_id": "market_regime_context",
            "grammar_role": "market_regime_context",
            "dataschema": "MarketRegimeContextOutput",
        },
        "options_flow": {
            "module_id": "options_flow_context",
            "grammar_role": "options_flow_context",
            "dataschema": "OptionsFlowContextOutput",
        },
        "posture": {
            "module_id": "posture_risk_permission",
            "grammar_role": "posture_risk_permission",
            "dataschema": "PostureRiskOutput",
        },
        "eligibility": {
            "module_id": "playbook_eligibility",
            "grammar_role": "playbook_eligibility",
            "dataschema": "PlaybookEligibilityOutput",
        },
        "execution": {
            "module_id": "expression_execution",
            "grammar_role": "expression_execution",
            "dataschema": "ExecutionExpressionOutput",
        },
    }

    def stage_sequence(self) -> tuple[str, ...]:
        """Return the governed six-stage serial-runtime order for one deterministic pass."""

        return self.stage_order

    def run_once(
        self,
        stage_inputs: Mapping[str, Any] | StageInputBundle,
        *,
        live_inventory_service: Any | None = None,
        live_inventory_request: Mapping[str, Any] | None = None,
        live_inventory_snapshot: DownstreamLiveInventorySnapshot | Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Return one bounded runtime pass from the admitted stage-input boundary."""

        bundle = _coerce_admitted_bundle(stage_inputs)
        if bundle is None:
            normalised_stage_inputs = _normalise_stage_inputs(stage_inputs)
            executed = [name for name in self.stage_order if name in normalised_stage_inputs]
            receipt = {
                "stage_order": list(self.stage_order),
                "executed_stages": executed,
                "missing_stages": [
                    name for name in self.stage_order if name not in normalised_stage_inputs
                ],
            }
            return _attach_runtime_live_inventory(
                receipt,
                live_inventory_service=live_inventory_service,
                live_inventory_request=live_inventory_request,
                live_inventory_snapshot=live_inventory_snapshot,
            )
        receipt = self._run_serial_bundle(bundle)
        return _attach_runtime_live_inventory(
            receipt,
            live_inventory_service=live_inventory_service,
            live_inventory_request=live_inventory_request,
            live_inventory_snapshot=live_inventory_snapshot,
        )

    def _run_serial_bundle(self, stage_input_bundle: StageInputBundle) -> dict[str, Any]:
        source_time_utc = _require_source_time_utc(stage_input_bundle)
        token = _time_token(source_time_utc)
        traceid = f"trace::serial_runtime::{token}"
        runid = f"run::serial_runtime::{token}"
        scenarioid = "live"
        inputfingerprint = _input_fingerprint(stage_input_bundle)
        packet_emitted_at = datetime.now(UTC)

        temporal = TemporalContextService().evaluate(stage_input_bundle.temporal)
        regime = RegimeContextService().evaluate(stage_input_bundle.regime)
        options_flow = OptionsFlowContextService().evaluate(stage_input_bundle.options_flow)
        posture = PostureService().evaluate(regime=regime)
        eligibility = PlaybookEligibilityService().evaluate(
            posture=posture, candidate_family_ids=[]
        )
        execution_input = ExecutionExpressionInput(
            temporal=temporal.model_dump(mode="json"),
            regime=regime.model_dump(mode="json"),
            options_flow=options_flow.model_dump(mode="json"),
            posture=posture.model_dump(mode="json"),
            eligibility=eligibility.model_dump(mode="json"),
        )
        execution = evaluate_execution_expression(
            execution_input=execution_input,
            eligibility_output=eligibility,
        )

        stage_outputs = {
            "temporal": temporal,
            "regime": regime,
            "options_flow": options_flow,
            "posture": posture,
            "eligibility": eligibility,
            "execution": execution,
        }
        stage_packets = self._build_stage_packets(
            stage_outputs=stage_outputs,
            source_time_utc=source_time_utc,
            packet_emitted_at=packet_emitted_at,
            traceid=traceid,
            runid=runid,
            scenarioid=scenarioid,
            inputfingerprint=inputfingerprint,
        )

        stage_local_handoff = StageLocalHandoffSurface(
            execution_post_modifier_pre_final_risk=execution.model_dump(mode="json"),
            lineage_tags=list(SERIAL_STAGE_LINEAGE_TAGS),
        )

        return {
            "stage_order": list(self.stage_order),
            "executed_stages": list(self.stage_order),
            "missing_stages": [],
            "serial_spine_contract": copy_serial_spine_contract(),
            "stage_dependencies": {
                stage_name: list(self._stage_dependencies[stage_name])
                for stage_name in self.stage_order
            },
            "stage_packet_ids": {
                stage_name: packet.packet_id for stage_name, packet in stage_packets.items()
            },
            "stage_outputs": {
                stage_name: output.model_dump(mode="json")
                for stage_name, output in stage_outputs.items()
            },
            "stage_packets": {
                stage_name: packet.model_dump(mode="json")
                for stage_name, packet in stage_packets.items()
            },
            "stage_local_handoff": stage_local_handoff.model_dump(mode="json"),
        }

    def _build_stage_packets(
        self,
        *,
        stage_outputs: dict[str, Any],
        source_time_utc: datetime,
        packet_emitted_at: datetime,
        traceid: str,
        runid: str,
        scenarioid: str,
        inputfingerprint: str,
    ) -> dict[str, Any]:
        stage_packet_ids = {
            stage_name: f"dmp::serial::{stage_name}::{_time_token(source_time_utc)}"
            for stage_name in self.stage_order
        }
        packets: dict[str, Any] = {}
        previous_packet_id: str | None = None
        for stage_name in self.stage_order:
            metadata = self._stage_packet_metadata[stage_name]
            dependencyids = [
                stage_packet_ids[name] for name in self._stage_dependencies[stage_name]
            ]
            packet = build_stage_packet(
                packet_id=stage_packet_ids[stage_name],
                dataschema=metadata["dataschema"],
                data=stage_outputs[stage_name],
                emitted_at=packet_emitted_at,
                traceid=traceid,
                runid=runid,
                scenarioid=scenarioid,
                module_id=metadata["module_id"],
                module_version="native",
                module_instance_id=f"{metadata['module_id']}::runtime",
                grammar_role=metadata["grammar_role"],
                stage_name=stage_name,
                parentids=[previous_packet_id] if previous_packet_id is not None else [],
                dependencyids=dependencyids,
                derivedfrom=_derived_from(stage_name, self._stage_dependencies[stage_name]),
                sourceartifactids=[],
                inputfingerprint=inputfingerprint,
                summary_headline=_stage_summary(stage_name, stage_outputs[stage_name]),
                dmpextensions={
                    "nvda": {
                        "schema_identifiers": {
                            "output_model_name": metadata["dataschema"],
                        },
                    }
                },
            )
            packets[stage_name] = packet
            previous_packet_id = packet.packet_id
        return packets


def _attach_runtime_live_inventory(
    receipt: dict[str, Any],
    *,
    live_inventory_service: Any | None,
    live_inventory_request: Mapping[str, Any] | None,
    live_inventory_snapshot: DownstreamLiveInventorySnapshot | Mapping[str, Any] | None,
) -> dict[str, Any]:
    if live_inventory_service is not None and live_inventory_snapshot is not None:
        raise ValueError(
            "live_inventory_service and live_inventory_snapshot cannot both be supplied"
        )
    if live_inventory_service is None and live_inventory_snapshot is None:
        if live_inventory_request is not None:
            raise ValueError("live_inventory_request requires live_inventory_service")
        return receipt
    if live_inventory_snapshot is not None:
        snapshot = _coerce_live_inventory_snapshot(live_inventory_snapshot)
    else:
        request = dict(live_inventory_request or {})
        allowed_keys = {"live_ids", "inventory_id", "capital_snapshot_id", "receipt_id"}
        extra_keys = set(request) - allowed_keys
        if extra_keys:
            joined = ", ".join(sorted(extra_keys))
            raise ValueError(f"live_inventory_request contains unsupported keys: {joined}")
        snapshot = live_inventory_service.build_live_snapshot(**request)
    receipt["runtime_live_inventory"] = snapshot.model_dump(mode="json")
    receipt["runtime_live_inventory_policy_effect"] = "read_only_no_serial_decision_change"
    return receipt


def _coerce_live_inventory_snapshot(
    live_inventory_snapshot: DownstreamLiveInventorySnapshot | Mapping[str, Any],
) -> DownstreamLiveInventorySnapshot:
    if isinstance(live_inventory_snapshot, DownstreamLiveInventorySnapshot):
        return live_inventory_snapshot
    return DownstreamLiveInventorySnapshot.model_validate(live_inventory_snapshot)


def _coerce_admitted_bundle(
    stage_inputs: Mapping[str, Any] | StageInputBundle,
) -> StageInputBundle | None:
    if isinstance(stage_inputs, StageInputBundle):
        return stage_inputs
    if isinstance(stage_inputs, Mapping):
        try:
            return StageInputBundle.model_validate(stage_inputs)
        except ValidationError:
            return None
    return None


def _normalise_stage_inputs(
    stage_inputs: Mapping[str, Any] | StageInputBundle,
) -> Mapping[str, Any]:
    if isinstance(stage_inputs, StageInputBundle):
        return stage_inputs.as_mapping()
    return stage_inputs


def _require_source_time_utc(stage_input_bundle: StageInputBundle) -> datetime:
    source_time_utc = stage_input_bundle.temporal.source_time_utc
    if source_time_utc is None:
        raise ValueError("Serial runtime requires temporal.source_time_utc.")
    if source_time_utc.tzinfo is None:
        return source_time_utc
    return source_time_utc.astimezone(UTC)


def _time_token(source_time_utc: datetime) -> str:
    return source_time_utc.isoformat().replace("+00:00", "Z").replace(":", "").replace("-", "")


def _input_fingerprint(stage_input_bundle: StageInputBundle) -> str:
    payload = json.dumps(
        stage_input_bundle.model_dump(mode="json"), sort_keys=True, separators=(",", ":")
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _derived_from(stage_name: str, dependencies: tuple[str, ...]) -> str:
    if not dependencies:
        return f"{stage_name}_from_declared_stage_inputs"
    dependency_label = "+".join(dependencies)
    return f"{stage_name}_from_{dependency_label}"


def _stage_summary(stage_name: str, payload: Any) -> str:
    if stage_name == "temporal":
        return f"session_state={payload.session_state}"
    if stage_name == "regime":
        return f"volatility_regime={payload.volatility_regime}"
    if stage_name == "options_flow":
        return f"term_structure_state={payload.term_structure_state}"
    if stage_name == "posture":
        return f"permission_state={payload.permission_state.value}"
    if stage_name == "eligibility":
        return f"active_families={','.join(payload.active_family_ids) if payload.active_family_ids else 'none'}"
    if stage_name == "execution":
        return f"lead_playbook_id={payload.lead_playbook_id or 'none'}"
    raise ValueError(f"Unknown stage name: {stage_name}")
