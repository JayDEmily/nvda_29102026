from __future__ import annotations

import csv
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
UNIT = ROOT / "project_control/canonical_project_manager/units/PM-020"
RAW = UNIT / "raw_validation"
PM019 = ROOT / "project_control/canonical_project_manager/units/PM-019"
CENSUS = ROOT / "project_control/canonical_project_manager/units/PM-011/P2_PHYSICAL_TEST_CENSUS.tsv"
LEDGER = ROOT / "project_control/canonical_project_manager/P2_ABSOLUTE_SEMANTIC_READ_LEDGER.tsv"
ALLOWED_DISPOSITIONS = {
    "ADMIT_TIER_A_CURRENT",
    "ADMIT_TIER_B_SHADOW",
    "BLOCKED_P3_REPAIR",
    "BLOCKED_MISSING_NORMATIVE_AUTHORITY",
    "NON_AUTHORITATIVE_OBSERVATIONAL",
    "RETIREMENT_RECOMMENDED_NOT_EXECUTED",
}


def rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def rc(name: str) -> int:
    return int((RAW / f"{name}.exit_code").read_text().strip())


verified: list[str] = []
failed: list[str] = []
unknown: list[str] = []
blocked: list[str] = []

census = rows(CENSUS)
physical_a = sorted((ROOT / "tests/tier_a").rglob("test_*.py"))
physical_b = sorted((ROOT / "tests/tier_b").rglob("test_*.py"))
if (len(physical_a), len(physical_b), len(census)) == (166, 13, 179):
    verified.append("physical discovery reproduces 166 Tier A / 13 Tier B / 179 total files")
else:
    failed.append(f"physical discovery mismatch: {len(physical_a)}/{len(physical_b)}/{len(census)}")
hash_mismatch = []
for row in census:
    path = ROOT / row["test_path"]
    if not path.is_file() or sha(path) != row["baseline_sha256"]:
        hash_mismatch.append(row["test_path"])
if hash_mismatch:
    failed.append(f"PM-011 test-hash continuity failed for {len(hash_mismatch)} files")
else:
    verified.append("all 179 physical test SHA-256 values match PM-011")

ledger = rows(LEDGER)
missing_receipts = [r for r in ledger if not r["RECEIPT_PATH"] or not (ROOT / r["RECEIPT_PATH"]).is_file()]
if len(ledger) == 179 and all(r["SEMANTICALLY_READ"] == "YES" for r in ledger) and not missing_receipts:
    verified.append("ledger is 179 YES / 0 NO with one existing receipt per row")
else:
    failed.append(f"ledger/receipt completeness failed: rows={len(ledger)}, missing_receipts={len(missing_receipts)}")
if len({r["TEST_PATH"] for r in ledger}) != 179 or len({r["RECEIPT_PATH"] for r in ledger}) != 179:
    failed.append("ledger test/receipt paths are not one-to-one")
else:
    verified.append("ledger test paths and receipt paths are one-to-one")
if any(r["FINAL_FILE_DISPOSITION"] not in ALLOWED_DISPOSITIONS for r in ledger):
    failed.append("ledger contains a non-enumerated final file disposition")
else:
    verified.append("all 179 final file dispositions use the allowed enumeration")
if any(int(r["ASSERTION_GROUP_COUNT"]) != int(r["RELATIONSHIP_COUNT"]) for r in ledger):
    failed.append("one or more ledger rows have unequal assertion-group and relationship counts")
else:
    verified.append("all ledger rows have equal assertion-group and relationship counts")

pm019_rc = int((PM019 / "PM-019_VALIDATION.exit_code").read_text().strip())
pm019_text = (PM019 / "PM-019_VALIDATION.txt").read_text()
if "Structural validation does not establish semantic acceptance." not in pm019_text:
    failed.append("PM-019 validator omitted the mandatory structural-validation warning")
if pm019_rc == 0:
    verified.append("PM-019 integration validator passed")
else:
    failed.append("PM-019 integration validator failed; see PM-019_VALIDATION.txt")
    blocked.append("active retained-test/proof-block configuration projection was not authorised because PM-019 registers do not agree")

trace = rows(PM019 / "P2_ASSERTION_GROUP_PROPOSITION_TRACEABILITY_REGISTER.tsv")
relation_defects = sum(r["SEMANTIC_RELATION_ENUM_STATUS"] != "RESOLVED_ALLOWED_ENUM" for r in trace)
strength_defects = sum(r["PROOF_STRENGTH_ENUM_STATUS"] != "RESOLVED_ALLOWED_ENUM" for r in trace)
authority_defects = sum(
    r["GROUP_DISPOSITION_PROJECTED"].startswith("ADMIT_")
    and r["AUTHORITY_RESOLUTION_MODE"] not in {"EXPLICIT_EXACT", "INHERITED_PREVIOUS_EXPLICIT_SAME_AUTHORITY"}
    for r in trace
)
if relation_defects:
    failed.append(f"{relation_defects} assertion-group relation projections are unresolved or outside the allowed enum")
if strength_defects:
    failed.append(f"{strength_defects} assertion-group proof-strength projections are unresolved or outside the allowed enum")
