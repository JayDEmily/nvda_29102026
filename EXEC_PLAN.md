# ExecPlan — U04 Accepted Baseline to U05 PostgreSQL Durability and Restart

## Status

**ACTIVE GOVERNING EXECPLAN — ACCEPTED BY PROGRAMME OWNER 2026-09-26.**

This document is a proposed narrow successor execution plan for one task only:

> advance the accepted Raw Signal Occurrence Truth implementation from the accepted U04 semantic baseline to an independently accepted U05 PostgreSQL durability/restart implementation.

The Programme Owner explicitly accepted this plan and authorised Stage 1 execution on 2026-09-26. This file is the active root `EXEC_PLAN.md`.

This plan intentionally does **not** continue the abandoned post-U04 CP0–CP8 execution/checkpoint state.

---

## 1. Fixed starting boundary

The fixed semantic starting point is the accepted U04 recovery baseline established by current repository governance:

- accepted U04 production candidate: `dc3b448191a2b2d3528ffb576b1ebc2c56839991`;
- accepted U04 production tree: `3c7a42eb215d708a0f8d8db37727133ecc234275`;
- independent Reviewer-032 PASS lineage: `dd42d645b59a62f88cfbc7fba47a75e415b7296f`;
- accepted semantic lineage: U01 through U04;
- U05: **not started** on the active recovery line.

The abandoned U05 implementation, `_postgres.py`, CP0–CP8 checkpoint/workboard state and abandoned U05 cycle evidence/results are `DO_NOT_CARRY_FORWARD` into the new active implementation line. They may be inspected only as historical/forensic evidence when useful to avoid a known failure class. They are not implementation authority and are not resumable execution state.

U01–U04 accepted meaning is not reopened by this plan.

---

## 2. Governing authority

This plan operationalises already-authorised work only. It does not create new Raw Signal semantics.

The governing authority remains, in order:

1. current explicit Programme Owner instruction;
2. `GUARDRAILS.md`;
3. applicable `AGENTS.md` / `AGENTS.override.md`;
4. this ExecPlan if explicitly accepted;
5. accepted task/normative/architecture authority;
6. accepted proof obligations and proof artefacts;
7. implementation/source/configuration;
8. historical evidence.

The existing accepted U05 engineering obligation is `IWO-U05 — PostgreSQL durability, idempotency, failure, restart and referential readback`.

Its primary proof obligations remain:

- `IA22R01-PROD-009`;
- `IA17-PROD-010`;
- persistence-bearing portions of `IA17-PROD-007` and `IA17-PROD-008`;
- supporting `IA17-ARCH-003`.

The accepted U05 purpose remains:

> bind U01–U04 owner facts to real PostgreSQL while preserving semantic ownership and exact transaction claims.

No new semantic meaning may be invented to make durability convenient.

---

## 3. U05 terminal proposition

U05 is acceptable only when evidence establishes the following complete proposition:

> A completely fresh Raw Signal semantic owner, starting with empty process-local semantic state and using the authorised durable PostgreSQL mechanism, preserves the accepted U01–U04 observable semantics through the declared owner public seam. The owner can recover or query the durable information required to make its own semantic decisions after restart; successful durability is claimed only after the relevant transaction commits; failed writes fabricate no semantic fallback; identical retries remain idempotent; conflicting identity reuse fails closed; original owner facts remain referentially readable with required lineage/schedule context; restart reconciliation of explicitly requested owed slots operates from durable state; and a missing owed slot is represented by a durable capture plus `unknown_not_established`, never inferred `zero_received`.

This proposition is not established by proving only that PostgreSQL can write and read records.

---

## 4. Explicit non-goals

U05 does not authorise or claim:

- P01/DMPV3 activation;
- K01 selection;
- provider/API/network integration;
- authoritative replay or re-execution;
- downstream business consumers;
- live external effects/accounts;
- retention/deletion policy;
- RTO/RPO, bounded-recovery, SLA or throughput claims;
- PostgreSQL partitioning or pooling;
- independently designed performance indexes;
- cross-kind atomicity;
- final distribution/version work belonging to later scope;
- reopening accepted U01–U04 semantics.

At any point where U05 requires a still-unresolved authority value rather than an implementation choice, stop and return the exact authority gap.

