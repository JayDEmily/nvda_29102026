# DS-A01 — implementation-authority ingress evidence

## Scope and claim boundary

This record supports only DS-A01: exact accepted-authority rebinding and preparation of a bounded implementation-authority/BICP candidate. It does **not** claim DS-A02 independent-review PASS, architecture admission, durable numeric allocation, implementation acceptance, production implementation, package authority, or gate promotion.

Repository execution state before the DS-A01 candidate commit:

- work branch: `work/ds-a01-authority-ingress`;
- branch-admission commit: `91358aed8d2422071cddfae39bdacf1217eb0f6c`;
- tree: `d76bb82ce76d8a8555d3a1b59a85c57c5f5f364a`;
- PCM `check`: PASS;
- PCM `ready`: `DS-A01`.

## 1. Accepted authority identity and acceptance provenance

Current `.pcm/control/instantiation.json` records:

- status `approved`;
- accepted brief archive `.pcm/brief/accepted_brief.tar`;
- archive SHA-256 `8ea9bf69f6a651f19e84bd1401cb9f4e8c10f8e62603a3ff407f4418936e1731`;
- source commit/tree `23968fdfcc489cdc2ea14aa9dd1e1aea3b3d72ce` / `81ff4871ddb14f8c5feec2bf1a543ce290fba0be`;
- Programme Owner approval timestamp `2026-10-04T00:13:16.410823+00:00` and note `Programme Owner approved finalisation in the current project-manager thread on 2026-10-04.`.

Git inspection establishes that commit `09c1ac507f6ac0d9931c286e5b66680f1045af31` changed the instantiation record from `status: draft` / `approval: null` to `status: approved` with that Programme Owner approval, and that this approval commit is an ancestor of both the current worker HEAD and current `main`.

The native ingress binding therefore uses the stable external acceptance reference:

`PCM-INSTANTIATION-APPROVAL@09c1ac507f6ac0d9931c286e5b66680f1045af31`.

That token refers to the existing approval record; it does not create acceptance. Current higher authority additionally states in `.pcm/project/PROJECT_OBJECTIVE.md` that the project is to "Admit and realise the exact accepted Derived Signal Calculation Truth brief", and `.pcm/project/EXEC_PLAN.md` is finalised by the Programme Owner and assigns DS-A01 to prepare the implementation-admission candidate.

The Markdown member itself still contains its pre-acceptance status text, `FINAL REPAIRED CANDIDATE FOR INDEPENDENT REVIEW — NOT ACCEPTED IMPLEMENTATION AUTHORITY`. That text is not rewritten. The same brief expressly says that, **if accepted**, the exact accepted bytes enter Implementation Admission. The later Programme Owner instantiation approval is the external acceptance event contemplated by that text; the raw brief bytes remain unchanged.

## 2. Exact accepted bytes

Observed archive/member hashes:

```text
8ea9bf69f6a651f19e84bd1401cb9f4e8c10f8e62603a3ff407f4418936e1731  .pcm/brief/accepted_brief.tar
603b850802a418780109095e7ae69bcece449da79fb24140a6d50297605e927c  NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md
63bc1b776fc8fa8ba82eb3c9b16916f295c9ec3d480a5a068937c2f25146f5f5  NVDA_DERIVED_SIGNAL_CATALOGUE.csv
519ea9449297d564ae4a02afc1bf4e60e4471631c81a0842620f9fb60bb4f9ae  NVDA_80_STEP_ACADEMIC_EVIDENCE_AUDIT_WITH_SIGNALS_ADDENDUM_81_94.xlsx
```

The CSV hash exactly equals the digest incorporated normatively by the accepted Markdown and REQ-001. The workbook hash exactly equals the reference-workbook digest stated by the accepted Markdown; the workbook remains reference evidence only.

Native Implementation Authority Ingress binds the Markdown member hash `603b...927c`, not the outer archive hash, because accepted brief clause 2 explicitly defines the Markdown as the single exact ingress byte object and incorporates the companion CSV by digest.

## 3. Companion catalogue mechanical checks

Mechanical validation of the exact hash-bound CSV produced:

