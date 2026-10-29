# VI-10R2 — Adversarial Product Proof Repair Evidence

## Status

`FROZEN SUCCESSOR PHYSICAL PROOF — PENDING FRESH VI-11R2 REVIEW`

This record binds the successor proof-only repair returned from VI-11R Tester Iteration 004. It does not claim proof adequacy acceptance and does not authorise VI-12R production implementation.

## Exact identities

- repair/control baseline: `a4c5ebc0c242c446ce14fee2c341e72ca2764212` / tree `d5a812678aea2de65876f6f77368f92e795ef411`
- frozen physical proof candidate: `56ea445d4bb5055b9fc39114bcd3c529b7f0bae5` / tree `b925e086a734492457dd9633a04743aa0c3c0471`
- reviewed predecessor wrapper: `120966888cff16a6b083ddf670fde302eb7b9bcc` / tree `7ec1c39d2243e8025eddf05bbf919957a6b8c5f8`
- reviewed predecessor physical proof: `375e61b73c219a40c9fc2e9684cf3f3e26d25d54` / tree `a45d5678aedea4e116f5e5a390b2bb6a128c33e4`
- Tester Iteration 004 archive SHA-256: `17be4cd55336d9daee27109fcbc59ae162583af1d2f56b2ab0b5fb37f06262aa`
- Tester Iteration 004 response SHA-256: `86444f62118c52ca1c65ed3557b5c6d064e514a9d9193f2d1a25d2d4973b7814`

## Mutation boundary

The physical candidate changes exactly these nine proof/control paths from the repair baseline:

```text
config/product_proof/families.yaml
tests/product/raw_signal/_process_probe.py
tests/product/raw_signal/_support.py
tests/product/raw_signal/test_u01_contract_owner_boundary.py
tests/product/raw_signal/test_u02_capture_schedule.py
tests/product/raw_signal/test_u03_observation_native_temporal.py
tests/product/raw_signal/test_u04_receipt_assessment.py
tests/product/raw_signal/test_u05_postgresql_durability.py
tests/product/raw_signal/test_u06_a00_composition.py
```

`src/nvda_desk/**` production diff count: `0`.

The six-family decomposition, 13 current product obligations, `NOT_CLASSIFIED` product tier treatment, IRB/BICP/IWO/METHOD-006 meaning and architecture-proof configuration are unchanged.

## Finding-to-physical-discriminator mapping

| Finding | Physical repair / discriminator |
|---|---|
| `T004-F001` — PostgreSQL may merely participate | U05 runs writer/readers in fresh mount namespaces with the host filesystem read-only and process-local tmpfs; requires distinctive semantic markers to exist in discovered non-system PostgreSQL rows; then deletes the correlated `native-record::<token>` PostgreSQL state without assuming a table/schema and requires a fresh reader to stop reproducing the exact original observation. A poisoned PostgreSQL DSN must also prevent fresh semantic read. This rejects local/shared-file state and deterministic reconstruction that merely requires PostgreSQL participation. |
| `T004-F002` — grouped transaction can pass | U05 splits policy, capture, assessment and observation commands across terminating writer processes. Each semantic success is read exactly by a fresh process before the later command. Fault-injected later observation/assessment commands must leave the prior committed fact readable and the failed fact absent. |
| `T004-F003` — incomplete original-fact readback | `_process_probe.py` writes deliberately distinctive policy, capture, observation and assessment facts, including policy lineage, schedule, native/provenance, temporal/order and supersession data. Fresh-process reads canonicalise and compare complete records rather than IDs/booleans. |
| `T004-F004` — lexical string identity separation | U01 derives public identity field types, rejects `str`/`Any`/universal collapse, requires one runtime-distinct type per active identity layer, constructs the same opaque payload independently through each layer type and exhaustively substitutes across active layers. Proof-local typed run/replay/packet/workbook/lineage specimens are substituted into active identity positions. U03 also performs observation/delivery typed substitution. |
| `T004-F005` — incomplete `.v1` compatibility | U01 parameterises requiredness across all five contracts; every UTC field including optional policy deactivation; exact finite discriminant/allowed-value sets and accepted values; invalid discriminants; conditional time/null law; concept/contract exact-value discrimination; active identity typing/substitution; provenance requiredness; lawful optional absence; and the optional-addition compatibility invariant. |
| `T004-F006` — mutable same policy ID/version | U02 re-registers the same policy ID/version while independently changing activation, deactivation and eligibility lineage; each conflict must fail and exact original reread must remain unchanged. Identical re-registration may only be idempotent or reject without mutation. |
| `T004-F007` — optional metadata presence not proved | U03 parameterises every accepted optional provider/native metadata field with a distinctive non-null value and proves exact stored+reread preservation; the companion absence case proves lawful `None` remains absence. |
| `T004-F008` — local ingestion ordering not discriminated | U03 rejects a lower ingestion sequence arriving later within the same typed scope and separately proves a lower sequence is lawful in an independent typed scope. |
| `T004-F009` — wrong effective-policy eligibility authority | U04 injects a recording/asserting eligibility authority that accepts only the exact admitted observation and exact stored effective policy object. Relation output must carry the capture's effective policy reference. A mismatched but existing policy version cannot authorise or mis-lineage the relation. |
| `T004-F010` — persistence mechanism may own Raw Signal semantics | U04 injects an explicit technical persistence port with storage/read methods only and requires already-decided assessment outcomes at the append boundary. U05 requires public persistence-port injection and statically rejects Raw Signal outcome/eligibility decision literals/names in production persistence/repository/adapter mechanisms. No physical PostgreSQL schema is prescribed. |
| `T004-F011` — A00 may miswire arguments while preserving order | U06's spy command/read facets record every material call argument. It requires authoritative policy/slot/capture/assessment/as-of/supersession inputs and exact M00-returned capture ID, observation ID and effective policy reference to flow into subsequent commands/readback, while also asserting exact call order and returned object identity. |

## Exact clean-candidate validation

Validation was run from clean commit `56ea445d4bb5055b9fc39114bcd3c529b7f0bae5`.

- `python tools/validate_product_proof.py` — `PASS`; 6 admitted families, 13 required obligations, 13/13 covered; aggregate `READY_FOR_PROOF`.
- `python -m pytest --collect-only -q tests/product/raw_signal` — `353 tests collected` with no collection error.
- `python tools/run_product_proof_gate.py --aggregate raw_signal_occurrence_truth_product` — return code `1`, expected pre-implementation red: `347 failed, 6 passed`. Failures remain attributable to the absent M00/A00 production seam and mandatory `NVDA_TEST_POSTGRES_DSN`, not collection/harness corruption.
- `python tools/validate_architecture.py` — `PASS`.
- `python -m pytest -q tests/architecture tests/bootstrap` — `74 passed`.
- `python tools/run_promotion_gate.py --set architecture_kernel` — `74 passed`; promotion set resolves all 11 admitted architecture/bootstrap paths.
- `python -m mypy src` — `Success: no issues found in 15 source files`.
- `ruff check src tests tools` — `All checks passed!`.
- `python tools/check_dependencies.py` — `PASS: dependency direction and cycle validation`.
- `python tools/check_public_seams.py` — `PASS: public-seam validation`.
- `git diff --check` — clean.
- post-validation `git status --porcelain=v1` — empty.

## Execution boundary

The worker does **not** claim that the eleven findings are independently closed. This candidate must be challenged by a fresh independent VI-11R2 reviewer against the exact accepted authority and complete proof surface. VI-12R remains prohibited until that reviewer returns an accepted `PASS` disposition.
