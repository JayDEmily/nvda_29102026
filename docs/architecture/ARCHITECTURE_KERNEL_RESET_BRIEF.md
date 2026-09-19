# Architecture Kernel Reset Brief

> **Historical evidence only — not current governing architecture authority.** This document records the 2026-08-04 reset task and intentionally preserves its then-current imperative wording. Current work is governed by `GUARDRAILS.md`, the accepted `EXEC_PLAN.md` and the steady-state architecture documents. In particular, references here to the former `G02` vocabulary-governance mechanism or former product identifiers must not be used to reactivate or reserve those historical allocations in the current post-reset namespace.

## Objective

Convert the current repository into a minimal, behaviour-neutral and extensible architecture kernel.

The resulting repository must retain only the architectural laws, packaging configuration, governance mechanisms and structural validation needed to build a modular Python system. It must not retain the existing business implementation, historical feature allocation or any assumption that the former `M00–M15` catalogue is complete or permanently correct.

The architecture must support the controlled admission, division, merger, replacement, deprecation and retirement of architectural objects without redesigning the repository.

This task does not define or implement any business capability.

## Required outcome

The final repository must provide:

1. a reusable modular-monolith foundation;
2. an open-ended declarative registry for architectural objects;
3. mechanically checked dependency and public-seam laws;
4. category-specific templates for future modules, protocols, governance planes, application shells, kernels and surfaces;
5. generic proof-admission, promotion and vocabulary-governance machinery;
6. no active inherited business or production behaviour;
7. no fixed enumeration or maximum count for future architectural objects;
8. preserved Git history containing the removed implementation.

The result is an architecture kernel, not an empty repository. Registry loading, schema validation, dependency analysis, packaging and test execution are lawful retained technical behaviours.

## Authority and source discipline

Read before modification:

- root `AGENTS.md`;
- applicable `AGENTS.override.md`;
- `00_TASK/PROJECT_EXECUTION_METHOD.md`;
- the active architecture blueprint;
- the testing and promotion authority;
- the supplied architecture and test-lineage audit;
- the current packaging, lock and build configuration.

Use the supplied audit to identify reusable laws and mechanisms. Do not treat it as proof that the current business implementation, ownership allocation or test population is semantically correct.

For every retained architecture or testing law, record its lineage as one of:

- `DIRECT_REPOSITORY_AUTHORITY`;
- `EXTERNAL_CORROBORATION`;
- `PROJECT_SPECIFIC_SYNTHESIS`;
- `PROJECT_SPECIFIC`;
- `UNKNOWN`.

Use official AWS, Google, Microsoft, IBM, Python and Python Packaging Authority sources. Do not claim that an external source originated a project-specific construct unless direct evidence establishes that lineage.

## Architectural-object taxonomy

Do not classify every architectural object as a module.

Identifiers consist of a category prefix followed by a monotonically allocated integer, zero-padded to at least two digits. `M00` through `M99` are followed by `M100`, `M101`, and so on. Equivalent allocation applies to `P`, `G`, `A`, `K` and `S`.

Identifiers are permanent historical identities. A retired identifier must never be reused for different meaning. Registry schemas must not contain a fixed enumeration or maximum numeric value.

### M — runtime semantic ownership module

A runtime module owns a coherent domain decision, transformation, policy or lifecycle.

A module must have:

- one explicit semantic responsibility;
- declared inputs and outputs;
- declared permitted dependencies;
- one declared typed public seam;
- replaceable internal implementation;
- independently testable obligations;
- explicit identity, state, time and side-effect ownership where relevant;
- no private cross-owner imports;
- no dependency cycles.

The number of runtime modules is not fixed. A new `M` identifier may be allocated only when an independent semantic ownership boundary has been established. A package, class, route or test directory does not establish module ownership by itself.

### P — protocol or governed information carrier

A protocol defines an information shape and the rules governing its identity, versioning, validation, compatibility and carriage. A protocol is not a runtime semantic owner and must not independently make domain decisions.

Register `P01` as `dmp_v3` with status `placeholder`. `P01` records the historical identity of DMPV3 as a protocol and carrier. Do not implement its schema or behaviour during this reset.

