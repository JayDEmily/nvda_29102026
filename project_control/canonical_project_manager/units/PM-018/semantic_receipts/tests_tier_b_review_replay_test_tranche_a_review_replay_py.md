# Semantic receipt — `tests/tier_b/review_replay/test_tranche_a_review_replay.py`

- Sequence `175`, PM-018; SHA-256 `df1cab3d29b1f102bbfb0730b531dd7f233804b6b59e5843e0bcd6e4351130fc`.
- Read full test `1-101`, review-replay contracts, deterministic comparison and citation-mapping services, plus proposition N07.2-009. Included in Tier-B run: `49 passed in 10.75s`.

## G1 — comparison remains review-only and identifies compared/missing sources
- Locator `23-47` proves two cited source identifiers are compared, none is missing, and the returned model carries `promoted_to_runtime=False` and no runtime-side-effect entries.
- The no-promotion fields are output invariants of this bounded service; they do not prove absence of side effects elsewhere in the repository.
- Relation `bounded_separable_clause`; strength `boundary`.

## G2 — citations join deterministically to review decisions
- Locator `50-77` proves source, decision, admission class, supersession status and rejection reason carriage for two rows.
- It does not validate the truth or authority of the imported claims or decisions.
- Relation `bounded_separable_clause`; strength `identity_lineage`.

## G3 — decision input order does not change the comparison result
- Locator `80-101` proves full model equality for one reversed decision ordering.
- Relation `bounded_separable_clause`; strength `replay`.

## File decision
- Groups/relationships `3/3`; final `ADMIT_TIER_B_SHADOW`.
- Admit as review-only deterministic comparison/trace shadow proof under N07.2-009. Promotion still requires missing/duplicate decision cases and stronger non-side-effect evidence at the target runtime boundary.
