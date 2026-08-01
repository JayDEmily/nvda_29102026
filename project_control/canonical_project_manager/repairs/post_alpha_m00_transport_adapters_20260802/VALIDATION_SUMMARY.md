# Post-alpha M00 Transport Adapter Validation Summary

## Outcome

`PASS:ALPHA_DEBT_001_RESOLVED`

The canonical CLI and ASGI entry surfaces now translate exact M00
`ApplicationCommand` and `ApplicationQuery` payloads through one explicitly
injected `RunCoordinator`. They no longer select `HttpApp`, `api.deps` or
`DeskRuntimeOrchestrator`. Those broad surfaces remain compatibility evidence;
they were not silently repaired, deleted or promoted.

The commit containing this summary is the final evidence-bearing closeout commit.
It must reproduce the commands and outcomes below from a clean worktree before
checkpoint/public closeout is claimed.

## Accepted scope

- CLI `run` and `query` JSON translation into M00 contracts.
- ASGI `GET /health`, `POST /commands/run`, and `POST /queries/review`.
- Explicit keyword-only coordinator injection for CLI and ASGI.
- Deterministic transport failures: malformed JSON 400; invalid M00 contract
  422; unsupported method 405; unknown path 404.
- Exact M00 static import quarantine permitting only `entry/cli.py` and
  `entry/asgi.py` outside the M00 package.
- Test-admission and promotion reconciliation for the new current blocker.

## Explicit exclusions retained

- no live data, broker, durable-state, deployment or Tier C claim;
- no raw-source-to-M03 composition;
- no M01–M13 owner-semantic changes;
- no broad legacy API/orchestrator removal or repair;
- no global vocabulary-debt work.

## Validation chain

Environment:

- CPython `3.13.5`;
- 38 compatible installed distributions;
- project installed non-editably from the accepted V6 runtime and V4 dev/build
  wheelhouses;
- installed-package smoke resolves `nvda_desk` from `.venv/site-packages`;
- installed entry smoke resolves `nvda_desk.entry` from `.venv/site-packages`,
  requires coordinator injection and serves mechanical health without invoking
  command/query execution.

Commands:

```text
make install-offline RUNTIME_WHEELHOUSE_ZIP=<accepted-v6-runtime.zip> DEV_WHEELHOUSE_ZIP=<accepted-v4-dev.zip>
make installed-package-smoke
make promotion-gate PROMOTION_RECEIPT=var/proof_receipts/post_alpha_transport_adapter_closeout.json
.venv/bin/python scripts/run_promotion_gate.py --verify-receipt var/proof_receipts/post_alpha_transport_adapter_closeout.json
.venv/bin/python -m pytest -q tests/tier_b
make format-check
make lint
make compile
git diff --check
git status --porcelain
```

Observed on clean semantic closeout commit
`3f939c98e1c4a4308c3c379ff4d1b699c48320f0`:

- authority: 196 families, 198 physical test paths, 68 proof blocks;
- current promotion: 15 proof blocks, 15 blocking families, 17 test paths;
- Tier A aggregate: 15/15 blocks, 769 tests passed, zero skips;
- Tier B: 85 passed;
- Black: 473 scoped files unchanged;
- Ruff: zero findings;
- compileall: passed;
- promotion evidence hash:
  `a81a1e2b9ec52d8e6819584bdb1caf4e6a4fac9796b3778b030afc1ed06b97e0`;
- receipt file SHA-256:
  `1f80018a8ba0b277c61a709aaa967ae7e28fa30068ba1e6f1e0dfaec603ebe90`;
- Git pre/post branch and commit in the receipt matched and were clean.

## Git and authority closeout

- branch: `work/post-alpha-m00-transport-adapters-v1`;
- baseline: `ef4aa1ae556df07871eca4ef93777edc189af8ed`;
- subordinate pack: `POST-ALPHA-M00-TRANSPORT-ADAPTERS-V1`;
- pack state: closed;
- canonical plan state remains
  `COMPLETE:ALPHA_CONSOLIDATED_WITH_EXPLICIT_DEBT`;
- `ALPHA-DEBT-001`: `RESOLVED_POST_ALPHA`;
- remaining material-debt rows remain unchanged.
