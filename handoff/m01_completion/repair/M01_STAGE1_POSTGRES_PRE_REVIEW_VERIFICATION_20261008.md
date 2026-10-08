# M01 Stage 1 — PostgreSQL pre-review verification, 2026-10-08

## Disposition and authority boundary

This document updates the execution evidence for the predecessor-selection repair candidate
previously frozen at `7b21aaec1fa6da695c552735a7153362aa5ea7a4` (tree
`c5e3656cbdd50086aff51beb81a2e48854526fe0`). It supersedes **only the claim of an
unavailable PostgreSQL execution environment** and the seven related PostgreSQL-test
exclusions in the original worker handoff. All behavioural repair and Stage-1 review boundaries
remain unchanged. No source, test, accepted authority, catalogue or execution-plan behaviour
was modified to obtain these results.

The user's follow-up explicitly required investigating and executing the previously excluded
tests where the Project's supplied proof environment made that possible.

## Environment reconstruction (observed)

The Project includes both preserved attachments:

- `NVDA_U05_PROOF_ENV_BOOTSTRAP_PY313_PG17_9_20260926.tar(1).gz`, whose integrity
  verification script checked all bundled wheels and scripts;
- `NVDA_POSTGRESQL_17_9_PORTABLE_RUNTIME_20260921.tar(1).gz`, with expected and observed
  SHA-256 `59822410ac6855365c90765de5071182ab382e87d9e9a2622424e7787c4e5caf`.

The supplied `bootstrap_all.sh` created a fresh Python 3.13.5 venv and PostgreSQL 17.9
cluster without a network package installation. The installed proof tools verified as
`pytest 9.0.3`, `psycopg 3.3.4` plus binary 3.3.4, `mypy 1.20.1`, `ruff 0.15.11`.
The repository-pinned `PyYAML 6.0.3` was provided via a `.pth` entry pointing at the
already-installed, exact-version host site-packages. This also exposed host-side pytest
plugins; all reported checks ran with the pinned pytest 9.0.3 executable and package.

Live database readback returned `server_version=17.9`, `UTF8`, `fsync=on`,
`synchronous_commit=on`, `full_page_writes=on`, and no TCP listener (Unix socket only).
A fresh `postgres` proof database provided an administrative `oai` role and separate
`nvda_m00_proof` and `nvda_m01_proof` LOGIN roles, each with its own same-named schema.
Readback of `current_user` and `current_schema()` established distinct M00/M01 identities.
A database-level `CREATE` privilege for the M00 proof role was needed by one
negative-path test that dynamically creates an auxiliary probe schema; it was granted
on the **fresh proof database only**.

The earlier worker's `PostgreSQL unavailable` statement was an incomplete execution
assessment, not a physical capability boundary. The archive and its bootstrap were
usable without code changes.

## Tests on source state `7b21aae`

All results below were obtained against the same source Git commit and ephemeral proof
cluster. The full command-level outputs are carried at
`handoff/m01_completion/proof/stage1_postgres_environment_20261008/`.

| Test class and exact invocation | Result | Evidence file |
|---|---|---|
| `pytest -q tests/implementation/derived_signal/test_ds_t01_persistence_isolation.py tests/implementation/derived_signal/test_ds_t01_r02_persistence_boundary_refinement.py tests/implementation/derived_signal/test_ds_t01_r03_postgres_privilege_boundary_refinement.py tests/implementation/derived_signal/test_ds_t01_r04_postgres_privilege_surface_refinement.py tests/implementation/derived_signal/test_ds_t01_r05_postgres_role_membership_refinement.py tests/implementation/derived_signal/test_ds_t01_selection_lineage_persistence.py` | **42 passed** | `m01_postgres_boundary_42_pass.log` |
| `pytest -q tests/product tests/architecture tests/bootstrap tests/implementation/derived_signal --ignore=tests/product/raw_signal/test_u05_postgresql_durability.py` | **662 passed** | `stage1_with_m01_postgres_662_pass.log` |
| `pytest -q tests/implementation/raw_signal` | **34 passed** | `m00_implementation_34_pass.log` |
| M00 PostgreSQL durability: collected all **55** exact node IDs from `tests/product/raw_signal/test_u05_postgresql_durability.py`, and ran ordered node-index subsets 1–15, 16–25, 26–29, 30–40, 41–55, using `pytest -q` except `-vv` for 26–29 | **15 + 10 + 4 + 11 + 15 = 55 passed** in five bounded invocations | `m00_durability_cases_*.log` |

`pytest` means the venv Python (`$NVDA_U05_PYTHON -m pytest`) with `PYTHONPATH=.:src`,
`NVDA_TEST_POSTGRES_DSN` and the separate `NVDA_TEST_M00_POSTGRES_DSN` and
`NVDA_TEST_M01_POSTGRES_DSN` set to the fresh cluster.

The M00 durability file was **not** demonstrated in one uninterrupted 55-test invocation:
large single invocations exceeded the current execution tool's per-command limit. The five
bounded invocations cover the exact collected set without omitting, deselecting or
modifying any case. One batch reported a multiprocessing `fork()` deprecation warning;
no assertion failed in the successful runs.

## Observed harness setup failures and resolution

1. An initial M01 isolation run produced **41 passed, 1 failed** because the M00 role
   lacked database-level `CREATE` to create a test-only schema. Granting that privilege
   in the ephemeral test database gave **42 passed** without any code/test modification.
2. The initial combined architecture run produced **661 passed, 1 failed** because Git
   refused ownership of the extracted checkout (`safe.directory`). Exporting
   `GIT_CONFIG_COUNT=1`, `GIT_CONFIG_KEY_0=safe.directory` and
   `GIT_CONFIG_VALUE_0=<extracted checkout>` to the test process gave **662 passed**.
3. Large uninterrupted M00 runs timed out under the tool command limit. Running the
   collected node IDs in the five contiguous batches above gave **55 passed**.

These setup failures remain recorded here; they were not represented as code defects or
silently counted as successes.

## Static and Git validation

On source commit `7b21aae`, the following commands passed:

- `ruff check src tests tools`: all checks passed;
- `python -m mypy src`: success, no issues in 21 source files;
- `python tools/validate_architecture.py`: PASS; zero dependency/public-seam violations;
- `git fsck --no-reflogs --no-progress`: exit 0, reporting pre-existing dangling but
  non-corrupt objects; `git status --porcelain`: empty.

The final documentation-only handoff commit must be read as a new exact review identity;
it does not imply a behavioural change to the tested predecessor-selection repair.
The independent reviewer remains responsible for class-level semantic review, including
non-D109/D170 aggregate graphs such as D121/D122. No independent Stage-1 acceptance,
Stage-2 authorisation or whole-M01 completion is claimed.
