# V2 Pass 02 — classification field separation

**Programme-owner approval:** 14 October 2026, to maintain separate `Family` and `Calculation class` fields for the future `02_Derived Signal Index`.

**Scope of this checkpoint:** extend only the existing `00_Guardrails & Method` in a separate V2 workbook. Do **not** create `01_Raw Signals` or `02_Derived Signal Index`. No M01 or original workbook alterations. The original Pass 01 V2 workbook stays available in Git, unchanged.

## Pre-existing family audit is committed

At incoming Git `HEAD` `5cf90f40d6adf7a1aa0b4b3354f183dd001b2a5d`, these review evidence files already exist in the committed tree:

- `reviews/derived_family_audit_20261014/NVDA_DERIVED_FAMILY_RECOMMENDATION_20261014.md` — complete recommendation report;
- `reviews/derived_family_audit_20261014/NVDA_DERIVED_FAMILY_209_ROW_REVIEW_20261014.xlsx` — 209-row review;
- `reviews/derived_family_audit_20261014/NVDA_DERIVED_FAMILY_FULL_209_ROW_AUDIT_20261014.csv` — 209 D-ID crosswalk;
- `reviews/derived_family_audit_20261014/NVDA_DERIVED_FAMILY_PROPOSED_40_DEFINITIONS_20261014.csv` — definitions;
- `reviews/derived_family_audit_20261014/NVDA_DERIVED_FAMILY_AUDIT_SUMMARY_20261014.json` — summary.

No replacement or rewrite of the existing review files is authorised by this checkpoint. These remain *proposals*, not accepted domain or implementation authority. The 40-family taxonomy has not been approved for adoption merely because the two-field scheme was approved.

## Future `02` field contract

- **`Family`**: current research grouping by subject/responsibility. Until a classification change is approved, it equals the original V1 `Family` value for the D-ID. A distinct immutable `Original family (V1)` field retains V1 provenance; a separate `Proposed family (review only)` records the 40-family proposal. The latter cannot be silently promoted to `Family`.
- **`Calculation class`**: independent category describing the mathematical or operational character of that D-signal. No value is assigned on the strength of a family label, the concept text, a paper citation, or the M01 kernel alone. Its admissible categories and each per-D assignment require evidence and subsequent scope approval.
- **`Calculation class status`**: explicit `UNASSESSED` with blank class value until actual classification; a blank is not a pass. `Family` and `Calculation class` are **two distinct columns** and each can change only under its own traceable decision.

`reviews/derived_family_audit_20261014/NVDA_FUTURE_02_TWO_FIELDS_209_ROW_PREVIEW_20261014.csv` is a **research preview only**, not a new workbook tab or normative catalogue. It demonstrates both fields for exactly 209 D-IDs, carrying original `Family`, review-only proposed family and a deliberately blank `Calculation_class` plus `UNASSESSED` status. It does not classify mathematical semantics.

## Workbook delta

- Preserve the original seven sheets (same values/formulas and structural source relationships).
- Keep `00_Guardrails & Method`, retaining all 35 Pass 01 rule IDs/content.
- Add `C-001` through `C-006` to its existing rule structure, establishing the mandatory separate fields, original/proposed-family distinction, row-specific calculation-class evidence, unassessed status, change control and M01 jurisdiction.
- Still no `01_Raw Signals` or `02_Derived Signal Index` worksheet.

**Deferred:** approve/reject the 40-family proposal and separately derive calculation-class taxonomy and 209 per-row assignments; creating/populating future `01`/`02`; revising M01 ownership/implementation. None was done by this checkpoint.
