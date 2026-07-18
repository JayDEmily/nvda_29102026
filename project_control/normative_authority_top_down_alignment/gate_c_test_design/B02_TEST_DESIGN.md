# Gate C test-design pack — B02

## Acceptance rule

Tests in this pack express the frozen normative propositions and Gate B semantic behaviour. They do not take current code or current test colour as authority. A red result against the untouched alpha implementation is valid Gate C evidence.

## Requirements

### C-008 — Prepared runtime substrate envelope

**Normative basis:** 5.5

**Behaviour to prove:** Define and prove the stable common envelope plus strongly typed payload contracts; require source/capture IDs and schema version without generic-dictionary drift.

**Positive case:** Nominal typed path produces the stated output and preserves owner-issued identity.

**Negative case:** Missing mandatory authority, invalid type, duplicate/conflict or forbidden authority fails with the specified bounded error/withholding behaviour.

**False-positive resistance:** A green test must not pass solely because a model validates, a registry row exists, or a process-memory object can be read in the same process.

**Extension/substitution:** Where this is a volatility boundary, add/replace one source, strategy, policy, state adapter or output consumer without editing unrelated domain modules.

**Replay/lineage:** Where material, assert source/config/policy IDs and deterministic domain output; do not include current wall-clock metadata in domain-result equivalence.

**Current test assessment:** partially_aligned

**Accepted target(s):** tests/tier_a/upstream_cognition/test_prepared_runtime_snapshot_contract_surface.py; tests/tier_a/upstream_cognition/test_prepared_runtime_substrate_surface.py; tests/tier_a/seam_boundaries/test_prepared_ingress_checkpoint_surface.py

**Authority status:** BLOCKED — The exact common prepared-envelope contract remains unresolved.

### C-009 — Stage input bundle

**Normative basis:** 5.5, 5.7

**Behaviour to prove:** Prove mandatory bundle identity, source lineage and policy/config version carriage while preserving typed stage contracts.

**Positive case:** Nominal typed path produces the stated output and preserves owner-issued identity.

**Negative case:** Missing mandatory authority, invalid type, duplicate/conflict or forbidden authority fails with the specified bounded error/withholding behaviour.

**False-positive resistance:** A green test must not pass solely because a model validates, a registry row exists, or a process-memory object can be read in the same process.

**Extension/substitution:** Where this is a volatility boundary, add/replace one source, strategy, policy, state adapter or output consumer without editing unrelated domain modules.

**Replay/lineage:** Where material, assert source/config/policy IDs and deterministic domain output; do not include current wall-clock metadata in domain-result equivalence.

**Current test assessment:** partially_aligned

**Accepted target(s):** tests/tier_a/normative_authority/test_gate_c_ingress_identity_and_dmp.py::test_c009_stage_bundle_carries_common_identity_and_version_metadata_without_widening_payloads

**Authority status:** READY / ADMITTED

### C-010 — DMPV3 boundary placement

**Normative basis:** 5.6; docs/09_DMPV3_PROTOCOL_CORE.md; docs/09.1_DMPV3_PROTOCOL_WORKING.md:15-151

**Behaviour to prove:** Require role-specific mandatory IDs, source artefact lineage and deterministic packet reproduction rules; test that pre-DMP inputs remain non-DMP.

**Positive case:** Nominal typed path produces the stated output and preserves owner-issued identity.

**Negative case:** Missing mandatory authority, invalid type, duplicate/conflict or forbidden authority fails with the specified bounded error/withholding behaviour.

**False-positive resistance:** A green test must not pass solely because a model validates, a registry row exists, or a process-memory object can be read in the same process.

**Extension/substitution:** Where this is a volatility boundary, add/replace one source, strategy, policy, state adapter or output consumer without editing unrelated domain modules.

**Replay/lineage:** Where material, assert source/config/policy IDs and deterministic domain output; do not include current wall-clock metadata in domain-result equivalence.

**Current test assessment:** partially_aligned

**Accepted target(s):** tests/tier_a/normative_authority/test_gate_c_ingress_identity_and_dmp.py::test_c010_c016_dmp_builder_rejects_missing_caller_owned_execution_context_and_lineage

**Authority status:** READY / ADMITTED
