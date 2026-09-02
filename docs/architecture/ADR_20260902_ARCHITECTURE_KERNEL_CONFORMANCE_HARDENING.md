# ADR — Architecture Kernel Conformance Hardening Before Capability Admission

- **Date:** 2026-09-02
- **Status:** Partially implemented on the work branch; remaining accepted work is explicitly deferred
- **Branch:** `work/2026-09-02-architecture-kernel-conformance`
- **Baseline:** `6a71d3ff04a2e88f6772ae5847c2805aa45278e3`
- **Historical normative reference:** `f35d81deab7e0f2fbd18f59de6347aac7c538e10`
- **Decision class:** foundation conformance / proof hardening / deferred Python platform intent

## Context

The architecture-kernel reset at `6a71d3f` is a deliberately empty, behaviour-neutral foundation. Its 38 admitted architecture/bootstrap tests pass and the reset is historically valid within its declared scope. The mature normative corpus at `f35d81d` defines a stronger future architecture than the empty kernel has yet had to exercise: semantic module ownership, heterogeneous typed seams, declared dependency direction, state/identity/time ownership, bounded side effects, lifecycle lineage, deliberate DMPV3 packet carriage, and exact proof scope.

A full read of the root operating authority, `PLANS.md`, all normative families routed by the mature control surface, the test-side override, the active test surface, schemas, registries and architecture implementation found no need to redesign that architecture. It did find dormant conformance and extensibility defects that become material when the first real runtime module, protocol or kernel is admitted.

This ADR therefore records a narrow decision:

> **Before capability admission begins, bring the executable architecture kernel and its proof surfaces into conformance with architectural laws that already exist. Do not replace those laws with a simpler generic architecture.**

## Architectural invariants preserved by this decision

1. Runtime modules (`M`), protocols (`P`), governance planes (`G`), application shells (`A`), technical kernels (`K`) and architecture surfaces remain distinct categories.
2. A seam is defined by its authority, contract and ownership semantics, not by one universal transport mechanism.
3. DMPV3 remains the canonical outer envelope only for deliberate packetised inter-module carriage where the architecture admits it. It is **not** made universal for raw ingress, source capture, temporal/calendar processing, repository access or every internal serial step.
4. Native ingress carriers, source/capture contracts, repository/port contracts, temporal projections, prepared/stage-specific carriers and packetised DMPV3 payloads may all be typed seams under different boundary regimes.
5. State and persistence remain governed by authoritative ownership and lawful ports/repositories; this ADR does not introduce process-level sandboxing or microservice isolation.
6. Mechanical proof establishes only the proposition actually exercised. Green tests do not create semantic or architectural authority beyond their scope.
7. No business capability, trading behaviour, DMPV3 runtime schema, state/transaction runtime mechanism or UUIDv7 usage location is authorised by this ADR.

## Decision 1 — Repair the real dependency-edge representation path

### Finding

`schemas/dependency_rules.schema.json` admits declared owner edges as objects of the form:

```yaml
declared_owner_edges:
  - source: M01
    target: M02
```

The dependency analyser currently constructs declared edges using the equivalent of:

```python
declared_edges = {tuple(edge) for edge in rules.get("declared_owner_edges", ())}
```

For a mapping, `tuple(edge)` produces the keys:

```python
("source", "target")
```

rather than the owner values:

```python
("M01", "M02")
```

### Reproduced probe

A schema-valid non-empty edge was accepted by schema validation and then failed in the analyser with:

```text
KeyError: 'unregistered architecture object: source'
```

The existing dependency-direction tests use in-memory list fixtures such as:

```python
[["M01", "M02"]]
```

which are not the representation admitted by the committed schema. The current green test therefore proves analyser behaviour for its fixture, not the real schema -> registry/rules -> analyser path.

### Required outcome

Use one canonical edge representation across schema, loading, validation, analysis and proof. Add an end-to-end regression test that begins with the real admitted configuration shape and proves at least a lawful `M01 -> M02 -> M03` graph plus rejection of undeclared/reversed/cyclic edges.

## Decision 2 — Make dependency schemas express the architecture's actual category law

### Finding

The architecture law permits runtime modules to depend on admitted `M`, `P` and `K` owners where the declared dependency is lawful. The current `module.schema.json` restricts `permitted_dependencies` to `M` identifiers only.

### Reproduced probe

A module declaring:

```yaml
permitted_dependencies:
  - P01
  - K01
```

