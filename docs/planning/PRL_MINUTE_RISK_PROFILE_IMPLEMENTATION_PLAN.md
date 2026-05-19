# Parallel Risk Lane minute-level risk profile implementation plan

Status: `implementation_planning`

Branch: `work/prl-minute-risk-profile-plan`

Date: `2026-05-18`

Scope: planning only. This document sequences contract, calculation, service, and test work for enriching the current Parallel Risk Lane (PRL) from a thin independent risk-envelope seam into a richer minute-level environmental risk profiler.

Non-goals: production implementation, test implementation, runtime source mutation, migrations, broad formatting, candidate formation, playbook selection, capital sizing, broker execution, serial-stage mutation, review-layer judgement, and direct workbook/reference reads at runtime.

## 1. Current baseline to preserve

| Baseline | Preserve because | Evidence |
|---|---|---|
| PRL is independent and parallel to serial candidate formation. | The lane may describe environmental risk only. | `docs/03_DOMAIN_MODEL_CORE.md`; `docs/04_TECHNICAL_ARCHITECTURE_CORE.md`; `docs/07_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_CORE.md` |
| PRL does not form candidates or allocate capital. | Core authority boundary. | `src/nvda_desk/contracts/parallel_risk.py`; `src/nvda_desk/risk/parallel/evaluate.py` |
| Current risk envelope states are `tight`, `broad`, `caution`, `block`. | Existing consumers/tests must remain compatible. | `src/nvda_desk/contracts/parallel_risk.py`; `src/nvda_desk/domain/parallel_risk/environment_assessment.py` |
| Current scheduled-event caution behaviour remains. | Regression protection for current temporal-window signal. | `src/nvda_desk/domain/parallel_risk/environment_assessment.py` |
| Current options DTE inversion caution remains. | Regression protection for present options-flow risk seam. | `src/nvda_desk/domain/parallel_risk/environment_assessment.py` |
| Current VIX caution/block behaviour remains until threshold authority is reconciled by a specific leaf. | Avoid silent runtime behaviour drift. | `src/nvda_desk/domain/parallel_risk/environment_assessment.py`; `config/coefficient_authority.v1.yaml` |
| Source temporal truth is preserved rather than replaced by capture/persist times. | Required for minute-level profile lineage and freshness. | `docs/04.1_TECHNICAL_ARCHITECTURE_WORKING.md`; `src/nvda_desk/contracts/temporal.py` |
| Workbook material is reference authority only after typed promotion. | Prevents runtime spreadsheet coupling. | `docs/reference/SIGNAL_WORKBOOK_AUTHORITY.md` |
| Missing/forbidden authority keys remain rejected. | Prevents PRL becoming a trading authority. | `src/nvda_desk/contracts/parallel_risk.py`; `src/nvda_desk/risk/parallel/evaluate.py` |

## 2. Target architecture delta

Target: add a backward-compatible `ParallelRiskMinuteProfile` output surface that packages PRL environmental risk as a minute-local, traceable, non-trading profile.

The delta should introduce:

- first-class risk atom states;
- watched-but-inactive risk atoms;
- risk-family states;
- per-signal snapshots;
- missing/quarantined signal register;
- freshness register;
- event-proximity register;
- contribution breakdown;
- explicit uncertainty summary;
- explicit authority flags;
- plain-English desk-risk description plus mechanical summary;
- lineage and source references.

The delta should not introduce:

- trade recommendations;
- capital percentages or notional sizing;
- broker orders;
- candidate formation or playbook selection;
- direct workbook reads;
- untyped Bloomberg-style signal assumptions.

## 3. Gate 1 — Contract delta plan

