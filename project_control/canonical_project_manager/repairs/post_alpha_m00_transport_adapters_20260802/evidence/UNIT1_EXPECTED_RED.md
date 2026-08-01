# Unit 1 Expected-red Evidence

- Date: 2026-08-02
- Branch: `work/post-alpha-m00-transport-adapters-v1`
- Baseline control commit: `2b77ffe`
- Command: `python -m pytest -q tests/tier_a/entry/test_entry_boundary_surface.py`
- Outcome: expected red, `15 failed`
- Intended failure class: current entry exports and constructors still select the legacy `HttpApp` / `DeskRuntimeOrchestrator` route and do not expose injected M00 command/query adapters.
- Representative failures: missing `run_command` and `query_command`; `create_app` has no `coordinator` argument; entry source lacks M00 import and contains prohibited legacy imports.
- Admission state: `entry_boundary_surface` is `next_gate_expected_red`; it is excluded from `pre_m00_current` promotion membership.
- Authority checks: proof authority and focused proof-control tests pass (`27 passed`).
- No production source was changed in Unit 1.
