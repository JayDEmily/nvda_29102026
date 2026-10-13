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

Context RED d307874 → production 7075768; scope focused 2 passed.
D178 RED 7e56807 → production 1fceb5c; execution focused 14 passed.
Risk RED e70736a (corrected flat immutable membership fixture) → production 076342c;
shared monetary focused 32 passed. D164/D176 RED 14e0309 → production 076342c;
combined approved contracts 50 passed. Account projection RED a65ebe9 → public repair pending commit.

Ruling: encode membership triples as explicit `contract|signed_quantity|source_ref`
strings in an immutable P_BASIC tuple — the existing configuration contract admits
flat scalars only — incompatible delimiters or ambiguous identities fail closed.
Ruling: replace inherited scalar D175/D133 and partial D189/bool D187 fixtures
with approved structured values, preserving arithmetic and refusal assertions —
the approved contract supersedes those fixture shapes, not valid test obligations.
Ruling: discard reproducible inherited mypy cache — fresh pinned checker passes
while the imported cache caused an internal checker error — no source/tests changed.

PostgreSQL execution BLOCKED in current host: only uid/gid 0 is mapped. runuser
reports `cannot set groups: Operation not permitted`; chown to oai reports
`Invalid argument`; unshare alternate non-root mapping reports `Operation not permitted`.
No PostgreSQL startup/security check is bypassed. Database acceptance cannot be claimed.
