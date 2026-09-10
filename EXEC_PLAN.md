# Architecture Kernel Completion and Implementation-Brief Ingress Readiness ExecPlan

## Status

**ACCEPTED — current active planning authority for this tranche.**

This document operationalises the current authorised objective. It does not create domain meaning, product requirements, or authority beyond that objective.

## 1. Mission

Produce a pristine, behaviour-neutral NVDA architecture kernel that is ready for future implementation work from an externally supplied, explicitly accepted **implementation-ready coding brief**.

The target boundary is:

```text
AUTHORITATIVE HUMAN / DOMAIN SOURCE
            |
            v
SEPARATE SEMANTIC-TO-BRIEF METHODOLOGY
            |
            v
ACCEPTED IMPLEMENTATION-READY CODING BRIEF
            |
            | exact authority ingress
            v
---------------------------------------------
        ARCHITECTURE KERNEL BOUNDARY
---------------------------------------------
            |
            | future implementation work
            | constrained by kernel law
            v
TESTS -> CODE -> COMPOSITION -> PROOF
```

The architecture kernel does **not** perform the upstream semantic-to-brief transformation.

The architecture kernel does **not** implement the future coding worker/process that will turn an implementation-ready brief into code.

This tranche prepares the repository so that such a future process has one clean, mechanically governed architecture into which it can implement.

## 2. Governing end-state

At completion, the repository must be:

- behaviour-neutral;
- free of active NVIDIA trading/business functionality;
- free of active Raw Signal-specific semantic or programme machinery;
- free of duplicated upstream semantic-reconstruction machinery;
- structurally capable of admitting future runtime modules, protocols, technical kernels, governance planes, application shells and architecture surfaces;
- mechanically governed for object identity, ownership, dependencies, public seams, lifecycle, composition, proof admission and packaging;
- capable of binding one exact accepted implementation-ready brief as implementation authority without reproducing that brief's upstream semantic derivation;
- capable of deriving and admitting tests and implementation under that exact brief;
- free of any requirement that the implementation-ready brief have been produced by a particular methodology or repository.

The kernel is therefore **implementation-brief agnostic**.

## 3. Explicit jurisdiction boundary

### 3.1 Upstream semantic-to-brief system

The upstream methodology owns:

- reading authoritative source material;
- semantic reconstruction;
- semantic ambiguity and Unknown handling;
- source fidelity;
- whole-field semantic conservation;
- semantic candidate identity;
- semantic review;
- semantic lineage;
- its own mechanical lineage;
- generation and acceptance of the implementation-ready coding brief.

None of that machinery belongs in this architecture repository.

The architecture repository must not reproduce:

- upstream semantic gates;
- upstream semantic-index construction;
- source-first semantic worker/reviewer orchestration;
- upstream candidate/successor machinery;
- upstream source corpus storage merely to re-prove the brief;
- upstream lineage graphs;
- upstream worker/tester handoff mechanisms.

### 3.2 Architecture-kernel system

The kernel owns only structural and implementation-governance law, including:

- architectural object taxonomy;
- permanent architectural identifiers;
- semantic ownership boundaries once supplied by accepted implementation authority;
- declared inputs and outputs;
- state/time/side-effect ownership declarations;
- dependency direction;
- dependency declaration;
- public seams;
- composition;
- object lifecycle;
- architecture proof admission;
- architecture promotion;
- packaging/bootstrap integrity;
- the generic boundary by which exact implementation authority enters a coding tranche.

### 3.3 Future implementation system

The future coding continuation will own the actual transformation:

```text
accepted implementation-ready brief
        ->
tests / implementation obligations
        ->
code
        ->
integration
```

That continuation is **not designed or implemented by this ExecPlan**.

This ExecPlan must leave a clean architectural surface for it.

## 4. Verified starting point

Repository baseline for this plan:

```text
HEAD:
892a6c042f19d19d84a3d1fb2c639033789f9bc1
```

The current architecture kernel already establishes:

- empty active runtime-module registry;
- empty active architecture-surface registry;
- object categories `M`, `P`, `G`, `A`, `K`, `S`;
- open-ended identifier allocation;
- dependency laws;
- public-seam law;
- lifecycle law;
- composition eligibility;
- architecture proof admission;
- architecture promotion;
- architecture/bootstrap package structure.

The active runtime-module registry is:

```yaml
modules: []
```

The current tree also contains programme-specific material from the Raw Signal clean-restart programme, including:

- Raw Signal source/candidate authority;
- Raw Signal semantic-index state;
- Gate-0 admission machinery;
- Gate-1+ semantic governance machinery;
- Raw Signal-specific Codex agents and orchestration;
- Raw Signal-specific work-order/review/admission schemas;
- Gate-0/governance tests and tools;
- Raw Signal programme control documents.

These surfaces must not remain active merely because they are present in the current Git tree.

Historical material remains recoverable through Git history and does not need an active-tree archive copy.

## 5. Non-goals

This tranche must not:

- implement Raw Signal;
- admit any NVIDIA business module;
- reactivate historical `M00–M15`;
- decide future module allocation;
- implement DMPV3 behaviour;
- implement state/transaction behaviour;
- implement trading, market data, calendar, risk, capital, execution, portfolio or replay behaviour;
- import or embed the upstream semantic-to-brief methodology;
- implement a new semantic-reconstruction methodology;
- design the future AI/code-writing worker;
- solve PMB ordering;
- use historical implementation order as current implementation authority;
- migrate to Python 3.14;
- introduce UUIDv7 capability;
- redesign the modular-monolith architecture without a demonstrated contradiction in current architectural law.

