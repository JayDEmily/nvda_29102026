# F01 — temporal quality/session/vintage: E1.1 authority and source extraction

**State:** `E1.1_SOURCE_EXTRACTED_ONLY`, not a completed F01 audit. No E1.2–E1.5 numerical/fixture/native-source challenge or independent reviewer admission is claimed.

**Source base:** accepted `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md:86–99` K01; original effective 209-row catalogue; Annex-B membership; M01 `_stage1.py:1163–1330`, dispatcher at `3713–3770`; M01 public tests cited below. Target M02 typed seam is `src/nvda_desk/market_measurement_truth/api.py:188–365` (current bounded Decimal occurrence contract).

| ID | Effective raw R | Predecessor | M01 exact branch (`_stage1.py`) | M01 public proof locator (`tests/product/derived_signal/`) | Initial reuse disposition | Authority-to-legacy distinction |
|---|---|---|---|---|---|---|
| D001 | `R002;R003` | `NONE_DECLARED` | `1199–1218` | `test_m01_f4_temporal_public.py:150–190` | **REUSE_AS_SPEC** | UTC normalisation of a true instant; legacy optional timezone fallback is not accepted native source certification. |
| D002 | `R001;R002` | `D001` | `1219–1236` | `test_m01_f4_temporal_public.py:153–182` | **REUSE_AS_SPEC** | Knowledge-cutoff age with explicit source_event/collector_receipt basis; negative age and date-only refusal established in calculation brief. |
| D003 | `R004` | `D001` | `1237–1247` | `test_m01_f4_temporal_public.py:150–195` | **REUSE_AS_SPEC** | IANA exchange timezone conversion of D001. Native/exchange timezone binding and DST still require certified configuration. |
| D004 | `R023;R024` | `D003` | `1248–1259` | `test_m01_f4_temporal_public.py:150–190` | **REEXPRESS** | Legacy optional HH:MM boundary subtraction does not establish full versioned exchange session calendar with holidays/overnight session identification. |
| D005 | `R023;R024` | `D003` | `1163–1190,1260–1264` | `test_m01_f4_temporal_public.py:150–190` | **REEXPRESS** | Legacy tuple of clock ranges and unique-match refusal is useful; complete admitted non-overlapping versioned phase schedule remains separate authority/configuration. |
| D009 | `R280;R281;R282` | `NONE_DECLARED` | `1265–1302` | `test_m01_f4_macro_vintage_public.py:14–113` | **REEXPRESS** | Legacy picks last visible co-referenced R280/R281/R282 revision; accepted K01 requires per-visible-vintage mutually exclusive status with revised category for earlier noninitial vintages. Existing two-vintage tests do not prove three-vintage revised case. |
| D010 | `R005;R023;R024` | `D003` | `1303–1330` | `test_m01_f4_temporal_public.py:198–242` | **REEXPRESS** | Legacy weekday/open/closed date tuple and liquid phase membership represent controlled synthetic case, not admitted native exchange-calendar truth; false when knowably closed. |

## Confirmed source construction and proof implications

1. M01 has a real K01 dispatch (`_stage1.py:3713–3770`) and seven explicit branches. The source is useful as a behavioural specification, not as a private M01 runtime dependency for M02. `api.py` reads typed R lineage publicly; M02 currently exposes Decimal `DerivedSignalOccurrenceV1.result` at `market_measurement_truth/api.py:220–246`, so UTC date/datetime, category, Boolean and structured age/vintage **cannot be claimed supported by that v1 occurrence type**. Their lawful future public result shapes and durable codecs require accepted family-specific design and new M02 proof.
2. Existing M01 controlled temporal public tests build actual M00 records (not pre-injected D001/D003), then construct requests: `test_m01_f4_temporal_public.py:16–175`. They demonstrate controlled timezone, 10-second source-age, 15-second receipt-age, date-only refusal, local trading date and phase, as well as missing-input and closed-calendar cases; these are **test inputs**, not certification of IBKR/FRED native data or production exchange calendars.
3. D009 source obtains complete co-referenced triples and refuses a partial newest tuple (`_stage1.py:1265–1282`, `test_m01_f4_macro_vintage_public.py:108–113`), a valuable reusable anti-omission precondition. It then sorts visible revisions and reports **only one latest row**, with no `revised` output (`_stage1.py:1283–1302`). This is a genuine **legacy-to-authority coverage gap**, not a proved production bug in accepted M02. Re-express the accepted per-vintage semantics rather than silently inheriting the legacy two-vintage fixture.
4. D004 M01 source applies one optional local HH:MM boundary (`_stage1.py:1248–1259`) and does not, by that branch alone, prove a complete session calendar. D005 `_phase_for_local` enforces exactly one matching configured interval but does not prove a versioned upstream exchange phase schedule (`_stage1.py:1163–1190`). D010 has explicit controlled weekdays/closed/open dates and liquid phases (`_stage1.py:1303–1330`), whose real source/profile validity must be separately admitted.
5. E1.2 requires **per-ID independently chosen witnesses**, e.g. source-event age based on two fully specified UTC instants and three-visible-vintage statuses, and typed output-shape decision. E1.3 requires actual history/co-reference/cutoff evidence and fault-precondition design; E1.4 requires source-calendar/projection/temporal-kind/SQLite holds; E1.5 requires direct manual source-sequence challenge. None is marked complete by this E1.1 source-only packet.

