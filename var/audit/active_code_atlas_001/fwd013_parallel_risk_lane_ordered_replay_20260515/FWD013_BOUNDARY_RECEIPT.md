# FWD-013 Boundary Receipt — Parallel risk lane ordered replay

Created UTC: 2026-05-15T01:45:25.781604+00:00

## Scope

Opened by user instruction `proceed with next gate` after FWD-012. Selected row: `FWD-013` / `5.8 Parallel risk lane`.

## Allowed

- Read authority/evidence/source/test/proof files for FWD-013.
- Create FWD-013 manifests, comparison report, proof summary, receipts, and ledger update.
- Mutate tests/source/config/fixtures only if comparison evidence required it.

## Not opened

- FWD-014 / downstream capital deployment authority.
- Broker/order execution, capital deployment sizing, live inventory, exit/close, serial candidate formation, original Atlas/Bridge JSON mutation, generated slice rebuild, dependency mutation, and vocabulary mutation.

## Decision

No FWD-013 source/test/config/fixture mutation was required by the current evidence. Existing parallel-risk proof families were rerun and captured.
