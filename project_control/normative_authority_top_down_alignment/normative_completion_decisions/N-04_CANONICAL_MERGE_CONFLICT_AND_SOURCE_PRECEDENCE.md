# N-04 — Canonical merge conflict and source precedence

## Status

Accepted — normative authority complete for `C-011`.

## Unresolved proposition

How must preparation resolve overlapping source-section values into canonical fields, when can one candidate lawfully win, what constitutes unsafe conflict, and what field-level lineage is required?

## Material read set

Normative authority read in full or as connected authority before decision: `docs/03`, `03.1`, `03.2`, `04`, `04.1`, `04.2.N03`, `05`, `07`, `07.1`, `09`, `09.1`, `11` and `11.1`.

Gate B and Gate C evidence read: `B03.1` with neighbouring canonicalisation/derivation context, row `C-011`, and the complete B03 Gate C design record.

Existing tests read as evidence: prepared-runtime substrate and transform-boundary tests.

Bounded source read as consequence evidence: the complete runtime preparation module, especially raw-section combination, temporal selection and options fallback.

## Adopted project decision

There is no global source precedence. Every overlapping semantic field is resolved by an explicit, versioned field-resolution rule that names admitted candidates, comparability requirements, equality/tolerance, authorised owner/fallback/supersession logic, lineage and failure outcome.

Semantically equal candidates may coalesce while retaining all provenance. Unequal candidates may be selected only under the field-specific rule. An unresolved mandatory single-valued conflict fails closed; a degraded or multi-valued result is lawful only where the typed contract explicitly admits it. Every multi-candidate field requires a deterministic resolution receipt.

Governing propositions: `docs/04.2_PREPARED_DATA_CONTRACTS_WORKING.md` sections `04.2.N04.1` through `04.2.N04.6`.

## Alternatives ruled out

- Market then options then provenance as a universal order: ruled out because source authority differs by semantic field.
- Latest, non-empty, highest confidence or dictionary insertion order as inherent authority: ruled out because those criteria require field-specific semantic authorisation.
- Silent last-write-wins: ruled out because it destroys conflicting evidence and owner lineage.
- Always failing on duplicate values: ruled out because semantically equal corroborating candidates can coalesce lawfully.
- Letting downstream stages resolve conflicts independently: ruled out because the prepared boundary owns canonicalisation and replayable receipt formation.

## Longitudinal effects

Source-family candidates enter preparation with identity and temporal truth; a versioned field rule compares and resolves them; the prepared typed payload carries the canonical/degraded fact and receipt reference; downstream consumers do not repeat source selection.

## Transverse effects

The decision fixes source precedence, equality/tolerance, candidate preservation, conflict/degradation, fallback/supersession, provider substitution, field lineage and deterministic replay while preserving domain-specific calendar supersession law.

## External sources

No external source was required. The exact policy is project-specific and derived from governed source ownership, typed preparation, temporal precision and fail-closed requirements.

## Current implementation consequence

Current raw-section combination is deterministic but uses implicit market/options/provenance order and special-case spot selection without field-level receipts or conflict rejection. No implementation change or conformance claim is made.

## Remaining Unknowns

- Exact field-resolution rule entries, tolerances and source roles are implementation-policy artefacts to be derived under this authority.
- Provider-specific source quality and completeness remain source-contract decisions.
- `N-09` still owns retention sufficient to reproduce candidate evidence and resolution receipts authoritatively.
