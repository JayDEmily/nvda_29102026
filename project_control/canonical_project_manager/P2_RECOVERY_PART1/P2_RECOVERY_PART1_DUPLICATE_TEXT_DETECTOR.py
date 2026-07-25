#!/usr/bin/env python3
"""Report exact duplicate or known-generic reasoning across Part 1 receipts.

The detector is deliberately non-semantic: it produces a human review list and
requires an explicit resolution register for any exact duplicate that remains.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import re
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

REQUIRED_FIELDS = (
    "Test locator",
    "Authority locator",
    "Authority match",
    "Behaviour proved",
    "Limitation",
    "Adversarial challenge",
    "Exact-surface falsifier",
    "Assertion that must fail and why",
    "Semantic relation",
    "Proof strength",
    "Disposition and return gate",
)
KNOWN_GENERIC = (
    "break the asserted exact behaviour; the relevant assertion fails.",
    "the stated assertion must fail when that behaviour is lost.",
    "break the asserted exact behaviour; the relevant assertion fails",
    "the stated assertion must fail when that behaviour is lost",
)
GROUP_RE = re.compile(r"(?m)^## G(?P<num>\d+) — (?P<title>.+)$")
FIELD_RE = re.compile(r"(?m)^- (?P<label>[^:]+):\s*(?P<value>.+)$")


@dataclass(frozen=True)
class Occurrence:
    sequence: str
    group: int
    title: str
    field: str
    receipt_path: str
    value: str

    @property
    def key(self) -> str:
        return f"{self.sequence}:G{self.group}:{self.field}"


def normalise(value: str) -> str:
    return " ".join(value.split()).casefold()


def hit_id(kind: str, normalised_value: str, occurrences: list[Occurrence]) -> str:
    material = kind + "\n" + normalised_value + "\n" + "\n".join(sorted(o.key for o in occurrences))
    return hashlib.sha256(material.encode("utf-8")).hexdigest()[:16]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--report", type=Path)
    parser.add_argument("--resolutions", type=Path)
    return parser.parse_args()


def split_groups(text: str) -> list[tuple[int, str, str]]:
    matches = list(GROUP_RE.finditer(text))
    groups: list[tuple[int, str, str]] = []
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else text.find("\n## File decision", start)
        if end < 0:
            end = len(text)
        groups.append((int(match.group("num")), match.group("title").strip(), text[start:end]))
    return groups


def load_resolutions(path: Path | None) -> dict[str, tuple[str, str]]:
    if path is None or not path.is_file():
        return {}
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        return {
            row.get("HIT_ID", ""): (row.get("STATUS", "").strip(), row.get("JUSTIFICATION", "").strip())
            for row in reader
            if row.get("HIT_ID")
        }


def main() -> int:
    args = parse_args()
    repo = args.repo_root.resolve()
    p1 = repo / "project_control/canonical_project_manager/P2_RECOVERY_PART1"
    report_path = args.report or (p1 / "validation/DUPLICATE_GENERIC_REVIEW.tsv")
    resolution_path = args.resolutions or (p1 / "validation/DUPLICATE_REVIEW_RESOLUTIONS.tsv")
    if not report_path.is_absolute():
        report_path = repo / report_path
    if not resolution_path.is_absolute():
        resolution_path = repo / resolution_path

    ledger_path = repo / "project_control/canonical_project_manager/P2_ABSOLUTE_SEMANTIC_READ_LEDGER.tsv"
    with ledger_path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    scoped = [row for row in rows if 67 <= int(row["SEQUENCE"]) <= 120]
    if len(scoped) != 54:
        print(f"RESULT=FAIL scoped_rows={len(scoped)} expected=54")
        return 1

    occurrences: list[Occurrence] = []
    structural_errors: list[str] = []
    for row in scoped:
        receipt_rel = row["RECEIPT_PATH"]
        text = (repo / receipt_rel).read_text(encoding="utf-8")
        for group_number, title, body in split_groups(text):
            values: dict[str, list[str]] = defaultdict(list)
            for match in FIELD_RE.finditer(body):
                values[match.group("label").strip()].append(match.group("value").strip())
            for field in REQUIRED_FIELDS:
                entries = values.get(field, [])
                if len(entries) != 1:
                    structural_errors.append(
                        f"{row['SEQUENCE']}:G{group_number}:{field}:count={len(entries)}"
                    )
                    continue
                occurrences.append(
                    Occurrence(
                        sequence=row["SEQUENCE"],
                        group=group_number,
                        title=title,
                        field=field,
                        receipt_path=receipt_rel,
                        value=entries[0],
                    )
                )

    if structural_errors:
        print("RESULT=FAIL structural_errors")
        for error in structural_errors:
            print(f"ERROR={error}")
        return 1

    hits: list[tuple[str, str, str, list[Occurrence]]] = []
    generic_norms = {normalise(value) for value in KNOWN_GENERIC}
    for occurrence in occurrences:
        norm = normalise(occurrence.value)
        if norm in generic_norms:
            hits.append((hit_id("KNOWN_PLACEHOLDER", norm, [occurrence]), "KNOWN_PLACEHOLDER", norm, [occurrence]))

    by_value: dict[str, list[Occurrence]] = defaultdict(list)
    for occurrence in occurrences:
        by_value[normalise(occurrence.value)].append(occurrence)
    for norm, same in by_value.items():
        if len(same) > 1:
            hits.append((hit_id("EXACT_DUPLICATE", norm, same), "EXACT_DUPLICATE", norm, sorted(same, key=lambda o: o.key)))

    # Deduplicate a placeholder hit from an identical duplicate-group hit only by hit ID/kind;
    # both remain visible because they represent separate review reasons.
    hits.sort(key=lambda item: (item[1], item[0]))
    resolutions = load_resolutions(resolution_path)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    unresolved = 0
    with report_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(
            [
                "HIT_ID",
                "HIT_KIND",
                "FIELD_SET",
                "OCCURRENCE_COUNT",
                "OCCURRENCES",
                "TEXT",
                "RESOLUTION_STATUS",
                "JUSTIFICATION",
            ]
        )
        for identifier, kind, _norm, same in hits:
            status, justification = resolutions.get(identifier, ("", ""))
            resolved = kind == "EXACT_DUPLICATE" and status == "JUSTIFIED" and bool(justification)
            if not resolved:
                unresolved += 1
            writer.writerow(
                [
                    identifier,
                    kind,
                    "|".join(sorted({o.field for o in same})),
                    len(same),
                    "|".join(o.key for o in same),
                    same[0].value,
                    status if resolved else "UNRESOLVED",
                    justification if resolved else "",
                ]
            )

    print(f"RESULT={'PASS' if unresolved == 0 else 'FAIL'}")
    print(f"SCOPED_RECEIPTS={len(scoped)}")
    print(f"SEMANTIC_FIELDS_EXAMINED={len(occurrences)}")
    print(f"REVIEW_HITS={len(hits)}")
    print(f"UNRESOLVED_HITS={unresolved}")
    print(f"REPORT={report_path.relative_to(repo).as_posix()}")
    if resolutions:
        unused = sorted(set(resolutions) - {item[0] for item in hits})
        print(f"UNUSED_RESOLUTIONS={len(unused)}")
    return 0 if unresolved == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
