# Atlas vocabulary governance candidate tranche plan — 2026-05-01

## Gate result
Candidate-specific planning package for `roadmap_vocabulary_governance_interface` only.

## Source lock
| Field | Value |
|---|---|
| Source ZIP | `/mnt/data/NVIDIA9_remotetest-main_gate6_candidate_selection_applied_2026-05-01.zip` |
| SHA256 | `34d323d6cb89be5910bf5400e217cc8c5b31b98ab21154729668f3c872c8e5cf` |
| Size bytes | `2884442` |
| Selected slice | `var/audit/atlas_surface_slices/slices/vocabulary_governance_interface.json` |
| Selected slice records | 10 |

## Candidate boundary
The selected candidate remains candidate-only. This plan does not open implementation, source code edits, pytest implementation edits, config edits, schema edits, vocabulary mutation, generated-slice edits, original Atlas/Bridge JSON edits, planning-compiler code edits, or executable leaves.

## Ten-record matrix summary
| Record | Symbol | Satisfaction | Proof/test action | Future route type |
|---|---|---|---|---|
| NIS-0101 | `nvda_desk.schemas.vocabulary` | `partially_satisfied` | `extend_existing` / `extend_existing_same_invariant` | `tests_first_conformance_route` |
| NIS-0102 | `VocabularyCategory` | `missing` | `admit_new` / `new_test_family_required` | `tests_first_conformance_route` |
| NIS-0103 | `RawDerivedTag` | `missing` | `admit_new` / `new_test_family_required` | `tests_first_conformance_route` |
| NIS-0104 | `VocabularyEntry` | `partially_satisfied` | `extend_existing` / `extend_existing_same_invariant` | `tests_first_conformance_route` |
| NIS-0105 | `VocabularyDocument` | `partially_satisfied` | `extend_existing` / `extend_existing_same_invariant` | `tests_first_conformance_route` |
| NIS-0106 | `VocabularyDocument._validate_uniqueness` | `already_satisfied` | `reuse_existing` / `no_test_change_required` | `no_change_evidence_only` |
| NIS-0107 | `VocabularyDocument.entry_index` | `missing` | `admit_new` / `new_test_family_required` | `tests_first_conformance_route` |
| NIS-0108 | `VocabularyDocument.from_json_text` | `transform_required` | `admit_new` / `new_test_family_required` | `documentation_or_control_surface_clarification` |
| NIS-0109 | `VocabularyDocument.from_json_path` | `transform_required` | `admit_new` / `new_test_family_required` | `documentation_or_control_surface_clarification` |
| NIS-0110 | `VocabularyDocument.to_json_text` | `transform_required` | `admit_new` / `new_test_family_required` | `documentation_or_control_surface_clarification` |

## Recommended next route
Recommended next route: `tests_first_conformance_route`.

Reason: the candidate has 6 tests-first records, 3 documentation/control-clarification records, and 1 evidence-only record. The next route should start by converting this planning package into a future tests-first conformance brief with a first gate that revalidates vocabulary, proof, and §5.18 owner/seam authority before touching any implementation surface.

## First future gate draft
Gate name: `VOCAB_GOVERNANCE_CONFORMANCE_INTAKE`.

Pass criteria:
- active repo source lock matches the future PM brief;
- selected slice still contains exactly 10 records;
- all records still map to `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md` §5.18;
- vocabulary gate either confirms reuse-existing posture or records lawful vocabulary admission before normative/control mutation;
- proof/test registry posture is read and explicitly classified;
- prohibited edit families remain at zero until the future brief opens exact leaves.

Fail criteria:
- selected slice, source lock, owner/seam binding, vocabulary posture, or proof/test posture diverges from the authorised future brief;
- any required in-scope source/test/config/schema surface is missing or cannot be read;
- any edit outside the future brief’s allowed paths would be required.

## Produced artefacts
- `var/audit/atlas_vocab_governance/2026-05-01_VOCAB_GOVERNANCE_SOURCE_AUTHORITY_RECEIPT.md`
- `var/audit/atlas_vocab_governance/2026-05-01_VOCAB_GOVERNANCE_SELECTED_SLICE_RECORD_MATRIX.json`
- `var/audit/atlas_vocab_governance/2026-05-01_VOCAB_GOVERNANCE_NATIVE_ARCHITECTURE_MAP.md`
- `var/audit/atlas_vocab_governance/2026-05-01_VOCAB_GOVERNANCE_NATIVE_SURFACE_INVENTORY.md`
- `var/audit/atlas_vocab_governance/2026-05-01_VOCAB_GOVERNANCE_PROOF_VOCABULARY_POSTURE.md`
- `var/audit/briefs/2026-05-01_ATLAS_VOCABULARY_GOVERNANCE_CANDIDATE_TRANCHE_PLAN.md`

## Stop
PM audit is required before any future route is launched.
