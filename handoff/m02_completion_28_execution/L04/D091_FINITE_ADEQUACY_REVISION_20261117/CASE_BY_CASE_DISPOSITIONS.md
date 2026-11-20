# Exact finite case dispositions - revised proposed preparation

Reference reviewed candidate: `0a549c11feef999ec985c90f4c7fd0599037eb06`; independent RETURN: `ff18a84c14bf7b9a21b608933be177d538176ed6` (separate reviewer branch, not merged).
Every row is a separately proposed physical execution, **not an observed PASS**. No exact current accepted proof reuse is established. All original 32 retain their IDs; one new pre-seal case is proposed.

## Independent per-case inventory

| Jurisdiction | Proposed ID | Decision | Discriminating reached predicate / output | Witnesses |
| --- | --- | --- | --- | --- |
| D091 | `D091-CONTROLLED-SUCCESS` | RETAIN_DISTINCT_CONDITIONAL_ON_TRUE_PUBLIC_SEAM | CATEGORY_DURABLE_REOPEN_AND_IDEMPOTENT_RETRY; PUBLIC_M00_RAW_AND_PAGED_R112_TO_D091_SELECTOR | P01_ZERO, P02_NEGATIVE_TENTH, P03_POSITIVE_TENTH, P04_NEGATIVE_QUARTER, P05_POSITIVE_QUARTER, P06_NEGATIVE_HALF, P07_POSITIVE_HALF, P08_NEGATIVE_THREE_QUARTERS, P09_POSITIVE_THREE_QUARTERS, P10_NEGATIVE_ONE, P11_POSITIVE_ONE, P12_INTERIOR, P13_TWO_PAGE_HISTORY, P14_DURABLE_PUBLIC_REOPEN, P15_RETRY_FIRST_TIMESTAMP, D04_FIRST_TIMESTAMP_PRESERVED |
| D091 | `D091-CONTROLLED-REACHED_REFUSAL` | RETAIN_DISTINCT_CONDITIONAL_ON_TRUE_PUBLIC_SEAM | RANGE; PUBLIC_M00_RAW_AND_PAGED_R112_TO_D091_SELECTOR | R01_EXACT_ONE_POINT_ZERO_ONE_RANGE |
| D091 | `D091-CONTROLLED-SEAL-REFUSAL` | RETAIN_DISTINCT_CONDITIONAL_ON_TRUE_PUBLIC_SEAM | COORDINATOR_POSTSEAL_INGRESS_REFUSAL; PRIVATE_COORDINATOR_GENUINE_POSTSEAL_SOURCE_INGRESS | S01_PRESEAL_PUBLIC_15_ADMISSIONS, S02_IMMUTABLE_SEAL, S03_DIRECT_POSTSEAL_LAWFUL_ADMISSION_REFUSED, S04_NO_COMMAND_ALIAS_ESCAPE, S05_UNCHANGED_IDS_BEFORE_AFTER_PAGINATION |
| D091 | `D091-CONTROLLED-NONFINITE-REFUSAL` | RETAIN_DISTINCT_CONDITIONAL_ON_TRUE_PUBLIC_SEAM | NONFINITE; PUBLIC_M00_RAW_AND_PAGED_R112_TO_D091_SELECTOR | O01_NAN_NONFINITE |
| D091 | `D091-CONTROLLED-ABSENT-REFUSAL` | RETAIN_DISTINCT_CONDITIONAL_ON_TRUE_PUBLIC_SEAM | ABSENT; PUBLIC_M00_RAW_AND_PAGED_R112_TO_D091_SELECTOR | O02_ABSENT_MODEL_DELTA |
| L01b | `L01B-R112-CONTROLLED-NATIVE-UNITS-REFUSAL` | AMEND_FIELD_SPECIFIC_REACHABILITY_RETAIN_DISTINCT | COORDINATOR_SOURCE_FIELD_REFUSAL; observation.native_units | O03_WRONG_ORIGINAL_NATIVE_UNITS |
| L01b | `L01B-R112-CONTROLLED-SOURCE-PROVIDER-REFUSAL` | AMEND_FIELD_SPECIFIC_REACHABILITY_RETAIN_DISTINCT | COORDINATOR_SOURCE_FIELD_REFUSAL; observation.source_provider | O04_WRONG_PROVIDER_VARIANT |
| L01b | `L01B-R112-CONTROLLED-SOURCE-VARIANT-REFUSAL` | AMEND_FIELD_SPECIFIC_REACHABILITY_RETAIN_DISTINCT | COORDINATOR_SOURCE_FIELD_REFUSAL; observation.source_variant | O04_WRONG_PROVIDER_VARIANT |
| L01b | `L01B-R112-CONTROLLED-CONTRACT-ID-REFUSAL` | AMEND_FIELD_SPECIFIC_REACHABILITY_RETAIN_DISTINCT | COORDINATOR_SOURCE_FIELD_REFUSAL; observation.native_record.identity.contract_id | O05_WRONG_CONTRACT_OR_MODEL_IDENTITY |
| L01b | `L01B-R112-CONTROLLED-UNDERLYING-REFUSAL` | AMEND_FIELD_SPECIFIC_REACHABILITY_RETAIN_DISTINCT | COORDINATOR_SOURCE_FIELD_REFUSAL; observation.native_record.identity.underlying | O05_WRONG_CONTRACT_OR_MODEL_IDENTITY |
| L01b | `L01B-R112-CONTROLLED-SECURITY-TYPE-REFUSAL` | AMEND_FIELD_SPECIFIC_REACHABILITY_RETAIN_DISTINCT | COORDINATOR_SOURCE_FIELD_REFUSAL; observation.native_record.identity.security_type | O05_WRONG_CONTRACT_OR_MODEL_IDENTITY |
| L01b | `L01B-R112-CONTROLLED-RIGHT-REFUSAL` | AMEND_FIELD_SPECIFIC_REACHABILITY_RETAIN_DISTINCT | COORDINATOR_SOURCE_FIELD_REFUSAL; observation.native_record.identity.right | O05_WRONG_CONTRACT_OR_MODEL_IDENTITY |
| L01b | `L01B-R112-CONTROLLED-EXPIRY-DATE-REFUSAL` | AMEND_FIELD_SPECIFIC_REACHABILITY_RETAIN_DISTINCT | COORDINATOR_SOURCE_FIELD_REFUSAL; observation.native_record.identity.expiry_date | O05_WRONG_CONTRACT_OR_MODEL_IDENTITY |
| L01b | `L01B-R112-CONTROLLED-STRIKE-REFUSAL` | AMEND_FIELD_SPECIFIC_REACHABILITY_RETAIN_DISTINCT | COORDINATOR_SOURCE_FIELD_REFUSAL; observation.native_record.identity.strike | O05_WRONG_CONTRACT_OR_MODEL_IDENTITY |
| L01b | `L01B-R112-CONTROLLED-CURRENCY-REFUSAL` | AMEND_FIELD_SPECIFIC_REACHABILITY_RETAIN_DISTINCT | COORDINATOR_SOURCE_FIELD_REFUSAL; observation.native_record.identity.currency | O05_WRONG_CONTRACT_OR_MODEL_IDENTITY |
| L01b | `L01B-R112-CONTROLLED-MODEL-VARIANT-REFUSAL` | AMEND_FIELD_SPECIFIC_REACHABILITY_RETAIN_DISTINCT | COORDINATOR_SOURCE_FIELD_REFUSAL; observation.native_record.identity.model_variant | O05_WRONG_CONTRACT_OR_MODEL_IDENTITY |
| L01b | `L01B-R112-CONTROLLED-SCALE-REFUSAL` | AMEND_FIELD_SPECIFIC_REACHABILITY_RETAIN_DISTINCT | COORDINATOR_SOURCE_FIELD_REFUSAL; observation.native_record.identity.scale | O05_WRONG_CONTRACT_OR_MODEL_IDENTITY |
| L01b | `L01B-R112-CONTROLLED-GENERATION-REFUSAL` | AMEND_FIELD_SPECIFIC_REACHABILITY_RETAIN_DISTINCT | COORDINATOR_SOURCE_FIELD_REFUSAL; observation.native_record.identity.generation | O06_WRONG_GENERATION_OR_REQUEST |
| L01b | `L01B-R112-CONTROLLED-REQUEST-ID-REFUSAL` | AMEND_FIELD_SPECIFIC_REACHABILITY_RETAIN_DISTINCT | COORDINATOR_SOURCE_FIELD_REFUSAL; observation.native_record.identity.request_id | O06_WRONG_GENERATION_OR_REQUEST |
| D091 | `D091-CONTROLLED-RECEIPT-ASOF-REFUSAL` | RETAIN_DISTINCT_CONDITIONAL_ON_TRUE_PUBLIC_SEAM | CLOCK_OR_SCOPE; PUBLIC_M00_RAW_AND_PAGED_R112_TO_D091_SELECTOR | H01_RECEIPT_NOT_EQUAL_ASOF |
| D091 | `D091-CONTROLLED-CUTOFF-ORDER-REFUSAL` | RETAIN_DISTINCT_CONDITIONAL_ON_TRUE_PUBLIC_SEAM | CLOCK_OR_SCOPE; PUBLIC_M00_RAW_AND_PAGED_R112_TO_D091_SELECTOR | H02_KNOWLEDGE_CUTOFF_ORDER |
| L01b | `L01B-R112-CONTROLLED-SEQUENCE-SCOPE-REFUSAL` | AMEND_FIELD_SPECIFIC_REACHABILITY_RETAIN_DISTINCT | COORDINATOR_SOURCE_FIELD_REFUSAL; observation.ingestion_sequence_scope | H03_WRONG_SEQUENCE_SCOPE |
| D091 | `D091-CONTROLLED-TOP-RANK-TIE-REFUSAL` | AMEND_NEGATIVE_SEAL_RETAIN_DISTINCT | HISTORY_OR_AMBIGUOUS_RANK; two independent maximum-rank IDs with equal receipt and sequence | H04_TWO_DISTINCT_TOP_RANK_TIE |
| D091 | `D091-CONTROLLED-OVER-64-REFUSAL` | AMEND_NEGATIVE_SEAL_RETAIN_DISTINCT | HISTORY_OR_AMBIGUOUS_RANK; 65th projectable history member after eight full pages | H05_PROJECTED_MORE_THAN_64 |
| D091 | `D091-CONTROLLED-CURSOR-NONPROGRESS-REFUSAL` | RETAIN_DISTINCT_CONDITIONAL_ON_TRUE_PUBLIC_SEAM | HISTORY_OR_AMBIGUOUS_RANK; PUBLIC_M00_RAW_AND_PAGED_R112_TO_D091_SELECTOR | H06_RETURNED_CURSOR_CYCLE_NONPROGRESS |
| D091 | `D091-CONTROLLED-DUPLICATE-ID-CONFLICT-REFUSAL` | RETAIN_DISTINCT_CONDITIONAL_ON_TRUE_PUBLIC_SEAM | HISTORY_OR_AMBIGUOUS_RANK; PUBLIC_M00_RAW_AND_PAGED_R112_TO_D091_SELECTOR | H07_DUPLICATE_ID_CONFLICT |
| D091 | `D091-CONTROLLED-PRECOMMIT-SQLITE-FAILURE` | RETAIN_DISTINCT_CONDITIONAL_ON_TRUE_PUBLIC_SEAM | PERSISTENCE_PRECOMMIT_CERTAIN_FAILURE; REAL_M02_SQLITE_TRANSACTION_AND_FRESH_STANDALONE_READER | D01_PRECOMMIT_SQLITE_FAILURE, D05_NO_SUCCESSFUL_READBACK_AFTER_FAILED_COMMIT |
| D091 | `D091-CONTROLLED-UNCERTAIN-COMMIT-FAILURE` | RETAIN_DISTINCT_CONDITIONAL_ON_TRUE_PUBLIC_SEAM | PERSISTENCE_UNCERTAIN_POSTCOMMIT; REAL_M02_SQLITE_TRANSACTION_AND_FRESH_STANDALONE_READER | D02_UNCERTAIN_COMMIT_RESULT |
| D091 | `D091-CONTROLLED-SAME-ID-CONTENT-CONFLICT` | RETAIN_DISTINCT_CONDITIONAL_ON_TRUE_PUBLIC_SEAM | PERSISTENCE_IMMUTABLE_CONFLICT; REAL_M02_SQLITE_TRANSACTION_AND_FRESH_STANDALONE_READER | D03_SAME_DERIVED_ID_DIFFERENT_CONTENT_REFUSAL |
| D091 | `D091-CONTROLLED-ORIGINAL-GETTER-MISSING` | RETAIN_DISTINCT_CONDITIONAL_ON_TRUE_PUBLIC_SEAM | ORIGIN_OR_IDENTITY; STAGE_B_TRUSTED_GETTER_THEN_STAGE_C_REAL_PAGES_THEN_STAGE_D_SELECTOR_ONLY_FAULT | new; no predecessor witness |
| D091 | `D091-CONTROLLED-ORIGINAL-GETTER-UNITS-MISMATCH` | RETAIN_DISTINCT_CONDITIONAL_ON_TRUE_PUBLIC_SEAM | ORIGIN_OR_IDENTITY; STAGE_B_TRUSTED_GETTER_THEN_STAGE_C_REAL_PAGES_THEN_STAGE_D_SELECTOR_ONLY_FAULT | new; no predecessor witness |
| D091 | `D091-CONTROLLED-ORIGINAL-GETTER-GENERATION-MISMATCH` | RETAIN_DISTINCT_CONDITIONAL_ON_TRUE_PUBLIC_SEAM | ORIGIN_OR_IDENTITY; STAGE_B_TRUSTED_GETTER_THEN_STAGE_C_REAL_PAGES_THEN_STAGE_D_SELECTOR_ONLY_FAULT | new; no predecessor witness |
| D091 | `D091-CONTROLLED-UNSEALED-REFUSAL` | ADD_SEPARATE_REACHED_PRESEAL_STAGE_PROPOSAL | UNSEALED; materialise before actual private M00 source seal | new; no predecessor witness |

