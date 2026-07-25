# Semantic receipt — `tests/tier_a/persistence/test_fwd003_import_registry_contract.py`

- Sequence `121`, PM-015; SHA-256 `c0bf2d39fcf61d5699f030d54f5e279f9890507832bcfd5a174b858c87bcfdc2`.
- Read full test `1-107`, full `src/nvda_desk/persistence/import_registry.py`, full `src/nvda_desk/schemas/import_registry.py`, current persistence/transaction authority and current PM-011 route. Targeted pytest was included in the PM-015 seven-file run: `25 passed in 0.26s`.

## G1 — bounded schema and duplicate/extra rejection

- Test locator `18-48` proves selected enum-constrained model construction, registry/grammar indexing, duplicate `registry_id` rejection and closed top-level input for the exercised specimen.
- This is real schema regression evidence, but no current normative proposition admits `SourceForm`, `MaturityState`, `RuntimeTarget`, `GrammarRole` or this import-registry document as project authority. A duplicate grammar mapping or dangling `registry_id` is not challenged here.
- Relation `related_but_not_proved`; strength `behavioural_schema`.

## G2 — backlog, depth, tokenisation and readiness reports

- Test locator `51-84` proves deterministic report values for two caller-authored JSONL rows and one grammar row.
- The tested readiness, backlog, import-depth and runtime-contract classifications are implementation-owned migration taxonomy. They are not established by current persistence, migration or blueprint propositions; tokenisation and labels cannot elevate them to authority.
- A semantically invalid registry can pass whenever its caller-authored labels produce the expected reports.
- Relation `unsupported_policy_taxonomy`; strength `behavioural_specimen`.

## G3 — no-loss assertion and report writing

- Test locator `87-107` proves set-membership checking for caller-supplied expected IDs and JSON report output for one seeded row.
- `assert_no_loss` proves only equality against the expected set supplied by the same caller; it does not prove completeness against a governed source population, semantic preservation, durable persistence or replay.
- Relation `related_but_not_proved`; strength `behavioural_specimen`.

## File decision

- Groups/relationships `3/3`; final `BLOCKED_MISSING_NORMATIVE_AUTHORITY`.
- Preserve the bounded schema, duplicate-ID, closed-input and deterministic-report clauses as implementation evidence. Tier-A admission requires exact normative authority for the registry taxonomy and governed source population, plus proof that readiness/no-loss classifications derive from that authority rather than caller-authored labels.
- No source, test, configuration, normative document, registry or proof-block mutation was executed.
