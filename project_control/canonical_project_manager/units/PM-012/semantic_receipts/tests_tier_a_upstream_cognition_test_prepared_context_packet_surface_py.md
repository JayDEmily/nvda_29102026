# Semantic receipt — `tests/tier_a/upstream_cognition/test_prepared_context_packet_surface.py`

## Process/restatement
- Sequence `029`, PM-012; SHA `bb0d40859b133970d47d730d0061534fc6b7343cb955cf52b5649b9b216e39c8`.
- Read full test `1-113`, preparation/context/checkpoint/packet surfaces, authority and routes. Pytest: `4 passed in 0.22s`.
- The file checks prepared-payload detachment/fingerprint repeatability, selected prepared-packet shell/lineage fields, checkpoint receipt detachment, and propagation of a failed-enrichment string into degraded validation.

## Relationships
1. `40-55`; `N04.2-001`/`N04.2-002`/`N04.2-006`, `docs/04.2...:17-64,126-146`: payload copying and repeatable JSON fingerprint for two equivalent snapshots. Mutating an alias or changing deterministic encoding fails `49-54`. Does not prove fingerprint completeness, collision resistance at semantic level, version binding or immutable source snapshot. `bounded_separable_clause` / `identity_lineage`; preserve.
2. `57-84`; `N04.2-002`, `27-64`; `N09-011`, `docs/09.1...:131-147`: selected prepared role labels, parent/source-artifact lists, non-empty fingerprint and extension alignment are carried. Altering observed fields fails `69-84`. It does not prove that snapshot ID is a retrievable source artefact, parent meaning, mandatory lineage, role checks or `valid` status; current default-valid is expressly non-compliance evidence. `related_but_not_proved` / `specimen_only`; P3/Gate D.
3. `87-95`; `N04.2-006`, `126-146`: receipt mapping mutation does not alter the snapshot and selected checkpoint values persist. Alias retention fails `95`. Does not prove deterministic field receipts, durability or valid-status semantics. `bounded_separable_clause` / `boundary`; preserve copy safety.
4. `98-113`; `N04.2-003`, `66-89`; `N09-006`, protocol validation `81-91`: one failed enrichment is named in payload, violations, keyflags and degraded state. Removing any carrier fails `109-113`. It does not prove that this failure is mandatory, complete, correctly owned or safely withheld downstream. `bounded_separable_clause` / `state_transition`; preserve narrow propagation.

## File disposition
- Groups `4`; relationships `4`; final `BLOCKED_P3_REPAIR`.
- The packet-carriage group materially overclaims canonical lineage/validation from selected labels and default `valid`; P3 must add role-specific identity, artefact, validation and authority-boundary proof. Narrow copy/failure-propagation evidence remains.
- No implementation/test mutation.
