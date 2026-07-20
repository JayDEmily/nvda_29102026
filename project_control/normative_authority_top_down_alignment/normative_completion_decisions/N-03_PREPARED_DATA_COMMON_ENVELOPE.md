# N-03 — Prepared-data common envelope

## Status

Accepted — normative authority complete for `C-008`.

## Unresolved proposition

What stable common envelope and typed payload boundary must every prepared runtime substrate expose, which identity/version/temporal/fingerprint facts are mandatory, and when must preparation fail closed rather than admit a generic or incomplete mapping?

## Material read set

Normative authority read in full or as the complete connected document before decision: `docs/03`, `docs/03.1`, `docs/04`, `docs/04.1`, `docs/07`, `docs/07.1`, `docs/09`, `docs/09.1`, `docs/11` and `docs/11.1`.

Gate B and Gate C evidence read: `B02.1` with its prepared-ingress context, row `C-008`, and the complete B02 Gate C design record.

Existing tests read as evidence: prepared runtime snapshot copy-boundary, prepared runtime substrate, transform-boundary, prepared ingress checkpoint and Gate C ingress identity/lineage tests.

Bounded source read as consequence evidence: runtime preparation, prepared-context packet construction, prepared-context contract, cognition ingress translator and typed stage-input bundle.

## Adopted project decision

Every prepared runtime substrate has a stable common envelope structurally separate from an explicitly tagged, strongly typed payload variant. The envelope mandatorily preserves prepared identity, per-input source/capture identities, input-family and source-contract identity, schema and preparation/derivation versions, per-source temporal truth and alignment policy, input and prepared semantic fingerprints, source artefact references, validation/completeness/limitation state and ordered parent-prepared lineage.

An authoritative cross-boundary prepared contract is not a generic dictionary. A mapping is permitted only as a bounded serialisation view after typed validation. Missing mandatory authority fails closed; only contract-permitted optional enrichment gaps may produce an explicitly degraded prepared state.

Governing propositions: `docs/04.2_PREPARED_DATA_CONTRACTS_WORKING.md` sections `04.2.N03.1` through `04.2.N03.7`.

## Alternatives ruled out

- Optional snapshot identity plus a generic payload dictionary: ruled out because the result cannot prove source/capture lineage, schema meaning or deterministic preparation.
- One anonymous provenance object for a multi-source substrate: ruled out because distinct source versions and temporal facts would be collapsed.
- A hash as sufficient replay evidence: ruled out because equality does not make missing source material retrievable.
- Successful model construction as authority: ruled out because validation shape alone cannot create missing owner-issued identity or source truth.
- Letting stage carriers define the prepared boundary: ruled out because stage allocation is downstream and is separately owned by `N-05`.

## Longitudinal effects

Admitted typed source material enters preparation; preparation creates one identified, versioned and fingerprinted prepared substrate with a typed payload; cognition and risk receive only admitted typed projections plus governed lineage; downstream packets and replay retain references to the same prepared authority.

## Transverse effects

The decision fixes identity roles, schema and policy versions, temporal preservation, source artefact lineage, input/result fingerprints, typed payload discrimination, validation/completeness, optional degradation, provider substitution and replay dependencies without granting trading authority to preparation.

## External sources

No external source was required. The exact envelope is project-specific and follows the already-governed owner/identity, typed-boundary, temporal-truth and fail-closed laws.

## Current implementation consequence

Current code has useful preparation and copy boundaries but exposes optional `snapshot_id`, generic payload/derived dictionaries and incomplete lineage. These are non-conforming implementation consequences only; no implementation change or conformance claim is made.

## Remaining Unknowns

- Concrete source-family payload schemas and provider-specific completeness guarantees remain bounded source-contract decisions.
- Production storage, retention duration and recovery technology remain intentionally unknown.
- `N-05` still owns exact propagation from the prepared envelope into common stage context versus stage-specific carriers.
- `N-09` still owns authoritative replay retention and executable-version availability.
