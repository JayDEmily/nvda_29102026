# Implementation ledger — plan: /repository/EXEC_PLAN.md

Base: 3fe9f792b10c1eb9d2797eccc2f81d623620f69c.
Authority: F4_OWNER_APPROVED_CLARIFICATION_20261013.md.
This is an implementation checklist, not another normative execution plan.

1. Prove/admit immutable RiskScope and synchronise approved catalogue contexts.
2. Prove/repair execution-cost and retained-edge D178 contracts.
3. Prove/repair D175 exact calibrated limits and D176 consumer.
4. Prove/repair joint D189 clipping and actual D192 breach/precedence.
5. Reconcile Stage-1 evidence, pinned-runtime/database verification and review.

Shared interface: D175 exact scope/ceiling → D176/D189/D192.
Shared interface: D133 retained execution terms → D164/D178.
Production must follow separately committed RED proofs for each unit.

Environment: Python 3.13.5, pytest 9.0.3, mypy 1.20.1, ruff 0.15.11,
psycopg 3.3.4 and PyYAML 6.0.3 installed from the supplied pinned wheels.
