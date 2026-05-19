# Validation Summary — PRL tranche final audit mainline 001

## Gate 3 — Pre-merge validation

| Check | Command | Result | Evidence path |
|---|---|---|---|
| Whitespace/diff hygiene | `git diff --check` | PASS, exit 0 | `premerge_git_diff_check.log` |
| Scaffold | `make scaffold-check` | PASS, `repo scaffold present`, exit 0 | `premerge_scaffold_check.log` |
| Parallel risk Tier A suite | `env PYTHONPATH=src PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest tests/tier_a/parallel_risk -q` | PASS, 103 passed | `premerge_parallel_risk_pytest.log` |
| PRL authority proof block | `env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 scripts/run_proof_block.py --block parallel_risk_lane_authority_surface` | PASS, 112 passed | `premerge_proof_parallel_risk_lane_authority_surface.log` |
| Targeted workbook / signal inventory / unavailable / VIX / vocabulary constraints | `env PYTHONPATH=src PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest tests/tier_a/parallel_risk/test_parallel_risk_signal_inventory_workbook.py tests/tier_a/parallel_risk/test_parallel_risk_signal_inventory_promotion.py tests/tier_a/parallel_risk/test_parallel_risk_inventory_backed_unavailable_signals.py tests/tier_a/parallel_risk/test_parallel_risk_vix_threshold_governance.py tests/tier_a/parallel_risk/test_parallel_risk_vix_threshold_preservation.py tests/tier_a/vocabulary/test_parallel_risk_description_vocabulary_constraints.py -q` | PASS, 26 passed | `premerge_targeted_prl_inventory_vix.log` |
| Workbook/runtime/config probe | Python workbook/config/token probe | PASS, sheet/config/classes present and runtime workbook-token hits empty | `deep_audit_probe.log` |

## Gate 7 — Post-merge validation

Post-merge results are appended after mainline merge.
