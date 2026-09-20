# Reviewer 012 — VI-11R4 / Tester Iteration 007 Fresh Proof-Adequacy Rechallenge

## Role

You are a fresh independent reviewer. Do not inherit Worker 011's reasoning or `VI10R4_ADVERSARIAL_PRODUCT_PROOF_REPAIR_EVIDENCE.md` as authority. Establish proof adequacy from primary authority and physical tests.

## Exact target

Frozen VI-10R4 physical proof candidate:

- commit: `0c626fb78fa7317fa265bd5ff871dd398c68404d`
- tree: `df10fd0e42178dfb7e6fabe0fd9a8e3a3a3249f6`

Repair/control baseline:

- commit: `4aee3dfde5ff0c9f83a113e5f2fb792f53f22981`

Rejected predecessor reviewed as Tester Iteration 006:

- physical proof: `ffcbc64b77b66f96c91926b423622281f125d757`
- wrapper: `d50bc2393078b584b722fb2bf4ba692f055c40ad`
- rejected archive SHA-256: `9340562c57ba7fb156676835740ea48195a880d0579604daf7ba55458c05ce0d`

## Mandatory read order

1. `GUARDRAILS.md`, root `AGENTS.md`, accepted `EXEC_PLAN.md`, `tests/AGENTS.override.md`.
2. Exact accepted IRB/BICP/IWO.
3. Exact routed METHOD-006 N04, Vocabulary Governance, N06, N18, N15 and N19.
4. `implementation/proof/VI11R3_TESTER_ITERATION_006_DISPOSITION.md`.
5. `implementation/proof/VI10R4_ADVERSARIAL_PRODUCT_PROOF_REPAIR_DESIGN.md`.
6. `implementation/proof/VI10R4_ADVERSARIAL_PRODUCT_PROOF_REPAIR_EVIDENCE.md` only as a Worker claim to challenge.
7. Full diff `4aee3dfde5ff0c9f83a113e5f2fb792f53f22981..0c626fb78fa7317fa265bd5ff871dd398c68404d` and every admitted product-proof/support file.

No production implementation candidate is part of this review.

## Required independent rechallenge

For every `T006-F001..F009`, construct at least one plausible materially wrong implementation and determine whether the physical proof rejects it. In particular challenge whether a wrong implementation can still:

- use PostgreSQL only as a gate/audit participant while semantic durable truth is reconstructed or sourced elsewhere, including after PostgreSQL database cloning and source removal;
- return API success before that command's own durable transaction commits;
- hide Raw Signal eligibility/relation/assessment semantics in a technical persistence helper outside the proof closure;
- accept unproved `.v1` keyword material via `**kwargs` or another compatibility escape;
- accept a correctly typed observation identity that does not correspond to durable observation authority;
- let eligible receipt evidence for one capture change another capture's assessment;
- forget policy/capture/assessment/ingestion high-water invariants across fresh-process restart;
- return an assessment after restart with any canonical field changed or omitted;
- mishandle exact start/end microseconds or one-microsecond-invalid schedule/policy grid boundaries.

Also rechallenge the full BC-014/BC-015 surface and all thirteen current BICP product obligations for materially wrong implementations not named by Tester Iteration 006.

## Boundary

- Do not inspect or author production implementation.
- Expected pre-implementation red is neither a defect nor proof adequacy.
- Do not change IRB/BICP/IWO/METHOD-006 meaning.
- Product and architecture proof axes remain separate.
- A reviewer PASS would authorise only controlled progression to VI-12R; it would not prove implementation correctness or operational fitness.

## Return contract

Return exactly one of:

- `PASS` — no material proof-adequacy finding remains; or
- `FAIL / RETURN_TO_WORKER` — enumerate each material finding with severity, violated authority, physical proof location, a concrete wrong implementation that can pass, why the proof misses it, and the smallest owning-layer repair.

Bind the review to the exact physical candidate commit/tree and submitted Iteration-007 archive SHA-256.
