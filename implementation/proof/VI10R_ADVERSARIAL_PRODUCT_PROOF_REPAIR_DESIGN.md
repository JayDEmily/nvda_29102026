# VI-10R — Adversarial Product Proof Repair Design

## Status

`AUTHORISED SUCCESSOR PROOF REPAIR — PRE-IMPLEMENTATION`

This design repairs the six material findings returned by VI-11 Tester Iteration 003. It supersedes the failed VI-10 proof design only for the repaired successor candidate. The failed candidate remains preserved in Git history.

## Bound predecessor and authority

- failed VI-10 proof target: `f83efd9b489dbe7072da8c96320504a468c55a1a` / tree `beba36d889696915bbcecccd861dab9ab0c1a4cd`
- VI-11 reviewed submission: `e778df15d7a478741cde53ffe8a0373e59e2820e` / tree `4612b37480e5145d769a88cf73590b511273ae1c`
- tester response SHA-256: `74a39cc175d3d34837971b76e78007fd891940ca7a3d5db76af7036a5df9a482`
- exact IRB, BICP, IWO and routed METHOD-006 authority remain unchanged.

No production implementation may be inspected or authored during this repair.

## Repair law

The successor proof must close every tester finding by making the prohibited implementation fail physically, not by narrowing claims or weakening family metadata.

### R1 — PostgreSQL durability and restart cross a real process boundary (`T003-F001`)

U05 must:

- perform committed writes in one Python process and read/reconcile in a later fresh Python process against the same PostgreSQL database;
- observe failed-write absence from a fresh process;
- establish direct PostgreSQL state mutation in addition to server-version connectivity;
- prove that a fresh read cannot succeed through a deliberately invalid PostgreSQL DSN, closing an alternative process-memory/local-substitute path;
- preserve no-cross-kind-atomicity/SLA/replay/retention nonclaims.

A proof-only subprocess driver may live under `tests/product/raw_signal/`; it must call the same production owner construction path as the ordinary tests and may not implement Raw Signal semantics.

### R2 — use the real production owner/composition construction path (`T003-F002`)

The private production symbols `_build_test_owner` and `_build_test_application` are no longer accepted proof construction paths.

- U01-U05 obtain the semantic owner through production public symbol `nvda_desk.raw_signal_occurrence_truth.api.create_owner`.
- Proof helpers may supply technical dependencies/fault injection only; they may not implement outcomes or domain decisions.
- U06 uses production A00 composition symbol `nvda_desk.composition.create_application` and injects a spy owner factory solely to prove that A00 constructs/uses M00 through its public command/read facets.
- U06 must assert call/delegation order and object identity of returned M00 results, so A00-owned outcome calculation or a test-only semantic path cannot pass.

These are proof-facing construction-shape constraints only; they add no product meaning.

### R3 — assessment outcomes are evidence-discriminated (`T003-F003`)

Normal assessment append proof must not let the caller author semantic truth unchecked.

- zero scenario: no eligible committed receipt is visible to the assessment transaction;
- one-or-more scenario: at least one eligible committed receipt is visible;
- later-evidence scenario: first establish lawful zero, then commit eligible evidence, then append one-or-more superseding the zero without overwrite;
- incompatible caller-supplied outcome must fail closed, or the production command may derive the outcome itself;
- `unknown_not_established` remains proven through the authorised restart missing-slot reconciliation path.

The repair chooses the stronger proof-facing shape: `append_capture_receipt_presence_assessment` receives identity/capture/as-of/supersession inputs and M00 derives the outcome. Supplying `outcome=` is a prohibited caller-semantic path and must fail.

### R4 — policy versions cannot overlap (`T003-F004`)

- the lawful v2 test begins exactly at v1's exclusive deactivation boundary;
- a separate negative test attempts an overlapping active interval and must fail closed.

### R5 — physical identity-layer substitution matrix (`T003-F005`)

U01/U03 must substitute actual values from one identity layer into another contract/command identity position and require fail-closed behaviour. The matrix covers the active slice's distinct concept, contract, scope-policy identity/reference, capture, observation, assessment, provider/source and delivery layers. Inactive run/replay/packet/workbook/lineage identities remain prohibited as unadmitted authority fields rather than being fabricated.

The proof does not require a particular identity-wrapper class name; it requires the runtime contracts/commands to preserve and reject cross-layer substitution.

### R6 — contract-wide `.v1` compatibility discrimination (`T003-F006`)

U01 must cover all five contracts and the BC-012 breaking classes:

- requiredness;
- discriminants/allowed values;
- time/null law;
- identity law;
- provenance law.

The compatibility proof must also demonstrate that a genuinely optional additive field is compatible only when existing v1 interpretation is unchanged. The proof harness therefore compares actual public constructor field requiredness against the accepted baseline while permitting only additional optional fields, and separately self-tests that compatibility rule with a synthetic optional addition. Runtime negative cases continue to exercise the governed discriminants and required fields directly.

## Mutation jurisdiction

Allowed successor mutation:

- `config/product_proof/families.yaml` only where case descriptions/limitations must match repaired physical proof;
- `tests/product/raw_signal/_support.py`;
- `tests/product/raw_signal/_process_probe.py`;
- `tests/product/raw_signal/test_u01_contract_owner_boundary.py` through `test_u06_a00_composition.py` as required by the six findings;
- VI-10R proof evidence and control/handoff records.

Prohibited:

- `src/nvda_desk/**` production behaviour;
- architecture registries/proof configuration;
- IRB/BICP/IWO/METHOD-006 meaning;
- product obligation removal, tier reclassification or aggregate weakening.

## Acceptance before re-review

The successor candidate must:

1. validate product-proof control with exactly the same 13 product obligations and six families;
2. collect the complete repaired physical suite;
3. remain expected-red before production implementation for attributable missing implementation/mandatory PostgreSQL environment, not malformed proof;
4. keep `architecture_kernel` green and preserve mypy/Ruff/dependency/seam checks;
5. contain no production-source mutation;
6. record explicit predecessor -> finding -> repair lineage;
7. be committed cleanly and handed to a fresh VI-11 reviewer.
