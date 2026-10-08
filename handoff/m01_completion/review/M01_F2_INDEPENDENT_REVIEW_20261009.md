# Independent M01 Stage-1 F2 review — REPAIR / RECURRENT_CLASS

## Exact submitted evidence boundary
- Worker `work/m01-completion` candidate: `dcd2067bbd306e1cf1aeb5fc9665dce25a4c8684` / tree `f3e320ed0b660622935a222063e8741ebf527ebb`.
- Reviewed predecessor accepted F1: `a50343063976e5c67eac7878c1e44e8f8c95064b`.
- Governing files read: `GUARDRAILS.md`, `AGENTS.md`, `tests/AGENTS.override.md`, active root `EXEC_PLAN.md`, `handoff/m01_completion/AUTHORITY_INDEX.md`, accepted Markdown brief and canonical CSV. The independently reviewed F1 map, original M01 Stage-1 signed-flow review and current worker F2 checkpoint were examined.
- No Stage-1 `PASS`, no F3 authorisation, no M00 semantic change, no programme acceptance.

## Disposition
**REPAIR / RECURRENT_CLASS — F2 not accepted; F3/F4 remain unauthorised.** This is a bounded F2 observation/temporal correlation return, not a reversion of demonstrated improvements to D016/D120 or a demand to repeat completed work.

## VERIFIED finding F2-R1: later quote changes an earlier trade's classification

Normative authority: accepted M01 brief §5 K08 D015 (`trade > midpoint` / `< midpoint` against **contemporaneous** quote with tie tick test), D016 signed-trade size, D120 signed option quantity/premium; catalogue rows D015/D016/D120; §8.1 exact input-time matching and §11 no-look-ahead.

Reviewer independent public-seam test:
`handoff/m01_completion/review/proof/test_f2_late_quote_sign_20261009.py` with output `F2_REVIEW_LATE_QUOTE_RED_20261009.log`.

Sequence (no worker composition/owner fixture helper): quote midpoint 5 at T0, trade buy price 6 size 2 at T0, sell price 4 size 3 at T+5s. With those inputs, `D015(T0)=+1`, `D015(T+5)=-1`. At T+10s **only** a new bid 2 / ask 4 midpoint-3 quote arrives, with **no new trade**. Public materialisation returns `D015(T+10)=+1`, wrongly relabelling the old price-4 sell using a later quote. `D016(T+10)=None`, `D120(T+10)=None` despite both trades having signed contemporaneous classifications. The event-window sums from admitted data are D016=-1 and D120 signed_contracts=-1 / signed_premium_notional=0 (2*6*100 - 3*4*100). The script's required no-reclassification assertion fails (exit code 1). This is an end-to-end semantic defect, not an isolated numerical test preference.

**Mechanism shown by source:** `_stage1.py` D015 (`_eval_k08`) compares latest raw R120 with latest D011 midpoint at *request* `as_of`; it does not bind each trade to the quote contemporaneous with that trade. The new `_observation_signs` reconstructs the most recent R120 from full D015 ultimate raw lineage, not from a persisted, explicit selected-trade-to-quote association. Re-evaluating the same trade at a later cutoff can produce contradictory classifications; the new correlation then returns `None`. This is materially related to the recurrent selection/lineage class found in earlier Stage-1 reviewer returns. Do not fix this by suppressing conflicting D015 records, preferring the latest answer by arbitrary order, or treating raw and derived identifiers as equal.

## VERIFIED improvements, limited scope
- Independent rerun of submitted F2 public tests and original reviewer witness: `PYTHONPATH=src pytest -q tests/product/derived_signal/test_m01_f2_observation_identity.py handoff/m01_completion/review/proof/test_stage1_signed_flow_public.py` → **12 passed** (`F2_REVIEW_EXISTING_FOCUSED_20261009.log`). This confirms those particular cases, not F2 closure.
- Production `_observation_signs` no longer intersects derived occurrence IDs with raw M00 occurrence IDs; D016/D120 now return expected one-/two-trade fixture sums for supported histories and preserve direct D predecessor references. Proof-before-source ordering is visible in commits `0235f36`, `620c7cf`, `82ebf46` preceding `c2c0f9c`.
- The worker's 672-case non-durability suite and 46-case focused/M00 runs are recorded but **not independently rerun** in this review. Their passing cannot override the new semantic failure. M00 multiprocess PostgreSQL durability was expressly not rerun by worker for this F2 pass.

## Separate unresolved prerequisite F2-U04: D064→D065 event identity

Source `_stage1.py` D065 still joins R284 `occurrence_id` to D064 **derived** `occurrence_id`, which are distinct namespaces and cannot establish the selected scheduled event. D064 has only R289 (no derived dependencies) per normative CSV; current K07 `_score` accepts only nonempty `P_SCORE.score_features` referencing derived dependencies. Thus a D064 public occurrence and subsequent D065 event-association public proof were not established by this candidate. This is a separate *verified source-level implementation barrier*, **not** a reproduced public D065 wrong output and **not** proof the normative brief is absent. Whether the accepted K07 feature schema and R289 value semantics already admit a correct raw dependency feature requires evidence-first determination before implementation. Preserve as **BLOCKED PREREQUISITE**; do not invent a scoring extractor or a cross-namespace join.

D017 raw/raw co-reference test and signed trade tests remain useful evidence; D121/D122, D109/D170 reproof and F4 class census are not part of this return and remain deferred. No inference that unrelated rows are defective.

## Routing / workload limit
Send worker **F2a only** (see `handoff/m01_completion/repair/M01_F2A_TEMPORAL_SIGN_WORKER_HANDOFF_20261009.md`). Worker must commit the authority-derived *failing* public proof first, repair only the per-trade contemporaneous quote/sign identity and downstream retained correlations, run focused checks, and return an exact Git checkpoint for independent review **before** tackling D064/D065. U04 remains explicitly blocked pending separate evidence-based prerequisite treatment. No F3, F4 or Stage 2.

Reviewer has not modified production, normative catalogue, root governance, worker tests or accepted ExecPlan; only added independent review evidence/disposition and review handoff material.
