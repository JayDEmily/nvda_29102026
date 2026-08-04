#!/usr/bin/env python3
"""Mechanically validate the chronological-semantic chapter reconstruction.

This validator checks proposition assignment, file/reference integrity and explicit
visibility controls. It does not certify semantic fidelity, authority resolution
or losslessness.
"""

from __future__ import annotations

import csv
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHAPTER_ROOT = ROOT / "chapter_reconstruction"
MAP_TSV = CHAPTER_ROOT / "02_PROPOSITION_TO_CHAPTER_MAP.tsv"
MAP_MD = CHAPTER_ROOT / "02_PROPOSITION_TO_CHAPTER_MAP.md"
INDEX_MD = CHAPTER_ROOT / "01_CHAPTER_INDEX.md"

CHAPTERS = {
    "01": "01_SYSTEM_PURPOSE_AND_ADVISORY_LIMITS.md",
    "02": "02_DATA_TRUTH_FROM_SOURCE_TO_STAGE_INPUTS.md",
    "03": "03_TEMPORAL_TRUTH_CALENDARS_AND_PROVENANCE.md",
    "04": "04_SERIAL_COGNITION_AND_STAGE_OWNERSHIP.md",
    "05": "05_PLAYBOOKS_POSTURE_MODIFIERS_AND_EXECUTION_CHOICES.md",
    "06": "06_DMP_PROTOCOL_EVOLUTION_AND_PACKET_CARRIAGE.md",
    "07": "07_PARALLEL_RISK_TERMINAL_RISK_AND_CAPITAL.md",
    "08": "08_EXECUTION_LIFECYCLE_CARRY_STATE_AND_PERSISTENCE.md",
    "09": "09_REVIEW_TRACE_REPLAY_AND_ASSURANCE.md",
    "10": "10_GOVERNANCE_COMPATIBILITY_AND_PUBLIC_BOUNDARIES.md",
}
REQUIRED_OUTPUTS = [
    CHAPTER_ROOT / "00_METHOD_AND_BASELINE.md",
    INDEX_MD,
    MAP_MD,
    MAP_TSV,
    CHAPTER_ROOT / "03_CROSS_REFERENCE_AND_COVERAGE.md",
    CHAPTER_ROOT / "04_CHAPTER_ASSURANCE_REPORT.md",
]
PROP_HEADING_RE = re.compile(r"^## (P-[A-Z]+-\d{3}) — ", re.MULTILINE)
PROP_ID_RE = re.compile(r"P-[A-Z]+-\d{3}")
PRIMARY_RE = re.compile(r"^\*\*Primary propositions:\*\* (.+)$", re.MULTILINE)
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
ALLOWED_STATES = {"active", "partially_superseded", "unresolved"}
ALLOWED_ROLES = {
    "introduction",
    "refinement",
    "constraint",
    "challenge",
    "replacement",
    "reinstatement",
    "current_form",
    "unresolved",
    "supporting_context",
}


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def proposition_ids() -> set[str]:
    ids: list[str] = []
    for path in sorted((ROOT / "reconstruction" / "propositions").glob("*.md")):
        ids.extend(PROP_HEADING_RE.findall(path.read_text(encoding="utf-8")))
    counts = Counter(ids)
    duplicates = sorted(pid for pid, count in counts.items() if count != 1)
    if duplicates:
        fail(f"approved proposition definitions are not unique: {duplicates}")
    if len(ids) != 83:
        fail(f"expected 83 approved propositions; observed {len(ids)}")
    return set(ids)


def read_map() -> list[dict[str, str]]:
    if not MAP_TSV.is_file():
        fail("chapter map TSV is missing")
    with MAP_TSV.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    required = {
        "proposition_id",
        "title",
        "authority_state",
        "primary_chapter",
        "primary_chapter_title",
        "cross_references",
        "developmental_role",
        "semantic_rationale",
        "proposition_record",
    }
    if not rows:
        fail("chapter map TSV is empty")
    missing = required.difference(rows[0])
    if missing:
        fail(f"chapter map TSV lacks columns: {sorted(missing)}")
    return rows


