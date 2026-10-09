> **SUPERSEDED AS A WORKER STOP — 09-10-2026, programme-owner 14:13 clarification.**
> The earlier absence of verified provider-native event-ID source data is no longer an F2b blocker for **provider-independent** M01 calculation. Controlled versioned events through the actual admitted M00 projection are expressly authorised. The previous field-search evidence and historical blocker are preserved below as a record, **not** as active work authority. Real-provider field identity, stability and integration remain `UNVERIFIED`. Current F2b calculation evidence: `../proof/f2b_provider_independent_20261009/F2_PROVIDER_INDEPENDENT_PROOF.md`.

# M01 F2b — BLOCKED on event-to-score identity authority

## Decision and scope

The F2a temporal-sign repair is preserved, but **F2b production work is BLOCKED**. The 2026-10-09 `EXEC_PLAN.md` and `M01_F2_CONSOLIDATED_WORKER_HANDOFF_20261009.md` explicitly require stopping at the first unestablished mandatory semantic relationship rather than creating an extractor or event join. Do not treat this as F2 acceptance, an instruction to start F3, or permission to skip D064/D065.

## Programme-owner proposed identity clarification — 09-10-2026, 13:55 AEDT; source-verification outcome

**STATUS: PROPOSED DOMAIN RULE, NOT YET ADOPTABLE FOR PRODUCTION. F2b `BLOCKED` on the first required native-source invariant.** This section supersedes only the *historical uncertainty about the intended correlation rule* above; it does not change the previously documented implementation defects or established F2a proof.

**Proposed rule examined:** event identity is the complete `(source_provider, source_variant where applicable, provider-native stable event identifier)` tuple. Its projected canonical identity dimension would be `event_id`. Different R284/R289 M00 observation occurrence IDs may lawfully denote the same event; identity must not be inferred from UUID equality, name/category or time proximity, nor conflated between providers. Revisions must obey the already-accepted cutoff and precedence laws. The proposal is conditional on actual provider-native source evidence establishing the field and its stability.

**First unproved source invariant — exact missing fact:** There is **no established provider/variant-specific native `event_id` field path or provider-native identifier contract for R284 and R289 in the active repository**. The active Git-tracked `src/`, `config/`, `schemas/` and `tests/` contain no `RawSignalProjectionMappingV1` construction for either R284 or R289, no provider event samples/revisions for these two IDs, and no real R284/R289 `native_record` schema to inspect. The sole R284 test reference in `tests/product/derived_signal/test_m01_stage1_semantics.py` is a *synthetic* K01 kernel-value fixture, not a provider-native M00 record. Therefore the native field name/path and its stability across timestamp or importance updates are **UNKNOWN**, not disproved. There is also no evidence that M00's optional `RawObservationOccurrenceV1.native_identifier` is the provider's stable event identifier; that generic field cannot be reinterpreted by assumption.

**Representation capability (proved separately from native availability):** M00 `RawSignalProjectionMappingV1.selection_identity_field_paths` can map a declared native scalar path to a key named `event_id` (`src/nvda_desk/raw_signal_occurrence_truth/api.py`, lines 586–627). Its read projection checks the provider/variant, extracts exact native paths, rejects missing/non-scalar identity fields and retains mapping ID/version, source/receipt/revision metadata (`api.py`, lines 1756–1806). `ProjectedRawValueV1` exposes provider, variant, `revision_vintage_native`, ingestion sequence and optional selection identity (lines 637–667). Its existing public-projection tests passed (5/5, Python 3.13.5). This proves a possible carrier, **not** that a real provider supplies the mandated event ID or that its revisions are correctly comparable.

**Distinct downstream implementation gap, not silently resolved:** M01 `ScoreFeatureV1` admits only `Dxxx` feature IDs (`derived_signal_calculation_truth/api.py:273–288`) and `_score` reads only derived predecessors (`_stage1.py:772–796`), whereas D064 has only raw R289. Existing D065 also compares an R284 raw occurrence ID to a D064 derived occurrence ID (`_stage1.py:2312–2340`). Both still need proof-first repair **after** the first native-source invariant is established; no change is authorised by guessing an R289 extractor or event identity.

**Recommended single resolution requiring programme-owner/source authority:** Supply the *actual* provider-native R284 and R289 records for **the same event at two or more revisions**, plus a versioned source-mapping declaration naming (a) provider and variant, (b) the exact field/path containing the stable provider event identifier for each feed/record, (c) the R284 scheduled-time and R289 importance value paths and units, and (d) the existing authoritative revision/temporal precedence relevant to those records. This is a concrete source contract, not a request to change M00. If one or both records lack a stable identifier, an explicit source-authority decision (or separately authorised M00 public-surface change) is required before implementation. Once established, resume F2b with proof-first public-seam cases and the accepted `P_SCORE` feature schema; do not infer scoring weights, mappings or revision precedence.

**Evidence:** Exact tracked-source search results are frozen at `M01_F2B_EVENT_SOURCE_READBACK_20261009.txt`; focused tests observed 5 M00 projection, 133 Derived Signal product, and 1 original late-quote reviewer witness passing. No F2b semantic test or production code was changed.

**Evidence/readback commands:**

```sh
git grep -n -E 'R284|R289' HEAD -- src tests config schemas
git grep -n -E 'event_id|eventId|calendar_event|economic_event' HEAD -- src tests config schemas
git grep -n -E 'RawSignalProjectionMappingV1\(' HEAD -- src tests
/opt/pyvenv/bin/pytest -q tests/product/derived_signal/test_ds_t01_m00_projection.py
```

