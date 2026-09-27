# VI-12R U05 Stage 5 — Whole-Restart Candidate Evidence

## Disposition

**WORKER STAGE 5 COMPLETE / EXACT U05 CANDIDATE FROZEN — NOT INDEPENDENTLY ACCEPTED**

Stage 5 of the active root `EXEC_PLAN.md` is complete at Worker-evidence level for the exact
candidate commit/tree identified below. This record establishes the whole-U05 integration,
adversarial-closure and mandatory source-logic-trace proposition required before independent review.
It does **not** claim fresh Tester `PASS`, U05 programme acceptance or promotion to `main`.

## Exact candidate state

- branch: `work/u05-restart-architecture`;
- Stage-5 frozen candidate: `249fb5f2f174b63bd49fe3e749f0e5cacea39d87`;
- candidate tree: `d09bb7cb419289ac4590b34b42196961a8e044fa`;
- candidate parent / Stage-5 authorisation boundary:
  `956a82be19cb0dfb6ab57cac0e6da08cca7e2a95`;
- active plan on `main`: `4bf4b4feb08412f65216fc95d8615d2cc46eadaf`;
- Stage-4 implementation boundary: `a580a4bc336239a73a5bb2a2c8f6a4ccc19d8625`;
- accepted U04 production baseline: `dc3b448191a2b2d3528ffb576b1ebc2c56839991`;
- independent U04 Reviewer-032 PASS: `dd42d645b59a62f88cfbc7fba47a75e415b7296f`.

The frozen Stage-5 candidate changes only proof/configuration paths relative to its Stage-5 parent:

- `config/product_proof/families.yaml`;
- `tests/product/raw_signal/_process_probe.py`;
- `tests/product/raw_signal/test_u05_postgresql_durability.py`;
- `tests/product/raw_signal/test_u05_stage5_whole_restart.py`.

No `src/**` production path changes in Stage 5. The production implementation being frozen is the
already-committed Stage-2 through Stage-4 lineage, now challenged as one integrated U05 system.

## Whole-U05 Worker proposition

For the frozen candidate, the Worker established that a completely fresh M00 owner with empty
process-local semantic state can preserve the accepted restart-sensitive U01-U04 semantics using the
authorised PostgreSQL transaction/query dependency, without caller-managed semantic hydration.

The integrated proof exercises durable policy/capture/observation/assessment facts, relation
re-derivation, stable retry/conflict behaviour, scope-local observation high-water, assessment-chain
predecessor semantics, explicit owed-slot reconciliation, transaction failure/commit barriers and
fresh referential readback through the public owner seam.

The Stage-5 proof also re-challenges the ordinary returned owner object graph for a persistence
mutation bypass using the same bounded object-graph domain independently accepted for U02: ordinary
attributes/slots are traversed, including Python name-mangled slots; arbitrary function-closure
introspection, monkey-patching, `eval`/`exec` and unrestricted metaprogramming are not claimed.

## Mandatory source-level logic trace

The Worker read the realised source path independently of the test suite:

- `src/nvda_desk/raw_signal_occurrence_truth/api.py`;
- `src/nvda_desk/raw_signal_occurrence_truth/_postgres.py`;
- the Stage-1 restart inventory in
  `implementation/architecture/VI12R_U05_STAGE1_RESTART_ARCHITECTURE.md`.

The durable branch of each restart-sensitive public command/read was traced from owner command/read
entry through transaction/query operations and back to the public return boundary. The trace found
no accepted restart-sensitive decision that requires `_OwnerState` after construction with a
`durability_port`. `_OwnerState` remains the accepted non-durable U01-U04 path when that port is not
injected.

### Restart-inventory discharge

