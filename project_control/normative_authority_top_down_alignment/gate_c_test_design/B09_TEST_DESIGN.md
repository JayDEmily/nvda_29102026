# Gate C test-design pack — B09

## Acceptance rule

Tests in this pack express the frozen normative propositions and Gate B semantic behaviour. They do not take current code or current test colour as authority. A red result against the untouched alpha implementation is valid Gate C evidence.

## Requirements

### C-035 — Parallel Risk Lane evaluation

**Normative basis:** 5.8

**Behaviour to prove:** Partition tests by normative atom/family semantics, require configuration/version/lineage, prove independence from sizing/playbook authority and replace global state.

**Positive case:** Nominal typed path produces the stated output and preserves owner-issued identity.

**Negative case:** Missing mandatory authority, invalid type, duplicate/conflict or forbidden authority fails with the specified bounded error/withholding behaviour.

**False-positive resistance:** A green test must not pass solely because a model validates, a registry row exists, or a process-memory object can be read in the same process.

**Extension/substitution:** Where this is a volatility boundary, add/replace one source, strategy, policy, state adapter or output consumer without editing unrelated domain modules.

**Replay/lineage:** Where material, assert source/config/policy IDs and deterministic domain output; do not include current wall-clock metadata in domain-result equivalence.

**Current test assessment:** partially_aligned

**Accepted target(s):** tests/tier_a/normative_authority/test_gate_c_orchestration_playbook_and_risk.py::test_c020_c035_parallel_risk_policy_state_is_instance_owned_not_module_global

**Authority status:** READY / ADMITTED

### C-036 — Final risk overlay and terminal join

**Normative basis:** 5.8, 5.11

**Behaviour to prove:** Define and prove the actual join contract: required PRL packet identity, hard/caution semantics, precedence, missing-authority failure and receipt lineage.

**Positive case:** Nominal typed path produces the stated output and preserves owner-issued identity.

**Negative case:** Missing mandatory authority, invalid type, duplicate/conflict or forbidden authority fails with the specified bounded error/withholding behaviour.

**False-positive resistance:** A green test must not pass solely because a model validates, a registry row exists, or a process-memory object can be read in the same process.

**Extension/substitution:** Where this is a volatility boundary, add/replace one source, strategy, policy, state adapter or output consumer without editing unrelated domain modules.

**Replay/lineage:** Where material, assert source/config/policy IDs and deterministic domain output; do not include current wall-clock metadata in domain-result equivalence.

**Current test assessment:** insufficient

**Accepted target(s):** tests/tier_a/serial_recommendation/test_execution_final_join_boundary.py

**Authority status:** BLOCKED — The final serial/parallel risk join contract and precedence remain unresolved.

### C-037 — Capital deployment authority

**Normative basis:** 5.11

**Behaviour to prove:** Prove owner-sourced input construction, mandatory IDs, precedence, fresh-capital semantics, no serial-confidence sizing and immutable receipt reproduction.

**Positive case:** Nominal typed path produces the stated output and preserves owner-issued identity.

**Negative case:** Missing mandatory authority, invalid type, duplicate/conflict or forbidden authority fails with the specified bounded error/withholding behaviour.

**False-positive resistance:** A green test must not pass solely because a model validates, a registry row exists, or a process-memory object can be read in the same process.

**Extension/substitution:** Where this is a volatility boundary, add/replace one source, strategy, policy, state adapter or output consumer without editing unrelated domain modules.

**Replay/lineage:** Where material, assert source/config/policy IDs and deterministic domain output; do not include current wall-clock metadata in domain-result equivalence.

**Current test assessment:** partially_aligned

**Accepted target(s):** tests/tier_a/capital_deployment/test_sequence9_capital_deployment_decision_surface.py; test_capital_authority_service_surface.py; test_capital_contract_models.py

**Authority status:** READY / ADMITTED
