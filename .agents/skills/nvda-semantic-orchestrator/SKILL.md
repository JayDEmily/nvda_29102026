---
name: nvda-semantic-orchestrator
description: Use for bounded NVDA Raw Signal semantic reconstruction under the gated IESRM method: source authority, independent falsification, systems-architect acceptance, normative derivation, adversarial proof, implementation, and semantic validation. Do not use for generic repository work, runtime repair, or forensic-history review.
---

# NVDA semantic orchestrator

Use this skill only for a bounded Raw Signal semantic unit identified by the active ExecPlan. The unit must be a coherent intent cluster, operational scenario, or proposition family that cannot truthfully be separated; do not size semantic work by sentence, row, file, module, or implementation convenience.

## Governing law

The method is gated understanding, not a workflow whose completion creates authority.

Codex and its subagents may investigate, derive, challenge, recommend, write, test, and implement within authorised scope. They do **not** self-approve semantic meaning, architecture trade-offs, semantic contracts, or stakeholder acceptance. For this repository, systems-architect acceptance authority remains with the user unless the user explicitly delegates a bounded decision.

A gate is an epistemic/authority boundary, not a hook, runtime state machine, receipt system, or mandatory document factory. Use the smallest existing artefact that can record the evidence and disposition clearly. Do not create parallel ledgers merely to represent gate state.

## Shared source surface

1. **Bind the authority.** Identify the exact source authority from `authority/AUTHORITY_MANIFEST.md`. Satisfy the manifest's mandatory full-source reading rule before the first Raw Signal semantic judgement. If rendering, formatting, formulas, merged cells, or workbook presentation may matter, inspect the authoritative workbook directly.

2. **Use one canonical source surface.** For repeated semantic workers and reviewers over the same corpus, keep the mandatory authoritative source surface and shared semantic instructions in a deterministic, stable order before role-specific or proposition-specific material. This maximises prompt-cache compatibility where the runtime provides it. Cache reuse is a cost/latency optimisation only: never narrow, omit, reorder, or reinterpret required authority merely to obtain a cache hit, and never make semantic acceptance depend on cache behaviour.

3. **Derive from authority before comparison.** Form the source-backed view before consulting candidate or historical interpretations. Candidate material is comparison evidence only and must not anchor, fill gaps in, or override source authority.

4. **Preserve epistemic and relational meaning.** Keep source fact, inference, proposed norm/design, and `Unknown` distinct. Where material, preserve rationale, chronology, alternatives, identity, provenance, ownership, relationships, temporal semantics, lifecycle/revision state, state transitions, edge conditions, examples/counterexamples, and meaningful absence. Do not preserve wording while flattening the relationships that give it meaning.

## IESRM progression stages and gates

These are IESRM semantic-method stages with explicit authority gates. They do not prescribe Codex runtime controls and are unrelated to the retired Codex Gate-0 machinery.

### Stage 0 — Authority and evidence integrity

Establish source roles, chronology/supersession, conflicts, and `Unknowns` before deriving meaning. Existing repository authority artefacts may satisfy this gate where they are complete for the bounded unit.

**Exit:** every material source has a declared role; no reconstruction, candidate, test, old code, or later artefact is silently treated as original/source authority.

### Stage 1 — Intent landscape

Derive the coherent stakeholder outcome, intended behaviour, rationale, preconditions/triggers, inputs/information state, outputs, invariants/prohibitions, examples/counterexamples, dependencies, quality concerns, alternatives, and unresolved branches without allocating them prematurely to implementation.

For material or ambiguous units, use a fresh semantic worker for source-derived interpretation and a fresh semantic reviewer for independent falsification. The reviewer should form its own first-pass source view before seeing the producer's rationale or desired conclusion where feasible.

**Exit:** the systems architect accepts, rejects, defers, or reopens the intent interpretation. Independent review may reject mechanically clean work; review completion itself is not acceptance.

### Stage 2 — Operational scenario

Express the accepted intent as an end-to-end mission thread: actor/goal, environment, admitted evidence, trigger, ordered meaning/authority transitions, expected outcome, degraded/unavailable paths, prohibited shortcuts, identity/time/lineage obligations, state/atomicity obligations, replay evidence, and success measures.