| Contract/file | Add/modify | New fields/classes | Source of need | Runtime authority risk | Test required |
|---|---|---|---|---|---|
| `src/nvda_desk/contracts/parallel_risk.py` | Add | `ParallelRiskMinuteProfile` | Accepted audit schema; current packet is too thin for minute risk. | Medium: profile may be misread as decision authority. Mitigate with authority flags and no action fields. | Contract construction, serialisation, authority-default tests. |
| `src/nvda_desk/contracts/parallel_risk.py` | Add | `RiskAtomState` | Required to represent atomic environmental risks independently of plays. | Medium: atom names could drift into play advice. Mitigate with `why_this_is_risk_not_play`. | Atom model validation and no forbidden output fields. |
| `src/nvda_desk/contracts/parallel_risk.py` | Add | `SignalSnapshotEntry` | Required to expose what data the profile saw and whether it was raw/derived/metadata/config/trace. | Low-to-medium: raw signal leakage. Mitigate with lawful-use field and lineage. | Snapshot model test with raw, derived, missing, quarantined cases. |
| `src/nvda_desk/contracts/parallel_risk.py` | Add | `MissingSignalRegisterEntry` | Missing signals must reduce confidence or disable atoms instead of being hallucinated. | Low: descriptive only. | Missing signal creates register entry and data-quality atom. |
| `src/nvda_desk/contracts/parallel_risk.py` | Add | `FreshnessRegisterEntry` | Source/capture/persist fields exist but PRL does not classify freshness. | Low: descriptive only. | Fresh/ageing/stale/unknown classification contract tests. |
| `src/nvda_desk/contracts/parallel_risk.py` | Add | `EventProximityRegisterEntry` | Calendar query has event materiality/proximity not currently projected into PRL. | Medium: event proximity can become trading permission. Mitigate descriptive-only language. | Event proximity register model and no action output tests. |
| `src/nvda_desk/contracts/parallel_risk.py` | Add | `RiskFamilyState` | Needed to summarise temporal, calendar, liquidity, options, macro, information, flow, behavioural, and operational risk families. | Medium: family states could be mistaken for capital gates. Mitigate authority flags. | Aggregation shape test. |
| `src/nvda_desk/contracts/parallel_risk.py` | Add | `ContributionBreakdownEntry` | Current `RiskEnvelopeContribution` is too coarse for atom-level trace. | Low. | Contribution records source signal IDs and atom IDs. |
| `src/nvda_desk/contracts/parallel_risk.py` | Add | `AuthorityFlags` | Required explicit boundary: no candidate, playbook, sizing, order, serial mutation, review judgement, direct workbook read. | Low; reduces risk. | Defaults all forbidden capabilities to `False`. |
| `src/nvda_desk/contracts/parallel_risk.py` | Add | enums/literals for atom state, freshness state, signal availability, signal kind, risk family IDs | Required for deterministic profile shape. | Low. | Literal validation tests. |
| `src/nvda_desk/contracts/parallel_risk.py` | Modify | Optional `minute_profile` field or adapter on `ParallelRiskLanePacket` | Backward-compatible service integration. | Medium if existing consumers break. Mitigate optional field and existing packet unchanged. | Backward-compat tests for existing packet construction. |
| `src/nvda_desk/contracts/parallel_risk.py` | Modify | Extend `ParallelRiskInputTrace` only if existing lineage fields are insufficient | Rich lineage in profile. | Low. | Existing trace tests plus enriched lineage test. |
| `src/nvda_desk/contracts/stage_inputs.py` | Add/modify later | Optional `calendar_context`, `market_substrate_snapshot`, `raw_signal_status` inputs | Event/missing/quarantine registers need typed upstream input. | Medium: hidden upstream reads. Mitigate explicit typed inputs only. | Stage bundle contract tests. |
| `src/nvda_desk/contracts/temporal.py` | Modify later | Optional `detailed_session_phase` or separate phase detail model | Need open-chaos/lunch/close nuance; first leaf may use placeholder. | Low. | Session phase placeholder tests. |
| `src/nvda_desk/contracts/market_substrate.py` | Modify later | Optional freshness/availability annotations | SignalSnapshotEntry may adapt substrate observations. | Low. | Adapter tests, no raw dict rummaging. |

Contract rule: first implementation leaf should add schemas without changing PRL runtime behaviour.

## 4. Gate 2 — Calculation delta plan

