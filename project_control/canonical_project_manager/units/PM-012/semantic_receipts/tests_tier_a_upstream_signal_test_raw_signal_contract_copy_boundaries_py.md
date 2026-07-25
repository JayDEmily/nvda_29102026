# Semantic receipt — `tests/tier_a/upstream_signal/test_raw_signal_contract_copy_boundaries.py`

- Sequence `036`, PM-012; SHA `eb88c7bd0ad639a1600b2c675dfee242bf0f98263f837b5f6ba69ec2398b2bf3`.
- Read full test `1-40`, full upstream-signal contract, authority and routes. Pytest: `2 passed in 0.18s`.
- G1 `9-17`, authority `N03-002` (`docs/03.1_DOMAIN_MODEL_WORKING.md:21-39`) and `N04-002` (`docs/04.1...:21-42`): closed raw carrier rejects an undeclared top-level `trade_allowed` authority field. Accepting it fails the expected exception. Declared payload can still encode forbidden meaning. `bounded_separable_clause` / `boundary`; admit narrow.
- G2 `20-40`, `N03-002`: constructor deep-detaches the asserted nested dict/list payload from caller mutation. Retaining an alias fails `37-40`. It does not prove source identity/version/lineage, post-construction immutability or payload semantics. `bounded_separable_clause` / `identity_lineage`; admit narrow.
- Groups/relationships `2/2`; final `ADMIT_TIER_A_CURRENT`, limited to top-level schema closure and caller-payload detachment. No mutation executed.
