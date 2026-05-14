# Gate 7 — Mutation/fault probe result: proof_executor_contract

Status: `PASS_FOR_SELECTED_FAMILY`

Temporary mutations were applied only to `scripts/run_proof_block.py`, then reverted before final validation. The file has no permanent diff.

| Probe | Expected result | Observed result | Evidence |
|---|---|---|---|
| disable `_validate_owned_paths(block)` | new missing-owned-path test fails | failed with `assert 0 != 0`; the command ran when validation was disabled | `logs/gate7_mutation_owned_path_probe.log` |
| replace list-argument subprocess execution with `shell=True` | new no-shell test fails | failed because `shell_injection_marker.txt` existed | `logs/gate7_mutation_shell_probe.log` |
| post-revert selected-family baseline | selected family passes again | `19 passed` | `logs/gate7_post_revert_baseline.log` |

Status file:

```text
owned_path_mutation_status=1
shell_mutation_status=1
post_revert_status=0
```

Interpretation: the added tests kill the two selected mutants and the baseline returned after revert. This proves only the selected invariants for the selected family; it does not prove full-suite reliability.
