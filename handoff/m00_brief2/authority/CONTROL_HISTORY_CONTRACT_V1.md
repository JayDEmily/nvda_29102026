# Proposed M00 observation-history read model v1

Status: PROPOSAL FOR INDEPENDENT REVIEW. L04 must first preserve the directly
reached baseline discovery failure, then obtain independent approval of this
exact additive contract before production implementation. No current public
capability, execution result or approval is asserted here.

Authority: original owner-commissioned Brief2 V3 §§1.6,3,4 N08/N09/N15 and
§5 Gates2–3; root ExecPlan L04; current execution commission and separate
M00/G01 binding. Original RawObservationOccurrence.v1 payload law, native
preservation, identity, retry and persistence law remain unchanged. This read
model exposes existing immutable observations; it introduces no new raw
semantic concept, table, broker operation, collector or downstream calculation.

## Exact public addition

In `nvda_desk.raw_signal_occurrence_truth.api`:

```python
@dataclass(frozen=True, slots=True)
class RawObservationHistoryPageV1:
    items: tuple[RawObservationOccurrenceV1, ...]
    next_cursor: str | None

# On the existing create_owner(...).reads facet:
def list_raw_observation_history(
    *,
    subject_instrument: str,
    source_provider: str,
    source_variant: str | None,
    received_at_or_before_utc: datetime,
    native_identity_selectors: tuple[tuple[tuple[str, ...], str], ...] = (),
    limit: int,
    cursor: str | None,
) -> RawObservationHistoryPageV1: ...
```

Export the new page type in this module's `__all__`. Preserve all existing
public factories, arguments, results, v1 payload fields and caller behaviour.
Only private read-facet callback wiring and owner-local implementation need
extend. `create_owner` construction remains unchanged.

## Selection, validation and page semantics

`subject_instrument` and `source_provider` are exact non-empty built-in strings.
`source_variant` is an exact non-empty built-in string or `None`; `None` selects
observations whose variant is absent, never a wildcard. Provider matches the
stored provider identity's string value. Subject, provider, variant, receipt
cutoff and every supplied native selector are AND conditions, applied before
pagination. No request/generation value is inferred from opaque IDs.

The receipt cutoff is an exact aware UTC datetime, inclusive. Its supported
domain is strictly earlier than `datetime.max` with UTC tzinfo. Reject the
unsupported maximum cutoff with `ValueError`; do not silently exclude an
admitted maximum receipt while claiming an inclusive result. Owner-local
enumeration can reuse the existing half-open private transaction query from
UTC datetime.min to cutoff+one microsecond, then apply exact filters. This
explicit bounded domain avoids changing shared persistence protocol or old
projected-history behaviour. No provider event-time filter is introduced;
receipt-only controls are deliberately discoverable by receipt.

`native_identity_selectors` is an exact tuple of exact `(path, expected)` tuples.
Each path is an exact non-empty tuple of non-empty built-in string keys; paths
must be distinct. Each expected value is an exact non-empty built-in string.
An empty selector tuple is allowed. Traverse mappings only; missing path,
non-mapping traversal, wrong value type or unequal value excludes an observation.
No coercion, default, zero/null substitution or semantic broker parsing occurs.
Malformed selector structure/type is rejected with `TypeError` or `ValueError`;
empty expected values or empty/duplicate paths are invalid. String identities are sufficient
for this version's explicitly declared request/generation/exchange carriers;
the method does not claim arbitrary native-value predicate support.

`limit` is an exact positive built-in integer (bool is invalid). Cursor `None`
starts at offset0; otherwise require a non-empty string of ASCII decimal digits,
interpreted as a nonnegative offset in this selected ordered population. Invalid
limit/cursor raises `ValueError`. Sort ascending by `(received_ts_utc,
ingestion_sequence_scope.value, ingestion_sequence,
observation_occurrence_id.value)`, then slice at the offset by limit. Return the
next offset as ASCII digits only when selected rows remain; otherwise `None`.
An offset beyond the population returns empty items and no next cursor.

Complete page exhaustion is guaranteed for a fixed committed population at
fixed selectors/cutoff. The cursor does not establish a multi-call snapshot or
isolation from concurrent ingress. The synthetic producer closes before final
consumer/reopen enumeration. Equal receipt/scope/sequence observations remain
distinct; ID tie-break gives deterministic display order, not causal order or
global sequencing. No committed matching fact may disappear merely because it
has no R role. Empty output means no matching admitted observations in this
query, not source continuity, validity, completeness or health.

