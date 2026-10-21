# Leaves P0.1, P0.2 and P1.1 — execution evidence and scope

**Checkpoint baseline:** `work/v2-g6-m01-m02-reuse-prep-20261020` at `58bbc7d7a7f7637ddab2cb74239913a3f2becc0e` / tree `c6005d1721decdb78ae82635c11b5af8fd59ef47` before documentary edits; verified clean. All work remains isolated from concurrent D014 worker.

| Leaf | Observed exit evidence | Status |
|---|---|---|
| P0.1 Baseline | `P0_1_PINNED_BASELINE.md` lists authority/source bytes and snapshot-only D011–D014 state; branch/HEAD/tree/status captured | VERIFIED documentary baseline |
| P0.2 Census | `M01_M02_REUSE_CROSSWALK.csv` has 126 unique Annex-B IDs with individual accepted name/authority, effective direct R and D dependencies, three separate readiness statuses; 83 unique Annex-C IDs across 26 receiving peers; union equals 209 original catalogue and Gate-2 traceability identities | VERIFIED identity census, not individual semantic audit |
| P1.1 Source/logic reuse | `FAMILY_P1_1_RATE_SPREADS.md`: D042/D043/D047 source branches and authored M01 tests inspected, 5 distinct raw R IDs, zero D predecessors, current M02 seam and reuse dispositions | VERIFIED bounded trace, not production/proof admission |

## Structural checks performed

- Exact Annex B membership count=126 (no duplicates); Annex C memberships=83 (no duplicates), peer rows=26; Annex intersection empty, union=209; catalogue/trace IDs match.
- Accepted Gate-2 classification `PROPOSED_M02_SEMANTIC_ELIGIBLE_CONDITIONAL` matches every Annex-B ID. All Annex-B declared direct D predecessors lie within Annex B (static graph membership only).
- Applied effective R references from Gate-3 `G3_3_Effective_Direct_R`, with accepted D028, D117, D138, D145 overlays superseding outdated raw catalogue declarations. Mere reordered IDs are normalized, not reinterpreted as a source change.
- Family exact K02/P_BASIC source IDs and empty derived dependencies compared to current catalogue and M01 source code; authored fixture is directly inspected but **not executed**.

## Explicit limits

P0.2 crosswalk entries beyond D042/D043/D047 provide **membership and existing authority pointers**, not comprehensive M01 source/test review; `NOT_AUDITED_P0_2` is intentional. The baseline did not prove native source provision, whole 126 closure, acceptability of the synthetic FRED fixture, or live D014 status. P1.2, P2.1 and all subsequent leaves remain pending. No full test suite, provider API calls, SQLite operations, production imports, new tests, guardrail/root-plan edits or main merge occurred.
