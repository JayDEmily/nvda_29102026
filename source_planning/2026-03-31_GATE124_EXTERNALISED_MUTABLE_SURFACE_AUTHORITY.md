# 2026-03-31 Gate 124 Externalised Mutable-Surface Authority

Status: complete on `main`; Gate 125 is now the active gate

## What landed

- `StateConditionedModifierService` now loads mutable-surface baselines, floors, and caps from `config/coefficient_authority.v1.yaml` instead of private class-level constants.
- `ResolvedRuntimeSurfaceValue` now carries governed authority metadata including owner stage, authority version, baseline reference, and numeric envelope where applicable.
- The old Gate 78 late-session scenario now states the true sequence explicitly: the modifier packet resolves `target_fresh_deployable_pct` to `20.625`, then the final-risk join derisks execution output to `13.4062`.

## Proof

- `PYTHONPATH=src pytest -q tests/test_gate78_modifier_runtime_integration.py tests/test_gate118_mutable_surface_operability.py tests/test_execution_review_runtime.py tests/test_gate121_final_risk_gateway_join.py tests/test_gate124_mutable_surface_authority.py`

## Receipt

- Gate 124 externalised mutable-surface authority without changing the admitted mutable-surface universe.
- Canonical vocabulary JSON was regenerated so the committed file matches the deterministic builder again.
