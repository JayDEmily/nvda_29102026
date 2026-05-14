# Gate 41 — Raw and Derived Signal Workbook Separation

Status: complete on `main`

## Purpose

Separate raw primitives from derived features in the NVDA signal workbook so source truth, feature engineering, and module consumption stop leaking into each other.

## Closed scope

- Split the workbook doctrine into `Raw_Primitives_Catalog` and `Derived_Features_Catalog`.
- Kept the legacy mixed catalog only as a continuity sheet and marked it non-authoritative.
- Added `Options_Chain_Raw_Spec` to define quote-row capture by expiry × strike × side.
- Added `Playbook_Module_Audit` so playbook families, data dependencies, and rewrite needs are visible in one place.

## Binding rules

1. Direct vendor/feed captures belong in raw only.
2. VWAP, realised-vol, skew, term, pin, gamma, and participation ratios belong in derived only.
3. Playbooks must read derived state from deterministic services, not invent ad hoc chain maths inside each module.

## Artifact

- `2026-03-25_NVDA_SIGNAL_WORKBOOK_v3.xlsx`

## Result

Gate 41 is closed. The workbook now treats raw and derived surfaces as separate authority layers.
