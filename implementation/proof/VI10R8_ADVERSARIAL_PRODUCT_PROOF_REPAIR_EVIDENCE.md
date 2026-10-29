# VI-10R8 Adversarial Product Proof Repair Evidence

## Status

`DEGRADED TCP WORKER CLAIM — PENDING FRESH VI-11R8 / TESTER ITERATION 011 AUDIT`

This record binds the VI-10R8 proof amendment to an immutable test-only commit and records the
current user's explicit direction to proceed with a TCP caveat. It does not claim that degraded
TCP execution satisfies the accepted mapped mount/network/PID namespace or exclusive-filesystem
proof boundary. It does not claim independent proof adequacy and does not authorise VI-12R
production implementation.

## Exact candidate

- Tester Iteration 010 disposition / repair parent: `e58a0a6116dfccde8645d4ea6b423774953adb48`
- amended VI-10R8 proof checkpoint: `09a6fd77829838522b0a7b037f068c5d1f30f3e1`
- degraded-TCP control parent: `0f9c0b74fb10bd6542614651427ac72a13ed68d0`
- degraded-TCP physical proof commit: `7dc7ce0bb4d162d785bac5b0f431bdab77d954e7`
- degraded-TCP physical proof tree: `134ddc76e61f9751e46cb1990c762ee028f86719`
- changed path in the physical commit:
  `tests/product/raw_signal/test_u05_postgresql_durability.py`
- production-source changes: none

The physical commit is an ordinary Git object and a Worker audit target. Because nine required
U05 cases remain explicitly unproved at the sandbox boundary, it is not represented as the fully
isolated physical proof candidate required by the earlier VI-10R8 design.

## Degraded-TCP control

The authoritative path is unchanged. Without an exact `NVDA_U05_DEGRADED_TCP=1` opt-in, a TCP
DSN still fails closed and U05 still requires a PostgreSQL Unix-domain socket plus the mapped
namespace harness.

With the opt-in and a TCP DSN:

- fresh-process PostgreSQL probes run as direct child processes;
- the child environment remains narrow and receives no cloud/service credential or alternate
  database configuration;
- each child receives task-local `HOME`, `TMPDIR`, `XDG_DATA_HOME` and working directory paths;
- any request for the dedicated public-return PID namespace fails explicitly with
  `DEGRADED TCP VALIDATION: UNPROVED`;
- the mapped mount/network namespace and exclusive-filesystem proposition fails explicitly with
  the same degraded-validation label; and
- no namespace-dependent case is skipped, xfailed or reported as passing.

Four implementation-independent controls establish the opt-in, fail-closed default, direct
process selection, task-local directories and explicit PID-namespace refusal.

## Portable PostgreSQL 17.9 runtime

The supplied archive
`NVDA_POSTGRESQL_17_9_PORTABLE_RUNTIME_20260921.tar-1-.gz`, outer SHA-256
`59822410ac6855365c90765de5071182ab382e87d9e9a2622424e7787c4e5caf`, had already passed gzip
integrity and its internal `SHA256SUMS` for all 1,937 files. The validation cluster was freshly
initialised under an unmapped user namespace as effective OS user `nobody`, listened only on
loopback TCP, used PostgreSQL 17.9, and ran with `fsync=on`, `synchronous_commit=on` and
`full_page_writes=on`.

## Product-proof control and collection

Against clean physical commit `7dc7ce0...`:

```text
product-proof control                  PASS
admitted physical families             6
required product obligations           13
covered product obligations            13/13
product collection                     438 tests
```

The aggregate `READY_FOR_PROOF` value is the structural product-proof control state only. It is
not a product PASS and does not override the red or unproved results below.

## Real-PostgreSQL degraded execution

The exact opt-in was:

```text
NVDA_U05_DEGRADED_TCP=1
NVDA_TEST_POSTGRES_DSN='host=127.0.0.1 port=55444 dbname=postgres user=nobody client_encoding=UTF8'
```

Observed results:

```text
U05                                      24 failed, 16 passed
  explicit degraded-boundary failures    9
  absent-production failures             15

complete product suite                  416 failed, 22 passed
  explicit degraded-boundary failures    9
  absent-production/static failures     407
```

The nine boundary failures are one mapped mount/network/exclusive-filesystem case, one separate
session PID-tree canary, five parameterised server COMMIT-ack cases, the kill-immediately-after-
return case and the visibility-before-writer-shutdown case. These results establish neither the
dedicated PID namespace nor filesystem exclusivity.

The remaining red results are attributable to the deliberately absent authorised Raw Signal/A00
production seam or its necessarily red static specimens. The PostgreSQL environment/version
discriminator and proof-owned `SyncRep` barrier canary passed against the real server.

## Separate architecture, static and integrity controls

Against clean physical commit `7dc7ce0...`:

```text
architecture validation                 PASS
architecture/bootstrap                  74 passed
architecture_kernel promotion           74 passed; rc=0
mypy src                                 PASS; 15 source files
Ruff src tests tools                     PASS
dependency direction                    PASS
public-seam validation                  PASS
git diff --check                        PASS
git fsck --full --strict                PASS
clean worktree                          PASS
```

## Audit request and boundary

Fresh Tester Iteration 011 is asked to audit the T010-F001/T010-F002 repairs at physical commit
`7dc7ce0...`, and to audit whether the degraded-TCP controls state their limitations truthfully.
The tester must not treat the nine explicit `UNPROVED` results as passes or silently substitute
them for the accepted namespace propositions.

VI-12R remains prohibited. A tester may judge the proof repair independently of the sandbox
limitation, but only an execution environment that supplies the accepted mapped namespace and
Unix-socket boundary can establish those nine propositions.
