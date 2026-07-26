# M13 State Kernel — Module-local Proof Record

## Status

`M13_PROOF_REPAIR_V4_REJECTED_MUTATION_FAILURE_BINDING_GAP`

- Module: `M13 state_kernel`
- Reviewed worker branch: `proof/m13-state-kernel-repair-v4` at `31e8ac38488466d1d457f98ffe014576423a5ebf`
- Independent PM V4 review branch: `review/m13-proof-v4`; reviewed source commit `6ef6e448e28cd96138c0aaeb3d8f8334cad55eb1`; source archive SHA-256 `4d41c7460690de774a61757d98d2907ac1df26a8fe0cbc3255b79ff89011a113`
- Independent PM V3 review branch: `review/m13-proof-v3`; reviewed source commit `e59b8bdfb5d1e34944aa1b661643c8e6570b940c`; source archive SHA-256 `e644bd06430449efa8f8277f4ecf222f43dbc93bd8766cbd61f86a6b5d961b9a`
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
- Production source: closed; V3 worker repair changes one candidate test plus worker proof/validation evidence only

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

## MLC-V — Independent Project Manager V3 decision

### Disposition

`CLOSED:the twelve-test suite does not prove rollback and clean retry for an earlier successfully prepared participant when a later RepositoryPort fails during prepare; a coordinator that rolls back only the participant that raises passes all twelve tests while leaving stale pending state in the earlier participant and poisoning the identical retry`

### Independent falsification

The V2 test exercises one participant that establishes pending state and raises during `prepare()`. It correctly requires rollback of that failing participant. It does not execute the adjacent ordering case required by proof-specification item 13:

```text
participant A prepares successfully and retains pending state
→ participant B establishes pending state and raises during prepare
→ coordinator rolls back B only
→ A remains pending
→ identical retry reaches A and fails on stale pending state
```

A retained mutant preserves conforming behaviour for commit failures and for a single participant that fails during `prepare()`, but on a prepare-phase exception it rolls back only the participant currently raising. The complete twelve-test family passes that mutant:

```text
12 passed
```

The two-participant direct probe observes:

```text
attempt_1=failed:second: participant prepare failed
first_pending_after_attempt_1={'command_id': 'command-1', 'state': {'count': 1}, 'sequence': 1}
first_rollback_calls_after_attempt_1=0
second_pending_after_attempt_1=None
second_rollback_calls_after_attempt_1=1
attempt_2=failed:first: stale pending transaction survived failed prepare
first_prepare_calls=2
first_commit_calls=0
first_rollback_calls=1
second_prepare_calls=1
second_commit_calls=0
second_rollback_calls=1
state_version=0
state={'count': 0}
receipts=()
M13_PRIOR_PREPARED_PARTICIPANT_FALSE_POSITIVE_REPRODUCED
```

The first participant's single rollback occurs only during the poisoned retry, not during the original later-participant failure. No internal state or receipt is committed, so the existing internal assertions remain green.

Evidence:

- `raw_validation/mutant_rollback_only_failing_prepare_participant_source.py`
- `raw_validation/prior_prepared_participant_direct_probe.py`
- `raw_validation/pm_v3_independent_precommit_validation.txt`
- `raw_validation/pm_v3_independent_precommit_validation.exit_code`

### Authority and proof assessment

- N-06 requires all declared state changes and transaction participation to be atomically resolved and failed mandatory participation to leave no truth presented as committed or pending transaction contamination.
- MLC-P item 13 explicitly requires every prepared participant to be rolled back when any repository participant fails.
- The twelve existing tests are lawful and necessary for their exercised behaviours, including rollback of the participant that itself raises during `prepare()`.
- They are not collectively sufficient because they never combine an earlier successfully prepared participant with a later prepare-phase failure.
- The defect is material: stale transaction-local state in the earlier participant poisons the identical retry and prevents the required sequence/version-1 commit.
- The missing proof can be expressed entirely through the accepted public `RepositoryPort.prepare/commit/rollback` seam; no implementation leakage or normative change is required.

