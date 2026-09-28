# ExecPlan — VI-14 through VI-18 Final Bounded-Implementation Closure

## Status

**DRAFT — successor root ExecPlan for Programme Owner review.**

This plan is authored from accepted/promoted U06 state on branch
`work/vi14-vi18-final-closure-plan`.

It does not become the active planning authority until explicitly accepted by the Programme Owner
and integrated into `main` under ordinary Git history. Until then, the completed U06 ExecPlan remains
historical current-main planning state and continues to require `STOP`.

Upon explicit acceptance and promotion of this successor plan:

- the completed U06 ExecPlan is superseded as active planning authority;
- it remains recoverable in ordinary Git history and is not destructively removed;
- this file becomes the single active root planning authority for VI-14 through VI-18;
- no change to `GUARDRAILS.md` or `AGENTS.md` is required or authorised by this plan.

---

## 1. Purpose and terminal boundary

The purpose of this ExecPlan is to complete the remaining accepted bounded-implementation successor
work after U01-U06 implementation acceptance and promotion.

The remaining programme gates are exactly:

- VI-14 — material interaction/direct-boundary closure;
- VI-15 — exact aggregate promotion and truthful packaging;
- VI-16 — fresh whole-BICP semantic review;
- VI-17 — integration / authority / provenance audit;
- VI-18 — freeze verified bounded implementation and STOP.

This plan does **not** create a U07, reopen accepted U01-U06 semantics, commission production,
activate downstream trading capability, select inactive modules, add provider/network integration,
or broaden the accepted Raw Signal Occurrence Truth BICP.

Terminal success means only that the exact BICP-admitted Raw Signal Occurrence Truth bounded
implementation has completed the accepted VI-14 through VI-18 closure sequence and is frozen with
exact proof, package, provenance and recovery identities.

After VI-18 terminal closure, **STOP**.

---

## 2. Fixed starting boundary

The planning base is the accepted/promoted U06 `main` state:

- base branch: `main`;
- base commit: `ed94f745effd65050f03d921ad0ae30769877206`;
- base tree: `d8e2587352be34823db214b0196203a747edafcd`;
- U06 independently accepted production/proof candidate:
  `8462630277b04d431ad393e2b73039cacb5d6247`;
- U06 candidate tree: `0a01dacbf54f61bd7f60cf5e68cc350c3cf8d0c6`;
- U06 independent Tester disposition / promotion lineage:
  `562767529235cedff77d3e740a259fab9d88716e`;
- U06 Stage-6 close-out commit on `main`:
  `ed94f745effd65050f03d921ad0ae30769877206`.

At the base state:

- U01-U06 accepted implementation semantics are closed for the scope governed by their accepted
  plans and review evidence;
- no U07 exists in the accepted IWO;
- the completed U06 ExecPlan explicitly stops before VI-14;
- current `pyproject.toml` still contains distribution metadata
  `nvda-architecture-kernel==0.1.0`, but accepted BICP/IWO authority explicitly leaves final
  distribution naming/version metadata unresolved until VI-15 authority closure.

The VI-14 through VI-18 programme must consume this exact accepted state rather than rerun accepted
U01-U06 work merely because later closure needs aggregate evidence.

---

## 3. Governing authority

### 3.1 Repository governance

Current repository governance remains:

1. current explicit Programme Owner instruction;
2. `GUARDRAILS.md`;
3. applicable `AGENTS.md` / `AGENTS.override.md`;
4. explicitly accepted current root `EXEC_PLAN.md`;
5. accepted normative/domain authority;
6. tests and proof derived from that authority;
7. source/configuration/schema state;
8. historical evidence.

`GUARDRAILS.md` is frozen during ordinary project execution and explicitly delegates current gates,
leaves, dependencies, acceptance conditions and progress to the accepted root `EXEC_PLAN.md`.

Root `AGENTS.md` likewise identifies the accepted root `EXEC_PLAN.md` as the single active planning
document and does not define an alternative gate structure.

`README.md` preserves the repository's existing Worker/Tester cycle and current-state routing model.
This plan does not create a new actor type or parallel review architecture.

### 3.2 Accepted bounded semantic authority

The plan remains bound to:

