# M13 State Kernel — Module-local Proof Record

## Status

`MLC-V_COMPLETE_IMPLEMENTATION_CLOSED`

- Module: `M13 state_kernel`
- Branch: `proof/m13-state-kernel`
- Baseline after fast-forward merge: `main` at `b153cd1e3e0808991dcf9c188e380d935cfd9283`
- Frozen proof checkpoint: `5f672ddf5a712a3446bada00ebcbbf1d7c0f321c`
- Historical requirement: `C-024`
- Historical obligation: `D-054`
- Governing protocol: `project_control/canonical_project_manager/GATE_C_COMPLETION_PROTOCOL.md`
- Production source: closed during this proof gate

## MLC-A — Authority sufficiency

**Result:** `AUTHORITY_SUFFICIENT`

### Governing proposition

`docs/07.2_STATE_RISK_AND_REPLAY_WORKING.md:17-76` admits the smallest owner-declared transaction boundary:

- one accepted domain command/decision and every mutation plus attesting receipt required for one named consistency unit;
- atomic visibility of declared state changes and the success receipt;
- no success receipt on validation, version, mutation or receipt failure;
- idempotency scoped to command type and consistency unit and bound to semantic input fingerprint, command/result identity, state version/sequence and receipt;
- exact duplicate replay returns the original committed result without repeating mutation;
- conflicting reuse fails;
- owner-specific transactions remain separate rather than becoming one global transaction;
- memory proof is explicitly non-durable and does not prove restart recovery or external-effect reconciliation.

### Accepted owner and surface

- Owner: `M13 state_kernel`.
- Architecture surface: `5.16 Persistence ledgers and receipts`.
- M13 owns transaction mechanics, idempotency binding, atomic receipts and storage ports.
- Domain modules retain semantic ownership of positions, capital, calendar facts, risk observations and other records.

### Bounded alpha transformation

```text
TransactionCommand + owner-declared working-state mutation
→ validate scoped idempotency and expected state version
→ execute against an isolated working copy
→ atomically publish resulting state version and AtomicReceipt
→ return committed receipt or exact duplicate replay response
```

### Identity, lineage, time, state and side effects

- Required identity: command ID; command type; consistency-unit ID; idempotency-key value; input semantic fingerprint; policy/config version; result ID; receipt ID.
- Required state truth: expected prior version; resulting version; deterministic committed sequence.
- State ownership: M13 owns only the transaction journal/mechanism. The test state is synthetic and has no trading-domain meaning.
- Time: no wall-clock value is required for deterministic transaction equivalence in this alpha slice.
- Side effects: none outside the in-memory boundary. External irreversible effects, outbox protocols and durable recovery are excluded.

### Prohibited authority

M13 must not:

- own domain-record meaning;
- create one repository-wide global transaction;
- treat a duplicate receipt ID as complete idempotency;
- claim production durability, crash atomicity, restart recovery or external-effect completion;
- fabricate domain identities, policy decisions or business results;
- import unopened domain modules to obtain semantic authority.

### Routed evidence

- Normative decision: `N-06_CROSS_STATE_TRANSACTION_BOUNDARY.md`.
- Historical proof envelope: `D-054.md`.
- Accepted architecture: M13 row in `Atlas_Architecture_Decision_Report.md` and machine projection.
- Atlas candidate evidence was screened for transaction/persistence meaning; no Atlas cohort was admitted as additional behaviour. Relevant rows remain supporting context only because the direct N-06 authority is complete.

## MLC-R — Relevant-test routing

### Current authoritative route

- `tests/tier_a/persistence/test_m13_state_kernel_contract.py` — new module-local Tier A proof family.

### Historical tests

The three historical `C-024` nodes in `test_gate_c_normative_completion_contracts.py` remain expected-red historical evidence but are **superseded for current M13 proof** because:

1. they target the superseded package path `nvda_desk.persistence.transactions` rather than the accepted `m13_state_kernel` package boundary;
2. they do not prove expected-version rejection, committed sequence, scoped idempotency, state/result/receipt binding, non-durable labelling or rollback after invalid receipt construction.

Disposition: `NON_AUTHORITATIVE_OBSERVATIONAL` for the current M13 opening decision; preserve unchanged for final consolidation.

### Shadow routes

- receipt-ledger and execution-record repository tests: `LEGACY_SHADOW_UNADMITTED` for M13 transaction authority; they prove only their local append/copy seams.
- Tier B checkpoint-receipt contract: observational shadow only; it does not prove state/receipt atomicity.
- all unrelated tests: `LEGACY_SHADOW_UNADMITTED`.

## MLC-O — Factual observation

### Historical C-024 nodes

- They import a missing `nvda_desk.persistence.transactions` module.
- They assert exact duplicate non-repetition, differing-input conflict and rollback after a mutation exception.
- Baseline execution on 25 July 2026 produced three failures solely because the module is absent.
- They do not observe a target M13 package, expected-version rejection, sequence/version binding, idempotency scope, invalid-receipt rollback, adapter durability status or ownership boundary.

### Existing persistence tests

- `ReceiptLedger` proves duplicate receipt-ID rejection and copy-safe append/read behaviour only.
- `ExecutionRecordsRepository` proves copy-safe insertion order only.
- Capital and position repositories are independent process-memory stores and do not atomically bind state to receipts.

## MLC-D — Test disposition

