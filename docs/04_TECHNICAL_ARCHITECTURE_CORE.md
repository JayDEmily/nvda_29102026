# 04_TECHNICAL_ARCHITECTURE_CORE

All repo paths in the numbered control stack are repo-root-relative.


## Architectural shape

The architecture has these top-level technical parts:

- a real-data admission and runtime-preparation path
- a financial-calendar reference and projection path
- a six-stage serial runtime path
- a separate parallel risk runtime path
- a downstream pre-deployment and capital-deployment path
- a downstream opening, execution, state-feedback, inventory, and close path
- a review and explanation path

That grouped structure is binding at the technical-lane level unless explicitly and lawfully revised.

The detailed native architecture-surface order, target package placement, component form, seams, ownership, persistence, test-family mapping, reservations, module allocation, and traceability are owned by `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md` inside its bounded architecture scope.

These grouped technical lanes must be interpreted as summaries over the detailed `docs/11` architecture surfaces, not as a competing surface count.

## Normalised packet-carriage layer

The technical architecture uses DMPV3 as the normalised outer envelope for live inter-module packet carriage.

That common outer envelope applies to packetised outputs including:

- serial stage outputs
- the parallel risk runtime path output
- financial-calendar packet emitters
- imported-module packet emitters
- review carriage where runtime outputs are packetised

The architecture uses one common outer envelope and module-specific payload contracts.

A common outer envelope does not merge bounded technical responsibilities.

Packet normalisation must not collapse:

- the real-data admission and runtime-preparation path
- the financial-calendar reference and projection path
- the serial runtime path
- the parallel risk runtime path
- the downstream pre-deployment and capital-deployment path
- the downstream opening, execution, inventory, and close path
- the review and explanation path

A module does not keep an alternative outer packet grammar once DMPV3 is the live packet-carriage law.

## Cross-cutting technical layers

State-conditioned modifiers and coefficient authority act across the governed runtime sequence.

Those layers do not replace bounded runtime-path responsibilities.

## Real-data admission and runtime-preparation path

The real-data admission and runtime-preparation path admits source truth and produces prepared runtime truth.

This path is technically separate from the serial runtime path.

This path does not form the candidate.

## Financial-calendar reference and projection path

The financial-calendar reference and projection path preserves financial-calendar truth and projected calendar context.

This path is technically separate from the serial runtime path.

This path does not form the candidate.

## Serial runtime path

The serial runtime path is the main technical path through the system.

It is implemented as an ordered six-stage structure:

1. temporal context
2. market regime context
3. options and flow context
4. posture and risk permission
5. playbook eligibility
6. expression and execution

This path produces the candidate.

The technical architecture preserves that ordered structure.

Later refinement inside a stage is lawful, but it does not erase, merge, renumber, or bypass a stage boundary without explicit lawful revision.

## Parallel risk runtime path

The parallel risk runtime path is structurally separate from the serial runtime path.

Its technical role is to evaluate the present environment in parallel while the serial runtime path forms the candidate.

It does not form the candidate.

The architecture preserves that separation in runtime handling.

The parallel risk runtime path remains identifiable as its own path in implementation and review.

## Downstream pre-deployment and capital-deployment path

The downstream pre-deployment gate sits downstream of candidate formation.

Its technical role is to block incomplete, disallowed, or unusable candidate material before capital deployment authority acts.

Capital deployment authority sits downstream of the downstream pre-deployment gate.

Its technical role is to consume the formed candidate together with the required earlier-step outputs and issue a bounded fresh-capital decision.

This path does not replace the serial runtime path.

This path does not replace the parallel risk runtime path.

The architecture preserves its downstream placement and bounded technical role.

## Downstream opening, execution, state-feedback, inventory, and close path

The downstream opening architecture preserves opening-state truth after capital deployment authority acts.

The execution bridge, execution receipt, and downstream state-feedback surfaces preserve post-deployment execution truth.

The live-inventory, position-state, and close architecture preserve open-position and close-path truth after opening state exists.

These downstream parts remain structurally separate from the serial runtime path, the parallel risk runtime path, and capital deployment authority.

## Required technical separation

The architecture keeps these things separate in implementation:

- real-data admission and runtime preparation
- financial-calendar reference and projection
- candidate formation
- environmental risk evaluation
- downstream pre-deployment blocking
- fresh-capital deployment decision
- downstream opening, execution, inventory, and close handling
- review of those results

The architecture is wrong if those technical parts collapse into one blended runtime path.

## Inspectable runtime handling

The architecture keeps the main technical parts inspectable.

A reviewer must be able to determine:

- what the real-data admission and runtime-preparation path produced
- what the financial-calendar reference and projection path produced
- what the serial runtime path produced
- what the parallel risk runtime path produced
- what the downstream pre-deployment gate blocked or allowed
- what capital deployment authority decided
- what downstream opening, execution, inventory, and close surfaces preserved

The architecture is not acceptable if those results are reconstructed only by guesswork.

## Bounded technical responsibilities

Each major technical part has a bounded responsibility.

A part does not silently absorb the job of a neighbouring part because it is convenient in code.

The architecture preserves bounded technical responsibilities between:

- the real-data admission and runtime-preparation path
- the financial-calendar reference and projection path
- the serial runtime path
- the parallel risk runtime path
- the downstream pre-deployment and capital-deployment path
- the downstream opening, execution, inventory, and close path
- the review and explanation path

## Native Architecture Blueprint boundary

Within native code-structure architecture scope, this document must be read with `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md`.

`docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md` owns target package placement, component form, seams, ownership, persistence, test-family mapping, reservations, module allocation, and traceability for native code-structure architecture.

It does not override the authority hierarchy defined by `docs/01_NORMATIVE_CORE.md`.

All durable terms used by live control documents must be governed by `docs/vocabulary/vocabulary_registry.md` or lawfully admitted by the vocabulary process before they become canonical language.
