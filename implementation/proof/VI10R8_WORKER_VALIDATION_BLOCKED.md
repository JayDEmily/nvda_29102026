# VI-10R8 Worker Validation Blocker

## Status

`AMENDED CHECKPOINT — REQUIRED ISOLATED REAL-POSTGRESQL VALIDATION BLOCKED`

This record does not freeze a VI-10R8 physical proof candidate, claim proof adequacy, start
Tester Iteration 011 or authorise VI-12R.

## Exact checkpoint

- Tester Iteration 010 disposition / repair parent: `e58a0a6116dfccde8645d4ea6b423774953adb48`
- repair-parent tree: `0a993d802646b9d149c02c27c4342058ee02bbb9`
- amended proof checkpoint: `09a6fd77829838522b0a7b037f068c5d1f30f3e1`
- amended checkpoint tree: `c57b13a513397f6ff23dbd62eb9350484fdaa411`
- changed path: `tests/product/raw_signal/test_u05_postgresql_durability.py`
- production-source changes: none

The checkpoint remains an ordinary Git commit only. It is not the immutable physical proof
candidate required by `VI10R8_ADVERSARIAL_PRODUCT_PROOF_REPAIR_DESIGN.md` acceptance.

## Amendments

### T010-F001

The server-side `SyncRep` discriminator is parameterised over all five durable-success command
paths: policy registration, scheduled-capture realisation, raw-observation admission, zero-received
assessment append and one-or-more-received assessment append. Each case now:

- establishes its own authority prerequisites before barrier installation;
- warms the same selected command path using an independent token;
- runs the selected public command under a unique PostgreSQL `application_name`;
- requires server `SyncRep` wait with no public-return marker;
- releases the server barrier before accepting the public-return marker;
- checks no open writer transaction remains; and
- performs fresh public readback against the precomputed expected record.

The command-specific warm-up prevents an unrelated first-use transaction from satisfying the
`SyncRep` observation before the selected durable write executes.

### T010-F002

The proof-owned graph restriction now recursively handles direct references, ordinary owner
objects, list, dict, tuple, set, frozenset and `functools.partial` function/argument/keyword
captures. It rejects concrete private bound methods and closures/defaults that retain concrete
adapter capability. Immutable containers are reconstructed, mutable containers are rewritten,
and the opposing-authority PostgreSQL discriminator retains its post-rewrite reachability check.

Implementation-independent canaries cover direct private capture, multi-level list/dict/tuple
capture, partial function/argument/keyword capture, closure capture, and successful nested rewrite
of admitted public record methods.

## Verified checks

The attached project wheelhouses reconstructed this exact Python toolchain:

```text
Python               3.13.5
pytest                9.0.3
mypy                  1.20.1
Ruff                  0.15.11
PyYAML                 6.0.3
Psycopg                3.3.4
```

Observed results against clean checkpoint `09a6fd7...`:

```text
product-proof control                 PASS; 6 families; 13/13 obligations
product collection                    434 tests
VI-10R8 graph canaries                9 passed, 27 deselected
architecture/bootstrap                74 passed
architecture_kernel promotion         74 passed; rc=0
mypy src                              PASS; 15 files
Ruff src tests tools                  PASS
dependency direction                  PASS
public-seam validation                PASS
git diff --check                      PASS
git fsck --full --strict              PASS
physical diff                         one tests/** path; zero src/** paths
```

### Portable PostgreSQL runtime readback

The later-supplied transfer archive
`NVDA_POSTGRESQL_17_9_PORTABLE_RUNTIME_20260921.tar.gz`, outer SHA-256
`59822410ac6855365c90765de5071182ab382e87d9e9a2622424e7787c4e5caf`, was read back
independently in this worker sandbox:

```text
gzip integrity                         PASS
internal SHA256SUMS                    PASS; 1,937/1,937 files
postgres --version                     PostgreSQL 17.9
initdb --version                       PostgreSQL 17.9
pg_ctl --version                       PostgreSQL 17.9
pg_config --version                    PostgreSQL 17.9
postgres/initdb/pg_ctl/psql/pg_config  no missing shared libraries
GNU m4 fallback                        1.4.19
```

A fresh cluster was initialised and started through an unmapped user namespace, in which the
server process ran as effective OS user `nobody`. Over loopback TCP, direct readback established
PostgreSQL `17.9` with `fsync=on`, `synchronous_commit=on` and `full_page_writes=on`. The repository
environment discriminator
`test_proof_environment_is_real_postgresql_17_9` then passed against a fresh server before clean
shutdown. This establishes runtime availability and the narrow real-server/version proposition
only; it is not the required isolated U05 execution.

## First unmet invariant

The current worker sandbox rejects the mandatory U05 namespace boundary:

```text
unshare --user --map-root-user --mount --net --fork true
unshare: write failed /proc/self/uid_map: Operation not permitted
rc=1
```

The portable PostgreSQL 17.9 runtime is now present and executable, so runtime availability is no
longer a blocker. The remaining blocker is the accepted isolation boundary itself. In this
sandbox an unmapped non-root user namespace can initialise PostgreSQL and serve over loopback TCP,
but filesystem Unix-socket creation fails with `Operation not permitted`; every attempted UID map
fails at `/proc/self/uid_map`; and mount/network/PID namespace creation remains denied. U05
requires both a filesystem Unix-domain-socket DSN and the mapped mount/network/PID boundary.
Replacing that boundary with the weaker TCP, same-process, mock, non-namespaced or client-only
execution is prohibited by the accepted proof design.

Consequently, the following required evidence is not established for checkpoint `09a6fd7...`:

- real PostgreSQL 17.9 execution of the five parameterised server COMMIT-ack cases;
- complete U05 expected-red execution and failure classification; and
- complete product expected-red execution and failure classification.

## Next lawful action

Resume this exact checkpoint in the preserved namespace-capable PostgreSQL 17.9 worker
environment. Run the required U05 and complete product proof without changing the accepted proof
boundary. Only if those results are attributable and all acceptance checks remain satisfied may a
later worker freeze a genuinely new VI-10R8 physical proof candidate and prepare the fresh Tester
Iteration 011 handoff.
