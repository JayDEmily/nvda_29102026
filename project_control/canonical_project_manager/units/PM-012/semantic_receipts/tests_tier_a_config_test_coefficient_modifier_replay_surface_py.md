# Semantic receipt — `tests/tier_a/config/test_coefficient_modifier_replay_surface.py`

## 1. Process record

- Sequence: `006`
- Unit: `PM-012`
- Test SHA-256: `3fd8a87689c8ce48ad4b428325b641c27c7bfeddd61ab28ce0ebc80453564a86`
- Test read in full: lines `1-40`.
- Exercised implementation read in full: `src/nvda_desk/config/coefficient_authority.py` lines `1-250`, `src/nvda_desk/cognition/modifiers/state_conditioned.py` lines `1-110`, `src/nvda_desk/contracts/modifiers.py` lines `1-120`, `src/nvda_desk/contracts/coefficient_authority.py` lines `1-213`, and `config/coefficient_authority.v1.yaml` lines `1-82`.
- No external fixture, parametrisation, setup/teardown or monkeypatch.
- Validation: `PYTHONPATH=src python -m pytest tests/tier_a/config/test_coefficient_modifier_replay_surface.py -q` returned `2 passed in 0.29s`, exit `0`.

## 2. Complete file restatement

The first test builds two coefficient/modifier replay receipts from the same default authority document, one active policy ID and owner stage. It verifies the receipt type, equal fingerprints, ascending coefficient-ID order and three declared closed-authority class strings. The second reaches the same receipt builder through `StateConditionedModifierService`, verifies owner-stage and active-policy identity, verifies two effective coefficient values produced by the selected policy, and verifies the fourth declared closed-authority class.

The file observes one policy, one owner stage, one checked-in configuration version and one repeated identical-input execution. It never changes an input or config dependency to prove fingerprint sensitivity, independently recomputes the fingerprint, verifies authority/schema/modifier versions, tests missing/duplicate/unknown policy IDs, tests hard bounds or owner-stage rejection, proves that the declared closed authorities are behaviourally inaccessible, exercises a downstream consumer, reconstructs a retained material decision, or establishes the full authoritative replay envelope in `07.2.N09`.

## 3. Authority context

- `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:271-286` defines row 5.9 as bounded coefficient/modifier authority, with governed config and state context as inputs, bounded coefficients/modifier packets as outputs, and unbounded mutation, hidden strategy changes, capital decisions and source ingestion prohibited. Its proof interface expressly includes replay determinism tests.
- `docs/11.1_NATIVE_ARCHITECTURE_BLUEPRINT_WORKING.md:53` records current implementation truth as `thin_seam`: bounded local behaviour exists, while material version carriage and complete consumer integration remain incomplete.
- `docs/06.1_PROCESS_AND_TRANCHE_LAW_WORKING.md:382-396` historically opened bounded row 5.9 replay receipt construction and required deterministic replay plus identification of closed authority classes without opening the prohibited decisions.
- `docs/07.1_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_WORKING.md:179-184` assigns coefficient/modifier ownership, permits consumers to use resolved packets and replay receipts, prohibits four authority classes and requires receipt carriage of authority/version, schema, owner stage, active modifier identities/versions, resolved snapshots, closed classes and deterministic semantic fingerprint.
- `docs/07.2_STATE_RISK_AND_REPLAY_WORKING.md:145-189` separately defines authoritative replay. In particular, a hash or local object is insufficient by itself (`175`), and complete result-changing configuration/policy/coefficient/modifier/executable versions are required (`161-181`). This test is therefore bounded row 5.9 receipt proof, not proof of authoritative end-to-end replay.
- Accepted P1 semantics keep `Coefficient Authority`, `Modifier Authority`, `State-conditioned Modifier` and `Bounded Dynamic Coefficient` separate: `project_control/canonical_project_manager/units/PM-010/P1_INTEGRATED_SEMANTIC_REGISTER.tsv:34-43`.

