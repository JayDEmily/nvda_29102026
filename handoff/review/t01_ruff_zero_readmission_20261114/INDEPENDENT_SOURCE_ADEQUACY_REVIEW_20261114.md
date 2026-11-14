# T01 — Independent seven-claim zero-Ruff source-adequacy review

**Date:** 14 November 2026 (Australia/Melbourne)
**Reviewer:** Separate ChatGPT engineering-review conversation, direct Ubuntu/GitHub access; **no Terra Max or other external model API submission**
**Candidate:** `work/t01-ruff-zero-readmission-20261114` at `c616dc5da96af2c2901f2c93e05bbf69f489a725`
**Comparison:** PR #12 candidate `b67f3e92470fe4e3281546fbc6fc62e347d5f0ee`
**Review publication:** Separate `review/t01-ruff7-source-adequacy-20261114` branch; does not advance the worker branch

## Verdict and exact jurisdiction

**ACCEPT_SOURCE_ADEQUACY — 7/7 proposed successor sources, specifically for unchanged controlled proof assertions under the existing contracts.**

**NOT_ADMITTED / NOT_PROVEN / NOT_MERGEABLE_ON_THIS_REVIEW_ALONE.** No new generation has been authorised or written. This review establishes that the seven lint-motivated replacements retain their prior controlled test meaning, physical selection, exact numerical expectations and refusal assertions. It does **not** establish a successful product-proof aggregate, full architecture CI, semantic completion of the 39 leaves/35 obligations, production readiness or programme admission.

The **next unmet condition** is an actual separate programme authority decision to admit **seven new immutable generations**, referring to this completed source-adequacy review and independently identifying each legitimate admission. The required `admission_authority_ref` is not created by this review or by a green Ruff check.

## Governing evidence inspected

- Entire candidate `GUARDRAILS.md`, `AGENTS.md`, `tests/AGENTS.override.md` and root `EXEC_PLAN.md`; the root plan is a documentary M02 tranche and does not silently commission this distinct proof admission. Current user direction authorises the direct review.
- Entire `handoff/review/t01_ruff_zero_readmission_20261114/INDEPENDENT_REVIEW_REQUEST.md`, complete `PROPOSED_SUCCESSOR_GENERATIONS.json`, the exact seven **current** Python sources, their seven predecessor Git blobs, and all seven current active generation pointers and predecessor JSON files.
- All seven associated proof contract documents loaded and examined for `claim_id`, owning M02 target, family paths, required names, boundary/case propositions and compulsory support. Pilot FND-P06 type seam; D030/D031 K04 current-vs-20-prior Z; D032/D033/D035/D036 K05 exact R151 sample grids, annualisation and required refusals.
- Actual enforcing controls `tools/product_proof_claims.py:263–405` (full retained Git transitions, exact generation, bound family/support bytes), `tools/run_product_proof_gate.py:24–82` (READY state, clean checkout, strict observed aggregate), and `handoff/foundation_implementation/authority/PA02_PRODUCT_PROOF_ADMISSION_PROPOSED.md:125–193` (historical methodological evidence, **not** new owner authority). Also `pyproject.toml`, `Makefile` and Issue #8 history.
- All new proof-related JSON remains in `handoff/review/`, not in the active admission paths. No nested handoff AGENTS override was present.

## Independent method and actual checks

A new independent read-only audit, **not** the worker's `VERIFY_SOURCE_CANDIDATE.py`, is committed beside this review as `INDEPENDENT_AUDIT.py`. Its raw result is `INDEPENDENT_AUDIT_RESULT.json`.

1. In complete-history isolated Ubuntu Git worktree, resolved exact candidate commit and verified its PR #12 ancestry. `git diff --name-only b67f3e9... c616dc5...` contains **exactly** seven specified proof-source changes and three review-only handoff files. No admission pointer, generator, authority, runner, production source or root governance file was altered by the candidate.
2. Parsed each of the seven new Python files and independently extracted its previous blob using `git show <base>:<path>`. Six retained executable test/function structures and the pilot's type specimen are AST-identical after normalising only the four explicit `pairwise(SAMPLES)` forms back to their old `zip(SAMPLES, SAMPLES[1:])`; the three other files match without normalisation. Imports differ only where necessary for `itertools.pairwise`.
3. Independently extracted the four literal timestamp tuples from the AST. For D032/D033/D035/D036, `tuple(pairwise(SAMPLES)) == tuple(zip(SAMPLES,SAMPLES[1:]))`, with respectively **5, 30, 5 and 10** unchanged return intervals. The substitutions preserve order, endpoints and exact `FRAC` assignment in each committed test.
4. Parsed and compared every proposed generation row against the actual current predecessor pointer, existing file SHA-256, full proposed family/support membership, complete contract family/test-name mapping, actual brief/binding/contract SHA-256 and expected M02 target. All seven are internally consistent and each changes precisely **one** pinned family or support hash. All seven proposed `adequacy_review_ref` and `admission_authority_ref` values remain `null`; no proposed generation file exists in active `config/product_proof`. Total proof population remains **11 physical families / 15 required test function names**, across **seven distinct claim aggregates**.
5. Independently ran `/home/jds/nvda_uv3135_20261112/.venv/bin/ruff check src tests tools` from the candidate worktree: **Ruff 0.15.11, All checks passed**. This static lint command used the existing isolated CPython **3.13.5** toolchain and did not run a product test. Also ran `git diff --check <base> HEAD` and `git fsck --full --strict --no-reflogs`: both exited 0. The worktree was clean before review-branch publication.

