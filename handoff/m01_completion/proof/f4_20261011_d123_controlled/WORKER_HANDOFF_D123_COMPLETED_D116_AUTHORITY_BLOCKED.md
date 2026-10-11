# M01 F4 — D123 controlled official-period correction; D116 source-authority STOP

**Date:** 11-10-2026. **Status:** `BLOCKED` (not F4 candidate, not Stage-1 acceptance).
**Base Git checkpoint:** `bd45dfb48f4e0721e23ea12d02aab875bc33c33d`.
**Delivery head/tree:** consult top-level `CHECKPOINT.json` in the enclosing single full-Git handoff archive; this file is committed before that final immutable hash exists.

## Current authority, bounds and chronology

The 11-10-2026 Programme-Owner instruction “M01 F4 — D123 Provider-Independent Official Open-Interest Proof” supersedes the earlier *live provider source-contract prerequisite* solely for controlled, explicitly versioned M00 public projections. The previously authorised D123 conditional call R047 / put R048 semantics remain binding. Source-integrated IBKR tick 27/28 reporting period and any OCC reporting-period mappings are **unverified**; synthetic controlled identity fields are not presented as provider-native fields. GUARDRAILS.md, AGENTS.md, active EXEC_PLAN.md, M00 ownership, normative catalogue rows and Stage-2 scope were not changed.

### Proof-before-production trace

1. Original +25-contract D123 public failure preserved by earlier checkpoint `bd45dfb` and its ancestors; missing official identity refusal retained separately in `test_m01_f4_d123_official_reporting_identity_red.py`.
2. RED tests committed `66269e0`, refined `eac6777`: controlled records admitted through the actual M00 public owner and mapped `RawSelectionIdentityV1`, with exact call/put/period/revision/version data. Original +25 result retained, not relaxed. `D123_PROOF_FIRST_RED.log` captures the failing pre-repair public cases.
3. Production repair committed `538bd02`: D123 selects exactly one applicable side R047 or R048, groups by explicit official reporting period and order, selects unambiguously highest revision precedence *per period*, uses current minus prior, and persists only the two selected versioned raw observations. The first D123 +25 witness now supplies an explicit controlled official-period record. Direct-kernel and public-interface tests both exercise the admitted path. `D123_FOCUSED_INITIAL_GREEN.log` and final logs give results.
4. Added PostgreSQL public durability/lineage proof in `tests/implementation/derived_signal/test_m01_f4_d123_controlled_postgresql.py` using separate M00 and M01 PostgreSQL role DSNs; exact result `+25`, mapping/unit version readback, exactly two underlying raw occurrence IDs, and retry stability. Its current result appears in `D123_POSTGRESQL_PUBLIC_LINEAGE_PASS.log` and `D123_FOCUSED_PUBLIC_AND_POSTGRESQL_FINAL.log`.

### Controlled M00 reporting-period contract

`handoff/m01_completion/authority/D123_CALCULATION_DEFINITION_AUTHORISED_CLARIFICATION_20261011.md` records the chronological authority amendment: `official_reporting_period_id`, `official_reporting_period_order`, `official_revision_id`, `official_revision_precedence` are **controlled test-contract** selection identity keys, mapped via existing M00 `RawSignalProjectionMappingV1.selection_identity_field_paths` with provider/variant and version references. Chronological period ordinal and per-period revision rank are explicit integers in controlled records only, not assumptions about IBKR. Missing, contradictory or ambiguous identities refuse. Actual live tick records lacking this source contract must fail closed.

### Verification actually performed

The exact generated logs in this directory are the controlling evidence, not a blanket success claim:

- 17 focused public, refusal, contract and M00-to-M01 PostgreSQL tests passed (`D123_FOCUSED_PUBLIC_AND_POSTGRESQL_FINAL.log`).
- 543 derived-product tests passed (`DERIVED_PRODUCT_543_PASS.log`).
- 1,120 architecture/product/implementation tests passed **with the separate M00 durability test file excluded** (`BROAD_ARCHITECTURE_PRODUCT_POSTGRESQL_1120_PASS.log`); this included the D123 PostgreSQL proof. Local PostgreSQL 17.9 fresh instance used distinct M00/M01 user roles and `fsync=on`, `synchronous_commit=on`, `full_page_writes=on`.
- Ruff lint passed (`RUFF_RECHECK.log`); Mypy 21 source files passed (`MYPY_RECHECK.log`); F4 ledger regeneration and integrity assertions succeeded (`F4_RECONCILIATION_RECHECK.log`).
- The first PostgreSQL failure log is stored **gzip-compressed without changing the bytes on decompression** to preserve the original whitespace in this raw pytest traceback while maintaining clean Git whitespace checks.
- The entire suite including `tests/product/raw_signal/test_u05_postgresql_durability.py` **did not complete** in this run: initial environment role setup had a CREATE privilege issue, corrected locally; another combined run was interrupted before its 55-case durability portion finished. Older historical RC14 evidence of 55 cases does not substitute for a fresh full-suite pass at this HEAD.
- Ruff `format --check` returned nonzero (four files would be reformatted, including preexisting production layout); Ruff **lint** passed. This is independently recorded in `RUFF_FORMAT_CHECK_NOT_PASS.log`, not silently reported as a pass.
- Real IBKR/OCC reporting-period field mapping and real-provider integration: **not executed, not verified**.

### Separate first unresolved F4 authority invariant — D116 / R075

`F4_20261011_D116_R075_SOURCE_AUTHORITY_CONFLICT.md` (in `handoff/m01_completion/proof/f4_20261009/`) records primary accepted-source evidence: the fixed M01 brief states **D116 = option_volume / open_interest**, the normative catalogue declares D116 raw dependencies **R041;R075**, but the source workbook `Raw Signals!A79:Y79` specifies **R075 = Average Option Volume** (IBKR tick 87; contracts/day). R047/R048 are actual call/put open interest sources in that workbook. The earlier RC14 numerical witness mislabeled controlled R075 as OI; it proves the numeric division, not source/denominator validity. No production, R075, D116, catalogue or brief alteration was made. This is NOT an exception granted by the D123 Programme Owner instruction.

**One required Programme-Owner decision:** retain fixed D116 volume/open-interest arithmetic and explicitly authorise correcting the D116 dependency to right-appropriate R047/R048, *or* explicitly authorise a different D116 denominator plus complete necessary normative/proof synchronisation. The former preserves the accepted arithmetic and is recommended, subject to the owner’s decision. D117/R075 is not conflated with D116.

### Conservatively regenerated F4 census at stop

- Catalogue dependency edges **490**, Stage-1 kernels **174**, closed Stage-1 rows **144**, cross-stage rows **30**.
- D123 **2** conditionally applicable raw edges now bounded provider-independent public proof.
- D116 **2** edges now classified `F4_AUTHORITY_BLOCKED_SOURCE_SEMANTICS`, not falsely counted as valid proof.
- **54** other unproved Stage-1-closed edges across **12** rows. **One additional blocked D116 row**, giving 13 closed rows lacking sufficient acceptance evidence.
- **30** cross-stage own-kernel/public refusal proof obligations remain unproved; **107** cross-stage predecessor edges deferred.
- Ledger source and regenerated outputs: `handoff/m01_completion/proof/f4_20261009/f4_progress_readback.py`, `F4_PROGRESS_READBACK.json`, `F4_RELATIONSHIP_PROOF_LEDGER.csv`, `F4_ROW_EVIDENCE_MATRIX.csv` and `F4_CLASS_PROOF_RECONCILIATION.csv`.

**Stop law:** no F4 or Stage-1 acceptance candidate is asserted. Resume only after the distinct D116/R075 normative-source decision; do not overwrite this history, relax tests or represent controlled D123 proof as live provider integration.
