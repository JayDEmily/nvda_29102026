# T01 SHA-bound lint — owner-adopted integration worker evidence

**Prepared:** 15 November 2026, Australia/Melbourne. **Author's result:** CANDIDATE_PREPARED, INDEPENDENT_REVIEW_AND_FINAL_CI_PENDING. Independent reviewer must reach own judgement and inspect primary evidence.

## Authority and exact lineage

Owner approved the narrowly defined SHA-bound lint policy and the preparation of a current-main-derived *integration candidate* in the 15 November conversation. Owner did **not** approve automatic main merge, new source/proof generation, final-only independent product-test schedule change, installed T01 successor plan or D145 release.

Source current main `a73349834fe4aa1422c194da0492315044b32b98`; source previously reviewed draft PR #14 `831471d69afd092779a6810ee570285182be88a8`; no-force merge `35f01b0dbcd4fdd5703b00afa582bac134f78985`; subsequent policy/governance implementation `c8d4346a9f56a1e38aa3bc48e4f4e891ceb2551d`. Extra reviewer handover-only files do not modify the policy proposition.

Current main's `AGENTS.md` owner continuous-execution first line is preserved. `GUARDRAILS.md`, active root `EXEC_PLAN.md`, `tests/AGENTS.override.md`, and `config/product_proof` source/generation/admission tree are **byte-identical to current main**: verified by an explicit `git diff --exit-code origin/main HEAD -- AGENTS.md EXEC_PLAN.md GUARDRAILS.md tests/AGENTS.override.md config/product_proof`. All seven bound product test/support files also remain unchanged. Source PR #14 23-path historical technical delta retained; extra integration changes include Makefile, neutral naming/adoption labels, new policy document and documentary T01 successor proposal.

## Local commands and results (not full new CI)

- Pinned CPython `3.13.5` and Ruff `0.15.11` used via existing managed `/home/jds/nvda_uv3135_20261112/.venv/bin` without installing a new runtime.
- `PATH=/home/jds/nvda_uv3135_20261112/.venv/bin:/usr/bin:/bin PYTHONDONTWRITEBYTECODE=1 .../.venv/bin/python tools/sha_bound_ruff_gate.py` — **exit 0**; `SHA_BOUND_RUFF_EXACT_MATCH: 51 immutable historical diagnostics; 08ae839b...`.
- `PATH=/home/jds/nvda_uv3135_20261112/.venv/bin:/usr/bin:/bin PYTHONDONTWRITEBYTECODE=1 make lint` — **exit 0**, exactly the same verifier and digest; prior F09 resolved at the candidate.
- `ruff check tools/sha_bound_ruff_gate.py` — **all checks passed**. An initially introduced 111-character message line was itself detected by the adopted whole-tree Ruff gate, then split without changing its message. Final local gate is green.
- Disposable HEAD `c8d4346a` at `/home/jds/nvda_t01_owner_policy_falsification_20261115`: the adapted independent review's CLI negative-test harness independently applied/restored five mutations: changed admitted source bytes; changed active admission pointer; changed current generation JSON bytes; changed policy manifest bytes; introduced a new F821 in a formerly clean source. All five were rejected with exact expected errors; baseline passed before and after. `OWNER_POLICY_ADVERSARIAL_TEST.py` and `OWNER_POLICY_ADVERSARIAL_RESULT.json` hold reproducible inputs and outputs. Disposable worktree had empty porcelain status.
- Earlier PR #14 [Actions 43553729850](https://github.com/JayDEmily/nvda_29102026/actions/runs/43553729850) verified its own predecessor draft: 221 architecture tests passed. This record is **not a new passing Actions run** for the owner-adopted candidate.

## Documentary T01 proposal only

Source PR #3 (`3d8f1fae...`) originally independently accepted `ACCEPT_DOCUMENTARY_DELTA`; the source successor is still not installed. This branch copies complete original proposed AGENTS/ExecPlan/test override/ledger by SHA, except exact current owner AGENTS first-line added to its proposal. Original `35` proof entries remain 34 L32/single paused D145 L31; no test cases allocated or released. Separate mapped dependency-focused G1/G2/G3/G4 windows are **unadopted proposals**, require coordinated owner approval and independent Tester preconditions. Do not treat this document as acceptance of a replacement active root plan.

## Outstanding before main

- Full GitHub Actions (`uv sync --locked --extra dev`, SHA-bound lint, existing `architecture_kernel` promotion, `git diff --check`) on the exact **final new PR head**.
- Independent review of all cumulative technical/governance paths, renamed policy/manifest hash, Makefile/Actions parity and negative refusal.
- Separate final owner decision for **main merge**, separately for eventual 39-leaf successor root installation, any earlier Tester schedule and selected runtime / SQLite profile qualification.
- Original checkpoint/restoration scope (historical 66+ refs, non-Git assets) and full separate Tester execution remain future gates.
- No proof aggregate, live API endpoint, market-data call, PostgreSQL action or D145 activation performed here.

**Status:** implementation at `c8d4346a` locally committed; final published review-head identity and CI must be verified separately. No claim of independent acceptance is made by this worker.
