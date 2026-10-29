# Stage-1 acceptance-boundary amendment — 2026-10-08

Programme Owner authority: explicit user approval on 2026-10-08 to amend the Stage-1 acceptance boundary and continue independent review.

The accepted brief and normative catalogue are unchanged. This amendment resolves an execution-plan circularity: Stage 1 previously required every Stage-1-kernel row to be publicly reachable before Stage 2 could start, while the normative catalogue gives some of those rows Stage-2 predecessors.

Normative catalogue census:

- 174 rows have Stage-1 kernels (`K01`–`K08`, `K16`, `K17`).
- 144 have dependency closure entirely within Stage 1.
- 25 have a direct Stage-2 predecessor: D097, D098, D107, D108, D128, D155, D158, D159, D163, D164, D166, D167, D172, D173, D175, D176, D178, D187, D190, D191, D192, D199, D200, D207, D208.
- 5 additional rows reach Stage 2 transitively: D156, D157, D171, D186, D189.
- Total cross-stage Stage-1 rows: 30.

Accepted execution boundary:

- all 174 Stage-1 rows: exact binding plus Stage-1 kernel implementation/proof;
- 144 Stage-1-closed rows: public end-to-end reachability required now;
- 30 cross-stage rows: own-kernel semantics and fail-closed public behaviour required now; full graph reachability deferred until their normative Stage-2 predecessors exist;
- Stage 2 must prove those cross-stage connections when implementing K09–K15;
- Stage 3 remains responsible for the complete 209-row end-to-end graph.

This changes no D identity, dependency, kernel mathematics, accepted brief clause, catalogue row or terminal M01 acceptance condition.
