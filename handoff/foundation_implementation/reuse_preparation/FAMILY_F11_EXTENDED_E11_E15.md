# F11 — USD index and FX percentage changes: E1.1–E1.5

**Disposition:** 4 individual `AUDITED_WITH_PRECISE_HOLDS` documentary assessments. This is NOT M02 implementation, native-source certification, independent proof or a combined acceptance unit.

**Evidence baseline:** preparation branch inherited from saved Gate 6 D014 generation-2 archive, after audited F05 `a2a07d80538e9a643f675157e2049ded191729f3`. The concurrent implementation worker’s current HEAD is UNKNOWN. No source code, product tests, provider or SQLite execution occurred in this tranche.

## E1.1 — authority, M01 interpretation, and family reuse

- Accepted kernel: `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md:166-182`; exact 209/126/83 classification in `handoff/foundation_implementation/authority/FOUNDATION_IMPLEMENTATION_BRIEF_PROPOSED.md` Annexes B/C, with accepted overlays applied.
- Existing implementation inspected: `src/nvda_desk/derived_signal_calculation_truth/_stage1.py:2118-2145,2245-2319`.
- Existing public-test source inspected: `tests/product/derived_signal/test_m01_f4_rc03_history_public.py:236-293`.
- Comparison material: effective catalogue `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv` (historical dependency bytes only where superseded), accepted `handoff/workbook_v2/gates_03_04/GATES_03_04_ASSESSMENT.md` and F01–F05 preparation packets.

All four use `100*(current/reference-1)` but are distinct series and native orientation; D049/D050/D051 are **currency units per USD**, so the same native quote inverted to USD per unit would produce a different percent. D048 has an explicit 20d option absent from three FX rows. M01 RC03 uses 300-second synthetic pairs rather than native daily input.

## E1.2–E1.4 — independently specified per-ID parameters, oracles, fixture prerequisites, refusals, and precise holds

### D048 — Broad USD rate of change

- **Effective direct raw input:** `R245`; predecessor `NONE_DECLARED`; original catalogue parameter window `1d/5d/20d`; declared units `percent`. These are input-mapping assertions, not proof of live source capability.
- **Mathematical law:** 100*(R245_t/R245_ref-1), broad trade-weighted USD index, selected 1d/5d/20d.
- **Controlled inputs:** R245 prior 100 and current 120.
- **Independent result:** 100*(120/100-1)=+20% (no rate/bps). This is an equation-derived witness, not output computed from the M01 implementation or a certified market sample.
- **Necessary history/fixture:** Two comparable index levels, same series/base/revision and exact selected 1d/5d/20d anchor, canonical source vintage.
- **Discriminating fault/refusal:** Use wrong USD index basket/rebase; 5-minute synthetic pair as 1-day result; prior=0 denominator; after-cutoff corrected value.
- **M01 reuse disposition:** REUSE_K03_PERCENT_RETURN_AS_SPEC; RC03 five-minute demonstration is not source-valid daily witness.
- **Unresolved exact receiver:** FRED/M00: broad index series rebasing/frequency, units/source vintage; M02 history profile and fractional result carrier.

### D049 — JPY/USD rate of change

- **Effective direct raw input:** `R274`; predecessor `NONE_DECLARED`; original catalogue parameter window `1d/5d`; declared units `percent`. These are input-mapping assertions, not proof of live source capability.
- **Mathematical law:** 100*(R274_t/R274_ref-1), JPY per USD quotation; preserve quote direction.
- **Controlled inputs:** R274 prior 100 JPY/USD, current 120 JPY/USD.
- **Independent result:** 100*(120/100-1)=+20% in JPY per USD; inverse quotation would be -16 2/3%. This is an equation-derived witness, not output computed from the M01 implementation or a certified market sample.
- **Necessary history/fixture:** Two same-direction native currency-pair quotes at selected 1d or 5d profile horizon with compatible sessions.
- **Discriminating fault/refusal:** Invert JPY/USD to USD/JPY; mix quote directions; native units unproved; reference zero; after-anchor wrong observation.
- **M01 reuse disposition:** REUSE_K03_PERCENT_FORMULA; require explicit instrument quote direction, not generic currency code.
- **Unresolved exact receiver:** DATA-001/FX source and M00: native pair convention, date/time and missing values; M02 exact ratio carrier.

### D050 — HKD/USD rate of change

- **Effective direct raw input:** `R275`; predecessor `NONE_DECLARED`; original catalogue parameter window `1d/5d`; declared units `percent`. These are input-mapping assertions, not proof of live source capability.
- **Mathematical law:** 100*(R275_t/R275_ref-1), HKD per USD, native side/direction preserved.
- **Controlled inputs:** R275 prior 7.5 HKD/USD, current 7.8 HKD/USD.
- **Independent result:** 100*(7.8/7.5-1)=+4%. This is an equation-derived witness, not output computed from the M01 implementation or a certified market sample.
- **Necessary history/fixture:** Two same-series eligible HKD per USD values and selected daily/5d anchor with comparable quotes.
- **Discriminating fault/refusal:** Unlawful inverse FX conversion, zero prior, mismatched settlement/source/calendar or feed variant.
- **M01 reuse disposition:** REUSE_PERCENT_FORMULA; retain distinct HKD/USD R275 and profile.
- **Unresolved exact receiver:** FX source/M00: HKD/USD native series and bid/ask or midpoint convention, daily/5d reference; M02 representation.

### D051 — CNY/USD rate of change

- **Effective direct raw input:** `R276`; predecessor `NONE_DECLARED`; original catalogue parameter window `1d/5d`; declared units `percent`. These are input-mapping assertions, not proof of live source capability.
- **Mathematical law:** 100*(R276_t/R276_ref-1), CNY per USD.
- **Controlled inputs:** R276 prior 7.5 CNY/USD, current 7.2 CNY/USD.
- **Independent result:** 100*(7.2/7.5-1)=-4%. This is an equation-derived witness, not output computed from the M01 implementation or a certified market sample.
- **Necessary history/fixture:** Two corresponding same-method CNY per USD quotes, admitted 1d/5d reference and cutoff.
- **Discriminating fault/refusal:** Confuse onshore CNY with offshore CNH, reverse orientation, zero prior, unavailable session/cutoff.
- **M01 reuse disposition:** REUSE_PERCENT_FORMULA; distinct R276 source requirement.
- **Unresolved exact receiver:** FX source/M00: precise onshore/offshore pair/quote side/units/session; M02 selected history and exact result.

## E1.5 — independent documentary challenge

Controlled JPY/USD increase100→120 produces +20%, but its inverse quote produces −16 2/3%; a fixture with only the numerically aligned inverted source must not be treated as valid R274. For D048 a 20-day anchor cannot use 5-day data, and a re-based broad USD index must not mix index base versions.

**Negative witness semantics:** provide genuinely eligible source events and calendar/profile state *before* introducing a test fault. An empty reader, exhausted pagination cursor, wrong test phase or fixture conveniently pre-populated by a helper cannot stand in for a semantic refusal. Inspect real M00 public projection, declared mapping/versions, selected occurrence IDs, immutable retry/history and future SQLite readback at implementation time; these were not executed or accepted here.

**Reconciliation:** D048, D049, D050, D051 each has a distinct numeric witness and source/selection/refusal contract. All 4 are `AUDITED_WITH_PRECISE_HOLDS`; no `ESTABLISHED_NATIVE` or `M02_ACCEPTED` claim. D028 legacy contradiction is retained rather than silently applying the wrong R044 fixture. Cross-family dependencies remain as mapped; this is a preparation packet only.
