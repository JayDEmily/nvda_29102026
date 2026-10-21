# F12 — Cboe volatility index point/percent changes: E1.1–E1.5

**Disposition:** 5 individual `AUDITED_WITH_PRECISE_HOLDS` documentary assessments. This is NOT M02 implementation, native-source certification, independent proof or a combined acceptance unit.

**Evidence baseline:** preparation branch inherited from saved Gate 6 D014 generation-2 archive, after audited F05 `a2a07d80538e9a643f675157e2049ded191729f3`. The concurrent implementation worker’s current HEAD is UNKNOWN. No source code, product tests, provider or SQLite execution occurred in this tranche.

## E1.1 — authority, M01 interpretation, and family reuse

- Accepted kernel: `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md:166-182`; exact 209/126/83 classification in `handoff/foundation_implementation/authority/FOUNDATION_IMPLEMENTATION_BRIEF_PROPOSED.md` Annexes B/C, with accepted overlays applied.
- Existing implementation inspected: `src/nvda_desk/derived_signal_calculation_truth/_stage1.py:2118-2145,2245-2319`.
- Existing public-test source inspected: `tests/product/derived_signal/test_m01_f4_rc03_history_public.py:236-293`.
- Comparison material: effective catalogue `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv` (historical dependency bytes only where superseded), accepted `handoff/workbook_v2/gates_03_04/GATES_03_04_ASSESSMENT.md` and F01–F05 preparation packets.

Every signal has a **two-field** typed result; do not collapse them into a scalar. The catalogue allows 5m/1h/1d only **where source permits**: the archived collector claims FRED/Cboe macro capture but not native intraday coverage for every VIX-family index. M01 RC03 300-second synthetic fixture is not evidence of source eligibility. Reference zero prohibits percent even if a point difference exists.

## E1.2–E1.4 — independently specified per-ID parameters, oracles, fixture prerequisites, refusals, and precise holds

### D052 — VIX change

- **Effective direct raw input:** `R236`; predecessor `NONE_DECLARED`; original catalogue parameter window `5m/1h/1d where source permits`; declared units `index points / percent`. These are input-mapping assertions, not proof of live source capability.
- **Mathematical law:** structured {point_change=R236_t-R236_ref,percent_change=100*(R236_t/R236_ref-1)} VIX.
- **Controlled inputs:** R236 VIX prior 100, current 120 (synthetic, NOT typical market range).
- **Independent result:** {point_change=+20 index points, percent_change=+20%}. This is an equation-derived witness, not output computed from the M01 implementation or a certified market sample.
- **Necessary history/fixture:** Two same VIX variant/source observations, selected source-supported 5m/1h/1d anchor, matching official/intraday methodology and source knowledge times.
- **Discriminating fault/refusal:** Use VIX3M R240; reference zero; 5-minute anchor using daily-only series; mix close and streaming quote or after-cutoff correction.
- **M01 reuse disposition:** REUSE_K03_TWO_FIELD_RESULT; RC03 300s fixture does not certify provider 5m eligibility.
- **Unresolved exact receiver:** Cboe/M00: VIX live vs historical cadence, native publication/timestamp, missing states and series methods; M02 structured precise output.

### D053 — VVIX change

- **Effective direct raw input:** `R237`; predecessor `NONE_DECLARED`; original catalogue parameter window `5m/1h/1d where source permits`; declared units `index points / percent`. These are input-mapping assertions, not proof of live source capability.
- **Mathematical law:** same point/percentage pair for VVIX R237.
- **Controlled inputs:** R237 VVIX prior 100, current 90.
- **Independent result:** {point_change=-10, percent_change=-10%}. This is an equation-derived witness, not output computed from the M01 implementation or a certified market sample.
- **Necessary history/fixture:** Two comparable native VVIX observations from exact source-supported horizon 5m/1h/1d only if evidenced.
- **Discriminating fault/refusal:** VIX value substituted, near-anchor later observation used, wrong native cadence, zero prior, wrong index method.
- **M01 reuse disposition:** REUSE_K03_TWO_FIELD_RESULT; keep VVIX distinct.
- **Unresolved exact receiver:** Cboe/M00: actual VVIX official/intraday data availability, time/date eligibility, mixed snapshots.

### D054 — VIX1D change

