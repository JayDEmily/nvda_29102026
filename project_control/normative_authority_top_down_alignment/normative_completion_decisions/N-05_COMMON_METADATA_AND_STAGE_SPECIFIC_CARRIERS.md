# N-05 — Common metadata and stage-specific carriers

## Status

Accepted — normative authority complete for `C-013`.

## Unresolved proposition

Which identity, lineage, version, temporal and completeness facts belong in a common cognition-ingress context, which facts belong only in stage-specific carriers, and how are independently dispatched carriers kept narrow without losing authority?

## Material read set

Normative authority read in full or as connected authority before decision: `docs/02`, `02.1`, `03`, `03.1`, `03.2`, `04`, `04.1`, `04.2.N03-N04`, `05`, `07`, `07.1`, `09`, `09.1`, `11` and `11.1`.

Gate B and Gate C evidence read: `B03.3` with neighbouring derivation/lineage context, row `C-013`, and the complete B03 Gate C design record.

Existing tests read as evidence: cognition ingress mapping, regime ingress, translation coordinator and Gate C ingress identity/version tests.

Bounded source read as consequence evidence: temporal, regime, options/flow and stage-input contracts; all three ingress mappers; ingress translator; prepared runtime substrate.

## Adopted project decision

Cognition ingress emits one typed stage-input bundle containing one immutable common stage context plus narrowly typed stage-specific carriers. The common context carries only bundle/prepared/source identity references, schema/preparation/derivation/mapping versions, prepared fingerprint, temporal/completeness/validation summary, resolution-receipt references and bundle-level status. Stage carriers carry only stage-required primitives, bounded structures, explicit missing states, stage contract/policy version and a common-context reference where detached.

Missing common authority, mismatched references, unknown variants, undeclared fields or payload widening fail closed. An incomplete carrier is lawful only when both the prepared and stage contracts admit the exact absence.

Governing propositions: `docs/04.2_PREPARED_DATA_CONTRACTS_WORKING.md` sections `04.2.N05.1` through `04.2.N05.6`.

## Alternatives ruled out

- Duplicating common identity/version fields into every stage carrier: ruled out because copies drift and widen stage payloads.
- Giving each stage the complete prepared mapping: ruled out because stages would inspect unrelated/provider-shaped facts and become coupled to preparation internals.
- Keeping all temporal and provenance truth only in the temporal carrier: ruled out because regime/options carriers would lose their enclosing prepared authority.
- One untyped metadata bag: ruled out because it permits undeclared lineage and authority contamination.
- Assuming bundle degradation automatically permits all stages to execute: ruled out because stage policies own bounded incomplete-state handling.

## Longitudinal effects

The prepared substrate is projected once into an identified common context and narrow carriers; the orchestrator dispatches each carrier with the same immutable context/reference; stages consume only owned fields; replay can reproduce the exact projection from retained prepared authority and mapping version.

## Transverse effects

The decision fixes common-versus-stage allocation, identity/reference consistency, contract and policy version carriage, temporal/completeness summary, payload narrowing, stage substitution, orchestrator non-authority and replay reconstruction.

## External sources

No external source was required. The exact allocation is project-specific and derives from the governed narrow-carrier, owner/identity and no-generic-mapping laws.

## Current implementation consequence

Current typed stage carriers are narrow but the bundle has no common context and the regime/options carriers lose prepared identity/version/fingerprint lineage. No implementation change or conformance claim is made.

## Remaining Unknowns

- Exact field names and concrete contract schemas are implementation artefacts to be derived from these propositions.
- Later-stage carrier families beyond the currently reconstructed serial stages require their own bounded contract work under the same law.
- `N-09` still owns authoritative retention and replay reconstruction requirements.
