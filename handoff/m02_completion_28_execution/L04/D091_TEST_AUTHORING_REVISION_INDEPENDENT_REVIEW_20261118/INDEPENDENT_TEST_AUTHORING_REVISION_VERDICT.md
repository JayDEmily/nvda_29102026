# Independent D091/L01b F01–F03 test-authoring revision verdict — 18 November 2026

**VERDICT: ACCEPT_REVISED_TEST_AUTHORING_ONLY.** The three *previous documentary authoring* findings F01–F03 are resolved to the extent required to accept the design of the **33 exact unexecuted physical test functions**, separately jurisdictioned as D091/L04 (18) and L01b/R112 source support (15). This does **not** accept the already-present four-source-file implementation candidate, establish a product runtime result, or release the reserved `_record_store.py`, product proof loader, strict Tester, claim generation, case execution, merge or D145.

## 1. Pinned authority, scope, lineage and reproducible static inspection

- Exact commission: Git commit `578aea2a0861eb875e7deb592765285c25903ec2`, `handoff/m02_completion_28_execution/L04/D091_TEST_AUTHORING_REVISION_20261118/INDEPENDENT_TEST_AUTHORING_REVISION_COMMISSION_20261118.md`, Git blob `8558a007f1adc35a614f46f0a03ab79494fc2881`; read in full. This verdict assesses **only** the pinned technical/test candidate `f4b8b57a5e870672808581ecbcf4804825058844`, actual Git tree **`58cae9e94fa94f20624c84f176808c245d96d833`**. Independent isolated Ubuntu checkout was detached at that exact commit with a clean worktree: `/home/jds/nvda_d091_f01_f03_revision_review_20261118_gpt6`.
- The initial tests-first authoring commit `b52a756ec920f3982ff8eae8a942e1c5163041de` is an ancestor of the candidate; its subsequent unaccepted four-source-path additions are `src/nvda_desk/market_measurement_truth/{api.py,_controlled_r112.py,_native_d091.py,_native_codec.py}`. The candidate is an ancestor of the commission. The later Worker receipt `92b08e888ab04481b06e5d12dbb7ae39ba09db41` and commission add documentation, not altered test files. At final review the draft PR #27 HEAD had advanced to `f2e8e3ef9fa112805a3f53155266d9db612046df` (four documentary commits after the pinned candidate, with **no** source/test changed in that comparison). No claim is made about subsequent uninspected Worker commits.
- Fully read governing `GUARDRAILS.md` (Git blob `54a4407609941f63f6b902076688ff102a3d5ba2`), root `AGENTS.md` (`b5b8f73bfef62cf34643aef419e6931599ad08b1`), applicable `tests/AGENTS.override.md` (`66666cc012889e585ef4da80049d5ee2a0244c53`) and all 428 lines of `EXEC_PLAN.md` (including §§3–4, L01b/L04 and the coordinated amendment). No additional scoped AGENTS files exist in the candidate tree. Reconciled inherited proposal headings against `handoff/astra_adr_continuation_20261115/OWNER_INSTALLATION_AUTHORITY.md`: an owner-installed governance package does not release product tests.
- Inspected direct owner A–E test-only policy `L01b/R112_NEGATIVE_FAULT_POLICY_DECISION_20261116/OWNER_TEST_ONLY_POLICY_ADOPTION_20261116.json`, direct owner 18+15 finite admission `OWNER_D091_L01B_FINITE_CASE_ADMISSION_20261117/OWNER_FINITE_CASE_ADMISSION_20261117.json` (Git blob `abb09419a425ee5eb2b19ed911fb32ecba41fd81`), active `TEST_EVIDENCE_LEDGER.json` D091 and L01b entries, original controlled R112 contract and batch, `L04/D091_FINITE_ADEQUACY_REVISION_20261117/{COHORT_AND_FIELD_REACHABILITY.md,REVISED_CASE_INVENTORY.json,FIELD_DISCRIMINATION_MATRIX.json}`, the pre-edit `IMPLEMENTATION_BRIEF.md`, `EXACT_RETURN_REPAIR_R1_R3.md` and `TECHNICAL_REPAIR_BINDING_V2.json`.
- Read full previous independent test-authoring **RETURN** at separate review commit `b85f9aaa50b7daad96a750c48bb01e653de7d66c`, report blob `b41441e27960e59120bbb305deb2b6a6e9c8407e`, and complete Worker `RETURN_RECONCILIATION_F01_F03_20261118.md`. Read original independent technical preparation verdict at `5ed971f5d78f8ef34cbf3e62cec97b2e3798c838`; it accepted revised pre-edit *preparation* only. That earlier technical conclusion cannot override the later direct owner H02 case semantics.
- Independently inspected both revised tests **in full**, actual M00 `src/nvda_desk/raw_signal_occurrence_truth/api.py` original DTO/getter/page implementation (notably lines 265–305, 473–566, 1116–1161, 1867–1936), actual M02 `_record_store.py` in full (especially lines 41–86, 137–170), and actual M02 `_native_codec.py` in full. Reviewed Worker static 29/29 receipt as attributed static evidence, never as product evidence.
- Independent **Python standard-library-only** AST/hash/JSON audit script external to the repository: `C:/Users/james/AppData/Local/Temp/nvda_f01_f03_revision_independent_static_20261118.py`, run from WSL with `python3 /mnt/c/Users/james/AppData/Local/Temp/nvda_f01_f03_revision_independent_static_20261118.py`. Observed: 18 D091 + 15 L01b distinct named top-level test functions, **33/33 exact owner-admitted file::name mappings**, zero extra functions, no test-function decorators, **27/27 physical negative fixture file SHA-256 checks**, and original two source SHA-256 calculations. The script imports only `pathlib`, `hashlib`, `json` and `ast`; it imports **no product code**, invokes **no pytest collection or execution**, and does not write repository paths.

