# Semantic receipt — `tests/tier_a/upstream_signal/test_raw_signal_transform_boundary_surface.py`

- Sequence `037`, PM-012; SHA `70e285e8e601ef43794433802dc213d950c63554167c4d03070302ed12a03de4`.
- Read full test `1-62`, all four scanned modules, authority and routes. Pytest: `2 passed in 0.04s`.
- G1 `40-52`, authority `N04-002` (`docs/04.1...:21-42`): nine import-prefix families are absent from four files. Add a listed import and `52` fails; renamed, dynamic, transitive or external forbidden ownership passes. `related_but_not_proved` / `token_only`.
- G2 `55-62`, same authority: seven donor symbol names are absent. Add one and `62` fails; equivalent renamed schemas/services pass. `related_but_not_proved` / `token_only`.
- Groups/relationships `2/2`; final `BLOCKED_P3_REPAIR`. No runtime transformation, dependency ownership, scope lock, field exposure or non-interference is exercised; the entire claimed boundary is lexical. No mutation executed.
