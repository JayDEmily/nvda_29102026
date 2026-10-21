"""Required section 7.3.4 checks, serial, exact candidate, binary output, first stop."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

root = Path(sys.argv[1]).resolve()
out = Path(sys.argv[2]).resolve()
out.mkdir(exist_ok=False)

def git(*args):
    return subprocess.check_output(['git', '-C', str(root), *args]).decode().strip()

head = git('rev-parse', 'HEAD')
tree = git('rev-parse', 'HEAD^{tree}')
env = os.environ.copy()
env.update(PYTHONUNBUFFERED='1', TMPDIR=str(out), MYPY_CACHE_DIR=str(out / 'mypy-cache'))
env.pop('PYTEST_ADDOPTS', None)
commands = []
for label, aggregate in [
    ('d014', 'neutral_market_measurement_truth_d014'),
    ('d013', 'neutral_market_measurement_truth_d013'),
    ('d012', 'neutral_market_measurement_truth_d012'),
    ('foundation', 'neutral_market_measurement_truth_pilot'),
    ('m00', 'raw_signal_occurrence_truth_sqlite'),
]:
    commands.append((label, ['tools/run_product_proof_gate.py', '--aggregate', aggregate],
                     b'observed aggregate outcome: exit=0'))
commands.extend([
    ('mypy', ['-m', 'mypy', 'src', 'tools/product_proof_claims.py',
              'tools/product_proof_outcomes.py', 'tools/validate_product_proof.py',
              'tools/run_product_proof_gate.py'], b'Success: no issues found'),
    ('scoped_ruff', ['-m', 'ruff', 'check',
                    'src/nvda_desk/market_measurement_truth/api.py',
                    'src/nvda_desk/market_measurement_truth/_rational.py',
                    'src/nvda_desk/market_measurement_truth/_raw_rational.py',
                    'src/nvda_desk/market_measurement_truth/_raw_rational_sqlite.py'],
                    b'All checks passed!'),
    ('promotion', ['tools/run_promotion_gate.py', '--set', 'architecture_kernel'], None),
])
assert not git('status', '--porcelain=v1', '--untracked-files=all')
for name, args, marker in commands:
    assert git('rev-parse', 'HEAD') == head
    assert not git('status', '--porcelain=v1', '--untracked-files=all')
    argv = [sys.executable, *args]
    log = out / (name + '.log')
    metadata = out / (name + '.json')
    record = dict(candidate=head, tree=tree, argv=argv, cwd=str(root),
                  reason='mandatory exact-candidate validation under root 7.3.4',
                  started_utc=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()))
    print('START', name, flush=True)
    start = time.monotonic()
    with log.open('xb') as stream:
        result = subprocess.run(argv, cwd=root, env=env, stdout=stream, stderr=subprocess.STDOUT)
    data = log.read_bytes()
    record.update(exit=result.returncode, duration_seconds=time.monotonic()-start,
                  log_sha256=hashlib.sha256(data).hexdigest(),
                  marker_present=marker is None or marker in data,
                  unchanged_head=git('rev-parse', 'HEAD') == head,
                  clean_after=not git('status', '--porcelain=v1', '--untracked-files=all'))
    metadata.write_text(json.dumps(record, indent=2)+'\n')
    print('END', name, json.dumps(record), flush=True)
    if result.returncode or not all(record[k] for k in ['marker_present','unchanged_head','clean_after']):
        raise SystemExit('FIRST_UNMET_CANDIDATE_INVARIANT ' + name)
print('ALL_REQUIRED_CANDIDATE_COMMANDS_COMPLETED', head, flush=True)