| Calculation | Inputs | Output | Existing support | New logic required | Threshold source | Test required |
|---|---|---|---|---|---|---|
| Source freshness scoring | `source_time_utc`, `captured_at_utc`, `persisted_at_utc`, `generated_at_utc`, per-family max age | `FreshnessRegisterEntry`, `freshness_state` | Temporal fields exist. | Calculate age and classify `fresh/ageing/stale/unknown`; first version may use conservative defaults. | New governed config needed; initial defaults local and explicit. | Fresh, stale, unknown, missing timestamp cases. |
| Missing signal register | `missing_fields` from regime/options, absent expected signals, upstream rejection/quarantine | `MissingSignalRegisterEntry`, optional data-quality atom | Missing fields and quarantine exist upstream. | Map missing/quarantine to confidence impact and atom disablement. | Static expected-signal set per current profile version. | Missing fields reduce confidence or emit data-quality atom. |
| Quarantined signal risk | `RawSignalIngressResult.quarantined`, `rejection_reason` | data-quality atom / register entry | Upstream ingress exists. | Adapter from ingress results to PRL register. | N/A. | Quarantined forbidden key is registerable but not consumed semantically. |
| Event proximity intensity | `RuntimeCalendarSnapshot.matches`, `proximity_seconds`, materiality, active windows | `EventProximityRegisterEntry`, event-risk atom intensity | Calendar query/projection exists upstream; not PRL-consumed. | Map active/near/far plus materiality to observe/caution. | Governed event materiality/proximity thresholds later. | Near high-materiality event raises atom; far event only watch. |
| Scheduled-event caution preservation | `TemporalEventWindow.tags` | current caution flag/contribution | Implemented. | Preserve existing flag exactly; enrich with atom wrapper. | Existing hardcoded behaviour until config leaf. | Existing tests remain green; new enriched packet contains equivalent flag. |
| Options DTE risk preservation | `front_dte`, `next_dte` | DTE caution contribution | Implemented. | Preserve current `front_dte > next_dte` rule; wrap as options calendar atom. | Existing hardcoded rule. | Regression for DTE inversion. |
| Current VIX threshold reconciliation | `vix_level`; coefficient authority config | caution/block contribution | Current hardcoded 30/50; config contains separate values. | Leaf 1 preserves current rule; later leaf chooses governed source and migrates tests. | Current hardcoded first; governed config after explicit acceptance. | Regression for current thresholds; reconciliation test pending. |
| Risk atom state calculation | signal cues, freshness, missingness, current envelope contributions | `RiskAtomState` | No current atom catalogue. | Define skeleton atoms for existing supported risks: scheduled event, VIX elevated/extreme, DTE inversion, missing/stale input. | Per-atom thresholds from existing rules/config. | Atom active/watch/inactive tests. |
| Risk family aggregation | atom states, intensities, confidences | `RiskFamilyState` | No current family aggregation. | Max/severity aggregation with confidence floor from missing/stale signals. | New deterministic rule. | Dominant atom sets family state and confidence. |
| Enriched envelope state | family states, current hard blocks/caution flags | `risk_envelope_state`, contributions, hard blocks, caution flags | Existing envelope ladder. | Preserve existing ladder; add atom/family contributions without changing old state. | Existing first. | Existing envelope regression plus enriched contribution check. |
| Coarse-to-detailed session phase placeholder | current `session_state`, source time | `detailed_phase` | Coarse classifier exists. | Add placeholder mapping: detailed phase equals coarse bucket or `unknown`; no VWAP/volume dynamic detail yet. | Existing clock only. | Profile contains detailed phase without claiming unavailable microstructure. |
| Lineage assembly | existing input trace, source refs, parent/dependency IDs | profile lineage | Partial trace exists. | Copy trace into profile and attach signal-level lineage. | N/A. | Enriched packet contains lineage and forbidden list empty. |
| Plain-English risk description | active atoms, family states, uncertainty | description strings | No direct current support. | Deterministic template from atom states; no action verbs. | N/A. | Output contains risk description and no trade/action instruction. |

