#!/usr/bin/env python3
"""Structural validator for P2 Recovery Part 1 semantic receipts.

This validator rejects known generic placeholders and incomplete assertion locators.
It does not decide whether a receipt's semantic judgement is correct.
"""
from __future__ import annotations

import argparse
import csv
import re
import sys
from dataclasses import dataclass
from pathlib import Path

RELATIONS = {
    "exact_full_proof",
    "bounded_separable_clause",
    "related_but_not_proved",
    "no_semantic_fit",
    "authority_missing",
    "authority_contradictory",
}
STRENGTHS = {
    "behavioural",
    "boundary",
    "state_transition",
    "identity_lineage",
    "substitution",
    "replay",
    "presence_only",
    "signature_only",
    "token_only",
    "specimen_only",
    "historical_observational",
}
DISPOSITIONS = {
    "ADMIT_TIER_A_CURRENT",
    "ADMIT_TIER_B_SHADOW",
    "BLOCKED_P3_REPAIR",
    "BLOCKED_MISSING_NORMATIVE_AUTHORITY",
    "NON_AUTHORITATIVE_OBSERVATIONAL",
    "RETIREMENT_RECOMMENDED_NOT_EXECUTED",
}
REQUIRED_LABELS = (
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
KNOWN_GENERIC_FRAGMENTS = (
    "break the asserted exact behaviour; the relevant assertion fails",
    "the stated assertion must fail when that behaviour is lost",
    "break the asserted exact behaviour",
    "the relevant assertion fails",
    "the stated assertion must fail",
)
EXACT_LOCATOR_RE = re.compile(
    r"(?:\bline(?:s)?\b|\bassertion(?:s)?\b|pytest\.raises)[^\n]{0,120}?"
    r"(?:`\d+(?:-\d+)?`|\b\d+(?:-\d+)?\b)",
    re.IGNORECASE,
)
GROUP_RE = re.compile(r"(?m)^## G(?P<num>\d+) — (?P<title>.+)$")
FIELD_RE = re.compile(r"(?m)^- (?P<label>[^:]+):\s*(?P<value>.+)$")


@dataclass(frozen=True)
class ValidationResult:
    sequence: str
    receipt_path: str
    groups: int
    relationships: int
    disposition: str
    errors: tuple[str, ...]

    @property
    def passed(self) -> bool:
        return not self.errors

    def output_lines(self) -> list[str]:
        if self.errors:
            return [
                f"RESULT=FAIL sequence={self.sequence} receipt={self.receipt_path}",
                *(f"ERROR={error}" for error in self.errors),
            ]
        return [
            (
                f"RESULT=PASS sequence={self.sequence} groups={self.groups} "
                f"relationships={self.relationships} disposition={self.disposition} "
                f"receipt={self.receipt_path}"
            ),
            "NOTE=Structural validation does not establish semantic acceptance.",
        ]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    scope = parser.add_mutually_exclusive_group(required=True)
    scope.add_argument("--sequence")
    scope.add_argument("--all", action="store_true", dest="validate_all")
    parser.add_argument(
        "--allow-ledger-no",
        action="store_true",
        help="validate a reopened receipt before its row is returned to YES",
    )
    return parser.parse_args()


def load_ledger(repo: Path) -> tuple[list[str], list[dict[str, str]]]:
    path = repo / "project_control/canonical_project_manager/P2_ABSOLUTE_SEMANTIC_READ_LEDGER.tsv"
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        return list(reader.fieldnames or []), list(reader)


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


def fields_for(group_body: str) -> dict[str, list[str]]:
    result: dict[str, list[str]] = {}
    for match in FIELD_RE.finditer(group_body):
        result.setdefault(match.group("label").strip(), []).append(match.group("value").strip())
    return result


def has_exact_locator(value: str) -> bool:
    return bool(EXACT_LOCATOR_RE.search(value))


def has_explicit_missing_assertion(value: str, disposition_value: str) -> bool:
    lower = value.lower()
    return (
        "no current assertion fails" in lower
        and "requires" in lower
        and "assertion" in lower
        and any(disposition in disposition_value for disposition in DISPOSITIONS)
    )


def forbidden_path_tokens() -> tuple[str, ...]:
    # Constructed in fragments so this validator does not itself contain a worker path.
    return (
        "/" + "mnt" + "/data/",
        "/" + "tmp/",
        "/" + "home" + "/oai/",
        "\\" + "mnt" + "\\data\\",
    )


def validate_sequence(repo: Path, sequence: str, *, allow_ledger_no: bool = False) -> ValidationResult:
    repo = repo.resolve()
    sequence = str(sequence).zfill(3)
    errors: list[str] = []

    _, rows = load_ledger(repo)
    matching = [row for row in rows if row.get("SEQUENCE") == sequence]
    if len(matching) != 1:
        return ValidationResult(sequence, "", 0, 0, "", (f"ledger row count {len(matching)}",))
    row = matching[0]
    seq_int = int(sequence)
    if not 67 <= seq_int <= 120:
        errors.append("sequence is outside Part 1 scope 067-120")
    if row.get("SEMANTICALLY_READ") != "YES" and not allow_ledger_no:
        errors.append(f"ledger SEMANTICALLY_READ={row.get('SEMANTICALLY_READ')!r}, expected YES")

    receipt_rel = row.get("RECEIPT_PATH", "")
    receipt_path = repo / receipt_rel
    if not receipt_path.is_file():
        errors.append(f"receipt missing: {receipt_rel}")
        text = ""
    else:
        text = receipt_path.read_text(encoding="utf-8")

    if f"Sequence `{sequence}`" not in text:
        errors.append("receipt sequence marker is absent or mismatched")
    if any(token in text for token in forbidden_path_tokens()):
        errors.append("worker-absolute path found in receipt")

    lowered = text.lower()
    for fragment in KNOWN_GENERIC_FRAGMENTS:
        if fragment in lowered:
            errors.append(f"known generic placeholder found: {fragment}")

    groups = split_groups(text)
    expected_groups_text = row.get("ASSERTION_GROUP_COUNT", "")
    try:
        expected_groups = int(expected_groups_text)
    except ValueError:
        expected_groups = -1
        errors.append(f"invalid ledger assertion group count: {expected_groups_text!r}")
    if len(groups) != expected_groups:
        errors.append(f"receipt group count {len(groups)} != ledger count {expected_groups}")
    if [number for number, _, _ in groups] != list(range(1, len(groups) + 1)):
        errors.append("group numbers are not contiguous from G1")

    test_path = row.get("TEST_PATH", "")
    test_file = repo / test_path
    if not test_file.is_file():
        errors.append(f"test path missing: {test_path}")

    group_dispositions: list[str] = []
    for number, title, body in groups:
        values = fields_for(body)
        for label in REQUIRED_LABELS:
            entries = values.get(label, [])
            if len(entries) != 1:
                errors.append(f"G{number} {title!r}: {label} count {len(entries)}, expected 1")
            elif not entries[0].strip():
                errors.append(f"G{number} {title!r}: {label} is empty")

        test_locator = (values.get("Test locator") or [""])[0]
        if test_path not in test_locator:
            errors.append(f"G{number}: test locator does not name the ledger test path")

        relation_raw = (values.get("Semantic relation") or [""])[0]
        relation_match = re.fullmatch(r"`([^`]+)`\.?", relation_raw)
        relation = relation_match.group(1) if relation_match else ""
        if relation not in RELATIONS:
            errors.append(f"G{number}: invalid semantic relation {relation_raw!r}")

        strength_raw = (values.get("Proof strength") or [""])[0]
        strength_match = re.fullmatch(r"`([^`]+)`\.?", strength_raw)
        strength = strength_match.group(1) if strength_match else ""
        if strength not in STRENGTHS:
            errors.append(f"G{number}: invalid proof strength {strength_raw!r}")

        disposition_raw = (values.get("Disposition and return gate") or [""])[0]
        disposition_match = re.match(r"`([^`]+)`(?:;|\.)", disposition_raw)
        disposition = disposition_match.group(1) if disposition_match else ""
        if disposition not in DISPOSITIONS:
            errors.append(f"G{number}: invalid group disposition {disposition_raw!r}")
        else:
            group_dispositions.append(disposition)
        if disposition.startswith("BLOCKED_") or disposition.startswith("RETIREMENT_"):
            if ";" not in disposition_raw or len(disposition_raw.split(";", 1)[1].strip()) < 12:
                errors.append(f"G{number}: blocked/retired disposition lacks a named return gate")

        falsifier = (values.get("Exact-surface falsifier") or [""])[0]
        assertion = (values.get("Assertion that must fail and why") or [""])[0]
        if not has_exact_locator(falsifier) and "no current assertion" not in falsifier.lower():
            errors.append(f"G{number}: exact-surface falsifier lacks an assertion locator or explicit assertion gap")
        if not (has_exact_locator(assertion) or has_explicit_missing_assertion(assertion, disposition_raw)):
            errors.append(
                f"G{number}: Assertion that must fail and why lacks an exact locator or explicit missing-assertion return gate"
            )
        for label in (
            "Authority match",
            "Behaviour proved",
            "Limitation",
            "Adversarial challenge",
            "Exact-surface falsifier",
            "Assertion that must fail and why",
        ):
            value = (values.get(label) or [""])[0]
            if len(value) < 20:
                errors.append(f"G{number}: {label} is structurally too short")

    relationship_text = row.get("RELATIONSHIP_COUNT", "")
    try:
        relationships = int(relationship_text)
    except ValueError:
        relationships = -1
        errors.append(f"invalid ledger relationship count: {relationship_text!r}")
    if relationships != len(groups):
        errors.append(f"ledger relationship count {relationships} != receipt group count {len(groups)}")

    summary = re.findall(r"(?m)^- Groups/relationships: `(\d+)/(\d+)`\.$", text)
    if summary != [(str(len(groups)), str(len(groups)))]:
        errors.append(f"file decision group summary mismatch: {summary!r}")

    final = re.findall(r"(?m)^- Final disposition: `([^`]+)`\.$", text)
    final_disposition = final[0] if len(final) == 1 else ""
    if len(final) != 1 or final_disposition not in DISPOSITIONS:
        errors.append(f"invalid or missing final disposition: {final!r}")
    else:
        if row.get("FINAL_FILE_DISPOSITION") and row.get("FINAL_FILE_DISPOSITION") != final_disposition:
            errors.append(
                f"ledger final disposition {row.get('FINAL_FILE_DISPOSITION')!r} != receipt {final_disposition!r}"
            )
        if group_dispositions and final_disposition not in set(group_dispositions):
            errors.append("final disposition is absent from all group dispositions")

    return ValidationResult(
        sequence=sequence,
        receipt_path=receipt_rel,
        groups=len(groups),
        relationships=relationships,
        disposition=final_disposition,
        errors=tuple(errors),
    )


def main() -> int:
    args = parse_args()
    repo = args.repo_root.resolve()
    sequences = [str(number).zfill(3) for number in range(67, 121)] if args.validate_all else [str(args.sequence).zfill(3)]
    failures = 0
    for sequence in sequences:
        result = validate_sequence(repo, sequence, allow_ledger_no=args.allow_ledger_no)
        for line in result.output_lines():
            print(line)
        failures += int(not result.passed)
    if args.validate_all:
        print(f"ROW_VALIDATOR_PASSES={len(sequences) - failures}")
        print(f"ROW_VALIDATOR_FAILURES={failures}")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
