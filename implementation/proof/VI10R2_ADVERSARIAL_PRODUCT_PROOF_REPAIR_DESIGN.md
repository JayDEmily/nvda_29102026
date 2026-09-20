# VI-10R2 — Adversarial Product Proof Repair Design

## Status

`AUTHORISED SUCCESSOR PROOF REPAIR — PRE-IMPLEMENTATION`

This successor repairs all eleven findings returned by VI-11R Tester Iteration 004. It preserves the failed VI-10R candidate and review wrapper in ordinary Git history.

## Bound predecessor and unchanged authority

- failed VI-10R physical proof: `375e61b73c219a40c9fc2e9684cf3f3e26d25d54` / tree `a45d5678aedea4e116f5e5a390b2bb6a128c33e4`
- reviewed wrapper: `120966888cff16a6b083ddf670fde302eb7b9bcc` / tree `7ec1c39d2243e8025eddf05bbf919957a6b8c5f8`
- Tester Iteration 004 archive SHA-256: `17be4cd55336d9daee27109fcbc59ae162583af1d2f56b2ab0b5fb37f06262aa`
- Tester Iteration 004 response SHA-256: `86444f62118c52ca1c65ed3557b5c6d064e514a9d9193f2d1a25d2d4973b7814`
- exact accepted IRB/BICP/IWO and routed METHOD-006 normatives remain unchanged.

## Repair law

The repair must make each concrete wrong implementation described by the independent reviewer fail physically. Claims or registry text may not be narrowed to avoid a finding.

### R1 — PostgreSQL is the semantic durable source (`T004-F001`)

U05 must combine two independent discriminators:

1. **direct fact correlation:** unique high-entropy semantic facts written through M00 must be observable in PostgreSQL durable user state, not merely an unrelated heartbeat/count; and
2. **alternative-local-store exclusion:** writer and later reader execute in separate mount namespaces with the repository/root filesystem read-only and only process-local ephemeral writable filesystems, so a shared SQLite/file semantic store cannot carry facts across the boundary.

The later fresh reader must reconstruct the facts through the production owner using the same PostgreSQL durable state. Poisoning PostgreSQL must prevent that read. No physical table/schema name is prescribed.

### R2 — own-transaction commit truth (`T004-F002`)

U05 splits semantic writes at command/process boundaries. After each successful occurrence-producing command and each assessment append:

- the writer process terminates;
- a fresh process reads that just-written fact before any later command is issued;
- a deliberately failing subsequent command is exercised where applicable; and
- the previously committed fact remains durably readable.

Grouped end-of-sequence success cannot satisfy this proof.

### R3 — exact original-fact readback (`T004-F003`)

U05 writes distinctive values across all material policy/capture/observation/assessment fields available in the accepted contracts, including schedule, lineage, native/provenance and temporal fields. Fresh-process reads compare canonicalised complete records, not booleans or IDs only.

### R4 — opaque layer-specific identity types (`T004-F004`)

U01/U03 derive the actual public identity field types from the public contract boundary. Active identity positions must not collapse to `str`, `Any` or one universal wrapper. The same opaque payload text is constructed independently through different layer-specific identity types and substituted across positions; rejection must follow type, not lexeme.

The active matrix covers policy ID/ref, contract ID, concept ID, capture ID, observation ID, assessment ID, provider/source ID and delivery ID. Where BC-015 requires inactive run/replay/packet/workbook/lineage layers, proof-local foreign opaque typed specimens are substituted into active identity positions to establish rejection without admitting those layers as product state.

### R5 — complete five-contract `.v1` compatibility (`T004-F005`)

U01 encodes the accepted compatibility surface for each of the five contracts and parameterises every governed dimension:

- exact requiredness;
- discriminants and complete allowed-value sets;
- every UTC/time constraint, including optional `deactivation_ts_utc` when present;
- null/absence law;
- identity type law;
- lineage/provenance field semantics.

A synthetic compatibility-harness self-test demonstrates that only genuinely optional additive fields with unchanged v1 interpretation are compatible.

### R6 — immutable policy-version re-registration (`T004-F006`)

U02 registers one policy version, proves exact identical re-registration is either idempotent or explicitly rejected without mutation, then separately changes each material immutable content dimension under the same policy ID/version. Every conflicting reuse must fail closed and the original must remain unchanged on reread.

### R7 — optional provider metadata presence preservation (`T004-F007`)

U03 supplies a distinctive lawful non-null value for every optional provider/native metadata field and proves exact owner/read round-trip preservation for each field, alongside the existing lawful-absence cases.

### R8 — local ingestion-sequence monotonicity (`T004-F008`)

U03 proves sequence decrease within one `ingestion_sequence_scope` fails closed, while a lower sequence in an independent scope remains lawful. No global uniqueness/order, overflow or unaccepted sequence semantics are added.

### R9 — effective-policy eligibility authority (`T004-F009`)

U04 uses a recording/asserting eligibility authority that rejects any call not carrying the exact admitted observation plus exact effective active policy/lineage for the capture. A mismatched-but-existing policy reference must fail closed and fabricate no relation.

### R10 — M00 owns semantics; persistence is a technical port (`T004-F010`)

The proof fixes a test-facing dependency-injection seam on public `create_owner` for a technical persistence port. A proof technical adapter exposes storage/read operations only and deliberately provides no eligibility, relation-derivation, assessment-outcome or other semantic-decision capability. U04/U05 demonstrate that M00 has decided semantic relation/assessment facts before persistence receives them.

A static boundary test inspects production persistence/repository/adapter surfaces and rejects imports/calls that move Raw Signal semantic decision helpers or outcome-selection logic into those mechanisms. It must avoid prescribing a physical PostgreSQL schema or filename.

This is a proof-facing construction constraint authorised by the IWO owner/adapter separation; it adds no new product semantics.

### R11 — full A00 semantic argument trace (`T004-F011`)

U06 records and asserts every material argument:

- exact registered-policy result/reference and authoritative slot inputs into capture realisation;
- exact M00-returned capture/observation identities and effective policy reference into relation derivation;
- exact assessment identity, returned capture identity, authoritative evidence-as-of time and supersession input into assessment append;
- exact M00-returned observation identity into final read.

Correct call order with materially wrong IDs/arguments must fail.

## Mutation jurisdiction

Allowed:

- `config/product_proof/families.yaml` only where descriptions/limitations must truthfully match physical proof;
- `tests/product/raw_signal/_support.py`;
- `tests/product/raw_signal/_process_probe.py`;
- the six `tests/product/raw_signal/test_u0*_*.py` physical families;
- VI-10R2 evidence/control/handoff records.

Prohibited:

- `src/nvda_desk/**` production behaviour;
- architecture registries/proof configuration;
- IRB/BICP/IWO/METHOD-006 meaning;
- obligation deletion, tier reclassification or aggregate weakening;
- hard-coding physical PostgreSQL table/schema names as new product law.

## Acceptance before fresh re-review

The successor candidate must:

1. retain exactly six product families and all thirteen accepted product obligations;
2. collect the complete repaired physical suite without harness/collection errors;
3. remain pre-implementation red for attributable missing production capability or mandatory PostgreSQL environment, not malformed proof;
4. keep the architecture axis green and preserve mypy/Ruff/dependency/seam checks;
5. contain no production-source mutation;
6. map every `T004-F001..F011` finding to a physical discriminator and evidence;
7. be committed cleanly and submitted to a fresh independent VI-11R rechallenge before VI-12R.
