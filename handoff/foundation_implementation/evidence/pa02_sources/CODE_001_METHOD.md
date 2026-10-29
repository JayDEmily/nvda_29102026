# CODE-001 — BICP-to-Code Methodology

Status: **PROPOSED DESIGN V0**

Gate namespace: `C00`–`C12`.

This methodology is intended to be reusable across bounded implementation contexts. The accepted Raw Signal BICP is the first reference case, not the definition of the method.

## Mission

Transform one exact accepted BICP and its exact admitted architecture-kernel baseline into an independently proved, architecture-admitted bounded implementation **without inventing semantics, silently resolving Unknowns or allowing tests/code structure to become authority**.

## Canonical flow

```text
ACCEPTED BICP
    |
    v
C00  methodology governance
    |
C01  exact input binding
    |
C02  implementation-readiness / Unknown gate
    |
C03  physical proof-realisation map
    |
C04  engineering realisation units
    |
C05  physical proof/test authoring
    |
C06  independent proof-adequacy review
    |
C07  proof admission + Implementation Work Order
    |
    |  CODE BOUNDARY
    v
C08  controlled implementation
    |
C09  bounded-unit closure
    |
C10  cross-unit / composition closure
    |
C11  architecture admission / promotion
    |
C12  final whole-BICP + integration/release closure
    |
    v
HUMAN / PROGRAMME ACCEPTANCE
```

## C00 — Methodology Governance

### Purpose

Freeze the rules under which a CODE-001 run may proceed.

### Required inputs

- this methodology version;
- governing programme/user instruction;
- applicable repository guardrails;
- accepted role/isolation model.

### Outputs

- accepted successor ExecPlan for the specific BICP run;
- explicit role map;
- branch/commit discipline;
- proof admission and supersession law;
- stop/repair law;
- claim vocabulary.

### Acceptance conditions

- methodology jurisdiction is explicit;
- BICP remains task authority rather than CODE-001 becoming semantic authority;
- no implementation/test-writing authority is implied merely by method existence;
- reviewer independence requirements are explicit;
- human/programme gates are explicit.

### Forbidden

- product code;
- product tests;
- durable architecture mutation;
- reinterpretation of BICP semantics.

## C01 — Exact Input Binding

### Purpose

Bind the exact immutable starting state.

### Required bindings

- accepted BICP bytes/digest;
- accepted BICP designation/terminal acceptance reference;
- exact kernel commit/tree admitted by BICP;
- exact implementation-authority lineage needed for traceability;
- accepted successor ExecPlan;
- any explicit post-BICP authority amendment.

### Output

`CODE_INPUT_BINDING` with exact hashes/Git objects and verification results.

### Acceptance conditions

Every bound identity is mechanically verified against primary evidence.

### Stop

Any mismatch, unavailable mandatory authority, or ambiguous baseline.

## C02 — Implementation Readiness / Remaining-Unknown Gate

### Purpose

Determine whether physical proof and implementation can be designed without settling a Remaining Unknown.

### Method

For every BICP Remaining Unknown and every implementation-freedom clause classify:

- `NOT_REQUIRED_FOR_THIS_REALISATION`;
- `EXPLICIT_IMPLEMENTATION_FREEDOM`;
- `AUTHORITY_REQUIRED_BEFORE_PROCEEDING`;
- `UNKNOWN_DEPENDENCY_NOT_YET_REACHED`.

Then inspect intended proof boundaries and necessary runtime mechanisms to find any hidden choice that would settle an Unknown.

### Output

`UNKNOWN_DISPOSITION` register and readiness verdict.

### Acceptance conditions

- every known material Unknown is dispositioned;
- no Unknown is relabelled freedom;
- no physical design is selected merely to avoid requesting authority.

### Stop

If adequate proof or implementation requires unresolved authority.

## C03 — Physical Proof-Realisation Map

### Purpose

Translate accepted BICP proof obligations into concrete falsifiable propositions without yet writing product code.

### Required analysis

For each BICP proof obligation identify:

- exact authority references;
- observable proposition;
- prohibited near-neighbour behaviour;
- state-before / trigger / state-after where applicable;
- representation boundary where meaning can collapse;
- interaction/dependency edges;
- direct evidence boundary;
- persistence/runtime environment requirement;
- positive case;
- negative/falsifier case;
- lawful optional absence;
- missing-mandatory-authority behaviour;
- lineage/identity/version behaviour;
- whether proof is local, stateful, persistence, architecture, composition or final-closure proof.

### Outputs

