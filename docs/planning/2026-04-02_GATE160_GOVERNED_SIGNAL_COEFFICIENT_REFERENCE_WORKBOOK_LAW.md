Status: complete on `work/gate-157-parallel-risk-lane-planning-pack-20260402`; Gate 161 is now the active gate
# Gate 160 — Governed Signal Coefficient Reference Workbook Law

## What closed

Gate 160 is complete on `work/gate-157-parallel-risk-lane-planning-pack-20260402`. The canonical workbook now has a durable repo role: it is a governed live reference ledger with explicit discoverability, promotion lineage, update discipline, and a bounded risk-lane-relevant subset.

## Workbook class and home

- canonical workbook path: `data/reference/signal_workbooks/2026-03-25_NVDA_SIGNAL_WORKBOOK_v3_bounds_handoff_copy.xlsx`
- historical predecessor path: `docs/planning/2026-03-25_NVDA_SIGNAL_WORKBOOK_v3.xlsx`
- class: governed live reference ledger
- companion authority doc: `docs/reference/SIGNAL_WORKBOOK_AUTHORITY.md`

The workbook is discoverable, mandatory reference for workbook-derived promotions, and still **not** direct runtime authority.

## Promotion lineage

Workbook material promotes lawfully only through typed config/contracts. This gate freezes the path as:

1. workbook cell or workbook concept in `data/reference/signal_workbooks/2026-03-25_NVDA_SIGNAL_WORKBOOK_v3_bounds_handoff_copy.xlsx`;
2. typed promotion into config/contracts with explicit lineage such as `workbook_ref`;
3. runtime consumption from typed config/contracts only.

## Update classes

The gate freezes the update classes named in `docs/reference/SIGNAL_WORKBOOK_AUTHORITY.md`:
- workbook-only maintenance;
- structural workbook reorganisation;
- coefficient-bound or threshold changes;
- new signal-family or lane-relevant-family additions;
- vocabulary-affecting changes.

Each class now carries paired-update obligations so workbook maintenance cannot drift away from repo law.

## Bounded risk-lane workbook subset

Immediately relevant to the future parallel risk lane:
- `Bounds_Method`;
- `Signal_Coeff_Handoff`;
- `Temporal_Bounds_Draft`;
- `Runtime_Surface_Drivers`;
- `Coeff_Universe_Index` families for temporal thresholds, regime/macro stress, options-flow/translation, posture/permission, and bounded coefficient surfaces.

Background only, not primary gate drivers:
- `Raw_Catalog`;
- `Derived_Beta_Leadership`;
- `Derived_Vol_Rates_FX`;
- `Derived_Execution_Options`;
- `Derived_Asia_Breadth`;
- `Repo_Stage_Summary`;
- `Repo_Python_Inventory`.

## Why this is honest

This gate does not elevate the workbook into runtime authority. It makes the workbook visible, governed, and safe to update without leaving later threads to rediscover its role from chat memory.

## Receipt

- branch: `work/gate-157-parallel-risk-lane-planning-pack-20260402`
- start commit: current pack baseline after Gate 159
- closing proof command: `.venv/bin/python -m pytest -q tests/test_gate160_governed_signal_coefficient_reference_workbook_law.py tests/test_gate159_workbook_lineage_and_consolidation_audit.py tests/test_gate158_co_resident_parallel_risk_lane_law.py tests/test_gate157_parallel_risk_lane_foundation_bootstrap.py`
- observed result: `passed`