- accepted BICP JSON:
  `handoff/authority/BICP_CANDIDATE_005.json`, SHA-256
  `5b99cead41fd8d3d372b5ed2ef4558065328b814e0a94c3680162fc6594df5ed`;
- accepted BICP Markdown:
  `handoff/authority/BICP_CANDIDATE_005.md`, SHA-256
  `6b2906b92e11bf09fd7f8b188e8ed6555a0a5ae61636909f676f84827601d21f`;
- accepted IWO JSON:
  `handoff/authority/VI05_IMPLEMENTATION_WORK_ORDER_CANDIDATE_001.json`, SHA-256
  `a673ff05bc58870fdfca49167482aabe4647889d7750fd1b49805c7064ef7eed`;
- accepted IWO Markdown:
  `handoff/authority/VI05_IMPLEMENTATION_WORK_ORDER_CANDIDATE_001.md`, SHA-256
  `b23fec7e83eace6353272f92b983160c2ab768043640d15d7ee1fb88f270ca0e`;
- G03 contract: `handoff/macro_gates/GATE_03_VERIFIED_BOUNDED_IMPLEMENTATION.md`;
- G03 execution binding: `handoff/macro_gates/GATE_03_BINDING.md`;
- accepted U01-U06 implementation/review/promotion lineage in ordinary Git history.

The accepted IWO states that it is complete only when all accepted VI leaves through VI-18 are
discharged. VI-18 PASS remains bounded implementation closure only, not broader NVDA completion.

### 3.3 Historical programme plan

The earlier accepted broad successor ExecPlan remains historical planning evidence for the intended
VI-14 through VI-18 semantics. Its relevant gate definitions are conserved here where they remain
consistent with current authority.

Historical planning labels and prior completion claims do not themselves establish current truth.
This successor plan binds them to the current accepted U06 state and current primary evidence.

---

## 4. Existing execution architecture — do not reinvent it

The repository already has a Worker/Tester operating model. This plan preserves it.

For each substantive leaf:

1. a `WORKER` executes the authorised leaf on one work branch from the then-current accepted `main`;
2. the Worker freezes one exact candidate commit/tree and records evidence;
3. a fresh `TESTER` independently challenges that exact candidate against the leaf's authority and
   acceptance proposition;
4. Tester disposition is exactly `PASS`, `FAIL / RETURN_TO_WORKER`, or `BLOCKED`;
5. `PASS` permits preserved-ancestry promotion of that exact accepted lineage to `main` under the
   standing accepted branch/promotion discipline;
6. `FAIL / RETURN_TO_WORKER` returns only the bounded defect/class to the Worker; repair creates a new
   exact candidate followed by fresh independent re-review;
7. `BLOCKED` stops dependent execution at the first unresolved blocker.

Do not create an additional auditor/reviewer role. Where a leaf is itself an audit or review, the
Worker prepares the exact candidate/evidence surface and the Tester performs the independent
challenge.

Completed review cycles remain immutable. Current-state routing must continue to use the existing
`WORKER_` / `TESTER_` cycle mechanism.

---

## 5. Planning law for the remaining tranche

### 5.1 Natural leaves only

Leaves are independently provable semantic obligations, not arbitrary chunks of work.

The VI-14 through VI-18 decomposition below contains seven leaves because current evidence supports
seven natural acceptance boundaries:

1. VI-14-L1 — integrated material interaction/direct-boundary closure;
2. VI-15-L1 — final distribution/version authority closure and exact metadata application;
3. VI-15-L2 — complete aggregate promotion and truthful package/install proof;
4. VI-16-L1 — whole-BICP semantic review;
5. VI-17-L1 — authority/lineage reconstruction;
6. VI-17-L2 — provenance/environment/repository-integrity audit;
7. VI-18-L1 — final freeze, recovery artefact and STOP.

No additional split is authorised merely for symmetry, receipt production or convenience.

If execution proves that one leaf contains two materially independent semantic propositions whose
failure/repair boundaries cannot be managed safely together, the current plan may be amended only
with explicit Programme Owner authority before downstream execution.

### 5.2 Preserve accepted evidence; close only what remains

VI-14 and later work must not treat U05/U06 acceptance as if it never happened.

