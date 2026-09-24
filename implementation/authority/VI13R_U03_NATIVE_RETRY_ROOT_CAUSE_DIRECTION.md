# Programme Owner Direction — U03 Native-Retry Root-Cause Closure

**Date:** 2026-09-24  
**Scope:** `VI-12R / IWO-U03` only  
**Trigger:** Reviewer 029 `R029-U03-F001` after the Reviewer 025–029 native-retry equality sequence

## Direction

The next Worker must not treat `R029-U03-F001` as another isolated `datetime` patch.

Reviewer 025 through Reviewer 029 have established a repeated class of implementation-coupled failures in the realised same-occurrence native retry comparator. Each predecessor witness has been closed, but the generic comparison strategy has continued to admit another representation collapse. The next unit of work is therefore the **root native-retry equality problem**, still entirely inside U03.

This direction changes execution strategy only. It does not alter IRB/BICP/IWO semantic meaning, does not narrow or broaden provider validity, does not authorise U04, and does not weaken any existing proof.

## Required Worker analysis before mutation

Using current authority and the realised public seam, the Worker must establish all of the following before choosing a repair:

1. the exact runtime value domain that is actually admitted by `native_record` under current authority and the realised U03 API;
2. which equality/representation rules are established for that domain by BC-005, BC-009 and BC-010 rather than by Python convenience;
3. whether that domain is finite/closed enough for one principled exact-content comparison strategy;
4. whether the existing snapshot/copy behaviour supplies sufficient representation evidence to compare independently reconstructed identical content without collapsing materially different provider-native content.

Do not infer a provider-value whitelist merely because common providers often use JSON-like scalars. Concrete provider mappings remain Unknown.

## Exactly two lawful outcomes

### A. Class-level repair is established

If current authority plus the realised admitted domain permits a principled closed comparison strategy, implement the smallest U03-only repair that establishes it.

The repair must:

- close `R029-U03-F001` and preserve closure of all Reviewer 025–028 findings;
- avoid relying on ordinary Python equality where it can erase fidelity-bearing representation;
- cover nested admitted values under the same rule rather than by one-off witness patches;
- preserve independently reconstructed genuinely identical native content as idempotent;
- reject materially different same-ID native content without mutating the first admitted record;
- preserve existing non-native observation-field equality semantics;
- preserve every existing accepted U01/U02/U03 public-semantic and owner-boundary guarantee;
- use compact strategy-level regression proof rather than growing an open-ended catalogue of one test per Python curiosity.

A candidate is **not eligible for Reviewer 030** merely because a `datetime` special case has been added. The Worker must record why the repaired comparator is closed over the established admitted domain and identify any deliberate fail-closed boundary.

### B. The domain cannot be closed from current authority

If `Mapping[str, object]`, current admission behaviour and the accepted semantic authority leave an open native-value universe for which exact independently reconstructed content cannot be determined without inventing provider validity or representation law, stop as:

`BLOCKED — U03 NATIVE VALUE DOMAIN / EXACT-CONTENT AUTHORITY GAP`

In that case:

- do not add another per-type patch;
- do not narrow `native_record` or reject an admitted value family by implementation convenience;
- do not route a superficially repaired candidate to Reviewer 030;
- identify the minimum Programme Owner authority decision needed to make the domain/equality rule closed and implementable.

## Reviewer 030 routing rule

Reviewer 030 is created only after Outcome A. Its review target is the **class-level closure claim**, not another unbounded search for unrelated Python equality curiosities. A new failure must either:

- demonstrate that an established admitted-domain category violates the claimed strategy; or
- demonstrate that the Worker's claimed domain closure is false under current authority/API.

If the domain itself remains unclosed, the Worker must have returned Outcome B before review.

## Unchanged boundaries

- U04 and later work remain prohibited.
- No IRB/BICP/IWO meaning is changed.
- No provider mapping, duplicate/retransmission equivalence, persistence/replay behaviour or downstream capability is invented.
- All existing tests remain valid and may not be weakened for green.