### G — continuous governance plane

A governance plane constrains, evaluates or projects the system. It is not a runtime business service.

Register:

- `G01` — `proof_and_promotion`, status `framework`;
- `G02` — `vocabulary`, status `framework`.

`G01` governs test admission, proof tier and lifecycle, normative traceability, proof-block membership, promotion sets and validation receipts.

`G02` governs canonical terminology, definition and alias admission, deprecation and replacement, identifier terminology and generated vocabulary projections.

Runtime modules must not import governance-plane implementation.

### A — application shell and composition

Register `A00` as `application_shell` with status `bootstrap`.

The application shell owns process startup and shutdown, dependency construction, adapter and transport translation, configuration injection, top-level run lifecycle and composition of admitted objects. It must not own business decisions or hide dependencies through a service locator.

The reset may retain a minimal composition-root skeleton, but it must not instantiate fictional domain modules.

### K — shared technical kernel or mechanism

Register `K01` as `state_and_transaction` with status `placeholder`.

A kernel may provide domain-neutral mechanisms such as transaction coordination, idempotency, atomic receipt handling, storage abstractions, clocks or technical identity primitives. A kernel must not acquire the semantic ownership of modules that use it.

Do not implement state or transaction behaviour during this reset.

### S — architecture surface

A surface is an end-to-end responsibility, assurance view or trace across multiple architectural objects. It is not automatically a package or semantic ownership module and does not establish implementation completion.

The active surface registry must begin empty. Do not import the former eighteen-surface catalogue as active architecture. Preserve it only as historical evidence where necessary.

## Dependency laws

The permitted dependency model must be declared in machine-readable form and checked against the Python import graph.

At minimum:

| Source category | Permitted dependencies |
|---|---|
| `A` application shell | Declared public seams of `M`, `P` and `K`; adapters and configuration |
| `M` runtime module | Its own internals; declared public seams of other `M` owners; admitted `P` contracts; admitted `K` abstractions |
| `P` protocol | Standard library, typing and protocol-local validation mechanisms only |
| `K` kernel | Domain-neutral technical dependencies; no dependency on runtime modules |
| `G` governance plane | May inspect repository artefacts through tooling; must not become a runtime dependency |
| `S` surface | Registry and documentation only unless later authority establishes otherwise |

Additional laws:

1. Every dependency edge must be declared before use.
2. Runtime module dependencies must be acyclic.
3. `M`, `P` and `K` must not depend on `A`.
4. Runtime code must not depend on `G` or `S`.
5. `P` must not contain domain decisions or orchestration.
6. `K` must not contain module-specific policy or vocabulary.
7. A surface must not become a package merely because it is registered.
8. Physical location does not prove semantic ownership.
9. A registry row does not prove implementation.
10. Placeholder objects must not be composable as implemented objects.

## Python public-seam law

Python naming conventions do not enforce access control. The repository must therefore define and mechanically enforce its own public-seam law.

Each runtime owner must declare exactly one cross-owner import target, normally either the package root or an explicit `api.py` or equivalent public contract module. The chosen target must be recorded in the object registry.

The architecture checker must reject imports from another owner’s undeclared submodules, imports from paths marked internal, relative-path workarounds, dynamic imports that evade registry validation and undeclared cross-owner dependencies.

`__all__`, leading underscores and type annotations may document the public interface but do not by themselves satisfy mechanical enforcement.

Typed seams are a project requirement enforced by the configured static-analysis toolchain. Do not claim that Python enforces type contracts at runtime unless explicit runtime validation exists.

## Extension, replacement and retirement law

Adding an instance of an existing architectural-object category must not require changing central source code beyond declarative registration, category-specific files generated from a template, application-shell composition where runtime participation is required and proof and vocabulary admission.

Do not implement fixed identifier enumerations, identifier-specific dispatch tables, hard-coded maximum counts, implicit filesystem discovery as architecture authority or runtime service-location through the registry.

A future runtime module must be addable by:

1. allocating the next unused `M` identifier;
2. declaring its semantic responsibility and exclusions;
3. declaring its inputs, outputs and ownership;
4. declaring permitted dependency edges;
5. creating its package from the module template;
6. defining its typed public seam;
7. admitting its vocabulary and normative obligations;
8. adding proposition-traced tests;
9. composing it at an application shell;
10. passing architecture and promotion validation.