## 4. Assertion group 1 — same bounded inputs produce the same receipt fingerprint (`8-19`)

1. **Behaviour:** constructs two receipts using the same authority file, policy list and owner stage; verifies the result type and equal fingerprint strings.
2. **Authority meaning:** row 5.9 requires deterministic semantic receipt construction for resolved coefficient/modifier authority.
3. **Fit:** this is a bounded positive specimen of deterministic output under identical logical inputs and executable/config state.
4. **Proved:** the current implementation returns `ModifierReplayReceipt` and repeats the same fingerprint for the tested input/config combination.
5. **Not proved:** fingerprint sensitivity to any changed policy, coefficient, version or implementation; collision resistance as a semantic claim; independently correct payload coverage; retrievability; full authoritative replay; identity/version completeness.
6. **Falsifier:** introduce nondeterministic material into the fingerprint payload or return a different receipt type.
7. **Required failure:** type assertion `18` or equality assertion `19`.
8. **Authority-violating implementation that passes:** hash a constant value for every possible input; both tested calls remain equal.
9. **Semantic relation:** `bounded_separable_clause`.
10. **Proof strength:** `replay` limited to identical-input receipt determinism.
11. **Disposition/gate:** `ADMIT_TIER_A_CURRENT` for this narrow clause only; not an `07.2.N09` replay-envelope claim.

## 5. Assertion group 2 — resolved coefficient order is deterministic (`20-22`)

1. **Behaviour:** verifies the returned coefficient IDs are in ascending lexical order.
2. **Authority meaning:** replay evidence requires deterministic ordering/version information sufficient to distinguish and reproduce result-changing material.
3. **Fit:** canonical ordering of the resolved snapshots is a separable deterministic-receipt property, although lexical order is the current implementation choice rather than the only lawful ordering policy.
4. **Proved:** all resolved coefficient IDs in this receipt are returned in sorted order.
5. **Not proved:** uniqueness, complete expected membership, stable ordering under added coefficients, order-version identity or that the ordering policy is itself declared in the receipt.
6. **Falsifier:** return the same tested coefficients in nonsorted order.
7. **Required failure:** equality assertion `20-22`.
8. **Authority-violating implementation that passes:** return a sorted but incomplete or semantically wrong coefficient set.
9. **Semantic relation:** `bounded_separable_clause`.
10. **Proof strength:** `replay` for deterministic snapshot ordering.
11. **Disposition/gate:** `ADMIT_TIER_A_CURRENT` with no completeness claim.

## 6. Assertion group 3 — three prohibited authority classes are named in the receipt (`23-25`)

1. **Behaviour:** checks that the receipt's `closed_authority_classes` contains capital deployment, source ingestion and hidden strategy change.
2. **Authority meaning:** row 5.9 must explicitly identify those authority classes as closed.
3. **Fit:** the assertions directly prove carriage of three exact required closure labels.
4. **Proved:** the tested receipt declares those three classes closed.
5. **Not proved:** behavioural impossibility of those decisions, recursive forbidden-key rejection, absence of hidden pathways or enforcement by downstream consumers.
6. **Falsifier:** omit or rename one tested label.
7. **Required failure:** membership assertion `23`, `24` or `25`.
8. **Authority-violating implementation that passes:** retain the labels while another method performs capital sizing, source ingestion or hidden strategy mutation.
9. **Semantic relation:** `bounded_separable_clause`.
10. **Proof strength:** `boundary` as declared receipt metadata, not whole-system non-interference.
11. **Disposition/gate:** `ADMIT_TIER_A_CURRENT` for identification of closed classes only.

## 7. Assertion group 4 — service wrapper preserves tested owner and active-policy identity (`28-37`)

