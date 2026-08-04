# Independent Losslessness Audit — 2026-08-04

## Verdict

`FAIL_REPAIRABLE`

## Audit scope reported by the independent reviewer

- governing `AGENTS.md`;
- all 98 admitted source documents;
- 61 Tranche A documents, 2,015 lines;
- 37 Tranche B documents, 10,738 lines;
- reconstruction, proposition, review, assurance, validation and Git-history surfaces.

## Material findings

| Defect | Finding | Exact evidence reported |
|---|---|---|
| D-01 | The canonical raw-path reconstruction omitted frozen specimen identity, states and outcomes including `75.0`, `116.0`, `same_session_event_window`, `balanced_options_state` and `30.25`. | Source: `source_planning/2026-03-30_GATE102_CANONICAL_RAW_PATH_HARNESS.md:L25-L47`; reconstruction: `reconstruction/propositions/A08.md:L9-L12`; source marked reconciled at `reconstruction/03_SOURCE_RECONCILIATION.md:L36`. |
| D-02 | The ordered modifier-to-final-risk transition `20.625` followed by `13.4062` was omitted. | Source: `source_planning/2026-03-31_GATE124_EXTERNALISED_MUTABLE_SURFACE_AUTHORITY.md:L5-L9`; reconstruction: `reconstruction/propositions/A11.md:L18-L21`; reconciliation at `reconstruction/03_SOURCE_RECONCILIATION.md:L50`. |
| D-03 | Threshold-edge behaviour and prepared/raw outcomes were omitted: `gamma_pressure_score=0.95`, `destabilising`, `19.6625`, `event_imminent_window`, no active playbooks, `final_risk=derisk`, and deployable percentage `0.0`. | Source: `source_planning/2026-03-31_GATE126_BOUNDED_TEMPORAL_THRESHOLD_AUTHORITY.md:L22-L28`, reinforced by `source_planning/2026-03-31_GATE130_RUNTIME_EXPECTATION_REFRESH.md:L6-L13`; reconstruction: `reconstruction/propositions/A12.md:L8-L11`; reconciliation at `reconstruction/03_SOURCE_RECONCILIATION.md:L52`. |
| D-04 | Scenario and observability reservations were promoted from a conditional default with a bounded-admission exception into unconditional `explicit_retirement`; the branch-selection evidence was external and not admitted. | Conditional authority: B029 `L24-L34`, `L144-L186`; B030 `L136-L150`; B022 `L37-L49`. Unsupported result: `reconstruction/propositions/B03.md:L15-L21`, canonicalised at `reconstruction/vision/01_OPERATING_OBJECTIVE_AND_ADVISORY_BOUNDARIES.md:L46-L50`. |
| D-05 | The mandatory proposition model was incompletely implemented; required inputs, transformations, outputs, time/state, failure behaviour, dependencies, exclusions and unresolved fields were frequently absent. | Requirement: `AGENTS.md:L117-L136`; `PLANS.md:L32-L44`. Examples: `reconstruction/propositions/A04.md:L19-L22`, `A08.md:L9-L12`, `A11.md:L18-L21`, `A12.md:L8-L11`. |
| D-06 | Tranche reviews were circular evidence because extraction and review occurred in the same model context while every tranche was marked `PASS`; mechanical validators explicitly do not certify semantics. | Requirement: `AGENTS.md:L48-L59`, `L136`, `L170-L185`. Admission: `PLANS.md:L26-L30`; `reconstruction/00_METHOD_STATUS_AND_SOURCE_MANIFEST.md:L28-L32`; final report `L64-L87`. |

## Integrity checks reported as passing

- original archive SHA-256 matched the recorded baseline;
- original repository HEAD was an ancestor of executed HEAD;
- original and executed 98-source trees and manifest were byte-identical;
- all 37 successor files matched recorded Git blob objects;
- unreachable acceptance commits contained no alternate semantic reconstruction;
- both validators and `compileall` passed mechanically;
- final worktree was clean on `work/evolved-vision-reconstruction-v1`;
- no repository files were modified and no commit was created by the auditor.

## Required repair reported

1. Restore or explicitly disposition omitted bounded outcomes from A030, A044 and A046.
2. Reclassify `P-RES-001` as conditional/unresolved unless external branch-resolution evidence is formally admitted.
3. Populate the required canonical proposition fields.
4. Independently re-review at least A08, A11, A12 and B03 before replacing the final assurance report.

## Provenance limitation

The independent reviewer reported that the upstream donor checkpoint named as the origin of the 37 recovered blobs was not supplied. Provenance before the admitted original archive therefore remains unknown. The reviewer did not treat that as a hard block to reconstruction repair.