## 6. Work discipline

Work one acceptance unit at a time.

For every mutation:

1. identify the exact governing authority;
2. identify the proposition being changed;
3. read the affected material in full;
4. make the smallest coherent change;
5. run proof that bears on that proposition;
6. inspect the result semantically;
7. do not advance if the acceptance condition is not established.

A green test is not semantic acceptance.

Historical `PASS`, `COMPLETE`, `accepted`, or similar labels do not bypass current verification.

At the first absent or failed required invariant, stop dependent downstream work.

## 7. AKR-1 — Establish the canonical end-state inventory

### Purpose

Determine exactly what belongs in the architecture kernel before any target-tree carry-forward decision is executed.

### Work

Classify every tracked active-tree file as exactly one of:

```text
KEEP
REWRITE
DO_NOT_CARRY_FORWARD
HISTORICAL_ONLY
BLOCKED
```

For every `KEEP` or `REWRITE`, record its continuing architecture-kernel responsibility.

The classification must explicitly cover:

- root control files;
- `authority/**`;
- `.agents/**`;
- `.codex/**`;
- `docs/governance/**`;
- `docs/orchestration/**`;
- `docs/history/**`;
- architecture documentation;
- architecture configuration;
- proof configuration;
- schemas;
- templates;
- source;
- tests;
- tools;
- packaging/build files.

### Mandatory historical challenge set

Before a structural control is classified `KEEP`, `REWRITE` or `DO_NOT_CARRY_FORWARD`, reconcile it against:

1. the mature pre-reset Native Architecture Blueprint and routed normative architecture corpus;
2. the mature ownership/runtime/state/proof/vocabulary maps relevant to that control;
3. the architecture-kernel reset brief and reset rationale;
4. the September 2026 architecture-kernel conformance ADR and exact implemented changes.

Historical material is **challenge evidence**, not automatic current authority. It may establish the architectural problem a control was intended to solve; it may not silently reactivate historical `M00–M15` semantics, allocations, implementation order or product behaviour.

For each material structural control answer:

1. What architectural problem was this control intended to solve?
2. What primary evidence established that problem?
3. Does that problem still exist in the target behaviour-neutral, implementation-brief-ready kernel?
4. Does the current mechanism solve the problem without acquiring another object's semantic responsibility?
5. Is the mechanism still the minimal correct kernel-level solution, or does it belong upstream/downstream/outside the kernel?
6. What current proof can falsify the claimed behaviour of the mechanism?

Where a classification depends on what an executable checker allegedly enforces, use a bounded executable challenge when practical rather than relying on function names, comments or existing green tests.

### Known AKR-1 challenge requirements

The inventory must explicitly assess these observed current limitations:

- the aggregate validator's reset-only requirement that no active runtime module exist cannot remain the permanent first-active-module admission rule;
- public-seam analysis must correctly account for `ImportFrom` forms such as `from nvda_desk import m02`, not only `import nvda_desk.m02...` forms;
- proof-family discovery must match the written jurisdiction for physical tests, including nested test files if the law claims recursive physical coverage;
- textual occurrence of a proposition ID establishes addressability/binding only; it must not be described as semantic entailment;
- the current reset/bootstrap tests must be distinguished from permanent future admission proof.

### Acceptance condition

AKR-1 passes only when:

- every tracked file has been semantically classified;
- every retained file has an identified architecture-kernel responsibility;
- no retained file depends for its purpose on Raw Signal semantics or the upstream semantic-to-brief process;
- every material current structural control has been challenged against the mature architecture/reset/September evidence;
- the September conformance problem set has not been silently regressed;
- no unresolved classification is silently converted to retention or `DO_NOT_CARRY_FORWARD`.

No target-tree carry-forward decision is executed before this gate passes.

## 8. AKR-2 — Stop carrying programme/domain-specific active surfaces forward

### Purpose

Return the active repository to the behaviour-neutral architecture-kernel jurisdiction.

### Expected `DO_NOT_CARRY_FORWARD` candidates

Subject to AKR-1 verification, current evidence identifies the following as programme/domain-specific candidates not to carry forward in the target active tree:

```text
Raw Signal source authority
Raw Signal candidate authority
Raw Signal workbook renderings
Raw Signal semantic-index state
Raw Signal admitted-state machinery
Gate-0 runtime/admission machinery
Gate-1+ semantic work-order machinery
Raw Signal semantic orchestrator skill
Raw Signal-specific Codex agents
Raw Signal-specific hooks
Raw Signal work-order / attempt / review / admission schemas
Gate-0 tests
Gate-1+ semantic-governance tests
Gate-0 tools
semantic-governance tools
Raw Signal programme roadmap/control state
completed Raw Signal restart-control surfaces
```

Do not create a duplicate archive directory for material that is already preserved by ordinary Git history.

### Root controls

Replace Raw Signal-specific root orientation with architecture-kernel orientation.

The target governance model is:

```text
GUARDRAILS.md
AGENTS.md
EXEC_PLAN.md
```

There is no separate normative `PLANS.md` role.

No mutable roadmap/receipt document may silently become a second planning authority.

### Acceptance condition

AKR-2 passes only when the active tree contains no business/domain programme whose semantics are not part of the architecture kernel, while historical evidence needed for subsequent architecture reconciliation remains available through Git or an explicitly justified active historical surface.

