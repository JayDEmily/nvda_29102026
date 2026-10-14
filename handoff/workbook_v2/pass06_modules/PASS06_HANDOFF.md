# Pass 06 — Working downstream module names in Workbook V2

**Date:** 14 October 2026 (Australia/Melbourne)
**Authority:** Direct programme-owner instruction to treat the previously proposed 30 responsibility groups as modules, label them M02–M31, preserve M00 and M01-1 as shared foundations, and deliberately duplicate strategy-dependent intermediate code when multiple downstream modules need it.
**Starting commit:** `8dd4a6b86b0158f7c0dba18acea44292e5638eaa`
**Scope:** V2 design workbook and decision/evidence documents only.

## Committed outputs

- `handoff/workbook_v2/NVDA_SIGNALS_RESEARCH_WORKBOOK_V2_PASS06.xlsx`
- `handoff/workbook_v2/decisions/ADR_WBV2_002_DOWNSTREAM_MODULES_LOCAL_DUPLICATION.md`
- `handoff/workbook_v2/pass06_modules/PASS06_30_MODULE_REGISTER.csv`
- `handoff/workbook_v2/pass06_modules/PASS06_95_D_MODULE_ALLOCATIONS.csv`
- `handoff/workbook_v2/pass06_modules/PASS06_107_CROSS_MODULE_D_REFERENCES.csv`
- `handoff/workbook_v2/pass06_modules/verify_pass06.py`
- `handoff/workbook_v2/pass06_modules/PASS06_VERIFICATION.json`

## Result

- 30 new independently labelled design worksheets `M02` through `M31`, using the one-to-one source group mapping `P01=>M02` ... `P30=>M31`; the module register contains those exact names and D-ID memberships.
- Complete 95-row index mapping excluded signals to proposed modules exactly once. The original 114 proposed M01-1 signals are retained in their unmodified original candidate worksheet.
- Six additive workbook guardrails `M-001`–`M-006` record the shared foundation, module-local duplication rule, D-identity and architecture-governance boundaries.
- Source 7 workbook tabs and the prior M01-1 tab are unchanged in all populated cells, formulas, styles, merges, hyperlinks, widths and row structure. Existing guardrail cells in `00` are preserved; only the new six rules were appended.
- 107 direct D-references currently cross proposed module boundaries; they represent 67 unique ordered module-pairs. This workbook pass does **not** migrate them. They are explicit outstanding interface/duplication-design obligations.

## Deferred

No production module allocation, duplicated code, tests, runtime routing, canonical D-occurrence changes, dependency rewrites, strategy coefficients or M01 Stage-2 work. The 30 module identities are **working design names**, not installed or registered M-owners. Original `D001–D209` canonical IDs, source evidence and accepted M01 graph are unchanged. The 30-group responsibility review is retained for subsequent source and semantic challenge.

## Reproduce static verification

From repository root:

`python handoff/workbook_v2/pass06_modules/verify_pass06.py`

This verifies source preservation, 30 module labels, 95 exact assignments, the M01-1 split, all six additive rules and the listed cross-module normative dependencies. It is **not** executable-module or test-suite acceptance evidence.
