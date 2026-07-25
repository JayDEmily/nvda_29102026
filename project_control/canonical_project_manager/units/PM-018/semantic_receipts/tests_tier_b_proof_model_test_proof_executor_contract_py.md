# Semantic receipt — `tests/tier_b/proof_model/test_proof_executor_contract.py`

- Sequence `170`, PM-018; SHA-256 `63339294cde496512aa4279e8cb242ae751a22450d9149ed22d6b00cba1146c6`.
- Read full test `1-457`, full proof runner `scripts/run_proof_block.py`, Makefile proof targets and current proof-block manifest. Included in Tier-B run: `49 passed in 10.75s`.
- Proof execution is operational evidence only; it does not establish semantic acceptance of the blocks it runs.

## G1 — control files exist (6-9)
Presence only; relation `related_but_not_proved`; strength `presence_only`.
## G2 — control surfaces contain manifest-driven tokens (12-23)
Token/presence evidence, not behaviour; relation `related_but_not_proved`; strength `token_only`.
## G3 — describe returns one manifest summary (26-50)
Proves selected ID, tier, ownership and command projection; relation `bounded_separable_clause`; strength `behavioural`.
## G4 — runner source contains owned-path validation calls (53-58)
Source-token evidence only; relation `related_but_not_proved`; strength `token_only`.
## G5 — check validates one block without execution (61-79)
Proves successful check-mode output for one current block; relation `bounded_separable_clause`; strength `behavioural`.
## G6 — check-all validates current manifest without execution (82-97)
Proves successful current-manifest validation output; relation `bounded_separable_clause`; strength `behavioural`.
## G7 — check-all writes a JSON receipt (100-133)
Proves receipt mode/status/count/IDs/command/owns fields for current manifest; relation `bounded_separable_clause`; strength `identity_lineage`.
## G8 — CLI source exposes check/list/receipt functions (135-145)
Token-only evidence; relation `related_but_not_proved`; strength `token_only`.
## G9 — single-block check receipt (148-177)
Proves one check receipt payload and ownership projection; relation `bounded_separable_clause`; strength `identity_lineage`.
## G10 — list JSON exposes selected block IDs (180-195)
Proves current list projection only; relation `bounded_separable_clause`; strength `behavioural`.
## G11 — detailed list exposes command/owns/tier summaries (198-224)
Proves selected summary fields; relation `bounded_separable_clause`; strength `behavioural`.
## G12 — Python command resolves to current interpreter (226-236)
Proves exact command-token substitution and non-Python shlex split; relation `bounded_separable_clause`; strength `substitution`.
## G13 — candidate-review clean-check block is describable (239-259)
Proves one current manifest row, not the validity of its candidate semantics; relation `bounded_separable_clause`; strength `presence_only`.
## G14 — proof-executor block is self-described (262-287)
Proves current block ID/tier/command/owns projection; relation `bounded_separable_clause`; strength `presence_only`.
## G15 — unknown block IDs are rejected (317-337)
Proves fail-closed lookup and available-ID message; relation `bounded_separable_clause`; strength `boundary`.
## G16 — missing owned paths block command execution (340-358)
Proves missing-path failure occurs before marker creation; relation `bounded_separable_clause`; strength `boundary`.
## G17 — duplicate block IDs are rejected (361-376)
Proves duplicate-ID manifest validation; relation `bounded_separable_clause`; strength `boundary`.
## G18 — non-mapping block entries are rejected (379-385)
Proves malformed-entry validation; relation `bounded_separable_clause`; strength `boundary`.
## G19 — check-all does not execute commands (388-409)
Proves validation-only mode by absence of marker side effect; relation `exact_full_proof`; strength `boundary`.
## G20 — block header precedes child output (412-435)
Proves deterministic output ordering for one command; relation `bounded_separable_clause`; strength `behavioural`.
## G21 — manifest commands run without shell evaluation (438-457)
Proves the semicolon/touch payload is tokenised without shell injection for one specimen; relation `bounded_separable_clause`; strength `boundary`.

## File decision
- Groups/relationships `21/21`; final `ADMIT_TIER_B_SHADOW`.
- Admit behavioural runner, validation, receipt and no-shell clauses as shadow proof. G1/G2/G4/G8/G13/G14 remain structural supplements, and no proof-block result should be described as semantic acceptance.
