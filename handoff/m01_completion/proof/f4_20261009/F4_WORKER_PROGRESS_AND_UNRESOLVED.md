# M01 F4 — public relationship proof progress (not a review candidate)

Date: 09-10-2026. Governing: `GUARDRAILS.md`, `AGENTS.md`, root `EXEC_PLAN.md`, F2 independent `F2_ACCEPTED` and F3 worker handoff. F3 base worktree `36105f05abaf4efd485594ac013078b606057b74` is preserved in ancestry. **This is an internal F4 recovery checkpoint; independent Stage-1 review is NOT requested or implied.**

## Established F4 work

1. **RC12 D145: four native book fields.** `test_m01_f4_book_ofi_public.py` builds controlled raw observations in the actual M00 owner and consumes them through M00's versioned public projection mapping. It computes the canonical OFI `+3` from two complete best-book state changes with native event source lineage. The negative witness removes R188 from one otherwise eligible event; the existing K17 path erroneously calculated a result by silently omitting that book mutation. The failing test and output were committed at `5534ddb` **before** the minimal `_stage1._eval_k17` repair at `cc8699e`. The repair rejects duplicate/missing required field-occurrence IDs rather than inventing a shortened event sequence; separate knowledge-cutoff and delayed-event proof remains. Red: `F4_RC12_D145_PUBLIC_RED.log`; focused green: `F4_RC12_D145_REPAIRED_FOCUSED.log`.
2. **RC13 D151: exact basket component denominators.** `test_m01_f4_basket_breadth_public.py` uses controlled M00 projections from three distinct basket subjects; R137 is lawfully absent for one. Public D151 returns `(2/3,1/2,2/3)` for its three independent breadth components; missing a required *selected basket binding* is refused, and all contributing observation IDs remain in raw lineage. Committed at `4936048`. No D151 production change.
3. **Conservative reconciliation.** `f4_progress_readback.py` checks the exact normative catalogue digest, 209 D rows, 174 Stage-1 rows, the 144 Stage-1-closed / 30 cross-stage partition, all 488 F1 edges plus D007 sentinel, and advances **only** the four D145 and four D151 raw edges. Output: `F4_RELATIONSHIP_PROOF_LEDGER.csv` and `F4_PROGRESS_READBACK.json`. Prior F2/F3 edge statuses are left untouched.

## Verification executed on this F4 source tree

- `725 passed`: `PYTHONPATH=.:src python -m pytest -q tests/product tests/architecture tests/bootstrap tests/implementation/derived_signal --ignore=tests/product/raw_signal/test_u05_postgresql_durability.py`, with pinned Python 3.13 proof environment and live PostgreSQL 17.9 local instance. **Both** `NVDA_TEST_M00_POSTGRES_DSN` and `NVDA_TEST_M01_POSTGRES_DSN` target separate established `f3_m00` and `f3_m01` roles/schemas; command readback is `F4_COMBINED_REGRESSION.log`.
- The first combined attempt had **41 environment configuration failures**, because the restored shell exported only the administrator DSN; `F4_INITIAL_MISSING_ROLE_DSN_FAIL.log` is retained. Those are not counted as test passes. The role-specific DSNs were established and the same suite was rerun successfully; `F4_COMBINED_REGRESSION.log` supersedes the failed *invocation*, not its evidence.
- Repository Ruff, source mypy (21 files), relevant formatter, structural architecture validation and F4 reconciliation readback pass. Exact logs present here.
- The **55 M00 durability cases** previously passed during F3 in bounded runs. They were **not rerun** during this intermediate F4 checkpoint, and are not presented as fresh F4 results.
- The F4 test harness uses controlled observations, not real provider-native event/book compatibility evidence. No M00 source code, accepted catalogue/brief, governing safeguards or package version was changed.

## Unresolved Stage-1 acceptance proposition

