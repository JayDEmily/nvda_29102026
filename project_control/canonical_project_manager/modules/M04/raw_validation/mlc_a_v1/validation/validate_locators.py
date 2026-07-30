#!/usr/bin/env python3
"""Mechanical exact-locator and coverage validation for Lane 2AW R2.

This script checks literal coverage and exact execution only. Human semantic
inspection remains recorded in LOCATOR_VALIDATION.tsv.
"""

from __future__ import annotations

import csv
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path


RECORD = Path(
    "project_control/canonical_project_manager/modules/M04/"
    "M04_AUTHORITY_WORKER_RECORD_V1.md"
)
EVIDENCE_ROOT = Path(
    "project_control/canonical_project_manager/modules/M04/"
    "raw_validation/mlc_a_v1"
)
LOCATOR_TABLE = EVIDENCE_ROOT / "LOCATOR_VALIDATION.tsv"
WORKBOOK_OUTPUT = EVIDENCE_ROOT / "validation/WORKBOOK_LOCATOR_OUTPUT.jsonl"
JSON_PATH = Path(
    "project_control/canonical_project_manager/architecture/"
    "Atlas_Architecture_Machine_Readable.json"
)

SHORTHAND_PATHS = {
    "GATE_C2_PROOF_ENVELOPE_REGISTER.tsv": (
        "project_control/normative_authority_top_down_alignment/"
        "GATE_C2_PROOF_ENVELOPE_REGISTER.tsv"
    ),
    "GATE_C2_BLOCKED_OR_RETURNED_UNITS.tsv": (
        "project_control/normative_authority_top_down_alignment/"
        "GATE_C2_BLOCKED_OR_RETURNED_UNITS.tsv"
    ),
    "gate_c2_proof_envelopes/D-010.md": (
        "project_control/normative_authority_top_down_alignment/"
        "gate_c2_proof_envelopes/D-010.md"
    ),
    "gate_c2_proof_envelopes/D-016.md": (
        "project_control/normative_authority_top_down_alignment/"
        "gate_c2_proof_envelopes/D-016.md"
    ),
    "N-03...md": (
        "project_control/normative_authority_top_down_alignment/"
        "normative_completion_decisions/N-03_PREPARED_DATA_COMMON_ENVELOPE.md"
    ),
    "N-05...md": (
        "project_control/normative_authority_top_down_alignment/"
        "normative_completion_decisions/"
        "N-05_COMMON_METADATA_AND_STAGE_SPECIFIC_CARRIERS.md"
    ),
    "N-09...md": (
        "project_control/normative_authority_top_down_alignment/"
        "normative_completion_decisions/N-09_AUTHORITATIVE_REPLAY.md"
    ),
    "B02_TEST_DESIGN.md": (
        "project_control/normative_authority_top_down_alignment/"
        "gate_c_test_design/B02_TEST_DESIGN.md"
    ),
    "B04_TEST_DESIGN.md": (
        "project_control/normative_authority_top_down_alignment/"
        "gate_c_test_design/B04_TEST_DESIGN.md"
    ),
    "D-010.md": (
        "project_control/normative_authority_top_down_alignment/"
        "gate_c2_proof_envelopes/D-010.md"
    ),
    "D-016.md": (
        "project_control/normative_authority_top_down_alignment/"
        "gate_c2_proof_envelopes/D-016.md"
    ),
}

WORKBOOK_LOCATORS = {
    "Surface Map!A7:O7",
    "Target Modules!A6:Q6",
    "Target Modules!E6",
    "Contracts!A8:E8",
}
JSON_SELECTOR_PREFIXES = (".surfaces[", ".modules[", ".contracts[")


def is_locator(value: str) -> bool:
    return (
        ".md:" in value
        or ".tsv:" in value
        or value in WORKBOOK_LOCATORS
        or value.startswith(JSON_SELECTOR_PREFIXES)
    )


def record_locators() -> list[tuple[int, str]]:
    found: list[tuple[int, str]] = []
    for line_number, line in enumerate(RECORD.read_text(encoding="utf-8").splitlines(), 1):
        for value in re.findall(r"`([^`]+)`", line):
            if is_locator(value):
                found.append((line_number, value))
    return found


