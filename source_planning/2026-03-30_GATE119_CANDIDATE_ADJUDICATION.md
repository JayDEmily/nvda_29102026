# Gate 119 — Candidate Adjudication and Contradiction Resolution

Status: complete on `main`

## Purpose

Replace registry-order lead selection with deterministic candidate adjudication so mixed eligible playbooks are resolved by scored reasons rather than list position alone.

## What changed

- `ExecutionExpressionOutput` now carries scored candidate adjudication records, lead-selection score, and contradiction-resolution state.
- `ExecutionExpressionService` now ranks eligible candidates deterministically and uses registry priority only as a tie-break.
- Review packets now expose the adjudication record automatically through the execution packet surface.

## Proof slice

- `PYTHONPATH=src pytest -q tests/test_gate119_candidate_adjudication.py tests/test_gate115_historical_evaluation_readiness_planning.py tests/test_document_hygiene.py`

## Outcome

- multi-eligible candidate pools now produce one explicit lead justified by score and recorded reasons
- contradiction and tie-break behaviour are review-visible rather than hidden in registry order
