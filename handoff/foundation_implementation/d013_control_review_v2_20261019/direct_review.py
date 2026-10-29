"""Independent V2 public-loader transitions, no Worker copy/generation helpers."""
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import sys

ROOT = Path('/workspace/scratch/d549b6d808a9/d013-v2-review-ONLCfC/direct-repository')
BASE = Path('/workspace/scratch/d549b6d808a9/d013-v2-review-ONLCfC/suite-repository')
sys.path[:0] = [str(ROOT / 'tools'), str(ROOT / 'src')]
from product_proof_claims import load_product_proof_claim

CLAIMS = {
    'raw_signal_occurrence_truth_sqlite': 'raw_signal_sqlite',
    'neutral_market_measurement_truth_pilot': 'market_measurement',
    'neutral_market_measurement_truth_d012': 'market_measurement_d012',
}
NEW = 'neutral_market_measurement_truth_d013'
spec = importlib.util.spec_from_file_location('reviewed_control_tests', ROOT / 'tests/architecture/test_proof_control.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
assert module.ROOT == ROOT
baseline_files = {
    p: p.read_bytes() for directory in CLAIMS.values()
    for p in (ROOT / 'config/product_proof' / directory).rglob('*.json')
}

def preservation():
    # Invoke only the reviewed proposition, never its composition/copy helpers.
    module.test_d013_actual_original_claim_generations_are_preserved()
    assert all(p.read_bytes() == raw for p, raw in baseline_files.items() if p.name != 'admission.json')

assert (ROOT / 'tests/product/market_measurement_d012/test_spread.py').is_file()
assert not (ROOT / 'tests/product/market_measurement_d013').exists()
assert not (ROOT / 'config/product_proof/market_measurement_d013').exists()
for claim_id, directory in CLAIMS.items():
    # An independent full copy per claim avoids carrying a control-only
    # revoked/advanced namespace into another claim's positive precondition.
    ROOT = BASE.parent / ('sequence-' + directory)
    shutil.copytree(BASE, ROOT, ignore=shutil.ignore_patterns('__pycache__'))
    module.ROOT = ROOT
    baseline_files = {
        p: p.read_bytes() for item in CLAIMS.values()
        for p in (ROOT / 'config/product_proof' / item).rglob('*.json')
    }
    value = load_product_proof_claim(ROOT, claim_id)
    assert value.state == 'READY_FOR_PROOF'
    print('BASELINE', claim_id, value.state, value.authority_sha256, value.generation_sha256, flush=True)
    pointer = ROOT / 'config/product_proof' / directory / 'admission.json'
    raw_pointer = pointer.read_bytes()
    old_ref = json.loads(raw_pointer)['current_generation']
    old_generation = ROOT / old_ref['path']
    old_raw = old_generation.read_bytes()
    generation = json.loads(old_raw)
    generation.update(generation=generation['generation'] + 1, previous_generation=old_ref,
                      adequacy_review_ref='independent-control-canary/new-review',
                      admission_authority_ref='independent-control-canary/new-admission')
    path = pointer.parent / 'generations' / f"{generation['generation']:04d}.json"
    assert not path.exists()
    try:
        path.write_text(json.dumps(generation, indent=2) + '\n')
        new_hash = hashlib.sha256(path.read_bytes()).hexdigest()
        pointer.write_text(json.dumps(dict(schema_version='1.0', current_generation=dict(
            path=path.relative_to(ROOT).as_posix(), sha256=new_hash))))
        value = load_product_proof_claim(ROOT, claim_id)
        assert value.claim_id == claim_id and value.state == 'READY_FOR_PROOF' and value.generation_sha256 == new_hash
        preservation()
        assert old_generation.read_bytes() == old_raw
        print('ADVANCE_ACCEPTED_PRESERVATION_PASS', claim_id, new_hash, flush=True)
    finally:
        pointer.write_bytes(raw_pointer)
        path.unlink()
        assert not path.exists()
    try:
        pointer.write_text(json.dumps(dict(schema_version='1.0', current_generation=None)))
        value = load_product_proof_claim(ROOT, claim_id)
        assert value.claim_id == claim_id and value.state == 'INCOMPLETE_COVERAGE' and value.generation_sha256 is None
        preservation()
        assert old_generation.read_bytes() == old_raw
        print('REVOCATION_ACCEPTED_PRESERVATION_PASS', claim_id, flush=True)
    finally:
        pointer.write_bytes(raw_pointer)
    assert all(p.read_bytes() == raw for p, raw in baseline_files.items())

physical = ROOT / 'tests/product/market_measurement_d013'
for name in ('_support.py', 'nested/helper.py', 'test_orphan.py', 'dangling.py'):
    path = physical / name
    path.parent.mkdir(parents=True, exist_ok=True)
    if name == 'dangling.py':
        path.symlink_to('absent-target.py')
    else:
        path.write_text('# Independent unowned Python canary, not domain proof.\n')
    for claim_id in CLAIMS:
        try:
            load_product_proof_claim(ROOT, claim_id)
        except ValueError as exc:
            assert 'unowned' in str(exc) or 'symlink' in str(exc)
            print('ORPHAN_REJECTED', name, claim_id, str(exc), flush=True)
        else:
            raise AssertionError((name, claim_id))
    path.unlink()
    if path.parent != physical:
        path.parent.rmdir()
physical.rmdir()

config = ROOT / 'config/product_proof/market_measurement_d013'
config.mkdir()
descriptor = {
    'schema_version': '1.0', 'claim_id': NEW,
    'brief_path': 'handoff/foundation_implementation/authority/G6_1_D013_IMPLEMENTATION_BRIEF_PROPOSED.md',
    'binding_path': 'implementation/authority/G6_1_D013_IMPLEMENTATION_AUTHORITY_BINDING.yaml',
    'contract_path': 'handoff/foundation_implementation/authority/G6_1_D013_PROOF_CONTRACT_PROPOSED.json',
    'physical_root': 'tests/product/market_measurement_d013',
    'admission_path': 'config/product_proof/market_measurement_d013/admission.json',
}
path = config / 'claim.json'
path.write_text(json.dumps(descriptor))
admission = config / 'admission.json'
admission.write_text(json.dumps(dict(schema_version='1.0', current_generation=None)))
preservation()
assert load_product_proof_claim(ROOT, NEW).state == 'INCOMPLETE_NO_PHYSICAL_FAMILIES'
print('COMBINED_DESCRIPTORS_PRESERVE_ORIGINALS_NEW_INCOMPLETE', flush=True)
path.write_text(json.dumps({**descriptor, 'extra': True}))
for claim_id in (*CLAIMS, NEW):
    try:
        load_product_proof_claim(ROOT, claim_id)
    except ValueError as exc:
        assert 'invalid D013 extension descriptor' in str(exc)
        print('MALFORMED_ALL_SELECTED_REJECTED', claim_id, str(exc), flush=True)
    else:
        raise AssertionError(claim_id)
admission.unlink()
path.unlink()
config.rmdir()
preservation()
assert all(p.read_bytes() == raw for p, raw in baseline_files.items())
print('DIRECT_V2_REVIEW_PASS', flush=True)
