# 2026-03-25 Gate 28 Ingress Substrate Contracts

Status: Complete on `main`  
Authority: Subordinate to the gate map and leaf ledger.

## Purpose

Gate 28 closes the first post-G27 executable tranche by proving that the seven planned ingress-substrate items already exist on the persisted branch as typed contract surfaces, with fences or runtime proxies kept explicit.

## Exact Gate-28 item set

1. `archive-module-006` / `event_flag_capture`
2. `archive-module-001` / `spot_data_capture`
3. `archive-module-002` / `vwap_accumulator`
4. `archive-module-008` / `vwap_roc`
5. `archive-module-007` / `peer_equity_capture`
6. `archive-module-005` / `macro_data_capture`
7. `archive-module-009` / `realized_volatility_engine`

## Closure note

This gate is intentionally narrow and mostly attributional on the persisted branch:

- `event_flag_capture` and `realized_volatility_engine` already existed in `tranche_a.py`.
- `spot_data_capture`, `vwap_accumulator`, `vwap_roc`, `peer_equity_capture`, and `macro_data_capture` already existed in `market_substrate.py`.
- Gate 28 therefore closes by proving the exact seven-item set, in frozen order, and by recording that the existing contract surfaces remain honest about proxy and fence boundaries.

## Binding honesty rules

- `event_flag_capture`, `spot_data_capture`, `peer_equity_capture`, `macro_data_capture`, and `realized_volatility_engine` may proxy from existing deterministic runtime inputs only.
- `vwap_accumulator` and `vwap_roc` must remain explicitly fenced until raw tick-derived state exists.
- No named-playbook widening, broker theatre, or hidden side-state is authorised inside Gate 28.
