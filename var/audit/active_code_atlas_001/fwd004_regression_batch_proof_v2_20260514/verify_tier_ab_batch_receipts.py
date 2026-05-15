#!/usr/bin/env python3
from __future__ import annotations
import json
import re
import sys
from pathlib import Path

ROOT = Path.cwd()
AUDIT = ROOT / 'var/audit/active_code_atlas_001/fwd004_regression_batch_proof_v2_20260514'
REPORTS = AUDIT / 'reports'
summary = json.loads((REPORTS / 'TIER_AB_BATCH_REGRESSION_SUMMARY.json').read_text())
assignments = json.loads((AUDIT / 'TIER_AB_BATCH_ASSIGNMENTS.json').read_text())
collected = [line.strip() for line in (AUDIT / 'TIER_AB_COLLECTED_NODEIDS.txt').read_text().splitlines() if line.strip()]
errors: list[str] = []
if summary.get('collected_count') != len(collected):
    errors.append(f"summary_collected_count_mismatch:{summary.get('collected_count')}:{len(collected)}")
if len(set(collected)) != len(collected):
    errors.append('collected_nodeids_not_unique')
assignment_nodeids = [a.get('nodeid') for a in assignments.get('assignments', [])]
if assignment_nodeids != collected:
    errors.append('assignments_do_not_match_collected_order_exactly')
seen_batches = {b['batch']: b for b in summary.get('batches', [])}
passed_total = 0
for batch_id, batch in seen_batches.items():
    node_file = AUDIT / f'TIER_AB_{batch_id}_nodeids.txt'
    cmd_file = REPORTS / f'tier_ab_{batch_id}.cmd'
    out_file = REPORTS / f'tier_ab_{batch_id}.out'
    err_file = REPORTS / f'tier_ab_{batch_id}.err'
    code_file = REPORTS / f'tier_ab_{batch_id}.exitcode'
    for file in [node_file, cmd_file, out_file, err_file, code_file]:
        if not file.exists():
            errors.append(f'missing_batch_file:{batch_id}:{file.relative_to(ROOT)}')
    if not code_file.exists():
        continue
    code = code_file.read_text().strip()
    if code != '0':
        errors.append(f'batch_exitcode_not_zero:{batch_id}:{code}')
    nodes = [line.strip() for line in node_file.read_text().splitlines() if line.strip()] if node_file.exists() else []
    if len(nodes) != batch.get('node_count'):
        errors.append(f'batch_node_count_mismatch:{batch_id}:{batch.get("node_count")}:{len(nodes)}')
    text = out_file.read_text(errors='replace') if out_file.exists() else ''
    m = re.search(r'(\d+) passed(?:,\s*(\d+) skipped)? in ', text)
    if not m:
        errors.append(f'batch_pytest_summary_missing:{batch_id}')
        continue
    passed = int(m.group(1))
    passed_total += passed
    if passed != len(nodes):
        errors.append(f'batch_passed_count_mismatch:{batch_id}:{passed}:{len(nodes)}')
if passed_total != len(collected):
    errors.append(f'passed_total_mismatch:{passed_total}:{len(collected)}')
report = {
    'validation_status': 'PASS' if not errors else 'FAIL',
    'error_count': len(errors),
    'errors': errors,
    'collected_count': len(collected),
    'assignment_count': len(assignment_nodeids),
    'batch_count': len(seen_batches),
    'passed_total_from_receipts': passed_total,
}
print(json.dumps(report, indent=2, sort_keys=True))
sys.exit(0 if not errors else 1)
