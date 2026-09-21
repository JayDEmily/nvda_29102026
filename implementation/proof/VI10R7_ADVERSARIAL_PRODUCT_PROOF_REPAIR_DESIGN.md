# VI-10R7 adversarial product-proof repair design

## Scope

Repair only Tester Iteration 009 findings `T009-F001..F004`. Preserve all previously accepted proof obligations and keep `src/**` untouched. VI-12R production implementation remains blocked.

## T009-F001 — PostgreSQL COMMIT acknowledgement precedes public return

Add a real-PostgreSQL discriminator that creates a proof-owned synchronous-replication commit barrier:

1. configure a temporary nonexistent synchronous standby name on the dedicated PostgreSQL 17.9 proof server and reload it;
2. start a public-command probe using a unique PostgreSQL `application_name`;
3. observe the server backend enter `SyncRep` wait after the COMMIT request has reached PostgreSQL;
4. prove that no public-return marker is emitted while the server is still waiting for synchronous commit acknowledgement;
5. remove/reload the proof barrier and require the public-return marker only after PostgreSQL releases COMMIT;
6. restore server configuration in `finally` regardless of outcome.

This directly rejects an adapter that flushes COMMIT and returns before consuming successful COMMIT completion.

## T009-F002 — technical PostgreSQL port cannot own semantic meaning

Wrap the actual default PostgreSQL persistence object in a proof-only protocol proxy exposing exactly the nine admitted record operations. Rewire the already-created default owner object graph to use that proxy, then exercise relation and assessment semantics under opposing eligibility authority. The proxy forwards only record operations to the real PostgreSQL adapter and records every call. A default-owner path that requires any adapter-private semantic method becomes unavailable; semantic outcomes must remain owner-derived while stored records remain invariant.

## T009-F003 — complete public Python signature typing

Bind every parameter and return annotation for all six command and five read facets, not only contract/identity parameters. The proof must:

- compare each complete signature against the admitted concrete type shape;
- include `datetime`, positive version integer, optional values, and typed `Sequence[...]` containers where the public seam carries collections;
- reject `Any`, `object`, universal `str`, untyped containers, variadic parameters and permissive unions anywhere on the eleven facets;
- retain the existing static cross-layer negative specimens and add negative cases for non-identity parameters.

## T009-F004 — catalogue-backed Decimal fidelity

Add canonical `R038` (`IBKR` / `EWrapper.tickSize` / Last Size / contracts-shares) as a Decimal native-value canary in U03 and the real PostgreSQL fresh-process restart/readback proof. Use a fractional value with significant trailing zeros and require exact `Decimal` runtime type plus exact decimal tuple/value preservation. This is a source-fidelity proof only and creates no universal Decimal rule, range law, or workbook bounds validation.

## Acceptance

A VI-10R7 successor is eligible for Tester Iteration 010 only if:

- all four repairs are present without weakening existing proof;
- real PostgreSQL 17.9 proof infrastructure is green and product execution remains attributable expected-red only because production symbols are absent;
- architecture/bootstrap promotion remains separately green;
- mypy, Ruff, product-control, dependency/public-seam validation, diff check and strict Git integrity pass;
- physical proof diff contains zero `src/**` production changes;
- the candidate is a genuine new commit/tree preserving rejected predecessors in ordinary Git history.