if authority_defects:
    failed.append(f"{authority_defects} admitted assertion groups lack exact group-level authority-locator projection")

if rc("proof_blocks_check_all") == 0:
    verified.append("all 51 current proof blocks pass structural --check-all validation without command execution")
else:
    failed.append("proof-block --check-all validation failed")
if rc("git_diff_check") == 0:
    verified.append("git diff --check passed")
else:
    failed.append("git diff --check failed")
if rc("git_fsck") == 0:
    verified.append("git fsck --full completed without integrity error; dangling blobs are retained repository objects")
else:
    failed.append("git fsck --full reported an integrity error")

if rc("tier_b_complete") == 0 and "49 passed" in (RAW / "tier_b_complete.txt").read_text():
    verified.append("complete Tier B shadow route passed: 49 passed")
else:
    failed.append("complete Tier B shadow route did not pass")

tier_a = (RAW / "tier_a_complete.txt").read_text()
summary = re.search(r"(\d+) failed, (\d+) passed", tier_a)
if summary:
    fail_count, pass_count = map(int, summary.groups())
else:
    fail_count = pass_count = -1
if (fail_count, pass_count) == (61, 1097):
    failed.append("complete Tier A route is red: 61 failed, 1097 passed")
else:
    failed.append(f"complete Tier A result differs from parsed current count: failed={fail_count}, passed={pass_count}")
if not any(token in tier_a.lower() for token in (" skipped", " xfailed", " error during collection", "errors during collection")):
    verified.append("complete Tier A output contains no skip, xfail or collection-error summary")
else:
    failed.append("complete Tier A output contains a skip, xfail or collection error")

expected_red = (RAW / "expected_gate_c_red_nodes_from_seq160.txt").read_text().splitlines()
actual_red = (RAW / "actual_gate_c_red_nodes.txt").read_text().splitlines()
if expected_red == actual_red and len(actual_red) == 42:
    verified.append("all 42 frozen Gate C expected-red nodes correspond exactly to the sequence-160 obligation set")
else:
    failed.append(f"Gate C expected-red correspondence mismatch: expected={len(expected_red)}, actual={len(actual_red)}")
failed_nodes = (RAW / "tier_a_failed_nodes.txt").read_text().splitlines()
non_gate = [x for x in failed_nodes if "/normative_authority/test_gate_c_" not in x]
if len(non_gate) == 19:
    failed.append("19 additional Tier A failures remain outside the frozen Gate C expected-red set")
else:
    failed.append(f"unexpected non-Gate-C failure count is {len(non_gate)}, expected current observation 19")

mutation = (RAW / "protected_mutation_comparison.txt").read_text()
if "unauthorised_changes=0" in mutation and "protected_surface_changes=0" in mutation:
    verified.append("sequence-160 comparison finds no source, test, normative, configuration, fixture, script or proof-block mutation")
else:
    failed.append("protected-surface mutation comparison found an unauthorised change")

config_baseline = Path("/mnt/data/nvda_p2_seq160_compare/NVDA_P2_SEMANTIC_REVIEW_GROUP_SEQ121_160_20260723/repository/NVIDIA_2026/config")
if config_baseline.is_dir() and sha(ROOT / "config/retained_test_registry.yaml") == sha(config_baseline / "retained_test_registry.yaml") and sha(ROOT / "config/proof_blocks.yaml") == sha(config_baseline / "proof_blocks.yaml"):
    verified.append("active retained-test registry and proof-block configuration remain byte-identical to sequence 160")
else:
    failed.append("active registry/proof configuration changed despite failed PM-019 gate")

counts = {
    "physical_tier_a_files": len(physical_a),
    "physical_tier_b_files": len(physical_b),
    "physical_total_files": len(census),
    "ledger_yes": sum(r["SEMANTICALLY_READ"] == "YES" for r in ledger),
    "ledger_no": sum(r["SEMANTICALLY_READ"] == "NO" for r in ledger),
    "assertion_groups": sum(int(r["ASSERTION_GROUP_COUNT"]) for r in ledger),
    "tier_a_pytest_passed": pass_count,
    "tier_a_pytest_failed": fail_count,
    "gate_c_expected_red": len(actual_red),
    "additional_tier_a_failures": len(non_gate),
    "tier_b_pytest_passed": 49,
    "dispositions": dict(Counter(r["FINAL_FILE_DISPOSITION"] for r in ledger)),
}
(UNIT / "P2_CURRENT_COUNT_SET.json").write_text(json.dumps(counts, indent=2, sort_keys=True) + "\n")

print("PM-020 PRE-PACKAGE VALIDATION")
print("\nVerified")
for item in verified:
    print(f"- {item}")
print("\nFailed")
for item in failed:
    print(f"- {item}")
print("\nUnknown")
for item in unknown or ["None at pre-package stage"]:
    print(f"- {item}")
print("\nBlocked")
for item in blocked or ["None"]:
    print(f"- {item}")
print("\nCurrent count set")
print(json.dumps(counts, indent=2, sort_keys=True))
print(f"\nPre-package result: {'FAIL' if failed else 'PASS'}")
raise SystemExit(1 if failed else 0)
