# Engineering Brief — M00 Raw Observation Truth, Native IBKR Compatibility and Verified Synthetic Output

**Document:** `NVDA-M00-STANDALONE-BRIEF-V3`  
**Issued:** 27 October 2026, 16:22 AEDT (Australia/Melbourne, UTC+11)  
**Status:** Owner-commissioned *worker handover specification*. Exact previously authorised synthetic inputs are carried forward; the additions and required outputs below are the agreed M00 development and acceptance targets. **No implementation, output readback, new test pass, PostgreSQL verification or live IBKR certification is claimed by this document.**  
**Current evidence anchor:** NVDA project Git `17d7553cf3ad92700f849f696134de67b64b0dfa`; repository source and governance must be freshly checked against the worker's actual latest bundle. This anchor is not an assertion that M00 was originally frozen at this commit.

## 0. Assignment, authority and stop conditions

**Assignment:** Implement and verify the complete M00-facing, authorised IBKR-representative *synthetic raw observation input → actual M00 admission → persisted observation → public raw projection → reusable verified synthetic output* pipeline for NVDA underlying shares and selected NVDA call **and** put options, including SMART depth, direct depth, asynchronous Level I quote constituents, correct native semantics, receipt ordering and provider control/discontinuity events. Produce an independently consumable, deterministic, **versioned M00 output fixture**. It must contain real M00 outputs, not a mock of the intended output. A downstream calculation worker may use the separately specified expected oracle immediately, but actual-production status requires matching real M00 output evidence.

**Entirely standalone:** All required input values, output obligations, rejection/absence expectations and source locators are stated here. No companion engineering brief or completion of another module is required. External upstream acquisition, deployed SQL and downstream derived-signal calculations are **not** in scope. Other modules' documents are not prerequisites.

**Current governing authority:** The worker must locate/read current `GUARDRAILS.md`, applicable `AGENTS.md` / `AGENTS.override.md`, and active `EXEC_PLAN.md` **in full**; inspect current normative raw-truth contracts, current M00 source, relevant tests and exact frozen M00 baseline. Follow user > applicable governance > current plan > normative contracts > tests > code/evidence. This document records explicit owner commissioning of narrowly necessary M00 production changes **if a requirement-relative defect is demonstrated**. It is *not* authority to edit frozen guardrails, weaken accepted tests, change unrelated signal definitions, alter destructive Git history or bypass required independent review/acceptance. If a governing authority specifically requires an additional unfreeze/plan approval, report the conflict and pause only the dependent modification; complete independent fixture/output work.

**Execution:** inspect → define immutable fixture inputs and independent expected-oracle outputs → exercise public M00 seams → preserve first failing requirement/witness → make smallest authorised production or test correction → repeat bounded relevant proof → independently verify as required → deliver verified outputs/checkpoint. Do not stop at an analysis where in-scope implementation and proof remain available. Do not label a proposed result `PASS` on assertion alone.

**Development backend:** SQLite is **mandatory** for current persistence and independent read-only reopen verification. PostgreSQL is **not available as an execution prerequisite** in the current controlled environment: preserve adapter compatibility; identify any PostgreSQL code implication statically if changed, defer its actual runtime verification and do not mark parity or live database integration certified. Do not install or require PostgreSQL just to complete this task. The historical signal-specific two-case/independent-review rules are not a generic limit on this separately commissioned M00 test programme; apply whichever active governance rule actually covers the M00 task.

## 1. M00 semantic contract (test the current implementation, do not assume failure)

