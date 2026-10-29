# Reviewer 008 — VI-11R2 Fresh Proof-Adequacy Rechallenge

## Role

You are a fresh independent reviewer. Do not inherit Worker 007's reasoning or the VI-10R2 evidence record as authority. Determine from primary authority and physical proof whether plausible materially wrong implementations can still pass.

## Exact target

Frozen VI-10R2 physical proof candidate:

- commit: `56ea445d4bb5055b9fc39114bcd3c529b7f0bae5`
- tree: `b925e086a734492457dd9633a04743aa0c3c0471`

Repair/control baseline:

- commit: `a4c5ebc0c242c446ce14fee2c341e72ca2764212`
- tree: `d5a812678aea2de65876f6f77368f92e795ef411`

Prior failed VI-10R physical proof:

- commit: `375e61b73c219a40c9fc2e9684cf3f3e26d25d54`
- tree: `a45d5678aedea4e116f5e5a390b2bb6a128c33e4`

## Mandatory read order

1. `GUARDRAILS.md`, root `AGENTS.md`, accepted root `EXEC_PLAN.md` and `tests/AGENTS.override.md`.
2. Exact accepted IRB/BICP/IWO.
3. Exact six routed METHOD-006 normative files (`N04`, Vocabulary Governance, `N06`, `N18`, `N15`, `N19`).
4. Tester Iteration 004 response/evidence/findings.
5. `implementation/proof/VI10R2_ADVERSARIAL_PRODUCT_PROOF_REPAIR_DESIGN.md`.
6. `implementation/proof/VI10R2_ADVERSARIAL_PRODUCT_PROOF_REPAIR_EVIDENCE.md` as a worker claim to challenge, not authority.
7. Full diff `a4c5ebc0...56ea445d` and every admitted product-proof/support file.

No production implementation candidate is part of this review.

## Required independent rechallenge

Re-test proof adequacy, not greenness. For each `T004-F001..F011`, independently construct at least one plausible wrong implementation and determine whether the physical proof would reject it.

At minimum challenge:

- whether PostgreSQL could still be a heartbeat/audit dependency while semantics are reconstructed or stored elsewhere, including after the proof's correlated PostgreSQL-state deletion;
- whether any occurrence/assessment can report durable success without its own committed transaction;
- whether complete original facts can be reconstructed incorrectly yet pass fresh-process readback;
- whether a universal lexical/string identity representation can satisfy the same-payload substitution matrix;
- whether any breaking `.v1` change in requiredness, finite discriminants/allowed values, UTC/time/null, identity or provenance semantics can escape U01;
- whether same policy ID/version content can mutate;
- whether any optional provider metadata value can be dropped/normalised when present;
- whether local ingestion ordering can regress or be incorrectly globalised;
- whether relation eligibility can use an observation or policy other than the exact effective authority while preserving superficially correct lineage;
- whether repository/adapter/persistence mechanisms can decide relation/assessment semantics behind the M00 façade;
- whether A00 can preserve call order while miswiring any material semantic argument or ID.

Also challenge the complete BC-014/BC-015 surface and all 13 current BICP product obligations, including materially wrong implementations not named by Iteration 004.

## Boundary

- Do not inspect or author a production implementation candidate.
- Do not treat the expected pre-implementation red suite as a defect or as proof adequacy.
- Do not modify IRB/BICP/IWO/METHOD-006 meaning.
- Product and architecture proof axes remain separate.
- A `PASS` authorises only progression into controlled VI-12R implementation; it does not establish implementation correctness or operational fitness.

## Return contract

Return exactly one of:

- `PASS` — no material proof-adequacy finding remains; or
- `FAIL / RETURN_TO_WORKER` — enumerate every material finding with severity, violated authority, physical proof location, concrete wrong implementation that can pass, why the proof misses it, and smallest owning-layer repair.

Bind the review to the exact candidate commit/tree and submitted archive SHA-256.
