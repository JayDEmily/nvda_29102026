from __future__ import annotations
import subprocess,sys
from pathlib import Path
repo=Path(sys.argv[1]).resolve(); start=int(sys.argv[2]); end=int(sys.argv[3]); out=Path(sys.argv[4])
raw=repo/'project_control/canonical_project_manager/modules/M13/raw_validation'; runner=raw/'v5_run_variant.py'
mutants=(
('durable_label','mutant_durable_label_source.py','exports_the_accepted_public_contract',b"AssertionError: assert 'durable'"),
('duplicate_reexec','mutant_duplicate_reexec_source.py','exact_duplicate_returns_original_identity',b'assert 2 == 1'),
('scope_value_only','mutant_scope_value_only_source.py','idempotency_key_is_scoped',b'IdempotencyConflictError: conflicting idempotency-key reuse'),
('ignore_version','mutant_ignore_version_source.py','stale_expected_version_fails_before_mutation',b'DID NOT RAISE'),
('commit_on_exception','mutant_commit_on_exception_source.py','mutation_failure_rolls_back_state_version',b'assert 1 == 0'),
('accept_invalid_receipt','mutant_accept_invalid_receipt_source.py','invalid_receipt_result_rolls_back',b'DID NOT RAISE'),
('commit_before_receipt','mutant_commit_before_receipt_source.py','receipt_write_failure_rolls_back_every_visible_change',b'assert 1 == 0'),
('no_participant_rollback','mutant_no_participant_rollback_source.py','receipt_write_failure_rolls_back_every_visible_change',b'Left contains one more item'),
('register_after_prepare','mutant_register_after_prepare_source.py','prepare_failure_rolls_back_failing_participant',b'rollback_calls'),
('rollback_only_failing_prepare_participant','mutant_rollback_only_failing_prepare_participant_source.py','later_prepare_failure_rolls_back_every_prepared_participant',b'rollback_calls'),
('pm_v4_failed_attempt_binding','pm_v4_mutant_failed_attempt_reserves_idempotency_source.py','failed_transaction_does_not_bind_idempotency_key',b'failed attempt reserved idempotency key'),)
rows=[]; passed=True
for idx,(mid,src,case,token) in enumerate(mutants[start:end],start=start):
  source=raw/src
  full=subprocess.run([sys.executable,str(runner),str(source)],cwd=repo,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,check=False)
  target=subprocess.run([sys.executable,str(runner),str(source),'--case',case],cwd=repo,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,check=False)
  ok=(full.returncode==1 and target.returncode==1 and token in target.stdout and b'1 failed, 45 deselected' in target.stdout)
  passed &= ok
  row=f"{idx+1}\t{mid}\t{src}\t{case}\t{full.returncode}\t{target.returncode}\t{'PASS' if ok else 'FAIL'}"
  print(row,flush=True); rows.append(row)
  if not ok: print(target.stdout.decode(errors='replace'),flush=True)
out.parent.mkdir(parents=True,exist_ok=True)
with out.open('a',encoding='utf-8') as f:
  for r in rows:f.write(r+'\n')
raise SystemExit(0 if passed else 1)
