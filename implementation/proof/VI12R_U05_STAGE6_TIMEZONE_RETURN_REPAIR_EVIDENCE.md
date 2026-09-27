# VI-12R U05 — Stage-6 timezone return bounded repair evidence

## Status

Worker bounded repair after independent Stage-6 `FAIL / RETURN_TO_WORKER` against the frozen U05
candidate `249fb5f2f174b63bd49fe3e749f0e5cacea39d87` / tree
`d09bb7cb419289ac4590b34b42196961a8e044fa`.

This record is Worker evidence only. It is not independent U05 acceptance and does not promote U05.

## Returned invariant

The independent Tester reported that fresh-owner PostgreSQL referential readback depended on the
PostgreSQL database/session timezone. A valid UTC policy persisted under a database whose
`TimeZone` was `Australia/Melbourne` was reconstructed by Psycopg as a `+10:00` aware datetime and
then rejected by the strict semantic constructor with:

`ValueError: activation_ts_utc must be UTC-aware`

The governing Stage-1 architecture requires PostgreSQL `timestamptz` values to reconstruct as
UTC-aware Python `datetime` values and states that local session timezone meaning must not replace
UTC semantic representation.

## Exact reproduction of the failed candidate

The failure was reproduced from an exact detached Git worktree at candidate
`249fb5f2f174b63bd49fe3e749f0e5cacea39d87` using PostgreSQL 17.9 / Psycopg 3.3.4:

- database default `TimeZone` was set to `Australia/Melbourne`;
- a fresh owner persisted a policy whose activation was `2026-09-27 06:00:00+00:00`;
- a completely fresh owner read the same policy through the public read seam;
- observed result: `ValueError: activation_ts_utc must be UTC-aware`.

The reproduced failure matches the independent Tester return proposition.

## Root cause

The candidate treated Psycopg's aware `datetime` representation of a PostgreSQL `timestamptz` as if
its timezone representation were already the semantic UTC representation. PostgreSQL correctly
stores an instant for `timestamptz`, but Psycopg returns that instant using the active session
timezone. `_policy_from_row()` and the other row reconstructors passed those values directly into
semantic records whose accepted contract requires zero UTC offset.

The same mechanism affected every persisted semantic `timestamptz` field:

- policy activation/deactivation;
- capture slot start/end;
- observation receipt timestamp;
- assessment evidence-as-of timestamp.

## Bounded repair

Candidate repair commit:

`2bdbedff62307ecfaf6186f9c12814fb662c11a7`

Candidate tree:

`e15e743e006217a8a3a6313011caf82265a679cf`

The repair is limited to:

- `src/nvda_desk/raw_signal_occurrence_truth/_postgres.py`;
- `tests/product/raw_signal/test_u05_stage2_restart_foundation.py`.

The PostgreSQL adapter now reconstructs every non-null `timestamptz` through one technical helper
that requires an aware database value and converts the same instant with `astimezone(UTC)` before
constructing semantic records. Optional policy deactivation uses the corresponding optional helper.

No schema, semantic owner rule, transaction rule, assessment rule, PostgreSQL global/session setting,
or accepted U01-U04 contract was changed.

## Regression discriminator

A new Stage-2 restart test:

`test_stage2_fresh_owner_normalizes_timestamptz_readback_under_non_utc_database_timezone`

performs the returned challenge directly:

1. records the proof database's original timezone;
2. sets the database default timezone to `Australia/Melbourne`;
3. verifies a newly opened raw Psycopg session actually reports `Australia/Melbourne`;
4. writes a UTC policy through one fresh public owner;
5. constructs another fresh owner;
6. reads the policy through the public read seam;
7. requires exact policy equality and a UTC `tzinfo` on the reconstructed activation timestamp;
8. restores the original database timezone in `finally`.

The discriminator passes on the repair candidate.

## Post-freeze Worker validation against exact candidate

All results below were rerun after repair candidate
`2bdbedff62307ecfaf6186f9c12814fb662c11a7` was committed.

- Stage-2 + Stage-3 + Stage-4 + Stage-5 restart set: **27 passed**.
- Configured U05 PostgreSQL durability family: **55 passed / 0 failed**. Execution was split into
  bounded batches to stay below the tool-call ceiling; any timed-out combined batch was rerun in
  smaller complete slices before being counted.
- Accepted U01-U04 regression set: **416 passed**.
- Architecture/bootstrap: **74 passed**.
- Ruff `0.15.11`: **All checks passed**.
- mypy `1.20.1` over `src`, using the established combined exact-toolchain environment required for
  PyYAML visibility: **Success: no issues found in 16 source files**.
- `git diff HEAD^..HEAD --check`: pass / no output.

Proof environment remained Python 3.13.5, PostgreSQL 17.9 and Psycopg 3.3.4 with the preserved U05
bootstrap environment. The database default was restored to `Etc/UTC` after the non-UTC challenge.

## Source-level closure check

The repaired source was traced for every `TIMESTAMPTZ` reconstruction. All persisted semantic
`timestamptz` fields now route through `_utc_datetime_from_row()` or its optional wrapper before
semantic construction; no previous direct row-datetime pass-through remains.

## Disposition

**WORKER REPAIR CANDIDATE READY FOR FRESH INDEPENDENT RE-REVIEW.**

The failed candidate `249fb5f...` remains failed and historical. The replacement candidate is
`2bdbedff62307ecfaf6186f9c12814fb662c11a7` / tree
`e15e743e006217a8a3a6313011caf82265a679cf`.

The next lawful action is a fresh independent Stage-6 Tester review against exactly that replacement
candidate. No U05 promotion or Stage-7 action is authorised until independent `PASS`.
