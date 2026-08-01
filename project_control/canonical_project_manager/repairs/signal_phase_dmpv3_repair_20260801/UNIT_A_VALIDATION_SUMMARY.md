# Acceptance Unit A — Validation Summary

## Outcome

**PASS** — signal-informed intraday phase authority is implemented and integrated through a narrow M05 temporal adapter. The accepted M05 runner remains pure and unchanged.

## Known true

- Authority/control amendment commit: `7748157`.
- Expected-red proof commit: `61f0033`.
- The baseline three C-026 nodes failed because `nvda_desk.domain.temporal.intraday_phase` did not exist.
- Focused current proof: **51 passed, 0 failed**.
- Wider affected current proof: **188 passed, 10 failed**.
- Identical accepted-baseline route: **178 passed, 13 failed**.
- Exact delta: the three C-026 nodes resolved; the ten C-004/C-013/C-024/C-046 failures remain pre-existing; **zero new failing nodes**.
- M05 vocabulary audit: **0 unresolved candidates**, 148 resolved occurrence rows in scope.
- Canonical vocabulary builder parity passes.
- `python -m compileall -q src` passes.

## Implemented surfaces

- `src/nvda_desk/domain/temporal/intraday_phase.py`
- `src/nvda_desk/domain/temporal/__init__.py`
- `src/nvda_desk/m05_serial_cognition/temporal_adapter.py`
- expanded temporal Stage Input fact/owner admission in `src/nvda_desk/m05_serial_cognition/contracts.py`
- public adapter export in `src/nvda_desk/m05_serial_cognition/__init__.py`

## Behaviour proved

- same clock time can produce different phases from different sustained signals;
- clock-only and stale evidence fail closed as explicit degradation;
- minimum dwell/hysteresis prevents one-observation transition;
- apparent regression is held without authoritative correction;
- authoritative correction preserves superseded-state lineage;
- identical evidence/state/policy replays deterministically;
- process-memory repository reads are detached and version-monotonic;
- the M05 adapter emits only admitted primitive facts and exact temporal authority lineage;
- degraded temporal results do not become positive permission.

## Evidence

- `evidence/UNIT_A_EXPECTED_RED.txt`
- `evidence/UNIT_A_FOCUSED_GREEN.txt`
- `evidence/UNIT_A_AFFECTED_BASELINE.txt`
- `evidence/UNIT_A_AFFECTED_CURRENT.txt`
- `evidence/UNIT_A_VOCABULARY_AUDIT.txt`

## Ruled out

- fixed-clock substitution as the detailed phase result;
- temporal repository access inside `SerialRunner`;
- M05 ownership of phase semantics or state;
- durability claims for the in-memory repository;
- degraded phase used as positive permission.

## Next gate

Acceptance Unit B: mandatory DMPV3 carriage for canonical M05/M06 egress into M09.
