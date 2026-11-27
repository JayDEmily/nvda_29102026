# NVIDIA V2 D091/L01b — implementation readiness after finite owner admission (17 November 2026)

**Disposition: PREIMPLEMENTATION PREPARATION COMPLETED; PRODUCT IMPLEMENTATION/TEST EXECUTION NOT RELEASED.** This is a bounded implementation-readiness handoff, not a new gate, case allocation, source policy, accepted owner/claim generation, or semantic product result.

## 1. Exact decision lineage

- Existing draft PR #27, Worker branch `work/t01-d091-finite-adequacy-20261116`.
- Revised candidate `aa01fc29544147f0ab22686af12579eecd5bf5f7`, tree `05ca3bce9655810c5fcd4cfe1926ffe1924cb988`.
- Independent verdict `5f47fdce8064d7cfcb452621323cbcca57af167d`: `ACCEPT_FINITE_ADEQUACY_PREPARATION_ONLY` with **33 conditional physical proposals**.
- Direct owner approval, original Git record and ledger commit `a4a41ac600ae63150ed2160911707ae49853d1bd`: **18 D091/L04 case identities, hard ceiling 18**, and **15 L01b/R112 source-support identities, separate hard ceiling 15**. These are finite **admissions, not execution release**.
- Source: `handoff/m02_completion_28_execution/OWNER_D091_L01B_FINITE_CASE_ADMISSION_20261117/OWNER_FINITE_CASE_ADMISSION_20261117.json`; revised inventory `handoff/m02_completion_28_execution/L04/D091_FINITE_ADEQUACY_REVISION_20261117/REVISED_CASE_INVENTORY.json`.
- Source policy: adopted original successful R112 contract SHA-256 `31c811e77468f44c2e412893326bc6d5f9ea037cdbf28712ce8e213652fdfc63`; fixed positive 15-member batch SHA-256 `1f4c46c5c247c78e3e18bb2de02c172f775379f664bad8e056ef6867a39d03dc`. These bytes were not changed here.

The machine-readable exact **33-case-to-public-seam** matrix is `IMPLEMENTATION_READINESS_MATRIX.json` in this directory. It preserves the two distinct jurisdictions, every original case ID, target stage, proposed test-node and negative fixture SHA where applicable. No 34th physical case is introduced.

## 2. Source inspection and bounded implementation path

Inspected the exact PR branch in WSL at `a4a41ac600ae63150ed2160911707ae49853d1bd` after a clean fast-forward, and corresponding current GitHub primary code:

- `src/nvda_desk/raw_signal_occurrence_truth/api.py:473-566,599-688,1074-1175,2127-2158`: existing `RawObservationOccurrenceV1`, `RawSignalProjectionMappingV1`, projected history with returned cursor, source original getter, and `create_owner()` returning a command/reads owner. This is the genuine M00 public source seam. **No new M00 product source alteration is assumed.**
- `src/nvda_desk/market_measurement_truth/api.py:132-256,590-702`: generic result `DerivedSignalOccurrenceV1.result` is `Decimal`; generic `RawProjectionReaderV1` exposes history but not the independent original getter needed by D091; the generic `create_owner` is for its currently configured measurement family. D091 needs the separately reviewed **categorical** DTO/factory and read-only source port, not a coerced numeric result.
- `src/nvda_desk/market_measurement_truth/_record_store.py:88-174`: typed `RecordState` supports immutable content-hash SQLite records and idempotent reuse; its existence does not automatically qualify a D091 category, observer or fault port. The new exact DTO codec and independent read-only D091 reader still require their own validation.
- `src/nvda_desk/market_measurement_truth/_native_d091.py`, `_controlled_r112.py` and the two case files below are **not present** at this pinned candidate. No D091 category product execution exists.

**Proposed, not yet implementation-released code/test paths:** `src/nvda_desk/market_measurement_truth/api.py`, `_controlled_r112.py`, `_native_d091.py`, `_native_codec.py`; plus `tests/product/m02_completion_28/d091/test_signal.py` (18 admitted physical cases) and `tests/product/m02_completion_28/l01b_r112/test_source.py` (15 source-support cases). These follow the design proposal `L04/D091_ENGINEERING_DESIGN_20261116/CHANGED_PATH_PROPOSAL.json` and the revised exact test-node inventory. No source or tests were changed under this preparation.

**Required semantic sequencing** (from `STAGE_PRECEDENCE.md` and `COHORT_AND_FIELD_REACHABILITY.md`): (A) check lawful request and true seal (UNSEALED before history); (B) validate the **actual** sealed private M00 cohort against its own immutable SUCCESS_15/B_TIE_2/B_OVER64_65 manifest; (C) exhaust genuine M00 projected pages and detect cycles/count/ties; (D) compare **all** projected candidates with genuine original getter, with G01–G03 faults restricted to selector read-only Stage D *after* trusted B and real C; (E/F) classify only the exact selected receipt, so original t12=1.01 yields RANGE, t13=Decimal NaN yields NONFINITE and t14 missing delta yields ABSENT; (G) only a lawful category appends/reads back an immutable D091 SQLite record. The 15 L01b malformed specimens require **individually observed field-specific public checked-ingress refusal before off-roster ID rejection**, with no M00 mutation. A result-only None or fabricated stage cannot substitute for these independent proof obligations.

