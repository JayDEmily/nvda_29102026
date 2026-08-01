# Unit 8 — Final validation and closeout

**Date:** 2026-08-01
**Branch:** `work/m00-testing-guardrail-repair-v1`
**Initial clean installed validation commit:** `cfd4f0eda798278c5c35aed62df36153cd1441a5`
**Outcome:** PASS

## Environment

- CPython: `3.13.5`
- Runtime wheelhouse SHA-256: `6e4459f4e5508303bdb2e03bcca7701ee72e640f36a716c20b3cd6b0c09b0b42`
- Dev/build wheelhouse SHA-256: `d71a1f5f22aaaa588a59012833c8d797258ea1505feec37e77d7948c818cc249`
- Lock export SHA-256: `cb20225ed8c83217cd2b0f8136dcf70ff4f3406083f3d691449a5621d2f7dd8e`
- Installed distributions: 38; `uv pip check` passed
- Environment receipt Git state: clean branch and commit, `dirty: false`

## Installed-package evidence

```text
installed-package-smoke=PASS .venv/lib/python3.13/site-packages/nvda_desk/__init__.py
installed-m00-smoke=PASS .venv/lib/python3.13/site-packages/nvda_desk/m00_application_shell/__init__.py
```

The installed M00 package exports exactly `ApplicationCommand`, `ApplicationQuery`, `ApplicationRunReceipt` and `RunCoordinator`.

## Aggregate and shadow proof

```text
promotion_gate=PASS set=pre_m00_current blocks=14/14 tests=754
promotion_receipt=PASS var/proof_receipts/pre_m00_current.json
evidence_hash=24fdc517b63b9cf1d5267687cce16dc8581fc0b790d44838edbae5c59529b887
skipped_tests=0
Tier B at initial installed commit: 83 passed
Closeout-control Tier B before final commit: 84 passed
Black: 473 files unchanged
Ruff: zero findings
```

The stable promotion-set key is retained for historical receipt continuity; its authoritative claim and membership now cover the exact current alpha proof through M00.

## Closeout state

The installed aggregate and all closeout controls pass. The final clean closeout commit and its regenerated receipt are recorded in the downloadable checkpoint manifest. Units 0–8 pass and the subordinate repair plan is closed. The canonical ExecPlan becomes the sole current authority and is ready for final alpha consolidation. Live brokerage, durable operations, production readiness and profitability remain unproved and out of scope.
