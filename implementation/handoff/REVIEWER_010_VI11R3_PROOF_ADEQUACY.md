# Reviewer 010 — VI-11R3 Fresh Proof-Adequacy Rechallenge

## Role

You are a fresh independent reviewer. Do not inherit Worker 009's reasoning or `VI10R3_ADVERSARIAL_PRODUCT_PROOF_REPAIR_EVIDENCE.md` as authority. Determine from primary authority and physical proof whether plausible materially wrong implementations can still pass.

## Exact target

Frozen VI-10R3 physical proof candidate:

- commit: `ffcbc64b77b66f96c91926b423622281f125d757`
- tree: `7884c38a5edf6a3538bc2acc6a3bc57a079ea888`

Repair/control baseline:

- commit: `d35153c6a15818c7b6b230bda79d07650f58ea6d`
- tree: `34b28cca978ee5dbe39eaae2703458dec1bd9bbb`

Failed predecessor physical proof:

- commit: `56ea445d4bb5055b9fc39114bcd3c529b7f0bae5`
- tree: `b925e086a734492457dd9633a04743aa0c3c0471`

## Mandatory read order

1. `GUARDRAILS.md`, root `AGENTS.md`, accepted root `EXEC_PLAN.md`, `tests/AGENTS.override.md`.
2. Exact accepted IRB/BICP/IWO.
3. Exact six routed METHOD-006 normatives: `N04`, Vocabulary Governance, `N06`, `N18`, `N15`, `N19`.
4. Tester Iteration 005 response/evidence/findings.
5. `implementation/proof/VI10R3_ADVERSARIAL_PRODUCT_PROOF_REPAIR_DESIGN.md`.
6. `implementation/proof/VI10R3_ADVERSARIAL_PRODUCT_PROOF_REPAIR_EVIDENCE.md` only as a Worker claim to challenge.
7. Full diff `d35153c6...ffcbc64b` and every admitted product-proof/support file.

No production implementation candidate is part of this review.

## Required independent rechallenge

For every `T005-F001..F011`, independently construct at least one plausible wrong implementation and determine whether the physical proof rejects it. Do not accept the Worker's mapping merely because a named test exists.

At minimum challenge whether a wrong implementation can:

- make PostgreSQL a gate/audit participant while reconstructing or storing semantics elsewhere, including through identity conventions, local durable state, or a separate service;
- report command success before that command's own transaction commits, including relation/assessment and reconciliation boundaries;
- persist a materially corrupted record while writer/readback agree with each other;
- introduce a semantic-breaking `.v1` field/change or accept aware non-UTC time as UTC;
- forget a scope's ingestion high-water mark after another scope interleaves;
- place eligibility/outcome/relation semantics in any technical persistence path not caught by the proof's mechanism closure;
- let A00 use a caller-selected policy identity instead of the registered/effective authority;
- accept invalid policy activation/deactivation or mishandle the exact v1→v2 slot boundary;
- omit the lower half of the `[start,end)` receipt test or avoid referential capture existence checks;
- count ineligible or out-of-slot raw observations as receipt-presence evidence;
- reconcile the requested capture identity while attaching wrong policy/schedule facts.

Also challenge the full BC-014/BC-015 surface and all thirteen current BICP product obligations for materially wrong implementations not named by Iteration 005.

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

Bind the review to the exact physical candidate commit/tree and submitted archive SHA-256.
