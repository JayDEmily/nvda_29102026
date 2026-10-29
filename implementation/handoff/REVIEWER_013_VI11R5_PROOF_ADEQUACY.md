# Reviewer 013 — VI-11R5 / Tester Iteration 008 Fresh Proof-Adequacy Rechallenge

## Role

You are a fresh independent reviewer. Do not inherit Worker reasoning or `VI10R5_ADVERSARIAL_PRODUCT_PROOF_REPAIR_EVIDENCE.md` as authority. Establish proof adequacy from primary authority and physical tests.

## Exact target

Frozen VI-10R5 physical proof candidate:

- commit: `e39740c6ddd24fa1372bde6ca630245285a807d7`
- tree: `dabf8fe94cfc14e74131604a42030514791c10ee`

Repair/source checkpoint / physical parent:

- commit: `96550e119e64d1145d057d98fbdcaed3f9e049b9`

Rejected predecessor reviewed as Tester Iteration 007:

- physical proof: `0c626fb78fa7317fa265bd5ff871dd398c68404d`
- wrapper: `30db3d00f1b9f32215ce1f06b156647e92f1e505`
- submitted archive SHA-256: `c320a72735dfa7b7e034b6cbed20372e03e4e97902868300517fb8560cf1ae73`

## Mandatory read order

1. `GUARDRAILS.md`, root `AGENTS.md`, accepted `EXEC_PLAN.md`, `tests/AGENTS.override.md`.
2. Exact accepted IRB/BICP/IWO.
3. Exact routed METHOD-006 N04, Vocabulary Governance, N06, N18, N15 and N19.
4. `implementation/proof/VI11R4_TESTER_ITERATION_007_DISPOSITION.md`.
5. `implementation/proof/VI10R5_ADVERSARIAL_PRODUCT_PROOF_REPAIR_DESIGN.md`.
6. `implementation/authority/source_signal_catalogue/README.md` only for the Programme Owner-directed catalogue provenance/boundary; it does not enlarge current product semantics.
7. `implementation/proof/VI10R5_ADVERSARIAL_PRODUCT_PROOF_REPAIR_EVIDENCE.md` only as a Worker claim to challenge.
8. Full diff `96550e119e64d1145d057d98fbdcaed3f9e049b9..e39740c6ddd24fa1372bde6ca630245285a807d7` and every admitted product-proof/support file.

No production implementation candidate is part of this review.

## Required independent rechallenge

For every `T007-F001..F007`, construct at least one plausible materially wrong implementation and determine whether the physical proof rejects it. In particular challenge whether a wrong implementation can still:

- keep semantic durable truth in any host path or channel other than PostgreSQL despite the exclusive process boundary, including mount/proc/file-descriptor escapes;
- return a public command before its own transaction commits by using lazy result inspection, another thread/process or deferred work after method return;
- let PostgreSQL persistence own eligibility/relation/outcome decisions while still satisfying the exact storage protocol and counterfactual fresh-adapter reread;
- forget same-assessment-ID conflict state or one ingestion scope's high-water after an A -> B -> A fresh-process sequence;
- fabricate scheduled-capture success/fallback after a failed PostgreSQL write;
- permit overlapping active policy intervals by changing `scope_policy_id`;
- expose any of the six command or five read facets with `Any` or cross-layer-compatible typing that escapes the positive/negative mypy specimens.

Also rechallenge the full BC-014/BC-015 surface and all thirteen current BICP product obligations for materially wrong implementations not named by Tester Iteration 007.

## Boundary

- Do not inspect or author production implementation.
- Expected pre-implementation red is neither a defect nor proof adequacy.
- Do not change IRB/BICP/IWO/METHOD-006 meaning.
- The canonical signal workbook supplies established catalogue IDs/definitions only; do not import its min/max/bounds material or `D001+` implementation into this tranche.
- Product and architecture proof axes remain separate.
- A reviewer PASS would authorise only controlled progression to VI-12R; it would not prove implementation correctness or operational fitness.

## Return contract

Return exactly one of:

- `PASS` — no material proof-adequacy finding remains; or
- `FAIL / RETURN_TO_WORKER` — enumerate each material finding with severity, violated authority, physical proof location, a concrete wrong implementation that can pass, why the proof misses it, and the smallest owning-layer repair.

Bind the review to the exact physical candidate commit/tree and submitted Iteration-008 archive SHA-256.
