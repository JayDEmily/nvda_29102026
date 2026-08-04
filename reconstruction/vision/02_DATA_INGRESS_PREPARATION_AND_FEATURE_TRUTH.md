# Data Ingress, Preparation and Feature Truth

## Authority propositions

`P-DAT-001`, `P-DAT-002`, `P-DAT-003`, `P-DAT-004`, `P-DAT-005`, `P-TRACE-001`, `P-TRACE-002`, `P-ARCH-002`, `P-ARCH-007`, `P-ARCH-009`, `P-ARCH-010`.

Exact lineage is retained in [`../propositions/A01.md`](../propositions/A01.md), [`../propositions/A04.md`](../propositions/A04.md), [`../propositions/A08.md`](../propositions/A08.md), [`../propositions/A09.md`](../propositions/A09.md), [`../propositions/B02.md`](../propositions/B02.md) and [`../propositions/B09.md`](../propositions/B09.md).

## 1. Ingress truth and ownership

Ingress exposes typed contracts for event flags, spot data, peer-equity data, macro data and realised volatility. A value may be proxied only from a deterministic runtime input and must carry an honest provenance or proxy status. The ingress layer cannot create playbooks, broker behaviour or hidden side state.

Raw-source decoding, runtime preparation and cognition ingress are separate responsibilities:

1. raw ingress decodes and admits source observations;
2. preparation deterministically produces the prepared runtime substrate;
3. cognition ingress translates that prepared substrate into explicit typed inputs for the cognitive stages;
4. the serial runtime consumes those stage inputs and must not reach back into preparation internals.

Boundary bootstrap and API wiring compose the application; they do not own runtime orchestration, broker logic or semantic translation. Calendar/reference import remains a reference-authority boundary rather than ordinary runtime ingress.

## 2. Raw and derived authority are distinct

Direct vendor or feed observations belong in raw capture. Derived values include VWAP, realised volatility, skew, term structure, pin, gamma and participation ratios. A mixed legacy catalogue may be retained for continuity, but it is not data authority.

VWAP accumulation and VWAP rate-of-change remain unavailable until actual raw tick-derived state exists. They must not be fabricated from an insufficient substrate. Playbooks consume deterministic derived services rather than reproducing chain mathematics locally.

## 3. Raw capture policy

The admitted capture design includes same-bucket historical baselines for volume, trade count and spread. During regular trading hours:

- capture the front two option expiries every 30 seconds over a near-spot strike band;
- capture farther tenors more coarsely for curve context only;
- preserve vendor-supplied expiry, DTE, strike, side, bid, ask, last, IV, delta, gamma, open interest and volume where those fields are actually supplied.

Missing vendor fields remain missing. The capture layer cannot manufacture quote precision or derived values to fill the row.

## 4. Canonical raw artefact and lawful preparation path

A canonical raw artefact must come from actual raw content. It must not be reconstructed from a workbook, padded with invented rows or populated with handwritten derived fields. It preserves source identity, capture time, OHLCV bars, repeated quote-level option snapshots, event rows and session/timestamp anchoring.

The admitted bounded specimen has this identity:

- symbol `NVDA`;
- source `gate_e_manual_pack`;
- capture time `2026-03-23T13:55:00Z`;
- four bars;
- three option-chain snapshots;
- 30 option-quote rows;
- two event rows.

These values identify the specimen only; they do not imply general production coverage.

The lawful path is:

`raw bundle -> prepared runtime dataset -> cognition inputs -> review outputs`

Prepared snapshots cannot be hand-injected as the primary ingress for a claim about the raw path. Coverage gaps and orphan rows remain visible. Repeated execution of identical admitted inputs must preserve deterministic packet identifiers, lineage and review output.

The Gate-102 raw-path harness also freezes one bounded deterministic specimen:

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
- add candidates and active playbooks both containing only `continuation_ladder`.

These values identify and freeze the admitted specimen and its bounded companion-fixture outcome. They are not general runtime defaults or evidence of coverage beyond that one run.

## 5. Raw/prepared parity

Raw-path and prepared-path runs must declare the exact comparable surface. The admitted parity surface includes:

- temporal input;
- options/flow input;
- regime input;
- inventory state;
- risk-budget-remaining percentage;
- sequence identity;
- stage-packet identifiers and lineage;
- review packet and summary;
- event-window state;
- options-behaviour cluster;
- permission state;
- target fresh deployable percentage;
- active playbook identifiers.

Any lawful divergence outside or later within that surface must be named and explained; it cannot be implied away.

## 6. Prepared normalised feature carriage

The prepared substrate carries one explicit normalised feature packet through preparation and cognition ingress. Its admitted fields are exactly:

- `intraday_move_vs_rolling_range_5m`;
- `distance_to_vwap_vs_rolling_range_5m`;
- `intraday_move_vs_price_realised_vol_15m`;
- `front_iv_vs_front_realised_vol_ratio`;
- `next_iv_vs_next_realised_vol_ratio`;
- `atm_straddle_vs_spot_pct`;
- `near_spot_front_volume_share`.

Coverage remains review-visible. Carriage does not imply that every field is already consumed by decision law or that any later threshold has been tuned.

The bounded source specimen records, without generalising them into policy, `0.2504` for the first snapshot's intraday move versus rolling range, `7.069` for its ATM straddle versus spot, `4.644` for the third snapshot's intraday move versus 15-minute realised volatility, `1.8438` for its front-IV ratio and `100.0%` feature coverage.

## 7. Typed boundary and failure semantics

Typed ingress distinguishes permitted coercion from prohibited payload shapes. Persistence boundaries expose explicit commit and rollback behaviour. API dependency translation maps successful results and typed lookup failures deliberately rather than leaking internal exceptions or arbitrary mappings.

Cognition ingress uses separate deterministic temporal, regime and options/flow mappers plus a thin coordinator. Calculations live in those mappers. Lawful absence is represented as absence, not as wall-clock fabrication, zero certainty or a supportive fixture substituted for native data.

The final owner of regime-source completeness is unresolved. Preparation and cognition ingress must preserve partial regime truth explicitly, but this corpus does not assign the final completeness responsibility. The literal carrier name `StageInputBundle` is also not independently admitted; the required semantic contract is a governed typed bundle, whatever lawful name later authority assigns.
