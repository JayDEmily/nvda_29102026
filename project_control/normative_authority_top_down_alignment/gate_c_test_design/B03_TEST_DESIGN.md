# Gate C test-design pack — B03

## Acceptance rule

Tests in this pack express the frozen normative propositions and Gate B semantic behaviour. They do not take current code or current test colour as authority. A red result against the untouched alpha implementation is valid Gate C evidence.

## Requirements

### C-011 — Raw section canonicalisation

**Normative basis:** 5.5

**Behaviour to prove:** Prove precedence and conflict behaviour, preserve source-section provenance per canonical field, and reject semantic collisions where silent choice is unsafe.

**Positive case:** Nominal typed path produces the stated output and preserves owner-issued identity.

**Negative case:** Missing mandatory authority, invalid type, duplicate/conflict or forbidden authority fails with the specified bounded error/withholding behaviour.

**False-positive resistance:** A green test must not pass solely because a model validates, a registry row exists, or a process-memory object can be read in the same process.

**Extension/substitution:** Where this is a volatility boundary, add/replace one source, strategy, policy, state adapter or output consumer without editing unrelated domain modules.

**Replay/lineage:** Where material, assert source/config/policy IDs and deterministic domain output; do not include current wall-clock metadata in domain-result equivalence.

**Current test assessment:** normative_completion_contract_admitted_expected_red

**Accepted target(s):** tests/tier_a/normative_authority/test_gate_c_normative_completion_contracts.py::test_c011_equal_field_candidates_coalesce_and_preserve_candidate_provenance; tests/tier_a/normative_authority/test_gate_c_normative_completion_contracts.py::test_c011_unequal_mandatory_candidates_without_field_policy_fail_closed

**Authority status:** READY / ADMITTED — N-04 resolved the former normative prerequisite.

### C-012 — Prepared feature derivation

**Normative basis:** 5.5, 5.9

**Behaviour to prove:** Prove derivation version, input provenance and deterministic replay for each material derived field.

**Positive case:** Nominal typed path produces the stated output and preserves owner-issued identity.

**Negative case:** Missing mandatory authority, invalid type, duplicate/conflict or forbidden authority fails with the specified bounded error/withholding behaviour.

**False-positive resistance:** A green test must not pass solely because a model validates, a registry row exists, or a process-memory object can be read in the same process.

**Extension/substitution:** Where this is a volatility boundary, add/replace one source, strategy, policy, state adapter or output consumer without editing unrelated domain modules.

**Replay/lineage:** Where material, assert source/config/policy IDs and deterministic domain output; do not include current wall-clock metadata in domain-result equivalence.

**Current test assessment:** partially_aligned

**Accepted target(s):** tests/tier_a/normative_authority/test_gate_c_ingress_identity_and_dmp.py::test_c012_prepared_lineage_names_material_derivation_versions_and_input_provenance

**Authority status:** READY / ADMITTED

### C-013 — Cognition ingress field mapping

**Normative basis:** 5.5, 5.7

**Behaviour to prove:** Preserve source/bundle identity and schema/policy versions without widening stage-specific payloads.

**Positive case:** Nominal typed path produces the stated output and preserves owner-issued identity.

**Negative case:** Missing mandatory authority, invalid type, duplicate/conflict or forbidden authority fails with the specified bounded error/withholding behaviour.

**False-positive resistance:** A green test must not pass solely because a model validates, a registry row exists, or a process-memory object can be read in the same process.

**Extension/substitution:** Where this is a volatility boundary, add/replace one source, strategy, policy, state adapter or output consumer without editing unrelated domain modules.

**Replay/lineage:** Where material, assert source/config/policy IDs and deterministic domain output; do not include current wall-clock metadata in domain-result equivalence.

**Current test assessment:** normative_completion_contract_admitted_expected_red

**Accepted target(s):** tests/tier_a/normative_authority/test_gate_c_normative_completion_contracts.py::test_c013_stage_bundle_allocates_one_common_context_and_narrow_references; tests/tier_a/normative_authority/test_gate_c_normative_completion_contracts.py::test_c013_stage_bundle_rejects_mismatched_common_context_reference

**Authority status:** READY / ADMITTED — N-05 resolved the former normative prerequisite.