1. Admit one `RawObservationOccurrenceV1` per **native callback** (or clearly documented provider control callback), with immutable occurrence identity, exact contract/subject, source provider/variant/callback, `native_record`, receipt UTC, optional matching epoch nanoseconds, scope and monotonic ingestion sequence, temporal kind, native timestamp when genuinely supplied, and exact provenance. Never represent four asynchronously collected option quote fields as one *native* callback.
2. Preserve raw vendor **side** `0=ASK`, `1=BID`; **operation** `0=INSERT`, `1=UPDATE`, `2=DELETE`; zero-based position relative to its subscribed book/side. Error `317` is **not** depth operation 317, and error `316` is **not** a depth operation. No side inversion, fabricated event timestamp, invented field, synthetic book row or duplicate normalised fact may be passed off as provider-native data.
3. Native `updateMktDepthL2` has no provider event timestamp parameter: `source_temporal_kind=receipt_only`, `source_timestamp_raw=None` and native timezone `None`; retain actual receipt time and ingestion order. A timestamped native shares `tickByTickBidAsk` may be `true_instant` if its real source event timestamp is preserved. A synthetic source time is a **test timestamp**, never a claim of actual exchange observation.
4. `RawSignalProjectionMappingV1` selects a particular `native_field_path` for each R ID; `project_raw_value()` returns exactly the native type/value, source IDs, mapping/version, receipt, sequence/scope, selection identity and temporal fields. Missing native fields project **absence**, never default zero or an invented callback. `list_projected_raw_history()` must accept receipt cutoff with `event_at_or_before_utc=None`, return deterministic paginated history and omit receipt-only observations under a non-null event-time cutoff by design.
5. A 30-second capture slot is not the raw callback cadence. Persist all individually received raw events. Keep identities distinct for STK, CALL, PUT, SMART/direct, subscription/request, generation, MPID/exchange and source variant; never merge scopes by coincidence of timestamps or sequence integers.
6. **Error/discontinuity discoverability:** Persist separately identified provider `error(reqId=...,errorCode=317)` and `316` events, with receive clock, request identity and order relative to affected depth, no synthetic R187 operation. Prove a consumer can discover **all applicable controls in an ordered public/history interface using identity/cutoff**, not only retrieve a control event when its ID is supplied in advance. Existing M00 may admit and read a known-ID control event; that alone is insufficient to claim ordered discovery. If no sanctioned public control-history seam exists, establish a failing proof, make the smallest governed additive extension, or report an explicit authority blocker; do not quietly enumerate private database tables or misuse a raw-signal R ID. Specify generation/invalidity lifecycle as a versioned, non-native control envelope or read model; do not fabricate broker callback arguments.
7. `R001` collector-receipt **projection**, if needed, must have genuine collector receipt provenance. The current mapping engine projects fields in `native_record`, not the observation envelope directly. Existing controlled tests place an independently traceable typed UTC receipt under `native_record['time']['receipt']`. If this derived carrier is reused, identify it as **collector-added metadata** and test it equals `received_ts_utc`; do not claim that IBKR sent the value or that it is exchange event time. If a cleaner public-envelope projection is needed, prove requirement and govern the change.
8. Side-specific book reconstruction, completeness, skew policy, midpoint/microprice/concentration and other **derived calculations are not M00 outputs**. Raw M00 output must supply exactly the facts, absence, order and discontinuities enabling a separately authorised consumer to decide.

## 2. Data authority, fixture isolation and exact mapping oracles

Keep the following distinct fixture families **immutable** under their existing V1 identities. They are *separate controlled scenarios*, never one merged provider trace. All have source-labelled **synthetic** identities; no `IBKR-live` / account-entitled / deployed-market attribution:

- **A:** `NVDA-IBKR-M00-SYNTHETIC-INPUT-V1`, reference date 20 Oct 2026; source shape for atomic shares quote, asynchronous selected CALL and PUT Level I, SMART STK/CALL/PUT depth; source scenarios below.
- **B:** `NVDA-CONTROLLED-IBKR-RECEIPT-BOOK-V1`, reference date 26 Oct 2026; seven immutable SMART depth mutations S01–S04/O01–O03 below, preserved **exactly**.
- **C:** `NVDA-M00-COHERENT-INTEGRATION-V2`, new **separate** controlled native-integration scenario; reconciles option Level I/II prices and includes six-field direct depth. Do **not** silently modify A/B to create C.

For native-shaped depth fields, required catalogue mapping per exact selected source variant:

| Raw R ID | Native field path | Type | Stock units | Option units |
|---|---|---|---|---|
| `R185` | `position` | int | book position | book position |
| `R187` | `operation` | int (0,1,2) | operation | operation |
| `R188` | `side` | int (0 ask,1 bid) | side | side |
| `R189` | `price` | Decimal | USD/share | USD/underlying share premium |
| `R190` | `size` | Decimal/integral numeric native carrier | shares | contracts |
| `R192` | `position` | int | direct book position | direct book position |
| `R193` | `marketMaker` | str | MPID or exchange, qualified by `isSmartDepth` and subscribed source | same |
| `R194` | `operation` | int | operation | operation |
| `R195` | `side` | int | side | side |
| `R196` | `price` | Decimal | USD/share | USD/underlying share premium |
| `R197` | `size` | Decimal/integral native | shares | contracts |

Level I raw roles: `R033=bid_size`, `R034=bid_price`, `R035=ask_price`, `R036=ask_size`; preserve one occurrence/ID for a genuinely atomic shares quote, **four distinct** occurrence IDs for four independently received options callbacks. `tickPrice(1)` bid price, `tickSize(0)` bid size, `tickPrice(2)` ask price, `tickSize(3)` ask size. Use exact `Decimal` values as test values with explicit expected type. Native callback shape, nested/native path and selection identity mapping may be adapted transparently into a **versioned envelope-to-native field map** but not change the values or fabricate provider fields. Do not conflate `source_provider` (synthetic origin) with native vendor named in metadata.

**Exact controlled source namespaces:** Fixture A uses `source_provider=foundation-controlled-ibkr-m00-v1`, with `source_variant=ibkr-bidask-atomic/native-v1` (A1), `ibkr-async-l1/native-v1` (A2/A3), or `ibkr-smart-depth/native-v1` (A4–A6). Fixture C uses `source_provider=foundation-controlled-ibkr-m00-coherent-v2`, with `source_variant=ibkr-smart-depth/native-v2` (C1) or `ibkr-direct-depth/native-v2` (C2/C3). These are **synthetic harness identifiers**, not live IBKR vendor authentication. Every envelope must explicitly distinguish the hypothetical native callback kind (`tickByTickBidAsk`, `tickPrice`, `tickSize`, `updateMktDepthL2`, `error`) from a source provider string and any controlled/collector metadata. Fixture B retains its own exact source namespace specified below. All mapping IDs are individually versioned with the fixture/scenario/R-role, so no contradictory source mapping is co-selected.