---

## 5. Failure-prevention laws for this restart

These controls are mandatory because they address the identified post-U04 failure classes.

### 5.1 Reconstruction before storage

Before production PostgreSQL implementation begins, enumerate every accepted U01–U04 invariant whose enforcement depends on process-local semantic state.

For each invariant, record:

- the accepted semantic proposition;
- the process-local state currently used to enforce it;
- the durable fact or relationship required after an empty-process restart;
- whether the owner must reconstruct, enumerate or query that information;
- the owner-level decision that depends on it;
- the public command/read path that proves the restarted behaviour;
- the failure mode if that durable information is absent or ambiguous.

At minimum the inventory must challenge the known state classes implicated by accepted U01–U04 behaviour, including policy overlap/effective-policy state, owed-slot/capture identity, observation identity/retry and sequence state, receipt-evidence eligibility inputs, assessment history/predecessor state and restart reconciliation.

**No production persistence implementation starts until this inventory is complete enough to explain how a completely fresh owner enforces every affected accepted invariant.**

### 5.2 Persistence is mechanism, not semantic owner

PostgreSQL, Psycopg, SQL schema, repository/store and adapter code remain technical mechanisms behind the M-owned persistence boundary.

They may store and retrieve the durable facts/query results required by the owner. They must not decide Raw Signal eligibility, relation truth, assessment outcome, supersession meaning or other M-owned semantic propositions.

The owner/persistence interface must be designed from the reconstruction inventory, not from convenient CRUD methods.

### 5.3 Fresh-owner rule

Every restart discriminator begins from:

- a completely fresh owner instance;
- empty process-local semantic state;
- only the inputs that the authorised production construction/public contract permits;
- the same committed PostgreSQL durable state.

A test or caller may not perform preparatory reads, cache hydration or private state injection merely to make the subsequent semantic command correct unless that operation is itself part of the authorised production contract being proved.

A restart proof that succeeds only after manual semantic hydration is a failure.

### 5.4 Public capability-boundary rule

When the persistence mechanism is first connected to the owner, immediately trace the reachable public object graph.

An ordinary caller must not be able to reach a concrete adapter, repository, connection or mutation capability that can bypass the M-owned semantic command boundary and directly write already-constructed semantic records.

Python underscore naming is not an architectural boundary.

### 5.5 Natural semantic stages, not mechanism checkpoints or micro-tasks

U05 work is decomposed into the smallest **natural semantic stages** that remain substantial enough to execute coherently. The plan must not recreate the abandoned mechanism-local CP model, but it must also not fragment one coherent engineering problem into artificial micro-tasks.

A stage boundary exists where there is a meaningful change in the proposition being established: architecture fixed before production mutation; first end-to-end restart path; observation semantics; assessment semantics; whole-U05 closure; independent acceptance.

A stage is not complete because a table exists, serialization works, commit acknowledgement works, or readback works in isolation. Each implementation stage must establish a coherent public semantic path through a fresh owner against committed durable state.

### 5.6 Git-native resumability

Every materially meaningful Worker state is committed on the U05 work branch.

These commits are resumability/history points, **not acceptance claims**.

Do not accumulate several semantic slices, proof changes or substantial implementation changes as one long dirty overlay.

Each work commit must make it possible to answer:

- what changed since the previous state;
- which semantic proposition the change was intended to establish;
- what proof was actually run;
- what remains unresolved.

### 5.7 Evidence-state identity

Every evidence/handoff record must identify the exact commit/tree or explicitly identified dirty state it describes.

A record must not state that a later slice is “not started” if that slice's implementation already exists in the referenced state.

Before handoff, compare the recorded status against the actual candidate tree.

### 5.8 Governance stability

Once U05 execution begins under this plan, do not redesign the execution methodology underneath the active implementation unless a genuine blocking governance defect is established.

A blocking governance correction must be isolated, explicitly authorised and committed separately before implementation resumes.

Ordinary implementation difficulty is not authority to redesign governance.

### 5.9 Tests discriminate; they do not define the architecture

Existing accepted proof is evidence of the required observable contract. Implementation must not be shaped merely to satisfy test mechanics.

When an implementation-specific false-positive path appears, strengthen the proof at the correct layer without weakening accepted semantics.

