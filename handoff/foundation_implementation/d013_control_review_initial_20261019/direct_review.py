"""Independent public-loader probes; no Worker fixture imports or domain execution."""
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path('/workspace/scratch/d549b6d808a9/d013-review-9IMqxv/repository')
sys.path[:0] = [str(ROOT / 'tools'), str(ROOT / 'src')]
from product_proof_claims import load_product_proof_claim

CLAIMS = ('raw_signal_occurrence_truth_sqlite', 'neutral_market_measurement_truth_pilot', 'neutral_market_measurement_truth_d012')
NEW = 'neutral_market_measurement_truth_d013'
CONFIG = ROOT / 'config/product_proof/market_measurement_d013'
PHYSICAL = ROOT / 'tests/product/market_measurement_d013'
BRIEF = 'handoff/foundation_implementation/authority/G6_1_D013_IMPLEMENTATION_BRIEF_PROPOSED.md'
BINDING = 'implementation/authority/G6_1_D013_IMPLEMENTATION_AUTHORITY_BINDING.yaml'
CONTRACT = 'handoff/foundation_implementation/authority/G6_1_D013_PROOF_CONTRACT_PROPOSED.json'

def resolve(label, selected=CLAIMS):
    result = {}
    for claim in selected:
        value = load_product_proof_claim(ROOT, claim)
        result[claim] = (value.state, value.authority_sha256, value.generation_sha256)
    print(label, json.dumps(result, sort_keys=True))
    return result

def rejected(label, selected=CLAIMS):
    for claim in selected:
        try:
            load_product_proof_claim(ROOT, claim)
        except (ValueError, OSError) as exc:
            print(label, claim, type(exc).__name__, str(exc))
        else:
            raise AssertionError((label, claim, 'unexpected acceptance'))

assert (ROOT / 'tests/product/market_measurement_d012/test_spread.py').is_file()
assert not PHYSICAL.exists() and not CONFIG.exists()
baseline = resolve('ACTUAL_BASELINE')
assert all(row[0] == 'READY_FOR_PROOF' for row in baseline.values())
for name in ('_support.py', 'nested/helper.py', 'test_orphan.py', 'dangling.py'):
    path = PHYSICAL / name
    path.parent.mkdir(parents=True, exist_ok=True)
    if name == 'dangling.py':
        path.symlink_to('absent-target.py')
    else:
        path.write_text('# Independent undeclared-source canary, not domain proof.\n')
    rejected('ABSENT_DESCRIPTOR_' + name)
    path.unlink()
    if path.parent != PHYSICAL:
        path.parent.rmdir()
PHYSICAL.rmdir()
assert resolve('RESTORED_BASELINE') == baseline

descriptor = dict(schema_version='1.0', claim_id=NEW, brief_path=BRIEF,
                  binding_path=BINDING, contract_path=CONTRACT,
                  physical_root='tests/product/market_measurement_d013',
                  admission_path='config/product_proof/market_measurement_d013/admission.json')
CONFIG.mkdir()
path = CONFIG / 'claim.json'
path.write_text(json.dumps(descriptor))
(CONFIG / 'admission.json').write_text(json.dumps(dict(schema_version='1.0', current_generation=None)))
assert resolve('BOTH_DESCRIPTORS_OLD_GENERATIONS') == baseline
new_value = resolve('NEW_NULL_NO_PHYSICAL', (NEW,))[NEW]
assert new_value[0] == 'INCOMPLETE_NO_PHYSICAL_FAMILIES' and new_value[2] is None
assert new_value[1] == hashlib.sha256((ROOT / BRIEF).read_bytes()).hexdigest()
path.write_text(json.dumps({**descriptor, 'extra': True}))
rejected('MALFORMED_DESCRIPTOR_ALL_SELECTED', (*CLAIMS, NEW))
path.write_text(json.dumps(descriptor))
binding = ROOT / BINDING
original = binding.read_bytes()
binding.write_bytes(original.replace(b'1f53d9c21c6eb4b90213137c4699a0688f994cd0ed55e54082268d8477abc148', b'a31c482d2dc4822539ede99e955761319585af4badea93b9fc279638e1e1f393'))
rejected('DIFFERENT_AUTHORITY_ALL_SELECTED', (*CLAIMS, NEW))
binding.write_bytes(original)
assert resolve('RESTORED_BOTH_DESCRIPTORS') == baseline
(CONFIG / 'admission.json').unlink()
path.unlink()
CONFIG.rmdir()
assert resolve('FINAL_BASELINE') == baseline
print('DIRECT_REVIEW_PASS')