**Deterministic identity convention:** For family A, except the named A1 identity, each positive event ID is `NVDA-M00-A-V1-{scenario}-SEQ{sequence}` with `{scenario}` exactly `A2`, `A3`, `A4`, `A5`, or `A6` as appropriate and the sequence displayed in its table (e.g. `NVDA-M00-A-V1-A2-SEQ11`). A1 uses `SYN-L1-STK-ATOMIC-01`. Fixture B keeps the seven literal `SYNTH-IBKR-V1-*` IDs shown. Fixture C uses its literal `COH-*` event IDs. Source request, generation and requested exchange are immutable typed *collector/control-envelope* identity/provenance; if a current mapping must select them via a nested native_record carrier, use an explicitly declared versioned **collector metadata** subobject, never attribute those synthetic fields to the actual IBKR callback. IDs are synthetic proof identities, not actual IBKR request IDs or `conId` values.

**Common synthetic reference for A/C:** `2026-10-20T12:40:00.000Z`; cutoff `2026-10-20T12:40:01.000Z`, except isolated C receipt timestamps where specified. STK key `NVDA-STK-CONTROL-1`; CALL `NVDA-OPT-C100-CONTROL-1` (`NVDA|OPT|2026-10-23|100|C|100|USD`); PUT `NVDA-OPT-P100-CONTROL-1` (same expiry/strike with P). These are hypothetical test keys, **not** asserted real `conId`s or proof the historical option traded. Native depth sequences are distinct per subscription/generation scope. Units: underlying shares, option displayed contracts, premium USD per underlying share, multiplier retained independently.

### A1. Atomic shares Level I

One `tickByTickBidAsk` callback, event timestamp `12:40:00.000Z`, received `12:40:00.080Z`, seq `1`, scope `STK1/BIDASK/G1`, ID `SYN-L1-STK-ATOMIC-01` (or this ID + explicit event suffix), `true_instant`. Exact native prices `bid_price=Decimal('99')`, `ask_price=Decimal('101')`, sizes `bid_size=Decimal('3')` shares, `ask_size=Decimal('1')` shares. **Expected public projections:** exactly `R033=3`, `R034=99`, `R035=101`, `R036=1`, four results sharing the **same** occurrence ID, source event timestamp, receipt and scope, with each exact R-specific mapping.

### A2. Independently received CALL Level I

Contract `NVDA-OPT-C100-CONTROL-1`, request `OPT-C100-R1`, generation `OPT-L1-G1`, scope `OPT-C100/L1/G1`, `receipt_only`, absent native event timestamp. **Each line is a separate M00 occurrence and a single intended R projection.**

| Sequence | Receipt 20 Oct (UTC) | Callback/native path | Exact native value | Expected R |
|---:|---|---|---|---|
| 11 | 12:40:00.100 | `tickPrice(1)`/`bid_price` | `Decimal('1.20')` | R034 |
| 12 | 12:40:00.130 | `tickSize(0)`/`bid_size` | `Decimal('10')` contracts | R033 |
| 13 | 12:40:00.160 | `tickPrice(2)`/`ask_price` | `Decimal('1.40')` | R035 |
| 14 | 12:40:00.180 | `tickSize(3)`/`ask_size` | `Decimal('8')` contracts | R036 |

### A3. Independently received PUT Level I

Contract `NVDA-OPT-P100-CONTROL-1`, request `OPT-P100-R1`, generation `OPT-P100-L1-G1`, scope `OPT-P100/L1/G1`, `receipt_only`; four distinct occurrences:

| Sequence | Receipt 20 Oct (UTC) | Callback/native path | Exact native value | Expected R |
|---:|---|---|---|---|
| 15 | 12:40:00.200 | `tickPrice(1)`/`bid_price` | `Decimal('2.20')` | R034 |
| 16 | 12:40:00.220 | `tickSize(0)`/`bid_size` | `Decimal('6')` contracts | R033 |
| 17 | 12:40:00.250 | `tickPrice(2)`/`ask_price` | `Decimal('2.40')` | R035 |
| 18 | 12:40:00.270 | `tickSize(3)`/`ask_size` | `Decimal('4')` contracts | R036 |

For A2 and A3 the *synthetic consumer-side* quote-coherence test may use an explicitly versioned `250 ms` oldest/newest receipt skew and `1000 ms` latest-field age criterion, for its **test context only**, **not** approved production policy. A2's skew is 80 ms, newest age at `12:40:00.300Z` is 120 ms; A3 skew is 70 ms, newest age at `12:40:00.400Z` is 130 ms. **M00 shall preserve callback facts even if these synthetic downstream assembly policies refuse them.** It must never emit a falsely native atomic options event.

