# VI-10R4 Adversarial Product Proof Repair Design

## Status

`ACTIVE WORKER REPAIR — TESTER ITERATION 006`

## Fixed authority and scope

This repair is downstream of the accepted IRB/BICP/IWO and the routed METHOD-006 authorities. It may mutate only product-proof control/tests/support/evidence. Production `src/**`, architecture authority/proof and accepted semantic meaning are out of scope.

The failed physical predecessor `ffcbc64b77b66f96c91926b423622281f125d757` remains ordinary Git history.

## Required discriminators

### T006-F001 — PostgreSQL is semantic durable source, not merely a gate

Add a PostgreSQL-native database-clone transfer proof: write high-entropy facts to an isolated source database, clone only PostgreSQL durable state into a new database identity, make the original database unavailable, and require fresh-process exact readback from the clone. The reader receives query identity but not the writer's high-entropy facts. A separate non-PostgreSQL semantic store keyed by the original DSN cannot satisfy the clone readback.

### T006-F002 — command success follows its own commit

For each durable command family, expose the public-command return immediately from a hold-open child, terminate that process without graceful release immediately after the result is observed, then require a fresh process to read the exact fact. This discriminates a command that returns and schedules commit afterward in the same process.

### T006-F003 — persistence cannot own Raw Signal decisions

Replace filename/import-seed assumptions with runtime discovery of the actual default persistence-port type plus a static dependency closure rooted at that type. Prohibit dynamic import escape from the technical closure and scan every reachable local helper for eligibility/relation/assessment decision logic. Retain the injected semantic-blind technical port proof.

### T006-F004 — closed `.v1` contracts reject unknown keyword material

For all five public `.v1` contracts, inject an unproved keyword field and require fail-closed behaviour. This is behavioural and remains valid even if a framework constructor exposes `**kwargs` internally.

### T006-F005 — typed-but-nonexistent observation authority

Use a correctly typed observation-occurrence identity that is not durably admitted and require relation derivation to reject it without invoking eligibility authority.

### T006-F006 — assessment evidence is capture-local

Create two captures under lawful authority, attach eligible committed receipt evidence only to capture A, and require capture A to assess one-or-more while capture B remains zero at the same evidence-as-of time.

### T006-F007 — restart-persistent invariants

Across fresh processes prove at least: immutable same-policy/version conflict still rejects; stable capture slot identity conflict still rejects; assessment immediate-predecessor law still rejects stale predecessor; same-scope ingestion high-water survives restart while an independent scope may use a lower sequence.

### T006-F008 — exact restart assessment readback

Compare the complete canonical recovered assessment, including identity, capture reference, exact outcome, evidence-as-of timestamp, units/concept/contract and lawful absence of supersedes reference.

### T006-F009 — exact interval and schedule-grid edges

Physically discriminate receipt at exact slot start, one microsecond before slot end, slot end itself, and one microsecond before slot start. Separately reject capture/policy grid times displaced by one microsecond from the required `:00/:30` boundaries.

## Acceptance before fresh review

- product-proof validator remains exact 6 families / 13 obligations;
- all physical product tests collect without harness errors;
- real PostgreSQL 17.9 path executes the strengthened U05 surface;
- pre-implementation product proof remains attributable red only because production seams are absent;
- architecture/bootstrap and promotion remain green and separate;
- mypy, Ruff, dependency and public-seam checks remain green;
- physical successor is one immutable commit with zero `src/**` changes;
- reviewer wrapper is a later control/evidence-only commit;
- the next package is explicitly Tester Iteration 007 and has new Git/archive identities.
