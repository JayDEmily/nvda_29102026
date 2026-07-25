# M13 State Kernel — Module-local Proof Record

## Status

`M13_PROOF_REPAIR_V2_PROPOSED_PENDING_INDEPENDENT_REVIEW`

- Module: `M13 state_kernel`
- Current worker branch: `proof/m13-state-kernel-repair-v2`
- Current V2 source checkpoint: `recovery/m13-pm-v2-closed` at `4d50939f308598efcb668487e2105f038a1fefd7`; source archive SHA-256 `772e328d37df00e123a7cfd2569e285b47b188a9d3bf70a06e5a1b6689352a6b`
- V2 proof-repair commit: `7b3b04c4647ee13674e46c55227b5352cb8c8361`
- Reviewed worker repair branch: `proof/m13-state-kernel-repair`
- Accepted control baseline: local `main` at `b153cd1e3e0808991dcf9c188e380d935cfd9283`
- Worker source checkpoint: `proof/m13-state-kernel` at `4a259217f0ea5c841e514848523b7bd0c496e41f`
- Proof-repair commit: `2dd25e3bdf5759fcaa2320cfd5bba988f9908eee`
- Reviewed evidence commit: `490e63ed3c96da90a81239326e2d33dd77bdbf36`
- Historical requirement: `C-024`
- Historical obligation: `D-054`
- Governing protocol: `project_control/canonical_project_manager/GATE_C_COMPLETION_PROTOCOL.md`
- Production source: closed; V2 worker repair changes one candidate test plus worker proof/validation evidence only

## Provenance boundary

The independent Project Manager rejected the original nine-test family and returned the gate to `MLC-P → MLC-T`. The user supplied the exact Project Manager disposition, reported decision commit `50d82f2bed689fc72afcbf8250f9625f9908f1f3`, reported checkpoint SHA-256 `5c52aabc7d22a75e51e87a60d86ecd4d7c28c1bdba96e7ec79ec2a314a59214f`, reproduction output and return instruction in the worker thread.

The Project Manager archive itself was not available to this worker's active filesystem. This repair therefore descends from the original worker checkpoint `4a259217...` and incorporates the user-supplied Project Manager decision as authoritative return-gate evidence. The captured evidence is preserved at:

- `raw_validation/independent_pm_rejection_user_supplied.txt`
- `raw_validation/pm_false_positive_reproduction_summary.txt`

No claim is made that this branch is a Git descendant of the reported Project Manager decision commit.

## Independent Project Manager return gate

### Disposition

`CLOSED:the frozen suite does not prove rollback when the attesting receipt write fails; a commit-before-receipt implementation passes all nine tests while leaving committed state with no receipt`

### Reproduced defect

The original nine tests allowed this unlawful sequence:

```text
publish state/version/idempotency truth
→ attempt attesting receipt/repository commit
→ receipt/repository commit fails
→ leave state visible without its attesting receipt
```

The retained commit-before-receipt mutant passes the original nine tests:

```text
9 passed, 2 repaired tests deselected
```

The repaired eleven-test family rejects that same mutant with two failures. Evidence:

- `raw_validation/mutant_commit_before_receipt_original_nine.txt`
- `raw_validation/mutant_commit_before_receipt.txt`

## MLC-A — Authority sufficiency

**Result:** `AUTHORITY_SUFFICIENT_UNCHANGED`

`docs/07.2_STATE_RISK_AND_REPLAY_WORKING.md:17-76` admits the smallest owner-declared transaction boundary:

- one accepted domain command/decision and every mutation plus attesting receipt required for one named consistency unit;
- declared repository participants and invariants;
- atomic visibility of every declared state mutation and the success receipt;
- no committed state, version, sequence, idempotency binding or success receipt when validation, expected-version check, mutation, repository participation or receipt write fails;
- idempotency scoped to command type and consistency unit and bound to semantic input fingerprint, command/result identity, state version/sequence and receipt;
- exact duplicate replay returns the original committed result without repeating mutation;
- conflicting reuse fails;
- repository interfaces expose transaction participation, expected-version and idempotent-commit semantics;
- memory proof is explicitly non-durable and does not prove restart recovery or external-effect reconciliation.

