# F03 — D015 trade direction and D016 signed trade volume: M01→M02 preparation

**Status:** DOCUMENTARY `AUDITED_WITH_PRECISE_HOLDS` for **both IDs**; *not* native-data certification, M02 implementation, admission or programme acceptance. **Inspection base:** isolated branch descending from `19c14ee461140649110d5d1cc4c1d5d7f40123be`; the concurrent implementation worker remains separate and may have advanced. F03 depends on F02 for D011 only. This is a preparation family, **not** a combined acceptance unit.

## E1.1 — exact accepted scope and inspected M01 evidence

| ID | Accepted effective meaning | M01 code and tests inspected | Carry-forward decision |
|---|---|---|---|
| D015 | `K08_RULE_BUCKET_POLICY`, `P_RULE`, raw R120/R126/R127, **D011** predecessor. Quote test versus trade-time midpoint: trade above/below returns `+1/-1`. At equality, compare with **last different** prior trade price (tick test); otherwise `0` = unknown. The output is a classification, not a guessed trading signal. | `src/nvda_desk/derived_signal_calculation_truth/_stage1.py:3005–3026`, `api.py:2619–2645`; `tests/product/derived_signal/test_m01_stage1_semantics.py:981–1024`, `test_m01_f2_observation_identity.py:86–145,165–178`, `test_m01_f2a_temporal_quote_sign.py:93–131`. | **REUSE_AS_SPEC; REEXPRESS_IN_M02.** Preserve the fixed classification law, trade-time quote join, last-different-trade rule, explicit 0/unknown and complete immutable selected lineage; do not copy old persistence or treat old green tests as M02 proof. |
| D016 | `K08_RULE_BUCKET_POLICY`, `P_RULE`, raw **R121** and **D015**. Sum each *matched trade* sign × size within one **separately selected fixed 1s/5s/60s/300s window**, no duplicate trades and no unclassified contributor. Its unit is shares/contracts according to the bound source. | `_stage1.py:615–671` (`_observation_signs`), `3027–3032` (sum), `api.py:2858–2866,2970–3000` (predecessor recovery/lineage), `test_m01_f2_observation_identity.py:86–145,169–219,258–278`, `test_m01_f2a_temporal_quote_sign.py:93–131`; fixture `native_signed_flow_fixture.py`. | **REUSE_MATCHING/REFUSAL_SEMANTICS; REPAIR_WINDOW_SCOPE.** Accepted Gate 2 review identifies old M01's actual all-loaded-history aggregation without named-window selection. Target law requires genuine per-window event filtering and matching complete predecessor records. |

Authoritative rows: `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv:16–17` (effective catalogue), `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md:273–274` (quote+tick test; `Σ sign_i×size_i`), `handoff/workbook_v2/gates_01_02/G2_CLASSIFICATION_CONTINUATION_20261017.md:141–142` (`FIXED_LAW` vs `MEASUREMENT_DOMAIN`), and incorporated current foundation Annex B in `handoff/foundation_implementation/authority/FOUNDATION_IMPLEMENTATION_BRIEF_PROPOSED.md:505–506` (D015 reuse with separation, D016 repair required). Effective Gate 2 makes D016's four named windows a **required measurement-domain contract**, not a strategy choice. The selectable window identity and source-history bounds still need a conforming exact concrete profile before acceptance.

## E1.2 — independently specified mathematical witnesses, *not* implementation-computed expected results

### D015, controlled trade sign

Use one admissible trade observation and a **contemporaneous trade-time** eligible D011 midpoint of exactly `100`, correct instrument/contract and visibility. The following are separate non-overlapping cases:

| Controlled case | Input | Expected mathematical output |
|---|---|---|
| Decisive buyer | last trade `101`, midpoint `100` | `+1` |
| Decisive seller | last trade `99`, midpoint `100` | `-1` |
| Midpoint equality, rising tick | trade `100`, last *different* older trade `98`, matching source identity | `+1` |
| Midpoint equality, falling tick | trade `100`, last *different* older trade `102`, matching identity | `-1` |
| Midpoint equality, no eligible different prior price | trade `100`, midpoint `100`, prior trade absent or equal | `0` (`unknown`; **not** a buy/sell classification) |

If an older trade at the same price exists before an even older **different** trade, a conforming tick test must select the last **different** eligible trade, not simply the previous row. A later quote must never reclassify a prior trade using information after that trade; a quote first appearing after the selected trade cannot silently become its contemporaneous D011. The old source and public test evidence address this causality, but exact future M02 proof is separate.

### D016, four controlled non-boundary window witnesses

Choose `as_of = 2026-10-20T12:00:10Z`, single correct subject/source/selection identity, four unique native trade occurrences with matching R121 sizes and **separately actually computed D015** classifications. These are synthetic mathematical witnesses, not IBKR-certified market records. All ages are strictly inside/outside each named window: no assertion about open/closed *boundary inclusion* is made.

| Trade ID | Age at as-of | Price relative to trade-time midpoint 100 | D015 | R121 size | Signed contribution |
|---|---:|---|---:|---:|---:|
| A | 0.5 s | 101 | +1 | Decimal `2` | `+2` |
| B | 3 s | 99 | -1 | Decimal `3` | `-3` |
| C | 30 s | 101 | +1 | Decimal `4` | `+4` |
| D | 120 s | 99 | -1 | Decimal `7` | `-7` |

| Fixed window | Expected selected IDs | Exact expected signed volume |
|---|---|---:|
| 1 second | A | `Decimal('2')` |
| 5 seconds | A, B | `Decimal('-1')` |
| 60 seconds | A, B, C | `Decimal('3')` |
| 300 seconds | A, B, C, D | `Decimal('-4')` |

