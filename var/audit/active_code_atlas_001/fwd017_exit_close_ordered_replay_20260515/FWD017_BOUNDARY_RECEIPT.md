# FWD-017 Boundary Receipt — Exit and close architecture

Created: 2026-05-15T06:46:41Z

## Scope

Opened row: `FWD-017 — 5.14 Exit and close architecture`.

Not opened:

- `FWD-018 — 5.15 Review and explanation layer`;
- `FWD-001` through `FWD-016` except regression/context evidence reads;
- broker/live trading execution;
- original Atlas/Bridge source-of-truth JSON;
- frozen `*_CORE.md` files;
- vocabulary remediation or candidate suppression.

## Boundary finding

Current exit/close behaviour is bounded to policy decisions, protocol-only close handoff material, and replayable receipts. It does not authorise broker/order execution, hidden live-inventory mutation, capital sizing recomputation, raw source ingestion, new candidate formation, or review/explanation mutation.

## Evidence

- Blueprint row 5.14: `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:356-371`.
- FWD-017 ledger row before replay: `ROADMAP_LEDGER.md:1952-2002`.
- Exit/close contracts: `src/nvda_desk/contracts/exit_close.py:97-244`.
- Exit/close service functions: `src/nvda_desk/downstream/exit_close.py:60-155`.
- Boundary tests: `tests/tier_a/downstream_runtime/test_exit_close_architecture_surface.py:35-294` and `tests/tier_a/downstream_runtime/test_exit_close_transform_boundary_surface.py:11-83`.
