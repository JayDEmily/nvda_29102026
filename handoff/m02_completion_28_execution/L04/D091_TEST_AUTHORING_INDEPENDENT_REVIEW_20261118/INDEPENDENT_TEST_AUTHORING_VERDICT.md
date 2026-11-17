# Independent D091 / L01b 33-case test-authoring verdict — 18 November 2026

**VERDICT: RETURN.** All 33 owner-admitted named test functions are authored in the two correct files, with no excess functions; independent non-product fixture, SHA-256 and AST audits succeeded. However, three discrete proof-adequacy gaps (F01–F03) prevent ACCEPT_TEST_AUTHORING_ONLY. This is a review of unexecuted assertions, not a product-code defect or failed product test.

## 1. Exact commission, reviewed candidate and authority

- Exact commission fully read: 9224470bae9ebe6c11ea5b1581c8ae2f4ab36933 at handoff/m02_completion_28_execution/L04/D091_TEST_AUTHORING_20261118/INDEPENDENT_TEST_AUTHORING_COMMISSION_20261118.md.
- Reviewed Worker candidate pinned: **b52a756ec920f3982ff8eae8a942e1c5163041de**; verified Git tree **28f8ff0c4750441eca2e5234bcec7be7ed246d17**. PR #27 open/draft at intake, Worker branch work/t01-d091-finite-adequacy-20261116, later tip 9224470bae9ebe6c11ea5b1581c8ae2f4ab36933. Git comparison from preauthoring 7bd9cb62e71aad5c4589cd5c6fd2aadcf39375f8 to pinned b52a756 shows only the two new test files plus static audit receipt and handover; b52a756 to 9224470 adds only the commission document.
- Governing repository files read in full: root GUARDRAILS.md, root AGENTS.md, tests/AGENTS.override.md, root EXEC_PLAN.md (successive sections, including L01b/L04, proof law and coordinated amendment). Repository tree scan found no additional nested applicable AGENTS file. The later owner five-file installation authority at handoff/astra_adr_continuation_20261115/OWNER_INSTALLATION_AUTHORITY.md was inspected to reconcile inherited proposal labels with the later installation. It does not release product execution.
- Governing owner admission: handoff/m02_completion_28_execution/OWNER_D091_L01B_FINITE_CASE_ADMISSION_20261117/OWNER_FINITE_CASE_ADMISSION_20261117.json and active TEST_EVIDENCE_LEDGER.json: **18 L04/D091 physical cases (ceiling 18), 15 separate L01b/R112 source-support cases (ceiling 15), execution held for all 33**. Owner adopted A–E negative-only test policy at L01b/R112_NEGATIVE_FAULT_POLICY_DECISION_20261116/OWNER_TEST_ONLY_POLICY_ADOPTION_20261116.json. No extra successful R112 source, positive D091 result or test release is inferred.
- Governing technical sources: L01b/R112_SOURCE_CONTRACT_PROPOSED.json and CONTROLLED_BATCH_INPUTS.json; L04/D091_FINITE_ADEQUACY_REVISION_20261117/REVISED_CASE_INVENTORY.json, FIELD_DISCRIMINATION_MATRIX.json and COHORT_AND_FIELD_REACHABILITY.md; L04/D091_PREEDIT_IMPLEMENTATION_BINDING_20261117/IMPLEMENTATION_BRIEF.md; L04/D091_PREEDIT_BINDING_REVISION_20261117/EXACT_RETURN_REPAIR_R1_R3.md and TECHNICAL_REPAIR_BINDING_V2.json. The separate independent pre-edit verdict at **5ed971f5d78f8ef34cbf3e62cec97b2e3798c838** accepted technical preparation only, not this test suite or execution.

## 2. Independently verified scope, source and fixture identity

An isolated clean Ubuntu Git checkout at /home/jds/nvda_d091_authoring_review_gpt6_20261118_0848 was detached at the exact reviewed commit and verified against its tree. A separate Python AST/JSON/hash-only verifier at C:/Users/james/AppData/Local/Temp/nvda_d091_gpt6_review_static_20261118.py reported **INDEPENDENT_STATIC_SOURCE_AND_FIXTURE_OK**; it did not import product code or invoke pytest. Independently checked:

