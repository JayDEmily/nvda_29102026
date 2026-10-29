# NVDA V2 G01 — controlled-input proof rerun / promotion boundary

**Date:** 14 October 2026 (Australia/Melbourne)
**Branch:** `work/v2-g01-contract-correct-controlled-proof-20261014`
**Source baseline:** `08ec7686338d4bb01bb114269963db001dc94451`
**Scope:** preserve the owner's contract-correct validation direction, rerun G01 controlled-input public-path witnesses, record blockers. No production/kernel, catalogue, schema, M00, active ExecPlan or existing test expectations have been modified.

## Executed evidence

- Exact command: `TEST_COMMAND.txt`.
- Exact combined standard output/error: `TEST_RUN.txt`.
- Process status: `TEST_EXIT_STATUS.txt` (= `1`, failed).
- Interpreter and test tools: `TEST_ENVIRONMENT.txt`.
- Selected three G01 public-path adversarial witnesses plus existing focused D025 and skew proofs.

**Observed: 34 passed, 3 failed.** The three failures are:

1. `D025`: correct accepted `R039=High=120`, `R040=Low=80`, `R037=Last=90` expects `0.25`, public path produced `0.75`.
2. `D099`: lawful native `R015=C/P`, plus corresponding R111/R112 IV/delta and contract identity, expects `10` volatility points, public path returned `None`.
3. `D100`: lawful native `R015=C/P` with 10Δ wings expects `30` volatility points, public path returned `None`.

These are failures using **controlled inputs**. They do not depend on a live IBKR feed. The existing green fixtures for skew and grouped flow may exercise wrong R015 semantics, so their green result is not evidence of contract correctness.

## Source-contract / authority finding requiring separate resolution

`handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv` has `D120` direct raw inputs `R120;R121;R126;R127;R015`, whereas accepted equation §5 says signed premium notional uses the **contract multiplier**. Original `Raw Signals` workbook assigns **R015 = option right** and **R016 = multiplier**; implementation `_stage1.py` currently parses `R015` as multiplier. This specific D120 positive-validation target is **AUTHORITY/SOURCE-CONTRACT BLOCKED** until the source binding is lawfully amended or a valid metadata supply is established by accepted authority. D120 was **not** exercised in this rerun; this observation comes from static source inspection, not an executed failing test.

## Why no production changes or `main` promotion

1. The accepted root `EXEC_PLAN.md` is still G01 and explicitly excludes production repairs under this gate. G01-L4 independent review and definition-admission decisions are outstanding. Source/contract repairs require an accepted bounded implementation-ready brief/plan under `docs/architecture/IMPLEMENTATION_AUTHORITY_INGRESS.md`.
2. The focused G01 witness run remains **RED** (3 failed); making a `main` claim would be false.
3. The supplied local Git archive has no `refs/heads/main` or `refs/remotes/origin/main`. Its configured `origin` points to missing `/mnt/data/nvda_f4_worker_isolated`.
4. A connected GitHub repository, `JayDEmily/nvda23e0_20260821_235327_architecture_kernel_reset`, has a `main` at `892a6c042f19d19d84a3d1fb2c639033789f9bc1` (observed via connected GitHub API). That repository did not recognise the local G01 commit `08ec7686338d4bb01bb114269963db001dc94451`; the local repository did not contain GitHub's current main commit. This does **not** establish common ancestry, current project-main identity or a safe merge target. Do not invent `main`, force-push or join histories without explicit verified transition authority.

**Disposition:** PROOF/EVIDENCE COMMITTED; CONTRACT-CORRECT IMPLEMENTATION NOT DEMONSTRATED; G01 REMAINS PARTIAL/BLOCKED; NO MAIN PROMOTION. Full Git branch is the recoverable checkpoint.
