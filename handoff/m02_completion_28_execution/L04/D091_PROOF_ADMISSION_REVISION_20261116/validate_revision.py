"""Static-only D091 RETURN revision verification; no product code imports/tests."""
from __future__ import annotations
from pathlib import Path
from decimal import Decimal
from hashlib import sha256
import json
import subprocess

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
BASE="6e7dbf79053a2222e82b2f1a7fb3e491ee6e141d"
REVIEW="c2e4559e648fc3b1a3e2b7d7eaea79568e75b7d4"
SOURCE_SHA="1f4c46c5c247c78e3e18bb2de02c172f775379f664bad8e056ef6867a39d03dc"
CONTRACT_SHA="31c811e77468f44c2e412893326bc6d5f9ea037cdbf28712ce8e213652fdfc63"
ORACLE_SHA="28bca489fc35faaef7b3a673e5c242b3463b125aa9038ee8d9c3a8c8192c5947"
OLD=ROOT/"handoff/m02_completion_28_execution/L01b"
def canon(o):return (json.dumps(o,sort_keys=True,separators=(",",":"),ensure_ascii=False,allow_nan=False)+"\n").encode()
def load(p):return json.loads(p.read_text(encoding="utf-8"))
def sha(p):return sha256(p.read_bytes()).hexdigest()
def git(*args):return subprocess.check_output(["git","-C",str(ROOT),*args],text=True).strip()
def main():
 assert git("merge-base","--is-ancestor",BASE,"HEAD")==""
 assert git("cat-file","-t",REVIEW)=="commit"
 assert sha(OLD/"CONTROLLED_BATCH_INPUTS.json")==SOURCE_SHA
 assert sha(OLD/"DOCUMENTARY_ORACLES.json")==ORACLE_SHA
 assert sha(OLD/"R112_SOURCE_CONTRACT_PROPOSED.json")==CONTRACT_SHA
 original=load(OLD/"CONTROLLED_BATCH_INPUTS.json")
 oracle=load(OLD/"DOCUMENTARY_ORACLES.json")
 contract=load(OLD/"R112_SOURCE_CONTRACT_PROPOSED.json")
 matrix=load(HERE/"REVISED_NODE_AND_FIXTURE_MATRIX.json")
 bundle=load(HERE/"EXACT_NEGATIVE_STIMULUS_BUNDLE.json")
 index=load(HERE/"NEGATIVE_FIXTURE_INDEX.json")
 previous=load(ROOT/"handoff/m02_completion_28_execution/L04/D091_PROOF_ADMISSION_PREP_20261116/FINITE_CASE_AND_WITNESS_MATRIX.json")
 active=load(ROOT/"handoff/m02_completion_28_execution/TEST_EVIDENCE_LEDGER.json")
 proof=next(x for x in active["proof_obligations"] if x["proof_id"]=="M02-C28-D091")
 proposed=load(ROOT/"handoff/planning/m02_foundation_completion_20261030/PROOF_ALLOCATION_PROPOSED.json")
 baseline=next(x for x in proposed["allocations"] if x["proof_id"]=="M02-C28-D091")
 assert baseline["proposed_case_count"]==2 and baseline["proposed_hard_ceiling"]==6
 assert proof["test_allocation"]["authorised_case_count"]==proof["test_allocation"]["hard_ceiling"]==0
 assert proof["test_allocation"]["cases"]==[] and proof["execution"]["runs"]==[]
 assert matrix["status"]=="REVIEW_CANDIDATE_NOT_OWNER_APPROVED_NOT_CASE_ADMITTED"
 assert matrix["owner_budget_approval"] is False and matrix["total_case_count_proposed"]==29
 assert matrix["revised_d091_cases_proposed"]==14 and matrix["revised_l01b_support_cases_proposed"]==15
 assert matrix["original_case_count"]==2 and matrix["old_prospective_ceiling"]==6
 assert matrix["active_authorised_case_count"]==matrix["active_l01b_cases"]==matrix["active_d091_cases"]==0
 assert matrix["product_runs"]==0 and matrix["source_original_sha256"]==SOURCE_SHA
 assert len(matrix["cases"])==29
 assert len({c["case_id"] for c in matrix["cases"]})==29
 assert len({c["test_node"] for c in matrix["cases"]})==29
 assert {c["case_id"] for c in matrix["cases"] if c["kind"]=="ORIGINAL"}=={i["case_id"] for i in baseline["cases"]}
 assert sum(c["coverage_owner"]=="L01b_R112_SOURCE_SUPPORT_NOT_D091" for c in matrix["cases"])==15
 assert sum(c["coverage_owner"]=="L04_D091" for c in matrix["cases"])==14
 assert all(c["status"]=="UNADMITTED_PROPOSAL" for c in matrix["cases"])
 assert all(c["reached_d091_diagnostic"] is False for c in matrix["cases"] if c["coverage_owner"]=="L01b_R112_SOURCE_SUPPORT_NOT_D091")
 assert all(c["test_node"].startswith("tests/product/m02_completion_28/l01b_r112/") for c in matrix["cases"] if c["coverage_owner"]=="L01b_R112_SOURCE_SUPPORT_NOT_D091")
 assert all(c["test_node"].startswith("tests/product/m02_completion_28/d091/") for c in matrix["cases"] if c["coverage_owner"]=="L04_D091")
 prior={v for c in previous["physical_case_nodes"] for v in c["witness_ids"]}
 current={v for c in matrix["cases"] for v in c["predecessor_witness_ids"]}
 assert len(prior)==39 and prior==current,sorted(prior-current)
 assert matrix["preceding_39_witness_ids_covered"]

 # Standalone canonical inputs and envelope hashes are actual byte checks.
 assert len(index["negative_fixtures"])==len(bundle["fixtures"])==24
 bundle_path=HERE/"EXACT_NEGATIVE_STIMULUS_BUNDLE.json"
 assert sha(bundle_path)==matrix["negative_fixture_bundle_sha256"]==index["bundle_sha256"]
 byid={c["case_id"]:c for c in matrix["cases"]}
 assert len({c["case_id"] for c in index["negative_fixtures"]})==24
 assert {x["case_id"] for x in bundle["fixtures"]}=={x["case_id"] for x in index["negative_fixtures"]}
 original_identity=original["members"][0]["observation"]["native_record"]["identity"]
 assert len(contract["contract_identity_fields"])==11
 assert set(contract["contract_identity_fields"])==set(original_identity)
 mutation_fields={}
 for entry in index["negative_fixtures"]:
  p=ROOT/entry["path"]
  record=load(p)
  assert p.read_bytes()==canon(record)
  assert sha(p)==entry["sha256"]==byid[entry["case_id"]]["fixture_sha256"]
  assert record in bundle["fixtures"]
  assert record["case_id"]==entry["case_id"]
  assert record["status"]=="PROPOSED_NOT_ADMITTED"
  assert record["original_source_sha256"]==SOURCE_SHA
  kind=record["stimulus_kind"]
  if kind in ("RAW_SOURCE_INGRESS","UNADMITTED_NEGATIVE_COHORT"):
   expected=record["proposed_m00_constructor"]
   assert expected["concept_id"]=="raw_signal.raw_observation_occurrence"
   assert expected["contract_id"]=="nvda.raw_signal.RawObservationOccurrence.v1"
   assert expected["delivery_artifact_ref"].startswith("T01-R112-NEGATIVE-")
   inp=record["input"]
   members=inp["members"] if "members" in inp else [inp]
   assert len({m["member_id"] for m in members})==len(members)
   assert len({m["observation"]["observation_occurrence_id"] for m in members})==len(members)
   for m in members:
    obs=m["observation"]
    assert list(obs["raw_signal_catalogue_ids"])==["R112"]
    assert set(obs["native_record"]["identity"])==set(contract["contract_identity_fields"])
    assert obs["source_temporal_kind"]=="receipt_only"
    assert obs["source_timestamp_raw"] is None
    assert obs["source_timezone_native"] is None
    assert obs["received_ts_utc"]==m["calculation_request_proposed"]["as_of_utc"]
   if entry["case_id"]=="D091-CONTROLLED-OVER-64-REFUSAL":
    assert len(members)==65
    assert [m["observation"]["ingestion_sequence"] for m in members]==list(range(1,66))
   if entry["case_id"]=="D091-CONTROLLED-TOP-RANK-TIE-REFUSAL":
    assert len(members)==2
    assert (members[0]["observation"]["received_ts_utc"],members[0]["observation"]["ingestion_sequence"])==(members[1]["observation"]["received_ts_utc"],members[1]["observation"]["ingestion_sequence"])
   if record["separate_proof_claim"]=="L01b_SOURCE_NEGATIVE_SUPPORT":
    assert len(members)==1
    mutation_key=next(iter(record["single_mutation"]))
    mutation_fields[entry["case_id"]]=mutation_key
    assert mutation_key.startswith("observation.")
  if kind=="FAULTING_READ_PORT_NOT_M00":
   assert record["input"]["sealed_original_cohort_ref"]==SOURCE_SHA
   pages=record["input"]["pages"]
   assert len(pages)==2 and len(pages[0]["items"])==8
   if "CURSOR-NONPROGRESS" in entry["case_id"]:
    assert pages[0]["next_cursor"]==pages[1]["request_cursor"]==pages[1]["next_cursor"]=="8"
   if "DUPLICATE-ID-CONFLICT" in entry["case_id"]:
    assert pages[0]["items"][0]["observation_occurrence_id"]==pages[1]["items"][0]["observation_occurrence_id"]
    assert pages[0]["items"][0]["native_value"]!=pages[1]["items"][0]["native_value"]
    assert record["expected_observable"].startswith("HISTORY_OR_AMBIGUOUS_RANK")
 assert len(mutation_fields)==15
 expected_mutations={"observation.native_units","observation.source_provider","observation.source_variant","observation.ingestion_sequence_scope"}
 expected_mutations|={"observation.native_record.identity."+k for k in contract["contract_identity_fields"]}
 assert set(mutation_fields.values())==expected_mutations
 # Documentary target-relative oracle only; not an R112/D091 runtime calculation.
 originals={x["observation"]["received_ts_utc"]:x for x in original["members"]}
 expected={
 "2026-11-15T12:00:12Z":("T01-R112-BATCH-12","RANGE"),
 "2026-11-15T12:00:13Z":("T01-R112-BATCH-13","NONFINITE"),
 "2026-11-15T12:00:14Z":("T01-R112-BATCH-14","ABSENT")}
 for ts,(observation_id,stage) in expected.items():
  m=originals[ts]
  assert m["observation"]["observation_occurrence_id"]==observation_id
  val=m["observation"]["native_record"]["model"].get("delta")
  actual="ABSENT" if val is None else ("NONFINITE" if not Decimal(val["text"]).is_finite() else ("RANGE" if abs(Decimal(val["text"]))>1 else "VALID"))
  assert actual==stage
 assert len(oracle["positive_members"])==12 and len(oracle["refusal_members"])==3
 assert len(original["members"])==15
 # All changed/untracked outputs must remain within additive, versioned documentary directory.
 changed=git("diff","--name-only",BASE,"HEAD").splitlines()
 changed+=git("diff","--cached","--name-only").splitlines()
 changed+=git("ls-files","--others","--exclude-standard").splitlines()
 rel=HERE.relative_to(ROOT).as_posix()+"/"
 assert changed and all(x.startswith(rel) for x in changed),changed
 print(json.dumps({"result":"D091_RETURN_REVISION_STATIC_PASS","case_proposals":29,"d091_case_proposals":14,"l01b_support_proposals":15,"original_witnesses_reconciled":39,"exact_new_negative_fixture_files":24,"negative_bundle_sha256":matrix["negative_fixture_bundle_sha256"],"original_source_sha256":SOURCE_SHA,"target_original_expected_stages":[s for _,s in expected.values()],"active_cases":0,"product_runs":0,"no_product_source_or_test_changes":True,"still_requires_independent_review":True},sort_keys=True))
if __name__=="__main__":main()
