# Unit 5 diagnostic pre-M00 baseline

Date: 2026-08-01
Branch: `work/m00-testing-guardrail-repair-v1`
Evidence commit: `1d657e7c7e5c9f007f22f1c37e5b5c77725630be`

## Aggregate current-blocking set

Command surface:

```text
python scripts/run_promotion_gate.py \
  --set pre_m00_current \
  --receipt var/proof_receipts/pre_m00_current-diagnostic.json \
  --timeout 90
```

Observed receipt:

```text
status: PASS
proof blocks: 13/13
passed tests: 738
skipped tests: 0
failed blocks: 0
duration: 41.539098 seconds
pre-run Git state: clean
post-run Git state: clean
branch/commit unchanged: yes
evidence hash: 54d658bc011a0bf4cb3c488e03c7539c2d358ea383dbc8671584ca76b3c12f2a
```

Receipt verification:

```text
promotion_receipt=PASS var/proof_receipts/pre_m00_current-diagnostic.json
```

The receipt is intentionally ignored local evidence and is not committed. Its environment identity records `/opt/pyvenv/bin/python`, not a repository-created `.venv`; therefore this is diagnostic evidence only.

## Tier B shadow

```text
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /opt/pyvenv/bin/python -m pytest -q tests/tier_b
78 passed in 43.85s
```

## Aggregate-runner defects found and repaired during Unit 5

- pipe-based output capture could leave the parent waiting on inherited descriptors;
- proof subprocesses were not isolated into their own sessions;
- undeclared ambient pytest plugins could alter or stall proof execution;
- residual proof process groups were not detected or terminated.

The runner now uses temporary-file capture, isolated sessions, forced pytest plugin-autoload disablement, and fail-closed residual-process-group detection. Contract proof: 29 targeted control tests passed after the final repair.

## Classification

**Current module proof:** green diagnostically.

**Authoritative promotion:** blocked because the repository's frozen environment cannot be materialised in this worker. The configured internal mirror returned HTTP 404 and public PyPI DNS resolution is unavailable. No alternative dependency set or copied environment was substituted.