### Independently pinned byte identities

| Tracked file | Actual SHA-256 |
|---|---|
| `tests/product/m02_completion_28/d091/test_signal.py` (34,669 bytes; 18 tests) | `d1eab7802786344ecf9ab4d4e2f46b802aba6d2fea0c72d14ad149492504b86f` |
| `tests/product/m02_completion_28/l01b_r112/test_source.py` (13,365 bytes; 15 tests) | `1f648998ca4c64829a3655057598e5ae5687b6568bb7e9eebf7ca2f17caa56f5` |
| `handoff/m02_completion_28_execution/L01b/CONTROLLED_BATCH_INPUTS.json` (original 15-member source) | `1f4c46c5c247c78e3e18bb2de02c172f775379f664bad8e056ef6867a39d03dc` |
| `handoff/m02_completion_28_execution/L01b/R112_SOURCE_CONTRACT_PROPOSED.json` (owner adopted) | `31c811e77468f44c2e412893326bc6d5f9ea037cdbf28712ce8e213652fdfc63` |

## 2. F01 — H02 clock-order precedence: ACCEPT for authoring with explicit technical reconciliation

**Governing conflict and scope:** `EXACT_RETURN_REPAIR_R1_R3.md` §R3.1 and `TECHNICAL_REPAIR_BINDING_V2.json` had assigned `as_of_utc <= knowledge_cutoff_utc` to the 21-field typed request **constructor**. But the higher-ranking, later **direct owner-admitted** exact H02 physical case `D091-CONTROLLED-CUTOFF-ORDER-REFUSAL` demands the public owner `materialise` issue the **business** `CLOCK_OR_SCOPE` diagnostic on a request with genuine valid UTC type/shape and *reversed* clock order. The source selection contract and the proposed Stage A business-preflight law independently demand `received_ts_utc == as_of_utc <= knowledge_cutoff_utc <= calculated_at_utc` for a successful output, while explicitly prescribing H02 `CLOCK_OR_SCOPE` before paging. Enforcing temporal order in the constructor would render this authorised business refusal unreachable.

