# Method, Status and Source Manifest

## Scope

Phase 1 reconstructs design intent from exactly 98 immutable Markdown sources: 61 original planning documents under `source_planning/` and 37 recovered successor briefs under `source_successor_briefs/`. No implementation, tests, Atlas material, current architecture or external project artefact is semantic authority unless its content is expressly restated inside those 98 sources.

## Baseline identity

| Item | Result |
|---|---|
| Original archive SHA-256 | `ac6af01badc5cd2dcc7ce770f7b50fd39d9c1bef026842d5fc545b5a6e103679` |
| Initial branch | `main` |
| Initial HEAD | `e908d3b072e4b1812e7fd2a1ce56563a1e4c6900` |
| Initial worktree | Clean |
| Tranche A count | 61 |
| Tranche B count | 37 |
| Mechanical source validator | Passed at baseline and after every repair unit |
| Mechanical manifest | `SOURCE_MANIFEST.tsv` |

Exact initial commands and output remain in `reconstruction/evidence/INITIAL_BASELINE.txt`.

## Reconstruction method

The corpus was processed chronologically using the tranche schedule in `PLANS.md`. Material instructions were assigned stable proposition IDs, classified by authority state, reconciled against later amendments and consolidated by capability. Exact source lineage remains in `reconstruction/propositions/`; every mandatory proposition field is now populated in `reconstruction/06_CANONICAL_PROPOSITION_FIELD_REGISTER.md`.

Mechanical tooling checks source identity, proposition coverage, citations, links, review-status presence and immutable-source Git state. It does not decide semantics, losslessness or independent acceptance.

## Worker and review status

- Semantic extraction and repair worker: GPT-5.6 Thinking in one continuing execution context.
- Original tranche review passes: performed in that same context and therefore non-independent.
- Independent audit: performed externally in a fresh worker context and returned `FAIL_REPAIRABLE` on 2026-08-04.
- Current repaired-result review: not independently performed. The four directly repaired tranches are marked `PENDING_FRESH_CONTEXT_REVIEW`; all other tranche notes are marked `NOT_PERFORMED` for independent review.

The prior same-context acceptance claims are withdrawn. Same-context observations remain only as working notes and cannot satisfy `AGENTS.md:L136` or the independent-review terminal condition.

## Source hashes

`SOURCE_MANIFEST.tsv` remains the authoritative mechanical list of all 98 admitted paths and SHA-256 values. No file under `source_planning/`, `source_successor_briefs/` or the manifest was changed by the repair.

## Tranche processing status

The commit column records the original extraction commit. Status describes present assurance, not historical commit validity.

| Tranche | Sources | Present status | Original extraction commit |
|---|---:|---|---|
| Plan/baseline | 98 inventoried | Mechanical identity established | `d9bf965` |
| A01 | 4 | Same-context working notes only; independent review not performed | `042b57d` |
| A02 | 4 | Same-context working notes only; independent review not performed | `a6ec84b` |
| A03 | 4 | Same-context working notes only; independent review not performed | `62be887` |
| A04 | 4 | Same-context working notes only; independent review not performed | `6741dfb` |
| A05 | 4 | Same-context working notes only; independent review not performed | `f79ec4f` |
| A06 | 4 | Same-context working notes only; independent review not performed | `d36fe5e` |
| A07 | 4 | Same-context working notes only; independent review not performed | `f0b016d` |
| A08 | 4 | Repaired for D-01; independent repaired-result review pending | `e9993b4` |
| A09 | 4 | Same-context working notes only; independent review not performed | `46fb998` |
| A10 | 4 | Same-context working notes only; independent review not performed | `72037f7` |
| A11 | 4 | Repaired for D-02; independent repaired-result review pending | `c3e79f7` |
| A12 | 4 | Repaired for D-03; independent repaired-result review pending | `243ddd0` |
| A13 | 4 | Same-context working notes only; independent review not performed | `a95cb07` |
| A14 | 4 | Same-context working notes only; independent review not performed | `6f70388` |
| A15 | 5 | Same-context working notes only; independent review not performed | `f585e26` |
| B01 | 3 | Same-context working notes only; independent review not performed | `0718d95` |
| B02 | 5 | Same-context working notes only; independent review not performed | `6f32b7d` |
| B03 | 5 | Repaired for D-04; independent repaired-result review pending | `ac95830` |
| B04 | 3 | Same-context working notes only; independent review not performed | `96a7f27` |
| B05 | 3 | Same-context working notes only; no canonical proposition admitted | `eb96212` |
| B06 | 3 | Same-context working notes only; independent review not performed | `a8d7a14` |
| B07 | 3 | Same-context working notes only; independent review not performed | `80224f2` |
| B08 | 4 | Same-context working notes only; independent review not performed | `75d82f2` |
| B09 | 3 | Same-context working notes only; independent review not performed | `f9152fb` |
| B10 | 5 | Same-context working notes only; independent review not performed | `aa0318e` |
| Original final consolidation | 83 propositions / 10 capability documents | Prior acceptance withdrawn after independent `FAIL_REPAIRABLE` | `45f696d` |

## Repair sequence

| Unit | Scope | Commit | Current status |
|---|---|---|---|
| Audit admission | Record external findings and bounded repair plan | `efa108c` | Evidence recorded |
| R1 | Restore A030 bounded raw-path identities, values, states and outcomes | `60754a3` | Implemented; independent verification pending |
| R2 | Restore A044 ordered `20.625 -> 13.4062` transition | `5cddd10` | Implemented; independent verification pending |
| R3 | Restore A046/A050 threshold and prepared/raw outcomes | `606b51d` | Implemented; independent verification pending |
| R4 | Restore B029 conditional reservation law and unresolved branch state | `ac89556` | Implemented; independent verification pending |
| R5 | Populate all mandatory fields for all 83 propositions and validate coverage | `53fea03` | Implemented mechanically; semantic verification pending |
| R6 | Withdraw circular assurance, rerun validation and package | Current repair unit | Implemented and mechanically validated; independent verification pending |

## Current consolidation state

- Source reconciliation: 98/98.
- Stable proposition IDs: 83.
- Canonical capability documents: 10.
- Mandatory proposition-field entries: 83/83.
- Current authority population: 80 active, one partially superseded at a named boundary (`P-PROTO-002`) and two unresolved (`P-ARCH-010`, `P-RES-001`).
- Independent losslessness verdict on the repaired result: not yet available.