Deferred calculation rule: VWAP, spread/depth, tape speed, dense options chain, real gamma, skew, OI, MOC imbalance, headline risk, crowding, and cognitive load must be represented as unavailable/missing/watchlisted only until typed runtime inputs exist.

## 5. Gate 3 — Test plan

| Test file | Behaviour under test | Fixture/input | Expected output | Regression protected |
|---|---|---|---|---|
| `tests/tier_a/parallel_risk/test_parallel_risk_minute_profile_contract.py` | New profile contracts instantiate and serialise. | Minimal profile with one atom, one signal, authority flags. | Valid model/dict with expected defaults. | Contract drift. |
| `tests/tier_a/parallel_risk/test_parallel_risk_minute_profile_authority.py` | PRL still cannot form candidates, size capital, issue orders, or select playbooks. | Profile construction plus forbidden-key attempt. | Authority flags false; forbidden fields rejected/absent. | Authority boundary. |
| `tests/tier_a/parallel_risk/test_parallel_risk_evaluation_surface.py` | Existing forbidden authority key rejection remains. | Existing packet with forbidden extensions. | Validation error as today. | No hidden authority regression. |
| `tests/tier_a/parallel_risk/test_parallel_risk_enriched_packet_preserves_current_envelope.py` | Current VIX/event/DTE behaviours remain. | Fixtures for scheduled window, DTE inversion, VIX 30/50. | Same envelope states/flags plus matching atoms. | Existing PRL semantics. |
| `tests/tier_a/parallel_risk/test_parallel_risk_freshness_register.py` | Stale signals identified. | Fresh source time, stale source time, missing source time. | Fresh/stale/unknown states and confidence impact. | Source temporal law. |
| `tests/tier_a/parallel_risk/test_parallel_risk_missing_signal_register.py` | Missing fields reduce confidence or create data-quality atoms. | Regime/options missing fields. | Register entries and data-quality atom; no invented values. | Missing-data hallucination prevention. |
| `tests/tier_a/parallel_risk/test_parallel_risk_event_proximity_register.py` | Event proximity projected descriptively. | Calendar match with materiality/proximity. | Event register and event-risk atom; no trade/capital output. | Calendar integration. |
| `tests/tier_a/parallel_risk/test_parallel_risk_signal_snapshot.py` | Signal snapshot records raw/derived/metadata/config/trace entries. | Temporal, VIX, DTE, missing/quarantined examples. | Entries with lineage, freshness, used-by atom IDs. | Signal auditability. |
| `tests/tier_a/parallel_risk/test_parallel_risk_unavailable_bloomberg_signals.py` | Unavailable Bloomberg-style signals are marked missing/unavailable, not hallucinated. | Expected VWAP/spread/gamma/skew configured unavailable. | Register entries with `not_available_untyped`; no values. | False precision prevention. |
| `tests/tier_a/parallel_risk/test_parallel_risk_workbook_runtime_boundary.py` | Workbook not read directly at runtime. | Monkeypatch/open spy or boundary fixture. | No workbook file access in PRL evaluation path. | Workbook authority boundary. |
| `tests/tier_a/parallel_risk/test_parallel_risk_lineage_profile.py` | Enriched packet contains lineage. | Stage bundle with packet IDs and source refs. | Profile lineage mirrors trace and selected stage IDs. | Auditability. |
| Existing `tests/tier_a/parallel_risk/test_parallel_risk_contract_models.py` | Existing contracts still work. | Current packet fixtures. | Existing tests continue to pass. | Backward compatibility. |
| Existing `tests/tier_a/parallel_risk/test_parallel_risk_lane_service_surface.py` | Service integration remains backward-compatible. | Existing service fixtures. | Existing outputs unchanged unless enriched profile requested. | Consumer compatibility. |

Testing rule: write tests before source implementation for each leaf. Do not add production behaviour without governing tests.

## 6. New or modified services

