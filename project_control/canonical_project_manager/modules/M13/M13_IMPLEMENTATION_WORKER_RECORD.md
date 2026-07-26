# M13 State Kernel Implementation Worker Record

## Disposition

`PROPOSED_M13_IMPLEMENTATION_AWAITING_INDEPENDENT_PROJECT_MANAGER_REVIEW`

This record is an implementation-worker proposal. It does not issue M13
acceptance, Gate C completion, durability, restart recovery, crash recovery,
multi-process safety, external-effect completion, production readiness, or
global transaction authority.

## Source checkpoint

- Source archive:
  `NVDA_M13_PM_V6_IMPLEMENTATION_OPEN_e8384ad_20260726.tar(1).gz`
- Archive SHA-256:
  `87c4f43ea814e920b1b2030044b62d1afa569565952a274524f0a7b58a754f0f`
- Source branch: `review/m13-proof-v6`
- Source commit: `e8384ada435097d64f46f5fe01d55e8d833bf1f4`
- Frozen proof SHA-256:
  `7f4fd1e3d9c7f7dc75675146f9e2a38d4fb259a1938986c7cdfc2b006ddfab0a`
- Source worktree: clean
- Git history: present; `git fsck --connectivity-only` exited 0
- Worker branch: `implementation/m13-state-kernel`

The complete required reading is inventoried in
`raw_validation/implementation_worker/M13_IMPLEMENT_FULL_READ_MANIFEST.tsv`.

## Implementation structure and ownership

The production addition is confined to
`src/nvda_desk/m13_state_kernel/`:

- `contracts.py` owns immutable command, key and committed-receipt values plus
  the two bounded conflict errors.
- `ports.py` owns the Unit of Work and repository-participant interfaces.
- `in_memory.py` owns transaction ordering and the explicitly non-durable
  detached alpha adapter.
- `__init__.py` is the only public export surface.

The package coordinates owner-declared state and repository participants but
does not interpret capital, positions, calendar facts, risk observations,
execution or any other domain record. It has no dependency on M00-M12 domain
modules and does not transfer ownership from existing persistence or repository
packages.

## Public contract

The explicit public surface is:

- `UnitOfWork`
- `RepositoryPort`
- `IdempotencyKey`
- `TransactionCommand`
- `AtomicReceipt`
- `InMemoryUnitOfWork`
- `IdempotencyConflictError`
- `StateVersionConflictError`

`IdempotencyKey`, `TransactionCommand` and `AtomicReceipt` are frozen,
slot-backed values. Required identifiers reject empty or whitespace-only
strings. The original fingerprint and policy-version strings are retained
without normalisation. No timestamp or wall-clock field was introduced.

## Transaction law

### Idempotency and version ordering

1. Resolve an already committed scoped key before optimistic-version
   rejection.
2. Return a detached replay response for an exact command identity
   `(command_id, input_fingerprint, policy_version)`.
3. Reject a different identity bound to the same scope
   `(key value, command type, consistency-unit ID)`.
4. Reject a stale version before mutation or participant work for an unbound
   scope.
5. Bind the scoped key only after all participant commits and internal
   publication succeed.

Duplicate replay changes only the returned `duplicate_replay` flag. It does not
mutate the stored receipt, rerun mutation, call participants, advance version or
sequence, or add a receipt.

### Owner mutation and receipt ordering

1. Deep-copy committed state into an isolated working value.
2. Run owner mutation.
3. Require a mapping containing non-empty `receipt_id` and `result_id`.
4. Build the complete proposed receipt before participant preparation.
5. Publish nothing internally until every participant commit succeeds.

Mutation and receipt-validation failures therefore leave no state, version,
sequence, receipt, participant or idempotency truth.

### Participant ordering and rollback

1. Register rollback responsibility before each `prepare()`.
2. Prepare participants in declaration order.
3. Commit participants in declaration order only after all prepares succeed.
4. On prepare or commit failure, call `rollback()` for the raising participant
   and all earlier responsible participants in reverse order.
5. Preserve the primary transaction exception. Cleanup exceptions are attached
   as notes and never replace it.
6. Publish internal state, version, sequence, receipt and scoped binding only
   after all participant commits return successfully.

Receipt writers use exactly the same participant protocol and ordering; the
implementation has no name-based or private-field special case.

## Detached non-durable adapter

`InMemoryUnitOfWork.durability == "non_durable_in_memory"`.

Initial state, transaction working state, participant inputs, snapshot
readbacks, receipt lists and returned receipts cross defensive-copy boundaries.
Version and sequence begin at zero and advance only after a complete successful
transaction. No filesystem, database, network, service or process-global
singleton is used.

## Proof and falsification

All raw commands, unedited outputs and exit codes are under
`raw_validation/implementation_worker/`.

### Production proof

Command:

```text
.venv/bin/python -m pytest tests/tier_a/persistence/test_m13_state_kernel_contract.py -vv
```

Result: exit 0; 46/46 passed. Every one of the 32 parameter IDs appeared
individually. There were no skips, xfails or deselections.

