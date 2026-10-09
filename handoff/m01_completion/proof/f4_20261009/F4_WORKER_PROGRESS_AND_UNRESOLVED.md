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