### A4. Native-shaped SMART stock depth, receipt only

Scope `STK1/SMART/G1`, request `STK-SMART-R1`, generation `STK-SMART-G1`, stock subject, each row a distinct `updateMktDepthL2(isSmartDepth=True)` occurrence, `source_timestamp_raw=None`:

| Seq | Receipt 20 Oct (UTC) | Operation | Side | Position | Price Decimal USD/share | Size Decimal shares |
|---:|---|---:|---:|---:|---|---|
| 21 | 12:39:59.100 | 0 | **1 BID** | 0 | 99.00 | 5 |
| 22 | 12:39:59.200 | 0 | **1 BID** | 1 | 98.00 | 3 |
| 23 | 12:39:59.300 | 0 | **0 ASK** | 0 | 101.00 | 2 |
| 24 | 12:39:59.400 | 0 | **0 ASK** | 1 | 102.00 | 4 |

Each has exact five public projections R185/R187/R188/R189/R190 with same per-row occurrence ID, request/generation and ordered receipt. Expected selected **raw** sizes by side/position: BID `(5,3)`; ASK `(2,4)`. These are readback completeness witnesses, **not** M00-calculated depth signals.

### A5. Legacy SMART CALL depth — **isolated mathematical scenario only**

Same CALL key, scope `OPT-C100/SMART/LEGACY-G1`, a historical **separate** synthetic market state (do **not** combine with A2 or C quote):

| Seq | Receipt 20 Oct (UTC) | Operation | Side | Position | Price Decimal | Size Decimal contracts |
|---:|---|---:|---:|---:|---|---|
| 31 | 12:39:59.100 | 0 | 1 BID | 0 | 99.80 | 5 |
| 32 | 12:39:59.200 | 0 | 1 BID | 1 | 99.00 | 7 |
| 33 | 12:39:59.300 | 0 | 0 ASK | 0 | 100.20 | 3 |

The separately specified synthetic midpoint `100.00` and inclusive ±`0.50` range are calculation-side test oracles **only**; **not** fields output by M00. Preserve A5's exact bytes/identity and exclude it from coherent A2/C market traces.

### A6. SMART PUT depth

Contract `NVDA-OPT-P100-CONTROL-1`, scope `OPT-P100/SMART/G1`, request `OPT-P100-SMART-R1`, separate generation:

| Seq | Receipt 20 Oct (UTC) | Operation | Side | Position | Price Decimal | Size Decimal contracts |
|---:|---|---:|---:|---:|---|---|
| 34 | 12:39:59.600 | 0 | 1 BID | 0 | 2.20 | 6 |
| 35 | 12:39:59.700 | 0 | 0 ASK | 0 | 2.40 | 4 |

No missing second levels are invented. Expected two distinct five-role R projection sets, and PUT identity must not be co-selected with CALL.

### B. Immutable alternative seven-event receipt book — independent scenario

Identity `NVDA-CONTROLLED-IBKR-RECEIPT-BOOK-V1`, synthetic provider `foundation-controlled-ibkr-book-v1`, variant `SMART`, `source_product_api=TWS_SOCKET_API_SYNTHETIC_SPECIMEN`, callback `updateMktDepthL2`, `isSmartDepth=True`, `marketMaker=SYNTH-EXCHANGE`, `receipt_only` with no provider timestamp/timezone; **one occurrence per row**, full five native fields. Stock subject `NVDA/STK/USD/SMART/TEST-ONLY` scope `SYNTH-STK-SMART-01` generation `GEN-STK-01`, option subject `NVDA/OPT/20261030/100/C/100/USD/SMART/TEST-ONLY` scope `SYNTH-OPT-SMART-01` generation `GEN-OPT-01` (independent of fixture A).

| Observation ID | Scope | Receipt UTC (2026-10-26) | Seq | Operation | Side | Pos | Price Decimal | Size Decimal |
|---|---|---|---:|---:|---|---:|---|---|
| `SYNTH-IBKR-V1-S01` | STK | 14:00:01 | 1001 | 0 | 1 BID | 0 | 99.00 | 5 |
| `SYNTH-IBKR-V1-S02` | STK | 14:00:02 | 1002 | 0 | 1 BID | 1 | 98.50 | 3 |
| `SYNTH-IBKR-V1-S03` | STK | 14:00:03 | 1003 | 0 | 0 ASK | 0 | 101.00 | 2 |
| `SYNTH-IBKR-V1-S04` | STK | 14:00:04 | 1004 | 0 | 0 ASK | 1 | 101.50 | 4 |
| `SYNTH-IBKR-V1-O01` | OPT | 14:00:05 | 2001 | 0 | 1 BID | 0 | 99.80 | 5 |
| `SYNTH-IBKR-V1-O02` | OPT | 14:00:06 | 2002 | 0 | 1 BID | 1 | 99.00 | 7 |
| `SYNTH-IBKR-V1-O03` | OPT | 14:00:07 | 2003 | 0 | 0 ASK | 0 | 100.20 | 3 |