- proof-realisation matrix;
- state/transition graph as needed;
- representation graph as needed;
- interaction graph as needed;
- BICP obligation -> physical proof coverage map.

### Acceptance conditions

- all 19 first-reference obligations receive a disposition;
- no new semantics are introduced;
- every physical proposition traces to accepted authority;
- Remaining Unknowns stay visible.

## C04 — Engineering Realisation Units

### Purpose

Partition implementation/proof work into risk-adaptive engineering units without altering semantic ownership.

### Grouping considerations

Prefer a separate unit where work introduces or materially changes:

- durable state;
- state transitions;
- identity/retry/supersession;
- time/provenance distinctions;
- persistence transaction semantics;
- public seams;
- cross-owner interaction;
- representation transitions;
- failure/restart behaviour;
- high-risk Remaining-Unknown boundary.

Strongly coupled low-risk obligations may share a unit.

### Output

Ordered realisation-unit DAG with per-unit authority/proof obligations.

### Acceptance conditions

- every unit is independently testable enough for meaningful closure;
- no unit invents a new semantic owner;
- dependency order follows actual proof/implementation dependencies, not arbitrary symmetry;
- cross-unit edges requiring later C10 proof are explicit.

## C05 — Physical Proof/Test Authoring

### Purpose

Create the actual test/proof candidates before production implementation.

### Rules

- proof author sees accepted authority and C03/C04 outputs;
- proof author does not see candidate implementation;
- direct-boundary proof is preferred over proxy proof;
- durability claims require real persistence evidence where the BICP requires it;
- proof must include semantic near-neighbour falsifiers;
- proof must avoid incidental global-state freezes unless authoritative.

### Outputs

- physical test/proof candidate bytes;
- proof-scope record;
- test environment requirements;
- evidence-capture plan;
- proof coverage map back to BICP IDs.

### Acceptance conditions

Authored proof is complete enough to enter independent adequacy review. This gate does **not** mean proof is admitted.

## C06 — Independent Proof-Adequacy Review

### Purpose

Determine whether the proposed physical proof can actually falsify materially unlawful implementations.

### Reviewer isolation

Reviewer receives:

- exact BICP/current authority needed to judge the obligation;
- C03 physical proposition;
- C05 proof candidate and proof-scope record.

Reviewer does **not** receive candidate production implementation or builder rationale as evidence.

### Core questions

- Could a semantically violating implementation still pass?
- Could two materially distinct authorised states collapse to the same representation and both pass?
- Does the proof exercise the boundary where the distinction can actually fail?
- Has the proof frozen incidental global state?
- Does the proof accidentally resolve an Unknown?
- Is required persistence/interaction evidence real rather than simulated away?

### Verdict

Exactly one of:

- `PASS`;
- `FAIL`;
- `BLOCKED`.

### Repair

`FAIL` returns to the owning C03/C05 layer. An authority defect returns upstream rather than being repaired in test code.

## C07 — Proof Admission + Implementation Work Order

### Purpose

Make the accepted proof immutable and issue the exact bounded authority for coding.

### Outputs

- immutable proof admission generation;
- exact proof hashes/Git refs;
- revocation/supersession mechanism;
- Implementation Work Order (IWO);
- allowed mutation surface;
- forbidden mutation surface;
- required checks/evidence;
- implementation-freedom list;
- Remaining-Unknown stop list;
- exact completion conditions.

### Acceptance conditions

- independent C06 `PASS` exists;
- proof bytes are durably bound before code;
- IWO changes no BICP meaning;
- IWO authorises only the smallest coherent realisation unit;
- no production coding happened before this gate.

### CODE BOUNDARY

Production implementation becomes permissible only below an accepted C07 for the applicable realisation unit.

## C08 — Controlled Implementation

### Purpose

Make the smallest coherent production change that satisfies accepted authority and admitted proof.

### Worker inputs

- exact BICP/current authority needed for the unit;
- exact admitted proof generation;
- exact IWO;
- required existing interfaces/source state.

### Rules

- tests are not weakened to obtain green;
- proof is not resealed around the implementation;
- code structure does not create semantic authority;
- adjacent capability is not implemented opportunistically;
- Unknowns trigger stop;
- work stays inside authorised mutation surfaces unless an explicit repair/amendment gate reauthorises scope.

### Output

Candidate implementation commit(s) for the bounded unit.

## C09 — Bounded-Unit Closure

### Purpose

Establish that one implemented engineering unit satisfies its admitted authority and proof.

### Required evidence as applicable