Local PostgreSQL propositions do not substitute for fresh-process semantic equivalence.

### 5.10 Logic trace before candidate freeze

Before U05 is frozen for independent review, perform a code-level logic trace through the realised owner → persistence → transaction → fresh-restart/reconciliation paths.

The trace must challenge the actual mechanism independently of the existing tests and specifically ask where any accepted U01–U04 decision still relies on process memory.

A green suite without this trace is insufficient for U05 candidate freeze.

---

## 6. Staged execution sequence

The sequence below is deliberately **coarse enough to preserve coherent engineering work and fine enough to prevent another long, uncommitted U05 overlay**. These are natural semantic stages, not a micro-task checklist and not a resurrection of CP0–CP8.

Every stage has a hard handoff boundary. At that boundary the Worker records what proposition was actually established, commits the meaningful work state on the U05 work branch, and stops before beginning the next stage. The next stage may proceed only from that exact committed state. These are resumability/history commits, not acceptance claims.

### Stage 1 — Restart architecture and durable contract

**Purpose:** resolve the architectural question that the abandoned U05 attempted to discover incrementally during implementation. No substantive PostgreSQL production implementation begins until this stage is coherent.

This stage includes, as one connected design exercise:

- establish and record the exact accepted U04 starting commit/tree and clean work branch;
- confirm abandoned U05 code/checkpoint machinery is absent from the active tree;
- inventory every U01–U04 invariant affected by loss of process memory;
- for each invariant identify the durable fact, relationship, enumeration or query a completely fresh owner requires;
- distinguish reconstruction from direct durable query where that distinction matters;
- derive the minimum owner/persistence port from those semantic needs rather than from CRUD convenience;
- define the minimum correctness-only PostgreSQL relation/type/constraint design;
- define transaction boundaries, commit acknowledgement, failure behaviour and referential readback;
- trace the proposed public object graph and ensure no ordinary caller can reach a persistence mutation capability that bypasses owner semantics;
- identify any Remaining Unknown that would require new semantic authority rather than an implementation choice.

The durable-reconstruction record should cover, at minimum, policy overlap/effective-policy state, owed-slot/capture identity, observation identity/retry/conflict and sequence/high-water state, eligible evidence needed for assessment, assessment history/immediate predecessor, explicit owed-slot reconciliation and referential retrieval of original owner facts.

**Stage exit:** the architecture can explain, invariant by invariant, how a fresh owner makes every restart-sensitive U01–U04 decision without caller-managed hydration. Any unresolved semantic authority gap is returned as `BLOCKED`. The design/evidence state is committed on the U05 work branch before production implementation begins.

### Stage 2 — PostgreSQL foundation and first complete restart path

**Purpose:** prove the architecture works end-to-end before broadening it across all semantic state. This is the first production implementation stage.

Implement only enough of the common PostgreSQL mechanism plus the policy/capture/reconciliation path to demonstrate a real fresh-owner vertical slice. Through the public owner seam and real PostgreSQL, establish that a fresh owner can:

- obtain the durable policy state needed for accepted overlap/effective-policy decisions;
- find an already-existing owed capture by lawful stable slot identity;
- reconcile an explicitly requested missing owed slot from durable state;
- durably create the required capture and initial `unknown_not_established` assessment where authorised;
- never infer `zero_received` from absence of durable evidence;
- claim success only after the transaction creating the semantic fact commits;
- leave no fabricated semantic fact after failed write/rollback;
- perform the path after discarding the original owner and constructing a completely fresh owner, without preparatory semantic hydration.

This stage also re-checks the realised object graph now that a concrete adapter exists. A private name is not sufficient; the concrete adapter/repository/connection must not be caller-reachable as a semantic bypass.

**Stage exit:** one genuine public semantic restart path works against committed PostgreSQL and demonstrates that the architecture is reconstruction-capable rather than merely record-persistent. If the architecture proves inadequate, stop and repair Stage 1 rather than accumulating later state classes. Commit the exact implementation/proof state.

### Stage 3 — Observation durability and restart semantics

**Purpose:** carry the established restart mechanism across the substantial U03 observation state as one coherent semantic unit.

Implement and prove through a completely fresh owner:

- durable reconstruction/readback of the accepted observation fact with NativeValueV1/value/time/provenance fidelity;
- same-identity identical-content retry idempotency against durable state;
- conflicting same-identity reuse fail-closed behaviour;
- recovery/query of the durable sequence/high-water information required by accepted observation semantics;
- correct behaviour where relevant durable predecessor/state already exists before the new process starts;
- failed observation writes leave neither a durable fact nor a fabricated semantic fallback;
- success is attributable to the transaction that committed the observation fact.

The proof must exercise the public production path from empty process-local semantic state; it must not populate the owner with helper reads merely to make the command succeed.

**Stage exit:** the restart-sensitive U03 invariants are enforced from durable state, and no correctness-critical observation identity/high-water state remains process-memory-only. Commit the exact implementation/proof state before proceeding.

### Stage 4 — Receipt evidence, assessment history and restarted U04 semantics

**Purpose:** carry durability across the accepted U04 assessment model while explicitly preventing recurrence of the U04 and abandoned-U05 failure classes.

Implement and prove through a completely fresh owner:

- durable access to admitted observations/evidence required for assessment;
- assessment outcome remains an M-owned semantic decision, not a database decision;
- optional receipt-relation materialisation is not a prerequisite for assessment correctness;
- missing eligibility authority fails closed wherever accepted U04 semantics require it;
- receipt time is never substituted for transaction/system-knowledge visibility;
- assessments remain append-only;
- the immediate predecessor is obtained correctly from durable assessment history;
- same-ID retry remains stable even when later evidence exists;
- a new assessment applies the accepted supersession rule after restart;
- failed assessment writes fabricate no assessment outcome;
- all of the above are exercised without caller/test-managed reconstruction of eligible evidence or predecessor state.

**Stage exit:** the complete accepted U04 assessment/receipt behaviour survives an empty-process restart using the durable contract established in Stage 1. Commit the exact implementation/proof state.

### Stage 5 — Whole-U05 integration, adversarial closure and candidate freeze

**Purpose:** determine whether the separately built semantic areas actually form one coherent U05 implementation. This stage is integration and adversarial closure, not another feature tranche.

From representative committed U01–U04 state:

- discard all owner/process-local semantic state and construct a fresh owner;
- exercise the full required public command and referential-read paths;
- discharge every row of the Stage 1 restart/reconstruction inventory;
- verify original durable facts retain required lineage/schedule context;
- verify policy, capture/reconciliation, observation and assessment decisions compose correctly after restart;
- challenge identical retries and identity conflicts against already-durable state;
- challenge transaction failures so that no semantic empty/unknown/zero fallback is fabricated;
- confirm no cross-kind atomicity or stronger transaction claim is being implied than authority permits;
- re-challenge the complete reachable object graph for persistence bypass;
- run the applicable product and architecture proof axes independently at their required level.

Then perform the mandatory **logic trace** through the realised owner → persistence → transaction → restart/reconciliation paths. Read the actual code path independently of the test suite and ask, for every accepted restart-sensitive decision, where its governing state comes from after process loss.

**Stage exit:** the complete terminal proposition in section 3 is established at Worker-evidence level for one clean committed tree; no known restart-sensitive invariant still depends on lost process memory; evidence and source state agree exactly. Freeze that one exact commit/tree as the U05 candidate.

### Stage 6 — Fresh independent Tester review

**Purpose:** independently challenge the exact frozen U05 candidate rather than continue Worker self-validation.

The Tester receives the governing authority, accepted U01–U04 lineage needed for context, Stage 1 reconstruction/contract record, exact candidate commit/tree/diff, Worker evidence, and relevant historical failure material only as risk evidence.

The Tester must inspect the realised code paths as well as execute the required proof. In particular, independently challenge:

- a completely fresh owner with no helper/fixture hydration;
- durable enforcement of the restart-sensitive U01–U04 invariants;
- transaction/failure claims at the level actually asserted;
- public-object-graph persistence bypass;
- recurrence of previously identified mechanism classes.

The Tester returns exactly `PASS`, `FAIL / RETURN_TO_WORKER`, or `BLOCKED` for the U05 unit. A failure routes a bounded repair on the U05 work lineage followed by a new exact candidate and fresh independent re-review; it does not authorise wholesale redesign or integration of a failed candidate.

