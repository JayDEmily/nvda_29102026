# N-06 — Cross-state transaction boundary

## Status

Accepted — normative authority complete for `C-024`.

## Unresolved proposition

What is the smallest admitted transaction boundary linking material state changes to receipts/execution records, and what atomicity, idempotency, sequencing, failure and replay law applies without inventing one global transaction?

## Material read set

Normative authority read in full or as connected authority before decision: `docs/04`, `04.1`, `05`, `07`, `07.1`, `09`, `09.1`, `11` and `11.1`.

Gate B and Gate C evidence read: `B06.3` with neighbouring persistence-repository context, row `C-024`, and the complete B06 Gate C design record.

Existing tests read as evidence: receipt-ledger, execution-record repository and checkpoint-receipt proof-model tests.

Bounded source read as consequence evidence: complete receipt-ledger and execution-record repository implementations, plus connected capital/position/execution receipt usages.

## Adopted project decision

The smallest admitted transaction boundary is one accepted domain command or decision plus every mutation and attesting receipt/commit record required to truthfully claim its result for one owner-declared consistency unit. Declared participants commit atomically; failure produces no success receipt. Idempotency binds command scope/key to semantic input fingerprint, result, state sequence and receipt. Same-key/same-input replay returns the original result without mutation; same-key/different-input fails.

Independent domains compose as linked owner-specific transactions, not one global transaction. External irreversible effects require an explicit prepare/commit, outbox, acknowledgement or compensation protocol and remain pending/uncertain until consistency is proven.

Governing propositions: `docs/07.2_STATE_RISK_AND_REPLAY_WORKING.md` sections `07.2.N06.1` through `07.2.N06.7`.

## Alternatives ruled out

- Appending a receipt after unrelated state writes and treating both as consistent: ruled out because partial success can falsely attest a result.
- One repository-wide/global transaction: ruled out because it destroys domain ownership and couples unrelated state.
- Duplicate-ID rejection in one ledger as complete idempotency: ruled out because input fingerprint, state version, result and external effects are not bound.
- Insertion order as committed sequence authority: ruled out because process lifetime and concurrency are not governed.
- Claiming external completion before acknowledgement/reconciliation: ruled out because local atomicity cannot prove an external irreversible effect.

## Longitudinal effects

An owner-declared command validates expected state and idempotency, applies all required state mutations and its receipt atomically, publishes one committed result, then permits the next owner-specific workflow transaction. Replay reconstructs transitions without issuing live side effects.

## Transverse effects

The decision fixes transaction scope, consistency-unit ownership, repository participation, expected-version checks, idempotency binding, sequence/version truth, failure/attempt records, external-effect uncertainty, adapter substitution and replay lineage.

## External sources

No external source was required. The exact boundary is project-specific and derived from existing owner, state, receipt, fail-closed and replay laws.

## Current implementation consequence

Current memory ledgers provide append/copy seams but no atomic cross-state unit, complete idempotency binding, committed sequencing or recovery guarantee. No implementation change or conformance claim is made.

## Remaining Unknowns

- Exact aggregate/consistency-unit definitions for each downstream command remain owner-specific implementation design under this law.
- Production database, message/outbox and external-broker protocols remain intentionally unknown.
- Recovery-time, retention and operational availability targets remain intentionally unknown.
