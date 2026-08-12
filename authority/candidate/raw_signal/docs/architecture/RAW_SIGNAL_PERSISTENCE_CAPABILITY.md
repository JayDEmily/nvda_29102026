# Raw Signal Persistence Capability

Status: **Normative authority — amended 2026-08-07 through the Gate 3 capture-set repair**. This document governs the admitted runtime capability; implementation/test claims require their own evidence.

## 1. Authority and scope

This document defines the first runtime data capability admitted for design after the behaviour-neutral architecture reset. It is governed by, in descending order for this task:

1. the active `PLANS.md` and direct user authority;
2. the architecture-kernel laws and object taxonomy;
3. the cross-module data-identity guidance supplied for this task;
4. `NVDA_80_STEP_ACADEMIC_EVIDENCE_AUDIT_WITH_SIGNALS_ADDENDUM_81_94(1).xlsx`, SHA-256 `519ea9449297d564ae4a02afc1bf4e60e4471631c81a0842620f9fb60bb4f9ae`.

The workbook is normative for the signal/data universe. Its `R001`–`R323` raw rows define the raw observations that this capability must be able to receive and retain. Its `D001`–`D209` rows define downstream information requirements that the retained raw state must be able to support; they do **not** make this capability the semantic owner of those derived calculations.

## 2. Architectural classification and identity

**Classification:** runtime semantic ownership module (`M`).

**Normative identifier:** `M00`.

**Normative name:** `raw_signal_persistence`.

**Future package:** `nvda_desk.raw_signal_persistence`.

**Future typed public seam:** `nvda_desk.raw_signal_persistence.api`.

`M00` is the next unused runtime-module identifier in the reset registry. The reset-era historical crosswalk reclassified the former `M00` application-shell meaning to `A00` and explicitly states that the historical crosswalk must not reserve future runtime semantics. This new `M00` therefore has only the meaning defined here.

The capability is classified as `M`, not `K`, because the persistent records carry domain semantics: source-native identities, signal/data-concept identities, market/session time meaning, revision/vintage meaning, validation disposition and replay lineage. A future `K` object may provide domain-neutral storage or transaction mechanics, but it cannot own these records' semantic meaning. It is not `P`: a protocol may carry the records but cannot own their lifecycle or make persistence/quarantine decisions.

`M00` is **not yet registered or composable** at Gate 1. Registration, proof and implementation are subsequent gates. The reset-era empty-registry validator therefore remains unchanged in this gate.

## 3. Semantic responsibility

`M00` owns the lifecycle of incoming raw signal observations after transport/adaptor translation and before downstream signal derivation. It must:

- accept a typed raw-observation input while preserving the provider-native payload and identifiers needed for audit and replay;
- assign or preserve distinct canonical data-concept, domain-instance, observation-occurrence, payload-contract and lineage identities without conflating them;
- preserve source, market and receipt-time semantics, including explicit absence of a true event instant;
- validate individual observations and related raw-state groups where validity is only detectable cross-record or cross-contract;
- retain accepted and quarantined observations without silently rewriting or deleting source evidence;
- provide deterministic ingestion-order replay and semantically explicit event-time querying;
- retain revision/vintage history and enough ordered observation history to support downstream persistence/change analysis;
- durably record one system capture-set instance for every scheduled 30-second capture slot, including slots for which no live raw data are received;
- expose persisted raw observations and capture-set availability through one typed public seam without leaking owner-private implementation;
- persist the retained occurrence history in PostgreSQL as the normative backing store while keeping physical table/index/partition design subordinate to these semantic laws.

## 4. Explicit exclusions

`M00` does **not** own or perform:

- calculation of any `D001`–`D209` derived signal;
- market-state, regime, probability, scenario, tradeability, structure, sizing, execution or live-control decisions;
- interpretation of news/event content or inferred market-participant intent;
- option-surface fitting, Greeks derivation, dealer-position inference or risk-neutral/physical distribution estimation;
- model calibration, learning, parameter promotion or signal disposition governance;
- provider connection management, entitlement management, network transport, the wall-clock/scheduler that triggers each capture attempt, or application-shell composition;
- DMPV3 protocol semantics or activation;
- domain-neutral database, transaction, clock or idempotency mechanism ownership.

