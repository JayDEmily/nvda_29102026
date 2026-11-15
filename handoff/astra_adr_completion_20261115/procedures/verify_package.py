"""Document/transport evidence checks only; no product imports or execution."""
from pathlib import Path
import json, subprocess, hashlib, gzip
R=Path(__file__).resolve().parents[3]; O=R/'handoff/astra_adr_completion_20261115'; P=R/'handoff/planning/t01_owner_lint_integration_20261115'; C=R/'handoff/planning/m02_foundation_completion_20261030'
def read(p):return json.loads(p.read_text())
base='02a19ae02678824908568d8db08f0e1d015cb861'
def git(*args):return subprocess.check_output(['git',*args],cwd=R)
ledger=read(P/'PROPOSED_TEST_EVIDENCE_LEDGER.json');old=json.loads(git('show',base+':'+str((P/'PROPOSED_TEST_EVIDENCE_LEDGER.json').relative_to(R))))
assert len(ledger['proof_obligations'])==35
for p,q in zip(ledger['proof_obligations'],old['proof_obligations']):
 for k in ['proof_id','claim','module','source_identity','prior_evidence']:assert p[k]==q[k],(p['proof_id'],k)
 assert p['test_allocation']['authorised_case_count']==0 and not p['test_allocation']['cases'] and not p['execution']['runs']
leaves=read(P/'PROPOSED_EXECUTION_REGISTER.json')['leaves'];orig=read(C/'LEAF_REGISTER.json');assert len(leaves)==len(orig)==39
for p,q in zip(leaves,orig):
 for k in q:
  if k!='status':assert p[k]==q[k],(p['leaf'],k)
for row in read(P/'GOVERNANCE_SOURCE_RECONCILIATION.json')['files']:
 assert hashlib.sha256((P/row['output']).read_bytes()).hexdigest()==row['output_sha256']
refs=read(O/'REQUIRED_REF_RESULTS.json');assert len(refs)==2281
assert all(x['object_status']==x['restoration_status']=='VERIFIED' and x['readback']==x['expected_tip'] for x in refs)
assert sum(x['inventory']=='ORIGINAL_66_REFS.json' for x in refs)==66
restore=read(O/'ORIGINAL_BUNDLE_RESTORE.json');assert not restore['ref_mismatches'] and restore['tracked_inventory_equal']
assert all(x['expected_sha256']==x['actual_sha256'] for x in restore['checksums'])
assert all(x['exit']==0 for x in restore['commands'])
assert all(x['exit']==0 for x in json.loads(gzip.decompress((O/'RECOVERY_COMMANDS.json.gz').read_bytes())))
assert all(not x['record_errors'] and not x['crc_error'] for x in read(O/'WHEEL_VERIFICATION.json'))
assert all(read(O/'RUNTIME_OBSERVATION.json')['checks'].values())
protected=['GUARDRAILS.md','AGENTS.md','EXEC_PLAN.md','tests/AGENTS.override.md','src','tests','config','vendor','.python-version','pyproject.toml','uv.lock','.github','Makefile']
assert not git('diff',base,'HEAD','--',*protected)
try:
 import jsonschema
 jsonschema.validate(ledger,read(C/'TEST_EVIDENCE_LEDGER.schema.json'));schema='VERIFIED'
except ImportError:schema='BLOCKED: jsonschema unavailable in executing interpreter'
print(json.dumps({'document_invariants':'VERIFIED','schema':schema,'refs':len(refs),'product_tests_executed':False,'protected_paths_unchanged':'VERIFIED'},indent=2))