The F4 ledger contains **344 Stage-1-closed edges still not individually reconciled to a positive/adversarial public-seam witness**. This is an evidence gap, **not** a finding of 344 implementation failures. D145/D151 prove bounded rows only; they do not establish every other RC12/RC13 mechanism. The full 144 closed rows' production/public end-to-end reachability and 30 cross-stage rows' own-kernel and lawful refusal propositions have not been established. No Stage-1 acceptance or Stage-2 authority.

**Next authorised action:** Continue F4 class/row-specific public and adversarial proof, including remaining RC12 book event mechanisms and other F1 matrix entries. Preserve proof-before-production Git order; reconcile every applicable relationship and the 144/30 population before producing the single independent Stage-1 F4 candidate. Do not return this internal checkpoint as a semantic acceptance candidate.


## 09-10-2026 continuation — F4 red proof / authority stop (latest)

F4 work after original `95ba585` checkpoint has implemented and proved bounded public mechanisms: D139/D140 SMART book-event side/level rates (incomplete-event refusal), D143 direct venue concentration and D144 SMART/direct divergence (incomplete-event refusal), and D007 versioned `RequiredFieldPolicy` completeness through M00 without mutating its zero-edge catalogue declaration. Their proof-first source commits and tests are preserved in the current Git ancestry, alongside prior D145 and D151 proofs. None is representative proof of an entire relationship class.

The first unresolved authority invariant is **D134/D135 representation**: accepted raw dependencies R185/R188/R190 omit operation R187, whereas the current `_book_events` path unconditionally depends on R187. A controlled M00 public witness returns a persisted zero bid depth for a projected nonzero bid. The accepted brief expressly requires event operations for *event-driven* L2 books but does not specify how a three-field complete snapshot is identified as coherent. The witness remains **failing** rather than being weakened or bypassed. Detailed source, negative test, and one programme-owner decision: `F4_RC12_D134_D135_AUTHORITY_BLOCKER.md`.

The conservative revised ledger accounts for **35 bounded F4 edges**, **317 still-unproved Stage-1-closed edges**, 18 accepted F2, 11 bounded F3, 107 Stage-2-deferred and the D007 zero-edge public sentinel, totalling the unchanged 488 normative dependencies plus the sentinel. The six D134/D135 raw edges remain **unproved**. Full public proof for 144 closed and kernel/refusal proof for 30 cross-stage remains open.

Focused deliberately failing witness: `F4_RC12_D134_D135_PUBLIC_DEPTH_RED.log`. Combined test run excluding **that failing witness** and separate M00 durability suite: **734 passed** with separate M00/M01 PostgreSQL DSNs (`F4_CURRENT_GIVEN_UNRESOLVED_PUBLIC_TEST_EXCLUDED.log`). Ruff and 21-source-file mypy pass (`F4_CURRENT_RUFF.log`, `F4_CURRENT_MYPY.log`). **The failed witness was not made to pass.** No full-F4 review candidate is offered; stop at programme-owner authority decision.


## 10-10-2026 internal RC02 continuation — current count/readback

Programme Owner's 09-10-2026 R187 exception and book repair are now committed,
resolving the previously documented D134/D135 authority blocker. After
`db943a7`, independent public M00 tests at
`tests/product/derived_signal/test_m01_f4_nbbo_algebra_public.py` establish:

- D011 midpoint `(100+102)/2 = 101`, exact R034/R035 lineage;
- D012 spread `102-100 = 2`, exact R034/R035 lineage;
- D013 percentage spread `100*2/101 = 200/101`, exact D011/D012 predecessor occurrence
  references with inherited R034/R035 lineage (no test-injected predecessor);
- D014 size imbalance `(8-2)/(8+2) = 0.6`, exact R033/R036 lineage;
- negative missing-field, future and other-subject observation exclusion; repeat
  materialisation returns the same derived occurrence.

