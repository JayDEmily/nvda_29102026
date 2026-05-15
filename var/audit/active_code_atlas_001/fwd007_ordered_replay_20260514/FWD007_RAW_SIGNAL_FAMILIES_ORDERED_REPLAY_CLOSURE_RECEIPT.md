# FWD-007 raw signal families ordered replay closure receipt

Status: `bounded_closed_current`

Branch: `worker/fwd007-ordered-replay-20260514`
Head before commit: `fa3fe10`

## Scope

This ordered replay opened **FWD-007 only**. FWD-008 and FWD-009 were not opened by this receipt.

## Superseded defect corrected

The prior combined FWD-006/FWD-007/FWD-008 closure report labelled `ACABC-0008` / `ACATQ-0008` as `missing`. This replay records the static Bridge comparison and queue status correctly as `comparison_status=partially_satisfied` and preserves the donor/native status count separately as `bridge_native_satisfaction_status_counts={"missing": 22}`.

## Coverage

- Selected native raw-signal-family Atlas IDs: `123`
- Covered selected IDs: `123`
- Unresolved selected IDs: `0`
- Direct native Atlas links: `0`
- Grouped comparison/queue overlay coverage: `123`
- Comparison status counts: `{'transform_required': 68, 'partially_satisfied': 55}`
- Bridge-native satisfaction status counts retained separately: `{'transform_required': 68, 'missing': 22, 'partially_satisfied': 33}`

## Proof

- `raw_signal_contract_copy_boundary_surface`: exit `0`, `2 passed`
- `raw_signal_transform_boundary_surface`: exit `0`, `2 passed`
- `support_spine_prepared_packet_review_surface`: exit `0`, `41 passed`
- Default-environment Tier A/B batch proof: `609/609` passed across `31` batches with all used exit codes `0`; `PYTEST_DISABLE_PLUGIN_AUTOLOAD` unset.
- Proof-block registry validation: `proof_blocks_check_all=PASS count=46`.

## Mutation boundary

No source, tests, config, fixtures, dependency, vocabulary, original Atlas/Bridge JSON, or generated Atlas slice mutation is authorised or recorded by this replay. The only intended mutations are this evidence directory and `ROADMAP_LEDGER.md`.

## Decision

FWD-007 is `bounded_closed_current` on corrected ordered-replay evidence. FWD-008 remains `evidence_blocked_pending_ordered_replay`; FWD-009 remains unopened.
