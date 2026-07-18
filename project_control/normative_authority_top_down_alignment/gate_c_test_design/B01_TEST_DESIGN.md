# Gate C test-design pack — B01

## Acceptance rule

Tests in this pack express the frozen normative propositions and Gate B semantic behaviour. They do not take current code or current test colour as authority. A red result against the untouched alpha implementation is valid Gate C evidence.

## Requirements

### C-001 — External source interface declaration

**Normative basis:** 5.1; docs/03.1_DOMAIN_MODEL_WORKING.md:13-45; docs/04.1_TECHNICAL_ARCHITECTURE_WORKING.md:13-42

**Behaviour to prove:** Prove every admitted external family either enters through this contract or through an explicitly different source-owned contract; reject fabricated source identity and forbidden authority recursively.

**Positive case:** Nominal typed path produces the stated output and preserves owner-issued identity.

**Negative case:** Missing mandatory authority, invalid type, duplicate/conflict or forbidden authority fails with the specified bounded error/withholding behaviour.

**False-positive resistance:** A green test must not pass solely because a model validates, a registry row exists, or a process-memory object can be read in the same process.

**Extension/substitution:** Where this is a volatility boundary, add/replace one source, strategy, policy, state adapter or output consumer without editing unrelated domain modules.

**Replay/lineage:** Where material, assert source/config/policy IDs and deterministic domain output; do not include current wall-clock metadata in domain-result equivalence.

**Current test assessment:** partially_aligned

**Accepted target(s):** tests/tier_a/normative_authority/test_gate_c_ingress_identity_and_dmp.py::test_c001_c003_market_adapter_enforces_external_source_authority_recursively; tests/tier_a/normative_authority/test_gate_c_ingress_identity_and_dmp.py::test_c001_c003_options_adapter_enforces_external_source_authority_recursively

**Authority status:** READY / ADMITTED

### C-002 — Raw market and options bundle decode

**Normative basis:** 5.2-5.3; docs/04.1_TECHNICAL_ARCHITECTURE_WORKING.md:44-77

**Behaviour to prove:** Require and preserve source/capture identity, test explicit section precedence, test that fallback inference cannot silently misclassify unrelated keys, and prove no cognition bypass.

**Positive case:** Nominal typed path produces the stated output and preserves owner-issued identity.

**Negative case:** Missing mandatory authority, invalid type, duplicate/conflict or forbidden authority fails with the specified bounded error/withholding behaviour.

**False-positive resistance:** A green test must not pass solely because a model validates, a registry row exists, or a process-memory object can be read in the same process.

**Extension/substitution:** Where this is a volatility boundary, add/replace one source, strategy, policy, state adapter or output consumer without editing unrelated domain modules.

**Replay/lineage:** Where material, assert source/config/policy IDs and deterministic domain output; do not include current wall-clock metadata in domain-result equivalence.

**Current test assessment:** partially_aligned

**Accepted target(s):** tests/tier_a/normative_authority/test_gate_c_ingress_identity_and_dmp.py::test_c002_raw_bundle_rejects_untyped_fallback_shape_instead_of_reclassifying_it

**Authority status:** READY / ADMITTED

### C-003 — Market snapshot adapter

**Normative basis:** 5.1, 5.5

**Behaviour to prove:** Prove the adapter composes the authoritative external-source contract and preserves identity/temporal lineage.

**Positive case:** Nominal typed path produces the stated output and preserves owner-issued identity.

**Negative case:** Missing mandatory authority, invalid type, duplicate/conflict or forbidden authority fails with the specified bounded error/withholding behaviour.

**False-positive resistance:** A green test must not pass solely because a model validates, a registry row exists, or a process-memory object can be read in the same process.

**Extension/substitution:** Where this is a volatility boundary, add/replace one source, strategy, policy, state adapter or output consumer without editing unrelated domain modules.

**Replay/lineage:** Where material, assert source/config/policy IDs and deterministic domain output; do not include current wall-clock metadata in domain-result equivalence.

**Current test assessment:** insufficient

**Accepted target(s):** tests/tier_a/normative_authority/test_gate_c_ingress_identity_and_dmp.py::test_c001_c003_market_adapter_enforces_external_source_authority_recursively; tests/tier_a/normative_authority/test_gate_c_ingress_identity_and_dmp.py::test_c001_c003_options_adapter_enforces_external_source_authority_recursively

**Authority status:** READY / ADMITTED

### C-004 — Options surface adapter

**Normative basis:** 5.1, 5.3, 5.5

**Behaviour to prove:** Prove typed options payload identity/version/time carriage or explicitly define why the stage may consume only derived primitives.