Tests committed at `954889f` before reconciliation changes, with Ruff-only
format hygiene at `566834e`. Focused: **11 passed**. Combined full non-durability:
**768 passed**, command:
`PYTHONPATH=.:src python -m pytest -q tests/product tests/architecture tests/bootstrap tests/implementation/derived_signal --ignore=tests/product/raw_signal/test_u05_postgresql_durability.py`,
under Python 3.13.5, PostgreSQL 17.9 and distinct `f4_m00`/`f4_m01` writer roles
with distinct same-named schemas. First run **767 passed, 1 failed** because
`f4_m00` lacked database-level schema CREATE privilege for a test-created probe;
this was corrected in the external **test environment**, not production, and the
whole suite rerun green. See `F4_RC02_FIRST_ROLE_NO_CREATE_FAIL.log` and
`F4_RC02_M00_M01_POSTGRESQL_COMBINED_REGRESSION.log`. `python -m ruff check
src tests tools handoff/m01_completion/proof/f4_20261009/f4_progress_readback.py`
passed; `python -m mypy src` passed (21 files). M00 durability suite not rerun.

The amended effective catalogue digest is
`8045c8c0c4a62fbc3b88759a65b415efb1f0d549764ddbdcae2c5c911cd8a64a`;
490 normative edges + D007 zero-edge sentinel reconcile to **272**
Stage-1-closed outstanding edges across **113** rows. All **30** cross-stage
own-kernel/refusal obligations remain open. This is bounded RC02 proof only,
not proof of every RC02 row or full Stage-1 acceptance. Continue F4 without
new intermediate independent review; preserve single consolidated acceptance
boundary. No Stage 2 implementation or authority change.


## 10-10-2026 expanded RC02 public proof — supersedes 272-edge snapshot

Proof-first commit `892ab71` adds
`tests/product/derived_signal/test_m01_f4_rc02_scalar_algebra_public.py`
with **25 passing tests** for D025 (0.5), D042 (1.25 percentage points),
D043 (1 percentage point), D047 (10 bps), D057 (-2 points, ratio 0.9),
D058 (1 point, ratio 20/19), D059 (-2 points, ratio 19/21), and D060
(ratio 110/19). Inputs are separately owned native M00 observations, selected
via exact public versioned projections. Each result is tested for canonical
numerical result, full R lineage and deterministic retry. Missing, future and
wrong-subject raw inputs are refused, as are zero denominators for D025/D060.
No production repair was required for these eight rows.

Complete applicable non-durability regression **793 passed** in live
PostgreSQL 17.9 separate M00/M01 role environment; Ruff and mypy (21 source
files) passed. Exact logs:
`F4_RC02_EXPANDED_POSTGRESQL_COMBINED_REGRESSION.log`,
`F4_RC02_EXPANDED_RUFF_PASS.log`, `F4_RC02_EXPANDED_MYPY_PASS.log`.
The M00 55 durability tests have not been rerun in this pass.
The reconciled F4 ledger now classifies **99 bounded F4 public edges**, 255
outstanding Stage-1-closed edges across 105 rows, 107 deferred Stage-2
edges, 18 accepted F2 scoped evidence, 11 bounded F3 edges, and one D007
zero-edge sentinel. 30 cross-stage own-kernel/refusal obligations remain
unproved. Stage 1 remains unaccepted; this is an internal proof checkpoint.


## 10-10-2026 RC02 provider VWAP gap and RC01 temporal repair (internal)

- `ff1bb57`: D018 public calculation with real M00 native trade-pair inputs,
  D017 recursive VWAP 4.8, provider VWAP 5, D018 result difference 0.2 and
  bps 10000*0.2/4.8; exact native/derived lineage and negative evidence.
- `97857be`: RC01 native M00 public D001–D005 temporal tests committed **red**:
  12 passed, receipt-only D002 failed because public graph demanded a
  nonexistent D001 even though accepted K01 age rule permits receipt age.
- `d5c34df`: bounded production graph repair passes all 13 RC01 temporal
  tests, including true-instant D001 and D002, date-only refusal, receipt-only
  D002 with collector basis and no invented D001, configured exchange date and
  overnight session phase, missing/future refusal and exact raw lineage.
  D002's **catalogue** D001 dependency was not removed.
