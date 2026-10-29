# VI-10R3 Adversarial Product Proof Repair Evidence

## Status

`FROZEN WORKER CLAIM — PENDING FRESH VI-11R3 INDEPENDENT REVIEW`

This record binds the VI-10R3 proof-only successor to one immutable physical proof candidate. It does not claim proof adequacy has been independently accepted and does not authorise VI-12R implementation.

## Exact candidate

- repair checkpoint / parent: `d35153c6a15818c7b6b230bda79d07650f58ea6d` / tree `34b28cca978ee5dbe39eaae2703458dec1bd9bbb`
- frozen VI-10R3 physical proof commit: `ffcbc64b77b66f96c91926b423622281f125d757`
- frozen physical proof tree: `7884c38a5edf6a3538bc2acc6a3bc57a079ea888`
- failed VI-10R2 physical predecessor preserved in history: `56ea445d4bb5055b9fc39114bcd3c529b7f0bae5`
- reviewed VI-10R2 wrapper preserved in history: `c164facaf011f2dc2da7ebcb2d90790b755c8782`

The physical diff from `d35153c6...` to `ffcbc64b...` contains exactly:

```text
config/product_proof/families.yaml
tests/product/raw_signal/_process_probe.py
tests/product/raw_signal/test_u01_contract_owner_boundary.py
tests/product/raw_signal/test_u02_capture_schedule.py
tests/product/raw_signal/test_u03_observation_native_temporal.py
tests/product/raw_signal/test_u04_receipt_assessment.py
tests/product/raw_signal/test_u05_postgresql_durability.py
tests/product/raw_signal/test_u06_a00_composition.py
```

No `src/**`, architecture registry, architecture-proof configuration, IRB, BICP, IWO or METHOD-006 normative byte changed in the physical candidate.

## Tester Iteration 005 finding-to-discriminator map

The entries below are Worker claims for fresh review, not accepted dispositions.

### T005-F001 — PostgreSQL semantic durable source

Physical discriminator:

- `test_postgresql_is_only_configured_cross_process_semantic_source_for_complete_facts` creates parent-held high-entropy semantic facts independent of query identities;
- child writer/reader environments are stripped of service credentials and receive the PostgreSQL DSN only through the probe payload;
- every isolated child runs in its own user/mount namespace with `/mnt/data` remounted read-only and `/tmp`, `/var/tmp` and `/dev/shm` replaced by process-local tmpfs scratch, preventing shared local durable state through the project/data filesystem;
- fresh readers receive query identity rather than the original high-entropy facts and must reproduce complete canonical records from the configured durable path;
- the proof directly confirms correlated high-entropy facts exist in PostgreSQL user-table state and destroys correlated PostgreSQL semantic state to require exact reproduction to cease;
- `test_owner_package_has_no_alternate_durable_backend_or_external_semantic_service` and the technical-module closure checks reject alternate configured file/network durable mechanisms in the owner package.

### T005-F002 — each command committed before success

Physical discriminator:

- `test_each_command_is_visible_before_writer_shutdown_and_matches_prewrite_authority` runs one public semantic command in a hold-open writer process, receives its success result while that writer remains alive, verifies no open PostgreSQL transaction exists for that writer application name, and reads the fact from a separate process before permitting writer shutdown;
- policy, capture, zero-assessment, observation and one-assessment writes are separated into individually observable commands;
- relation derivation and assessment append are separate probe actions;
- reconciliation has a `fail_after_occurrence_commit` barrier proving recovered capture durability before the unknown assessment append.

### T005-F003 — independent pre-write durable oracle

Physical discriminator:

- `_authoritative_facts()` creates independent high-entropy source facts in the parent;
- `_expected_records()` canonicalises policy/capture/observation/assessment expectations before writer execution;
- fresh readback is compared to those parent-held expectations, not to writer-returned records.

### T005-F004 — complete `.v1` compatibility / UTC discrimination

Physical discriminator:

- U01 treats the accepted `.v1` field set as closed absent separate authority; every unproved added field is incompatible;
- parameterised required/null/discriminant/identity/provenance checks span all five contracts;
- every `_utc` field is challenged with both naive datetime and timezone-aware non-UTC offset values.

### T005-F005 — per-scope ingestion monotonicity survives interleaving

Physical discriminator:

- `test_ingestion_sequence_high_water_survives_scope_interleaving` exercises `A:10`, `B:1`, `A:9` rejection, then `A:11` acceptance.

