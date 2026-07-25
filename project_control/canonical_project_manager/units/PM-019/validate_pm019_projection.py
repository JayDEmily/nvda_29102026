from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
UNIT = ROOT / "project_control/canonical_project_manager/units/PM-019"
PHRASE = "Structural validation does not establish semantic acceptance."


def read(name: str) -> list[dict[str, str]]:
    with (UNIT / name).open("r", encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


candidate = read("P2_CURRENT_TEST_AUTHORITY_CANDIDATE_REGISTER.tsv")
groups = read("P2_ASSERTION_GROUP_PROPOSITION_TRACEABILITY_REGISTER.tsv")
proof = read("P2_PROOF_DISPOSITION_REGISTER.tsv")
deps = read("P2_DEPENDENCY_RETURN_GATE_REGISTER.tsv")
failures: list[str] = []
passes: list[str] = []

if len(candidate) == 179 and len({r['TEST_PATH'] for r in candidate}) == 179 and len({r['SEQUENCE'] for r in candidate}) == 179:
    passes.append("179 physical tests occur exactly once in the authority candidate register")
else:
    failures.append("authority candidate register is not a one-to-one 179-file projection")

expected_groups = sum(int(r["ASSERTION_GROUP_COUNT"]) for r in candidate)
if len(groups) == expected_groups == 777:
    passes.append("all 777 receipt-declared assertion groups occur once in the traceability register")
else:
    failures.append(f"assertion-group projection mismatch: expected {expected_groups}, found {len(groups)}")

by_file = Counter(r["TEST_PATH"] for r in groups)
for row in candidate:
    if by_file[row["TEST_PATH"]] != int(row["ASSERTION_GROUP_COUNT"]):
        failures.append(f"group-count mismatch for {row['TEST_PATH']}")

bad_relation = [r for r in groups if r["SEMANTIC_RELATION_ENUM_STATUS"] != "RESOLVED_ALLOWED_ENUM"]
bad_strength = [r for r in groups if r["PROOF_STRENGTH_ENUM_STATUS"] != "RESOLVED_ALLOWED_ENUM"]
if bad_relation:
    failures.append(f"{len(bad_relation)} assertion groups do not project one allowed semantic-relation enum")
else:
    passes.append("every assertion group projects one allowed semantic-relation enum")
if bad_strength:
    failures.append(f"{len(bad_strength)} assertion groups do not project one allowed proof-strength enum")
else:
    passes.append("every assertion group projects one allowed proof-strength enum")

admitted = [r for r in groups if r["GROUP_DISPOSITION_PROJECTED"].startswith("ADMIT_")]
unresolved_authority = [
    r for r in admitted
    if r["AUTHORITY_RESOLUTION_MODE"] not in {
        "EXPLICIT_EXACT",
        "INHERITED_PREVIOUS_EXPLICIT_SAME_AUTHORITY",
    }
]
if unresolved_authority:
    failures.append(
        f"{len(unresolved_authority)} admitted assertion-group relationships lack an exact group-level authority locator projection"
    )
else:
    passes.append("every admitted assertion-group relationship resolves to an exact authority locator")

expected_deps = [r for r in candidate if not r["FINAL_FILE_DISPOSITION"].startswith("ADMIT_")]
if len(deps) == len(expected_deps) == 143:
    passes.append("all 143 non-admitted files occur once in the dependency/return-gate register")
else:
    failures.append(f"dependency register count mismatch: expected {len(expected_deps)}, found {len(deps)}")

missing_gate = []
for row in deps:
    decision = json.loads(row["DEFICIT_AND_RETURN_GATE_JSON"])
    if not any(token in decision.lower() for token in ("return gate", "p3", "replace", "supplement", "retire", "missing", "authority")):
        missing_gate.append(row)
if missing_gate:
    failures.append(f"{len(missing_gate)} blocked/observational/retirement files lack a mechanically detectable deficit or return-gate statement")
else:
    passes.append("every non-admitted file retains an explicit deficit or return-gate statement")

candidate_status_mismatch = [
    r for r in candidate
    if (r["AUTHORITY_CANDIDATE_STATUS"] != "NOT_RETAINED_CURRENT")
    != r["FINAL_FILE_DISPOSITION"].startswith("ADMIT_")
]
if candidate_status_mismatch:
    failures.append("one or more rejected relationships were restored through candidate-status projection")
else:
    passes.append("no rejected file disposition is restored through a generic candidate substitute")

if len(proof) == 179 and {r["TEST_PATH"] for r in proof} == {r["TEST_PATH"] for r in candidate}:
    passes.append("proof disposition register covers the same 179-file population")
else:
    failures.append("proof disposition register does not match the 179-file population")

print("PM-019 STRUCTURAL VALIDATION")
print(PHRASE)
print("\nPASS")
for item in passes:
    print(f"- {item}")
print("\nFAIL")
for item in failures:
    print(f"- {item}")
print("\nCOUNTS")
print(f"- files: {len(candidate)}")
print(f"- assertion groups: {len(groups)}")
print(f"- admitted assertion groups: {len(admitted)}")
print(f"- relation enum defects: {len(bad_relation)}")
print(f"- strength enum defects: {len(bad_strength)}")
print(f"- admitted groups without exact group-level authority locator: {len(unresolved_authority)}")
print(f"- dependency/return-gate rows: {len(deps)}")
print(f"- final result: {'FAIL' if failures else 'PASS'}")
print(PHRASE)
raise SystemExit(1 if failures else 0)
