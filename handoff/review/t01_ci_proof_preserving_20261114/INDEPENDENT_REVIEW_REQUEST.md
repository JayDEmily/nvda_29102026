# Independent review request — proof-preserving T01 CI correction

**Date:** 14 November 2026, Melbourne. **Status:** WORKER CANDIDATE, NOT ACCEPTED OR PROMOTED.
Repository: `JayDEmily/nvda_29102026`.
Branch: `work/t01-ci-proof-preserving-20261114`.
**Review exact tip after the document commit** and compare to the fixed base `8f236660e9b5982c242b6f114882f045cd1f291e` (Python 3.13.5 + uv offline lock candidate).
**Prior rejected Ruff branch:** `8674d1e6fb81cefe6cd66ec45808348bb4f2e793` (PR #7). Do not merge it.
**Frozen authority:** `GUARDRAILS.md` Git blob `54a4407609941f63f6b902076688ff102a3d5ba2` retained byte-identically.

## Bounded implementation submitted

1. Exact full-history checkout in `.github/workflows/architecture-kernel.yml`, `actions/checkout@v4` with `fetch-depth: 0`. This is required by `tools/product_proof_claims.py::_admission_history` which walks retained Git pointer/generation transitions. YAML parse of the first checkout step passed. No test/authority/check steps removed or reordered.
2. Three architecture test files `tests/architecture/test_identifier_taxonomy.py`, `test_implementation_authority_ingress.py`, and `test_registry_schema.py` now assert the correct already-admitted M03 allocation and next unused M04/M05 IDs. Primary authority: [D040 independent acceptance](https://github.com/JayDEmily/nvda_29102026/blob/171a9149dea53f44a1bd1fec6a1d7971c3c1a9f3/handoff/configured_market_conditions/d040_execution/final_review.md), `config/architecture/modules.yaml` and `implementation_allocations.yaml`. Original test expectations were written before the 23–24 October 2026 admission. Retired-ID and nonmutation checks remain operative.
3. Two non-generation-bound formatting changes only: `src/nvda_desk/derived_signal_calculation_truth/_financial_policy.py` and `tests/product/derived_signal/test_m01_stage1_semantics.py`. For both, before/after Python AST dumps match exactly. The latter is a comment-only wrap.
4. **Seven SHA-bound proof test/support files are left completely unchanged**, unlike PR #7. They match the original base's Git blobs and existing SHA-256 generation records. No generation/admission/claim/contract file was changed.

## Direct author verification (not independent acceptance)

- Clean isolated WSL checkout + original wheelhouse and lockfile: `uv 0.10.0 sync --locked --extra dev --offline` on CPython **3.13.5** -> **PASS**, 15 resolved and 14 installed.
- `pytest -q` on the three changed `tests/architecture/` files -> **37 passed** in **1.36s**. These are architecture tests only, **not** admitted physical product proof cases.
- Ruff 0.15.11 on the five changed Python paths -> **PASS**. `git diff --check` -> **PASS**.
- A read-only call to `load_product_proof_claim` for all **seven** affected product claims in the full-history worktree returned **`READY_FOR_PROOF`**. This is *claim-readiness metadata*, **not** semantic proof acceptance. No physical product test or product-proof gate was executed.
- Whole-tree Ruff `ruff check --output-format=json src tests tools` still gives exactly **51 diagnostics**: 38 E501, five I001, four B905 and four RUF007. All 51 occur *exclusively in the seven immutable SHA-pinned proof files*; no other files have Ruff diagnostics. Full CI on this exact candidate has **NOT BEEN RUN**, and CI clearance is not established.
- Original GitHub Actions witness [run 43205348398](https://github.com/JayDEmily/nvda_29102026/actions/runs/43205348398) had 132 architecture failures/89 passes on a different candidate, before these changes. It is not a validation of this branch.

## Material unresolved authority/technical questions — do not bypass

**F1: Immutable proof bytes vs whole-tree Ruff.** Exact generation hashes deliberately bind the seven original file bytes. Formatting those files made earlier PR #7's cryptographic admission invalid; leaving them intact leaves 51 whole-tree Ruff findings. An independent reviewer must determine an authority-compliant resolution: a properly reviewed/admitted *new* generation for changed files, or an explicitly accepted alternative lint scope that **does not weaken product validators**. Do not silently reseal original generations or insert lint suppressions as a shortcut. No new generation or changed lint rule is part of this candidate.

**F2: Pre-admission architecture fixture.** `tests/architecture/test_proof_control.py::_copy_candidate` creates an M02-absent universe, but newer actual M03 depends on M02 and current foundation binding targets `modify M02`. A preliminary transitive-graph pruning experiment failed a targeted test with `ImplementationAuthorityError: modify target M02 is not registered`; the entire trial edit was reverted before commit. Correct historical fixture semantics require a separate audited fixture/authority contract. Also the old hardcoded physical-path count 93 conflicts with 198 observed in original CI; do not simply change numbers or omit paths.

**F3: Independent review and CI.** No independent reviewer has judged this new exact candidate. No required full architecture CI run can be reported PASS. Main integration, root AGENTS/ExecPlan adoption, production proofs and D145 activation are not authorised by these worker-level corrections.

## Reviewer request

Read `GUARDRAILS.md`, applicable current `AGENTS.md`, test override and active `EXEC_PLAN.md` in full. Inspect the exact base/head diff, all seven generation records and historical D040 acceptance; independently verify unchanged proof-bound bytes, source AST equivalence, the 37-test scope, full-history checkout, and the 51-diagnostic residual set. Classify any finding under the recurrence rule. Return a pinned **ACCEPT_BOUNDED_CORRECTIONS / RETURN / PARTIAL / BLOCKED** decision, clearly separating validated parts from unresolved proof-admission and fixture questions. No product test execution, proof-admission mutations, governance-root edits or main merge under this request.

This document does not grant a new lint exception, case allocation, test rerun or programme acceptance.
