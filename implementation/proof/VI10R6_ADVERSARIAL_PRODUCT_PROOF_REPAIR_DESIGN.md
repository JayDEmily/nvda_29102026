# VI-10R6 Adversarial Product Proof Repair Design

## Status

`FROZEN WORKER REPAIR DESIGN — TESTER ITERATION 008 FINDINGS`

## Fixed authority and scope

This repair is downstream of the accepted IRB/BICP/IWO and routed METHOD-006 authorities, the independent Tester Iteration 008 disposition, and the programme-authorised catalogue-carriage clarification in `implementation/authority/VI10R6_SIGNAL_CATALOGUE_CARRIAGE.md`.

The failed Iteration 008 wrapper `432a52689c4b3aaec0d745c801e63335c1196f2c` and physical candidate `e39740c6ddd24fa1372bde6ca630245285a807d7` remain ordinary Git history. VI-12R production implementation remains out of scope until fresh independent proof review returns PASS.

No workbook min/max/bounds law, concrete provider-field mapping, or `D001+` derived behaviour is admitted by this repair.

## Required discriminators

### T008-F001 — whole execution-tree command-return durability

The exact public-command `return` event must freeze the writer and every descendant that could continue durable work after return. The proof uses a dedicated PID namespace with a proof supervisor as PID 1, then stops all writer descendants before exposing the return marker and stops the writer itself. A separate-session forked canary must be unable to emit post-return activity while the tree is frozen. The existing fresh-process readback / immediate-kill durability checks remain.

### T008-F002 — storage semantics invariant under opposing eligibility authority

The real default PostgreSQL storage port must remain record-only. Identical database state is cloned, then opened by owners using opposing eligibility resolvers. Technical storage readback of the identical persisted policy/capture/observation facts must remain identical, while only owner-controlled relation/assessment semantics may differ. The storage adapter must not derive eligibility, receipt relation, or assessment outcome.

### T008-F003 — exact/exhaustive public-facet typing

For all six public command facets and all five read facets, inspect declared type hints for every contract/identity-bearing parameter. Each must resolve to exactly the admitted concrete contract/identity type; widened `Any`, `object`, universal `str`, or widened unions are not acceptable. Existing positive/negative mypy specimens remain additional evidence.

### T008-F004 — native numeric fidelity across PostgreSQL restart

Use native numeric specimens containing zero, high-precision floating values, very small negative values, percentage/rate-like values, and native null. Require exact value and runtime numeric type to survive command storage and fresh-process PostgreSQL readback. These are fidelity canaries only: no numeric plausibility, min/max, rescaling, rounding or sign law is introduced.

### T008-F005 — canonical `R001`–`R323` carriage

`RawObservationOccurrenceV1` must carry optional `raw_signal_catalogue_ids` composed of separately typed `RawSignalCatalogueId` values. Prove canonical endpoints, rejection of malformed/out-of-range/`Dxxx` values, optional absence, non-empty/non-duplicate present collections, multi-ID carriage for one provider logical record, identity non-substitutability, and exact PostgreSQL restart carriage. Catalogue identity remains distinct from provider-native and occurrence identity.

## Acceptance before fresh review

- product-proof control remains exactly six families / 13 obligations / 13 covered;
- all product tests collect without harness errors;
- exact Python 3.13.5 / pytest 9.0.3 / mypy 1.20.1 / Ruff 0.15.11 / Psycopg 3.3.4 dependencies are used;
- real PostgreSQL 17.9 executes U05 with `fsync`, `synchronous_commit`, and `full_page_writes` on;
- proof infrastructure/discriminator tests reachable before implementation are green;
- full pre-implementation product red is attributable only to absent authorised production seams;
- architecture/bootstrap/promotion remain green and separate;
- mypy, Ruff, dependency and public-seam checks remain green;
- physical successor contains zero `src/**` production mutation;
- a later wrapper packages a genuinely new Tester Iteration 009 candidate.
