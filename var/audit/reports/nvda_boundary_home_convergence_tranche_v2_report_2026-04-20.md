# NVDA boundary-home-convergence tranche v2 report — 2026-04-20

## Scope

Execute `nvda_boundary_home_convergence_tranche_v2_brief_2026-04-20.md` on branch `work/boundary-home-convergence-tranche-v2-20260420` from baseline `main` at `f54fd937c88117aa9577a175bfc22a26456396d5`.

This tranche was bounded to:
- `src/nvda_desk/api/`
- `src/nvda_desk/entry/`
- `src/nvda_desk/ingress/`
- thin compatibility wrappers only where needed under `src/nvda_desk/api/http/` and `src/nvda_desk/adapters/ingress/`
- the minimum truthful Tier A proof mirror for the touched boundary homes
- tranche receipt/report surfaces under `var/audit/`

This tranche did not widen into replay, scenarios, observability, imported-module disposition, persistence migrations, broker integration, or downstream policy expansion.

## Closed leaves

1. `43fa4e8` — API boundary module-cut convergence
2. `636d49b` — entry home convergence
3. `d5e88a8` — ingress home convergence
4. `5748dff` — minimum truthful proof mirror
5. `625c2eb` — tranche closeout report and brief lineage

## Observed directly

### Workbook and benchmark alignment
- The governing workbook anchors for this tranche were the locked ranges named in the brief: `Target_Structure!A3:G27`, `Ownership_Matrix!A3:H38`, `Component_Skeleton!A3:G39`, `Test_Architecture!A3:H20`, and `Reservations!A3:H12`.
- The benchmark-owned API cut now exists physically at `src/nvda_desk/api/app.py:12-56` and `src/nvda_desk/api/deps.py:13-23`.
- The legacy API path remains only as a thin compatibility wrapper at `src/nvda_desk/api/http/app.py:3-7`.
- The benchmark-owned entry home now exists physically at `src/nvda_desk/entry/asgi.py:11-26` and `src/nvda_desk/entry/cli.py:15-54`.
- The benchmark-owned ingress home now exists physically at `src/nvda_desk/ingress/raw_bundle_loader.py:11-97`.
- The compatibility ingress wrappers remain thin at `src/nvda_desk/adapters/ingress/market_snapshot_feed.py:12-19` and `src/nvda_desk/adapters/ingress/options_surface_feed.py:12-16`.
- Calendar import remained reference-boundary only; this tranche did not reclassify it as runtime ingress. The existing boundary remains at `src/nvda_desk/adapters/ingress/calendar_feed.py:1-16`.

### Proof mirror admitted
- `config/retained_test_registry.yaml:28-30` now routes native Tier A roots for `tests/tier_a/api/`, `tests/tier_a/entry/`, and `tests/tier_a/ingress/`.
- `config/retained_test_registry.yaml:162-223` now records the bounded retained seed families:
  - `api_boundary_surface`
  - `entry_boundary_surface`
  - `ingress_raw_bundle_loader_surface`
- The admitted native proof files are:
  - `tests/tier_a/api/test_api_boundary_surface.py:24-52`
  - `tests/tier_a/entry/test_entry_boundary_surface.py:24-53`
  - `tests/tier_a/ingress/test_raw_bundle_loader_surface.py:24-75`

### Touched surfaces
- Added:
  - `src/nvda_desk/api/__init__.py`
  - `src/nvda_desk/api/app.py`
  - `src/nvda_desk/api/deps.py`
  - `src/nvda_desk/entry/__init__.py`
  - `src/nvda_desk/entry/asgi.py`
  - `src/nvda_desk/entry/cli.py`
  - `src/nvda_desk/ingress/__init__.py`
  - `src/nvda_desk/ingress/raw_bundle_loader.py`
  - `tests/tier_a/api/test_api_boundary_surface.py`
  - `tests/tier_a/entry/test_entry_boundary_surface.py`
  - `tests/tier_a/ingress/test_raw_bundle_loader_surface.py`
  - `var/audit/reports/nvda_boundary_home_convergence_tranche_v2_report_2026-04-20.md`
  - `var/audit/briefs/nvda_boundary_home_convergence_tranche_v2_brief_2026-04-20.md`
- Changed:
  - `src/nvda_desk/api/http/app.py`
  - `src/nvda_desk/adapters/ingress/market_snapshot_feed.py`
  - `src/nvda_desk/adapters/ingress/options_surface_feed.py`
  - `config/retained_test_registry.yaml`
  - `var/audit/nvda_running_audit_log.xlsx`

## Inferred

- The benchmark-home count moved from `17 / 24` to `19 / 24` because tranche v1 already reported `entry` and `ingress` as still absent, and this tranche created both physical homes while leaving the other absent homes untouched. This inference is based on the prior closed report at `var/audit/reports/nvda_benchmark_home_convergence_tranche_v1_report_2026-04-20.md` and the current physical tree.
- The next bounded benchmark-home work, if later queued, should now be outside this runtime-boundary tranche because the remaining absent homes are no longer boundary-home drift.

## Unknown

- Whether the remaining absent benchmark homes should each be physically converged or partly lawfully retired in later governance work remains unknown at this tranche boundary.

## Proof outcome

Native proof floor on the final working tree:
- `PYTHONPATH=src pytest -q tests/tier_a tests/tier_b` → `88 passed`
- `python3 -m compileall src tests/tier_a tests/tier_b` → clean

Bounded proof mirror check used during Leaf 4:
- `PYTHONPATH=src pytest -q tests/tier_a/api/test_api_boundary_surface.py tests/tier_a/entry/test_entry_boundary_surface.py tests/tier_a/ingress/test_raw_bundle_loader_surface.py` → `6 passed`
- `python3 -m compileall src/nvda_desk/api src/nvda_desk/entry src/nvda_desk/ingress src/nvda_desk/adapters/ingress tests/tier_a/api tests/tier_a/entry tests/tier_a/ingress` → clean

The offline two-bundle `.venv` path was not rerun because this tranche did not change packaging, installability assumptions, or proof invocation surfaces.

## Benchmark-home count after closeout

Observed directly / inferred combined state after closeout:
- workbook target package families physically present: `19 / 24`
- remaining absent benchmark homes:
  - `nvda_desk.legacy.imported`
  - `nvda_desk.analysis.replay`
  - `nvda_desk.analysis.scenarios`
  - `nvda_desk.observability`
  - `nvda_desk.persistence.migrations`

## Exact carry-forward created by this tranche

- `src/nvda_desk/entry/cli.py:30-54` remains intentionally bounded to `inspect-config` and `run-once`. Replay and evaluation CLI behaviour were not admitted because the benchmark homes `analysis.replay` and `analysis.scenarios` remain unconverged.
- `src/nvda_desk/api/app.py:37-56` remains a minimal app shell with only `healthcheck` and `run_once` route handlers. This tranche did not admit broader route families, auth, persistence injection growth, or broker-facing web work.
- `src/nvda_desk/ingress/raw_bundle_loader.py:72-97` admits only raw bundle decode into one upstream typed carrier. This tranche did not widen into preparation feature derivation, cognition-stage logic, or calendar-reference redesign.

## Closeout judgement

This tranche is complete within its bounded scope.

The active working branch has no unreconciled leaves from this tranche after receipt reconciliation.

Judgement: **ready-to-close**.

This report does not itself merge or delete the branch.
