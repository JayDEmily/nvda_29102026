# 02_BRIEFING_AND_EXECUTION_OPERATING_MODEL_CORE

All repo paths in the numbered control stack are repo-root-relative.


## Operating model

The repo emulates the cognition flow of a Tier 1 NVDA desk trader at Goldman Sachs.

The system does not operate as an abstract prediction engine.

The system operates as disciplined desk behaviour under institutional constraints.

The binding design lens is human desk judgement under institutional discipline.

The operating model behaves as one ordered runtime sequence:

1. real-data admission and runtime preparation
2. financial-calendar reference and projection
3. temporal context
4. market regime context
5. options and flow context
6. posture and risk permission
7. playbook eligibility
8. expression and execution
9. downstream pre-deployment gate
10. capital state, bounded sizing, and capital deployment authority
11. downstream opening architecture
12. execution bridge, execution receipt, and downstream state feedback
13. live inventory, position state, and close architecture
14. review and explanation surfaces

No governed step is optional.

No governed step is skipped, merged, reordered, or reclassified without explicit normative change.

## Serial desk-cognition behaviour

The main desk-cognition spine is serial and ordered.

Its six stages are:

1. temporal context
2. market regime context
3. options and flow context
4. posture and risk permission
5. playbook eligibility
6. expression and execution

The serial desk-cognition spine forms the candidate.

Each stage has a bounded behavioural job.

A later stage does not take over the job of an earlier stage.

An earlier stage does not pre-empt the bounded job of a later stage.

## Independent parallel risk behaviour

The independent parallel risk lane runs alongside the governed runtime sequence while the serial desk-cognition spine forms the candidate.

The independent parallel risk lane produces an independent reading of the present environment.

That reading does not become candidate formation.

That reading remains distinct from the downstream pre-deployment gate and capital deployment authority.

## Downstream pre-deployment behaviour

The downstream pre-deployment gate blocks incomplete, disallowed, or unusable candidate material before capital deployment authority acts.

The downstream pre-deployment gate does not form the candidate.

The downstream pre-deployment gate does not decide fresh-capital deployment.

## Capital deployment behaviour

Capital deployment authority operates downstream of candidate formation and the downstream pre-deployment gate.

Its behavioural role is to decide whether fresh capital is deployed against the formed candidate, and in what bounded way.

It consumes preserved earlier-step truth including capital state and bounded sizing surfaces.

It does not replace serial candidate formation.

It does not replace the independent parallel risk reading.

The operating model preserves a clean behavioural distinction between:

- candidate formation
- environmental risk reading
- downstream pre-deployment blocking
- fresh-capital deployment judgement

## Downstream architecture behaviour

The downstream opening architecture preserves the authorised opening state after capital deployment authority.

The execution bridge, execution receipt, and downstream state-feedback surfaces preserve post-deployment execution truth.

The live-inventory, position-state, and close architecture preserves open-position and close-path truth after opening state exists.

These downstream surfaces do not replace candidate formation, the independent parallel risk reading, or capital deployment authority.

## Human judgement under deterministic implementation

The runtime is deterministic.

The operating model preserves human institutional judgement within that deterministic runtime.

The system preserves bounded judgement about:

- environment
- permission
- caution
- deployment restraint

The operating model is invalid if those behaviours are flattened into opaque mechanical output or replaced by unconstrained improvisation.

## Explanation requirement

Explanation is part of the operating model.

The repo must remain able to state, in plain language:

- what candidate the serial desk-cognition spine formed
- what the independent parallel risk lane concluded about the environment
- what the downstream pre-deployment gate blocked or allowed
- what capital deployment authority decided about fresh capital
- what downstream opening, execution, inventory, and close surfaces preserved

If those answers cannot be stated distinctly, the operating model is not being preserved.

## Native Architecture Blueprint boundary

Within native code-structure architecture scope, this document must be read with `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md`.

`docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md` owns target package placement, component form, seams, ownership, persistence, test-family mapping, reservations, module allocation, and traceability for native code-structure architecture.

It does not override the authority hierarchy defined by `docs/01_NORMATIVE_CORE.md`.

All durable terms used by live control documents must be governed by `docs/vocabulary/vocabulary_registry.md` or lawfully admitted by the vocabulary process before they become canonical language.
