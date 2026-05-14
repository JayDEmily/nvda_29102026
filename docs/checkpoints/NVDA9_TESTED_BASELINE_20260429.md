# NVDA9 Tested Baseline Checkpoint — 2026-04-29

Status: TESTED LOCAL BASELINE

## Purpose

This checkpoint records the local Repo D recovery and hygiene baseline before GitHub preservation.

## Source

- Source environment: Ubuntu WSL2 local repo
- Repo root: `/home/jds/dev/NVDA9`
- Original recovered stream: Repo D
- Active branch before promotion: `work/bridge-gate5-vocabulary-law-20260426`

## Baseline scope

This baseline includes:

- Rehydrated Git repo from `repo_D_latest_ea3ff8a_2026-04-28.zip`
- Repo root promoted to `/home/jds/dev/NVDA9`
- Python pinned to `3.13.5`
- `.python-version` added for repo-local pyenv alignment
- `pyproject.toml` dependency cleanup
- Makefile repaired as canonical repo command entrypoint
- Root `scripts` package aligned with active import surface
- Dev tooling added:
  - `pytest==9.0.3`
  - `black==26.3.1`
  - `ruff==0.15.11`
- Black formatting applied
- Ruff import sorting applied
- E402 docstring/future-import layout fixed
- F401 unused imports resolved while preserving wrapper re-export surfaces
- Vocabulary touch stamp updated through repo-native workflow where required

## Verification

At the time of checkpoint preparation:

- Python: `3.13.5`
- Black: passes
- Ruff: passes
- Pytest: `133 passed`
- Git status: clean except ignored/generated artefacts

## Ignored/generated artefacts

The following generated artefact may exist locally and is intentionally ignored:

- `var/vocabulary/synonym_candidates.json`

It is not part of trusted committed state.

## Promotion rule

This checkpoint may be promoted to local `main` only after:

1. `make format-check` passes
2. `make lint` passes
3. `make test` passes
4. local `main` can be fast-forwarded from the tested work branch

No GitHub merge or PR is implied by this checkpoint.
