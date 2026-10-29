# Additive M02 native-compatible public contract v1

Status: commissioned bounded synthetic compatibility contract; documentary, NOT_RUN. Owner commission `owner-chat/20261028/downstream-reconciliation/execute-entire-plan` and the specifically accepted synthetic receipt/quote/direct/case choices recorded in L01 STATUS govern. These are new public siblings in `nvda_desk.market_measurement_truth.api`. No old factory, V1 request, old brief hash, selector, raw projection, claim or generation is reinterpreted.

The names and signatures below are fixed requirements. Existing `VersionRefV1`, `OwnerAdmissionV1`, `MemoryStorageV1`, `SQLiteStorageV1`, `SQLiteReadStorageV1`, `ExactRatioV1`, `BookSlopePairV1`, `BookRatePairV1` and `VenueConcentrationV1` retain their current meaning. Standard dataclass validation must reject wrong exact primitive types, non-UTC times, duplicate identities and malformed versions. A property annotation does not replace semantic validation.

```python
class NativeRawReaderV1(Protocol):
    def list_projected_raw_history(
        self, raw_signal_catalogue_id: raw_api.RawSignalCatalogueId, *,
        mappings: Sequence[raw_api.RawSignalProjectionMappingV1],
        subject_instrument: str | None,
        received_at_or_before_utc: datetime | None,
        event_at_or_before_utc: datetime | None = None,
        limit: int, cursor: str | None,
    ) -> raw_api.ProjectedRawHistoryPageV1: ...
    def list_raw_observation_history(
        self, *, subject_instrument: str, source_provider: str,
        source_variant: str | None, received_at_or_before_utc: datetime,
        native_identity_selectors: tuple[tuple[tuple[str, ...], str], ...] = (),
        limit: int, cursor: str | None,
    ) -> raw_api.RawObservationHistoryPageV1: ...

@dataclass(frozen=True, slots=True)
class NativeSourceProfileV1:
    ref: VersionRefV1
    provider: str
    variant: str
    subject_instrument: str
    request: str
    generation: str
    ingestion_scope: str
    requested_exchange: str
    security_type: str
    option_right: str | None
    contract_identity: str
    time_basis: str  # exactly 'collector_receipt' for these new profiles
    complete_from_utc: datetime
    warmup_observation_ids: tuple[str, ...]
    warmup_side_levels: tuple[tuple[int, int], ...]
    projection_mappings: tuple[raw_api.RawSignalProjectionMappingV1, ...]
    maximum_observations: int
    source_context_ref: VersionRefV1

@dataclass(frozen=True, slots=True)
class NativeSourceRequestV1:
    source_profile_ref: VersionRefV1
    as_of_utc: datetime
    knowledge_cutoff_utc: datetime

@dataclass(frozen=True, slots=True)
class NativeRawLineageV1:
    raw_signal_id: str
    observation_occurrence_id: str
    projection_mapping_ref: VersionRefV1
    projection: raw_api.ProjectedRawValueV1
    canonical_value: datetime | int | str | Decimal
    time_basis: str
    event_time_utc: datetime | None
    received_ts_utc: datetime

@dataclass(frozen=True, slots=True)
class NativeControlLineageV1:
    observation: raw_api.RawObservationOccurrenceV1
    kind: str
    request: str
    generation_before: str
    generation_after: str
    invalidates: bool

@dataclass(frozen=True, slots=True)
class NativeBookRowV1:
    side: int
    position: int
    price: Decimal | None
    size: Decimal
    mpid: str | None
    requested_exchange: str
    observation_occurrence_id: str

@dataclass(frozen=True, slots=True)
class NativeSourceSnapshotV1:
    owner_object_id: str
    owner_namespace: str
    implementation_brief_sha256: str
    source_snapshot_id: str
    request: NativeSourceRequestV1
    profile: NativeSourceProfileV1
    raw_input_lineage: tuple[NativeRawLineageV1, ...]
    controls: tuple[NativeControlLineageV1, ...]
    standing_rows: tuple[NativeBookRowV1, ...]
    effective_as_of_utc: datetime
    knowledge_cutoff_utc: datetime
    calculated_at_utc: datetime

@dataclass(frozen=True, slots=True)
class NativeQuoteAssemblyV1:
    policy_ref: VersionRefV1
    constituent_occurrence_ids: tuple[str, ...]  # role order R033,R034,R035,R036
    constituent_receipts_utc: tuple[datetime, ...]  # same role order
    maximum_skew: timedelta
    maximum_latest_age: timedelta
    source_context_ref: VersionRefV1

@dataclass(frozen=True, slots=True)
class NativeCalculationRequestV1:
    derived_signal_id: str
    source_profile_ref: VersionRefV1
    as_of_utc: datetime
    knowledge_cutoff_utc: datetime
    depth_levels: int
    band: Decimal | None
    window_seconds: int | None
    side: int | None
    positions: tuple[int, ...]
    predecessor_occurrence_ids: tuple[str, ...]

@dataclass(frozen=True, slots=True)
class NativeMeasurementOccurrenceV1:
    owner_object_id: str
    owner_namespace: str
    implementation_brief_sha256: str
    derived_signal_id: str
    derived_occurrence_id: str
    request: NativeCalculationRequestV1
    definition: CalculationDefinitionV1
    source: NativeSourceSnapshotV1 | None
    quote_assembly: NativeQuoteAssemblyV1 | None
    predecessors: tuple[NativeMeasurementOccurrenceV1 | DerivedSignalOccurrenceV1, ...]
    selected_event_ids: tuple[str, ...]
    result: Decimal | ExactRatioV1 | BookSlopePairV1 | BookRatePairV1 | VenueConcentrationV1
    units: str
    result_shape: str
    effective_as_of_utc: datetime
    knowledge_cutoff_utc: datetime
    calculated_at_utc: datetime
```