Vendor-calculated values remain raw when the workbook defines them as provider observations ingested unchanged. Preserving those values is not equivalent to `M00` deriving them.

## 5. Inputs and outputs

### 5.1 Typed input contract — `RawObservationInput`

A public input must carry, where applicable to the source row:

- `data_concept_id`: stable canonical concept identity, separate from the workbook alias;
- `workbook_alias`: the applicable historical `Rxxx` alias for traceability;
- `payload_contract_id` and `payload_contract_version`;
- `source_native_identity`: provider/product/endpoint/native identifier/native field/source variant sufficient to reconstruct the source meaning;
- `domain_instance_identity`: instrument, option contract, account, position, order, execution, release, series or other domain instance as applicable;
- `provider_payload`: source-native value(s) and native metadata required for lossless audit/replay;
- `source_timestamp_raw`: preserved verbatim when supplied;
- `source_timezone_native`: preserved when supplied; absence remains absence;
- `event_ts_utc`: nullable; populated only when the source provides enough information for a true instant;
- `event_time_kind`: at least `instant`, `date_only`, or `receipt_only`;
- `receipt_ts_utc`: mandatory collector receipt instant;
- `ingestion_sequence`: mandatory monotonic tie-breaker within the collector ordering domain;
- market/exchange timezone and economically relevant session context where applicable;
- source data status/variant, cadence/frequency, freshness basis and availability semantics where applicable;
- revision/vintage identity where the provider can revise history;
- lineage parent/reference identities where the observation is a revision, replacement or provider-linked occurrence;
- `capture_set_id` when the observation was collected as part of the scheduled 30-second capture path.

A field that is semantically inapplicable may be absent/null. A field whose value is unknown must not be fabricated merely to satisfy a generic shape.

### 5.2 Ingest result — `PersistenceDisposition`

Every ingest attempt returns a typed disposition containing:

- the stable observation occurrence identifier;
- `accepted` or `quarantined` status;
- zero or more machine-readable reason codes;
- the persisted record identity/revision identity;
- enough identity to correlate the disposition with the submitted `RawObservationInput`.

Quarantine is a retained state, not silent discard.

### 5.3 Persisted output — `RawObservationRecord`

A persisted record contains the complete input semantics plus:

- immutable occurrence identity;
- validation/quarantine disposition and reasons;
- persistence/revision lineage;
- storage/replay ordering metadata that does not alter source-native time semantics.

### 5.4 Replay/query contract

The public seam must support typed retrieval/replay by combinations of:

- canonical data concept;
- historical workbook alias;
- domain instance;
- source/provider/source variant;
- receipt-time interval;
- true event-time interval where available;
- trading date/session context;
- revision/vintage;
- accepted/quarantined disposition.

The contract must expose whether returned records have `instant`, `date_only` or `receipt_only` temporal semantics.

### 5.5 Typed public operations

To make the Gate 1 contract executable and testable without exposing owner-private SQL or table design, `nvda_desk.raw_signal_persistence.api` must export these public contract types and operations:

- `RawObservationInput` — concrete typed value object for the input fields in section 5.1; it must be keyword-constructible from the normative field names;
- `RawObservationQuery` — concrete typed value object for the filters in section 5.4 and an optional `available_by_receipt_ts_utc` historical-decision bound; it must be keyword-constructible;
- `PersistenceDisposition` — typed ingest result from section 5.2;
- `RawObservationRecord` — typed persisted output from section 5.3;
- `RawCaptureSetInput`, `RawCaptureSetQuery` and `RawCaptureSetRecord` — concrete typed capture-set values defined in section 5.6;
- `RawSignalPersistence` — typed public capability interface;
- `create_postgres_persistence(dsn: str) -> RawSignalPersistence` — composition operation that constructs the PostgreSQL-backed capability without exposing SQL/table internals. The backing-store name is exposed only at composition; downstream data access remains through the `RawSignalPersistence` interface.

`RawSignalPersistence` must provide these operations:

