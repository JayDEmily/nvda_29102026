# Gate 5 — Reversible mutation / fault-injection plan: proof_executor_contract

Status: `PASS_FOR_SELECTED_FAMILY`

| Probe | Mutation target | Expected failing test | Revert method | Baseline return check |
|---|---|---|---|---|
| disable owned-path validation | replace `_validate_owned_paths(block)` in `scripts/run_proof_block.py` with a comment | `test_proof_executor_rejects_missing_owned_paths_before_running` | restore original file from pre-probe copy | full selected-family pytest returns 19 passed |
| execute command via shell | replace `subprocess.run(resolved_command, check=False)` with `subprocess.run(command, shell=True, check=False)` | `test_proof_executor_runs_manifest_commands_without_shell_evaluation` | restore original file from pre-probe copy | full selected-family pytest returns 19 passed |

No permanent source mutation is authorised. Mutations are temporary and must be reverted before closeout.
