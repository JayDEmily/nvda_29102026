# AKR-7.2 static architecture enforcement and structural-truth evidence

## Scope

AKR-7.2 traces the current static architecture enforcement path using the fresh environment reconstructed in AKR-7.1, then reconciles validator output with the active normative law, registries, schemas and executable implementation.

This leaf does not execute the complete admitted architecture/bootstrap proof or promotion set; those remain AKR-7.3. It does not implement the external rehearsal brief or design the future brief-to-code continuation.

Start state:

```text
branch: work/akr-7-final-pristine-kernel-proof
HEAD: 755a3f50561a3256a64d3d7e878d181d03d572a8
fresh interpreter: /mnt/data/nvda_akr7_env_7_1/bin/python
Python: 3.13.5
```

## Governing material read

Before execution, the current `GUARDRAILS.md`, root `AGENTS.md` and complete accepted `EXEC_PLAN.md` were read. No nested `AGENTS.md` applies below the root in the files changed by this leaf.

The steady-state architecture law read for this trace was:

```text
docs/architecture/ARCHITECTURE_KERNEL.md
docs/architecture/ARCHITECTURAL_OBJECT_TAXONOMY.md
docs/architecture/OWNERSHIP_AND_COMPONENT_LAW.md
docs/architecture/DEPENDENCY_LAWS.md
docs/architecture/PUBLIC_SEAM_LAW.md
docs/architecture/EXTENSION_AND_RETIREMENT_RULES.md
docs/architecture/IMPLEMENTATION_AUTHORITY_INGRESS.md
docs/architecture/TEST_AND_PROMOTION_KERNEL.md
```

The current architecture registries, dependency rules, implementation-allocation ledger, category schemas, dependency schema, implementation-allocation schema, implementation-authority schema, proof registries/schemas and executable architecture source/tool wrappers were also read before interpreting the command results.

## Required static commands

Using only the fresh AKR-7.1 interpreter:

```text
make validate PYTHON=/mnt/data/nvda_akr7_env_7_1/bin/python
```

observed:

```text
architecture objects: 4
active runtime modules: 0
implementation allocations: 0
admitted test families: 11
promotion sets: 1
dependency/public-seam violations: 0
PASS: structural architecture validation
```

```text
/mnt/data/nvda_akr7_env_7_1/bin/python tools/check_dependencies.py
```

observed:

```text
PASS: dependency direction and cycle validation
```

```text
/mnt/data/nvda_akr7_env_7_1/bin/python tools/check_public_seams.py
```

observed:

```text
PASS: public-seam validation
```

```text
make typecheck PYTHON=/mnt/data/nvda_akr7_env_7_1/bin/python
```

observed:

```text
Success: no issues found in 13 source files
```

No AKR-7.3 pytest or promotion execution was run in this leaf.

## Current structural truth

Loading the committed registries through `ArchitectureRegistry.from_repository` established these current objects:

```text
P01 | protocol           | placeholder | no package/public seam
G01 | governance plane   | framework   | no runtime package/public seam
A00 | application shell  | bootstrap   | nvda_desk.composition / nvda_desk.composition
K01 | technical kernel   | placeholder | no package/public seam
```

Current additional state:

```text
modules: []
surfaces: []
retired_ids across all category registries: []
active runtime modules: []
implementation_allocations: []
declared_owner_edges: []
public_seam_exceptions: []
```

Only `A00` is currently a registered package owner. It is `bootstrap`, not `active`. Therefore the current zero dependency/public-seam violation result establishes consistency of the present empty-runtime state; by itself it does not exercise every future cross-owner rejection case.

## Enforcement trace and proof boundaries

### Schema and registry state

`ArchitectureRegistry.from_repository` validates each category registry against its category schema, enforces category placement, global current-ID uniqueness, current/retired non-overlap, package/public-seam pairing, seam containment, declared-dependency referential integrity and current lifecycle predecessor/successor integrity.

For executable categories `A`, `M` and `K`, an `active` object must carry package and public-seam metadata. The module schema additionally requires an active `M` to declare its semantic responsibility, inputs, outputs, exclusions, state/time/side-effect ownership, component forms and writer/reader/persistence/replay fields.

The aggregate validator adds a physical-source check for every active Python-visible registered object: its registered package and public-seam dotted paths must exist beneath `src/`.

A direct scratch invocation through these production loaders/checks established the boundary:

```text
active M with only id/name/status/description:
REJECTED — active projection fields required by module schema

active M with complete projection + physical package/public seam:
ACCEPTED by registry/readiness checks

same active M after physical package/public seam was removed:
REJECTED — registered package and public seam do not exist
```

These probes used an external temporary repository copy and did not mutate committed production state.

### Dependency plane and public seams

`analyse_repository` validates `dependency_rules.yaml`, loads the current architecture registry and walks every Python file beneath `src/` using the AST. It maps imports to the most-specific registered package owner and checks:

```text
UNDECLARED_EDGE
FORBIDDEN_DIRECTION
PRIVATE_SEAM
DYNAMIC_IMPORT
MODULE_CYCLE
EDGE_NOT_IN_OWNER_REGISTRY
EDGE_TO_RETIRED
```

The analyser handles ordinary `import` and `ImportFrom` forms and the admitted direct/aliased dynamic-import forms implemented in the current code. Framework packages declared in `dependency_rules.yaml` are excluded from owner-edge treatment.

`tools/check_dependencies.py` fails on any violation returned by that analyser. `tools/check_public_seams.py` intentionally filters the same analyser output to `PRIVATE_SEAM` only; undeclared-edge, category-direction, dynamic-import and cycle failures belong to the broader dependency validator/aggregate path.

The current positive result is therefore a statement about the current source/registry state. Full blocking negative proof remains AKR-7.3.

### Typed public seams

`pyproject.toml` pins `mypy==1.20.1`; `[tool.mypy]` sets Python 3.13 and `files = ["src"]`. The repository-native `make typecheck` runs `python -m mypy src`.

The observed success establishes that the 13 current source files are statically type-consistent under that checker/configuration. The current registry contains no active runtime `M` public seam, so this success does not by itself prove rejection of every future incompatible seam call. The admitted blocking negative proof for the typed-seam proposition remains part of AKR-7.3 and was not executed here.

### Candidate resolution versus durable allocation

`IMPLEMENTATION_AUTHORITY_INGRESS.md` and `allocation.py` agree that create-candidate resolution is non-durable. `consumed_identifiers` uses the union of current registered identities, current retired identities and durable post-reset implementation allocations. `resolve_candidate_identifiers` adds earlier candidates only to an in-memory set for the current request and does not write registry or allocation state.

Against current committed state, direct resolution produced:

```text
categories: M, M, A
candidates: M00, M01, A01
```

The SHA-256 of `config/architecture/implementation_allocations.yaml` was identical before and after resolution:

```text
79f68bb3e318d2ff7ce664d778e0fc1c505e8fe0bd50bbe20804a0bda7ba4676
```

The durable allocation loader validates `config/architecture/implementation_allocations.yaml` against `schemas/implementation_allocation.schema.json`, materialises only `object_id`, `name` and `implemented_on`, rejects duplicate `object_id` values and parses each architecture identifier. The committed ledger is empty.

## `implemented_on` calendar-validity observation

The known AKR-7.2 observation was reproduced through the production allocation loader using an external temporary root carrying the committed allocation schema.

With:

```text
implemented_on: "2026-02-31"
```

`load_implementation_allocations` accepted the record and returned the same string. With:

```text
implemented_on: "2026-2-31"
```

the loader rejected the record because it did not match the schema regex:

```text
^[0-9]{4}-[0-9]{2}-[0-9]{2}$
```

Human inspection explains the result: the schema constrains textual shape only, and `allocation.py` stores `implemented_on` as `str` without calendar parsing.

Current authority was then checked for the stronger proposition. Across the current governing ExecPlan and steady-state architecture law, `implemented_on` is specified as one of the three minimal durable-allocation fields, but no normative proposition states that the value must be a calendar-valid date. The accepted ExecPlan explicitly requires this observation to be deferred when stronger calendar validation is not required by current authority.

Disposition for this leaf:

```text
UNRESOLVED / DEFERRED LIMITATION
```

The current loader admits impossible calendar dates that satisfy the textual shape. No calendar-validity repair is made in AKR-7.2 because that stronger invariant is not established by current authority. This limitation must remain explicit in AKR-7 closeout unless later higher authority changes the requirement.

## Leaf conclusion

AKR-7.2 acceptance is established for the current committed source state: the active structural state and the static enforcement paths required by the leaf were traced from current law/configuration through the executable code as well as run through the fresh AKR-7.1 environment.

No contradiction requiring an AKR-7.2 repair was established. The `implemented_on` shape-only validation behaviour is reproduced and explicitly deferred as an unresolved limitation under the current authority boundary.

AKR-7.3 has not been executed.