**Adjudication:** The Worker proposal to leave precise UTC-aware *type and instant validity* in `D091BucketRequestV1.__post_init__`, but move *relative temporal ordering* exclusively to the first `D091BucketOwnerV1.materialise` Stage A guard is a **bounded technical precedence reconciliation under the already adopted owner H02 case**, not a newly invented source rule or relaxation of valid successful-selection time constraints. The invalid-order request is *representable solely to be refused* by the owner; it cannot categorise, reach M00 paging or create a result row. The authored H02 function in `test_signal.py` calls the public owner, asserts `None`, one actual `D091DiagnosticEventV1(stage='CLOCK_OR_SCOPE')`, and no durable rows; it does **not** accept a generic constructor `ValueError`, override the request with coercion, or silently ignore the contradiction.

**Boundary:** The earlier pre-edit sentence allocating order validation to the constructor must **not** continue as an implementation requirement in contradiction to H02. This review resolves the *test-authoring authority/technical precedence* choice; it does **not** install a revised accepted V2 contract by editing normative documents, approve the unaccepted source implementation, or prove a runtime H02 event. A later independent source/contract implementation review must verify both exact-UTC constructor checks and Stage A early business ordering on actual code before admitting product proof. No further owner **source/domain** decision is needed solely for this relocation because the precise owner H02 semantic outcome is already admitted.

## 3. F02 — all original M00 source fields after each malformed refusal: ACCEPT

**Original gap:** the previous `RETURN` observed that L01b post-refusal tests asserted only IDs/types, so mutation of original native content could go unnoticed. `COHORT_AND_FIELD_REACHABILITY.md` RETURN-03 requires **the exact fifteen original IDs and complete content**, not merely sealed cohort size.

**Revised inspected mechanism:**
- In `l01b_r112/test_source.py`, `_load_original` SHA-verifies independent fixed source-file bytes; `_observation` builds a full original `raw.RawObservationOccurrenceV1` with typed native Decimals, eleven contract identity fields, receipt, sequence/scope, provider, variant and units. `_canonical_native_value` recursively traverses `Mapping`, lists and tuples, converts `Decimal` to `as_tuple()`, so exact representations including `Decimal('NaN')` are compared without NaN self-equality failure. `_assert_exact_original` traverses **every** `dataclasses.fields(raw.RawObservationOccurrenceV1)`, including optional and provider-native fields.
- After **each distinct** malformed candidate obtains the correct `CoordinatorSourceFieldRefusal(field_path)` before off-roster rejection, `_post_refusal_original_seal` calls genuine checked ingress for **all 15 unchanged originals**, compares all fields on each returned admission, seals and uses genuine M00 `get_raw_observation_occurrence` on **all 15** with the same complete-source comparison. It also establishes rejected novel IDs were not admitted. All 15 separate named physical tests share this full postcondition; the first native-units case spells out a direct sequence.
- In `d091/test_signal.py`, `_native_content` descends actual dataclasses/Mapping/tuples/Decimals, and `_assert_real_original_content` compares **every raw field** on checked admission and genuine postseal getter. `_assert_clean_source` uses this full comparison after D091 fault cases.
- The independent static audit confirms **27 unchanged referenced negative fixture SHA-256 identities**, unique named cases and the original controlled source SHA. No new successful source specimen, unadmitted field variant, extra product test or arbitrary source writer is introduced. These assertions are **written but not executed**; they prove adequate discrimination by inspection, not that M00 satisfies them at runtime.

## 4. F03 — genuinely reached immutable store conflict: ACCEPT for authoring

**Required real boundary:** pre-edit R1 demands **two public `owner.materialise` calls**, genuine original M00 getter and full pagination **each time**, a construction-scoped test-only second *append-input* candidate with internally coherent `Decimal('0.498')` instead of original `Decimal('0.499')`, same logical derived occurrence ID and category, actual immutable `RecordState._existing` comparator reached, with the first SQLite row/time intact on a standalone read-only reopen.

