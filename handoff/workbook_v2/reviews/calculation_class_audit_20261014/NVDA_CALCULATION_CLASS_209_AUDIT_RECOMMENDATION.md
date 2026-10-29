# Workbook V2 — Calculation-class proposal for D001–D209

**Status: REVIEW EVIDENCE ONLY — not an accepted taxonomy, normative amendment, M01 review, or implementation authority.**

**Baseline:** V2 branch `work/workbook-v2-pass01-guardrails-method-20261014`, incoming commit `261ecdd81ccb26019c2d36481d95da2f8dba199d`. Current user direction: continue incremental V2 work; previously approved two distinct future index columns, `Family` and `Calculation class`. This pass proposes the second field's definitions and a row-by-row classification but does not adopt it.

## Inputs actually inspected

1. The exact original V1 workbook, all **209 Derived Signals rows (A5:O213), all 15 cell values per row**, including headers/notes: `handoff/m01_completion/authority/NVDA_80_STEP_ACADEMIC_EVIDENCE_AUDIT_WITH_SIGNALS_ADDENDUM_81_94.xlsx`; SHA-256 `519ea9449297d564ae4a02afc1bf4e60e4471631c81a0842620f9fb60bb4f9ae`. Each V1 row is fingerprinted across its complete 15-cell value vector in the CSV.
2. All **209 effective M01 catalogue rows** (all 18 named columns), including each row's R/D dependencies, kernel, parameter profile, authority class, typed contexts, units and calculation concept: `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv`; SHA-256 `26c5486d1a4c7ff68025c7ce2d7e6847a7798759b847a716c942fd05345f3803`.
3. Every row of the prior V2 209-row family audit and 209-row future-index preview, together with V2 Pass 02's `C-001`–`C-006` separation/approval rules.
4. Root `GUARDRAILS.md`, `AGENTS.md`, `EXEC_PLAN.md`, M01 authority index, and D116 authorised correction. The original V1 workbook supplies research-reference meaning; the current effective M01 catalogue and authorised amendments govern M01 implementation.

## Proposed computational classification

Exactly one **primary proposed** calculation class per D-ID. This class is independent of its present or proposed family, and is NOT inferred mechanically from its M01 kernel.

| Code | Proposed class | D-signal count |
|---|---|---:|
| C01 | Temporal and data integrity | 9 |
| C02 | Market deterministic transform | 86 |
| C03 | Descriptive statistical estimate | 28 |
| C04 | Model-based market inference | 17 |
| C05 | Configured composite score | 22 |
| C06 | Structured state assembly | 1 |
| C07 | Candidate economic measurement | 9 |
| C08 | Live portfolio economic measurement | 8 |
| C09 | Policy and decision rule | 11 |
| C10 | Execution outcome measurement | 3 |
| C11 | P&L path attribution | 6 |
| C12 | Retrospective model/decision evaluation | 8 |
| C13 | Operational recalculation scheduling | 1 |
| **Total** | | **209** |

Positive definitions and exclusion boundaries are in `NVDA_PROPOSED_13_CALCULATION_CLASSES.csv` and the **Class Definitions** worksheet. `NVDA_209_CALCULATION_CLASS_REVIEW_ONLY.csv` and the **209 Row Audit** worksheet contain the individual classification reasoning and exact V1 and normative row evidence.

This is NOT the earlier 122/87 test of whether calculations can be isolated from strategy. The 13 categories separate the character of outputs and calculations; they do not certify raw-market-only inputs, strategy independence, a complete mathematical definition, unit-level implementation or independent tests.

## Two-field separation demonstrated

- **21 of 34 original V1 families** contain more than one proposed calculation class.
- **8 of 17 effective M01 kernels** contain more than one proposed calculation class.
- The family label therefore cannot determine the calculation class, and the kernel identifier cannot replace per-row output/context analysis.
- Original V1 family remains preserved; the 40-family restructuring stays an unapproved review proposal.
- The approved `Calculation class` field remains **blank and UNASSESSED** in all 209 future-02 preview rows. Only the separately named **Proposed class review** column is populated. No family reassignment or `02_Derived Signal Index` tab was made.

## Differences between V1 and the effective catalogue

These differences must be retained as evidence, not silently reconciled by choosing the old value or rewriting source history:

- **22** rows have a different direct R-dependency identifier set.
- **13** rows have a different direct D-dependency identifier set.
- **One** row has a different calculation-concept string: **D116**. The V1 concept permitted comparison with historical average option volume; the 11 October authorised correction fixes D116 to exact-contract option volume / applicable CALL or PUT open interest. `R075` is not an alternative denominator. See `handoff/m01_completion/authority/D116_CALCULATION_DEFINITION_AUTHORISED_CORRECTION_20261011.md`.
- Differences in dependency declarations may arise from the accepted brief or approved amendments; the audit does **not** classify those differences as defects. Both versions and per-D `SAME/DIFF` flags are preserved in the row audit. Only one concept-text difference was observed; this does not assert every other source field has equivalent legal meaning.

## Cases reserved for explicit adjudication

**46 D-identifiers** carry a `YES` `Adjudication_Needed` flag in the row audit. Examples include D007 (RequiredFieldPolicy), D078–D082 (conditional regression), D096/D102 (surface conventions), D104 (authorised skew equation), D125–D130 (inferred dealer exposure), D155–D159 (mixed model/state/quality), D175/D189 (risk policy), D200/D201 (retrospective evaluation) and D208 (signal disposition). This flag is **review priority, not a claimed failing calculation**. No unflagged row is independently accepted by omission.

## Verification and changes

- One proposal per D001–D209, no duplicate or omitted identifier. All 209 are mapped to exactly one of the 13 proposed codes.
- Exact source-row identity, source family, source concept, and effective catalogue identity cross-checks are enforced by the generator. V1/current concept mismatch for D116 is captured explicitly.
- Export readback checks 209 rows and 209 blank/UNASSESSED future-index class fields.
- New content is confined to this review folder. The original workbook and V2 Pass 01/02 workbooks, accepted brief/catalogue, root `EXEC_PLAN`, M00/M01 source and tests remain unchanged.

**Next decision, not executed:** independently review and accept/amend the class taxonomy and each D-signal assignment before populating any accepted `02` column. Separately approve/reject the proposed 40-family taxonomy; the two decisions are independent.