def validate_required_outputs() -> None:
    missing = [p.relative_to(ROOT).as_posix() for p in REQUIRED_OUTPUTS if not p.is_file()]
    if missing:
        fail(f"required chapter outputs are missing: {missing}")
    empty = [p.relative_to(ROOT).as_posix() for p in REQUIRED_OUTPUTS if p.stat().st_size == 0]
    if empty:
        fail(f"required chapter outputs are empty: {empty}")

    observed = {p.name for p in (CHAPTER_ROOT / "chapters").glob("*.md")}
    expected = set(CHAPTERS.values())
    if observed != expected:
        fail(
            "chapter file set differs; "
            f"missing={sorted(expected-observed)}, extra={sorted(observed-expected)}"
        )


def validate_map(rows: list[dict[str, str]], approved: set[str]) -> dict[str, list[str]]:
    ids = [r["proposition_id"] for r in rows]
    counts = Counter(ids)
    duplicates = sorted(pid for pid, count in counts.items() if count != 1)
    if duplicates:
        fail(f"primary map proposition IDs are not unique: {duplicates}")
    if set(ids) != approved:
        fail(
            "primary map coverage differs from approved propositions; "
            f"missing={sorted(approved-set(ids))}, extra={sorted(set(ids)-approved)}"
        )
    if len(rows) != 83:
        fail(f"expected 83 primary assignments; observed {len(rows)}")

    by_chapter: dict[str, list[str]] = {chapter: [] for chapter in CHAPTERS}
    for row in rows:
        pid = row["proposition_id"]
        chapter = row["primary_chapter"]
        if chapter not in CHAPTERS:
            fail(f"{pid} has invalid primary chapter: {chapter}")
        by_chapter[chapter].append(pid)
        if row["authority_state"] not in ALLOWED_STATES:
            fail(f"{pid} has invalid authority state: {row['authority_state']}")
        if row["developmental_role"] not in ALLOWED_ROLES:
            fail(f"{pid} has invalid developmental role: {row['developmental_role']}")
        if not row["semantic_rationale"].strip():
            fail(f"{pid} lacks semantic rationale")
        record = ROOT / row["proposition_record"]
        if not record.is_file():
            fail(f"{pid} references missing proposition record: {row['proposition_record']}")
        if not re.search(rf"^## {re.escape(pid)} — ", record.read_text(encoding="utf-8"), re.MULTILINE):
            fail(f"{pid} is not defined by mapped proposition record: {row['proposition_record']}")

        refs = [value for value in row["cross_references"].split(";") if value]
        bad_refs = sorted(set(refs).difference(CHAPTERS))
        if bad_refs:
            fail(f"{pid} has invalid cross-reference chapters: {bad_refs}")
        if chapter in refs:
            fail(f"{pid} cross-references its own primary chapter")
        if len(refs) != len(set(refs)):
            fail(f"{pid} has duplicate cross-reference chapters")

    if any(not ids for ids in by_chapter.values()):
        fail("one or more chapters have no primary propositions")
    return by_chapter


