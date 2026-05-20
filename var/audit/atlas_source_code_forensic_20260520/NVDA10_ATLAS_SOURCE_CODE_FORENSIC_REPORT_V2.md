# NVDA10 Atlas Source-Code Implementation Forensic Report — V2

## Direct answer

By this report’s evidence rule, **1128 of 1,716 Atlas ideas are not included in active codebase source code**.

**588 of 1,716 Atlas ideas are included in active codebase source code**: 508 already existed in source code, and 80 were added or modified in source code.

## Headline counts

- `atlas_ideas_total`: `1716`
- `mapped_to_active_codebase_18_services`: `1716`
- `mapped_existing_in_source_code`: `508`
- `mapped_added_to_source_code`: `80`
- `mapped_tests_exist_but_source_code_missing_or_incomplete`: `0`
- `mapped_not_migrated`: `1128`
- `mapped_not_traceable`: `0`
- `included_in_active_codebase_source_code_total`: `588`
- `not_included_in_active_codebase_source_code_total`: `1128`

## Mutually exclusive classification meanings

- `mapped_existing_in_source_code` — Mapped to one of the 18 services; active-code source behaviour was found as existing code. This is included in the active codebase, but not counted as newly added source code.
- `mapped_added_to_source_code` — Mapped to one of the 18 services; accepted evidence links the Atlas idea to new or modified source-code behaviour.
- `mapped_tests_exist_but_source_code_missing_or_incomplete` — Mapped to one of the 18 services; accepted tests exist, but source-code behaviour was not proven or appears incomplete by this report’s evidence rule.
- `mapped_not_migrated` — Mapped to one of the 18 services; no accepted per-Atlas source-code behaviour proof and no accepted per-Atlas test proof were found.
- `mapped_not_traceable` — Atlas idea exists, but mapping or evidence is too weak to classify safely.

## Required report fields

- `atlas_id` — Stable Atlas idea identifier from the 1,716-record Atlas corpus.
- `atlas_idea_text` — Original Atlas idea text/excerpt used for row-level interpretation.
- `mapped_service` — One of the active codebase’s 18 services assigned by the Atlas Bridge.
- `bridge_mapping_status` — Whether this row has a usable Atlas Bridge mapping to one of the 18 services.
- `source_code_status` — Whether the active codebase contains source-code behaviour for the Atlas idea under this report’s evidence rule.
- `test_status` — Whether accepted per-Atlas tests exist, were added, were reused, or were not found.
- `classification` — The single mutually exclusive plain-English state for this Atlas idea.
- `evidence` — Paths, IDs, code/test ranges, proof commands, and receipts supporting the classification.
- `notes` — Plain-English caveats, especially where old audit wording could be confused with source-code implementation.

## Service breakdown

| mapped_service | existing in source code | added to source code | tests exist but source missing/incomplete | not migrated | not traceable | total |
|---|---:|---:|---:|---:|---:|---:|
| DMPV3 packet carriage | 68 | 5 | 0 | 0 | 0 | 73 |
| Downstream capital deployment authority | 2 | 0 | 0 | 0 | 0 | 2 |
| Dynamic coefficient and modifier authority | 0 | 0 | 0 | 193 | 0 | 193 |
| Exit and close architecture | 0 | 0 | 0 | 90 | 0 | 90 |
| External source interfaces and API ingress | 8 | 0 | 0 | 226 | 0 | 234 |
| Financial and event calendar architecture | 2 | 0 | 0 | 115 | 0 | 117 |
| Live position and inventory architecture | 2 | 17 | 0 | 19 | 0 | 38 |
| Opening architecture and placement readiness | 0 | 23 | 0 | 51 | 0 | 74 |
| Parallel risk lane | 0 | 0 | 0 | 57 | 0 | 57 |
| Persistence, ledgers, and receipts | 23 | 15 | 0 | 59 | 0 | 97 |
| Playbook library architecture | 75 | 20 | 0 | 0 | 0 | 95 |
| Prepared ingress and runtime context preparation | 51 | 0 | 0 | 0 | 0 | 51 |
| Raw capture and source temporal law | 108 | 0 | 0 | 0 | 0 | 108 |
| Raw signal families | 0 | 0 | 0 | 123 | 0 | 123 |
| Review and explanation layer | 1 | 0 | 0 | 142 | 0 | 143 |
| Serial desk-cognition spine | 139 | 0 | 0 | 0 | 0 | 139 |
| Testing, proof, and checkpoint surfaces | 19 | 0 | 0 | 53 | 0 | 72 |
| Vocabulary governance interface | 10 | 0 | 0 | 0 | 0 | 10 |

## Evidence basis

- Source tarball: `/mnt/data/fwd014-final-non310-clean-handoff.tar.gz`
- Repo path: `/mnt/data/nvda10_forensic/repo/MVD-A10_1704_V1`
- Branch: `work/fwd014-final-non310-sweep`
- HEAD: `1f417b39ddd75312f92670d7f0927813a5dffe8c`
- `git status --short`: ``
- Authority hierarchy and Atlas governance: `AGENTS.md:109-143`.
- Static structural inventory is navigation only and does not prove semantic implementation: `PLANS.md:56-75`.
- Atlas/Bridge/slice count evidence: `PLANS.md:651-657`; `PLANS.md:674-679`; `var/audit/atlas_surface_slices/atlas_surface_slice_manifest.json`.
- Final package repair sequence says 430 disputed audit rows were covered by target-surface repair ledgers/tests: `ROADMAP_LEDGER.md:4193-4214`. Those rows are classified as existing source-code behaviour with tests added/rerun unless direct new source-code repair evidence exists for the Atlas ID.

## Method rule that fixes the previous confusing headline

This report uses one classification axis only. A row cannot simultaneously be “not implemented as new source code” and “source-code satisfied” in the headline. Existing source-code behaviour and newly added source-code behaviour are separate categories, but both count as included in active codebase source code. Rows with neither accepted per-Atlas source-code proof nor accepted per-Atlas test proof are counted as not included in active codebase source code.

## Output files

- Full per-ID JSON: `NVDA10_ATLAS_SOURCE_CODE_FORENSIC_PER_ID_V2.json`
- Per-ID JSONL: `NVDA10_ATLAS_SOURCE_CODE_FORENSIC_PER_ID_V2.jsonl`
- Not-included subset JSON: `NVDA10_ATLAS_NOT_INCLUDED_IN_ACTIVE_CODEBASE_SOURCE_V2.json`
- Flat CSV index: `NVDA10_ATLAS_SOURCE_CODE_FORENSIC_PER_ID_V2.csv`
