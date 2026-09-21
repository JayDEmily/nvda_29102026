# VI-10R6 — canonical Raw Signal catalogue-ID carriage

## Status

**CURRENT PROGRAMME-AUTHORISED CONTRACT CLARIFICATION FOR THIS TRANCHE.**

This record resolves only Tester Iteration 008 finding `T008-F005`. It does not reopen unrelated accepted Raw Signal meaning.

## Authority

Current Programme Owner direction on 2026-09-21 establishes that the preserved workbook
`NVDA_80_STEP_ACADEMIC_EVIDENCE_AUDIT_WITH_SIGNALS_ADDENDUM_81_94.xlsx`, SHA-256
`519ea9449297d564ae4a02afc1bf4e60e4471631c81a0842620f9fb60bb4f9ae`, is the canonical catalogue source for established Raw Signal identifiers `R001`–`R323` and that those identifiers are materially important to the Raw Signal data model.

The accepted IRB remains controlling for the current tranche. In particular:

- BC-005 requires exact provider-native logical-record fidelity;
- BC-010 requires workbook alias, provider/source identifier, domain occurrence, concept and contract identities to remain separately typed;
- BC-012 permits a new optional `.v1` field only when it cannot change interpretation of an existing v1 payload;
- BC-013 forbids workbook identity from deciding Raw Signal outcomes;
- BC-016 keeps concrete provider eligibility/mapping contents and `D001+` outside this tranche.

## Bound carriage rule

`RawObservationOccurrenceV1` gains one **optional provenance field**:

`raw_signal_catalogue_ids`

When present, it carries one or more separately typed `RawSignalCatalogueId` values. The admitted value space for this tranche is exactly `R001` through `R323` as established by the canonical workbook.

The field is compatible under BC-012 because its absence leaves every previously valid v1 payload with exactly its prior interpretation. Presence adds provenance only; it does not alter observation identity, native value meaning, temporal meaning, receipt assessment, eligibility, schedule membership or any existing field.

### Identity separation

`RawSignalCatalogueId` is a distinct identity layer. It is not interchangeable with:

- `native_identifier` or any provider/source identifier;
- `observation_occurrence_id`;
- `delivery_artifact_ref`;
- concept ID;
- contract/schema ID;
- capture/policy/assessment identity;
- ingestion-sequence scope;
- run/replay/packet identity.

A provider logical record may lawfully carry more than one canonical Raw Signal ID because BC-006 permits one provider logical record to contain multiple native fields. The carriage therefore does **not** assert a universal one-record/one-signal rule. It also does not itself define the concrete provider-field-to-catalogue mapping; such mapping remains separately governed/Unknown where BC-016 says so.

When no admitted mapping supplies a canonical Raw Signal ID, the field is absent (`None`). An empty collection is not a substitute for absence. Duplicate IDs within one carriage value are invalid because they do not represent an additional identity binding. No semantic ordering claim is made from collection order.

### Bounds and derived-signal exclusion

This clarification does **not** admit workbook min/max/bounds, plausibility validation, rescaling, rounding or sign normalisation. It does not admit any `D001+` derived-signal behaviour. `Dxxx` values are not valid `RawSignalCatalogueId` values.

## Proof consequences

The VI-10R6 proof must establish at minimum:

1. optional absence preserves the prior v1 interpretation;
2. valid `R001` and `R323` endpoints are accepted, malformed/out-of-range/`Dxxx` IDs are rejected;
3. the catalogue identity type is runtime/static distinct from every other active identity layer;
4. one logical record can carry multiple distinct catalogue IDs without splitting the observation or conflating them with provider-native identity;
5. catalogue IDs survive the real PostgreSQL restart/readback path exactly;
6. no proof introduces workbook bounds or concrete provider mapping decisions.
