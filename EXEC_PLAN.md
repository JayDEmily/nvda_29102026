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
- architecture vocabulary;
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
- vocabulary configuration;
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

## 12. AKR-6 — Rehearse brief-to-implementation ingress without adding business code

### Purpose

Prove that the pristine architecture is genuinely ready for the next system.

### Method

Use a bounded synthetic/test-only implementation-ready brief.

It must contain no NVIDIA trading or Raw Signal meaning.

The rehearsal must demonstrate:

```text
exact accepted brief binding
        ->
architecture-object projection
        ->
registry/schema validation
        ->
dependency/public-seam validation
        ->
proof derivation/admission
        ->
candidate composition validation
```

The rehearsal must not leave a synthetic runtime module active in the committed production registry.

The repository's final production state remains:

```yaml
modules: []
surfaces: []
```

unless separate human authority explicitly changes that invariant.

### Negative proof

The rehearsal must also establish failure for at least:

- missing brief identity;
- changed brief bytes under the same claimed binding;
- absent implementation acceptance;
- structurally invalid object projection;
- undeclared dependency;
- unlawful seam;
- attempt to treat upstream methodology metadata as architecture authority.

### Acceptance condition

AKR-6 passes only when the complete generic ingress path is exercised without domain semantics and without coupling the kernel to the upstream methodology.

**A new accepted implementation-ready brief must be able to enter without requiring modification of the kernel's foundational architectural laws.**

## 13. AKR-7 — Final pristine-kernel proof

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
  vocabulary/

docs/
  architecture/
  provenance/

schemas/
  architecture-object schemas
  dependency/proof/vocabulary schemas
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

### Next authorised acceptance unit

`AKR-3 — Reconcile and simplify architecture authority`.

Do not begin AKR-4 or later work until AKR-3 acceptance conditions are established.
