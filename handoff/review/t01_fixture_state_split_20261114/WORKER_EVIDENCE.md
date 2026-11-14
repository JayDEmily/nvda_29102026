# T01 — current-vs-historical proof fixture split: worker evidence

Date: 14 November 2026 (Australia/Melbourne). **Status: WORKER_IMPLEMENTED_AND_SCOPED_ARCHITECTURE_TESTED; INDEPENDENT_REVIEW PENDING.**

## Git scope and authority

- Repo: `JayDEmily/nvda_29102026`.
- Exact parent fixture candidate: `b0f08c938b382dd06e0b838f6e4944f112c9600c` (draft PR #11).
- **One-file repair commit:** `40489f95048747527cd757cee774d588fdfcfc1b` on `work/t01-fixture-state-split-20261114`.
- Inherited original historical inventory commit `86b23f1ef5bf4a1510e93333fa4b2cfc869c3b71`: original 93 product `test_*.py`, 101 `.py`, six proof config files. The parent PR #11 preserves that exact manifest, SHA-256 `3840d197d6b570cd7912aea606ce859d529ffc14c1ff93ce0378f767ebfc54b9`.
- Applicable frozen `GUARDRAILS.md`, root `AGENTS.md`, test override, active `EXEC_PLAN.md` and `docs/architecture/TEST_AND_PROMOTION_KERNEL.md` inspected. A *test fixture correction* cannot change accepted product-proof bytes, admission rules, governing roots or required lint policy.

## Observed failure and causal mechanism

At exact parent `b0f08c9`, static AST discovery found **27 architecture test functions** using `_copy_candidate` directly or through `_d012_control_candidate`, expanding to **61 actual parameterised cases** under Pytest 9.0.3.

1. First run executed 38 passing parameterised cases, then the 39th failed with `shutil.Error: [Errno 28] No space left on device`. The temporary WSL filesystem `/tmp` is **2.0 GiB tmpfs**, 100% full at failure; main `/home/jds` WSL filesystem had over 900 GiB free. First-run log SHA-256: `4666ccbdbc9f64b7a5cae1d696be246cfd7f97f32ead508b913b7cda947e0965`.
2. Cleaned **only this run's** disposable `/tmp/pytest-of-jds/pytest-18` (~1.9 GiB) after checking owner/timestamp, preserved original log. Follow-up ran just the **23 not-yet-passed parameterised cases** using disk-backed `--basetemp` under `/home/jds`; 22 passed, one failed. Follow-up log SHA-256: `14efe602ea33b93f1bd5d69e566720a9668c2fa0a5f898f408872d37be9568ae`.
3. The remaining actual assertion-path failure was `test_m00_brief2_fixed_extension_and_exact_authority`: `FileNotFoundError` for `config/product_proof/m00_brief2/claim.json` inside the disposable fixture. **Cause directly inspected:** `_copy_candidate` deliberately deletes all post-18-October proof-config files to build a historical M02-absent pre-admission candidate, but this **27 October M00 Brief 2 test** needs the *current admitted* `m00_brief2` descriptor and generation. The accepted current descriptor and exact-brief SHA checks live in `tools/product_proof_claims.py::_m00_brief2_extension` (around lines 737-785); the failing test's authored purpose is positive current extension plus two tamper refusals. This is a fixture-projection mismatch; it is not evidence of a failed product proof or of an incorrect original admission.

## One-file bounded implementation

In `tests/architecture/test_proof_control.py` only (15 added/5 removed):
- Extract original byte-for-byte copy commands into `_copy_current_candidate(tmp_path)`, asserting disposable root differs from `ROOT`. It copies current descriptors, accepted generations and current architecture without pruning.
- The existing `_copy_candidate(tmp_path)` calls that copy helper, then performs its **unchanged historical membership pruning and canary reset**. Its manifest and historical 93-case assertion are retained.
- The M00 Brief2 test calls **`_copy_current_candidate`** instead of the historical helper, requires a successful current extension against that disposable copy, then retains both existing negative mutations: descriptor's physical-root mismatch and original-brief byte tamper.
- **Unchanged:** all physical product files, SHA-bound historical generations, admission pointers, `GUARDRAILS.md`, `AGENTS.md`, `EXEC_PLAN.md`, `pyproject.toml`, `uv.lock`, exact CI workflow and lint scope.

## Verification on pinned repair commit

- Isolated WSL CPython **3.13.5**, uv **0.10.0**, `uv sync --locked --extra dev --offline`: 15 packages resolved, 14 installed, exit 0.
- `ruff 0.15.11 check tests/architecture/test_proof_control.py`: **PASS**, `git diff --check`: **PASS**.
- Scoped first targeted test of M00 Brief2 extension and both falsifiers: **1 passed in 16.63s** (disk-backed temporary fixtures). Two representative historical fixture controls: **2 passed in 1.71s**.
- Comprehensive impact-set **re-execution warranted by the shared helper refactor**: exact `HEAD=40489f95048747527cd757cee774d588fdfcfc1b`, 27 impacted architecture functions, **61/61 parameterised cases passed in 121.42 seconds**, exit 0. Invoked `.venv/bin/python -m pytest -vv --maxfail=1 --basetemp=/home/jds/.tmp_nvda_fixture_split_all61_20261114/pytest-run <27 explicit node ids>`. `TMPDIR` was set to that same disk-backed parent; no tmpfs resource failure.
- **Raw unedited Pytest output**: `architecture_fixture_split_61_cases_pytest.log`, **10,366 bytes**, SHA-256 `f7450d86589502f4fa7f438d96d90ba6ad046591e23c7d27c8069e21fbb530d3`. It includes the explicit 27 selectors and all 61 parameterised results.
- No product-proof execution or new generation admission. These are architecture tests of disposable control fixtures; aggregate architecture promotion was not run.

## Other model branches (independent evidence, not a defect verdict)

- `review/t01-pre-admission-fixture-terra56-20261114` at `4c7f93bd...`: 200k-budget job stopped before verdict; operator report **BLOCKED**.
- `review/t01-pre-admission-fixture-terra56-7m-20261114` at `68bba0ae...`: new 7M job failed on invalid blank `github_file_text.path` in first batch, no completed independent judgement; operator report **BLOCKED**.
- Neither report establishes a defect in PR #11, but neither provides independent acceptance of this successor either. The candidate PR #11 is preserved byte-identically.

## Remaining boundaries and next recipient

The **51 existing whole-tree Ruff findings** on seven SHA-bound immutable proof files are still unresolved. The optional hash-bound lint prototype in draft PR #10 is only a **proposal** and is not wired into CI. The original full architecture CI run `43205348398` (132 failed / 89 passed) was on a different, proof-invalidating predecessor, and does not apply to this exact candidate. Full CI is **NOT VERIFIED**; do not claim promotion or merge into main. Independent semantic review of this one-file split and the inherited historical fixture remains outstanding. D145 stays suspended. Root governing documents and PRs #3/#5/#7/#9/#10/#11 are not changed by this Worker.

**Reviewer request:** independently check the exact diff `b0f08c9..40489f9`, original M00 Brief2 test authoring at `487b8222`, two fixture projections, positive and two tamper cases, 27 affected functions, raw log hash, untouched proof-generation bytes, and non-transferability of other reviewers' blocked tool execution. Return precise ACCEPT_BOUNDED / RETURN / PARTIAL / BLOCKED judgement without granting full CI clearance.
