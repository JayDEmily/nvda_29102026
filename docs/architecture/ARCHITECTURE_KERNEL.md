# Architecture Kernel

## Status

Steady-state normative authority for the behaviour-neutral NVDA architecture kernel.

The 2026-08-04 reset brief and the 2026-09-02 conformance ADR are historical evidence explaining how this kernel was reached. They are not the steady-state owner of the laws below.

## Purpose

This repository provides the structural laws and proof machinery required to admit future capabilities without pre-selecting or implying NVIDIA business behaviour.

The kernel owns architecture grammar. Accepted implementation authority owns future domain meaning.

The kernel does not own trading, market-data, calendar, risk, capital, execution, portfolio or replay behaviour; it does not own a fixed runtime-module catalogue or a fixed architecture-surface catalogue; and it does not treat registration, code, tests or historical lineage as proof of semantic admission.

## Authority map

Each detailed architectural rule has one semantic owner:

| Concern | Owning authority |
|---|---|
| category meanings, identifier grammar and lifecycle statuses | `ARCHITECTURAL_OBJECT_TAXONOMY.md` |
| semantic ownership, component forms, writer/reader and persistence-role separation | `OWNERSHIP_AND_COMPONENT_LAW.md` |
| runtime dependency direction and dependency-plane separation | `DEPENDENCY_LAWS.md` |
| Python-visible public boundaries and seam contracts | `PUBLIC_SEAM_LAW.md` |
| proof admission, proof scope and promotion | `TEST_AND_PROMOTION_KERNEL.md` |
| admission, replacement, split, merger, deprecation and retirement | `EXTENSION_AND_RETIREMENT_RULES.md` |
| external corroboration and historical challenge lineage | `EXTERNAL_LINEAGE_INDEX.md` |

This document owns only the cross-cutting registry, composition and packaging propositions below. It does not restate the detailed laws owned by those documents.

## Cross-cutting propositions

- **AK-REG-001 — Declarative registry authority.** Each architectural-object category is governed by one schema-valid registry. Registry rows declare current architectural identity and status; they are not service locators and do not create semantic authority or implementation truth.
- **AK-REG-002 — Registry-state truth.** The current registries must describe the current admitted architecture truthfully. Empty bootstrap state is historical starting evidence, not a permanent steady-state invariant. Future admitted objects are added through the category-appropriate lifecycle without changing this law.
- **AK-COMP-001 — Composition eligibility.** Runtime composition may select only objects whose category, status, implementation form and public boundary make them lawfully composable. Registration alone never makes an object composable.
- **AK-PKG-001 — Truthful installed package.** The built distribution contains only source that belongs to the currently admitted kernel and admitted implementation state, and it must import outside the repository without source-tree path injection.
- **AK-PKG-002 — Unadmitted-capability exclusion.** Product/runtime packages, behavioural proof, entry points and production dependencies that lack current admission must not enter the active distribution or blocking proof population merely because they exist in history.

## Current-state location

Current object identities and statuses are read from `config/architecture/*.yaml`; proof state is read from `config/proof/*.yaml`; current vocabulary state is read from `config/vocabulary/`.

No duplicate current-state table in this document overrides those registries.

## Historical challenge law

Historical architecture may challenge a current design decision when it documents a structural problem that can still occur. It does not reactivate former `M00–M15` ownership, the former eighteen-surface catalogue, product behaviour or historical implementation status.

The generic mature-architecture lessons retained by the current authority are expressed in the owning laws above, including:

- surface is not module and module is not package;
- carrier/protocol is not semantic owner;
- shared technical mechanism is not consumer-domain owner;
- semantic owner, authorised writer, reader, coordinator and reviewer are distinct roles;
- runtime dependency, transaction participation, governance/proof dependency and build/test dependency are distinct planes;
- code/test presence and structural status do not establish implementation or semantic truth.

## Validation boundary

Schema, registry, import-graph, public-seam, proof-admission, packaging and test results establish only the propositions they actually exercise. They cannot establish a future object's semantic responsibility, adequacy, business correctness or operational fitness.
