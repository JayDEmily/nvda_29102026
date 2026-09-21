# VI-10R8 adversarial product-proof repair design

## Scope

Repair only Tester Iteration 010 findings `T010-F001` and `T010-F002`. Preserve all previously accepted/current proof obligations, including the Iteration-010-closed complete public typing and Decimal-fidelity discriminators. Keep `src/**`, IRB/BICP/IWO/METHOD-006 meaning and architecture proof configuration untouched. VI-12R remains blocked.

## Authority rebound

The repair is bounded by:

- IRB BC-001 — M owns semantic persistence/transaction-outcome truth; PostgreSQL adapter is only a technical translator;
- IRB BC-011 — each occurrence or assessment is committed in its own transaction and durable success is claimed only after the relevant transaction commits;
- IRB BC-013 — PostgreSQL/driver/schema/test/adapter cannot decide Raw Signal outcomes;
- IRB BC-015 — real PostgreSQL proof must establish own-transaction commit truth and failure non-fabrication;
- `IA22R01-PROD-009`, `IA17-PROD-001`, `IA17-PROD-011`;
- IWO-U05 — durable-success signal only after commit, with the Psycopg adapter behind the M-owned persistence port;
- N15-P04/P08 — proof level must match the actual durable/state boundary and same-process evidence cannot substitute for restart/durability proof;
- N18-P09 and N19-P04 — semantic write/mechanism separation survives projection and architecture proof must preserve owner-versus-mechanism separation.

## T010-F001 — complete server-side COMMIT-ack discrimination

Retain the existing client PID-tree return-boundary kill/readback test as complementary evidence, but make the server-side SyncRep discriminator cover each durable-success command path separately.

Use one parameterised real-PostgreSQL proof with independent tokens and preconditions for:

1. capture-scope policy registration;
2. scheduled-capture occurrence realisation;
3. raw-observation occurrence admission;
4. zero-received assessment append; and
5. one-or-more-received assessment append after its required durable observation/relation lineage exists.

For each case:

- establish all prerequisite durable records before enabling the proof barrier;
- warm the production PostgreSQL path before barrier installation;
- configure a proof-owned nonexistent synchronous standby and reload PostgreSQL;
- run the selected public command under a unique `application_name`;
- observe the command backend waiting in PostgreSQL `SyncRep` while asserting no public-return marker exists;
- release the server-side barrier;
- require the public-return marker only after PostgreSQL releases COMMIT;
- require no open writer transaction at the frozen public-return boundary;
- read the newly durable record through a fresh public read probe and compare it with precomputed authority-derived expectation;
- restore PostgreSQL configuration in `finally`.

A future implementation that waits for COMMIT acknowledgement on only one command kind while returning early on another must fail at least one parameterised case.

## T010-F002 — structural record-only capability restriction across nested caching forms

Retain the proof-only record-capability proxy, but replace the partial owner-object traversal with recursive capability rewriting/inspection for every owner attribute through the ordinary caching forms the proof admits.

The traversal must:

- replace direct concrete-adapter references with the record-only proxy;
- replace approved bound record methods with the corresponding proxy method;
- recursively rewrite mutable `list` and `dict` values;
- reconstruct/rewrite immutable `tuple`/`frozenset` and mutable `set` elements where they contain approved record capabilities;
- recursively rewrite `functools.partial` function/argument/keyword captures;
- reject any closure capture that can still reach the concrete adapter or a concrete-adapter bound method, rather than attempting unsafe closure-cell mutation;
- recurse through owner-package objects and through ordinary containers encountered from every owner attribute;
- reject private concrete-adapter methods at any nesting depth;
- confirm after rewrite that no concrete-adapter identity/bound-method capability remains reachable through the admitted graph forms.

Add implementation-independent canaries for nested list, dict, tuple, partial and closure capture. The nested list/dict/tuple/partial canaries must demonstrate that private capability cannot survive; the closure canary must fail closed when a closure retains concrete/private adapter capability.

Then retain the opposing-eligibility real-PostgreSQL owner test and require it to operate only through the record-only proxy while identical technical storage facts remain invariant.

## Acceptance

A VI-10R8 successor is eligible for Tester Iteration 011 only if:

- both Iteration-010 findings are physically discriminated without weakening closed or existing proof;
- no `src/**` production byte changes;
- product-proof control still binds six families and all 13 current product obligations;
- product tests collect successfully and the still-unimplemented product remains attributable expected-red rather than failing from proof defects;
- real PostgreSQL execution is used for U05 durability discrimination when the preserved authorised environment is available;
- architecture/bootstrap promotion remains separately green;
- applicable static/dependency/public-seam/diff/integrity checks pass;
- rejected Iteration-010 physical proof remains preserved in ordinary Git history; and
- a fresh Tester Iteration 011 receives a genuinely new immutable physical proof commit/tree.