Accepted U05/U06 evidence already exercises substantial parts of the historical VI-14 risk surface,
including real PostgreSQL durability/restart/readback behaviour and real production A00->M00
composition. VI-14 therefore begins with evidence reconciliation against the historical VI-14
proposition and executes only genuinely unproved integrated axes.

Re-running a validation because it is required to establish the final current aggregate is lawful.
Rebuilding accepted implementation semantics merely because the old broad plan predates their
closure is not.

### 5.3 No hidden authority defaults

A Remaining Unknown may not be converted into implementation or packaging convenience.

The explicit known VI-15 authority stop is final distribution naming/version metadata. Current
`pyproject.toml` values are repository state, not final authority. VI-15-L1 must stop for explicit
Programme Owner authority before final metadata is chosen or represented as final.

Any newly discovered unresolved authority dependency stops the affected leaf at that exact point.

---

## 6. VI-14 — Material interaction/direct-boundary closure

### VI-14-L1 — Integrated real-boundary closure

**Purpose:** close the historical VI-14 material-interaction proposition against the now-realised and
accepted U01-U06 implementation without duplicating already accepted work.

#### Worker scope

The Worker must first map each historical VI-14 proposition to current accepted evidence:

- A00 production construction/injection;
- declared A00 -> M dependency;
- typed M-owned public boundary;
- no reverse M -> A00 dependency;
- non-owning PostgreSQL mechanism behind M-owned persistence authority;
- real transaction/readback/failure behaviour;
- restart reconciliation from committed durable state;
- referential readback;
- required sequential/end-to-end A00 -> M composition;
- no overclaim of cross-kind atomicity, SLA, RTO/RPO, recovery or replay.

For each proposition classify the current state as:

- `ALREADY_ESTABLISHED_BY_ACCEPTED_EVIDENCE`;
- `REQUIRES_CURRENT_INTEGRATED_REVALIDATION`;
- `UNPROVED`;
- `BLOCKED`.

The Worker then executes the smallest current integrated validation needed to close all required
VI-14 propositions on one exact candidate. Existing accepted U05/U06 proof should be reused as
lineage/evidence where it remains directly bearing; do not manufacture new tests where existing
proof plus current integrated execution establishes the proposition.

If a real defect is found, repair only within current authority and rerun the affected proof plus
required predecessor/integration regression. Any code/proof/config/dependency change creates a new
candidate requiring Tester review.

#### Tester challenge

The Tester independently challenges the exact VI-14 candidate and, at minimum:

- inspects realised source boundaries rather than relying only on Worker receipts;
- checks the A00 -> M ownership/dependency/public-seam path;
- exercises at least one direct authority-derived production sequence through the declared public
  seam without relying exclusively on a Worker convenience fixture;
- checks the real PostgreSQL durability/restart/readback claims actually asserted by VI-14;
- confirms no reverse dependency, persistence bypass or inactive-capability activation;
- confirms the closure does not overclaim atomicity, SLA, recovery or replay.

#### VI-14-L1 acceptance

PASS requires one exact independently reviewed candidate where every historical VI-14 proposition is
bound either to current accepted evidence or current integrated proof, with no material unproved axis
and no broadened semantic claim.

On PASS, promote the accepted VI-14 lineage to `main` and advance to VI-15-L1.

---

## 7. VI-15 — Exact aggregate promotion and truthful packaging

VI-15 has two natural leaves because final distribution/version identity is an explicit unresolved
authority matter, while physical package construction/install proof is a separate mechanical and
behavioural proposition.

### VI-15-L1 — Final distribution/version authority closure

**Purpose:** close the BICP/IWO Remaining Unknown for final distribution naming/version metadata and
apply only the metadata explicitly authorised by the Programme Owner.

#### Worker scope before the authority stop

The Worker must inspect and record:

- current distribution name/version metadata;
- package/module topology actually admitted by the final implementation;
- current packaging configuration and build backend;
- any normative/package-law constraints bearing on the final distribution identity;
- whether changing final metadata would require any non-metadata source/configuration mutation.

The Worker must not infer that `nvda-architecture-kernel==0.1.0` is final merely because it is the
current `pyproject.toml` state.

The Worker then records the smallest explicit decision required and stops for Programme Owner
authority.

#### Mandatory Programme Owner authority checkpoint

