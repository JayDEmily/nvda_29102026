# VI-12R U02 Reviewer-023 repair evidence

## Status

**WORKER REPAIR CANDIDATE — NOT INDEPENDENTLY ACCEPTED.**

Reviewer 023 returned `FAIL / RETURN_TO_WORKER` on U02 because the realised public command/read
facets directly exposed shared mutable `_U02State` through `_state`. The authorised repair is only
`R023-U02-F001`; U03 remains prohibited.

## Exact repaired candidate

- branch: `work/vi12r-u02-r023-repair`;
- rejected candidate: `a77dc596b7cbc3f248097df94d8dd0bef4491bec`;
- Reviewer-023 FAIL commit: `b7a5389d361172d33e3033b209ba5c67350c6fee`;
- repaired candidate: `5c62ec5147da718297b251b5a287405ebf3b4755`;
- tree: `dc1293d2c3d7e234e53a8d663f25eac51f7086ab`;
- repair paths: `src/nvda_desk/raw_signal_occurrence_truth/api.py` and
  `tests/product/raw_signal/test_u02_capture_schedule.py`.

## Repair proposition

Public command/read facets no longer carry an ordinary caller-reachable mutable semantic-state
object. Their stored capabilities are only validated command/read callables; owner-local U02 state
remains behind those capabilities. The exact `_state` bypass is absent, and bounded direct-attribute
traversal rejects an equivalent trivially renamed mutable container/wrapper exposure.

This claim does not extend to arbitrary function-closure introspection, runtime monkey-patching,
`eval`/`exec` or unrestricted Python metaprogramming.

## Validation

Exact pinned environment: Python 3.13.5, pytest 9.0.3, mypy 1.20.1, Ruff 0.15.11.

- focused U01+U02: 328/328 passed;
- concrete Reviewer-023 regressions: 2/2 passed;
- Ruff: pass;
- source mypy: pass, 15 source files;
- product-proof control: pass, 6 families / 13 of 13 obligations;
- architecture/dependency/public-seam controls: pass;
- architecture/bootstrap: 74/74 passed;
- architecture promotion: 74/74 passed;
- Git diff/integrity: pass;
- clean committed candidate state: yes.

Fresh Reviewer 024 must independently disposition the repaired U02 candidate. U03 remains
prohibited until U02 receives `PASS` and is lawfully promoted to forward `main`.