| Proof surface | Disposition | Reason |
|---|---|---|
| New M13 module-local test family | `CANDIDATE_TIER_A_PENDING_MLC_V` | Targets accepted owner and full bounded proposition; blocking authority requires independent acceptance |
| Historical three C-024 nodes | `NON_AUTHORITATIVE_OBSERVATIONAL` for current M13 | Correct partial intent, stale target path and incomplete proof |
| Existing persistence repository tests | `LEGACY_SHADOW_UNADMITTED` for M13 | Useful local seam proof, not transaction-authority proof |
| Tier B checkpoint receipt | `NON_AUTHORITATIVE_OBSERVATIONAL` | Receipt detachment only; no transaction state |

## MLC-P — Accepted proof specification

The current M13 proof must establish:

1. the accepted public seam exports `UnitOfWork`, `IdempotencyKey`, `AtomicReceipt` and `RepositoryPort`, plus a typed command, in-memory adapter and bounded conflict errors;
2. the in-memory adapter is explicitly labelled `non_durable_in_memory`;
3. success atomically binds command identity, scoped idempotency key, semantic input fingerprint, policy version, result identity, prior/resulting state versions, committed sequence and receipt;
4. exact duplicate replay invokes no mutation and preserves original result/receipt identity and sequence;
5. same scoped key with different input, command identity or policy version fails without state or receipt change;
6. the same raw key value is independent across command type/consistency-unit scope;
7. stale expected state version fails before mutation and emits no receipt;
8. mutation failure rolls back state, version and success receipt;
9. invalid receipt/result material after a state mutation also rolls back the working state;
10. state and receipt readbacks are detached copies;
11. no proof or API claims production durability, restart recovery, external-effect reconciliation or domain-state ownership.

## MLC-T — Test implementation

Target file: `tests/tier_a/persistence/test_m13_state_kernel_contract.py`.

The historical C-024 file is not edited. The new family is registered as a Tier A candidate through the retained-test registry and a dedicated proof block. It does not become blocking authority until independent `MLC-V` acceptance.

## MLC-V — Proof validation and acceptance boundary

### Mechanical and semantic falsification result

| Check | Result | Evidence |
|---|---|---|
| Current repository targeted proof | EXPECTED RED — 9 failed because `nvda_desk.m13_state_kernel` is absent | `raw_validation/current_repository_expected_red.txt` |
| Isolated conforming reference outside repository | PASS — 9 passed | `raw_validation/reference_conforming.txt` |
| Non-durable labelling mutant | REJECTED | `raw_validation/mutant_durable_label.txt` |
| Duplicate-reexecutes-mutation mutant | REJECTED | `raw_validation/mutant_duplicate_reexec.txt` |
| Raw-key-only scoping mutant | REJECTED | `raw_validation/mutant_scope_value_only.txt` |
| Stale-version-ignored mutant | REJECTED | `raw_validation/mutant_ignore_version.txt` |
| Commit-on-exception mutant | REJECTED | `raw_validation/mutant_commit_on_exception.txt` |
| Invalid-receipt-accepted mutant | REJECTED | `raw_validation/mutant_accept_invalid_receipt.txt` |
| Proof-block structure | PASS — 52 blocks | `raw_validation/supporting_validation.txt` |
| Proof-executor contract | PASS — 21 passed | `raw_validation/supporting_validation.txt` |
| Retained registry and M13 vocabulary records | PASS — 121 Tier A files; 130 vocabulary records | `raw_validation/supporting_validation.txt` |
| Vocabulary schema | PASS — 2 passed | `raw_validation/supporting_validation.txt` |
| Vocabulary builder stability | PASS — deterministic SHA-256 `5279f27963f2745915e11381fbc6b81c128a228563400ad9a6623ab9b5f4fe95` | `raw_validation/vocabulary_after.sha256` |
| Vocabulary builder parity node | INHERITED RED — same `Serial Desk-Cognition` heading failure at baseline `b153cd1` and current branch | current and baseline parity outputs |
| Existing persistence shadow | PASS — 16 passed | `raw_validation/supporting_validation.txt` |
| Tier B checkpoint shadow | PASS — 2 passed | `raw_validation/supporting_validation.txt` |
| New test syntax | PASS — `compileall` | `raw_validation/supporting_validation.txt` |
| Production source mutation | NONE | Git changed-path validation |

The external reference and six mutation variants are proof-strength evidence only. They are stored under `raw_validation/` and are not production implementation, test fixtures or authority sources.

### Independence constraint

The same Project Manager execution pass authored the accepted proof specification and the test file. Section `MLC-V` of the governing protocol states that the test author cannot provide final acceptance. Mechanical reference and mutation validation cannot silently waive that role-separation rule.

### Gate result

`CLOSED:MLC-V_INDEPENDENT_PM_ACCEPTANCE_REQUIRED`

Known true:

- normative and vocabulary authority is sufficient;
- the current public target and proof obligations are explicit;
- the test is expected-red for the truthful missing-package reason;
- a conforming isolated implementation satisfies all nine tests;
- six material false-positive variants are rejected;
- no production source has changed.

Not yet accepted:

- final independent Project Manager determination that this test family exactly matches the accepted proof specification and is sufficient to issue `IMPLEMENTATION_OPEN`.

`M13-IMPLEMENT` remains closed. The next lawful leaf is an independent read-only acceptance of this frozen proof record and test file.
