# VI-12R U05 Stage 3 — Observation Durability and Restart Evidence

## Status

**WORKER STAGE-3 COMPLETE — STAGE 4 NOT STARTED — NOT U05 ACCEPTANCE**

This record closes Stage 3 of the active root `EXEC_PLAN.md` only. It records Worker evidence for
observation durability and restart semantics on the exact committed Stage-3 implementation/proof
state. It does not claim restarted receipt/assessment semantics, whole-U05 closure, independent
Tester acceptance, or promotion.

## Binding state

- branch: `work/u05-restart-architecture`;
- Stage-2 handoff parent: `303d0ccdf6ccc78867c0ca6879c11a85db63e322`;
- Stage-3 implementation/proof commit: `55927d065c9fff4283aa29197518e5927c0092bc`;
- Stage-3 implementation/proof tree: `32a83b3a1f6e81b4b6498c2ea1d12430e23cff56`;
- active plan on `main`: `4bf4b4feb08412f65216fc95d8615d2cc46eadaf`;
- accepted U04 production candidate: `dc3b448191a2b2d3528ffb576b1ebc2c56839991`;
- independent Reviewer-032 U04 PASS: `dd42d645b59a62f88cfbc7fba47a75e415b7296f`.

The Stage-3 implementation commit changes only:

- `src/nvda_desk/raw_signal_occurrence_truth/api.py`;
- `src/nvda_desk/raw_signal_occurrence_truth/_postgres.py`;
- `tests/product/raw_signal/test_u05_stage3_observation_restart.py`.

No Stage-4 receipt-evidence or ordinary restarted assessment implementation is introduced by this
commit.

## Stage-3 proposition established

Against real PostgreSQL, a completely fresh owner with empty process-local semantic state can now,
through the owner public seam:

1. durably append a complete accepted `RawObservationOccurrenceV1`;
2. read the original durable observation by domain identity from another fresh owner;
3. reconstruct observation identities, provenance, receipt time, optional source metadata,
   catalogue identities and nanosecond evidence without using process-local owner state;
4. reconstruct the complete finite NativeValueV1 carrier from a deterministic versioned `bytea`
   codec, including `None`, exact bool/int/float/Decimal/string/bytes, list, tuple and logical mapping
   distinctions;
5. preserve IEEE-754 float representation, including signed zero and a non-default NaN payload;
6. preserve `Decimal.as_tuple()` representation for finite Decimal values, NaN, sNaN and Infinity;
7. bind a same-identity retry to the durable original and return it only for accepted exact content;
8. reject conflicting reuse of an already-durable observation identity without replacing the first
   occurrence;
9. query the durable maximum ingestion sequence for the exact `ingestion_sequence_scope` and enforce
   the accepted non-decrease rule after complete process loss;
10. keep ingestion high-water scope-local rather than inventing a global ordering;
11. continue to permit an equal sequence and a higher sequence according to accepted U03 law;
12. roll back a failed observation write so neither the fact nor a phantom high-water survives;
13. return public success only after the observation transaction exits successfully and commits; and
14. retain the Stage-2 private durability capability boundary and all accepted U01-U04 behaviour.

## Realised ownership and transaction mechanism

The Stage-1 contract remains intact:

- M-owner code reads a durable same-identity observation and applies the accepted
  `_observations_exactly_equal` semantic comparator;
- M-owner code obtains the durable scope-local high-water and decides whether the new sequence is
  lawful;
- PostgreSQL stores/query already-decided observation facts and supplies transaction/locking
  mechanics only;
- the observation high-water query takes the existing technical write-lock mechanism on the
  observation relation before `MAX(ingestion_sequence)` is evaluated;
- after that correctness lock is obtained, the owner re-reads the observation identity before
  appending, so a concurrent same-ID writer is rebound to owner idempotency/conflict semantics rather
  than treated as semantic authority by a database uniqueness error;
