# Gate 4 — Known-bad specimen construction: proof_executor_contract

Status: `PASS_FOR_SELECTED_FAMILY`

All specimens are temporary in-test manifests written under `tmp_path`. They do not use current repo output as expected truth.

| Specimen | Invalid condition | Expected failure mode | Implemented test |
|---|---|---|---|
| `missing_block` against manifest containing only `known_block` | unknown block id | non-zero exit and stderr contains unknown block plus available block | `test_proof_executor_rejects_unknown_block_ids` |
| block owns `does_not_exist.txt` | missing owned path | non-zero exit; command side-effect file is absent | `test_proof_executor_rejects_missing_owned_paths_before_running` |
| two blocks with `proof_block_id: duplicate_block` | duplicate id | non-zero exit and duplicate-id stderr | `test_proof_executor_check_all_rejects_duplicate_block_ids` |
| `proof_blocks: ["not-a-proof-block-mapping"]` | non-mapping entry | non-zero exit and non-mapping entry stderr | `test_proof_executor_check_all_rejects_non_mapping_entries` |
| command contains `; touch shell_injection_marker.txt` | shell metacharacter must not execute | run succeeds but marker file is absent | `test_proof_executor_runs_manifest_commands_without_shell_evaluation` |

Line evidence after amendment: `tests/tier_b/proof_model/test_proof_executor_contract.py:289-407`.
