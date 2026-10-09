# M01 F2b — BLOCKED on event-to-score identity authority

## Decision and scope

The F2a temporal-sign repair is preserved, but **F2b production work is BLOCKED**. The 2026-10-09 `EXEC_PLAN.md` and `M01_F2_CONSOLIDATED_WORKER_HANDOFF_20261009.md` explicitly require stopping at the first unestablished mandatory semantic relationship rather than creating an extractor or event join. Do not treat this as F2 acceptance, an instruction to start F3, or permission to skip D064/D065.

## Verified accepted semantics and typed capability

1. The exact normative catalogue row D064 declares **R289 only**, **no derived predecessor**, kernel K07 and parameter profile `P_SCORE`; D065 declares raw R284 and D062/D064, kernel K08 `P_RULE`. Neither row declares an event-ID join key.
2. Accepted brief §5 K07 defines a caller-supplied, *immutable ordered* feature schema with exact signal dependency/extractor/weight/transform; D064 concept requires event category/importance and historical market/NVDA sensitivity into a bounded score. K08 D065 selects the eligible event by its scheduled time and declared nearest/earlier tie law, then applies **that selected event's** D064 importance; §11 forbids look-ahead.
3. The typed M00 `ProjectedRawValueV1` exposes `observation_occurrence_id`, versioned projection mapping, subject, source/receipt time and optional `RawSelectionIdentityV1` key/value dimensions. A shared raw observation ID could prove same-native-record co-reference; the type does not guarantee that separate R284 and R289 observations from distinct updates share that ID, nor does it define a universal `event_id` field or update linkage.
4. M01 `ScoreFeatureV1.__post_init__` currently admits only Dxxx IDs; `_stage1.py` `_score` looks only at derived inputs, so raw-only D064 is **not implemented**. This is an implementation deficiency, **not proof** that a lawful raw-source `P_SCORE` feature is impossible. The existing public `_eval_k08` D065 incorrectly equates R284 raw occurrence ID with D064 derived occurrence ID; no cross-namespace equivalence exists.
5. No accepted schema or rule inspected identifies a mandatory versioned stable event association between independently updated R284 scheduled-event records and R289 importance/sensitivity observations. Arbitrarily requiring equal M00 observation IDs would wrongly exclude valid separately updated event records unless that same-native-record limitation is in fact accepted; arbitrarily adding `event_id` is also not admitted without an authoritative binding declaration. Choosing either would legislate new domain law.

## First unmet invariant and single programme decision required

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
