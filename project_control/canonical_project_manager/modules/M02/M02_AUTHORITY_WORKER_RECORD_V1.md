# M02 Authority Worker Record V1

## Assignment

- Programme mode: `MVP_FAST_TRACK`
- Owner module: `M02 calendar`
- Contract boundary: `K04 FinancialCalendarSnapshot`
- Requirements: `N-02; C-005; C-018`
- Source checkpoint: `95e0a866dc7e34c383fd802b2b77a72b661ff18d`
- Active gate: `C-NORM`
- Checkpoint state: `DRAFT_IN_PROGRESS_NOT_ACCEPTED`
- Gate D: `CLOSED`

## Question

Is numbered authority sufficient to govern the exact four-layer financial-calendar snapshot, owner-issued fact candidates, equal-value coalescence, explicit supersession/fail-closed conflict and deterministic runtime projection without granting calendar code downstream trading authority?

## Pre-change finding

`PARTIAL_AUTHORITY_PRESENT_PUBLIC_BOUNDARY_INCOMPLETE`

Section 03.2.N02 already defines the exact four semantic layers, owners, identity/version requirements, precedence, supersession, failure/degradation and provider/persistence separation. Atlas K04 accepts `FinancialCalendarSnapshot`, `CalendarFactCandidate` and `CalendarProjection` as M02 public interfaces. The remaining gap was an exact numbered runtime/public-contract boundary tying those names to owner/emitter/state/consumer law and governed vocabulary.

## Draft C-NORM proposition

`M02-K04-NORMATIVE-AUTHORITY-V1`

The current draft proposition is:

1. M02 owns `CalendarFactCandidate`, `FinancialCalendarSnapshot` and `CalendarProjection` meaning.
2. A candidate belongs to exactly one governed layer and carries explicit semantic-key, value/absence, temporal, source/version, validation and supersession facts.
3. A snapshot binds exactly `market_session_reference`, `financial_event_reference`, `operational_calendar_state` and `derived_runtime_calendar_context`; storage or packet shapes do not create extra layers.
4. Equal candidates may coalesce only under an explicit comparison rule and must preserve all lineage.
5. Unequal candidates require lawful version selection or explicit operational supersession; caller order, capture recency, non-empty value and derived context cannot decide precedence.
6. Mandatory unresolved conflict or missing session authority withholds projection. Unknown event completeness is not `no events`; reference-only degraded mode requires explicit policy.
7. Projection is deterministic and side-effect-free, preserves selected/conflict/missing lineage and grants no candidate, risk, capital, execution, position or lifecycle authority.
8. M13 participation, where used, provides transaction mechanics only and does not own calendar facts.

## Direct current implementation observation

- `src/nvda_desk/contracts/reference_data.py` has no exact K04 public contracts or four-layer enum.
- `BundleLayerReference.layer_id` accepts arbitrary labels.
- `src/nvda_desk/calendar/reference/projection.py` projects checked rows but has no governed equal-value coalescence or explicit supersession/conflict law.
- `src/nvda_desk/calendar/operational/events.py` provides bounded volatile query state but no explicit owned composition from reference projection.
- Existing C-005/C-018 proof is therefore expected red until C-PROOF/Gate D.

## Pause boundary

At this checkpoint, the authority/vocabulary amendment and pre-change read manifest are drafted but C-NORM has not been accepted, validated or recorded in the active ExecPlan, roadmap or validation log. No M02 production source, runtime configuration, fixtures or physical proof has changed.

## Gate boundary

C-NORM changes numbered authority, vocabulary and programme records only. It does not alter M02 production source, runtime configuration, fixtures or physical proof. Gate D remains closed until the minimum truthful C-PROOF is accepted.
