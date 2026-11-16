"""Documentary-only crosswalk and source evidence consistency validation.
No product imports, test collection or product execution.
"""
from pathlib import Path
import hashlib,json,subprocess
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
BASE='4683f2a0d9f052ee18c8ca5ef31ab93923cca374'
REVIEW='2045bdb84e29d282072451696cfd6515fcf41c1b'
def git(*args):return subprocess.check_output(['git','-C',str(ROOT),*args],text=True).strip()
def load(p):return json.loads((ROOT/p).read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
def run():
 assert git('merge-base','--is-ancestor',BASE,'HEAD')==''
 assert git('cat-file','-t',REVIEW)=='commit'
 p=str(HERE.relative_to(ROOT))+'/COMPLETE_CANDIDATE_CASE_INTAKE.json'
 m=load(p)
 assert m['status']=='WORKER_PREPARATION_FOR_INDEPENDENT_ADEQUACY_REVIEW_ONLY'
 assert m['base_commit']==BASE and m['independent_owner_policy_review']==REVIEW
 cases=m['candidate_cases']
 assert len(cases)==m['case_inventory_count']==32
 assert len({x['case_id'] for x in cases})==len({x['proposed_test_node'] for x in cases})==32
 assert sum(x['jurisdiction']=='L04_D091' for x in cases)==m['d091_case_proposals']==17
 assert sum(x['jurisdiction']=='L01b_R112_SOURCE_SUPPORT_NOT_D091' for x in cases)==m['l01b_case_proposals']==15
 assert sum(x['originally_proposed'] for x in cases)==2
 assert {x['case_id'] for x in cases if x['originally_proposed']}=={'D091-CONTROLLED-SUCCESS','D091-CONTROLLED-REACHED_REFUSAL'}
 counts={}
 for x in cases:
  counts[x['policy_group']]=counts.get(x['policy_group'],0)+1
  assert x['physical_case_status']=='UNADMITTED'
  assert x['reuse_disposition']=='NOT_ESTABLISHED_PER_EXACT_NEW_CASE'
  assert x['reached_public_seam_proof']=='NOT_EXECUTED'
  assert x['separate_owner_case_budget_required'] is True
 assert counts==m['classification_counts']
 assert counts=={'G_ORIGINAL_SUCCESSFUL_COHORT':5,'A_L01B_MALFORMED_ORIGINAL_NEGATIVE_ONLY':15,'B_ALTERNATIVE_COHORT_EXCEPTION':2,'C_PAGINATED_READ_FAULT_PORT':2,'D_D091_ORIGINAL_GETTER_READONLY_FAULT_PORT':3,'E_SQLITE_FAILURE_SEAM':3,'F_ALREADY_FIXED_REQUEST_NEGATIVE_NO_NEW_SOURCE':2}
 assert sum(bool(x['test_only_fixture_path']) for x in cases)==m['verified_fixture_count']==27
 original=load('handoff/m02_completion_28_execution/L01b/CONTROLLED_BATCH_INPUTS.json')
 assert len(original['members'])==15
 assert sha('handoff/m02_completion_28_execution/L01b/CONTROLLED_BATCH_INPUTS.json')==m['original_source_sha256']=='1f4c46c5c247c78e3e18bb2de02c172f775379f664bad8e056ef6867a39d03dc'
 assert sha('handoff/m02_completion_28_execution/L01b/R112_SOURCE_CONTRACT_PROPOSED.json')==m['original_source_contract_sha256']=='31c811e77468f44c2e412893326bc6d5f9ea037cdbf28712ce8e213652fdfc63'
 policy=load('handoff/m02_completion_28_execution/L01b/R112_NEGATIVE_FAULT_POLICY_DECISION_20261116/PROPOSED_NEGATIVE_SOURCE_AND_FAULT_POLICY.json')
 adoption=load('handoff/m02_completion_28_execution/L01b/R112_NEGATIVE_FAULT_POLICY_DECISION_20261116/OWNER_TEST_ONLY_POLICY_ADOPTION_20261116.json')
 assert adoption['state']=='OWNER_ADOPTED_TEST_ONLY_POLICY_NO_PRODUCT_RELEASE'
 assert len(policy['exact_specimens'])==27
 specby={x['case_id']:x for x in policy['exact_specimens']}
 assert len(specby)==27
 for x in cases:
  if x['test_only_fixture_path']:
   assert x['case_id'] in specby
   spec=specby[x['case_id']]
   assert x['test_only_fixture_path']==spec['path']
   assert x['test_only_fixture_sha256']==spec['sha256']==sha(spec['path'])
  else:
   assert x['case_id'] not in specby and x['policy_group']=='G_ORIGINAL_SUCCESSFUL_COHORT'
 assert {x['case_id'] for x in cases if x['policy_group']=='G_ORIGINAL_SUCCESSFUL_COHORT'}=={
 'D091-CONTROLLED-SUCCESS','D091-CONTROLLED-REACHED_REFUSAL','D091-CONTROLLED-SEAL-REFUSAL',
 'D091-CONTROLLED-NONFINITE-REFUSAL','D091-CONTROLLED-ABSENT-REFUSAL'}
 prior=load('handoff/m02_completion_28_execution/L04/D091_PROOF_ADMISSION_REVISION_20261116/REVISED_NODE_AND_FIXTURE_MATRIX.json')
 getter=load('handoff/m02_completion_28_execution/L04/D091_ORIGINAL_GETTER_FAULT_PREP_20261116/ADDITIONAL_GETTER_CASE_PROPOSAL.json')
 assert {x['case_id'] for x in cases}=={x['case_id'] for x in prior['cases']}|{x['case_id'] for x in getter['additional_proposals']}
 assert len(prior['cases'])==29 and len(getter['additional_proposals'])==3
 witnesses={w for x in cases for w in x['predecessor_witness_ids']}
 assert len(witnesses)==m['original_prior_witness_names_reconciled']==39
 assert m['historical_reuse_index_policy']=='REUSABLE_FOR_UNCHANGED_EXACT_PROPOSITIONS_ONLY'
 idx=load('handoff/planning/m02_foundation_completion_20261030/EVIDENCE_REUSE_INDEX.json')
 assert idx['decision']==m['historical_reuse_index_policy']
 original_allocation=load('handoff/planning/m02_foundation_completion_20261030/PROOF_ALLOCATION_PROPOSED.json')
 a=next(x for x in original_allocation['allocations'] if x['proof_id']=='M02-C28-D091')
 assert a['proposed_case_count']==2 and a['proposed_hard_ceiling']==6
 assert m['prospective_historical_d091_ceiling']==6
 ledger=load('handoff/m02_completion_28_execution/TEST_EVIDENCE_LEDGER.json')
 cur=next(x for x in ledger['proof_obligations'] if x['proof_id']=='M02-C28-D091')
 assert cur['test_allocation']['authorised_case_count']==cur['test_allocation']['hard_ceiling']==0
 assert cur['test_allocation']['cases']==[] and cur['execution']['runs']==[]
 assert m['current_active_d091_count']==m['current_active_d091_ceiling']==m['runs']==0
 assert not m['physical_case_authorised'] and not m['case_budget_adopted'] and not m['executable_fault_ports_admitted']
 assert m['coverage_is_final_or_minimal']=='UNKNOWN_INDEPENDENT_ASSESSMENT_REQUIRED'
 changed=git('diff','--name-only',BASE,'HEAD').splitlines()+git('diff','--cached','--name-only').splitlines()+git('ls-files','--others','--exclude-standard').splitlines()
 rootdir=str(HERE.relative_to(ROOT))+'/'
 assert changed and all(x.startswith(rootdir) for x in changed),changed
 print(json.dumps({'result':'D091_FINITE_ADEQUACY_INTAKE_STATIC_PASS','proposed_case_count':32,'proposed_D091_cases':17,'proposed_L01b_cases':15,'original_cases':2,'predecessor_witnesses':39,'fixture_hashes_checked':27,'policy_groups':counts,'owner_budget_approved':False,'authorised_cases':0,'product_runs':0,'test_and_product_source_changes':False,'full_semantic_adequacy_established':False},sort_keys=True))
if __name__=='__main__':run()
