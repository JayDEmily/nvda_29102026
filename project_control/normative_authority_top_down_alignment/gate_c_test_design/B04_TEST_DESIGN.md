# Gate C test-design pack — B04

## Acceptance rule

Tests in this pack express the frozen normative propositions and Gate B semantic behaviour. They do not take current code or current test colour as authority. A red result against the untouched alpha implementation is valid Gate C evidence.

## Requirements

### C-014 — Source, capture, domain and packet identity distinction

**Normative basis:** docs/03.1_DOMAIN_MODEL_WORKING.md:25-45; docs/04.1_TECHNICAL_ARCHITECTURE_WORKING.md:13-42; docs/09.1_DMPV3_PROTOCOL_WORKING.md:15-61

**Behaviour to prove:** Create an identifier-role matrix in tests: owner, mandatory/optional status, propagation and forbidden fabrication for every material ID.

**Positive case:** Nominal typed path produces the stated output and preserves owner-issued identity.

**Negative case:** Missing mandatory authority, invalid type, duplicate/conflict or forbidden authority fails with the specified bounded error/withholding behaviour.

**False-positive resistance:** A green test must not pass solely because a model validates, a registry row exists, or a process-memory object can be read in the same process.

**Extension/substitution:** Where this is a volatility boundary, add/replace one source, strategy, policy, state adapter or output consumer without editing unrelated domain modules.

**Replay/lineage:** Where material, assert source/config/policy IDs and deterministic domain output; do not include current wall-clock metadata in domain-result equivalence.

**Current test assessment:** insufficient

**Accepted target(s):** tests/tier_a/temporal/test_fwd006_reopened_row_raw_capture_source_temporal_proof.py; tests/tier_a/packets/test_parallel_risk_lineage_completeness.py; tests/tier_b/review_lineage/test_review_replay_dmp_v3_lineage.py

**Authority status:** READY / ADMITTED

### C-015 — Prepared lineage record

**Normative basis:** 5.2, 5.5, 5.15-5.16

**Behaviour to prove:** Require source artefact IDs/fingerprint and preparation policy/schema versions; prove detached copy and replay equivalence.

**Positive case:** Nominal typed path produces the stated output and preserves owner-issued identity.

**Negative case:** Missing mandatory authority, invalid type, duplicate/conflict or forbidden authority fails with the specified bounded error/withholding behaviour.

**False-positive resistance:** A green test must not pass solely because a model validates, a registry row exists, or a process-memory object can be read in the same process.

**Extension/substitution:** Where this is a volatility boundary, add/replace one source, strategy, policy, state adapter or output consumer without editing unrelated domain modules.

**Replay/lineage:** Where material, assert source/config/policy IDs and deterministic domain output; do not include current wall-clock metadata in domain-result equivalence.

**Current test assessment:** partially_aligned

**Accepted target(s):** tests/tier_a/normative_authority/test_gate_c_ingress_identity_and_dmp.py::test_c012_prepared_lineage_names_material_derivation_versions_and_input_provenance

**Authority status:** READY / ADMITTED

### C-016 — Serial packet lineage chain

**Normative basis:** 5.6-5.7; docs/09.1_DMPV3_PROTOCOL_WORKING.md:104-151

**Behaviour to prove:** Prove required sourceartifactids, supplied execution context IDs, deterministic domain outputs independent of emitted_at, and exact dependency semantics.

**Positive case:** Nominal typed path produces the stated output and preserves owner-issued identity.

**Negative case:** Missing mandatory authority, invalid type, duplicate/conflict or forbidden authority fails with the specified bounded error/withholding behaviour.

**False-positive resistance:** A green test must not pass solely because a model validates, a registry row exists, or a process-memory object can be read in the same process.

**Extension/substitution:** Where this is a volatility boundary, add/replace one source, strategy, policy, state adapter or output consumer without editing unrelated domain modules.

**Replay/lineage:** Where material, assert source/config/policy IDs and deterministic domain output; do not include current wall-clock metadata in domain-result equivalence.

**Current test assessment:** partially_aligned

**Accepted target(s):** tests/tier_a/normative_authority/test_gate_c_ingress_identity_and_dmp.py::test_c010_c016_dmp_builder_rejects_missing_caller_owned_execution_context_and_lineage; tests/tier_a/normative_authority/test_gate_c_ingress_identity_and_dmp.py::test_c016_dmp_domain_content_is_reproducible_when_process_metadata_is_explicit

**Authority status:** READY / ADMITTED

### C-017 — Parallel Risk packet lineage

**Normative basis:** 5.8; docs/07.1_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_WORKING.md:163-171

**Behaviour to prove:** Require input/parent/dependency/source IDs at admitted runtime boundaries and prove no serial outputs other than declared inputs influence the lane.

**Positive case:** Nominal typed path produces the stated output and preserves owner-issued identity.

**Negative case:** Missing mandatory authority, invalid type, duplicate/conflict or forbidden authority fails with the specified bounded error/withholding behaviour.

**False-positive resistance:** A green test must not pass solely because a model validates, a registry row exists, or a process-memory object can be read in the same process.

**Extension/substitution:** Where this is a volatility boundary, add/replace one source, strategy, policy, state adapter or output consumer without editing unrelated domain modules.

**Replay/lineage:** Where material, assert source/config/policy IDs and deterministic domain output; do not include current wall-clock metadata in domain-result equivalence.

**Current test assessment:** partially_aligned

**Accepted target(s):** tests/tier_a/normative_authority/test_gate_c_orchestration_playbook_and_risk.py::test_c017_parallel_risk_bootstrap_rejects_missing_upstream_identity_and_lineage

**Authority status:** READY / ADMITTED
