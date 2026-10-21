# P1.2–P2.2 — Rate-spread preparation: D042, D043, D047

**State:** Documentary M01-to-M02 reuse evidence; NOT new executable proof, implementation authority, native FRED admission or independent reviewer acceptance. Read with `FAMILY_P1_1_RATE_SPREADS.md`. Source snapshot `19c14ee`; M01 `src/nvda_desk/derived_signal_calculation_truth/_stage1.py:1387–1445`, `tests/product/derived_signal/test_m01_f4_rc02_scalar_algebra_public.py:19–151`; governing `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md:114–129`, current Annex B.

## P1.2 — actual synthetic fixture/historical prerequisites

- These are **latest-eligible scalar selections**, not multiday return windows. Each valid M01 fixture has exactly one occurrence per required R field: D042 `{R247,R249}`; D043 `{R246,R249}`; D047 `{R257,R256}`. Each has its own M00 `RawObservationOccurrenceV1`, independent sequence number, explicit `metric.value` native path, `raw_signal_catalogue_ids`, NVDA synthetic subject, `true_instant`, received timestamp, source/provider and projection mapping. Entries are admitted into an in-memory M00 owner; they are not FRED service responses or stored SQLite proof.
- In the old fixture `NOW=2026-10-09T14:00:00Z`. For each enumerated field sequence `i`, event and receipt are `NOW - i seconds`; request as-of/receipt cutoff both equal NOW. Controlled policy permits `maximum_staleness=10s`, `maximum_clock_skew=10s`. Those values are **test-fixture parameters**, not established FRED publication, vintage or cross-series alignment policy. A new target may choose them only under an explicitly admitted profile.
- A missing final mapped field produces refusal, as does setting its receipt to `NOW+1s` or its subject to `OTHER`; these are three distinct controlled refusals in the original tests. Exact duplicate request returns the same occurrence via the M01 public owner. These tests do **not** establish M02 durable first-write, SQLite restart, pagination or immutable readback; no pagination/history volume is required by the scalar arithmetic itself.
- Negative-case preconditions: first independently admit all necessary other R fields and keep their versions/subject valid; then omit or mis-stamp **only** the intended target field. For future receipt, preserve native event and mapping identity and put receipt **after cutoff**; do not accidentally fail because mapping is absent. For subject mismatch, keep source/mapping and canonical value unchanged.
- Trigger-to-observation: complete two-field mapped public selection -> signed Decimal arithmetic; missing/late/cross-subject selection -> no occurrence; identical retry -> same first result. These are M01 behavioural witnesses only. No temporal interpolation, market-session boundary or native FRED revision semantics is established.

## P2.1 — independent arithmetic witnesses

Canonical rate/yield fractions, not displayed FRED `Percent` strings. Inputs below are controlled **Decimal representations**; each expected result is calculated by explicit subtraction and integer scaling from the accepted equations, not by executing M01/M02.

| D | Inputs (canonical fractions) | Expected | Reason |
| --- | --- | --- | --- |
| D042 | R249=.0425, R247=.0390 | +0.35 percentage points | `100*(.0425-.0390)` |
| D042 | R249=.0390, R247=.0425 | −0.35 percentage points | signed inversion |
| D042 | R249=.04, R247=.04 | 0 percentage points | equal rates |
| D043 | R249=.0430, R246=.0410 | +0.20 percentage points | `100*(.0430-.0410)` |
| D043 | R249=.0410, R246=.0430 | −0.20 percentage points | signed inversion |
| D043 | R249=.04, R246=.04 | 0 percentage points | equal rates |
| D047 | R257=.0532, R256=.0530 | +2 basis points | `10000*(.0532-.0530)` |
| D047 | R257=.0530, R256=.0532 | −2 basis points | signed inversion |
| D047 | R257=.05, R256=.05 | 0 basis points | equal rates |

No denominator or positivity restriction exists in these three subtractions; an invented “rates must be positive” rejection is prohibited. Signed precise decimal fractions are algebra inputs, not native-provider value certifications. Each D's exact R IDs and `P_BASIC` source/equation version must be retained in any eventual M02 proof.

## P2.2 — source certification holds

Workbook `Raw Signals!A250:M261` identifies FRED `DGS3MO→R246`, `DGS2→R247`, `DGS10→R249`, `DFF→R256`, `SOFR→R257`, with `value`, **Percent**, daily. Current per-field publisher implementation, missing-marker treatment, official observation date versus ingestion timestamp, revised vintages, calendar alignment across two series and the versioned Percent→fraction converter are **UNKNOWN** in this assessment. Existing synthetic `native_units='canonical'` proves none of them. Source-profile owner must supply per-series R mapping/projection variant, exact percent conversion, observation and receipt clock definition, missing flag, vintage/selection and allowed alignment. This is a targeted source-contract request; no native range is invented.

**P1/P2 reuse dispositions:** equations and negative sequences `REUSE_AS_SPEC`; M01 dispatcher and public owner `REEXPRESS` under admitted typed M02 contracts; M01 PostgreSQL-specific ownership/role fixtures `NOT_REUSABLE` as SQLite evidence. Applicable SQLite public/writer/read isolation, late-receipt, immutable identity and fresh-process review remain future M02 proof; original M01 tests cannot be automatically admitted as M02 proof.
