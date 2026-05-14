# NVDA imported-module subsystem disposition tranche v1 — closeout report

Date: 2026-04-20
Active branch: `work/imported-module-subsystem-disposition-tranche-v1-20260420`
Accepted baseline promoted to `main` before tranche start: `65f24831eb012f20b0114f63cdaab869dbcbfcc8`
Observed pre-promotion `main`: `aa4bad4728a0ea1cfc72570337584f1c8cc11a42`

## Direct answer

This tranche closed the imported-module subsystem truthfully as **retired / quarantined historical source evidence only**.

No native package was admitted under `src/nvda_desk/legacy/imported/`.
No prohibited surface was widened.

## Leaf chronology

1. `5d41a4b` — dependence map and disposition audit
2. `1616f23` — explicit quarantine marker for the top-level archive tree
3. `b951923` — minimum truthful proof mirror
4. tranche closeout commit — this report, brief lineage copy, and workbook reconciliation

## What changed

### Disposition outcome

Observed directly after closeout:

- `legacy_import/README.md` now states that the tree is historical source evidence only;
- the README states that there is no admitted native package at `src/nvda_desk/legacy/imported/`;
- the README states that native runtime and native Tier A / Tier B proof must not import from the tree.

Truth judgement:

- the benchmark workbook keeps the family provisional / reserved rather than mandatory always-admit runtime ownership;
- no native runtime or native proof import path into `legacy_import/` was found;
- the package build scope remains limited to the native `src/` tree plus native tests;
- the historical tree remains valuable as archive evidence, but not as a live native owner.

Therefore the truthful closeout state is retirement / quarantine, not bridge admission.

### Proof mirror

Observed directly after closure:

- `tests/tier_a/legacy_imported/test_imported_module_containment_surface.py` now asserts:
  - absence of `src/nvda_desk/legacy/imported/`;
  - absence of exact `legacy_import` or `nvda_desk.legacy.imported` references across native runtime and native Tier A / Tier B python files;
  - explicit quarantine wording in `legacy_import/README.md`;
  - package-build exclusion in `pyproject.toml`.
- `config/retained_test_registry.yaml` now admits the new Tier A family root `tests/tier_a/legacy_imported/` and the blocker `imported_module_containment_surface`.

## Proof run

### Targeted tranche proof

`PYTHONPATH=src pytest -q tests/tier_a/legacy_imported/test_imported_module_containment_surface.py`

Observed output:

- `2 passed in 0.27s`

`python3 -m compileall tests/tier_a/legacy_imported`

Observed output:

- clean

### Tranche proof floor

`PYTHONPATH=src pytest -q tests/tier_a tests/tier_b`

Observed output:

- `102 passed in 1.69s`

`python3 -m compileall src tests/tier_a tests/tier_b`

Observed output:

- clean

## Why bridge admission was false

Bridge admission was not lawful in this tranche because:

- no current native runtime surface imports or instantiates any module from `legacy_import/`;
- no current native Tier A or Tier B python surface depends on `legacy_import/`;
- `tests/AGENTS.override.md` already declares legacy tests under `legacy_import/tests/` to be source evidence only;
- surviving native uses of the word `imported` are bounded calendar/reference or review-citation concepts, not ownership of a native imported-module subsystem;
- admitting `src/nvda_desk/legacy/imported/` here would fabricate live capability to satisfy a provisional workbook reservation cosmetically.

## Deferred truth retained intentionally

This tranche did **not** admit:

- `src/nvda_desk/legacy/imported/`
- `analysis.scenarios`
- `observability`
- API, entry, ingress, replay, or broker-boundary follow-on work
- broad rewrites or deletions inside the historical `legacy_import/` tree

## Benchmark-home state after closeout

Observed benchmark-home count remains `21 / 24`.

Remaining absent benchmark homes:

- `src/nvda_desk/legacy/imported/` — remains a retired / quarantined benchmark reservation rather than a live native home
- `src/nvda_desk/analysis/scenarios/`
- `src/nvda_desk/observability/`
