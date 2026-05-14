# TEST_FALSE_POSITIVE_RESISTANCE_AUDIT_001 Tier A mutation/fault probe plan

## Scope

This plan covers a bounded representative mutation/fault queue for Tier A tests that were smoke-only or weak before assertion-strength hardening.

The probes target the test/proof surfaces that previously lacked direct observable assertions. They do not use current runtime output as the oracle.

## Planned probes

| Probe | Protected surface | Temporary mutation/fault | Expected failing test | Expected failure reason | Revert method |
|---|---|---|---|---|---|
| `P1_wrong_module_helper` | module helper identity | mutate `_require_module` in `tests/tier_a/analysis/test_replay_evaluation_surface.py` to return `json` for every request | `test_replay_evaluation_surface_is_present` | module-name assertion rejects wrong module | `git restore tests/tier_a/analysis/test_replay_evaluation_surface.py` |
| `P2_wrong_attr_helper` | attribute helper identity | mutate `_require_attr` in `tests/tier_a/calendar_operational/test_calendar_operational_surface.py` to return `object()` | `test_calendar_operational_surfaces_are_present` | attribute identity assertion rejects wrong object | `git restore tests/tier_a/calendar_operational/test_calendar_operational_surface.py` |
| `P3_forbidden_ingress_import` | forbidden external client import boundary | prepend `import requests` to `src/nvda_desk/adapters/ingress/market_snapshot_feed.py` | `test_current_ingress_adapters_do_not_import_concrete_network_clients` | forbidden import boundary assertion reports non-disjoint imported roots | `git restore src/nvda_desk/adapters/ingress/market_snapshot_feed.py` |
| `P4_missing_fixture_root_path` | governed fixture-root path | mutate fixture path to `fixtures/missing_dmp_v3` in `tests/tier_a/parallel_risk/test_parallel_risk_dmp_fixture_root.py` | `test_dmp_v3_fixture_root_is_present_for_parallel_risk_shell_proofs` | path-parts/existence assertion rejects wrong fixture path | `git restore tests/tier_a/parallel_risk/test_parallel_risk_dmp_fixture_root.py` |
| `P5_observability_reserved_package_present` | observability package remains absent | temporarily create `src/nvda_desk/observability/` | `test_observability_package_home_remains_absent` | reserved-package absence assertion fails | remove temporary directory |

## Non-claims

- This is a bounded representative probe queue, not exhaustive proof for all 381 Tier A tests.
- Runtime implementation, dependency changes, VENV creation, `black`, `ruff`, and vocabulary admission remain closed.
- Mutation/fault files must be reverted before any commit.
