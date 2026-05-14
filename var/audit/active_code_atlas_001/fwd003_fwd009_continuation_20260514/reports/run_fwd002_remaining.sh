#!/usr/bin/env bash
set +e
cd /mnt/data/work_nvda10/repo
report=var/audit/active_code_atlas_001/fwd003_fwd009_continuation_20260514/reports
run_capture(){ name="$1"; shift; "$@" > "$report/${name}.stdout" 2> "$report/${name}.stderr"; st=$?; printf '%s\n' "$st" > "$report/${name}.status"; printf '%s status=%s\n' "$name" "$st" >> "$report/run_fwd002_remaining.progress"; }
run_capture FWD002_proof_executor_contract_pytest env PYTHONPATH=src python -m pytest -q tests/tier_b/proof_model/test_proof_executor_contract.py
run_capture FWD002_tier_b env PYTHONPATH=src python -m pytest -q tests/tier_b
run_capture FWD002_tier_a env PYTHONPATH=src python -m pytest -q tests/tier_a
PYTHONPATH=src pytest -q tests/tier_a tests/tier_b > "$report/FWD002_EXACT_COMBINED_PYTEST.out" 2>&1
status=$?
printf "%s\n" "$status" > "$report/FWD002_EXACT_COMBINED_PYTEST.exitcode"
printf 'FWD002_EXACT_COMBINED_PYTEST exitcode=%s\n' "$status" >> "$report/run_fwd002_remaining.progress"
printf 'done\n' > "$report/run_fwd002_remaining.done"
