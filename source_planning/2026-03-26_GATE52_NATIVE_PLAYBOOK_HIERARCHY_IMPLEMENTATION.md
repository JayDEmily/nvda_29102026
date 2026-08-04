# Gate 52 — Native Playbook Hierarchy Implementation

Status: complete on `main`

## Purpose

Make `family -> setup_variant -> execution_expression` a native runtime surface instead of leaving hierarchy as a thin compatibility wrapper around a flat rule list.

## Leaves closed in Gate 52

1. `LEAF-G52-001` — make family/setup-variant selection native in runtime contracts.
2. `LEAF-G52-002` — convert execution and review lineage to hierarchy-native outputs.
3. `LEAF-G52-003` — keep the legacy playbook bridge explicit and tested.

## Outputs landed by Gate 52

- `src/nvda_desk/schemas/cognition.py`
- `src/nvda_desk/services/playbook_registry.py`
- `src/nvda_desk/services/playbook_eligibility.py`
- `src/nvda_desk/services/execution_expression.py`
- `src/nvda_desk/services/review_explanation.py`
- `tests/test_gate52_native_playbook_hierarchy.py`

## Entry rule

Gate 51 must already be complete on `main`, with stage ownership and boundary semantics frozen.

## Exit rule

The runtime must emit family and setup-variant candidates natively, execution must preserve family/setup lineage, and the old flat playbook list must remain only as an explicit compatibility bridge.

## Non-goals

- no carry/weekend/event-horizon implementation changes;
- no DMP binding-surface promotion;
- no vocabulary-governance rewrite.
