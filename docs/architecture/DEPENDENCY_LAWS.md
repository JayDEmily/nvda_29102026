# Dependency Laws

## Category direction

| Source | May depend on | Must not depend on |
|---|---|---|
| Application shell (`A`) | declared public seams of active `M`, admitted `P`, active `K`, adapters and configuration | private owner implementation, `G`, `S` |
| Runtime module (`M`) | its own internals, declared public seams of permitted `M`, admitted `P`, active `K` abstractions | `A`, `G`, `S`, undeclared owners, private owner internals |
| Protocol (`P`) | standard library, typing and protocol-local validation | `A`, `M`, `G`, `S`, domain orchestration |
| Kernel (`K`) | domain-neutral technical dependencies | `A`, `M`, `G`, `S`, module policy |
| Governance plane (`G`) | repository artefacts through tools | runtime import participation |
| Surface (`S`) | documentation and registry metadata | runtime import participation |

## Dependency declaration

Every active runtime owner records:

- package root;
- public seam;
- permitted owner identifiers;
- optional accepted technical-port exceptions.

An import is lawful only when both the category direction and the declared owner edge permit it.

## Acyclicity

The directed graph formed by active `M` dependencies must be acyclic. The checker reports the exact cycle path and fails closed.

## Framework package

`nvda_desk.architecture` is repository framework code, not a registered runtime owner. `nvda_desk.composition` is the `A00` bootstrap package. Neither establishes domain capability.
