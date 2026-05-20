# VALIDATION_SUMMARY — main reconciliation 2026-05-20

| Check | Status | Evidence |
|---|---:|---|
| `git diff --check` | 0 | `reports/git_diff_check.*` |
| `make scaffold-check` | 0 | `reports/scaffold_check.*` |
| Forensic JSON parse | 0 | `reports/validate_forensic_json.*` |
| Forensic count check | 0 | `reports/validate_forensic_counts.*`; output confirms 1,716 records, 508 existing source, 80 added source, 1,128 not migrated. |
| Proof block registry check | 0 | `reports/proof_blocks_check_all.*`; output: `proof_blocks_check_all=PASS count=51`. |
| Target-surface non-310 repair tests, fast isolated run | 0 | `reports/targeted_non310_repair_tests_fast.*`; output: `430 passed in 9.23s`. |
| FWD-014 capital-deployment proof, fast isolated run | 0 | `reports/targeted_fwd014_capital_fast.*`; output: `29 passed in 0.47s`. |

A first non-isolated `targeted_non310_repair_tests` run was interrupted by the outer execution timeout after partial progress; it has no status file and is superseded by the complete isolated run above.
