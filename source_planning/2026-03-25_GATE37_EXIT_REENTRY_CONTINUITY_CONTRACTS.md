# 2026-03-25 Gate 37 Exit, Re-entry, and Continuity Contracts

Status: Complete on `main`  
Gate: 37  
Leaf: `LEAF-G37-001`

## Closed set

1. `archive-module-035` / `dynamic_partial_exit_model`
2. `archive-module-034` / `take_profit`
3. `archive-module-033` / `trailing_stop`
4. `archive-module-036` / `trade_reentry_marker`
5. `archive-module-045` / `fill_feedback_router`
6. `archive-module-047` / `ladder_continuity_tracker`

## What closed this gate

- Reconciled the exact six exit-chain and continuity surfaces already emitted inside `execution_lifecycle.py`.
- Proved the Gate-37 set in frozen order with no widening into review-ledger or feedback-overlay backlog items.
- Kept every surface explicitly bounded to preview exits, preview continuity, and dry-run feedback routing.

## Honesty boundary

- `dynamic_partial_exit_model`, `take_profit`, and `trailing_stop` remain advisory exit surfaces only.
- `trade_reentry_marker` and `fill_feedback_router` remain preview continuity surfaces and must not imply broker-side state.
- `ladder_continuity_tracker` remains a preview hash/continuity surface rather than a live ladder-management engine.