The Programme Owner must explicitly authorise the final distribution name and version metadata, or
explicitly authorise retention of the current values as final.

No Worker or Tester may make that decision by convention, precedent, package-manager behaviour or
implementation convenience.

#### Worker scope after authority is supplied

Apply only the authorised metadata and any strictly necessary packaging metadata consequence. Do not
change product semantics, owner identity, module admission, dependencies or proof meaning unless the
new authority explicitly requires it.

Freeze one exact VI-15-L1 candidate.

#### Tester challenge

The Tester independently verifies:

- the Programme Owner authority exists and is exact;
- final metadata matches that authority exactly;
- no unrelated semantic/configuration/dependency mutation was smuggled into the leaf;
- accepted U01-U06/VI-14 semantics remain unchanged.

#### VI-15-L1 acceptance

PASS requires explicit final package identity authority plus exact, bounded metadata application on
one independently reviewed candidate.

On PASS, promote to `main` and advance to VI-15-L2.

### VI-15-L2 — Aggregate promotion and package/install proof

**Purpose:** prove that the complete admitted implementation is green on both proof axes and that the
built distribution truthfully contains and exposes only the admitted bounded capability.

#### Worker scope

From one clean committed VI-15-L1 accepted state, the Worker must:

1. run the complete product blocking set as one separately attributable proof axis;
2. run the complete architecture/bootstrap blocking set as a separate proof axis;
3. fail closed on red, incomplete or unauthorised skipped coverage;
4. build the configured wheel and source distribution from the exact clean committed candidate;
5. inventory and inspect wheel/sdist contents;
6. install the built distribution into an environment outside the repository/source tree without
   repository path injection;
7. prove the installed distribution exposes the admitted Raw Signal Occurrence Truth/A00 behaviour
   required by the package proposition;
8. prove unadmitted/inactive capability is absent from the installed distribution or otherwise
   remains lawfully inactive as required by current package/architecture authority;
9. record exact package filenames, byte sizes and cryptographic hashes;
10. record the exact build toolchain/environment identities bearing on reproducibility/provenance.

A source-tree import is not a substitute for the isolated installed-distribution proposition.

#### Tester challenge

The Tester independently challenges the exact package candidate, including:

- separate product and architecture aggregate attribution;
- build from the exact committed state;
- wheel/sdist inventory;
- isolated installation outside the source tree;
- installed admitted behaviour;
- exclusion/non-activation of unadmitted capability;
- exact package hashes and package identity/version.

#### VI-15-L2 acceptance

PASS requires separately green complete product and architecture proof axes plus independently
reviewed package-build/install evidence for one exact committed/package state.

On PASS, promote the accepted VI-15-L2 lineage to `main` and advance to VI-16-L1.

---

## 8. VI-16 — Fresh whole-BICP semantic review

### VI-16-L1 — Whole-BICP semantic closure

**Purpose:** challenge the realised implementation, proof and package as one bounded system against
the whole accepted BICP/IRB rather than another local implementation unit.

#### Worker scope

The Worker prepares one exact review candidate and review packet that binds:

- accepted BICP/IRB identities;
- all twelve named Raw Signal propositions;
- BC-001 composition;
- all nineteen current proof obligations;
- final implementation paths;
- final package identity and hashes;
- VI-14 and VI-15 accepted evidence;
- all Remaining Unknowns and their current dispositions;
- inactive capabilities that must remain inactive.

The Worker must perform a whole-system trace for obvious gaps before handoff but does not self-award
VI-16 semantic acceptance.

No production/proof/package bytes may change after candidate freeze without returning to the Worker
and creating a new candidate.

#### Tester challenge

The fresh Tester reviews the whole accepted BICP/IRB against the exact frozen implementation/proof/
package state and challenges, at minimum:

- all twelve named Raw Signal propositions;
- BC-001 composition;
- all nineteen proof obligations;
- no added semantic meaning;
- no hidden Remaining-Unknown defaults;
- no inactive capability activation;
- no mechanism-as-semantic-owner substitution;
- boundedness of all product-visible claims;
- proof relevance to the final realised/package bytes.

Tester verdict is exactly `PASS`, `FAIL / RETURN_TO_WORKER`, or `BLOCKED`.

#### VI-16-L1 acceptance