All seven rows have exact public five-role projections and are retrievable via receipt cutoff `2026-10-26T14:00:10Z` with `event_at_or_before_utc=None`. A non-null event-time cutoff must exclude all seven. Expected scoped stock size positions `(bid 5,3; ask 2,4)` and option `(bid 5,7; ask 3)` are **external test oracles**, not M00's own calculated records. Any provider timestamp inserted to 'make event filtering work' is a failing test.

### C1. Integrated coherent SMART CALL depth — new, separate controlled fixture V2

Use CALL `NVDA-OPT-C100-CONTROL-1`, the A2 Level I values **as independent reference inputs**, and new independent receipt-only book scope `OPT-C100/SMART/COHERENT-V2`, generation `OPT-C100-SMART-COHERENT-V2` (unique per stream). Avoid reusing A5's legacy option prices. Each event is operation 0, native `isSmartDepth=True`, native side 1 BID/0 ASK, request/venue identity present as controlled metadata.

| Event ID | Receipt UTC (20 Oct) | Seq | Side | Pos | Price Decimal USD/share | Size Decimal contracts |
|---|---|---:|---:|---:|---|---|
| `COH-SMART-C01` | 12:39:59.100 | 301 | 1 BID | 0 | 1.20 | 5 |
| `COH-SMART-C02` | 12:39:59.200 | 302 | 1 BID | 1 | 0.70 | 7 |
| `COH-SMART-C03` | 12:39:59.300 | 303 | 0 ASK | 0 | 1.40 | 3 |

**Independent expected M00 outputs:** 3 distinct occurrences; `3 × 5=15` exact public projection rows for the five roles; same per-event identity across the five projections; no projected R187=317. Midpoint `1.30`, inclusive band `0.80..1.80`, depth count `5+3=8` (excluding `0.70` size 7) are **external checking examples only**, not calculated by M00 or represented as synthetic native source fields.

### C2. Native direct-depth **shares** — six-role test

One controlled direct subscription on an explicitly identified requested exchange `SYNTH-DIRECT-EXCHANGE-1`; `isSmartDepth=False` means native `marketMaker` is **MPID** `ALPHA` or `BETA`, **not** an exchange. Each callback contains all six native fields (`position`,`marketMaker`,`operation`,`side`,`price`,`size`) and a separate request exchange identity in its admitted envelope/provenance. Contract STK, scope `STK1/DIRECT-EXCH1/GEN1`, `receipt_only`, source time absent, operation 0, native side codes. Positions are per **book side within the subscribed book**, not restarted independently per MPID:

| Event ID | Seq | Receipt UTC (20 Oct) | MPID | Side | Pos | Price Decimal | Size Decimal shares |
|---|---:|---|---|---|---:|---|---|
| `COH-DIRECT-STK-01` | 401 | 12:39:58.100 | ALPHA | 1 BID | 0 | 99.00 | 4 |
| `COH-DIRECT-STK-02` | 402 | 12:39:58.200 | BETA | 1 BID | 1 | 98.50 | 1 |
| `COH-DIRECT-STK-03` | 403 | 12:39:58.300 | ALPHA | 0 ASK | 0 | 101.00 | 2 |
| `COH-DIRECT-STK-04` | 404 | 12:39:58.400 | BETA | 0 ASK | 1 | 101.50 | 1 |

**Expected M00 output:** four immutable occurrences and **24** independent six-role R projections; native MPIDs preserved, source exchange separately identified. An external check can group display quantities as ALPHA 6/BETA 2 shares, but M00 must **not** emit a concentration index, aggregate or a fabricated exchange label.

### C3. Native direct-depth **selected CALL** — six-role test

Same controlled CALL key, separate requested exchange `SYNTH-DIRECT-OPT-EXCHANGE-1`, scope `OPT-C100/DIRECT-EXCH1/GEN1`; receipt-only, operation 0, native `isSmartDepth=False`. These option observations are **conditional capability specimens**, not proof IBKR supplies or the account subscribes to direct option Level II.

| Event ID | Seq | Receipt UTC (20 Oct) | MPID | Side | Pos | Price Decimal | Size Decimal contracts |
|---|---:|---|---|---|---:|---|---|
| `COH-DIRECT-CALL-01` | 501 | 12:39:58.500 | ALPHA | 1 BID | 0 | 1.20 | 4 |
| `COH-DIRECT-CALL-02` | 502 | 12:39:58.600 | BETA | 1 BID | 1 | 1.10 | 1 |
| `COH-DIRECT-CALL-03` | 503 | 12:39:58.700 | ALPHA | 0 ASK | 0 | 1.40 | 2 |
| `COH-DIRECT-CALL-04` | 504 | 12:39:58.800 | BETA | 0 ASK | 1 | 1.50 | 1 |

