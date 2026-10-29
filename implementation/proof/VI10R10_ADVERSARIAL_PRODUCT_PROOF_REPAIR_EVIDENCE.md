# VI-10R10 adversarial product-proof repair evidence

## Status

`WORKER CLAIM — PENDING FRESH VI-11R10 / TESTER ITERATION 013 AUDIT`

This record binds the proof amendment to an immutable test-only commit. It does not claim
independent proof adequacy, does not relabel unavailable PostgreSQL or namespace execution as a
pass, and does not authorise VI-12R production implementation.

## Exact candidate

- Tester Iteration 012 handoff parent: `36bba0d26b988881812d2333f7e1eb3e8e63786b`;
- preserved failed VI-10R9 physical proof: `0917e0319a460a6d7ffb40b776b716f80f8f8684`;
- VI-10R10 physical proof commit: `548a61107fda52e643142542ddb60dee584bd46e`;
- VI-10R10 physical proof tree: `e4e0850990545b46d57bb8241596fa1e51c60451`;
- changed path: `tests/product/raw_signal/test_u05_postgresql_durability.py`;
- production-source changes: none.

## T012-F001 repair

The uniquely named writer's `backend_xid` is now captured while the backend is visibly blocked in
`SyncRep`. After release, public-return freezing and exact fresh readback, the proof gathers the
`xmin` transaction identity of every non-system PostgreSQL row carrying the action-specific
semantic record identity. It accepts only when that set is exactly the waited transaction ID.

The new two-commit canary places one semantic identity into separate `command_audit` and
`semantic_write` transactions. The database helper must expose both `xmin` values, and the binding
predicate must reject the first transaction as the semantic durable-success discriminator.

## T012-F002 repair

The real opposing-eligibility proof now constructs semantic owners with the record-only proxy via
the authorised `persistence_port` seam instead of constructing them with the concrete adapter and
rewriting afterwards. The checker still verifies that no concrete identity or recoverable
capability remains in either semantic owner graph.

The graph helpers additionally recognise live weak references, weak bound methods and both weak
proxy forms. Four implementation-independent canaries first remove the ordinary direct-port
reference, then prove both post-rewrite detection and fail-closed rewriting.

## Executed evidence

Against physical commit `548a611...` in the available Python 3.12 worker runtime:

```text
focused transaction/graph canaries          18 passed / 34 deselected
product collection                           450 tests
product-proof control                        PASS; 6 families / 13 of 13 obligations
structural architecture validator            PASS
architecture/bootstrap excluding exact
  typechecker-dependent cases                71 passed / 3 deselected
Ruff src tests tools                          PASS
dependency direction                         PASS
public-seam validation                       PASS
git diff --check                             PASS
physical diff                                1 tests/** path / 0 src/** paths
strict Git fsck                              PASS
```

The full product run collected 450 tests and completed at `420 failed / 30 passed`. U05 completed
at `28 failed / 24 passed`: 26 cases stopped at the missing live PostgreSQL DSN and two at the
deliberately absent `create_owner` production seam. These red results are not represented as
proof-adequacy passes.

## Unproved worker-runtime axes

The attached PostgreSQL runtime manifest verifies, and its `postgres` and `initdb` binaries report
17.9. Live cluster startup is blocked in this worker sandbox: the process runs as UID 0,
PostgreSQL correctly refuses `initdb` as root, UID switching fails because only UID 0 is mapped,
and an unprivileged user namespace cannot write `/proc/self/uid_map`. Consequently the new
database-backed transaction-correlation canary and the prior PostgreSQL U05 cases were not freshly
executed here. Fresh Tester Iteration 013 must run them against PostgreSQL 17.9.

The workspace also exposes Python 3.12 rather than exact Python 3.13.5. The preserved mypy 1.20.1
and `librt` wheels remain CPython-3.13-specific, so the three mypy-dependent architecture cases
and aggregate promotion were not rerun. No weaker result is represented as equivalent.

The nine mapped namespace/filesystem propositions remain explicit `UNPROVED` caveats under current
Programme Owner direction.

## Audit boundary

Fresh Tester Iteration 013 must independently challenge the transaction-ID correlation, injection
construction and weak-capability canaries, and separately run the unavailable live-PostgreSQL and
exact Python-3.13.5 axes. VI-12R remains prohibited unless that review accepts this successor.
