# Derived Signal Calculation Truth — DS-I01 foundation implementation candidate

## Status

**CANDIDATE FOR DS-R01 INDEPENDENT REVIEW.**

This candidate implements only the Gate 2 foundation authorised by DS-I01. It does not implement any D001–D209 calculation kernel, activate M01 as composable, select final distribution identity/version, choose production PostgreSQL role/schema names, or authorise external effects.

## Accepted predecessor and authority boundary

DS-T01 is accepted at tag `accepted/DS-T01` and established the executable foundation proof boundary before production implementation. DS-I01 is bound to REQ-003, REQ-004, REQ-005, REQ-008 and REQ-010 and to the admitted M01 architecture/work order.

The implementation preserves the architecture admission:

- semantic owner: `M01`, `derived_signal_calculation_truth`;
- owner package: `nvda_desk.derived_signal_calculation_truth`;
- public seam: `nvda_desk.derived_signal_calculation_truth.api`;
- only owner dependency: `M01 -> M00`;
- M00 remains owner of Raw Signal Occurrence Truth;
- no direct M01 access to M00 PostgreSQL relations is admitted;
- no provider/network/order/account external-effect authority is admitted.

## M00 additive typed projection

`nvda_desk.raw_signal_occurrence_truth.api` gains an additive read-only projection surface:

- immutable `RawSignalProjectionMappingV1` binds one canonical `Rxxx` to one provider/source-variant/native-field path and native-unit meaning;
- `project_raw_value(...)` returns a value only when exactly one mapping matches the requested `Rxxx`, provider and source variant and the mapped native field exists;
- absent or ambiguous mappings, missing observation/catalogue provenance, or missing native field produce no projection rather than a guessed value;
- `ProjectedRawValueV1` preserves source observation identity, mapping identity/version, provider/variant, native field/value/units, subject, temporal metadata, receipt ordering and revision metadata;
- `list_projected_raw_history(...)` provides bounded deterministic ordering and pagination with optional subject and receipt-cutoff filtering;
- the projection performs no D calculation, aggregation, interpolation, window calculation or unit rescaling.

The existing `RawObservationOccurrenceV1` stored payload and identity are unchanged.

## M01 foundation public seam

`nvda_desk.derived_signal_calculation_truth.api` establishes the non-kernel calculation/read foundation required by the accepted brief:

- immutable/version-identified typed context carriers for admitted non-signal inputs;
- explicit `UnitConventionVersionV1` affine conversion requiring exact native-unit match and no magnitude heuristic;
- `CalculationRequestV1` carrying exact D identity, subject, as-of, knowledge cutoff, calculation-definition, parameter-set, input-selection-policy and context-version references;
- `DerivedSignalOccurrenceV1` carrying D identity, opaque occurrence identity, definition/context versions, subject/universe, effective/window/cutoff/calculation times, typed result/units/shape, raw projection lineage, predecessor-D lineage, convention references and optional supersession;
- typed reads by occurrence ID and bounded D history, preserving absence as `None`/empty history rather than fabricating a value;
- an owner factory that requires an M00 raw-projection reader and exposes no external-effect command surface.

`materialise(...)` intentionally returns absence in DS-I01 because no D kernel has yet been admitted by later kernel implementation tasks. This is fail-closed foundation behaviour, not a competing calculation implementation.

## M01 persistence mechanism and ownership separation

`nvda_desk.derived_signal_calculation_truth._postgres` is a private PostgreSQL persistence mechanism. It creates and uses only an M01-owned derived-occurrence table in the connection's current schema and persists the typed occurrence fields/lineage required by the foundation contract.

Persistence semantics implemented here include:

- same occurrence ID + identical content is idempotent;
- conflicting content under the same occurrence ID is rejected;
- reads return absence for unknown identity;
- bounded history is stably ordered;
- the PostgreSQL factory is not exported on the M01 public API.

The implementation does not name or grant production database roles/schemas. The proof environment uses temporary distinct roles/schemas only to establish the accepted separation invariant.

## Lifecycle truth

M01 advances from `placeholder` to `bootstrap` because this task creates the admitted implementation shell while leaving M01 inactive and non-composable. The architecture lifecycle proof is updated accordingly.

The repository bootstrap package-enumeration proof is also updated so source packages owned by either `bootstrap` or `active` architecture objects may physically exist. This aligns the proof with the governing taxonomy; it does not make bootstrap objects active or composable.

The two lifecycle-proof path changes were explicitly authorised by the Programme Owner during DS-I01 and recorded as bounded DS-I01 write-scope additions.

## Deliberate non-claims

This candidate does **not** claim:

- any authoritative D001–D209 kernel result;
- predecessor-D graph execution;
- production provider/native-field mappings or concrete production context/parameter instances;
- production PostgreSQL schema/role names or physical layout;
- final occurrence-ID generation law beyond the typed carrier contract;
- active/composable M01 runtime status;
- final package/distribution name or version;
- downstream action, provider/network, order, cancellation or account authority.

Those matters remain for later governed tasks exactly as the accepted plan requires.

## Review boundary

DS-R01 must independently challenge the exact candidate against the accepted M00 public-seam boundary, mapping ambiguity refusal, explicit unit/version law, occurrence lineage, persistence-role separation, typed absence/result behaviour, lifecycle truth and external-effect exclusion before this foundation is relied upon as independently reviewed implementation state.