**Stop and delivery:** No F2b production/proof assertions built on a fabricated provider, no changes to M00 or accepted catalogue/brief, and no F3/F4/Stage 2. Preserve exact F2a commits/tests and previous reviewer evidence. Deliver one consolidated full-Git `BLOCKED` archive; the one independent F2 review remains pending valid F2b closure.

## Verified accepted semantics and typed capability

1. The exact normative catalogue row D064 declares **R289 only**, **no derived predecessor**, kernel K07 and parameter profile `P_SCORE`; D065 declares raw R284 and D062/D064, kernel K08 `P_RULE`. Neither row declares an event-ID join key.
2. Accepted brief §5 K07 defines a caller-supplied, *immutable ordered* feature schema with exact signal dependency/extractor/weight/transform; D064 concept requires event category/importance and historical market/NVDA sensitivity into a bounded score. K08 D065 selects the eligible event by its scheduled time and declared nearest/earlier tie law, then applies **that selected event's** D064 importance; §11 forbids look-ahead.
3. The typed M00 `ProjectedRawValueV1` exposes `observation_occurrence_id`, versioned projection mapping, subject, source/receipt time and optional `RawSelectionIdentityV1` key/value dimensions. A shared raw observation ID could prove same-native-record co-reference; the type does not guarantee that separate R284 and R289 observations from distinct updates share that ID, nor does it define a universal `event_id` field or update linkage.
4. M01 `ScoreFeatureV1.__post_init__` currently admits only Dxxx IDs; `_stage1.py` `_score` looks only at derived inputs, so raw-only D064 is **not implemented**. This is an implementation deficiency, **not proof** that a lawful raw-source `P_SCORE` feature is impossible. The existing public `_eval_k08` D065 incorrectly equates R284 raw occurrence ID with D064 derived occurrence ID; no cross-namespace equivalence exists.
5. No accepted schema or rule inspected identifies a mandatory versioned stable event association between independently updated R284 scheduled-event records and R289 importance/sensitivity observations. Arbitrarily requiring equal M00 observation IDs would wrongly exclude valid separately updated event records unless that same-native-record limitation is in fact accepted; arbitrarily adding `event_id` is also not admitted without an authoritative binding declaration. Choosing either would legislate new domain law.

## Historical unmet identity rule before 13:55 proposed clarification

**UNKNOWN:** The exact, authoritative event identity/correlation rule for attaching R289-derived D064 importance to an R284 scheduled event across separate event records or revisions, including which typed raw projection/selection identity supplies that stable identifier. Without this, even a valid generic raw-only K07 extractor cannot establish that D065 compares the *selected event's* score. Positive, competing-event, version/cutoff and lineage public-seam proofs would only encode a guessed join.

**ONE AUTHORITY QUESTION:** *What exact versioned event-identity field and matching/revision rule is authoritative for associating R289 importance/sensitivity observations with the selected R284 scheduled event in D065, including when the two raw signals come from distinct observation occurrences?*

## Stop boundary

No F2b production modifications, no invented score extractor or join, no changed canonical catalogue/brief, no weakening of source/public schemas. Preserve F2a proof-before-production history and submit this full-Git BLOCKED evidence packet to the programme owner for that decision. Resume F2b only after the requisite law is established. One consolidated independent F2 review is still required after actual F2b closure.

## Programme-owner clarification — 09-10-2026, 13:41 AEDT

**Status: AUTHORISED CLARIFICATION.** This instruction is a programme-owner decision about *where event filtering is applied*, not a revision of the accepted D001–D209 catalogue, the existing M01 mathematical contracts, or the still-missing F2b event-correlation law.

**M01 calculation truth (unchanged):**

- **D064 — Event Importance Score:** preserve the accepted K07 importance-score calculation and its existing R289 input, `P_SCORE` parameter profile, immutable feature/transform/weight requirements, versioning, lineage and fail-closed missing-feature behaviour. Do **not** introduce the proposed event-level coefficient range `0.01–100` into M01.
- **D065 — Active Event-Window Flag:** calculate the actual `TRUE`/`FALSE` applicability under accepted K08 rules, including selected R284 event time, deterministic window/tie-break selection, correlation with that selected event's D064, importance threshold, version/temporal eligibility, lineage and fail-closed missing/ambiguous prerequisites. Do **not** make D065 permanently `TRUE` or `FALSE` or fabricate a flag where required truth is unavailable.

**Deferred to a future analysis/strategy module (record only; not authorised to implement in M01):**

| Configuration | Type | Default | Effect |
| --- | --- | --- | --- |
| `event_filter_enabled` | Boolean | `FALSE` | `FALSE`: downstream strategy decisions do not apply event-window filtering. `TRUE`: downstream strategy decisions apply the **actual D065 result**. |

Missing or unavailable D065 truth must never be silently converted into either Boolean value. This downstream switch controls *use* of a valid D065 result in strategy decisions; it does not alter the D064 or D065 calculation, eligibility or persistence semantics.

**F2b authority remains `BLOCKED`:** This clarification does **not** identify the stable versioned event identity, its admitted raw-projection carrier, or the exact update/revision matching rule needed to associate separate R284 scheduled-event and R289 importance/sensitivity observations. The **ONE AUTHORITY QUESTION** above remains open *unchanged*. No invented extractor or event join, no weakened accepted contract, no F2b production repair and no F3 progression are authorised.

**Routing:** retain the consolidated F2a→F2b worker sequence with one independent review only **after both** F2 units are established. At the present unresolved F2b prerequisite, invoke the governing immediate-`BLOCKED` stop; preserve the F2a checkpoint and return one full-Git handoff. This clarification grants neither F2b acceptance, F2 acceptance, Stage-1 acceptance nor authority to begin F3/F4/Stage 2. It supersedes only the earlier proposed `0.01–100` coefficient range and the suggestion to hardcode D065 to `TRUE`.
