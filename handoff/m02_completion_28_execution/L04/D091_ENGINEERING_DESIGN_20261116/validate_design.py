"""Static D091 engineering design packet verification; no NVIDIA product imports/tests."""
from __future__ import annotations

import hashlib
import json
import subprocess
from decimal import Decimal
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
BASE = "8c289ffcc2e373edf239eddfd5bbeabf1aae7e2d"
REVIEW = "37fab2c81e1ed98b227f75f600d3e0c12347d7d5"
SHA_SOURCE = "31c811e77468f44c2e412893326bc6d5f9ea037cdbf28712ce8e213652fdfc63"
SHA_BATCH = "1f4c46c5c247c78e3e18bb2de02c172f775379f664bad8e056ef6867a39d03dc"
SHA_ORACLE = "28bca489fc35faaef7b3a673e5c242b3463b125aa9038ee8d9c3a8c8192c5947"


def cmd(*args: str) -> str:
    return subprocess.check_output(["git", "-C", str(REPO), *args], text=True).strip()


def load(path: str) -> dict:
    return json.loads((REPO / path).read_text(encoding="utf-8"))


def check_sha(path: str, sha: str) -> None:
    assert hashlib.sha256((REPO / path).read_bytes()).hexdigest() == sha, path


def main() -> None:
    proof = load("handoff/m02_completion_28_execution/L04/D091_ENGINEERING_DESIGN_20261116/PROOF_COVERAGE_CANDIDATE.json")
    changed = load("handoff/m02_completion_28_execution/L04/D091_ENGINEERING_DESIGN_20261116/CHANGED_PATH_PROPOSAL.json")
    source = load("handoff/m02_completion_28_execution/L01b/R112_SOURCE_CONTRACT_PROPOSED.json")
    raw = load("handoff/m02_completion_28_execution/L01b/CONTROLLED_BATCH_INPUTS.json")
    oracle = load("handoff/m02_completion_28_execution/L01b/DOCUMENTARY_ORACLES.json")
    ledger = load("handoff/m02_completion_28_execution/TEST_EVIDENCE_LEDGER.json")
    register = load("handoff/m02_completion_28_execution/EXECUTION_REGISTER.json")
    adoption = load("handoff/m02_completion_28_execution/L01b/R112_OPERATIVE_DECISION_PREP_20261115/OWNER_SOURCE_ADOPTION_20261115.json")
    original = load("handoff/planning/m02_foundation_completion_20261030/PROOF_ALLOCATION_PROPOSED.json")
    original_d091 = next(x for x in original["allocations"] if x["proof_id"] == "M02-C28-D091")

    assert cmd("merge-base", "--is-ancestor", BASE, "HEAD") == ""
    assert cmd("cat-file", "-t", REVIEW) == "commit"
    assert changed["base_candidate"] == BASE and changed["independent_source_review"] == REVIEW
    assert proof["original_proposed_case_count"] == original_d091["proposed_case_count"] == 2
    assert proof["original_hard_ceiling"] == original_d091["proposed_hard_ceiling"] == 6
    assert proof["currently_admitted_case_count"] == proof["currently_executed_case_count"] == 0
    assert len(proof["physical_case_nodes"]) == 2
    assert [x["id"] for x in proof["physical_case_nodes"]] == [x["case_id"] for x in original_d091["cases"]]
    assert all(x["proposed_node"].endswith("::test_d091_controlled_" + ("success" if i == 0 else "reached_refusal")) for i, x in enumerate(proof["physical_case_nodes"]))
    assert all(x["status"] == "UNADMITTED_PROPOSAL" for x in proof["physical_case_nodes"])
    assert proof["tester"] == "NOT_DESIGNATED" and proof["runner"] == "NOT_PRODUCT_QUALIFIED"
    assert len(register["leaves"]) == 39 and len(ledger["proof_obligations"]) == 35
    assert all(x["test_allocation"]["authorised_case_count"] == 0 and not x["execution"]["runs"] for x in ledger["proof_obligations"])
    assert adoption["status"] == "OWNER_POLICY_ADOPTED_INDEPENDENT_OPERATIVE_CLEARANCE_PENDING"
    assert adoption["source_contract_sha256"] == SHA_SOURCE
    assert not adoption["d091_implementation_released"]
    assert source["profile_id"] == "T01-R112-CONTROLLED-FRACTION-1"
    assert source["selection"]["history_page_size"] == 8
    assert source["selection"]["maximum_projected_members"] == 64
    assert source["source_provider"] == "t01-controlled-option-delta"
    assert source["source_temporal_kind"] if "source_temporal_kind" in source else True
    assert proof["source_contract_sha256"] == changed.get("source_sha256", SHA_SOURCE) == SHA_SOURCE
    check_sha("handoff/m02_completion_28_execution/L01b/R112_SOURCE_CONTRACT_PROPOSED.json", SHA_SOURCE)
    check_sha("handoff/m02_completion_28_execution/L01b/CONTROLLED_BATCH_INPUTS.json", SHA_BATCH)
    check_sha("handoff/m02_completion_28_execution/L01b/DOCUMENTARY_ORACLES.json", SHA_ORACLE)
    assert proof["raw_batch_sha256"] == SHA_BATCH and proof["documentary_oracles_sha256"] == SHA_ORACLE
    assert len(raw["members"]) == 15 and len(oracle["positive_members"]) == 12
    assert len(oracle["refusal_members"]) == 3
    assert len({x["observation"]["observation_occurrence_id"] for x in raw["members"]}) == 15
    labels = {x["name"] for x in source["rule_profile"]["bins"]}
    assert labels == {"ABS_00_10", "ABS_10_25", "ABS_25_50", "ABS_50_75", "ABS_75_100"}
    for row in oracle["positive_members"]:
        x = abs(Decimal(row["signed_delta"]))
        matches = [b["name"] for b in source["rule_profile"]["bins"] if Decimal(b["min"]) <= x and (x < Decimal(b["max"]) or b["max_inclusive"] and x == Decimal(b["max"]))]
        assert matches == [row["expected_label"]], row
    assert changed["no_product_implementation"] and changed["no_product_cases"]
    assert all(x["operation"] != "MODIFY_NOW" for x in changed["paths"])
    rel = HERE.relative_to(REPO).as_posix() + "/"
    names = cmd("diff", "--name-only", BASE, "HEAD").splitlines()
    names += cmd("diff", "--cached", "--name-only").splitlines()
    names += cmd("ls-files", "--others", "--exclude-standard").splitlines()
    assert names and all(x.startswith(rel) for x in names), names
    print(json.dumps({
        "result": "D091_ENGINEERING_DESIGN_STATIC_CHECK_PASS",
        "base": BASE, "source_contract_sha256": SHA_SOURCE,
        "review_commit_available": REVIEW, "source_members": 15,
        "positive_documentary_oracles": 12, "physical_cases_proposed": 2,
        "active_product_cases_admitted": 0, "executed_product_cases": 0,
        "coverage_unmapped": sum(x["status"].startswith("UNMAPPED") for x in proof["coverage"]),
        "source_code_changed": False, "product_tests_executed": False,
        "change_scope": rel
    }, sort_keys=True))


if __name__ == "__main__":
    main()