**Expected M00 output:** four distinct observations; **24** six-role public projections, no side/MPID/source exchange substitution. A selected PUT is already mandatory in A3/A6; if direct PUT coverage is required by current accepted raw contract, construct it as a separately versioned symmetric fixture before certifying full per-right direct coverage. Do not silently interpret CALL-only direct tests as direct PUT coverage.

## 3. M00 expected outputs, not just authorised inputs — hard acceptance contract

**The exact expected raw outputs are authorised by this document as test oracles.** They are **not** claims of already executed/accepted M00 output. For each specified event, construct an immutable expected-output manifest independently of the production projection code, with:

- `fixture_id`, `fixture_version`, `scenario_id`, native callback kind and source-provider label `synthetic`, source variant, subscription/request, generation, exact contract/subject, native field path, mapping ID+version, catalogue R ID and native units;
- `observation_occurrence_id`, exact native typed value (including `Decimal` type and lexical scale where preservation is required), `source_temporal_kind`, null or genuinely present `source_timestamp_raw`, source timezone, `received_ts_utc`, ingestion scope+sequence; and selection identity carrying versioned requested subject/source/generation/MPID where applicable;
- **expected absences**: no projection for a missing R field, no native event-time when receipt-only, no invented reset as R187, no unearned composite quote, no M00 derived D result, no observation after selected receipt cutoff;
- exact positive projection row counts above and per-R scoped ordering; SQLite persisted and freshly reopened readback equals the original authorised typed observation and independently specified projection expected values;
- canonical deterministic serialisation (e.g. JSON or JSONL carrying `decimal` as canonical string plus `native_type='Decimal'`, UTC with `Z` plus type marker), manifest schema version, sorted/canonical ordering and SHA-256 for input oracle, expected output oracle and **actual M00-produced output**. Preserve Decimal versus int and source-time `null` unambiguously; do not rely on binary float or JSON numeric imprecision.

**Minimum positive counts (different fixture families and scopes must never be conflated):**

| Scenario | Native M00 observations | Expected public R projections | Critical provenance assertion |
|---|---:|---:|---|
| A1 atomic STK L1 | 1 | 4 | all four co-reference one native occurrence |
| A2 CALL L1 callbacks | 4 | 4 | all four have different native occurrence IDs |
| A3 PUT L1 callbacks | 4 | 4 | different contract/right, four IDs |
| A4 SMART STK depth | 4 | 20 | one per native mutation, five R roles |
| A5 legacy SMART CALL | 3 | 15 | isolated incompatible quote context |
| A6 SMART PUT | 2 | 10 | one-level-per-side only |
| B seven-event SMART book | 7 | 35 | separate date, IDs and source variants |
| C1 coherent SMART CALL | 3 | 15 | prices coherent with 1.20/1.40 L1 |
| C2 direct STK | 4 | 24 | six R roles, MPID≠source exchange |
| C3 direct CALL | 4 | 24 | six R roles, native-coded |
| **Totals for the ten listed positive scenarios** | **36** | **155** | **subject to documented field-specific mapping** |

These are expected **per-scenario** counts with deliberately complete fields; no stronger integrated assertion may be inferred merely from this total. For native control events separate from R projections, count admitted control observations **in addition**, never by inventing an R187 value. Preserve missingness as missingness; no zero-filled substitutions. When an expected row is not returned, demonstrate which M00 invariant failed; rectify in scope or report a precise blocker.

**Public seam proof:** Use actual `create_owner()` commands/reads, `RawObservationOccurrenceV1`, `RawSignalProjectionMappingV1`, `project_raw_value()` and `list_projected_raw_history()` with exact subject/source/version selectors. One query per R role as appropriate; verify `ProjectedRawValueV1` attributes and cursor completeness. Persist to SQLite via actual persistence port; close and **reopen** storage in a fresh owner and read using public interface. The independent expected oracle must be constructed from the signed-off tables, not by serialising M00 output and declaring it expected. A control-history seam, if required, must have a documented public schema, stable ordering, pagination/cutoff and subject/request/generation selection; private SQLite inspection alone is insufficient to prove public access.

**Output deliverables:** `synthetic_input_v*.jsonl` (or JSON), `expected_m00_output_v*.jsonl`, `actual_m00_output_v*.jsonl`, `output_schema_v*.json`, `manifest_v*.json` including all scenario IDs, source Git SHA, environment/backend, test/review status, individual SHA-256, mismatch/refusal summaries; reproducible test code or fixtures. Package the verified actual output plus independent oracle for handoff. If the implementation cannot pass some cases, **deliver the expected contract with explicit unverified/failed status**, not a counterfeit actual-output file or an unconditional completion statement.

## 4. Negative tests — M00 ownership, no downstream calculation mandate

The worker must cover at least these **M00-specific** propositions with representative, independent public-seam tests. Preserve existing still-valid assertions; fix invalid tests only when requirement-relative evidence warrants. Negative cases belong in isolated copies and cannot mutate approved positive input bytes.

