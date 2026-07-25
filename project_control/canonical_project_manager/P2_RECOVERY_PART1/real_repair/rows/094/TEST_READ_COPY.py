from __future__ import annotations

import json

from nvda_desk.testing.harnesses import (
    SerialRuntimeParallelRiskBoundarySpecimen,
    build_serial_runtime_parallel_risk_boundary_specimen,
    write_serial_runtime_parallel_risk_boundary_artifacts,
)

FORBIDDEN_SEAM_NAMES = (
    "preparation_input_packet",
    "preparation packet",
    "preparation packet id",
)


def test_serial_runtime_parallel_risk_boundary_specimen_emits_admitted_boundary_path() -> None:
    specimen = build_serial_runtime_parallel_risk_boundary_specimen()

    assert isinstance(specimen, SerialRuntimeParallelRiskBoundarySpecimen)
    assert tuple(specimen.serial_runtime_receipt["stage_packets"].keys()) == (
        "temporal",
        "regime",
        "options_flow",
        "posture",
        "eligibility",
        "execution",
    )
    assert set(specimen.selected_stage_packets) == {"temporal"}
    assert specimen.bootstrap_input_packet.lineage.parentids == [
        specimen.selected_stage_packets["temporal"].packet_id
    ]
    assert specimen.bootstrap_input_packet.lineage.dependencyids == [
        specimen.selected_stage_packets["temporal"].packet_id
    ]
    assert (
        specimen.bootstrap_input_packet.data.bootstrap_source
        == "serial_runtime.stage_packets.temporal"
    )
    assert specimen.lane_packet.lineage.parentids == [specimen.bootstrap_input_packet.packet_id]
    assert specimen.lane_packet.lineage.dependencyids == [specimen.bootstrap_input_packet.packet_id]


def test_serial_runtime_parallel_risk_boundary_specimen_artifacts_are_written_under_bounded_home(
    tmp_path,
) -> None:
    artefacts = write_serial_runtime_parallel_risk_boundary_artifacts(output_dir=tmp_path)

    assert artefacts.serial_runtime_receipt_json.exists()
    assert artefacts.selected_stage_packets_json.exists()
    assert artefacts.bootstrap_input_packet_json.exists()
    assert artefacts.parallel_risk_lane_output_packet_json.exists()
    assert artefacts.parallel_risk_observation_record_json.exists()
    assert artefacts.specimen_receipt_md.exists()

    receipt_payload = json.loads(artefacts.serial_runtime_receipt_json.read_text(encoding="utf-8"))
    selected_payload = json.loads(artefacts.selected_stage_packets_json.read_text(encoding="utf-8"))
    bootstrap_payload = json.loads(
        artefacts.bootstrap_input_packet_json.read_text(encoding="utf-8")
    )
    lane_payload = json.loads(
        artefacts.parallel_risk_lane_output_packet_json.read_text(encoding="utf-8")
    )
    specimen_receipt = artefacts.specimen_receipt_md.read_text(encoding="utf-8").lower()

    assert receipt_payload["stage_order"] == [
        "temporal",
        "regime",
        "options_flow",
        "posture",
        "eligibility",
        "execution",
    ]
    assert set(receipt_payload["stage_packets"]) == {
        "temporal",
        "regime",
        "options_flow",
        "posture",
        "eligibility",
        "execution",
    }
    assert set(selected_payload) == {"temporal"}
    assert bootstrap_payload["lineage"]["parentids"] == [selected_payload["temporal"]["id"]]
    assert bootstrap_payload["lineage"]["dependencyids"] == [selected_payload["temporal"]["id"]]
    assert bootstrap_payload["data"]["bootstrap_source"] == "serial_runtime.stage_packets.temporal"
    assert lane_payload["lineage"]["parentids"] == [bootstrap_payload["id"]]
    assert lane_payload["lineage"]["dependencyids"] == [bootstrap_payload["id"]]
    assert "module_8_parallel_risk_workbook" not in artefacts.home.as_posix().lower()
    assert "module_8_parallel_risk_workbook" not in specimen_receipt
    for forbidden_name in FORBIDDEN_SEAM_NAMES:
        assert forbidden_name not in specimen_receipt
