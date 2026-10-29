# M01 F4 RC07 — consolidated authority-blocked continuation

Date: 12-10-2026. Branch continues RC06 HEAD `40bddf2f9cced4ebeddf4f3b42873be519775fc7` without rewriting its Git history. Status: **F4 IN PROGRESS; STAGE 1 NOT ACCEPTED; NOT A REVIEW CANDIDATE**.

## Authorised semantic repair completed

- Programme owner D104 formula: `(D100_now - D100_prior) - (D099_now - D099_prior)`. Separate skew families, same configured comparison anchor; exact selected historical pairs and reconstructable raw/predecessor lineage. No D099/D100 mathematical amendments.
- Proof-first Git commit: `500c796` (9 RED, one preliminary PASS). Production Git commit: `475b9b0`. Normative authorised clarification: `0120277`. Original mixed-family failing witness retained in its earlier Git lineage.
- D104 new focused suite: **10 passed**. F4 ledger regeneration accounts **0 unresolved closed-stage dependency edges** across 144 Stage-1-closed rows; zero-edge sentinel retained. This is dependency-edge reconciliation, **not** an assertion that all row-level acceptance propositions are completed.

## Source-semantic preflight

- See `SOURCE_SEMANTIC_PREFLIGHT_DISCREPANCY_REGISTER.md` (PF-01–PF-11), the **174-row** `STAGE1_174_ROW_SOURCE_MEANING_SURVEY.csv`, and `PREFLIGHT_READBACK.json`. Regenerate via `generate_source_semantic_preflight.py` (requires installed `artifact_tool` for authoritative workbook inspection).
- The sole historical F1/current catalogue raw dependency mismatch is the explicitly authorised D116 correction (`R041;R075` to `R041;R047;R048`), not a new normative defect.
- D123 official-period handling is provider-independent controlled M00 proof only; live IBKR/OCC period/revision mapping remains unverified.
- D117 R075 numerical source role and D138 book-state source contract are suspected/unverified issues, not accepted catalogue defects.

## Cross-stage evidence, classification and mandatory stop

Exact stage boundary: 174 Stage-1 rows, of which 144 closed and 30 require Stage-2 predecessor truth (25 direct, five transitive). The `CROSS_STAGE_30_ROW_PROOF_STATUS.csv` identifies every row, authority dependencies, test file and disposition. All 30 remain **NOT READY** for row-level own-kernel-plus-public-refusal acceptance.

- **28 rows** have new controlled own-kernel numerical/refusal cases; the D173 candidate-neighbour direct test already existed; **D186 is blocked**. Some own-kernel tests are bounded arithmetic, not full mandatory-dependency semantics (notably D178/D189/D192).
- **D097/D098/D107/D108** have additional public M00 absence/refusal checks, but those tests are boundary smoke checks and not all 30 have discriminating public refusal proofs.
- **D186**: normative brief §5 K08 demands D155 entry snapshot comparison, exact `EntryStateContextV1.d155_occurrence_id`, immutable versioned P_RULE feature weights/scales. Code attempts `entry.entry_state_vector`, which the actual `api.EntryStateContextV1` does not declare. Moreover, D186 code expects `similarity_weights/scales` as named pairs, while the admitted `CalculationParameterSetV1` rejects nested `(name, Decimal)` pairs within an immutable parameter tuple. The committed RED proof fails at parameter admission. The source-to-typed-contract representation is not authoritatively established. **Do not invent a serialisation or silently broaden every P_RULE parameter.** No D186 production change has been made.
- **D178** source rule calls for D133/D177 active execution-cost/edge-reserve bounds, but code does not apply those declared predecessor values in its calculation.
- **D189** source rule calls for D175 risk-capped hedge adjustment, but code ignores D175 and lacks an accepted Greek-exposure-to-risk-currency conversion.
- **D192** mandatory-hedge branch is conditioned on the hedge flag/adjustment, not on D175 actually being breached, contrary to accepted §5 precedence rule. The exact breach predicate is not admitted.

These are separate propositions; D186 is the clearest mandatory typed-parameter blocker. D178/D189/D192 have verified dependency-rule omissions and unresolved exact parameter/unit conversion prerequisites. No unauthorised Stage-2 kernels, unrelated catalogue changes or architecture modifications were made.

### One recommended programme-owner clarification

Issue **one consolidated, bounded normative/typed-contract clarification** specifying (a) the admitted immutable representation of D186's named P_RULE similarity weights/scales and retrieval of the entry D155 occurrence by `EntryStateContextV1.d155_occurrence_id`, and (b) the exact computable rules/units/parameter sources by which D178 uses D133+D177, D189 risk-clips against D175 and D192 establishes a D175 risk breach. Preserve accepted mathematical and dependency meaning. After authority, commit discriminating RED public/own-kernel proofs, repair these four distinct mechanisms under separate semantic commits, complete the remaining 30-row public refusal evidence, and rerun final-stage acceptance validation. Do not treat this blocked checkpoint as an independent reviewer submission.

## Current-tree validation and limitations

- Derived-signal product regression **667 passed**. Deliberately RED D186 contract test **excluded and separately recorded**; do not report whole product suite passed.
- Architecture/bootstrap suite **74 passed**; first collection failure from missing local Psycopg resolved without repository change.
- Broader `tests/architecture tests/bootstrap tests/product tests/implementation` **1,246 passed** against PostgreSQL 17.9 with distinct M00/M01 test roles. Excludes the intentionally RED D186 and the slow 55-case M00 durability module. Earlier environment-only failures due missing PyYAML and missing M00/M01 DSNs are retained, with successful rerun.
- M00 durability **55/55 case identities passed across four isolated pytest invocations** (20 + 9 + 1 + 25). The whole-module attempt was interrupted at 29, so do not claim a *single complete-run* PASS.
- Scoped Ruff lint/format and Mypy source checks passed. Repository-wide Ruff format not claimed; 62 inherited files needed formatting at preceding checkpoint.
- Generated source-semantic survey proves structural workbook ID presence and F1/current catalogue comparison; **not** exhaustive source-level mathematical certification.

All executed command logs are in `f4_20261012_final_checks`, `f4_20261012_d104_authorised`, or `f4_20261012_source_preflight`. The original D104 RED history, all accepted D116/D123 repairs and complete incoming Git ancestry are preserved. No Stage 1/Stage 2 programme acceptance is asserted.

## Delivery identity

The archive manifest outside the Git repository records final Git HEAD, tree, archive SHA-256 and extracted readback. The current handoff is an **authority-blocked preservation checkpoint** and not the next legitimate consolidated F4 acceptance review candidate.
