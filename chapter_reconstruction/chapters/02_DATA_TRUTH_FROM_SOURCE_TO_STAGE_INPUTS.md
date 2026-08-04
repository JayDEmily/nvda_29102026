# Chapter 2 — Data Truth from Source to Stage Inputs

## Chapter role

This chapter follows information from first admission through preparation and into cognition. Its governing question is not merely whether a value exists, but whether the system can lawfully say where it came from, whether it is raw or derived, what transformation produced it, and what remains absent.

**Primary propositions:** `P-DAT-001`, `P-DAT-002`, `P-DAT-003`, `P-DAT-004`, `P-DAT-005`, `P-TRACE-001`, `P-TRACE-002`, `P-ARCH-002`, `P-ARCH-007`, `P-ARCH-009`, `P-ARCH-010`.

## 1. Original intention: typed ingress with truth fences

The data path begins with typed ingress contracts for event flags, spot data, peer-equity data, macro data and realised volatility. A proxy is lawful only when it is derived deterministically from an admitted runtime input and carries an explicit provenance or proxy status. Unsupported data remains visibly unavailable. The ingress layer cannot create playbooks, broker behaviour, scheduling or hidden side state. (`P-DAT-001`)

VWAP is the clearest example of the truth fence. VWAP accumulation and VWAP rate-of-change cannot be claimed until the system has actual raw tick-derived state sufficient to produce them. A convenient substitute, an inferred number or a downstream reconstruction from inadequate data is not lawful truth. The exact accumulation, retention and rate-of-change window policies remain unresolved, but the prohibition on fabrication is settled.

## 2. Raw observations and derived features become separate authorities

The design then corrected the inherited tendency to mix observations and calculations in one catalogue. Direct vendor or feed observations belong in raw capture. VWAP, realised volatility, skew, term structure, pin, gamma and participation ratios are derived features. A mixed legacy catalogue may remain for continuity, but it is not authoritative. (`P-DAT-002`)

This separation has a downstream consequence: playbooks consume governed deterministic feature services. They do not reproduce ad hoc chain mathematics locally. Otherwise two playbooks could derive nominally identical concepts differently and the system would lose a single source of truth.

Raw data therefore answers, “What did the source supply?” Derived data answers, “What deterministic transformation did the system lawfully perform?” The two answers may be related, but they are not interchangeable.

## 3. Options capture acquires an explicit density and cadence policy

The raw options design adds same-bucket historical baselines for volume, trade count and spread. During regular trading hours, the front two expiries are captured densely every 30 seconds over a near-spot strike band. Farther tenors are captured more coarsely and only for curve context. (`P-DAT-003`)

Where the vendor supplies them, each raw option row targets:

- expiry and DTE;
- strike and option side;
- bid, ask and last;
- implied volatility;
- delta and gamma;
- open interest and volume.

Vendor-absent fields remain absent. A coarse-tenor row cannot claim dense coverage, and a raw row cannot silently acquire derived-feature authority. The near-spot band width, farther-tenor cadence and retention policy are not specified by the admitted corpus.

## 4. A canonical raw artefact must preserve actual source identity

The next development replaces abstract claims about a raw path with an admitted bounded artefact. A canonical raw artefact must be built from actual repository raw content. It cannot be reconstructed from a workbook, padded with fabricated rows or populated with handwritten prepared values. It preserves source identity, capture time, OHLCV bars, repeated quote-level option-chain snapshots, event rows and timestamp/session anchoring. (`P-DAT-004`)

The frozen specimen identity is:

- symbol `NVDA`;
- source `gate_e_manual_pack`;
- capture time `2026-03-23T13:55:00Z`;
- four bars;
- three option-chain snapshots;
- 30 option-quote rows;
- two event rows.

These values identify one admitted specimen. They are not production defaults and do not establish broader source coverage.

## 5. The lawful source-to-review path becomes explicit

The canonical path is:

`raw bundle -> prepared runtime dataset -> cognition inputs -> review outputs`

Raw input is typed. Preparation occurs through the admitted preparation service. Cognition conversion is explicit. Runtime execution consumes the resulting typed inputs. A hand-injected prepared snapshot cannot stand in as the primary ingress when the claim under test concerns the raw path. Coverage gaps and orphan rows remain visible. Identical inputs must reproduce stable packet IDs, lineage and review output. (`P-TRACE-001`)

The bounded Gate-102 specimen freezes all of the following together:

- aligned chain coverage `100.0`;
- aligned bar coverage `75.0`;
- one visible orphan bar;
- dataset ID `gate102_canonical_raw_runtime`;
- three prepared snapshots;
- first sequence ID `seq-opening-balance`;
- first spot price `116.0`;
- event window `same_session_event_window`;
- options-behaviour cluster `balanced_options_state`;
- permission `allow`;
- target fresh deployable percentage `30.25`;
- `add_candidates` containing only `continuation_ladder`;
- active playbooks containing only `continuation_ladder`.

The specimen and companion fixture prove one deterministic bounded path. They do not establish general runtime defaults, universal coverage or a complete production source population.

## 6. Raw/prepared parity is a declared semantic contract

A parity claim must name the surfaces being compared. The admitted raw/prepared comparison includes:

