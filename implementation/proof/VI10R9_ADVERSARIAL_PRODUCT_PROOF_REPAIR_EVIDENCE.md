# VI-10R9 adversarial product-proof repair evidence

## Status

`DEGRADED TCP WORKER CLAIM — PENDING FRESH VI-11R9 / TESTER ITERATION 012 AUDIT`

This record binds the proof amendment to an immutable test-only commit. It does not claim
independent proof adequacy, does not treat the nine degraded namespace/filesystem failures as
passes, and does not authorise VI-12R production implementation.

## Exact candidate

- Tester Iteration 011 handoff parent: `d1bad95bddd8b868449f2566b40d38126d50a789`;
- VI-10R9 physical proof commit: `0917e0319a460a6d7ffb40b776b716f80f8f8684`;
- VI-10R9 physical proof tree: `fd5a1cb626f1fb7c41602f989d5f900c080f9537`;
- changed paths:
  - `tests/product/raw_signal/_process_probe.py`;
  - `tests/product/raw_signal/test_u05_postgresql_durability.py`;
- production-source changes: none.

## T011-F001 repair

Every durable-success boundary action now constructs the owner, resolves the selected public
command and prepares all command arguments before emitting `semantic_write_ready`. The parent
starts the child before installing the barrier, waits for `READY`, installs and confirms the
barrier, then sends `GO` before observing `SyncRep`.

The real-PostgreSQL canary commits and reads back an `owner_setup` row before `READY`; after the
barrier is installed and `GO` sent, it independently observes the `semantic_write` transaction in
`SyncRep` with no child output. Only barrier release permits completion. A structural control
checks this order for all five durable-success actions.

## T011-F002 repair

The rewriter and the post-rewrite identity checker now inspect instance dictionaries, slots,
class/MRO namespaces, function-referenced globals and reachable module state. Shared class/module
storage is never rewritten: any retained concrete identity or bound adapter capability is rejected
fail closed.

Thirteen graph canaries pass: the prior nine direct/container/partial/closure/public-method cases
plus four new external-storage cases for class, slots, global and module storage. The class case
uses the tester's exact `type(self)._cached = adapter._semantic_decision` escape.

## Product control and real-PostgreSQL execution

Against physical commit `0917e03...`:

```text
product-proof control                     PASS
admitted physical families                6
required/covered product obligations       13 / 13
product collection                         444 tests
U05 degraded TCP                           24 failed / 22 passed
complete product suite                     416 failed / 28 passed
```

The six additional green tests are one five-action handshake-order control, one real-PostgreSQL
setup-versus-semantic transaction canary, and four external-capability canaries. The 24 U05
failures remain the same nine explicit `DEGRADED TCP VALIDATION: UNPROVED` boundary propositions
plus fifteen failures attributable to deliberately absent production. The complete product suite
retains 407 absent-production/static failures plus those nine explicit boundary failures.

The fresh PostgreSQL 17.9 loopback-TCP cluster ran as effective user `nobody` with `fsync=on`,
`synchronous_commit=on` and `full_page_writes=on`. This does not establish the mapped
mount/network/PID namespace or exclusive-filesystem propositions.

## Separate static, architecture and integrity controls

```text
structural architecture validator          PASS
architecture/bootstrap excluding exact
  typechecker-dependent cases              71 passed / 3 deselected
Ruff src tests tools                        PASS
dependency direction                       PASS
public-seam validation                     PASS
git diff --check                           PASS
physical diff                              2 tests/** paths / 0 src/** paths
```

The current reset workspace exposes Python 3.12, not the project's exact Python 3.13.5 runtime.
The preserved mypy 1.20.1 and `librt` wheels are CPython-3.13-specific. Consequently, the exact
mypy-dependent architecture cases and aggregate promotion were not freshly rerun here; no weaker
result is represented as equivalent. Git diff establishes that `src/**`, architecture
configuration, architecture/bootstrap tests and promotion tools are byte-unchanged from the
reviewed handoff parent. Fresh Tester Iteration 012 is asked to rerun the exact 3.13.5
architecture axis.

## Audit boundary

Fresh Tester Iteration 012 must audit the two repaired false-positive paths independently. The
nine degraded namespace/filesystem propositions remain explicit `UNPROVED` caveats and are not a
reason asserted here for proof acceptance.