## Finite jurisdiction census

* D091/L04: 18 separately identified proposals (17 retained, of which 2 have amended test-only negative cohort specifications, plus one new UNSEALED). Historical original success/refusal pair remains exact. The prospective old ceiling was six; current authorised ceiling is zero. Proposed later owner decision: 18 exact identities and a matching ceiling, **not adopted now**.
* L01b/R112: 15 retained separately identified malformed-source ingress proposals, each amended to require field-specific pre-roster checked ingress. Proposed later owner decision: 15 exact identities and a separate matching ceiling, **not adopted now**.
* Combined: 33 proposals, no product runs, no admission, no Testers designated by this packet. Numeric equality to 33 is derived from separate observable branches and no exact reused accepted product evidence, **not an implementation-independent mathematical minimum**.

## 39 predecessor witness crosswalk

The 39 inherited witness IDs are precisely the sorted union below, each mapped in `REVISED_CASE_INVENTORY.json`; the UNSEALED proposal is new and correctly has no predecessor name. D04 shares the P15 positive retry physical case. D05 shares the D01 precommit physical case. G01-G03 have no inherited witness IDs.

`D01_PRECOMMIT_SQLITE_FAILURE`, `D02_UNCERTAIN_COMMIT_RESULT`, `D03_SAME_DERIVED_ID_DIFFERENT_CONTENT_REFUSAL`, `D04_FIRST_TIMESTAMP_PRESERVED`, `D05_NO_SUCCESSFUL_READBACK_AFTER_FAILED_COMMIT`, `H01_RECEIPT_NOT_EQUAL_ASOF`, `H02_KNOWLEDGE_CUTOFF_ORDER`, `H03_WRONG_SEQUENCE_SCOPE`, `H04_TWO_DISTINCT_TOP_RANK_TIE`, `H05_PROJECTED_MORE_THAN_64`, `H06_RETURNED_CURSOR_CYCLE_NONPROGRESS`, `H07_DUPLICATE_ID_CONFLICT`, `O01_NAN_NONFINITE`, `O02_ABSENT_MODEL_DELTA`, `O03_WRONG_ORIGINAL_NATIVE_UNITS`, `O04_WRONG_PROVIDER_VARIANT`, `O05_WRONG_CONTRACT_OR_MODEL_IDENTITY`, `O06_WRONG_GENERATION_OR_REQUEST`, `P01_ZERO`, `P02_NEGATIVE_TENTH`, `P03_POSITIVE_TENTH`, `P04_NEGATIVE_QUARTER`, `P05_POSITIVE_QUARTER`, `P06_NEGATIVE_HALF`, `P07_POSITIVE_HALF`, `P08_NEGATIVE_THREE_QUARTERS`, `P09_POSITIVE_THREE_QUARTERS`, `P10_NEGATIVE_ONE`, `P11_POSITIVE_ONE`, `P12_INTERIOR`, `P13_TWO_PAGE_HISTORY`, `P14_DURABLE_PUBLIC_REOPEN`, `P15_RETRY_FIRST_TIMESTAMP`, `R01_EXACT_ONE_POINT_ZERO_ONE_RANGE`, `S01_PRESEAL_PUBLIC_15_ADMISSIONS`, `S02_IMMUTABLE_SEAL`, `S03_DIRECT_POSTSEAL_LAWFUL_ADMISSION_REFUSED`, `S04_NO_COMMAND_ALIAS_ESCAPE`, `S05_UNCHANGED_IDS_BEFORE_AFTER_PAGINATION`

