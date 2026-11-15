# NVIDIA T01 — independent cumulative integration review of draft PR #16

**Date:** 15 November 2026, Melbourne. **Verdict: `ACCEPT_INTEGRATION_CANDIDATE`** for the pinned, main-derived lint-policy and architecture integration **only**. No main merge, proof admission, successor-governance installation, runtime-equivalence acceptance or D145 release is granted.

- Repository: `JayDEmily/nvda_29102026`.
- Exact candidate/PR #16 head: `ef0f6876f2b5673a91946eeaaaac964b40e1efe7`.
- Exact main baseline, confirmed both as `origin/main` and remote `refs/heads/main`: `a73349834fe4aa1422c194da0492315044b32b98`.
- Candidate Git tree: `bad45045e04604cdcb0e7ce8d3d62820558cacb4`.
- Predecessor technical PR #14: `831471d69afd092779a6810ee570285182be88a8`; two-parent reconciliation `35f01b0dbcd4fdd5703b00afa582bac134f78985`; implementation `c8d4346a9f56a1e38aa3bc48e4f4e891ceb2551d`, all verified as ancestors of the candidate.
- Governing review commission: [pinned independent request](https://github.com/JayDEmily/nvda_29102026/blob/ef0f6876f2b5673a91946eeaaaac964b40e1efe7/handoff/review/t01_owner_lint_integration_20261115/INDEPENDENT_REVIEW_REQUEST_20261115.md). Prior, independent PR #14 design review: [`41558c469...`](https://github.com/JayDEmily/nvda_29102026/blob/41558c469e2ff7b5f504b1731b1525c7922da92b/handoff/review/t01_hash_bound_lint_policy_20261115/INDEPENDENT_PR14_REVIEW_20261115.md).

## 1. Governance and proof boundaries — verified

Read frozen `GUARDRAILS.md`, current root `AGENTS.md`, `EXEC_PLAN.md`, `tests/AGENTS.override.md` and normative `docs/architecture/TEST_AND_PROMOTION_KERNEL.md` (AK-PROOF-001/002). A direct Git diff from exact main to exact candidate over `GUARDRAILS.md`, `AGENTS.md`, `EXEC_PLAN.md`, `tests/AGENTS.override.md`, all `config/product_proof`, and seven product-proof sources returned **no changed paths**. The main owner continuous-execution first line remains intact (root AGENTS Git blob `725f520eeb45f0febabf3ae813ce6bb09c54ee44`). No original proof bytes, active pointer descriptors, generation files, original validator implementation or active root programme were replaced.

The 14-commit cumulative candidate is a normal history-preserving merger of main and the older PR #14 technical lineage, not a wholesale tree replacement. Historical commits remain reachable. The current main ref still equals the specified baseline; PR #14 remains at its reviewed exact head, draft/open/unmerged; documentary PR #3 remains at `3d8f1fae68cdba41c7a1e96df6cb59d1ee35afd9`, draft/open/unmerged. No evidence supports treating PR #3 as an installed root plan. Future 66-ref/non-Git-asset receiver closure is a separate T01 execution/transfer gate, **not established by this integration review**.

## 2. Complete cumulative 36-path classification

Compared exact main versus candidate using both GitHub's paginated PR file inventory and local `git diff --name-status`: **36 paths, 3,263 additions and 29 deletions**, agreeing with PR metadata. Classes and all paths:

| Class | Count | Paths |
|---|---:|---|
| CI/runtime/tool entrypoints | 5 | `.github/workflows/architecture-kernel.yml`, `.python-version`, `Makefile`, `pyproject.toml`, `uv.lock` |
| Adopted policy/verifier | 3 | `config/lint/SHA_BOUND_RUFF_BASELINE.json`, `tools/sha_bound_ruff_gate.py`, `docs/ci/T01_SHA_BOUND_RUFF_POLICY_20261115.md` |
| Newly vendored CPython 3.13 wheels | 4 | `vendor/wheels/librt-0.16.0-cp313-cp313-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl`; `vendor/wheels/mypy-1.20.1-cp313-cp313-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl`; `vendor/wheels/psycopg_binary-3.3.4-cp313-cp313-manylinux2014_x86_64.manylinux_2_17_x86_64.whl`; `vendor/wheels/pyyaml-6.0.3-cp313-cp313-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl` |
| Product-code/proof-adjacent formatting | 2 | `src/nvda_desk/derived_signal_calculation_truth/_financial_policy.py`; `tests/product/derived_signal/test_m01_stage1_semantics.py` |
| Architecture tests/historical fixture | 5 | `tests/architecture/test_identifier_taxonomy.py`; `tests/architecture/test_implementation_authority_ingress.py`; `tests/architecture/test_proof_control.py`; `tests/architecture/test_registry_schema.py`; `tests/architecture/fixtures/pre_admission_20261018_inventory.json` |
| Retained historical handoff material | 6 | `handoff/planning/t01_immutable_ruff_20261114/PROPOSAL.md`; `handoff/review/t01_ci_proof_preserving_20261114/INDEPENDENT_REVIEW_REQUEST.md`; `handoff/review/t01_fixture_state_split_20261114/WORKER_EVIDENCE.md`; `handoff/review/t01_fixture_state_split_20261114/architecture_fixture_split_61_cases_pytest.log`; `handoff/review/t01_hash_bound_lint_ci_20261114/INDEPENDENT_REVIEW_REQUEST.md`; `handoff/review/t01_pre_admission_fixture_20261114/REVIEW_REQUEST.md` |
| Uninstalled proposed T01 governance | 7 | `handoff/planning/t01_owner_lint_integration_20261115/GOVERNANCE_RECONCILIATION_20261115.md`; `GOVERNANCE_SOURCE_RECONCILIATION.json`; `PROPOSED_AGENTS.md`; `PROPOSED_DEPENDENCY_WINDOW_LEDGER_DELTA.json`; `PROPOSED_EXEC_PLAN.md`; `PROPOSED_TESTS_AGENTS.override.md`; `PROPOSED_TEST_EVIDENCE_LEDGER.json` (all six unqualified names in this row have the same preceding directory) |
| New integration reviewer handover/worker receipts | 4 | `handoff/review/t01_owner_lint_integration_20261115/INDEPENDENT_REVIEW_REQUEST_20261115.md`; `OWNER_POLICY_ADVERSARIAL_RESULT.json`; `OWNER_POLICY_ADVERSARIAL_TEST.py`; `WORKER_INTEGRATION_EVIDENCE_20261115.md` (same directory) |

**Predecessor conservation:** Relative to current main, PR #14 has 24 differences including the obsolete version of `AGENTS.md`; its **23 non-AGENTS technical paths** comprise 20 retained byte-identically in this candidate, one intentionally revised workflow and two historical `PROPOSED_*` lint files deliberately replaced by the owner-adopted `SHA_BOUND_*` files. No main-tracked path is deleted in the final candidate diff, and the predecessor lint proposal survives in Git ancestry, not active tree. This is normal `DO_NOT_CARRY_FORWARD` treatment, not Git history destruction.

**Fixture and AST assessment:** The independently inspected 18 October historical source commit `86b23f1ef5bf4a1510e93333fa4b2cfc869c3b71` has exactly the inventory's 101 `tests/product` Python paths, including 93 test files. `test_proof_control.py` uses historical membership pruning only in a disposable candidate, and explicitly separates current M00 Brief2 controls, retaining its positive baseline and falsifiers. M03 is already present in current module allocation, justifying M04 next-ID test expectations. Both formatting files have equal original/candidate Python ASTs (attributes excluded). These are fixture corrections, not new product-proof admissions.

## 3. SHA-bound lint implementation and independent adversarial evidence

At `tools/sha_bound_ruff_gate.py`, the verifier hashes the **whole immutable policy manifest**, checks its status `OWNER_ADOPTED_PENDING_MAIN_INTEGRATION`, requires precisely **seven canonically sorted proof paths**, Ruff version `ruff 0.15.11` and full `ruff check --output-format=json src tests tools`. It individually verifies product source SHA-256, active selected generation path and recorded SHA, generation bytes and claim/family/support membership; it canonicalises **all** diagnostics, including message, code, path, row, column. Unexpected findings, missing findings, changed source/generation/selected pointer, changed manifest or Ruff version cause rejection. **It checks the selected generation fields of admission descriptors, not a separate byte hash of each whole admission JSON**; this review independently compared the complete admission files against main.

- Manifest byte SHA-256 `7ae5ed8df7fcf775adb9aa9d6462c4dc1dcf4aafe778a007934abdbf00a307c2` (matches verifier constant).
- Exactly **51** existing historical diagnostics: `38 E501 + 5 I001 + 4 B905 + 4 RUF007`, no newly accepted findings. Canonical set digest `08ae839b0596c31ecb73a4667845f0d19dfe0c4503c52079434dd98e835a2a8f`.
- All seven source SHA-256, admission descriptor *byte equality to main*, selected generation pointers, generation byte hashes, claims and membership independently checked against exact main and the committed manifest.

**Independently reproduced (fresh, unrelated temporary local clone; no live candidate edit):**
1. Exact candidate checkout; Python `3.13.5` and Ruff `0.15.11`.
2. `python tools/sha_bound_ruff_gate.py`: exit **0**, `SHA_BOUND_RUFF_EXACT_MATCH: 51 ... 08ae839b...`.
3. `make lint PYTHON=<pinned-3.13.5-python>`: exit **0**, identical diagnostic count/digest and same verifier.
4. Append a syntactically valid **new F821 undefined-name canary** to clean `tools/validate_architecture.py` in the disposable clone only; direct gate exits **1** and prints `SHA_BOUND_RUFF_REJECTED: Ruff findings changed by path`, including that added path.
5. Restore the exact original test file; the verifier returns exit **0** with identical output; disposable `git status --porcelain` empty; temporary clone auto-removed.

The Worker's recorded five different negative mutations (`OWNER_POLICY_ADVERSARIAL_RESULT.json`) were inspected as *worker evidence*, **not** claimed as five newly independently rerun cases. The independent F821 negative directly establishes rejection of a previously clean source. This resolves prior PR #14 reviewer F09's demonstrated `Makefile`/Actions acceptance divergence. No product test was executed.

Local `uv` CLI was not on the Ubuntu shell PATH (the attempted isolated literal `uv --version` returned FileNotFoundError), so this reviewer **did not independently repeat `uv sync` locally**. Instead, the *exact workflow's* locked install and `uv run python tools/sha_bound_ruff_gate.py` are verified from primary successful GitHub Actions logs, on the same proved tree. This limitation is not hidden or relabelled as local uv testing.

## 4. Wheel archives, lock, CI and runtime boundaries

Four new CPython-3.13-specific wheel files were independently inspected: ZIP CRC passes; every populated internal wheel `RECORD` SHA-256 entry matches; wheel tags match `cp313` and Linux x86_64; their physical SHA-256 digests are in the sibling evidence JSON. `uv.lock` pins version/source `vendor/wheels` and wheel path, but does **not** contain per-wheel content hashes; the exact Git tree fixes their content for this candidate. Publisher-origin attestation was not independently obtained. `.python-version` and `pyproject.toml` require exact Python `3.13.5`; lock also declares `==3.13.5`.

Primary [Actions run 43668257053](https://github.com/JayDEmily/nvda_29102026/actions/runs/43668257053), [job 132672363788](https://github.com/JayDEmily/nvda_29102026/actions/runs/43668257053/job/132672363788): `completed / success`, **all ten steps success**, no failed step. Full-history `actions/checkout@v4` with `fetch-depth: 0`, `setup-uv@v6`, `uv sync --locked --extra dev`, SHA-bound lint, unchanged `run_promotion_gate.py --set architecture_kernel` and `git diff --check` passed. Primary log prints **221 passed in 1,726.81 seconds**, 11 admitted architecture/bootstrap families and exact 51-diagnostic digest. A Node-20 deprecation warning was emitted by Actions, not a job failure.

**Critical CI identity distinction:** checkout targeted `refs/remotes/pull/16/merge`, synthetic merge commit `146304dd5d1279946937132fa6ca01ffd50433d3`, **not literally the PR head commit**. Independently fetched this merge ref in a disposable clone and proved that its Git tree is **identical** to exact candidate `ef0f...`: both `bad45045e04604cdcb0e7ce8d3d62820558cacb4`; file diff empty. CI is therefore valid evidence for the candidate's exact file content and merge-on-main integration, not a misleading claim that Actions checked out the head commit object itself.

Architecture/bootstrap CI is not product proof. Historical CPython 3.12.14/SQLite 3.53.1 recorded proof conditions are not qualified as equivalent to CPython 3.13.5/this host's SQLite. No PostgreSQL/SQLite install or backend validation, product-case run, physical acceptance or D145 action occurred.

## 5. Governance reconciliation and proposed test windows

Independently fetched each original proposed file directly from PR #3 source commit, checked all **four source/output SHA-256 pairs** in `GOVERNANCE_SOURCE_RECONCILIATION.json`, and compared content: proposed ExecPlan, test override and 35-obligation ledger **byte-identical** to their PR #3 originals; proposed AGENTS is exactly the source with the newer main first-line owner directive prepended. Active root files are unchanged.

The original `LEAF_REGISTER.json` at PR #3's source has **39 unique named leaves**: 38 `PROPOSED_NOT_ATTEMPTED` and paused L31. Exactly **35 unique original proof obligations** are conserved; their execution ledger contains **34 still scheduled at L32 with 0 authorised cases** and a single D145 entry **L31 / BLOCKED / no tests**. The new window proposal maps every one of the 35 IDs once, matches each owner leaf's nominal gate and reports **G1 11 / G2 12 / G3 4 / G4 7 / D145 1 paused**. All 34 non-D145 owning leaves are still `PROPOSED_NOT_ATTEMPTED`. There is **no test release or case budget**.

**Semantic review:** The windows are mechanically accurate *gate labels*, but are **not executable gates** as written. The G1 history support profiles must precede the D079–D081 joint-fit coefficients and D078 residual; G2 source option expiry/calendar/IV support must precede D085/D086 and their option-dependent children; G3 option trade/sign evidence and previously accepted D091/D085 must precede D120/D121/D122; G4 D102 quality/surface must precede D111 density and D112/D113 tails, while D141 source attribution and D151 basket denominators need independent contracts. Exact source profile, accepted meaning, parent evidence, finite case allocation, independently designated Tester and an owner-adopted **coordinated** ExecPlan/override/ledger amendment are still required. No 11/12/4/7 window permits automatic testing or forward admission; parent `IMPLEMENTED_UNTESTED` is not independently accepted proof. Current final-only L32 remains the uninstalled successor ledger's schedule, **not** active root authority.

**GOV-DOC-01 — ISOLATED, prospective documentary relocation mismatch (not a blocking active lint/CI defect):** `handoff/planning/t01_owner_lint_integration_20261115/PROPOSED_TESTS_AGENTS.override.md:3` instructs future readers to load proposed AGENTS and ExecPlan at `handoff/planning/t01_main_reconciliation_20261112/`, but those two paths do **not exist in the exact PR #16 tree**; the reviewed copies are now under `handoff/planning/t01_owner_lint_integration_20261115/`. This is an inherited pointer from the byte-identical PR #3 source, not evidence of installed governance. **Before any future installation**, amend the proposed test override's references, update source/output reconciliation digests and independently review that new package. Do not silently rewrite the source copy or install it through this review.

No source-policy/clock/true-event decision, test-budget or checkpoint-method change is admitted by the proposed paperwork. D145 remains PAUSED.

## 6. Verdict and exact remaining decisions

**ACCEPT_INTEGRATION_CANDIDATE** at `ef0f6876f2b5673a91946eeaaaac964b40e1efe7` for the narrowly adopted, SHA-bound 51-diagnostic lint policy, reconciled Makefile/Actions implementation, conserved predecessor technical/fixture code and successful exact-tree architecture CI. **No verified blocking issue in the active candidate integration was found.** This is a scope-specific review verdict, not a claim of product correctness or programme acceptance.

**Not accepted by this verdict:** the uninstalled 39-leaf successor programme; the non-adopted 11/12/4/7 testing-window proposal; any product proof, runtime/backend equivalence, D145 reactivation or new transfer-method approval. GOV-DOC-01 and source/parent readiness must be resolved before governance installation.

**Still reserved to the owner:** (1) an explicit main-merge decision for exact candidate SHA `ef0f6876...` after this review; (2) a *separate* decision to adopt a corrected exact T01 governance/Tester/checkpoint package; (3) any later lawful case admissions, provider/clock policy and runtime qualifications. PR #16 remains draft/unmerged. No candidate edits, merge, product test, proof admission or live model API job were performed.

Primary links: [PR #16](https://github.com/JayDEmily/nvda_29102026/pull/16), [exact candidate](https://github.com/JayDEmily/nvda_29102026/commit/ef0f6876f2b5673a91946eeaaaac964b40e1efe7), [Actions evidence](https://github.com/JayDEmily/nvda_29102026/actions/runs/43668257053), [lint policy](https://github.com/JayDEmily/nvda_29102026/blob/ef0f6876f2b5673a91946eeaaaac964b40e1efe7/docs/ci/T01_SHA_BOUND_RUFF_POLICY_20261115.md), [uninstalled governance package](https://github.com/JayDEmily/nvda_29102026/tree/ef0f6876f2b5673a91946eeaaaac964b40e1efe7/handoff/planning/t01_owner_lint_integration_20261115).

See sibling `INDEPENDENT_EVIDENCE.json` for machine-readable pinned facts, wheel SHA-256 digests and command outcomes.
