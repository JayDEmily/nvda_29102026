# Architecture Kernel

## Status

Accepted authority for the behaviour-neutral architecture kernel created by the 2026-08-04 reset brief.

## Purpose

This repository provides the structural laws and proof machinery required to admit future capabilities without retaining or implying any former NVDA business behaviour.

The kernel owns:

- architectural-object taxonomy;
- declarative object registration;
- dependency and public-seam validation;
- composition eligibility;
- object lifecycle and immutable identifier history;
- architecture-only test admission and promotion;
- generic vocabulary governance;
- package and bootstrap proof.

The kernel does not own:

- trading, market-data, calendar, risk, capital, execution, portfolio or replay behaviour;
- a pre-selected runtime-module catalogue;
- a pre-selected architecture-surface catalogue;
- DMPV3 schema or processing behaviour;
- state or transaction implementation;
- proof of any future domain semantics.

## Normative propositions

- **AK-TAX-001 — Category separation.** Runtime modules (`M`), protocols (`P`), governance planes (`G`), application shells (`A`), technical kernels (`K`) and architecture surfaces (`S`) are distinct object categories. Registration in one category cannot create authority in another.
- **AK-REG-001 — Declarative registry authority.** Each object category is governed by one schema-valid YAML registry. Registry rows describe admitted identity and status only; they are not service locators and do not prove implementation.
- **AK-REG-002 — Truthful initial state.** The runtime module and architecture surface registries are empty. `P01`, `G01`, `G02`, `A00` and `K01` are the only initial non-module identities and carry non-active statuses.
- **AK-ID-001 — Unbounded permanent identifiers.** Object identifiers use a category prefix and a numeric suffix padded to at least two digits. Allocation continues beyond `99`; retired identifiers are never reused.
- **AK-DEP-001 — Declared dependencies.** Every cross-owner runtime dependency must be declared before use. Active runtime module dependencies must be acyclic.
- **AK-DEP-002 — Category direction.** Runtime code must not depend on governance planes or surfaces. Protocols and kernels must not depend on application shells or runtime modules. Application shells compose but do not own domain decisions.
- **AK-SEAM-001 — Public seam only.** Cross-owner imports must enter through the target owner’s declared public seam. Python naming conventions are documentation only; repository-owned static validation provides enforcement.
- **AK-COMP-001 — Composition eligibility.** Only objects with status `active` and a declared implementation package/public seam may enter runtime composition. `placeholder`, `bootstrap`, `framework`, `deprecated` and `retired` rows are non-composable.
- **AK-LIFE-001 — Controlled lifecycle.** Admission, deprecation, replacement, split, merger and retirement preserve object identity and predecessor/successor lineage. Retired identities cannot return as different meaning.
- **AK-EXT-001 — Open-ended extension.** Adding an instance of an existing object category requires declarative registration, category-local files, proof/vocabulary admission and shell composition where applicable. Central identifier enumerations and identifier-specific dispatch are prohibited.
- **AK-PROOF-001 — Exact proof admission.** Every active architecture test has one exact path, tier, lifecycle, normative proposition set, proof block and promotion-set disposition. Folder placement does not admit proof.
- **AK-PROOF-002 — One aggregate gate.** The `architecture_kernel` promotion set is registry-derived and executes every current blocking proof block. A green result proves only the named structural propositions.
- **AK-PKG-001 — Minimal installed package.** The built distribution contains the architecture registry and composition skeleton only; it imports outside the repository without path injection.
- **AK-PKG-002 — Legacy exclusion.** Former runtime packages, behavioural tests, entry points and production dependencies are absent from the active distribution and proof population.

## Initial registry state

```yaml
modules: []
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

No row above is evidence of a completed implementation.

## Validation boundary

Schema, import-graph, public-seam, proof-admission, packaging and test results establish only the propositions they exercise. They cannot establish a future module’s semantic responsibility, adequacy, business correctness or operational fitness.
