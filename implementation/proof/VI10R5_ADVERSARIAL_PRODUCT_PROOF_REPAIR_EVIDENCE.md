# VI-10R5 Adversarial Product Proof Repair Evidence

## Status

`FROZEN WORKER CLAIM — PENDING FRESH VI-11R5 / TESTER ITERATION 008 REVIEW`

This record binds the VI-10R5 proof-only successor to one immutable physical proof candidate. It does not claim independent proof adequacy and does not authorise VI-12R production implementation.

## Exact candidate

- Tester Iteration 007 repair/source checkpoint / physical parent: `96550e119e64d1145d057d98fbdcaed3f9e049b9`
- frozen VI-10R5 physical proof commit: `e39740c6ddd24fa1372bde6ca630245285a807d7`
- frozen physical proof tree: `dabf8fe94cfc14e74131604a42030514791c10ee`
- rejected VI-10R4 physical predecessor preserved in ordinary Git history: `0c626fb78fa7317fa265bd5ff871dd398c68404d`
- rejected VI-11R4 wrapper preserved in history: `30db3d00f1b9f32215ce1f06b156647e92f1e505`

The physical diff from `96550e119e64d1145d057d98fbdcaed3f9e049b9` to `e39740c6ddd24fa1372bde6ca630245285a807d7` contains exactly:

```text
config/product_proof/families.yaml
tests/product/raw_signal/_process_probe.py
tests/product/raw_signal/test_u01_contract_owner_boundary.py
tests/product/raw_signal/test_u02_capture_schedule.py
tests/product/raw_signal/test_u05_postgresql_durability.py
tests/product/raw_signal/typecheck/public_seam_negative.py
tests/product/raw_signal/typecheck/public_seam_positive.py
```

No `src/**`, architecture registry/proof, IRB, BICP, IWO or METHOD-006 normative byte changed in the physical candidate.

The parent checkpoint separately preserves the Programme Owner-directed canonical signal catalogue at `implementation/authority/source_signal_catalogue/NVDA_80_STEP_ACADEMIC_EVIDENCE_AUDIT_WITH_SIGNALS_ADDENDUM_81_94.xlsx`, SHA-256 `519ea9449297d564ae4a02afc1bf4e60e4471631c81a0842620f9fb60bb4f9ae`, for established `R001–R323` / `D001–D209` IDs and definitions only. No workbook bounds/min-max law or `D001+` implementation is admitted by this proof repair.

## Tester Iteration 007 finding-to-discriminator map

The entries below are Worker claims for fresh independent challenge, not accepted dispositions.

### T007-F001 — PostgreSQL is the exclusive reachable durable semantic channel

- Fresh-process probes execute in a private user/mount/network namespace and a tmpfs-rooted chroot.
- Host interpreter/source material and the PostgreSQL Unix-socket path are recursively bind-mounted read-only; all discovered submounts are remounted read-only rather than relying on a top-level bind flag.
- The only writable filesystems visible inside the proof root are ephemeral `tmpfs` and `proc`.
- A black-box control attempts a write to an actual host source path and requires failure while an ephemeral write succeeds.
- Existing database clone/source-removal and PostgreSQL-row-deletion discriminators remain: semantic state must move with PostgreSQL state and exact readback must cease if correlated PostgreSQL state is removed.

### T007-F002 — durable commit is proven at the public method-return event

- A proof-owned Python profile hook targets the exact public command method code object and fires on its `return` event before caller-side inspection or serialisation of the returned object.
- At that event the child prints only a constant boundary marker and immediately self-`SIGSTOP`s. This freezes the entire process, including any background/lazy commit thread; it does not merely block the calling thread on stdin.
- While the child is stopped, the parent requires no open PostgreSQL writer transaction and exact fresh-process readback.
- A separate path kills the stopped child at the same return boundary and requires the fact to remain durably readable.
- Policy, scheduled-capture, raw-observation and assessment writes are covered.

### T007-F003 — persistence has an exact record-only data-flow surface