- Combined readback:
  `F4_RC01_D002_D018_COMBINED_REGRESSION.log`: **809 passed** in separate
  PostgreSQL 17.9 M00/M01 roles, excluding the separately scoped 55-case M00
  durability suite. Ruff and 21-file source mypy passed:
  `F4_RC01_D002_D018_RUFF.log`, `F4_RC01_D002_D018_MYPY.log`.
- Current F4 reconciliation enumerates **490 authority edges** and the D007
  sentinel; **240 Stage-1-closed relationship edges across 99 rows remain**
  unproved, alongside **30 unproved cross-stage kernel/public-refusal rows**.
  No row is accepted merely because class-level or per-edge accounting exists.
  Do not submit Stage 1 for review yet. M00 provider/live compatibility and
  Stage-2 functionality remain outside this proof.


## 10-10-2026 current RC01 / RC14 native exact-contract evidence and durability

Additional `daf8ab2` and `d4442fa` proof-first (test-only) commits establish:

- D010 public configured open/closed market calendar, native raw and D003
  predecessor evidence, missing-input refusal;
- D085 public seven whole expiry days with exact option-contract identity and
  D004 overnight trading-day predecessor, missing/past-expiry refusal;
- D086 public ACT/365F from exact UTC D001 and provider expiry at configured
  16:00 Australia/Melbourne with exact option-contract identity, missing/past
  expiry refusal;
- D087/D088 public exact-contract midpoint 100/spread 2 and D087 recursive
  predecessor linkage, and D089/D090 strike 150/spot 120=1.25/log(1.25),
  selecting the true contract over competing C2 and refusing missing, future,
  and zero denominator. Each preserves bounded raw/derived lineage and retries.

Whole applicable non-durability regression **832 passed** using Python 3.13.5,
pinned pytest 9.0.3 and PostgreSQL 17.9 with independent M00/M01 roles.
Ruff and mypy 21 files pass. Exact logs:
`F4_RC01_RC14_832_PINNED_PYTEST_COMBINED_REGRESSION.log`,
`F4_RC01_RC14_832_PINNED_RUFF.log`,
`F4_RC01_RC14_832_PINNED_MYPY.log`.

Separately scoped M00 durability proof: **55/55 passed in eight non-overlapping
batches** under a clean Python 3.13.5 virtualenv with pinned pytest and
psycopg 3.3.4. An unrelated Pydantic object graph exception prevented an
initial **ambient** invocation (14 passed, 1 failed in the final 15-test
batch); that failed run and negative diagnosis remain available. No M00 code
or test was modified to obtain the passing isolated rerun. Details, exact
collected test IDs and 8 passing logs in `F4_M00_DURABILITY_CLEAN_READBACK.md`.

Current ledger: 490 authority dependencies + D007 sentinel, 132 newly
bounded F4 public edges plus inherited 18 accepted F2 scoped, 11 bounded F3,
107 deferred cross-stage edges; **222 outstanding Stage-1-closed edges across
92 rows** and **all 30 cross-stage own-kernel/refusal row obligations** remain.
This is not the consolidated F4/Stage-1 review candidate.


## 10-10-2026 RC01 D062 + RC20 D009 complete-vintage proof and repair

- `feeeb52` is proof-first public M00 D062 earliest eligible future event:
  event in 120 seconds/2 minutes beats 300 seconds; exact native R284 and
  D001 predecessor/raw R002/R003 lineage; historical/past-only, missing and
  future-received input refusal; deterministic retry.
- `b509b04` is a separately committed **red** RC20 public D009 macro-vintage
  test (1 failed, 2 passed): a newer source-native revision with missing
  required R282 was excluded from alignment, causing older complete revision
  to masquerade as latest known vintage. Original red log preserved:
  `F4_RC20_MACRO_INCOMPLETE_PUBLIC_RED.log`.
- `a5ab688` is the bounded production completeness repair for native D009
  macro revision fields R280/R281/R282. Focused D009/D062: 6 passed;
  no changes to the normative catalogue or M00 source ownership.