- temporal input;
- options/flow input;
- regime input;
- inventory state;
- risk-budget-remaining percentage;
- sequence identity;
- stage-packet IDs and lineage;
- review packet and summary;
- event-window state;
- options-behaviour cluster;
- permission state;
- target fresh deployable percentage;
- active playbook IDs.

Identical declared inputs must produce equality across that surface. A later lawful divergence is possible only if it is named and explained. Parity outside the declared surface is not implied. (`P-TRACE-002`)

## 7. Preparation carries one exact normalised feature packet

The prepared substrate carries a provenance-bearing normalised feature packet through preparation and cognition ingress. Its admitted fields are exactly: (`P-DAT-005`)

- `intraday_move_vs_rolling_range_5m`;
- `distance_to_vwap_vs_rolling_range_5m`;
- `intraday_move_vs_price_realised_vol_15m`;
- `front_iv_vs_front_realised_vol_ratio`;
- `next_iv_vs_next_realised_vol_ratio`;
- `atm_straddle_vs_spot_pct`;
- `near_spot_front_volume_share`.

Coverage remains visible to review. Carriage does not imply that each field is already consumed by decision law, that its threshold has been tuned or that additional fields are admitted by resemblance.

The bounded specimen preserves, without converting them into general policy:

- `0.2504` for the first snapshot's intraday move versus rolling range;
- `7.069` for the first snapshot's ATM straddle versus spot;
- `4.644` for the third snapshot's intraday move versus 15-minute realised volatility;
- `1.8438` for the third snapshot's front-IV ratio;
- `100.0%` feature coverage.

The admitted corpus does not restate the formulae, units and validity ranges for all seven fields.

## 8. Infrastructure seams must preserve semantic truth

Typed ingress must distinguish lawful coercion from prohibited payload shape. Persistence seams require explicit commit and rollback behaviour. API dependency seams must translate success and typed lookup failure deliberately rather than leak arbitrary mappings or widen domain authority. These are bounded seam rules, not a claim that every route has identical policy or coverage. (`P-ARCH-002`)

The successor corpus clarifies the ownership sequence: (`P-ARCH-007`)

1. boundary bootstrap and API wiring compose the application;
2. raw ingress decodes and admits source material;
3. preparation produces the runtime substrate;
4. cognition ingress performs semantic translation;
5. the serial runtime consumes typed stage inputs.

Bootstrap does not own runtime orchestration or broker logic. Calendar and reference imports remain reference-authority boundaries rather than ordinary runtime ingress. Compatibility wrappers may survive only when they do not obscure those separations.

## 9. Cognition ingress becomes the explicit translation owner

The current preparation-to-cognition boundary assigns deterministic translation to cognition ingress, not to the serial runtime. Separate temporal, regime and options/flow mappers perform the calculations. A thin coordinator assembles their explicit typed outputs. The serial runtime consumes the resulting bundle and may not reach back into preparation internals. (`P-ARCH-009`)

Lawful absence remains absence. Missing temporal or options truth cannot be replaced by wall-clock fabrication, and missing regime confidence cannot be represented as artificial zero certainty. The coordinator does not become a calculation owner merely because it assembles the stage inputs.

## 10. Regime completeness remains unresolved

The preparation-to-regime seam must represent partial information explicitly. The admitted successor tranche does not settle whether preparation or cognition ingress ultimately owns regime-source completeness. A supportive fixture cannot silently replace the native path or make the seam look complete. (`P-ARCH-010`)

The current authoritative position is therefore two-part:

- cognition ingress owns deterministic translation and explicit typed partiality;
- final responsibility for obtaining complete regime-source truth remains unresolved.

## 11. Current authoritative position

The data path now has a lawful sequence and a set of non-negotiable truth controls:

- source observations and derived features have separate authority;
- unsupported values remain absent or fenced;
- raw options capture has a declared dense/coarse policy;
- the canonical raw artefact preserves actual source identity and cannot be reconstructed from a workbook;
- the raw-to-review path is explicit and deterministic;
- parity is asserted only over a declared comparison surface;
- the normalised feature packet has an exact admitted field set and visible coverage;
- typed infrastructure seams preserve coercion, transaction and translation boundaries;
- cognition ingress owns stage-input translation;
- regime-completeness ownership remains open.

## Cross-references

- Advisory ceilings on context and options: [Chapter 1](01_SYSTEM_PURPOSE_AND_ADVISORY_LIMITS.md).
- Source-time and capture-time distinctions: [Chapter 3](03_TEMPORAL_TRUTH_CALENDARS_AND_PROVENANCE.md).
- Serial consumption of typed stage inputs: [Chapter 4](04_SERIAL_COGNITION_AND_STAGE_OWNERSHIP.md).
- Playbooks consuming governed features: [Chapter 5](05_PLAYBOOKS_POSTURE_MODIFIERS_AND_EXECUTION_CHOICES.md).
- Replay, parity and specimen review: [Chapter 9](09_REVIEW_TRACE_REPLAY_AND_ASSURANCE.md).
- API, compatibility and public boundary governance: [Chapter 10](10_GOVERNANCE_COMPATIBILITY_AND_PUBLIC_BOUNDARIES.md).
