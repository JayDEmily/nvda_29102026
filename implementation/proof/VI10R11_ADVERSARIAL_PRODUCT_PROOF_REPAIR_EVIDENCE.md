# VI-10R11 adversarial product-proof repair evidence

## Status

`WORKER CLAIM — PENDING FRESH VI-11R11 / TESTER ITERATION 014 AUDIT`

This record binds the proof amendment to an immutable test-only commit. It does not claim
independent proof adequacy, does not relabel unavailable PostgreSQL or namespace execution as a
pass, and does not authorise VI-12R production implementation.

## Exact candidate

- Tester Iteration 013 continuity parent:
  `39b5ca75e74ecd5cdee50c66c3a26fe3f34aec65` / tree
  `b044dae0738d9a7bf416319dc18bc7ea59c379b9`;
- preserved failed VI-10R10 physical proof: `548a61107fda52e643142542ddb60dee584bd46e`;
- VI-10R11 physical proof commit: `cca84de4ce2e9df52647352237c8a64e52a10db5`;
- VI-10R11 physical proof tree: `6b7881fc045345eef357248f4fa8f75f38599923`;
- changed path: `tests/product/raw_signal/test_u05_postgresql_durability.py`;
- production-source changes: none.

## T013-F001 repair

The five-command SyncRep proof now installs its database-write trace only after the child emits
`semantic_write_ready`. Every existing non-system regular relation is covered by an `AFTER` row
trigger, and its OID is recorded. The exact writer then proceeds under `GO` and the SyncRep barrier.
At the frozen public return, exact fresh readback is followed by two fail-closed checks: no new
untraced durable relation may exist, and every recorded write XID must equal the backend XID
observed in `SyncRep`.

The successor live canary uses an audit row containing the only literal marker and a separately
committed payload row linked by surrogate ID. It requires the predecessor marker predicate to
accept the audit XID, then requires the successor trace to expose both XIDs and reject the split.

## T013-F002 repair

The opposing-eligibility test now creates every concrete default PostgreSQL adapter only inside a
separate child process. Parent-side semantic owners receive only an allowlisted nine-method record
port. That port has no `_inner`, and the child endpoint rejects `_semantic_decision` or any other
non-protocol dispatch. Both eligibility outcomes are still derived by the semantic owners, while
the same cloned durable state remains unchanged under opposing eligibility authority.

The graph checker no longer has an opaque proxy exception. A focused canary adds `_inner` back to
the record proxy and requires the checker and rewriter to expose/reject the exact previous escape.

## Executed evidence

Against physical commit `cca84de...` in the available Python 3.12 worker runtime:

```text
focused transaction/capability canaries      20 passed / 35 deselected
product collection                            453 tests
product-proof control                         PASS; 6 families / 13 of 13 obligations
structural architecture validator             PASS
architecture/bootstrap excluding exact
  typechecker-dependent file                  71 passed
Ruff src tests tools                           PASS
dependency direction                          PASS
public-seam validation                        PASS
git diff --check                              PASS
physical diff                                 1 tests/** path / 0 src/** paths
strict Git fsck                               PASS
```

The full product run completed at `420 failed / 33 passed`. U05 completed at `28 failed / 27
passed` when the portable runtime's `libpq` was supplied. These expected-red results arise from the
missing live PostgreSQL DSN and deliberately absent product implementation and are not represented
as proof-adequacy passes.

## Unproved worker-runtime axes

The preserved portable `postgres` and `initdb` binaries report PostgreSQL 17.9 and Psycopg 3.3.4
loads against its `libpq`. A live cluster cannot be initialised in this worker sandbox: the process
runs as UID 0, PostgreSQL refuses `initdb` as root, and `setpriv` cannot map UID/GID 65534 because
only UID 0 is mapped. The new database-write trace, split-marker/surrogate canary and the complete
five-command SyncRep cases therefore remain Worker-`UNPROVED` and must be executed by Tester
Iteration 014.

The worker runtime is Python 3.12 rather than exact Python 3.13.5. The three typechecker-dependent
architecture cases and aggregate promotion were not substituted with the available 71-test axis.
The nine mapped namespace/filesystem propositions also remain explicit `UNPROVED` caveats under
current Programme Owner direction.

## Audit boundary

Fresh Tester Iteration 014 must independently run the unavailable PostgreSQL and exact
Python-3.13.5 axes, challenge the database-write trace and process-isolated capability directly,
and return a fresh proof-adequacy verdict. VI-12R remains prohibited unless that review accepts
this successor.
