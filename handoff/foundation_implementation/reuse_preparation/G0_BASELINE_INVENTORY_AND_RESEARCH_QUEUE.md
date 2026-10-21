# Gate 0 — verified inventory and bounded research queue

**Status:** Gate 0 documentary inventory prepared on the isolated research branch; **not** native source certification, implementation, programme acceptance or proof admission.

## 0.1 Verified checkpoint and authority scope

- Research branch incoming HEAD: `4467f3d3816eea574f102161080feb17bc415e08`, parent preparation `3951b89790a4ae9fc8947de3e20a75c71acfbf78`; underlying documentary review baseline `19c14ee461140649110d5d1cc4c1d5d7f40123be`.
- Source bundle: `NVDA_V2_126_SIGNAL_SOURCE_TEST_RESEARCH_PLAN_20261021.bundle`; advertised research ref checked against incoming HEAD, complete-history verification passed. The preparation history is recoverable; no claim is made about the current live implementation worker or halted pilot.
- Frozen governance SHA256: `GUARDRAILS.md` `585dc9b1a95719a7b60929b0d3ea64696fd6d52cd19b2b4a463c5bb9d34947b6`; `AGENTS.md` `d431f1a0c139912606211474880d5ecf595549507eface0f4e5ae4b3f52b468d`; root `EXEC_PLAN.md` `69a10020d8f7219d790cb5f7d0ce209574578b4f91b5ba44b3a205e07d1afbbf`.
- Governing repository sources consulted: full frozen guardrails, root agent instructions, applicable root plan/status/G6 authority, approved task-local plan, Annex B/C in `handoff/foundation_implementation/authority/FOUNDATION_IMPLEMENTATION_BRIEF_PROPOSED.md`, effective M01 catalogue, `HANDOFF.md`, `OPEN_GAPS.md` and the prior exact family map. The local root plan is a **historical snapshot**; current external worker progress is **UNKNOWN**.
- `tests/AGENTS.override.md` governs work under `tests/` only; this gate modifies no test paths and does not activate those instructions.

## 0.2 Inventory reconciliation

- Annex B: **126 distinct foundation D IDs**; Annex C: **83 distinct downstream D IDs**, across 26 proposed peers; exact union **209**, disjoint and equal to the 209-row effective M01 catalogue.
- Existing crosswalk: **126 distinct D IDs** exactly equal to Annex B and 126 family-map IDs; no missing/extra IDs. **35 preparation families**, **82 distinct raw R IDs**, **35 distinct D predecessor IDs**. **19** D rows declare no raw R input; **88** D rows declare no D predecessor. These are valid `NONE_DECLARED` relationships, not missing records.
- Per-row raw references and predecessor lists agree *exactly, including order*, between the crosswalk and family coverage map; predecessor identities all occur in Annex B. Both the D-dependency graph and consolidated family-prerequisite graph are acyclic in this snapshot.
- Legacy catalogue raw input membership differs at **D028, D117, D138 and D145**. Each crosswalk row explicitly declares `ACCEPTED_OVERLAY_SUPERSEDES_CATALOGUE`; preserve the effective corrected inputs, not the legacy catalogue fields. There are **21** additional list-order-only differences relative to the M01 catalogue, not evidence of additional input membership change. The D predecessor sets agree with the catalogue.
- Existing disposition: **118** `AUDITED_WITH_PRECISE_HOLDS`; **8** `DOCUMENTARY_REUSE_PACKET_PREPARED_NATIVE_HOLD`. Documentary preparation does not imply native-source mapping, admitted proof or runtime acceptance.

## Reproducible Gate 1 research queue — without new provider assumptions

- `G0_126_SIGNAL_COVERAGE_INDEX.csv`: one row per Annex B identity, retaining effective inputs, dependency/queue assignment and verbatim inherited holds/statuses with primary CSV row references. This is a coverage/index artefact, not a new authority copy.
- `G0_82_RAW_REFERENCE_RESEARCH_QUEUE.csv`: one row for each **distinct referenced R ID** with all directly dependent D IDs, affected preparation families and inherited source-hold text. Those are **82 R-reference investigations to deduplicate**, not a finding that 82 providers or 82 distinct API calls exist. Gate 1 must collapse shared provider/field/contract inquiries further using accepted source maps.
- Prior `OPEN_GAPS.md` remains the authority-aware **hold register**. Specific open groups include native time/calendar, FRED rate observations and vintages, options/OI, option trade-volume/cumulative baseline, multi-level SMART/direct order-book replay, dynamic basket profile, and mathematical model/surface conventions. They retain their exact existing dependants and receivers. No provider fact is claimed resolved by this inventory.
- Preparation families in dependency-closed topological order (order within independent families is not an implementation or programme priority):

| Family | D IDs | Cross-family prerequisites |
| --- | ---: | --- |
| F01 | 7 | NONE |
| F02 | 4 | NONE |
| F03 | 2 | F02 |
| F04 | 2 | NONE |
| F05 | 9 | NONE |
| F06 | 4 | NONE |
| F07 | 5 | NONE |
| F08 | 3 | NONE |
| F09 | 3 | NONE |
| F10 | 3 | NONE |
| F11 | 4 | NONE |
| F12 | 5 | NONE |
| F13 | 4 | NONE |
| F14 | 2 | F01 |
| F15 | 4 | NONE |
| F16 | 5 | NONE |
| F17 | 2 | F16 |
| F18 | 5 | F16;F17 |
| F19 | 1 | NONE |
| F20 | 2 | F01 |
| F21 | 3 | NONE |
| F22 | 4 | NONE |
| F23 | 2 | NONE |
| F24 | 7 | F20 |
| F25 | 4 | F24 |
| F26 | 2 | F08;F24 |
| F27 | 2 | F21;F22 |
| F28 | 3 | F20;F22;F24 |
| F29 | 5 | NONE |
| F30 | 1 | NONE |
| F31 | 3 | F03;F20;F21 |
| F32 | 1 | F22 |
| F33 | 7 | F02 |
| F34 | 5 | NONE |
| F35 | 1 | NONE |

## Exit boundary

**Gate 0 inventory reconciliation:** exact identity/coverage counts, corrected-input overlays, dependency closure and a deduplicated R-reference research queue established. **Gate 1 not started.** Source research, fixture engineering, live-authority updates, proof control and D042/D043/D047 pilot execution remain outside this gate. Existing external worker/pilot state remains UNKNOWN; no shared implementation branch is touched.
