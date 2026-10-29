# VI-10R10 adversarial product-proof repair design

## Scope

Repair only Tester Iteration 012 findings `T012-F001` and `T012-F002`. Preserve the failed
VI-10R9 candidate, all earlier proof discriminators and the nine explicit degraded-TCP
`UNPROVED` propositions. Keep `src/**`, IRB/BICP/IWO/METHOD-006 meaning, product obligations and
architecture proof configuration untouched. VI-12R remains blocked.

## T012-F001 — server transaction identity bound to semantic storage

The proof records `pg_stat_activity.backend_xid` for the uniquely named writer while it is blocked
in `SyncRep`. After acknowledgement, public-return freezing and fresh readback of the exact
expected record, it searches every non-system PostgreSQL base table for the record's unique
semantic identity marker and reads each matching row's `xmin`.

The durable-success proof accepts only the singleton set `{waiting_backend_xid}`. Therefore:

- a setup/schema transaction with no semantic row fails because no expected identity is bound to
  the waited transaction;
- an audit transaction copying the identity followed by a later semantic transaction fails because
  the marker spans two transaction identities; and
- a semantic write in a later transaction cannot inherit acknowledgement from the earlier wait.

A real-PostgreSQL canary writes the same identity in separate audit and semantic commits and proves
that the correlation exposes both transaction identities. A separate pure discriminator canary
proves the two-transaction set is rejected.

## T012-F002 — inject first and reject weak capability

The opposing-eligibility storage proof obtains each concrete default PostgreSQL port from a donor
owner, wraps it in the exact record-only proxy, then constructs a new semantic owner through the
already-authorised `persistence_port` injection seam. The semantic owner never receives the
concrete port for later post-hoc replacement.

Both residual graph helpers also fail closed on:

- live `weakref.ref` objects resolving to the concrete adapter;
- `weakref.WeakMethod` objects resolving to its bound methods;
- `weakref.ProxyType`; and
- `weakref.CallableProxyType`.

Implementation-independent canaries remove the direct port first, require the post-rewrite graph
checker to detect each weak capability, and require the rewriter to reject it.

## Acceptance

The successor is eligible for Tester Iteration 013 only if the new focused canaries pass,
product-proof control remains six families / 13 of 13 obligations, product collection succeeds,
there are no `src/**` changes, and applicable architecture/static/integrity controls pass. Any
unavailable live-PostgreSQL, exact Python-3.13.5 or namespace execution remains explicitly
unproved; it is not substituted with a weaker result.
