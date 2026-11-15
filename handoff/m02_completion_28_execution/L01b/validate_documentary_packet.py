"""Validate proposal bytes and literal interval arithmetic; never import product code."""
from pathlib import Path
from decimal import Decimal
import json,hashlib,subprocess
R=Path(__file__).resolve().parents[3];O=Path(__file__).resolve().parent
p=json.loads((O/'R112_SOURCE_CONTRACT_PROPOSED.json').read_text());o=json.loads((O/'DOCUMENTARY_ORACLES.json').read_text());a=json.loads((O/'PROOF_RELEASE_PROPOSAL.json').read_text());prov=json.loads((O/'SOURCE_PROVENANCE.json').read_text())
for s in prov['sources']:assert hashlib.sha256((R/s['path']).read_bytes()).hexdigest()==s['sha256'],s['path']
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