| Stage-1 restart-sensitive invariant | Realised durable source after process loss | Stage-5 disposition |
| --- | --- | --- |
| Policy same-ID/version retry/conflict | `register_policy()` reads `get_policy()` before append | VERIFIED |
| Policy interval overlap | write transaction enumerates `list_policies()`; M00 applies `_intervals_overlap` | VERIFIED |
| Effective policy reference | `get_policy_by_ref()` used by capture/relation/assessment paths | VERIFIED |
| Stable owed-slot retry | `get_capture_by_slot(scope_ref, slot_start)` in capture write transaction | VERIFIED |
| Capture identity cannot move slots | `get_capture(capture_id)` before append | VERIFIED |
| Capture referential readback | read transaction `get_capture()` | VERIFIED |
| Observation exact same-ID retry/conflict | `get_observation()` plus M00 `_observations_exactly_equal()` | VERIFIED |
| Scope-local ingestion high-water | `get_observation_high_water(exact_scope)` inside write transaction | VERIFIED |
| High-water remains scope-local | SQL max query is qualified by exact `ingestion_sequence_scope` | VERIFIED |
| Observation exact referential readback | full row reconstruction plus NativeValueV1 binary codec | VERIFIED |
| Receipt relation durable inputs | read transaction obtains observation, capture and effective policy; M00 decides relation | VERIFIED |
| Optional relation materialisation cannot control assessment | no relation table/query; assessment queries durable in-slot observations directly | VERIFIED |
| Assessment capture-local eligible evidence | `list_observations_received_between([slot_start,slot_end))`; M00 applies resolver | VERIFIED |
| Missing eligibility authority fails closed | M00 raises when in-slot evidence needs adjudication and resolver is absent | VERIFIED |
| Assessment same-ID stability after later evidence | `get_assessment()` occurs before new outcome derivation | VERIFIED |
| Assessment changed-content ID conflict | stored capture/as-of/supersession compared before retry return | VERIFIED |
| Immediate-predecessor append-only chain | `list_assessments()` + M00 `_order_assessment_chain()` and predecessor check | VERIFIED |
| Assessment list/readback | `get_assessment()` and `list_assessments()` through fresh read transactions | VERIFIED |
| Reconciliation finds existing owed slot | reconciliation calls durable `realise_capture()` stable-slot path | VERIFIED |
| Missing owed slot -> capture + unknown, never zero | capture commits first; later assessment transaction appends `unknown_not_established` only when chain absent | VERIFIED |
| Interrupted reconciliation resumes | committed capture is rediscovered on retry; assessment absence is queried separately | VERIFIED |
| Original four fact families remain readable | fresh owner direct durable reads for policy/capture/observation/assessment | VERIFIED |

### Ownership and semantic/technical boundary trace

`api.py` retains semantic ownership:

- policy overlap and schedule activity are decided in M00;
- observation exact-content and sequence admissibility are decided in M00;
- receipt-window eligibility and relation existence are decided in M00;
- assessment zero/one outcome and supersession validity are decided in M00;
- restart reconciliation chooses the authorised `unknown_not_established` fact in M00.

`_postgres.py` exposes only transaction plus record/query operations. It stores/reconstructs already
owner-decided records, provides correctness locking/constraints and commits/rolls back transactions;
it does not expose an eligibility, schedule-truth, relation, outcome or supersession decision method.

### Transaction/failure trace

`_PostgresPersistence.transaction()` creates the connection, enables `synchronous_commit=on` for
writes, yields the record/query transaction, commits only after the semantic command body returns,
rolls back on exception and closes the connection. Public durable command paths return only after
that context exits successfully.

Reconciliation intentionally uses the authorised two-transaction shape: capture realisation commits
first; assessment creation follows in its own transaction. A failure after the capture commit leaves
a truthful committed capture and no fabricated assessment. Fresh retry discovers the capture and
creates the missing initial unknown assessment. No cross-kind atomicity is claimed.

## Public-object-graph challenge and bounded proof-domain clarification

During the mandatory logic trace, the Worker observed that Python function closure introspection can
recover a constructor dependency from a stored semantic command closure. That observation initially
looked like the prior U02 ordinary-state bypass class. Primary authority was then re-read before any
production redesign.

The accepted Public Seam Law explicitly does not require prevention of arbitrary metaprogramming,
and independent Reviewer-024 accepted the U02 repair with arbitrary function-closure introspection
expressly outside the proof domain. The Stage-1 U05 contract likewise requires that an ordinary
caller cannot obtain append/SQL capability by following the ordinary returned owner object graph.
The ExecPlan operationalises that accepted boundary; it does not create a stronger Python-security
law.

Accordingly:

- the closure observation is **VERIFIED** but is **NOT a failure under the accepted proof domain**;
- no production indirection/security mechanism was added merely to hide Python closure internals;
- the Stage-5 ordinary graph discriminator resolves name-mangled slots correctly and contains a
  canary that would detect the exact adapter placed in such a slot;
