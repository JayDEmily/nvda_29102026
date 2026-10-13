# NVDA research workbook V2 — Pass 01 preservation handoff

**Scope:** dedicated design branch; new `00_Guardrails & Method` sheet **only**. The future `01_Raw Signals` and `02_Derived Signal Index` are **not created**. No M01, M00, normative catalogue, accepted brief, software module or source workbook changes are authorised or performed.

## Source and authority

- Source: `handoff/m01_completion/authority/NVDA_80_STEP_ACADEMIC_EVIDENCE_AUDIT_WITH_SIGNALS_ADDENDUM_81_94.xlsx`.
- Exact V1 SHA-256: `519ea9449297d564ae4a02afc1bf4e60e4471631c81a0842620f9fb60bb4f9ae`.
- V1 is reference research evidence, not current M01 implementation authority; `handoff/m01_completion/AUTHORITY_INDEX.md`, accepted M01 brief, and the effective normative CSV govern M01 implementation. `GUARDRAILS.md` and `EXEC_PLAN.md` retain their jurisdictions.
- Base HEAD before design branch: `585fccc95521fb22e17348e77bd665198a8ec675` (paused M01 Stage 1, not accepted; Stage 2 not started).

## Exhaustive source inspection

The source workbook was parsed in full, including every populated cell and all original column definitions in the relevant two worksheets. The review checked every R/D record rather than sampled examples.

| V1 worksheet | Header row | Source rows | Data records | Populated worksheet cells | Families |
|---|---:|---:|---:|---:|---:|
| `Raw Signals` | 4 | 5–327 | 323 | 7,517 | 19 |
| `Derived Signals` | 4 | 5–213 | 209 | 2,637 | 34 |

**Actual data observations used in rule design:** all original 25 Raw columns A:Y and 15 Derived columns A:O; source/native field identity and timestamp meaning; 19/34 source families; status labels; dependencies with three D-source blanks (`D007`, `D204`, `D205`); academic framework-step links; source notes; original titles explicitly distinguishing calculation concepts from equations. Provider/status labels do not establish live market-data access. Original family names do not assign module ownership. Original D raw/derived columns do not supersede the current normative M01 catalogue.

`PASS01_SOURCE_ROW_DIGESTS.csv` records **each original source row** (532 total) with original Excel row, ID, family, count of populated cells and SHA-256 over its nonempty source cell values/formulas. `PASS01_SOURCE_CENSUS.json` records source counts and complete readback results. The original workbook provides the underlying cell values; the digest register is evidence, not substitute authority.

## Workbook change

- New file: `NVDA_SIGNALS_RESEARCH_WORKBOOK_V2_PASS01.xlsx`.
- Exactly one new worksheet: `00_Guardrails & Method`, containing **35** separately identified, evidenced rules in four sections.
- Sections: A. Jurisdiction/source fidelity (6); B. future 01 raw source contract (12); C. future 02 derived ID/family contract (12); D. verification/future-pass restrictions (5).
- The seven original worksheets are carried forward unchanged in content and inspected XML row/column layout. The new `00` worksheet is **appended**; original tab order is intentionally preserved at Pass 01, not rearranged.

## Verification performed

Reproducible scripts: `pass01_build.py`, `pass01_verify.py`.

- V1 hash preflight asserted before building V2.
- V1 row IDs exhaustively checked against `R001`–`R323` and `D001`–`D209`, one of each.
- All seven original sheets compared source-to-output: same cells/values/formulas, merges and hyperlinks; row and column XML attributes also equal.
- Original sheet names remain unchanged; no `01_Raw Signals` or `02_Derived Signal Index` created.
- New worksheet rule identifiers: 35 unique.
- V2 was re-imported and read from the exported XLSX; targeted content, formula-error scan and a visual render of the header were inspected.
- Commit, full Git integrity and archive extraction readback are performed separately at checkpoint close-out and recorded in the final conversation response.

**Not established by this pass:** current API connectivity, academic validity, correctness of original research, 209 equations, independent D-signal proofs, programme acceptance of a revised architecture, or new module boundaries.

## Resume boundary

Continue from this branch, reread repository governance and original source workbook. The next pass may touch `01_Raw Signals` or `02_Derived Signal Index` **only upon new programme-owner instruction**. Do not interpret the 35 rules as a completed V2 governance system beyond the two identified future worksheets.
