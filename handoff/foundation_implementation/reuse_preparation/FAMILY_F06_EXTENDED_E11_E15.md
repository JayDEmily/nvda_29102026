# F06 — Volume/time-bucket baselines and z scores: E1.1–E1.5

**Disposition:** 4 individual `AUDITED_WITH_PRECISE_HOLDS` documentary assessments. This is NOT M02 implementation, native-source certification, independent proof or a combined acceptance unit.

**Evidence baseline:** preparation branch inherited from saved Gate 6 D014 generation-2 archive, after audited F05 `a2a07d80538e9a643f675157e2049ded191729f3`. The concurrent implementation worker’s current HEAD is UNKNOWN. No source code, product tests, provider or SQLite execution occurred in this tranche.

## E1.1 — authority, M01 interpretation, and family reuse

- Accepted kernel: `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md:184-201`; exact 209/126/83 classification in `handoff/foundation_implementation/authority/FOUNDATION_IMPLEMENTATION_BRIEF_PROPOSED.md` Annexes B/C, with accepted overlays applied.
- Existing implementation inspected: `src/nvda_desk/derived_signal_calculation_truth/_stage1.py:2333-2486`.
- Existing public-test source inspected: `tests/product/derived_signal/test_m01_f4_rc04_baselines_public.py:1-160;tests/product/derived_signal/test_m01_f4_rc04_elapsed_fraction_public.py:1-154`.
- Comparison material: effective catalogue `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv` (historical dependency bytes only where superseded), accepted `handoff/workbook_v2/gates_03_04/GATES_03_04_ASSESSMENT.md` and F01–F05 preparation packets.

D028 has an accepted R041-only same-exact-fraction/complete-session overlay that **supersedes** legacy R044-as-fraction M01 production and the `elapsed_fraction` tests; those tests are historical negative evidence, not drop-in fixtures. For D029–D031, the M01 sample-SD law and declared `source_native_time_of_day_bucket` matcher are reusable, but the synthetic two-sample fixture does not establish a 20–60-session native baseline. Do not conflate D028 ratio with the z score or R041 cumulative with R144/R062/R063 period rates.

## E1.2–E1.4 — independently specified per-ID parameters, oracles, fixture prerequisites, refusals, and precise holds

### D028 — Relative volume versus normal time-of-day

- **Effective direct raw input:** `R041`; predecessor `NONE_DECLARED`; original catalogue parameter window `Time-of-day baseline`; declared units `multiple`. These are input-mapping assertions, not proof of live source capability.
- **Mathematical law:** V_current / mean(V_prior,1..N), N>=2 immediately preceding compatible sessions; same exact eligible elapsed-session fraction, R041 ONLY.
- **Controlled inputs:** Current R041=30 shares at fraction 1/2; two prior full compatible sessions R041=10 and 20 at exactly fraction 1/2.
- **Independent result:** 30/((10+20)/2)=2 (dimensionless). This is an equation-derived witness, not output computed from the M01 implementation or a certified market sample.
- **Necessary history/fixture:** Three fully modelled sessions (current + N=2 strictly preceding), each with calendar identity, common session type/duration and unique R041 cumulative counters at exact fraction 1/2; versioned complete calendar/profile; each source receipt before cutoff.
- **Discriminating fault/refusal:** Missing exact fraction in either mandatory prior session; wrong session duration; counter reset/ambiguous value; wrong shares/units; zero prior mean; prior seen only after cutoff; wrong fraction nearer than true member must never be substituted.
- **M01 reuse disposition:** REEXPRESS_EFFECTIVE_D028; old _eval_k04 D028 R044 elapsed-fraction branch and its test fixtures are CONTRARY to accepted overlay; retain only same-fraction/ratio/insufficient-history propositions.
- **Unresolved exact receiver:** SRC-CALENDAR/SRC-VOLUME/M00: cash equity session calendar and break-adjusted exact fraction, reliable R041 cumulative session counters, generation/reset and freshness; M02: R041-only metadata-driven selector + exact ratio carrier.

### D029 — Volume z-score

