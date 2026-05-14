"""Build the admitted serial-runtime-to-parallel-risk boundary specimen."""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from nvda_desk.contracts.options_flow import OptionsFlowContextInput
from nvda_desk.contracts.parallel_risk import (
    ParallelRiskObservationAppendReceipt,
    ParallelRiskObservationRecord,
)
from nvda_desk.contracts.regime import MarketRegimeContextInput
from nvda_desk.contracts.stage_inputs import StageInputBundle
from nvda_desk.contracts.temporal import TemporalContextInput
from nvda_desk.persistence.parallel_risk_observations import (
    ParallelRiskObservationStore,
    build_parallel_risk_observation_record,
)
from nvda_desk.runtime.orchestrator import DeskRuntimeOrchestrator
from nvda_desk.services.parallel_risk_lane_service import ParallelRiskLaneService

DEFAULT_BOUNDARY_SPECIMEN_HOME = Path("var/audit/specimens/serial_runtime_parallel_risk_boundary")
SPECIMEN_SOURCE_TIME_UTC = datetime(2026, 4, 21, 9, 31, tzinfo=UTC)
SPECIMEN_PERSISTED_AT_UTC = datetime(2026, 4, 21, 9, 32, tzinfo=UTC)
SPECIMEN_OBSERVATION_ID = "observation::serial_runtime_parallel_risk_boundary::20260421T093100Z"


@dataclass(frozen=True)
class SerialRuntimeParallelRiskBoundarySpecimenArtifacts:
    """Describe the exact artefacts written by the boundary specimen harness."""

    home: Path
    serial_runtime_receipt_json: Path
    selected_stage_packets_json: Path
    bootstrap_input_packet_json: Path
    parallel_risk_lane_output_packet_json: Path
    parallel_risk_observation_record_json: Path
    specimen_receipt_md: Path


@dataclass(frozen=True)
class SerialRuntimeParallelRiskBoundarySpecimen:
    """Hold the deterministic specimen assembled for the admitted boundary path."""

    serial_runtime_receipt: dict[str, Any]
    selected_stage_packets: dict[str, Any]
    bootstrap_input_packet: Any
    lane_packet: Any
    observation_record: ParallelRiskObservationRecord
    append_receipt: ParallelRiskObservationAppendReceipt


def build_serial_runtime_parallel_risk_boundary_specimen() -> (
    SerialRuntimeParallelRiskBoundarySpecimen
):
    """Build the deterministic specimen for the admitted boundary path."""

    serial_runtime_receipt = DeskRuntimeOrchestrator().run_once(_specimen_stage_input_bundle())
    service_result = ParallelRiskLaneService().run_from_serial_runtime(
        receipt=serial_runtime_receipt
    )
    bootstrap_input_packet = service_result["bootstrap_input_packet"]
    lane_packet = service_result["lane_packet"]
    observation_record = build_parallel_risk_observation_record(
        observation_id=SPECIMEN_OBSERVATION_ID,
        input_packet=bootstrap_input_packet,
        output_packet=lane_packet,
        persisted_at_utc=SPECIMEN_PERSISTED_AT_UTC,
    )
    store = ParallelRiskObservationStore()
    append_receipt = store.append_observation(observation_record)
    return SerialRuntimeParallelRiskBoundarySpecimen(
        serial_runtime_receipt=serial_runtime_receipt,
        selected_stage_packets=service_result["selected_stage_packets"],
        bootstrap_input_packet=bootstrap_input_packet,
        lane_packet=lane_packet,
        observation_record=observation_record,
        append_receipt=append_receipt,
    )