## 9. AKR-3 — Reconcile and simplify architecture authority

### Purpose

Leave one internally coherent structural authority surface.

### Work

Re-read and reconcile:

```text
ARCHITECTURE_KERNEL.md
ARCHITECTURAL_OBJECT_TAXONOMY.md
DEPENDENCY_LAWS.md
PUBLIC_SEAM_LAW.md
TEST_AND_PROMOTION_KERNEL.md
EXTENSION_AND_RETIREMENT_RULES.md
applicable architecture ADRs
```

Remove active references whose only purpose was the superseded Raw Signal programme.

Do not duplicate the same architectural rule across multiple documents unless the second occurrence has a distinct routing or explanatory function.

### September conformance disposition

For each September conformance concern, record one explicit disposition:

```text
RETAIN_AS_KERNEL_LAW
REWRITE_AS_KERNEL_LAW
OWNED_ELSEWHERE
DO_NOT_CARRY_FORWARD_WITH_EVIDENCE
BLOCKED
```

At minimum cover:

- real dependency-edge representation;
- category/dependency-direction law, including lawful M→P/K use;
- representable P/K activation without forcing module semantics;
- active-module semantic/ownership obligations;
- named dynamic-import detection and import-form coverage;
- proof-scope accuracy;
- lifecycle/permanent-identity lineage;
- public-seam exception law;
- the accepted-but-unimplemented typed-seam checker decision.

Do not regress an established structural problem merely because the current reset state is empty. If a September decision is changed, the evidence must establish why the original architectural problem no longer exists or why a different minimal mechanism now owns it.

### Authority-manifest disposition

The existing Raw Signal `authority/AUTHORITY_MANIFEST.md` must not simply have stale hashes recalculated.

First determine whether a static architecture-authority hash manifest is still necessary after programme-specific governance is no longer active.

Then choose exactly one lawful disposition:

```text
A. DO_NOT_CARRY_FORWARD because no kernel invariant requires it; or
B. replace it with a kernel-only mechanically validated authority-binding surface
   because a demonstrated kernel invariant requires one.
```

Do not retain a receipt mechanism merely because it historically existed.

### Acceptance condition

AKR-3 passes only when:

- current architecture documents agree on their jurisdictions;
- one rule has one clear semantic owner;
- active authority contains no Raw Signal programme semantics;
- every September conformance concern has an explicit evidence-backed disposition;
- no stale authority-binding record remains;
- no second planning authority remains.

## 10. AKR-4 — Define the implementation-ready-brief ingress boundary

### Purpose

Create the exact boundary at which upstream semantic work ends and architecture-governed implementation can begin.

### Required law

The kernel must define a generic **implementation-authority ingress**.

An implementation tranche may begin only from:

```text
one exact implementation-ready brief
+
explicit current human/programme acceptance of that brief for implementation
+
exact immutable brief identity
```

The architecture must treat the brief as external semantic authority.

It must not require knowledge of how that brief was produced.

It must not require the upstream semantic methodology to exist inside this repository.

### Required responsibilities

The ingress boundary must establish only:

1. which exact brief bytes govern the implementation tranche;
2. that those bytes were explicitly accepted for implementation;
3. which architectural objects or structural surfaces the tranche proposes to create or modify;
4. which architecture constraints apply;
5. which tests and implementation changes are claimed to derive from that brief;
6. how those downstream artefacts remain traceable to the exact brief.

It must not reconstruct the source behind the brief.

It must not re-run upstream semantic gates.

It must not restate the entire brief into a second normative corpus merely for ceremony.

Where architectural registries require concise structural projections such as:

- semantic responsibility;
- inputs;
- outputs;
- exclusions;
- state ownership;
- time ownership;
- side effects;
- dependencies;

those projections must point back to the exact accepted brief and must not become an independent competing source of domain meaning.

### Failure rule

If implementation discovers that the accepted brief:

- lacks required meaning;
- contains an unresolved semantic contradiction;
- cannot lawfully map into the architecture;
- conflicts with a higher architectural invariant;

the implementation process must stop at that boundary.

It must not invent the missing meaning.

It must not launch a second semantic-reconstruction process inside the kernel.

The unresolved matter returns to the authority owner/upstream process.

### Coupling prohibition

The active architecture must not require identifiers or runtime knowledge specific to:

```text
M10
G1-G7
PMB
briefing_to_code_methodology
worker/tester submission numbering
semantic candidate numbering
```

Those may exist in upstream provenance but are opaque to the kernel.

### Acceptance condition

AKR-4 passes only when an exact accepted implementation-ready brief can be bound as implementation authority without importing or reproducing the upstream methodology.

## 11. AKR-5 — Complete dormant structural readiness

### Purpose

Finish the architecture controls required before the first real implementation brief is admitted.

### Static typed-seam enforcement

The current architecture requires typed public seams.

Select and admit one pinned development-only static type checker that:

- supports the pinned Python platform;
- can be reproduced in the offline/hermetic development environment;
- can actually detect incompatible Python-visible public-seam use;
- does not become a production/runtime dependency.

Do not select a tool merely by convention.

If no suitable tool can be installed under the admitted environment constraints, record the exact blocker and stop this dependent gate.

Add one repository-native entry point for type checking.

### Activation-path proof

Exercise the real committed architecture representations for future activation, including at minimum:

