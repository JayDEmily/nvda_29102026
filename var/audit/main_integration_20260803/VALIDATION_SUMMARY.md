# Main Integration Validation Summary — 2026-08-03

## Outcome before final checkpoint commit

PASS for the bounded `main` integration leaf.

## Integration state

- Local `main` was created from accepted `origin/main` at `98c462a4f8fb258b79429ec083565d6f2e2fffd9`.
- `main` was advanced with `git merge --ff-only work/vocabulary-governance-dedup-v1` through:
  - `3a8e861bf75455a650dd0049c9cc5b52e75cbe36`;
  - `9e1d22b627f7b94873d514616b4fce2d727ce9de`.
- `ROADMAP_LEDGER.md` was then updated on `main` to record integration rather than a pending candidate.
- `Active ExecPlan` remains `none`; no successor phase was activated.

## Pre-integration drift

One uncommitted line change was present in `ROADMAP_LEDGER.md` before integration. It was not part of the accepted commit and weakened the agreed ExecPlan-owned routing rule. It was discarded. Exact evidence is retained in `evidence/ROADMAP_LEDGER_PREINTEGRATION_DRIFT.diff.gz`.

## Validation

| Check | Result |
|---|---|
| Tier A | PASS — 2,007 tests |
| Tier B + Tier C | PASS — 102 tests |
| Combined behavioural tests | PASS — 2,109 tests |
| Proof authority | PASS — 201 families, 203 tests, 73 blocks |
| Ruff, every Python file changed since `98c462a` | PASS — 5 files |
| Black, every Python file changed since `98c462a` | PASS — 5 files unchanged |
| Python compilation | PASS — `src`, `scripts`, `tests` |
| Git diff whitespace check | PASS |
| Git object integrity | PASS |

## Broad-tooling observation

A whole-repository `ruff check .` was also attempted and returned 138 errors in retained historical/archive/tooling surfaces. These are outside this Markdown-only integration leaf and were not introduced by the two integrated commits. No suppression or unrelated repair was performed. The complete output is retained in `evidence/RUFF_PRECOMMIT.log`.

A whole-repository Black run was interrupted by the outer command timeout. The bounded Black check covering every Python file changed by the integrated commits passed.

## Post-commit requirement

After the final checkpoint commit, rerun the two deterministic behavioural sets and the proof-authority check against the exact clean `main` commit. Store those results with the handoff archive rather than altering the validated commit.
