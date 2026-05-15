# FWD-006 Ordered Replay Closure Receipt — Raw capture and source temporal law

Status: `bounded_closed_current`

Scope: FWD-006 only. FWD-007, FWD-008, and FWD-009 were not opened by this replay.

Input state:
- Started from forensic audit commit `c5c7e0c` on `worker/fwd006-fwd008-forensic-audit-20260514`.
- New worker branch: `worker/fwd006-ordered-replay-20260514`.
- The forensic audit defect was accepted as controlling: the prior combined FWD-006/FWD-007/FWD-008 closure evidence was not acceptable as row closure.

Evidence correction:
- Supersedes prior combined report path `var/audit/active_code_atlas_001/fwd006_fwd008_closure_20260514/FWD006_THREE_WAY_COMPARISON_REPORT.json` for FWD-006 closure claims.
- Corrected report path: `var/audit/active_code_atlas_001/fwd006_ordered_replay_20260514/FWD006_THREE_WAY_COMPARISON_REPORT.json`.
- `ACABC-0005` / `ACATQ-0005` is recorded as `comparison_status=partially_satisfied`.
- The original Bridge-native count for that group is retained separately as `bridge_native_satisfaction_status_counts={"missing": 11}`. The replay does not relabel those donor-native rows as originally satisfied.

Coverage finding:
- Selected native raw-capture/source-temporal Atlas IDs: 108.
- Current covered selected native Atlas IDs: 108.
- Current unresolved selected native Atlas IDs: 0.
- Direct selected native Atlas links: 0.
- Grouped comparison/queue satisfaction overlay coverage: 108.
- Comparison status counts: `transform_required=66`, `partially_satisfied=42`.
- Bridge-native satisfaction status counts retained separately: `transform_required=66`, `missing=11`, `partially_satisfied=31`.

Proof captured:
- `raw_capture_source_temporal_law_surface`: exit code `0`, `3 passed`.
- `source_temporal_standard_surface`: exit code `0`, `4 passed`.
- `raw_capture_transform_boundary_surface`: exit code `0`, `3 passed`.
- Default-environment Tier A/B batch proof: 609 collected nodes, 609 unique nodes, 31/31 batch receipts, all used exit codes `0`, passed summaries total `609`, assignment once-only `true`.
- The default-environment proof does not set `PYTEST_DISABLE_PLUGIN_AUTOLOAD`.

Mutation boundary:
- No source, test, config, fixture, data, dependency, original Atlas/Bridge JSON, generated Atlas slice, or vocabulary data mutation is part of the intended FWD-006 replay.
- Audit/ledger/report files are the only intended mutation class.

Decision:
- FWD-006 may be recorded as `bounded_closed_current` after manifest validation, proof-block check-all, diff check, and clean post-commit status are captured.
- FWD-007 remains the next ordered gate and is not opened by this receipt.

Final validation receipts captured before commit:
- Full-read manifest validation command path: `reports/manifest_validation.cmd`; exit code path: `reports/manifest_validation.exitcode`; observed exit code `0`.
- Proof-block registry command path: `reports/proof_blocks_check_all.cmd`; exit code path: `reports/proof_blocks_check_all.exitcode`; observed exit code `0`.
- Diff whitespace check command path: `reports/git_diff_check.cmd`; exit code path: `reports/git_diff_check.exitcode`; observed exit code `0`.
