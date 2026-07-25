# Semantic receipt — `tests/tier_b/review_lineage/test_bounded_trace_review_regime.py`

- Sequence `172`, PM-018; SHA-256 `a0ba9e1d4a2f5ef1a30bf0745773d9d64c31a7ddace6b6db78af9796e264e1d9`.
- Read full test `1-38`, bounded-trace review service and trace-review contracts. Included in Tier-B run: `49 passed in 10.75s`.

## G1 — service and run-result surfaces exist
- Locator `21-27` proves import/symbol/model presence only.
- Relation `related_but_not_proved`; strength `presence_only`.

## G2 — selected human-sanity fields exist
- Locator `30-38` proves five field names only.
- It does not construct a regime scenario, verify values, compare runs or establish that the output is human-readable or review-only.
- Relation `related_but_not_proved`; strength `signature_only`.

## File decision
- Groups/relationships `2/2`; final `NON_AUTHORITATIVE_OBSERVATIONAL`.
- Preserve as a contract-shape smoke test; behavioural scenario/report proof is still required.