PASS requires fresh independent whole-BICP semantic acceptance of one exact final implementation/
proof/package candidate.

On PASS, promote the accepted VI-16 lineage to `main` and advance to VI-17-L1.

---

## 9. VI-17 — Integration / authority / provenance audit

VI-17 is split because authority-lineage reconstruction and release/environment/integrity provenance
are separable propositions with different evidence and failure modes.

### VI-17-L1 — Authority and lineage reconstruction

**Purpose:** prove that the exact final candidate descends lawfully from the accepted semantic and
architecture authority through IWO, proof and implementation history.

#### Worker scope

Reconstruct and record, with exact identities:

```text
IRB / accepted BICP
  -> implementation authorisation
  -> accepted IWO
  -> architecture admission / owner allocation / dependency / seam authority
  -> product and architecture proof obligations
  -> U01-U06 implementation/review lineage
  -> VI-14 interaction closure
  -> VI-15 package candidate
  -> VI-16 whole-BICP accepted candidate
```

At minimum audit:

- fixed authority hashes;
- start/final Git identities and ancestry;
- durable allocation/registry state;
- owner/dependency/seam declarations;
- proof registrations/memberships/results;
- changed-path authority for substantive implementation mutations;
- absence of unauthorised authority mutation;
- authority -> IWO -> proof -> code -> package traceability.

#### Tester challenge

The Tester independently reconstructs the material lineage from primary repository/Git evidence
rather than accepting the Worker's map as proof.

Any irreconcilable authority/lineage break is `BLOCKED` or `FAIL / RETURN_TO_WORKER` according to
whether it is an authority gap or repairable evidence/mechanical defect.

#### VI-17-L1 acceptance

PASS requires independently reproducible authority-to-final-candidate lineage with no material gap
or unauthorised semantic mutation.

On PASS, promote to `main` and advance to VI-17-L2.

### VI-17-L2 — Provenance, environment and repository-integrity audit

**Purpose:** prove exactly what package/environment/repository state is being frozen and that the
state is internally consistent, recoverable and resumable.

#### Worker scope

Audit and record:

- final package hashes and inventories;
- final distribution name/version identity;
- external dependency and toolchain identities used for accepted proof/build;
- PostgreSQL proof-environment identity and relevant durability configuration;
- final product and architecture aggregate results;
- final package/install proof identity;
- inactive-capability closure;
- repository clean state;
- `git diff --check` / repository integrity checks appropriate to the final state;
- reachable ancestry for all accepted candidates/reviews/promotions;
- absence of post-review production/proof/config/dependency drift;
- recovery/resumability prerequisites required for VI-18 artefact creation.

Do not claim reproducible build identity unless actually established. Exact recorded provenance is
required; stronger reproducibility claims require corresponding proof.

#### Tester challenge

The Tester independently checks the final provenance and integrity evidence, including exact package
hashes/inventory, relevant toolchain/PostgreSQL identity, Git integrity/ancestry, clean state and
absence of unreviewed byte drift.

#### VI-17-L2 acceptance

PASS requires one independently reviewed provenance/integrity state sufficient to support final
freeze without an unresolved identity, environment, package or repository-integrity gap.

On PASS, promote to `main` and advance to VI-18-L1.

---

## 10. VI-18 — Freeze verified bounded implementation and STOP

### VI-18-L1 — Final freeze and durable recovery artefact

**Purpose:** freeze the exact bounded implementation already accepted by VI-14 through VI-17,
preserve a durable recovery artefact, record terminal state, and stop.

VI-18 is a closure/freeze leaf, not an opportunity to change implementation meaning.

#### Worker scope

The Worker must record the exact terminal identities, including:

- final `main` commit/tree proposed for closure;
- active implementation identity;
- final distribution name/version;
- final wheel/sdist filenames and hashes;
- final product aggregate result identity;
- final architecture aggregate result identity;
- accepted VI-14/15/16/17 review identities;
- Remaining Unknowns still intentionally unresolved/out of scope;
- inactive capabilities that remain inactive;
- exact repository clean/integrity state;
- one durable full-Git recovery artefact sufficient to reconstruct the accepted repository history.

The recovery artefact must be read back/validated against the recorded repository identities. A file
existing on disk is not sufficient evidence of recoverability.