- physical proof execution;
- static/type validation;
- direct persistence/integration evidence;
- failure/restart evidence;
- architecture/dependency/seam validation;
- clean diff/scope audit;
- fresh semantic review against full unit authority.

### Acceptance conditions

- admitted proof passes on the actual committed implementation state;
- no proof mutation after admission except through formal supersession;
- fresh semantic reviewer finds no material mismatch;
- limitations and deferred cross-unit edges remain explicit.

Local PASS does not imply C10 PASS.

## C10 — Cross-Unit / Composition Closure

### Purpose

Prove the interaction graph and required composition after locally accepted units exist.

### First reference case includes

- governed `A00 -> M00` public-seam composition;
- no reverse/private bypass;
- persistence mechanism remains non-owning;
- no inactive P01/K01/downstream capability appears;
- cross-unit state/time/identity meaning remains consistent.

### Outputs

- interaction/composition proof;
- end-to-end/sequential evidence where BICP requires it;
- cross-unit contradiction disposition.

### Acceptance conditions

Every material C03/C04 interaction edge has a closing disposition.

## C11 — Architecture Admission / Promotion

### Purpose

Create the durable architecture state for an implementation that has already satisfied applicable semantic/product proof.

### Possible actions, only when separately authorised by accepted plan

- durable M-category allocation;
- architecture registry updates;
- dependency declaration;
- public-seam registration;
- implementation allocation;
- proof registration;
- packaging/composition/promotion state.

### Rules

- BICP's non-durable candidate identity does not become durable merely because code exists;
- registry presence does not confer semantic correctness;
- current BUILD-001 validators/proof/promotion law must be exercised against the exact state claimed.

### Acceptance conditions

Architecture state, code state and admitted proof state agree exactly for the claimed implementation.

## C12 — Final Independent Closure

### Purpose

Close the entire bounded implementation from original accepted BICP through released Git/package state.

### Review A — whole-BICP semantic audit

Re-open the accepted BICP/authority and map every material obligation/Unknown/exclusion through:

```text
BICP
 -> physical proof
 -> implementation
 -> interaction/composition
 -> final observable state
```

Check for lost meaning, disappeared Unknowns, unauthorised capability and cross-layer semantic collapse.

### Review B — integration/authority/release audit

Independently check:

- exact authority binding;
- exact proof generations and supersession state;
- registries/allocations;
- dependencies/public seams;
- package/entry points;
- Git ancestry and clean state;
- reproducibility from a fresh committed state;
- release artefact integrity;
- fresh-context resumability.

### Clean release transaction

Preferred pattern:

```text
closeout commit
 -> clean detached clone/worktree
 -> required validation
 -> archive/bundle from committed state
 -> rehydrate elsewhere
 -> verify exact HEAD/tree and Git health
 -> rerun required validation
 -> release candidate
```

### Terminal boundary

C12 evidence does not self-approve the programme. Human/programme acceptance remains the terminal gate.

## Repair and loop model

CODE-001 does not use one universal retry loop. Findings return to the owning layer:

```text
C02 authority blocker   -> upstream authority / BICP amendment path
C03 mapping defect      -> repair C03
C04 unit decomposition  -> repair C04
C05 proof defect        -> repair C05
C06 review FAIL         -> owning proof/mapping layer, then fresh C06
C08 implementation bug  -> repair C08 without changing admitted proof
admitted-proof defect   -> revoke/supersede proof, fresh C06/C07 generation
C09 semantic defect     -> determine owner: implementation, proof, or authority
C10 composition defect  -> owning unit/composition layer
C11 architecture defect -> architecture state/plan unless it exposes semantic mismatch
C12 semantic defect     -> owning upstream layer; do not patch release evidence
```

Every failed generation remains preserved in Git/history.

## First-reference fixed facts

For Raw Signal BICP 005, CODE-001 must begin with:

- BICP JSON SHA-256 `5b99cead41fd8d3d372b5ed2ef4558065328b814e0a94c3680162fc6594df5ed`;
- terminal IA commit `f64cf4c3f04e8e02ea368defb6d89d0f3ed0df7b`;
- BUILD-001 baseline commit `17263909abae9ca8cabb2440db282d12ff492ad6`;
- BUILD-001 baseline tree `26c421f7cbc75d61ea3e538d79091f4e01136585`;
- 19 accepted proof obligations;
- non-durable M-category candidate `M00`;
- supporting modify target `A00`;
- runtime dependency `A00 -> M00`;
- Remaining Unknowns preserved exactly as BICP records them.

The actual successor product repository/remote is not selected by this methodology draft.
