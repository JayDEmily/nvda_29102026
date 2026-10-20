# F07 — Intraday realised volatility, jump variation and ATR: E1.1–E1.5

**Disposition:** 5 individual `AUDITED_WITH_PRECISE_HOLDS` documentary assessments. This is NOT M02 implementation, native-source certification, independent proof or a combined acceptance unit.

**Evidence baseline:** preparation branch inherited from saved Gate 6 D014 generation-2 archive, after audited F05 `a2a07d80538e9a643f675157e2049ded191729f3`. The concurrent implementation worker’s current HEAD is UNKNOWN. No source code, product tests, provider or SQLite execution occurred in this tranche.

## E1.1 — authority, M01 interpretation, and family reuse

- Accepted kernel: `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md:202-217`; exact 209/126/83 classification in `handoff/foundation_implementation/authority/FOUNDATION_IMPLEMENTATION_BRIEF_PROPOSED.md` Annexes B/C, with accepted overlays applied.
- Existing implementation inspected: `src/nvda_desk/derived_signal_calculation_truth/_stage1.py:2494-2579`.
- Existing public-test source inspected: `tests/product/derived_signal/test_m01_f4_rc04_realised_risk_public.py:1-315`.
- Comparison material: effective catalogue `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv` (historical dependency bytes only where superseded), accepted `handoff/workbook_v2/gates_03_04/GATES_03_04_ASSESSMENT.md` and F01–F05 preparation packets.

Annualised RV needs complete exact sampling instants and sum of actual trading-time year fractions; the old implementation uses a single `trading_year_fraction_per_interval` multiplied by return count. D034 has a **session-completeness** obligation not discharged by its old two-hour synthetic three-point test. D038 uses an explicit pi approximation and R151 closes while R149/R150 are declared dependencies; do not treat their purpose as certified. D039 correctly selects latest bars before checking missing high/low but its source co-occurrence and 5m calendar still need native mapping.

## E1.2–E1.4 — independently specified per-ID parameters, oracles, fixture prerequisites, refusals, and precise holds

### D032 — 5-minute realised volatility

- **Effective direct raw input:** `R151`; predecessor `NONE_DECLARED`; original catalogue parameter window `5 minutes`; declared units `annualised volatility`. These are input-mapping assertions, not proof of live source capability.
- **Mathematical law:** sqrt(sum(ln(P_i/P_(i-1))^2)/sum(Delta_tau_i)); complete 5-minute high-frequency R151 time-grid.
- **Controlled inputs:** Controlled R151 prices 100,200,100 at times t0,t0+150s,t0+300s; independently declared each Delta_tau=theta/2.
- **Independent result:** sqrt(2*(ln 2)^2/theta)=sqrt(2/theta)*ln(2), theta=sum trading-year fractions >0. This is an equation-derived witness, not output computed from the M01 implementation or a certified market sample.
- **Necessary history/fixture:** At least 3 aligned sampled close instants spanning actual full 5 min; explicit required instants, each two return intervals and positive Delta_tau_i, no session break unless calendar profile covers it.
- **Discriminating fault/refusal:** Missing t0+150s; extra unrelated t0+100s cannot replace required sample; delayed revision after cutoff; wrong subject; zero theta; nonpositive close.
- **M01 reuse disposition:** REUSE_M01_LOG_RETURN_AND_COMPLETE_SAMPLE_GRID_AS_SPEC; M01 source uses one scalar dt multiplied by return count, not independently varying Delta_tau_i.
- **Unresolved exact receiver:** SRC-CALENDAR/CALC-PROFILE/M00: R151 real 5-min sampling and trading-time/year calendar; exact logarithm/sqrt carrier and numerical precision.

### D033 — 30-minute realised volatility

- **Effective direct raw input:** `R151`; predecessor `NONE_DECLARED`; original catalogue parameter window `30 minutes`; declared units `annualised volatility`. These are input-mapping assertions, not proof of live source capability.
- **Mathematical law:** same exact realised-vol law, but complete 30-minute R151 window.
- **Controlled inputs:** Controlled 100,200,100 at t0,t0+15m,t0+30m; Delta_tau1+2=theta>0.
- **Independent result:** sqrt(2/theta)*ln(2) with theta for whole 30-minute admitted trading-time grid. This is an equation-derived witness, not output computed from the M01 implementation or a certified market sample.
- **Necessary history/fixture:** Three deliberately sparse mathematical points suffice only under a versioned 15m sampling policy; production must prove complete 30m horizon at the admitted finer native grid.
- **Discriminating fault/refusal:** Only 5m series; missing 15m required anchor; old sample outside 30m masked by newer invalid point; nonpositive price; wrong calendar.
- **M01 reuse disposition:** REUSE_K05_RV_FORMULA_AND_INTERVAL_GRID_AS_SPEC; D033 distinct full-horizon requirement.
- **Unresolved exact receiver:** SRC-CALENDAR/M00: R151 sampling density and 30m completeness; M02 precision/version policy.

### D034 — Intraday/session realised volatility

