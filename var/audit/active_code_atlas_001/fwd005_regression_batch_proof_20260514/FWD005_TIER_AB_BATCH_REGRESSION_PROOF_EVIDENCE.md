# FWD-005 Tier A/B Adaptive Batch Regression Proof

## Decision

The adaptive batch proof is usable for FWD-005 closure: `True`.

## Counts

- Collected Tier A/B node IDs: 639
- Unique node IDs: 639
- Duplicate collected node IDs: 0
- Execution receipts used: 51
- Assignment once-only: True
- All used execution exit codes zero: True
- Passed summaries total: 639
- Passed total matches collected unique node count: True

## Adaptive exception

original tier_ab_batch_31 completed pytest summary but did not yield captured shell exitcode; its 20 node IDs were split into deterministic singleton receipts batch31_split_01..20 and the original uncaptured batch31 output is retained but not used for proof.

The uncaptured original `tier_ab_batch_31` output is retained as non-closure evidence. The closure proof uses `tier_ab_batch_01` through `tier_ab_batch_30`, `batch31_split_01` through `batch31_split_20`, and `tier_ab_batch_32`.
