Status: complete on `work/gate-157-parallel-risk-lane-planning-pack-20260402`; Gate 160 is now the active gate
# Gate 159 — Workbook Lineage and Consolidation Audit

## What closed

Gate 159 is complete on `work/gate-157-parallel-risk-lane-planning-pack-20260402`. The repo now has one **governed workbook authority path** and one explicitly historical predecessor path rather than two half-live workbook stories.

## Inventory

- old workbook path: `docs/planning/2026-03-25_NVDA_SIGNAL_WORKBOOK_v3.xlsx`
- new workbook path: `data/reference/signal_workbooks/2026-03-25_NVDA_SIGNAL_WORKBOOK_v3_bounds_handoff_copy.xlsx`
- old sheet count: 20
- new sheet count: 27
- overlap sheet count: 20
- old-only sheets: none
- new-only sheets: ['Repo_Python_Inventory', 'Repo_Stage_Summary', 'Runtime_Surface_Drivers', 'Coeff_Universe_Index', 'Bounds_Method', 'Temporal_Bounds_Draft', 'Signal_Coeff_Handoff']
- identical overlap sheets: ['Gate_41_44_Summary']
- changed overlap sheets: 19

## Comparison result

The new workbook is a **clean successor with expanded scope** rather than a divergent fork:

- every legacy sheet name from the old workbook exists in the new workbook;
- the new workbook adds governance-rich sheets such as `Repo_Python_Inventory`, `Repo_Stage_Summary`, `Runtime_Surface_Drivers`, `Coeff_Universe_Index`, `Bounds_Method`, `Temporal_Bounds_Draft`, and `Signal_Coeff_Handoff`;
- only `Gate_41_44_Summary` remains byte-for-byte identical across overlapping sheets; the other overlapping sheets changed, which is consistent with the new workbook being an enriched successor rather than a copied duplicate;
- there are **no old-only sheets**, so workbook-as-ledger loss risk is low.

## Canonical survivor decision

- canonical governed workbook authority path: `data/reference/signal_workbooks/2026-03-25_NVDA_SIGNAL_WORKBOOK_v3_bounds_handoff_copy.xlsx`
- old workbook fate: retained at `docs/planning/2026-03-25_NVDA_SIGNAL_WORKBOOK_v3.xlsx` as **historical archive evidence only** for Gate 41 / Gate 95 / Phase 0 audit surfaces; it is retired from active authority and must not be used as the canonical workbook path for later coefficient or risk-lane work.

## Rewrites completed in this gate

Active lineage references were rewritten to the canonical survivor path in:
- `scripts/build_canonical_vocabulary.py`;
- `docs/vocabulary/2026-03-25_CANONICAL_DESK_COGNITION_VOCABULARY.json` for `raw_primitive` and `derived_feature`;
- `docs/planning/2026-03-31_SIGNAL_COEFFICIENT_AUTHORITY_GATES_v1.md`;
- `docs/planning/2026-03-31_SIGNAL_COEFFICIENT_AUTHORITY_LEAVES_v1.json`.

Historical evidence refs intentionally left pointing to the old workbook remain in the Phase 0 audit surfaces and old-gate receipts that specifically prove the earlier 20-sheet workbook state. Those refs are deliberate archive lineage, not active authority.

## Why this is honest

This gate does **not** pretend the old workbook never existed. It proves the relationship between the two files, freezes the canonical survivor, and keeps the predecessor only where historical proof still requires it.

## Receipt

- branch: `work/gate-157-parallel-risk-lane-planning-pack-20260402`
- start commit: current pack baseline after Gate 158
- closing proof command: `.venv/bin/python -m pytest -q tests/test_gate159_workbook_lineage_and_consolidation_audit.py tests/test_gate158_co_resident_parallel_risk_lane_law.py tests/test_gate157_parallel_risk_lane_foundation_bootstrap.py`
- observed result: `passed`