**Revised inspected mechanism:**
1. `_SelectorReadAdapter(genuine,'TRACE')` is passed only through the selector **read** capability. Its `list_projected_raw_history` first delegates to the genuine M00 port and increments `page_calls`; its original getter similarly delegates to real `get_raw_observation_occurrence` and increments `getter_calls`. Alterations exist only for separately admitted `H06/H07/G01/G02/G03` modes, never `TRACE`; `selector.injected == 0` is asserted. Trusted private Stage B remains separate from the selector adapter. The actual inspected M00 paging emits offset-cursor slices; t11 must demand two pages (8+4) and twelve original getter calls per public invocation.
2. `test_d091_controlled_same_id_content_conflict` checks first public `materialise` returns a genuine typed 0.499 `D091BucketOccurrenceV1`, with `(page_calls,getter_calls)==(2,12)`, and a fully matching independent fresh SQLite reader row. Its second public call is expected to raise `PersistenceFailureV1`, and the cumulative counters **must equal (4,24)** with zero injected selector fault. An exception before the second genuine traversal cannot satisfy these assertions.
3. Beyond a matching error string and `outcome_uncertain=False`, it traverses the **raised exception's real `__traceback__`** to exactly one `_existing` Python frame with actual path suffix `nvda_desk/market_measurement_truth/_record_store.py`; extracts that frame's *actual* locals `value` and `old`. The fully inspected unchanged `RecordState._existing` receives locals of these exact names in its real `RecordState.append` transaction and raises `PersistenceFailureV1('immutable measurement identity conflict')` only on a same-ID mismatch of canonical bytes after normalising the first calculated time. Consequently a premature fake `PersistenceFailureV1` without reaching this real comparator **cannot** satisfy the traceback assertion.
4. It checks the comparator's real new candidate has **three coupled** 0.498 values (signed, selected projection, embedded `original_observation.native_record.model.delta`), with the old comparator candidate's 0.499, both actual typed D091 occurrences, same logical derived ID, same category `ABS_25_50`, and original first time. It independently reopens SQLite, compares the complete first persisted row again and asserts exactly one row, while the genuine unchanged sealed M00 source still reads 0.499.
5. These are bounded test-only construction and read traces, not a direct `RecordState.append` test, mock store, arbitrary fault-stage setter, private-cohort mutation, schema edit or new positive R112 source. Actual D03 second-append construction remains **unproven until source inspection and strict Tester execution**. The comparator traceback already yields direct discriminating evidence; adding an unapproved `_record_store.py` instrumentation hook is **not required for F03 authoring**.

## 5. Exact finite 33-case census — assertions reviewed, not results

**L04/D091: 18/18 owner-admitted physical cases; no parameterisation or extra functions.**