For any split, merger, replacement or retirement, preserve original identifiers, record predecessor and successor relationships, record semantic migration and compatibility effects, prevent retired objects from active composition, never reuse retired identifiers and retain historical traceability through Git and the crosswalk.

The same admission and lifecycle principles apply to protocols, governance planes, shells, kernels and surfaces, but their templates must not imply that every category requires executable runtime code.

## Retain or reconstruct

Retain only assets required by the architecture kernel:

- `pyproject.toml`;
- build-system configuration;
- package and test bootstrap configuration;
- a reproducible minimal dependency lock;
- modular-monolith dependency laws;
- the private cross-owner import prohibition;
- the typed public-seam requirement;
- the composition-root law;
- separation of semantic ownership from shared mechanisms;
- generic proof-admission and promotion machinery;
- generic vocabulary-governance machinery;
- architecture registry and validation tooling;
- the prior architecture audit as historical evidence;
- full Git history.

Review every retained dependency. Remove dependencies required only by deleted production behaviour, then regenerate the lock from the minimal admitted toolchain.

## Remove from the active tree

Delete from the active branch:

- existing production and domain implementations;
- existing `m00_...` through `m15_...` packages;
- compatibility and migration packages;
- current business contracts and packet implementations;
- former module-specific public APIs;
- inherited behavioural tests;
- inherited test-family admissions and proof-block populations;
- Atlas and cohort artefacts;
- Behaviour Register artefacts;
- migration ledgers;
- execution receipts;
- implementation-completion reports;
- stale architecture overlays describing implementation status;
- hard-coded assumptions that the former module catalogue is exhaustive;
- packaging entry points and dependencies belonging only to removed behaviour.

Do not copy deleted material into a new archive directory. Git history is the implementation archive.

Historical crosswalk and audit evidence may remain because they explain lineage; they must not be importable or composable runtime authority.

## Required repository structure

Create a minimal structure equivalent to:

```text
AGENTS.md
PLANS.md
pyproject.toml
<minimal dependency lock>
docs/architecture/
docs/history/
docs/evidence/architecture_audit_20260804/
config/architecture/
config/proof/
config/vocabulary/
schemas/
templates/{module,protocol,governance_plane,application_shell,kernel,surface}/
src/nvda_desk/{architecture,composition}/
tests/{architecture,bootstrap}/
tools/
```

The detailed required files are stated in the execution plan and acceptance proof. Equivalent naming is acceptable only where it improves precision without altering the required separation or outcome.

## Initial active registry state

The runtime module registry must begin empty:

```yaml
modules: []
```

Register only these non-module structural identities:

```yaml
protocols:
  - id: P01
    name: dmp_v3
    status: placeholder

governance_planes:
  - id: G01
    name: proof_and_promotion
    status: framework
  - id: G02
    name: vocabulary
    status: framework

application_shells:
  - id: A00
    name: application_shell
    status: bootstrap

kernels:
  - id: K01
    name: state_and_transaction
    status: placeholder

surfaces: []
```

Do not create fictional implementation to satisfy a registry row.

Registry validation must distinguish at least `placeholder`, `bootstrap`, `framework`, `active`, `deprecated` and `retired`. Only an `active` executable object may be selected for runtime composition.

## Proof and promotion reset

Preserve the generic Tier A/B/C and lifecycle machinery, but remove all inherited family admissions and proof-block populations.

Re-establish only the proof required for the architecture kernel.

- **Tier A:** current blocking proof for an admitted architecture-kernel proposition.
- **Tier B:** bounded shadow proof relevant to current work but not blocking under current authority.
- **Tier C:** separately executable historical, observational, slow or operational assurance that is not currently blocking.

Tier and lifecycle are independent fields. Folder placement, filename or a historical registry row must not create proof authority.

Every admitted test family must have an exact physical path, one tier, one lifecycle, exact normative proposition identifiers, an owning proof block and an explicit promotion-set disposition.

Initial proof state:

