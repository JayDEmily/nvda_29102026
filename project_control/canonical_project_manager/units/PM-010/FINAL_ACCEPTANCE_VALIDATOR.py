from __future__ import annotations

import csv
import hashlib
import json
import re
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
CONTROL_ROOT = ROOT / "project_control/canonical_project_manager"
UNIT_ROOT = CONTROL_ROOT / "units"
BRIEF_ROOT = CONTROL_ROOT / "WORKER_BRIEFS"
sys.path.insert(0, str(ROOT / "src"))

import nvda_desk.vocabulary_synonym_audit as audit
from nvda_desk.schemas.vocabulary import vocabulary_document_from_dict
from nvda_desk.vocabulary_builder import build_canonical_payload, read_registry_admission_records

REGISTERS = {
    "PM-003": UNIT_ROOT / "PM-003/ARCHITECTURE_MIGRATION_CONTROL_ADJUDICATION_REGISTER.tsv",
    "PM-004": UNIT_ROOT / "PM-004/COEFFICIENT_MODIFIER_EVALUATION_ADJUDICATION_REGISTER.tsv",
    "PM-005": UNIT_ROOT / "PM-005/CALENDAR_TEMPORAL_PROVENANCE_ADJUDICATION_REGISTER.tsv",
    "PM-006": UNIT_ROOT / "PM-006/DMP_PROTOCOL_IDENTITY_LINEAGE_ADJUDICATION_REGISTER.tsv",
    "PM-007": UNIT_ROOT / "PM-007/STAGE_INGRESS_SERIAL_CAPITAL_ADJUDICATION_REGISTER.tsv",
    "PM-008": UNIT_ROOT / "PM-008/OPENING_POSITION_EXIT_CLOSE_ADJUDICATION_REGISTER.tsv",
    "PM-009": UNIT_ROOT / "PM-009/PARALLEL_RISK_REVIEW_PLAYBOOK_ADJUDICATION_REGISTER.tsv",
}
BRIEFS = {
    "PM-003": BRIEF_ROOT / "PM-003_ARCHITECTURE_MIGRATION_CONTROL_TERMS.md",
    "PM-004": BRIEF_ROOT / "PM-004_COEFFICIENT_MODIFIER_EVALUATION_TERMS.md",
    "PM-005": BRIEF_ROOT / "PM-005_CALENDAR_TEMPORAL_PROVENANCE_TERMS.md",
    "PM-006": BRIEF_ROOT / "PM-006_DMP_PROTOCOL_IDENTITY_LINEAGE_TERMS.md",
    "PM-007": BRIEF_ROOT / "PM-007_STAGE_INGRESS_SERIAL_CAPITAL_TERMS.md",
    "PM-008": BRIEF_ROOT / "PM-008_OPENING_POSITION_EXIT_CLOSE_TERMS.md",
    "PM-009": BRIEF_ROOT / "PM-009_PARALLEL_RISK_REVIEW_PLAYBOOK_TERMS.md",
}
FIXED_LIST_HEADINGS = {
    "Human headings:",
    "Generated entries:",
    "Working-overlay admissions:",
    "Human headings and matching generated entries:",
}


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fixed_labels_from_brief(path: Path) -> list[str]:
    """Parse only the named fixed-list paragraphs, excluding explanatory prose."""
    text = path.read_text(encoding="utf-8")
    try:
        fixed = text.split("## Fixed concept set", 1)[1].split("\n## ", 1)[0]
    except IndexError as exc:
        raise AssertionError(f"missing fixed concept set in {path}") from exc
    lines = fixed.splitlines()
    labels: list[str] = []
    for index, line in enumerate(lines):
        if line.strip() not in FIXED_LIST_HEADINGS:
            continue
        cursor = index + 1
        while cursor < len(lines) and not lines[cursor].strip():
            cursor += 1
        paragraph: list[str] = []
        while cursor < len(lines) and lines[cursor].strip():
            paragraph.append(lines[cursor])
            cursor += 1
        extracted = re.findall(r"`([^`]+)`", " ".join(paragraph))
        assert extracted, f"empty fixed-label paragraph after {line!r} in {path}"
        for label in extracted:
            if label not in labels:
                labels.append(label)
    assert labels, f"no fixed labels parsed from {path}"
    return labels


