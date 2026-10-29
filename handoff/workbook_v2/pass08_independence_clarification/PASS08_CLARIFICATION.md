# Pass 08 — M02–M31 module self-sufficiency clarification

**Status:** Workbook V2 design clarification only; no new production module admitted. Parent checkpoint: `6df15c94a85422090b62900cce89cb234af6abea`.

## Binding V2 design reading

- **M00** and proposed **M01-1** supply reusable foundational raw/derived-raw facts.
- **M02–M31** are peer modules, independently executable, independently configurable and testable. They **must not have runtime or private-data dependencies on one another**. Their working numbers are not an execution sequence.
- Where downstream peers need equivalent strategy-dependent intermediate mathematics, each **contains its own local implementation and tests**, including the required intermediate calculation chain back to lawful foundational ingress. Private intermediate results are not duplicate canonical `Dxxx` outputs.
- Inherited cross-group `Dxxx` references describe the *existing accepted M01 calculation graph only*. They cannot be read as proposed runtime interfaces, peer module calls, design-authorised D-ownership transfers, or an instruction to route data between peers.
- The applicable validation target is **independent module self-sufficiency**, not 'cross-module dependency migration'. Work to implement or accept such modules has **not** been authorised by this documentation pass.

## Current evidence and limitations

The Pass06 107-reference / 67 ordered-group-pair crosswalk remains unchanged as historical audit evidence. The Workbook V2 module sheets must label these entries 'historical D-lineage only; no runtime edge'. The accepted normative M01 catalogue, M00/M01 implementation, Git history and production registry remain unchanged. No per-module full transitive closure or independent execution proof is claimed.

## Superseded descriptions

This clarification **supersedes wording, not accepted mathematics**, in Pass06 handoff, prior worksheet annotations, and related review documents describing the 107 references as 'interfaces to migrate' or 'dependency migration'. It does not rewrite those historical evidence artefacts. ADR-WBV2-002 is the operative V2 design statement and the new Pass08 workbook is the current reader-facing version.

## Relationship to base architecture

`docs/architecture/DEPENDENCY_LAWS.md` (`AK-DEP-001`) permits properly declared and acyclic M-to-M runtime dependencies generally. It **does not require** any peer-module dependency. The owner-approved V2-specific design deliberately chooses *none between M02–M31* and is not an amendment to the generic normative law.
