# Semantic receipt — `tests/tier_a/review_runtime/test_review_contract_authority_boundaries.py`

- Sequence `136`, PM-016; SHA-256 `d6179385b7b04744dec0375be9b1f902486d3d3874f96849ed1bd9df6e79c7f1`.
- Read full test `1-48`, full `src/nvda_desk/contracts/review.py`, current review-only explanation authority and PM-011 routes. Targeted run contribution: six parametrised cases/tests passed inside `24 passed in 0.29s`.

## G1 — exact top-level execution-authority field rejection

- Locator `14-33` exercises five review models against four exact top-level fields: `trade_allowed`, `broker_order_id`, `capital_sizing`, and `risk_limit_override`. All are rejected by closed Pydantic models.
- This is authoritative bounded proof for those exact fields at the top level and aligns with the rule that review/explanation does not become runtime, capital, risk or execution authority.
- It does not prove rejection of renamed, nested or semantically equivalent authority, nor any downstream behavioural non-mutation.
- Relation `exact_bounded_clause_proved`; strength `behavioural_schema`.

## G2 — caller-list detachment

- Locator `36-48` proves two input lists are copied into `ReviewLineagePacket` and remain unchanged after caller mutation.
- This is a bounded contract-isolation clause; it does not prove lineage truth, source availability or replay completeness.
- Relation `exact_bounded_clause_proved`; strength `behavioural_copy_boundary`.

## File decision

- Groups/relationships `2/2`; final `ADMIT_TIER_A_CURRENT` for the exact bounded clauses only.
- Admission scope is limited to rejection of the four named top-level fields across the five exercised models and detachment of the two exercised input lists. No phrase-global or nested-authority claim is admitted.
- No source, test, configuration, normative document, registry or proof-block mutation was executed.