### Accepted owner and surface

- Owner: `M13 state_kernel`.
- Architecture surface: `5.16 Persistence ledgers and receipts`.
- M13 owns transaction mechanics, idempotency binding, atomic receipts and storage ports.
- Domain modules retain semantic ownership of positions, capital, calendar facts, risk observations and other records.

### Bounded alpha transformation

```text
TransactionCommand + owner-declared mutation + declared RepositoryPort participants
→ validate scoped idempotency and expected state version
→ execute against an isolated working copy
→ prepare declared participants
→ commit all participants and internal state/receipt truth as one consistency unit
→ on any participant or receipt failure, roll back every visible change
→ return committed AtomicReceipt or exact duplicate replay response
```

### Identity, state and side effects

- Required identity: command ID; command type; consistency-unit ID; idempotency-key value; input semantic fingerprint; policy/config version; result ID; receipt ID.
- Required state truth: expected prior version; resulting version; deterministic committed sequence.
- State ownership: M13 owns only the transaction journal/mechanism. Test state is synthetic and has no trading-domain meaning.
- Repository participation: `RepositoryPort` exposes an executable transaction-participant seam. The proof exercises preparation, commit failure and rollback; type existence alone is insufficient.
- Time: no wall-clock value is required for deterministic transaction equivalence in this alpha slice.
- Side effects: none outside the in-memory boundary. External irreversible effects, outbox protocols and durable recovery remain excluded.

### Prohibited authority

M13 must not:

- own domain-record meaning;
- create one repository-wide global transaction;
- treat a duplicate receipt ID as complete idempotency;
- publish state/version/sequence/idempotency truth before all declared participants and the attesting receipt can commit;
- omit participant rollback after a failed repository or receipt write;
- claim production durability, crash atomicity, restart recovery or external-effect completion;
- fabricate domain identities, policy decisions or business results;
- import unopened domain modules to obtain semantic authority.

## MLC-R — Relevant-test routing

### Current candidate route

- `tests/tier_a/persistence/test_m13_state_kernel_contract.py` — module-local candidate Tier A family, now twelve tests pending independent review.

### Historical tests

The three historical `C-024` nodes in `test_gate_c_normative_completion_contracts.py` remain expected-red historical evidence but are `NON_AUTHORITATIVE_OBSERVATIONAL` for the current opening decision. They target a superseded package path and do not prove expected-version rejection, deterministic sequence, scoped idempotency, participant rollback, receipt-write rollback or explicit non-durable status.

### Shadow routes

- receipt-ledger and execution-record repository tests: `LEGACY_SHADOW_UNADMITTED` for M13 transaction authority;
- Tier B checkpoint-receipt contract: observational shadow only;
- all unrelated tests: `LEGACY_SHADOW_UNADMITTED`.

## MLC-O — Factual observation

- Existing receipt, execution-record, capital-state and position stores are independent seams; they do not provide one atomic state-plus-receipt consistency unit.
- The original nine candidate tests type-checked `RepositoryPort` but never executed it.
- The original nine tests did not inject a failing receipt writer or repository participant.
- A commit-before-receipt mutant therefore passed all original nine tests while retaining state/version changes after the later participant failure.
- The two repair tests execute public transaction participants and observe both internal and participant-visible truth before retrying the identical command.

## MLC-D — Test disposition

| Proof surface | Disposition | Reason |
|---|---|---|
| Repaired eleven-test M13 family | `CANDIDATE_TIER_A_PENDING_INDEPENDENT_MLC-V` | Targets the accepted owner and closes the Project Manager's atomicity false positive; final authority still requires independent acceptance |
| Original nine behaviours | `PRESERVED_UNCHANGED` | Lawful partial proof; retained exactly and still reject their original six mutants |
| Two participant/receipt-failure behaviours | `CANDIDATE_REPAIR_PENDING_INDEPENDENT_MLC-V` | Exercise the missing public participant and rollback boundary |
| Historical three C-024 nodes | `NON_AUTHORITATIVE_OBSERVATIONAL` | Correct partial intent, stale target path and incomplete proof |
| Existing repository tests | `LEGACY_SHADOW_UNADMITTED` for M13 | Local seam proof, not transaction-authority proof |
| Tier B checkpoint receipt | `NON_AUTHORITATIVE_OBSERVATIONAL` | Receipt detachment only; no transaction state |

