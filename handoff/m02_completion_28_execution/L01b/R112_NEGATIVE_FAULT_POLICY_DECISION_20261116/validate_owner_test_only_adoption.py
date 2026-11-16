"""Validate exact owner A–E test-only policy adoption record; no product code import/test."""
from pathlib import Path
from hashlib import sha256
import json
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
BASE = "230395c88d6724f7e1689ae47c5164d180096c34"
EXPECTED_GROUPS = {
 "A_L01B_MALFORMED_ORIGINAL_NEGATIVE_ONLY":15,
 "B_ALTERNATIVE_COHORT_EXCEPTION":2,
 "C_PAGINATED_READ_FAULT_PORT":2,
 "D_D091_ORIGINAL_GETTER_READONLY_FAULT_PORT":3,
 "E_SQLITE_FAILURE_SEAM":3,
}
def git(*args):
    return subprocess.check_output(["git", "-C", str(ROOT), *args], text=True).strip()
def load(path):
    return json.loads(path.read_text(encoding="utf-8"))
def digest(path):
    return sha256(path.read_bytes()).hexdigest()
def main():
    assert git("merge-base", "--is-ancestor", BASE, "HEAD") == ""
    proposed_path=HERE/"PROPOSED_NEGATIVE_SOURCE_AND_FAULT_POLICY.json"
    actual=load(HERE/"OWNER_TEST_ONLY_POLICY_ADOPTION_20261116.json")
    prior=load(proposed_path)
    assert actual["state"]=="OWNER_ADOPTED_TEST_ONLY_POLICY_NO_PRODUCT_RELEASE"
    assert actual["pinned_exact_request_candidate"]==BASE
    assert actual["reply_quoted_verbatim"]=="Yep, I approve."
    assert actual["question_quoted_verbatim"]=="Do you approve scopes A–E on PR #26 at the exact commit above, strictly as test-only policy permissions? The physical-case budgets and execution prerequisites would remain separate decisions."
    assert actual["target_pr"]==26
    assert actual["request_path_git_blob_sha1"]==git("rev-parse", BASE+":"+str(proposed_path.relative_to(ROOT)))
    assert prior["state"]=="OWNER_DECISION_REQUEST_ONLY_NOT_ADOPTED"
    assert set(actual["approved_scope_ids"])==set(EXPECTED_GROUPS)
    assert len(actual["approved_scope_ids"])==5
    assert len(actual["approved_test_only_groups"])==5
    assert sum(z["count"] for z in actual["approved_test_only_groups"].values())==25
    assert actual["approved_negative_specimens_total"]==25
    for k,v in EXPECTED_GROUPS.items():
        assert actual["approved_test_only_groups"][k]["count"]==v
        assert actual["approved_test_only_groups"][k]["status"]=="OWNER_ADOPTED_TEST_ONLY_POLICY"
        assert prior["proposed_policy_groups"][k]["count"]==v
        assert prior["proposed_policy_groups"][k]["owner_decision"]=="PENDING"
    f=actual["no_new_source_policy_needed_group"]
    assert f["scope"]=="F_ALREADY_FIXED_REQUEST_NEGATIVE_NO_NEW_SOURCE"
    assert f["specimens"]==2 and f["decision"]=="NOT_REQUESTED_OR_ADOPTED_AS_NEW_SOURCE_POLICY"
    assert prior["proposed_policy_groups"][f["scope"]]["owner_decision"]=="NOT_REQUESTED"
    assert len(prior["exact_specimens"])==27
    assert sum(x["decision_group"] in EXPECTED_GROUPS for x in prior["exact_specimens"])==25
    for row in prior["exact_specimens"]:
        assert digest(ROOT/row["path"])==row["sha256"]
    original=ROOT/"handoff/m02_completion_28_execution/L01b"
    assert digest(original/"R112_SOURCE_CONTRACT_PROPOSED.json")==actual["source_positive_contract_sha256"]==prior["original_owner_adopted_source_contract_sha256"]
    assert digest(original/"CONTROLLED_BATCH_INPUTS.json")==actual["source_positive_fifteen_member_sha256"]==prior["original_adopted_successful_cohort_sha256"]
    b24=ROOT/"handoff/m02_completion_28_execution/L04/D091_PROOF_ADMISSION_REVISION_20261116/EXACT_NEGATIVE_STIMULUS_BUNDLE.json"
    b3=ROOT/"handoff/m02_completion_28_execution/L04/D091_ORIGINAL_GETTER_FAULT_PREP_20261116/EXACT_GETTER_FAULT_BUNDLE.json"
    assert digest(b24)==actual["existing_24_negative_bundle_sha256"]==prior["existing_24_negative_bundle_sha256"]
    assert digest(b3)==actual["getter_three_negative_bundle_sha256"]==prior["getter_3_new_bundle_sha256"]
    assert actual["d091_proposed_cases_not_admitted"]==17
    assert actual["l01b_proposed_cases_not_admitted"]==15
    assert actual["d091_active_authorised_cases"]==actual["d091_active_hard_ceiling"]==actual["product_test_executions"]==0
    assert actual["policy_adoption_for_test_only_meaning"] and not actual["specific_test_case_authorisation"] and not actual["new_case_budget_approved"]
    assert not actual["specific_test_port_code_implemented"] and not actual["claim_or_generation_modified"]
    assert not actual["production_or_live_source_approved"] and actual["unchanged_source_positive_members"]
    assert not actual["pr_merge_authorised"] and actual["d145"]=="PAUSED"
    ledger=load(ROOT/"handoff/m02_completion_28_execution/TEST_EVIDENCE_LEDGER.json")
    d091=next(x for x in ledger["proof_obligations"] if x["proof_id"]=="M02-C28-D091")
    assert d091["test_allocation"]["authorised_case_count"]==d091["test_allocation"]["hard_ceiling"]==0
    assert d091["test_allocation"]["cases"]==[] and d091["execution"]["runs"]==[]
    paths=git("diff","--name-only",BASE,"HEAD").splitlines()+git("diff","--cached","--name-only").splitlines()+git("ls-files","--others","--exclude-standard").splitlines()
    allowed=str(HERE.relative_to(ROOT))+"/"
    assert paths and all(p.startswith(allowed) for p in paths),paths
    assert set(Path(p).name for p in paths).issubset({
      "OWNER_TEST_ONLY_POLICY_ADOPTION_20261116.md",
      "OWNER_TEST_ONLY_POLICY_ADOPTION_20261116.json",
      "INDEPENDENT_POLICY_ADOPTION_REVIEW_REQUEST.md",
      "validate_owner_test_only_adoption.py"
    })
    print(json.dumps({"result":"R112_OWNER_A_E_TEST_ONLY_POLICY_ADOPTION_STATIC_PASS",
       "approved_scopes":list(EXPECTED_GROUPS),"approved_test_only_specimens":25,
       "request_only_F_specimens":2,"reference_specimen_sha256_checked":27,
       "source_success_contract_preserved":True,"d091_admitted":0,"product_runs":0,
       "test_case_budget_released":False,"product_source_or_tests_changed":False},sort_keys=True))
if __name__=="__main__":
    main()
