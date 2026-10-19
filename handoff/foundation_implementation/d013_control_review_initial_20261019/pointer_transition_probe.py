"""Synthetic admission-control advancement, never a real proof admission."""
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

ROOT = Path('/workspace/scratch/d549b6d808a9/d013-review-9IMqxv/repository')
sys.path[:0] = [str(ROOT / 'tools'), str(ROOT / 'src')]
from product_proof_claims import load_product_proof_claim

directory = ROOT / 'config/product_proof/market_measurement_d012'
pointer = directory / 'admission.json'
original = pointer.read_bytes()
ref = json.loads(original)['current_generation']
generation = json.loads((ROOT / ref['path']).read_text())
assert generation['generation'] == 1
generation.update(generation=2, previous_generation=ref,
                  adequacy_review_ref='independent-control-canary/new-review',
                  admission_authority_ref='independent-control-canary/new-admission')
path = directory / 'generations/0002.json'
assert not path.exists()
try:
    path.write_text(json.dumps(generation, indent=2) + '\n')
    pointer.write_text(json.dumps(dict(schema_version='1.0', current_generation=dict(
        path=path.relative_to(ROOT).as_posix(), sha256=hashlib.sha256(path.read_bytes()).hexdigest()))))
    value = load_product_proof_claim(ROOT, 'neutral_market_measurement_truth_d012')
    print('CONTROL_SYNTHETIC_ADVANCE', value.state, value.generation_sha256)
    assert value.state == 'READY_FOR_PROOF'
    spec = importlib.util.spec_from_file_location('reviewed_control_tests', ROOT / 'tests/architecture/test_proof_control.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    try:
        module.test_d013_actual_original_claim_generations_are_preserved()
    except AssertionError:
        print('CURRENT_POINTER_PIN_REJECTS_CONTROL_VALID_ADVANCE: AssertionError')
    else:
        raise AssertionError('expected checkpoint-pin false rejection did not occur')
finally:
    pointer.write_bytes(original)
    path.unlink()
print('ORIGINAL_POINTER_AND_GEN1_RESTORED', load_product_proof_claim(ROOT, 'neutral_market_measurement_truth_d012').generation_sha256)