`NativeSourceReadsV1` has `get_source_snapshot(source_snapshot_id: str) -> NativeSourceSnapshotV1 | None` and `list_source_history(*, source_profile_ref: VersionRefV1, effective_at_or_before_utc: datetime, knowledge_at_or_before_utc: datetime, limit: int) -> tuple[NativeSourceSnapshotV1, ...]`. `NativeSourceOwnerV1.reads` returns this facet and `.materialise(request: NativeSourceRequestV1) -> NativeSourceSnapshotV1 | None` performs bounded native selection/replay and appends only successful snapshots.

`NativeMeasurementReadsV1` has `get_derived_occurrence(derived_occurrence_id: str) -> NativeMeasurementOccurrenceV1 | None` and `list_derived_history(*, derived_signal_id: str, subject_instrument: str, effective_at_or_before_utc: datetime, knowledge_at_or_before_utc: datetime, limit: int) -> tuple[NativeMeasurementOccurrenceV1, ...]`. `NativeMeasurementOwnerV1.reads` returns this facet and `.materialise(request: NativeCalculationRequestV1) -> NativeMeasurementOccurrenceV1 | None`. Missing/ineligible input or a reached semantic refusal returns None with no appended record; malformed admission/storage fails construction. Each factory recognises only its own exact admitted brief, signal, versioned profile and parameters; this generic carrier is not an open catalogue calculator.

Exact factories (all keyword-only, return native facets above):