**Exit:** the systems architect approves the operational scenario. Material intent must be represented by an authorised scenario or remain explicitly unresolved/deferred.

### Stage 3 — Quality-attribute scenarios

Make architecture-significant qualities measurable where material: stimulus, environment, affected artefact, required response, response measure, and trade-offs. Preserve conflicts rather than resolving them implicitly.

**Exit:** the systems architect dispositions/prioritises the material quality-attribute scenarios. Do not select an architecture/design trade-off without reference to those priorities.

### Stage 4 — Alternatives and architecture decision

For each material interpretation/design uncertainty, keep materially distinct alternatives alive until evidence or prioritised quality concerns eliminate them. Record supporting/contradicting evidence, assumptions, consequences, rejection conditions, and revisit triggers.

**Exit:** the systems architect approves the selected ADR/decision or leaves the question open/deferred. Codex may recommend; it may not turn the first plausible option into authority.

### Stage 5 — Semantic contract

Before implementation across an ownership boundary, define the semantic owner, producers/consumers, input/output meanings, raw/derived/configured classification, required/optional law, unavailable/stale/conflicting behaviour, invariants, permitted transformations, prohibited authority, identity layers, time semantics, lineage/replay, versioning, compatibility/retirement, examples/anti-examples, and required acceptance evidence.

**Exit:** the systems architect approves semantic meaning and prohibited authority. A schema-valid carrier is not an approved semantic contract.

### Stage 6 — Acceptance evidence and vertical semantic slice

Only after the governing scenario, material trade-offs/ADR, and semantic contracts are authorised may the bounded implementation slice proceed. Define acceptance evidence before implementation, then keep normative writing, adversarial test authoring, and minimal implementation logically distinct. Tests derive from authorised normative meaning; implementation derives from authorised meaning and proof.

After mechanical validation, use an independent semantic reviewer to compare the implementation with the source-backed authorised meaning, not merely with green tests or normative wording.

**Exit:** the user-visible scenario outcome, public-boundary fidelity, lineage/replay, prohibited-path behaviour, and relevant verification are demonstrated, and the systems architect validates the scenario outcome. Verification and stakeholder/intended-use validation are distinct; one does not substitute for the other.

## Gate operation

- Apply each gate that is material to the bounded unit. A gate may be `Not applicable` only when the accepted scope shows its concern is genuinely absent; record why rather than skipping it implicitly. No later gate cures an unresolved earlier one.
- The main Codex thread reconciles evidence and prepares a recommended gate disposition; it does not grant itself semantic acceptance.
- Record a systems-architect disposition explicitly before crossing a gate that requires it. `Pending`, `Rejected`, or `Deferred` means later dependent semantic work does not become authorised. Present the systems architect with the bounded decision, source-backed evidence, material alternatives, independent challenge, consequences, and remaining `Unknowns`; do not turn gate approval into a request for routine commands or diagnostics.
- A later discovery may reopen an earlier gate. Do not force new evidence to fit an already accepted interpretation or plan.
- Do not manufacture consensus. If source evidence cannot support closure, preserve `Unknown` or an open alternative and escalate the exact decision.
- Do not require every custom agent for every gate. Use bounded independent agents when they materially improve derivation, falsification, proof, or implementation quality.
- Parallelise independent read-heavy work when useful. Keep dependent or write-bearing semantic work serial unless the ExecPlan establishes a safe reason otherwise.
- Update the active ExecPlan with material discoveries, systems-architect dispositions, authorised boundaries, validation, and remaining `Unknowns`. Use Git for coherent implementation checkpoints rather than duplicate evidence ledgers.

## Output standard

For each bounded unit, leave enough exact source location, source-backed meaning, independent challenge, material alternatives, systems-architect disposition, relational/provenance constraints, acceptance boundary, and unresolved uncertainty for the next authorised stage to know what was established and what was not.

This skill is frozen after this repair. Do not modify it unless the user explicitly reopens it.