- tests/product/m02_completion_28/d091/test_signal.py: exactly **18** individually named functions, file SHA-256 **3606c7f97c1c6f089191c71dd00340ff2de5a9b32fed4e38db563bce332adf9c**, Git blob a9e34d5ae3df65ef8a5b96f2e4c50d3bded4c36d, 31,400 bytes.
- tests/product/m02_completion_28/l01b_r112/test_source.py: exactly **15** individually named functions, file SHA-256 **1d964a8e65cfa50966994de2f9aa39ec74ca0faad239a8a91bd1a7bc2e7b1241**, Git blob ade6572dc24de683ab8566be43430ef20fb49931, 12,410 bytes.
- Original 15-member successful R112 source SHA-256 **1f4c46c5c247c78e3e18bb2de02c172f775379f664bad8e056ef6867a39d03dc**; original controlled contract SHA-256 **31c811e77468f44c2e412893326bc6d5f9ea037cdbf28712ce8e213652fdfc63**; original IDs T01-R112-BATCH-00 through -14.
- All **27/27 fixture-backed** case references match their actual byte SHA-256 (12 D091 and 15 L01b), and all **15** source negative specimens have distinct off-roster IDs and exactly one mutated t00 source field, independently reconstructed from original bytes rather than trusting a fixture's explanatory label. The original 12 signed value oracles are 0, ±0.10, ±0.25, ±0.50, ±0.75, ±1.00, 0.499 and match the five-bin source contract.
- No authoring delta outside the two named test files and the authoring receipt/handover; no evidence of product source, proof generation, claim registry or current ledger modification. The Worker-authored separate static receipt reports 29/29 checks; independent checks here confirm counts/bytes but do not promote those claims to product validity.

The actual M00 raw public interface was inspected (src/nvda_desk/raw_signal_occurrence_truth/api.py, especially lines 473–566, 1116–1161, 1395–1460 and 1798–1936): actual original getter, checked admission, mapping-based projected units and returned numeric-offset cursors. Actual M02 immutable SQLite store was inspected (_record_store.py lines 42–85 and 137–170), as was the strict codec allowlist (_native_codec.py lines 29–55). The D091 owner/DTO, private coordinator and fault ports remain **future proposed implementation**, correctly absent during tests-first review. Their absence is not itself a test defect.

## 3. Individual D091/L04 assessment — exact 18 owner cases

Every body and shared helper was inspected. The following table assesses the authored assertions, not executed outcomes.

| # | Owner physical case ID | Authored function | Documentary assessment |
|---:|---|---|---|
| 1 | D091-CONTROLLED-SUCCESS | test_d091_controlled_success | Positive 12-point signed category oracle in one physical case, 15 checked admissions, genuine 8+4 page history, durable reopen and retry timestamp. |
| 2 | D091-CONTROLLED-REACHED_REFUSAL | test_d091_controlled_reached_refusal | Original t12 1.01, categorical RANGE refusal. |
| 3 | D091-CONTROLLED-SEAL-REFUSAL | test_d091_controlled_seal_refusal | Complete original cohort seal; 16th lawful ingress postseal rejection, state unchanged. |
| 4 | D091-CONTROLLED-NONFINITE-REFUSAL | test_d091_controlled_nonfinite_refusal | Original t13 NaN, NONFINITE refusal. |
| 5 | D091-CONTROLLED-ABSENT-REFUSAL | test_d091_controlled_absent_refusal | Original t14 original raw exists but delta absent, ABSENT refusal. |
| 6 | D091-CONTROLLED-RECEIPT-ASOF-REFUSAL | test_d091_controlled_receipt_asof_refusal | H01 receipt t0+0.5s mismatch, CLOCK_OR_SCOPE. |
| 7 | D091-CONTROLLED-CUTOFF-ORDER-REFUSAL | test_d091_controlled_cutoff_order_refusal | F01 RETURN: invalid DTO clock order must not be silently bypassed to reach owner business event. |
| 8 | D091-CONTROLLED-TOP-RANK-TIE-REFUSAL | test_d091_controlled_top_rank_tie_refusal | B_TIE true 2-member negative-only M00 sealed cohort; equal rank, distinct IDs. |
| 9 | D091-CONTROLLED-OVER-64-REFUSAL | test_d091_controlled_over_64_refusal | B_OVER64 true 65-member negative-only M00 sealed cohort, nine 8+...+1 pages. |
| 10 | D091-CONTROLLED-CURSOR-NONPROGRESS-REFUSAL | test_d091_controlled_cursor_nonprogress_refusal | H06 read-only returned cursor nonprogress after second genuine page. |
| 11 | D091-CONTROLLED-DUPLICATE-ID-CONFLICT-REFUSAL | test_d091_controlled_duplicate_id_conflict_refusal | H07 contradictory repeated ID in second genuine page read adapter. |
| 12 | D091-CONTROLLED-PRECOMMIT-SQLITE-FAILURE | test_d091_controlled_precommit_sqlite_failure | D01 precommit certain transaction failure and independently reopened empty SQLite read. |
| 13 | D091-CONTROLLED-UNCERTAIN-COMMIT-FAILURE | test_d091_controlled_uncertain_commit_failure | D02 actual committed result under uncertain acknowledgement, reopened row. |
| 14 | D091-CONTROLLED-SAME-ID-CONTENT-CONFLICT | test_d091_controlled_same_id_content_conflict | F03 RETURN: second call error text does not prove second getter/pages, 0.498 test candidate or real immutable comparator reached. |
| 15 | D091-CONTROLLED-ORIGINAL-GETTER-MISSING | test_d091_controlled_original_getter_missing | G01 selector-only getter missing, private genuine B getter retained by proposed construction. |
| 16 | D091-CONTROLLED-ORIGINAL-GETTER-UNITS-MISMATCH | test_d091_controlled_original_getter_units_mismatch | G02 selector-only original units contradiction, genuine B untouched. |
| 17 | D091-CONTROLLED-ORIGINAL-GETTER-GENERATION-MISMATCH | test_d091_controlled_original_getter_generation_mismatch | G03 selector-only generation contradiction, genuine B untouched. |
| 18 | D091-CONTROLLED-UNSEALED-REFUSAL | test_d091_controlled_unsealed_refusal | Preseal original t00 checked ingress, UNSEALED before selector page; original remaining 14 admitted afterward. |

