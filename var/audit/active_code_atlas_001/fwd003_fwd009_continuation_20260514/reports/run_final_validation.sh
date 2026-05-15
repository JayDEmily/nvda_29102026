#!/usr/bin/env bash
set +e
cd /mnt/data/work_nvda10/repo
report=var/audit/active_code_atlas_001/fwd003_fwd009_continuation_20260514/reports
run_capture(){ name="$1"; shift; "$@" > "$report/${name}.stdout" 2> "$report/${name}.stderr"; st=$?; printf '%s\n' "$st" > "$report/${name}.status"; printf '%s status=%s\n' "$name" "$st" >> "$report/run_final_validation.progress"; }
run_capture final_git_status git status --short
run_capture final_git_diff_check git diff --check
run_capture final_manifest_validator python var/audit/active_code_atlas_001/tools/validate_full_read_manifest.py var/audit/active_code_atlas_001/fwd003_fwd009_continuation_20260514/FWD003_FWD009_CLOSURE_GRADE_READ_MANIFEST.json
run_capture final_proof_blocks_check_all python scripts/run_proof_block.py --check-all
run_capture final_tier_b env PYTHONPATH=src python -m pytest -q tests/tier_b
run_capture final_tier_a env PYTHONPATH=src python -m pytest -q tests/tier_a
PYTHONPATH=src pytest -q tests/tier_a tests/tier_b > "$report/final_exact_combined_tier_a_tier_b.out" 2>&1
st=$?
printf '%s\n' "$st" > "$report/final_exact_combined_tier_a_tier_b.exitcode"
printf 'final_exact_combined_tier_a_tier_b exitcode=%s\n' "$st" >> "$report/run_final_validation.progress"
printf 'done\n' > "$report/run_final_validation.done"
