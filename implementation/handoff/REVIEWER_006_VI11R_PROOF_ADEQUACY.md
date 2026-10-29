# Reviewer 006 — VI-11R Fresh Proof-Adequacy Rechallenge

## Role

You are a fresh independent reviewer. Do not inherit Worker 005's reasoning as authority. Review
the physical proof against the exact accepted authority and decide whether plausible materially
wrong implementations could still pass.

## Exact target

Physical successor proof candidate:

- commit: `375e61b73c219a40c9fc2e9684cf3f3e26d25d54`
- tree: `a45d5678aedea4e116f5e5a390b2bb6a128c33e4`

Repair-control baseline:

- commit: `e3fe1344b4b8b87adac47d5a2771c1b66ec6e03f`
- tree: `8b0dee55c6bb050b46bae30611438a778a7cc381`

Failed predecessor proof target:

- commit: `f83efd9b489dbe7072da8c96320504a468c55a1a`
- tree: `beba36d889696915bbcecccd861dab9ab0c1a4cd`

## Read first

1. exact IRB/BICP/IWO;
2. exact six routed METHOD-006 normative files;
3. `tests/AGENTS.override.md` and current product-proof control;
4. Tester Iteration 003 response/evidence/findings;
5. `implementation/proof/VI10R_ADVERSARIAL_PRODUCT_PROOF_REPAIR_DESIGN.md`;
6. target diff `e3fe1344...375e61b7` and every admitted physical product test/support file.

No production implementation is part of this review.

## Required rechallenge

Re-test proof adequacy, not greenness. At minimum independently challenge whether each returned
wrong-implementation class can still pass:

- `T003-F001`: same-process/global-memory or alternative local persistence masquerading as real
  PostgreSQL durability/restart;
- `T003-F002`: private/test-only semantic owner or A00-owned semantics bypassing production M00
  command/read facets;
- `T003-F003`: caller-selected assessment outcomes inconsistent with eligible committed evidence;
- `T003-F004`: overlapping active policy versions;
- `T003-F005`: cross-layer identity substitution accepted by untyped/universal-ID contracts;
- `T003-F006`: silent `.v1` breaking changes in any of the five contracts across requiredness,
  discriminants/allowed values, time/null, identity or provenance.

Also challenge the complete BC-014/BC-015 proof surface and all 13 current BICP product obligations,
not only those six previous findings. A repaired previous finding does not imply overall proof
adequacy.

## Boundary

- Do not inspect or author a production implementation candidate.
- Do not treat the expected pre-implementation red suite as a defect or as proof adequacy.
- Do not modify IRB/BICP/IWO/METHOD-006 meaning.
- Product and architecture proof axes remain separate.
- A PASS authorises only progression from VI-11 into controlled VI-12R implementation; it does not
  establish product implementation or operational fitness.

## Return contract

Return exactly one of:

- `PASS` — no material proof-adequacy finding remains; or
- `FAIL` / `RETURN_TO_WORKER` — enumerate each material finding with severity, violated authority,
  physical proof location, a concrete wrong implementation that could pass, why the proof misses
  it, and the smallest owning-layer repair.

Bind the review to the exact candidate commit/tree and submitted archive SHA-256.
