#!/usr/bin/env bash
set +e
out="var/audit/active_code_atlas_001/fwd003_closure_gate_20260514/reports"
for name in tier_b tier_a tier_a_tier_b_combined; do
  rm -f "$out/${name}.status" "$out/${name}.stdout" "$out/${name}.stderr"
done
PYTHONPATH=src python -m pytest -q tests/tier_b > "$out/tier_b.stdout" 2> "$out/tier_b.stderr"
printf '%s' "$?" > "$out/tier_b.status"
PYTHONPATH=src python -m pytest -q tests/tier_a > "$out/tier_a.stdout" 2> "$out/tier_a.stderr"
printf '%s' "$?" > "$out/tier_a.status"
PYTHONPATH=src python -m pytest -q tests/tier_a tests/tier_b > "$out/tier_a_tier_b_combined.stdout" 2> "$out/tier_a_tier_b_combined.stderr"
printf '%s' "$?" > "$out/tier_a_tier_b_combined.status"
printf 'done' > "$out/run_broad_validation.done"
