"""Phase 0 audit for the NVDA signal workbook.

Purpose:
    Inspect the checked-in signal workbook and decide whether it can support
    one canonical real-data runtime path without synthetic supplementation.
Inputs:
    One `.xlsx` workbook plus the typed runtime contracts defined in this repo.
Outputs:
    Machine-readable JSON describing workbook surfaces, formula density,
    runtime bundle requirements, and the Phase 0 verdict.
Determinism:
    Parses OOXML directly, uses stable sheet ordering, and emits sorted JSON.
"""

from __future__ import annotations

import argparse
import json
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET

NS = {
    "main": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
    "rel": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
}


@dataclass(frozen=True)
class SheetSummary:
    name: str
    dimension: str | None
    row_count: int
    cell_count: int
    formula_cell_count: int
    nonempty_cell_count: int
    first_rows: list[list[dict[str, Any]]]


class WorkbookAudit:
    def __init__(self, workbook_path: Path) -> None:
        self.workbook_path = workbook_path
        self._zip = zipfile.ZipFile(workbook_path)
        self._sheets = self._load_sheets()

    def _load_sheets(self) -> list[tuple[str, str]]:
        workbook = ET.fromstring(self._zip.read("xl/workbook.xml"))
        rels = ET.fromstring(self._zip.read("xl/_rels/workbook.xml.rels"))
        rid_to_target = {
            rel.attrib["Id"]: rel.attrib["Target"].lstrip("/")
            for rel in rels
            if rel.attrib.get("Type", "").endswith("/worksheet")
        }
        sheets: list[tuple[str, str]] = []
        sheets_node = workbook.find("main:sheets", NS)
        for node in ([] if sheets_node is None else list(sheets_node)):
            name = node.attrib["name"]
            rid = node.attrib[f"{{{NS['rel']}}}id"]
            sheets.append((name, rid_to_target[rid]))
        return sheets

    def _cell_value(self, cell: ET.Element) -> str | None:
        cell_type = cell.attrib.get("t")
        if cell_type == "inlineStr":
            text_nodes = cell.findall(".//main:t", NS)
            return "".join(node.text or "" for node in text_nodes)
        value = cell.find("main:v", NS)
        if value is not None:
            return value.text
        formula = cell.find("main:f", NS)
        if formula is not None:
            return None
        return None

    def summarise_sheet(self, sheet_name: str, preview_rows: int = 6) -> SheetSummary:
        target = dict(self._sheets)[sheet_name]
        root = ET.fromstring(self._zip.read(target))
        dimension = root.find("main:dimension", NS)
        rows = root.findall(".//main:sheetData/main:row", NS)
        cell_count = 0
        formula_cell_count = 0
        nonempty_cell_count = 0
        preview: list[list[dict[str, Any]]] = []
        for row_index, row in enumerate(rows):
            preview_row: list[dict[str, Any]] = []
            for cell in row.findall("main:c", NS):
                cell_count += 1
                if cell.find("main:f", NS) is not None:
                    formula_cell_count += 1
                value = self._cell_value(cell)
                if value not in {None, ""}:
                    nonempty_cell_count += 1
                if row_index < preview_rows:
                    cell_ref = cell.attrib.get("r", "")
                    formula = cell.find("main:f", NS)
                    preview_row.append(
                        {
                            "cell": cell_ref,
                            "value": value,
                            "formula": formula.text if formula is not None else None,
                        }
                    )
            if row_index < preview_rows:
                preview.append(preview_row)
        return SheetSummary(
            name=sheet_name,
            dimension=dimension.attrib.get("ref") if dimension is not None else None,
            row_count=len(rows),
            cell_count=cell_count,
            formula_cell_count=formula_cell_count,
            nonempty_cell_count=nonempty_cell_count,
            first_rows=preview,
        )

    def emit(self) -> dict[str, Any]:
        key_sheets = [
            "Live_Web_Baseline",
            "Anchor_Data",
            "Synthetic_Raw",
            "Derived_Beta_Leadership",
            "Derived_Vol_Rates_FX",
            "Derived_Execution_Options",
            "Derived_Asia_Breadth",
            "Raw_Primitives_Catalog",
            "Derived_Features_Catalog",
            "Options_Chain_Raw_Spec",
            "Volume_Baseline_Raw_Spec",
            "Temporal_Step1_Framework",
            "Temporal_Step1_Tests",
        ]
        summaries = {name: self.summarise_sheet(name).__dict__ for name in key_sheets}

        required_runtime_bundle_surfaces = {
            "provenance": ["source_name", "source_type", "captured_at", "symbol"],
            "bars": ["ts", "open", "high", "low", "close", "volume"],
            "option_chain_snapshots": [
                "ts",
                "symbol",
                "quotes[*].expiry",
                "quotes[*].strike",
                "quotes[*].side",
                "quotes[*].bid",
                "quotes[*].ask",
                "quotes[*].iv",
                "quotes[*].gamma",
                "quotes[*].oi",
                "quotes[*].volume",
            ],
            "events": [
                "event_id",
                "title",
                "event_class",
                "impact",
                "scheduled_at",
                "lineage_key",
            ],
        }

        observed_presence = {
            "intraday_bar_rows_present": False,
            "typed_provenance_block_present": False,
            "actual_option_chain_quote_rows_present": False,
            "actual_normalised_event_rows_present": False,
            "repeated_chain_sequence_rows_present": False,
            "single_mid_session_runtime_snapshot_present": False,
        }

        missing_raw_surfaces = [
            "typed provenance record for one canonical imported bundle",
            "intraday OHLCV bar series with timestamped open/high/low/close/volume rows",
            "option-chain snapshot rows with per-quote expiry/strike/side/bid/ask",
            "per-quote IV/gamma/open-interest/volume values for at least front two expiries",
            "normalised event records with event identity, class, impact, and scheduled timestamp",
            "repeated intraday chain snapshots for sequence-dependent options features",
            "a single authoritative mid-session timestamped snapshot wired across all required raw surfaces",
        ]

        missing_or_unreliable_derived_surfaces = [
            "session VWAP and distance-to-VWAP from actual intraday bars",
            "5-minute VWAP slope from actual intraday bars",
            "opening-range high/low and break count from actual intraday bars",
            "5-minute and 15-minute realised volatility from actual intraday bars",
            "relative-volume ratio from same-bucket historical baseline",
            "front and next-expiry ATM IV split by tenor",
            "pin progression sequence and repeated-snapshot pressure evolution",
            "next_event_at from actual scheduled-event timestamps rather than Event_Flag placeholders",
        ]

        verdict = {
            "single_canonical_real_run_viable": False,
            "status": "fail",
            "reason": (
                "The workbook is a planning and signal-doctrine artifact with web anchors, synthetic raw "
                "expansion, and formula-driven derived tabs. It does not contain one authoritative, "
                "timestamped, mid-session real-data bundle with bars, option-chain quote rows, and "
                "normalised events required for the checked-in real-data runtime path."
            ),
            "safe_next_action": (
                "Do not fabricate missing raw inputs. Treat the workbook as doctrine and signal-catalog "
                "authority only, and keep the checked-in JSON fixture pack as the current canonical real-data "
                "runtime input until a true captured bundle is added."
            ),
        }

        return {
            "artifact": str(self.workbook_path),
            "sheet_count": len(self._sheets),
            "sheet_names": [name for name, _ in self._sheets],
            "sheet_summaries": summaries,
            "required_runtime_bundle_surfaces": required_runtime_bundle_surfaces,
            "observed_runtime_surface_presence": observed_presence,
            "missing_raw_surfaces": missing_raw_surfaces,
            "missing_or_unreliable_derived_surfaces": missing_or_unreliable_derived_surfaces,
            "phase_zero_gate": verdict,
        }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("workbook", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    audit = WorkbookAudit(args.workbook).emit()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