```text
valid M -> M dependency
undeclared M -> M dependency
forbidden reverse dependency
M dependency cycle
private cross-owner import
ImportFrom owner/seam bypass such as `from nvda_desk import m02`
named dynamic-import bypass
active M with incomplete required ownership
lawful M -> P dependency
lawful M -> K dependency
invalid P/K activation
malformed public-seam exception
invalid lifecycle identity
lawful historical predecessor identity
typed seam incompatibility
```

These tests must operate through the same schemas, registries and loaders future committed architecture will use.

Hand-built analyser-only fixtures cannot be the sole proof of a committed-configuration proposition.

The aggregate validator must be capable of accepting a minimally valid active `M` under the permanent architecture law. The reset-only invariant that the runtime module registry must remain empty must not survive as the first-active-module admission rule.

### Proof discovery and proposition binding

The proof system must account for every physical test file in each governed architecture/bootstrap jurisdiction according to the written law. If jurisdictional coverage is recursive, discovery must be recursive; a non-recursive top-level glob is insufficient.

Mechanical proposition-reference checks may establish that a proof artefact addresses/binds a proposition identifier. They must not be described as proving semantic entailment merely because the identifier text occurs in the file.

### Acceptance condition

AKR-5 passes only when the architecture can mechanically reject the representative invalid future states and accept the representative valid states it claims to support, including a lawful first active module, complete physical-test accounting, and the required Python-visible seam/type checks.

## 12. AKR-6 — COMPLETE — Rehearse exact implementation-authority ingress and gate-owned candidate resolution without adding business code

### Purpose

Prove that one exact externally accepted implementation-ready brief can cross the architecture-kernel boundary, receive only the bounded architectural judgement genuinely required from a worker, and then enter deterministic mechanical validation without importing the upstream methodology, inventing domain meaning, inheriting historical allocation numbers or admitting product behaviour.

AKR-6 is an ingress rehearsal, not implementation. It ends after a bounded architecture projection has been mechanically validated and any new-object identifiers have been resolved as candidates. It does **not** choose concrete package/public-seam import paths, derive behavioural proof from the brief, write brief-derived code, durably allocate an implementation identity, compose runtime objects or admit product behaviour.

### Recovery source and authority

The durable recovery source for this gate is the preserved corrected-projection checkpoint:

```text
source HEAD: 38fda5a22ffeade00ac9976ec87d979333a00390
checkpoint archive SHA-256: bc5f9f5eb573671ea57597bc822bb395e869c529be1d1eecf4c97f162cf949e3
external brief SHA-256: 938debe255d68668b0ae60f021d679fc8e3022be6eb050e7f3cd6112818fd342
```

That checkpoint is recovery evidence, not proof that its final AKR-6 projection was correct. In particular, its recorded `create:M16` projection and package/public-seam stop boundary must not be carried forward as current conclusions merely because they were committed.

Later sandbox-local AKR-6 work is not available as recoverable Git objects. Do not recreate missing commit SHAs or treat prior assistant reports as proof. Reconstruct the gate from current explicit user authority, this ExecPlan, current normative architecture law, the exact external brief and executable repository evidence.

The following already-established checkpoint dispositions remain governing unless contradicted by higher current authority:

- the exact external brief bytes remain unchanged;
- the inherited vocabulary-governance mechanism and its former `G02` structural allocation are `DO_NOT_CARRY_FORWARD` from the target active tree, not lifecycle-retired current identities;
- a literal architecture identifier appearing in the external brief does not automatically become a current architecture target;
- upstream M10/G1-G7/PMB metadata remains opaque to the kernel.

### Correct ingress boundary

The AKR-6 path is:

```text
exact accepted external brief bytes
        ->
exact-byte + external-acceptance binding
        ->
bounded architectural judgement
        ->
minimal projection intent
        ->
gate-owned candidate identifier resolution
        ->
mechanical create/modify validation
        ->
ACCEPT or precise REFUSAL
        ->
STOP before implementation
```

The bounded architectural judgement is the only semantic step in this gate. It may read the brief only far enough to establish:

- the architecture category required by each genuinely new responsibility;
- a concise responsibility name needed to distinguish separate new objects;
- whether a responsibility maps to an already-current object rather than creating a new one;
- ownership, consumer/composer and other architecture relationships required to make that projection;
- whether the projection can be made without inventing meaning or violating kernel law.

It does not judge domain merit and it does not choose numeric identifiers for new objects.

### Current post-reset identifier authority

Current explicit programme authority requires the post-reset allocation namespace to be determined from current post-reset state, not from the former product catalogue. Historical `M00-M16` product allocations do not reserve the same numeric identifiers in the new implementation namespace merely because they existed before the reset.

Permanent non-reuse applies prospectively to identities that are current, retired under current lifecycle authority, or durably recorded as post-reset implementation allocations. Historical pre-reset product numbering remains recoverable evidence and must not silently alias newly allocated current identities.

Therefore any current predecessor/successor values whose only meaning is a former product-number reclassification must not remain as active string-level lineage if reuse of the same post-reset identifier would make that historical string refer to a newly current object. Preserve the generic predecessor/successor lifecycle mechanism; disposition only the legacy current values that would create that alias.

### Minimal implementation-allocation history

Maintain one minimal machine-readable post-reset implementation-allocation history under `config/architecture/`. It is not a second architecture registry and must not duplicate ownership, dependencies, lifecycle status, seams or proof metadata.

Each durable post-reset implementation allocation records only:

```text
object_id
name
implemented_on
```

