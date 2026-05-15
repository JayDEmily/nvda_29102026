# FWD-004 Tier A/B batch regression proof evidence

Date: 2026-05-14
Branch: `worker/fwd-003-through-fwd-009-closure-continuation`
Source commit before this remediation gate: `861d260`
Scope: FWD-004 regression-proof remediation only. FWD-005 not opened.

## Reason

The previous FWD-004 closure gate had targeted DMPV3 proof, manifest validation, proof-block validation, and clean diff evidence, but did not have a captured monolithic Tier A/B pytest exit-code receipt. The user required deterministic batch execution before FWD-004 may stand as closed.

## Collection

- Collection command receipt: `reports/tier_ab_collect_nodeids.raw.out`, `reports/tier_ab_collect_nodeids.raw.err`, `reports/tier_ab_collect_nodeids.raw.exitcode`.
- Collected node list: `TIER_AB_COLLECTED_NODEIDS.txt`.
- Collection exit code: `0`.
- Collected Tier A/B node IDs: `639`.
- Unique node IDs: `639`.
- Duplicate node IDs: `0`.

## Deterministic batching

- Batch assignment manifest: `TIER_AB_BATCH_ASSIGNMENTS.json`.
- Batch size: `20`.
- Batch count: `32`.
- Per-batch files: `TIER_AB_batch_NN_nodeids.txt` plus `reports/tier_ab_batch_NN.cmd`, `.out`, `.err`, `.exitcode`.
- Assignment proof: `assigned_once=True`.

## Execution result

- All batch exit codes zero: `True`.
- Every batch summary pass count equals its assigned node count: `True`.
- Total passed count from pytest summaries: `639`.
- Total passed count matches collected node count: `True`.
- Timeout batch count: `0`.
- Closure regression proof status: `PASS`.

## Batch receipt index

| Batch | Node count | Exit code | Passed summary | Timeout | Elapsed seconds |
|---|---:|---:|---:|---:|---:|
| `batch_01` | 20 | 0 | 20 | False | 4.811 |
| `batch_02` | 20 | 0 | 20 | False | 5.684 |
| `batch_03` | 20 | 0 | 20 | False | 5.52 |
| `batch_04` | 20 | 0 | 20 | False | 4.891 |
| `batch_05` | 20 | 0 | 20 | False | 5.128 |
| `batch_06` | 20 | 0 | 20 | False | 4.96 |
| `batch_07` | 20 | 0 | 20 | False | 5.089 |
| `batch_08` | 20 | 0 | 20 | False | 5.09 |
| `batch_09` | 20 | 0 | 20 | False | 5.373 |
| `batch_10` | 20 | 0 | 20 | False | 6.901 |
| `batch_11` | 20 | 0 | 20 | False | 5.338 |
| `batch_12` | 20 | 0 | 20 | False | 5.742 |
| `batch_13` | 20 | 0 | 20 | False | 5.388 |
| `batch_14` | 20 | 0 | 20 | False | 4.787 |
| `batch_15` | 20 | 0 | 20 | False | 5.018 |
| `batch_16` | 20 | 0 | 20 | False | 5.757 |
| `batch_17` | 20 | 0 | 20 | False | 5.81 |
| `batch_18` | 20 | 0 | 20 | False | 5.945 |
| `batch_19` | 20 | 0 | 20 | False | 6.295 |
| `batch_20` | 20 | 0 | 20 | False | 5.58 |
| `batch_21` | 20 | 0 | 20 | False | 5.074 |
| `batch_22` | 20 | 0 | 20 | False | 5.693 |
| `batch_23` | 20 | 0 | 20 | False | 6.3 |
| `batch_24` | 20 | 0 | 20 | False | 5.788 |
| `batch_25` | 20 | 0 | 20 | False | 4.929 |
| `batch_26` | 20 | 0 | 20 | False | 23.397 |
| `batch_27` | 20 | 0 | 20 | False | 5.313 |
| `batch_28` | 20 | 0 | 20 | False | 15.701 |
| `batch_29` | 20 | 0 | 20 | False | 5.17 |
| `batch_30` | 20 | 0 | 20 | False | 7.861 |
| `batch_31` | 20 | 0 | 20 | False | 39.083 |
| `batch_32` | 19 | 0 | 19 | False | 4.942 |

## Finding

FWD-004 may stand as `bounded_closed_current` under the user's regression-proof condition because the exact collected Tier A/B node list was assigned once, every deterministic batch produced captured command/stdout/stderr/exit-code receipts, every batch exited `0`, and the total pytest passed count equals the collected node count.

No source, test, config, fixture, dependency, original Atlas/Bridge JSON, or generated slice mutation was made by this remediation gate.

## Follow-on validation

- Batch receipt verification: `reports/batch_receipt_verification.exitcode` = `0`; `reports/batch_receipt_verification.out` records `validation_status=PASS`, `error_count=0`, `passed_total_from_receipts=639`.
- Current read manifest: `FWD004_TIER_AB_BATCH_REGRESSION_READ_MANIFEST.json`.
- Manifest validation: `reports/manifest_validation.exitcode` = `0`; `reports/manifest_validation.out` records `validation_status=PASS`, `entry_count=239`, `full_read_false_count=0`.
- `git diff --check`: `reports/git_diff_check_final.exitcode` = `0`.
- `python scripts/run_proof_block.py --check-all`: `reports/proof_blocks_check_all.exitcode` = `0`; output records `proof_blocks_check_all=PASS count=46`.
