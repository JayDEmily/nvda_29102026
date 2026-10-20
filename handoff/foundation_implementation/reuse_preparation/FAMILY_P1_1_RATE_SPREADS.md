# P1.1 — source/logic reuse family: FRED rate spreads (D042, D043, D047)

**Status:** SOURCE/LOGIC TRACED ONLY. No independent expected-witness authoring (P2.1), historical fixture precondition audit (P1.2), provider certification, new test, M02 implementation or acceptance. Snapshot base `58bbc7d7a7f7637ddab2cb74239913a3f2becc0e`.

## Bounded dependency-closed family

| D ID | Accepted exact formula from calculation brief §5 / current catalogue | Raw input mapping | Unit/output | M01 location |
|---|---|---|---|---|
| D042 | `100 × (R249 − R247)` | R249=10Y yield, R247=2Y yield | decimal yield fractions in, Decimal percentage points out | `_stage1.py:1440–1442` |
| D043 | `100 × (R249 − R246)` | R249=10Y yield, R246=3M yield | decimal yield fractions in, Decimal percentage points out | `_stage1.py:1440–1442` |
| D047 | `10000 × (R257 − R256)` | R257=SOFR, R256=EFFR | decimal rate fractions in, Decimal basis points out | `_stage1.py:1443–1444` |

All three belong to accepted `K02_ALGEBRA`/`P_BASIC` and have zero D predecessors; the static family is dependency-closed on raw R inputs **conditional on independently admitted M00 projections**. The older workbook `Derived Signals!A46:O46`, `A47:O47` and `A51:O51` confirms the signal wording and rates. It does not establish an enabled live FRED collector.

## Original source-to-actual-seam trace

- **Legacy M01:** `src/nvda_desk/derived_signal_calculation_truth/_stage1.py:1387–1460:_eval_k02`, exactly the three named branches; its `api.py:3092–3155:create_owner` selects public M00 projection mappings, immutable parameter sets, selection policies and units; `api.py:3069–3091:materialise` is the public result route. The stage-1 `KernelValueV1` and wide `object`-shaped kernel result are **not** an admitted new M02 typed public contract.
- **Existing authored test evidence:** `tests/product/derived_signal/test_m01_f4_rc02_scalar_algebra_public.py:29–38,41–117,120–153` includes controlled M00 raw projection per field, expected numeric examples (D042 1.25pp, D043 1pp, D047 10bp), omitted input, future-received and cross-subject refusals, repeat materialisation and raw lineage. These are old authored fixture assertions, **not newly run or independently re-proved M02 expectations**.
- **Current M02:** `src/nvda_desk/market_measurement_truth/api.py:139–229,322–349` defines fixed `CalculationDefinitionV1`, policy, unit convention, raw binding, public lineage/occurrence and `create_owner`; it has a bounded scalar Decimal path plus separately authorised ratio paths. D042/D043/D047 are **not admitted** in the saved G6.1 checkpoint. Do not import M01's private `_stage1` or `_postgres` or widen the new public seam by inference.
- **Original workbook native-field navigation:** `Raw Signals!A250:M250` R246 = FRED `DGS3MO`; `A251:M251` R247=`DGS2`; `A253:M253` R249=`DGS10`; `A260:M260` R256=`DFF`; `A261:M261` R257=`SOFR`. All label the native field `value`, unit **Percent**, cadence Daily. The M01 synthetic fixture uses **canonical decimal fractions** (e.g. `0.0525`) and an explicitly configured identity unit convention; it does **not** prove the native Percent→decimal conversion or date/vintage synchronisation.

## Proposed reuse disposition (not implementation authority)

| Existing mechanism / proposition | Disposition | Reason / future boundary |
|---|---|---|
| Three fixed scalar equations and direction of signed differences | **REUSE_AS_SPEC** | Exactly matches accepted §5 laws and M01 direct branch; preserve sign, percentage-points versus basis-points scaling |
| M01 controlled M00 projection tests and negative input sequences | **REUSE_AS_SPEC** | Propositions/lineage are useful, but old fixture construction/old test paths cannot be counted as new admitted M02 proof |
| M01 `_eval_k02` private dispatcher and wide `object` carrier | **REEXPRESS** | Implement future bounded typed M02 meaning through its authorised public seam; no M01 private runtime dependency |
| M01 `_postgres.py` and previous owner persistence | **NOT_REUSABLE** for new backend assurance | SQLite owner-local profile is accepted; PostgreSQL test/role assumptions cannot substitute for SQLite first-write/readback/isolation proof |
| Native FRED `Percent` conversion, date/revision meaning, multi-series time alignment, missing/sentinel values | **UNKNOWN** | Workbook names source field only; requires exact source contract and controlled policy version before operational eligibility |

## Source and proof differences outstanding

- Static source closure is 5 unique raw inputs with no D predecessor; however M00 projections, compatible policy/clock semantics and each canonical Decimal scaling remain explicit independent requirements.
- Legacy tests use separate M00 admissions and a synthetic 10-second staleness/skew policy; this is **fixture construction**, not an accepted FRED daily alignment convention. P1.2 must examine these history/selection/refusal prerequisites before defining any new fixture.
- P2.1 must independently compute positive/zero/negative and precision witnesses from the accepted laws, rather than copying the M01 `CASES` table as the expected-answer authority.
- The exact FRED source contract, units, missing values, official observation dates, release/revisions, and admissible selection across different rate series are pending source research; no live data exists in this assessment.
- **No Stage-2 production kernel is required for these three K02 cases.** This is a bounded source assertion, not a claim that all 126 foundation routes have production logic.

**P1.1 exit:** source/branch, test/fixture, raw closure, current public seam and each reuse disposition are identified. No negative claim about strategy-dependent chains elsewhere; none is needed in this selected three-ID family.
