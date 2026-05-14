# NVDA persistence-migration-lifecycle tranche v1 report — 2026-04-20

## Scope

Execute `nvda_persistence_migration_lifecycle_tranche_v1_brief_2026-04-20.md` on branch `work/persistence-migration-lifecycle-tranche-v1-20260420` from the accepted boundary-home baseline after promoting `main` from `f54fd937c88117aa9577a175bfc22a26456396d5` to `167fd520321ce3925ae9ebd96abe508d9af377e5`.

This tranche was bounded to:
- `src/nvda_desk/persistence/migrations/**`
- minimal related edits under `src/nvda_desk/persistence/__init__.py`
- top-level `alembic/**`
- the minimum truthful Tier A migration-lifecycle proof mirror
- tranche receipt/report surfaces under `var/audit/`

This tranche did not widen into replay, scenarios, observability, imported-module disposition, entry/API/ingress follow-on work, broad persistence-domain redesign, or packaging changes.

## Closed leaves

1. `e8f1884` — migration-lifecycle owner audit and admissibility decision
2. `11b52e5` — migration-home convergence
3. `b3f4b81` — minimum truthful migration proof mirror
4. `b85cd12` — tranche closeout surfaces and brief lineage

## Observed directly

### Promotion precondition and baseline
- `main` was still at `f54fd937c88117aa9577a175bfc22a26456396d5` when this tranche started.
- The accepted boundary-home branch `work/boundary-home-convergence-tranche-v2-20260420` was at `167fd520321ce3925ae9ebd96abe508d9af377e5`.
- `main` was fast-forwarded to that accepted state before the tranche branch was opened.

### Migration-lifecycle convergence
- The benchmark-owned migration home now exists physically at `src/nvda_desk/persistence/migrations/__init__.py` and `src/nvda_desk/persistence/migrations/layout.py`.
- The package-owned migration home declares the explicit relationship to the current top-level Alembic placeholder tool root rather than fabricating a full migration environment.
- Top-level `alembic/` remained in place and now states its placeholder tool-root role explicitly at `alembic/README.md` and `alembic/versions/README.md`.
- No `alembic.ini`, `env.py`, or `script.py.mako` exists in the current tree. This tranche did not fabricate those surfaces.
- `src/nvda_desk/persistence/__init__.py` was narrowed to package-level ownership wording only.

### Proof mirror admitted
- `config/retained_test_registry.yaml` now routes native Tier A roots for `tests/tier_a/migrations/`.
- `config/retained_test_registry.yaml` now records the bounded retained seed family `migration_lifecycle_surface`.
- The admitted native proof file is `tests/tier_a/migrations/test_migration_lifecycle_surface.py`.

### Touched surfaces
- Added:
  - `src/nvda_desk/persistence/migrations/__init__.py`
  - `src/nvda_desk/persistence/migrations/layout.py`
  - `tests/tier_a/migrations/test_migration_lifecycle_surface.py`
  - `var/audit/briefs/nvda_persistence_migration_lifecycle_tranche_v1_brief_2026-04-20.md`
  - `var/audit/reports/nvda_persistence_migration_lifecycle_tranche_v1_report_2026-04-20.md`
- Changed:
  - `src/nvda_desk/persistence/__init__.py`
  - `alembic/README.md`
  - `alembic/versions/README.md`
  - `config/retained_test_registry.yaml`
  - `var/audit/nvda_running_audit_log.xlsx`

## Inferred

- The benchmark-home count moved from `19 / 24` to `20 / 24` because the prior closed boundary report carried `nvda_desk.persistence.migrations` as still absent and this tranche created that physical home while leaving the other absent homes untouched.
- The next bounded benchmark-home work, if later queued, is now outside persistence-migration-lifecycle drift because the remaining absent homes are `legacy.imported`, `analysis.replay`, `analysis.scenarios`, and `observability`.

## Unknown

- Whether top-level Alembic should later become a real migration environment or remain a placeholder pending broader persistence work is unknown at this tranche boundary.

## Proof outcome

Native proof floor on the final working tree:
- `PYTHONPATH=src pytest -q tests/tier_a tests/tier_b` → `90 passed`
- `python3 -m compileall src tests/tier_a tests/tier_b` → clean

Bounded proof mirror check used during Leaf 3:
- `PYTHONPATH=src pytest -q tests/tier_a/migrations/test_migration_lifecycle_surface.py` → `2 passed`
- `python3 -m compileall src/nvda_desk/persistence/migrations tests/tier_a/migrations` → clean

The offline two-bundle `.venv` path was not rerun because this tranche did not change packaging, installability assumptions, or proof invocation surfaces.

## Benchmark-home count after closeout

Observed directly / inferred combined state after closeout:
- workbook target package families physically present: `20 / 24`
- remaining absent benchmark homes:
  - `nvda_desk.legacy.imported`
  - `nvda_desk.analysis.replay`
  - `nvda_desk.analysis.scenarios`
  - `nvda_desk.observability`

## Exact carry-forward created by this tranche

- `src/nvda_desk/persistence/migrations/layout.py` admits only layout declaration for the package-owned migration home and the current top-level Alembic placeholder tool root. This tranche did not admit a real Alembic environment, revision scripts, or schema-autogeneration workflow.
- `alembic/README.md` and `alembic/versions/README.md` now declare placeholder tool-root status explicitly, but this tranche did not widen into ORM metadata wiring, migration execution commands, or persistence-domain redesign.

## Closeout judgement

This tranche is complete within its bounded scope.

The active working branch has no unreconciled leaves from this tranche after receipt reconciliation.

Judgement: **ready-to-close**.

This report does not itself merge or delete the branch.