- `ingest(observation: RawObservationInput) -> PersistenceDisposition`;
- `query(criteria: RawObservationQuery) -> tuple[RawObservationRecord, ...]`;
- `replay_ingestion(criteria: RawObservationQuery) -> tuple[RawObservationRecord, ...]`, ordered deterministically by `(receipt_ts_utc, ingestion_sequence)`;
- `replay_event_time(criteria: RawObservationQuery) -> tuple[RawObservationRecord, ...]`, containing only `event_time_kind=instant` records and ordered by `(event_ts_utc, receipt_ts_utc, ingestion_sequence)` so equal event instants remain deterministic without fabricating time for date-only or receipt-only records;
- `record_capture_set(capture_set: RawCaptureSetInput) -> RawCaptureSetRecord`;
- `query_capture_sets(criteria: RawCaptureSetQuery) -> tuple[RawCaptureSetRecord, ...]`, ordered deterministically by `(scheduled_capture_ts_utc, capture_set_id)`.

`RawObservationInput` uses these exact public field names. Required fields are `data_concept_id: str`, `workbook_alias: str`, `payload_contract_id: str`, `payload_contract_version: str`, `source_native_identity: str`, `domain_instance_identity: str`, `provider: str`, `source_variant: str`, `provider_payload: Mapping[str, object]`, `event_time_kind: Literal["instant", "date_only", "receipt_only"]`, `receipt_ts_utc: datetime` and `ingestion_sequence: int`. Optional fields are `source_timestamp_raw: str | None`, `source_timezone_native: str | None`, `event_ts_utc: datetime | None`, `market_timezone_native: str | None`, `exchange_timezone_native: str | None`, `market_session: str | None`, `trading_date: date | None`, `source_data_status: str | None`, `cadence_frequency: str | None`, `freshness_basis: str | None`, `revision_vintage_identity: str | None`, `lineage_parent_reference_ids: tuple[str, ...]` and `capture_set_id: str | None`. Identity strings are opaque stable identifiers at this seam; they are not physical database keys.

`RawObservationQuery` may leave every filter unset and uses these exact optional public field names: `data_concept_id`, `workbook_alias`, `domain_instance_identity`, `source_native_identity`, `provider`, `source_variant`, `receipt_ts_from_utc`, `receipt_ts_to_utc`, `event_ts_from_utc`, `event_ts_to_utc`, `trading_date`, `market_session`, `revision_vintage_identity`, `disposition`, `event_time_kind`, `available_by_receipt_ts_utc` and `capture_set_id`. Time-bound fields are UTC `datetime` values; `trading_date` is a `date`; `disposition` is `accepted` or `quarantined`; `event_time_kind` uses the three values above.

`PersistenceDisposition` exposes `observation_occurrence_id`, `status`, `reason_codes`, `persisted_record_id` and `persistence_revision_id`. `status` is `accepted` or `quarantined`; `reason_codes` is an ordered tuple of machine-readable strings. `RawObservationRecord` exposes every `RawObservationInput` field plus `observation_occurrence_id`, `disposition`, `reason_codes`, `persisted_record_id` and `persistence_revision_id`. These names make identity and quarantine evidence observable without exposing owner-private storage keys or table design.

When `available_by_receipt_ts_utc` is set, no record or revision received after that bound may be returned. This is the public mechanism required by `RSP-PERSIST-004`; it does not imply that later revisions are deleted or overwritten.

These field names, operation names and signatures are part of the normative public seam. Physical schema, SQL, indexes, transaction layout and pooling remain private implementation detail.

### 5.6 Scheduled 30-second capture-set contract

The system capture clock is a distinct concept from any provider-native cadence. The live collection path schedules **one capture set every 30 seconds** on an exact UTC slot sequence. Provider streams may be faster, slower, event-driven or unavailable; that heterogeneity does not remove a scheduled capture-set slot.

`RawCaptureSetInput` uses these exact public fields:

- `capture_stream_id: str` — stable identity of the live capture stream/collection domain;
- `scheduled_capture_ts_utc: datetime` — the UTC timestamp of the 30-second slot; it must lie on the stream's 30-second schedule and is not a market/event timestamp;
- `recorded_ts_utc: datetime` — the actual UTC instant at which the capture-set availability result is recorded by the persistence capability;
- `availability: Literal["complete", "partial", "unavailable"]`;
- `reason_codes: tuple[str, ...]` — empty for `complete`; non-empty evidence for `partial` or `unavailable`.

