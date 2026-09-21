# VI-10R6 Adversarial Product Proof Repair Evidence

## Status

`FROZEN WORKER CLAIM — PENDING FRESH VI-11R6 / TESTER ITERATION 009 REVIEW`

This record binds the VI-10R6 proof-only successor to one immutable physical proof candidate. It does not claim independent proof adequacy and does not authorise VI-12R production implementation.

## Exact candidate

- Tester Iteration 008 disposition / repair checkpoint / physical parent: `7eb85b097dd4e05705cc781fd102bddf0f6762ca`
- parent tree: `89ae9abb0a45c76594faf6bdf6c96d8f77293c9f`
- frozen VI-10R6 physical proof commit: `355497c8db9cd1f615539634ddb5fa5bea5d405d`
- frozen physical proof tree: `1798b78addf2d81cfd08e1de42944afc94910b92`
- rejected VI-10R5 physical predecessor preserved in ordinary Git history: `e39740c6ddd24fa1372bde6ca630245285a807d7`
- rejected VI-11R5 wrapper preserved in ordinary Git history: `432a52689c4b3aaec0d745c801e63335c1196f2c`
- rejected submitted Iteration-008 archive SHA-256: `bc3bf766a2e0c524cde887a4e2d5e48eda4728015039a877599d2aca9e24851d`

The physical diff from the parent to the frozen candidate contains exactly:

```text
tests/product/raw_signal/_process_probe.py
tests/product/raw_signal/_support.py
tests/product/raw_signal/test_u01_contract_owner_boundary.py
tests/product/raw_signal/test_u03_observation_native_temporal.py
tests/product/raw_signal/test_u05_postgresql_durability.py
```

No `src/**`, architecture registry/proof, IRB, BICP, IWO or METHOD-006 normative byte changed in the physical candidate.

The parent checkpoint already carries the programme-authorised catalogue-carriage clarification and canonical workbook. The workbook remains source authority for established catalogue IDs/definitions only; this proof does not admit bounds, concrete provider mapping defaults or `D001+` implementation.

## Tester Iteration 008 finding-to-discriminator map

The entries below are Worker claims for fresh independent challenge, not accepted dispositions.

### T008-F001 — whole execution tree is frozen at public return

- Return-boundary probes now run in a dedicated PID namespace with a separate proof supervisor as namespace PID 1.
- At the exact profiled public-method `return` event, the writer issues `SIGSTOP` to all other processes in that namespace before exposing the boundary marker, then stops itself.
- Host-side proof identifies the writer by its namespace PID and requires the writer plus every host-visible descendant to be stopped.
- A canary forks a child, moves that child into a separate session with `setsid()`, and continuously emits ticks. After the public return marker the parent requires the writer and child to be stopped and requires no further tick to become readable before release.
- The same barrier is used by the immediate-kill/readback durability paths.

### T008-F002 — real PostgreSQL storage stays technical under opposing eligibility authority

- The existing exact record-only default-storage protocol discriminator remains.
- A source PostgreSQL database containing policy/capture/observation facts is cloned into two identical databases.
- Fresh owners open those identical clones with opposite eligibility resolvers.
- Direct technical-port readback of policy/capture/observation facts must be byte-for-observable-value identical across both clones before and after semantic calls.
- Owner-controlled relation and assessment results are required to differ according to eligibility; storage readback of the underlying identical persisted source facts is required not to change.

### T008-F003 — exact declared types across all eleven public facets

- U01 enumerates all six command facets and five read facets.
- Every contract/identity-bearing parameter is inspected through `get_type_hints`.
- Annotation leaves must equal exactly the admitted concrete contract/identity type for that parameter.
- `Any`, `object`, universal `str`, and widened-union escape hatches therefore fail the physical discriminator.
- Existing strict positive and eleven-line negative mypy specimens remain as independent static evidence.

### T008-F004 — native numeric value/type fidelity on real PostgreSQL

- The common U05 authoritative observation includes native integer zero, a high-precision native float and native null and participates in the existing fresh-process PostgreSQL durability/readback paths.
- Additional restart specimens exercise very small negative floating values and negative percentage/rate-like values.
- Canonical comparison records both exact numeric value representation and the runtime numeric type; stringification, integer/float coercion, silent rounding or null rewriting cannot satisfy the discriminator.
- U03 carries corresponding same-process workbook-ID-backed numeric fidelity cases.
- No range, plausibility, sign or min/max rule is asserted.

### T008-F005 — canonical Raw Signal catalogue identity is carried separately

- U01 requires a distinct `RawSignalCatalogueId` runtime/static type and an optional `raw_signal_catalogue_ids` field on `RawObservationOccurrenceV1`.
- `R001` and `R323` are accepted; malformed, out-of-range and `Dxxx` identifiers are rejected.
- Absence is `None`; an empty present collection and duplicates are rejected.
- A single provider logical record may carry multiple catalogue IDs without changing provider-native identity or observation identity.
- Cross-layer identity substitution is rejected.
- U05 authoritative and numeric restart specimens require exact catalogue-ID carriage through PostgreSQL/fresh-process readback.

## Clean physical-candidate validation

All commands below were rerun against exact clean commit `355497c8db9cd1f615539634ddb5fa5bea5d405d`.

### Runtime

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

The PostgreSQL 17.9 runtime was rebuilt from the preserved project source and preserved bison/flex build artefacts; no weaker database substitute was used.

### Product proof control / collection

```text
python tools/validate_product_proof.py
PASS
6 admitted physical families
13 required obligations
13/13 covered
aggregate READY_FOR_PROOF

python -m pytest --collect-only -q tests/product/raw_signal
417 tests collected
```

### Real PostgreSQL expected-red execution

With `NVDA_TEST_POSTGRES_DSN` bound to the exact PostgreSQL 17.9 Unix-socket server:

```text
python -m pytest -q tests/product/raw_signal
407 failed, 10 passed
```

All 407 failed tests were classified from the pytest failure summary. They resolve to absent authorised production/API symbols (`CaptureScopePolicyV1`, `ScheduledCaptureOccurrenceV1`, `RawObservationOccurrenceV1`, `CaptureReceiptEvidenceRelationV1`, `CaptureReceiptPresenceAssessmentV1`, `RawSignalCatalogueId`, `create_owner`, A00 `create_application`) or the positive/negative static specimens that necessarily fail because those same API symbols do not yet exist. Six child-process assertion wrappers contain the same absent-`create_owner` cause. No PostgreSQL, DSN, permission, namespace, filesystem or proof-control failure remains.

For U05 specifically:

```text
16 failed, 4 passed
```

The four implementation-independent environment/discriminator tests pass, including the separate-session descendant return-barrier canary. The sixteen red tests require the absent Raw Signal production seam.

### Separate architecture/static/integrity axis

```text
python tools/validate_architecture.py
PASS

python -m pytest -q tests/architecture tests/bootstrap
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

VI-10R6 is frozen as a Worker proof candidate only. `T008-F001..F005` remain open until fresh Tester Iteration 009 independently accepts the physical proof. VI-12R production implementation remains prohibited.
