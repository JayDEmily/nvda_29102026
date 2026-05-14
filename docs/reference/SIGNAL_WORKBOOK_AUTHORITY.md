# Signal Workbook Authority

## Canonical governed workbook

- canonical live reference ledger: `data/reference/signal_workbooks/2026-03-25_NVDA_SIGNAL_WORKBOOK_v3_bounds_handoff_copy.xlsx`
- historical predecessor retained as archive evidence only: `docs/planning/2026-03-25_NVDA_SIGNAL_WORKBOOK_v3.xlsx`

## Role

The canonical workbook is a **governed live reference ledger**. It is not normative prose, not direct runtime authority, not a disposable planning attachment, and not a substitute for typed config/contracts.

It exists to preserve:
- signal/coefficient provenance;
- bounds research and handoff detail;
- workbook-to-authority promotion lineage;
- a bounded source for future coefficient and parallel-risk-lane planning.

## Discoverability contract

Future coefficient or parallel-risk-lane work must consult this workbook when a gate, config surface, or receipt claims workbook-derived provenance. The companion discoverability surfaces are:
- `docs/01_NORMATIVE.md`;
- `config/README.md`;
- `docs/vocabulary/2026-03-25_CANONICAL_DESK_COGNITION_VOCABULARY.json`;
- the current active planning pack when workbook-derived work is in scope.

## Promotion lineage

Workbook content never becomes runtime truth by direct read. The lawful lineage is:

1. workbook cell or workbook concept in `data/reference/signal_workbooks/2026-03-25_NVDA_SIGNAL_WORKBOOK_v3_bounds_handoff_copy.xlsx`;
2. typed promotion into config/contracts with explicit lineage, including `workbook_ref` or successor lineage fields;
3. runtime consumption from typed config/contracts only.

Direct runtime reads from the workbook are forbidden.

## Update classes and paired-update obligations

### Workbook-only maintenance
Allowed when the change is purely cosmetic or note clean-up and does not affect promoted authority, vocabulary, or risk-lane-relevant subsets.

### Structural workbook reorganisation
Requires paired updates to this reference doc, relevant planning receipts, and any affected `workbook_ref` lineage notes.

### Coefficient-bound or threshold changes
Require paired updates to typed config/contracts, promotion receipts, and relevant planning or implementation gates when the changed surface is already admitted into authority.

### New signal-family or lane-relevant family additions
Require paired updates to this reference doc and whichever planning pack owns the new family.

### Vocabulary-affecting changes
Require canonical vocabulary updates in the same branch.

## Risk-lane-relevant workbook subset

Immediately relevant to the future parallel risk lane:
- `Bounds_Method`;
- `Signal_Coeff_Handoff`;
- `Temporal_Bounds_Draft`;
- `Runtime_Surface_Drivers`;
- `Coeff_Universe_Index` rows/families for temporal thresholds, regime/macro stress, options-flow/translation, posture/permission, and bounded coefficient surfaces.

Useful background but not primary gate drivers:
- `Raw_Catalog`;
- `Derived_Beta_Leadership`;
- `Derived_Vol_Rates_FX`;
- `Derived_Execution_Options`;
- `Derived_Asia_Breadth`;
- `Repo_Stage_Summary`;
- `Repo_Python_Inventory`.

Out of scope by default for the current pack unless a later gate says otherwise:
- broader playbook-module and execution-shape material that does not directly define the future lane's bounded input or posture surface.


## Workbook temporal provenance

Workbook dates are reference-ledger provenance.
They are not same-moment live runtime capture by default.

An anchor row may blend fields with different source dates.
A workbook-derived specimen must preserve field-level provenance where dates differ.
A workbook-derived promotion must preserve field-level provenance where dates differ.
A workbook-derived specimen or promotion must not masquerade as same-moment live runtime capture.

The workbook remains a governed reference ledger.
It is not direct runtime authority and it is not the primary source temporal-law authority.

## Blueprint Alignment

This document is subordinate to `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md`.

- All structures, stages, and components MUST align to architecture surfaces in `docs/11`.
- All terms MUST be defined in `docs/vocabulary/vocabulary_registry.md`.
- No definitions in this document may contradict `docs/11`.
