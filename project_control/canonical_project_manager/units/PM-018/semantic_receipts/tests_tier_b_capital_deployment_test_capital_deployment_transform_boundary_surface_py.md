# Semantic receipt — `tests/tier_b/capital_deployment/test_capital_deployment_transform_boundary_surface.py`

- Sequence `167`, PM-018; SHA-256 `252905dbfef7502920b58a9c74e049531e4f0894a23991b3efb2ed2f2aff28e7`.
- Read full test `1-85`, four capital source surfaces, closed capital input/decision contracts and downstream-capital authority law. Included in the 13-file Tier-B run: `49 passed in 10.75s`.

## G1 — four source files lack four donor tokens
- Locator `60-66` proves only textual absence in the listed files. Renamed or indirect posture ownership would pass, and harmless text could fail.
- Relation `related_but_not_proved`; strength `token_only`.

## G2 — closed capital input rejects donor posture fields
- Locator `69-72` proves three extra-field specimens fail Pydantic validation.
- This directly protects the input transform boundary for those fields, not all possible posture smuggling.
- Relation `bounded_separable_clause`; strength `boundary`.

## G3 — posture hard-stop truth arrives as pre-deployment block
- Locator `75-85` proves the capital evaluator blocks when the upstream pre-deployment result is false, emits the expected rationale, and does not expose the donor surface token in consumed inputs or JSON.
- It does not prove the upstream block was itself lawfully derived.
- Relation `bounded_separable_clause`; strength `behavioural`.

## File decision
- Groups/relationships `3/3`; final `ADMIT_TIER_B_SHADOW`.
- Admit G2-G3 as shadow boundary evidence; retain G1 only as weak supplementary evidence and replace it with behavioural negative specimens before Tier-A promotion.