def main() -> int:
    rows_by_unit = {unit: read_tsv(path) for unit, path in REGISTERS.items()}

    # The validator derives exact fixed-label coverage from the governing briefs.
    fixed_counts: dict[str, int] = {}
    for unit, brief in BRIEFS.items():
        expected = fixed_labels_from_brief(brief)
        assigned = [row["assigned_exact_label"] for row in rows_by_unit[unit]]
        duplicates = [label for label, count in Counter(assigned).items() if count != 1]
        assert not duplicates, f"{unit} duplicate assigned_exact_label values: {duplicates}"
        missing_or_replaced = [label for label in expected if assigned.count(label) != 1]
        assert not missing_or_replaced, (
            f"{unit} fixed labels missing or silently replaced: {missing_or_replaced}"
        )
        fixed_counts[unit] = len(expected)

    decisions = [(unit, row) for unit, rows in rows_by_unit.items() for row in rows]
    assert len(decisions) == 129, f"semantic decision count changed: {len(decisions)}"

    roles = Counter()
    expected_refs: set[str] = set()
    for unit, row in decisions:
        disposition = row["semantic_disposition"].casefold()
        if disposition in {"quarantine", "reject", "retire", "retired"} or not row["canonical_slug"]:
            roles["quarantined"] += 1
        elif disposition == "alias" or row["candidate_action"] == "alias_only":
            roles["alias_only"] += 1
            expected_refs.add(f"{unit}:{row['concept_id']}")
        else:
            roles["canonical"] += 1
            expected_refs.add(f"{unit}:{row['concept_id']}")
    assert roles == Counter({"canonical": 117, "quarantined": 9, "alias_only": 3}), roles

    corrected = {(unit, row["concept_id"]): row for unit, row in decisions}
    for key in [
        ("PM-004", "CME-003"), ("PM-004", "CME-004"),
        *[("PM-005", f"CTP-{index:03d}") for index in range(24, 29)],
        ("PM-009", "PRP-003"), ("PM-009", "PRP-004"),
    ]:
        assert corrected[key]["semantic_disposition"] == "quarantine", key
        assert corrected[key]["canonical_slug"] == "", key
    for key in [("PM-009", "PRP-002"), ("PM-009", "PRP-007")]:
        assert corrected[key]["semantic_disposition"] in {"admit_new", "enrich", "retain"}, key
        assert corrected[key]["source_locator"].startswith("docs/"), key

    serial_alias = corrected[("PM-007", "SSC-010")]
    serial_spine = corrected[("PM-007", "SSC-015")]
    assert serial_alias["assigned_exact_label"] == "Serial Desk-cognition"
    assert serial_alias["semantic_disposition"] == "alias"
    assert serial_alias["candidate_action"] == "alias_only"
    assert serial_alias["canonical_slug"] == "serial_desk_cognition_spine"
    assert serial_spine["assigned_exact_label"] == "Serial Desk-cognition Spine"
    assert serial_spine["semantic_disposition"] in {"admit_new", "enrich", "retain"}
    assert serial_spine["canonical_slug"] == "serial_desk_cognition_spine"

    downstream = corrected[("PM-008", "OPC-010")]
    assert downstream["canonical_slug"] == "downstream_state_reader_layer"
    assert downstream["source_locator"].startswith(
        "docs/07_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_CORE.md:183-195"
    )

    pm008_norm = read_tsv(UNIT_ROOT / "PM-008/NORMATIVE_CANDIDATE_RE_ADJUDICATION_REGISTER.tsv")
    pm009_norm = read_tsv(UNIT_ROOT / "PM-009/NORMATIVE_CANDIDATE_RE_ADJUDICATION_REGISTER.tsv")
    assert len(pm008_norm) == 1
    assert pm008_norm[0]["owning_p1_unit"] == "PM-008"
    assert pm008_norm[0]["owning_concept_id"] == "OPC-010"
    assert pm008_norm[0]["path"] == "docs/07_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_CORE.md"
    assert pm008_norm[0]["line"] == "195"
    assert not [row for row in pm009_norm if row["normative_occurrence_id"] == "PM-009-NORM-005"]
    assert not [row for row in pm009_norm if row["path"] == pm008_norm[0]["path"] and row["line"] == "195"]

    schema, version, notes, records = read_registry_admission_records()
    assert schema == "v1"
    assert version == "2026-07-21-p1-corrected-v4"
    assert len(records) == 117
    projected_refs = [ref for record in records for ref in record.semantic_decision_refs]
    assert set(projected_refs) == expected_refs
    assert len(projected_refs) == len(set(projected_refs)) == 120

    record_by_slug = {record.projection["canonical_slug"]: record for record in records}
    spine_record = record_by_slug["serial_desk_cognition_spine"]
    assert spine_record.heading == "Serial Desk-cognition Spine"
    assert "Serial Desk-cognition" in spine_record.projection["allowed_aliases"]
    assert set(spine_record.semantic_decision_refs) == {"PM-007:SSC-010", "PM-007:SSC-015"}
    assert "stage_read_state" not in record_by_slug
    assert "downstream_state_reader_layer" in record_by_slug

    payload = build_canonical_payload()
    vocabulary_document_from_dict(payload)
    tracked_payload = json.loads((ROOT / "data/vocabulary/canonical_vocabulary.json").read_text(encoding="utf-8"))
    assert payload == tracked_payload
    assert len(payload["entries"]) == 117
    slugs = {entry["canonical_slug"] for entry in payload["entries"]}
    for absent in [
        "mutable_runtime_surface", "baseline_only_surface", "temporal_conformance_inventory",
        "already_conformant", "needs_proof_test_remediation_only",
        "needs_code_persistence_remediation_in_tranche_3", "reserved_blocked", "candidate_audit",
        "stage_read_state",
    ]:
        assert absent not in slugs
    assert {
        "financial_calendar_architecture", "capital_deployment_authority",
        "serial_desk_cognition_spine", "downstream_state_reader_layer",
    } <= slugs

    integrated = read_tsv(UNIT_ROOT / "PM-010/P1_INTEGRATED_SEMANTIC_REGISTER.tsv")
    trace = read_tsv(UNIT_ROOT / "PM-010/P1_PROJECTION_TRACEABILITY.tsv")
    assert len(integrated) == 129
    assert Counter(row["projection_role"] for row in integrated) == Counter(
        {"canonical_record": 117, "quarantined_no_projection": 9, "alias_only": 3}
    )
    integrated_keys = {(row["source_unit"], row["source_concept_id"]) for row in integrated}
    assert integrated_keys == set(corrected)
    assert len(trace) == 117
    assert [row["canonical_slug"] for row in trace] == [entry["canonical_slug"] for entry in payload["entries"]]
    for row, entry in zip(trace, payload["entries"], strict=True):
        assert row["json_entry_sha256"] == hashlib.sha256(
            json.dumps(entry, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
        ).hexdigest()

    dispositions = read_tsv(UNIT_ROOT / "PM-010/P1_CANDIDATE_SEMANTIC_DISPOSITION_REGISTER.tsv")
    assert len(dispositions) == 499
    key = lambda row: (
        row["path"], int(row["line"]), int(row["column"]), row["phrase"], row["context_sha256"]
    )
    assert len({key(row) for row in dispositions}) == 499
    normative = [row for row in dispositions if row["source_class"] == "governing_normative_document"]
    assert len(normative) == 59
    assert all(row["p2_route"] == "none_normative_resolved_in_P1" for row in normative)
    assert all(row["normative_re_adjudication_ref"] != "none" for row in normative)
    assert all(row["audit_resolution_effect"] == "suppress_same_occurrence_only" for row in dispositions)

    original_register = audit.RESOLVED_OCCURRENCES_PATH
    try:
        audit.RESOLVED_OCCURRENCES_PATH = Path("/tmp/does_not_exist_p1_occurrence_register.tsv")
        fresh_unresolved = audit.build_report()["candidates"]
    finally:
        audit.RESOLVED_OCCURRENCES_PATH = original_register
    assert len(fresh_unresolved) == 499
    assert {key(row) for row in fresh_unresolved} == {key(row) for row in dispositions}

    final_report = audit.build_report()
    assert final_report["schema_version"] == "v2_occurrence_scoped"
    assert final_report["candidates"] == []
    assert final_report["resolved_occurrence_count"] == 499
    tracked_report = json.loads((ROOT / "var/vocabulary/synonym_candidates.json").read_text(encoding="utf-8"))
    assert tracked_report == final_report
    stamp = json.loads((ROOT / "data/vocabulary/vocabulary_touch_stamp.json").read_text(encoding="utf-8"))
    assert stamp["fingerprint"] == final_report["fingerprint"]
    assert final_report["vocabulary_touched"] is False

    source = (ROOT / "src/nvda_desk/vocabulary_synonym_audit.py").read_text(encoding="utf-8")
    lexicon_body = source.split("def _lexicon", 1)[1].split("def _looks_like_bounded_label", 1)[0]
    assert "disallowed_phrases" not in lexicon_body
    assert "audit_noncanonical_phrases" not in lexicon_body
    occurrence_key_body = source.split("def _resolved_occurrence_keys", 1)[1].split("def build_report", 1)[0]
    assert '"line"' in occurrence_key_body and '"column"' in occurrence_key_body

    with tempfile.TemporaryDirectory(prefix="p1_builder_") as temp:
        p1 = Path(temp) / "one.json"
        p2 = Path(temp) / "two.json"
        rendered = json.dumps(payload, indent=2, ensure_ascii=False) + "\n"
        p1.write_text(rendered, encoding="utf-8")
        p2.write_text(json.dumps(build_canonical_payload(), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        assert p1.read_bytes() == p2.read_bytes() == (ROOT / "data/vocabulary/canonical_vocabulary.json").read_bytes()

    locator_result = subprocess.run(
        [sys.executable, str(UNIT_ROOT / "PM-010/VALIDATE_SOURCE_LOCATORS.py")],
        cwd=ROOT, check=True, capture_output=True, text=True,
    )
    assert "source_locator_validation=PASS" in locator_result.stdout

    changed = subprocess.run(
        ["git", "diff", "--name-only", "HEAD"], cwd=ROOT, check=True, capture_output=True, text=True
    ).stdout.splitlines()
    forbidden_prefixes = ("tests/", "config/")
    forbidden_exact = {
        "AGENTS.md", "PLANS.md", "ROADMAP_LEDGER.md", "ROADMAP_LEDGER_V2.md",
        "project_control/canonical_project_manager/EXEC_PLAN.md",
    }
    assert not [path for path in changed if path.startswith(forbidden_prefixes) or path in forbidden_exact]
    source_changes = [path for path in changed if path.startswith("src/")]
    assert source_changes == [
        "src/nvda_desk/vocabulary_builder.py", "src/nvda_desk/vocabulary_synonym_audit.py"
    ]
    subprocess.run(["git", "diff", "--check"], cwd=ROOT, check=True)

    print("p1_reopened_validation=PASS")
    print("project_manager_acceptance=PENDING")
    print("p2_status=NOT_BEGUN")
    print(f"semantic_decisions={len(decisions)}")
    print(f"canonical_records={len(records)}")
    print(f"alias_only_decisions={roles['alias_only']}")
    print(f"quarantined_decisions={roles['quarantined']}")
    print("fixed_label_coverage=" + ",".join(f"{unit}:{fixed_counts[unit]}" for unit in sorted(fixed_counts)))
    print(f"candidate_occurrences_dispositioned={len(dispositions)}")
    print(f"governing_normative_occurrences_in_integrated_audit={len(normative)}")
    print(f"audit_unresolved_candidates={len(final_report['candidates'])}")
    print(f"generated_json_sha256={sha(ROOT / 'data/vocabulary/canonical_vocabulary.json')}")
    print(f"audit_fingerprint={final_report['fingerprint']}")
    print(f"tracked_changed_paths={len(changed)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