The Worker updates current-state/terminal handoff records to describe the proposed terminal state and
freezes one exact VI-18 candidate.

#### Tester challenge

The Tester independently verifies:

- VI-14 through VI-17 are accepted prerequisites;
- terminal commit/tree and package hashes match the accepted state;
- no unreviewed production/test/config/dependency/package bytes appeared after their relevant review;
- Remaining Unknowns and inactive capabilities are truthfully recorded;
- recovery artefact integrity/readback and repository reconstruction evidence;
- final repository state is clean and integrity checks pass;
- terminal claims remain bounded to the accepted BICP.

If VI-18 work changes substantive implementation/proof/config/dependency/package bytes after the
relevant VI-16/VI-17 acceptance, the affected upstream review is stale and must be repeated before
VI-18 can PASS.

#### Terminal disposition

Terminal outcome is exactly one of:

```text
PASS
FAIL_REPAIRABLE
BLOCKED
```

`PASS` means only that the exact BICP-admitted Raw Signal Occurrence Truth bounded implementation is
realised, independently reviewed, packaged, provenance-audited and frozen with exact lineage and no
unauthorised semantic expansion.

After terminal `PASS`, **STOP**.

---

## 11. Branch, review and promotion discipline

For execution after this plan is accepted:

- one independently provable leaf per work branch;
- branch from then-current accepted `main`;
- do not pre-create downstream leaf branches;
- preserve ordinary ancestry; no squash/rebase/history rewrite for tidiness;
- substantial Worker boundaries are committed before Tester handoff;
- one Tester reviews one exact frozen leaf candidate;
- failed candidates and repairs remain recoverable in Git history;
- Tester evidence and promotion/close-out records are separate from candidate bytes where practical;
- after Tester PASS, promote the exact accepted lineage to `main` before starting the next dependent
  leaf;
- do not carry a dirty worktree into another leaf;
- genuine new authority decisions stop for the Programme Owner.

The existing `handoff/control/CURRENT_STATE.md` and `handoff/review_cycles/` mechanism remains the
routing surface. No alternative workflow is introduced here.

---

## 12. Mutation discipline by gate

### VI-14

Expected mutation is primarily proof/evidence/integration closure. Production changes are permitted
only for a demonstrated current-authority defect and require exact regression and fresh Tester review.

### VI-15-L1

Expected mutation is final package metadata and evidence only, after explicit Programme Owner
authority. No metadata value may be invented.

### VI-15-L2

Expected mutation is packaging/proof/evidence required to build and verify the admitted distribution.
Do not broaden runtime capability to make packaging convenient.

### VI-16

Expected Worker mutation is review packet/evidence only. Any substantive repair discovered by the
Tester returns to the owning layer and produces a new exact candidate before VI-16 re-review.

### VI-17

Expected mutation is audit/provenance/evidence only. A substantive implementation or authority defect
must be repaired at its owning layer and then revalidated through every downstream acceptance made
stale by that repair.

### VI-18

Expected mutation is terminal state/handoff/recovery artefact evidence only. Substantive byte changes
invalidate the affected prior review and cannot be hidden inside close-out.

`GUARDRAILS.md` remains frozen throughout ordinary execution.

---

## 13. Evidence discipline

Every Worker and Tester record must distinguish:

- `VERIFIED` — established by identified primary evidence;
- `UNPROVED` — required proposition not yet established;
- `BLOCKED` — required proposition cannot currently be established for an identified reason;
- `NOT_IN_SCOPE` — proposition not required by the current leaf.

Each material leaf record must include where applicable:

- exact branch, commit and tree;
- predecessor accepted commit/tree;
- changed paths;
- exact authority/proposition under test;
- relevant package hashes;
- proof/build/runtime environment identities;
- commands/checks actually executed;
- explicit test/result counts where applicable;
- source-level trace findings where material;
- limitations/non-claims;
- first unmet invariant on failure;
- next lawful action.

A PASS receipt without sufficient semantic evidence is not acceptance.

---

## 14. Mandatory stop conditions

Stop dependent execution at the first occurrence of any of the following:

- current governance or accepted BICP/IWO identity cannot be rebound;
- current `main` does not descend from the exact accepted predecessor required by the leaf;
- an unresolved Remaining Unknown becomes necessary for execution and lacks current authority;
- package name/version would need to be chosen without Programme Owner authority;
- proof, packaging or implementation would activate P01, K01, DMPV3, replay, provider/network,
  external effects/accounts or downstream consumer semantics;
- architecture law cannot represent the required accepted state;
- a proof cannot discriminate the governed semantic distinction;
- real PostgreSQL evidence is required for an asserted proposition but cannot be established;
- product or architecture aggregate is red, incomplete or skipped without authority;
- package/install proof depends on repository path injection or source-tree substitution;
- Tester has an unresolved material finding;
- authority -> IWO -> proof -> code -> package lineage cannot be reconstructed;
- post-review substantive byte drift makes downstream review evidence stale;
- final repository integrity/readback or recovery-artefact verification fails.

Preserve the last proved state and first unmet invariant. Do not continue downstream merely to make
progress.

---

## 15. Definition of tranche done

This VI-14 through VI-18 tranche is done only when all of the following are true for the exact
terminal state:

1. exact accepted BICP/IRB/IWO bytes remain bound;
2. accepted U01-U06 implementation semantics remain conserved;
3. VI-14 integrated material interaction/direct-boundary closure passes independent Tester review;
4. final distribution name/version has explicit Programme Owner authority;
5. final package metadata matches that authority exactly;
6. complete product blocking proof is green and separately attributable;
7. complete architecture/bootstrap blocking proof is green and separately attributable;
8. wheel/sdist are built from exact clean committed state and inventoried/hashed;
9. installed distribution is proved outside the source tree without path injection;
10. installed distribution exposes admitted capability and does not silently activate unadmitted
    capability;
11. fresh whole-BICP semantic review passes against the exact final implementation/proof/package;
12. authority/lineage reconstruction independently passes;
13. provenance/environment/repository-integrity audit independently passes;
14. no Remaining Unknown became a hidden default;
15. no mechanism became semantic owner;
16. inactive capabilities remain inactive;
17. no unreviewed substantive byte drift exists after the review that bears on those bytes;
18. terminal commit/tree, package hashes, proof identities and accepted review identities are exact;
19. durable full-Git recovery artefact is created and its readback/reconstruction evidence passes;
20. final repository state is clean and integrity checks pass;
21. terminal boundedness/non-claims are recorded truthfully;
22. VI-18 Tester accepts the exact terminal freeze candidate;
23. terminal state is promoted/recorded on `main` with ancestry preserved;
24. project stops at the bounded-implementation boundary.

Anything less is an intermediate state, not VI-18 terminal PASS.

---

## 16. Planned leaf sequence and progress

The active sequence after plan acceptance is:

- [ ] **VI-14-L1** — integrated material interaction/direct-boundary closure — Worker -> Tester;
- [ ] **VI-15-L1** — final distribution/version authority closure and exact metadata application —
  Worker -> Programme Owner authority checkpoint -> Worker freeze -> Tester;
- [ ] **VI-15-L2** — complete aggregate promotion and truthful package/install proof — Worker ->
  Tester;
- [ ] **VI-16-L1** — whole-BICP semantic review — Worker packet/freeze -> Tester review;
- [ ] **VI-17-L1** — authority and lineage reconstruction — Worker -> Tester;
- [ ] **VI-17-L2** — provenance/environment/repository-integrity audit — Worker -> Tester;
- [ ] **VI-18-L1** — final freeze, recovery artefact and STOP — Worker -> Tester -> terminal close-out.

No downstream leaf begins before the preceding leaf is accepted and promoted, except that bounded
preparation that cannot mutate or prejudge the downstream proposition may be performed only if the
current ExecPlan and current-state routing explicitly authorise it.

---

## 17. Plan retirement and activation

This document is presently a draft on the planning branch.

If the Programme Owner approves it:

1. commit the accepted plan on the planning branch if not already committed;
2. integrate the accepted plan into `main` with preserved ancestry;
3. update current-state routing to name **VI-14-L1 Worker** as the next authorised action;
4. create the first VI-14-L1 work branch from that accepted `main` state;
5. execute under the existing Worker/Tester cycle.

The previous U06 ExecPlan remains ordinary Git history and must not be destructively deleted or
rewritten.
