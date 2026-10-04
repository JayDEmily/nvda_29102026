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
- `list_projected_raw_history(...)` provides bounded deterministic ordering and pagination with optional subject, receipt-cutoff and true-event-cutoff filtering; event filtering refuses observations that do not carry an established `true_instant` rather than fabricating event time;
- the projection performs no D calculation, aggregation, interpolation, window calculation or unit rescaling.

The existing `RawObservationOccurrenceV1` stored payload and identity are unchanged.

## M01 foundation public seam

`nvda_desk.derived_signal_calculation_truth.api` establishes the non-kernel calculation/read foundation required by the accepted brief:

- immutable/version-identified typed context carriers for every admitted clause-6 non-signal input, with context-specific fields rather than identity/version-only shells: `CalculationParameterSetV1` carries its profile and immutable named configured parameters; `RequiredFieldPolicyV1` carries a non-empty distinct requirement set; `CandidateStructureContextV1` carries candidate identity, aligned leg contract/side/quantity data, candidate quantity, premium/entry assumptions and positive risk capital; `CandidateSetContextV1` carries ordered candidate identities, explicit eligibility classes and exact directed neighbour relations; `LivePositionContextV1` carries exact leg contracts, signed quantities, multipliers and M00/current-state occurrence references; `OrderIntentContextV1` carries side/size/urgency; `EntryStateContextV1` carries the exact D155 occurrence reference; `EvaluationSetV1` carries forecast identities, realised-outcome definition, evaluation window, comparator and locked model/version; `RecalculationScheduleV1` carries explicit trigger rules; `PnLConventionVersionV1`, `OptionRevaluationConventionVersionV1`, `ExecutionCostScheduleVersionV1`, `AttributionPathContextV1` and `InputSelectionPolicyVersionV1` carry the corresponding accepted convention/path/selection content;
- explicit `UnitConventionVersionV1` affine conversion requiring exact native-unit match and no magnitude heuristic;
- `CalculationRequestV1` carrying exact D identity, subject, as-of, knowledge cutoff, calculation-definition, parameter-set, input-selection-policy and context-version references;
- `DerivedSignalOccurrenceV1` carrying D identity, opaque occurrence identity, definition/context versions, subject/universe, effective/window/cutoff/calculation times, typed result/units/shape, raw projection lineage, predecessor-D lineage, convention references and optional supersession;
- typed reads by occurrence ID and bounded D history, preserving absence as `None`/empty history rather than fabricating a value;
- an owner factory that requires an M00 raw-projection reader and exposes no external-effect command surface.

`materialise(...)` intentionally returns absence in DS-I01 because no D kernel has yet been admitted by later kernel implementation tasks. This is fail-closed foundation behaviour, not a competing calculation implementation.

## DS-R01 isolated context-contract repair

The first DS-R01 review returned `REPAIR -> DS-I01` for one isolated defect: fourteen admitted context classes carried only `context_id` and `version`, so the public seam could not represent the context-specific clause-6 meanings required by REQ-004 and the admitted work order. The repair is bounded to the existing DS-I01 foundation authority.

The repaired public seam now makes those context meanings constructible and validates load-bearing invariants without choosing calculation kernels or concrete production instances. In particular:

- `CandidateStructureContextV1` accepts and validates candidate identity, aligned leg identities/sides/quantities, explicit candidate quantity, premium/entry assumptions and positive `risk_capital_currency`;
- `InputSelectionPolicyVersionV1` accepts and validates explicit join keys, maximum staleness/skew tolerances, admitted temporal-basis permissions and versioned basket membership;
- candidate-set ordering/eligibility/neighbour identity, live-position leg state, D155 entry anchor, evaluation window/model lock, P&L inclusion/exclusion, option revaluation convention, pre-trade cost schedule and aligned attribution-path references are represented explicitly rather than hidden in implementation defaults;
- all context carriers remain frozen/version-identified, and the repair adds no D-kernel mathematics, no provider-specific fallback, no concrete production mappings/parameters/context instances and no external-effect authority.

The accepted DS-T01 test bytes are unchanged by this repair. Fresh review must therefore challenge the higher-authority context-content proposition directly in addition to the inherited proof suite.

## DS-R01 recurrent foundation-contract repair

The second DS-R01 review classified the remaining defect mechanism as `RECURRENT_CLASS foundation-contract/proof-boundary drift`: accepted Gate-2 semantics were still stronger than the inherited green/shape proof in more than one public contract. Programme Owner authority therefore admitted the bounded proof refinement `DS-T01-R01` before any further source repair, followed by this implementation refinement `DS-I01-R01`.

The accepted refinement proof directly discriminates the complete repaired class boundary without adding kernel semantics. This candidate now additionally establishes:

- M00 projected-history selection can express a true-event cutoff independently from receipt cutoff; a `receipt_only`/`date_only` observation or an unparseable/unauthorised source instant is not assigned a fabricated event instant and is excluded when an event criterion is requested;
- `RawInputLineageV1.raw_signal_id` is restricted to canonical admitted `R001-R323`;
- `CalculationRequestV1.context_refs`, `DerivedSignalOccurrenceV1.parameter_context_refs` and `convention_refs` contain exact typed `VersionRefV1` values and reject duplicate identity/version references;
- persisted raw lineage contains exact `RawInputLineageV1` values; predecessor occurrence IDs and universe members are non-empty/distinct;
- persisted occurrence values exclude `None` because absence is represented by the public read/materialise seam, and runtime validation rejects mutable/float/arbitrary carriers outside the admitted recursive immutable `DerivedResultV1` contract while retaining nested tuple/Decimal/datetime/category/boolean values.

The repair changes only the already-admitted M00 read projection and M01 foundation carrier validation. It does not add provider-specific parsing to M01, any D-kernel implementation, a concrete production mapping/context instance, architecture expansion or external-effect authority.

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
