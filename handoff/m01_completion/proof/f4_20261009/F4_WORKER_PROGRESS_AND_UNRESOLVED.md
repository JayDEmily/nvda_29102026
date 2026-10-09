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