### Return gate

`M13-IMPLEMENT` remains closed. The next lawful unit is bounded `M13-PROOF-REPAIR-V3` only:

1. preserve all twelve existing test functions and semantics;
2. use at least two declared participants;
3. make the first participant prepare successfully and retain observable pending state;
4. make a later participant establish pending state and raise during `prepare()`;
5. require rollback/cleanup of the failing participant and every previously prepared participant;
6. require no pending or participant-visible committed truth, no internal state/version/sequence/idempotency binding and no success receipt; and
7. require the identical retry to commit as sequence/version `1` with exactly one success receipt, rejecting the retained rollback-only-current-participant mutant for this intended reason.

No production source, normative meaning, test semantics, proof configuration or later module is opened by this decision.

## M13-PROOF-REPAIR-V3 worker proposal — awaiting independent Project Manager review

### Proposed bounded repair

The worker preserved all twelve existing M13 test functions byte-for-byte at function-source level and appended one test:

- `test_m13_later_prepare_failure_rolls_back_every_prepared_participant_and_allows_clean_retry`

The new proof uses two declared `RepositoryPort` participants. Participant A prepares successfully and holds observable pending state. Participant B also establishes pending state, then raises during `prepare()`. The test requires mandatory rollback or equivalent cleanup for both B and every earlier prepared participant, no participant pending or visible committed state, unchanged internal state/version/receipt truth, and an uncontaminated identical retry that commits once as sequence/version `1` with exactly one matching success receipt.

### Worker validation result

- Target retained mutant with original twelve tests: `12 passed`.
- Target retained mutant with repaired thirteen-test family: rejected because participant A has `rollback_calls == 0` after participant B fails during prepare.
- Conforming reference with repaired family: `13 passed`.
- Every previously retained mutant: rejected by the repaired family.
- Production source, normative documents and proof/retained-test configuration: unchanged.

Evidence is recorded under `raw_validation/v3_*`, including the full-read manifest, original-twelve preservation report, target-mutant outputs, conforming-reference output, retained-mutant matrix and worker validation summary.

This is a proposed proof repair only. `M13-IMPLEMENT` remains closed. No acceptance, `IMPLEMENTATION_OPEN`, or later-module claim is made.

## MLC-V — Independent Project Manager V4 decision

### Source verification

- Supplied archive SHA-256: `4d41c7460690de774a61757d98d2907ac1df26a8fe0cbc3255b79ff89011a113`.
- Source branch/commit/worktree: `proof/m13-state-kernel-repair-v3` / `6ef6e448e28cd96138c0aaeb3d8f8334cad55eb1` / clean.
- The twelve PM V3 source test functions are unchanged and exactly one V3 function is appended.
- Frozen thirteen-test SHA-256: `9bca3237bd24e905ce8772d9360f56bb824fa36eb46c4c9e2d82d581e0744374`.

### Disposition

`CLOSED:the thirteen-test suite does not prove that a failed transaction leaves no idempotency binding; an implementation that reserves the scoped key and failed input after rollback passes all thirteen tests, permits exact retry, but falsely rejects a different uncommitted input using that key`

### Independent falsification

The retained false-positive implementation restores state, version, receipt and participant truth after failure, but writes a separate failed-attempt reservation keyed by the same `(command_type, consistency_unit_id, key value)` scope. It permits the exact failed input to execute again, so every existing clean-retry assertion remains green. It rejects a different input using that uncommitted key as an idempotency conflict.

The complete thirteen-test family passes this implementation:

```text
13 passed
```

The public-seam probe observes:

```text
attempt_1=failed:prepare failed
after_failure_rollback_calls=1
after_failure_pending=None
after_failure_state_version=0
after_failure_receipts=()
different_input_retry=failed:IdempotencyConflictError:failed attempt reserved idempotency key
final_state_version=0
final_state={'count': 0}
final_receipts=()
```

