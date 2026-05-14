# 03_DOMAIN_MODEL_CORE

All repo paths in the numbered control stack are repo-root-relative.


## Main domain shape

The repo models a bounded institutional trading cognition system for NVDA.

The system has these main domain parts:

- real-data admission and runtime preparation
- financial-calendar reference and projection
- a six-stage serial desk-cognition spine
- Parallel Risk Lane
- a downstream pre-deployment gate
- capital state, bounded sizing, and capital deployment authority
- downstream opening architecture
- execution bridge, execution receipt, and downstream state feedback
- live inventory, position state, and close architecture
- review and explanation surfaces

That structure is binding unless explicitly and lawfully revised.

## Real-data admission and runtime preparation

Real-data admission and runtime preparation are a separate part of the system.

Their job is to admit source truth and prepare runtime-ready truth before serial desk-cognition begins.

Their job is not candidate formation.

Their job is not capital deployment.

## Financial-calendar reference and projection

Financial-calendar reference and projection are a separate part of the system.

Their job is to preserve calendar truth and projected calendar context for later governed steps.

Their job is not candidate formation.

Their job is not capital deployment.

## Serial desk-cognition spine

The serial desk-cognition spine is the path that moves from prepared runtime truth to candidate formation.

It has six stages:

1. temporal context
2. market regime context
3. options and flow context
4. posture and risk permission
5. playbook eligibility
6. expression and execution

These six stages are real domain boundaries.

They are not labels of convenience.

Later refinement inside a stage is lawful, but it does not erase a stage boundary without explicit lawful revision.

## Parallel Risk Lane

The Parallel Risk Lane is a separate part of the system.

Its job is to assess the present environment while the serial desk-cognition spine forms the candidate.

Its job is not candidate formation.

It remains separate from the serial desk-cognition spine even when both are working from the same market state.

## Downstream pre-deployment gate

The downstream pre-deployment gate is a separate part of the system.

Its job is to block incomplete, disallowed, or unusable candidate material before capital deployment authority acts.

Its job is not candidate formation.

Its job is not the fresh-capital decision itself.

## Capital architecture

Capital state, bounded sizing, and capital deployment authority are a separate downstream part of the system.

Their job is to decide whether fresh capital is deployed against an already formed candidate, and in what bounded way.

Their job is not candidate formation.

Their job is not general portfolio management.

Their job is not close-position logic.

They remain separate from both the serial desk-cognition spine and Parallel Risk Lane.

## Downstream architecture

The downstream opening architecture is a separate part of the system.

Its job is to preserve opening-state truth after capital deployment authority acts.

The execution bridge, execution receipt, and downstream state-feedback surfaces are a separate part of the system.

Their job is to preserve execution truth after opening state exists.

The live-inventory, position-state, and close architecture are a separate part of the system.

Their job is to preserve open-position and close-path truth after opening state exists.

These downstream parts do not replace candidate formation, the independent parallel risk reading, or capital deployment authority.

## What must stay separate

The domain model requires the system to keep these things separate:

- admitting and preparing runtime truth
- preserving financial-calendar truth
- forming the candidate
- assessing the environment in parallel
- blocking unusable candidate material before capital deployment
- deciding whether fresh capital is deployed
- preserving downstream opening, execution, inventory, and close truth
- explaining those separate results clearly

The domain model is wrong if those things collapse into one blended concept.

## Review and explanation surfaces

The system must be able to explain, in plain language:

- what runtime truth was admitted and prepared
- what financial-calendar truth was preserved
- what candidate was formed
- what the environmental assessment was
- what the downstream pre-deployment gate blocked or allowed
- what the fresh-capital decision was
- what downstream opening, execution, inventory, and close surfaces preserved

If the system cannot state those answers separately, the domain model is not being preserved.

## Vocabulary discipline

Domain terms remain stable and deliberate.

A new durable term does not appear where an established term already exists for the same meaning.

Near-synonyms that blur domain boundaries are not permitted.

## Native Architecture Blueprint boundary

Within native code-structure architecture scope, this document must be read with `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md`.

`docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md` owns target package placement, component form, seams, ownership, persistence, test-family mapping, reservations, module allocation, and traceability for native code-structure architecture.

It does not override the authority hierarchy defined by `docs/01_NORMATIVE_CORE.md`.

All durable terms used by live control documents must be governed by `docs/vocabulary/vocabulary_registry.md` or lawfully admitted by the vocabulary process before they become canonical language.
