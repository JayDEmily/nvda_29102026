# VI-12R U05 Stage 1 — Restart Architecture Evidence

## Disposition

**WORKER STAGE 1 COMPLETE AT DESIGN/EVIDENCE LEVEL — NOT U05 ACCEPTANCE**

Stage 1 of the active root `EXEC_PLAN.md` is complete at the exact design commit below. This evidence
records only the restart-architecture/durable-contract proposition required by Stage 1. It does not
claim PostgreSQL production implementation, PostgreSQL integration proof, U05 product acceptance, or
independent Tester acceptance.

## Exact state described

- branch: `work/u05-restart-architecture`
- Stage-1 design commit: `bd5d904e4b94ea29ba0d8b147420d4a086fcdf1b`
- Stage-1 design tree: `19c1d3270a274c687b52d28dd316f0421929d2f7`
- active plan/base commit on `main`: `4bf4b4feb08412f65216fc95d8615d2cc46eadaf`
- accepted U04 production candidate: `dc3b448191a2b2d3528ffb576b1ebc2c56839991`
- accepted U04 production tree: `3c7a42eb215d708a0f8d8db37727133ecc234275`
- independent Reviewer-032 PASS lineage: `dd42d645b59a62f88cfbc7fba47a75e415b7296f`

The only path added between the active plan/base commit and the Stage-1 design commit is:

- `implementation/architecture/VI12R_U05_STAGE1_RESTART_ARCHITECTURE.md`

No `src/**` or U01-U04 product-test path differs from the accepted U04 production source as a result
of Stage 1. `src/nvda_desk/raw_signal_occurrence_truth/_postgres.py` is not tracked on this active
line.

## Semantic proposition established at Worker-design level

The Stage-1 architecture record explains, invariant by invariant, how a completely fresh owner with
empty process-local semantic state can obtain the durable records/queries required to enforce the
accepted restart-sensitive U01-U04 semantics without caller-managed semantic hydration.

The record covers:

- policy identity/idempotency, policy overlap and effective-policy lookup;
- stable owed-slot/capture identity and capture referential readback;
- observation identity, exact NativeValueV1 retry/conflict behaviour and scope-local ingestion
  high-water;
- receipt-relation inputs without making optional relation materialisation durability authority;
- durable eligible evidence needed for assessment;
- assessment same-ID stability, append-only history and immediate-predecessor reconstruction;
- interrupted explicit owed-slot reconciliation;
- referential readback of original policy, capture, observation and assessment facts;
- transaction/commit/failure boundaries and the no-cross-kind-atomicity constraint;
- the non-semantic PostgreSQL/adapter boundary and the public-object-graph bypass constraint;
- the minimum correctness-only physical PostgreSQL relation/type/constraint direction authorised by
  VI-04;
- exact NativeValueV1 durable reconstruction requirements rather than lossy JSON-style coercion.

The selected architecture is query-on-demand durable authority for restart-sensitive decisions,
rather than eager caller/test hydration of process-local owner caches. PostgreSQL/repository code is
restricted to technical record/query mechanics; the M owner remains responsible for overlap,
eligibility, relation, assessment and supersession decisions.

## Primary authority/evidence inspected

The Worker inspected the current governing and accepted primary material required by Stage 1,
including:

- `GUARDRAILS.md`;
- root `AGENTS.md`;
- active root `EXEC_PLAN.md`;
- `handoff/control/CURRENT_STATE.md`;
- `handoff/authority/VI05_IMPLEMENTATION_WORK_ORDER_CANDIDATE_001.md`, including `IWO-U05`;
- `handoff/authority/VI04_AUTHORITY_CLOSURE.md`;
- `handoff/authority/IRB_ACCEPTED_IMPLEMENTATION_BRIEF.md`, including BC-010 through BC-016 and
  especially BC-011;
- accepted U04 implementation at `src/nvda_desk/raw_signal_occurrence_truth/api.py`;
- `implementation/proof/VI13R_U04_REVIEWER_032_DISPOSITION.md` and the accepted U04 lineage needed
  to establish the starting boundary.

Historical abandoned U05/CP material was not adopted as implementation authority or resumable state.

## Verified repository checks

The following checks were actually run against the Stage-1 design commit/state:

1. `git rev-parse HEAD` ->
   `bd5d904e4b94ea29ba0d8b147420d4a086fcdf1b`.
2. `git rev-parse HEAD^{tree}` ->
   `19c1d3270a274c687b52d28dd316f0421929d2f7`.
3. `git rev-parse main` ->
   `4bf4b4feb08412f65216fc95d8615d2cc46eadaf`.
4. `git diff --name-status main..HEAD` showed only
   `A implementation/architecture/VI12R_U05_STAGE1_RESTART_ARCHITECTURE.md`.
5. `git diff --name-status dc3b448191a2b2d3528ffb576b1ebc2c56839991..HEAD -- src/nvda_desk/raw_signal_occurrence_truth tests/product/raw_signal`
   produced no output.
6. The `api.py` blob at accepted U04 and Stage-1 HEAD is identical:
   `b8aa18ee89ecc3d93d25420a8d09ea69075128e2`.
7. `git ls-files --error-unmatch src/nvda_desk/raw_signal_occurrence_truth/_postgres.py` did not
   find a tracked file.
8. The Stage-1 design worktree was clean immediately after the design commit.

## Validation boundary

**VERIFIED:** the Stage-1 design record and Git-state checks above.

**NOT IN SCOPE / NOT RUN:** PostgreSQL runtime/integration tests, U05 production tests, product-suite
regression tests, mypy/Ruff, or a public object-graph test against a concrete adapter. Stage 1 changes
no production source and deliberately precedes PostgreSQL production implementation. Those runtime
claims begin in Stage 2 or later and must not be inferred from this design evidence.

**NOT CLAIMED:** U05 `PASS`, U05 acceptance, U05 promotion, or correctness of an implementation that
does not yet exist on this recovery line.

## Remaining unknowns / blockers

No Stage-1 semantic-authority blocker was established. The Remaining Unknowns preserved by current
authority remain preserved in the architecture record; Stage 1 does not select defaults for them.

If Stage 2 discovers that any preserved unknown is required to make a semantic decision, execution
must stop at that exact authority gap.

## Stage boundary / next lawful action

Stage 1 stops here. Stage 2 is not started by this evidence record.

The next lawful engineering action is only a separately authorised Stage 2 execution from this
committed Stage-1 lineage: PostgreSQL foundation plus the first complete policy/capture/reconciliation
fresh-owner restart path. If the realised Stage-2 adapter proves the Stage-1 contract inadequate, the
Worker must stop and repair Stage 1 rather than accumulating later semantic slices.