- The default PostgreSQL technical port must expose exactly nine public callables: policy/capture/observation/assessment append/get plus assessment-list read. Every operation has fixed bounded arity and no `*args`/`**kwargs` escape.
- No relation/eligibility/outcome decision operation is admitted on that storage surface; receipt-evidence relation remains owner-derived/on-demand as permitted by the IWO.
- The default PostgreSQL port is exercised directly with a complete owner-decided counterfactual assessment whose `zero_received` outcome deliberately disagrees with the eligible observation evidence visible in durable state.
- The adapter must persist and reread that record unchanged. A completely new owner/adapter object graph then rereads the same record from PostgreSQL with a counterfactual eligibility resolver and must still return the exact original `zero_received` fact.
- This replaces the prior semantic-name/literal scanner as the ownership discriminator; the package-level alternate-backend/external-service exclusion remains only as a durability-channel control.

### T007-F004 — restart-persistent assessment identity and per-scope ingestion high-water

Across fresh processes U05 now requires:

- same assessment occurrence ID + identical content is idempotent and returns the exact stored fact;
- same assessment occurrence ID + changed content rejects after restart;
- ingestion scope A accepts high-water 42;
- independent scope B accepts 1;
- returning to scope A with 40 rejects after the scope switch;
- returning to scope A with 43 succeeds.

Existing same-process identity/high-water discriminators remain.

### T007-F005 — failed scheduled-capture write cannot fabricate success

- U05 injects `fail_before_commit` into a scheduled-capture command on the real PostgreSQL path.
- The command must fail rather than return a semantic fallback.
- A separate fresh process must observe that exact capture occurrence identity as absent.
- Existing raw-observation and assessment fail-before-commit non-fabrication cases remain.

### T007-F006 — one-active-policy law spans distinct policy identities

- U02 now registers a correctly typed second `scope_policy_id` whose interval overlaps the existing active policy and requires rejection.
- A distinct successor identity beginning exactly at the predecessor's exclusive deactivation boundary is separately exercised as a lawful non-overlapping case.
- Existing same-policy version overlap and boundary cases remain.

### T007-F007 — all eleven public command/read facets are physically static-type discriminated

- `public_seam_positive.py` exercises all six command facets and all five read facets with explicit contract/identity input and output annotations.
- mypy 1.20.1 runs with `--strict --disallow-any-expr`; a public seam collapsed to `Any` cannot satisfy the lawful specimen.
- `public_seam_negative.py` contains exactly eleven marked cross-layer/wrong-contract calls, one per public facet.
- The pytest proof requires mypy to report a static error at every marked line, rather than merely requiring the negative specimen to fail somewhere.

## Clean physical-candidate validation

All commands below were rerun against exact clean commit `e39740c6ddd24fa1372bde6ca630245285a807d7`.

### Product proof control / collection

```text
python tools/validate_product_proof.py
PASS
6 admitted physical families
13 required obligations
13/13 covered
aggregate READY_FOR_PROOF

pytest --collect-only -q tests/product/raw_signal
397 tests collected
```

### Real PostgreSQL expected-red execution

Proof runtime:

```text
Python               3.13.5
pytest                9.0.3
mypy                  1.20.1
Ruff                  0.15.11
Psycopg                3.3.4
PostgreSQL             17.9
fsync                  on
synchronous_commit     on
full_page_writes       on
```

With `NVDA_TEST_POSTGRES_DSN` bound to that exact PostgreSQL 17.9 Unix-socket server:

```text
pytest -q -rA tests/product/raw_signal
388 failed, 9 passed
```

The environment classifier found no missing-DSN, Psycopg, connection, permission, namespace or Unix-socket failure signature. Explicit red reasons remain the deliberately absent M00 Raw Signal public seam/contracts/`create_owner` and A00 `create_application`. The PostgreSQL version check and exclusive-filesystem control execute green before production exists. This is expected pre-implementation red evidence only; it is not an independent proof-adequacy PASS.

### Separate architecture/static/integrity axis

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

VI-10R5 is frozen as a Worker proof candidate only. `T007-F001..F007` remain open until fresh Tester Iteration 008 independently accepts the proof. VI-12R production implementation remains prohibited.