## Next required work

Proceed **F01 E1.2** with the accepted K01 equations and distinct per-ID outputs; do not invent native timezone/calendar/version authority or adapt the current Decimal facet by assumption. Preserve identity and history semantics. Resume E1.3–E1.5 only after correct output-shape/authority distinctions are recorded.

## E1.2 — authority-derived expected result and negative witnesses

**Evidence type:** independent reference calculations/controlled symbolic inputs; not executable product tests or provider-certified market readings. `E1.1` source table above provides per-ID M01 branches/tests and why reuse differs.

| ID | Required result shape | Controlled witness and refusal |
|---|---|---|
| D001 | UTC datetime | 2026-10-10T00:59:50+11:00 native true_instant -> 2026-10-09T13:59:50Z; date_only/receipt_only -> no D001 |
| D002 | typed pair {basis,age_seconds} (Decimal seconds) | At cutoff 2026-10-09T14:00:00Z, true event 13:59:50Z -> (source_event,10 s); receipt_only received 13:59:45Z -> (collector_receipt,15 s); date_only or negative age -> refusal |
| D003 | IANA-zone aware local datetime | D001 2026-10-09T13:59:50Z converted using Australia/Melbourne -> 2026-10-10T00:59:50+11:00; unknown zone -> refusal |
| D004 | exchange-local date | Under **controlled configured** overnight trading-date boundary 06:00 Melbourne on 2026-10-10 00:59:50 local -> configured trading date 2026-10-09; no assertion this is an actual exchange calendar |
| D005 | non-overlapping session-phase category | Under **controlled configured** schedule overnight [00:00,06:00), day [06:00,16:00), 00:59:50 -> overnight; no matching phase -> no phase; overlapping schedule not admissible |
| D009 | category per visible vintage plus realtime/cutoff metadata | Three complete co-referenced triples v1,v2,v3 visible before cutoff: v1 -> initial; v2 -> revised; v3 -> latest_known_at_cutoff; one visible -> initial; future-only v3 excluded |
| D010 | Boolean open AND liquid/RTH | With a **controlled** calendar declaring 2026-10-10 a valid open day and 00:59:50 Melbourne as liquid overnight phase -> true; identical time declared closed -> false; unknown calendar -> no asserted Boolean |

**Independent time conversion:** UTC time is native `2026-10-10 00:59:50+11:00` minus 11 hours = `2026-10-09 13:59:50Z`; `14:00:00Z − 13:59:50Z = 10 seconds`. A hypothetical received timestamp at `13:59:45Z` gives 15 seconds. These arithmetic witnesses are independent of M01 evaluator outputs. A calendar example is only valid under the declared *synthetic* configuration, not as a real exchange date claim.

## E1.3 — minimum applicable history/fixture preconditions

| ID | Required source/ordering/fault precondition |
|---|---|
| D001 | one eligible R002 source event; R003 supplies timezone when source is naive; no invented midnight |
| D002 | one eligible R002 and R001 observation, D001 required only for true_instant; cutoff and receipt timestamps must be known and unmodified |
| D003 | D001 predecessor plus R004/configured zone; timezone and DST policy versioned, no look-ahead |
| D004 | D003 and R023/R024 plus a complete versioned calendar/session rule, not merely clock offset; overnight boundary and holidays must be consistent |
| D005 | D003 and R023/R024 plus an ordered non-overlapping versioned phase schedule; half-open endpoint selection must be explicit |
| D009 | For three statuses require three native occurrence identities each with R280/R281/R282 (nine projected field values), released/received before cutoff; a newest partial triple must cause refusal, not implicit fallback |
| D010 | D003 and R005/R023/R024 plus coherent market-open and liquid-phase configuration; use knowable closed state instead of fabricating an open reading |