D091 helper evidence: original source binding/15-source checks lines 65–82; independent projected pages via actual read port 139–163; proposed checked real M00 admissions and genuine seal 166–191; request construction 194–211; source-only selector read adapter 287–354; positive classification and fresh durable reader 370–412; H06/H07 519–548; D01–D03 551–603; G01–G03 606–615,642–662; separate genuine preseal 618–639. B cohorts are negative-only, not extra lawful successful source. The future source implementation must keep trusted Stage B original getters separate from C/D selector-only adapters; the current assertions alone cannot prove the future implementation does so.

## 4. Individual L01b/R112 assessment — exact 15 owner cases

Every named test and the shared negative-field and post-refusal helpers was inspected. All fifteen tests verify the exact corresponding negative fixture SHA, one-field mutation against the original t00 (apart from novel opaque ID), actual checked coordinator ingress with field-specific CoordinatorSourceFieldRefusal, then re-admission of the original fifteen and sealing. The first native-units test spells out a direct call/assert sequence rather than relying only on shared helper. All fifteen inherit the F02 content-comparison gap described below. They are distinct L01b source refusals, not additional D091 category outcomes.

| # | Owner physical case ID | Authored function | Documentary assessment |
|---:|---|---|---|
| 1 | L01B-R112-CONTROLLED-NATIVE-UNITS-REFUSAL | test_l01b_r112_controlled_native_units_refusal | One-field native_units negative; exact field-first refusal. Shared post-refusal original-content check missing (F02). |
| 2 | L01B-R112-CONTROLLED-SOURCE-PROVIDER-REFUSAL | test_l01b_r112_controlled_source_provider_refusal | One-field source_provider negative; exact field-first refusal. Shared post-refusal original-content check missing (F02). |
| 3 | L01B-R112-CONTROLLED-SOURCE-VARIANT-REFUSAL | test_l01b_r112_controlled_source_variant_refusal | One-field source_variant negative; exact field-first refusal. Shared post-refusal original-content check missing (F02). |
| 4 | L01B-R112-CONTROLLED-CONTRACT-ID-REFUSAL | test_l01b_r112_controlled_contract_id_refusal | One-field identity.contract_id negative; exact field-first refusal. Shared post-refusal original-content check missing (F02). |
| 5 | L01B-R112-CONTROLLED-UNDERLYING-REFUSAL | test_l01b_r112_controlled_underlying_refusal | One-field identity.underlying negative; exact field-first refusal. Shared post-refusal original-content check missing (F02). |
| 6 | L01B-R112-CONTROLLED-SECURITY-TYPE-REFUSAL | test_l01b_r112_controlled_security_type_refusal | One-field identity.security_type negative; exact field-first refusal. Shared post-refusal original-content check missing (F02). |
| 7 | L01B-R112-CONTROLLED-RIGHT-REFUSAL | test_l01b_r112_controlled_right_refusal | One-field identity.right negative; exact field-first refusal. Shared post-refusal original-content check missing (F02). |
| 8 | L01B-R112-CONTROLLED-EXPIRY-DATE-REFUSAL | test_l01b_r112_controlled_expiry_date_refusal | One-field identity.expiry_date negative; exact field-first refusal. Shared post-refusal original-content check missing (F02). |
| 9 | L01B-R112-CONTROLLED-STRIKE-REFUSAL | test_l01b_r112_controlled_strike_refusal | One-field identity.strike negative; exact field-first refusal. Shared post-refusal original-content check missing (F02). |
| 10 | L01B-R112-CONTROLLED-CURRENCY-REFUSAL | test_l01b_r112_controlled_currency_refusal | One-field identity.currency negative; exact field-first refusal. Shared post-refusal original-content check missing (F02). |
| 11 | L01B-R112-CONTROLLED-MODEL-VARIANT-REFUSAL | test_l01b_r112_controlled_model_variant_refusal | One-field identity.model_variant negative; exact field-first refusal. Shared post-refusal original-content check missing (F02). |
| 12 | L01B-R112-CONTROLLED-SCALE-REFUSAL | test_l01b_r112_controlled_scale_refusal | One-field identity.scale negative; exact field-first refusal. Shared post-refusal original-content check missing (F02). |
| 13 | L01B-R112-CONTROLLED-GENERATION-REFUSAL | test_l01b_r112_controlled_generation_refusal | One-field identity.generation negative; exact field-first refusal. Shared post-refusal original-content check missing (F02). |
| 14 | L01B-R112-CONTROLLED-REQUEST-ID-REFUSAL | test_l01b_r112_controlled_request_id_refusal | One-field identity.request_id negative; exact field-first refusal. Shared post-refusal original-content check missing (F02). |
| 15 | L01B-R112-CONTROLLED-SEQUENCE-SCOPE-REFUSAL | test_l01b_r112_controlled_sequence_scope_refusal | One-field ingestion_sequence_scope negative; exact field-first refusal. Shared post-refusal original-content check missing (F02). |

