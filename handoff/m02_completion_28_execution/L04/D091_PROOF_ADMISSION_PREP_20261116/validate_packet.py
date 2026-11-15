"""Read-only documentary consistency check for a proposed D091 test admission.
No NVIDIA product code import, test collection, subprocess pytest, or product run.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
from decimal import Decimal
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
BASE = "07f8140fd9306e51b05f241b02341a2b14579bc2"
REVIEW = "05f6b4b707c6231dc9b4d54a4a6cb626711808de"
SOURCE_PATH = "handoff/m02_completion_28_execution/L01b/R112_SOURCE_CONTRACT_PROPOSED.json"
BATCH_PATH = "handoff/m02_completion_28_execution/L01b/CONTROLLED_BATCH_INPUTS.json"
ORACLE_PATH = "handoff/m02_completion_28_execution/L01b/DOCUMENTARY_ORACLES.json"
SOURCE_SHA = "31c811e77468f44c2e412893326bc6d5f9ea037cdbf28712ce8e213652fdfc63"
BATCH_SHA = "1f4c46c5c247c78e3e18bb2de02c172f775379f664bad8e056ef6867a39d03dc"
ORACLE_SHA = "28bca489fc35faaef7b3a673e5c242b3463b125aa9038ee8d9c3a8c8192c5947"


def git(*args: str) -> str:
    return subprocess.check_output(["git", "-C", str(REPO), *args], text=True).strip()


def load(path: Path | str) -> dict:
    target = path if isinstance(path, Path) else REPO / path
    return json.loads(target.read_text(encoding="utf-8"))


def check_sha(path: str, expected: str) -> None:
    assert hashlib.sha256((REPO / path).read_bytes()).hexdigest() == expected, path


def main() -> None:
    assert git("merge-base", "--is-ancestor", BASE, "HEAD") == ""
    assert git("cat-file", "-t", REVIEW) == "commit"
    check_sha(SOURCE_PATH, SOURCE_SHA)
    check_sha(BATCH_PATH, BATCH_SHA)
    check_sha(ORACLE_PATH, ORACLE_SHA)
    s = load(SOURCE_PATH)
    r = load(BATCH_PATH)
    o = load(ORACLE_PATH)
    m = load(HERE / "FINITE_CASE_AND_WITNESS_MATRIX.json")
    x = load(HERE / "ORIGINAL_SOURCE_AND_ORACLE_BINDINGS.json")
    e = load(HERE / "RUNTIME_METADATA_OBSERVATION.json")
    old = load("handoff/planning/m02_foundation_completion_20261030/PROOF_ALLOCATION_PROPOSED.json")
    active = load("handoff/m02_completion_28_execution/TEST_EVIDENCE_LEDGER.json")
    register = load("handoff/m02_completion_28_execution/EXECUTION_REGISTER.json")

    original = next(z for z in old["allocations"] if z["proof_id"] == "M02-C28-D091")
    active_entry = next(z for z in active["proof_obligations"] if z["proof_id"] == "M02-C28-D091")
    assert original["proposed_case_count"] == 2 and original["proposed_hard_ceiling"] == 6
    assert len(original["cases"]) == 2
    assert m["original_physical_case_count"] == 2
    assert m["proposed_additional_physical_cases"] == 4
    assert m["proposed_total_physical_cases"] == m["historical_prospective_ceiling"] == 6
    assert len(m["physical_case_nodes"]) == 6
    assert m["actual_product_cases_admitted"] == m["actual_product_cases_executed"] == 0
    assert m["missing_owner_approval"] is True
    assert active_entry["test_allocation"]["authorised_case_count"] == 0
    assert active_entry["test_allocation"]["hard_ceiling"] == 0
    assert active_entry["test_allocation"]["cases"] == []
    assert active_entry["execution"]["runs"] == []
    assert len(active["proof_obligations"]) == 35 and len(register["leaves"]) == 39
    ids = [z["case_id"] for z in m["physical_case_nodes"]]
    assert len(ids) == len(set(ids))
    assert ids[:2] == [z["case_id"] for z in original["cases"]]
    assert all(z["kind"] == "ORIGINAL_PROPOSED" for z in m["physical_case_nodes"][:2])
    assert all(z["kind"] == "ADDITIONAL_REQUIRES_OWNER_APPROVAL" for z in m["physical_case_nodes"][2:])
    assert all(z["status"] == "PROPOSED_UNADMITTED" for z in m["physical_case_nodes"])
    assert len({z["node"] for z in m["physical_case_nodes"]}) == 6
    assert all(z["node"].startswith("tests/product/m02_completion_28/d091/test_signal.py::test_d091_controlled_") for z in m["physical_case_nodes"])
    witnesses = [w for z in m["physical_case_nodes"] for w in z["witness_ids"]]
    assert len(witnesses) == len(set(witnesses))
    evidence = m["evidence_units"]
    assert len(evidence) == 7 and len({z["id"] for z in evidence}) == 7
    assert {w for row in evidence for w in row["witnesses"]} == set(witnesses)
    assert all(set(row["node_ids"]) <= set(ids) for row in evidence)
    assert len(o["positive_members"]) == 12 and len(o["refusal_members"]) == 3
    assert len(r["members"]) == 15 and len(x["members"]) == 15
    assert len({z["observation"]["observation_occurrence_id"] for z in r["members"]}) == 15
    assert {z["source_member_id"] for z in x["members"]} == {z["member_id"] for z in r["members"]}
    assert all(z["receipt_utc"] == z["as_of_utc"] for z in x["members"])
    source = {z["member_id"]: z for z in r["members"]}
    for item in o["positive_members"]:
        specimen = source[item["witness"]]["observation"]["native_record"]["model"]["delta"]
        assert specimen["native_type"] == "Decimal" and specimen["text"] == item["signed_delta"]
        z = abs(Decimal(item["signed_delta"]))
        matches = [
            b["name"] for b in s["rule_profile"]["bins"]
            if Decimal(b["min"]) <= z
            and (z < Decimal(b["max"]) or (b["max_inclusive"] and z == Decimal(b["max"])))
        ]
        assert matches == [item["expected_label"]], item
        bound = next(v for v in x["members"] if v["source_member_id"] == item["witness"])
        assert bound["oracle_expected_category"] == item["expected_label"]
    assert s["selection"]["history_page_size"] == 8
    assert s["selection"]["maximum_projected_members"] == 64
    assert s["selection"]["temporal_kind"] == "receipt_only"
    assert m["raw_source_contract_sha256"] == SOURCE_SHA
    assert m["source_fixture_sha256"] == BATCH_SHA and m["documentary_oracles_sha256"] == ORACLE_SHA
    assert e["python"] == "3.13.5" and e["sqlite_version"] == "3.49.1"
    assert e["repo_head"] == BASE and e["product_proofs_executed"] == 0
    assert not e["d091_source_imported"] and not e["full_receiver_qualification"]
    changed = git("diff", "--name-only", BASE, "HEAD").splitlines()
    changed += git("diff", "--cached", "--name-only").splitlines()
    changed += git("ls-files", "--others", "--exclude-standard").splitlines()
    relative = HERE.relative_to(REPO).as_posix() + "/"
    assert changed and all(v.startswith(relative) for v in changed), changed
    print(json.dumps({
        "status": "D091_PROOF_ADMISSION_PREPARATION_STATIC_PASS",
        "base": BASE,
        "source_sha256": SOURCE_SHA,
        "original_cases": 2, "new_cases_proposed_not_approved": 4,
        "total_cases_proposed_not_approved": 6,
        "declared_distinct_witnesses": len(witnesses),
        "positive_source_oracles_checked": 12,
        "original_raw_members": 15, "unapproved_negative_fixture_classes": 2,
        "active_case_count": 0, "product_tests_executed": 0,
        "change_scope": relative, "not_product_qualification": True
    }, sort_keys=True))


if __name__ == "__main__":
    main()
