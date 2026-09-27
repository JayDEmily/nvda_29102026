# VI-12R U05 Stage 4 — Receipt Evidence, Assessment History and Restart Evidence

## Status

**WORKER STAGE-4 COMPLETE — STAGE 5 NOT STARTED — NOT U05 ACCEPTANCE**

This record closes Stage 4 of the active root `EXEC_PLAN.md` only. It records Worker evidence for
fresh-owner receipt-evidence derivation, durable assessment evidence/history and restarted accepted
U04 semantics on the exact committed Stage-4 implementation/proof state. It does not claim whole-U05
integration/adversarial closure, Stage-5 candidate freeze, independent Tester acceptance or
promotion.

## Binding state

- branch: `work/u05-restart-architecture`;
- Stage-3 handoff parent: `298e74b5d9fa1f5ea30549b567e875c385e668a4`;
- Stage-4 implementation/proof commit: `a580a4bc336239a73a5bb2a2c8f6a4ccc19d8625`;
- Stage-4 implementation/proof tree: `60a6da53b194db3c02a20351319a476369b22f53`;
- active plan on `main`: `4bf4b4feb08412f65216fc95d8615d2cc46eadaf`;
- accepted U04 production candidate: `dc3b448191a2b2d3528ffb576b1ebc2c56839991`;
- independent Reviewer-032 U04 PASS: `dd42d645b59a62f88cfbc7fba47a75e415b7296f`.

The Stage-4 implementation commit changes only:

- `src/nvda_desk/raw_signal_occurrence_truth/api.py`;
- `src/nvda_desk/raw_signal_occurrence_truth/_postgres.py`;
- `tests/product/raw_signal/test_u05_stage4_assessment_restart.py`.

No Stage-5 whole-U05 candidate-freeze or Tester work is introduced by this commit.

## Stage-4 proposition established

Against real PostgreSQL, a completely fresh owner with empty process-local semantic state can now,
through the owner public seam:

1. re-derive an optional `CaptureReceiptEvidenceRelationV1` from durable observation, capture and
   effective-policy facts without a persisted relation cache/table;
2. preserve the accepted no-relation result for out-of-slot or ineligible observations and reject a
   mismatched effective policy lineage;
3. derive an assessment from durable capture-local in-slot observation evidence without first
   materialising the optional receipt relation;
4. apply the separately injected eligibility authority in M00 and keep the database non-semantic;
5. fail closed when in-slot durable evidence requires eligibility adjudication but no eligibility
   authority is present, without writing a fabricated zero assessment;
6. preserve lawful `zero_received` for durable in-slot evidence adjudicated ineligible;
7. avoid the rejected U04 receipt-time/system-knowledge proxy: an admitted durable observation is not
   filtered out merely because its `received_ts_utc` is later than the supplied
   `evidence_as_of_ts_utc`;
8. read same-ID durable assessment state before recomputing outcome, so retry remains stable even
   after later evidence exists;
9. reject conflicting reuse of an existing assessment identity;
10. reconstruct the append-only capture-local assessment chain from durable history and require a
    new assessment to supersede exactly the immediate predecessor;
11. treat a reconciliation-created durable `unknown_not_established` assessment as the lawful
    immediate predecessor for a later U04 assessment;
12. read individual assessments and ordered assessment history from a fresh owner;
13. preserve the accepted fail-closed read behaviour for a nonexistent capture assessment list;
14. roll back a failed normal assessment write so no assessment outcome remains durable;
15. return normal assessment success only after transaction-context exit/commit acknowledgement;
16. collapse concurrent identical same-ID root attempts to one durable assessment; and
17. prevent two concurrent distinct successors from branching one predecessor.

## Realised ownership and transaction mechanism

The Stage-1 durable contract remains the governing mechanism.

For durable receipt-relation derivation the M-owner:

- opens a read transaction;
- reads the exact durable observation and capture by domain identity;
- checks that the supplied `scope_policy_ref` is the capture's effective policy reference;
- reads that exact durable policy;
- applies the accepted half-open capture receipt window and separately injected eligibility resolver;
- constructs the relation in M00 only when the accepted semantic conditions are met.

No relation table is added and no relation cache is hydrated. Repeated fresh-owner relation derivation
therefore depends only on durable U01-U03 facts plus the admitted eligibility authority.

For a durable ordinary assessment the M-owner:

- validates the typed command inputs;
- opens one write transaction;
- checks for an already-durable same assessment identity before new semantic derivation;
- reads the durable capture and effective policy;
- obtains and M00-orders the durable capture-local assessment history;
- uses the assessment-history query's existing correctness lock to serialize predecessor
  read/check/write;
