# 06_PROCESS_AND_TRANCHE_LAW_CORE

All repo paths in the numbered control stack are repo-root-relative.


## Scope of this document

This document owns:

- active-pack law
- execution read sequence
- one-gate-at-a-time law
- document-touch law
- state-integrity law
- receipt law
- closeout law

## Execution read sequence

Substantive execution must read in this order:

1. `AGENTS.md`
2. the active bounded pack surface in scope
3. `docs/00_CONTROL_SURFACE_ROUTING_INDEX.md`
4. `docs/01_NORMATIVE_CORE.md`
5. the numbered live authority documents that own the active question, in the order required by the active bounded pack where that order does not contradict higher-priority live law
6. `PLANS.md` when the active bounded pack routes it as the repo-level plan standard
7. the active bounded pack execution-plan surfaces that define the current gate
8. retained evidence only after all live authority above has been read

Conflict precedence is owned by `docs/01_NORMATIVE_CORE.md`.

## Active-pack law

Substantive repo work must run through one active bounded pack.

The active bounded pack must be declared together by:

- repo-root `AGENTS.md`
- `docs/06.1_PROCESS_AND_TRANCHE_LAW_WORKING.md` when it contains admitted local material

For the current programme stage, the active bounded pack is the pack jointly declared by current live route surfaces:

- repo-root `AGENTS.md`
- `docs/06.1_PROCESS_AND_TRANCHE_LAW_WORKING.md` when it contains admitted local material
- `PLANS.md` when that pack routes it as the repo-level plan standard
- the ordered repo-local ExecPlan surfaces that pack routes

No file becomes part of the active bounded pack by implication.

No file becomes mutable merely because it is nearby, relevant, or historically related.

## One-control-front and bounded-assignment law

Only one canonical Project Manager control and integration front is active at a time.

The default execution route opens one bounded objective. An expressly routed parallel workflow may open up to six independent lane assignments under that same control front, provided each lane has only one bounded semantic objective, one named canonical base, an explicit dependency gate, a disjoint write set and declared shared locks.

Parallel lanes do not create parallel canonical states. Worker and tester activity may overlap; Project Manager acceptance, integration, control-state mutation and checkpoint publication remain sequential.

A control cycle is closed only when every integrated assignment, touched live control surface and required receipt agrees on the same state. Held, blocked or unfinished assignments must be recorded explicitly rather than implied closed.

## Document-touch law

Every active bounded pack must classify relevant surfaces as:

- touched
- read-only mandatory reading
- prohibited

A touched surface is editable.

A read-only mandatory-reading surface must be read and obeyed. It must not be edited unless the active bounded pack explicitly moves it into touched scope and states why.

A prohibited surface must neither be edited nor treated as mutable support for convenience changes.

No surface enters touched scope by assumption, adjacency, or convenience.

## State-integrity law

Any test, assertion, or control-surface rule that encodes a temporary or point-in-time state must declare its lifecycle as one of:

- later-state tolerant
- mandatory retire at closeout
- mandatory replace at closeout

A temporary-state surface must not remain in place as if it were permanent law after the state it described has lawfully changed.

## No-retroactive-scope-legalisation law

A file that was not in mutable scope at gate open must not be touched first and legalised later.

If an unlisted file becomes necessary during execution, stop and reopen the bounded pack before touching it.

## Adjacent-governed-surface law

If a gate touches a surface that belongs to a governed block, that governed block must be reconciled before closeout.

A green local slice does not close a gate while another touched governed block remains unreconciled.

## Receipt law

If branch truth changed, update every required receipt surface that records that changed truth.

Required receipt surfaces include:

- the active bounded pack surface when its truth changed
- `config/retained_test_registry.yaml` when test migration status changed
- touched manifest or proof-ownership surfaces when their truth changed
- touched control surfaces whose recorded state changed

A receipt is incorrect if it omits a changed live surface that current live doctrine requires it to record.

## Closeout law

A gate is not closed until all touched live control surfaces and required receipts agree on the same state.

If any touched live control surface or required receipt disagrees, the gate is not closed.

## Live-authority boundary law

The live authority stack is limited to the control documents and active bounded pack surfaces routed by current live doctrine.

Historical support material, retained evidence, and non-authority files do not enter the live authority stack unless a higher-priority live surface explicitly routes them there.

Repo-root `README.md` is not part of the live authority stack.

## Process-closeout rule

Work is not closed if any required process condition remains unmet.

That includes any case where:

- no active bounded pack is routed
- a touched governed surface remains unreconciled
- a required receipt is missing or incorrect
- current repo truth and stated repo truth do not match

A clean narrative does not close a gate.

## Native Architecture Blueprint boundary

Within native code-structure architecture scope, this document must be read with `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md`.

`docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md` owns target package placement, component form, seams, ownership, persistence, test-family mapping, reservations, module allocation, and traceability for native code-structure architecture.

It does not override the authority hierarchy defined by `docs/01_NORMATIVE_CORE.md`.

All durable terms used by live control documents must be governed by `docs/vocabulary/vocabulary_registry.md` or lawfully admitted by the vocabulary process before they become canonical language.