```text
CATALOGUE_VALIDATION: PASS
rows=209
ordered_unique_ids=D001..D209
raw_dependency_refs=328 distinct=115 all_within=R001..R323
derived_dependency_refs=276 unresolved=0
kernel_bindings=209 nonempty rows across 17 kernels
dependency_graph=acyclic
workbook_locator_missing=0
```

Reference-workbook identity checks on the exact archived workbook produced:

```text
WORKBOOK_REFERENCE_VALIDATION: PASS
Raw Signals IDs=R001..R323 exact ordered unique set
Derived Signals IDs=D001..D209 exact ordered unique set
```

These checks establish the catalogue identity/graph propositions above only. They do not make the workbook authoritative over the Markdown/CSV or establish the later runtime proof obligations.

## 4. Lawful bounded projection basis

The accepted brief and current architecture law establish one coherent projection without inventing a second semantic owner:

- create one category-`M` runtime semantic owner named `derived_signal_calculation_truth` because the accepted responsibility is one coherent deterministic calculation/transformation owner;
- modify existing `M00` only for the additive read-only typed raw-value/history projection expressly required by accepted brief clause 9 and REQ-003;
- preserve M00 Raw Signal Occurrence Truth ownership, persistence meaning and writer boundary;
- direct the new owner's runtime dependency to M00 through M00's declared public seam; do not create an M00-to-new-owner dependency;
- do not allocate a numeric create ID in this worker-produced authority record.

This is consistent with AK-OWN-001, AK-DEP-001, AK-SEAM-001 and the runtime-module extension sequence. No evidence inspected requires a second runtime semantic owner for the accepted Derived Signal responsibility.

## 5. Schema-valid ingress binding and mechanical candidate resolution

Binding artefact:

- path: `implementation/authority/DS_IMPLEMENTATION_AUTHORITY_BINDING.yaml`;
- SHA-256: `ae365e6ac6635ba9de2dc76136f47c18fc4f501c2f158ec4db9bf407ccde799e`;
- create target: category `M`, name `derived_signal_calculation_truth`, no caller-supplied object ID;
- modify target: existing object `M00`.

Validation command executed against the exact extracted Markdown member:

`PYTHONPATH=src python tools/validate_implementation_authority.py --binding implementation/authority/DS_IMPLEMENTATION_AUTHORITY_BINDING.yaml --brief /mnt/data/ds_a01_brief_recheck/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md`

Observed output:

```text
PASS: implementation authority brief_sha256=603b850802a418780109095e7ae69bcece449da79fb24140a6d50297605e927c
candidate_targets: create:derived_signal_calculation_truth->M01, modify:M00
```

The `M01` string above is **only** the validator's current deterministic, non-durable candidate resolution from current post-reset architecture state. It is not present in the create intent, is not a durable allocation, and is not selected or authorised by DS-A01. Durable numeric allocation remains for the later architecture-admission responsibility.

## 6. No durable architecture mutation by ingress validation

SHA-256 before and after the validation command:

```text
config/architecture/modules.yaml
before 412f3f4082d78a2425d8204a6544bff330311cdc1860e855fe78c47c3652b9e4
after  412f3f4082d78a2425d8204a6544bff330311cdc1860e855fe78c47c3652b9e4

config/architecture/implementation_allocations.yaml
before 29519e0a15ff3ee253e31101163a49f8e8bb671a4c5ed43edfb3d2c5f36005b8
after  29519e0a15ff3ee253e31101163a49f8e8bb671a4c5ed43edfb3d2c5f36005b8
```

The equality of each pair establishes that the mechanical ingress validation did not mutate those durable architecture surfaces.

## 7. Exact DS-A01 candidate identity and limits

- BICP candidate path: `handoff/authority/DS_BICP_CANDIDATE.md`;
- BICP candidate SHA-256 before this evidence record is committed: `e3a0be75da103d69d29ab3dee97429d343033b6c29e72c039e77e799e4869634`.

The candidate carries no numeric create identifier and records the unresolved matters required by the accepted brief. No production source, architecture registry/allocation state, package metadata, requirements, delegation, semantic authority or review law is changed by DS-A01 candidate preparation.

Independent semantic review of these exact candidate/evidence bytes is the separate DS-A02 responsibility. DS-A01 does not claim that review outcome.