def table_locators() -> list[tuple[int, str]]:
    with LOCATOR_TABLE.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    required_columns = {
        "record_line",
        "literal_locator",
        "resolved_target",
        "exact_command",
        "inspected_value",
        "exit_status",
        "semantic_inspection",
        "result",
    }
    missing_columns = required_columns.difference(rows[0] if rows else {})
    if missing_columns:
        raise ValueError(f"missing_locator_table_columns={sorted(missing_columns)}")
    for index, row in enumerate(rows, 2):
        if row["exit_status"] != "0":
            raise ValueError(f"nonzero_locator_exit_status=row:{index}")
        if row["result"] != "PASS":
            raise ValueError(f"nonpass_locator_result=row:{index}")
        if not row["exact_command"] or not row["inspected_value"] or not row["semantic_inspection"]:
            raise ValueError(f"incomplete_locator_evidence=row:{index}")
    return [(int(row["record_line"]), row["literal_locator"]) for row in rows]


def selected_line_numbers(specification: str) -> list[int]:
    selected: list[int] = []
    for part in specification.split(","):
        if "-" in part:
            start_text, end_text = part.split("-", 1)
            selected.extend(range(int(start_text), int(end_text) + 1))
        else:
            selected.append(int(part))
    return selected


def sed_expression(specification: str) -> str:
    commands: list[str] = []
    for part in specification.split(","):
        if "-" in part:
            start_text, end_text = part.split("-", 1)
            commands.append(f"{start_text},{end_text}p")
        else:
            commands.append(f"{part}p")
    return ";".join(commands)


def resolve_text_locator(literal: str) -> tuple[Path, str]:
    path_text, line_specification = literal.rsplit(":", 1)
    resolved = Path(SHORTHAND_PATHS.get(path_text, path_text))
    return resolved, line_specification


def load_workbook_output() -> dict[str, dict[str, object]]:
    output: dict[str, dict[str, object]] = {}
    for line in WORKBOOK_OUTPUT.read_text(encoding="utf-8").splitlines():
        item = json.loads(line)
        output[str(item["locator"])] = item
    return output


def main() -> int:
    record_items = record_locators()
    table_items = table_locators()
    record_counter = Counter(record_items)
    table_counter = Counter(table_items)
    missing = list((record_counter - table_counter).elements())
    extra = list((table_counter - record_counter).elements())
    print(f"record_locator_occurrences={len(record_items)}")
    print(f"validation_rows={len(table_items)}")
    print(f"missing_coverage={missing}")
    print(f"substitute_or_extra_coverage={extra}")
    if missing or extra:
        return 1

    workbook_output = load_workbook_output()
    failures = 0
    for record_line, literal in record_items:
        print(f"\nrecord_line={record_line}")
        print(f"literal_locator={literal}")
        if literal in WORKBOOK_LOCATORS:
            item = workbook_output.get(literal)
            if item is None:
                print("workbook_locator_missing=true")
                failures += 1
                continue
            print(f"workbook_values={json.dumps(item['values'], ensure_ascii=False)}")
            print(f"workbook_formulas={json.dumps(item['formulas'], ensure_ascii=False)}")
            print("exit_status=0")
            continue
        if literal.startswith(JSON_SELECTOR_PREFIXES):
            process = subprocess.run(
                ["jq", "-e", literal, str(JSON_PATH)],
                text=True,
                capture_output=True,
                check=False,
            )
            print(f"json_command=jq -e {literal!r} {str(JSON_PATH)!r}")
            print(f"json_output={process.stdout.rstrip()}")
            print(f"json_stderr={process.stderr.rstrip()}")
            print(f"exit_status={process.returncode}")
            if process.returncode != 0:
                failures += 1
            continue
        path, line_specification = resolve_text_locator(literal)
        lines = path.read_text(encoding="utf-8").splitlines()
        print(f"resolved_target={path}")
        print(f"line_specification={line_specification}")
        print(
            "text_command="
            f"nl -ba {str(path)!r} | sed -n {sed_expression(line_specification)!r}"
        )
        for line_number in selected_line_numbers(line_specification):
            if line_number < 1 or line_number > len(lines):
                print(f"missing_line={line_number}")
                failures += 1
                continue
            print(f"{line_number}:{lines[line_number - 1]}")
        print("exit_status=0")

    print(f"\nlocator_validation_failures={failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
