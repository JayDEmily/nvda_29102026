import hashlib
import json
from pathlib import Path
import subprocess

out = Path(__file__).parent
source = Path('/workspace/scratch/83dd7c79f14f/NVDA_V2_CLEAN_RECOVERED_REPO_20261022')
root = Path((out / 'private_path.txt').read_text().strip())
def git(*args): return subprocess.check_output(['git', *args], cwd=root)
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
tracked = [p for p in git('ls-files', '-z').decode().split('\0') if p]
assert all((root / p).read_bytes() == (source / p).read_bytes() for p in tracked)
assert all((root / p).stat().st_ino != (source / p).stat().st_ino for p in tracked)
api = 'src/nvda_desk/market_measurement_truth/api.py'
assert (root / api).read_bytes().startswith(git('show', '7b141bd:' + api))
changed = git('diff', '--name-only', 'cde2c85', 'HEAD', '--', 'src', 'tests', 'tools', 'config', 'schemas', 'implementation').decode().splitlines()
assert changed == ['src/nvda_desk/market_measurement_truth/_trade_direction.py']
old_tracked = git('ls-tree', '-r', '--name-only', '7b141bd', 'src', 'tests', 'config/product_proof', 'implementation/authority', 'handoff/foundation_implementation/authority').decode().splitlines()
protected = [p for p in old_tracked if p != api]
assert all((root / p).read_bytes() == git('show', '7b141bd:' + p) for p in protected)
assert sha(root / 'handoff/foundation_implementation/d015_execution/implementation_review_initial.md') == 'cec111451e205ec53b68ac8585793ac07fbd81426c7e90840db9663298bcc15e'
assert sha(root / 'handoff/foundation_implementation/d015_execution/factory_first_failure.log') == 'd9faa31b76d337b99566199ca68a4c53eb9c417aacef9207f5000c2a9d5326c1'
expected = {
    'handoff/foundation_implementation/authority/D015_IMPLEMENTATION_BRIEF.md': '84baa16665db5f8543eba3b1770dafcfb36cc5e8064b2f1837beb924713acb0d',
    'handoff/foundation_implementation/authority/D015_PROOF_CONTRACT.json': 'e4d481ca99dbb55e2ad4b753dc33b8ba244873eac50e541a8352a6f5384a73c5',
    'config/product_proof/market_measurement_d015/generations/0001.json': 'd495a09f834349b7817a28911a58afa372b635ed0d1d211efd4fc8a4f822e543',
    'tests/product/market_measurement_d015/test_trade_direction.py': '95de43d4538ee3b302430c7c6455edef0373e6bb09ee2f2cb111bfc54178f2fc',
}
assert all(sha(root / p) == v for p,v in expected.items())
assert git('status', '--porcelain=v1') == b''
result = {'candidate': git('rev-parse', 'HEAD').decode().strip(), 'tree': git('rev-parse', 'HEAD^{tree}').decode().strip(), 'private_clean': True, 'tracked_files_identical_to_active': len(tracked), 'preserved_previous_production_and_proof_paths': len(protected), 'old_api_byte_prefix_identical': True, 'only_successor_production_change': changed, 'initial_return_and_first_failure_preserved': True, 'verified_hashes': expected, 'new_service_sha256': sha(root / 'src/nvda_desk/market_measurement_truth/_trade_direction.py'), 'new_store_sha256': sha(root / 'src/nvda_desk/market_measurement_truth/_trade_direction_sqlite.py')}
out.joinpath('06_audit.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
