# Reviewer 014 — VI-11R6 / Tester Iteration 009 Fresh Proof-Adequacy Rechallenge

## Role

You are a fresh independent reviewer. Do not inherit Worker reasoning or `VI10R6_ADVERSARIAL_PRODUCT_PROOF_REPAIR_EVIDENCE.md` as authority. Establish proof adequacy from primary authority and physical tests.

## Exact target

Frozen VI-10R6 physical proof candidate:

- commit: `355497c8db9cd1f615539634ddb5fa5bea5d405d`
- tree: `1798b78addf2d81cfd08e1de42944afc94910b92`

Repair/source checkpoint / physical parent:

- commit: `7eb85b097dd4e05705cc781fd102bddf0f6762ca`
- tree: `89ae9abb0a45c76594faf6bdf6c96d8f77293c9f`

Rejected Tester Iteration 008 target preserved in history:

- physical proof: `e39740c6ddd24fa1372bde6ca630245285a807d7`
- wrapper: `432a52689c4b3aaec0d745c801e63335c1196f2c`
- submitted archive SHA-256: `bc3bf766a2e0c524cde887a4e2d5e48eda4728015039a877599d2aca9e24851d`

## Governing material

Read and apply, in authority order:

1. root `GUARDRAILS.md`;
2. applicable `AGENTS.md` / `tests/AGENTS.override.md`;
3. root `EXEC_PLAN.md`;
4. accepted IRB/BICP/IWO and routed METHOD-006 authority;
5. `implementation/authority/VI10R6_SIGNAL_CATALOGUE_CARRIAGE.md` for the narrow programme-authorised `R001`–`R323` carriage clarification;
6. Tester Iteration 008 disposition;
7. the physical proof itself.

Worker evidence/design records are navigation aids, not proof authority.

## Required review challenge

Re-test all five Iteration-008 findings against the new physical proof. For each finding, construct at least one materially wrong implementation and determine whether the physical proof rejects it.

In particular challenge whether a wrong implementation can still:

- return successfully while a forked or separate-session descendant performs the durable commit afterwards;
- let PostgreSQL persistence consult eligibility/relation/outcome policy or rewrite owner-decided meaning while passing direct readback checks;
- widen any of the eleven public command/read facets with `Any`, `object`, universal `str` or a permissive union;
- round, stringify, coerce type/sign/zero/null, or otherwise destroy native numeric fidelity across PostgreSQL restart;
- drop, conflate, fabricate or reinterpret canonical `R001`–`R323` catalogue IDs, including multi-ID logical records, while preserving provider-native/occurrence identity separately.

Also independently establish that:

- product-proof control is still six families / 13 obligations / 13 covered;
- no production `src/**` byte changed in the physical candidate;
- architecture proof remains a separate green axis;
- expected pre-implementation red is caused only by absent production seams, not by a broken test harness or unavailable PostgreSQL proof path.

## Boundary

- Do not inspect or author production implementation as a substitute for proof review.
- Expected pre-implementation red is neither a defect nor proof adequacy.
- Do not change accepted IRB/BICP/IWO/METHOD-006 meaning.
- The catalogue-carriage clarification admits canonical `R001`–`R323` provenance only. Do not import workbook min/max/bounds, concrete provider mapping defaults or `D001+` implementation.
- Product and architecture proof axes remain separate.
- A reviewer PASS would authorise only controlled progression to VI-12R; it would not prove implementation correctness or operational fitness.

## Return contract

Return exactly one of:

- `PASS` — no material proof-adequacy finding remains; or
- `FAIL / RETURN_TO_WORKER` — enumerate each material finding with severity, violated authority, physical proof location, a concrete wrong implementation that can pass, why the proof misses it, and the smallest owning-layer repair.

Bind the review to the exact physical candidate commit/tree and submitted Tester Iteration 009 archive SHA-256 supplied with the package.