The ledger begins empty for the reset kernel and remains empty after AKR-6 because this gate performs no implementation admission. Candidate resolution consults the union of:

```text
current registered architecture identities
+
current retired identities
+
post-reset durable implementation allocations
+
earlier candidate resolutions within the same binding
```

For a new `M` responsibility when no current/post-reset `M` identity has been consumed, the first candidate must therefore resolve to `M00`. Two distinct new `M` responsibilities in the same binding must be representable and resolve deterministically to `M00`, then `M01`, rather than collapsing as duplicate identical create records.

Candidate resolution is **not** durable allocation. Re-running the same non-mutating rehearsal against unchanged current state may resolve the same candidate again. The identity becomes consumed only at a later separately authorised implementation/admission step that changes the current architecture/allocation state.

### AKR-6 recovery leaves

Work these leaves one semantic acceptance unit at a time. Commit each proved unit separately. Stop at the first failed required invariant.

#### AKR-6R1 — Reconcile current identifier and lineage authority

Establish the post-reset identity boundary in normative law and current registries before changing ingress mechanics.

Required work:

- reconcile `AK-ID-001` / lifecycle wording with the current post-reset allocation authority;
- inspect current foundation-object predecessor/successor values individually;
- disposition only legacy predecessor/lineage values whose sole function is pre-reset product-number reclassification and which could alias a newly current post-reset identifier;
- preserve generic lifecycle lineage capability for future post-reset replacement/split/merger work;
- rewrite or disposition any test whose sole proposition is preservation of those legacy active aliases, while retaining generic lifecycle negative/positive proof;
- ensure historical evidence remains recoverable through normal Git history and does not become a current allocation source.

Acceptance: a newly current `M00` cannot be mistaken for the historical predecessor formerly called `M00`, and the generic lifecycle mechanism still has executable proof.

#### AKR-6R2 — Establish the minimal post-reset allocation history and candidate resolver

Add the minimal `implementation_allocations` configuration/schema/loading surface and one deterministic candidate-resolution mechanism.

Required work:

- ledger fields are only `object_id`, `name`, `implemented_on` unless a further field is proved necessary;
- the reset ledger starts empty;
- candidate resolution uses current registered IDs, current retired IDs, durable post-reset allocation IDs and earlier candidates in the same request;
- no historical crosswalk or former M-number catalogue participates in allocation;
- category extension remains open-ended beyond `99`;
- no AKR-6 operation writes the ledger.

Acceptance: the repository mechanically resolves the first presently available `M` candidate as `M00`, supports sequential same-category candidates, and leaves the committed ledger unchanged.

#### AKR-6R3 — Correct the semantic/mechanical contract and make numeric resolution gate-owned

Change the implementation-authority binding contract so the worker supplies only the semantic projection information that cannot be derived mechanically.

For a new object, the projection input must contain a category and a concise responsibility name and must not contain a caller-selected `object_id`. For an existing object, the projection input must contain the existing `object_id` and must not masquerade as a create request.

The gate must itself resolve each create intent to the canonical current candidate identifier before create/modify state validation. The repository-facing template, Python data model, schema, validator and CLI output must all express the same contract.

The responsibility name exists to distinguish multiple independent creates of the same category; it is not a package name, Python import path, public-seam name or new source of domain authority.

Acceptance: a caller cannot force historical `M16` as the numeric create identity; `create {category: M, name: ...}` resolves mechanically from current state, while `modify:A00` remains a bounded semantic mapping whose existence is mechanically checked.

#### AKR-6R4 — Rebuild focused mechanical proof around the real repository-facing path

Derive focused tests from the corrected contract rather than adapting validation merely to obtain green.

Required proof includes at minimum:

```text
exact brief bytes match bound SHA-256
changed bytes fail closed
missing/invalid external acceptance record fails
upstream methodology metadata cannot become ingress authority
create forbids caller-supplied object_id
create requires lawful category and distinguishing name
first empty-M candidate resolves to M00
multiple distinct same-category creates resolve M00, M01, ... in order
current/retired/durable-allocation identities are not reused
modify requires an existing current object
invalid/nonexistent modify fails
production registries are not mutated by rehearsal
implementation-allocation ledger is not mutated by rehearsal
repository binding template validates against the same schema/code path it documents
```

Use the real schemas/loaders/registry state for committed-configuration propositions. Hand-built fixtures may supplement but not replace proof of the actual repository path.

Acceptance: tests falsify the former caller-numbered design and exercise the same path a future worker will actually invoke.

#### AKR-6R5 — Re-run the exact brief and perform a human semantic trace

Use the exact external brief identified above. Do not modify its bytes to make the rehearsal fit the kernel.

Read it only far enough to establish the bounded architecture projection from current authority. For the preserved rehearsal brief, verify directly from the brief rather than from the old projection receipt whether it establishes:

- one new coherent runtime semantic ownership responsibility in category `M`;
- the concise responsibility name `raw_signal_occurrence_truth`;
- `A00` as the existing initial caller/consumer/composer mapping;
- `P01` and `K01` as non-active/non-consumers for this slice;
- literal historical/upstream identifiers such as `M16` or `G02` that must not themselves force current target allocation.

If any of those propositions is not established by the exact brief plus current higher authority, stop rather than reconstructing the lost conclusion from memory.

Feed only the resulting minimal projection intent into the mechanical gate. The expected candidate is not authority; it must be produced by the resolver from current state.

