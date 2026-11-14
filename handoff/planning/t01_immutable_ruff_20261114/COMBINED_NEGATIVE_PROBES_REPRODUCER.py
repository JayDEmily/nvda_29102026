from pathlib import Path
import subprocess, hashlib, json, sys, datetime
R=Path('/home/jds/nvda_ci_lint_combination_20261114')
receipt=Path('/home/jds/nvda_validation_receipts_20261114/ruff_baseline_combined_negative_probes_20261114.log')
assert not receipt.exists()
expected='c8a776e' # local cherry-pick of original PR10 proposal onto exact PR12 tree
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip()
assert head.startswith(expected),head
assert not subprocess.check_output(['git','status','--porcelain'],cwd=R)
PY=R/'.venv/bin/python'
verifier=R/'tools/proposed_admitted_ruff_baseline.py'
manifest_file=R/'config/lint/PROPOSED_SHA_BOUND_RUFF_BASELINE.json'
manifest=json.loads(manifest_file.read_text())
def sha(x):return hashlib.sha256(x).hexdigest()
def execute(label,expect_rc,needle):
 p=subprocess.run([str(PY),str(verifier)],cwd=R,capture_output=True,text=True)
 output=(p.stdout+'\n'+p.stderr).strip()
 assert p.returncode==expect_rc,(label,p.returncode,output)
 assert needle in output,(label,output)
 line=f'{label}: rc={p.returncode}; {output[:500]}'
 with receipt.open('a') as f:f.write(line+'\n')
 print(line,flush=True)
def controlled_tamper(label,path,mutation,needle):
 before=path.read_bytes()
 try:
  path.write_bytes(mutation(before))
  assert path.read_bytes()!=before
  execute(label,1,needle)
 finally:
  path.write_bytes(before)
  assert path.read_bytes()==before and sha(path.read_bytes())==sha(before)
execute('CONTROL_BASELINE',0,'PROPOSED_BASELINE_EXACT_MATCH: 51')
first=R/manifest['files'][0]['path']
controlled_tamper('FROZEN_SOURCE_CHANGE',first,lambda b:b+b'\n# TEMPORARY NEGATIVE PROBE DO NOT COMMIT\n','admitted source bytes changed')
pointer=R/manifest['files'][0]['admission_path']
def mutate_pointer(b):
 d=json.loads(b)
 d['current_generation']['sha256']='0'*64
 return (json.dumps(d,indent=2)+'\n').encode()
controlled_tamper('ADMISSION_POINTER_CHANGE',pointer,mutate_pointer,'generation bytes or pointer changed')
controlled_tamper('MANIFEST_CHANGE',manifest_file,lambda b:b+b'\n','baseline manifest byte identity changed')
newfile=R/'src/nvda_desk/_negative_ruff_probe_20261114.py'
assert not newfile.exists()
try:
 newfile.write_text('def novel_lint():\n    return intentionally_undefined_name_20261114\n')
 execute('UNEXPECTED_NEW_RUFF_DIAGNOSTIC',1,'Ruff findings changed by path')
finally:
 newfile.unlink(missing_ok=True)
execute('CONTROL_AFTER_ALL_RESTORED',0,'PROPOSED_BASELINE_EXACT_MATCH: 51')
assert not subprocess.check_output(['git','status','--porcelain'],cwd=R)
raw=receipt.read_bytes()
print('EXPERIMENT_HEAD',head,'RECOVERY_CLEAN','YES','RECEIPT_BYTES',len(raw),'SHA256',sha(raw),'DONE',datetime.datetime.now().isoformat(),flush=True)
