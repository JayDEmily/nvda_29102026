# Chapter 3 — Temporal Truth, Calendars and Provenance

## Chapter role

This chapter separates three temporal questions that the earlier design had allowed to blur together:

1. What market phase or event window is the cognitive system in?
2. When did the source observation actually occur, and with what precision?
3. When did the repository capture, persist or packetise that observation?

The answers use related metadata but remain distinct authorities.

**Primary propositions:** `P-TMP-001`, `P-TMP-002`, `P-TMP-003`, `P-TMP-004`, `P-TMP-005`, `P-PROTO-004`, `P-TMP-006`, `P-TMP-007`, `P-TMP-008`.

## 1. Original temporal model replaced: signal-aware phase becomes Step-1 truth

The first material authority change replaces hard elapsed-minute buckets as cognitive temporal truth. Step 1 classifies temporal state from primitive temporal observables and event facts. Fixed clock buckets may still exist as data or compatibility history, but they no longer decide the market phase merely because a given number of minutes has elapsed. (`P-TMP-001`)

The outward `TemporalContextOutput` remains stable for downstream consumers. That preservation matters: replacement of the internal truth rule does not authorise silent payload breakage, DMP identity changes or inconsistent event-window labels.

Canonical outward language becomes `temporal_state`. `session_clock` may survive only as an explicit compatibility wrapper delegated to that authority. It cannot become a parallel temporal truth or a route back to elapsed-minute classification. No hidden DMP rename or silent API break is permitted. (`P-TMP-002`)

## 2. Event timing develops into class-specific policy

Temporal classification then acquires explicit event classes:

- macro-like events;
- policy events;
- company-like events;
- expiry events;
- venue-session events.

The applied timing profile is review-visible. Macro-like events use a tighter imminent window. Company-like events retain longer same-session and cooling-off windows. The system does not use one generic window for every event merely because the input shape is similar. (`P-TMP-003`)

The calendar authority also carries declared future trading days. A next-session hint cannot be calculated with a weekend-only shortcut. The admitted deterministic examples include a 2026-11-27 half-day followed by 2026-11-30, and a manual 2026-12-24/2026-12-29 calendar yielding `2026-12-29T09:30:00-05:00` after the 24 December close. These examples prove calendar-aware behaviour; they are not a universal holiday table.

The complete numeric durations for every event-class profile are not restated in the admitted corpus and remain unresolved.

## 3. Temporal thresholds become governed policy

Temporal thresholds and timing parameters load through governed identifiers rather than private constants. Behavioural thresholds and clock/timing parameters remain separate policy classes. Where a runtime primitive is expressed as a percentage but the governing authority is expressed in basis points, the conversion is deterministic and explicit. (`P-TMP-004`)

The boundary is equally important. Non-admitted controls, including break-count floors and selected open-window guards, remain visibly outside the governed set. A workbook is research provenance, not direct runtime law. No Asia/Japan coefficient or other external coefficient enters by implication.

The bounded threshold authority preserves exact outcomes:

- at the edge, `gamma_pressure_score=0.95` remains classified `destabilising`;
- the corresponding terminal-risk path reduces `target_fresh_deployable_pct` to `19.6625`;
- the canonical prepared and raw harnesses both produce `event_imminent_window`;
- both have no active playbooks;
- both produce `final_risk=derisk`;
- both produce `target_fresh_deployable_pct=0.0`;
- the prepared-runtime expectation applies across all three prepared snapshots.

These are frozen bounded specimen outcomes after the event-window and terminal-risk evolution. They are not universal defaults and do not widen the admitted coefficient set.

## 4. A provider-agnostic source-time grammar is introduced

The successor corpus adds a separate architecture-level grammar for source-facing and persisted temporal truth. Where applicable, it contains: (`P-TMP-005`)

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

The grammar applies to raw captures, local capture files, derived raw surfaces, persistence records, workbook-derived specimens, replay/proof surfaces and packets where relevant. It supports timestamp-level observations, date-level observations and mixed-date reference-ledger sources. It is not shaped around one provider.

The grammar does not replace signal-aware market phase, event windows or governed threshold semantics. It answers a different question: what temporal fact does this field represent, and how precisely did the source actually provide it?

## 5. Observation, capture, persistence and packet emission remain separate

Source observation, repository capture and persistence are distinct events. They may occur at different times and with different precision. A surface may not collapse them into one timestamp, infer UTC precision from a date-only source or create its own local temporal grammar.

