# 2026-03-31 Gate 125 Review-Visible Coefficient Lineage

Status: complete on `main`; Gate 126 is now the active gate

## What landed

- `EffectivePolicySnapshot` and `ReviewLineagePacket` now carry the same resolved-surface chain produced by the modifier runtime packet.
- Review output renders baseline reference, baseline/effective value, clamp state, precedence band, source policy ids, and authority version without reconstructing a second coefficient story from free text.
- Prepared and raw canonical paths preserve identical review-visible coefficient lineage.

## Proof

- `PYTHONPATH=src pytest -q tests/test_execution_review_runtime.py tests/test_gate103_raw_prepared_parity.py tests/test_gate121_final_risk_gateway_join.py tests/test_gate125_review_visible_lineage.py`

## Receipt

- Gate 125 closes the review-visibility part of the governed coefficient chain and advances the active pack to Gate 126.