The durable branch obtains facts only through the existing owner-local
`transaction(write=False).list_observations_received_between`. SQLite performs
ordinary mode=ro/query_only read transactions. Its create=False constructor
still uses mode=rw for validation; this contract makes no filesystem permission
boundary claim. The memory branch selects the same already admitted immutable
facts. No new persistence method, schema, writes, locking or schedule logic is
required. Retained PostgreSQL adapter compatibility is inspected statically;
no PostgreSQL runtime certification follows.

## Versioned control transport and consumer meaning

The five L01 controls remain byte-identical input/oracle files. Each callback
becomes one existing RawObservationOccurrenceV1 with its explicit control ID,
receipt, scope, sequence, subject, provider, variant, callback and temporal
fields. `native_record` preserves every `native_callback` field at its original
path, plus separately named `_collector` metadata. Synthetic technical choices:
delivery ref `synthetic-delivery:<control_id>`, source product
`TWS_SOCKET_API_SYNTHETIC_SPECIMEN`, native_identifier=subject and
native_tick_series_identifier=request. These are declared harness identities,
not broker-supplied contract or generation parameters. Raw catalogue IDs and
inapplicable source/time/session/units/status/revision metadata remain absent.

The `_collector` mapping has schema_version `collector-control-transport/1`,
origin `synthetic`, subject, request, generation equal to the control's declared
generation_before, requested_exchange `SMART`, and `control` equal to the
separate `m00-control-envelope/1` record. The latter preserves exact kind,
origin, request, generation_before, generation_after and boolean invalidates.
Provider errors carry native reqId101/errorCode317 or316/errorString; reconnect,
gap and restart remain collector-labelled controls with empty native callback.
Nothing fabricates depth `operation=317/316`, an R187 projection, provider time
or an initial/completed book.

A consumer knowing subject/source/request/generation/cutoff queries generic
paths `_collector.request`, `_collector.requested_exchange` and
`_collector.generation` to enumerate depth and controls relative to one another.
It recognises the separately declared control schema from returned immutable
metadata. For a new generation it also queries the same subject/source/request/
exchange with `_collector.control.generation_after=<new generation>` and unions
those results by observation ID with ordinary generation discovery. A G1 query
discovers G1's invalidations and outgoing restart; a consumer starting at G2
discovers its incoming G1→G2 restart boundary without knowing its ID. Earlier
G1 invalidations remain discoverable by querying G1 using that boundary's
generation_before link; they are not falsely returned as G2-native controls.
Generic M00 implements AND predicates only;
the consumer owns this versioned union and control-envelope interpretation.

Invalidates=true records the declared discontinuity affecting the identified
request/generation. A restart boundary links old to new generation; it does not
erase earlier facts or itself prove re-warm-up, subsequent completeness,
continuity, standing book state or availability. Tied clocks/sequence retain
unknown causal order. The control serializer derives actual output only from
publicly returned persisted callback/envelope/collector values; it never copies
input control objects or expected rows into actual results.

## Required L04 proof and bounded correction boundary

The single `test_control_discoverability` first admits A4's four depth events
then five independent controls through real public commands/SQLite. Known-ID
full typed reads and absent R187 are separately checked. The first generic
discovery call is allowed to fail on the unmodified baseline; preserve that
reached result before any implementation. It must subsequently enumerate all
nine exact immutable observations and five literal control outputs, page1/full
exhaustion, with no discovery input containing control IDs. Expected controls
come independently from the L01 oracle and typed observation expectations from
the declared transport and accepted literal depth oracle.

Cutoffs before/at error317 and before/at restart preserve exact prefix results;
G2 consumer selection discovers the restart link independently. Six wrong
subject/provider/variant/request/generation/exchange counterfacts remain
retained but excluded. For the generation counterfact, both before/after links
and mirrored collector generation change consistently. Full typed retained
counterfacts and all selected/prefix/link results are read again in fresh
processes given only database path and selectors/known-ID read queries as
appropriate; database bytes must remain unchanged. Plain control values also
undergo canonical JSON exact comparison and the accepted output schema, avoiding
Python bool/int numeric-equality collapse. Explicit new limit/cursor/maximum
cutoff domain refusals are checked without changing old valid tests.

Independent reviewer must approve source adequacy, preserve the reached
baseline discovery failure, approve this exact compatibility/ownership contract
before production coding, then independently exercise depth→error→restart→
history/cutoff without Worker convenience composition or prior control IDs.
No old test, original claim/generation, frozen guardrail, new owner, v1 payload
shape or consumer migration is authorised by this proposal. Required breaking
changes stop for owner disposition. L05 output publication remains separate.
