"""D091 documentary getter-fault packet validation: no product import or test."""
from pathlib import Path
import json,hashlib,subprocess
R=Path(__file__).resolve().parents[4]
HERE=Path(__file__).resolve().parent
BASE="b5c818fc52863539512456605981f36318c8a3e8"
REVIEW="ab30bee937f16d13a7ad5d6a1ee79eed091694e1"
S="1f4c46c5c247c78e3e18bb2de02c172f775379f664bad8e056ef6867a39d03dc"
C="31c811e77468f44c2e412893326bc6d5f9ea037cdbf28712ce8e213652fdfc63"
def ld(p):return json.loads(p.read_text(encoding="utf-8"))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def git(*x):return subprocess.check_output(["git","-C",str(R),*x],text=True).strip()
def canon(x):return (json.dumps(x,sort_keys=True,separators=(",",":"),ensure_ascii=False,allow_nan=False)+"\n").encode()
def main():
 assert git("merge-base","--is-ancestor",BASE,"HEAD")==""
 assert git("cat-file","-t",REVIEW)=="commit"
 original_path=R/"handoff/m02_completion_28_execution/L01b/CONTROLLED_BATCH_INPUTS.json"
 original_contract=R/"handoff/m02_completion_28_execution/L01b/R112_SOURCE_CONTRACT_PROPOSED.json"
 assert sha(original_path)==S and sha(original_contract)==C
 source=ld(original_path)
 target=next(x for x in source["members"] if x["observation"]["observation_occurrence_id"]=="T01-R112-BATCH-11")
 assert len(source["members"])==15 and target["observation"]["received_ts_utc"]=="2026-11-15T12:00:11Z"
 assert sum(x["observation"]["received_ts_utc"]<="2026-11-15T12:00:11Z" and bool(x["observation"]["native_record"]["model"].get("delta")) for x in source["members"])==12
 assert target["observation"]["native_record"]["model"]["delta"]["native_type"]=="Decimal"
 assert set(target["observation"]["native_record"]["identity"])==set(ld(original_contract)["contract_identity_fields"])
 prior=ld(R/"handoff/m02_completion_28_execution/L04/D091_PROOF_ADMISSION_REVISION_20261116/REVISED_NODE_AND_FIXTURE_MATRIX.json")
 assert len(prior["cases"])==29 and prior["revised_d091_cases_proposed"]==14 and prior["revised_l01b_support_cases_proposed"]==15
 assert len({s for x in prior["cases"] for s in x["predecessor_witness_ids"]})==39
 idx=ld(HERE/"EXACT_GETTER_FAULT_INDEX.json")
 b=ld(HERE/"EXACT_GETTER_FAULT_BUNDLE.json")
 m=ld(HERE/"ADDITIONAL_GETTER_CASE_PROPOSAL.json")
 assert len(idx["files"])==len(b["test_only_fault_fixtures"])==len(m["additional_proposals"])==3
 assert sha(HERE/"EXACT_GETTER_FAULT_BUNDLE.json")==idx["bundle_sha256"]==m["new_getter_fault_bundle_sha256"]
 assert all(x==0 for x in [m["active_d091_authorised_count"],m["active_d091_ceiling"],m["active_l01b_case_release"],m["actual_product_runs"]])
 assert (m["predecessor_proposed_cases"],m["predecessor_d091_case_count"],m["predecessor_l01b_case_count"])==(29,14,15)
 assert (m["total_d091_proposed_after_addition"],m["total_l01b_proposed_unchanged"],m["total_cross_jurisdiction_proposals"])==(17,15,32)
 assert m["this_is_not_a_final_closed_minimum"] is True
 cases={x["case_id"]:x for x in m["additional_proposals"]}
 assert len(cases)==3
 assert len({x["test_node"] for x in cases.values()})==3
 fault_kinds=set()
 for item in idx["files"]:
  p=R/item["path"];v=ld(p)
  assert p.read_bytes()==canon(v)
  assert sha(p)==item["sha256"]==cases[item["case_id"]]["fixture_sha256"]
  assert v in b["test_only_fault_fixtures"]
  assert v["case_id"]==item["case_id"]
  assert v["status"]=="PROPOSED_NOT_APPROVED_NOT_PRODUCT_TEST"
  assert v["original_fifteen_member_batch_sha256"]==S
  assert v["adopted_original_contract_sha256"]==C
  assert v["original_complete_observation_documentary"]==target["observation"]
  assert v["target_request_original"]==target["calculation_request_proposed"]
  assert v["projected_history"]["projection_is_not_mutated"] is True
  assert v["projected_history"]["expected_request_cursor_sequence"]==[None,"8"]
  assert v["projected_history"]["second_page_size"]==4
  assert v["expected_stage"]=="ORIGIN_OR_IDENTITY"
  assert v["expected_result"] is None and v["expected_d091_persisted_occurrences"]==0
  assert not v["test_seam"]["normal_m00_fault_claim"] and not v["test_seam"]["writer_handle_exposed"]
  assert v["test_seam"]["need_owner_and_independent_test_seam_approval"] is True
  kind=v["fault_kind"];fault_kinds.add(kind)
  returned=v["test_only_getter_response_documentary"]
  if kind=="MISSING_GETTER_RESULT":
   assert returned is None and v["one_mutation"]=={"getter":"None for existing observation ID"}
  else:
   assert returned is not None
   baseline=target["observation"]
   diffs=[]
   def compare(a,z,path):
    if type(a) is dict and type(z) is dict:
     assert set(a)==set(z)
     for k in a:compare(a[k],z[k],path+[k])
    elif a!=z:diffs.append((".".join(path),a,z))
   compare(baseline,returned,[])
   assert len(diffs)==1
   if kind=="ORIGINAL_UNITS_CONTRADICTION":
    assert diffs==[("native_units","signed_decimal_fraction","decimal_percent")]
   elif kind=="ORIGINAL_IDENTITY_CONTRADICTION":
    assert diffs==[("native_record.identity.generation","T01-R112-CONTROL-G1","T01-R112-CONTROL-G2")]
   else:raise AssertionError(kind)
 assert fault_kinds=={"MISSING_GETTER_RESULT","ORIGINAL_UNITS_CONTRADICTION","ORIGINAL_IDENTITY_CONTRADICTION"}
 ledger=ld(R/"handoff/m02_completion_28_execution/TEST_EVIDENCE_LEDGER.json")
 v=next(x for x in ledger["proof_obligations"] if x["proof_id"]=="M02-C28-D091")
 assert v["test_allocation"]["authorised_case_count"]==v["test_allocation"]["hard_ceiling"]==0
 assert not v["execution"]["runs"]
 changes=git("diff","--name-only",BASE,"HEAD").splitlines()+git("diff","--cached","--name-only").splitlines()+git("ls-files","--others","--exclude-standard").splitlines()
 rel=HERE.relative_to(R).as_posix()+"/"
 assert changes and all(x.startswith(rel) for x in changes),changes
 print(json.dumps({"result":"D091_GETTER_FAULT_PREPARATION_STATIC_PASS","original_source_sha256":S,"separate_proposed_cases":3,"underlying_predecessor_proposed_cases":29,"d091_proposed_cases":17,"l01b_proposed_cases":15,"total_proposals":32,"new_fixture_sha256_verified":3,"preceding_witness_ids":39,"cases_admitted":0,"product_runs":0,"product_source_or_test_changes":False,"genuine_source_and_sealed_port_execution":"NOT_PERFORMED","acceptance":"STILL_REQUIRES_INDEPENDENT_REVIEW_AND_OWNER_AUTHORITY"},sort_keys=True))
if __name__=="__main__":main()
