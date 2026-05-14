# NVDA benchmark-home-convergence tranche v1 report — 2026-04-20

## Scope

Execute `nvda_benchmark_home_convergence_tranche_v1_brief_2026-04-20.md` on `work/prebuild-tranche-leaf-ledger-law-20260420` from baseline `ab5de0de9110538ceafab43c5401372fc2c1e9e7`.

This tranche was bounded to:
- `nvda_desk.config`
- `nvda_desk.cognition.modifiers`
- `nvda_desk.calendar.reference`
- `nvda_desk.calendar.operational`
- the minimum truthful proof-family mirror for those moved homes

No feature expansion, API widening, workbook rewrite, or governance-law rewrite was performed.

## Closed leaves

1. `acfcb27` — config home convergence
2. `dca2759` — modifier home convergence
3. `fd8d371` — calendar split convergence
4. `02e33bb` — minimum benchmark-shaped proof mirror

## Observed outcome

The benchmark-owned homes required by this tranche now exist physically:
- `src/nvda_desk/config/`
- `src/nvda_desk/cognition/modifiers/`
- `src/nvda_desk/calendar/reference/`
- `src/nvda_desk/calendar/operational/`

Compatibility continuity was kept bounded and explicit:
- `src/nvda_desk/services/coefficient_authority_service.py` now acts as a thin wrapper over the config home
- `src/nvda_desk/domain/posture/modifier_application.py` now acts as a thin wrapper over the modifier home
- `src/nvda_desk/reference/calendar_import.py` and `src/nvda_desk/reference/calendar_projection.py` now act as thin wrappers over the calendar reference home

The benchmark-home count moved from `13 / 24` physically present to `17 / 24` physically present.

The remaining absent benchmark package families are:
- `nvda_desk.entry`
- `nvda_desk.ingress`
- `nvda_desk.legacy.imported`
- `nvda_desk.analysis.replay`
- `nvda_desk.analysis.scenarios`
- `nvda_desk.observability`
- `nvda_desk.persistence.migrations`

## Proof outcome

Native proof floor on the working tree:
- `PYTHONPATH=src pytest -q tests/tier_a tests/tier_b` → `82 passed in 1.16s`
- `python3 -m compileall src tests/tier_a tests/tier_b` → clean

Offline two-bundle `.venv` path on the same repo state:
- runtime bootstrap → `runtime install ok`
- dev supplement bootstrap → `dev supplement install ok`
- `PYTHONPATH=src pytest -q tests/tier_a tests/tier_b` inside repo-local `.venv` → `82 passed in 2.11s`
- `python3 -m compileall src tests/tier_a tests/tier_b` inside repo-local `.venv` → clean

## Proof mirror changes admitted

New native Tier A families admitted in `config/retained_test_registry.yaml`:
- `config_authority_surface`
- `state_conditioned_modifier_surface`
- `calendar_operational_surface`

Updated native Tier A family:
- `calendar_reference_projection_crosswalk` now points at the benchmark-owned `calendar.reference` home rather than the legacy wrapper home

## Closeout judgement

This tranche is complete within its bounded scope.

The active working branch has no unreconciled leaves from this tranche.

Judgement: **ready-to-close**.

This report does not itself merge or delete the branch.