- re-reads the assessment identity under that lock so a concurrent same-ID writer resolves to
  owner-level retry/conflict semantics;
- validates first-assessment/immediate-predecessor supersession law in M00;
- queries durable observations only by the capture's exact `[slot_start_utc, slot_end_utc)` receipt
  interval;
- invokes the admitted eligibility resolver in M00 for those candidate observations;
- derives exactly `zero_received` or `one_or_more_received` in M00;
- appends the already-decided assessment record through the technical persistence transaction; and
- returns public success only after the transaction context exits and PostgreSQL commits.

The adapter does not decide eligibility, assessment outcome or supersession meaning. PostgreSQL
constraints remain correctness backstops: assessment identity is primary-key unique; one root per
capture is unique; and one predecessor cannot acquire multiple successors. No UPDATE/DELETE semantic
operation is introduced.

## Durable evidence query added

Stage 4 adds only the Stage-1-authorised technical observation-window query:

- `received_ts_utc >= slot_start_utc`;
- `received_ts_utc < slot_end_utc`.

It does **not** compare `received_ts_utc` with `evidence_as_of_ts_utc`. This preserves Reviewer-032's
accepted U04 boundary: the current authority does not provide a historical system-knowledge/commit
clock, and receipt time cannot be substituted for one.

## Accepted predecessor behaviour conserved

The non-durable U01-U04 path remains unchanged when no U05 `durability_port` is injected. The exact
accepted U01-U04 regression set remains 416/416 green after Stage 4.

The legacy U04 `persistence_port` remains a separate append-only technical sink and remains mutually
exclusive with the U05 `durability_port`; Stage 4 does not reinterpret that accepted U04 seam as the
new transactional port.

## Concurrency challenge

The Stage-4 real-PostgreSQL proof includes two concurrent assessment cases through fresh public owner
instances:

- two simultaneous identical attempts for the same root assessment identity both resolve to the one
  durable assessment;
- after that root exists, two simultaneous distinct successor identities both naming that root cannot
  branch it: one successor is stored and the other is rejected by the M-owned immediate-predecessor
  rule after serialization.

This establishes the Stage-1 assessment-chain physical correctness proposition for the realised
mechanism without creating a throughput/performance claim.

## Primary authority and evidence inspected

The Worker inspected the current governing and accepted material required for this stage, including:

- `GUARDRAILS.md`;
- root `AGENTS.md` and `tests/AGENTS.override.md`;
- active root `EXEC_PLAN.md`, especially Stage 4;
- `handoff/control/CURRENT_STATE.md`;
- `implementation/architecture/VI12R_U05_STAGE1_RESTART_ARCHITECTURE.md`;
- Stage-2 and Stage-3 U05 evidence records;
- accepted `IRB_ACCEPTED_IMPLEMENTATION_BRIEF.md` BC-007, BC-008, BC-011 and BC-013/016 boundary;
- `VI04_AUTHORITY_CLOSURE.md`;
- `VI05_IMPLEMENTATION_WORK_ORDER_CANDIDATE_001.md` IWO-U04 and IWO-U05;
- accepted U04 Worker repair evidence and Reviewer-031/032 dispositions;
- accepted U01-U04 production/product tests.

The abandoned pre-recovery U05 implementation, CP0-CP8 checkpoint state and abandoned U05 result
records were not resumed or used as implementation authority.

## Exact runtime evidence

Stage-4 runtime proof used the preserved U05 proof environment:

- Python `3.13.5`;
- pytest `9.0.3`;
- mypy `1.20.1`;
- Ruff `0.15.11`;
- Psycopg `3.3.4`;
- PostgreSQL `17.9`;
- `server_encoding=UTF8`;
- `fsync=on`;
- `synchronous_commit=on`;
- `full_page_writes=on`;
- empty `listen_addresses` with Unix-domain-socket transport.

No SQLite, mock database or process-local persistence substitute was used for the Stage-4 restart
proof.

## Validation rerun against the committed Stage-4 tree

All results below were rerun after
`a580a4bc336239a73a5bb2a2c8f6a4ccc19d8625` was committed.

1. Stage-4 focused real-PostgreSQL discriminator:
   - `pytest tests/product/raw_signal/test_u05_stage4_assessment_restart.py -q`;
   - result: **12 passed**.
2. Stage-2 + Stage-3 + Stage-4 real-PostgreSQL restart set:
   - `test_u05_stage2_restart_foundation.py`;
   - `test_u05_stage3_observation_restart.py`;
   - `test_u05_stage4_assessment_restart.py`;
   - result: **24 passed**.
