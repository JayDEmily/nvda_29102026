# Gate C normative-authority tests

These tests are admitted by `project_control/normative_authority_top_down_alignment/EXEC_PLAN.md`.
They express the frozen normative baseline and Gate B semantic units. A failing test may be an
accepted Gate C result; production implementation changes belong to Gate D.

The suite must not mutate governed tracked artefacts. Tests use isolated temporary paths for any
generated material and distinguish process-memory behaviour from durable persistence.
