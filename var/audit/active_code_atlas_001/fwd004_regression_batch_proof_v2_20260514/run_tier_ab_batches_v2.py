#!/usr/bin/env python3
import json
import os
import re
import shlex
import signal
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path.cwd()
SRC_AUDIT = ROOT / 'var/audit/active_code_atlas_001/fwd004_regression_batch_proof_20260514'
AUDIT = ROOT / 'var/audit/active_code_atlas_001/fwd004_regression_batch_proof_v2_20260514'
REPORTS = AUDIT / 'reports'
REPORTS.mkdir(parents=True, exist_ok=True)
NODE_SOURCE = SRC_AUDIT / 'TIER_AB_COLLECTED_NODEIDS.txt'
if not NODE_SOURCE.exists():
    raw = ROOT / 'var/audit/active_code_atlas_001/fwd004_regression_batch_proof_20260514/reports/tier_ab_collect_nodeids.raw.out'
    nodes = [line.strip() for line in raw.read_text().splitlines() if line.strip().startswith('tests/') and '::' in line]
else:
    nodes = [line.strip() for line in NODE_SOURCE.read_text().splitlines() if line.strip()]
seen = set(); dups = []
for n in nodes:
    if n in seen: dups.append(n)
    seen.add(n)
BATCH_SIZE = 20
TIMEOUT_SECONDS = 60
batches = [nodes[i:i+BATCH_SIZE] for i in range(0, len(nodes), BATCH_SIZE)]
(AUDIT / 'TIER_AB_COLLECTED_NODEIDS.txt').write_text('\n'.join(nodes) + '\n')
assignments = []
for idx, batch in enumerate(batches, start=1):
    batch_id = f'batch_{idx:02d}'
    (AUDIT / f'TIER_AB_{batch_id}_nodeids.txt').write_text('\n'.join(batch) + '\n')
    cmd_text = ' '.join(['PYTHONPATH=src', 'python', '-m', 'pytest', '-q', *[shlex.quote(n) for n in batch]])
    (REPORTS / f'tier_ab_{batch_id}.cmd').write_text(cmd_text + '\n')
    for offset, nodeid in enumerate(batch):
        assignments.append({'nodeid': nodeid, 'batch': batch_id, 'collection_index_1based': (idx-1)*BATCH_SIZE + offset + 1})
(AUDIT / 'TIER_AB_BATCH_ASSIGNMENTS.json').write_text(json.dumps({
    'batch_size': BATCH_SIZE,
    'timeout_seconds_per_batch': TIMEOUT_SECONDS,
    'collected_count': len(nodes),
    'unique_count': len(seen),
    'duplicate_count': len(dups),
    'duplicates': dups,
    'batch_count': len(batches),
    'assignments': assignments,
}, indent=2, sort_keys=True) + '\n')
summary = {
    'proof_version': 'v2_batch_size_20',
    'source_node_list': str(NODE_SOURCE.relative_to(ROOT)) if NODE_SOURCE.exists() else 'raw_collect_fallback',
    'collected_count': len(nodes),
    'unique_count': len(seen),
    'duplicate_count': len(dups),
    'batch_size': BATCH_SIZE,
    'timeout_seconds_per_batch': TIMEOUT_SECONDS,
    'batch_count': len(batches),
    'batches': [],
}
(REPORTS / 'tier_ab_batch_progress.json').write_text(json.dumps(summary, indent=2, sort_keys=True) + '\n')
passed_total = 0
for idx, batch in enumerate(batches, start=1):
    batch_id = f'batch_{idx:02d}'
    out_path = REPORTS / f'tier_ab_{batch_id}.out'
    err_path = REPORTS / f'tier_ab_{batch_id}.err'
    code_path = REPORTS / f'tier_ab_{batch_id}.exitcode'
    start = time.time()
    env = os.environ.copy(); env['PYTHONPATH'] = 'src'
    timeout_hit = False
    try:
        proc = subprocess.run(
            [sys.executable, '-m', 'pytest', '-q', *batch],
            cwd=ROOT,
            env=env,
            text=True,
            capture_output=True,
            timeout=TIMEOUT_SECONDS,
            start_new_session=True,
        )
        stdout, stderr, returncode = proc.stdout, proc.stderr, proc.returncode
    except subprocess.TimeoutExpired as exc:
        timeout_hit = True
        stdout = exc.stdout or ''
        stderr = exc.stderr or ''
        if isinstance(stdout, bytes): stdout = stdout.decode(errors='replace')
        if isinstance(stderr, bytes): stderr = stderr.decode(errors='replace')
        stderr += f'\nTIMEOUT_EXPIRED_AFTER_SECONDS={TIMEOUT_SECONDS}\n'
        returncode = 124
    elapsed = time.time() - start
    out_path.write_text(stdout)
    err_path.write_text(stderr)
    code_path.write_text(str(returncode))
    combined = stdout + '\n' + stderr
    passed = None
    m = re.search(r'(\d+) passed(?:,\s*(\d+) skipped)? in ', combined)
    if m:
        passed = int(m.group(1))
    if passed is not None:
        passed_total += passed
    rec = {
        'batch': batch_id,
        'node_count': len(batch),
        'exitcode': returncode,
        'timeout_hit': timeout_hit,
        'passed_count_from_pytest_summary': passed,
        'elapsed_seconds': round(elapsed, 3),
        'command_file': str((REPORTS / f'tier_ab_{batch_id}.cmd').relative_to(ROOT)),
        'stdout': str(out_path.relative_to(ROOT)),
        'stderr': str(err_path.relative_to(ROOT)),
        'exitcode_file': str(code_path.relative_to(ROOT)),
        'nodeids_file': str((AUDIT / f'TIER_AB_{batch_id}_nodeids.txt').relative_to(ROOT)),
    }
    summary['batches'].append(rec)
    summary['passed_total_from_pytest_summaries_so_far'] = passed_total
    (REPORTS / 'tier_ab_batch_progress.json').write_text(json.dumps(summary, indent=2, sort_keys=True) + '\n')

assigned_once = len(assignments) == len(nodes) and len({a['nodeid'] for a in assignments}) == len(nodes)
summary['assigned_once'] = assigned_once
summary['all_batch_exitcodes_zero'] = all(b['exitcode'] == 0 for b in summary['batches'])
summary['all_batches_have_expected_pass_count'] = all(b['passed_count_from_pytest_summary'] == b['node_count'] for b in summary['batches'])
summary['timeout_batch_count'] = sum(1 for b in summary['batches'] if b['timeout_hit'])
summary['passed_total_from_pytest_summaries'] = passed_total
summary['passed_total_matches_collected_count'] = passed_total == len(nodes)
summary['closure_regression_proof_status'] = 'PASS' if (summary['all_batch_exitcodes_zero'] and summary['all_batches_have_expected_pass_count'] and assigned_once and passed_total == len(nodes) and len(dups) == 0) else 'FAIL'
(REPORTS / 'TIER_AB_BATCH_REGRESSION_SUMMARY.json').write_text(json.dumps(summary, indent=2, sort_keys=True) + '\n')
print(json.dumps(summary, indent=2, sort_keys=True))
sys.exit(0 if summary['closure_regression_proof_status'] == 'PASS' else 1)