The same probe against the conforming reference commits the different input as fresh truth:

```text
different_input_retry=committed:sequence=1:command_id=command-2
final_state_version=1
final_state={'count': 1}
```

Evidence:

- `raw_validation/pm_v4_mutant_failed_attempt_reserves_idempotency_source.py`
- `raw_validation/pm_v4_failed_attempt_binding_probe.py`
- `raw_validation/pm_v4_failed_binding_mutant_full.txt`
- `raw_validation/pm_v4_failed_binding_mutant_probe.txt`
- `raw_validation/pm_v4_failed_binding_reference_probe.txt`
- `raw_validation/pm_v4_independent_precommit_validation.txt`

### Authority and proof assessment

- N-06 requires the scoped idempotency key to be atomically bound to semantic input, committed result, resulting state version/sequence and receipt. No successful commit means no committed binding.
- MLC-P items 12 and 13 explicitly require failed participant/receipt paths to leave idempotency binding uncommitted; item 14 requires uncontaminated retry and no hidden sequence consumption.
- The worker's V3 test is lawful and necessary. It closes the prior defect by proving rollback of the later failing participant and the earlier prepared participant.
- The thirteen tests prove exact retry executes again as sequence `1`, but they do not prove the key is unbound for another uncommitted input. A conflict-only failed reservation is therefore invisible to the family.
- The defect is observable entirely through the accepted `UnitOfWork.execute` public seam and does not require implementation inspection, normative change or production code.

### Return gate

`M13-IMPLEMENT` remains closed. The next lawful unit is bounded `M13-PROOF-REPAIR-V4` only:

1. preserve all thirteen existing test functions and semantics;
2. create one transaction failure that rolls back with no committed state, version, sequence, receipt or participant truth;
3. submit a second `TransactionCommand` using the same scoped `IdempotencyKey` with a different semantic input and command identity while the expected version remains `0`;
4. require that second command to execute as a fresh transaction and commit as sequence/version `1` with exactly one success receipt;
5. require exact replay of the second committed command to return its original receipt without repeating mutation; and
6. reject the retained failed-attempt idempotency-reservation mutant for this intended reason.

No production source, normative meaning, existing test semantics, proof configuration or later module is opened by this decision.


## M13-PROOF-REPAIR-V4 worker proposal

**Disposition:** `PROPOSED_REPAIR_AWAITING_INDEPENDENT_PROJECT_MANAGER_REVIEW`

The independent Project Manager V4 `CLOSED` decision remains preserved. Production implementation and `IMPLEMENTATION_OPEN` remain closed.

The worker preserved all thirteen existing test functions and added one public-`UnitOfWork.execute` proof that a failed repository-participant transaction creates no idempotency binding. The proof reuses the same scoped key with a different command identity and semantic fingerprint at expected version 0, requires a fresh sequence/version-1 commit with exactly one success receipt, and requires exact replay to return that receipt without repeating mutation.

Evidence:

- `raw_validation/v4_original_thirteen_preservation.txt`: thirteen pre-existing test ASTs unchanged; one test added.
- `raw_validation/v4_target_mutant_original_thirteen.txt`: failed-attempt reservation mutant passes 13/13 with the new test deselected.
- `raw_validation/v4_target_mutant_repaired_family.txt`: the same mutant fails the new test at the intended false idempotency-conflict boundary.
- `raw_validation/v4_reference_conforming.txt`: conforming reference passes 14/14.
- `raw_validation/v4_retained_mutants_summary.tsv`: every previously retained mutant remains rejected.
- `raw_validation/v4_current_repository_expected_red.txt`: absent production implementation remains expected-red, 14 failed.
- `raw_validation/v4_supporting_validation.txt`: proof-block, proof-executor, checkpoint, YAML, syntax and diff validation passed.

