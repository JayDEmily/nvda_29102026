# M01–M03 Semantic Continuity — Bounded Normative Alignment

## Governing locators

- `docs/07.1_NORMATIVE_WORKING.md` sections 7.9 and 7.10.
- `docs/04.2_DATA_PREPARATION_AND_PROVENANCE_WORKING.md` N03/N04.
- `docs/11.1_NATIVE_ARCHITECTURE_BLUEPRINT_WORKING.md` M01–M03 and
  M00-UPSTREAM-001 through M00-UPSTREAM-004.
- `project_control/canonical_project_manager/CONTINUATION.md` section 11.

## C-NORM-01 — M01 semantic binding authority

A source family routed to M03 must declare, in its registered family contract,
which concrete payload fields represent which M03 prepared semantic fields.
Each binding names the payload field, semantic field, exact scalar value type,
unit and required/optional status. M01 validates the binding against the
registered concrete payload model and carries the immutable binding set in its
accepted source artefact and raw-signal product. M01 does not resolve competing
sources or derive prepared fields.

## C-NORM-02 — M02 selected fact completeness

Each selected M02 field carries the selected value, value type, unit and complete
candidate/source/layer lineage. Type and unit must be common across every
coalesced selected candidate and are included in projection identity. M02 does
not create M03 prepared identity.

## C-NORM-03 — M03 owner-evidence construction

The canonical M03 builder accepts exact accepted M01 source artefacts and exact
usable M02 projections, not caller-authored lineage references. It revalidates
the owner products, constructs M03 candidate records from their declared facts,
resolves each direct prepared field under an explicit versioned M03 field policy,
executes only admitted deterministic derivation rules, and constructs the tagged
prepared payload and receipts itself.

A direct prepared value must equal the selected owner evidence. A derived value
must be recomputed from exact selected input fields and record exact candidate
IDs and fingerprints. Missing mandatory evidence, unresolved conflicts,
unsupported operations, type/unit mismatch, owner-product forgery, foreign M02
lineage or any caller attempt to inject a prepared value withholds the envelope.

## C-NORM-04 — M00 delegation

M00 sequences M01, M02 and M03. It passes exact accepted owner products and the
caller-selected M03 policy/rule identifiers. It must not inspect source payload
field names, construct semantic references, choose values, calculate
derivations, or accept a caller-authored `PreparedRuntimePayloadV1`.

## C-NORM-05 — Scope boundary

This repair closes M01/M02 evidence into M03. It does not claim that M05 serial
cognition is yet bound to the exact M03 payload. That separately verified defect
remains open and must be visible in closeout controls.
