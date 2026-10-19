"""One bounded literal-only actual-state transition diagnostic; no Worker helpers."""
from pathlib import Path
import sys
import json
import hashlib
import subprocess
import importlib

BASE = Path(__file__).resolve().parent
ROOT = BASE / 'candidate'
OLD = ('raw_signal_occurrence_truth_sqlite', 'neutral_market_measurement_truth_pilot',
       'neutral_market_measurement_truth_d012', 'neutral_market_measurement_truth_d013')
NEW = 'neutral_market_measurement_truth_d014'
MODULE = ROOT / 'tools/product_proof_claims.py'
EXPECTED_MODULE_SHA = 'b2670e26f51d4b6f4fc8c656c859b9e5d63ca9aadd84ff2f818ff06cd9bb118a'
DIR = ROOT / 'config/product_proof/market_measurement_d014'
DESCRIPTOR = DIR / 'claim.json'
POINTER = DIR / 'admission.json'
PHYSICAL = ROOT / 'tests/product/market_measurement_d014'
ENTRY = {
    'schema_version': '1.0', 'claim_id': NEW,
    'brief_path': 'handoff/foundation_implementation/authority/G6_1_D014_IMPLEMENTATION_BRIEF_PROPOSED.md',
    'binding_path': 'implementation/authority/G6_1_D014_IMPLEMENTATION_AUTHORITY_BINDING.yaml',
    'contract_path': 'handoff/foundation_implementation/authority/G6_1_D014_PROOF_CONTRACT_PROPOSED.json',
    'physical_root': 'tests/product/market_measurement_d014',
    'admission_path': 'config/product_proof/market_measurement_d014/admission.json',
}
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
def wire(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'))
def emit(value):
    print(wire(value), flush=True)
def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + '\n')

assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip() == 'f01ad17c48f0eb21148cb7b2aa4e2b2f428c0f2b'
assert sha(MODULE) == EXPECTED_MODULE_SHA
assert not DIR.exists() and not PHYSICAL.exists()
sys.path[:0] = [str(ROOT / 'tools'), str(ROOT / 'src')]
api = importlib.import_module('product_proof_claims')
assert Path(api.__file__).resolve() == MODULE
protected = {}
for prefix in ('config/product_proof','tests/product','implementation/authority','handoff/foundation_implementation/authority'):
    for path in (ROOT / prefix).rglob('*'):
        if path.is_file() and '__pycache__' not in path.parts:
            protected[path.relative_to(ROOT).as_posix()] = sha(path)
protected_wire = wire(protected)
protected_digest = hashlib.sha256(protected_wire.encode()).hexdigest()
emit({'initial_manifest':protected, 'manifest_sha256':protected_digest})
call_number = 0
def inventory():
    assert Path(api.__file__).resolve() == MODULE
    assert sha(MODULE) == EXPECTED_MODULE_SHA
    assert all(sha(ROOT/name) == digest for name,digest in protected.items())
    result = {'module_path':str(Path(api.__file__).resolve()), 'module_sha256':sha(MODULE),
              'protected_count':len(protected), 'protected_manifest_sha256':protected_digest,
              'protected_bytes_unchanged':True, 'd014':{}}
    for prefix in (DIR,PHYSICAL):
        if prefix.exists():
            for path in [prefix,*sorted(prefix.rglob('*'))]:
                name=path.relative_to(ROOT).as_posix()
                if path.is_symlink(): row={'kind':'symlink','target':str(path.readlink())}
                elif path.is_file(): row={'kind':'file','sha256':sha(path),'bytes':path.stat().st_size}
                else: row={'kind':'directory'}
                result['d014'][name]=row
    return result
def call(label, identity, expected):
    global call_number
    call_number += 1
    before=inventory()
    emit({'call':call_number,'label':label,'claim':identity,'phase':'before','inventory':before})
    error=None; result=None
    try:
        claim=api.load_product_proof_claim(ROOT,identity)
        result={'claim_id':claim.claim_id,'state':claim.state,'target':claim.target_id,
                'generation_sha256':claim.generation_sha256}
    except (ValueError,OSError) as exc:
        error={'type':type(exc).__name__,'text':str(exc)}
    after=inventory()
    emit({'call':call_number,'label':label,'claim':identity,'phase':'after','inventory':after,
          'result':result,'error':error})
    assert before == after, ('read-side state mutation',label,identity)
    if expected == 'reject-orphan':
        assert error and error['type']=='ValueError' and 'unowned D014 extension Python source without descriptor' in error['text'],(label,identity,result,error)
    else:
        assert error is None and result['state']==expected,(label,identity,result,error)

for identity in OLD: call('initial-original-baseline',identity,'READY_FOR_PROOF')
write(DESCRIPTOR,ENTRY)
write(POINTER,{'schema_version':'1.0','current_generation':None})
assert not PHYSICAL.exists()
for identity in OLD: call('installed-descriptor-null-original',identity,'READY_FOR_PROOF')
call('installed-descriptor-null-new',NEW,'INCOMPLETE_NO_PHYSICAL_FAMILIES')
DESCRIPTOR.unlink()
assert not DESCRIPTOR.exists()
for identity in OLD: call('descriptor-removed-original',identity,'READY_FOR_PROOF')
for name in ('_support.py','nested/helper.py','test_orphan.py','dangling.py'):
    witness=PHYSICAL/name
    witness.parent.mkdir(parents=True,exist_ok=True)
    if name=='dangling.py': witness.symlink_to('absent-target.py')
    else: witness.write_text('# Temporary literal ownership control only, never domain proof.\n')
    assert not DESCRIPTOR.exists() and (witness.is_file() or witness.is_symlink())
    for identity in (*OLD,NEW): call('orphan/'+name,identity,'reject-orphan')
    witness.unlink()
    assert not witness.exists() and not witness.is_symlink()
    emit({'transition':'cleanup/'+name,'inventory':inventory()})
    for identity in OLD: call('cleanup-original/'+name,identity,'READY_FOR_PROOF')
emit({'outcome':'EXACT_INSTALL_NULL_REMOVE_ORPHANS_CLEANUP_SEQUENCE_PASS','calls':call_number,
      'final_inventory':inventory(),'no_domain_proof':True})