was rejected by schema validation because `P01` and `K01` do not match the current `^M...$` restriction.

### Required outcome

The schema must express the category relationships already authorised by `ARCHITECTURE_KERNEL_RESET_BRIEF.md` and `DEPENDENCY_LAWS.md`, without collapsing `M`, `P` and `K` into one object type.

## Decision 3 — Make future `P` and `K` activation representable without category conflation

### Finding

The generic registry considers an active executable object to require a package and public seam. That is appropriate for Python-visible enforcement. However, the current `kernel.schema.json` does not permit `package` or `public_seam` fields, while registry integrity requires them for an active `K`.

### Reproduced probe

An active `K01` without package/public seam:

```text
schema: PASS
registry: FAIL — active executable object K01 lacks package/public_seam
```

Adding those fields:

```text
schema: FAIL — unexpected property 'package'
```

The current representation therefore has no valid state in which an executable technical kernel can both satisfy its schema and satisfy registry integrity.

A related issue exists for protocols: the architecture permits modules to depend on admitted protocol contracts, but the protocol schema currently has no Python package/public-seam representation for a future executable protocol owner.

### Required outcome

Define activation semantics for `P` and `K` that preserve their distinct categories while giving the dependency/public-seam checker enough information to enforce any Python-visible ownership boundary. Do not solve this by recategorising protocols or kernels as runtime modules.

## Decision 4 — Enforce active-module semantic obligations that the schema already declares

### Finding

`module.schema.json` correctly states that an active module requires materially important ownership/contract fields including semantic responsibility, inputs, outputs, permitted dependencies, package, public seam, exclusions, state ownership, time ownership and side effects. It expresses those conditional requirements using JSON Schema composition/condition keywords.

The repository-owned schema validator intentionally supports a subset of JSON Schema and currently does not execute the relevant `allOf` / `if` / `then` semantics.

### Reproduced probe

The following intentionally incomplete active module was accepted by the schema layer:

```yaml
modules:
  - id: M01
    name: x
    status: active
    description: x
```

Observed result:

```text
ACTIVE_M_MISSING_OBLIGATIONS_SCHEMA: PASS
```

Later registry checks catch some missing structural fields, but they do not establish all of the semantic ownership declarations the module schema says are mandatory.

### Required outcome

The repository-owned validation path must actually enforce the active-object obligations expressed by the admitted schemas. The repair should prefer the smallest coherent change to the existing validator/schema design rather than adding a dependency merely for convenience.

## Decision 5 — Complete static enforcement of typed Python-visible seams

### Finding

The architecture already requires typed public seams and says the configured static-analysis toolchain enforces them. The current development toolchain contains `pytest` and Ruff; Ruff is not a static type checker.

### Reproduced probe

Code with explicit incompatible annotations such as:

```python
def takes_int(x: int) -> int:
    return x

value: int = "not-an-int"
result = takes_int("also-not-an-int")
```

passes the currently configured Ruff checks.

### Decision

Add a **pinned development-only static type checker** and make its admitted checks part of the promotion surface for Python-visible seams. Tool selection must be justified against the repository's hermetic/offline model and must not introduce unrelated runtime dependencies or broaden the stack for convenience.

This decision does **not** imply that every architectural seam is DMPV3 or that static typing alone proves semantic correctness. It supplies one mechanical control for the Python-visible contract layer appropriate to each seam regime.

## Decision 6 — Close ordinary dynamic-import bypasses

### Finding

The architecture prohibits dynamic imports that evade registry/public-seam validation, including equivalent dynamic import calls. The current checker detects direct spellings such as `__import__(...)` and `importlib.import_module(...)`, but not ordinary aliasing.

### Reproduced probe

```python
from importlib import import_module as load

load("nvda_desk.m02.api")
```

Observed result:

```text
violations=[]
```

### Required outcome

The checker must reject materially equivalent dynamic-import forms that would bypass owner/dependency/public-seam validation. Regression proof must include aliases and other ordinary forms the selected implementation claims to cover. The proposition must not claim exhaustive Python dynamic-execution prevention unless that is actually proved.

## Decision 7 — Narrow Tier-A proof claims to exact exercised propositions and add real-path integration proof

### Finding

The proof framework itself is well governed: tests are admitted, tiers/lifecycle are explicit, proof blocks derive paths from authority, and unadmitted tests fail. Several registered propositions are nevertheless broader than their current assertions.

