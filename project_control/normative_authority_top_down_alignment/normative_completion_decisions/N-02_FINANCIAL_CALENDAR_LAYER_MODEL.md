# N-02 — Financial-calendar layer model and ownership

## Status

Accepted — normative authority complete for `C-005` and `C-018`.

## Unresolved proposition

What are the exact financial-calendar business layers, their owners and identities; how do reference, operational and derived facts relate; and what precedence, substitution, conflict and degradation law applies?

## Material read set

Normative authority read in full or as the complete connected document before decision: `docs/03`, `docs/03.1`, `docs/04`, `docs/04.1`, `docs/07`, `docs/07.1`, `docs/10`, `docs/10.1`, `docs/11`, `docs/11.1`, and the vocabulary registry/process surfaces.

Gate B and Gate C evidence read: `B01.5` with neighbouring ingress units, `B05.1` with neighbouring state-ownership units, rows `C-005` and `C-018`, and the complete B01/B05 Gate C design records.

Existing tests read as evidence: calendar reference crosswalk, financial-calendar authority and transform-boundary tests, operational calendar tests, runtime calendar query proof, and Gate C state/calendar authority proof.

Bounded source read as consequence evidence: reference contracts, importer, projection/crosswalk, operational event/session repositories and bounded SQLite session storage.

## Adopted project decision

The exact business model has four layers: `market_session_reference`, `financial_event_reference`, `operational_calendar_state`, and `derived_runtime_calendar_context`.

The two reference layers own distinct immutable selected-version fact families. Operational state may append observed facts and may supersede a named same-family fact only through explicit authorised supersession lineage. Derived context is a non-owning versioned projection and never writes source truth. There is no global source order: precedence is per semantic key and fact family; unresolved same-level conflict fails closed or produces an explicitly degraded partial context where the projection contract permits.

Governing propositions: `docs/03.2_INPUT_AND_CALENDAR_DOMAIN_WORKING.md` sections `03.2.N02.1` through `03.2.N02.7`.

## Alternatives ruled out

- One undifferentiated `calendar` store: ruled out because session truth, scheduled-event truth, observed corrections and derived context have different owners and update laws.
- Treating importer, projector, in-memory repository and SQLite table as four business layers: ruled out because those are technical implementations, not semantic facts.
- Global precedence by recency, file order or non-empty value: ruled out because it can silently select a fact without owner-authorised semantic substitution.
- Operational state silently overwriting reference: ruled out because history, lineage and correction authority would disappear.
- Derived runtime context becoming source truth: ruled out because projection would become self-authorising.

## Longitudinal effects

Checked session and event reference facts enter separately; authorised operational updates append alongside them; projection resolves an as-of context under explicit supersession/conflict law; temporal, serial and Parallel Risk consumers receive context only; downstream decision authority remains separate.

## Transverse effects

The decision fixes calendar vocabulary, source/version identity, state ownership, persistence classification, precedence, substitution, completeness/degradation, projection lineage and replay obligations. `N-09` must retain exact selected facts, versions and supersession decisions for authoritative replay.

## External sources

No external source was required. The exact model is a project-specific decomposition derived from the already-governed separation of reference truth, operational state, derived context, identity ownership and fail-closed behaviour. Vendor calendar models were not adopted by implication.

## Current implementation consequence

Current code has explicit reference import, crosswalk projection, operational event/session repositories and a bounded SQLite session table. It accepts arbitrary layer IDs and lacks one governed supersession/precedence contract. These are implementation consequences only; no implementation change or conformance claim is made.

## Remaining Unknowns

- Concrete provider-specific schemas and completeness guarantees remain input-contract decisions.
- Production persistence, retention and recovery remain intentionally unknown.
- Numeric materiality or downstream trading consequences remain owned by later policy boundaries, not this calendar model.