## MLC-P — Repaired proof specification

The M13 proof must establish:

1. the accepted public seam exports `UnitOfWork`, `IdempotencyKey`, `AtomicReceipt` and `RepositoryPort`, plus a typed command, in-memory adapter and bounded conflict errors;
2. the in-memory adapter is explicitly labelled `non_durable_in_memory`;
3. success binds command identity, scoped idempotency key, semantic input fingerprint, policy version, result identity, prior/resulting state versions, committed sequence and receipt;
4. exact duplicate replay invokes no mutation and preserves original result/receipt identity and sequence;
5. same scoped key with different input, command identity or policy version fails without state or receipt change;
6. the same raw key value is independent across command type/consistency-unit scope;
7. stale expected state version fails before mutation and emits no receipt;
8. mutation failure rolls back state, version and success receipt;
9. invalid receipt/result material after mutation also rolls back working state;
10. state and receipt readbacks are detached copies;
11. `RepositoryPort` provides an executable transaction-participant seam rather than a type-only marker;
12. when an attesting receipt writer fails after another participant has made a change visible, rollback restores participant-visible state and leaves internal state, state version, sequence, idempotency binding and success receipt uncommitted;
13. when any repository participant fails, every prepared participant is rolled back and no internal truth is committed;
14. after either failure, exact retry of the same command executes again and commits as sequence `1`, proving no hidden idempotency or sequence consumption;
15. no proof or API claims production durability, restart recovery, external-effect reconciliation or domain-state ownership.

The public participant proof uses the minimal `prepare(...)`, `commit()` and `rollback()` transaction-participation shape. This establishes required behaviour, not storage technology or production durability.

## MLC-T — Test implementation

Target file: `tests/tier_a/persistence/test_m13_state_kernel_contract.py`.

- The original nine test functions and assertions remain unchanged.
- Two tests were appended:
  - `test_m13_receipt_write_failure_rolls_back_every_visible_change_and_allows_clean_retry`
  - `test_m13_repository_participant_failure_rolls_back_participant_and_internal_truth`
- The historical C-024 file remains unchanged.
- Production `src/**` remains unchanged.
- The proof block command already targets the complete file and required no command change.

Candidate test SHA-256 after repair:

`f66b8cbe60a70c9dca02b2a65c6f6770273a1be213d5c203cb9fa29dd545d9ee`

## MLC-V — Worker falsification and independent acceptance boundary

### Mechanical falsification result

| Check | Result | Evidence |
|---|---|---|
| Current repository targeted proof | EXPECTED RED — 11 failed solely because `nvda_desk.m13_state_kernel` is absent | `raw_validation/current_repository_expected_red.txt` |
| Isolated conforming reference | PASS — 11 passed | `raw_validation/reference_conforming.txt` |
| Original nine against PM commit-before-receipt mutant | FALSE POSITIVE REPRODUCED — 9 passed | `raw_validation/mutant_commit_before_receipt_original_nine.txt` |
| Repaired family against PM commit-before-receipt mutant | REJECTED — 2 failed, 9 passed | `raw_validation/mutant_commit_before_receipt.txt` |
| No-participant-rollback mutant | REJECTED — 2 failed, 9 passed | `raw_validation/mutant_no_participant_rollback.txt` |
| Original non-durable labelling mutant | REJECTED by preserved original behaviour | `raw_validation/mutant_durable_label_original_nine.txt` |
| Original duplicate-reexecution mutant | REJECTED by preserved original behaviour | `raw_validation/mutant_duplicate_reexec_original_nine.txt` |
| Original raw-key-only scope mutant | REJECTED by preserved original behaviour | `raw_validation/mutant_scope_value_only_original_nine.txt` |
| Original stale-version mutant | REJECTED by preserved original behaviour | `raw_validation/mutant_ignore_version_original_nine.txt` |
| Original commit-on-exception mutant | REJECTED by preserved original behaviour | `raw_validation/mutant_commit_on_exception_original_nine.txt` |
| Original invalid-receipt mutant | REJECTED by preserved original behaviour | `raw_validation/mutant_accept_invalid_receipt_original_nine.txt` |
| Production source mutation | NONE | Git changed-path validation |