- The full applicable non-durability PostgreSQL 17.9 suite passes **838
  tests**. Exact invocation after sourcing `/mnt/data/f4_pg_env/postgres.env`:
  `PYTHONPATH=.:src python -m pytest -q tests/product tests/architecture tests/bootstrap tests/implementation/derived_signal --ignore=tests/product/raw_signal/test_u05_postgresql_durability.py`
  with `NVDA_TEST_M00_POSTGRES_DSN` and `NVDA_TEST_M01_POSTGRES_DSN`
  individually set to local PostgreSQL 17.9 `f4_m00` and `f4_m01` roles.
  `python -m ruff check src tests tools handoff/m01_completion/proof/f4_20261009/f4_progress_readback.py`
  and `python -m mypy src` both pass. Logs:
  `F4_RC01_RC20_838_POSTGRESQL_COMBINED_REGRESSION.log`,
  `F4_RC01_RC20_838_RUFF.log`, `F4_RC01_RC20_838_MYPY.log`.
- Readback is conservatively reconciled to **137 newly bounded F4 public
  relationship edges**, **217 still-unproved Stage-1-closed edges across 90
  rows**, 18 inherited accepted F2 scoped edges, 11 bounded F3 edges, 107
  deferred cross-stage edges, and the D007 zero-edge sentinel. All 30
  cross-stage own-kernel/refusal obligations remain. Do not promote
  bounded proof status into Stage-1 acceptance.
- Separately scoped M00 durability 55/55 pass remains prior clean pinned
  readback at `30c5e54`; it was **not rerun** for these two public rows.


## 10-10-2026 RC03 public history/anchor class — post-838 continuation

- Proof-first commit `3480116` adds independent M00 public-interface cases across
  **all 24 RC03 Stage-1-closed rows**: D019–D024, D026–D027, D044–D046,
  D048–D056 and D066–D069.  There are **29 matching RC03 relationship
  edges** in the authoritative F1 inventory. The proof includes distinct
  1m/5m/30m anchors and D024 predecessor graph, exact log returns, session
  open/prior close/VWAP comparisons, configured yield/volatility/risk history,
  price/percent/basis-point output, one-day anchors, and M00 raw/derived
  lineage plus deterministic retry. Negative witnesses cover wrong subjects,
  ineligible nearer observations, missing references and future-cutoff inputs.
  No production change or catalogue mutation was necessary for this class.
- The focused suite passes **29/29** cases
  (`test_m01_f4_rc03_history_public.py`). The expanded live PostgreSQL 17.9
  regression passes **867 tests** with separate writer roles and schemas;
  exact log `F4_RC03_867_POSTGRESQL_COMBINED_REGRESSION.log`. Ruff and mypy
  (21 files) pass in `F4_RC03_RUFF.log` and `F4_RC03_MYPY.log`.
- Environmental attempts and diagnostics are preserved:
  an initial collection failure for absent PyYAML 6.0.3 was observed and
  summarised in `F4_RC03_ENVIRONMENT_DIAGNOSTIC.md`;
  `F4_RC03_FULL_POSTGRESQL_COMBINED_REGRESSION.log` documents the interim
  866-pass/1-fail run with inherited ANSI colour forced in mypy output.
  The final pinned execution isolated colour configuration without editing
  or bypassing any tests, and was green.
- Effective normative catalogue remains the authorised R187-adjusted
  SHA-256 `8045c8c0c4a62fbc3b88759a65b415efb1f0d549764ddbdcae2c5c911cd8a64a`
  with **490 edges plus one D007 sentinel**. F4 ledger now records **166
  bounded F4 public edges**, **188 outstanding Stage-1-closed edges across
  66 rows**, 18 inherited F2 scoped edges, 11 F3 bounded edges, 107
  deferred Stage-2 edges and one D007 zero-edge sentinel. **All 30
  cross-stage own-kernel/refusal obligations remain open.** RC03 bounded
  public edge evidence is not whole Stage-1 or independent acceptance.
- The previous separate **55/55** pinned M00 PostgreSQL durability readback
  is retained at `30c5e54`; this run did not independently rerun that suite.