Then trace the path manually as a future human would: exact input -> template/binding -> parser/schema -> resolver -> registry/ledger state -> result. Inspect active human-facing historical documents that could reasonably mislead a future worker into treating reset-era imperative wording as current authority. Where needed, add a prominent historical/non-governing status notice rather than rewriting the historical substance.

Acceptance: the exact brief traverses the real path without package/public-seam invention, legacy-number inheritance, hidden ledger mutation or upstream-methodology coupling, and the human-facing route agrees with the executable route.

#### AKR-6R6 — Reconcile evidence, close only from executable proof, and preserve a durable checkpoint

Replace/supersede stale AKR-6 projection evidence so it describes the executable contract actually proved. Do not retain `create:M16` or package/public-seam naming as the current AKR-6 result if the corrected path does not produce those propositions.

Before declaring AKR-6 complete:

- rerun all validation that bears on the changed surfaces;
- run the exact external brief through the repository-native ingress command;
- record the exact candidate resolutions and the fact that they are non-durable;
- verify production `modules` and `surfaces` remain empty;
- verify `implementation_allocations` remains empty;
- human-read the changed code, schema, template, normative law, evidence and tests as one end-to-end path;
- run repository-integrity checks required by the ExecPlan;
- leave a clean committed state;
- create a durable full-Git checkpoint/bundle of the closed AKR-6 state **before AKR-7 begins** so a volatile sandbox loss cannot require reconstruction again.

### Negative proof

In addition to the leaf-specific proof above, the rehearsal must fail closed for at least:

- missing brief identity;
- changed brief bytes under the same claimed binding;
- absent implementation acceptance;
- structurally invalid projection intent;
- caller attempt to select a numeric create identity;
- reuse of a current, retired or durably post-reset allocated identity;
- nonexistent modify target;
- attempt to treat upstream methodology metadata or literal historical identifiers as current architecture authority.

Do not require package/public-seam naming, behavioural proof derivation, dependency/seam implementation validation or candidate composition merely to close AKR-6. Those are downstream implementation/admission concerns and importing them here recreates the package-naming blocker found in the preserved checkpoint.

### Acceptance condition

AKR-6 passes only when all six recovery leaves are established from current evidence and the exact external brief can traverse the corrected boundary as:

```text
external exact bytes
        ->
bounded judgement supplies create category/name + existing modify mapping
        ->
kernel resolves new numeric candidate(s)
        ->
mechanical ingress validation
        ->
accepted bounded target projection
        ->
STOP
```

For the preserved rehearsal input, no numbered create target may be preselected by the worker. If the current `M` allocation state is still empty when the exact rehearsal is executed, the kernel must itself resolve `raw_signal_occurrence_truth` to candidate `M00`; that outcome is a consequence to verify, not a value to encode into the semantic projection input.

The committed production state after AKR-6 remains behaviour-neutral:

```yaml
modules: []
surfaces: []
implementation_allocations: []
```

No `COMPLETE` claim is permitted until the code path, schema, template, normative wording, focused tests, exact-brief rehearsal evidence and human end-to-end trace all agree.

## 13. AKR-7 — Final pristine-kernel proof

AKR-7 must not begin until AKR-6R6 has closed AKR-6 from executable proof and a durable full-Git checkpoint of that closed state has been created.

### Required proof classes

#### Environment

Reconstruct the locked development environment from the repository's admitted offline dependency surface.

#### Static architecture

Run the architecture schema/registry validator.

#### Dependency and seam proof

Run declared dependency and public-seam validation.

#### Type proof

Run the admitted static type checker.

#### Architecture tests

Run the complete admitted architecture/bootstrap blocking set.

#### Promotion

Run the registry-derived `architecture_kernel` promotion set.

#### Packaging

Build the distribution and install it outside the repository root.

Verify that the installed package imports without repository path injection.

#### Exclusion

Prove the built artefact contains no:

- historical production modules;
- Raw Signal implementation;
- Raw Signal semantic authority;
- Raw Signal orchestration;
- behavioural test population from removed programmes;
- product console entry point;
- domain production dependency.

#### Repository integrity

Run:

```text
git diff --check
git fsck --full
git status
```

and any additional proof genuinely required by the changed surfaces.

### Final state assertions

The closeout must establish from evidence that:

1. the active tree is behaviour-neutral;
2. no product module is active;
3. no architecture surface is active unless separately admitted;
4. the kernel contains no upstream semantic-reconstruction process;
5. the kernel contains no Raw Signal semantic programme;
6. the kernel accepts an exact external implementation-ready brief through one generic ingress boundary;
7. architectural allocation remains open-ended;
8. future code is constrained by declared ownership, dependencies, public seams, lifecycle and proof;
9. typed public seams are mechanically checked;
10. packaging is minimal and reproducible;
11. historical product/domain work remains recoverable from Git history;
12. all unresolved matters are explicitly reported.

## 14. Expected target tree

The exact inventory is governed by AKR-1, but the target shape is approximately:

```text
GUARDRAILS.md
AGENTS.md
EXEC_PLAN.md
README.md
LICENSE
Makefile
pyproject.toml
uv.lock
.python-version

config/
  architecture/
  proof/
docs/
  architecture/
  provenance/

schemas/
  architecture-object schemas
  dependency/proof schemas
  minimal implementation-authority-ingress schema if mechanically required

templates/
  module/
  protocol/
  governance_plane/
  application_shell/
  kernel/
  surface/

src/
  nvda_desk/
    architecture/
    composition/

tests/
  architecture/
  bootstrap/

tools/
  architecture validation
  dependency validation
  public-seam validation
  proof/promotion runner
```

