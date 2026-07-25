# Semantic receipt — `tests/tier_a/normative_authority/test_gate_c_orchestration_playbook_and_risk.py`

- Sequence `146`, PM-017; SHA-256 `81ea3953226ca4b69dc947a6f5c0e6088734d6ceae89fb0ccc4d358b6bc2af8b`.
- Read full test `1-97`, directly exercised runtime, Parallel Risk and playbook surfaces, current propositions `C-017;C-020;C-025;C-027;C-031;C-032;C-033;C-035`, and Gate C admission evidence. Targeted run: `1 passed, 5 failed`, within the frozen expected-red pack.

## G1 — Parallel Risk bootstrap requires upstream identity/lineage
- Locator `33-41` requires missing trace/run/scenario/derivation/source/fingerprint authority to fail.
- Relation `bounded_separable_clause`; strength `identity_lineage`.
## G2 — Parallel Risk policy state is instance-owned
- Locator `44-50` requires one service instance's decision not to appear in another instance.
- Relation `bounded_separable_clause`; strength `state_transition`.
## G3 — temporal and regime outputs carry defining policy versions
- Locator `53-59` requires non-empty policy-version fields on both outputs.
- Relation `bounded_separable_clause`; strength `identity_lineage`.
## G4 — governed orchestration rejects invalid mapping
- Locator `62-64` requires one untyped partial stage mapping to fail rather than execute.
- Relation `bounded_separable_clause`; strength `boundary`.
## G5 — playbook registry substitution leaves consumer unchanged
- Locator `67-91` substitutes a two-entry registry and requires selection by candidate family with registry/metadata carriage.
- Relation `bounded_separable_clause`; strength `substitution`.
## G6 — orchestrator receives candidate families and registry as owned inputs
- Locator `94-97` requires two named parameters. Signature proof only; correct use is not proved.
- Relation `bounded_separable_clause`; strength `signature_only`.

## File decision

- Groups/relationships `6/6`; final `ADMIT_TIER_A_CURRENT` under the Gate C admission receipt.
- Five current failures remain implementation obligations; the one green substitution specimen does not imply orchestration completion.
- No source, test, configuration, normative document, registry or proof-block mutation was executed.