- high-water check and observation append occur in one transaction;
- `synchronous_commit=on` remains set for write transactions and the public command returns only
  after transaction-context exit commits;
- exceptions roll back and propagate; no failed observation write is converted into an empty,
  unknown or zero semantic result.

The in-memory U03 path remains unchanged when no U05 `durability_port` is injected. The new durable
observation path does not hydrate `_OwnerState.observations_by_identity` or
`ingestion_high_water_by_scope`; fresh-owner correctness therefore does not depend on reconstructing
those caches.

## PostgreSQL observation representation

Stage 3 adds the Stage-1-authorised relation `rsot_raw_observation_occurrence_v1` containing:

- observation identity;
- delivery/provider identities;
- versioned NativeValueV1 `bytea` content;
- receipt timestamp and optional nanosecond evidence;
- ingestion sequence and exact scope;
- source temporal kind;
- optional ordered Raw Signal catalogue identities; and
- the accepted optional provenance/source/timezone/session/revision headers.

No separate semantic high-water table is introduced. The durable high-water is the maximum committed
sequence in the exact scope, as specified by Stage 1. No performance index, relation materialisation,
assessment-evidence query or Stage-4 semantic mechanism is introduced.

## NativeValueV1 codec trace

The Stage-1 requirement that JSON/JSONB must not collapse admitted U03 distinctions is realised by a
private deterministic binary codec with an explicit `NVDA-NATIVE-V1` version prefix and recursive
branch tags.

- exact float content is stored as IEEE-754 binary64 bytes;
- exact Decimal tuple content is encoded as sign/digits/exponent, including the special exponent
  forms for NaN, sNaN and Infinity;
- mapping implementation/order is not preserved as semantic content; logical exact-string keys are
  encoded in deterministic UTF-8 key order;
- list versus tuple remains distinct;
- provider-native `None` remains a typed native value inside the codec and is not collapsed with SQL
  `NULL`, which is reserved for structural optional-field absence.

During the Worker logic trace, the first special-Decimal decode implementation was found to assume an
integral Decimal exponent. Accepted U03 authority explicitly preserves NaN representation through
`Decimal.as_tuple()`, whose exponent may be `n`, `N` or `F`. The codec was repaired before commit and
the focused PostgreSQL proof now includes `-NaN`, `sNaN` and `-Infinity` readback.

## Primary authority and evidence inspected

The Worker inspected the current governing and accepted material required for this stage, including:

- `GUARDRAILS.md`;
- root `AGENTS.md` and `tests/AGENTS.override.md`;
- active root `EXEC_PLAN.md`, especially Stage 3;
- `handoff/control/CURRENT_STATE.md`;
- `implementation/architecture/VI12R_U05_STAGE1_RESTART_ARCHITECTURE.md`;
- `implementation/proof/VI12R_U05_STAGE2_RESTART_FOUNDATION_EVIDENCE.md`;
- accepted U03 implementation/proof lineage including
  `VI12R_U03_NATIVE_DOMAIN_CLOSURE_EVIDENCE.md` and Reviewer-030 disposition;
- `implementation/authority/VI13R_U03_NATIVE_VALUE_DOMAIN_AUTHORITY.md`;
- accepted U01-U04 production/product tests.

The abandoned pre-recovery U05 implementation, CP0-CP8 checkpoint state and abandoned U05 result
records were not resumed or used as implementation authority.

## Exact runtime evidence

Stage-3 runtime proof used the preserved U05 proof environment:

- Python `3.13.5`;
- pytest `9.0.3`;
- mypy `1.20.1`;
- Ruff `0.15.11`;
- Psycopg `3.3.4`;
- PostgreSQL `17.9`;
- `server_encoding=UTF8`;
- `fsync=on`;
- `synchronous_commit=on`;
- `full_page_writes=on`;
- empty `listen_addresses` with Unix-domain-socket transport.

No SQLite, mock database or process-local persistence substitute was used for the Stage-3 restart
proof.