| Service/file | Change | Purpose | Authority guard |
|---|---|---|---|
| `src/nvda_desk/risk/parallel/evaluate.py` | Add optional enriched-profile assembly path after existing envelope evaluation. | Build `ParallelRiskMinuteProfile` without changing existing envelope semantics. | Reuse forbidden-key validation; do not inspect upstream internals. |
| `src/nvda_desk/services/parallel_risk_lane_service.py` | Add backward-compatible method or flag for minute profile. | Allow current packet consumers to continue while new consumers request enriched profile. | Output descriptive profile only. |
| New `src/nvda_desk/domain/parallel_risk/freshness.py` | Freshness register calculation. | Local deterministic data-quality calculation. | No trading outputs. |
| New `src/nvda_desk/domain/parallel_risk/missing_signals.py` | Missing/quarantine register and data-quality atoms. | Prevent hallucinated unavailable signals. | Register only; no candidate decisions. |
| New `src/nvda_desk/domain/parallel_risk/risk_atoms.py` | Atom skeleton for currently supported risks. | Convert current envelope contributors into atom states. | Atom text must include why risk, not play. |
| New `src/nvda_desk/domain/parallel_risk/family_aggregation.py` | Aggregate atom states into family states. | Machine-readable family profile. | No capital or play permission. |
| New `src/nvda_desk/domain/parallel_risk/event_proximity.py` | Adapt calendar snapshots into event register/atoms. | Enrich event risk from available calendar surfaces. | Requires typed calendar input only. |

## 7. Gate 4 — Implementation sequence

| Leaf ID | Goal | Files likely touched | Tests to add/update | Acceptance criterion | Rollback risk |
|---|---|---|---|---|---|
| PRL-MRP-001 | Add contract-only schema classes/enums. | `src/nvda_desk/contracts/parallel_risk.py` | `test_parallel_risk_minute_profile_contract.py` | New models construct/serialise; existing contract tests pass. | Low; contract addition only. |
| PRL-MRP-002 | Add authority-flag tests and defaults. | `src/nvda_desk/contracts/parallel_risk.py` | `test_parallel_risk_minute_profile_authority.py` | All authority flags false by default; forbidden fields absent/rejected. | Low. |
| PRL-MRP-003 | Add source freshness register domain calculation. | New `domain/parallel_risk/freshness.py`; maybe contracts | `test_parallel_risk_freshness_register.py` | Fresh/stale/unknown states deterministic; no source temporal substitution. | Medium if thresholds disputed. |
| PRL-MRP-004 | Add missing/quarantined signal register. | New `domain/parallel_risk/missing_signals.py`; maybe adapters | `test_parallel_risk_missing_signal_register.py` | Missing fields register; confidence impact; no invented values. | Medium due expected-signal policy. |
| PRL-MRP-005 | Add event proximity register using typed calendar snapshot. | New `domain/parallel_risk/event_proximity.py`; `contracts/stage_inputs.py` optional calendar context | `test_parallel_risk_event_proximity_register.py` | Event materiality/proximity enters PRL descriptively. | Medium; input contract extension. |
| PRL-MRP-006 | Add risk atom skeleton for existing supported risks. | New `domain/parallel_risk/risk_atoms.py`; `environment_assessment.py` adapter | `test_parallel_risk_enriched_packet_preserves_current_envelope.py` | Existing VIX/event/DTE risks appear as atoms without state drift. | Medium. |
| PRL-MRP-007 | Add risk-family aggregation. | New `domain/parallel_risk/family_aggregation.py` | Family aggregation tests | Atom severity maps deterministically to family states. | Low-medium. |
| PRL-MRP-008 | Add enriched packet assembly. | `risk/parallel/evaluate.py`; `contracts/parallel_risk.py` | lineage/profile assembly tests | Existing packet unchanged; enriched profile optional and lineaged. | Medium. |
| PRL-MRP-009 | Add backward-compatible service integration. | `services/parallel_risk_lane_service.py` | service surface tests | Existing service tests pass; new method/flag returns profile. | Medium. |
| PRL-MRP-010 | Add unavailable-signal handling for Bloomberg-style future signals. | Missing-signal domain/config | `test_parallel_risk_unavailable_bloomberg_signals.py` | VWAP/spread/gamma/skew etc marked unavailable, not valued. | Low-medium. |
| PRL-MRP-011 | Reconcile VIX threshold authority. | `config/coefficient_authority.v1.yaml`; PRL config adapter if authorised | threshold reconciliation tests | Current behaviour preserved until explicit threshold migration; config refs documented. | Medium-high; behaviour change risk. |
| PRL-MRP-012 | Update docs/current-state map after implementation. | `NVDA10_CURRENT_STATE_ARCHITECTURE_MAP.md`; docs planning/architecture if authorised | doc/surface tests if any | Documentation states implemented vs missing accurately. | Low. |

