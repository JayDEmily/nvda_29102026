# Gate C test-design pack — B07

## Acceptance rule

Tests in this pack express the frozen normative propositions and Gate B semantic behaviour. They do not take current code or current test colour as authority. A red result against the untouched alpha implementation is valid Gate C evidence.

## Requirements

### C-025 — Temporal context evaluation

**Normative basis:** 5.2, 5.4, 5.7

**Behaviour to prove:** Preserve current source-time/timezone tests and add policy/version tests for the accepted temporal classifier.

**Positive case:** Nominal typed path produces the stated output and preserves owner-issued identity.

**Negative case:** Missing mandatory authority, invalid type, duplicate/conflict or forbidden authority fails with the specified bounded error/withholding behaviour.

**False-positive resistance:** A green test must not pass solely because a model validates, a registry row exists, or a process-memory object can be read in the same process.

**Extension/substitution:** Where this is a volatility boundary, add/replace one source, strategy, policy, state adapter or output consumer without editing unrelated domain modules.

**Replay/lineage:** Where material, assert source/config/policy IDs and deterministic domain output; do not include current wall-clock metadata in domain-result equivalence.

**Current test assessment:** partially_aligned

**Accepted target(s):** tests/tier_a/normative_authority/test_gate_c_orchestration_playbook_and_risk.py::test_c025_c027_temporal_and_regime_outputs_carry_the_policy_versions_that_define_them

**Authority status:** READY / ADMITTED

### C-026 — Signal-informed intraday phase interpretation

**Normative basis:** Direct user architecture instruction 2026-07-17; frozen surfaces 5.2, 5.4, 5.7; detailed algorithm remains absent from normative corpus

**Behaviour to prove:** PREREQUISITE: create a numbered normative addendum defining phase inputs, transition semantics, state/history, versioning and graceful degradation; then write signal-path and anti-clock-cutoff tests.

**Positive case:** Nominal typed path produces the stated output and preserves owner-issued identity.

**Negative case:** Missing mandatory authority, invalid type, duplicate/conflict or forbidden authority fails with the specified bounded error/withholding behaviour.

**False-positive resistance:** A green test must not pass solely because a model validates, a registry row exists, or a process-memory object can be read in the same process.

**Extension/substitution:** Where this is a volatility boundary, add/replace one source, strategy, policy, state adapter or output consumer without editing unrelated domain modules.

**Replay/lineage:** Where material, assert source/config/policy IDs and deterministic domain output; do not include current wall-clock metadata in domain-result equivalence.

**Current test assessment:** misleading

**Accepted target(s):** Current temporal tests cover fixed thresholds; no admitted test proves signal-driven phase transition.

**Authority status:** BLOCKED — Signal-informed intraday phase inputs, transitions, history and versioning require a numbered normative addendum.

### C-027 — Market regime classification

**Normative basis:** 5.7

**Behaviour to prove:** Prove current bounded classifier exactly, unknown handling and policy-version carriage; do not inflate scope until normative requirements expand.

**Positive case:** Nominal typed path produces the stated output and preserves owner-issued identity.

**Negative case:** Missing mandatory authority, invalid type, duplicate/conflict or forbidden authority fails with the specified bounded error/withholding behaviour.

**False-positive resistance:** A green test must not pass solely because a model validates, a registry row exists, or a process-memory object can be read in the same process.

**Extension/substitution:** Where this is a volatility boundary, add/replace one source, strategy, policy, state adapter or output consumer without editing unrelated domain modules.

**Replay/lineage:** Where material, assert source/config/policy IDs and deterministic domain output; do not include current wall-clock metadata in domain-result equivalence.

**Current test assessment:** partially_aligned

**Accepted target(s):** tests/tier_a/normative_authority/test_gate_c_orchestration_playbook_and_risk.py::test_c025_c027_temporal_and_regime_outputs_carry_the_policy_versions_that_define_them

**Authority status:** READY / ADMITTED

### C-028 — Options-flow surface classification

**Normative basis:** 5.7

**Behaviour to prove:** Prove honest unknowns and isolation; future richer flow must enter through versioned contracts rather than changing unrelated stages.

**Positive case:** Nominal typed path produces the stated output and preserves owner-issued identity.

**Negative case:** Missing mandatory authority, invalid type, duplicate/conflict or forbidden authority fails with the specified bounded error/withholding behaviour.

