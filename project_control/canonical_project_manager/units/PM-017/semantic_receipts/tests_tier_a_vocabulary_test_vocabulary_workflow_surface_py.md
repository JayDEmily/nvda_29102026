# Semantic receipt — `tests/tier_a/vocabulary/test_vocabulary_workflow_surface.py`

- Sequence `166`, PM-017; SHA-256 `8928caec2cf7e619a6db54278bf637e0b89fd7221d0f656b6b516bf6e27dfcc6`.
- Read full test `1-20`, full consolidation workflow document and vocabulary candidate-action law. Targeted run: `1 passed in 0.03s`.

## G1 — workflow file and four action tokens are present
- Locator `8-18` proves the named Markdown file exists and contains the four action spellings.
- It does not prove the workflow is current, internally consistent or followed by code.
- Relation `related_but_not_proved`; strength `presence_only`.

## G2 — audit/LLM-pass wording is present
- Locator `19-20` checks two text fragments only. The concatenated literal `"candidate" "_audit"` is a source-level token check, not workflow behaviour.
- Relation `related_but_not_proved`; strength `token_only`.

## File decision
- Groups/relationships `2/2`; final `NON_AUTHORITATIVE_OBSERVATIONAL`.
- The file is a useful documentation-smoke check but cannot establish candidate governance, semantic admission or execution of the LLM review gate.
- No protected source, test, configuration, normative, registry or proof-block file was changed.
