from __future__ import annotations
import os, subprocess, sys
from pathlib import Path
repo=Path(sys.argv[1]).resolve(); start=int(sys.argv[2]); end=int(sys.argv[3]); out=Path(sys.argv[4])
raw=repo/'project_control/canonical_project_manager/modules/M13/raw_validation'
runner=raw/'v5_run_variant.py'; source=raw/'v5_configurable_failed_binding_mutant_source.py'
boundaries=(
'stale_expected_state_version','owner_mutation_exception','invalid_mutation_result_mapping','invalid_or_empty_receipt_id','invalid_or_empty_result_id','repository_participant_prepare_failure','repository_participant_commit_failure','attesting_receipt_writer_failure')
comparison_cases={'command_id':'same-command-id-different-fingerprint','semantic_input_fingerprint':'different-command-id-same-fingerprint','policy_version':'different-command-id-same-fingerprint','complete_command_identity':'same-command-id-different-fingerprint'}
labels={'stale_expected_state_version':'stale-expected-state-version','owner_mutation_exception':'owner-mutation-exception','invalid_mutation_result_mapping':'invalid-mutation-result-mapping','invalid_or_empty_receipt_id':'invalid-or-empty-receipt-id','invalid_or_empty_result_id':'invalid-or-empty-result-id','repository_participant_prepare_failure':'repository-participant-prepare-failure','repository_participant_commit_failure':'repository-participant-commit-failure','attesting_receipt_writer_failure':'attesting-receipt-writer-failure'}
items=[]
for boundary in boundaries:
  for comparison,dimension in comparison_cases.items():
    suffix='complete-command-identity-corrected-version' if boundary=='stale_expected_state_version' and comparison=='complete_command_identity' else dimension
    items.append((boundary,comparison,f"{labels[boundary]}--{suffix}"))
passed=True; rows=[]
for idx,(boundary,comparison,case_id) in enumerate(items[start:end],start=start):
  env=os.environ.copy(); env['M13_MUTATION_BOUNDARY']=boundary; env['M13_BINDING_COMPARISON']=comparison
  cmd=[sys.executable,str(runner),str(source),'--case',case_id]
  cp=subprocess.run(cmd,cwd=repo,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,check=False)
  ok=(cp.returncode==1 and b'hidden failed-attempt binding falsely conflicts' in cp.stdout and case_id.encode() in cp.stdout and b'1 failed, 45 deselected' in cp.stdout)
  passed &= ok
  row=f"{idx+1}\t{boundary}\t{comparison}\t{case_id}\t{cp.returncode}\t{'PASS' if ok else 'FAIL'}"
  print(row,flush=True); rows.append(row)
  if not ok:
    print(cp.stdout.decode(errors='replace'),flush=True)
out.parent.mkdir(parents=True,exist_ok=True)
with out.open('a',encoding='utf-8') as f:
  for r in rows:f.write(r+'\n')
raise SystemExit(0 if passed else 1)
