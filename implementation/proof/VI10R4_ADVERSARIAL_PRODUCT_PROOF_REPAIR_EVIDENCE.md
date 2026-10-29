# VI-10R4 Adversarial Product Proof Repair Evidence

## Status

`FROZEN WORKER CLAIM — PENDING FRESH VI-11R4 / TESTER ITERATION 007 REVIEW`

This record binds the VI-10R4 proof-only successor to one immutable physical proof candidate. It does not claim independent proof adequacy and does not authorise VI-12R production implementation.

## Exact candidate

- Tester Iteration 006 repair checkpoint / parent: `4aee3dfde5ff0c9f83a113e5f2fb792f53f22981`
- frozen VI-10R4 physical proof commit: `0c626fb78fa7317fa265bd5ff871dd398c68404d`
- frozen physical proof tree: `df10fd0e42178dfb7e6fabe0fd9a8e3a3a3249f6`
- rejected VI-10R3 physical predecessor preserved in ordinary Git history: `ffcbc64b77b66f96c91926b423622281f125d757`
- rejected VI-11R3 wrapper preserved in history: `d50bc2393078b584b722fb2bf4ba692f055c40ad`

The physical diff from `4aee3dfde5ff0c9f83a113e5f2fb792f53f22981` to `0c626fb78fa7317fa265bd5ff871dd398c68404d` contains exactly:

```text
config/product_proof/families.yaml
tests/product/raw_signal/_process_probe.py
tests/product/raw_signal/test_u01_contract_owner_boundary.py
tests/product/raw_signal/test_u02_capture_schedule.py
tests/product/raw_signal/test_u04_receipt_assessment.py
tests/product/raw_signal/test_u05_postgresql_durability.py
```

No `src/**`, architecture registry/proof, IRB, BICP, IWO or METHOD-006 normative byte changed in the physical candidate.

## Tester Iteration 006 finding-to-discriminator map

The entries below are Worker claims for fresh independent challenge, not accepted dispositions.

### T006-F001 — PostgreSQL is the semantic durable source

- U05 writes independent high-entropy policy/observation facts to a dedicated PostgreSQL source database, clones that database using PostgreSQL `CREATE DATABASE ... TEMPLATE ...`, drops the source database, and requires isolated fresh readers using only the clone DSN plus domain query identity to reproduce exact policy/capture/observation/assessment facts.
- The original source DSN must no longer read.
- A separate test discovers high-entropy facts in PostgreSQL user tables, deletes the correlated PostgreSQL state, and requires exact readback to cease.
- Isolated readers run with `/mnt/data` read-only, private tmpfs scratch, a new network namespace, stripped environment, and Unix-socket PostgreSQL access; owner-package static proof rejects alternate configured file/network durable mechanisms.
- The isolation namespace and database clone/drop harness were separately executed before freeze: Unix-socket connection succeeded from the isolated namespace; a sentinel row survived PostgreSQL database clone and became unavailable through the dropped source database.

### T006-F002 — command success follows its own durable commit

- U05 obtains the public command result from a hold-open writer process while that process remains alive, then kills the writer immediately without graceful release and requires a separate fresh process to read the exact durable record.
- Policy, capture, zero assessment, observation and one-or-more assessment command families are exercised this way.
- The existing concurrent-read proof also checks that no PostgreSQL transaction remains open for the writer application after the public command has returned and before writer shutdown.

### T006-F003 — technical persistence cannot decide Raw Signal meaning

- U05 discovers the default technical persistence port from the runtime owner object graph and roots a local static module/import closure at that actual mechanism plus Psycopg-using modules rather than relying on persistence filenames.
- Every module in the resulting technical closure is rejected if it carries eligibility resolver access, Raw Signal outcome/relation semantic literals, named semantic decision functions, or dynamic import escape.
- The whole owner package is additionally rejected for alternate durable backends/external semantic services and common writable file/mmap/subprocess/dynamic-import mechanisms.
- U04 separately injects a semantic-blind persistence port and proves the port receives already-decided records while exposing no eligibility/outcome decision API.