1. **Behaviour:** obtains a receipt through the state-conditioned service and verifies owner stage `posture` and active policy list `['negative_gamma_stress']`.
2. **Authority meaning:** the receipt must carry owner stage and active modifier identity/version material, and the wrapper must not replace governed runtime stages or invent ownership.
3. **Fit:** the assertions prove exact identity carriage for one owner and one policy ID through the wrapper.
4. **Proved:** the requested owner-stage string and active policy ID survive into the receipt unchanged for this call.
5. **Not proved:** modifier-policy version, authority version, schema assertion, duplicate/unknown policy handling, owner-stage validation, identity preservation for multiple policies, ordering semantics or downstream consumption.
6. **Falsifier:** rewrite the owner stage or active policy list before returning the receipt.
7. **Required failure:** equality assertion `36` or `37`.
8. **Authority-violating implementation that passes:** preserve the two strings while resolving policy content from an unversioned or wrong authority source.
9. **Semantic relation:** `bounded_separable_clause`.
10. **Proof strength:** `identity_lineage` limited to tested owner/policy identifiers.
11. **Disposition/gate:** `ADMIT_TIER_A_CURRENT`; no version-completeness claim.

## 8. Assertion group 5 — one state-conditioned policy produces two expected effective values (`35-39`)

1. **Behaviour:** indexes resolved snapshots by coefficient ID and verifies `max_risk_per_trade == 0.25` and `hedge_required is True`.
2. **Authority meaning:** Modifier Authority may change only admitted mutable coefficient surfaces through a promoted state-conditioned policy, while Coefficient Authority owns baseline/bounds/config records.
3. **Fit:** this is a bounded positive specimen of the currently promoted policy's output meaning for one numeric and one Boolean coefficient.
4. **Proved:** the checked-in `negative_gamma_stress` policy currently resolves the two asserted effective values for owner stage `posture`.
5. **Not proved:** baseline values, hard-floor/cap enforcement, policy direction, surface-class legality, owner-stage rejection, no modification of baseline-only records, state-condition activation, policy version or consumer application.
6. **Falsifier:** change either resolved effective value or omit either coefficient.
7. **Required failure:** equality assertions `38-39` or dictionary lookup at those lines.
8. **Authority-violating implementation that passes:** hard-code these two outputs while ignoring config lineage, bounds, state conditions or other resolved surfaces.
9. **Semantic relation:** `bounded_separable_clause`.
10. **Proof strength:** `behavioural` for the two tested resolved values.
11. **Disposition/gate:** `ADMIT_TIER_A_CURRENT` for this promoted-config specimen only.

## 9. Assertion group 6 — unbounded runtime mutation is named closed (`40`)

1. **Behaviour:** verifies the receipt also declares `unbounded_runtime_mutation` closed.
2. **Authority meaning:** row 5.9 expressly prohibits unbounded coefficient tuning/live self-mutation.
3. **Fit:** the exact required closure label is carried in the receipt.
4. **Proved:** this receipt identifies unbounded runtime mutation as a closed class.
5. **Not proved:** that all coefficient writes are structurally impossible, that the config cannot be mutated elsewhere, or that the policy cannot escape hard bounds.
6. **Falsifier:** omit or rename the closure label.
7. **Required failure:** membership assertion `40`.
8. **Authority-violating implementation that passes:** keep the label while exposing a separate live self-tuning path.
9. **Semantic relation:** `bounded_separable_clause`.
10. **Proof strength:** `boundary` as declared receipt metadata.
11. **Disposition/gate:** `ADMIT_TIER_A_CURRENT` for closed-class identification only.

## 10. Final file disposition

`ADMIT_TIER_A_CURRENT`

The file proves six separable current row 5.9 clauses: identical-input receipt determinism, deterministic coefficient ordering, carriage of four required closed-class labels, tested owner/policy identity carriage and two promoted effective values. Its Tier-A claim must remain narrow. It does not prove complete coefficient/modifier authority, actual non-interference, material version carriage, fingerprint sensitivity, full consumer integration or authoritative replay under `07.2.N09`.

- Assertion-group count: `6`
- Relationship count: `6`
- Return gate: retain in the Tier-A projection only with the bounded row 5.9 claim above; do not route it as full authoritative replay-envelope proof.
