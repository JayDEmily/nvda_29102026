from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import os, subprocess, sys
ROOT=Path(__file__).resolve().parents[6]
RUNNER=ROOT/'project_control/canonical_project_manager/modules/M13/raw_validation/v5_run_variant.py'
SOURCE=ROOT/'project_control/canonical_project_manager/modules/M13/raw_validation/v7_worker/v7_overbroad_guard_mutant_source.py'
MUTANTS={
'module_global_active_flag':'phase-owner-mutation--scope-different-command-and-unit--b-succeeds--a-succeeds',
'class_global_static_active_flag':'phase-owner-mutation--scope-different-command-and-unit--b-succeeds--a-succeeds',
'universal_active_marker_registry':'phase-owner-mutation--scope-different-command-and-unit--b-succeeds--a-succeeds',
'guard_keyed_only_by_command_type':'phase-owner-mutation--scope-same-command-different-unit--b-succeeds--a-fails',
'guard_keyed_only_by_consistency_unit_id':'phase-owner-mutation--scope-different-command-same-unit--b-fails--a-succeeds',
'guard_keyed_only_by_command_type_and_consistency_unit_id':'phase-owner-mutation--scope-same-command-and-unit-different-keys--b-fails--a-fails',
'guard_shared_by_concrete_class':'phase-owner-mutation--scope-different-command-and-unit--b-succeeds--a-succeeds',
'early_clear_before_participant_commit_with_global_coupling':'same_instance_rejection_and_distinct_instance_admission_hold_together',
}
def run_target(item):
    m,case=item
    env=os.environ.copy(); env['M13_V7_GUARD_MUTANT']=m; env['PYTHONPATH']=str(ROOT/'src')
    cmd=[sys.executable,str(RUNNER),str(SOURCE),'--case',case,'--quiet']
    p=subprocess.run(cmd,cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
    return m,p.returncode,p.stdout
with ThreadPoolExecutor(max_workers=8) as ex:
    results=[f.result() for f in as_completed([ex.submit(run_target,x) for x in MUTANTS.items()])]
for m,rc,out in sorted(results):
    ok=rc==1 and '1 failed' in out and 'ERROR' not in out
    print(f'{m}\texit={rc}\tintended_rejection={"PASS" if ok else "FAIL"}')
    if not ok:
        print(out)
        raise SystemExit(1)
print('v7_guard_mutants_targeted=8/8 PASS')
