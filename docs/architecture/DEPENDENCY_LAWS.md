# Dependency Laws

## Normative propositions

- **AK-DEP-001 — Declared runtime dependencies.** Every cross-owner Python/runtime dependency is declared before use and must enter through the target's lawful public boundary. Active `M`-to-`M` dependencies are acyclic.
- **AK-DEP-002 — Category direction.** Runtime dependency direction follows architectural category law; runtime code must not acquire governance/surface dependencies and shared carriers/mechanisms must not invert ownership toward their consumers.

## Runtime dependency direction

| Source | May depend on | Must not depend on |
|---|---|---|
| Application shell (`A`) | declared public boundaries of admitted `M`, `P`, `K`; adapters and configuration | private owner implementation, `G`, `S` |
| Runtime module (`M`) | own internals; declared public boundaries of permitted `M`; admitted `P`; admitted `K` abstractions | `A`, `G`, `S`, undeclared owners, private owner internals |
| Protocol (`P`) | standard library, typing and protocol-local mechanisms | `A`, `M`, `G`, `S`, domain orchestration |
| Kernel (`K`) | domain-neutral technical dependencies | `A`, `M`, `G`, `S`, module policy |
| Governance plane (`G`) | repository artefacts through governance tooling | runtime import participation |
| Surface (`S`) | documentation and registry/proof metadata | runtime import participation |

Machine-readable category rules own the exact currently admitted registered-category edges. Ordinary library/tool dependencies that are not registered architecture owners remain governed by package/toolchain authority.

## Dependency declaration

Every Python-visible runtime owner declares, as applicable:

- package root;
- public seam;
- permitted architecture-owner identifiers;
- narrowly justified public-seam exceptions where a normal seam cannot express the required boundary.

An observed cross-owner import is lawful only when category direction, owner declaration and public-seam law all permit it.

## Dependency planes

Do not collapse different dependency questions into one graph:

1. **runtime/contracts plane** — Python/runtime owner dependencies governed by the rules above;
2. **state/transaction participation plane** — use of a technical persistence/transaction mechanism without transfer of semantic ownership;
3. **governance/promotion plane** — proof and promotion prerequisites that must not become production imports;
4. **build/test plane** — development and proof dependencies used to build or test the repository.

A relation in one plane does not automatically create an edge in another.

## Acyclicity

The directed graph formed by admitted `M` runtime dependencies must be acyclic. Acyclicity does not make a category-forbidden or private-seam dependency lawful.

## Framework packages

Repository architecture/governance framework packages are not domain owners merely because runtime analysis tools import or inspect them. The application composition package is an `A` concern and may coordinate admitted owners without acquiring their semantic decisions.
