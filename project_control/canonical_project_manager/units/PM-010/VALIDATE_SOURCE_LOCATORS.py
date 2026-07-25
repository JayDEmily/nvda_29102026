from __future__ import annotations

import csv
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
UNIT_ROOT = ROOT / "project_control/canonical_project_manager/units"
INDEX_PATH = UNIT_ROOT / "PM-010/SOURCE_REVISION_INDEX.tsv"
LOCATOR = re.compile(r"^(?P<path>.+?):(?P<start>\d+)(?:-(?P<end>\d+))?$")
REGISTERS = [
    UNIT_ROOT / "PM-003/ARCHITECTURE_MIGRATION_CONTROL_ADJUDICATION_REGISTER.tsv",
    UNIT_ROOT / "PM-004/COEFFICIENT_MODIFIER_EVALUATION_ADJUDICATION_REGISTER.tsv",
    UNIT_ROOT / "PM-005/CALENDAR_TEMPORAL_PROVENANCE_ADJUDICATION_REGISTER.tsv",
    UNIT_ROOT / "PM-006/DMP_PROTOCOL_IDENTITY_LINEAGE_ADJUDICATION_REGISTER.tsv",
    UNIT_ROOT / "PM-007/STAGE_INGRESS_SERIAL_CAPITAL_ADJUDICATION_REGISTER.tsv",
    UNIT_ROOT / "PM-008/OPENING_POSITION_EXIT_CLOSE_ADJUDICATION_REGISTER.tsv",
    UNIT_ROOT / "PM-009/PARALLEL_RISK_REVIEW_PLAYBOOK_ADJUDICATION_REGISTER.tsv",
]
OCCURRENCE_REGISTERS = [
    *sorted(UNIT_ROOT.glob("PM-00[3-9]/NORMATIVE_CANDIDATE_RE_ADJUDICATION_REGISTER.tsv")),
    UNIT_ROOT / "PM-010/P1_CANDIDATE_SEMANTIC_DISPOSITION_REGISTER.tsv",
]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def index() -> dict[tuple[str, str], Path]:
    result: dict[tuple[str, str], Path] = {}
    with INDEX_PATH.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            result[(row["declared_revision"], row["original_path"])] = ROOT / row["evidence_copy"]
    return result


def resolve_revision(original: str, declared: str, evidence: dict[tuple[str, str], Path]) -> Path:
    kind, expected = declared.split(":", 1)
    if kind == "worktree_sha256":
        path = ROOT / original
    elif kind == "snapshot_sha256":
        path = evidence.get((declared, original))
        if path is None:
            raise AssertionError(f"missing revision evidence: {declared} {original}")
    else:
        raise AssertionError(f"unsupported revision declaration: {declared}")
    if not path.is_file():
        raise AssertionError(f"source revision file missing: {path}")
    actual = digest(path)
    if actual != expected:
        raise AssertionError(
            f"source revision hash mismatch: {original} declared={expected} actual={actual} evidence={path}"
        )
    return path


def validate_adjudication_registers(evidence: dict[tuple[str, str], Path]) -> int:
    count = 0
    for register in REGISTERS:
        with register.open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle, delimiter="\t"))
        for row in rows:
            revisions = json.loads(row["source_revision"])
            if not isinstance(revisions, dict):
                raise AssertionError(f"source_revision is not an object: {register} {row['concept_id']}")
            locators = [item.strip() for item in row["source_locator"].split(";") if item.strip()]
            if not locators:
                raise AssertionError(f"empty source locator: {register} {row['concept_id']}")
            for locator in locators:
                match = LOCATOR.fullmatch(locator)
                if not match:
                    raise AssertionError(f"invalid locator syntax: {register} {row['concept_id']} {locator!r}")
                original = match.group("path")
                start = int(match.group("start"))
                end = int(match.group("end") or start)
                if start < 1 or end < start:
                    raise AssertionError(f"invalid line interval: {register} {row['concept_id']} {locator}")
                declared = revisions.get(original)
                if declared is None:
                    raise AssertionError(
                        f"locator has no declared source revision: {register} {row['concept_id']} {original}"
                    )
                source = resolve_revision(original, declared, evidence)
                line_count = len(source.read_text(encoding="utf-8", errors="strict").splitlines())
                if end > line_count:
                    raise AssertionError(
                        f"locator exceeds source: {register} {row['concept_id']} {locator} lines={line_count}"
                    )
                count += 1
            extras = set(revisions) - {LOCATOR.fullmatch(item).group("path") for item in locators}
            if extras:
                raise AssertionError(
                    f"ambiguous unused source revisions: {register} {row['concept_id']} extras={sorted(extras)}"
                )
    return count


def validate_occurrence_registers() -> int:
    count = 0
    for register in OCCURRENCE_REGISTERS:
        with register.open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle, delimiter="\t"))
        for row in rows:
            path = row["path"]
            line = int(row["line"])
            column = int(row["column"])
            declared = row["source_revision"]
            if not declared.startswith("worktree_sha256:"):
                raise AssertionError(f"occurrence source is not a current worktree revision: {register} {path}")
            source = ROOT / path
            if digest(source) != declared.split(":", 1)[1]:
                raise AssertionError(f"occurrence source hash mismatch: {register} {path}:{line}")
            lines = source.read_text(encoding="utf-8", errors="strict").splitlines()
            if line < 1 or line > len(lines):
                raise AssertionError(f"occurrence line exceeds source: {register} {path}:{line}")
            context = lines[line - 1]
            if context != row["source_context"]:
                raise AssertionError(f"occurrence context mismatch: {register} {path}:{line}")
            context_hash = hashlib.sha256(context.encode("utf-8")).hexdigest()
            if context_hash != row["context_sha256"]:
                raise AssertionError(f"occurrence context hash mismatch: {register} {path}:{line}")
            if column < 1 or column > len(context) + 1:
                raise AssertionError(f"occurrence column exceeds source line: {register} {path}:{line}:{column}")
            count += 1
    return count


def main() -> int:
    evidence = index()
    adjudication_locator_count = validate_adjudication_registers(evidence)
    occurrence_locator_count = validate_occurrence_registers()
    print("source_locator_validation=PASS")
    print(f"adjudication_locators={adjudication_locator_count}")
    print(f"occurrence_locators={occurrence_locator_count}")
    print(f"source_revision_evidence_rows={len(evidence)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
