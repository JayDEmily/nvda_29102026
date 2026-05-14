"""Build one bounded Module 8 workbook-derived StageInputBundle specimen."""

from __future__ import annotations

import json
import posixpath
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from hashlib import sha256
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET
from zipfile import ZipFile

from nvda_desk.contracts.options_flow import OptionsFlowContextInput
from nvda_desk.contracts.packets import DeskModulePacketV3
from nvda_desk.contracts.parallel_risk import (
    ParallelRiskObservationAppendReceipt,
    ParallelRiskObservationRecord,
)
from nvda_desk.contracts.regime import MarketRegimeContextInput
from nvda_desk.contracts.stage_inputs import StageInputBundle
from nvda_desk.contracts.temporal import TemporalContextInput, build_source_temporal_payload
from nvda_desk.persistence.parallel_risk_observations import (
    ParallelRiskObservationStore,
    build_parallel_risk_observation_record,
)
from nvda_desk.services.parallel_risk_lane_service import ParallelRiskLaneService

DEFAULT_WORKBOOK_PATH = Path(
    "data/reference/signal_workbooks/2026-03-25_NVDA_SIGNAL_WORKBOOK_v3_bounds_handoff_copy.xlsx"
)
DEFAULT_SPECIMEN_HOME = Path("var/audit/specimens/module_8")
ANCHOR_ROW_REF = "Anchor_Data!A7:AE7"
ANCHOR_DATE_REF = "Anchor_Data!A7"
ANCHOR_SPOT_PRICE_REF = "Anchor_Data!B7"
ANCHOR_NQ_CLOSE_REF = "Anchor_Data!G7"
ANCHOR_VIX_REF = "Anchor_Data!M7"
ANCHOR_EVENT_FLAG_REF = "Anchor_Data!AE7"
LWB_NVDA_SEED_REF = "Live_Web_Baseline!B6:C6"
LWB_VIX_SEED_REF = "Live_Web_Baseline!B9:C9"
LWB_NASDAQ100_SEED_REF = "Live_Web_Baseline!B16:C16"
EXCEL_EPOCH = datetime(1899, 12, 30)
_NS_MAIN = {"s": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
_NS_REL = {"r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships"}
_NS_PKG = {"p": "http://schemas.openxmlformats.org/package/2006/relationships"}

SPECIMEN_TRACE_ID = "trace::module_8_parallel_risk_workbook_specimen"
SPECIMEN_RUN_ID = "run::module_8_parallel_risk_workbook_specimen"
SPECIMEN_SCENARIO_ID = "workbook_specimen"
SPECIMEN_BOOTSTRAP_PACKET_ID = "module-8-parallel-risk-bootstrap-workbook-specimen-20260301"
SPECIMEN_OUTPUT_PACKET_ID = "module-8-parallel-risk-output-workbook-specimen-20260301"
SPECIMEN_OBSERVATION_ID = "module-8-parallel-risk-observation-workbook-specimen-20260301"
SPECIMEN_PACKET_EMITTED_AT = datetime(2026, 4, 22, 0, 0, tzinfo=UTC)
SPECIMEN_OBSERVATION_PERSISTED_AT = datetime(2026, 4, 22, 0, 1, tzinfo=UTC)


@dataclass(frozen=True)
class Module8ParallelRiskWorkbookMapping:
    """Hold the bounded workbook-derived Module 8 specimen mapping."""

    workbook_path: Path
    stage_input_bundle: StageInputBundle
    derivedfrom: str
    sourceartifactids: list[str]
    inputfingerprint: str
    mapping_metadata: dict[str, Any]


@dataclass(frozen=True)
class Module8ParallelRiskWorkbookSpecimen:
    """Hold the full bounded Module 8 workbook-derived specimen artefact set."""

    mapping: Module8ParallelRiskWorkbookMapping
    bootstrap_input_packet: DeskModulePacketV3
    stage_a_output_packet: DeskModulePacketV3
    observation_record: ParallelRiskObservationRecord
    append_receipt: ParallelRiskObservationAppendReceipt


@dataclass(frozen=True)
class Module8ParallelRiskWorkbookSpecimenArtifacts:
    """Record the deterministic artefact paths written for the specimen."""

    home: Path
    stage_input_bundle_json: Path
    bootstrap_input_packet_json: Path
    stage_a_output_packet_json: Path
    append_only_observation_record_json: Path
    specimen_receipt_md: Path


class _XlsxCellReader:
    """Read bounded cell values from one XLSX workbook using only stdlib parsing."""

    def __init__(self, workbook_path: Path):
        self._workbook_path = workbook_path
        self._zip = ZipFile(workbook_path)
        self._shared_strings = self._load_shared_strings()

    def close(self) -> None:
        self._zip.close()

    def _load_shared_strings(self) -> list[str]:
        if "xl/sharedStrings.xml" not in self._zip.namelist():
            return []
        root = ET.fromstring(self._zip.read("xl/sharedStrings.xml"))
        strings: list[str] = []
        for si in root.findall("s:si", _NS_MAIN):
            text = "".join(node.text or "" for node in si.findall(".//s:t", _NS_MAIN))
            strings.append(text)
        return strings

    def _sheet_target(self, sheet_name: str) -> str:
        workbook_root = ET.fromstring(self._zip.read("xl/workbook.xml"))
        rel_id = None
        for sheet in workbook_root.findall("s:sheets/s:sheet", {**_NS_MAIN, **_NS_REL}):
            if sheet.attrib.get("name") == sheet_name:
                rel_id = sheet.attrib.get(
                    "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"
                )
                break
        if rel_id is None:
            raise KeyError(f"Sheet not found: {sheet_name}")
        rel_root = ET.fromstring(self._zip.read("xl/_rels/workbook.xml.rels"))
        for rel in rel_root.findall("p:Relationship", _NS_PKG):
            if rel.attrib.get("Id") == rel_id:
                target = rel.attrib["Target"].lstrip("/")
                if not target.startswith("xl/"):
                    target = posixpath.join("xl", target)
                return posixpath.normpath(target)
        raise KeyError(f"Workbook relationship not found for sheet: {sheet_name}")

    def read_cells(self, sheet_name: str) -> dict[str, Any]:
        root = ET.fromstring(self._zip.read(self._sheet_target(sheet_name)))
        cells: dict[str, Any] = {}
        for cell in root.findall(".//s:c", _NS_MAIN):
            cell_ref = cell.attrib["r"]
            cell_type = cell.attrib.get("t")
            value_node = cell.find("s:v", _NS_MAIN)
            inline_node = cell.find("s:is", _NS_MAIN)
            if cell_type == "s" and value_node is not None and value_node.text is not None:
                cells[cell_ref] = self._shared_strings[int(value_node.text)]
                continue
            if cell_type == "inlineStr" and inline_node is not None:
                cells[cell_ref] = "".join(
                    node.text or "" for node in inline_node.findall(".//s:t", _NS_MAIN)
                )
                continue
            if value_node is None or value_node.text is None:
                cells[cell_ref] = None
                continue
            text = value_node.text
            try:
                number = float(text)
                if number.is_integer():
                    cells[cell_ref] = int(number)
                else:
                    cells[cell_ref] = number
            except ValueError:
                cells[cell_ref] = text
        return cells


def _excel_serial_to_naive_datetime(serial_value: int | float) -> datetime:
    return EXCEL_EPOCH + timedelta(days=float(serial_value))


def _mapping_metadata(
    anchor_cells: dict[str, Any], live_cells: dict[str, Any], workbook_path: Path
) -> dict[str, Any]:
    event_flag = anchor_cells.get("AE7")
    missing_fields = {
        "temporal": ["next_event_time_utc", "windows"],
        "regime": ["nvda_return_pct", "nq_return_pct"],
        "options_flow": ["front_dte", "next_dte"],
    }
    return {
        "classification": "governed-workbook-derived bounded specimen",
        "workbook_path": workbook_path.as_posix(),
        "sheet_refs_used": {
            "anchor_primary": ANCHOR_ROW_REF,
            "anchor_date": ANCHOR_DATE_REF,
            "anchor_spot_price": ANCHOR_SPOT_PRICE_REF,
            "anchor_nq_close": ANCHOR_NQ_CLOSE_REF,
            "anchor_vix": ANCHOR_VIX_REF,
            "anchor_event_flag": ANCHOR_EVENT_FLAG_REF,
            "live_web_nvda_seed": LWB_NVDA_SEED_REF,
            "live_web_vix_seed": LWB_VIX_SEED_REF,
            "live_web_nasdaq100_seed": LWB_NASDAQ100_SEED_REF,
        },
        "anchor_row_ref": ANCHOR_ROW_REF,
        "field_seed_dates": {
            "temporal.source_date": {
                "anchor_ref": ANCHOR_DATE_REF,
                "anchor_row_date": _excel_serial_to_naive_datetime(anchor_cells["A7"])
                .date()
                .isoformat(),
                "seed_source": "anchor_row_date_only",
            },
            "options_flow.spot_price": {
                "anchor_ref": ANCHOR_SPOT_PRICE_REF,
                "seed_ref": LWB_NVDA_SEED_REF,
                "seed_observed_date": str(live_cells["C6"]),
                "seed_metric": str(live_cells["A6"]),
            },
            "regime.vix_level": {
                "anchor_ref": ANCHOR_VIX_REF,
                "seed_ref": LWB_VIX_SEED_REF,
                "seed_observed_date": str(live_cells["C9"]),
                "seed_metric": str(live_cells["A9"]),
            },
            "regime.nq_return_pct": {
                "anchor_ref": ANCHOR_NQ_CLOSE_REF,
                "seed_ref": LWB_NASDAQ100_SEED_REF,
                "seed_observed_date": str(live_cells["C16"]),
                "seed_metric": str(live_cells["A16"]),
                "mapping_state": "missing_explicit_no_lawful_return_basis",
            },
        },
        "mapped_direct_fields": {
            "temporal.source_date": ANCHOR_DATE_REF,
            "regime.vix_level": ANCHOR_VIX_REF,
            "options_flow.spot_price": ANCHOR_SPOT_PRICE_REF,
        },
        "missing_fields": missing_fields,
        "anchor_event_flag": event_flag,
        "event_flag_note": (
            "Anchor_Data!AE7 indicates an event flag, but no lawful next_event_time_utc timestamp or event window can be derived from the workbook surfaces inspected."
            if event_flag
            else "No anchor event flag asserted on the mapped row."
        ),
        "not_direct_live_runtime_authority": True,
        "not_full_raw_runtime_bundle": True,
        "mixed_date_provenance_preserved": True,
    }


def build_module_8_parallel_risk_workbook_mapping(
    workbook_path: str | Path = DEFAULT_WORKBOOK_PATH,
) -> Module8ParallelRiskWorkbookMapping:
    """Build the bounded workbook-derived StageInputBundle mapping for Module 8."""

    resolved_workbook_path = Path(workbook_path)
    reader = _XlsxCellReader(resolved_workbook_path)
    try:
        anchor_cells = reader.read_cells("Anchor_Data")
        live_cells = reader.read_cells("Live_Web_Baseline")
    finally:
        reader.close()

    source_date = _excel_serial_to_naive_datetime(anchor_cells["A7"]).date()
    metadata = _mapping_metadata(anchor_cells, live_cells, resolved_workbook_path)
    bundle = StageInputBundle(
        temporal=TemporalContextInput(
            **build_source_temporal_payload(source_date=source_date),
            next_event_time_utc=None,
            windows=[],
        ),
        regime=MarketRegimeContextInput(
            nvda_return_pct=None,
            nq_return_pct=None,
            vix_level=float(anchor_cells["M7"]),
            missing_fields=list(metadata["missing_fields"]["regime"]),
        ),
        options_flow=OptionsFlowContextInput(
            spot_price=float(anchor_cells["B7"]),
            front_dte=None,
            next_dte=None,
            missing_fields=list(metadata["missing_fields"]["options_flow"]),
        ),
    )
    fingerprint_payload = {
        "workbook_path": resolved_workbook_path.as_posix(),
        "anchor_row_ref": ANCHOR_ROW_REF,
        "anchor_values": {
            "A7": anchor_cells["A7"],
            "B7": anchor_cells["B7"],
            "G7": anchor_cells["G7"],
            "M7": anchor_cells["M7"],
            "AE7": anchor_cells.get("AE7"),
        },
        "field_seed_dates": metadata["field_seed_dates"],
        "missing_fields": metadata["missing_fields"],
    }
    fingerprint = "sha256:" + sha256(repr(fingerprint_payload).encode("utf-8")).hexdigest()
    return Module8ParallelRiskWorkbookMapping(
        workbook_path=resolved_workbook_path,
        stage_input_bundle=bundle,
        derivedfrom=f"reference-ledger::{ANCHOR_ROW_REF}",
        sourceartifactids=[resolved_workbook_path.as_posix()],
        inputfingerprint=fingerprint,
        mapping_metadata=metadata,
    )


def build_module_8_parallel_risk_workbook_specimen(
    workbook_path: str | Path = DEFAULT_WORKBOOK_PATH,
) -> Module8ParallelRiskWorkbookSpecimen:
    """Build the full bounded workbook-derived Module 8 specimen through the native lane path."""

    mapping = build_module_8_parallel_risk_workbook_mapping(workbook_path=workbook_path)
    service = ParallelRiskLaneService()
    specimen_extensions = {
        "nvda": {
            "specimen": {
                "classification": mapping.mapping_metadata["classification"],
                "workbook_path": mapping.workbook_path.as_posix(),
                "anchor_row_ref": mapping.mapping_metadata["anchor_row_ref"],
                "manual_promotion": True,
                "not_live_runtime_authority": True,
            }
        }
    }
    bootstrap_input_packet = service.build_bootstrap_input_packet(
        stage_input_bundle=mapping.stage_input_bundle,
        packet_id=SPECIMEN_BOOTSTRAP_PACKET_ID,
        traceid=SPECIMEN_TRACE_ID,
        runid=SPECIMEN_RUN_ID,
        scenarioid=SPECIMEN_SCENARIO_ID,
        emitted_at=SPECIMEN_PACKET_EMITTED_AT,
        derivedfrom=mapping.derivedfrom,
        sourceartifactids=list(mapping.sourceartifactids),
        inputfingerprint=mapping.inputfingerprint,
        dmpextensions=specimen_extensions,
    )
    stage_a_output_packet = service.evaluate(
        bootstrap_packet=bootstrap_input_packet,
        output_packet_id=SPECIMEN_OUTPUT_PACKET_ID,
    )
    observation_record = build_parallel_risk_observation_record(
        observation_id=SPECIMEN_OBSERVATION_ID,
        input_packet=bootstrap_input_packet,
        output_packet=stage_a_output_packet,
        persisted_at_utc=SPECIMEN_OBSERVATION_PERSISTED_AT,
    )
    store = ParallelRiskObservationStore()
    append_receipt = store.append_observation(observation_record)
    return Module8ParallelRiskWorkbookSpecimen(
        mapping=mapping,
        bootstrap_input_packet=bootstrap_input_packet,
        stage_a_output_packet=stage_a_output_packet,
        observation_record=observation_record,
        append_receipt=append_receipt,
    )


def write_module_8_parallel_risk_workbook_specimen_artifacts(
    specimen: Module8ParallelRiskWorkbookSpecimen | None = None,
    output_dir: str | Path = DEFAULT_SPECIMEN_HOME,
) -> Module8ParallelRiskWorkbookSpecimenArtifacts:
    """Write the bounded Module 8 workbook-derived specimen artefacts."""

    resolved_output_dir = Path(output_dir)
    resolved_output_dir.mkdir(parents=True, exist_ok=True)
    resolved_specimen = specimen or build_module_8_parallel_risk_workbook_specimen()

    artefact_paths = Module8ParallelRiskWorkbookSpecimenArtifacts(
        home=resolved_output_dir,
        stage_input_bundle_json=resolved_output_dir / "stage_input_bundle.json",
        bootstrap_input_packet_json=resolved_output_dir / "bootstrap_input_packet.json",
        stage_a_output_packet_json=resolved_output_dir / "stage_a_output_packet.json",
        append_only_observation_record_json=resolved_output_dir
        / "append_only_observation_record.json",
        specimen_receipt_md=resolved_output_dir / "specimen_receipt.md",
    )

    _write_json(
        artefact_paths.stage_input_bundle_json,
        resolved_specimen.mapping.stage_input_bundle.model_dump(mode="json"),
    )
    _write_json(
        artefact_paths.bootstrap_input_packet_json,
        resolved_specimen.bootstrap_input_packet.model_dump(mode="json"),
    )
    _write_json(
        artefact_paths.stage_a_output_packet_json,
        resolved_specimen.stage_a_output_packet.model_dump(mode="json"),
    )
    _write_json(
        artefact_paths.append_only_observation_record_json,
        resolved_specimen.observation_record.model_dump(mode="json"),
    )
    artefact_paths.specimen_receipt_md.write_text(
        _build_specimen_receipt(
            specimen=resolved_specimen,
            artefact_paths=artefact_paths,
        ),
        encoding="utf-8",
    )
    return artefact_paths


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _build_specimen_receipt(
    *,
    specimen: Module8ParallelRiskWorkbookSpecimen,
    artefact_paths: Module8ParallelRiskWorkbookSpecimenArtifacts,
) -> str:
    mapping = specimen.mapping
    mapped_direct = mapping.mapping_metadata["mapped_direct_fields"]
    seed_dates = mapping.mapping_metadata["field_seed_dates"]
    return f"""# Module 8 workbook-derived specimen receipt

## Classification

This is a governed workbook-derived specimen. It is not a live admitted raw bundle and not direct runtime authority.

## Workbook source

- workbook path: `{mapping.workbook_path.as_posix()}`
- primary row surface: `{mapping.mapping_metadata["anchor_row_ref"]}`
- exact sheet names used: `Anchor_Data`, `Live_Web_Baseline`

## Exact cells / rows used

- `Anchor_Data!A7:AE7`
- `Anchor_Data!A7`
- `Anchor_Data!B7`
- `Anchor_Data!G7`
- `Anchor_Data!M7`
- `Anchor_Data!AE7`
- `Live_Web_Baseline!B6:C6`
- `Live_Web_Baseline!B9:C9`
- `Live_Web_Baseline!B16:C16`

## Fields mapped directly

- `temporal.source_date` <- `{mapped_direct["temporal.source_date"]}` with anchor-row date only and `field-level provenance` preserved via `{seed_dates["temporal.source_date"]["anchor_ref"]}`
- `regime.vix_level` <- `{mapped_direct["regime.vix_level"]}` with `field-level provenance` `{seed_dates["regime.vix_level"]["seed_ref"]}`
- `options_flow.spot_price` <- `{mapped_direct["options_flow.spot_price"]}` with `field-level provenance` `{seed_dates["options_flow.spot_price"]["seed_ref"]}`

## Fields left missing explicitly

- `temporal.source_time_raw` = `null`
- `temporal.next_event_time_utc` = `null`
- `temporal.windows` = `[]`
- `regime.nvda_return_pct` = `null`
- `regime.nq_return_pct` = `null`
- `options_flow.front_dte` = `null`
- `options_flow.next_dte` = `null`

No exact raw workbook time token was preserved on the workbook promotion path inspected here, so `temporal.source_time_raw` remains `null` rather than being fabricated from `source_date`.

The workbook event flag at `Anchor_Data!AE7` was not promoted into `next_event_time_utc` or event windows because no lawful timestamped event record is present on the inspected workbook surfaces.

## Provenance rule preserved

- `Anchor_Data` row 7 is the primary mapping surface.
- `Anchor_Data!A7` is used as the anchor-row date only.
- `Live_Web_Baseline` field dates remain field-level provenance.
- Mixed-date workbook fields were not collapsed into one fake live observation timestamp.
- Packet emission time and persistence time were kept separate from workbook source-date provenance.

## Deterministic artefacts written

- stage input bundle JSON: `{artefact_paths.stage_input_bundle_json.as_posix()}`
- bootstrap input DMPV3 packet JSON: `{artefact_paths.bootstrap_input_packet_json.as_posix()}`
- Stage A output DMPV3 packet JSON: `{artefact_paths.stage_a_output_packet_json.as_posix()}`
- append-only observation record JSON: `{artefact_paths.append_only_observation_record_json.as_posix()}`
"""
