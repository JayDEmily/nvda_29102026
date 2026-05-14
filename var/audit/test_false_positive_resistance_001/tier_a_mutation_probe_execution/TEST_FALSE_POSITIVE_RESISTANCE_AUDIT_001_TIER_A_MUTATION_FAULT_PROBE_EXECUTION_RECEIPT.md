# TEST_FALSE_POSITIVE_RESISTANCE_AUDIT_001 Tier A mutation/fault probe execution receipt

## Summary

- Probe count: `5`
- Killed probes: `5` / `5`
- Expected reason observed: `5` / `5`
- Baseline after revert status: `0`
- Baseline after revert passed: `True`

| Probe | Status | Killed | Expected reason observed |
|---|---:|---|---|
| `P1_wrong_module_helper` | `1` | `True` | `True` |
| `P2_wrong_attr_helper` | `1` | `True` | `True` |
| `P3_forbidden_ingress_import` | `1` | `True` | `True` |
| `P4_missing_fixture_root_path` | `1` | `True` | `True` |
| `P5_observability_reserved_package_present` | `1` | `True` | `True` |

## Revert proof

- All temporary mutation/fault file changes were reverted before this receipt was written.
- Targeted baseline after revert passed according to `targeted_baseline_after_probe_reverts.status`.

## Non-claims

- This is representative mutation/fault evidence for previously weak assertion paths, not exhaustive full-suite trust proof.
- Current runtime correctness is not claimed.

## Determinism repeats after mutation reverts

- Repeat statuses: `[0, 0, 0]`
- Determinism passed: `True`