These four sums were computed from the literal event set, not the M01 evaluator. A D015 result `0/unknown`, absent or conflicting classification for **any selected R121 trade** must refuse D016 rather than discard that volume or reinterpret unknown as signed zero. An **empty/zero-volume** window requires an exact accepted result-vs-refusal contract; do not infer one from ordinary arithmetic or old all-history behaviour. Window-boundary inclusion, session reset semantics, unknown native size sentinel/negative size meanings and trade temporal-kind also require exact admitted source/profile decisions.

## E1.3 — fixture/history validity and falsifiers

1. **Trade-time causality:** materialise a selected native trade at `t=5` with only a quote at `t=7`, and a request at `t=10`. Even if that quote is known at cutoff `t=10`, it cannot classify the `t=5` trade. Existing public test `test_m01_f2a_temporal_quote_sign.py:124–131`; first ensure absence/failure is for source-time incompatibility, not absent M00 pages or missing D011 configuration.
2. **Predecessor identity:** create independent D015 occurrences for A/B/C/D using their own trade-time D011 quote selection. D016's admissible R121 events must be matched to exactly those signed trades using **native M00 observation occurrence IDs** and complete immutable D015 source lineage, *not* same-looking D IDs or coincidental event times. Existing `_observation_signs`, `test_m01_f2_observation_identity.py:99–145,169–219` are reusable specifications, not accepted SQLite target proof.
3. **Ambiguity/refusal:** set one trade to midpoint with no different earlier price; its D015 output is `0`, and D016 must refuse if it would otherwise consume that trade. Separately exercise competing same-time native trades, wrong-contract trade size, missing older sign, changed mapping version, late `received_ts_utc`, duplicate conflicting sign, and incomplete R121 history. Tests `test_m01_f2_observation_identity.py:171–219,258–278` supply old falsifiers. Do not count an unrelated failed precondition as proof of the targeted refusal.
4. **Window boundaries:** use **both** sides of each exact duration boundary once the accepted source-time/session/inclusivity law is bound; the witness table intentionally avoids boundary times. Enforce complete source-history pagination for a 300-second window and sufficient older observations for the tick test. Never fabricate a next-page cursor after real source exhaustion (D014 lesson). A single page/one trade proves neither selection nor absence/non-duplication across pages.
5. **New M02 persistence:** no enabled D015/D016 typed public/result/SQLite owner or source-certified mapping exists in this inspected isolated base; future authoritative brief must specify the result and configuration identities, immutable first-write/history, no-look-ahead, first failure behaviour, fresh-process read-only recovery, negative/static proof and isolated SQLite store without relying on legacy M01/PostgreSQL evidence.

## E1.4 — upstream DATA-001 provenance; certification still unresolved

The user supplied a screenshot naming private GitHub repository **`JayDEmily/nvda_capture_collector`** as DATA-001 and its recommended operator setup. A direct authenticated read of its `main` `README.md` (Git blob `d20372c184728eaab6cf4a23224e0939a28d31ba`, observed this pass) independently confirms **IB Gateway Stable / Windows 11 / paper socket port 4002**, alongside FRED and Cboe, a **Python 3.13.5** pin, Parquet canonical writes, JSON manifests, and SQLite for collector checkpoints. The README states live IBKR snapshots were coded and fake-smoke-tested but **not end-to-end verified** in its sandbox; downstream runtime export ingestion remains an integration step. [Private repository README](https://github.com/JayDEmily/nvda_capture_collector/blob/main/README.md).

**Therefore:** no verified evidence yet binds actual DATA-001 fields into M00 `R120` trade price, `R121` trade size, `R126`/`R127` contemporaneous quote fields, their exact provider variants/timestamp semantics/units, trade occurrence join identity, session/calendar or subscription-dependent availability. No claim is made that D015/D016 are live-ready, that DATA-001 produces admitted tick-by-tick histories, or that its Python version should be used by the separate Python 3.12.14 NVDA/M02 environment. Distinguish a planned/implemented *collector* feature, an actual native provider observation, an accepted M00 projection and an accepted M02 measurement: they are four separate propositions.

**Receiver:** DATA-001 IBKR API/source-owner and M00 projection/collector-integrator for exact R120/R121/R126/R127 field semantics and delivery; M02 calculation/source-profile owner for trade/time/window/SQLite admission. The existing source holds `RAW-PROJECTION`, `CALC-PROFILE` and any actual session/calendar holds remain; no native calls or inter-repository integration were performed.

## E1.5 — bounded independent documentary challenge / disposition

- Independently derive all five D015 sign witnesses and four D016 sums above; specifically, for fixed five-second window `2−3=−1`, not all-history `2−3+4−7=−4`. The latter all-history total is a **known M01 risk**, not the five-second expected answer.
- Directly sequence `absence of trade → quote at or before trade → D015 first classification → R121 trade-size admission → D016 matching/window sum → later signed predecessor → new immutable version → old result retained`, and a separate `post-trade-only quote` refusal, without a convenience helper that pre-admits all raw values. This sequence is a **future proof specification**, not a claimed run.
- D015 has fixed classification semantics and reusable temporal/source-selection evidence. D016 requires **new window semantics**, not merely a translated SQL backend. Both have **source and public-owner holds** and neither may be labelled implementation-ready from the former M01 code or this brief.

**Individual dispositions:** `D015 AUDITED_WITH_PRECISE_HOLDS`; `D016 AUDITED_WITH_PRECISE_HOLDS`. All 126 canonical foundation identities and all 83 downstream identities remain preserved. Existing 19 assessed rows rise to **21 documentary-audited** after these two row updates; 105 remain to audit. This packet is author self-review only, not independent reviewer admission, root ExecPlan change, M02 proof or provider certification.