```python
def create_native_source_owner(*, admission: OwnerAdmissionV1,
    raw_reader: NativeRawReaderV1, storage: MemoryStorageV1 | SQLiteStorageV1,
    utc_now: Callable[[], datetime]) -> NativeSourceOwnerV1: ...
def create_native_source_reader(*, admission: OwnerAdmissionV1,
    storage: SQLiteReadStorageV1) -> NativeSourceReadsV1: ...

def create_native_option_midpoint_owner(*, admission: OwnerAdmissionV1,
    raw_reader: NativeRawReaderV1, storage: MemoryStorageV1 | SQLiteStorageV1,
    utc_now: Callable[[], datetime]) -> NativeMeasurementOwnerV1: ...  # D087

def create_native_book_depth_owner(*, admission: OwnerAdmissionV1,
    raw_reader: NativeRawReaderV1, predecessor_reader: NativeMeasurementReadsV1,
    storage: MemoryStorageV1 | SQLiteStorageV1,
    utc_now: Callable[[], datetime]) -> NativeMeasurementOwnerV1: ...  # D131

def create_native_smart_depth_owner(*, admission: OwnerAdmissionV1,
    raw_reader: NativeRawReaderV1, storage: MemoryStorageV1 | SQLiteStorageV1,
    utc_now: Callable[[], datetime]) -> NativeMeasurementOwnerV1: ...  # D134

def create_native_smart_ask_owner(*, admission: OwnerAdmissionV1,
    raw_reader: NativeRawReaderV1, storage: MemoryStorageV1 | SQLiteStorageV1,
    utc_now: Callable[[], datetime]) -> NativeMeasurementOwnerV1: ...  # D135

def create_native_smart_imbalance_owner(*, admission: OwnerAdmissionV1,
    bid_reader: NativeMeasurementReadsV1, ask_reader: NativeMeasurementReadsV1,
    storage: MemoryStorageV1 | SQLiteStorageV1,
    utc_now: Callable[[], datetime]) -> NativeMeasurementOwnerV1: ...  # D136

def create_native_book_slope_owner(*, admission: OwnerAdmissionV1,
    raw_reader: NativeRawReaderV1, predecessor_reader: MeasurementReadsV1,
    storage: MemoryStorageV1 | SQLiteStorageV1,
    utc_now: Callable[[], datetime]) -> NativeMeasurementOwnerV1: ...  # D138

def create_native_book_insert_rate_owner(*, admission: OwnerAdmissionV1,
    raw_reader: NativeRawReaderV1, storage: MemoryStorageV1 | SQLiteStorageV1,
    utc_now: Callable[[], datetime]) -> NativeMeasurementOwnerV1: ...  # D139

def create_native_book_delete_rate_owner(*, admission: OwnerAdmissionV1,
    raw_reader: NativeRawReaderV1, storage: MemoryStorageV1 | SQLiteStorageV1,
    utc_now: Callable[[], datetime]) -> NativeMeasurementOwnerV1: ...  # D140

def create_native_direct_venue_owner(*, admission: OwnerAdmissionV1,
    raw_reader: NativeRawReaderV1, storage: MemoryStorageV1 | SQLiteStorageV1,
    utc_now: Callable[[], datetime]) -> NativeMeasurementOwnerV1: ...  # D143

def create_native_microprice_owner(*, admission: OwnerAdmissionV1,
    raw_reader: NativeRawReaderV1, storage: MemoryStorageV1 | SQLiteStorageV1,
    utc_now: Callable[[], datetime]) -> NativeMeasurementOwnerV1: ...  # D137
```

For every native measurement factory above there is the corresponding `create_native_<same_stem>_reader(*, admission: OwnerAdmissionV1, storage: SQLiteReadStorageV1) -> NativeMeasurementReadsV1`. `create_native_smart_imbalance_owner` always takes **two** lawful readers. Native D138 takes actual public D011 via existing `MeasurementReadsV1`; no new D011 semantic profile is created.

## Owner-local durable codec

M02 alone writes native records through its existing `RecordState`/SQLite mechanism. A native namespace and native discriminator separate these records from every original V1 namespace. Exact source snapshot, source profile, raw projection, control observation, datetime, Decimal lexical scale, integer, right/null, mapping, quote membership, predecessor and definition versions survive encode/decode. New typed native codecs may be owner-local siblings. Do not relax the old `_selection.eligible` or coerce old persisted records into native shape. Ordinary `SQLiteReadStorageV1` reopening must reconstruct equal exact types through the native public reader and leave database bytes unchanged. Identity hashes include the semantic payload and versioned profile/brief/definition; exclude only occurrence ID and `calculated_at_utc` as in current owners. No result-only durable representation is sufficient.
