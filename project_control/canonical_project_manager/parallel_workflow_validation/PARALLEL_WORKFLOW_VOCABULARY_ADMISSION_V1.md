# Parallel Workflow Vocabulary Admission V1

## Decision

`ADMITTED:M15_PARALLEL_WORKFLOW_CONTROL_TERMS_V1`

Direct user authority on 28–29 July 2026 establishes a recurring PM-controlled execution architecture. The following are durable programme-control concepts and therefore require human semantic admission before continued use in live controls:

1. `PM-controlled Parallel Workflow`;
2. `Parallel Execution Lane`;
3. `Lane Assignment`;
4. `Material Read Set`;
5. `Worker Candidate Archive`;
6. `Tester-approved Portability Artefact`;
7. `Independent Control Test`.

The `Lane Assignment` record governs its lifecycle and exceptional status tokens. These are control-state values, not runtime-domain states or independent architecture modules.

## Distinctions

- Parallel execution does not create parallel canonical authority.
- A lane is capacity, not module ownership or a long-lived branch.
- An assignment is one revisioned semantic unit, not a programme or automatic continuation chain.
- A Material Read Set is a stale-base trigger, not general required reading.
- A Worker Candidate Archive is unaccepted candidate state.
- A Tester-approved Portability Artefact is reconstructable evidence suitable for PM review, not canonical acceptance.
- An Independent Control Test tests the operating-control package and cannot repair or accept it.

## Projection route

Human authority is recorded in `docs/10.1_VOCABULARY_AND_TERM_GOVERNANCE_WORKING.md` and `docs/vocabulary/vocabulary_registry.md`. `data/vocabulary/canonical_vocabulary.json` must be regenerated only through `python scripts/build_canonical_vocabulary.py`.