| ID | Perturbation | Exact M00 expectation |
|---|---|---|
| N01 | Native `side=1` book element read as ASK or `side=0` as BID | M00 preserves exact native value; fails any test expecting inversion |
| N02 | `receipt_only`, source timestamp `None` | **Valid** M00 admission and receipt-based projection history |
| N03 | `receipt_only` with invented non-null source timestamp | Raw observation validation **rejects** |
| N04 | Query receipt-only row using a non-null `event_at_or_before_utc` | Row **excluded** by event-time selection; separately positive with `event_at_or_before_utc=None` |
| N05 | Same `(receipt,scope,sequence)` used for two distinct observations | Determine actual M00 monotonic contract (non-decreasing) and retain facts; do not falsely claim uniqueness; demonstrate that any required ambiguity marker/order cannot disappear silently |
| N06 | Remove operation, position, side, size or MPID from one callback | Other native facts persist; corresponding R role **absent** or control-quality status rejects; never manufacture missing R |
| N07 | Insert/update/delete and zero size | Preserve exact operations, positions and zero values; M00 does not itself infer book standing state or reassign positions |
| N08 | Separate native `error(317)` after populated book | Exact receipt/order/control identity and restart generation **discoverable**; no native R187=317; cannot hide reset from public consumer |
| N09 | `error(316)` / reconnect / gap / restart | Preserve discontinuity and scope/generation; don't silently assert stream continuity |
| N10 | Swap STK/CALL/PUT or SMART/direct selection | Public projection identity and selectors prevent silent subject/source co-selection |
| N11 | Replace one of four asynchronous quote callbacks with different contract | M00 retains original contracts; cannot export a falsely single native observation |
| N12 | Duplicate batch UTC on distinct callbacks | Native callback IDs stay distinct; no fake atomicity or source timestamp |
| N13 | Inject strictly post-cutoff raw receipt | Public receipt history excludes it; ordinary full readback remains possible |
| N14 | Missing initial depth snapshot / missing book field | Preserve seen records; no implied complete initial book or fabricated zero |
| N15 | Control event ID known but control not listable by subject/receipt | **Fails required discoverability**, even if known-ID read works; triggers bounded interface correction/authority adjudication |
| N16 | Input replay, same immutable occurrence ID with changed native payload | Identical replay idempotent where governed; conflicting replay rejected; previous occurrence retained |
| N17 | Option direct `marketMaker` is MPID when `isSmartDepth=False` | Preserve MPID and requested exchange distinctly; don't label MPID a venue without qualifier |
| N18 | Incomplete / missing `R001` receipt carrier | Projection absent rather than invent provider time; verify valid collector receipt carrier equals envelope time when used |

**Explicit exclusions:** M00 need not calculate an imbalance, concentration, banded depth, midpoint or microprice; nor implement a production skew threshold. Consumer refusal conditions may be documented as rationale, but M00 verification is admission, losslessness, projection, discoverability, ordering and persistence. No test may claim live-source availability from synthetic sample data.

## 5. Implementation and acceptance gates

**Gate 0 — Establish current truth:** Read entire current governing files and normative raw contracts; hash/check Git source, identify frozen baseline, exact current public read capabilities, SQLite version/runtime, existing tests, schema and source variants. Record which referenced assumptions are confirmed or stale. Preserve baseline and history.

**Gate 1 — Owner-authorised fixtures and oracle:** Materialise all ten scenarios as separately versioned synthetic fixtures with immutable input hashes and exact independently produced expected-output rows. Verify all 36/155 positive event/projection expectations as specification arithmetic, with tests checking each exact native value and identity, not only counts. Introduce separate control fixtures and documented absence cases.

**Gate 2 — Baseline M00 proof:** Use current public M00 owner and SQLite persistence; record actual positive/negative outcomes, public query results and fresh read-only reopen. Confirm or falsify core compatibility for exact native fields, temporal kinds, source identities and cutoff/pagination. Prove control history discoverability end-to-end or isolate first unmet invariant.

**Gate 3 — Bounded corrective work:** When a specific M00 defect is established, correct code and/or tests within the owner's now-explicit M00 update commissioning, respecting any more-specific governance approval. Do not automatically modify core for a bad mapping/fixture or alter provider-native values. If a suitable already admitted public control history exists, use it; if absent, specify and implement a narrow, versioned public discovery contract only under proper authority. Avoid unrelated redesign.

**Gate 4 — Deterministic output publication:** Produce actual M00-generated machine-readable output and compare against independent oracle, including absent/negative outputs; hash each, include Git commit, environment, backend and mapping versions, and verify reproducibility from clean checkout to fresh SQLite reopen. Deliver output schema and exact public replay/query instructions. Outputs may be reused independently regardless of whether live collector has been implemented.

**Gate 5 — Independent verification and handoff:** Apply current required independent semantic review, tests and commit/bundle checkpoint discipline to this newly commissioned M00 unit. Mark every gate `VERIFIED`, `FAILED`, `BLOCKED` or `NOT_ATTEMPTED`, with proof command/results and exact first unmet invariant. Preserve existing accepted evidence, never manufacture a sign-off. Distinguish `EXPECTED_SYNTHETIC_OUTPUT_AUTHORISED`, `ACTUAL_M00_OUTPUT_VERIFIED`, `SQLITE_READBACK_VERIFIED`, `POSTGRES_RUNTIME_DEFERRED`, `LIVE_IBKR_UNVERIFIED` explicitly.

