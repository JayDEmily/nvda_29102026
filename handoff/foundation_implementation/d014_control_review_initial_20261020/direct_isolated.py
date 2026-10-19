"""Pristine per-witness copies; independent literal loader, no test helpers."""
from pathlib import Path
import sys, subprocess, shutil, json, hashlib

base = Path(__file__).resolve().parent
old = ['raw_signal_occurrence_truth_sqlite', 'neutral_market_measurement_truth_pilot', 'neutral_market_measurement_truth_d012', 'neutral_market_measurement_truth_d013']
new = 'neutral_market_measurement_truth_d014'
selected = old + [new]
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p, obj):
 p.parent.mkdir(parents=True, exist_ok=True)
 p.write_text(json.dumps(obj, indent=2)+'\n')
if len(sys.argv) == 1:
 jobs = [('null', 'all')]
 jobs += [(case, identity) for case in ['support','nested','test','dangling','malformed','overlap','crossgen'] for identity in selected]
 jobs += [(phase, identity) for phase in ['advance','revoke'] for identity in old]
 for i,(case,identity) in enumerate(jobs):
  argv = [sys.executable, str(Path(__file__).resolve()), str(i), case, identity]
  result = subprocess.run(argv, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
  print(result.stdout.decode(), end='', flush=True)
  assert result.returncode == 0, (case,identity,result.returncode)
 print('ALL 44 PRISTINE INDEPENDENT ACTUAL-STATE CASES PASS', flush=True)
 raise SystemExit
i, case, identity = sys.argv[1:]
root = base / ('isolated-'+i)
subprocess.run(['git','clone','--shared','-q','/workspace/scratch/d549b6d808a9/g52-recovery/repository',str(root)],check=True)
shutil.copyfile(base/'proposed/tools/product_proof_claims.py',root/'tools/product_proof_claims.py')
sys.path[:0] = [str(root/'tools'),str(root/'src')]
from product_proof_claims import load_product_proof_claim as load
assert Path(sys.modules['product_proof_claims'].__file__).resolve() == root/'tools/product_proof_claims.py'
protected = {p:p.read_bytes() for p in (root/'config/product_proof').rglob('*.json')}
for original in old:
 assert load(root,original).state == 'READY_FOR_PROOF'
directory = root/'config/product_proof/market_measurement_d014'
entry = {'schema_version':'1.0','claim_id':new,
 'brief_path':'handoff/foundation_implementation/authority/G6_1_D014_IMPLEMENTATION_BRIEF_PROPOSED.md',
 'binding_path':'implementation/authority/G6_1_D014_IMPLEMENTATION_AUTHORITY_BINDING.yaml',
 'contract_path':'handoff/foundation_implementation/authority/G6_1_D014_PROOF_CONTRACT_PROPOSED.json',
 'physical_root':'tests/product/market_measurement_d014','admission_path':'config/product_proof/market_measurement_d014/admission.json'}
descriptor=directory/'claim.json'; pointer=directory/'admission.json'
if case in ['support','nested','test','dangling']:
 name={'support':'_support.py','nested':'nested/helper.py','test':'test_orphan.py','dangling':'dangling.py'}[case]
 p=root/entry['physical_root']/name; p.parent.mkdir(parents=True,exist_ok=True)
 if case=='dangling': p.symlink_to('missing.py')
 else: p.write_text('# independent control-only orphan\n')
 assert not descriptor.exists()
else:
 write(descriptor,entry); write(pointer,{'schema_version':'1.0','current_generation':None})
 if case=='malformed': descriptor.write_text('{')
 if case=='overlap': write(descriptor,dict(entry,physical_root='tests/product/market_measurement_d013'))
 if case=='crossgen':
  foreign=root/'config/product_proof/market_measurement_d013/generations/0001.json'
  write(pointer,{'schema_version':'1.0','current_generation':{'path':foreign.relative_to(root).as_posix(),'sha256':sha(foreign)}})
if case=='null':
 assert not (root/entry['physical_root']).exists()
 assert load(root,new).state=='INCOMPLETE_NO_PHYSICAL_FAMILIES'
 for original in old: assert load(root,original).state=='READY_FOR_PROOF'
elif case in ['advance','revoke']:
 name=dict(zip(old,['raw_signal_sqlite','market_measurement','market_measurement_d012','market_measurement_d013']))[identity]
 p=root/'config/product_proof'/name/'admission.json'
 reference=json.loads(p.read_text())['current_generation']; prior=root/reference['path']; prior_bytes=prior.read_bytes()
 if case=='advance':
  record=json.loads(prior_bytes); record.update(generation=record['generation']+1,previous_generation=reference,adequacy_review_ref='independent-control-fiction/review',admission_authority_ref='independent-control-fiction/admission')
  successor=prior.parent/('%04d.json'%record['generation']); write(successor,record)
  write(p,{'schema_version':'1.0','current_generation':{'path':successor.relative_to(root).as_posix(),'sha256':sha(successor)}})
  claim=load(root,identity); assert claim.state=='READY_FOR_PROOF' and claim.generation_sha256==sha(successor)
 else:
  write(p,{'schema_version':'1.0','current_generation':None})
  assert load(root,identity).state=='INCOMPLETE_COVERAGE'
 assert prior.read_bytes()==prior_bytes
 protected.pop(p)
else:
 try: load(root,identity)
 except (ValueError,OSError) as exc: print(case,identity,type(exc).__name__,str(exc),flush=True)
 else: raise AssertionError((case,identity,'accepted invalid control'))
 if case in ['support','nested','test','dangling']: assert p.is_file() or p.is_symlink()
assert all(p.read_bytes()==data for p,data in protected.items())
print('PASS',i,case,identity,'old bytes retained',flush=True)
