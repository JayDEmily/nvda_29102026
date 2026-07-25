# Semantic receipt — `tests/tier_a/normative_authority/test_gate_c_ingress_identity_and_dmp.py`

- Sequence `144`, PM-017; SHA-256 `0e705c9a2dd5afea58e6c4414a78b98731685bfa8d8a8774c18683205391ac29`.
- Read full test `1-113`, directly exercised ingress, stage-input, preparation-lineage and DMP builder surfaces, current propositions `C-001;C-002;C-003;C-009;C-010;C-012;C-015;C-016`, and the Gate C admission receipt/promotion manifest. Targeted run: `1 passed, 6 failed`; those failures are within the frozen `11 green / 42 expected red` Gate C implementation pack.

## G1 — market external authority is recursively rejected

- Locator `18-26` requires a nested `trade_allowed` field to fail closed.
- It exactly exercises one nested forbidden execution-authority specimen; renamed or semantically equivalent keys are outside this assertion.
- Relation `bounded_separable_clause`; strength `boundary`.

## G2 — options external authority is recursively rejected

- Locator `29-42` requires nested `authorised_notional_usd` to fail closed.
- This is one exact nested capital-authority specimen, not exhaustive semantic detection.
- Relation `bounded_separable_clause`; strength `boundary`.

## G3 — unrelated untyped API payload is not silently reclassified

- Locator `45-49` requires `RawBundleLoader` to reject an unrelated provider mapping.
- It proves one fail-closed specimen for typed-family ownership; it does not enumerate all malformed or ambiguous families.
- Relation `bounded_separable_clause`; strength `boundary`.

## G4 — stage bundle carries common identity/version metadata

- Locator `52-61` requires four named fields on `StageInputBundle`.
- This is exact contract-shape proof only; it does not prove population, truth or propagation of those fields.
- Relation `bounded_separable_clause`; strength `presence_only`.

## G5 — prepared lineage names material derivation and provenance fields

- Locator `64-73` requires five exact lineage fields.
- This proves required schema names, not source truth or derivation reproducibility.
- Relation `bounded_separable_clause`; strength `presence_only`.

## G6 — DMP builder cannot fabricate execution context or lineage

- Locator `76-88` requires omission of trace, run, scenario, source-artifact and fingerprint authority to fail.
- This is a direct negative boundary for caller-owned DMP context.
- Relation `bounded_separable_clause`; strength `identity_lineage`.

## G7 — explicit process metadata yields reproducible DMP domain content

- Locator `91-113` builds the same envelope twice and requires equality, exact emission time and source-artifact carriage.
- It proves deterministic construction for one explicit specimen, not semantic truth of caller-supplied metadata or full packet-role validity.
- Relation `bounded_separable_clause`; strength `identity_lineage`.

## File decision

- Groups/relationships `7/7`; final `ADMIT_TIER_A_CURRENT` under the explicit Gate C admission authority.
- Current red assertions remain blocking Gate D implementation obligations; semantic admission is not an implementation-pass claim.
- No source, test, configuration, normative document, registry or proof-block mutation was executed.
