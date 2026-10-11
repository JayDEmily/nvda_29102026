# M01 F4 — authorised D116 repair and continuing F4 checkpoint

**Date:** 11 October 2026. **Disposition:** IN PROGRESS — NOT an F4/Stage-1 independent-review candidate. This file records the current active scope without superseding root governance or ExecPlan. Exact Git HEAD/tree are in the surrounding full-Git archive CHECKPOINT.json (outside Git to avoid a circular commit reference).

## Authority and implementation

- Latest programme-owner instruction authorises *only* D116's source correction to `R041;R047;R048` with R047 applicable to CALL and R048 applicable to PUT; accepted D116 ratio `option_volume / open_interest` is unchanged.
- The accepted dual-source D123 right-conditional history implementation, controlled official reporting periods, absence refusal and prior evidence remain unchanged.
- R075 remains **Average Option Volume**, and D117 retains its `R041;R075` dependencies. The two authoritative/runtime CSV catalogues have the same SHA-256 (`d651436df1fcd1395f8f1147dfd80db1ed178da4834447a947c3c9c32fd82aa7`).
- Proof-first D116 red suite was committed as `e4f2963`; D116 catalogue/production and corrected RC14 fixture as `9e80dbb`; additional bounded D110 public M00 lineage and refusal proof as `7b355b5`; D123 proof formatting clean-up as `be93e6a`. Full predecessor history is retained by Git.
- The previously misleading D116 R075 synthetic fixture is recoverable in preceding Git history; the updated active fixture uses R047/1000 for the accepted 300/1000=0.3 ratio.

## Current validation observations

All commands run from repository root with Python 3.13.5 and PostgreSQL 17.9, using `PYTHONPATH=src`. PostgreSQL M00 and M01 boundary tests used distinct `m00_proof`/`m01_proof` roles, PostgreSQL server with `fsync`, `full_page_writes` and `synchronous_commit` enabled.

1. `python -m pytest -q tests/implementation/derived_signal/test_m01_f4_d116_authorised_postgresql.py tests/implementation/derived_signal/test_m01_f4_d123_controlled_postgresql.py tests/product/derived_signal/test_m01_f4_d116_authorised_public.py tests/product/derived_signal/test_m01_f4_d123_controlled_public.py tests/product/derived_signal/test_m01_f4_d110_spot_expected_move_public.py` — **40 passed**, `logs/d116_d123_d110_focused_current.log`.
2. `python -m pytest -q tests/architecture tests/bootstrap tests/product tests/implementation/derived_signal --ignore=tests/product/raw_signal/test_u05_postgresql_durability.py` — **1,111 passed**, `logs/full_non_durability_regression_current.log`.
3. `python -m mypy src` — **21 source files, no errors**, `logs/mypy_current.log`.
4. `python -m ruff check` for affected calculation source and tests — **PASS**, `logs/ruff_lint_current.log`.
5. `python -m ruff format --check` for seven directly affected calculation source and test files — **7 already formatted**, `logs/ruff_scoped_format_current.log`.
6. `python -m ruff format --check .` — **FAIL**, 62 files (outside bounded repair) would be reformatted, `logs/ruff_repo_wide_format_not_clean.log`. No blanket formatting was performed because unrelated changes are outside the bounded authority. This is an explicit outstanding *whole-repository formatting* validation.
7. `python -m pytest -q tests/product/raw_signal/test_u05_postgresql_durability.py` — **55 passed in 34.22s** in a separately isolated Python 3.13.5 virtual environment with pinned pytest 9.0.3, psycopg 3.3.4 and no ambient Pydantic, using actual PG 17.9. See `logs/clean_durability_55_pass.log`. The preceding *ambient* environment group produced one failure from installed Pydantic's `MockValSer` during recursive graph inspection; that failure is preserved at `logs/ambient_durability_one_failure.log` and must not be erased or described as a production defect based only on that evidence. The clean suite was run **in one invocation**, not a skipped-test substitution. The no-Pydantic isolation follows existing repository environment diagnostics for the same issue.
8. F4 reconciliation generator `python handoff/m01_completion/proof/f4_20261009/f4_progress_readback.py` — **PASS** and regenerated existing CSV/JSON ledgers; readback below is not an acceptance statement.

The above tests do **not** establish completion of the full Stage-1 semantic acceptance proposition.

## Evidence census and next legitimate work

- Authoritative Stage-1 population: **174** own-kernel rows; **144** Stage-1-closed and **30** cross-stage.
- Active catalogue dependencies: **491** relationships, plus the D007 zero-dependency sentinel. **303** F4 bounded public-edge dispositions; inherited F2/F3 evidence retained.
- **52** still-outstanding Stage-1-closed relationship edges in **11** rows: D041 (3), D078 (7), D079 (4), D080 (4), D081 (4), D084 (3), D104 (2), D132 (6), D148 (9), D149 (4), D150 (6).
- **30** cross-stage own-kernel and lawful public-refusal obligations remain unproved. These are proof obligations, not established software defects; they cannot be silently marked accepted because existing kernel unit tests pass.
- D110's two previously outstanding edges were closed by `tests/product/derived_signal/test_m01_f4_d110_spot_expected_move_public.py`, with exact M00 source lineage, D109 predecessor, numerical result 9% and absence/decoy/future refusal.
- All accepted F4 acceptance conditions and semantic boundaries remain binding. Stage 1 is unaccepted; Stage 2 remains unauthorised.

## Reproduction and limitations

The original M00 and PostgreSQL offline proof runtime bundles, needed to reproduce PG tests, are separate programme inputs and are not represented as included in this repository. PostgreSQL role DSNs (`NVDA_TEST_M00_POSTGRES_DSN`, `NVDA_TEST_M01_POSTGRES_DSN`) must be configured correctly; durability uses `NVDA_TEST_POSTGRES_DSN` for a role able to exercise its own server-ack protocol. For isolated durability use `PYTHONPATH=.:src` and disable external pytest-plugin autoload (`PYTEST_DISABLE_PLUGIN_AUTOLOAD=1`). Do **not** treat clean-env success as passing the ambient environment's one failed test.

Continue F4 per current ExecPlan and latest owner instructions. Return for independent review only after all 52 remaining closed-stage relationship edges, the 30 cross-stage obligations and applicable validation/acceptance evidence are resolved. This archive is a continuation checkpoint and **must not** be sent as an accepted Stage-1 candidate.
