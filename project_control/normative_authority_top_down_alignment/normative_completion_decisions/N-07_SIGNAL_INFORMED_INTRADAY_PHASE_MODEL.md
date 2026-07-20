# N-07 — Signal-informed intraday phase model

## Status

Accepted — normative authority complete for `C-026`.

## Unresolved proposition

Which signal families, phase states, transition semantics, state/history, versioning and degradation rules define a truthful signal-informed intraday phase interpretation rather than a fixed-clock bucket?

## Material read set

Direct user architecture authority dated 2026-07-17 and the current execution brief were applied.

Normative authority read in full or as connected authority before decision: `docs/02`, `02.1`, `03`, `03.1`, `03.2`, `04`, `04.1`, `04.2`, `05`, `07`, `07.1`, `09`, `09.1`, `11` and `11.1`.

Gate B and Gate C evidence read: `B07.1-B07.3` in context, row `C-026`, and the complete B07 Gate C design record.

Existing tests read as evidence: source temporal-standard and temporal/regime policy-version tests, plus current runtime temporal expectations.

Bounded source read as consequence evidence: complete session-clock classifier and temporal-context service. The PRL minute-profile plan was read only as non-authoritative planning evidence and did not define this decision.

## Adopted project decision

The detailed ordered phases are `pre_open`, `opening_price_discovery`, `opening_transition`, `continuous_session`, `closing_transition`, `closing_auction` and `post_close`; `unresolved` is a non-phase outcome. A signal-informed decision requires source/session truth plus recent typed evidence from activity/participation, liquidity/spread and price-discovery/instability families, with authoritative market-structure status when supplied.

Clock/session position supplies factual session boundaries, order and a prior; inside the session it cannot alone force behavioural transitions. The interpreter is session-stateful, uses prior phase/history, sustained multi-family evidence and versioned hysteresis/dwell rules, normally advances monotonically, and exposes confidence/evidence/degradation state. Clock-only results leave the detailed phase unresolved and are labelled degraded.

Governing propositions: `docs/02.2_SIGNAL_INFORMED_INTRADAY_PHASE_WORKING.md` sections `02.2.N07.1` through `02.2.N07.8`.

## Alternatives ruled out

- Fixed 10:30 or any other magical cut-off ending opening behaviour: ruled out because elapsed time is a prior/eligibility fact, not behavioural evidence.
- One volume, spread or volatility proxy standing in for the full phase judgement: ruled out because the required evidence families are distinct.
- Stateless classification of each observation: ruled out because transition, hysteresis and held/degraded semantics require prior state/history.
- Silent carry-forward or clock imputation when signals are missing: ruled out because held state and clock-only fallback must be explicit.
- Allowing the temporal phase to grant trading permission: ruled out because it is context consumed by separately owned serial/risk/capital policies.

## Longitudinal effects

Typed recent signals and session reference enter a session-scoped stateful interpreter; the versioned policy compares current evidence with prior phase/history; one confirmed, held-degraded or unresolved output is emitted; later serial and Parallel Risk consumers receive context only; replay reconstructs the same transition from retained evidence.

## Transverse effects

The decision fixes phase vocabulary, required signal families, clock prior, transition order, hysteresis/state history, evidence quality, missing/conflicting data, source/policy/state versions, consumer authority and replay lineage.

## External sources

No external source was used as normative evidence. This is a project-specific cognition model directly authorised by the user and constrained by the governed architecture. No market-microstructure paper or vendor algorithm was adopted by implication.

## Current implementation consequence

Current temporal code is a fixed-clock classifier and cannot claim conformance to the detailed signal-informed model. No implementation change or conformance claim is made.

## Remaining Unknowns

- Numerical thresholds, baselines, lookback windows, dwell periods, weighting and confidence calibration remain versioned policy/configuration to be designed and proved later.
- Exact admitted signal contracts and data-provider availability remain source/preparation implementation work.
- Production state persistence and recovery remain intentionally unknown.
