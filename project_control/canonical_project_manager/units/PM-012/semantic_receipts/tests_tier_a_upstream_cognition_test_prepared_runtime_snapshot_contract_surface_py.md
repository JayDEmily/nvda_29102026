# Semantic receipt — `tests/tier_a/upstream_cognition/test_prepared_runtime_snapshot_contract_surface.py`

- Sequence/unit `030` / `PM-012`; SHA `2554646fc4e655ba998ec0c57159de5a530eab9f9f1878d891c15c7b6f979604`.
- Read full test `1-20`, full snapshot/preparation implementation, authority and routes. Pytest: `1 passed in 0.04s`.
- **Assertion group `8-20`:** `PreparedRuntimeSnapshot.as_mapping()` deep-detaches the observed nested dictionary/list path. Authority `N04.2-001`, `docs/04.2_PREPARED_DATA_CONTRACTS_WORKING.md:17-25`, requires a stable typed prepared envelope and treats mappings as serialisation views. If an alias is retained, assertion `20` fails after mutation. The test does not prove object-wide immutability, identity/lineage/version/fingerprint, serialisation round-trip or preparation correctness. Relation `bounded_separable_clause`; strength `boundary`; disposition narrow admission.
- Groups/relationships `1/1`; final `ADMIT_TIER_A_CURRENT`, limited solely to nested mapping detachment on the asserted path. No implementation/test mutation.