No `src/**`, normative document, proof-block configuration, retained-test configuration, acceptance status or implementation gate was changed.

## MLC-V — Independent Project Manager V5 decision

### Source verification

- Supplied archive SHA-256: `83e1f2bfee1b0665b190383567436c6797e20907481b05091152426a72907d31`.
- Source branch/commit/worktree: `proof/m13-state-kernel-repair-v4` / `31e8ac38488466d1d457f98ffe014576423a5ebf` / clean.
- Source parent: PM V4 closure `41007ee74562b09619be9b71ef0a0c40fde16dd3`.
- All thirteen source-checkpoint test functions are unchanged and exactly one V4 function is appended.
- Frozen fourteen-test SHA-256: `c1bc90aedf2905989c22f851f2560969868e87e50bca3f352f6bc91b91200cca`.

### Disposition

`CLOSED:the fourteen-test suite proves no failed idempotency binding only for repository-participant failure; an implementation that reserves the scoped key only when the mutation raises passes all fourteen tests, leaves state/version/receipts uncommitted, but falsely rejects a different uncommitted input using that key`

### Independent falsification

The retained PM V4 mutant is correctly rejected by the new V4 test. The conforming reference passes 14/14 and all previously retained mutants remain rejected.

An independent adjacent mutant preserves the conforming participant, receipt and successful-commit paths but writes a failed-attempt reservation only when the owner mutation raises. The complete fourteen-test family passes this implementation:

```text
14 passed
```

The public-seam probe observes:

```text
attempt_1=failed:RuntimeError:mutation failed
after_failure_state_version=0
after_failure_state={'count': 0}
after_failure_receipts=()
different_input_retry=failed:IdempotencyConflictError:mutation failure reserved idempotency key
final_state_version=0
final_state={'count': 0}
final_receipts=()
```

The same probe against the conforming reference commits the different input as fresh truth:

```text
different_input_retry=committed:sequence=1:command_id=command-2
final_state_version=1
final_state={'count': 1}
```

A second adjacent mutant demonstrates that the V4 test also changes command ID and fingerprint together, so it cannot prove that each identity component is unbound independently. The mutant retains a failed participant-path binding keyed to the command identity only and passes all fourteen tests:

```text
14 passed
```

When the failed command is corrected by changing only its semantic fingerprint while preserving command ID, policy version, scoped key and expected version `0`, the mutant falsely rejects it while the conforming reference commits sequence `1`:

```text
attempt_1=failed:RuntimeError:prepare failed
corrected_same_command_id=failed:IdempotencyConflictError:failed attempt reserved command identity
state_version=0
receipts=()
```

Evidence:

- `raw_validation/pm_v5_mutant_mutation_failure_reserves_idempotency_source.py`
- `raw_validation/pm_v5_mutation_failure_binding_probe.py`
- `raw_validation/pm_v5_mutation_failure_mutant_full.txt`
- `raw_validation/pm_v5_mutation_failure_mutant_probe.txt`
- `raw_validation/pm_v5_mutation_failure_reference_probe.txt`
- `raw_validation/pm_v5_mutant_failed_binding_command_id_only_source.py`
- `raw_validation/pm_v5_command_identity_binding_probe.py`
- `raw_validation/pm_v5_command_identity_mutant_full.txt`
- `raw_validation/pm_v5_command_identity_mutant_probe.txt`
- `raw_validation/pm_v5_command_identity_reference_probe.txt`
- `raw_validation/pm_v5_independent_validation_summary.txt`
- `raw_validation/pm_v5_postedit_validation_summary.txt`
- `raw_validation/pm_v5_postedit_runs/`
- `raw_validation/pm_v5_full_read_manifest.tsv`

### Authority and proof assessment

