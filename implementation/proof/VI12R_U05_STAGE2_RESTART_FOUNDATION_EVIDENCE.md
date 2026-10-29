# VI-12R U05 Stage 2 — PostgreSQL Restart Foundation Evidence

## Disposition

**WORKER STAGE 2 COMPLETE AT IMPLEMENTATION/PROOF LEVEL — NOT U05 ACCEPTANCE**

Stage 2 of the active root `EXEC_PLAN.md` is complete for the exact implementation commit identified
below. This evidence establishes only the Stage-2 PostgreSQL foundation plus the first complete
policy/capture/reconciliation fresh-owner restart slice. It does not claim Stage 3 observation
durability, Stage 4 restarted assessment semantics, whole-U05 closure, independent Tester PASS, or
promotion.

## Exact implementation state described

- branch: `work/u05-restart-architecture`
- Stage-2 implementation/proof commit: `0f707b487951d5c42ae57ad91b682e65901f5ff4`
- Stage-2 implementation/proof tree: `9c65ac00bd31151e188bef4f5e4541e378ada67c`
- Stage-1 handoff base: `28139d45d87ba642712b53c62151ccb503aac1d2`
- active plan on `main`: `4bf4b4feb08412f65216fc95d8615d2cc46eadaf`
- accepted U04 production candidate: `dc3b448191a2b2d3528ffb576b1ebc2c56839991`
- independent Reviewer-032 U04 PASS: `dd42d645b59a62f88cfbc7fba47a75e415b7296f`

The Stage-2 implementation commit changes only:

- `pyproject.toml`;
- `src/nvda_desk/raw_signal_occurrence_truth/api.py`;
- `src/nvda_desk/raw_signal_occurrence_truth/_postgres.py`;
- `tests/bootstrap/test_legacy_exclusion.py`;
- `tests/product/raw_signal/test_u05_stage2_restart_foundation.py`.

No Stage-3 observation persistence implementation is present in this commit.

## Stage-2 proposition established

Against real PostgreSQL, a newly constructed owner with empty process-local semantic state can now,
through the owner public seam:

1. read durable policy state and use the durable policy set for owner-side overlap decisions;
2. retry an already-durable policy identity/content and reject a newly overlapping policy after
   restart;
3. find an already-realised capture through the stable `(scope_policy_ref, slot_start_utc)` identity;
4. preserve same-slot/same-capture idempotency and reject conflicting slot/capture identity reuse;
5. reconcile an explicitly requested missing owed slot after restart;
6. create the capture in its own committed transaction and, only if no current assessment exists,
   create the authorised initial `unknown_not_established` assessment in a later transaction;
7. never turn durable absence into `zero_received` during reconciliation;
8. preserve an already-current assessment rather than creating a second unknown merely because a
   different assessment identity was supplied on a later reconciliation call;
9. propagate transaction/write failure rather than manufacture a semantic fact;
10. preserve a successfully committed capture when the later assessment transaction fails, then let
    a fresh owner recover by appending the missing initial unknown assessment;
11. wait for the persistence transaction context to exit before public success: an injected
    transaction-exit failure causes the public call to fail and the uncommitted capture to disappear;
12. read the committed capture/assessment back through a completely fresh owner; and
13. return an owner object graph whose ordinary public/data attributes do not expose the concrete
    PostgreSQL adapter, transaction or SQL capability.

## Realised ownership and transaction mechanism

The Stage-1 semantic/technical boundary is retained:

- M-owner code decides policy overlap, schedule validity, stable-slot identity semantics and whether
  reconciliation is authorised to create `unknown_not_established`;
- the PostgreSQL adapter supplies only record/query and transaction mechanics;
- policy and stable-slot write paths use correctness locks so the owner evaluates against a durable
  set that cannot race another writer through the checked interval/slot;
- write transactions set `synchronous_commit=on` and return to the public command only after context
  exit commits successfully;
- exceptions roll back and propagate;
- capture and initial-assessment reconciliation intentionally use two transactions, preserving the
  accepted no-cross-kind-atomicity boundary;
- PostgreSQL constraints back identity/referential correctness but do not decide Raw Signal
  semantics.

The accepted U04 append-only technical assessment sink remains a separate `persistence_port`
construction path. The new U05 transaction/query dependency is injected separately as
`durability_port`. This separation was required after regression proof showed that treating the old
U04 append-only sink as the new restart port changed accepted U04 behaviour.

Ordinary restarted U04 assessment derivation is deliberately **not** implemented by Stage 2. When a
U05 `durability_port` owner is used, the ordinary assessment append command remains deferred to
Stage 4 rather than partially persisting a decision derived from process-local observation state.
Only the Stage-2 reconciliation path creates an assessment durably at this stage.

## PostgreSQL physical foundation implemented in Stage 2

The private technical adapter defines only the Stage-2 correctness relations:

- `rsot_capture_scope_policy_v1`;
- `rsot_scheduled_capture_occurrence_v1`;
- `rsot_capture_receipt_presence_assessment_v1`.

The observation relation and NativeValueV1 durable codec are not implemented in Stage 2 and remain
Stage-3 work.

The driver admitted by current programme authority is now the exact runtime dependency pin:

`psycopg[binary]==3.3.4`

