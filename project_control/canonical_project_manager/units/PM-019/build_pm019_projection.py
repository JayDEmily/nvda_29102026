from __future__ import annotations

import csv
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
UNIT = ROOT / "project_control/canonical_project_manager/units/PM-019"
LEDGER = ROOT / "project_control/canonical_project_manager/P2_ABSOLUTE_SEMANTIC_READ_LEDGER.tsv"

ALLOWED_RELATIONS = {
    "exact_full_proof",
    "bounded_separable_clause",
    "related_but_not_proved",
    "no_semantic_fit",
    "authority_missing",
    "authority_contradictory",
}
ALLOWED_STRENGTHS = {
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
ALLOWED_DISPOSITIONS = {
    "ADMIT_TIER_A_CURRENT",
    "ADMIT_TIER_B_SHADOW",
    "BLOCKED_P3_REPAIR",
    "BLOCKED_MISSING_NORMATIVE_AUTHORITY",
    "NON_AUTHORITATIVE_OBSERVATIONAL",
    "RETIREMENT_RECOMMENDED_NOT_EXECUTED",
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def write_tsv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def find_end(lines: list[str], start: int, starts: list[int]) -> int:
    later = [i for i in starts if i > start]
    if later:
        return min(later)
    for i in range(start + 1, len(lines)):
        if re.match(r"^##\s+(?:File|Whole-file|Final)", lines[i], re.I):
            return i
    return len(lines)


def parse_groups(text: str, expected: int) -> tuple[list[dict[str, object]], str]:
    lines = text.splitlines()
    starts: list[tuple[int, int, str]] = []
    for i, line in enumerate(lines):
        m = re.match(
            r"^#{2,4}\s+(?:(?:\d+\.\s+)?Assertion group\s+|Group\s+|G)(\d+)\b",
            line,
            re.I,
        )
        if m:
            starts.append((i, int(m.group(1)), line))
    if len(starts) == expected:
        indexes = [x[0] for x in starts]
        return [
            {
                "ordinal": n,
                "heading": heading,
                "start_line": i + 1,
                "end_line": find_end(lines, i, indexes),
                "text": "\n".join(lines[i : find_end(lines, i, indexes)]).strip(),
            }
            for i, n, heading in starts
        ], "headings"

    relation_start = None
    relation_end = len(lines)
    for i, line in enumerate(lines):
        if re.match(r"^##\s+.*(?:Relationship|Assertion-group)", line, re.I):
            relation_start = i + 1
            break
    if relation_start is not None:
        for i in range(relation_start, len(lines)):
            if re.match(r"^##\s+(?:File|Whole-file|Final)", lines[i], re.I):
                relation_end = i
                break
        numbered: list[tuple[int, int, str]] = []
        for i in range(relation_start, relation_end):
            m = re.match(r"^(\d+)\.\s+", lines[i])
            if m:
                numbered.append((i, int(m.group(1)), lines[i]))
        if len(numbered) == expected:
            indexes = [x[0] for x in numbered] + [relation_end]
            result = []
            for index, (i, n, heading) in enumerate(numbered):
                end = indexes[index + 1]
                result.append(
                    {
                        "ordinal": n,
                        "heading": heading,
                        "start_line": i + 1,
                        "end_line": end,
                        "text": "\n".join(lines[i:end]).strip(),
                    }
                )
            return result, "numbered_relationships"
        table: list[dict[str, object]] = []
        seen: set[int] = set()
        for i in range(relation_start, relation_end):
            m = re.match(r"^\|\s*(\d+)\s*\|", lines[i])
            if m and int(m.group(1)) not in seen:
                n = int(m.group(1))
                seen.add(n)
                table.append(
                    {
                        "ordinal": n,
                        "heading": lines[i],
                        "start_line": i + 1,
                        "end_line": i + 1,
                        "text": lines[i],
                    }
                )
        if len(table) == expected:
            return table, "table"

    bullets: list[tuple[int, int, str]] = []
    for i, line in enumerate(lines):
        m = re.match(r"^[-*]\s+(?:\*\*)?G(?:roup)?\s*(\d+)\b", line, re.I)
        if m:
            bullets.append((i, int(m.group(1)), line))
    if len(bullets) == expected:
        indexes = [x[0] for x in bullets]
        return [
            {
                "ordinal": n,
                "heading": heading,
                "start_line": i + 1,
                "end_line": find_end(lines, i, indexes),
                "text": "\n".join(lines[i : find_end(lines, i, indexes)]).strip(),
            }
            for i, n, heading in bullets
        ], "bullets"

    table_anywhere: list[dict[str, object]] = []
    seen: set[int] = set()
    for i, line in enumerate(lines):
        m = re.match(r"^\|\s*(\d+)\s*\|", line)
        if m and int(m.group(1)) not in seen:
            n = int(m.group(1))
            seen.add(n)
            table_anywhere.append(
                {
                    "ordinal": n,
                    "heading": line,
                    "start_line": i + 1,
                    "end_line": i + 1,
                    "text": line,
                }
            )
    if len(table_anywhere) == expected:
        return table_anywhere, "table_anywhere"

    if expected == 1:
        candidates = [
            (i, line)
            for i, line in enumerate(lines)
            if re.search(r"\b(?:Sole group|Assertion group)\b", line, re.I)
        ]
        if candidates:
            i, heading = candidates[0]
            end = find_end(lines, i, [i])
            return [
                {
                    "ordinal": 1,
                    "heading": heading,
                    "start_line": i + 1,
                    "end_line": end,
                    "text": "\n".join(lines[i:end]).strip(),
                }
            ], "sole"

    raise ValueError(f"Could not mechanically parse {expected} assertion groups")


def ordered_unique(items: list[str]) -> list[str]:
    return list(dict.fromkeys(items))


def extract_explicit_enum(text: str, kind: str) -> tuple[str, str]:
    if kind == "relation":
        allowed = ALLOWED_RELATIONS
        patterns = [
            r"\*\*Semantic relation:\*\*\s*`?([a-z_]+)",
            r"\bRelation\s*[: ]\s*`([a-z_]+)`",
            r"\brelation\s+`([a-z_]+)`",
            r"\|\s*`?([a-z_]+)`?\s*/\s*`?[a-z_]+`?\s*\|",
            r"\.\s*`([a-z_]+)`\s*/\s*`[a-z_]+`",
        ]
    else:
        allowed = ALLOWED_STRENGTHS
        patterns = [
            r"\*\*Proof strength:\*\*\s*`?([a-z_]+)",
            r"\bStrength\s*[: ]\s*`([a-z_]+)`",
            r"\bstrength\s+`([a-z_]+)`",
            r"\|\s*`?[a-z_]+`?\s*/\s*`?([a-z_]+)`?\s*\|",
            r"\.\s*`[a-z_]+`\s*/\s*`([a-z_]+)`",
        ]
    raw: list[str] = []
    for pattern in patterns:
        raw.extend(x.lower() for x in re.findall(pattern, text, re.I))
    raw = ordered_unique(raw)
    allowed_hits = [x for x in raw if x in allowed]
    if len(allowed_hits) == 1:
        return allowed_hits[0], "RESOLVED_ALLOWED_ENUM"
    if len(allowed_hits) > 1:
        return "|".join(allowed_hits), "AMBIGUOUS_MULTIPLE_ALLOWED_ENUMS"
    if raw:
        return "|".join(raw), "NON_ENUM_EXPLICIT_VALUE"
    return "", "UNRESOLVED_NOT_EXPLICITLY_PARSED"


def extract_authority(text: str) -> tuple[list[str], list[str], list[str]]:
    ids = sorted(
        set(
            re.findall(
                r"\b(?:N\d+(?:\.\d+)?-\d{3}|C-\d{3}|PRP-\d{3}|P1-\d{3}|PM-\d{3}-[A-Z0-9-]+)\b",
                text,
            )
        )
    )
    candidates = sorted(
        set(
            re.findall(
                r"(?:(?:docs|project_control|config)/[^`\s,)\];]+\.(?:md|tsv|yaml|json))(?::\d+(?:-\d+)?)?",
                text,
            )
        )
    )
    exact: list[str] = []
    unresolved: list[str] = []
    for value in candidates:
        path_part = value.split(":", 1)[0]
        if "..." not in path_part and (ROOT / path_part).exists():
            exact.append(value)
        else:
            unresolved.append(value)
    return ids, exact, unresolved


def file_decision_excerpt(text: str) -> str:
    lines = text.splitlines()
    starts = [
        i
        for i, line in enumerate(lines)
        if re.match(r"^##\s+(?:\d+\.\s+)?(?:File|Final).*disposition|^##\s+File decision", line, re.I)
    ]
    if starts:
        return "\n".join(lines[starts[-1] :]).strip()
    return "\n".join(lines[-12:]).strip()


ledger = read_rows(LEDGER)
if len(ledger) != 179 or any(row["SEMANTICALLY_READ"] != "YES" for row in ledger):
    raise SystemExit("PM-019 requires exactly 179 completed ledger rows")

candidate_rows: list[dict[str, str]] = []
group_rows: list[dict[str, str]] = []
proof_rows: list[dict[str, str]] = []
dependency_rows: list[dict[str, str]] = []

for row in ledger:
    test_path = ROOT / row["TEST_PATH"]
    receipt_path = ROOT / row["RECEIPT_PATH"]
    if not test_path.is_file() or not receipt_path.is_file():
        raise SystemExit(f"Missing current path for sequence {row['SEQUENCE']}")
    text = receipt_path.read_text(encoding="utf-8")
    groups, parse_mode = parse_groups(text, int(row["ASSERTION_GROUP_COUNT"]))
    receipt_ids, receipt_exact_locs, receipt_unresolved_locs = extract_authority(text)
    tier = "Tier A" if "/tier_a/" in row["TEST_PATH"] else "Tier B"
    candidate_status = (
        "CURRENT_TIER_A_CANDIDATE"
        if row["FINAL_FILE_DISPOSITION"] == "ADMIT_TIER_A_CURRENT"
        else "SHADOW_TIER_B_CANDIDATE"
        if row["FINAL_FILE_DISPOSITION"] == "ADMIT_TIER_B_SHADOW"
        else "NOT_RETAINED_CURRENT"
    )
    candidate_rows.append(
        {
            "SEQUENCE": row["SEQUENCE"],
            "ALLOCATED_UNIT": row["ALLOCATED_UNIT"],
            "TIER": tier,
            "TEST_PATH": row["TEST_PATH"],
            "TEST_SHA256": sha256(test_path),
            "RECEIPT_PATH": row["RECEIPT_PATH"],
            "RECEIPT_SHA256": sha256(receipt_path),
            "ASSERTION_GROUP_COUNT": row["ASSERTION_GROUP_COUNT"],
            "RELATIONSHIP_COUNT": row["RELATIONSHIP_COUNT"],
            "FINAL_FILE_DISPOSITION": row["FINAL_FILE_DISPOSITION"],
            "AUTHORITY_CANDIDATE_STATUS": candidate_status,
            "STATUS_NOTE": row["STATUS_NOTE"],
        }
    )
    previous_ids: list[str] = []
    previous_locs: list[str] = []
    for group in groups:
        group_text = str(group["text"])
        relation, relation_status = extract_explicit_enum(group_text, "relation")
        strength, strength_status = extract_explicit_enum(group_text, "strength")
        ids, exact_locs, unresolved_locs = extract_authority(group_text)
        authority_mode = "EXPLICIT_EXACT" if exact_locs else ""
        if not exact_locs and re.search(r"\bsame (?:authority|locator|proposition)\b", group_text, re.I):
            if previous_locs:
                exact_locs = list(previous_locs)
                ids = sorted(set(ids) | set(previous_ids))
                authority_mode = "INHERITED_PREVIOUS_EXPLICIT_SAME_AUTHORITY"
        if not exact_locs:
            if receipt_exact_locs:
                authority_mode = "FILE_CONTEXT_ONLY"
            else:
                authority_mode = "UNRESOLVED"
        if exact_locs:
            previous_locs = list(exact_locs)
            previous_ids = list(ids)
        group_rows.append(
            {
                "SEQUENCE": row["SEQUENCE"],
                "ALLOCATED_UNIT": row["ALLOCATED_UNIT"],
                "TEST_PATH": row["TEST_PATH"],
                "GROUP_ORDINAL": str(group["ordinal"]),
                "RECEIPT_PATH": row["RECEIPT_PATH"],
                "RECEIPT_LINE_RANGE": f"{group['start_line']}-{group['end_line']}",
                "RECEIPT_PARSE_MODE": parse_mode,
                "GROUP_HEADING": str(group["heading"]),
                "GROUP_TEXT_SHA256": hashlib.sha256(group_text.encode("utf-8")).hexdigest(),
                "SEMANTIC_RELATION_EXPLICIT": relation,
                "SEMANTIC_RELATION_ENUM_STATUS": relation_status,
                "PROOF_STRENGTH_EXPLICIT": strength,
                "PROOF_STRENGTH_ENUM_STATUS": strength_status,
                "GROUP_DISPOSITION_PROJECTED": row["FINAL_FILE_DISPOSITION"],
                "AUTHORITY_IDS_EXPLICIT": json.dumps(ids, separators=(",", ":")),
                "AUTHORITY_LOCATORS_EXACT": json.dumps(exact_locs, separators=(",", ":")),
                "AUTHORITY_LOCATORS_UNRESOLVED_RAW": json.dumps(unresolved_locs, separators=(",", ":")),
                "AUTHORITY_RESOLUTION_MODE": authority_mode,
                "RECEIPT_AUTHORITY_IDS_ALL": json.dumps(receipt_ids, separators=(",", ":")),
                "RECEIPT_AUTHORITY_LOCATORS_ALL": json.dumps(receipt_exact_locs, separators=(",", ":")),
                "GROUP_TEXT_JSON": json.dumps(group_text, ensure_ascii=False),
            }
        )
    decision = file_decision_excerpt(text)
    proof_rows.append(
        {
            "SEQUENCE": row["SEQUENCE"],
            "TEST_PATH": row["TEST_PATH"],
            "FINAL_FILE_DISPOSITION": row["FINAL_FILE_DISPOSITION"],
            "ASSERTION_GROUP_COUNT": row["ASSERTION_GROUP_COUNT"],
            "RELATIONSHIP_COUNT": row["RELATIONSHIP_COUNT"],
            "RECEIPT_PATH": row["RECEIPT_PATH"],
            "FILE_DECISION_SHA256": hashlib.sha256(decision.encode("utf-8")).hexdigest(),
            "FILE_DECISION_JSON": json.dumps(decision, ensure_ascii=False),
        }
    )
    if row["FINAL_FILE_DISPOSITION"] not in {"ADMIT_TIER_A_CURRENT", "ADMIT_TIER_B_SHADOW"}:
        dependency_rows.append(
            {
                "SEQUENCE": row["SEQUENCE"],
                "TEST_PATH": row["TEST_PATH"],
                "FINAL_FILE_DISPOSITION": row["FINAL_FILE_DISPOSITION"],
                "RECEIPT_PATH": row["RECEIPT_PATH"],
                "DEFICIT_AND_RETURN_GATE_SHA256": hashlib.sha256(decision.encode("utf-8")).hexdigest(),
                "DEFICIT_AND_RETURN_GATE_JSON": json.dumps(decision, ensure_ascii=False),
            }
        )

write_tsv(
    UNIT / "P2_CURRENT_TEST_AUTHORITY_CANDIDATE_REGISTER.tsv",
    candidate_rows,
    list(candidate_rows[0]),
)
write_tsv(
    UNIT / "P2_ASSERTION_GROUP_PROPOSITION_TRACEABILITY_REGISTER.tsv",
    group_rows,
    list(group_rows[0]),
)
write_tsv(
    UNIT / "P2_PROOF_DISPOSITION_REGISTER.tsv",
    proof_rows,
    list(proof_rows[0]),
)
write_tsv(
    UNIT / "P2_DEPENDENCY_RETURN_GATE_REGISTER.tsv",
    dependency_rows,
    list(dependency_rows[0]),
)

summary = {
    "ledger_rows": len(ledger),
    "assertion_groups": len(group_rows),
    "dependency_rows": len(dependency_rows),
    "dispositions": {},
    "relation_enum_status": {},
    "strength_enum_status": {},
    "authority_resolution_mode": {},
}
for row in candidate_rows:
    summary["dispositions"][row["FINAL_FILE_DISPOSITION"]] = summary["dispositions"].get(row["FINAL_FILE_DISPOSITION"], 0) + 1
for row in group_rows:
    for key, field in [
        ("relation_enum_status", "SEMANTIC_RELATION_ENUM_STATUS"),
        ("strength_enum_status", "PROOF_STRENGTH_ENUM_STATUS"),
        ("authority_resolution_mode", "AUTHORITY_RESOLUTION_MODE"),
    ]:
        summary[key][row[field]] = summary[key].get(row[field], 0) + 1
(UNIT / "PM-019_PROJECTION_SUMMARY.json").write_text(
    json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
)
print(json.dumps(summary, indent=2, sort_keys=True))
