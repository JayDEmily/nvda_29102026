# T01 CI — historical pre-admission fixture repair (worker submission)

Date: 14 November 2026, Melbourne.
Status: **WORKER CANDIDATE / INDEPENDENT REVIEW PENDING**. No CI, product proof or main promotion acceptance.
Repository: `JayDEmily/nvda_29102026`.
Branch: `work/t01-pre-admission-fixture-20261114`.
Fixed base: `85f8c5fc96bde8eac86326d9f7b60f47893aad73` — the clean proof-preserving CI review candidate.

## Problem established from original source, not a guessed threshold

`tests/architecture/test_proof_control.py::_copy_candidate` was introduced at commit `86b23f1ef5bf4a1510e93333fa4b2cfc869c3b71` (18 October 2026). Its stated purpose is to build a **disposable pre-admission control universe**; `test_sqlite_current_and_historical_paths_partition_exactly` explicitly expected **93** physical product `test_*.py` files at that time. Original `git ls-tree -r` verifies exactly 93 paths and 101 Python files under `tests/product`, and only six files under `config/product_proof`.

Current pinned branch `85f8c5f` contains **216** physical product test files: the original 93 plus 123 later files. Its `config/product_proof` tree contains 391 files, i.e. 385 additional relative to the original six. The fixture copied all present files but manually removed only optional D012–D020 roots. This left later independently admitted proof claims and physical paths in what was asserted to be the 18 October pre-admission universe; a later M03 module (independently accepted in D040) also depends on the removed M02. This directly explains previously observed wrong historical counts and an invalid temporary dependency graph.

## Exact in-scope proposed repair

1. `tests/architecture/fixtures/pre_admission_20261018_inventory.json` contains **only historical file-name membership** from the exact original Git commit, not historical acceptance claims or replacement source bytes. Its SHA-256 is `3840d197d6b570cd7912aea606ce859d529ffc14c1ff93ce0378f767ebfc54b9`. The current `_copy_candidate` helper verifies that exact manifest byte identity and original commit.
2. `tests/architecture/test_proof_control.py::_copy_candidate` copies the current repository into a *disposable `tmp_path`*, then prunes all later `*.py` product-test paths and `config/product_proof` files not in the historical membership; asserts exact resulting membership; then retains existing canary resets. **No actual tracked product file or generation is modified or deleted by the helper.**
3. The temporary pre-admission architecture registry additionally removes dependents of its deliberately removed M02, including the later M03. Existing allocation and dependency-rule filtering already uses this removed-ID set. No live registry, current module acceptance, proof admission, source code, lockfile or workflow is edited.
4. The historic `93` test count remains unchanged and proves the exact originally intended membership rather than replacing the assertion with the current 198/216 counts. Newer admissions remain intact in the real repository and are also used by tests that deliberately select `ROOT` rather than the temporary pre-admission universe.

## Direct targeted author validation (not independent acceptance)

- Recomputed the historical manifest from `git ls-tree -r` of exact original commit; **101 original Python paths, 93 `test_*.py` paths, six original proof configuration paths**, equal to committed manifest.
- Python 3.13.5 with `uv 0.10.0 sync --locked --extra dev --offline` in isolated WSL worktree: exit 0, 15 resolved / 14 installed.
- `ruff check tests/architecture/test_proof_control.py`: **PASS**.
- `git diff --check`: exit 0.
- Scoped individual architecture cases:
  - `test_pending_authority_target_and_empty_proof_are_not_success`: **1 passed**.
  - `test_sqlite_current_and_historical_paths_partition_exactly`: **1 passed**, including rerun after manifest-hash pin.
  - `test_d014_combined_extensions_have_complete_disjoint_ownership`: **1 passed**.
  - `test_d012_extension_resolves_without_resealing_original_claims`: **1 passed**.
- The earlier failed approach merely removed transitive M03; it still returned `modify target M02 is not registered` because post-admission proof descriptors remained in the temporary universe. This final candidate addresses **both** historical proof-file membership and the transitive module dependency, not the symptom only.

No actual physical product proof case was run by this worker. Architecture tests above use temporary synthetic control candidates; this does not establish current domain or product semantic acceptance.

## Limits, independent review and remaining CI

This is a **test-fixture correction**, not authority to rewrite expected product outputs. The reviewer must inspect original historical file membership and pre-admission contract, ensure only disposable files are pruned, verify exact source/diff, audit the four targeted results and assess whether other architecture controls using `_copy_candidate` remain meaningful. The broader 132-failure architecture log pertains to an older PR #7 candidate and must not be claimed as a result for this branch.

A separate, unapproved lint baseline proposal is at draft [PR #10](https://github.com/JayDEmily/nvda_29102026/pull/10). Its standalone verifier matches 51 existing lint findings but is not connected to CI; the existing whole-tree Ruff stage still fails on original proof-bound bytes. No owner-approved policy replacement, newly admitted proof generation, independent reviewer clearance or full architecture CI pass has occurred. D145 remains paused, and root `GUARDRAILS.md`, `AGENTS.md`, `EXEC_PLAN.md` remain unchanged.

**Verdict sought:** independently review this bounded fixture reconstruction and return ACCEPT_BOUNDED / RETURN / PARTIAL / BLOCKED for its exact candidate, without conflating it with the lint-policy decision.
