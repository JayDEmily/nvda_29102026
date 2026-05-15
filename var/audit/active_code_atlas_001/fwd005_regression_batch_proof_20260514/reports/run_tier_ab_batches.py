from __future__ import annotations
import json, math, re, subprocess, sys
from pathlib import Path
ROOT = Path.cwd()
AUD = ROOT / 'var/audit/active_code_atlas_001/fwd005_regression_batch_proof_20260514'
REP = AUD / 'reports'
REP.mkdir(parents=True, exist_ok=True)
collect_cmd = ['env','PYTHONPATH=src','python','-m','pytest','--collect-only','-q','tests/tier_a','tests/tier_b']
(REP/'collect.cmd').write_text(' '.join(collect_cmd)+'\n')
proc = subprocess.run(collect_cmd, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
(REP/'collect.out').write_text(proc.stdout)
(REP/'collect.err').write_text(proc.stderr)
(REP/'collect.exitcode').write_text(str(proc.returncode)+'\n')
if proc.returncode != 0:
    raise SystemExit(proc.returncode)
nodeids = []
for line in proc.stdout.splitlines():
    s=line.strip()
    if s.startswith('tests/') and '::' in s:
        nodeids.append(s)
# preserve order, require uniqueness
seen=set(); unique=[]; dups=[]
for n in nodeids:
    if n in seen: dups.append(n)
    else:
        seen.add(n); unique.append(n)
(AUD/'TIER_AB_COLLECTED_NODEIDS.txt').write_text('\n'.join(unique)+'\n')
BATCH_SIZE=20
batches=[unique[i:i+BATCH_SIZE] for i in range(0,len(unique),BATCH_SIZE)]
assignments={
    'schema_version':'fwd005_tier_ab_batch_assignments_v1',
    'batch_size':BATCH_SIZE,
    'collected_node_count':len(nodeids),
    'unique_node_count':len(unique),
    'duplicate_node_count':len(dups),
    'batch_count':len(batches),
    'batches':[]
}
summary_batches=[]
for idx,batch in enumerate(batches,1):
    label=f'tier_ab_batch_{idx:02d}'
    nodefile=AUD/f'TIER_AB_batch_{idx:02d}_nodeids.txt'
    nodefile.write_text('\n'.join(batch)+'\n')
    cmd=['env','PYTHONPATH=src','python','-m','pytest','-q',*batch]
    (REP/f'{label}.cmd').write_text(' '.join(cmd)+'\n')
    p=subprocess.run(cmd,cwd=ROOT,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    (REP/f'{label}.out').write_text(p.stdout)
    (REP/f'{label}.err').write_text(p.stderr)
    (REP/f'{label}.exitcode').write_text(str(p.returncode)+'\n')
    passed=None
    m=re.search(r'(\d+) passed', p.stdout)
    if m: passed=int(m.group(1))
    assignments['batches'].append({'batch_index':idx,'node_file':str(nodefile.relative_to(ROOT)),'node_count':len(batch)})
    summary_batches.append({'batch_index':idx,'node_count':len(batch),'exitcode':p.returncode,'passed_summary':passed})
    print(f'batch {idx}/{len(batches)} exit={p.returncode} nodes={len(batch)} passed_summary={passed}', flush=True)
summary={
    'schema_version':'fwd005_tier_ab_batch_regression_summary_v1',
    'collected_node_count':len(nodeids),
    'unique_node_count':len(unique),
    'duplicate_node_count':len(dups),
    'batch_size':BATCH_SIZE,
    'batch_count':len(batches),
    'batches':summary_batches,
    'all_batch_exitcodes_zero':all(b['exitcode']==0 for b in summary_batches),
    'total_passed_summary':sum((b['passed_summary'] or 0) for b in summary_batches),
    'passed_total_matches_unique_node_count':sum((b['passed_summary'] or 0) for b in summary_batches)==len(unique),
    'assignment_once_only':len(unique)==sum(len(b) for b in batches)==len(set().union(*[set(b) for b in batches])) if batches else True,
}
(AUD/'TIER_AB_BATCH_ASSIGNMENTS.json').write_text(json.dumps(assignments,indent=2)+'\n')
(REP/'TIER_AB_BATCH_REGRESSION_SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
raise SystemExit(0 if summary['all_batch_exitcodes_zero'] and summary['passed_total_matches_unique_node_count'] and summary['assignment_once_only'] and not dups else 1)
