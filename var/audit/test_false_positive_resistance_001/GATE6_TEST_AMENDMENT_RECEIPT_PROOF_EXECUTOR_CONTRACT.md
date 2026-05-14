# Gate 6 — Test amendment receipt: proof_executor_contract

Status: `PASS_FOR_SELECTED_FAMILY`

Changed test file:

- `tests/tier_b/proof_model/test_proof_executor_contract.py`

Added helper surface:

- `_write_temp_proof_manifest`, lines `289-300`.
- `_run_temp_proof_executor`, lines `303-314`.

Added tests:

- `test_proof_executor_rejects_unknown_block_ids`, lines `317-337`.
- `test_proof_executor_rejects_missing_owned_paths_before_running`, lines `340-358`.
- `test_proof_executor_check_all_rejects_duplicate_block_ids`, lines `361-376`.
- `test_proof_executor_check_all_rejects_non_mapping_entries`, lines `379-385`.
- `test_proof_executor_runs_manifest_commands_without_shell_evaluation`, lines `388-407`.

Validation commands:

```bash
python -m pytest tests/tier_b/proof_model/test_proof_executor_contract.py -q
python scripts/run_proof_block.py --check proof_executor_contract
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python scripts/run_proof_block.py --block proof_executor_contract
```

Results:

```text
selected_pytest_status=0
proof_block_check_status=0
proof_block_run_status=0
```

Evidence logs:

- `logs/gate6_selected_test_post_amendment.log`: `19 passed in 25.93s`.
- `logs/gate6_proof_block_check.log`: `proof_block_check=PASS proof_executor_contract`.
- `logs/gate6_proof_block_run.log`: selected proof block passed with 19 tests.

No source/runtime/dependency/VENV/black/ruff change was made.