- the realised owner/facets do not expose the injected PostgreSQL port, transaction object or a
  `transaction` method through that admitted ordinary attribute/slot graph.

This distinction is recorded so a future reviewer does not either ignore a real Python property or
silently expand the accepted seam contract into unrestricted introspection resistance.

## Real PostgreSQL and product proof

The configured U05 product-proof family
`tests/product/raw_signal/test_u05_postgresql_durability.py` was repaired only where needed to drive
the current authorised injected transaction/query port rather than the abandoned pre-implementation
record-only/default-adapter shape. The proof still challenges real PostgreSQL durability,
commit-acknowledgement, process loss, failure rollback, cross-process readback, retry/conflict,
assessment history, reconciliation and technical/non-semantic ownership.

The new `test_u05_stage5_whole_restart.py` composes the already-proved Stage-2 through Stage-4 areas
through repeated fresh-owner construction and concludes with fresh referential readback of all four
semantic fact families. Its public-object-graph test uses the bounded ordinary traversal described
above.

## Post-freeze validation against the exact candidate

All results below were rerun after candidate commit
`249fb5f2f174b63bd49fe3e749f0e5cacea39d87` was frozen.

1. Stage-2 + Stage-3 + Stage-4 + Stage-5 real-PostgreSQL restart set:
   - four focused restart files;
   - result: **26 passed**.
2. Configured U05 PostgreSQL durability product family:
   - `tests/product/raw_signal/test_u05_postgresql_durability.py`;
   - collected 55 tests;
   - executed in bounded batches only to stay below the tool-call time ceiling;
   - aggregate result: **55 passed / 0 failed**.
3. Accepted U01-U04 regression set:
   - U01 owner/contract boundary;
   - U02 capture schedule;
   - U03 native/temporal observation;
   - U04 receipt/assessment;
   - result: **416 passed**.
4. Architecture/bootstrap:
   - `pytest tests/architecture tests/bootstrap -q` in the established combined exact toolchain;
   - result: **74 passed**.
5. Static typing:
   - mypy `1.20.1` over `src`;
   - result: **Success: no issues found in 16 source files**.
6. Ruff:
   - `ruff check src tests tools`;
   - result: **All checks passed**.
7. Candidate diff whitespace check:
   - `git diff HEAD^..HEAD --check`;
   - result: no output / pass.
8. Candidate Git identities:
   - `HEAD` = `249fb5f2f174b63bd49fe3e749f0e5cacea39d87`;
   - tree = `d09bb7cb419289ac4590b34b42196961a8e044fa`;
   - `main` = `4bf4b4feb08412f65216fc95d8615d2cc46eadaf`;
   - branch = `work/u05-restart-architecture`;
   - candidate worktree was clean before this evidence/handoff-only close-out change.

## Proof environment

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
- empty `listen_addresses`; Unix-domain-socket proof transport.

No SQLite, mock database or process-local durable substitute was used for the asserted real
PostgreSQL propositions.

## Known limitations and nonclaims

- **NOT INDEPENDENTLY ACCEPTED:** Stage 6 fresh Tester review has not begun.
- **NOT PROMOTED:** `main` intentionally remains at the accepted plan/U04 recovery baseline while the
  U05 work lineage awaits independent review.
- no cross-kind transaction atomicity is claimed;
- no replay-equivalence, RTO/RPO, catch-up deadline, retention or performance/SLA claim is made;
- arbitrary Python function-closure introspection and unrestricted metaprogramming resistance are
  outside the accepted public-seam proof domain;
- PostgreSQL `17.9` is the exact proof environment, not production-version authority.

## Stage boundary / next lawful action

Stage 5 stops here. The exact U05 candidate for independent review is
`249fb5f2f174b63bd49fe3e749f0e5cacea39d87` / tree
`d09bb7cb419289ac4590b34b42196961a8e044fa`.

The next lawful action is **Stage 6 — fresh independent Tester review** in a separate fresh review
context/thread against that exact candidate and its ancestry/evidence. This Worker must not promote
or begin Stage 7 unless and until that independent Tester returns `PASS` on the exact candidate.