Migration order: contracts first, tests second, source calculation third, service integration fourth, documentation last.

## 8. Gate 5 — Do-not-build-yet register

| Signal | Why not now | Required upstream source | Required contract | Future PRL atom |
|---|---|---|---|---|
| VWAP | Workbook/spec/source docs imply it; runtime typed signal absent from PRL. | Intraday trade/quote/VWAP feed or prepared VWAP service. | `MarketMicrostructureContext` or `VwapSignalEntry`. | VWAP reliability risk; VWAP gravity risk. |
| Spread/depth | Raw bid/ask spec exists, but typed runtime projection absent. | NBBO/L2 quote source with sizes and timestamps. | `LiquidityContext` / `QuoteDepthSnapshot`. | Liquidity-poor order book risk; execution fragility risk. |
| Tape speed | Trade count/volume specs exist, but baseline and runtime service absent. | Intraday trades/volume curve. | `TapeSpeedContext`. | Open chaos risk; false-liquidity risk. |
| Dense options chain | Options-chain workbook spec exists, but runtime chain contract absent. | Options chain feed with quote, volume, OI, IV, Greeks. | `OptionsChainSnapshot`. | Options liquidity risk; IV/skew risk. |
| Real gamma exposure | Current gamma calc is not real exposure. | Options chain, OI, Greeks, spot, expiry, model assumptions. | `DealerConvexityContext`. | Gamma flip / dealer acceleration risk. |
| Skew | Current `skew_state` is effectively unknown. | IV by strike/expiry. | `OptionsSkewContext`. | Skew asymmetry risk. |
| OI concentration | Not currently captured. | Option OI by strike/expiry. | `StrikeConcentrationContext`. | Strike pin / magnet risk. |
| MOC imbalance | Not present in repo runtime data. | Closing auction imbalance source. | `AuctionContext`. | Closing auction liquidity-pull risk. |
| Headline risk | Calendar explicitly excludes unscheduled headline facts. | News/headline feed with source/time/reliability. | `HeadlineRiskContext`. | Headline reliability risk. |
| Crowding / real-money flow | Source docs discuss it; repo lacks typed source. | ETF/fund flow/prime/positioning source. | `FlowPositioningContext`. | Crowded deleveraging risk. |
| Cognitive load | Source docs/user prompt imply it; no operator/context signal contract. | Alert density, event density, signal conflict, optional operator-state data. | `CognitiveLoadContext`. | Attention fragmentation / cognitive load risk. |

Do-not-build rule: these signals may appear only as `missing`, `unavailable`, or `watchlisted_untyped` until upstream source, contract, and tests exist.

## 9. Risk and authority guards

| Guard | Required implementation constraint | Test/evidence |
|---|---|---|
| Candidate isolation | No candidate-forming fields/classes/methods in profile. | Authority tests and forbidden field checks. |
| Capital isolation | No deployable percent, notional, or position-size fields. | Forbidden-key regression tests. |
| Order isolation | No broker/order instructions. | Raw ingress and PRL authority tests. |
| Serial-spine preservation | PRL profile consumes typed inputs only; does not mutate serial packets. | Service/evaluate tests. |
| Workbook boundary | Runtime PRL does not open workbook files. | Workbook runtime boundary test. |
| Missing-signal honesty | Unavailable signals are explicit missing/unavailable entries. | Missing/unavailable tests. |
| Source temporal law | Source time, capture time, persist time remain distinct. | Freshness tests. |
| Backward compatibility | Existing PRL packet/envelope output remains valid. | Existing Tier A PRL tests. |
| Description-not-advice | Plain-English summary describes risk and forbids action verbs/output fields. | Text/field authority tests. |

