# TEST_FALSE_POSITIVE_RESISTANCE_AUDIT_001 Tier A assertion-strength hardening receipt

## Scope

- Physical Tier A pytest files under `tests/tier_a/`.
- Gate: `TEST_FALSE_POSITIVE_RESISTANCE_AUDIT_001_TIER_A_REMAINING_ASSERTION_STRENGTH_AUDIT`.
- Assertion-shape hardening only; no runtime/source/dependency/VENV/black/ruff changes.

## Pre-state

- Pre-hardening audit classified `38` smoke-only tests and `6` weak-assertion tests.
- Pre-hardening files needing follow-up: `41`.

## Post-state

- Tier A pytest files: `95`
- Tier A test functions: `381`
- `strong behavioural assertion`: `381`
- Files needing follow-up: `0`
- Files provisionally assertion-strong by this audit: `95`

## Result

No smoke-only, weak-assertion, harness-only, or dangerous false-positive-risk Tier A test functions remain under this assertion-shape audit.

## Non-claims

- This does not prove current code correctness.
- This does not prove full Tier A false-positive resistance.
- Known-bad specimens, controlled mutation/fault probes, and determinism evidence remain required before trust promotion.
