# VI-10R7 Adversarial Product Proof Repair Evidence

## Status

`FROZEN WORKER CLAIM — PENDING FRESH VI-11R7 / TESTER ITERATION 010 REVIEW`

This record binds the VI-10R7 proof-only successor to one immutable physical proof candidate. It does not claim independent proof adequacy and does not authorise VI-12R production implementation.

## Exact candidate

- Tester Iteration 009 disposition / repair checkpoint / physical parent: `52f6b77bfb96bd72971bbdf83c6b2c731c329271`
- parent tree: `c068a3e8c0ce2c39a49fbd198947a1d5976b5148`
- frozen VI-10R7 physical proof commit: `816696590912bfac22d9397bef19dc1eb5315f17`
- frozen physical proof tree: `561d8610e98c965d43aac02f296b8cee39f02129`
- rejected VI-10R6 physical predecessor preserved in ordinary Git history: `355497c8db9cd1f615539634ddb5fa5bea5d405d`
- rejected VI-11R6 wrapper preserved in ordinary Git history: `ffa57057091b52a9abe54cb87cd1827c8dc76f4f`
- rejected submitted Iteration-009 archive SHA-256: `70174e024783e5bdf0420a17e13e815a707be2c5ea3e88fb45f2114780c6bbb7`

The physical diff from the parent to the frozen candidate contains exactly:

```text
tests/product/raw_signal/_process_probe.py
tests/product/raw_signal/test_u01_contract_owner_boundary.py
tests/product/raw_signal/test_u03_observation_native_temporal.py
tests/product/raw_signal/test_u05_postgresql_durability.py
tests/product/raw_signal/typecheck/public_seam_negative.py
tests/product/raw_signal/typecheck/public_seam_positive.py
```

No `src/**`, architecture registry/proof, IRB, BICP, IWO or METHOD-006 normative byte changed in the physical candidate.

## Tester Iteration 009 finding-to-discriminator map

The entries below are Worker claims for fresh independent challenge, not accepted dispositions.

### T009-F001 — PostgreSQL commit acknowledgement causally precedes public success return

- `test_postgresql_sync_commit_barrier_itself_waits_for_server_acknowledgement` independently proves the proof-owned PostgreSQL barrier itself is effective: with a deliberately unavailable synchronous standby, the server backend enters `SyncRep`, the client transaction has not returned, and only release of the barrier permits commit completion/readback.
- `test_public_success_return_requires_postgresql_commit_acknowledgement` applies that same server-side barrier to the Raw Signal public command path.
- The command runs with a unique PostgreSQL `application_name`; the proof observes its server backend in `wait_event_type='IPC'` / `wait_event='SyncRep'` while requiring that the public-return marker is still absent.
- Only after the proof restores the synchronous-standby setting may the server acknowledge COMMIT, the public command return, and fresh readback proceed.
- A client implementation that merely flushes COMMIT and returns without consuming successful server acknowledgement therefore cannot satisfy this discriminator.

### T009-F002 — real PostgreSQL storage is exercised through a record-only capability

- `_RecordOnlyPersistenceProxy` exposes only the nine admitted technical record operations used by the proof.
- The production object graph is rewritten from the concrete PostgreSQL adapter to that proxy before the owner semantic calls in the opposing-authority clone discriminator.
- Rewriting handles direct references and cached approved bound record methods; cached private adapter methods, private partials/closures or other concrete-adapter semantic capabilities are rejected rather than carried through.
- `test_record_only_proxy_rewrite_rejects_cached_private_adapter_capability` is an implementation-independent canary proving that a cached private semantic helper is rejected.
- `test_default_postgresql_storage_is_invariant_under_opposing_eligibility_authority` then requires owner semantic differences under opposing eligibility authority while the identical PostgreSQL source facts remain technically invariant through the record-only surface.

### T009-F003 — complete exact typing of all eleven public facets

- `test_every_public_facet_declares_complete_exact_parameter_and_return_types` binds every parameter and return annotation on all six command and five read facets, not only identity/contract-bearing parameters.
- The discriminator includes datetime, integer/version, optional, sequence/container and return types and rejects variadics, `Any`, `object`, universal `str`, untyped containers and widened/permissive unions.
- The positive mypy specimen includes the complete expected seam, including reconcile return typing.
- The negative mypy specimen now carries fifteen independently expected failures, adding wrong datetime, sequence-element and policy-version cases while retaining the earlier cross-layer substitutions.

### T009-F004 — catalogue-backed Decimal native fidelity

- U03 carries canonical `R038` / `Last Size` with native `Decimal("0.00100")` and units `contracts/shares`.
- Same-process proof requires the runtime value to remain Decimal and preserve the exact Decimal tuple as well as the textual coefficient/exponent form.
- U05 carries the same catalogue-backed Decimal specimen through real PostgreSQL and fresh-process restart/readback.
- Canonical comparison requires `Decimal`, value `0.00100`, and tuple `[0, [1, 0, 0], -5]`; coercion to float/string, rounding, exponent loss or another numeric type cannot satisfy the proof.
- This is a native-fidelity canary only. It creates no universal Decimal law, min/max, sign, range or plausibility rule.

## Clean physical-candidate validation

All results below were obtained against exact clean physical commit `816696590912bfac22d9397bef19dc1eb5315f17`.

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

PostgreSQL 17.9 was built from the preserved project source using the preserved Bison/Flex toolchain. The validation cluster ran as `nobody` over a Unix socket; no weaker database substitute was used.

### Product proof control / collection

```text
python tools/validate_product_proof.py
PASS
6 admitted physical families
13 required obligations
13/13 covered
aggregate READY_FOR_PROOF

python -m pytest --collect-only -q tests/product/raw_signal
422 tests collected
```

### Real PostgreSQL expected-red execution

With `NVDA_TEST_POSTGRES_DSN` bound to the exact PostgreSQL 17.9 Unix-socket server:

```text
python -m pytest -q tests/product/raw_signal/test_u05_postgresql_durability.py
18 failed, 6 passed

python -m pytest -q tests/product/raw_signal
410 failed, 12 passed
```

The six U05 green tests include the PostgreSQL environment/isolation controls plus the new server commit-ack barrier canary and private-adapter-capability canary. The eighteen red U05 tests require the absent authorised Raw Signal production seam.

All 410 product-suite failures were classified to deliberately absent authorised production/API symbols (`CaptureScopePolicyV1`, `ScheduledCaptureOccurrenceV1`, `RawObservationOccurrenceV1`, `CaptureReceiptEvidenceRelationV1`, `CaptureReceiptPresenceAssessmentV1`, `RawSignalCatalogueId`, `create_owner`, A00 `create_application`) or static specimens that necessarily remain red while those symbols do not exist. No PostgreSQL connection, namespace, filesystem, fixture, collection or proof-control failure was observed in the completed run.

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

nvda-check-dependencies equivalent registered entrypoint
PASS

nvda-check-public-seams equivalent registered entrypoint
PASS

git diff --check
PASS

git fsck --full --strict
PASS

git status --porcelain
<empty>
```

The dependency/public-seam commands were invoked through their registered Python entrypoint functions with `PYTHONPATH=src:$PWD` because the disposable venv did not install console-script shims. No validator was substituted.

## Boundary

VI-10R7 is frozen as a Worker proof candidate only. `T009-F001..F004` remain open until fresh Tester Iteration 010 independently accepts the physical proof. VI-12R production implementation remains prohibited.
