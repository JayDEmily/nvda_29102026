#!/usr/bin/env python3
"""Mechanical validation for the evolved-vision reconstruction outputs.

This validator checks identity, coverage, references and required artefacts. It does
not decide semantic correctness, supersession or losslessness.
"""

from __future__ import annotations

import csv
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECON = ROOT / "reconstruction"
MANIFEST = ROOT / "SOURCE_MANIFEST.tsv"

REQUIRED_FILES = [
    ROOT / "PLANS.md",
    RECON / "00_METHOD_STATUS_AND_SOURCE_MANIFEST.md",
    RECON / "01_CHRONOLOGICAL_AUTHORITY_AND_SUPERSESSION_INDEX.md",
    RECON / "02_CANONICAL_VISION_INDEX.md",
    RECON / "03_SOURCE_RECONCILIATION.md",
    RECON / "04_UNRESOLVED_CONFLICTS_AND_EXTERNAL_REFERENCES.md",
    RECON / "05_FINAL_ASSURANCE_REPORT.md",
]
EXPECTED_TRANCHES = [f"A{i:02d}" for i in range(1, 16)] + [f"B{i:02d}" for i in range(1, 11)]
PROPOSITION_RE = re.compile(r"^## (P-[A-Z]+-\d{3}) — (.+)$", re.MULTILINE)
SOURCE_CITATION_RE = re.compile(
    r"`((?:source_planning|source_successor_briefs)/[^`]+\.md):L(\d+)-L(\d+)`"
)
SOURCE_ID_RE = re.compile(r"\|\s*([AB]\d{3})\s*\|")
PROP_ID_RE = re.compile(r"P-[A-Z]+-\d{3}")
MARKDOWN_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def read_manifest() -> list[dict[str, str]]:
    if not MANIFEST.is_file():
        fail("SOURCE_MANIFEST.tsv is missing")
    with MANIFEST.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def validate_required_outputs() -> None:
    missing = [p.relative_to(ROOT).as_posix() for p in REQUIRED_FILES if not p.is_file()]
    if missing:
        fail(f"required output files are missing: {missing}")
    empty = [p.relative_to(ROOT).as_posix() for p in REQUIRED_FILES if p.stat().st_size == 0]
    if empty:
        fail(f"required output files are empty: {empty}")
    vision = sorted((RECON / "vision").glob("*.md"))
    if len(vision) != 10:
        fail(f"expected 10 canonical vision documents; observed {len(vision)}")
    if any(p.stat().st_size == 0 for p in vision):
        fail("one or more canonical vision documents are empty")


def validate_propositions() -> set[str]:
    records = sorted((RECON / "propositions").glob("*.md"))
    expected_records = {f"{t}.md" for t in EXPECTED_TRANCHES}
    observed_records = {p.name for p in records}
    if observed_records != expected_records:
        fail(
            "proposition-record set differs; "
            f"missing={sorted(expected_records-observed_records)}, "
            f"extra={sorted(observed_records-expected_records)}"
        )

    definitions: list[str] = []
    citation_count = 0
    for path in records:
        text = path.read_text(encoding="utf-8")
        local_defs = [m.group(1) for m in PROPOSITION_RE.finditer(text)]
        definitions.extend(local_defs)
        if local_defs and "source_" not in text:
            fail(f"proposition record lacks source lineage: {path.relative_to(ROOT)}")
        citation_count += len(SOURCE_CITATION_RE.findall(text))

    counts = Counter(definitions)
    duplicates = sorted(pid for pid, count in counts.items() if count != 1)
    if duplicates:
        fail(f"proposition IDs are not uniquely defined: {duplicates}")
    if len(definitions) != 83:
        fail(f"expected 83 proposition definitions; observed {len(definitions)}")
    if citation_count == 0:
        fail("no full source citations found in proposition records")
    return set(definitions)


def validate_source_citations() -> None:
    files = list((RECON / "propositions").glob("*.md"))
    files += [
        RECON / "01_CHRONOLOGICAL_AUTHORITY_AND_SUPERSESSION_INDEX.md",
        RECON / "04_UNRESOLVED_CONFLICTS_AND_EXTERNAL_REFERENCES.md",
    ]
    checked = 0
    for path in files:
        text = path.read_text(encoding="utf-8")
        for rel, start_raw, end_raw in SOURCE_CITATION_RE.findall(text):
            source = ROOT / rel
            if not source.is_file():
                fail(f"citation path does not exist in {path.relative_to(ROOT)}: {rel}")
            start, end = int(start_raw), int(end_raw)
            line_count = sum(1 for _ in source.open("r", encoding="utf-8"))
            if start < 1 or end < start or end > line_count:
                fail(
                    f"invalid citation range in {path.relative_to(ROOT)}: "
                    f"{rel}:L{start}-L{end} (source has {line_count} lines)"
                )
            checked += 1
    if checked < 100:
        fail(f"expected at least 100 validated full source citations; observed {checked}")


