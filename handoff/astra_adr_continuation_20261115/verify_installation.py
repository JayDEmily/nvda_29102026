"""Verify exact owner-authorised governance bytes and retained proof boundaries."""
from pathlib import Path
import subprocess,json,hashlib
R=Path(__file__).resolve().parents[2]
SOURCE='a28702cde241b3f833b51071aac8cb41591b37dd';BASE='02a19ae02678824908568d8db08f0e1d015cb861';P='handoff/planning/t01_owner_lint_integration_20261115/'
M={'AGENTS.md':'PROPOSED_AGENTS.md','EXEC_PLAN.md':'PROPOSED_EXEC_PLAN.md','tests/AGENTS.override.md':'PROPOSED_TESTS_AGENTS.override.md','handoff/m02_completion_28_execution/EXECUTION_REGISTER.json':'PROPOSED_EXECUTION_REGISTER.json','handoff/m02_completion_28_execution/TEST_EVIDENCE_LEDGER.json':'PROPOSED_TEST_EVIDENCE_LEDGER.json'}
def git(*a):return subprocess.check_output(['git',*a],cwd=R)
rows=[]
for target,source in M.items():
 expected=git('show',SOURCE+':'+P+source);actual=(R/target).read_bytes();assert actual==expected,target;rows.append({'target':target,'source':SOURCE+':'+P+source,'sha256':hashlib.sha256(actual).hexdigest(),'bytes':len(actual)})
assert (R/'GUARDRAILS.md').read_bytes()==git('show',BASE+':GUARDRAILS.md')
protected=['src','tests/product','tests/implementation','tests/architecture','tests/bootstrap','config','vendor','.python-version','pyproject.toml','uv.lock','tools','.github','Makefile']
assert not git('diff',BASE,'--',*protected)
ledger=json.loads((R/'handoff/m02_completion_28_execution/TEST_EVIDENCE_LEDGER.json').read_text());register=json.loads((R/'handoff/m02_completion_28_execution/EXECUTION_REGISTER.json').read_text())
assert len(register['leaves'])==39 and len(ledger['proof_obligations'])==35
for p in ledger['proof_obligations']:
 assert p['test_allocation']['authorised_case_count']==0 and not p['test_allocation']['cases'] and not p['execution']['runs']
 if p['proof_id']=='M02-C28-D145':assert p['execution']['semantic_status']=='BLOCKED'
try:
 import jsonschema
 schema=json.loads((R/'handoff/planning/m02_foundation_completion_20261030/TEST_EVIDENCE_LEDGER.schema.json').read_text());jsonschema.validate(ledger,schema)
except ImportError:raise RuntimeError('jsonschema required for this documentary verification')
print(json.dumps({'source':SOURCE,'status':'VERIFIED_EXACT_INSTALLATION','files':rows,'frozen_guardrails_unchanged':True,'product_paths_unchanged':True,'leaves':39,'proof_obligations':35,'released_cases':0,'new_product_runs':0,'D145':'PAUSED'},indent=2))
