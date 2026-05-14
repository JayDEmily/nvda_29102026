# 01_NORMATIVE_CORE

All repo paths in the numbered control stack are repo-root-relative.

## Authority hierarchy

When documents conflict, precedence is:

1. this document
2. other `.md` files in `docs/`
3. repository configuration files
4. scripts, tests, and source code
5. ephemeral planning or chat material

No lower-precedence surface overrides, weakens, or silently reinterprets a rule stated here.

Dedicated control documents elaborate this core inside their own ownership boundaries. They do not override it.

## Frozen repo invariants

This repo exists to emulate the cognition flow of a Tier 1 NVDA desk trader at Goldman Sachs, including the human judgement lens behind that desk behaviour.

The runtime is deterministic. It is not an autonomous LLM trader.

Repo truth is governed by documents, contracts, and controlled proof.

The system must remain replayable, auditable, and explainable.

Done is binary. Done means correct, unambiguous, internally consistent, and fully reconciled where required.

A work item that is partially correct, ambiguous, internally inconsistent, or unreconciled where reconciliation is required is not done.

Normative doctrine governs tests and code. Tests and code conform to doctrine.

## Governed runtime sequence

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

A governed step must not be collapsed, merged, skipped, reordered, or reclassified without explicit normative change.

## Serial desk-cognition spine

The serial desk-cognition spine consists of:

1. temporal context
2. market regime context
3. options and flow context
4. posture and risk permission
5. playbook eligibility
6. expression and execution

The serial desk-cognition spine forms the candidate.

The serial desk-cognition spine does not own the independent parallel risk lane.

The serial desk-cognition spine does not own capital deployment authority.

## Parallel risk lane

The independent parallel risk lane runs alongside the governed runtime sequence and remains distinct from the serial desk-cognition spine, the downstream pre-deployment gate, capital deployment authority, and downstream execution and inventory surfaces.

The independent parallel risk lane is not a numbered stage of the serial desk-cognition spine.

The independent parallel risk lane does not form the candidate.

The independent parallel risk lane does not allocate capital.

## Cross-cutting governed layers

State-conditioned modifiers and coefficient authority act across the governed runtime sequence. They do not replace governed runtime steps.

DMPV3 governs live inter-module packet carriage. If a runtime output is packetised, it uses the canonical DMPV3 outer envelope.

## Runtime model boundary

This document owns top-level repo truth, authority hierarchy, frozen repo invariants, the governed runtime sequence, and the top-level serial/parallel/capital/downstream boundaries.

Detailed operating behaviour is owned by `docs/02_BRIEFING_AND_EXECUTION_OPERATING_MODEL_CORE.md`.

Domain contracts and bounded domain meanings are owned by `docs/03_DOMAIN_MODEL_CORE.md`.

Technical architecture is owned by `docs/04_TECHNICAL_ARCHITECTURE_CORE.md`.

Guardrails and anti-pattern law are owned by `docs/05_GUARDRAILS_CORE.md`.

Repo process and tranche law are owned by `docs/06_PROCESS_AND_TRANCHE_LAW_CORE.md`.

Runtime output ownership and later-step usage law are owned by `docs/07_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_CORE.md`.

Testing, proof, and promotion law are owned by `docs/08_TESTING_AND_PROMOTION_CORE.md`.

DMPV3 packet-carriage detail is owned by `docs/09_DMPV3_PROTOCOL_CORE.md`.

Vocabulary and term governance are owned by `docs/10_VOCABULARY_AND_TERM_GOVERNANCE_CORE.md`.

## Native Architecture Blueprint boundary

`docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md` is the primary native code-structure architecture authority inside the authority hierarchy defined by this document.

It owns target package placement, component form, seams, ownership, persistence, test-family mapping, reservations, module allocation, and traceability for native code-structure architecture.

It does not outrank this document and must not reinterpret the top-level runtime sequence, serial/parallel/capital/downstream boundaries, or authority hierarchy defined here.

All durable terms used by live control documents must be governed by `docs/vocabulary/vocabulary_registry.md` or lawfully admitted by the vocabulary process before they become canonical language.