No domain package is required for a pristine kernel.

No upstream methodology package is required.

## 15. Definition of "ready to accept a coding brief"

The repository is ready only when a future worker can receive an accepted implementation-ready brief and answer these questions without inventing architecture:

```text
What architectural object owns each required responsibility?
What are its lawful inputs and outputs?
What does it explicitly not own?
What state/time/side effects does it own?
What other owners may it depend on?
What is its sole public seam?
How is it composed?
Which exact tests prove its brief-derived obligations?
Which structural tests prove architectural legality?
What exact brief authorised each implemented obligation?
```

The architecture supplies the framework for those answers.

The implementation-ready brief supplies the domain meaning.

Neither system duplicates the other's job.

## 16. Deferred work

The following remain outside this ExecPlan:

- design of the future implementation-writing methodology;
- implementation of any real coding brief;
- Raw Signal semantic admission;
- historical M16 re-admission;
- DMPV3 activation;
- state/transaction activation;
- product module allocation;
- product build order;
- PMB ordering solution;
- Python 3.14 migration;
- UUIDv7 adoption;
- deployment or production readiness.

## 17. Closeout

Closeout must report:

- starting commit;
- final commit;
- exact retained-file inventory;
- exact `DO_NOT_CARRY_FORWARD` inventory;
- rewritten control surfaces;
- implementation-brief ingress surface;
- dependency/toolchain changes;
- complete commands executed;
- exact observed validation results;
- final registry state;
- final package contents;
- unresolved/deferred matters;
- `git diff --check` result;
- `git fsck --full` result;
- final clean-worktree evidence.

No `PASS`, `COMPLETE`, `PRISTINE`, `READY`, or equivalent claim is permitted unless the evidence establishes the exact corresponding proposition.

## 18. Terminal outcomes

Return exactly one:

```text
PASS
FAIL_REPAIRABLE
BLOCKED
```

`PASS` means only:

> The repository is a clean, behaviour-neutral, structurally proven architecture kernel with a generic exact implementation-ready-brief ingress boundary and no active product semantics or duplicated upstream semantic methodology.

It does not mean that any product capability has been implemented.

It does not mean the future brief-to-code implementation worker exists.

It means the repository is structurally ready for that future work.

## 19. Current progress — reconstructed execution

The prior sandbox-local AKR commits were lost and were not recoverable as Git objects. Under explicit user authority, this tranche was re-executed from the preserved source repository rather than recreating lost SHAs from narrative summaries.

### Reconstructed source and governance

- preserved source baseline: `892a6c042f19d19d84a3d1fb2c639033789f9bc1`;
- reconstructed accepted governance/control-surface commit: `caea0c7bffb5d62b215ae2884f6ab22beaf39406`.

### AKR-1 — COMPLETE

- branch: `work/akr-1-end-state-inventory`;
- reconstructed AKR-1 commit: `985c9cec866e6690e6268aafa181cc7840602b60`;
- exact tracked/inventory coverage at close: `218 / 218`;
- classifications: `KEEP 54`, `REWRITE 39`, `HISTORICAL_ONLY 3`, `DO_NOT_CARRY_FORWARD 122`, `BLOCKED 0`;
- reproduced challenge findings include the `ImportFrom` public-seam blind spot, reset-only active-module aggregate blocker and non-recursive physical-test discovery.

### AKR-2 — COMPLETE

- branch: `work/akr-2-programme-surface-carry-forward`;
- programme-surface mutation commit: `ab6641b28bef8307e4e921d0aa4b524050980840`;
- 63 AKR-1-classified Raw Signal/programme-specific paths are no longer present in the active tree and remain recoverable from prior Git commits;
- directly affected generic orientation surfaces were rewritten: `README.md`, `tests/AGENTS.override.md`, `docs/provenance/CLEAN_REPOSITORY_PROVENANCE.md`, and the stale `/PLANS.md` sdist reference in `pyproject.toml`;
- structural validation passed;
- architecture/bootstrap proof passed: `38 passed` on CPython `3.13.5` / pytest `9.0.3`;
- registry-derived `architecture_kernel` promotion passed on the committed AKR-2 state;
- `git diff --check` passed and `git fsck --full` reported no repository-integrity defect.

### AKR-3 — COMPLETE

- branch: `work/akr-3-architecture-authority-reconciliation`;
- commit: `38ea93e482717180959afea9aa6b19659025368b`;
- steady-state architecture authority was reconciled without reactivating the historical `M00-M15` product allocation;
- `OWNERSHIP_AND_COMPONENT_LAW.md` carries forward generic owner/component/state-role separation;
- the known checker/proof/type-mechanical gaps were explicitly left for AKR-5 rather than being claimed as proved by normative text.

### AKR-4 — COMPLETE

- branch: `work/akr-4-implementation-brief-ingress`;
- commit: `fcf2d9a6c8b28ab91a4b90673bfafc261f222d47`;
- a generic implementation-authority ingress binds exact brief bytes, an external implementation-acceptance reference and a bounded create/modify architectural projection;
- the ingress does not embed the brief, M10, G1-G7, PMB or upstream semantic-reconstruction machinery;
- revalidation immediately before AKR-5 entry observed structural validation PASS, Ruff PASS, `44 passed` architecture/bootstrap tests and `44 passed` registry-derived architecture promotion.