**False-positive resistance:** A green test must not pass solely because a model validates, a registry row exists, or a process-memory object can be read in the same process.

**Extension/substitution:** Where this is a volatility boundary, add/replace one source, strategy, policy, state adapter or output consumer without editing unrelated domain modules.

**Replay/lineage:** Where material, assert source/config/policy IDs and deterministic domain output; do not include current wall-clock metadata in domain-result equivalence.

**Current test assessment:** normatively_aligned

**Accepted target(s):** tests/tier_a/options_flow_history/test_options_flow_contract_models.py; tests/tier_b/serial_boundaries/test_options_flow_output_contract_isolation.py

**Authority status:** READY / ADMITTED

### C-029 — Posture and risk-permission stage

**Normative basis:** 5.7, 5.9

**Behaviour to prove:** Prove baseline/effective values, modifier precedence, immutable authority version/fingerprint and no policy smuggling.

**Positive case:** Nominal typed path produces the stated output and preserves owner-issued identity.

**Negative case:** Missing mandatory authority, invalid type, duplicate/conflict or forbidden authority fails with the specified bounded error/withholding behaviour.

**False-positive resistance:** A green test must not pass solely because a model validates, a registry row exists, or a process-memory object can be read in the same process.

**Extension/substitution:** Where this is a volatility boundary, add/replace one source, strategy, policy, state adapter or output consumer without editing unrelated domain modules.

**Replay/lineage:** Where material, assert source/config/policy IDs and deterministic domain output; do not include current wall-clock metadata in domain-result equivalence.

**Current test assessment:** partially_aligned

**Accepted target(s):** tests/tier_a/modifiers/test_state_conditioned_modifier_surface.py; tests/tier_b/serial_boundaries/test_posture_permission_envelope.py

**Authority status:** READY / ADMITTED

### C-030 — Dynamic coefficient authority

**Normative basis:** 5.9

**Behaviour to prove:** Prove substitution of coefficient documents/policies without changing consumers, carry document fingerprint/version, and keep execution modifiers fail-closed until admitted.

**Positive case:** Nominal typed path produces the stated output and preserves owner-issued identity.

**Negative case:** Missing mandatory authority, invalid type, duplicate/conflict or forbidden authority fails with the specified bounded error/withholding behaviour.

**False-positive resistance:** A green test must not pass solely because a model validates, a registry row exists, or a process-memory object can be read in the same process.

**Extension/substitution:** Where this is a volatility boundary, add/replace one source, strategy, policy, state adapter or output consumer without editing unrelated domain modules.

**Replay/lineage:** Where material, assert source/config/policy IDs and deterministic domain output; do not include current wall-clock metadata in domain-result equivalence.

**Current test assessment:** partially_aligned

**Accepted target(s):** tests/tier_a/config/test_sequence8_coefficient_modifier_authority_specimen.py; test_coefficient_modifier_replay_surface.py; tests/tier_a/modifiers/test_dynamic_modifier_transform_boundary_surface.py

**Authority status:** READY / ADMITTED

### C-031 — Six-stage serial runtime orchestration

**Normative basis:** 5.7; docs/05.1_GUARDRAILS_WORKING.md fail-closed law

**Behaviour to prove:** Separate explicit inspection API from governed run_once; fail closed on invalid execution input; supply candidate families through an owned contract; make domain replay independent of wall clock.

**Positive case:** Nominal typed path produces the stated output and preserves owner-issued identity.

**Negative case:** Missing mandatory authority, invalid type, duplicate/conflict or forbidden authority fails with the specified bounded error/withholding behaviour.

**False-positive resistance:** A green test must not pass solely because a model validates, a registry row exists, or a process-memory object can be read in the same process.

**Extension/substitution:** Where this is a volatility boundary, add/replace one source, strategy, policy, state adapter or output consumer without editing unrelated domain modules.

**Replay/lineage:** Where material, assert source/config/policy IDs and deterministic domain output; do not include current wall-clock metadata in domain-result equivalence.

**Current test assessment:** misleading

**Accepted target(s):** tests/tier_a/normative_authority/test_gate_c_orchestration_playbook_and_risk.py::test_c031_governed_run_once_rejects_structurally_invalid_stage_mapping

**Authority status:** READY / ADMITTED