| # | Exact owner case ID | Exact authored test function | Expected proof intent/stage |
|---:|---|---|---|
| 1 | `D091-CONTROLLED-SUCCESS` | `test_d091_controlled_success` | `CATEGORY_DURABLE_REOPEN_AND_IDEMPOTENT_RETRY` |
| 2 | `D091-CONTROLLED-REACHED_REFUSAL` | `test_d091_controlled_reached_refusal` | `RANGE` |
| 3 | `D091-CONTROLLED-SEAL-REFUSAL` | `test_d091_controlled_seal_refusal` | `COORDINATOR_POSTSEAL_INGRESS_REFUSAL` |
| 4 | `D091-CONTROLLED-NONFINITE-REFUSAL` | `test_d091_controlled_nonfinite_refusal` | `NONFINITE` |
| 5 | `D091-CONTROLLED-ABSENT-REFUSAL` | `test_d091_controlled_absent_refusal` | `ABSENT` |
| 6 | `D091-CONTROLLED-RECEIPT-ASOF-REFUSAL` | `test_d091_controlled_receipt_asof_refusal` | `CLOCK_OR_SCOPE` |
| 7 | `D091-CONTROLLED-CUTOFF-ORDER-REFUSAL` | `test_d091_controlled_cutoff_order_refusal` | `CLOCK_OR_SCOPE` |
| 8 | `D091-CONTROLLED-TOP-RANK-TIE-REFUSAL` | `test_d091_controlled_top_rank_tie_refusal` | `HISTORY_OR_AMBIGUOUS_RANK` |
| 9 | `D091-CONTROLLED-OVER-64-REFUSAL` | `test_d091_controlled_over_64_refusal` | `HISTORY_OR_AMBIGUOUS_RANK` |
| 10 | `D091-CONTROLLED-CURSOR-NONPROGRESS-REFUSAL` | `test_d091_controlled_cursor_nonprogress_refusal` | `HISTORY_OR_AMBIGUOUS_RANK` |
| 11 | `D091-CONTROLLED-DUPLICATE-ID-CONFLICT-REFUSAL` | `test_d091_controlled_duplicate_id_conflict_refusal` | `HISTORY_OR_AMBIGUOUS_RANK` |
| 12 | `D091-CONTROLLED-PRECOMMIT-SQLITE-FAILURE` | `test_d091_controlled_precommit_sqlite_failure` | `PERSISTENCE_PRECOMMIT_CERTAIN_FAILURE` |
| 13 | `D091-CONTROLLED-UNCERTAIN-COMMIT-FAILURE` | `test_d091_controlled_uncertain_commit_failure` | `PERSISTENCE_UNCERTAIN_POSTCOMMIT` |
| 14 | `D091-CONTROLLED-SAME-ID-CONTENT-CONFLICT` | `test_d091_controlled_same_id_content_conflict` | `PERSISTENCE_IMMUTABLE_CONFLICT` |
| 15 | `D091-CONTROLLED-ORIGINAL-GETTER-MISSING` | `test_d091_controlled_original_getter_missing` | `ORIGIN_OR_IDENTITY` |
| 16 | `D091-CONTROLLED-ORIGINAL-GETTER-UNITS-MISMATCH` | `test_d091_controlled_original_getter_units_mismatch` | `ORIGIN_OR_IDENTITY` |
| 17 | `D091-CONTROLLED-ORIGINAL-GETTER-GENERATION-MISMATCH` | `test_d091_controlled_original_getter_generation_mismatch` | `ORIGIN_OR_IDENTITY` |
| 18 | `D091-CONTROLLED-UNSEALED-REFUSAL` | `test_d091_controlled_unsealed_refusal` | `UNSEALED` |

**L01b/R112: 15/15 separately admitted physical source-support cases; no D091 category result claims.**

