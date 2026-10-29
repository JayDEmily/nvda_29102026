# D123 calculation-definition clarification — Programme Owner, 2026-10-11

**Authority revision:** `D123-20261011-01` (date-labelled normative clarification; **not** a new runtime value or an invented provider-mapping version).
**Authority:** Explicit programme-owner instruction, 2026-10-11, “M01 F4 — D123 Open-Interest Dependency and Official-Refresh Correction”.
**State:** semantic rule AUTHORISED; the mandatory official-reporting-period source contract is not yet established. **This is not an implementation-completion or acceptance statement.**

## Scope and invariant

D123 remains the same `D123`, bound to `K02_ALGEBRA` with declared `R047;R048` catalogue dependencies and arithmetic `current_official_OI - prior_official_OI`. The immutable catalogue row must not be changed by treating these inputs as simultaneous opposite-right values for a single exact contract.

* For a selected exact **call** contract, `R047` is mandatory and `R048` is **not applicable**. A missing `R048` must not itself defeat D123.
* For a selected exact **put** contract, `R048` is mandatory and `R047` is **not applicable**. A missing `R047` must not itself defeat D123.
* Select only exact matching underlying, expiry, strike, option right, native contract identity, source, eligible temporal and version context. No opposite-right substitute or fabricated co-identity is authorised. This D123-specific source-selection exception does not extend to D119 or other genuinely conjunctive calculations.
* Use the **latest two distinct eligible official OI reporting refreshes** for the selected exact contract. Distinguish identity of a reported period from any later revision *to the same period*. A later-arriving tick is not automatically a new official reporting period. Apply the knowledge cutoff, temporal eligibility and established version/revision precedence; preserve both exact raw observations and versions in derived lineage. Fail closed if either reporting period or its authoritative revision cannot be established without ambiguity.

## Required source-contract prerequisite (unresolved)

This clarification **does not** assign an unproved official reporting-period identity to `source_timestamp_raw`, `received_ts_utc`, `ingestion_sequence`, `revision_vintage_native`, or a fabricated key in `RawSelectionIdentityV1`. Nor does it define a string/numeric sort over provider revision vintages. The admitted M00 projection can carry a provider-mapped exact identity, but no admitted provider-specific official OI reporting-period mapping and revision-ordering rule was established by the inspected repository authority for R047/R048.

No production repair may represent these unresolved inputs as established, including an implementation which silently takes the last two received ticks. Continue only when authoritative source evidence supplies the exact M00-accessible identity/ordering semantics and their mapping/version law. Preserve the original +25-call-contract public regression witness and its numerical expected result; the witness's different source instants alone do not prove distinct official reporting periods.

No change to accepted D123 arithmetic, declared catalogue rows, M00 ownership, unrelated calculations, Stage 2 scope or distribution version `1.0.0` is authorised here.

## Subsequent Programme-Owner amendment — provider-independent implementation admitted (2026-10-11)

**Authority:** “M01 F4 — D123 Provider-Independent Official Open-Interest Proof”,
11-10-2026. This instruction **supersedes** the historical “no production
repair pending live provider mapping” restriction in the section above **only**
for provider-independent calculations through controlled, explicitly versioned
M00 projections. The earlier restricted state is retained above for chronology,
not as a current prohibition of the bounded controlled proof.

The admitted `RawSignalProjectionMappingV1.selection_identity_field_paths`
projects the following controlled native-record fields into
`RawSelectionIdentityV1`, without changing the M00 interface or ownership:

| M00 selection identity key | Controlled test-contract meaning |
| --- | --- |
| `official_reporting_period_id` | Non-empty stable string identifying one official OI reporting period; revisions of the same period retain this identity |
| `official_reporting_period_order` | Non-negative integer chronological ordinal; each distinct period has one distinct ordinal, with larger values later |
| `official_revision_id` | Non-empty immutable identifier for one correction/version within the given reporting period |
| `official_revision_precedence` | Positive integer correction order *within that period*, with larger precedence replacing smaller; tied or contradictory rankings refuse |

The selected contract is identified independently and exactly by `contract_id`,
`underlying_instrument`, `expiry`, `strike`, `option_right`, and the controlled
`source_provider` / `source_variant` namespace. The M00 projection mapping
reference and unit convention reference carry concrete version identities;
source/event and receipt timestamps enforce as-of and knowledge eligibility.
A test must explicitly supply every official-period and revision field through
its controlled native record and admitted mapping. No timestamp, UUID,
`revision_vintage_native` or arrival order is reinterpreted as one of these
four official semantic fields.

The current result is selected from the highest eligible period ordinal and
the prior result from the next lower distinct eligible period ordinal, using
the single highest unambiguous revision precedence **within each**. All
candidate revisions must have a coherent period/ordering contract; any
ambiguous or absent essential field refuses rather than guessing. Persist only
the two selected raw occurrence IDs and their exact versioned mapping/unit
lineage for the derived delta. A call's R048 and a put's R047 are not mandatory.

These test-contract fields and revision-ordering conventions are **controlled
provider-independent semantics**, not verified meanings of live IBKR ticks
27/28, OCC feeds or any provider-native record. Real-source integration still
requires an independently evidenced official-period/revision mapping. Real
records without such admitted fields must fail closed. Stage 1 and F4 remain
unaccepted until the separate full F4 acceptance criteria are established.
