# Gate 02 — Existing Implementation Admission Handoff Adoption

## Contract identity

- **Gate ID:** `G02`
- **Contract revision:** `G02-R1`
- **Label:** Existing Implementation Admission Handoff Adoption
- **Lifecycle state:** `DEFINED`

## Objective

Reconcile the already-produced Implementation Admission terminal state and establish one exact BICP as the macro Project's authorised downstream payload without rerunning the completed specialist admission work.

## Entry criteria

- G01 is `ACCEPTED`.
- exact Implementation Admission repository/package identity remains available;
- exact IA-24/BICP Candidate 005 bytes and independent review evidence remain mechanically verifiable;
- Programme Owner is presented with the terminal-state provenance caveat and can make the required acceptance/adoption decision.

## Scope

- verify the exact supplied IA repository and accepted-candidate byte identities;
- reconcile the fact that current repository `main` points at IA-24 while IA-24 files retain terminal-gate-pending wording;
- identify the exact BICP payload proposed for adoption;
- record the Programme Owner disposition;
- if accepted, establish the exact BICP as authorised downstream input for G03/G04.

## Non-scope

- rerunning IA-01 through IA-24;
- changing BICP semantics;
- writing or changing product tests/code;
- resolving BICP Remaining Unknowns;
- accepting CODE-001 methodology;
- architecture allocation/promotion beyond what is already contained in the BICP evidence.

## Dependencies

- accepted G01;
- Implementation Admission repository commit `f64cf4c3f04e8e02ea368defb6d89d0f3ed0df7b`;
- exact Candidate 005 and IA-23R-05 review evidence.

## Authority references

- Project `PROJECT_OBJECTIVE.md` and `GUARDRAILS.md`;
- accepted G01 delivery architecture;
- Implementation Admission source authority at the exact bound repository identity;
- explicit current Programme Owner/user acceptance for macro adoption.

## Leaf set / decomposition status

- `G02-L01` — mechanically verify IA repository/BICP/review identities and terminal-state provenance.
- `G02-L02` — bounded owner closeout: present exact payload + caveat and obtain `ACCEPT | REJECT | BLOCKED`.
- `G02-L03` — if accepted, record adopted payload identity, authority effect and downstream binding; otherwise preserve blocker/rejection.

## Gate-level evidence

- exact Git/package identities;
- `admission/BICP_ACCEPTED.md`;
- `admission/IA_CLOSEOUT.md`;
- `admission/packet/BICP_CANDIDATE_005.*`;
- accepted independent review evidence for IA-23R-05;
- Programme Owner disposition.

## Known unknowns / blockers

- the IA-24 files contain terminal-gate-pending wording while supplied `main` points at the IA-24 closeout commit. G02 exists specifically to resolve the macro Project's reliance state without rewriting that history.

## Specialist methodology/profile requirements

Implementation Admission source is evidence/input to this adoption Gate. The Gate does not rerun the specialist method.

## Frontier references

`F-G01-001` — resolve exact macro acceptance status of the existing IA-24/BICP handoff.

## Result / handoff object

If accepted: an exact Project-level adoption record naming one BICP payload by digest and the exact architecture baseline/acceptance lineage on which successor work may rely.

## Downstream consumer

- G03 for CODE-001 methodology qualification context;
- G04 for eventual exact BICP input after G03 has accepted a CODE-001 methodology generation.

## Authority effect

`AUTHORISED_DOWNSTREAM_INPUT` limited to the exact adopted BICP and its declared bound architecture/authority lineage.

It does not authorise product implementation by itself.

## Execution binding set

To be frozen before `READY` from:

- accepted G01 identity;
- IA package/repository commit/tree;
- Candidate 005 exact digests;
- IA-23R-05 review/verdict-lock identities;
- exact owner disposition surface.

## Handoff identity structure

- payload: BICP Candidate 005 exact JSON/Markdown byte identities plus its exact admitted baseline/lineage;
- wrapper/process: IA repository/archive identity recorded separately.

## Risk/decomposition disposition

`ADEQUATELY_BOUNDED` — adoption/reconciliation only; no product mutation.

## Composition requirement

`NONE` — the Gate establishes a single exact adopted handoff and authority effect.

## Exit criteria

1. exact candidate/review/repository identities are mechanically verified;
2. terminal-state provenance caveat is explicit;
3. Programme Owner disposition is explicit;
4. on acceptance, exact payload and downstream authority effect are recorded without semantic mutation;
5. no implementation work has occurred under G02.