`tests/bootstrap/test_legacy_exclusion.py` was correspondingly repaired. Primary authority in
`implementation/authority/VI03_REMAINING_UNKNOWN_IMPACT.md` states that the earlier Psycopg exclusion
proved only the behaviour-neutral kernel state, was not a permanent architectural ban, and must be
re-evaluated after an explicitly admitted production dependency. `VI04_AUTHORITY_CLOSURE.md` then
explicitly admits `psycopg[binary]==3.3.4`. The repaired bootstrap proposition continues to exclude
the other historical runtime dependencies and now requires the exact authorised Psycopg pin.

## Primary authority and evidence inspected

The Worker inspected the current governing and accepted material required for this stage, including:

- `GUARDRAILS.md`;
- root `AGENTS.md` and `tests/AGENTS.override.md`;
- active root `EXEC_PLAN.md`, especially Stage 2;
- `handoff/control/CURRENT_STATE.md`;
- `implementation/architecture/VI12R_U05_STAGE1_RESTART_ARCHITECTURE.md`;
- `implementation/authority/VI04_AUTHORITY_CLOSURE.md`;
- `implementation/work_order/VI05_IMPLEMENTATION_WORK_ORDER_CANDIDATE_001.md`;
- `handoff/authority/IRB_ACCEPTED_IMPLEMENTATION_BRIEF.md`, especially BC-010 through BC-016;
- accepted U01-U04 implementation and product tests;
- `implementation/authority/VI03_REMAINING_UNKNOWN_IMPACT.md` for the bootstrap dependency
  proposition.

The abandoned pre-recovery U05 `_postgres.py`, CP0-CP8 implementation/checkpoint state and old
handoff results were not used as implementation authority or resumed code.

## Exact runtime evidence

Stage-2 runtime proof used the project-preserved U05 proof environment and PostgreSQL runtime:

- Python `3.13.5`;
- Psycopg `3.3.4`;
- PostgreSQL `17.9`;
- PostgreSQL `fsync=on`;
- PostgreSQL `synchronous_commit=on`;
- PostgreSQL `full_page_writes=on`.

The PostgreSQL process was the real local server addressed by `NVDA_TEST_POSTGRES_DSN`; no SQLite,
mock database or process-local substitute was used for the Stage-2 restart tests.

## Validation run against the committed Stage-2 tree

The following validation was rerun after commit `0f707b487951d5c42ae57ad91b682e65901f5ff4`
was created:

1. Stage-2 focused real-PostgreSQL discriminator:
   - `pytest tests/product/raw_signal/test_u05_stage2_restart_foundation.py -q`
   - result: **7 passed**.
2. Accepted U01-U04 regression set:
   - `test_u01_contract_owner_boundary.py`
   - `test_u02_capture_schedule.py`
   - `test_u03_observation_native_temporal.py`
   - `test_u04_receipt_assessment.py`
   - result: **416 passed**.
3. Architecture/bootstrap suite in the exact combined project toolchain:
   - `pytest tests/architecture tests/bootstrap -q`
   - result: **74 passed**.
4. Static typing:
   - mypy `1.20.1` over `src`
   - result: **Success: no issues found in 16 source files**.
5. Ruff over all Stage-2 modified Python paths:
   - result: **All checks passed**.
6. `git diff --check` against the Stage-2 implementation commit parent:
   - result: no whitespace errors.
7. Exact Git identities after the implementation commit:
   - `HEAD` = `0f707b487951d5c42ae57ad91b682e65901f5ff4`;
   - tree = `9c65ac00bd31151e188bef4f5e4541e378ada67c`;
   - `main` = `4bf4b4feb08412f65216fc95d8615d2cc46eadaf`;
   - worktree clean before this evidence/handoff-only close-out change.

## Failures found and resolved during Stage 2

Two issues were found by proof before Stage-2 closure:

1. **Accepted U04 persistence seam regression.** The first wiring treated the old U04 append-only
   assessment persistence fixture as the new U05 transaction/query port. The full U01-U04 regression
   run failed 1 test (`415 passed, 1 failed`). The repair restored the accepted U04 seam and separated
   the U05 durability dependency. Final U01-U04 proof is 416/416.
2. **Premature Stage-4 assessment persistence.** Logic tracing showed that ordinary assessment append
   had been wired to the new durable port even though its restart-sensitive evidence/predecessor
   reconstruction is Stage-4 work. That wiring was removed; the Stage-2 durable assessment write is
   limited to explicit owed-slot reconciliation.

Environment-only command failures were also observed and resolved without changing semantics: one
initial regression invocation used a wrong U03 filename; and isolated proof environments lacking
PyYAML/mypy could not collect the complete architecture suite until the already-preserved exact
project toolchains were combined. These were invocation/environment defects, not product-test
failures.

## Validation boundary

**VERIFIED:** the Stage-2 policy/capture/reconciliation restart slice and checks recorded above for the
exact implementation commit.

**NOT VERIFIED / NOT CLAIMED:**

- durable observation identity, NativeValueV1 fidelity or ingestion high-water after restart
  (Stage 3);
- ordinary receipt-evidence/assessment derivation and predecessor semantics after restart (Stage 4);
- complete U01-U04 restart equivalence (Stage 5);
- full historical U05 product-proof-family green status;
- independent Tester acceptance;
- U05 promotion or programme acceptance.

## Stage boundary / next lawful action

Stage 2 stops here. Stage 3 has not started.

The next lawful engineering action is only a separately authorised Stage-3 execution from this
committed lineage: observation durability and restart semantics. No observation persistence work is
authorised by this Stage-2 close-out itself.