3. Accepted U01-U04 regression set:
   - `test_u01_contract_owner_boundary.py`;
   - `test_u02_capture_schedule.py`;
   - `test_u03_observation_native_temporal.py`;
   - `test_u04_receipt_assessment.py`;
   - result: **416 passed**.
4. Architecture/bootstrap suite:
   - `pytest tests/architecture tests/bootstrap -q` in the established combined Python 3.13.5
     environment with repository `src` and exact proof-venv packages on `PYTHONPATH`;
   - result: **74 passed**.
5. Static typing:
   - mypy `1.20.1` over `src` in the established combined exact project toolchain;
   - result: **Success: no issues found in 16 source files**.
6. Ruff over the Stage-4 modified Python paths:
   - result: **All checks passed**.
7. `git diff HEAD^..HEAD --check`:
   - result: no whitespace errors.
8. Exact Git state after implementation commit:
   - `HEAD` = `a580a4bc336239a73a5bb2a2c8f6a4ccc19d8625`;
   - tree = `60a6da53b194db3c02a20351319a476369b22f53`;
   - parent = `298e74b5d9fa1f5ea30549b567e875c385e668a4`;
   - `main` = `4bf4b4feb08412f65216fc95d8615d2cc46eadaf`;
   - worktree clean before this evidence/handoff-only close-out change.

## Environment-only validation issues

Two architecture/bootstrap invocations failed before the final 74/74 run because the combined
sandbox environment was composed incorrectly:

1. one invocation omitted repository `src` from `PYTHONPATH`, so an architecture subprocess could
   not import `nvda_desk` (73 tests passed and one environment-dependent subprocess test failed);
2. a later chained invocation sourced the proof environment before invoking unqualified `python`, so
   `python` resolved to the isolated proof venv rather than the host Python containing project-pinned
   PyYAML 6.0.3; collection then stopped with ten `ModuleNotFoundError: yaml` errors.

The final command used explicit host `/opt/pyvenv/bin/python` plus both repository `src` and the exact
proof-venv site-packages on `PYTHONPATH`, matching the established Stage-2/3 combined-toolchain
pattern, and passed 74/74. No test, authority or semantic condition was weakened.

The first direct mypy invocation likewise used the isolated proof venv and reported the known PyYAML
stub/environment gap in addition to two genuine Stage-4 local-variable typing collisions. The two
Stage-4 collisions were repaired. Final mypy in the established combined environment is clean across
all 16 source files.

## Logic-trace boundary

The realised durable relation path was read through independently of the tests:

`owner.commands.derive_capture_receipt_evidence_relation`
→ read transaction
→ durable observation/capture/effective-policy identity queries
→ M-owned capture-window check
→ admitted eligibility authority
→ M-owned optional relation construction
→ transaction exit.

The realised ordinary assessment path was read through independently of the tests:

`owner.commands.append_capture_receipt_presence_assessment`
→ write transaction
→ durable same-ID read
→ durable capture/effective-policy reads
→ durable assessment-history query/correctness lock
→ same-ID re-read under lock
→ M-owned immediate-predecessor validation
→ durable in-slot observation query
→ admitted eligibility authority
→ M-owned outcome construction
→ technical assessment insert
→ transaction context exit/commit
→ public success.

The corresponding assessment reads are durable identity/history queries, with history ordering and
chain-integrity validation performed in M00.

No correctness-critical relation/evidence/assessment identity or predecessor state in these durable
paths is sourced from process-local `_OwnerState`.

## Validation boundary

**VERIFIED:** Stage-4 fresh-owner optional relation derivation, durable assessment evidence/outcome,
missing-authority fail-closed behaviour, stable same-ID retry, durable immediate-predecessor chain,
reconciliation predecessor, assessment readback/history, assessment rollback/commit acknowledgement,
and bounded concurrent chain integrity for the exact implementation commit above.

**NOT VERIFIED / NOT CLAIMED:**

- whole-U05 integrated restart equivalence across all Stage-1 inventory rows (Stage 5);
- Stage-5 adversarial closure and mandatory whole-path logic trace;
- exact U05 candidate freeze;
- independent Tester acceptance;
- U05 promotion or programme acceptance.

## Stage boundary / next lawful action

Stage 4 stops here. Stage 5 has not started.

The next lawful engineering action is only a separately authorised Stage-5 execution from this
committed lineage: whole-U05 integration, adversarial closure and candidate freeze. This Stage-4
close-out does not itself authorise that work.