**Completion criteria:** (i) independent oracle exists; (ii) all specified native events and controls have correct public M00 representation or a clearly documented blocked interface; (iii) all 36 positive native observations and 155 raw projections exactly match specification via **actual** public seam, unless governing authority changes the scope; (iv) all applicable negatives prove the M00 requirements; (v) real SQLite close/reopen/readback; (vi) deterministic portable output artifact and manifest; (vii) applicable independent review/admission; (viii) no improper claim of PostgreSQL/live equivalence. Failure of a mandatory item is **not** accepted completion.

## 6. Pinpoint source references — navigation, not substituted authority

**Anchor:** Git `17d7553cf3ad92700f849f696134de67b64b0dfa` from `NVDA_V2_D143_ACCEPTED_FULL_HISTORY_20261027(3).bundle`. Line locators apply to that exact revision and may move. The worker's latest bundle and governing text take priority after fresh inspection.

| Ref | Exact file/symbol | Reason to inspect |
|---|---|---|
| GOV-1 | `GUARDRAILS.md` entire; `AGENTS.md` entire; `tests/AGENTS.override.md` entire; active `EXEC_PLAN.md` entire | Repository authority, freeze, test and acceptance controls, SQLite signal-development evidence |
| RAW-1 | `src/nvda_desk/raw_signal_occurrence_truth/api.py:473–565` `RawObservationOccurrenceV1` | Exact native record, receipt and temporal schema; receipt-only must not carry source timestamp |
| RAW-2 | Same `:600–660` `RawSignalProjectionMappingV1`, `ProjectedRawValueV1` | Field paths, typed projection/value/lineage fields |
| RAW-3 | Same `:1753–1820` `project_raw_value`, `:1822–1890` `list_projected_raw_history` | Mapping picks values only from native record, public cutoff/pagination/sort |
| RAW-4 | Same `:1350–1435` admission/read implementation; `:897–905` persistence transaction protocol | Immutable identity and monotonic high-water; named-ID read vs general enumeration |
| SQL-1 | `src/nvda_desk/raw_signal_occurrence_truth/_sqlite.py` observation schema, `list_observations_received_between`, `append_observation`, `create_sqlite_persistence` | Genuine SQLite write/reopen/read public proof path |
| SQL-2 | `src/nvda_desk/raw_signal_occurrence_truth/_postgres.py` | Preserve compatibility; **no runtime PostgreSQL certification** in this task |
| TEST-1 | `tests/product/raw_signal/test_u03_observation_native_temporal.py` | Receipt-only/source clock and monotonic sequence regression |
| TEST-2 | `tests/product/raw_signal_sqlite/test_contract_native.py`, `test_sqlite_durability.py` | Raw fidelity, persisted typed/native readback and independent reopen |
| TEST-3 | `tests/product/market_measurement_d139/test_signal.py:28–32,64–103` | Example of explicit `R001` collector receipt native carrier; downstream test evidence, **not** M00 law |
| TEST-4 | `tests/product/market_measurement_d143/test_signal.py:27–31` | Existing six-role direct mapping witness; controlled semantics are not native admission |
| NORM-1 | `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md` §9; applicable accepted workbook raw field semantics | Exact native projection and timing meaning; M00 does not calculate derived outputs |
| IBKR-1 | https://www.interactivebrokers.com/docs/tws-api/doc/md/market-depth ; https://interactivebrokers.github.io/tws-api/market_depth.html | `updateMktDepthL2` native sides/operations, `marketMaker` and `isSmartDepth` meaning |
| IBKR-2 | https://interactivebrokers.github.io/tws-api/message_codes.html | `316`, `317` as distinct callback errors, not depth operations |
| IBKR-3 | https://interactivebrokers.github.io/tws-api/tick_data.html ; https://interactivebrokers.github.io/tws-api/tick_types.html | Level I tick fields; genuine atomic tick-by-tick vs independent option callbacks |

**Reference limitations:** Main Git checkpoint is a current accessible worker checkpoint, not demonstrated independent M00 frozen checkpoint; no deployed SQL, external broker session, permitted option-depth feeds or production control adapter was inspected by issuance of this brief. Reopen exact source and revalidate references before coding.

## 7. Worker reporting template

Provide a concise handover report showing: exact checkout/commit; governing revisions freshly inspected (full/partial); all ten input fixture identities and hashes; expected-output oracle hash; for each scenario actual-vs-expected row count, values, source types and absence tests; SQLite fresh readback; control-event discoverability and any new interface; changed implementation/tests with pinpoint diff and defect requirement; precise test commands/results; independent reviewer disposition; actual output bundle hash; PostgreSQL deferred status and any static risk; all remaining `UNKNOWN/BLOCKED` with evidence. Never claim a new accepted state just because a brief or fixture was generated.