**Positive case:** Nominal typed path produces the stated output and preserves owner-issued identity.

**Negative case:** Missing mandatory authority, invalid type, duplicate/conflict or forbidden authority fails with the specified bounded error/withholding behaviour.

**False-positive resistance:** A green test must not pass solely because a model validates, a registry row exists, or a process-memory object can be read in the same process.

**Extension/substitution:** Where this is a volatility boundary, add/replace one source, strategy, policy, state adapter or output consumer without editing unrelated domain modules.

**Replay/lineage:** Where material, assert source/config/policy IDs and deterministic domain output; do not include current wall-clock metadata in domain-result equivalence.

**Current test assessment:** partially_aligned

**Accepted target(s):** tests/tier_a/upstream_cognition/test_cognition_ingress_mapping_surfaces.py; tests/tier_a/upstream_signal/test_raw_signal_transform_boundary_surface.py

**Authority status:** BLOCKED — Exact typed options identity/version/time contract remains unresolved in the frozen corpus.

### C-005 — Financial calendar reference import

**Normative basis:** 5.4; docs/03.1_DOMAIN_MODEL_WORKING.md:17-45

**Behaviour to prove:** Preserve current negative tests and add authoritative fixture(s) proving the adopted calendar layer model once that model is explicitly specified.

**Positive case:** Nominal typed path produces the stated output and preserves owner-issued identity.

**Negative case:** Missing mandatory authority, invalid type, duplicate/conflict or forbidden authority fails with the specified bounded error/withholding behaviour.

**False-positive resistance:** A green test must not pass solely because a model validates, a registry row exists, or a process-memory object can be read in the same process.

**Extension/substitution:** Where this is a volatility boundary, add/replace one source, strategy, policy, state adapter or output consumer without editing unrelated domain modules.

**Replay/lineage:** Where material, assert source/config/policy IDs and deterministic domain output; do not include current wall-clock metadata in domain-result equivalence.

**Current test assessment:** normatively_aligned

**Accepted target(s):** tests/tier_a/calendar_reference/test_calendar_reference_projection_crosswalk.py; tests/tier_a/financial_calendar/test_financial_calendar_authority_surface.py

**Authority status:** BLOCKED — The exact financial-calendar layer model, names and precedence remain unresolved.

### C-006 — Operational calendar and event entry

**Normative basis:** 5.4, 5.16

**Behaviour to prove:** Prove duplicate/identity rules, separation from candidate/sizing authority, and one explicit composition between checked reference projection and operational query state.

**Positive case:** Nominal typed path produces the stated output and preserves owner-issued identity.

**Negative case:** Missing mandatory authority, invalid type, duplicate/conflict or forbidden authority fails with the specified bounded error/withholding behaviour.

**False-positive resistance:** A green test must not pass solely because a model validates, a registry row exists, or a process-memory object can be read in the same process.

**Extension/substitution:** Where this is a volatility boundary, add/replace one source, strategy, policy, state adapter or output consumer without editing unrelated domain modules.

**Replay/lineage:** Where material, assert source/config/policy IDs and deterministic domain output; do not include current wall-clock metadata in domain-result equivalence.

**Current test assessment:** partially_aligned

**Accepted target(s):** tests/tier_a/normative_authority/test_gate_c_state_calendar_and_repositories.py::test_c006_reference_projection_has_one_explicit_owned_composition_into_operational_query_state

**Authority status:** READY / ADMITTED

### C-007 — Raw signal family and market substrate carriers

**Normative basis:** 5.3

**Behaviour to prove:** Prove a new signal family can be added through a registry/adapter without changing unrelated preparation or cognition, and preserve timestamp/source identity.

**Positive case:** Nominal typed path produces the stated output and preserves owner-issued identity.

**Negative case:** Missing mandatory authority, invalid type, duplicate/conflict or forbidden authority fails with the specified bounded error/withholding behaviour.

**False-positive resistance:** A green test must not pass solely because a model validates, a registry row exists, or a process-memory object can be read in the same process.

**Extension/substitution:** Where this is a volatility boundary, add/replace one source, strategy, policy, state adapter or output consumer without editing unrelated domain modules.

**Replay/lineage:** Where material, assert source/config/policy IDs and deterministic domain output; do not include current wall-clock metadata in domain-result equivalence.

**Current test assessment:** partially_aligned

**Accepted target(s):** tests/tier_a/upstream_signal/test_fwd007_raw_signal_family_rebuild_contract.py; tests/tier_a/upstream_signal/test_raw_signal_contract_copy_boundaries.py; tests/tier_a/upstream_signal/test_upstream_signal_coverage_map_and_scope_lock.py

**Authority status:** READY / ADMITTED
