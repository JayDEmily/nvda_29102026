# Gate C test-design pack — B08

## Acceptance rule

Tests in this pack express the frozen normative propositions and Gate B semantic behaviour. They do not take current code or current test colour as authority. A red result against the untouched alpha implementation is valid Gate C evidence.

## Requirements

### C-032 — Playbook registry and library

**Normative basis:** 5.10; docs/02.1_BRIEFING_AND_EXECUTION_OPERATING_MODEL_WORKING.md:44-60

**Behaviour to prove:** Prove registry-driven composition: add/remove a playbook without editing orchestrator/eligibility/domain code, preserve stable contract and reject unknown/disabled definitions.

**Positive case:** Nominal typed path produces the stated output and preserves owner-issued identity.

**Negative case:** Missing mandatory authority, invalid type, duplicate/conflict or forbidden authority fails with the specified bounded error/withholding behaviour.

**False-positive resistance:** A green test must not pass solely because a model validates, a registry row exists, or a process-memory object can be read in the same process.

**Extension/substitution:** Where this is a volatility boundary, add/replace one source, strategy, policy, state adapter or output consumer without editing unrelated domain modules.

**Replay/lineage:** Where material, assert source/config/policy IDs and deterministic domain output; do not include current wall-clock metadata in domain-result equivalence.

**Current test assessment:** partially_aligned

**Accepted target(s):** tests/tier_a/normative_authority/test_gate_c_orchestration_playbook_and_risk.py::test_c032_playbook_registry_substitution_does_not_require_consumer_changes

**Authority status:** READY / ADMITTED

### C-033 — Playbook eligibility compilation

**Normative basis:** 5.7, 5.10

**Behaviour to prove:** Prove candidate-family origin, registry version and composed selection; preserve stand-down when posture blocks or candidate set is empty.

**Positive case:** Nominal typed path produces the stated output and preserves owner-issued identity.

**Negative case:** Missing mandatory authority, invalid type, duplicate/conflict or forbidden authority fails with the specified bounded error/withholding behaviour.

**False-positive resistance:** A green test must not pass solely because a model validates, a registry row exists, or a process-memory object can be read in the same process.

**Extension/substitution:** Where this is a volatility boundary, add/replace one source, strategy, policy, state adapter or output consumer without editing unrelated domain modules.

**Replay/lineage:** Where material, assert source/config/policy IDs and deterministic domain output; do not include current wall-clock metadata in domain-result equivalence.

**Current test assessment:** partially_aligned

**Accepted target(s):** tests/tier_a/normative_authority/test_gate_c_orchestration_playbook_and_risk.py::test_c033_orchestrator_receives_candidate_families_and_registry_as_owned_inputs

**Authority status:** READY / ADMITTED

### C-034 — Execution expression and lifecycle plan

**Normative basis:** 5.7, 5.10-5.11

**Behaviour to prove:** Prove deterministic lead-selection authority, candidate identity, no broker/capital authority, and lifecycle extension through contracts.

**Positive case:** Nominal typed path produces the stated output and preserves owner-issued identity.

**Negative case:** Missing mandatory authority, invalid type, duplicate/conflict or forbidden authority fails with the specified bounded error/withholding behaviour.

**False-positive resistance:** A green test must not pass solely because a model validates, a registry row exists, or a process-memory object can be read in the same process.

**Extension/substitution:** Where this is a volatility boundary, add/replace one source, strategy, policy, state adapter or output consumer without editing unrelated domain modules.

**Replay/lineage:** Where material, assert source/config/policy IDs and deterministic domain output; do not include current wall-clock metadata in domain-result equivalence.

**Current test assessment:** partially_aligned

**Accepted target(s):** tests/tier_a/serial_recommendation/test_execution_service_surface.py; test_serial_transform_boundary_surface.py; test_execution_final_join_boundary.py

**Authority status:** READY / ADMITTED