### AKR-5 — COMPLETE

- branch: `work/akr-5-dormant-structural-readiness`;
- initial blocker commit: `3d0f2330f76f54bd4fd0257c35391ed3bee7fa94`;
- the missing checker dependency was supplied as `NVDA_AKR5_TYPECHECKER_DEPENDENCY_INGRESS_20260909.tar(1).gz`, SHA-256 `3d4e9aa4f7483143f40c30a838f63b6c8b83abcaeee9a8bc8cfdefa5320bd00a`;
- pinned development-only checker: `mypy==1.20.1`; the required missing wheels are now part of the repository-local offline wheelhouse and the lock resolves with `uv --offline`;
- functional implementation commit: `c335b33974fb6e4b4ac2e1987697ba4e5fe6cc3b`;
- the aggregate validator now accepts a lawful first active module instead of enforcing the reset-only empty-module invariant;
- active Python-visible owners must have a physically present registered package and public seam;
- the reproduced `ImportFrom` owner/seam bypass is repaired and blocking proof covers it;
- proof discovery is recursive across the governed architecture/bootstrap jurisdictions;
- active-module structural projection now makes component-form and state writer/reader/persistence/replay declarations explicit;
- lawful P/K activation and invalid P/K package/seam states are exercised through the committed schemas/loaders;
- `make typecheck` is the repository-native static-check entry point; current source passes it and blocking proof demonstrates rejection of an incompatible typed public-seam call;
- clean-worktree `architecture_kernel` promotion at the functional commit passed `62` tests across `11` admitted families;
- Ruff, offline lock verification, `git diff --check` and `git fsck --full` completed without reported failure;
- exact AKR-5 evidence is recorded in `docs/evidence/akr5/AKR5_STRUCTURAL_READINESS.md`.

### AKR-6 — COMPLETE (reconstructed)

The durable recovery point was `38fda5a22ffeade00ac9976ec87d979333a00390`, supplied by the preserved corrected-projection checkpoint whose archive SHA-256 is `bc5f9f5eb573671ea57597bc822bb395e869c529be1d1eecf4c97f162cf949e3`. The bound external brief remained exact and unchanged at SHA-256 `938debe255d68668b0ae60f021d679fc8e3022be6eb050e7f3cd6112818fd342`.

The reconstruction was planned at `b116445bc0145daa4b8952400809cb029a2de1de` and then executed as bounded semantic units:

- AKR-6R1 — post-reset identity/lineage boundary: `d6f23bb58b1aaf1eee8ab6d9a2ce4f4901d4ffdf`;
- AKR-6R2 — minimal allocation history and non-mutating candidate resolver: `66422b0329460e085637bf16859f63956a4a3f60`;
- AKR-6R3 — create category/name contract and gate-owned numeric candidate resolution: `c6ab75bbf9412ad7a2c758d44254a568942274a6`;
- AKR-6R4 — focused proof of the repaired ingress mechanics: `165d5a40ec9a8582c2dbaa5f3a57897226e4d1e4`;
- AKR-6R4 human-trace correction — repository command output aligned with non-durable candidate semantics: `04ea962ef92edfeff16dca37a981946a541884a2`;
- AKR-6R5 — exact-brief semantic/executable trace: `ff028950813e3e398a243a2b1252ecf79caa277e`.

The reconstructed path no longer carries the checkpoint's `create:M16, modify:A00` result or package/public-seam naming blocker as current AKR-6 evidence. That stale projection-attempt file is `DO_NOT_CARRY_FORWARD` from the closed active tree and remains recoverable through ordinary Git history. The current non-normative trace is `docs/evidence/akr6/AKR6_HUMAN_TRACE.md`.

The exact brief establishes, for this bounded rehearsal, one coherent new runtime semantic owner named `raw_signal_occurrence_truth`, A00 as the existing sole initial caller/consumer/composer mapping, and P01/K01 as non-active non-consumers. Current higher authority prevents literal historical `M16`/`G02` strings from forcing current post-reset allocation. The minimal projection intent therefore supplies `create {category: M, name: raw_signal_occurrence_truth}` plus `modify:A00`; it does not supply a numbered create target.

Repository-native execution resolves that create intent non-durably from current state and produces:

```text
PASS: implementation authority brief_sha256=938debe255d68668b0ae60f021d679fc8e3022be6eb050e7f3cd6112818fd342
candidate_targets: create:raw_signal_occurrence_truth->M00, modify:A00
```

Candidate `M00` is not a durable implementation allocation. The rehearsal writes no production object, registry row, package, public seam or allocation record. At close the committed production state remains:

```yaml
modules: []
surfaces: []
implementation_allocations: []
```

Pre-close proof on the reconstructed R1-R5 state established structural validation with four architecture objects, zero active runtime modules, zero implementation allocations and zero dependency/public-seam violations; mypy reported no issues in 13 source files; the complete architecture/bootstrap proof set passed `74` tests; and the registry-derived `architecture_kernel` promotion set passed the same `74` tests across `11` admitted paths. The exact external brief command produced the candidate result above. These results prove the bounded structural/ingress propositions they exercise; they do not prove downstream domain implementation.

AKR-6R6 closes by carrying the stale projection evidence out of the active tree, reconciling this progress record with the executable path, re-running the required proof on the committed closeout state, and creating a durable full-Git checkpoint before AKR-7 begins. AKR-7 remains blocked until that checkpoint has been created and verified.