The external reference and eight mutation variants are falsification evidence only. They are not production implementation, fixtures or authority sources.

### Worker gate result before independent review

`CLOSED:REPAIRED_PROOF_REQUIRES_INDEPENDENT_MLC-V_ACCEPTANCE`

Known true from worker evidence:

- N-06 and M13 ownership authority remain sufficient;
- the Project Manager's original false-positive mutant still passes the original nine tests;
- the two repaired tests reject that mutant and independently reject omitted participant rollback;
- a conforming isolated reference satisfies all eleven tests;
- the original nine behaviours remain intact and continue to reject their original six mutants;
- current production remains expected-red for the truthful absent-package reason;
- no production source changed.

Not accepted at the worker checkpoint:

- independent Project Manager determination that the repaired eleven-test family exactly and sufficiently proves the admitted public seam;
- `IMPLEMENTATION_OPEN`.

At commit `490e63e...`, `M13-IMPLEMENT` remained closed and independent `MLC-V` was next. The reconstructed independent decision below supersedes that pending-review pointer.

## MLC-V — Independent Project Manager V2 decision reconstruction

### Reconstruction provenance

The previously created PM V2 checkpoint (`review/m13-proof-v2`, reported commit `7e95102ae21d246936bcad97bf2112db9c40a96f`, reported archive SHA-256 `9d780f4455d32e0ecd49190155d9643fdb9d0615d2cc559c882194f1d15f1801`) could not be located. This decision was reconstructed independently from the sole repository input `proof/m13-state-kernel-repair` at `490e63ed3c96da90a81239326e2d33dd77bdbf36`, archive SHA-256 `6f6cd368e8be9f2b69fa7448967714e4517fa7dea3ad787072d96aa8df3b455a`.

This record does not claim to reproduce the lost commit identity or archive bytes. It reproduces the bounded decision and its executable evidence.

### Disposition

`CLOSED:the repaired suite does not prove rollback and clean retry when a RepositoryPort fails during prepare; a coordinator that registers participants for rollback only after prepare returns passes all eleven tests while leaving stale participant transaction state after the failure`

### Independent falsification

The retained mutant differs from the conforming proof reference only in participant-registration order:

```text
participant.prepare(...)
prepared.append(participant)
```

A participant that creates pending transaction state and then raises from `prepare()` is therefore absent from the rollback set. The complete frozen eleven-test family passes this implementation:

```text
11 passed
```

The direct probe then executes the identical command twice and observes:

```text
attempt_1=failed:participant prepare failed
attempt_2=failed:stale pending transaction survived failed prepare
prepare_calls=2
commit_calls=0
rollback_calls=0
pending=True
participant_visible=[]
state_version=0
state={'count': 0}
receipts=()
M13_PREPARE_FAILURE_FALSE_POSITIVE_REPRODUCED
```

Evidence:

- `raw_validation/mutant_register_after_prepare_source.py`
- `raw_validation/prepare_failure_mutant_eleven_tests.txt`
- `raw_validation/prepare_failure_mutant_eleven_tests.exit_code`
- `raw_validation/prepare_failure_direct_probe.py`
- `raw_validation/prepare_failure_direct_probe_output.txt`
- `raw_validation/prepare_failure_direct_probe.exit_code`

### Authority and proof assessment

- N-06 authority remains sufficient and unchanged: all declared changes must be atomically visible, failed mandatory participation must not leave committed truth, and repository interfaces must expose transaction participation and rollback/failure truth.
- The eleven existing tests are lawful and necessary for the behaviours they exercise.
- They are not collectively sufficient for MLC-P items 13 and 14 because both participant tests fail during `commit()`, after successful `prepare()` has completed. Neither test makes the failing participant establish pending state and raise during `prepare()`.
- The mutant leaves internal state/version/receipt truth uncommitted, so the existing internal rollback assertions remain green. The prohibited participant-local pending state is unobserved by the eleven-test family.
- The stale pending state contaminates the identical retry, which proves the missing behaviour is material rather than an internal implementation preference.
- No implementation leakage is required to close the gap: the public `RepositoryPort.prepare/commit/rollback` seam can express the required proof.

