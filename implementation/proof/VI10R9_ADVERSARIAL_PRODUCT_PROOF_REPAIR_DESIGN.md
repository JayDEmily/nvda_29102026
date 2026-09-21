# VI-10R9 adversarial product-proof repair design

## Scope

Repair only Tester Iteration 011 findings `T011-F001` and `T011-F002`. Preserve all earlier proof
discriminators and the explicit degraded-TCP caveat. Keep `src/**`, IRB/BICP/IWO/METHOD-006
meaning, product obligations and architecture proof configuration untouched. VI-12R remains
blocked.

## T011-F001 — semantic-write transaction handshake

For all five durable-success command paths, the child must complete owner construction and command
input preparation before emitting `semantic_write_ready`. The parent must:

1. start the child while the PostgreSQL synchronous-replication barrier is off;
2. wait for the child's `READY` marker;
3. install and confirm the proof-owned unavailable-standby barrier;
4. send `GO`;
5. observe that uniquely named backend in `SyncRep` with no public-return marker; and
6. release the barrier before accepting public success and fresh readback.

An independent real-PostgreSQL canary must deliberately commit an owner-setup transaction before
`READY`, verify that setup row, then establish that only the post-`GO` transaction enters
`SyncRep`. A separate structural canary must bind all five boundary actions to the sequence
`_owner` -> `_await_semantic_write_release` -> `_observe_public_method_return`.

## T011-F002 — fail-closed external capability storage

Retain the record-only proxy and recursive instance/container rewrite, but extend both the rewriter
and post-rewrite checker across the concrete non-instance paths identified by the tester:

- inspect class and MRO namespaces without mutating shared class state;
- inspect declared slots without invoking arbitrary descriptors;
- inspect function defaults, keyword defaults, closures and only referenced global names;
- inspect reachable module namespaces while avoiding recursive traversal into unrelated modules;
- reject any class/module/global/slotted path retaining the adapter identity or a bound adapter
  capability; and
- continue rewriting admitted public record methods only where the storage is safely mutable and
  instance-owned.

Implementation-independent canaries must cover the tester's exact class-cache escape, slotted
state, a referenced global function and reachable module storage. Shared namespaces fail closed
rather than being mutated.

## Acceptance

The successor is eligible for Tester Iteration 012 only if the new canaries pass, product-proof
control remains six families / 13 of 13 obligations, product collection succeeds, degraded real
PostgreSQL execution remains attributable expected-red, no `src/**` byte changes, and applicable
architecture/static/integrity controls remain green or any unavailable exact runtime is stated
without substitution.
