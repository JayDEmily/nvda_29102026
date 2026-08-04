# Final Assurance Report

## 1. Scope and result

This report covers Phase 1 design-intent reconstruction only. The evidence boundary is exactly 61 original planning documents under `source_planning/` and 37 recovered successor briefs under `source_successor_briefs/`.

The reconstruction has produced:

- one hash-verified 98-source manifest;
- 25 chronological tranche records and 25 recorded tranche reviews;
- 83 stable proposition IDs;
- one chronological authority/supersession index;
- one 98-source reconciliation;
- ten capability-organised canonical vision documents;
- one explicit unresolved/external-authority register;
- mechanical validation tooling.

The current authority population is 81 active propositions, one proposition partially superseded only at a named boundary (`P-PROTO-002`) and one unresolved ownership proposition (`P-ARCH-010`).

## 2. What is established

### 2.1 Corpus identity and coverage

All 98 admitted source files are present, non-empty and match the SHA-256 values in `SOURCE_MANIFEST.tsv`. The 61/37 split is preserved. Every source ID and path appears exactly once in `reconstruction/03_SOURCE_RECONCILIATION.md`.

### 2.2 Chronological adjudication

Tranche A was reconstructed before successor propositions were admitted. Each Tranche B proposition was classified within the allowed successor classes. Later documents were not treated as automatically authoritative. Explicit replacement and partial-supersession chains are recorded in `reconstruction/01_CHRONOLOGICAL_AUTHORITY_AND_SUPERSESSION_INDEX.md` and the proposition records.

### 2.3 Canonical design coverage

All 83 proposition IDs are assigned to exactly one canonical capability document. Exact source lineage remains in `reconstruction/propositions/`. The canonical design preserves explicit lists, formulae and bounded examples where the corpus states them, including:

- the seven prepared normalised features;
- the eight mutable runtime surfaces;
- the 8/16/2 coefficient-scope split;
- the six serial cognitive stages;
- the three options-first playbooks;
- the five carry actions;
- the seven terminal-risk overlap classes;
- the source-time grammar fields;
- the bounded capital formula;
- the DMP v1 -> v2 -> bounded DMPV3 authority chain.

Negative requirements and non-goals remain explicit: no fabricated raw truth, no hidden serial state, no arbitrary mapping seams, no live broker authority, no booked-state theatre, no autonomous feedback loop, no scenario/observability subsystem by implication, and no live read-back from parallel-risk persistence.

### 2.4 Unresolved matters remain visible

The corpus does not resolve every implementation-grade detail. `reconstruction/04_UNRESOLVED_CONFLICTS_AND_EXTERNAL_REFERENCES.md` records one unresolved ownership decision, incomplete schemas/formulae/thresholds and all material classes of external authority. No missing value or owner was harmonised by invention.

## 3. What is not established

This work does **not** establish:

- that any current implementation conforms to the reconstructed vision;
- that any historical implementation or test claim in the sources was true;
- current architecture quality, module mapping or production readiness;
- the content of external workbooks, protocols, code, tests, fixtures, receipts, tags or excluded documents;
- profitability, alpha quality or live-trading safety;
- the unresolved details listed in the unresolved register.

No current code, Atlas/cohort material, tests or project documents outside the admitted 98-source corpus were used as semantic authority.

## 4. Review assurance

Every tranche has a recorded `PASS` review artefact. The review passes checked source coverage, lost negative requirements, over-compression, unsupported wording and supersession scope against the untouched tranche sources and prior accepted propositions.

However, the available environment did not provide a fresh independent model/subagent context. The same GPT-5.6 Thinking context performed extraction, procedural review and final consolidation. Therefore:

- **procedural same-context review is established**;
- **genuinely independent fresh-context acceptance is not established**.

This limitation prevents a claim that the independent-review condition in `AGENTS.md` has been fully satisfied. The semantic reconstruction is ready for external independent review; it is not represented as independently certified.

## 5. Mechanical validation

Final commands and exact outputs are preserved in `reconstruction/evidence/FINAL_VALIDATION.txt` after execution. The required commands are:

```bash
python tools/validate_source_corpus.py
python tools/validate_reconstruction.py
python -m compileall tools
git diff --exit-code -- source_planning source_successor_briefs SOURCE_MANIFEST.tsv
git status --short
```

Mechanical validators check identity, file/path coverage, proposition uniqueness, citation ranges, review presence and canonical-index coverage. They do not certify semantic losslessness.

## 6. Assurance verdict

**CONDITIONALLY ACCEPTED FOR PHASE-1 HANDOVER.**

The admitted corpus has been fully processed into a bounded, traceable and chronologically resolved design specification, subject to the explicit unresolved register. Mechanical completion and same-context semantic review are established. Independent fresh-context semantic acceptance remains outstanding and must be performed before claiming full compliance with the repository's independent-review terminal condition.