### Return gate

`M13-IMPLEMENT` remains closed. The next lawful unit is bounded `M13-PROOF-REPAIR-V2` only:

1. preserve the existing eleven test functions and semantics;
2. add one executable participant that establishes observable pending state and raises during `prepare()`;
3. require rollback/cleanup of that failing participant;
4. require no internal or participant-visible committed truth and no success receipt;
5. require an uncontaminated identical retry committing as sequence/version `1` with exactly one success receipt; and
6. reject the retained register-after-successful-prepare mutant for this intended reason.

No production source, normative meaning, later module or implementation authority is opened by this reconstructed decision.

## MLC-P/T — Worker V2 prepare-failure proof repair proposal

### Preserved Project Manager decision

The reconstructed PM V2 `CLOSED` disposition above remains authoritative. This worker section does not reverse it, accept the proof or open implementation.

### Added proof behaviour

One fixture and one test were appended at `tests/tier_a/persistence/test_m13_state_kernel_contract.py:482-579`:

- `_prepare_failure_participant` establishes observable `pending` transaction-local state inside `prepare()` and raises before `prepare()` returns;
- `test_m13_prepare_failure_rolls_back_failing_participant_and_allows_uncontaminated_retry` requires the failing participant to receive rollback/cleanup, leaves no visible or pending participant state, leaves M13 state/version/receipt truth unchanged, and reuses the identical command and mutation successfully as sequence/version `1` with exactly one receipt.

This maps directly to N-06 atomic participation and failure truth at `docs/07.2_STATE_RISK_AND_REPLAY_WORKING.md:27-68`.

### Preservation

- All eleven pre-existing test functions retain identical function-source SHA-256 values.
- Preservation evidence: `raw_validation/v2_original_eleven_preservation_base.txt` and `raw_validation/v2_original_eleven_preservation_after.txt`.
- New test-file SHA-256: `f457aaba1f90a5f40c7e43cc34dbb26dada5fcb43292661f61a7b18e345fdc5f`.
- No production source, normative document, proof block or retained-test registry entry was changed.

### Worker falsification

| Check | Result | Evidence |
|---|---|---|
| Conforming reference, complete repaired family | PASS — 12 passed | `raw_validation/v2_reference_conforming.txt` |
| Register-after-prepare mutant, old family | FALSE POSITIVE REPRODUCED — 11 passed | `raw_validation/v2_prepare_mutant_old_eleven.txt` |
| Same mutant, repaired family | REJECTED — 1 failed, 11 passed; explicit post-failure assertion observes `rollback_calls == 0` | `raw_validation/v2_prepare_mutant_repaired_family.txt` |
| Commit-before-receipt mutant | REJECTED — 3 failed, 9 passed | `raw_validation/v2_mutant_commit_before_receipt_repaired_family.txt` |
| No-participant-rollback mutant | REJECTED — 3 failed, 9 passed | `raw_validation/v2_mutant_no_participant_rollback_repaired_family.txt` |
| Original six retained mutants | Each rejected by the complete repaired family | `raw_validation/v2_mutant_*_repaired_family.txt` |
| Current repository | EXPECTED RED — 12 failed solely because `nvda_desk.m13_state_kernel` is absent | `raw_validation/v2_current_repository_expected_red.txt` |
| Direct PM V2 probe | FALSE POSITIVE REPRODUCED — zero rollback, pending retained and identical retry poisoned | `raw_validation/v2_prepare_failure_direct_probe.txt` |

### Committed-state validation

Commit `7b3b04c4647ee13674e46c55227b5352cb8c8361` was revalidated from a clean worktree. The complete conforming and falsification matrix, absent-production expected-red result, proof-block structure, proof-executor contract, persistence shadow, checkpoint shadow, immutable-path hashes and changed-path boundary all produced the expected results. Evidence: `raw_validation/v2_postcommit_validation.txt`.

### Worker disposition

`READY_FOR_INDEPENDENT_PM_REVIEW`

The twelve-test family is a proposed repair only. Final Project Manager acceptance remains pending and `M13-IMPLEMENT` remains closed.