DMPV3 adds another distinct event. `packet.time` is packet emission time. It is not source observation time. Source observation remains separately represented under the canonical source grammar. DMPV3 inherits upstream temporal truth and cannot manufacture source precision merely because the envelope requires an emission timestamp. (`P-PROTO-004`)

The packet-time clock source and precision are not fully specified by the admitted corpus, but the semantic distinction is settled.

## 6. Workbook dates remain field-level reference provenance

Workbook-derived material is not a live same-moment observation. One anchor row may combine fields carrying different source dates. Promotion therefore preserves field-level provenance wherever the dates differ. `source_date` may lawfully carry a date-level observation, but an anchor date cannot be transformed into a common synthetic UTC timestamp for every field. (`P-TMP-006`)

The workbook remains a governed reference ledger. It may support a bounded specimen or proof, but it does not become direct runtime authority and does not acquire precision absent from the source.

## 7. Raw temporal tokens are copied exactly or left null

`source_time_raw` is the exact token supplied by the source artefact. It is not generated from `source_time_utc`, reformatted from `source_date` or replaced with a convenient normalised representation. When the exact token exists, it is copied exactly. When it does not, the field is `None`/`null`. Workbook promotion follows the same rule. (`P-TMP-007`)

This repair closes a subtle but material loophole. A normalised timestamp may be useful, but it is not the same fact as the original source token. Preserving one cannot justify fabricating the other.

## 8. Legacy aliases are retired only at named remediated seams

The active preparation/raw-bundle seam converges on the canonical grammar. Its internal `observed_at` field and reads of `bundle.provenance.observed_at` are retired. No alias, compatibility property, hidden fallback or dual grammar may retain them there. Workbook-derived parallel-risk specimen carriage likewise retires `observed_at` and `next_event_at`; regenerated artefacts must use the canonical grammar. (`P-TMP-008`)

The replacement is deliberately scoped. Names such as `starts_at`, `ends_at`, `recorded_at` or overloaded `emitted_at` are replaced only where they represented one of the canonical temporal facts on a specifically admitted remediated surface. The authority does not establish a repository-wide lexical ban divorced from semantics.

Historical evidence containing old names remains historical evidence. Convergence changes the active seam; it does not rewrite the record.

## 9. Current authoritative position

The temporal model now has a resolved hierarchy:

- Step 1 uses signal-aware temporal state, not elapsed-minute buckets;
- `temporal_state` is canonical outward language and `session_clock` is bounded compatibility only;
- event windows use explicit class-specific profiles and calendar-aware future sessions;
- thresholds and timing parameters come from governed authority with explicit unit conversion;
- exact bounded threshold outcomes remain preserved;
- one provider-agnostic grammar distinguishes source, capture and persistence facts;
- DMPV3 packet time is emission time, not source observation time;
- workbook provenance remains field-level and may be mixed-date;
- `source_time_raw` is exact or null;
- legacy aliases are removed only at named equivalent seams.

## 10. Unresolved matters

The admitted corpus does not fully specify:

- the complete signal-aware classifier formula and state thresholds;
- every event-profile duration;
- all allowed values, ranges and null rules for the source-time grammar;
- complete threshold identifiers and unit rules;
- DMPV3 emission-clock precision;
- every future seam that may require temporal convergence.

These are explicit gaps. They do not permit a return to clock buckets, guessed timestamps, synthetic UTC precision or ungoverned coefficients.

## Cross-references

- Raw capture and workbook authority: [Chapter 2](02_DATA_TRUTH_FROM_SOURCE_TO_STAGE_INPUTS.md).
- Step-1 ownership in the serial spine: [Chapter 4](04_SERIAL_COGNITION_AND_STAGE_OWNERSHIP.md).
- DMPV3 packet carriage: [Chapter 6](06_DMP_PROTOCOL_EVOLUTION_AND_PACKET_CARRIAGE.md).
- Threshold consequences in final risk and capital: [Chapter 7](07_PARALLEL_RISK_TERMINAL_RISK_AND_CAPITAL.md).
- Persisted temporal truth: [Chapter 8](08_EXECUTION_LIFECYCLE_CARRY_STATE_AND_PERSISTENCE.md).
- Workbook specimens and replay lineage: [Chapter 9](09_REVIEW_TRACE_REPLAY_AND_ASSURANCE.md).
- Governed coefficient authority and scoped compatibility: [Chapter 10](10_GOVERNANCE_COMPATIBILITY_AND_PUBLIC_BOUNDARIES.md).
