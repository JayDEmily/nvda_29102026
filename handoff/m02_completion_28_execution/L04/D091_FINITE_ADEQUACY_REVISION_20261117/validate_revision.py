#!/usr/bin/env python3
"""Documentary-only PR27 revision checks; no product imports, cases or SQLite actions."""
from pathlib import Path
import json, hashlib, sys
from decimal import Decimal
from datetime import datetime,timezone

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
SOURCE=ROOT/'handoff/m02_completion_28_execution/L01b/CONTROLLED_BATCH_INPUTS.json'
CONTRACT=ROOT/'handoff/m02_completion_28_execution/L01b/R112_SOURCE_CONTRACT_PROPOSED.json'
INTAKE=ROOT/'handoff/m02_completion_28_execution/L04/D091_FINITE_ADEQUACY_INTAKE_20261116/COMPLETE_CANDIDATE_CASE_INTAKE.json'
LEDGER=ROOT/'handoff/m02_completion_28_execution/TEST_EVIDENCE_LEDGER.json'
OLD_ALLOC=ROOT/'handoff/planning/m02_foundation_completion_20261030/PROOF_ALLOCATION_PROPOSED.json'
REUSE=ROOT/'handoff/planning/m02_foundation_completion_20261030/EVIDENCE_REUSE_INDEX.json'
HIST_REUSE=ROOT/'handoff/m02_remaining_readiness/EVIDENCE_REUSE.json'
SOURCE_SHA='1f4c46c5c247c78e3e18bb2de02c172f775379f664bad8e056ef6867a39d03dc'
CONTRACT_SHA='31c811e77468f44c2e412893326bc6d5f9ea037cdbf28712ce8e213652fdfc63'
INDEPENDENT='ff18a84c14bf7b9a21b608933be177d538176ed6'
BASE='0a549c11feef999ec985c90f4c7fd0599037eb06'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sh(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def ensure(pred,msg):
 if not pred: raise AssertionError(msg)
def is_utc(s):
 x=datetime.fromisoformat(s.replace('Z','+00:00')); return x.tzinfo==timezone.utc
def diffs(a,b,prefix=''):
 if isinstance(a,dict) and isinstance(b,dict):
  ensure(a.keys()==b.keys(),'observation key drift '+prefix)
  return [y for k in a for y in diffs(a[k],b[k],prefix+('.' if prefix else '')+k)]
 if isinstance(a,list) and isinstance(b,list):
  ensure(len(a)==len(b),'observation array drift '+prefix)
  return [y for i in range(len(a)) for y in diffs(a[i],b[i],prefix+'.'+str(i))]
 return [prefix] if a!=b else []
def run():
 ensure(sh(SOURCE)==SOURCE_SHA,'original successful source SHA changed')
 ensure(sh(CONTRACT)==CONTRACT_SHA,'adopted source contract SHA changed')
 original=read(SOURCE);contract=read(CONTRACT);intake=read(INTAKE)
 inv=read(HERE/'REVISED_CASE_INVENTORY.json')
 field=read(HERE/'FIELD_DISCRIMINATION_MATRIX.json')
 b=read(HERE/'NEGATIVE_ONLY_SEALED_COHORTS.json')
 ensure(inv['reviewed_candidate']==BASE and inv['return_review_commit']==INDEPENDENT,'independent review provenance wrong')
 ensure(len(original['members'])==15,'successful 15 changed')
 originals=[x['observation']['observation_occurrence_id'] for x in original['members']]
 ensure(len(set(originals))==15,'successful source duplicate ids')
 ensure(originals==['T01-R112-BATCH-'+str(i).zfill(2) for i in range(15)],'positive source ID drift')
 ensure(contract['source_provider']==original['members'][0]['observation']['source_provider'],'source provider mismatch')
 ensure(contract['native_units']==original['members'][0]['observation']['native_units'],'source native units mismatch')
 orig0=original['members'][0]['observation']
 ensure(orig0['native_record']['model']['delta']['text']=='0','preseal t00 not exact')
 ensure(is_utc(orig0['received_ts_utc']),'original receipt not UTC')
 ensure(len(intake['candidate_cases'])==32 and len(inv['physical_cases'])==33,'case census wrong')
 old={x['case_id']:x for x in intake['candidate_cases']}
 new={x['case_id']:x for x in inv['physical_cases']}
 ensure(len(new)==33 and len(old)==32 and set(old).issubset(new),'missing original physical case ID')
 ensure(set(new)-set(old)=={'D091-CONTROLLED-UNSEALED-REFUSAL'},'unexpected new case(s)')
 ensure([x['case_id'] for x in inv['physical_cases'][:32]]==[x['case_id'] for x in intake['candidate_cases']],'prior case order/identity changed')
 ensure(len({x['proposed_test_node'] for x in inv['physical_cases']})==33,'test node not independently counted')
 for key,c in old.items():
  n=new[key]
  ensure(c['jurisdiction']==n['jurisdiction'] and c['predecessor_witness_ids']==n['predecessor_witness_ids'],'witness or jurisdiction altered '+key)
  ensure(c.get('test_only_fixture_path')==n.get('test_only_fixture_path') and c.get('test_only_fixture_sha256')==n.get('test_only_fixture_sha256'),'fixture mutation '+key)
 ensure(sum(x['jurisdiction']=='L04_D091' for x in new.values())==18,'D091 count')
 ensure(sum(x['jurisdiction']=='L01b_R112_SOURCE_SUPPORT_NOT_D091' for x in new.values())==15,'L01b count')
 ensure(inv['proposed_d091_case_count']==inv['proposed_d091_ceiling_for_owner_decision_only']==18,'D091 proposed ceiling')
 ensure(inv['proposed_l01b_case_count']==inv['proposed_l01b_ceiling_for_owner_decision_only']==15,'L01b proposed ceiling')
 ensure(all(x['admission']=='NONE' and x['observed_product_proof']=='NOT_EXECUTED' for x in new.values()),'false proof or admission')
 ensure(all(x['reuse_generation'] is None and x['reuse_raw_result'] is None for x in new.values()),'unsupported reuse')
 expected_wits={'P'+str(i).zfill(2)+'_'+s for i,s in []}
 expected_wits=set()
 for pfx,num in [('P',15),('R',1),('S',5),('O',6),('H',7),('D',5)]:
  expected_wits.update(x for c in old.values() for x in c['predecessor_witness_ids'] if x.startswith(pfx) and x[1:3].isdigit() and int(x[1:3])>=1 and int(x[1:3])<=num)
 actual_wits={x for c in new.values() for x in c['predecessor_witness_ids']}
 ensure(len(actual_wits)==39 and actual_wits==expected_wits==set(inv['all_39_predecessor_witness_ids']),'39 original named witnesses changed')
 ensure(new['D091-CONTROLLED-UNSEALED-REFUSAL']['predecessor_witness_ids']==[],'fabricated UNSEALED historical witness')
 ensure(new['D091-CONTROLLED-UNSEALED-REFUSAL']['test_only_source_member']==originals[0],'preseal source is not original t00')
 ensure(new['D091-CONTROLLED-UNSEALED-REFUSAL']['expected_stage']=='UNSEALED','UNSEALED stage not explicit')
 fixture_cases=[x for x in old.values() if x.get('test_only_fixture_path')]
 ensure(len(fixture_cases)==27,'27 unchanged negative fixtures not identified')
 ensure(len({x['test_only_fixture_path'] for x in fixture_cases})==27,'fixture aliases')
 for c in fixture_cases:
  f=ROOT/c['test_only_fixture_path']
  ensure(f.is_file() and sh(f)==c['test_only_fixture_sha256'],'fixture SHA mismatch '+c['case_id'])
  ensure(read(f)['case_id']==c['case_id'],'fixture case mismatch '+c['case_id'])
 ensure(len(field['cases'])==15,'source field row count')
 fs={x['case_id']:x for x in field['cases']}
 ensure(set(fs)=={x for x in new if x.startswith('L01B-')},'field case mismatch')
 for id,x in fs.items():
  spec=read(ROOT/x['fixture_path'])
  ensure(sh(ROOT/x['fixture_path'])==x['fixture_sha256'],'A SHA mismatch '+id)
  mutate=spec['single_mutation'];ensure(len(mutate)==1 and x['path'] in mutate,'A mutation mismatch '+id)
  changes=set(diffs(orig0,spec['input']['observation']))
  ensure(changes=={'observation_occurrence_id',x['path'].removeprefix('observation.')},'additional A field mutation '+id+': '+str(changes))
  ensure(x['expected_valid']!=x['malformed_value'],'A no wrong field '+id)
  ensure(x['negative_occurrence_id'] not in originals,'A fixture actually successful ID '+id)
  ensure(new[id]['predicate']==x['path'] and new[id]['expected_stage']=='COORDINATOR_SOURCE_FIELD_REFUSAL','A stage or path drift '+id)
 ensure(len({x['path'] for x in fs.values()})==15,'A fields not unique')
 expected_paths={'observation.native_units','observation.source_provider','observation.source_variant','observation.ingestion_sequence_scope'}|{'observation.native_record.identity.'+x for x in contract['contract_identity_fields']}
 ensure(set(x['path'] for x in fs.values())==expected_paths,'15 full source-field coverage missing')
 modes=b['cohorts']
 ensure(set(modes)=={'B_TIE','B_OVER64'},'negative cohort roster')
 ensure(modes==inv['negative_test_only_cohort_manifests'],'cohort manifest mismatch')
 for mode,n in [('B_TIE',2),('B_OVER64',65)]:
  m=modes[mode];f=ROOT/m['fixture_path'];data=read(f)
  ensure(sh(f)==m['fixture_sha256'],'B fixture hash mismatch '+mode)
  oo=[v['observation'] for v in data['input']['members']]
  ensure(len(oo)==m['raw_member_count']==m['expected_projected_count']==n,'B cohort count '+mode)
  ensure(len({x['observation_occurrence_id'] for x in oo})==n,'duplicate B raw IDs '+mode)
  ensure(not (set(x['observation_occurrence_id'] for x in oo)&set(originals)),'B contaminated original source '+mode)
  ensure([x['observation_occurrence_id'] for x in oo]==m['expected_ids'],'B exact ID map drift '+mode)
  ensure(all(x['source_provider']==contract['source_provider'] and x['source_variant']==contract['source_variant'] and x['native_units']==contract['native_units'] and x['subject_instrument']==orig0['subject_instrument'] for x in oo),'B source fields not projectable '+mode)
  ensure(all(x['native_record']['identity']==orig0['native_record']['identity'] for x in oo),'B identity mismatch '+mode)
  ensure(all(x['source_temporal_kind']=='receipt_only' and x['source_timestamp_raw'] is None and x['source_timezone_native'] is None and x['ingestion_sequence_scope']==contract['selection']['ingestion_sequence_scope'] for x in oo),'B clock/scope mismatch '+mode)
  ensure(all(x['native_record']['model']['delta']['native_type']=='Decimal' and Decimal(x['native_record']['model']['delta']['text']).is_finite() for x in oo),'B native Decimal not projectable '+mode)
  ensure(all(is_utc(x['received_ts_utc']) for x in oo),'B non-UTC receipt '+mode)
  request=data['input']['read_request']; ensure(request['as_of_utc']==request['knowledge_cutoff_utc']==oo[-1]['received_ts_utc'],'B request not target exact receipt '+mode)
  ensure(m['expected_page_sizes']==([8]*8+[1] if n==65 else [2]),'B expected pagination != 8x8+1 or 2')
  ensure(m['allowed_derived_outcome']=='REFUSAL_ONLY_NO_SUCCESSFUL_D091_CATEGORY' and m['never_use_positive_roster'],'B source expansion')
 if True:
  tie=[v['observation'] for v in read(ROOT/modes['B_TIE']['fixture_path'])['input']['members']]
  ensure(len({(x['received_ts_utc'],x['ingestion_sequence']) for x in tie})==1,'B tie absent')
  over=[v['observation'] for v in read(ROOT/modes['B_OVER64']['fixture_path'])['input']['members']]
  ensure([x['ingestion_sequence'] for x in over]==list(range(1,66)),'B overflow sequence wrong')
  ensure(len({x['received_ts_utc'] for x in over})==65,'B over64 receipt missing')
 led=[x for x in read(LEDGER)['proof_obligations'] if x['proof_id']=='M02-C28-D091']
 ensure(len(led)==1,'D091 ledger missing')
 ll=led[0]
 ensure(ll['test_allocation']['authorised_case_count']==0 and ll['test_allocation']['hard_ceiling']==0 and ll['test_allocation']['cases']==[] and ll['execution']['runs']==[],'current ledger not zero')
 oldalloc=[x for x in read(OLD_ALLOC)['allocations'] if x['proof_id']=='M02-C28-D091']
 ensure(len(oldalloc)==1 and oldalloc[0]['proposed_case_count']==2 and oldalloc[0]['proposed_hard_ceiling']==6,'old prospective pair/ceiling changed')
 ensure({x['case_id'] for x in oldalloc[0]['cases']}=={'D091-CONTROLLED-SUCCESS','D091-CONTROLLED-REACHED_REFUSAL'},'original D091 identities changed')
 reuse=read(REUSE);hist=read(HIST_REUSE)
 ensure(reuse['historical_count']==98 and reuse['L14_claim_count']==11,'reuse index census changed')
 ensure('historical_controlled_evidence' in hist and 'L14_separate_profiles' in hist,'original accepted reuse evidence missing')
 ensure(inv['exact_accepted_case_reuse_identified']==[],'unverified reused product cases')
 ensure(inv['product_runs']==0 and inv['active_authorised_count']==0 and inv['active_hard_ceiling']==0,'false admission in revised packet')
 return {'status':'D091_L01B_REVISION_DOCUMENTARY_STATIC_PASS','reviewed_candidate':BASE,'return_review_commit':INDEPENDENT,
         'source_sha256':sh(SOURCE),'contract_sha256':sh(CONTRACT),'original_cases_checked':len(old),
         'proposed_D091':18,'proposed_L01b':15,'proposed_combined':33,'predecessor_witnesses_checked':39,
         'negative_fixture_hashes_verified':27,'L01b_single_source_field_mutations':15,
         'negative_B_raw_cohorts':[2,65],'expected_B_history_pages':{'B_TIE':[2],'B_OVER64':[8]*8+[1]},
         'reusable_exact_new_product_cases_proven':0,'admitted_cases':0,'product_test_runs':0,
         'limitations':'Documentary fixture/authority consistency only. Does not execute M00/M02, check genuine future seam or approve case budgets.'}
if __name__=='__main__':
 try: print(json.dumps(run(),indent=2))
 except (AssertionError,ValueError,KeyError,TypeError,FileNotFoundError) as e:
  print('D091_L01B_REVISION_DOCUMENTARY_STATIC_FAIL',type(e).__name__,str(e),file=sys.stderr);sys.exit(1)
