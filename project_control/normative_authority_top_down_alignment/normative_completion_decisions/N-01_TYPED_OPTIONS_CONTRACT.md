# N-01 — Typed options contract

## Status

Accepted — normative authority complete for `C-004`.

## Unresolved proposition

Must the serial options stage consume and carry raw/typed provider options material with its identity/version/time fields, or may it consume only derived primitives; and, under either choice, where must the original options evidence remain traceable?

## Material read set

Normative authority read in full or as the complete connected document before decision: `docs/03_DOMAIN_MODEL_CORE.md`, `docs/03.1_DOMAIN_MODEL_WORKING.md`, `docs/04_TECHNICAL_ARCHITECTURE_CORE.md`, `docs/04.1_TECHNICAL_ARCHITECTURE_WORKING.md`, `docs/07_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_CORE.md`, `docs/07.1_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_WORKING.md`, `docs/09_DMPV3_PROTOCOL_CORE.md`, `docs/09.1_DMPV3_PROTOCOL_WORKING.md`, `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md`, and `docs/11.1_NATIVE_ARCHITECTURE_BLUEPRINT_WORKING.md`.

Gate B and Gate C evidence read: `B01.4` with neighbouring `B01.3` and `B01.5`, `GATE_C_TEST_AUTHORITY_REGISTER.tsv` row `C-004`, and `gate_c_test_design/B01_TEST_DESIGN.md`.

Existing tests read as evidence: `tests/tier_a/upstream_cognition/test_cognition_ingress_mapping_surfaces.py`, `tests/tier_a/upstream_signal/test_raw_signal_transform_boundary_surface.py`, and `tests/tier_a/normative_authority/test_gate_c_ingress_identity_and_dmp.py`.

Bounded source read as consequence evidence: `src/nvda_desk/contracts/options_flow.py`, `src/nvda_desk/adapters/ingress/options_surface_feed.py`, `src/nvda_desk/cognition/ingress/options_mapper.py`, `src/nvda_desk/cognition/serial/options_flow.py`, and `src/nvda_desk/domain/options_flow/surface_state.py`.

## Adopted project decision

Raw/provider options material terminates at the source adapter and is preserved through a typed options-material contract before cognition. The serial options stage receives only typed derived primitives, explicit absence state, and a required lineage reference through the governed enclosing context. Raw chains, provider responses and generic mappings do not cross the cognition boundary.

The typed pre-cognition material must preserve source/provider identity, source-issued identity where available, repository capture identity, schema and preparation-policy versions, effective/observed/captured time semantics, fingerprint, validation outcome and source limitations. Missing mandatory authority fails closed; lawful source limitations remain explicit.

Governing propositions: `docs/03.2_INPUT_AND_CALENDAR_DOMAIN_WORKING.md` sections `03.2.N01.1` through `03.2.N01.7`.

## Alternatives ruled out

- Carrying the full raw options chain through serial cognition: ruled out because it couples provider volatility and ungoverned payload breadth into cognition.
- Keeping the current three derived values with no lineage reference: ruled out because it makes derived values self-authenticating and destroys options evidence identity/version/time.
- Using one generic mapping with optional metadata: ruled out because absence and schema drift become ungoverned.
- Reconstructing source identity from DMP packet identity, timestamps, filenames or hashes: ruled out because those facts have different owners and scopes.

## Longitudinal effects

Ingress must preserve typed options evidence; preparation must derive the bounded stage input; the serial options stage must not accept raw/provider material; Parallel Risk Lane and downstream consumers may use only admitted outputs and lineage; replay must locate the exact prepared options evidence rather than infer it from stage values.

## Transverse effects

The decision constrains input identity, temporal truth, prepared-data lineage, stage-carrier allocation, provider substitution, DMP carriage and replay. Packages `N-03`, `N-05` and `N-09` must preserve these obligations.

## External sources

No external source was required to choose this project-specific boundary. Existing project authority already requires typed volatility boundaries, owner-issued identity, explicit temporal truth, no generic-dictionary drift and no downstream fabrication. External vendor architecture examples were therefore not used as evidence.

## Current implementation consequence

Current `OptionsFlowContextInput` carries derived values and explicit missing fields but no governed reference to options-material identity/version/time. The current adapter and mapper therefore provide partial evidence only. This is not an implementation change and no conformance claim is made.

## Remaining Unknowns

- Exact field names and physical nesting for the common prepared/stage metadata remain owned by `N-03` and `N-05`.
- Exact provider-specific mandatory/optional facts remain contract-specific and are not selected by this package.