Examples include:

- dependency tests proving in-memory fixture shapes while the schema-valid edge path is broken;
- lifecycle proof that tests retired-ID non-reuse but does not exercise the full admission/deprecation/replacement/split/merger/predecessor-successor proposition associated with the broader lifecycle claim;
- extension proof that exercises identifier grammar and `M99 -> M100` while broader future extension/admission mechanics remain unproved.

### Required outcome

Each Tier-A proposition must either be narrowed to what its assertions actually prove or be expanded with end-to-end proof that exercises the claimed path. In particular, future module/protocol/kernel admission needs schema -> load -> registry -> dependency/public-seam analysis -> promotion proof using representations that can actually exist in committed configuration.

## Decision 8 — Strengthen architectural lifecycle lineage validation

### Finding

Architecture objects carry predecessor/successor lineage, but current integrity validation accepts arbitrary predecessor strings and does not materially validate lifecycle relationship grammar/integrity.

### Reproduced probe

Equivalent construction:

```python
ArchitectureObject(
    "M01",
    ...,
    predecessors=("NOT_AN_ID",),
)
```

was accepted by registry integrity validation.

### Required outcome

Validate lifecycle relationship identities and structural consistency without requiring all historical predecessors to remain active/current registry objects. Historical identity must remain representable; the repair must not erase legitimate retired/superseded ancestry.

## Decision 9 — Make public-seam exception configuration schema-complete

### Finding

The current dependency-rules schema permits `public_seam_exceptions` members as generic objects, while the analyser assumes specific keys such as source owner, target owner and import path.

### Reproduced probe

The schema-valid configuration:

```yaml
public_seam_exceptions:
  - {}
```

passes schema validation and then raises a key error in the analyser.

### Required outcome

The schema and analyser must agree on one explicit exception contract. Exceptions remain exceptional and must not become a general escape hatch from owner/public-seam law.

## Decision 10 — Retain CPython 3.13.5 now; record CPython 3.14.7 as a future migration target

### Verified external fact

Python 3.14 added standard-library UUID versions 6, 7 and 8 under RFC 9562. The standard-library API includes:

```python
import uuid

identifier = uuid.uuid7()
```

As of 2026-09-02, the stable Python 3.14 maintenance release identified for a future migration is **CPython 3.14.7**.

### Decision

The active project platform remains pinned to exact CPython `3.13.5`. **No Python-version migration is performed by this branch or this implementation tranche.**

CPython `3.14.7` is recorded as a future migration target because Python 3.14 provides standard-library UUIDv7 capability. The timing of that migration is deliberately deferred.

When a future migration is explicitly authorised, it must be atomic across the active environment declaration and proof surface. At minimum, review/update together:

- `pyproject.toml` `requires-python`;
- `.python-version`;
- Ruff target version;
- `uv.lock`;
- the hermetic/offline wheelhouse and its checksums/readme;
- any current README/control text that claims the supported Python boundary;
- CI/bootstrap/install proof that depends on the interpreter version.

Historical evidence that truthfully records Python 3.13.5 must remain historical evidence and must not be rewritten. A future migration is not complete until its hermetic environment reconstructs and the admitted proof passes.

## Decision 11 — Future UUIDv7 capability will use the Python standard library; no UUIDv7 package is added now

### Verified external fact

`uuid.uuid7()` is part of Python 3.14's standard-library `uuid` module. No separate UUIDv7 package is required once the project eventually migrates to Python 3.14 or later.

### Decision

No third-party UUID/UUIDv7 runtime dependency is added now. The current Python 3.13.5 platform therefore gains **no UUIDv7 capability from this ADR or branch**.

If and when the project migrates to the recorded Python 3.14.7 target, UUIDv7 generation is intended to use standard-library `uuid.uuid7()` rather than a third-party UUIDv7 package.

This ADR deliberately does not decide:

- where UUIDv7 will be used;
- which architectural/domain identities should use UUIDv7;
- whether any existing identity scheme should migrate;
- persistence representation;
- ordering assumptions derived from UUIDv7 timestamps;
- lineage semantics;
- packet identity semantics;
- database-indexing strategy.

Any later use of UUIDv7 must be separately admitted by the authority that owns that identity. In particular, DMPV3 packet occurrence identity must not silently become domain/source identity merely because UUIDv7 becomes available.

## Findings explicitly withdrawn or reframed

The following are **not** defects requiring repair under this ADR:

1. **Empty runtime-module registry at the reset HEAD.** This was an explicit reset invariant and remains valid historical proof.
2. **Unimplemented DMPV3 runtime behaviour and K01 state/transaction machinery.** Both were deliberately out of scope and represented as non-active identities/placeholders.
3. **Absence of process/OS sandboxing between modules.** The architecture deliberately uses a modular-monolith ownership/port/repository model rather than microservice/process isolation absent a demonstrated requirement.
4. **Need for a new universal seam map.** The mature normative architecture already defines heterogeneous seam, ownership, dependency and public-contract laws. This tranche must enforce those laws rather than create a competing control model.

## Required regression/activation proof before first real capability admission

The implementation tranche must produce evidence for at least the following representative cases using the real committed configuration path rather than only hand-built analyser fixtures:

```text
schema-valid M01 -> M02 edge                 -> accepted and analysed correctly
undeclared M01 -> M02 import                 -> FAIL
reverse/forbidden dependency                  -> FAIL
M01 -> M02 -> M01 cycle                      -> FAIL
private cross-owner import                    -> FAIL
aliased dynamic import bypass                 -> FAIL
active M missing ownership/contract fields    -> FAIL
lawful M -> P dependency                      -> PASS when P is lawfully admitted
lawful M -> K dependency                      -> PASS when K is lawfully admitted
invalid P/K activation representation         -> FAIL coherently, never schema-pass/analyser-crash
malformed public-seam exception               -> FAIL at validation, not runtime KeyError
invalid lifecycle predecessor identifier      -> FAIL
historical valid predecessor lineage          -> PASS without requiring retired object reactivation
incompatible typed Python seam                -> FAIL static analysis
aggregate architecture-kernel promotion       -> PASS
```

These are regression targets, not a complete test plan. Additional tests are justified only where required to prove an admitted proposition or a newly implemented repair.

## Implementation constraints

- No architecture redesign unless a repair demonstrates that an existing normative law is internally contradictory.
- No universalisation of DMPV3.
- No new runtime dependency for UUIDv7.
- No dependency addition solely because it is an easier implementation path.
- A static type checker may be added as a pinned **development-only** dependency because static typed-seam enforcement is already an architectural requirement; the exact tool must be selected deliberately and incorporated into the hermetic proof surface.
- Preserve full Git history; no rebase/squash/history rewrite.
- Preserve historical reset evidence as historical evidence.
- Do not claim production readiness or semantic correctness from structural proof.

## Consequences

### Positive

- The first real module is admitted onto a foundation whose actual schema/configuration paths have been exercised, rather than onto an empty-kernel proof that never needed those paths.
- Existing modularity, ownership and DMPV3 semantics are preserved rather than simplified into a generic transport model.
- Typed-seam enforcement becomes an actual toolchain property where Python static analysis can establish it.
- The future Python 3.14.7 migration target and its standard-library UUIDv7 rationale are recorded without disturbing the current proven Python 3.13.5 platform.
- Future defects in these foundation paths become regressions against explicit failing probes rather than rediscovered architectural ambiguities.

### Cost / risk

- A future CPython 3.14.7 migration will require a coherent hermetic wheelhouse/lock rebuild; that cost is deferred with the migration and is not incurred by this branch.
- Adding a static type checker expands the development/tooling supply surface and therefore requires pinned, offline-reproducible admission.
- Strengthening proof may expose further dormant activation bugs. Such bugs are repair evidence, not authority to redesign unrelated architecture.

## Implementation disposition at close of this work session

The conformance work completed on this branch implements Decisions 1, 2, 3, 4, 6, 7, 8 and 9.

Decision 5 (static typed-seam enforcement) remains accepted but is not implemented by this work session. Decisions 10 and 11 are now explicitly **deferred future platform intentions**, not current implementation requirements: the repository remains on exact Python 3.13.5, and no UUIDv7 capability or third-party UUID package is introduced.

The completed conformance repairs remain subject to these closeout conditions:

1. their representative regression/activation proof passes through real committed representations;
2. the aggregate architecture-kernel promotion gate passes;
3. the worktree is clean and the implementation commits preserve full history; and
4. no claim exceeds the exact proposition established by its evidence.

Any future Python 3.14.7 migration or UUIDv7 adoption requires a new explicitly authorised implementation step and its own atomic environment/proof update.

The reset at `6a71d3f` remains historically PASS within its original empty-kernel scope.
