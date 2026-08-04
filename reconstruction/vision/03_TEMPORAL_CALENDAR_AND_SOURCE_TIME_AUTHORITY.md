# Temporal, Calendar and Source-Time Authority

## Authority propositions

`P-TMP-001`, `P-TMP-002`, `P-TMP-003`, `P-TMP-004`, `P-TMP-005`, `P-TMP-006`, `P-TMP-007`, `P-TMP-008`, `P-PROTO-004`.

Exact lineage is retained in [`../propositions/A04.md`](../propositions/A04.md), [`../propositions/A05.md`](../propositions/A05.md), [`../propositions/A09.md`](../propositions/A09.md), [`../propositions/A12.md`](../propositions/A12.md) and [`../propositions/B08.md`](../propositions/B08.md).

## 1. Signal-aware market phase is the cognitive temporal truth

The first cognitive stage uses a signal-aware temporal-state classifier built from primitive temporal observables. Fixed elapsed-minute buckets are not authoritative market-phase truth. The outward temporal context remains stable for downstream consumers, and event-window labels must remain internally consistent.

Canonical outward naming is `temporal_state`. `session_clock` may survive only as an explicit compatibility wrapper. Compatibility cannot reintroduce elapsed-minute truth, silently rename packet identity or break outward consumers without a declared migration.

## 2. Event-class timing and calendar authority

Event timing is classified through explicit profiles for:

- macro-like events;
- policy events;
- company-like events;
- expiry events;
- venue-session events.

The applied timing profile is review-visible. Macro-like events use a tighter imminent window than company-like events; company-like events retain longer same-session and cooling-off windows. Exact numeric window values are not present in the admitted corpus and remain unresolved rather than invented.

Calendar authority carries declared future trading days so the next-session-open hint is based on the trading calendar, not a weekend-only shortcut. The admitted examples show a 2026-11-27 half-day followed by 2026-11-30, and a manual 2026-12-24/2026-12-29 calendar producing `2026-12-29T09:30:00-05:00` after the 24 December close. These are deterministic examples, not a universal holiday table.

## 3. Governed temporal thresholds

Admitted temporal thresholds and timing parameters load through governed identifiers. Behavioural thresholds and clock/timing parameters remain different classes of policy. Where an observed primitive is a percentage and the authority is expressed in basis points, conversion is deterministic and explicit.

Non-admitted controls, including break-count floors and selected open-window guards, remain visibly outside the governed set. A workbook is research provenance, not direct runtime law. No Asia/Japan coefficient or other external coefficient may enter by implication.

The admitted bounded outcomes are also part of the temporal authority:

- at the threshold edge, `gamma_pressure_score=0.95` remains `destabilising`, and terminal risk reduces `target_fresh_deployable_pct` to `19.6625`;
- the canonical prepared and raw harnesses both produce `event_imminent_window`, no active playbooks, `final_risk=derisk`, and `target_fresh_deployable_pct=0.0`;
- the prepared-runtime expectation applies across all three prepared snapshots.

These are frozen specimen outcomes after event-window and terminal-risk evolution, not general defaults or permission to admit additional coefficients.

## 4. Canonical source-time grammar

Source-facing and persisted temporal truth uses one provider-agnostic grammar, where applicable:

- `source_time_raw`;
- `source_time_kind`;
- `source_timezone_raw`;
- `source_time_utc`;
- `source_date`;
- `captured_at_utc`;
- `persisted_at_utc`;
- `source_provider`;
- `source_channel`;
- `time_granularity`.

The grammar applies consistently to raw captures, local capture files, derived raw surfaces, persistence records, workbook-derived specimens, replay/proof material and packets where the fields are relevant. It must support timestamp-level, date-level and mixed-date reference-ledger sources without being shaped around one provider.

Source observation, packet emission, repository capture and persistence are distinct facts. They must not be collapsed into one timestamp. Provider-supplied raw time and source granularity are preserved where available. No surface may invent precision, apply false UTC normalisation or create a divergent local grammar.

The corpus does not fully enumerate allowed enum values, validation ranges or null rules for several grammar fields. Those details remain unresolved.

## 5. Raw-token and workbook rules

`source_time_raw` is the exact source-supplied token. It is never derived from a normalised UTC value or date. When the exact token is unavailable, the field is `null`; absence is not repaired with a convenient guess.

Workbook dates are reference-ledger provenance. A single anchor row may contain values with different source dates. Field-level provenance must therefore survive promotion. `source_date` may represent a lawful date-level observation, but a mixed-date row cannot masquerade as one live same-moment capture or be assigned a fabricated common UTC time.

## 6. Packet-time rule

For DMPV3, `packet.time` is the packet emission time. It is not source observation time. Any applicable source observation remains separate under the canonical source-time grammar. Packet carriage inherits temporal truth; it does not redefine or enrich it.

## 7. Scoped retirement of legacy aliases

At the admitted preparation/raw-bundle seam, internal `observed_at` and reads of `bundle.provenance.observed_at` are retired. No alias, fallback, compatibility property or dual grammar may keep them alive there. Workbook-derived parallel-risk specimens likewise retire `observed_at` and `next_event_at`.

Names such as `starts_at`, `ends_at`, `recorded_at` or `emitted_at` are replaced only when, on a specifically remediated seam, they were being used as one of the canonical temporal facts. The authority is scoped convergence, not a repository-wide lexical purge.
