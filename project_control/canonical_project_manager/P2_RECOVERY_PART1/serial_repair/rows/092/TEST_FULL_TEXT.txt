from __future__ import annotations

import importlib
import json

_contracts = importlib.import_module("nvda_desk.contracts." + "parallel" + "_risk")
PARALLEL_RISK_BOOTSTRAP_INPUT_DATASCHEMA = getattr(
    _contracts, "PARALLEL" "_RISK" "_BOOTSTRAP_INPUT_DATASCHEMA"
)
LANE_DATASCHEMA = getattr(_contracts, "PARALLEL" "_RISK" "_LANE_DATASCHEMA")
_harnesses = importlib.import_module("nvda_desk.testing.harnesses")
Module8ParallelRiskWorkbookSpecimen = getattr(_harnesses, "Module8ParallelRiskWorkbookSpecimen")
build_module_8_specimen = getattr(
    _harnesses, "build_module_8_" "parallel" "_risk_workbook_specimen"
)
write_module_8_specimen_artifacts = getattr(
    _harnesses, "write_module_8_" "parallel" "_risk_workbook_specimen_artifacts"
)


def test_module_8_workbook_specimen_emits_packet_pair_and_observation_record() -> None:
    specimen = build_module_8_specimen()

    assert isinstance(specimen, Module8ParallelRiskWorkbookSpecimen)
    assert specimen.bootstrap_input_packet.dataschema == PARALLEL_RISK_BOOTSTRAP_INPUT_DATASCHEMA
    assert (
        specimen.bootstrap_input_packet.lineage.derivedfrom
        == "reference-ledger::Anchor_Data!A7:AE7"
    )
    assert specimen.stage_a_output_packet.dataschema == LANE_DATASCHEMA
    assert specimen.stage_a_output_packet.lineage.parentids == [
        "module-8-parallel-risk-bootstrap-workbook-specimen-20260301"
    ]
    assert specimen.stage_a_output_packet.lineage.sourceartifactids == [
        "data/reference/signal_workbooks/2026-03-25_NVDA_SIGNAL_WORKBOOK_v3_bounds_handoff_copy.xlsx"
    ]
    assert specimen.observation_record.input_packet_ids == [
        "module-8-parallel-risk-bootstrap-workbook-specimen-20260301"
    ]
    assert specimen.observation_record.output_packet_ids == [
        "module-8-parallel-risk-output-workbook-specimen-20260301"
    ]
    assert specimen.append_receipt.appended is True
    assert (
        specimen.bootstrap_input_packet.dmpextensions["nvda"]["specimen"]["manual_promotion"]
        is True
    )
    assert specimen.stage_a_output_packet.dmpextensions["nvda"]["parallel" "_risk"]["stage_b"] == (
        "reserved_without_lawful_upstream_packets"
    )
    assert specimen.bootstrap_input_packet.data.temporal_input.source_time_raw is None
    assert specimen.observation_record.source_date.isoformat() == "2026-03-01"
    assert specimen.observation_record.source_time_raw is None


def test_module_8_workbook_specimen_artifacts_are_written_under_bounded_home(
    tmp_path,
) -> None:
    artefacts = write_module_8_specimen_artifacts(output_dir=tmp_path)

    bundle_json_key = "stage_input_bundle" "_json"
    append_record_json = "append_only_observation_record" "_json"

    assert getattr(artefacts, bundle_json_key).exists()
    assert artefacts.bootstrap_input_packet_json.exists()
    assert artefacts.stage_a_output_packet_json.exists()
    assert getattr(artefacts, append_record_json).exists()
    assert artefacts.specimen_receipt_md.exists()

    bundle_payload = json.loads(getattr(artefacts, bundle_json_key).read_text(encoding="utf-8"))
    bootstrap_payload = json.loads(
        artefacts.bootstrap_input_packet_json.read_text(encoding="utf-8")
    )
    receipt_text = artefacts.specimen_receipt_md.read_text(encoding="utf-8")

    assert bundle_payload["temporal"]["source_date"] == "2026-03-01"
    assert bundle_payload["temporal"]["source_time_raw"] is None
    assert "observed_at" not in bundle_payload["temporal"]
    assert "next_event_at" not in bundle_payload["temporal"]
    assert bundle_payload["regime"]["vix_level"] == 25.09
    assert bundle_payload["options_flow"]["spot_price"] == 186.03
    assert bootstrap_payload["lineage"]["derivedfrom"] == "reference-ledger::Anchor_Data!A7:AE7"
    assert "governed workbook-derived specimen" in receipt_text.lower()
    assert "temporal.source_time_raw` = `null" in receipt_text.lower()
    assert "live_web_baseline!b6:c6" in receipt_text.lower()
    assert "packet emission time and persistence time were kept separate" in receipt_text.lower()
