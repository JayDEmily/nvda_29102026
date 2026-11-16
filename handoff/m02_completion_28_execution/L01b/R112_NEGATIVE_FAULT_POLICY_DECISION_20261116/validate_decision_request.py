"""Static verification of an owner decision *request*, not adoption, case admission or product runtime."""
from __future__ import annotations
from pathlib import Path
from hashlib import sha256
import json
import subprocess

HERE=Path(__file__).resolve().parent
R=HERE.parents[3]
BASE="e52318c0ea399e5e585aef985803950f0e793d3a"
REVIEW="14127e0e444781b1868eb51dc74b37eaf9efc327"
SOURCE="1f4c46c5c247c78e3e18bb2de02c172f775379f664bad8e056ef6867a39d03dc"
CONTRACT="31c811e77468f44c2e412893326bc6d5f9ea037cdbf28712ce8e213652fdfc63"
B24="e433359c0b0cfdf4c6ed5c1dbe95ee7b7159d524f97917c3b7bfbc81d1867080"
B3="c76e3189dce4c2ebed6ccd76afad38b0d56e3b20e1e30859cd8eb00dc8e9c8cd"

def git(*args):
    return subprocess.check_output(["git","-C",str(R),*args],text=True).strip()
def ld(path):
    return json.loads(path.read_text(encoding="utf-8"))
def h(path):
    return sha256(path.read_bytes()).hexdigest()

def main():
    assert git("merge-base","--is-ancestor",BASE,"HEAD")==""
    assert git("cat-file","-t",REVIEW)=="commit"
    manifest=ld(HERE/"PROPOSED_NEGATIVE_SOURCE_AND_FAULT_POLICY.json")
    assert manifest["state"]=="OWNER_DECISION_REQUEST_ONLY_NOT_ADOPTED"
    assert manifest["candidate_base_commit"]==BASE
    assert manifest["independent_getter_review_commit"]==REVIEW
    assert manifest["source_population_success_contract_unchanged"] is True
    assert manifest["original_owner_adopted_source_contract_sha256"]==CONTRACT
    assert manifest["original_adopted_successful_cohort_sha256"]==SOURCE
    assert manifest["existing_24_negative_bundle_sha256"]==B24
    assert manifest["getter_3_new_bundle_sha256"]==B3
    assert h(R/"handoff/m02_completion_28_execution/L01b/R112_SOURCE_CONTRACT_PROPOSED.json")==CONTRACT
    assert h(R/"handoff/m02_completion_28_execution/L01b/CONTROLLED_BATCH_INPUTS.json")==SOURCE
    assert h(R/"handoff/m02_completion_28_execution/L04/D091_PROOF_ADMISSION_REVISION_20261116/EXACT_NEGATIVE_STIMULUS_BUNDLE.json")==B24
    assert h(R/"handoff/m02_completion_28_execution/L04/D091_ORIGINAL_GETTER_FAULT_PREP_20261116/EXACT_GETTER_FAULT_BUNDLE.json")==B3

    expected={"A_L01B_MALFORMED_ORIGINAL_NEGATIVE_ONLY":15,
              "B_ALTERNATIVE_COHORT_EXCEPTION":2,
              "C_PAGINATED_READ_FAULT_PORT":2,
              "D_D091_ORIGINAL_GETTER_READONLY_FAULT_PORT":3,
              "E_SQLITE_FAILURE_SEAM":3,
              "F_ALREADY_FIXED_REQUEST_NEGATIVE_NO_NEW_SOURCE":2}
    specimens=manifest["exact_specimens"]
    assert len(specimens)==27
    assert len({x["case_id"] for x in specimens})==27
    assert len({x["path"] for x in specimens})==27
    totals={k:sum(x["decision_group"]==k for x in specimens) for k in expected}
    assert totals==expected,totals
    assert len(manifest["proposed_policy_groups"])==6
    for k,group in manifest["proposed_policy_groups"].items():
        assert group["count"]==expected[k]
        assert group["owner_decision"]==("NOT_REQUESTED" if k.startswith("F_") else "PENDING")
    oldindex=ld(R/"handoff/m02_completion_28_execution/L04/D091_PROOF_ADMISSION_REVISION_20261116/NEGATIVE_FIXTURE_INDEX.json")
    newindex=ld(R/"handoff/m02_completion_28_execution/L04/D091_ORIGINAL_GETTER_FAULT_PREP_20261116/EXACT_GETTER_FAULT_INDEX.json")
    old_hashes={x["case_id"]:(x["path"],x["sha256"]) for x in oldindex["negative_fixtures"]}
    new_hashes={x["case_id"]:(x["path"],x["sha256"]) for x in newindex["files"]}
    assert len(old_hashes)==24 and len(new_hashes)==3
    assert set(old_hashes).isdisjoint(new_hashes)
    assert set(old_hashes)|set(new_hashes)=={x["case_id"] for x in specimens}
    for row in specimens:
        p=R/row["path"]
        assert h(p)==row["sha256"]
        assert (row["path"],row["sha256"])==(old_hashes|new_hashes)[row["case_id"]]
        assert row["source_scope"] in ("UNADMITTED_TEST_STIMULUS_NOT_LAWFUL_PRODUCTION_SOURCE","READ_ONLY_SELECTOR_FAULT_RESPONSE_NOT_M00_SOURCE_MUTATION")
        if row["decision_group"].startswith("D_"):
            assert row["jurisdiction"]=="L04_D091"
        elif row["decision_group"].startswith("A_"):
            assert row["jurisdiction"]=="L01b_R112_SOURCE_SUPPORT_NOT_D091"

    cases=manifest["case_proposals_summary"]
    assert cases["D091"]==17 and cases["L01b"]==15 and cases["combined"]==32
    assert cases["current_D091_admitted"]==cases["current_D091_ceiling"]==cases["current_D091_runs"]==0
    assert cases["final_adequacy"]=="NOT_ESTABLISHED"
    ledger=ld(R/"handoff/m02_completion_28_execution/TEST_EVIDENCE_LEDGER.json")
    active=next(z for z in ledger["proof_obligations"] if z["proof_id"]=="M02-C28-D091")
    assert active["test_allocation"]["authorised_case_count"]==0
    assert active["test_allocation"]["hard_ceiling"]==0
    assert not active["test_allocation"]["cases"] and not active["execution"]["runs"]
    assert all(phrase in manifest["exclude_from_this_decision"] for phrase in
       ["physical test case admission or budget change","product code, test authoring or execution","PR merge or D145 reactivation"])

    changes=git("diff","--name-only",BASE,"HEAD").splitlines()
    changes+=git("diff","--cached","--name-only").splitlines()
    changes+=git("ls-files","--others","--exclude-standard").splitlines()
    rootdir=HERE.relative_to(R).as_posix()+"/"
    assert changes and all(x.startswith(rootdir) for x in changes),changes
    print(json.dumps({"result":"R112_OWNER_NEGATIVE_POLICY_REQUEST_STATIC_PASS","proposed_source_fault_policy_decisions":5,
    "request_only_no_source_adoption":True,"referenced_sha_verified_fixture_bytes":27,"groups":totals,
    "referenced_prior_cases_D091":17,"referenced_prior_cases_L01b":15,
    "current_admitted":0,"product_runs":0,"changed_product_or_authority_files":False,
    "real_test_fault_seam_or_runtime_executed":False},sort_keys=True))

if __name__=="__main__":
    main()