The proposed five-field output-only `D091DiagnosticEventV1` and its seven finite stages are described in `L04/D091_PROOF_ADMISSION_PREP_20261116/DIAGNOSTIC_OBSERVER_CONTRACT.md`. It is *not* yet a callable, accepted product interface. No event is allowed to create successful data or set its own failure stage.

## 3. Exact remaining release prerequisites

1. **Typed product API and source/test-port binding:** accept and bind exact D091 categorical DTO/codec, output-only observer, private-coordinator writer-capability boundary, genuine negative-cohort construction and bounded read-only/SQLite fault ports; preserve the existing M00 and numeric M02 meanings.
2. **Claim/generation/implementation brief:** the current 35-obligation active ledger has D091 case IDs/ceiling but still records the product candidate/claim/source identity as unbound future. Prepare and independently clear the versioned M02 owner admission, result definition, calculation generation, proof contract and exact changed paths **before product code/test creation**; do not invent a claim generation or silently edit older `config/product_proof` claims.
3. **L00 recipient and actual required non-Git assets:** the independent product Tester must establish the necessary fresh pinned GitHub recipient/object/66-ref and asset proof under the installed checkpoint law. Previous engineering/GitHub reads alone are not the distinct Tester receipt.
4. **Qualified runtime:** selected product runner must bind actual CPython 3.13.5, loaded SQLite native library/source identity/feature needs and dependency lock. Current desktop WSL did **not** achieve the previously documented exact runtime qualification; see `NONPRODUCT_RUNTIME_PREFLIGHT_FAILURE.json`. Do not use its generic Python3.14.4 or SQLite3.49.1 default as proof of product-runner equivalence.
5. **Separate strict Tester and valid schedule:** designate and commission the distinct Tester for the exact admitted 18+15 cases only after required first release/claim/runner/receiver checks. Dependency-window design does not authorise arbitrary execution. No case may run solely because it is under a ceiling.

These prerequisites are evidence gates, **not defects in current product code**: the D091 categorical owner has not yet been implemented. A current explicit owner instruction to continue preparation does not by itself establish missing independent product-runner or receiver evidence, new generation bindings or a strict Tester designation.

## 4. Isolated non-product runtime attempt (current Windows/WSL host)

Read-only baseline: `/home/jds/.local/bin/python3.13 -V` returned **Python 3.13.5**; local `-m sqlite3 --version` returned **3.49.1**. Even with `LD_LIBRARY_PATH` directed at the newly isolated build, it continued returning **3.49.1**.

For a bounded *non-product* attempt, downloaded the official SQLite 3.54.1 source into `/home/jds/nvda_d091_runtime_20261117` (not the repository), verified official archive SHA-256 `926ef8d3eab93fbf6e06011901273eec076b25594a4e1cdadd50c987f4f6d64e` and SHA3 identities, compiled the **exact historically recorded command** under current local GCC **15.2.0** with exit code zero. The new lib SHA-256 is `44a469c2ed17ee19dca5f0c949f97b98b7ad0f1260bdb41fc153a4530324fb2f`, **not** the historical qualified GCC14.2.0 library `c53706980906943301153b630aeddba1b4aab6fe5eeda5752d8293952707db4e`; new bytes 1,957,800 versus historical 1,859,280. The **unmodified** repository `runtime_probe.py` exited 1 because the local `_sqlite3` module has no `__file__`, so its expected dynamic-extension inspection cannot be performed here. Exact historical binary/probe verification **FAILED**; nine storage assertions were **not** completed on this host. No equivalence or local qualification is claimed.

Raw receipt and trace are at `NONPRODUCT_RUNTIME_PREFLIGHT_FAILURE.json` in this directory, with preserved command, hashes, exit code and stderr; local original receipt at `/home/jds/nvda_d091_runtime_20261117/preflight_receipt.json`. No system SQLite library was installed or replaced. No NVIDIA product code or product test was run.

## 5. Stopping boundary and next authorised work

**Complete at this preparation boundary:** owner finite allocations remain exactly 18/15 and read-only code/runtime prerequisites were inspected; this record and matrix are durable on the *existing PR #27 Worker branch*. The **first unmet invariant** for moving to executable D091 proof is not the case budget—it is **exact implementation/claim/read-port/runner/Tester and recipient release**. Resolve source/claim/read-port decisions and an independently reviewable implementation brief next; obtain true runner and distinct Tester evidence before execution. No part of this document authorises a Worker product run, main merge, D145 activation, source-policy amendment or additional physical case.