def validate_source_reconciliation(rows: list[dict[str, str]]) -> None:
    text = (RECON / "03_SOURCE_RECONCILIATION.md").read_text(encoding="utf-8")
    observed_ids = SOURCE_ID_RE.findall(text)
    counts = Counter(observed_ids)
    manifest_ids = {row["source_id"] for row in rows}
    if set(observed_ids) != manifest_ids:
        fail(
            "source reconciliation IDs differ from manifest; "
            f"missing={sorted(manifest_ids-set(observed_ids))}, "
            f"extra={sorted(set(observed_ids)-manifest_ids)}"
        )
    duplicates = sorted(source_id for source_id, count in counts.items() if count != 1)
    if duplicates:
        fail(f"source IDs are not reconciled exactly once: {duplicates}")
    for row in rows:
        path = row["repository_path"]
        if text.count(f"`{path}`") != 1:
            fail(f"source path is not reconciled exactly once: {path}")


def validate_reviews() -> None:
    review_dir = RECON / "tranches"
    reviews = sorted(review_dir.glob("*_REVIEW.md"))
    expected = {f"{t}_REVIEW.md" for t in EXPECTED_TRANCHES}
    observed = {p.name for p in reviews}
    if observed != expected:
        fail(
            "review set differs; "
            f"missing={sorted(expected-observed)}, extra={sorted(observed-expected)}"
        )
    for path in reviews:
        text = path.read_text(encoding="utf-8")
        if not re.search(r"\bPASS\b", text):
            fail(f"review does not record PASS: {path.relative_to(ROOT)}")


def validate_canonical_coverage(propositions: set[str]) -> None:
    vision_files = sorted((RECON / "vision").glob("*.md"))
    counts: Counter[str] = Counter()
    for path in vision_files:
        text = path.read_text(encoding="utf-8")
        for pid in PROP_ID_RE.findall(text):
            counts[pid] += 1
    if set(counts) != propositions:
        fail(
            "canonical vision proposition coverage differs; "
            f"missing={sorted(propositions-set(counts))}, "
            f"extra={sorted(set(counts)-propositions)}"
        )
    repeated = sorted(pid for pid, count in counts.items() if count != 1)
    if repeated:
        fail(f"propositions are not assigned to exactly one canonical document: {repeated}")

    index = (RECON / "02_CANONICAL_VISION_INDEX.md").read_text(encoding="utf-8")
    missing_index = sorted(pid for pid in propositions if pid not in index)
    if missing_index:
        fail(f"canonical index omits proposition IDs: {missing_index}")
    for path in vision_files:
        rel = path.relative_to(RECON).as_posix()
        if rel not in index:
            fail(f"canonical index omits vision document: {rel}")


def validate_plan_schedule(rows: list[dict[str, str]]) -> None:
    plan = (ROOT / "PLANS.md").read_text(encoding="utf-8")
    for tranche in EXPECTED_TRANCHES:
        if tranche not in plan:
            fail(f"PLANS.md omits tranche {tranche}")
    for row in rows:
        if row["source_id"] not in plan and row["source_id"] not in (RECON / "03_SOURCE_RECONCILIATION.md").read_text(encoding="utf-8"):
            fail(f"source ID absent from schedule and reconciliation: {row['source_id']}")



def validate_markdown_links() -> None:
    for path in sorted(RECON.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        for target in MARKDOWN_LINK_RE.findall(text):
            target = target.split("#", 1)[0]
            if not target or "://" in target or target.startswith("mailto:"):
                continue
            linked = (path.parent / target).resolve()
            try:
                linked.relative_to(ROOT.resolve())
            except ValueError:
                fail(f"markdown link escapes repository in {path.relative_to(ROOT)}: {target}")
            if not linked.exists():
                fail(f"broken markdown link in {path.relative_to(ROOT)}: {target}")


def validate_source_tree_git_clean() -> None:
    command = [
        "git",
        "diff",
        "--exit-code",
        "--",
        "source_planning",
        "source_successor_briefs",
        "SOURCE_MANIFEST.tsv",
    ]
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    if result.returncode != 0:
        sys.stderr.write(result.stdout)
        sys.stderr.write(result.stderr)
        fail("immutable source corpus or manifest differs from Git")


def main() -> None:
    rows = read_manifest()
    validate_required_outputs()
    propositions = validate_propositions()
    validate_source_citations()
    validate_source_reconciliation(rows)
    validate_reviews()
    validate_canonical_coverage(propositions)
    validate_plan_schedule(rows)
    validate_markdown_links()
    validate_source_tree_git_clean()
    print(
        "PASS: reconstruction mechanics validated "
        "(98 sources, 25 tranche records/reviews, 83 propositions, 10 canonical documents)"
    )
    print(
        "NOTE: this script validates artefact presence, identity, coverage and citations; "
        "it does not certify semantic losslessness or independent review"
    )


if __name__ == "__main__":
    main()