`RawCaptureSetRecord` contains every `RawCaptureSetInput` field plus immutable `capture_set_id: str`. `RawCaptureSetQuery` may filter by `capture_stream_id`, `availability`, `scheduled_capture_ts_from_utc` and `scheduled_capture_ts_to_utc`.

A scheduled slot is persisted even when **zero live observations are received**. Such a slot is represented by a `RawCaptureSetRecord` with `availability="unavailable"`, its scheduled UTC slot, its actual recorded UTC instant and one or more machine-readable reasons. `partial` represents a slot in which some expected live data were received but the capture set was incomplete. `complete` represents a capture set the collection path has declared complete.

The capture-set record is the durable evidence that the sampling opportunity existed. It must not fabricate an `event_ts_utc` for missing observations and it must not synthesize a fake raw observation value merely to make the raw-observation table appear dense. Absence is represented explicitly by the capture-set availability record.

For observations produced by the scheduled capture path, `RawObservationInput.capture_set_id` links the observation to its capture set. A single capture set may therefore have zero, one or many raw-observation occurrences. The capture-set availability state and the individual observation disposition (`accepted`/`quarantined`) are independent.

`M00` owns persistence and query of this capture-set ledger. It does **not** own the external wall clock or scheduler that initiates a capture attempt every 30 seconds. The application/collector composition must invoke `record_capture_set` once for every scheduled slot, including a slot where source data are unavailable for any reason while the collection process can report that state. A total process/host outage cannot be written while the process is absent; recovery/backfill of such operational outages requires separate application/operations authority and is not silently invented here.

## 6. Identity law

The following identities are separate and must never substitute for one another:

1. **canonical data-concept identity** — what the observation means across module boundaries;
2. **source-native identity** — provider/product/endpoint/native field/source variant;
3. **payload-contract identity/version** — the schema used to validate/carriage the record;
4. **domain-instance identity** — the particular instrument/contract/account/order/etc.;
5. **observation-occurrence identity** — this specific observed occurrence;
6. **lineage identity** — provenance, revision, replacement and replay relationships;
7. **packet occurrence identity**, if a future admitted protocol carries the record.

Workbook identifiers `R001`–`R323` are normative historical aliases and traceability keys, not the sole cross-module concept identity. The Gate 1 canonical raw concept mapping is in `data/RAW_SIGNAL_CONCEPTS.tsv`.

The four Nasdaq Data Link endpoint rows that expose the same semantic `Ticker symbol` concept intentionally map to the same canonical concept identity while retaining distinct source variants/endpoints. This demonstrates the required separation between concept identity and source-native identity.

## 7. Time and provenance law

### RSP-TIME-001 — UTC computational axis

UTC is the canonical internal instant axis for observations, joins, persistence metadata and event sequencing **when a true instant exists**. Market/exchange timezone, session, daylight-saving context and source timezone remain separately preserved.

### RSP-TIME-002 — no fabricated instants

Date-only inputs remain date-only. Receipt-time-only callbacks remain receipt-time-only. `event_ts_utc` is null where the source does not establish a true event instant.

Examples explicitly required by the workbook include daily historical bars and macro observations that can be date-only, and Level-II callbacks whose local receipt time may be authoritative when no provider event timestamp is supplied.

### RSP-TIME-003 — two replay orders

- **Ingestion replay** is deterministic on `(receipt_ts_utc, ingestion_sequence)` and is valid for every persisted record.
- **Event-time analysis/replay** uses `event_ts_utc` only for records with `event_time_kind=instant`. Date-only and receipt-only records are not assigned invented clock times to force a false total order.

### RSP-TIME-004 — revisions and vintages

Mutable/revisable sources preserve observation value, observation date/time, provider revision/vintage identity and receipt lineage. A latest value must not erase earlier vintages required for look-ahead-safe replay.

### RSP-TIME-005 — scheduled capture time is not event time