Shared L01b mechanics: _fixture() lines 117–126, _assert_one_bad_field_only() lines 129–139, _post_refusal_original_seal() lines 142–162, common _exercise_refusal() lines 165–185, direct native_units function 190–205, remaining 14 individually named functions 208–261. Field-first source refusal must occur before off-roster rejection and before any public M00 write.

## 5. Three material RETURN findings

### F01 — H02 invalid request cannot satisfy the accepted constructor and reached business-stage requirements simultaneously

**Requirement:** The R112 contract requires received_ts_utc == as_of_utc <= knowledge_cutoff_utc <= calculated_at_utc. Accepted V2 EXACT_RETURN_REPAIR_R1_R3.md §R3 item 1 makes D091BucketRequestV1 a frozen 21-init-field typed DTO with as_of_utc <= knowledge_cutoff_utc; item 4 makes calculated time come solely from owner.utc_now(). TECHNICAL_REPAIR_BINDING_V2.json bound_request.utc_clock_order independently repeats as_of<=knowledge_cutoff<=now. The owner H02 case separately demands the real D091 diagnostic CLOCK_OR_SCOPE, not merely an early generic constructor failure.

**Observed:** test_signal.py lines **194–211** build D091BucketRequestV1 directly. In **test_d091_controlled_cutoff_order_refusal, lines 472–486**, source t00 has receipt/as_of 2026-11-15T12:00:00Z but the fixture and test set knowledge_cutoff=2026-11-15T11:59:59Z. The test then expects owner.materialise(request) to return None and emit CLOCK_OR_SCOPE. A correctly validated bound request constructor must reject that ordering before materialise executes. This is a demonstrable authoring/technical-contract contradiction, **not** an observed runtime exception.

