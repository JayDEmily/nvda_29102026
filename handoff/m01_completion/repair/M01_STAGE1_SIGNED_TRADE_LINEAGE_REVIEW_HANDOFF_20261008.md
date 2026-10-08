# Stage-1 independent reviewer return — signed-trade lineage class

**Decision:** `REPAIR / RECURRENT_CLASS / RETURN_TO_WORKER_STAGE1`.

**Reviewed source:** `work/m01-completion` at worker `HEAD 514cf90e4c49a3dc72d318796549a6da9dc38cc7`, tree `be8959b949cd094b76276cc66779535c9611f8f8`. The new reviewer files are evidence and handoff only; the reviewed production source is unchanged.

## First failed semantic invariant (verified)

Accepted brief K08 requires `D016 = Σ trade_sign_i*trade_size_i` and D120 to return both `Σ sign*size` and `Σ sign*size*trade_price*multiplier`, aligned to the correct trade observation. The accepted catalogue binds both to the D015 predecessor.

The independently created public `create_owner(...).materialise(...)` fixture supplies one exact NVDA C100 option contract, a quote bid 4/ask 6, one trade at 6 of size 2 with multiplier 100, all required raw R bindings, explicit `P_BASIC/P_RULE` versions, one-minute window, exact selection, units, as-of/cutoff and projection mapping. D011 materialises 5 and D015 materialises sign +1.

**Expected:** D016=2; D120 signed_contracts=2, signed_premium_notional=1200. **Observed:** D016=0; D120=(signed_contracts=0,signed_premium_notional=0), both stored as occurrences with lineage and predecessor IDs.

The production owner represents a D015 derived input with its hashed *D015 occurrence* ID (`api.py`, `_occurrence_kernel_value`). Stage-1 D016 and D120 use D015's derived occurrence ID as the dictionary key but query it with the *M00 raw trade observation* ID (`_stage1.py`, `_eval_k08`). The two namespaces are not equal. Consequently the sign is silently discarded and an unjustified zero is persisted; this is not absence due to an incomplete fixture.

## Reviewer reproducer and evidence

- `handoff/m01_completion/review/proof/stage1_signed_flow_public_fixture.py` — direct public-seam fixture, no worker helper.
- `handoff/m01_completion/review/proof/test_stage1_signed_flow_public.py` — two deliberately failing authoritative result assertions.
- `handoff/m01_completion/review/proof/stage1_signed_flow_public_fail_20261008.log` — pinned Python 3.13.5 / pytest 9.0.3 run, **2 failed**.
- `handoff/m01_completion/review/proof/stage1_existing_regression_194_pass_20261008.log` — existing derived-signal product + architecture + bootstrap, **194 passed**, which does not establish the failed semantic proposition.

Reproduce in the preserved pinned Python environment:

```sh
PYTHONPATH=.:src:handoff/m01_completion/review/proof python -m pytest -q handoff/m01_completion/review/proof/test_stage1_signed_flow_public.py
```

Reviewer also ran Ruff, mypy and structural architecture validator successfully. PostgreSQL boundary suites were **not rerun independently**; the worker's reported PostgreSQL evidence remains available but cannot resolve the failed signed-flow invariant.

## Classification and required worker boundary

**RECURRENT_CLASS** because the previous M01 reviews repeatedly concerned unproven or incompatible lineage across R/D graph edges. This is a distinct concrete failure mode: a derived-occurrence identity is confused with its underlying raw-observation identity. Do not infer that fixing D016 and D120 arithmetic locally closes the wider graph-alignment class.

The worker will first author public-seam proofs of correct D015→D016 and D015→D120 per-trade correlation, including positive buy/sell arithmetic, different trade observations/contracts, missing classification, deterministic retries and exact raw/D lineage. Then repair only the proven Stage-1 mechanism and independently inspect sibling raw/derived ID joins for equivalent errors. Prove D121/D122 multi-contract grouping through their normative D120/D091 and D120/D085 edges as part of Stage-1 class closure; the present review **did not independently execute those dependent aggregate graphs** once their D120 prerequisite failed.

Do not change M00 ownership, normative CSV/brief, governing files, package version, or previously admitted D109/D170 behaviour. Preserve proof-before-production Git order. Freeze the next exact Stage-1 candidate for another independent review. Stage 2 remains unauthorised.