No witness name is treated as a test run, and no G01-G03 predecessor is fabricated.

## Evidence and constraints per unique mechanism

SUCCESS: exact signed Decimal 12 requests, five bins, two or more pages, independent SQLite reopen and idempotent first timestamp. REACHED_REFUSAL: original t12 1.01 RANGE after full provenance, no earlier source error.
NONFINITE vs ABSENT: original t13 NaN and t14 missing model.delta, distinguish target-specific business validity from complete-history provenance. H01: t0+0.5s rejects older receipt under zero-age policy; H02: cutoff before as-of rejects at prehistory request stage.
SEAL-REFUSAL: genuinely completed original 15 and permanent seal, independent lawful sixteenth ingress refused; **not** UNSEALED.
UNSEALED: one real t00 public admission, valid request at t00 while coordinator still ADMITTING; D091 materialise must emit only UNSEALED before any M00 page; no persisted category; then optional completion of remaining 14 verifies no state corruption, without a second product calculation.
H04/H05: separate scope-B actual M00 in-memory admission and original getter readback under a trusted test-only manifest, genuine sealed same-owner private state, full public pagination; reject due to tie vs 65th member only after B/C stage.
H06/H07: only the D091 read-side pagination response may be faulted after genuine sealed original cohort; the real M00 storage is untouched. G01-G03: trusted real Stage B getter followed by real Stage C pages, then selector-only Stage D contradictory getter.
D01/D02/D03: disposable real M02 SQLite transaction path with failure before commit, uncertain postcommit acknowledgement, or conflicting same immutable ID, respectively; independent newly opened SQLite reader inspects actual outcome. D01 includes D05 absence, success includes D04 preserved first time.
L01b A=15: each field is its own independent pre-roster checked-ingress predicate, with matching exact fixture hash and field-specific rejection output. No malformed raw M00 member is admitted and each original positive source may still seal as the original fifteen.

## Reviewer burden and nonadmission

Independently inspect actual public methods and future implementation ordering. A proposed test sequence does not prove that the current unimplemented coordinator/selector exists or passes. The proposed two-part physical budgets remain owner-reserved. The accepted design, policy adoption and prior documentary reviews confer no product-case release.
