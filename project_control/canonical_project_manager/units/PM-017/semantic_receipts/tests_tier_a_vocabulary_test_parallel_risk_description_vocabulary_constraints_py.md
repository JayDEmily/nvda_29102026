# Semantic receipt — `tests/tier_a/vocabulary/test_parallel_risk_description_vocabulary_constraints.py`

- Sequence `152`, PM-017; SHA-256 `daa3095f849e384882bbd6769bf10c7b7c9da70f004d7852f62a8a8d7944aa84`.
- Read full test `1-29` and full `docs/planning/PRL_RISK_DESCRIPTION_VOCABULARY_CONSTRAINTS.md`. Targeted run: `2 passed` inside `63 passed, 3 failed in 5.75s`.

## G1 — planning document names vocabulary sources

- Locator `6-18` checks five literal path strings in a planning document.
- This proves planning-document text only. It does not resolve those sources, enforce their current decisions or prove a renderer uses them.
- Relation `no_semantic_fit`; strength `presence_only`.

## G2 — planning document declares no free-form advice and no renderer implementation

- Locator `21-29` checks four literal declarations, including `Do not implement a renderer`.
- The assertions are accurate planning-state evidence but no runtime or contract surface is exercised.
- Relation `no_semantic_fit`; strength `historical_observational`.

## File decision

- Groups/relationships `2/2`; final `NON_AUTHORITATIVE_OBSERVATIONAL`.
- Retain only as planning-document inventory; it cannot serve as Tier-A description safety or vocabulary enforcement proof.
- No source, test, configuration, normative document, registry or proof-block mutation was executed.
