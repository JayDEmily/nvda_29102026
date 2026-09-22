# VI-10R11 adversarial product-proof repair design

## Scope

Repair only accepted Tester Iteration 013 findings `T013-F001` and `T013-F002`. Preserve the failed
VI-10R10 candidate and Tester Iteration 013 continuity in ordinary Git ancestry. Keep `src/**`,
IRB/BICP/IWO/METHOD-006 meaning, product obligations and architecture proof configuration
untouched. Preserve the nine explicit degraded-TCP `UNPROVED` propositions. VI-12R remains blocked.

## T013-F001 — trace the actual post-GO database-write transactions

After the writer has constructed its owner and emitted `semantic_write_ready`, the proof installs a
row trigger on every current non-system regular PostgreSQL relation and records the exact covered
relation OIDs. Each post-`GO` `INSERT`, `UPDATE` or `DELETE` writes an event in the same transaction
containing `pg_current_xact_id()`.

At the frozen public-return boundary, after exact fresh readback, the proof:

1. rejects any newly created durable regular relation that was not in the traced relation set;
2. collects every post-`GO` write transaction identity without inspecting row text; and
3. accepts only the singleton set containing the backend XID observed in PostgreSQL `SyncRep`.

This applies to all five durable-success commands. An implementation cannot satisfy the proof by
placing the marker in an audit/identity transaction and joining a later surrogate payload commit.
A real-PostgreSQL canary deliberately constructs exactly that split representation: the old marker
predicate accepts the audit XID, while the successor write trace exposes both XIDs and rejects it.

## T013-F002 — isolate the concrete adapter outside the owner address space

The opposing-eligibility proof no longer injects an in-process forwarding wrapper. A proof-owned
record-only port starts a separate process and constructs the concrete default PostgreSQL adapter
only inside that process after the fork. The semantic owner receives a parent-side capability with:

- exactly the nine admitted record-storage callables;
- no `_inner` or other concrete adapter object in reachable parent state; and
- a server-side allowlist that rejects every private or non-protocol method name.

The source, true-eligibility and false-eligibility semantic owners all use this boundary. The graph
checker no longer treats any record-only wrapper as opaque, and the rewriter first rejects a
replacement whose own state contains the concrete adapter. Focused canaries prove direct private
dispatch rejection and the exact previous `_port._inner` escape is visible and rejected.

## Acceptance

The successor is eligible for Tester Iteration 014 only if the focused canaries pass, product-proof
control remains six families / 13 of 13 obligations, product collection succeeds, the physical
commit changes no `src/**`, and applicable architecture/static/integrity controls pass. Unavailable
live-PostgreSQL, exact Python-3.13.5 or namespace execution remains explicitly unproved and is not
substituted with a weaker result.
