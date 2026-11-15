"""Validate proposal bytes and literal interval arithmetic; never import product code."""
from pathlib import Path
from decimal import Decimal
import json,hashlib,subprocess
R=Path(__file__).resolve().parents[3];O=Path(__file__).resolve().parent
p=json.loads((O/'R112_SOURCE_CONTRACT_PROPOSED.json').read_text());o=json.loads((O/'DOCUMENTARY_ORACLES.json').read_text());a=json.loads((O/'PROOF_RELEASE_PROPOSAL.json').read_text());prov=json.loads((O/'SOURCE_PROVENANCE.json').read_text())
for s in prov['sources']:assert hashlib.sha256((R/s['path']).read_bytes()).hexdigest()==s['sha256'],s['path']
artifact_path=R/p['delivery_artifact_binding']['path'];assert hashlib.sha256(artifact_path.read_bytes()).hexdigest()==p['delivery_artifact_binding']['sha256']
batch=json.loads(artifact_path.read_text());assert len(batch['members'])==15
assert p['source_specimen']['delivery_artifact_ref']==p['delivery_artifact_binding']['delivery_artifact_ref']
import ast
module=ast.parse((R/'src/nvda_desk/raw_signal_occurrence_truth/api.py').read_text());raw=next(n for n in module.body if isinstance(n,ast.ClassDef) and n.name=='RawObservationOccurrenceV1');required={n.target.id for n in raw.body if isinstance(n,ast.AnnAssign) and n.value is None};assert required<=set(p['source_specimen'])
seen=set()
for member in batch['members']:
 obs=member['observation'];req=member['calculation_request_proposed'];assert obs['observation_occurrence_id'] not in seen;seen.add(obs['observation_occurrence_id'])
 assert obs['received_ts_utc']==req['as_of_utc']==req['knowledge_cutoff_utc']<=req['calculated_at_utc']
 assert obs['native_record']['identity']==p['specimen_contract']
 assert not {'expected_label','expected_bucket','result','D091'} & set(obs['native_record'])
assert p['selection']['history_page_size']==8 and p['selection']['closed_batch_precondition']
old=json.loads((R/'handoff/m02_foundation_prerequisites_20261029/R3_TENTATIVE_SYNTHETIC_PROFILES_V1.json').read_text())['profiles']['D091_delta_buckets'];assert p['rule_profile']['bins']==old['bins']
bins=p['rule_profile']['bins'];assert Decimal(bins[0]['min'])==0 and Decimal(bins[-1]['max'])==1
for i,b in enumerate(bins):
 assert b['min_inclusive'] and Decimal(b['min'])<Decimal(b['max'])
 assert b['max_inclusive']==(i==len(bins)-1)
 if i:assert b['min']==bins[i-1]['max']
for w in o['positive_members']:
 v=abs(Decimal(w['signed_delta']));matches=[b['name'] for b in bins if Decimal(b['min'])<=v and (v<Decimal(b['max']) or b['max_inclusive'] and v==Decimal(b['max']))];assert matches==[w['expected_label']]
orig=json.loads((R/'handoff/planning/m02_foundation_completion_20261030/PROOF_ALLOCATION_PROPOSED.json').read_text());assert a['original_allocation']==next(x for x in orig['allocations'] if x['proof_id']=='M02-C28-D091');assert not a['admitted_cases'] and not a['executed_runs'] and not a['new_case_ids']
base=prov['base_commit'];protected=['GUARDRAILS.md','AGENTS.md','EXEC_PLAN.md','tests','src','config','implementation','vendor','tools','.python-version','pyproject.toml','uv.lock','.github','Makefile','handoff/m02_completion_28_execution/EXECUTION_REGISTER.json','handoff/m02_completion_28_execution/TEST_EVIDENCE_LEDGER.json'];assert not subprocess.check_output(['git','diff',base,'--',*protected],cwd=R)
ledger=json.loads((R/'handoff/m02_completion_28_execution/TEST_EVIDENCE_LEDGER.json').read_text());assert len(ledger['proof_obligations'])==35 and all(x['test_allocation']['authorised_case_count']==0 and not x['execution']['runs'] for x in ledger['proof_obligations'])
print(json.dumps({'status':'DOCUMENTARY_IDENTITY_AND_LITERAL_ARITHMETIC_VERIFIED','positive_literal_members':len(o['positive_members']),'original_physical_case_objects_preserved':2,'admitted_cases':0,'executed_product_runs':0,'protected_paths_unchanged':True,'product_source_imported':False,'source_admission':'NOT_GRANTED'},indent=2))
