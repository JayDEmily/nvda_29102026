# Gate C test-design pack — B05

## Acceptance rule

Tests in this pack express the frozen normative propositions and Gate B semantic behaviour. They do not take current code or current test colour as authority. A red result against the untouched alpha implementation is valid Gate C evidence.

## Requirements

### C-018 — Financial calendar state ownership

**Normative basis:** 5.4, 5.16

**Behaviour to prove:** Before tests, confirm the authoritative calendar layer model; then prove owner, precedence, identity and substitution at each layer.

**Positive case:** Nominal typed path produces the stated output and preserves owner-issued identity.

**Negative case:** Missing mandatory authority, invalid type, duplicate/conflict or forbidden authority fails with the specified bounded error/withholding behaviour.

**False-positive resistance:** A green test must not pass solely because a model validates, a registry row exists, or a process-memory object can be read in the same process.

**Extension/substitution:** Where this is a volatility boundary, add/replace one source, strategy, policy, state adapter or output consumer without editing unrelated domain modules.

**Replay/lineage:** Where material, assert source/config/policy IDs and deterministic domain output; do not include current wall-clock metadata in domain-result equivalence.

**Current test assessment:** partially_aligned

**Accepted target(s):** tests/tier_a/financial_calendar/test_financial_calendar_authority_surface.py; test_financial_calendar_transform_boundary_surface.py; tests/tier_a/calendar_operational/test_calendar_operational_surface.py

**Authority status:** BLOCKED — Calendar layer ownership and precedence depend on the unresolved layer model.

### C-019 — Core material runtime state repositories

**Normative basis:** 5.13, 5.15-5.16

**Behaviour to prove:** Retain local contract tests but add restart/durable adapter contract tests only where the normative boundary requires durability; never label memory stores durable.

**Positive case:** Nominal typed path produces the stated output and preserves owner-issued identity.

**Negative case:** Missing mandatory authority, invalid type, duplicate/conflict or forbidden authority fails with the specified bounded error/withholding behaviour.

**False-positive resistance:** A green test must not pass solely because a model validates, a registry row exists, or a process-memory object can be read in the same process.

**Extension/substitution:** Where this is a volatility boundary, add/replace one source, strategy, policy, state adapter or output consumer without editing unrelated domain modules.

**Replay/lineage:** Where material, assert source/config/policy IDs and deterministic domain output; do not include current wall-clock metadata in domain-result equivalence.

**Current test assessment:** implementation_locked

**Accepted target(s):** tests/tier_a/normative_authority/test_gate_c_state_calendar_and_repositories.py::test_c019_c023_shared_memory_repository_contract_is_copy_safe_and_instance_isolated

**Authority status:** READY / ADMITTED

### C-020 — Parallel Risk policy-decision state

**Normative basis:** 5.8, 5.16

**Behaviour to prove:** Prove injected repository ownership, run/session identity, duplicate law and isolation between service instances/tests.

**Positive case:** Nominal typed path produces the stated output and preserves owner-issued identity.

**Negative case:** Missing mandatory authority, invalid type, duplicate/conflict or forbidden authority fails with the specified bounded error/withholding behaviour.

**False-positive resistance:** A green test must not pass solely because a model validates, a registry row exists, or a process-memory object can be read in the same process.

**Extension/substitution:** Where this is a volatility boundary, add/replace one source, strategy, policy, state adapter or output consumer without editing unrelated domain modules.

**Replay/lineage:** Where material, assert source/config/policy IDs and deterministic domain output; do not include current wall-clock metadata in domain-result equivalence.

**Current test assessment:** insufficient

**Accepted target(s):** tests/tier_a/normative_authority/test_gate_c_orchestration_playbook_and_risk.py::test_c020_c035_parallel_risk_policy_state_is_instance_owned_not_module_global

**Authority status:** READY / ADMITTED

### C-021 — API-local veto and risk-block state

**Normative basis:** 5.1, 5.8, 5.16

**Behaviour to prove:** Either remove from admitted architecture or define typed owner/contract; test that API storage cannot influence domain decisions directly.

**Positive case:** Nominal typed path produces the stated output and preserves owner-issued identity.

**Negative case:** Missing mandatory authority, invalid type, duplicate/conflict or forbidden authority fails with the specified bounded error/withholding behaviour.

**False-positive resistance:** A green test must not pass solely because a model validates, a registry row exists, or a process-memory object can be read in the same process.

**Extension/substitution:** Where this is a volatility boundary, add/replace one source, strategy, policy, state adapter or output consumer without editing unrelated domain modules.

**Replay/lineage:** Where material, assert source/config/policy IDs and deterministic domain output; do not include current wall-clock metadata in domain-result equivalence.

**Current test assessment:** insufficient

**Accepted target(s):** tests/tier_a/normative_authority/test_gate_c_outputs_replay_and_api.py::test_c021_c048_api_does_not_own_untyped_veto_or_risk_block_state

**Authority status:** READY / ADMITTED
