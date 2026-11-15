"""Pure-document D091 pre-admission consistency checks. No product imports or tests."""
from __future__ import annotations
import hashlib
import json
import subprocess
from decimal import Decimal
from pathlib import Path

THIS = Path(__file__).resolve()
REPO = THIS.parents[4]
BASE = "3ec136d149eb0e5b1d089f861998416361cd2088"
PREFIX = "handoff/m02_completion_28_execution/L04/D091_PRE_ADMISSION_20261115/"

def read(path: str) -> object:
    return json.loads((REPO / path).read_text(encoding="utf-8"))

def git(*args: str) -> str:
    return subprocess.check_output(("git", "-C", str(REPO), *args), text=True).strip()

def main() -> None:
    p = PREFIX
    manifest = read(p + "PACKET_MANIFEST.json")
    proposal = read(p + "PROPOSED_CASE_ADMISSION.json")
    runtime = read(p + "RUNTIME_OBSERVATION.json")
    orig = read("handoff/planning/m02_foundation_completion_20261030/PROOF_ALLOCATION_PROPOSED.json")
    ledger = read("handoff/m02_completion_28_execution/TEST_EVIDENCE_LEDGER.json")
    register = read("handoff/m02_completion_28_execution/EXECUTION_REGISTER.json")
    raw = read("handoff/m02_completion_28_execution/L01b/R112_SOURCE_CONTRACT_PROPOSED.json")
    oracle = read("handoff/m02_completion_28_execution/L01b/DOCUMENTARY_ORACLES.json")
    artifact_path = REPO / raw["delivery_artifact_binding"]["path"]
    artifact = read(raw["delivery_artifact_binding"]["path"])
    assert manifest["base_commit"] == proposal["baseline_main_commit"] == BASE
    assert manifest["base_tree"] == "791eeace5fc7ece326d75d24ca993c78d2893823"
    assert git("merge-base", "--is-ancestor", BASE, "HEAD") == ""
    assert len(register["leaves"]) == 39
    assert len(ledger["proof_obligations"]) == 35
    assert all(not x["test_allocation"]["authorised_case_count"] and not x["execution"]["runs"] for x in ledger["proof_obligations"])
    assert proposal["admitted_case_count"] == proposal["executed_case_count"] == 0
    assert proposal["execution_release"] == "NONE"
    alloc = next(x for x in orig["allocations"] if x["proof_id"] == "M02-C28-D091")
    assert alloc["proposed_case_count"] == proposal["proposed_case_count"] == 2
    assert alloc["proposed_hard_ceiling"] == proposal["original_hard_ceiling"] == 6
    for old, new in zip(alloc["cases"], proposal["cases"], strict=True):
        assert old["case_id"] == new["case_id"] and old["proof_path"] == new["proof_path"]
    assert len({x["proposed_node"] for x in proposal["cases"]}) == 2
    assert len(artifact["members"]) == 15 and len(oracle["positive_members"]) == 12
    assert len(oracle["refusal_members"]) == 3
    sha = hashlib.sha256(artifact_path.read_bytes()).hexdigest()
    assert sha == proposal["source_artifact_sha256"] == raw["delivery_artifact_binding"]["sha256"]
    for row in oracle["positive_members"]:
        delta = abs(Decimal(row["signed_delta"]))
        matches = [
            b["name"] for b in raw["rule_profile"]["bins"]
            if Decimal(b["min"]) <= delta and (delta < Decimal(b["max"]) or b["max_inclusive"] and delta == Decimal(b["max"]))
        ]
        assert matches == [row["expected_label"]]
    assert runtime["local_sqlite_version"] == "3.49.1"
    assert runtime["actual_python_version"] == "3.13.5"
    assert runtime["no_product_tests"] and runtime["no_system_change"]
    assert not (REPO / alloc["cases"][0]["proof_path"]).exists()
    assert set(manifest["files"]) == {x.name for x in THIS.parent.iterdir() if x.is_file()}
    changes = git("diff", "--name-only", BASE, "HEAD").splitlines()
    assert all(x.startswith(PREFIX) for x in changes), changes
    print(json.dumps({
        "status": "PRE_ADMISSION_PACKET_STATIC_CHECK_PASS",
        "approved_source": False, "admitted_cases": 0, "executed_cases": 0,
        "original_case_ids_preserved": 2, "published_changes_scoped": True,
        "note": "No product import, product runner or product test was invoked.",
    }, sort_keys=True))

if __name__ == "__main__":
    main()