**Required:** Formally reconcile exact constructor validation and H02 refusal-stage precedence against the governing pre-edit binding; where correction changes that accepted contract, obtain its independent and owner-governed release. Revise the existing H02 assertion or DTO stage boundary only after that reconciliation. **Do not** silently substitute a generic ValueError for the separately admitted business diagnostic, or implement a DTO that violates its accepted binding simply to satisfy this test.

### F02 — The fifteen source-refusal tests do not prove exact original M00 content survived refusal

**Requirement:** COHORT_AND_FIELD_REACHABILITY.md RETURN-03 item 4 requires independently checking all original fifteen **IDs AND complete source content** via genuine M00 getter after the malformed candidate is rejected and before claiming an unpoisoned sealed cohort.

**Observed:** In test_source.py _post_refusal_original_seal(), lines **142–162**, each original is checked-admitted, sealed and fetched from M00, but the assertions compare returned **types and observation_occurrence_id only** (lines 148–149, 157–158); they do not compare the entire admitted and returned immutable RawObservationOccurrenceV1 objects with the original independently constructed DTO, including native decimal, source provider/variant, model identity, receipt, sequence, units and scope. The independently verified one-field fixture differences do not establish persisted original content integrity. This is a shared deficiency affecting all fifteen, not fifteen unrelated defects. D091 _admit_and_seal() lines 175–191 and _assert_clean_source() lines 270–276 also use ID-only source checks.

**Required:** Within the same post-refusal helper and physical cases, assert exact full original DTO/content equality on each real checked-admit return and genuine getter readback, maintaining original identities, field-first refusals, exact 15-case budget and original source byte hashes. Do not add new positive source stimuli.

### F03 — The D03 test does not discriminate real second-append immutable identity conflict from a premature matching error

**Requirement:** EXACT_RETURN_REPAIR_R1_R3.md §R1 specifies two genuinely lawful public materialise calls, actual original getter and complete pagination **on both**, a one-shot **second append** test-only internally coherent candidate with delta 0.498 in original/projection/signed fields (first true source 0.499), unchanged derived logical ID, and real RecordState.append/_existing refusing changed canonical bytes; first durable row must remain retrievable independently. Its critical validation paragraph explicitly requires test-side observation of getter, paging, call identity and the second-append fault boundary.

**Observed:** In **test_d091_controlled_same_id_content_conflict(), lines 581–603**, the first public call/readback and second public call are present, and second exception text, outcome_uncertain and unchanged first row are checked. But the authored assertions do **not** establish the second M00 getter and page traversal, the second 0.498 candidate at the actual append input, one-shot after-first-write behaviour, or arrival at real _existing. A premature PersistenceFailureV1 with the same text could satisfy this test without reaching the required immutable comparator. This is a proof-discrimination gap; there is no implemented D03 pathway to accuse of faulty behaviour.

**Required:** Strengthen **this existing D03 physical function** using an independently observable read-only test port/trace and final source inspection, proving both true source getter/pagination sequences and the second corrupted candidate reaching the genuine immutable comparator, while preserving original sealed R112 source, logical ID, first row and first timestamp. Any necessary edits to _record_store.py are a **separately reserved changed-path decision**, not authorised by this review.

## 6. Scope of acceptance, holds and next review

**Return for bounded repair of F01–F03, not a complete redesign.** The other 31 D091/L01b proof intents remain defined and mapped; the 33 original case IDs, 18/15 hard ceilings, 27 fixture byte identities, five category labels and source policy should remain unchanged unless separately authorised. In particular, the C/G fault ports remain scoped to selector read responses after private genuine Stage B, B negative cohorts cannot become alternative successful-source profiles, and D01/D02 require actual SQLite transaction boundaries rather than error-label simulation.

The four previously scoped future source files are not deemed ready by an unfavourable test-first verdict. The extra _record_store.py and tools/product_proof_claims.py paths, proof claim/generation, independent Tester/runner, product execution and main merge remain independently held. Zero product executions and zero pytest collections in this independent review. No M00/M02 source was imported into the static verifier; no product tests were run; no Worker branch, source, active ledger, claim or registry was modified. D145 stays **PAUSED**.

A bounded revised Worker commit must expose new exact test file SHA-256, Git commit/tree and a second independent authoring review. The owner’s already granted 18+15 physical-case *admission* is not revoked by this RETURN; its currently authored assertions simply do not pass independent adequacy review. This report is independently committed on a separate review branch; the commit SHA/tree/one-file remote readback are independently verified outside this self-referential report.
