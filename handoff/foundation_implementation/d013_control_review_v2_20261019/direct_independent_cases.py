"""One fresh actual-state copy per mutation; no cleanup transition or Worker helper."""
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import sys

BASE = Path('/workspace/scratch/d549b6d808a9/d013-v2-review-ONLCfC/suite-repository')
sys.path[:0] = [str(BASE / 'tools'), str(BASE / 'src')]
from product_proof_claims import load_product_proof_claim

CLAIMS = {'raw_signal_occurrence_truth_sqlite': 'raw_signal_sqlite',
          'neutral_market_measurement_truth_pilot': 'market_measurement',
          'neutral_market_measurement_truth_d012': 'market_measurement_d012'}
NEW = 'neutral_market_measurement_truth_d013'
spec = importlib.util.spec_from_file_location('reviewed_cases', BASE / 'tests/architecture/test_proof_control.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

def fresh(name):
    root = BASE.parent / 'independent-cases' / name
    shutil.copytree(BASE, root, ignore=shutil.ignore_patterns('__pycache__'))
    return root

def old_records(root):
    return {p: p.read_bytes() for directory in CLAIMS.values()
            for p in (root / 'config/product_proof' / directory / 'generations').glob('*.json')}

def proposition(root, old):
    module.ROOT = root
    module.test_d013_actual_original_claim_generations_are_preserved()
    assert all(p.read_bytes() == raw for p, raw in old.items())

for claim_id, directory in CLAIMS.items():
    for transition in ('advance', 'revoke'):
        root = fresh(directory + '-' + transition)
        old = old_records(root)
        baseline = load_product_proof_claim(root, claim_id)
        assert baseline.state == 'READY_FOR_PROOF' and baseline.claim_id == claim_id
        pointer = root / 'config/product_proof' / directory / 'admission.json'
        ref = json.loads(pointer.read_text())['current_generation']
        if transition == 'advance':
            record = json.loads((root / ref['path']).read_text())
            record.update(generation=record['generation'] + 1, previous_generation=ref,
                          adequacy_review_ref='independent-canary/fresh-review',
                          admission_authority_ref='independent-canary/fresh-admission')
            path = pointer.parent / 'generations' / f"{record['generation']:04d}.json"
            assert not path.exists()
            path.write_text(json.dumps(record, indent=2) + '\n')
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            pointer.write_text(json.dumps(dict(schema_version='1.0', current_generation=dict(
                path=path.relative_to(root).as_posix(), sha256=digest))))
            value = load_product_proof_claim(root, claim_id)
            assert value.claim_id == claim_id and value.state == 'READY_FOR_PROOF' and value.generation_sha256 == digest
        else:
            pointer.write_text(json.dumps(dict(schema_version='1.0', current_generation=None)))
            value = load_product_proof_claim(root, claim_id)
            assert value.claim_id == claim_id and value.state == 'INCOMPLETE_COVERAGE' and value.generation_sha256 is None
        proposition(root, old)
        print('DIRECT_TRANSITION_PASS', claim_id, transition, value.state, value.generation_sha256, flush=True)

for index, name in enumerate(('_support.py', 'nested/helper.py', 'test_orphan.py', 'dangling.py')):
    root = fresh('orphan-' + str(index))
    path = root / 'tests/product/market_measurement_d013' / name
    path.parent.mkdir(parents=True, exist_ok=True)
    if name == 'dangling.py':
        path.symlink_to('absent-target.py')
    else:
        path.write_text('# Independent control-only unowned source.\n')
    for claim_id in CLAIMS:
        try:
            load_product_proof_claim(root, claim_id)
        except ValueError as exc:
            assert 'unowned' in str(exc) or 'symlink' in str(exc)
        else:
            raise AssertionError((name, claim_id))
    print('DIRECT_ORPHAN_ALL_THREE_REJECT', name, flush=True)

root = fresh('descriptor')
config = root / 'config/product_proof/market_measurement_d013'
config.mkdir()
prefix = 'handoff/foundation_implementation/authority/G6_1_D013_'
descriptor = dict(schema_version='1.0', claim_id=NEW,
                  brief_path=prefix + 'IMPLEMENTATION_BRIEF_PROPOSED.md',
                  binding_path='implementation/authority/G6_1_D013_IMPLEMENTATION_AUTHORITY_BINDING.yaml',
                  contract_path=prefix + 'PROOF_CONTRACT_PROPOSED.json',
                  physical_root='tests/product/market_measurement_d013',
                  admission_path='config/product_proof/market_measurement_d013/admission.json')
path = config / 'claim.json'
path.write_text(json.dumps(descriptor))
(config / 'admission.json').write_text(json.dumps(dict(schema_version='1.0', current_generation=None)))
proposition(root, old_records(root))
assert load_product_proof_claim(root, NEW).state == 'INCOMPLETE_NO_PHYSICAL_FAMILIES'
print('DIRECT_COMBINED_DESCRIPTOR_NEW_INCOMPLETE_PASS', flush=True)
path.write_text(json.dumps({**descriptor, 'extra': True}))
for claim_id in (*CLAIMS, NEW):
    try:
        load_product_proof_claim(root, claim_id)
    except ValueError as exc:
        assert 'invalid D013 extension descriptor' in str(exc)
    else:
        raise AssertionError(claim_id)
print('DIRECT_MALFORMED_DESCRIPTOR_ALL_FOUR_REJECT', flush=True)
print('DIRECT_INDEPENDENT_CASES_PASS', flush=True)