Every scheduled live capture set has a `scheduled_capture_ts_utc` on the exact 30-second system capture clock and a `recorded_ts_utc` showing when its availability result was persisted. These timestamps remain valid even when no provider data are received. Neither timestamp may be copied into `event_ts_utc` as a substitute for a missing source event instant.

## 8. Raw-state validation and quarantine

Validation is evidence-preserving. The input payload and relevant context remain retainable even when the disposition is quarantined.

At minimum, where applicable to the source family, Gate 2 behaviour must be derived from these categories:

- malformed or semantically impossible values;
- stale observations or invalid source data-status state;
- crossed/impossible quotes and pathological spreads;
- duplicate observations/occurrences;
- bad ticks and impossible size/price combinations;
- option-chain inconsistencies visible only across related strikes/expiries, including put-call and monotonicity/no-arbitrage checks where the workbook requires them;
- source-variant identity errors, including conflating SMART depth with direct-exchange depth;
- sequence/reset conditions such as the workbook's depth-reset event;
- required timestamp, timezone, revision/vintage or identity omissions where the particular source contract requires them.

A cross-contract inconsistency may arise from stale/asynchronous source state rather than an economically impossible market. The normative response is therefore quarantine/diagnostic preservation, not silent correction.

## 9. Persistence and replay law

### RSP-PERSIST-001 — lossless provider evidence

Persistence must preserve source-native identifiers, native fields, source variant and provider payload required to reconstruct the original observation meaning.

### RSP-PERSIST-002 — immutable occurrence history

An accepted or quarantined occurrence is not overwritten by a later value. Later observations/revisions are new occurrences linked by lineage.

### RSP-PERSIST-003 — deterministic ingest replay

For a fixed persisted occurrence set, ingestion replay returns the same ordered semantic records using receipt UTC and ingestion sequence.

### RSP-PERSIST-004 — revision-safe historical replay

A replay bounded to a historical decision time must be able to select only source observations/vintages that were available by that time; later revisions must not leak backwards.

### RSP-PERSIST-005 — support for persistence/change analysis

The store must retain consecutive observations, gaps, disappearance/reappearance and revision history with sufficient time/sequence identity for downstream owners to determine whether a change appeared once, persisted, strengthened, weakened, disappeared or re-emerged. `M00` does not itself classify those downstream states.

### RSP-PERSIST-006 — PostgreSQL backing store

PostgreSQL is the normative persistent backing store for `M00`. Each retained raw-observation occurrence, including quarantined evidence and revision/vintage lineage required by this authority, must be durably representable in PostgreSQL. In addition, **every scheduled 30-second live capture-set slot must have a durable PostgreSQL capture-set instance even when no live observations are received**. The 30-second cadence belongs to the system capture-set clock; raw source cadences remain heterogeneous and may be event-driven.

The choice of PostgreSQL resolves the storage-technology question only. Physical table layout, indexes, partitioning strategy, connection-pool policy and exact transaction boundaries remain implementation decisions that must preserve the identity, time, quarantine, immutability and replay laws in this document.

### RSP-PERSIST-007 — database access remains owner-mediated

PostgreSQL is an implementation backing store, not a cross-module public API. Downstream owners must obtain raw observations through `nvda_desk.raw_signal_persistence.api`; they must not couple directly to `M00` private SQL, table names or persistence internals. This preserves the kernel law that cross-owner interaction occurs through the target owner's typed public seam.

## 10. Source-variant preservation

The raw mapping preserves source-native variants that are semantically material, including:

- SMART versus direct-exchange depth;
- option bid/ask/last/model computation variants;
- historical-bar `whatToShow` variants;
- market-data live/frozen/delayed state;
- separate Nasdaq Data Link endpoint variants;
- FRED observation/release/vintage identities;
- provider-native date-only versus instant-bearing records.

Source variants are not collapsed merely because their numeric payload resembles another source.

## 11. Dependencies and composition

At Gate 1, `M00` has **no admitted runtime owner dependency**.

`P01` (`dmp_v3`) and `K01` (state/transaction kernel) remain placeholders under the reset and therefore cannot be treated as available dependencies. `A00` may later compose adapters and `M00`, but `M00` must not depend on `A00`.