- **Effective direct raw input:** `R144`; predecessor `NONE_DECLARED`; original catalogue parameter window `20-60 sessions`; declared units `z-score`. These are input-mapping assertions, not proof of live source capability.
- **Mathematical law:** z=(current-mean(prior_N))/sample_sd(prior_N), sample SD N-1, matching same time-of-day bucket; R144.
- **Controlled inputs:** R144 prior same-bucket bar volumes 8 and 12; current 16 (separate sessions).
- **Independent result:** (16-10)/sqrt(((8-10)^2+(12-10)^2)/(2-1))=6/sqrt(8)=3/sqrt(2). This is an equation-derived witness, not output computed from the M01 implementation or a certified market sample.
- **Necessary history/fixture:** N+1 eligible bucketed bar events; N=2 historical and current never in own baseline; native bucket and one bar per required session, ordered receive/cutoff, sample definition versioned.
- **Discriminating fault/refusal:** Only one prior; flat history (8,8) => s=0 refusal; near-time wrong bucket=999 should not displace matched prior; wrong subject; late receipt; ambiguous bucket.
- **M01 reuse disposition:** REUSE_K04_SAMPLE_SD_AND_NATIVE_BUCKET_FILTER_AS_SPEC; old helper has two historical cases, not verified native 20–60 session completeness.
- **Unresolved exact receiver:** SRC-VOLUME/SRC-CALENDAR/M00: R144 bar volume and native session/time-of-day buckets, missing/zero/trading sessions, units; M02: exact annual calendar baseline profile and nonterminating z carrier.

### D030 — Trade-rate z-score

- **Effective direct raw input:** `R062`; predecessor `NONE_DECLARED`; original catalogue parameter window `20-60 sessions`; declared units `z-score`. These are input-mapping assertions, not proof of live source capability.
- **Mathematical law:** same sample z-score, but current/prior R062 trade count rate per minute (not bar volume).
- **Controlled inputs:** R062 prior same-bucket trade rates 8 and 12; current 16 trades/min.
- **Independent result:** (16-10)/sqrt(8)=3/sqrt(2) z-score. This is an equation-derived witness, not output computed from the M01 implementation or a certified market sample.
- **Necessary history/fixture:** N=2 complete previous same-bucket observations + one current; source-native trades/minute numerator and minute duration aligned by instrument/session.
- **Discriminating fault/refusal:** Treat count as share-volume; include different minute, wrong instrument or current in its own sample; zero SD or insufficient prior.
- **M01 reuse disposition:** REUSE_K04_SAMPLE_SD_AND_BUCKET_SELECTOR_AS_SPEC; preserve distinct R062 field and trades/minute units.
- **Unresolved exact receiver:** SRC-VOLUME/M00: R062 native trade counting/rate, minute interval, subscription gaps/session bucket; M02: exact baseline/window/representation.

### D031 — Volume-rate z-score

- **Effective direct raw input:** `R063`; predecessor `NONE_DECLARED`; original catalogue parameter window `20-60 sessions`; declared units `z-score`. These are input-mapping assertions, not proof of live source capability.
- **Mathematical law:** same sample z-score, but current/prior R063 share volume rate per minute (not R041 cumulative nor R144 bar total).
- **Controlled inputs:** R063 prior same-bucket volume rates 8 and 12; current 16 shares/min.
- **Independent result:** (16-10)/sqrt(8)=3/sqrt(2) z-score. This is an equation-derived witness, not output computed from the M01 implementation or a certified market sample.
- **Necessary history/fixture:** N=2 previous eligible same-bucket volume-rate observations + current; identical share/minute units and native bucket/source-version.
- **Discriminating fault/refusal:** Use cumulative R041 or one-bar R144 as rate; wrong unit/minute, session/gap, flat baseline or future-known prior.
- **M01 reuse disposition:** REUSE_K04_SAMPLE_SD_AND_BUCKET_SELECTOR_AS_SPEC; keep R063 distinct.
- **Unresolved exact receiver:** SRC-VOLUME/M00: R063 native rate window and unit conversion, missing minutes; M02: versioned baseline N, time bucket, exact output.

## E1.5 — independent documentary challenge

For D028 instantiate a three-session calendar with equal session durations and distinct immutable identities, then make one of the two mandatory prior sessions incompatible **without removing it from the raw history**; refusal must occur rather than skipping to an older session. For D029 create a same-bucket 8/12 history and current 16 plus a later but wrong-bucket 999; the z oracle stays 3/sqrt(2). Deleting one required historical member must refuse, even if an older eligible member exists outside the exact N-session range.

**Negative witness semantics:** provide genuinely eligible source events and calendar/profile state *before* introducing a test fault. An empty reader, exhausted pagination cursor, wrong test phase or fixture conveniently pre-populated by a helper cannot stand in for a semantic refusal. Inspect real M00 public projection, declared mapping/versions, selected occurrence IDs, immutable retry/history and future SQLite readback at implementation time; these were not executed or accepted here.

**Reconciliation:** D028, D029, D030, D031 each has a distinct numeric witness and source/selection/refusal contract. All 4 are `AUDITED_WITH_PRECISE_HOLDS`; no `ESTABLISHED_NATIVE` or `M02_ACCEPTED` claim. D028 legacy contradiction is retained rather than silently applying the wrong R044 fixture. Cross-family dependencies remain as mapped; this is a preparation packet only.
