# Implementation Authority Ingress

## Status

Steady-state normative authority for the boundary between an externally accepted implementation-ready brief and architecture-governed implementation work.

This boundary does not own upstream semantic reconstruction and does not define a code-writing methodology.

## Normative propositions

- **AK-INGRESS-001 — Exact brief-byte binding.** Brief-derived implementation work is authorised only against the exact implementation-ready brief bytes identified by SHA-256. A changed byte sequence is a different implementation authority and cannot inherit the prior binding.
- **AK-INGRESS-002 — External acceptance, no self-authorisation.** The kernel records a non-empty reference to explicit current human/programme acceptance for implementation, but a schema-valid binding record cannot create or prove that acceptance. The acceptance must exist in higher authority before the binding is used.
- **AK-INGRESS-003 — Bounded architectural projection and gate-owned candidate resolution.** The ingress binding records only the exact brief identity, its external acceptance reference and minimal architectural projection intent. A new-object intent supplies its architecture category plus a concise responsibility name; it does not supply a numeric object identifier. An existing-object modification supplies the current object identifier. The kernel deterministically resolves numeric create candidates from current post-reset allocation state. Candidate resolution is non-durable and does not itself allocate or admit an implementation identity. The binding does not copy, summarise, reconstruct or replace the brief's domain meaning.
- **AK-INGRESS-004 — Fail-closed semantic/architecture boundary.** If the accepted brief does not supply enough meaning to determine a lawful architectural projection, contains an unresolved semantic contradiction, or requires violation of kernel law, implementation stops and returns the defect to the authority owner/upstream process. The kernel does not invent the missing meaning.
- **AK-INGRESS-005 — Upstream-methodology opacity.** Implementation-authority ingress is methodology-agnostic. M10, G1-G7, PMB, worker/tester numbering, semantic-candidate numbering and other upstream process metadata are not required fields and do not create implementation authority.

## Two-sided admission boundary

The boundary answers two questions in order.

### 1. Is there implementation authority?

The worker must establish from current higher authority that one exact brief has been explicitly accepted for implementation. The mechanical binding then records:

- the SHA-256 of those exact raw brief bytes;
- a non-empty external acceptance reference;
- a bounded list of projection intents: `create` carries architecture category plus a concise responsibility name, while `modify` carries an existing current architecture identifier.

The repository validator can prove that supplied brief bytes match the recorded digest and that the record is structurally valid. It cannot prove that the human/programme actually accepted the brief or that the brief is semantically complete.

### 2. Can the accepted brief be projected lawfully?

Understanding the brief sufficiently to choose architecture-object targets is required implementation judgement. That judgement is bounded by the brief and by kernel law.

For `create`, the worker supplies no numeric identifier. The kernel resolves the candidate identifier mechanically from current registered identities, current retired identities, durable post-reset implementation allocations and earlier create candidates in the same binding. The concise responsibility name distinguishes independent same-category creates; it is not a package name or public-seam name. Candidate resolution is not durable allocation and does not mutate any registry or allocation history. A `modify` target must already exist. The target list is an architectural projection only; it is not a second normative brief.

An architecture identifier appearing in the brief is not automatically a current projection target. Target status must be established from the exact brief meaning, current higher authority and current kernel law. Where current higher authority explicitly dispositions an inherited structural allocation as `DO_NOT_CARRY_FORWARD`, the projection must not recreate that allocation merely because its historical identifier remains in the unchanged brief bytes. The projection record must state that disposition explicitly; it must not silently rewrite the brief or invent a replacement owner.

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
- create/modify projection intent is structurally invalid or a caller attempts to select a numeric create identifier;
- a resolved create candidate would reuse an identity consumed by current post-reset state;
- the requested implementation requires a category, ownership rule or seam that the brief does not establish.

A rejected ingress is not a semantic rejection of the upstream methodology. It means only that architecture-governed implementation cannot lawfully begin from the supplied authority state.