No pytest, `run_product_proof_gate.py`, architecture promotion gate, provider model job, runtime/product market-data session or new admission command was executed. The product proof contracts' historically specified **CPython 3.12.14/SQLite 3.53.1** execution environment was not recreated or substituted by the static 3.13.5 checks.

## Independent source-level adequacy by claim

| Claim | Reviewed physical change | Accepted positive/refusal proposition retained | Source verdict |
|---|---|---|---|
| Pilot generation 4→5 | `typing/valid_seam.py`: remove a blank line between imports; required FND-P06 support | Real public factory and typed M00 reader, typed return/optional reads; `test_public_seam_static_compatibility` and its other selected physical families unchanged | **ACCEPT_SOURCE_ADEQUACY** |
| D030 generation 2→3 | `test_trade_rate_zscore.py`: wrap `UnitConventionVersionV1` | R062 current 16 trades/min and 20 prior alternating 8/12; negative all 8 yields zero sample SD, `None` and empty history; exact Decimal and durable readback retained | **ACCEPT_SOURCE_ADEQUACY** |
| D031 generation 2→3 | `test_volume_rate_zscore.py`: wrap `UnitConventionVersionV1` | R063 current 16 shares/min and 20 prior alternating 8/12; negative prior-0 receipt after cutoff is directly seen at later cutoff, excluded at current cutoff and refuses with empty history | **ACCEPT_SOURCE_ADEQUACY** |
| D032 generation 2→3 | `test_five_minute_realised_volatility.py`: formatting, one pairwise substitution | Six 12:35–12:40 R151 samples, five year-fraction intervals, exact 50-digit result; negative missing 12:37 with off-grid 12:37:30 cannot repair and refuses | **ACCEPT_SOURCE_ADEQUACY** |
| D033 generation 2→3 | `test_thirty_minute_realised_volatility.py`: formatting, one pairwise substitution | 31 12:10–12:40 samples, 30 intervals, exact expected annualised result; negative removes first 25 grid events, leaves last six and refuses | **ACCEPT_SOURCE_ADEQUACY** |
| D035 generation 2→3 | `test_five_day_realised_volatility.py`: formatting, one pairwise substitution | Six 15–20 October official closes, five year fractions and exact expected result; negative missing 17 October close cannot be rescued by an older 14 October decoy | **ACCEPT_SOURCE_ADEQUACY** |
| D036 generation 2→3 | `test_ten_day_realised_volatility.py`: formatting, one pairwise substitution | Eleven 10–20 October official closes, ten year fractions and exact expected result; negative keeps only six closes and refuses | **ACCEPT_SOURCE_ADEQUACY** |

For all D030–D036, the public raw projection, accepted synthetic fixture, `OwnerAdmissionV1` calls, persisted result identity and exact positive/negative assertions remained AST-identical to the previously admitted sources, except for the proven four interval-construction replacements. This is a semantic review of **the actual asserted test boundaries**, not a claim of new runtime execution or general correctness of the underlying production mathematics.

## Historical recurrence and current admission blocker

Issue [#8](https://github.com/JayDEmily/nvda_29102026/issues/8) records the earlier PR #7 class of failure: Ruff-edited proof bytes no longer matched retained generation SHA pins, and the actual architecture test suite refused them. The same immutable-byte invariant is deliberately unsatisfied in this **unadmitted** candidate. It is **not** a new source-code regression, nor a reason to weaken the SHA validator. Treat this as the known **RECURRENT_CLASS: altered SHA-pinned proof bytes require new legitimately reviewed/admitted generation identities**. The candidate's separate proposed successors address the provenance design; the missing independent programme admission decision remains the first active blocker.

The source-equivalence judgement does **not** authorise copying old authority strings, setting reviewer or admission fields to an invented value, rewriting old generations, bypassing the current resolver, invoking product proof early or merging. Actual `tools/product_proof_claims.py:396–405` compares file SHA-256 against the current active generations; the independent audit confirms all seven changed physical paths disagree with those old SHA pins.

## Exact next sequence (not executed by this review)

1. Obtain one **real, separately traceable programme admission decision** explicitly covering the seven named claim successors and this pinned independent review. Preserve claim-specific references as required by authority. No admission is inferred from the user's instruction to continue reviewing.
2. Under that authority, materialise new immutable generation **0005** for pilot and **0003** for D030/D031/D032/D033/D035/D036, one lawful transition per claim, each with its actual review/admission refs and predecessor hash. Do not change old generations; keep full Git history. Confirm current resolver is ready at each committed state.
3. Have the authorised **independent strict tester** execute one exact existing claim-scoped `run_product_proof_gate.py --aggregate <claim>` at a time, in its governed pinned environment, retaining raw positive/refusal evidence and governed snapshots.
4. Only after genuine admission and product acceptance, run original strict whole-tree Ruff and architecture-kernel CI on the fully admitted candidate, then obtain independent cumulative review before considering integration.
5. Preserve PR #14 as historical lint-policy evidence, unchanged original proofs, main, the 39 leaves/35 documentary obligations and D145 suspension.

**Final disposition:** `ACCEPT_SOURCE_ADEQUACY (7/7); BLOCKED_PROGRAMME_ADMISSION_AUTHORITY; NO_PRODUCT_PROOF_EXECUTED; NO_MERGE.`
