# Semantic receipt — `tests/tier_a/packets/test_dmpv3_extension_canonical_leaf_surface.py`

## 1. Process record

- Sequence: `017`
- Unit: `PM-012`
- Test SHA-256: `45dfe7e719fb31b6b8aae23b28cc0bd82d8cdcec3456f46acf9b48286ecd107d`
- Test read in full: lines `1-72`.
- Exercised implementation read in full: `src/nvda_desk/contracts/packets.py` and `src/nvda_desk/packets/dmp_packets.py`.
- Current retained-registry and proof-block routes inspected.
- Validation: `PYTHONPATH=src python -m pytest tests/tier_a/packets/test_dmpv3_extension_canonical_leaf_surface.py -q` returned `3 passed in 0.17s`, exit `0`.

## 2. Complete file restatement

The file checks that the canonical envelope and packet builder symbols exist. It then emits one packet with a caller-owned `nvda.execution_context` leaf plus an unknown custom extension and requires both leaves to survive the canonical merge. Finally, it attempts to inject a conflicting `nvda.semantic_dependencies` value and requires the builder to restore the canonical dependency list from `lineage.dependencyids` while preserving the unrelated execution-context leaf.

The file does not prove packet-role validity, lawful execution-context meaning, extension admission, schema-identifier overwrite, source identity, temporal lineage, complete lineage requirements, validation correctness, persistence, replay or boundary placement.

## 3. Authority context

- `docs/09_DMPV3_PROTOCOL_CORE.md:141-153` defines `dmpextensions` as bounded compatibility metadata, reserves repo-owned `nvda` leaves, forbids replacement or weakening of canonical fields, and requires custom extension merge without erasing canonical leaves.
- `docs/09.1_DMPV3_PROTOCOL_WORKING.md:106-119` requires governed extensions to have admitted ownership and semantics, forbids them from hiding authority or overwriting canonical fields/repo leaves, and permits unknown extensions to be preserved only as non-authoritative metadata.
- `docs/09.1_DMPV3_PROTOCOL_WORKING.md:41-61` defines `dependencyids` as identities of material governed dependencies distinct from immediate causal parents.

## 4. Assertion group 1 — canonical packet symbols are present (`9-11`)

1. **Behaviour:** imports and asserts non-`None` values for `DmpV3Envelope` and `build_dmp_v3_packet`.
2. **Authority meaning:** identifies the repo-owned canonical packet surface named by the protocol.
3. **Fit:** related surface-presence evidence only.
4. **Proved:** both imported symbols resolve.
5. **Not proved:** builder use, packet validity, canonical emission or any runtime boundary.
6. **Falsifier:** remove or rename either exported symbol.
7. **Required failure:** assertions `10-11`.
8. **Authority-violating implementation that passes:** expose inert or semantically wrong objects under the same names.
9. **Semantic relation:** `related_but_not_proved`.
10. **Proof strength:** `presence_only`.
11. **Disposition/gate:** retained only as bounded presence evidence.

## 5. Assertion group 2 — custom extension leaves survive canonical merge (`14-38`)

1. **Behaviour:** supplies `nvda.execution_context` and `custom.reader_hint`, then requires both values in the emitted extension map.
2. **Authority meaning:** custom compatibility metadata may be preserved without erasing unrelated repo-owned `nvda` leaves.
3. **Fit:** direct bounded extension-merge clause.
4. **Proved:** the two asserted leaves survive the recursive merge in this packet construction.
5. **Not proved:** that either leaf is admitted governed input, has a lawful owner/version/consumer, or can influence behaviour.
6. **Falsifier:** erase or overwrite either asserted leaf during merge.
7. **Required failure:** assertions `35-38`.
8. **Authority-violating implementation that passes:** preserve arbitrary extension content and later reinterpret it as source, decision or execution authority.
9. **Semantic relation:** `bounded_separable_clause`.
10. **Proof strength:** `behavioural`.
11. **Disposition/gate:** admitted only as unknown/custom metadata preservation and non-erasure proof.

## 6. Assertion group 3 — caller extension cannot replace canonical dependency annotation (`41-72`)

1. **Behaviour:** injects a conflicting extension dependency list, while supplying canonical `dependencyids`, and requires both lineage and the `nvda` compatibility leaf to contain the canonical list; an unrelated execution-context leaf must remain.
2. **Authority meaning:** extension data cannot overwrite or contradict canonical lineage-derived dependency annotations.
3. **Fit:** direct bounded anti-overwrite clause.
4. **Proved:** the tested builder restores `nvda.semantic_dependencies` from `lineage.dependencyids` after merge and preserves the unrelated leaf.
5. **Not proved:** truth, completeness or role-specific mandatory status of those dependency identities; other canonical leaves are not asserted.
6. **Falsifier:** permit the injected dependency list to replace either canonical carrier.
7. **Required failure:** assertions `62-72`.
8. **Authority-violating implementation that passes:** copy fabricated caller dependency IDs consistently into both canonical and extension carriers.
9. **Semantic relation:** `bounded_separable_clause`.
10. **Proof strength:** `identity_lineage`.
11. **Disposition/gate:** admitted narrow canonical-leaf precedence proof.

## 7. File-level disposition

- Assertion groups: `3`.
- Explicit proposition relationships: `3`.
- Final disposition: `ADMIT_TIER_A_CURRENT`.
- Admission scope: packet-extension merge non-erasure and canonical `dependencyids` precedence over a conflicting extension compatibility leaf only.
- Explicit exclusions: no extension governance/admission, full packet identity, packet-role validity, source or temporal lineage, schema-identifier guard, validation, persistence, replay or downstream authority proof.
- No implementation or test mutation executed.