- admit only the new architecture and bootstrap test families;
- place current architecture-kernel laws in Tier A;
- leave Tier B and Tier C empty unless a specific retained proof justifies admission;
- do not admit any former behavioural test;
- do not carry forward former proof-block or promotion-set membership.

Mechanical proof establishes only the architecture-kernel propositions it names. It does not establish future domain semantics.

## Historical identifier crosswalk

Create a historical crosswalk without preserving former identifiers as active architecture:

| Former identifier | Historical reclassification |
|---|---|
| `M00` | `A00` application shell |
| `M04` | `P01` DMPV3 protocol and carrier |
| `M13` | `K01` state and transaction kernel |
| `M14` | `G01` proof and promotion governance |
| `M15` | `G02` vocabulary governance |
| `M01–M03`, `M05–M12` | Historical candidate runtime modules; inactive unless independently re-established |

The crosswalk is evidence of historical classification only. It must not admit, implement or reserve future runtime semantics.

## Root AGENTS.md

Replace the root `AGENTS.md` with a concise operating map stating that the repository is a behaviour-neutral extensible architecture kernel; former packages and Git history are not active business authority; object categories must not be conflated; runtime modules require a demonstrated semantic ownership boundary; dependency edges and public seams must be declared; private cross-owner imports are prohibited; registries are declarative metadata, not service locators; placeholder registration does not prove implementation; ambiguity must be reported rather than filled with invented architecture; production behaviour is outside this reset; and the authoritative architecture documents and validation commands.

## ExecPlan

Replace `PLANS.md` with one self-contained ExecPlan for the reset. It must record exact base commit, governing authority, complete files inspected, retained and deleted assets, dependency and lock changes, taxonomy and lineage decisions, proof reset, validation commands and observed output, deviations, unresolved matters, commit sequence and final Git state.

Do not create a subsequent capability-development plan.

## Required validation

At minimum, prove:

1. a clean environment can install the project from the regenerated lock;
2. a built wheel or source distribution installs outside the repository root;
3. all retained Python imports resolve in that installed environment;
4. the active runtime-module registry is empty;
5. identifiers use the correct category and unbounded numeric form;
6. retired identifiers cannot be reused;
7. all registries conform to their schemas;
8. all dependency edges are declared;
9. the active runtime dependency graph is acyclic;
10. cross-owner imports use only declared public seams;
11. governance and surface artefacts are not runtime dependencies;
12. placeholders cannot be composed as implemented objects;
13. no former production package remains importable or included in built distributions;
14. no former console entry point or production dependency remains active;
15. no inherited behavioural test is admitted;
16. every retained architecture test has exact proof admission and normative traceability;
17. the architecture does not impose a maximum identifier count, including the transition from `M99` to `M100`;
18. architecture, bootstrap and promotion-control tests pass;
19. `git diff --check <base>..HEAD` passes;
20. `git fsck --full` reports no repository-integrity defect;
21. the final worktree is clean.

Retain exact commands and unabridged output. State explicitly that these checks prove structural and bootstrap properties only. They do not prove any future domain design or implementation.

## Branch and commit requirements

Perform the reset on `work/architecture-kernel-reset-v1` from exact base commit `d24f9626a23b526384668b3cb26ee811b235eb5c`.

Preserve the existing Git history. Do not rewrite, squash or orphan the historical repository.

Use bounded commits with one clear purpose each.

## Return requirements

Return terminal verdict, branch name, base commit, final `HEAD`, commit list, retained-file inventory, deleted-file inventory, dependency and lock changes, final repository tree, registry state, proof-family and promotion-set state, validation commands and exact output, lineage index, unresolved matters, clean-worktree evidence, a full-history downloadable tarball and its SHA-256.

## Terminal condition

Return exactly one of `PASS`, `FAIL_REPAIRABLE` or `HARD_BLOCK`.

`PASS` requires a clean, installable, business-behaviour-free and extensible architecture kernel with category-correct non-reusable identifiers, an empty active runtime-module registry, no inherited business implementation or behavioural proof, mechanically enforced dependency and public-seam laws, minimal reproducible packaging, proposition-traced architecture proof, preserved Git history and passing required validation.

A mechanically green result must not be represented as proof of future domain semantics.
