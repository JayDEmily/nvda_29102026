# Unit 4 — Durable State, Evidence and Restart Recovery

## Outcome

PASS for bounded SQLite durability. This unit does not establish live-account truth, external-effect recovery, backup policy or universal durability.

## Implemented surfaces

- `SqliteUnitOfWork` implements the accepted M13 transactional/read port over one SQLite transaction for state, version, sequence and `AtomicReceipt`.
- Deterministic durable JSON accepts an explicit subset only: scalar JSON values, finite `Decimal`, UTC `datetime`, tuples, lists and string-key mappings.
- `SqliteEvidenceRepository` implements a typed evidence port retaining owner, occurrence identity, Pydantic contract path, canonical content fingerprint and committed sequence.
- M11 accepts an injected transactional state port, truthfully labels SQLite-backed paper positions/snapshots/receipts, and restores the last transition, fill history and lifecycle history after restart.
- Exact duplicate fills and lifecycle decisions remain idempotent across restart, including a prior fill replay after a later durable close; they do not reopen or remutate portfolio state.
- M12 can build replay material from a typed evidence occurrence reloaded after restart.

## Admitted propositions

`M13-DURABLE-001` through `M13-DURABLE-006`, and `M11-DURABLE-001` through `M11-DURABLE-002`, in `docs/07.2_STATE_RISK_AND_REPLAY_WORKING.md`.

## Validation

- Expected-red extensions before implementation: restart snapshot time, lifecycle receipt replay and old-fill-after-close protection failed on the previous process-memory-only implementation.
- Unit 4 proof: `10 passed`.
- Affected M13/M11/M12 plus proof-control run: `237 passed`.
- Proof authority: `PASS families=199 tests=201 blocks=71`.
- Promotion membership check: `18` blocks, `18` families, `20` test paths.
- Black on changed Python: PASS after formatting three branch-owned files.
- Ruff on changed Python: PASS, zero findings.

## Ruled out

- No live broker or provider operation was introduced.
- No credential, account or endpoint configuration was added.
- No process-memory state is represented as durable.
- No arbitrary Python object or non-UTC timestamp can enter the durable state codec.
- No existing module semantic owner was transferred to M13.

## Next gate

Unit 5: explicit live-provider and broker operational boundary, default offline and fail-closed.