If later implementation establishes a genuine need for an admitted protocol or technical kernel, that dependency requires an explicit normative amendment, registry declaration and proof before use.

The PostgreSQL decision requires a Python PostgreSQL client dependency at the implementation/dependency gate. Gate 1 does not itself choose or install that package; the dependency must be explicit and pinned in `pyproject.toml` and `uv.lock` before Gate 2 tests rely on it.

### RSP-ARCH-001 — Gate 3 runtime admission

When the Gate 3 implementation exists, `M00` must be admitted in `config/architecture/modules.yaml` as the single active runtime module with package `nvda_desk.raw_signal_persistence`, public seam `nvda_desk.raw_signal_persistence.api` and no runtime-owner dependencies. This is the lawful `AK-EXT-001` evolution from the reset baseline and supersedes only the reset-era assumption that the current module registry must remain empty. `P01` and `K01` remain non-composable placeholders.

The registry-derived composition plan may therefore expose `M00` as composable. This does not move provider connection management or application-shell wiring into `M00`; those exclusions remain binding.

## 12. Relationship to the complete signal universe

The workbook maps:

- 323 raw rows, `R001`–`R323`;
- 209 derived rows, `D001`–`D209`;
- 292 direct raw-to-derived dependency edges;
- 257 derived-to-derived dependency edges.

Every dependency reference resolves to an existing workbook row and the derived dependency graph is acyclic. `data/DERIVED_SIGNAL_REQUIREMENTS.tsv` preserves every downstream derived definition and its direct/ultimate raw support path. `data/SIGNAL_DEPENDENCY_EDGES.tsv` is the complete machine-readable edge set.

Three derived rows have no explicit raw or derived signal dependency in the workbook:

- `D007` Required-field completeness ratio;
- `D204` Brier score for binary probability outputs;
- `D205` Log score / negative log likelihood.

They remain mapped. Gate 1 does not invent signal dependencies for them. Their required non-signal/schema/forecast/outcome inputs are a downstream ownership/contract concern.

## 13. Gate 1 Unknowns

`UNKNOWN-RSP-001` — The workbook leaves the provider for the economic-calendar/consensus rows `R283`–`R289` pending/TBD. `M00` can define the concept/time/provenance contract, but the provider-native contract cannot be finalised until authoritative provider selection exists.

`UNKNOWN-RSP-002` — **Resolved in part by direct user authority on 2026-08-07:** PostgreSQL is the required backing-store technology. Physical schema, indexing, partitioning, pooling and exact transaction implementation remain later implementation choices constrained by this contract.

`UNKNOWN-RSP-003` — The future semantic owners of `D001`–`D209` have not been admitted by the clean kernel. Gate 1 therefore records them as unadmitted downstream requirements rather than assigning ownership speculatively.

`UNKNOWN-RSP-004` — `D007`, `D204` and `D205` do not name explicit signal dependencies in the workbook. No missing inputs are invented here.

`UNKNOWN-RSP-005` — Any future use of `P01` or `K01` depends on their independent admission/activation and cannot be assumed from placeholder identity alone.

## 14. Gate 2 proof obligations derived from this authority

Gate 2 may derive tests for the propositions in this document and the complete mapping only. In particular it must prove:

- exact coverage of `R001`–`R323` and `D001`–`D209`;
- dependency-reference integrity and derived-graph acyclicity;
- identity non-conflation;
- no fabricated event timestamps;
- receipt/sequence deterministic replay;
- source-variant preservation;
- revision/vintage-safe replay;
- accepted-versus-quarantined evidence retention;
- PostgreSQL-backed persistence without exposing database internals as a cross-module API;
- exact 30-second scheduled capture-set persistence, including an `unavailable` zero-observation slot with both scheduled and recorded UTC timestamps and no fabricated event timestamp;
- linkage of scheduled-path observations to their capture set without forcing unrelated event-driven observations into a false 30-second cadence;
- typed public-seam isolation and declared dependency compliance.

No test may add a persistence behaviour, validation rule or dependency not grounded in this Gate 1 authority.