| # | Exact owner case ID | Exact authored test function | Expected proof intent/stage |
|---:|---|---|---|
| 1 | `L01B-R112-CONTROLLED-NATIVE-UNITS-REFUSAL` | `test_l01b_r112_controlled_native_units_refusal` | `COORDINATOR_SOURCE_FIELD_REFUSAL` |
| 2 | `L01B-R112-CONTROLLED-SOURCE-PROVIDER-REFUSAL` | `test_l01b_r112_controlled_source_provider_refusal` | `COORDINATOR_SOURCE_FIELD_REFUSAL` |
| 3 | `L01B-R112-CONTROLLED-SOURCE-VARIANT-REFUSAL` | `test_l01b_r112_controlled_source_variant_refusal` | `COORDINATOR_SOURCE_FIELD_REFUSAL` |
| 4 | `L01B-R112-CONTROLLED-CONTRACT-ID-REFUSAL` | `test_l01b_r112_controlled_contract_id_refusal` | `COORDINATOR_SOURCE_FIELD_REFUSAL` |
| 5 | `L01B-R112-CONTROLLED-UNDERLYING-REFUSAL` | `test_l01b_r112_controlled_underlying_refusal` | `COORDINATOR_SOURCE_FIELD_REFUSAL` |
| 6 | `L01B-R112-CONTROLLED-SECURITY-TYPE-REFUSAL` | `test_l01b_r112_controlled_security_type_refusal` | `COORDINATOR_SOURCE_FIELD_REFUSAL` |
| 7 | `L01B-R112-CONTROLLED-RIGHT-REFUSAL` | `test_l01b_r112_controlled_right_refusal` | `COORDINATOR_SOURCE_FIELD_REFUSAL` |
| 8 | `L01B-R112-CONTROLLED-EXPIRY-DATE-REFUSAL` | `test_l01b_r112_controlled_expiry_date_refusal` | `COORDINATOR_SOURCE_FIELD_REFUSAL` |
| 9 | `L01B-R112-CONTROLLED-STRIKE-REFUSAL` | `test_l01b_r112_controlled_strike_refusal` | `COORDINATOR_SOURCE_FIELD_REFUSAL` |
| 10 | `L01B-R112-CONTROLLED-CURRENCY-REFUSAL` | `test_l01b_r112_controlled_currency_refusal` | `COORDINATOR_SOURCE_FIELD_REFUSAL` |
| 11 | `L01B-R112-CONTROLLED-MODEL-VARIANT-REFUSAL` | `test_l01b_r112_controlled_model_variant_refusal` | `COORDINATOR_SOURCE_FIELD_REFUSAL` |
| 12 | `L01B-R112-CONTROLLED-SCALE-REFUSAL` | `test_l01b_r112_controlled_scale_refusal` | `COORDINATOR_SOURCE_FIELD_REFUSAL` |
| 13 | `L01B-R112-CONTROLLED-GENERATION-REFUSAL` | `test_l01b_r112_controlled_generation_refusal` | `COORDINATOR_SOURCE_FIELD_REFUSAL` |
| 14 | `L01B-R112-CONTROLLED-REQUEST-ID-REFUSAL` | `test_l01b_r112_controlled_request_id_refusal` | `COORDINATOR_SOURCE_FIELD_REFUSAL` |
| 15 | `L01B-R112-CONTROLLED-SEQUENCE-SCOPE-REFUSAL` | `test_l01b_r112_controlled_sequence_scope_refusal` | `COORDINATOR_SOURCE_FIELD_REFUSAL` |

The names and file locations in these tables were compared exactly against the actual owner-admitted `proposed_test_node` list using AST for each physical file. The separate D091 owner ceiling remains **18** and L01b source-support ceiling **15**, both **admitted with execution held**; an allocation is not a successful run. The unchanged 27 fixture hashes and source originals were checked from actual tracked bytes. The previous RETURN's three authoring findings are treated as resolved; no prior independent finding is downgraded to runtime PASS.

## 6. Decision, conditions and reserved authority

**ACCEPT_REVISED_TEST_AUTHORING_ONLY** for candidate/tree and two exact SHA-bound test files above. This independent documentary decision authorises neither changes to a prior governing document nor substantive source product acceptance; it is not a strict Tester verdict, case release, evidence generation or implementation release. The source candidate was introduced after tests-first but before the original independent authoring RETURN; it **remains unaccepted** and may not be assumed correct because the tests are now appropriately authored.

Particularly: actual D01/D02 transaction injection still needs a *separate explicit owner changed-path release* for `src/nvda_desk/market_measurement_truth/_record_store.py`; proof registration still needs independently governed `tools/product_proof_claims.py` changed-path authority and claim/generation admission. The strict appointed product Tester, accepted exact runner/CPython/SQLite and fresh receiver/asset evidence, product execution, dependent consumer acceptance, main merge and D145 activation remain **held**. This review ran **zero product tests, zero pytest collections**, made **zero Worker branch/product source/ledger/test changes**, admitted **zero additional physical cases** and issued no product result.

**Publication:** independent review branch `review/d091-l01b-pr27-test-authoring-revision-independent-20261118-gpt6` starts **exactly** at `f4b8b57a5e870672808581ecbcf4804825058844`; this file is the **sole intended commit change**. Commit SHA/tree and remote one-file readback must be independently verified *after* publication; they cannot be self-certified within this pre-commit report.
