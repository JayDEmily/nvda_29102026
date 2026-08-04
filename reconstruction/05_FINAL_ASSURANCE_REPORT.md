# Repair Status and Assurance Report

## 1. Verdict

**REPAIRED_PENDING_INDEPENDENT_REVIEW**

The externally audited repository returned `FAIL_REPAIRABLE`. Repair changes for D-01 through D-05 have been implemented in the existing full-history branch. D-06 has been corrected at the evidence level by withdrawing all same-context acceptance claims and marking independent review truthfully. The repaired result has not yet received a fresh-context independent verdict, so losslessness and terminal acceptance are not claimed.

## 2. Evidence boundary and integrity

The semantic evidence boundary remains exactly 61 original planning documents under `source_planning/` and 37 recovered successor briefs under `source_successor_briefs/`. `SOURCE_MANIFEST.tsv` remains unchanged. The original archive SHA-256 is `ac6af01badc5cd2dcc7ce770f7b50fd39d9c1bef026842d5fc545b5a6e103679`.

The independent audit established that the original and executed 98-source trees were byte-identical and that original HEAD `e908d3b072e4b1812e7fd2a1ce56563a1e4c6900` remained an ancestor. The repair has not changed the admitted sources or manifest.

## 3. Repairs implemented

| Defect | Repair surface | Implemented change | Independent verification |
|---|---|---|---|
| D-01 | A08 / A030 | Restored the frozen Gate-102 specimen identities, coverage values, states and outcomes, including `75.0`, `116.0`, `same_session_event_window`, `balanced_options_state` and `30.25` | Pending |
| D-02 | A11 / A044 | Restored the ordered modifier-to-final-risk transition: `20.625` followed by `13.4062` | Pending |
| D-03 | A12 / A046 and A050 | Restored the threshold-edge and prepared/raw outcomes: `0.95`, `destabilising`, `19.6625`, event-imminent/no-playbook/derisk and `0.0` | Pending |
| D-04 | B03 / B029, B030 and B022 | Replaced unsupported unconditional retirement with the admitted conditional branch law; `P-RES-001` is now unresolved | Pending |
| D-05 | All 83 propositions | Added `reconstruction/06_CANONICAL_PROPOSITION_FIELD_REGISTER.md` with every field required by `AGENTS.md:L119-L134`; extended mechanical validation to require complete coverage | Semantic verification pending |
| D-06 | All tranche reviews and assurance surfaces | Removed circular same-context acceptance status, preserved those notes only as non-independent observations and recorded fresh-context review as outstanding | Not independently resolved |

The exact external findings remain preserved in `reconstruction/evidence/INDEPENDENT_LOSSLESSNESS_AUDIT_20260804.md`.

## 4. Current reconstructed state

The repository contains:

- 98 immutable admitted sources and one hash manifest;
- 25 proposition records covering 83 stable proposition IDs;
- 83 complete proposition-field entries;
- one chronological authority and supersession index;
- one complete source reconciliation;
- ten capability-organised canonical design documents;
- one unresolved/external-authority register;
- 25 review-status records that no longer claim independent acceptance;
- mechanical validation tooling.

The current authority population is 80 active propositions, one proposition partially superseded only at the expressly admitted DMPV3 boundary (`P-PROTO-002`) and two unresolved propositions (`P-ARCH-010`, `P-RES-001`).

## 5. What the repair does not establish

The repair does not establish:

- that every proposition is now lossless;
- that no additional source-specific omission exists in the remaining corpus;
- that the decomposed mandatory fields are semantically correct merely because they are populated;
- that any current implementation conforms to the reconstruction;
- that historical implementation, test, receipt or Git claims inside the sources were true;
- the content of external workbooks, protocols, code, tests, reports or absent Gates 151–156;
- production readiness, trading safety, profitability or live broker authority.

Mechanical validation cannot supply any of those conclusions.

## 6. Validation

The final repair validation commands are:

```bash
python tools/validate_source_corpus.py
python tools/validate_reconstruction.py
python -m compileall tools
git diff --exit-code -- source_planning source_successor_briefs SOURCE_MANIFEST.tsv
git diff --check
```

Exact final output is preserved in `reconstruction/evidence/REPAIR_FINAL_VALIDATION_20260804.txt`. These commands validate identity, presence, coverage, citation ranges, links, review-status shape and Python syntax only.

## 7. Required terminal gate

A fresh worker must independently reread the admitted sources and audit the repaired reconstruction, with particular attention to A08, A11, A12, B03 and the 83-entry field register. The acceptable terminal verdict remains `PASS`, `FAIL_REPAIRABLE` or `HARD_BLOCK`, supported by exact source and reconstruction lines.

Until that review returns `PASS`, this repository is a repaired candidate, not a certified lossless reconstruction.