def validate_chapters(by_chapter: dict[str, list[str]], approved: set[str]) -> None:
    for chapter, filename in CHAPTERS.items():
        path = CHAPTER_ROOT / "chapters" / filename
        text = path.read_text(encoding="utf-8")
        primary_match = PRIMARY_RE.search(text)
        if not primary_match:
            fail(f"chapter {chapter} lacks a primary-propositions declaration")
        declared = PROP_ID_RE.findall(primary_match.group(1))
        if Counter(declared) != Counter(by_chapter[chapter]):
            fail(
                f"chapter {chapter} primary declaration differs from TSV; "
                f"declared={declared}, mapped={by_chapter[chapter]}"
            )
        for pid in by_chapter[chapter]:
            if text.count(pid) < 2:
                fail(f"chapter {chapter} does not substantively expose primary proposition {pid}")
        unknown = sorted(set(PROP_ID_RE.findall(text)).difference(approved))
        if unknown:
            fail(f"chapter {chapter} contains unknown proposition IDs: {unknown}")
        if not re.search(r"^## (?:\d+\. )?Current authoritative position$", text, re.MULTILINE):
            fail(f"chapter {chapter} lacks a current-authoritative-position section")
        if not re.search(r"^## (?:\d+\. )?.*[Uu]nresolved.*$", text, re.MULTILINE):
            fail(f"chapter {chapter} lacks an unresolved-matters section")

    ch1 = (CHAPTER_ROOT / "chapters" / CHAPTERS["01"]).read_text(encoding="utf-8").lower()
    ch2 = (CHAPTER_ROOT / "chapters" / CHAPTERS["02"]).read_text(encoding="utf-8").lower()
    ch6 = (CHAPTER_ROOT / "chapters" / CHAPTERS["06"]).read_text(encoding="utf-8").lower()
    if "p-res-001" not in ch1 or "unresolved" not in ch1:
        fail("P-RES-001 is not visibly unresolved in Chapter 1")
    if "p-arch-010" not in ch2 or "unresolved" not in ch2:
        fail("P-ARCH-010 is not visibly unresolved in Chapter 2")
    if "p-proto-002" not in ch6 or not re.search(r"partial(?:ly)? supersess", ch6):
        fail("P-PROTO-002 partial supersession is not explicit in Chapter 6")


def validate_markdown_links() -> None:
    markdown_files = [
        CHAPTER_ROOT / "00_METHOD_AND_BASELINE.md",
        INDEX_MD,
        MAP_MD,
        CHAPTER_ROOT / "03_CROSS_REFERENCE_AND_COVERAGE.md",
        CHAPTER_ROOT / "04_CHAPTER_ASSURANCE_REPORT.md",
        *sorted((CHAPTER_ROOT / "chapters").glob("*.md")),
    ]
    checked = 0
    for path in markdown_files:
        text = path.read_text(encoding="utf-8")
        for raw_target in LINK_RE.findall(text):
            target = raw_target.split("#", 1)[0]
            if not target or "://" in target or target.startswith("mailto:"):
                continue
            resolved = (path.parent / target).resolve()
            if not resolved.exists():
                fail(f"broken Markdown link in {path.relative_to(ROOT)}: {raw_target}")
            checked += 1
    if checked < 25:
        fail(f"unexpectedly few internal Markdown links validated: {checked}")


def validate_projection_surfaces(approved: set[str]) -> None:
    for path in (MAP_MD, INDEX_MD, CHAPTER_ROOT / "03_CROSS_REFERENCE_AND_COVERAGE.md"):
        text_ids = set(PROP_ID_RE.findall(path.read_text(encoding="utf-8")))
        missing = sorted(approved.difference(text_ids))
        if missing:
            fail(f"{path.relative_to(ROOT)} does not expose all approved propositions: {missing}")
        unknown = sorted(text_ids.difference(approved))
        if unknown:
            fail(f"{path.relative_to(ROOT)} contains unknown proposition IDs: {unknown}")


def main() -> None:
    approved = proposition_ids()
    validate_required_outputs()
    rows = read_map()
    by_chapter = validate_map(rows, approved)
    validate_chapters(by_chapter, approved)
    validate_markdown_links()
    validate_projection_surfaces(approved)
    counts = ", ".join(f"Ch{chapter}={len(ids)}" for chapter, ids in by_chapter.items())
    print(f"PASS: 83 approved propositions assigned exactly once across 10 chapters ({counts})")
    print("PASS: chapter files, primary declarations, mappings, cross-references and visibility controls resolve")
    print("NOTE: this script validates structure and coverage only; it does not certify semantic fidelity or losslessness")


if __name__ == "__main__":
    main()