- **Effective direct raw input:** `R151`; predecessor `NONE_DECLARED`; original catalogue parameter window `1 session`; declared units `annualised volatility`. These are input-mapping assertions, not proof of live source capability.
- **Mathematical law:** same realised-vol law over one complete named session, annualised by actual trading-time fractions.
- **Controlled inputs:** Controlled session open 100, mid-session 200, session close 100 at exact admitted grid points; total trading-year fraction theta.
- **Independent result:** sqrt(2/theta)*ln(2); no unapproved 390-minute/252-day constant assumed. This is an equation-derived witness, not output computed from the M01 implementation or a certified market sample.
- **Necessary history/fixture:** At least one complete session with declared calendar opening, closing, eligible trading instants and sample density; cannot infer session coverage from 3 synthetic prices alone.
- **Discriminating fault/refusal:** Early close not accounted; missing end-of-session sample; after-hours samples presented as session closes; incorrect DST/calendar, zero theta.
- **M01 reuse disposition:** REUSE_FORMULA_ONLY; legacy 3-observation test is not proof of a full session (existing `_instants` chooses 3 one-hour-spaced events).
- **Unresolved exact receiver:** SRC-CALENDAR/M00: exact NVDA session and R151 full grid; CALC-PROFILE: trading-year interval measure and result precision.

### D038 — Jump-variation estimate

- **Effective direct raw input:** `R149;R150;R151`; predecessor `NONE_DECLARED`; original catalogue parameter window `Intraday / rolling days`; declared units `variance`. These are input-mapping assertions, not proof of live source capability.
- **Mathematical law:** RV=sum r_i^2; BV=(pi/2)*sum_(i=2..N)|r_i||r_(i-1)|; JV=max(RV-BV,0) over admitted R151 return series.
- **Controlled inputs:** R151 closes 100,200,200,200 -> log returns (ln 2,0,0).
- **Independent result:** RV=(ln 2)^2, BV=0, JV=(ln 2)^2; flat 100,100,100,100 -> 0. This is an equation-derived witness, not output computed from the M01 implementation or a certified market sample.
- **Necessary history/fixture:** At least four declared ordered sample instants for three returns in concrete illustrative case; R149/R150 co-listed raw shape requires independent source-role examination; actual horizon/grid/knowledge cutoff versioned.
- **Discriminating fault/refusal:** Missing middle sample; historical high/low R149/R150 not co-referenced if declared as requirements; zero/nonpositive close; after-cutoff correction; incompatible sampling density.
- **M01 reuse disposition:** REUSE_BIPOWER_IDENTITY_AS_SPEC; old M01 uses truncated Decimal pi constant and computes from R151 only while declares R149/R150; exact pi/precision and extra source-role need decision.
- **Unresolved exact receiver:** CALC-PROFILE/M00: annual/high-frequency grid, whether R149/R150 are genuine evidence prerequisites, approximation of pi/logs and output numeric representation.

### D039 — 5-minute average true range

- **Effective direct raw input:** `R141;R142;R143`; predecessor `NONE_DECLARED`; original catalogue parameter window `Rolling 5-minute bars`; declared units `price`. These are input-mapping assertions, not proof of live source capability.
- **Mathematical law:** TR_i=max(high_i-low_i, abs(high_i-prev_close_i), abs(low_i-prev_close_i)); ATR=mean(TR_i) over versioned bar_count of five-minute bars.
- **Controlled inputs:** Previous close=100; bar1 high=110 low=90 close=105; bar2 high=112 low=99 close=108; bar_count=2.
- **Independent result:** TR1=max(20,10,10)=20; TR2=max(13,7,6)=13; ATR=(20+13)/2=16.5 price units. This is an equation-derived witness, not output computed from the M01 implementation or a certified market sample.
- **Necessary history/fixture:** bar_count+1 close observations (3 for two bars), high/low same occurrence IDs as each selected bar close, exactly adjacent 5m bars; select latest target bars BEFORE rejecting incomplete co-fields.
- **Discriminating fault/refusal:** Latest bar missing high but older complete bar must not substitute; one 10-minute gap; high<low or mismatched native bar id; absent previous close; wrong session.
- **M01 reuse disposition:** REUSE_K05_TR/ATR_ARITHMETIC_AND_LATEST_WINDOW_SELECTOR_AS_SPEC; M01 has direct incomplete/latest-bar and gap witnesses.
- **Unresolved exact receiver:** M00 SRC-CALENDAR: R141/R142/R143 bar identity/chronology/units, native 5m trade classification; M02 complete selection/typed readback.

## E1.5 — independent documentary challenge

For D032 ensure wrong later sample does not silently replace a missing required timestamp; independently calculate 100,200,100 -> sqrt(2/theta)*ln2. For D038 calculate 100,200,200,200 -> (ln2)^2 (BV=0), distinguishing jump from zero-variation fixture. For D039 use previous close100 and bars(110/90/105,112/99/108) -> 16.5, then remove latest high but provide an older complete bar and require refusal.

**Negative witness semantics:** provide genuinely eligible source events and calendar/profile state *before* introducing a test fault. An empty reader, exhausted pagination cursor, wrong test phase or fixture conveniently pre-populated by a helper cannot stand in for a semantic refusal. Inspect real M00 public projection, declared mapping/versions, selected occurrence IDs, immutable retry/history and future SQLite readback at implementation time; these were not executed or accepted here.

**Reconciliation:** D032, D033, D034, D038, D039 each has a distinct numeric witness and source/selection/refusal contract. All 5 are `AUDITED_WITH_PRECISE_HOLDS`; no `ESTABLISHED_NATIVE` or `M02_ACCEPTED` claim. D028 legacy contradiction is retained rather than silently applying the wrong R044 fixture. Cross-family dependencies remain as mapped; this is a preparation packet only.
