#!/usr/bin/env python3
import json, os, subprocess, sys, time
from datetime import datetime, timezone
from pathlib import Path
ROOT = Path.cwd()
AUD = ROOT / 'var/audit/active_code_atlas_001/fwd017_batched_proof_hardening_20260515'
REPORTS = AUD / 'reports'
REPORTS.mkdir(parents=True, exist_ok=True)

def iso():
    return datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

def run(name, cmd, timeout_s=240):
    base = REPORTS / name
    (base.with_suffix('.command')).write_text(' '.join(cmd) + '\n', encoding='utf-8')
    (base.with_suffix('.started_at')).write_text(iso() + '\n', encoding='utf-8')
    start = time.time()
    try:
        cp = subprocess.run(cmd, cwd=ROOT, env={**os.environ, 'PYTHONPATH':'src'}, text=True,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout_s)
        status = cp.returncode
        out, err = cp.stdout, cp.stderr
    except subprocess.TimeoutExpired as exc:
        status = 124
        out = exc.stdout or ''
        err = (exc.stderr or '') + f'\nTIMEOUT after {timeout_s}s\n'
        if isinstance(out, bytes): out = out.decode('utf-8', errors='replace')
        if isinstance(err, bytes): err = err.decode('utf-8', errors='replace')
    elapsed = time.time() - start
    (base.with_suffix('.stdout')).write_text(out, encoding='utf-8')
    (base.with_suffix('.stderr')).write_text(err, encoding='utf-8')
    (base.with_suffix('.status')).write_text(str(status) + '\n', encoding='utf-8')
    (base.with_suffix('.ended_at')).write_text(iso() + '\n', encoding='utf-8')
    (base.with_suffix('.duration_seconds')).write_text(f'{elapsed:.3f}\n', encoding='utf-8')
    return {'name': name, 'cmd': cmd, 'status': status, 'duration_seconds': elapsed}

batches = []
for tier in ['tier_b', 'tier_a']:
    base = ROOT / 'tests' / tier
    for path in sorted(p for p in base.iterdir() if p.is_dir()):
        name = f'{tier}_{path.name.replace("-","_")}'
        batches.append((name, ['python', '-m', 'pytest', '-q', str(path)]))

results = []
for name, cmd in batches:
    results.append(run(name, cmd))
    (AUD / 'BATCHED_PYTEST_PROGRESS.json').write_text(json.dumps(results, indent=2), encoding='utf-8')
(AUD / 'BATCHED_PYTEST_SUMMARY.json').write_text(json.dumps({'results': results}, indent=2), encoding='utf-8')