- **Effective direct raw input:** `R238`; predecessor `NONE_DECLARED`; original catalogue parameter window `5m/1h/1d where source permits`; declared units `index points / percent`. These are input-mapping assertions, not proof of live source capability.
- **Mathematical law:** same point/percentage pair for VIX1D R238.
- **Controlled inputs:** R238 VIX1D prior 10, current 11.
- **Independent result:** {point_change=+1, percent_change=+10%}. This is an equation-derived witness, not output computed from the M01 implementation or a certified market sample.
- **Necessary history/fixture:** Two source-certified VIX1D observations on chosen anchor, methodology/version and observation times matched.
- **Discriminating fault/refusal:** Assume 5m collection without source; R236 VIX substitution; zero prior or wrong market-state.
- **M01 reuse disposition:** REUSE_K03_TWO_FIELD_RESULT; preserve one-day implied index meaning.
- **Unresolved exact receiver:** Cboe/M00: VIX1D availability and cadence, index methodology and source-version; M02 full typed pair.

### D055 — VIX9D change

- **Effective direct raw input:** `R239`; predecessor `NONE_DECLARED`; original catalogue parameter window `5m/1h/1d where source permits`; declared units `index points / percent`. These are input-mapping assertions, not proof of live source capability.
- **Mathematical law:** same point/percentage pair for VIX9D R239.
- **Controlled inputs:** R239 VIX9D prior 20, current 20.
- **Independent result:** {point_change=0, percent_change=0%}. This is an equation-derived witness, not output computed from the M01 implementation or a certified market sample.
- **Necessary history/fixture:** Two VIX9D observations at source-permitted anchor, different immutable occurrences with equal values.
- **Discriminating fault/refusal:** Treat unchanged value as missing measurement; R238 one-day quote substitutes; no supported selected horizon, zero prior.
- **M01 reuse disposition:** REUSE_K03_TWO_FIELD_RESULT; confirm zeros are real result not no-observation.
- **Unresolved exact receiver:** Cboe/M00: VIX9D publication cadence/time series availability and compatible snapshots.

### D056 — VIX3M change

- **Effective direct raw input:** `R240`; predecessor `NONE_DECLARED`; original catalogue parameter window `5m/1h/1d where source permits`; declared units `index points / percent`. These are input-mapping assertions, not proof of live source capability.
- **Mathematical law:** same point/percentage pair for VIX3M R240.
- **Controlled inputs:** R240 VIX3M prior 40, current 25.
- **Independent result:** {point_change=-15, percent_change=-37.5%}. This is an equation-derived witness, not output computed from the M01 implementation or a certified market sample.
- **Necessary history/fixture:** Two comparable VIX3M observations with admissible 5m/1h/1d horizon selected and source-proved.
- **Discriminating fault/refusal:** Conflate VIX3M with current VIX, reference zero, mixed native snapshot types or unobserved intraday data.
- **M01 reuse disposition:** REUSE_K03_TWO_FIELD_RESULT; preserve R240 separate index tenor.
- **Unresolved exact receiver:** Cboe/M00: VIX3M historical/intraday supply, official publication and timezone; M02 exact ratio and durable structured fields.

## E1.5 — independent documentary challenge

With R236 VIX current120/prior100 the result is (+20points,+20%); source-time selection must reject an after-anchor point decoy. For R239 VIX9D equal20/20, zero/zero remains an actual occurrence. Replace its 5m reference with a daily-only snapshot and require a source/profile refusal, not fabricated interpolation.

**Negative witness semantics:** provide genuinely eligible source events and calendar/profile state *before* introducing a test fault. An empty reader, exhausted pagination cursor, wrong test phase or fixture conveniently pre-populated by a helper cannot stand in for a semantic refusal. Inspect real M00 public projection, declared mapping/versions, selected occurrence IDs, immutable retry/history and future SQLite readback at implementation time; these were not executed or accepted here.

**Reconciliation:** D052, D053, D054, D055, D056 each has a distinct numeric witness and source/selection/refusal contract. All 5 are `AUDITED_WITH_PRECISE_HOLDS`; no `ESTABLISHED_NATIVE` or `M02_ACCEPTED` claim. D028 legacy contradiction is retained rather than silently applying the wrong R044 fixture. Cross-family dependencies remain as mapped; this is a preparation packet only.
