# Implementation Authority Ingress

## Status

Steady-state normative authority for the boundary between an externally accepted implementation-ready brief and architecture-governed implementation work.

This boundary does not own upstream semantic reconstruction and does not define a code-writing methodology.

## Normative propositions

- **AK-INGRESS-001 — Exact brief-byte binding.** Brief-derived implementation work is authorised only against the exact implementation-ready brief bytes identified by SHA-256. A changed byte sequence is a different implementation authority and cannot inherit the prior binding.
- **AK-INGRESS-002 — External acceptance, no self-authorisation.** The kernel records a non-empty reference to explicit current human/programme acceptance for implementation, but a schema-valid binding record cannot create or prove that acceptance. The acceptance must exist in higher authority before the binding is used.
- **AK-INGRESS-003 — Bounded architectural projection.** The ingress binding records only the exact brief identity, its external acceptance reference and the architectural object identities proposed for creation or modification. It does not copy, summarise, reconstruct or replace the brief's domain meaning.
- **AK-INGRESS-004 — Fail-closed semantic/architecture boundary.** If the accepted brief does not supply enough meaning to determine a lawful architectural projection, contains an unresolved semantic contradiction, or requires violation of kernel law, implementation stops and returns the defect to the authority owner/upstream process. The kernel does not invent the missing meaning.
- **AK-INGRESS-005 — Upstream-methodology opacity.** Implementation-authority ingress is methodology-agnostic. M10, G1-G7, PMB, worker/tester numbering, semantic-candidate numbering and other upstream process metadata are not required fields and do not create implementation authority.

## Two-sided admission boundary

The boundary answers two questions in order.

### 1. Is there implementation authority?

The worker must establish from current higher authority that one exact brief has been explicitly accepted for implementation. The mechanical binding then records:

- the SHA-256 of those exact raw brief bytes;
- a non-empty external acceptance reference;
- a bounded list of proposed architecture-object targets, each marked `create` or `modify`.

The repository validator can prove that supplied brief bytes match the recorded digest and that the record is structurally valid. It cannot prove that the human/programme actually accepted the brief or that the brief is semantically complete.

### 2. Can the accepted brief be projected lawfully?

Understanding the brief sufficiently to choose architecture-object targets is required implementation judgement. That judgement is bounded by the brief and by kernel law.

A `create` target must not already exist or reuse a retired identity. A `modify` target must already exist. The target list is an architectural projection only; it is not a second normative brief.

All architecture laws continue to apply. The binding cannot waive ownership, dependency, seam, lifecycle, proof, packaging or category rules.

## Brief handling

The kernel does not require the brief to be copied into the repository and does not store brief text in the binding document.

The raw brief is supplied to the validation operation. SHA-256 is computed over the bytes exactly as supplied; no newline, encoding, whitespace or document normalisation is performed before hashing.

The brief digest is therefore the immutable byte identity used for downstream traceability.

## Downstream traceability

The brief digest is the stable reference for brief-derived architectural projections and later implementation/proof evidence. Future implementation machinery may add narrower work-order, changed-path or proof records, but those records must point back to this exact digest and may not redefine the brief's meaning.

AKR-4 does not design that downstream implementation workflow.

## Failure disposition

Return upstream rather than implementing when any of the following is unresolved:

- no explicit current acceptance for implementation;
- supplied brief bytes do not match the recorded digest;
- a required responsibility cannot be allocated without inventing meaning;
- the proposed projection conflicts with a current architecture invariant;
- create/modify target state is structurally inconsistent with the current registry;
- the requested implementation requires a category, ownership rule or seam that the brief does not establish.

A rejected ingress is not a semantic rejection of the upstream methodology. It means only that architecture-governed implementation cannot lawfully begin from the supplied authority state.
