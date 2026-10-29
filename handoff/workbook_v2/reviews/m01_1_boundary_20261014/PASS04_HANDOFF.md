# Workbook V2 — Pass 04: M01-1 candidate semantic boundary

**Status:** COMPLETED AS A RESEARCH-CLASSIFICATION PROPOSAL; not programme acceptance, M01 architecture mutation, or 114 individual proofs.

## Programme-owner direction and authority

The Programme Owner directed that the proposed module criteria be committed on the active Workbook V2 work branch, that each D001–D209 be individually classified as M01-1 derived raw market calculation or not, and that the V2 workbook receive a worksheet containing only proposed M01-1 signals.

The new proposal record is `handoff/workbook_v2/decisions/ADR_WBV2_001_MODULE_RESPONSIBILITY_CLASSIFICATION.md`. It does **not** edit or supersede the frozen root `GUARDRAILS.md`, accepted M01 brief, normative CSV, active `EXEC_PLAN.md`, source code or independent review authority. **M01-1 is a proposed designation, not a registered software module.**

## Inputs inspected

- All 209 D001–D209 rows in current effective `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv`, covering every named column, source R dependencies, predecessor D dependencies, calculation concept, fixed kernel, profile, typed contexts and cited governing rule. SHA-256: `26c5486d1a4c7ff68025c7ce2d7e6847a7798759b847a716c942fd05345f3803`.
- Original 209 source rows of the reference workbook `Derived Signals` (A5:O213), and the 323 raw-source inventory `Raw Signals` (A5:Y327), distinguishing market/time/calendar feeds from M00 account, positions and order/execution feeds. Original workbook SHA-256: `519ea9449297d564ae4a02afc1bf4e60e4471631c81a0842620f9fb60bb4f9ae`.
- Accepted M01 brief §5 (all K01–K17 kernels and exact row-specific mathematics), §§6–9 (non-signal inputs, normative dependencies, history and typed raw projection), authorised amendments indexed at `handoff/m01_completion/AUTHORITY_INDEX.md`.
- Existing 209-row proposed family and 13-class audits as **review context only**. Neither family nor calculation class was used as a mechanical substitute for row-level assessment.
- Current root repository governance `GUARDRAILS.md`, `AGENTS.md` and accepted `EXEC_PLAN.md`.

## Exact review output

- **114 YES — proposed M01-1 semantic eligibility**, displayed exclusively in new V2 tab `M01-1 Derived Raw`.
- **95 NO — not admitted to M01-1 at this time**, retained as original D rows and the full 209-row audit; these may become downstream modules or might require fixed-definition clarification to reconsider.
- Full row evidence: `M01_1_FULL_209_ROW_ELIGIBILITY_REVIEW.csv` (one YES/NO, exact source row, original/proposed family, proposed calculation class, source and effective concepts, raw/D dependencies, kernel/profile/context, explicit reason, assessment and code/test-proof status).
- Candidate-only workbook: `handoff/workbook_v2/NVDA_SIGNALS_RESEARCH_WORKBOOK_V2_PASS04.xlsx`; original seven source worksheets plus `00_Guardrails & Method` are carried forward unchanged from Pass 02. **Future `01_Raw Signals` and `02_Derived Signal Index` remain uncreated.**

### Selected boundary witnesses

| D-ID | Result | Row-specific rationale |
|---|---|---|
| D035 | YES | Fixed historical five-day realised-volatility estimator using market price returns with required complete history; window is a versioned measurement convention |
| D042 | YES | Defined Treasury 10-year minus 2-year slope, converted to percentage points from market rate signals |
| D079 | YES, conditional on fixed measurement convention | OLS fitted beta from upstream market-return histories. Coefficients are fitted *outputs*, not tuned playbook weights; exact factor, window and sample subset must remain definition-bound |
| D096 | YES, conditional on fixed interpolation convention | Deterministic 50-delta IV linear interpolation; a separate extrapolation/model variant is **not** admitted by this proposal |
| D104 | YES | Authorised change in relative 10-delta/25-delta skew from qualified upstream D099 and D100 |
| D091 | NO | Externally versioned delta-bucket thresholds not established as a single immutable non-discretionary measurement definition |
| D109, D110, D121 | NO | Depend directly or transitively on D091, so cannot pass whole-graph qualification until that predecessor does |
| D141, D142 | NO | Configurable replenishment/recovery event thresholds need fixed non-strategy definition evidence |
| D151 | NO | Canonical variant permits externally weighted basket, not yet a fixed non-strategy measurement rule for the entire D identity |
| D125–D130 | NO | Inferred dealer-side assumptions, scenario revaluation and model-dependent exposure |
| D175–D176 | NO | Permissible monetary risk limits and position sizing are strategy/portfolio policies |
| D204 | NO | Brier-score arithmetic is deterministic, but its inputs are a forecast-evaluation set, not solely raw market signals |

**Boundary caveat:** semantic YES does not mean an individual tested production calculation is proved. All 209 rows explicitly state `NOT_INDIVIDUALLY_VERIFIED_IN_THIS_PASS` for implementation and independent test proof. Source-level code/test verification, exact P-profile freezing for individually marked rows, actual model allocation and M01 governance remain future separately authorised work. NO due insufficient fixed semantics is not proof of permanent ineligibility.

## Checks executed

`python handoff/workbook_v2/reviews/m01_1_boundary_20261014/build_pass04.py`

`python handoff/workbook_v2/reviews/m01_1_boundary_20261014/verify_pass04.py`

The independent readback checks:

- 209 unique D identifiers, one YES/NO each, with current effective authority dependencies and original V1 row locators;
- no accepted YES-to-NO predecessor D edges, and no direct account, position or order/execution R205–R235 edges from an eligible D;
- 114 and only 114 expected eligible D IDs appear in the added worksheet in source order;
- eight pre-existing V2 worksheets are unchanged cell-for-cell, formulas, merges, hyperlinks and row/column structures;
- source digests match the exact accepted reference/effective authority files;
- no accepted M01 source/authority/runtime module content is modified by this V2-only pass.

Proof receipts are in `M01_1_AUDIT_SUMMARY.json` and `PASS04_VERIFICATION.json`. These checks prove the **review artefact's fidelity and classification accounting**, not the semantic correctness of each classification or individual mathematical/independent-test proof.

## Non-adoptions

The prior proposed 40-family restructuring, prior proposed 13 calculation classes, and the new 114-row M01-1 proposal remain **separate, not automatically accepted** review materials. No Stage 2, playbook, other-module architecture admission, test migration, M01 implementation or downstream strategy work was performed.