### T005-F006 — semantic decisions cannot hide in technical persistence

Physical discriminator:

- `test_complete_technical_persistence_closure_contains_no_semantic_decision_logic` discovers the technical closure from modules that import Psycopg and recursively follows local imports rather than selecting filenames;
- `test_owner_package_has_no_alternate_durable_backend_or_external_semantic_service` rejects unadmitted alternate durability/service mechanisms;
- `test_default_postgresql_path_exposes_same_semantic_free_storage_protocol` inspects the actual default persistence-port object graph and requires the same storage-only protocol shape used by the injected proof port;
- U04 verifies persistence receives already-decided semantic records and exposes no eligibility/outcome decision capability.

### T005-F007 — A00 policy reference consistency

Physical discriminator:

- U06 traces every material downstream argument;
- `test_a00_rejects_caller_policy_ref_that_disagrees_with_registered_policy` supplies an intentionally mismatched caller policy reference and requires rejection before capture realisation, so a caller reference cannot silently override the registered policy identity/version.

### T005-F008 — policy validity and version boundary

Physical discriminator:

- U02 rejects unaligned activation/deactivation and deactivation at/before activation;
- `test_v2_owns_first_slot_at_activation_boundary_and_v1_stops_before_it` proves the exact v1/v2 take-effect boundary and that neither version may claim the other's slot.

### T005-F009 — complete half-open receipt interval / typed missing capture

Physical discriminator:

- U04 checks receipt immediately before slot start and at slot end as lawful no-relation cases;
- missing-capture proof uses a correctly typed but nonexistent capture identity so the negative reaches referential existence rather than failing only type validation.

### T005-F010 — assessments depend on eligible committed receipt evidence

Physical discriminator:

- `test_ineligible_or_out_of_slot_raw_observation_does_not_make_one_or_more` appends assessments after ineligible, pre-slot and at-end observations and requires `zero_received`;
- only eligible in-slot committed evidence may produce `one_or_more_received`.

### T005-F011 — exact restart-reconciliation facts

Physical discriminator:

- reconciliation returns/readbacks the complete recovered capture;
- parent-held expected capture binds exact capture identity, policy reference and slot start/end;
- the unknown assessment must reference that exact recovered capture;
- the injected post-capture barrier demonstrates capture commit precedes assessment append.

## Clean-candidate validation

The following was run against exact commit `ffcbc64b77b66f96c91926b423622281f125d757` with a clean Git worktree.

### Product proof control and collection

```text
python tools/validate_product_proof.py
PASS
6 admitted physical families
13 required obligations
13/13 covered
aggregate state READY_FOR_PROOF

pytest --collect-only -q tests/product/raw_signal
373 tests collected
```

### Real PostgreSQL proof environment

PostgreSQL source archive:

```text
postgresql-17.9.tar.bz2
SHA-256 3b9a62538a8da151e807a3ddb1198e8605f2032544d78f403ae883d27ecf1ee4
```

The source was built locally for this proof run. The fresh non-root cluster reported:

```text
server_version       17.9
fsync                on
synchronous_commit   on
full_page_writes     on
```

With `NVDA_TEST_POSTGRES_DSN` bound to that server:

```text
pytest -q tests/product/raw_signal
364 failed, 9 passed
```

There were zero collection errors, zero missing-DSN failures, zero mount/isolation failures and zero module-import failures. The 364 failures classify as:

- 358 direct missing M00 public-seam failures;
- 3 subprocess-wrapper failures whose underlying traceback is the same missing `create_owner` M00 seam;
- 3 missing A00 `create_application` production-composition failures.

This is expected pre-implementation red evidence only. It does not prove proof adequacy or implementation correctness.

Product execution log SHA-256:
`9f770c0d13bbe4a589f2cc7c843ba35aab76fe02d57e35747fb6b23f2dfdda2f`.

### Separate architecture/static axis

```text
python tools/validate_architecture.py
PASS

pytest -q tests/architecture tests/bootstrap
74 passed

python tools/run_promotion_gate.py --set architecture_kernel
74 passed; promotion set resolved 11 test paths

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

git status --porcelain=v1
<empty>
```

Architecture promotion log SHA-256:
`9f48328001a3afde7cbf177ffbfc96d475677be38818ec27961223bd5dd399ab`.

## Boundary

VI-10R3 is frozen as a Worker proof candidate only. `T005-F001..F011` remain open until a fresh independent VI-11R3 reviewer accepts the physical proof. VI-12R production implementation remains prohibited.