**M00 history and fault construction:** For D009, a pagination/partial-field refusal test must admit enough complete co-referenced native occurrences and allow cursor traversal to reach the intended incomplete/revised tuple before activating a fault. A source page that simply exhausts before the target witness would be an invalid fixture. No unapproved fixed page size or real calendar is asserted. For the other six, available current observations must be correctly filtered for subject, receipt cutoff, temporal kind, selection version and predecessor occurrence identity; multiple observations require no-look-ahead and defined eligible selection. An exact minimum beyond each declared dependency remains profile-specific.

## E1.4 — native and M02 holds by signal

| ID | Specific outstanding authority/source question and receiver | M02 architecture gap |
|---|---|---|
| D001 | IBKR/source researcher + M00: actual R002 native timestamp type/offset, temporal kind and R003 timezone origin/version | Accepted typed result/identity/history/SQLite proof not established in bounded v1 Decimal occurrence |
| D002 | M00 source/temporal owner: R001/R002 native kind and received_ts, precise temporal-kind policy and future receipt handling | Accepted typed result/identity/history/SQLite proof not established in bounded v1 Decimal occurrence |
| D003 | Calendar/source custodian: actual exchange IANA timezone source for each instrument and history/revision | Accepted typed result/identity/history/SQLite proof not established in bounded v1 Decimal occurrence |
| D004 | Calendar authority: R023/R024 exchange session identity, calendar holidays, overnight date attribution, early close/version | Accepted typed result/identity/history/SQLite proof not established in bounded v1 Decimal occurrence |
| D005 | Calendar authority: official phases, auction/early close/session sequence and versioned exchange-local effective dates | Accepted typed result/identity/history/SQLite proof not established in bounded v1 Decimal occurrence |
| D009 | FRED/native macro researcher + M00: R280/R281/R282 series publication/realtime vintage identity, revision order, timestamp and native missing fields | Accepted typed result/identity/history/SQLite proof not established in bounded v1 Decimal occurrence |
| D010 | Calendar owner + IBKR feed research: authoritative open/closed/RTH status, exchange holidays, exceptional sessions, market-state precedence | Accepted typed result/identity/history/SQLite proof not established in bounded v1 Decimal occurrence |

**Confirmed M02 interface distinction:** `src/nvda_desk/market_measurement_truth/api.py:220–246` currently types its original `DerivedSignalOccurrenceV1.result` as `Decimal`. F01 needs datetime, date, category, Boolean or structured outputs; any additive typed facet/contract must be independently authorised and reviewed before code. This preparation branch does **not** specify an implementation design or approve a generic union.

## E1.5 — direct manual challenge and disposition

1. **Numeric check independent of helper:** instant with +11:00 offset converts to UTC previous day, and selected cutoff gives exactly +10 seconds, while 13:59:45 receipt gives +15 seconds; negative age would refuse under K01. This does not depend on the M01 `public_temporal` helper or call the M01 evaluator.
2. **Three-vintage challenge independent of helper:** explicitly name v1/v2/v3 and all three complete R-field triples; at cutoff v3 latest, v2 revised, v1 initial. M01 two-vintage public fixture proves latest and initial, but not the authority-required intermediate revised result. Never label old M01 behaviour full authority compliance.
3. **Boundary challenge:** overnight configured trading date differs from the civil date; wrong time-zone offset or a 06:00 exact boundary must follow the *admitted* session/calendar policy. Synthetic Saturday-open case proves conditional Boolean algebra, not native exchange operation.
4. **Refusal/cursor challenge:** malformed latest vintage co-reference must refuse instead of choosing an older revision; missing/ambiguous calendar, future receipt and wrong subject/version also cannot be silently accepted. D009 must exercise each distinct status without hidden helper preclassification.

**E1.5 author assessment:** Each of D001/D002/D003/D004/D005/D009/D010 is `AUDITED_WITH_PRECISE_HOLDS`: its K01 authority, M01 source/test relevance, typed output shape, one independently reasoned controlled result, material refusal/fixture preconditions, reuse disposition and exact outstanding receiver are documented. This does **not** mean mathematical/calendar/source-certification or M02 implementation/test/proof acceptance. D009 is specifically `REEXPRESS` due to observed latest-only legacy implementation. Author challenge is not independent review. All unaffected 118-row census statuses remain unchanged; after these seven, 15 detailed rows and 111 census-only rows should remain.

**Baseline:** source snapshot `19c14ee` descendant, family E0.2 map commit `f120843`, E1.1 commit `a07edeb`. Only documentary files are touched.
