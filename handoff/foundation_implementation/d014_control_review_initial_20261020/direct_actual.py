"""Independent literal actual-state public-loader probes; no Worker helpers."""
from pathlib import Path
import subprocess
import shutil
import sys
import json
import hashlib

base = Path(__file__).resolve().parent
root = base / 'actual-state-v2'
subprocess.run(['git', 'clone', '--no-hardlinks', '/workspace/scratch/d549b6d808a9/g52-recovery/repository', str(root)], check=True)
shutil.copyfile(base / 'proposed/tools/product_proof_claims.py', root / 'tools/product_proof_claims.py')
sys.path[:0] = [str(root / 'tools'), str(root / 'src')]
from product_proof_claims import load_product_proof_claim

old = ['raw_signal_occurrence_truth_sqlite', 'neutral_market_measurement_truth_pilot', 'neutral_market_measurement_truth_d012', 'neutral_market_measurement_truth_d013']
new = 'neutral_market_measurement_truth_d014'
selected = old + [new]
directory = root / 'config/product_proof/market_measurement_d014'
descriptor = directory / 'claim.json'
pointer = directory / 'admission.json'
entry = {
 'schema_version': '1.0', 'claim_id': new,
 'brief_path': 'handoff/foundation_implementation/authority/G6_1_D014_IMPLEMENTATION_BRIEF_PROPOSED.md',
 'binding_path': 'implementation/authority/G6_1_D014_IMPLEMENTATION_AUTHORITY_BINDING.yaml',
 'contract_path': 'handoff/foundation_implementation/authority/G6_1_D014_PROOF_CONTRACT_PROPOSED.json',
 'physical_root': 'tests/product/market_measurement_d014',
 'admission_path': 'config/product_proof/market_measurement_d014/admission.json',
}
def write(path, value):
 path.parent.mkdir(parents=True, exist_ok=True)
 path.write_text(json.dumps(value, indent=2) + '\n')
def digest(path):
 return hashlib.sha256(path.read_bytes()).hexdigest()
def states(ids):
 result = {identity: load_product_proof_claim(root, identity).state for identity in ids}
 print(result, flush=True)
 return result
def rejects(label):
 for identity in selected:
  try:
   load_product_proof_claim(root, identity)
  except (ValueError, OSError) as exc:
   print(label, identity, type(exc).__name__, str(exc), flush=True)
  else:
   raise AssertionError((label, identity, 'unexpected acceptance'))
protected = {p: p.read_bytes() for p in (root / 'config/product_proof').rglob('*.json')}
initial = states(old)
assert set(initial.values()) == {'READY_FOR_PROOF'}
write(descriptor, entry)
write(pointer, {'schema_version':'1.0', 'current_generation':None})
assert not (root / entry['physical_root']).exists()
assert states(old) == initial
assert states([new])[new] == 'INCOMPLETE_NO_PHYSICAL_FAMILIES'
print('literal descriptor/null, no physical family: PASS', flush=True)
descriptor.unlink()
for name in ['_support.py', 'nested/helper.py', 'test_orphan.py', 'dangling.py']:
 path = root / entry['physical_root'] / name
 path.parent.mkdir(parents=True, exist_ok=True)
 if name == 'dangling.py':
  path.symlink_to('missing.py')
 else:
  path.write_text('# temporary independent ownership falsifier\n')
 rejects('absent-descriptor/' + name)
 path.unlink()
 assert not path.exists() and not path.is_symlink(), str(path)
 print('removed direct falsifier', path, flush=True)
 assert states(old) == initial
write(descriptor, entry)
descriptor.write_text('{')
rejects('malformed descriptor')
write(descriptor, dict(entry, physical_root='tests/product/market_measurement_d013'))
rejects('overlap descriptor')
write(descriptor, entry)
foreign = root / 'config/product_proof/market_measurement_d013/generations/0001.json'
write(pointer, {'schema_version':'1.0', 'current_generation':{'path':foreign.relative_to(root).as_posix(), 'sha256':digest(foreign)}})
rejects('cross-claim generation')
write(pointer, {'schema_version':'1.0', 'current_generation':None})
for identity, name in zip(old, ['raw_signal_sqlite','market_measurement','market_measurement_d012','market_measurement_d013']):
 p = root / 'config/product_proof' / name / 'admission.json'
 original_pointer = p.read_bytes()
 reference = json.loads(original_pointer)['current_generation']
 prior = root / reference['path']
 prior_bytes = prior.read_bytes()
 record = json.loads(prior_bytes)
 record.update(generation=record['generation']+1, previous_generation=reference, adequacy_review_ref='independent-control-fiction/review', admission_authority_ref='independent-control-fiction/admission')
 successor = prior.parent / ('%04d.json' % record['generation'])
 assert not successor.exists()
 write(successor, record)
 write(p, {'schema_version':'1.0','current_generation':{'path':successor.relative_to(root).as_posix(),'sha256':digest(successor)}})
 assert states([identity])[identity] == 'READY_FOR_PROOF'
 assert load_product_proof_claim(root, identity).generation_sha256 == digest(successor)
 assert prior.read_bytes() == prior_bytes
 write(p, {'schema_version':'1.0','current_generation':None})
 assert states([identity])[identity] == 'INCOMPLETE_COVERAGE'
 assert prior.read_bytes() == prior_bytes
 successor.unlink()
 p.write_bytes(original_pointer)
 print('advance/revoke retained immutable generation:', identity, 'PASS', flush=True)
assert states(old) == initial
assert all(path.read_bytes() == data for path,data in protected.items())
print('ALL DIRECT ACTUAL-STATE PROBES PASS; no Worker fixture/helper used; no domain proof', flush=True)