### Stage 7 — Promotion and close-out

Only after fresh Tester `PASS`:

- integrate the accepted U05 work lineage into `main` with preserved ancestry;
- record exact accepted candidate, review and promotion identities;
- update current-state/handoff authority so it describes the promoted repository truth;
- verify evidence names the exact promoted state;
- retain all ordinary work/review commits in Git history;
- stop. U06 does not begin under this plan.

---

## 7. Git and state-management discipline

During U05:

- `main` remains the accepted baseline until U05 receives independent acceptance;
- ordinary implementation occurs on one U05 work lineage;
- meaningful intermediate work is committed, even when not accepted;
- WIP/work commits never carry `PASS`, accepted or promoted meaning merely because they exist;
- do not squash/rebase/history-rewrite for tidiness;
- do not keep hundreds of lines of multi-slice production work uncommitted across sessions;
- do not let governance-only commits advance the implementation base invisibly underneath a large dirty overlay;
- every handoff names its exact commit/tree and states whether the worktree was clean;
- failed candidates remain recoverable in Git history.

---

## 8. Evidence discipline

For every semantic slice, evidence must distinguish:

- **VERIFIED:** commands/tests/traces actually run and their observed result;
- **UNPROVED:** required axis not established in the current environment;
- **BLOCKED:** required axis cannot presently be established for an identified reason;
- **NOT IN SCOPE:** proposition not required by the current slice.

Do not convert `UNPROVED` into `PASS` because another axis is green.

Each evidence record must include:

- exact commit/tree;
- exact changed paths;
- semantic proposition under test;
- proof environment where material;
- commands/checks actually run;
- result counts where applicable;
- known limitations;
- next lawful action.

Evidence and source state must agree before handoff.

---

## 9. Mandatory stop conditions

Stop dependent U05 work at the first occurrence of any of the following:

- active baseline/authority cannot be established exactly;
- a U01–U04 invariant has no lawful durable reconstruction/query path;
- a needed value is a Remaining Unknown without authority;
- persistence requires making an M-owned semantic decision;
- fresh-owner correctness requires caller/test-managed semantic hydration;
- an ordinary caller can reach a persistence mutation capability that bypasses the semantic owner;
- real PostgreSQL proof required for the asserted proposition is unavailable and the proposition cannot lawfully be narrowed;
- implementation evidence and recorded checkpoint/handoff state disagree;
- a required transaction/durability claim cannot be attributed to the transaction that created the semantic fact;
- logic trace reveals a material accepted invariant still depends on process-local state after restart;
- fresh Tester identifies an unresolved material defect.

Preserve the last exact proved work commit and the first unmet invariant. Do not continue downstream merely to accumulate progress.

---

## 10. Definition of U05 done

U05 is done only when all of the following are true for one exact committed candidate:

1. accepted U01–U04 semantics remain conserved;
2. every restart-relevant U01–U04 invariant has an explicit durable reconstruction/query mechanism;
3. PostgreSQL remains a non-semantic mechanism behind the M-owned persistence boundary;
4. success is claimed only after the relevant commit;
5. failed writes produce no fabricated semantic fallback;
6. identical retry/conflict semantics operate against durable state;
7. a fresh owner can read original durable facts by domain identity with required lineage/schedule context;
8. restart reconciliation operates from committed durable state;
9. a missing owed slot produces durable capture + `unknown_not_established`, never inferred zero;
10. U04 assessment semantics remain correct after restart without optional relation hydration or receipt-time proxying;
11. the public object graph exposes no persistence mutation bypass;
12. real PostgreSQL evidence establishes the claims for which real PostgreSQL is required;
13. applicable product and architecture proof axes pass independently at their required level;
14. a code-level logic trace finds no unresolved process-memory dependency for the governed restart semantics;
15. exact source/evidence/handoff state is Git-resumable and internally consistent;
16. a fresh independent Tester returns `PASS` on that exact candidate;
17. accepted promotion preserves ancestry and records exact final identities.

Anything less is an intermediate work state, not U05 acceptance.

---

## 11. Deferred work

This plan stops at accepted U05.

U06 A00 governed sequential composition, aggregate/final packaging and later whole-tranche work remain outside this plan and require the then-current governing authority after U05 close-out.
