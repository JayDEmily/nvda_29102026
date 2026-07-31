# M02 Authority Worker Record V1

## Assignment

- Programme mode: `MVP_FAST_TRACK`
- Owner module: `M02 calendar`
- Contract boundary: `K04 FinancialCalendarSnapshot`
- Requirements: `N-02; C-005; C-018`
- Source checkpoint: `95e0a866dc7e34c383fd802b2b77a72b661ff18d`
- Active gate: `C-PROOF`
- Checkpoint state: `C_NORM_ACCEPTED`
- Gate D: `OPEN`

## Question

Is numbered authority sufficient to govern the exact four-layer financial-calendar snapshot, owner-issued fact candidates, equal-value coalescence, explicit supersession/fail-closed conflict and deterministic runtime projection without granting calendar code downstream trading authority?

## Pre-change finding

`PARTIAL_AUTHORITY_PRESENT_PUBLIC_BOUNDARY_INCOMPLETE`

Section 03.2.N02 already defines the exact four semantic layers, owners, identity/version requirements, precedence, supersession, failure/degradation and provider/persistence separation. Atlas K04 accepts `FinancialCalendarSnapshot`, `CalendarFactCandidate` and `CalendarProjection` as M02 public interfaces. The remaining gap was an exact numbered runtime/public-contract boundary tying those names to owner/emitter/state/consumer law and governed vocabulary.

## Accepted C-NORM proposition

`M02-K04-NORMATIVE-AUTHORITY-V1`

The accepted proposition is:

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

## 2026-07-31 fast-track C-NORM acceptance

### Disposition

`PASS:C-NORM:M02_K04_FINANCIAL_CALENDAR_AUTHORITY`

Numbered authority now governs the exact K04 public boundary rather than relying on arbitrary layer labels, provider manifests, retained code or historical tests:

- `docs/07.1_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_WORKING.md` section 7.9 defines the three canonical contracts, exact four-layer identity, owner-issued candidate facts, equal-value coalescence, explicit supersession, unresolved-conflict preservation, lawful absence and deterministic projection law.
- `docs/10.1_VOCABULARY_AND_TERM_GOVERNANCE_WORKING.md` section 10.18 admits those exact concepts under namespace `m02` without transferring M01 source authority, M13 transaction mechanics or downstream decision authority.
- `docs/11.1_NATIVE_ARCHITECTURE_BLUEPRINT_WORKING.md` section 11.10.3.3 fixes one explicit K04 public package API and narrows current bundle, packet, snapshot, trace and compatibility surfaces to adapters only.
- `docs/vocabulary/vocabulary_registry.md` and the generated projection admit `m02.calendar_fact_candidate`, `m02.financial_calendar_snapshot` and `m02.calendar_projection`.

### Evidence

- human registry parse and generated projection parity: PASS — 156 entries; namespaces `global`, `m02`, `m04`, `m07`, `m08`;
- M02 scoped vocabulary audit: PASS — zero unresolved candidates across 23 files;
- M02 vocabulary stamp: PASS — stamp matches the clean report;
- static normative assertions and `git diff --check`: PASS;
- M02 production, test, runtime configuration and fixture mutation: none;
- existing vocabulary parity proof: EXPECTED RED — 3 passed / 1 failed because its prior assertion hard-codes namespaces without `m02`.

Exact outputs and the current full-read manifest are under `raw_validation/fast_track_k04_v1/`. No test was changed during C-NORM.

## Gate boundary

C-PROOF is open for the smallest truthful K04 public-seam family. It must prove exact four-layer identity; equal-value coalescence with complete lineage; fail-closed unequal/derived override without lawful supersession; mandatory session authority versus lawful degraded/empty event states; deterministic projection identity; and foreign-authority closure. Gate D remains closed.


## 2026-07-31 fast-track C-PROOF acceptance

### Disposition

`PASS:C-PROOF:GATE_D_OPEN:M02_K04_FINANCIAL_CALENDAR_AUTHORITY`

The minimum truthful K04 proof is now admitted:

- 13 reference and false-positive cases pass;
- six explicit mutants are killed: caller-order selection, derived-source override, missing-session defaulting, unknown-events-as-empty, lineage dropping and foreign-authority leakage;
- vocabulary namespace parity passes 4/4 with the already-admitted `m02` namespace and exact three M02 identities;
- the M02 scoped vocabulary audit remains clean with zero unresolved candidates;
- the registered proof block and all proof-block manifests validate;
- seven production-facing assertions remain exact red solely because `nvda_desk.m02_financial_calendar` does not yet exist.

No production file was changed during C-PROOF. Gate D is open only for the bounded canonical M02 public package and must resolve those seven exact red cases without weakening the reference or mutant proof.
