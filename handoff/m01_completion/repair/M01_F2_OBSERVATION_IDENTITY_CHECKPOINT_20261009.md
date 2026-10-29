# M01 Stage 1 — F2 bounded observation-identity repair checkpoint (2026-10-09)

## Authority, sequencing and disposition

The current root `GUARDRAILS.md`, `AGENTS.md`, `tests/AGENTS.override.md`, `EXEC_PLAN.md` §4 F1–F4, and the reviewer F1 acceptance commit `a503430` were read before implementation. Only F2 is authorised; F1 accepted does **not** mean Stage 1 accepted. This checkpoint is a WORKER EVIDENCE candidate for independent review, **not** Stage-1 `PASS`. F3 and F4 have not been entered.

## Verified repair mechanism

The reviewer canonical public repro (`handoff/m01_completion/review/proof/test_stage1_signed_flow_public.py`) established that derived D015 occurrence IDs cannot be used as M00 raw R120/R121 observation IDs. The original sign was +1, yet D016/D120 persisted unjustified zeros. The new kernel helper `_observation_signs` joins a D015 sign through its **persisted raw source lineage**, source/cutoff times, and subject and exact contract identity, requires a complete native trade field set and refuses absent/conflicting classifications rather than emitting a fabricated total. D016 and D120 calculate their accepted signed size and signed premium-notional sums. The owner selects all historical D015 inputs but persists only actual contributing D015 IDs as direct predecessors; ultimate R-lineage remains preserved. D017 now checks all raw price-size native observation identities and refuses partial co-reference rather than aggregating an intersection.

Proof-first history: two test-only commits demonstrated the baseline failures before any production modification; the third test-only commit reformatted tests; only after these did a source-only repair commit occur. Proof logs are in `handoff/m01_completion/proof/f2_observation_identity_20261009/`.

### Exact public proof

- Unmodified independent reviewer fixture: D011=5, D015=+1, D016=2, D120=(signed_contracts=2,signed_premium_notional=1200).
- Two opposite trades share one contract; aggregation includes both D015 predecessor IDs and the corresponding R121 trade IDs; retry and recalculation remain deterministic.
- Missing, ambiguous, absent-size, mismatched contract, incompatible mapping version, later-cutoff and cross-record raw-pair cases refuse or select only eligible facts.
- `F2_EDGE_RECONCILIATION.csv` maps **all 18 F1 edges** of the six explicitly assessed rows (D015, D016, D017, D064, D065, D120). This is *mechanism-level representative proof*, not 18 separately executed edge tests.

### Important unresolved U04 — **BLOCKED public proof / no invented repair**

D065's event importance comparison is not yet independently proved through the admitted public materialisation seam. Source `_eval_k08` still compares a selected R284 raw event `occurrence_id` directly with a D064 **derived** occurrence `occurrence_id`; no accepted cross-namespace identity equality exists. Its prerequisite D064 row declares **R289 raw only, no derived dependencies**, whereas current K07 `_score` requires a nonempty `score_features` list all referencing the row's **derived** dependencies. That makes a public end-to-end D064→D065 witness unsupported by the present implementation. Authorising a raw-score mapping or treating raw and derived event IDs as interchangeable would invent a substantive upstream scoring rule; neither was attempted. Therefore U04 is **UNPROVED/BLOCKED for public correlation** and cannot be counted as an F2 closure or Stage-1 acceptance. The earlier F1 U04 classification remains open. This is a separately identified prerequisite implementation gap, not a passed D065 regression.

U06 D017 raw/raw pairing is exercised. RC07 D015 quote-to-trade cardinality variants are not all independently exhausted. F3 D109/D170 re-proof, D121/D122 multi-contract grouping and F4 census-wide semantic acceptance remain deferred. The 144 Stage-1-closed and 30 Stage-2-dependent populations are unchanged. M00 source owner, raw tables, authority and version 1.0.0 are unchanged.

## Validation environment, commands and limitations

- Python 3.13.5 / pinned `pytest 9.0.3`, `psycopg 3.3.4`, `ruff 0.15.11`, `mypy 1.20.1` from provided U05 offline bootstrap; PostgreSQL 17.9 from supplied portable archive. Pinned PyYAML 6.0.3 is linked from preinstalled `/opt/pyvenv` and imports successfully; no repository dependency or version altered.
- Fresh database `postgres` has separate `nvda_m00_proof` and `nvda_m01_proof` roles and schemas, with database `CREATE` granted to the test M00 role. The environment uses Unix socket only and PostgreSQL durability settings verified by bootstrap.
- `pytest -q tests/product tests/architecture tests/bootstrap tests/implementation/derived_signal --ignore=tests/product/raw_signal/test_u05_postgresql_durability.py` **672 passed** (with separate M00/M01 role DSNs configured and repository added to Git safe.directory). Exact output: `proof/f2_observation_identity_20261009/full_non_durability_672_pass.log`.
- `pytest -q tests/implementation/raw_signal tests/product/derived_signal/test_m01_f2_observation_identity.py handoff/m01_completion/review/proof/test_stage1_signed_flow_public.py` **46 passed** (including unchanged reviewer witness). Exact output: `proof/f2_observation_identity_20261009/focused_and_m00_46_pass.log`.
- `python -m mypy src`: **21 source files, no issues**; `ruff check src tests tools`: passed; `python tools/validate_architecture.py`: passed, **0 dependency/public-seam violations**.
- The **55-case M00 multiprocess PostgreSQL durability file was not rerun** in this F2 pass; it is separate from the above 672-count suite and must not be represented as passed here. It was previously checked in bounded batches by the predecessor worker, as recorded in `M01_STAGE1_POSTGRES_PRE_REVIEW_VERIFICATION_20261008.md`. F4 still requires its proper environment-level verification.

No tests, dependencies, normative CSV, brief, ExecPlan, guardrails or architecture rules were weakened to obtain these results. Submission is for an independent F2 **partial/bounded repair disposition and explicit U04 prerequisite**; it must not be promoted to Stage-1 acceptance or used to self-authorise F3 until the reviewer resolves the blocker.