- A potential D123 exact-contract/open-interest history concern was
  identified by static source inspection only; no positive defect claim or
  F4 ledger credit is made without a public reproducer. Continue with
  authority-derived unproved classes, not Stage 2.


## 10-10-2026 RC01 data-quality and receipt trigger — post-RC03 continuation

- Proof-first commit `1a8a0c6` adds public M00 witnesses for D006
  staleness score, D008 structured alignment and D209 recalculation trigger.
  Immutable declared P_SCORE features combine age, admitted provider type
  code and cadence in D006 (exact result 2.75); D008 reports two true instants
  of five-second skew, coverage 2/3, one receipt-only missing event instant,
  and a versioned bounded sigmoid score. D209 persists the native receipt
  timestamp and control fact with versioned schedule context, without actions.
  Tests cover full raw/predecessor lineage, deterministic retry, incomplete
  fields, wrong source and future/receipt-only refusal. 12 focused tests pass.
- Full applicable isolated PostgreSQL 17.9 non-durability regression:
  **879 passed** (`F4_RC01_879_POSTGRESQL_COMBINED_REGRESSION.log`).
  Ruff and mypy pass (`F4_RC01_879_RUFF.log`, `F4_RC01_879_MYPY.log`).
  The prior 55 passing M00 durability tests were not rerun this time.
- The amended normative catalogue is unchanged at 490 dependency edges
  (plus D007 zero-edge sentinel). RC01 now has zero unproved Stage-1-closed
  relationships. F4 ledger stands at **174 newly bounded public edges**
  and **180 still unproved Stage-1-closed edges across 63 rows**.
  All 30 cross-stage own-kernel/public-refusal obligations remain open.
  This is bounded evidence only, not full Stage-1 proof or acceptance.



## 10-10-2026 RC04 D028 exact elapsed-session-fraction repair

- Proof-first commit `d86b83b` includes accepted-brief §5 K04 public M00 evidence:
  D028 R041/R044 per-native-occurrence pairing; prior source volume at
  elapsed fractions 0.25 and 0.75 may not be compared with current 0.5.
  Original public red output preserved in
  `F4_RC04_D028_ELAPSED_FRACTION_PUBLIC_RED.log` (1 failed/10 passed).
  Additional tests demonstrate D029–D031 sample N-1 z arithmetic and
  insufficient/zero-SD refusal; these **do not** independently establish the
  matching same-time-of-day/20–60-session horizon requirements, so those
  rows receive **no F4 public proof ledger credit**.
- Bounded production repair commit `fe293a0`: D028 now pairs R041/R044 using
  the *same native M00 observation occurrence*, refuses missing/invalid
  elapsed fractions, filters historical volumes to the exact current
  fraction and never treats unmatched values as suitable baseline inputs.
  The interleaved wrong-fraction volume=999 cannot change the correct
  D028 result 16/mean(8,12)=1.6.  No normative catalogue mutation.
- Final focused RC04 D028 + K04 arithmetic tests **13 passed**; combined
  applicable non-durability PostgreSQL M00/M01 suite **892 passed**.
  Ruff and mypy pass; see `F4_RC04_D028_892_POSTGRESQL_COMBINED_REGRESSION.log`,
  `F4_RC04_892_RUFF.log`, `F4_RC04_892_MYPY.log`.
- Exact F1/F4 reconciliation remains 490 normative edges plus D007
  zero-edge sentinel. Only D028 R041/R044 (two edges) promoted to bounded
  public proof, leaving **178 outstanding Stage-1-closed edges across
  62 rows**; all 30 cross-stage own-kernel/public-refusal obligations
  remain open.  D029–D031, remaining RC04 and other F4 classes remain
  unproved beyond the explicitly stated partial arithmetic checks.
- The separately scoped 55-test M00 durability suite has **not** been
  rerun in this continuation; previous 55/55 checkpoint remains historical.
  F4 and Stage 1 are not accepted. Stage 2 remains unauthorised.
