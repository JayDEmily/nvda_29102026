# NVDA10 Clean Baseline Status

Date: 2026-05-08

## Baseline

- Repo path: `/home/jds/dev/nvda10`
- Branch: `main`
- Validation HEAD commit: `086d73fad8a40ff2f11c64fcd3a9a2ab1b502be3`
- Remote URL: `https://github.com/JayDEmily/nvda10.git`
- Baseline statement: this is the clean baseline before Atlas feature migration begins.

## Root Layout Verification

All required root paths were present:

- `AGENTS.md`
- `PLANS.md`
- `pyproject.toml`
- `src/`
- `tests/`
- `docs/`
- `var/audit/`
- `project_control/`
- `evidence_index/`
- `_archive/`
- `assembly_reports/`

## Validation Status

- `make compile`: passed.
- `make test-targeted TESTS="tests/tier_a/upstream_signal/test_upstream_non_interference_and_sanity_traces.py tests/tier_a/upstream_signal/test_upstream_signal_coverage_map_and_scope_lock.py tests/tier_b/review_replay/test_tranche_a_review_replay.py"`: passed, 9 tests passed.

## Working Tree

- Pre-report working tree status: clean.

## Current Known Caveats

- Original Atlas ZIP container missing; Atlas content present.
- Stage1E.1 `FOUND_EQUIVALENT`, not `FOUND_EXACT`.
- GAP-006 exact worktree TAR found equivalent.