## 10. Acceptance criteria

Implementation can be accepted only after a future implementation branch shows:

1. Contract tests for all new profile/register/atom/snapshot classes pass.
2. Existing PRL contract/evaluation/service tests still pass.
3. Current VIX/event/DTE behaviours are preserved unless an explicit threshold migration leaf changes them with tests.
4. Forbidden authority keys are still rejected.
5. New profile authority flags default to no candidate, no playbook, no capital, no broker execution, no serial mutation, no review judgement, and no direct workbook read.
6. Missing and quarantined signals appear in registers and reduce confidence or disable atoms.
7. Stale signals are identified using source/capture/persist/generated timestamps without substituting one temporal meaning for another.
8. Calendar event proximity enters the profile only through typed calendar context.
9. Bloomberg-style rich signals without typed runtime support are marked unavailable; no values are fabricated.
10. The profile contains lineage/source references for all used signals.
11. Plain-English risk description contains no trade recommendation, order instruction, position-size instruction, or playbook selection.
12. Documentation/current-state map distinguishes implemented, upstream-available, deferred, and out-of-scope surfaces.

## 11. Out-of-scope items

- Implementing the enriched contracts or calculations in this planning task.
- Running production market data or broker connections.
- Adding actual Bloomberg/market-data integrations.
- Building dense options-chain ingestion.
- Calculating real dealer gamma exposure.
- Creating trading strategy/playbook logic.
- Capital allocation or position sizing.
- Rewriting existing normative architecture docs.
- Direct runtime workbook reads.

## 12. Open implementation questions

1. Should `ParallelRiskMinuteProfile` be embedded inside `ParallelRiskLanePacket` or emitted by a sibling service method?
2. What is the first governed source for freshness thresholds?
3. Should VIX threshold reconciliation preserve current 30/50 hardcoded behaviour or migrate to `coefficient_authority.v1.yaml` values in the same implementation tranche?
4. Should calendar proximity use continuous intensity or discrete buckets first?
5. Where should expected-signal inventory live so missing-signal checks are governed but not overfit?
6. Should plain-English risk description be deterministic template-only, or allow later natural-language rendering from atom states?
7. What minimum lineage is required for external consumers: signal-level, atom-level, family-level, or all three?

---

## 14. Resolved design decisions from PRL-MRP-001/002 opening

### 14.1 Expected signal inventory authority

The expected-signal inventory for future missing/unavailable signal checks belongs in the governed Excel signal workbook, not in an isolated code constant or free-floating Markdown table.

Current governed workbook identified for this route:

- `data/reference/signal_workbooks/2026-03-25_NVDA_SIGNAL_WORKBOOK_v3_bounds_handoff_copy.xlsx`

Existing raw-signal / raw-primitives sheet identified:

- `Raw_Primitives_Catalog`

Future required sheet name:

- `Parallel Risk Lane Signal Inventory`

Runtime boundary: the workbook remains governance/reference material. Runtime code must not read the workbook directly. Any runtime use must occur only after typed promotion into config/contracts.

### 14.2 Plain-English risk description authority

Future plain-English desk-risk description output must be deterministic and governed. It must use deterministic templates and vocabulary references; it must not use free-form generative commentary.

Vocabulary governance sources identified for future design before any description engine work:

- `docs/vocabulary/README.md`
- `docs/vocabulary/CONSOLIDATION_WORKFLOW.md`
- `docs/vocabulary/vocabulary_registry.md`
- `data/vocabulary/canonical_vocabulary.json`

Boundary: this implementation leaf records references only. It does not implement a plain-English description engine and does not create trade advice, play-selection, capital-sizing, order-instruction, or review-judgement authority.
