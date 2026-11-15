# T01 owner-approved historical Ruff policy — integration candidate, not main

**Owner decision:** 15 November 2026. In this conversation the owner expressly agreed to the independently reviewed recommendation: adopt the narrow SHA-bound Ruff policy and prepare one current-main-derived integration candidate, with independent review and a later separate main-merge decision. This does not authorise proof admissions, new product cases, installation of the T01 successor ExecPlan, backend/runtime parity or D145 activation.

## Exact acceptance rule

- Run Ruff **0.15.11** over all `src tests tools` without excluding any subtree.
- Require exactly **51 historical diagnostics**, 38 E501 + 5 I001 + 4 B905 + 4 RUF007, solely on seven immutable, already-admitted product proof/support files.
- Diagnostic identity includes path, code, message, line and column. Sorted canonical digest: `08ae839b0596c31ecb73a4667845f0d19dfe0c4503c52079434dd98e835a2a8f`.
- Preserve each source file SHA, active admission pointer, exact generation SHA, claim and family/support membership. A changed source, generation, pointer, manifest, diagnostic or Ruff version **fails**; zero findings also fails for this specific historical-state baseline.
- This is an owner-adopted **lint-policy exception**; it neither edits physical proof bytes nor weakens the actual product/architecture validators.
- Prior independent bounded review: [15 November report](https://github.com/JayDEmily/nvda_29102026/blob/41558c469e2ff7b5f504b1731b1525c7922da92b/handoff/review/t01_hash_bound_lint_policy_20261115/INDEPENDENT_PR14_REVIEW_20261115.md); prior draft test [Actions 43553729850](https://github.com/JayDEmily/nvda_29102026/actions/runs/43553729850) was passing, **but is not the new candidate's CI**.

## One main-derived integration

From main `a73349834fe4aa1422c194da0492315044b32b98`, ordinary merge PR #14 technical history `831471d69afd092779a6810ee570285182be88a8`, preserving main's first-line owner `AGENTS.md`. Replace draft-only policy references with:
- `config/lint/SHA_BOUND_RUFF_BASELINE.json` — status `OWNER_ADOPTED_PENDING_MAIN_INTEGRATION`, exact SHA-256 `7ae5ed8df7fcf775adb9aa9d6462c4dc1dcf4aafe778a007934abdbf00a307c2`, pinned inside verifier;
- `tools/sha_bound_ruff_gate.py` — deterministic fail-closed candidate verifier;
- `.github/workflows/architecture-kernel.yml` — invokes that verifier while keeping full-history checkout, locked environment install, unchanged architecture promotion and diff check;
- `Makefile` `lint` — invokes the exact same verifier through `$(PYTHON)` in a configured interpreter environment.

The change to `Makefile` is an explicit additional path: the old `make lint` rejected all 51 despite the proposed CI gate passing. No product files or proof admissions are changed.

## Separate governance work

The independently reviewed T01 39-leaf successor, full original 35-obligation ledger, proposed AGENTS, and test override are copied into `handoff/planning/t01_owner_lint_integration_20261115/` with verified source hashes. The proposed AGENTS adds today's first-line continuous-execution owner instruction. They remain **reviewable proposals, not installed root authority**.

A separate dependency-window proposal maps 34 not-yet-released tests into G1/G2/G3/G4 windows, preserves D145 paused and allocates no new cases. It does **not** alter the currently effective L32 schedule; a coordinated owner-approved plan/override/ledger amendment and independent Tester remain necessary.

## Verification/acceptance limits

Fresh GitHub Actions on the **final new commit** and a separately independent cumulative review are required before owner-directed main promotion. CI architecture results are not new physical product tests or CPython/SQLite equivalence evidence. Historical proof contract CPython 3.12.14/SQLite 3.53.1 versus inspected managed Python 3.13.5/SQLite 3.49.1 still requires future compatibility qualification. D145 stays PAUSED.