- N-06 binds the scoped idempotency key atomically to semantic input, committed result, resulting state version/sequence and receipt. A mutation exception produces none of those committed facts and therefore cannot lawfully reserve the key.
- MLC-A expressly states that validation, expected-version, mutation, repository-participation and receipt-write failures leave no idempotency binding.
- The worker's V4 test is lawful and necessary. It closes the PM V4 participant-prepare false positive.
- The fourteen-test family is not collectively sufficient because the new fresh-reuse assertion is attached only to participant failure. The existing mutation-failure test observes state/version/receipt rollback but never reuses the uncommitted scoped key with a different input.
- The defects are observable entirely through `UnitOfWork.execute`; no private implementation state, normative change or production code is required.
- The V4 fresh-reuse test changes command ID and fingerprint simultaneously. It therefore does not establish that a failed attempt leaves each admitted identity dimension independently unbound.

### Return gate

`M13-IMPLEMENT` remains closed. The next lawful unit is bounded `M13-PROOF-REPAIR-V5` only:

1. preserve all fourteen existing test functions and semantics;
2. add a bounded public-seam failure/binding matrix covering stale expected-version rejection, mutation exception, invalid `receipt_id`, invalid `result_id`, participant `prepare()` failure, participant `commit()` failure and attesting-receipt writer failure;
3. after each failed attempt, require a corrected fresh command using the same scoped key and expected version `0` to commit as sequence/version `1` with exactly one receipt;
4. vary command ID, semantic fingerprint and policy version independently, so no hidden failed binding can survive behind a combined identity change;
5. retain exact replay of each first successful corrected command without repeated mutation; and
6. reject both retained PM V5 mutants for their intended false-conflict reasons: mutation-failure reservation and failed-binding-by-command-identity.

No production source, normative meaning, existing test semantics, proof configuration or later module is opened by this decision.

## M13-PROOF-REPAIR-V5 worker proposal

**Worker result:** `PROPOSED_REPAIR_AWAITING_INDEPENDENT_PROJECT_MANAGER_REVIEW`

The authoritative Project Manager V5 `CLOSED` disposition above is preserved without
replacement or reinterpretation. This worker section is a bounded repair proposal only.
`M13-IMPLEMENT`, `IMPLEMENTATION_OPEN`, final Project Manager acceptance, M01 and every
later module remain closed.

### Source and preservation boundary

- Sole source checkpoint: `NVDA_M13_PM_V5_CLOSED_479000b_20260726.tar.gz`.
- Verified source archive SHA-256:
  `a56a1097bad88c21f4d2d91196961c947b849d76f66d50fa273cb4a507446572`.
- Verified source branch/commit:
  `review/m13-proof-v5` /
  `479000b512ef74b8134bc11cefc7a3ef13fac0e1`.
- Verified source worktree: clean; complete `.git` history present; `git fsck --full
  --no-dangling` clean; 190 reachable commits.
- Frozen fourteen-test SHA-256:
  `c1bc90aedf2905989c22f851f2560969868e87e50bca3f352f6bc91b91200cca`.
- Worker branch: `proof/m13-state-kernel-repair-v5`.
- All fourteen frozen test-function ASTs and names remain unchanged. One parameterised
  test function was appended, producing 32 individually named semantic matrix cases and
  46 collected semantic test items in total.
- Preservation evidence:
  `raw_validation/v5_worker_runs/fourteen_preservation.txt`.

### Failure/binding matrix and N-06 mapping

The complete auditable mapping is retained in
`raw_validation/v5_failure_binding_matrix.tsv`. The matrix crosses eight independently
admitted unsuccessful boundaries with four binding-comparison dimensions:

| ID | Intended public-seam failure boundary | Participant-observable reach |
|---|---|---|
| `FB-01` | stale expected-state-version rejection | mutation and participants not reached |
| `FB-02` | owner mutation exception | working-state mutation reached; participants not reached |
| `FB-03` | mutation result is not a mapping | mutation reached; receipt construction and participants not reached |
| `FB-04` | invalid or empty `receipt_id` | mutation reached; participants not reached |
| `FB-05` | invalid or empty `result_id` | mutation reached; participants not reached |
| `FB-06` | repository-participant `prepare()` failure | earlier participant prepared; failing participant pending; writer not prepared |
| `FB-07` | repository-participant `commit()` failure | all prepared; earlier commit and failing commit reached; writer not committed |
| `FB-08` | attesting-receipt writer failure | all prepared; state participants and failing writer commit reached |

For every boundary the matrix independently uses:

1. same command ID with a different semantic input fingerprint;
2. different command ID with the same semantic input fingerprint;
3. same command ID and fingerprint with a different policy version; and
4. complete command identity unchanged, with the stale case correcting only expected
   state version from the rejected value to actual version `0`.

Every case preserves the same scoped `IdempotencyKey`, command type and consistency-unit
ID. The failed attempt is asserted to leave state version `0`, state `{"count": 0}`, no
receipt/sequence, no participant-visible truth and no participant pending state. Earlier
prepared, failing, not-yet-committed and attesting-writer participants are all observed.

The corrected command then uses actual version `0` through the same `UnitOfWork.execute`
seam. A fresh sequence `1` / resulting-version `1` commit, one receipt, one successful
mutation and participant truth containing only the corrected transaction prove that no
failed-attempt binding remains. Exact replay returns the original receipt without any
additional mutation, prepare, commit, version, sequence, receipt or participant truth.

This maps directly to N-06: a scoped idempotency key is bound only atomically with a
committed semantic input, committed result, resulting state version, sequence and
attesting receipt. Each matrix failure lacks that tuple, so both transaction truth and
the binding must remain absent.

### Falsification

- Conforming reference:
  `raw_validation/v5_worker_runs/conforming_repaired_family.txt` records 46/46 passing,
  including every parameter ID in verbose pytest output.
- PM V5 mutation-exception reservation:
  `raw_validation/v5_worker_runs/pm_v5_mutation_failure_old_fourteen.txt` records the
  frozen family false positive at 14/14; the complete repaired family records 3 intended
  failures; the single intended case records rejection when a same-command-ID corrected
  fingerprint is falsely conflicted.
- PM V5 command-ID-only failed binding:
  `raw_validation/v5_worker_runs/pm_v5_command_identity_old_fourteen.txt` records the
  frozen family false positive at 14/14; the complete repaired family records 6 intended
  failures; the single intended prepare/fingerprint case records the false conflict.
- Additional configurable mutation source:
  `raw_validation/v5_configurable_failed_binding_mutant_source.py`.
- Additional mutation matrix:
  `raw_validation/v5_worker_runs/additional_mutants/summary.tsv` records 32/32 intended
  rejections, crossing all eight reservation boundaries with comparison by command ID,
  semantic input fingerprint, policy version and complete command identity. Every
  variant has its own raw command, output and exit-code sidecar.
- Earlier retained mutants:
  `raw_validation/v5_worker_runs/earlier_mutants/summary.tsv` records 11/11 rejection.
  Each mutant has both a full-family output and a single preserved-test output proving
  the intended defect rather than an interface or fixture mismatch.

### Repository-state and authority boundary

- Current production remains expected-red because
  `nvda_desk.m13_state_kernel` is absent; the repaired family collects correctly and
  fails 46 items for that missing production seam.
- No `src/**` file is added or changed.
- No numbered normative document is changed.
- `config/proof_blocks.yaml` and `config/retained_test_registry.yaml` are unchanged.
- No frozen test function is renamed, removed, weakened or semantically reordered.
- The only proof change is the appended V5 matrix plus worker-owned M13 proof and raw
  validation evidence.

The final Git commit, tracked evidence hashes, validation outputs and Git-preserving
checkpoint are closeout evidence reported externally after the committed bytes exist;
they cannot be self-recorded in those bytes without recursively changing the commit or
archive identifier.
