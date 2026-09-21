# Reviewer 015 — VI-11R7 / Tester Iteration 010 Fresh Proof-Adequacy Rechallenge

## Role

You are a fresh independent reviewer. Do not inherit Worker reasoning or `VI10R7_ADVERSARIAL_PRODUCT_PROOF_REPAIR_EVIDENCE.md` as authority. Establish proof adequacy from primary authority and physical tests.

## Exact target

Frozen VI-10R7 physical proof candidate:

- commit: `816696590912bfac22d9397bef19dc1eb5315f17`
- tree: `561d8610e98c965d43aac02f296b8cee39f02129`

Repair/disposition checkpoint / physical parent:

- commit: `52f6b77bfb96bd72971bbdf83c6b2c731c329271`
- tree: `c068a3e8c0ce2c39a49fbd198947a1d5976b5148`

Rejected Tester Iteration 009 target preserved in history:

- physical proof: `355497c8db9cd1f615539634ddb5fa5bea5d405d`
- wrapper: `ffa57057091b52a9abe54cb87cd1827c8dc76f4f`
- submitted archive SHA-256: `70174e024783e5bdf0420a17e13e815a707be2c5ea3e88fb45f2114780c6bbb7`

## Governing material

Read and apply, in authority order:

1. root `GUARDRAILS.md`;
2. applicable `AGENTS.md` / `tests/AGENTS.override.md`;
3. root `EXEC_PLAN.md`;
4. accepted IRB/BICP/IWO and routed METHOD-006 authority;
5. `implementation/authority/VI10R6_SIGNAL_CATALOGUE_CARRIAGE.md` for the narrow programme-authorised `R001`–`R323` carriage clarification;
6. Tester Iteration 009 disposition;
7. the physical proof itself.

Worker evidence/design records are navigation aids, not proof authority.

## Required review challenge

Re-test all four Iteration-009 findings against the new physical proof. For each finding, construct at least one materially wrong implementation and determine whether the physical proof rejects it.

In particular challenge whether a wrong implementation can still:

- issue/flush COMMIT and publicly return before PostgreSQL has successfully acknowledged transaction completion;
- hide semantic decision-making in a private/cached/closed-over concrete PostgreSQL adapter capability while appearing record-only on its public surface;
- widen any parameter or return on any of the eleven Python-visible public facets to `Any`, `object`, universal `str`, an untyped container or a permissive union;
- coerce catalogue-backed `R038` `Decimal("0.00100")` to float/string/rounded numeric or lose its Decimal coefficient/exponent across PostgreSQL restart/readback.

Independently challenge the two added implementation-independent controls rather than assuming they establish their intended proposition:

- the PostgreSQL `SyncRep` barrier canary must truly prevent server acknowledgement/client commit return until released;
- the record-only graph rewrite canary must reject cached private semantic adapter capability rather than merely rename or hide it.

Also independently establish that:

- product-proof control is still six families / 13 obligations / 13 covered;
- no production `src/**` byte changed in the physical candidate;
- architecture proof remains a separate green axis;
- expected pre-implementation red is caused only by absent production seams, not by a broken test harness or unavailable PostgreSQL proof path;
- previously closed `T008-F001` and `T008-F005` have not regressed.

## Boundary

- Do not inspect or author production implementation as a substitute for proof review.
- Expected pre-implementation red is neither a defect nor proof adequacy.
- Do not change accepted IRB/BICP/IWO/METHOD-006 meaning.
- Canonical `R001`–`R323` provenance remains optional and separately typed. Do not import workbook min/max/bounds, concrete provider mapping defaults or `D001+` implementation.
- Decimal coverage is a native-value fidelity specimen, not a universal Decimal/range law.
- Product and architecture proof axes remain separate.
- A reviewer PASS would authorise only controlled progression to VI-12R; it would not prove implementation correctness or operational fitness.

## Return contract

Return exactly one of:

- `PASS` — no material proof-adequacy finding remains; or
- `FAIL / RETURN_TO_WORKER` — enumerate each material finding with severity, violated authority, physical proof location, a concrete wrong implementation that can pass, why the proof misses it, and the smallest owning-layer repair.

Bind the review to the exact physical candidate commit/tree and submitted Tester Iteration 010 archive SHA-256 supplied with the package.