### T006-F004 — closed `.v1` contracts reject unknown keyword material

- U01 parameterises all five active `.v1` contracts with a lawful baseline payload plus an unproved `__unproved_v1_extension__` keyword and requires fail-closed behaviour.
- This is behavioural and therefore rejects a constructor that hides unknown-field acceptance behind `**kwargs` even when signature/shape inspection looks closed.

### T006-F005 — typed-but-nonexistent observation authority

- U04 supplies a correctly typed observation-occurrence identity that was never durably admitted.
- Relation derivation must reject it and the eligibility resolver must remain uncalled, proving a typed reference alone cannot substitute for actual observation authority.

### T006-F006 — assessment evidence is capture-local

- U04 creates two lawful captures, gives eligible committed receipt evidence only to capture A, then assesses both at the same evidence-as-of instant.
- Capture A must derive `one_or_more_received`; capture B must derive `zero_received`.

### T006-F007 — restart-persistent invariants

Across fresh processes U05 requires:

- conflicting re-registration of the same policy identity/version still rejects;
- a second capture identity for the same stable policy/slot cannot replace the original;
- lawful immediate assessment supersession succeeds while a stale predecessor rejects;
- same-scope ingestion high-water survives restart (42 accepted, then 40 rejected);
- an independent scope may lawfully use sequence 1.

### T006-F008 — exact restart assessment readback

- U05 compares the complete canonical recovered assessment record after restart, not only selected identity/outcome fields.
- The comparison therefore binds assessment identity type/value, capture reference, exact outcome, evidence-as-of timestamp, concept/contract discriminants, and lawful supersedes absence/presence.

### T006-F009 — exact half-open interval and microsecond schedule-grid edges

- U04 physically discriminates receipt at one microsecond before start, exact start, one microsecond before end, and exact end; only `[start,end)` is relation-eligible.
- U02 rejects capture slot starts displaced by one microsecond from exact half-minute boundaries and rejects policy activation/deactivation displaced by one microsecond from the authorised `:00/:30` grid.

## Clean physical-candidate validation

All commands below were rerun against exact clean commit `0c626fb78fa7317fa265bd5ff871dd398c68404d`.

### Product proof control / collection

```text
python tools/validate_product_proof.py
PASS
6 admitted physical families
13 required obligations
13/13 covered
aggregate READY_FOR_PROOF

pytest --collect-only -q tests/product/raw_signal
393 tests collected
```

### Real PostgreSQL expected-red execution

PostgreSQL runtime:

```text
server_version       17.9
fsync                on
synchronous_commit   on
full_page_writes     on
```

With `NVDA_TEST_POSTGRES_DSN` bound to that server:

```text
pytest -q tests/product/raw_signal
384 failed, 9 passed
```

The failure classifier found no unknown explicit failure reasons and no missing-DSN, import, connection, permission or isolation-namespace failure signature. Explicit failure reasons are the deliberately absent M00 Raw Signal public seam / `create_owner` and A00 `create_application` production seam. This is pre-implementation red evidence only; it is not a proof-adequacy PASS.

### Separate architecture/static axis

```text
python tools/validate_architecture.py
PASS

pytest -q tests/architecture tests/bootstrap
74 passed

python tools/run_promotion_gate.py --set architecture_kernel
74 passed; rc=0

mypy src
Success: no issues found in 15 source files

ruff check src tests tools
All checks passed!

nvda-check-dependencies
PASS

nvda-check-public-seams
PASS

git diff --check
PASS

git fsck --full --strict
PASS

git status --porcelain
<empty>
```

## Boundary

VI-10R4 is frozen as a Worker proof candidate only. `T006-F001..F009` remain open until fresh Tester Iteration 007 independently accepts the proof. VI-12R production implementation remains prohibited.