## Validation rerun against the committed Stage-3 tree

All results below were rerun after
`55927d065c9fff4283aa29197518e5927c0092bc` was committed.

1. Stage-3 focused real-PostgreSQL discriminator:
   - `pytest tests/product/raw_signal/test_u05_stage3_observation_restart.py -q`
   - result: **5 passed**.
2. Stage-2 + Stage-3 real-PostgreSQL restart set:
   - `test_u05_stage2_restart_foundation.py`;
   - `test_u05_stage3_observation_restart.py`;
   - result: **12 passed**.
3. Accepted U01-U04 regression set:
   - `test_u01_contract_owner_boundary.py`;
   - `test_u02_capture_schedule.py`;
   - `test_u03_observation_native_temporal.py`;
   - `test_u04_receipt_assessment.py`;
   - result: **416 passed**.
4. Architecture/bootstrap suite:
   - `pytest tests/architecture tests/bootstrap -q`;
   - result: **74 passed**.
5. Static typing:
   - mypy `1.20.1` over `src` in the established combined exact project toolchain;
   - result: **Success: no issues found in 16 source files**.
6. Ruff over all Stage-3 modified Python paths:
   - result: **All checks passed**.
7. `git diff HEAD^..HEAD --check`:
   - result: no whitespace errors.
8. Exact Git state after implementation commit:
   - `HEAD` = `55927d065c9fff4283aa29197518e5927c0092bc`;
   - tree = `32a83b3a1f6e81b4b6498c2ea1d12430e23cff56`;
   - parent = `303d0ccdf6ccc78867c0ca6879c11a85db63e322`;
   - `main` = `4bf4b4feb08412f65216fc95d8615d2cc46eadaf`;
   - worktree clean before this evidence/handoff-only close-out change.

## Environment-only validation issue

One architecture/bootstrap invocation initially used the proof-venv `python3.13` selected by the
sourced environment. That venv intentionally does not contain PyYAML, so collection stopped with ten
`ModuleNotFoundError: yaml` errors. The command was rerun using the host Python 3.13.5 interpreter
(which contains project-pinned PyYAML 6.0.3) with the exact proof-venv packages on `PYTHONPATH`, the
same combined-toolchain pattern already used by Stage 2. The architecture/bootstrap result was
74/74. Likewise, mypy was run through that combined interpreter so its already-present PyYAML typing
support was available. These were environment composition failures, not product-test failures, and
no semantic/test relaxation was made.

## Logic-trace boundary

The realised Stage-3 path was read through independently of the tests:

`owner.commands.admit_raw_observation_occurrence`
→ durable same-ID query
→ durable scope-local high-water query/correctness lock
→ same-ID re-read under that lock
→ M-owned exact-content/high-water decision
→ PostgreSQL observation append
→ transaction context exit/commit
→ public success.

The corresponding referential read is:

`owner.reads.get_raw_observation_occurrence`
→ read transaction
→ PostgreSQL identity query
→ exact typed observation/native decode
→ public record.

No correctness-critical observation identity/high-water input in those paths is sourced from
process-local `_OwnerState` when a `durability_port` is present.

## Validation boundary

**VERIFIED:** Stage-3 durable observation identity/content/readback, NativeValueV1 fidelity,
scope-local high-water after restart, failure rollback and commit acknowledgement for the exact
implementation commit above.

**NOT VERIFIED / NOT CLAIMED:**

- durable receipt-relation derivation from a fresh owner (Stage 4);
- ordinary restarted assessment evidence/predecessor/supersession semantics (Stage 4);
- whole-U05 restart equivalence (Stage 5);
- independent Tester acceptance;
- U05 promotion or programme acceptance.

## Stage boundary / next lawful action

Stage 3 stops here. Stage 4 has not started.

The next lawful engineering action is only a separately authorised Stage-4 execution from this
committed lineage: receipt evidence, assessment history and restarted U04 semantics. This Stage-3
close-out does not itself authorise that work.