### Retained falsification

Command:

```text
.venv/bin/python project_control/canonical_project_manager/modules/M13/raw_validation/implementation_worker/run_retained_falsification.py
```

Result: exit 0.

- Both PM V5 false positives passed the old fourteen cases and failed the
  repaired family for their intended hidden-binding conflict.
- All 32 configurable variants were rejected at the intended combination of
  eight failure boundaries and four binding comparisons.
- All 11 earlier retained mutants failed both the complete family and the
  intended targeted case without collection or interface error.

### Implementation-derived falsification

Command:

```text
M13_PYTHON="$PWD/.venv/bin/python" M13_SITE_PACKAGES="$PWD/.venv/lib/python3.13/site-packages" .venv/bin/python project_control/canonical_project_manager/modules/M13/raw_validation/implementation_worker/run_implementation_mutants.py
```

Result: exit 0; 8/8 complete-family rejections and 8/8 targeted intended
rejections.

The derived mutations were early binding, early internal publication, omitted
rollback of the prepare raiser, omitted rollback of an earlier participant,
stored-receipt mutation on replay, snapshot leakage, ignored policy version and
sequence advancement on failure.

## Affected and shadow validation

The consolidated evidence is
`raw_validation/implementation_worker/validation_runs/validation_summary.tsv`.

| Surface | Exit | Result |
|---|---:|---|
| Frozen M13 proof | 0 | 46 passed |
| M13 collection | 0 | 46 collected |
| Public-contract implementation checks | 0 | passed |
| Complete persistence Tier A | 0 | 82 passed |
| Proof-block structural validation | 0 | 52 passed |
| Proof-executor contract | 0 | 21 passed |
| Checkpoint shadow | 0 | 2 passed |
| Exact vocabulary builder parity | 0 | passed |
| Complete vocabulary parity file | 1 | admitted pre-existing one-test shadow failure |
| Architecture/import boundary | 0 | passed |
| Ruff | 0 | passed |
| Black check | 0 | passed |

The complete repository shadow used the same Python 3.13.5 environment for the
source checkpoint and implementation:

- Source checkpoint: exit 1; 107 failed, 1201 passed.
- Implementation: exit 1; 61 failed, 1247 passed.
- Exact failed-node comparison: all 61 remaining nodes are unchanged source
  checkpoint failures; exactly the 46 missing-M13 failures were resolved; zero
  new or changed failures exist.

The complete failure inventories and raw outputs are retained byte-for-byte in
`validation_runs/repository_shadow_baseline.txt.gz`,
`validation_runs/repository_shadow_current.txt.gz`, and
`validation_runs/repository_shadow_comparison.txt.gz`.

The archive did not include its virtual environment. Initial complete-suite
collection therefore failed for missing locked dependencies. The environment
was repaired using the repository's exact Python and locked package versions;
the final source and implementation shadow runs used that identical repaired
environment.

## Architecture and vocabulary review

AST import inventory established:

- no M13 import of any M00-M12 domain package;
- no M13 top-level outgoing dependency;
- no top-level cycle containing M13;
- no import of tests, raw validation, retained references or mutants;
- no production import from API, cognition, capital, downstream or review;
- all changed `src/**` paths are under the accepted M13 package.

Semantic inspection confirms that the module coordinates opaque state and
participant mechanics only. It adds no persistence claim beyond the explicit
non-durable label.

The exported durable concepts reuse admitted entries for State Kernel, Unit of
Work, Idempotency Key, Atomic Receipt, Repository Port and Transaction Command.
The in-memory adapter and bounded conflict-error names remain module-local
implementation vocabulary under the accepted review. No new global durable
term is required.

## Code-quality inspection

All M13 source was read in full after formatting and falsification. Syntax,
compile, Ruff, Black and `git diff --check` pass. The source contains no broad
exception suppression: rollback failures are recorded without hiding the
primary transaction failure. No public mutable collection is exposed. No dead
compatibility surface or domain-specific helper was added. Comments are limited
to the non-obvious duplicate-before-version, register-before-prepare and
publish-after-participants laws.

Production-source hashes differ from every retained reference source hash. The
implementation was derived from N-06, accepted ownership and the frozen public
proof rather than copied wholesale from the conforming falsification snapshot.

## Changed paths and evidence

Changed production paths are exactly:

- `src/nvda_desk/m13_state_kernel/__init__.py`
- `src/nvda_desk/m13_state_kernel/contracts.py`
- `src/nvda_desk/m13_state_kernel/in_memory.py`
- `src/nvda_desk/m13_state_kernel/ports.py`

All other additions are this worker record, validation scripts, full-read
inventory and raw implementation evidence under the M13 worker-owned validation
directory. Tests, normative documents, vocabulary authority, proof-block
configuration, retained-test configuration and all pre-existing source packages
remain unchanged.

Final tracked hashes, commit identity and fresh-extraction checkpoint evidence
are retained with the final worker checkpoint. The commit and archive do not
change this proposal-only disposition.
