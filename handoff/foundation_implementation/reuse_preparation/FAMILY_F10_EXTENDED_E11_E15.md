# F10 — Treasury real/nominal/breakeven rate changes: E1.1–E1.5

**Disposition:** 3 individual `AUDITED_WITH_PRECISE_HOLDS` documentary assessments. This is NOT M02 implementation, native-source certification, independent proof or a combined acceptance unit.

**Evidence baseline:** preparation branch inherited from saved Gate 6 D014 generation-2 archive, after audited F05 `a2a07d80538e9a643f675157e2049ded191729f3`. The concurrent implementation worker’s current HEAD is UNKNOWN. No source code, product tests, provider or SQLite execution occurred in this tranche.

## E1.1 — authority, M01 interpretation, and family reuse

- Accepted kernel: `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md:166-182`; exact 209/126/83 classification in `handoff/foundation_implementation/authority/FOUNDATION_IMPLEMENTATION_BRIEF_PROPOSED.md` Annexes B/C, with accepted overlays applied.
- Existing implementation inspected: `src/nvda_desk/derived_signal_calculation_truth/_stage1.py:2118-2145,2245-2319`.
- Existing public-test source inspected: `tests/product/derived_signal/test_m01_f4_rc03_history_public.py:236-293`.
- Comparison material: effective catalogue `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv` (historical dependency bytes only where superseded), accepted `handoff/workbook_v2/gates_03_04/GATES_03_04_ASSESSMENT.md` and F01–F05 preparation packets.

Canonical decimal-rate input is not the native FRED percent string. The approved rate movement is a basis-point **difference**, not a percentage ratio. M01 `_history_anchor` is generic and RC03 supplies 300 seconds to all D044–D046: that test demonstrates arithmetic, not the approved 1d/5d horizon. Rate observation dates and vintage visibility need source-proof.

## E1.2–E1.4 — independently specified per-ID parameters, oracles, fixture prerequisites, refusals, and precise holds

### D044 — 10-year real-yield change

- **Effective direct raw input:** `R252`; predecessor `NONE_DECLARED`; original catalogue parameter window `1d/5d`; declared units `basis points`. These are input-mapping assertions, not proof of live source capability.
- **Mathematical law:** 10000*(R252_t-R252_ref), canonical decimal interest rate (10y TIPS real yield), 1d or 5d profile anchor.
- **Controlled inputs:** R252 current 0.0425 and eligible prior 0.0410, selected daily anchor.
- **Independent result:** 10000*(0.0015)=+15 basis points. This is an equation-derived witness, not output computed from the M01 implementation or a certified market sample.
- **Necessary history/fixture:** Two eligible same-series annualised decimal-rate observations covering admitted 1d/5d calendar anchor; preserve vintage and knowledge cutoff; nearer post-anchor value decoy.
- **Discriminating fault/refusal:** Only 5-minute history as substitute for daily anchor; percent 4.25 treated as canonical decimal; after-cutoff FRED revision; wrong maturity.
- **M01 reuse disposition:** REUSE_RATE_DIFFERENCE_KERNEL; RC03 fixture currently tests 300-second anchor, NOT proof of allowed 1d/5d horizon.
- **Unresolved exact receiver:** FRED/M00: actual real-yield series units percent vs decimal conversion, source release date/vintage and daily/trading date anchors; M02 exact time profile.

### D045 — 10-year nominal-yield change

- **Effective direct raw input:** `R249`; predecessor `NONE_DECLARED`; original catalogue parameter window `1d/5d`; declared units `basis points`. These are input-mapping assertions, not proof of live source capability.
- **Mathematical law:** 10000*(R249_t-R249_ref), canonical decimal 10y nominal Treasury yield.
- **Controlled inputs:** R249 current .0500 and prior .0490 over selected 1d horizon.
- **Independent result:** 10000*(.0010)=+10 basis points. This is an equation-derived witness, not output computed from the M01 implementation or a certified market sample.
- **Necessary history/fixture:** Two same-maturity eligible observations at authorised daily/5d anchor and vintage/receipt cutoff.
- **Discriminating fault/refusal:** Use 2y tenor R250, 300s anchor or 5d numerator versus 1d reference; after-cutoff revision.
- **M01 reuse disposition:** REUSE_K03_SIMPLE_DIFFERENCE; avoid RC03 300s synthetic time standing in for native daily.
- **Unresolved exact receiver:** FRED/M00: R249 units, maturity/measurement-date/vintage; daily/5d definition; M02 exact backend.

### D046 — 10-year breakeven-inflation change

- **Effective direct raw input:** `R255`; predecessor `NONE_DECLARED`; original catalogue parameter window `1d/5d`; declared units `basis points`. These are input-mapping assertions, not proof of live source capability.
- **Mathematical law:** 10000*(R255_t-R255_ref), canonical decimal 10y breakeven inflation yield.
- **Controlled inputs:** R255 prior .0225, current .0200, selected 5d horizon.
- **Independent result:** 10000*(-.0025)=-25 basis points. This is an equation-derived witness, not output computed from the M01 implementation or a certified market sample.
- **Necessary history/fixture:** Two 10y breakeven series observations with one authorised five-day reference and full source/calendar version.
- **Discriminating fault/refusal:** Swap 10y nominal or raw percent 2.00 without converting; missing requested five-day reference; incompatible vintage.
- **M01 reuse disposition:** REUSE_K03_SIMPLE_DIFFERENCE; preserve breakeven R255 identity.
- **Unresolved exact receiver:** FRED/M00: source calendar/vintage, 10y breakeven formula/field and canonical percent→decimal profile.

## E1.5 — independent documentary challenge

Use same maturity/source series with R252 prior .0410/current .0425 => +15 bp. Place a higher-valued more recent but after-anchor event and prove it is not the reference. Repeat with an actual 5d reference, not an invented 300-second proxy; a revised FRED observation received after cutoff must be absent.

**Negative witness semantics:** provide genuinely eligible source events and calendar/profile state *before* introducing a test fault. An empty reader, exhausted pagination cursor, wrong test phase or fixture conveniently pre-populated by a helper cannot stand in for a semantic refusal. Inspect real M00 public projection, declared mapping/versions, selected occurrence IDs, immutable retry/history and future SQLite readback at implementation time; these were not executed or accepted here.

**Reconciliation:** D044, D045, D046 each has a distinct numeric witness and source/selection/refusal contract. All 3 are `AUDITED_WITH_PRECISE_HOLDS`; no `ESTABLISHED_NATIVE` or `M02_ACCEPTED` claim. D028 legacy contradiction is retained rather than silently applying the wrong R044 fixture. Cross-family dependencies remain as mapped; this is a preparation packet only.