def write_serial_runtime_parallel_risk_boundary_artifacts(
    *,
    specimen: SerialRuntimeParallelRiskBoundarySpecimen | None = None,
    output_dir: str | Path = DEFAULT_BOUNDARY_SPECIMEN_HOME,
) -> SerialRuntimeParallelRiskBoundarySpecimenArtifacts:
    """Write the exact artefacts for the admitted boundary specimen."""

    resolved_output_dir = Path(output_dir)
    resolved_output_dir.mkdir(parents=True, exist_ok=True)
    resolved_specimen = specimen or build_serial_runtime_parallel_risk_boundary_specimen()

    artefact_paths = SerialRuntimeParallelRiskBoundarySpecimenArtifacts(
        home=resolved_output_dir,
        serial_runtime_receipt_json=resolved_output_dir / "serial_runtime_receipt.json",
        selected_stage_packets_json=resolved_output_dir / "selected_stage_packets.json",
        bootstrap_input_packet_json=resolved_output_dir / "bootstrap_input_packet.json",
        parallel_risk_lane_output_packet_json=resolved_output_dir
        / "parallel_risk_lane_output_packet.json",
        parallel_risk_observation_record_json=resolved_output_dir
        / "parallel_risk_observation_record.json",
        specimen_receipt_md=resolved_output_dir / "specimen_receipt.md",
    )

    _write_json(
        artefact_paths.serial_runtime_receipt_json, resolved_specimen.serial_runtime_receipt
    )
    _write_json(
        artefact_paths.selected_stage_packets_json,
        {
            stage_name: packet.model_dump(mode="json")
            for stage_name, packet in resolved_specimen.selected_stage_packets.items()
        },
    )
    _write_json(
        artefact_paths.bootstrap_input_packet_json,
        resolved_specimen.bootstrap_input_packet.model_dump(mode="json"),
    )
    _write_json(
        artefact_paths.parallel_risk_lane_output_packet_json,
        resolved_specimen.lane_packet.model_dump(mode="json"),
    )
    _write_json(
        artefact_paths.parallel_risk_observation_record_json,
        resolved_specimen.observation_record.model_dump(mode="json"),
    )
    artefact_paths.specimen_receipt_md.write_text(
        _build_specimen_receipt(specimen=resolved_specimen, artefact_paths=artefact_paths),
        encoding="utf-8",
    )
    return artefact_paths


def _specimen_stage_input_bundle() -> StageInputBundle:
    return StageInputBundle(
        temporal=TemporalContextInput(source_time_utc=SPECIMEN_SOURCE_TIME_UTC),
        regime=MarketRegimeContextInput(
            nvda_return_pct=0.1,
            nq_return_pct=0.05,
            vix_level=20.0,
        ),
        options_flow=OptionsFlowContextInput(
            spot_price=101.0,
            front_dte=1,
            next_dte=5,
        ),
    )


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _build_specimen_receipt(
    *,
    specimen: SerialRuntimeParallelRiskBoundarySpecimen,
    artefact_paths: SerialRuntimeParallelRiskBoundarySpecimenArtifacts,
) -> str:
    selected_temporal_packet = specimen.selected_stage_packets["temporal"]
    return f"""# serial-runtime-to-parallel-risk boundary specimen receipt

## boundary classification

This specimen proves the admitted serial runtime boundary packet set only.

## admitted path

- serial runtime boundary packet set: `receipt[\"stage_packets\"]`
- selected temporal stage packet: `{selected_temporal_packet.packet_id}`
- bootstrap input packet: `{specimen.bootstrap_input_packet.packet_id}`
- parallel risk lane packet: `{specimen.lane_packet.packet_id}`

## packet-id derivation

- selected temporal stage packet id seed: `{selected_temporal_packet.packet_id}`
- bootstrap input packet id: `{specimen.bootstrap_input_packet.packet_id}`
- parallel risk lane packet id: `{specimen.lane_packet.packet_id}`

## deterministic artefacts written

- serial runtime receipt JSON: `{artefact_paths.serial_runtime_receipt_json.as_posix()}`
- selected stage packets JSON: `{artefact_paths.selected_stage_packets_json.as_posix()}`
- bootstrap input packet JSON: `{artefact_paths.bootstrap_input_packet_json.as_posix()}`
- parallel risk lane packet JSON: `{artefact_paths.parallel_risk_lane_output_packet_json.as_posix()}`
- parallel risk observation record JSON: `{artefact_paths.parallel_risk_observation_record_json.as_posix()}`
- specimen receipt Markdown: `{artefact_paths.specimen_receipt_md.as_posix()}`

## bounded proof notes

- selected stage packets contains exactly `temporal`
- bootstrap input packet lineage depends only on the selected temporal stage packet
- parallel risk lane packet lineage depends only on the bootstrap input packet
- only the selected temporal stage packet is admitted for live Module 8 semantic read in this tranche
"""
