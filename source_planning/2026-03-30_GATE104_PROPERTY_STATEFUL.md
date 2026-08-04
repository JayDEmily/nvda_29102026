Status: Gate 104 complete on `main`; Gate 105 is the next active gate in the successor testing pack

# 2026-03-30_GATE104_PROPERTY_STATEFUL.md

## Purpose

Add targeted Hypothesis-backed property and stateful tests only for the bounded high-risk services named by the successor testing pack.

## Gate 104 result

- Verdict: `complete_targeted_property_stateful`
- Downstream permission: Gate 105 may begin

## Scope frozen by this gate

Property coverage:
- `StateConditionedModifierService` bounded combination-law checks
- `PlaybookEligibilityService` bounded no-trade law checks

Stateful coverage:
- `EventStoreService` ordered query/next-event sequence law

## Dependency note

Hypothesis was added to the repo dev dependencies for this gate only because the active pack explicitly requires targeted property/stateful testing.
This gate does **not** authorise indiscriminate property-test sprawl elsewhere in the repo.

## What is now frozen

- modifier kill-switch and bounded deployable-capital law remain stable across generated high-risk combinations;
- playbook-eligibility no-trade law remains stable across generated permission/event/options combinations;
- generated ordered event-store queries keep next-event progression monotonic rather than skipping backward.
