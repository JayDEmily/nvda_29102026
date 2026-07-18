# Gate C test-design pack — B12

## Acceptance rule

Tests in this pack express the frozen normative propositions and Gate B semantic behaviour. They do not take current code or current test colour as authority. A red result against the untouched alpha implementation is valid Gate C evidence.

## Requirements

### C-043 — Daily P&L reporting

**Normative basis:** 5.15-5.16

**Behaviour to prove:** Prove report derivation/reconciliation, source event IDs, duplicate/idempotent behaviour and explicit non-authoritative alpha status.

**Positive case:** Nominal typed path produces the stated output and preserves owner-issued identity.

**Negative case:** Missing mandatory authority, invalid type, duplicate/conflict or forbidden authority fails with the specified bounded error/withholding behaviour.

**False-positive resistance:** A green test must not pass solely because a model validates, a registry row exists, or a process-memory object can be read in the same process.

**Extension/substitution:** Where this is a volatility boundary, add/replace one source, strategy, policy, state adapter or output consumer without editing unrelated domain modules.

**Replay/lineage:** Where material, assert source/config/policy IDs and deterministic domain output; do not include current wall-clock metadata in domain-result equivalence.

**Current test assessment:** partially_aligned

**Accepted target(s):** tests/tier_a/normative_authority/test_gate_c_outputs_replay_and_api.py::test_c043_daily_pnl_reporting_is_idempotent_by_report_identity_and_preserves_evidence_ids

**Authority status:** READY / ADMITTED

### C-044 — Daily review packet assembly

**Normative basis:** 5.15

**Behaviour to prove:** Prove redaction, explicit missing-material flags, packet/source lineage and no mutation/promotion of runtime authority.

**Positive case:** Nominal typed path produces the stated output and preserves owner-issued identity.

**Negative case:** Missing mandatory authority, invalid type, duplicate/conflict or forbidden authority fails with the specified bounded error/withholding behaviour.

**False-positive resistance:** A green test must not pass solely because a model validates, a registry row exists, or a process-memory object can be read in the same process.

**Extension/substitution:** Where this is a volatility boundary, add/replace one source, strategy, policy, state adapter or output consumer without editing unrelated domain modules.

**Replay/lineage:** Where material, assert source/config/policy IDs and deterministic domain output; do not include current wall-clock metadata in domain-result equivalence.

**Current test assessment:** partially_aligned

**Accepted target(s):** tests/tier_a/review_runtime/test_review_stage_surface.py; test_review_transform_boundary_surface.py; test_fwd018_review_packet_and_slv_replay_contract.py

**Authority status:** READY / ADMITTED

### C-045 — Review explanation

**Normative basis:** 5.15

**Behaviour to prove:** Preserve negative/missing-material tests and add origin validation at the upstream packet-lineage owner, not inside explanation text.

**Positive case:** Nominal typed path produces the stated output and preserves owner-issued identity.

**Negative case:** Missing mandatory authority, invalid type, duplicate/conflict or forbidden authority fails with the specified bounded error/withholding behaviour.

**False-positive resistance:** A green test must not pass solely because a model validates, a registry row exists, or a process-memory object can be read in the same process.

**Extension/substitution:** Where this is a volatility boundary, add/replace one source, strategy, policy, state adapter or output consumer without editing unrelated domain modules.

**Replay/lineage:** Where material, assert source/config/policy IDs and deterministic domain output; do not include current wall-clock metadata in domain-result equivalence.

**Current test assessment:** normatively_aligned

**Accepted target(s):** tests/tier_a/review_runtime/test_review_explanation_service_surface.py; tests/tier_b/review_lineage/test_review_effective_policy_lineage.py

**Authority status:** READY / ADMITTED

### C-046 — Replay comparison

**Normative basis:** 5.15-5.16

**Behaviour to prove:** Define the minimum replay envelope, then test reconstruction from retained authoritative artefacts; retain comparison utility as a subordinate tool.

**Positive case:** Nominal typed path produces the stated output and preserves owner-issued identity.

**Negative case:** Missing mandatory authority, invalid type, duplicate/conflict or forbidden authority fails with the specified bounded error/withholding behaviour.

**False-positive resistance:** A green test must not pass solely because a model validates, a registry row exists, or a process-memory object can be read in the same process.

**Extension/substitution:** Where this is a volatility boundary, add/replace one source, strategy, policy, state adapter or output consumer without editing unrelated domain modules.

**Replay/lineage:** Where material, assert source/config/policy IDs and deterministic domain output; do not include current wall-clock metadata in domain-result equivalence.

**Current test assessment:** partially_aligned

**Accepted target(s):** tests/tier_a/analysis/test_replay_evaluation_surface.py; tests/tier_b/review_replay/test_tranche_a_review_replay.py; tests/tier_b/review_lineage/test_review_replay_dmp_v3_lineage.py

**Authority status:** BLOCKED — The minimum authoritative replay envelope remains unresolved.

### C-047 — Walk-forward and strategic-ladder analysis

**Normative basis:** 5.15

**Behaviour to prove:** Prove analysis-only boundary, dataset/window identity, deterministic ranking and no runtime promotion.

**Positive case:** Nominal typed path produces the stated output and preserves owner-issued identity.

**Negative case:** Missing mandatory authority, invalid type, duplicate/conflict or forbidden authority fails with the specified bounded error/withholding behaviour.

**False-positive resistance:** A green test must not pass solely because a model validates, a registry row exists, or a process-memory object can be read in the same process.

**Extension/substitution:** Where this is a volatility boundary, add/replace one source, strategy, policy, state adapter or output consumer without editing unrelated domain modules.

**Replay/lineage:** Where material, assert source/config/policy IDs and deterministic domain output; do not include current wall-clock metadata in domain-result equivalence.

**Current test assessment:** partially_aligned

**Accepted target(s):** tests/tier_a/normative_authority/test_gate_c_outputs_replay_and_api.py::test_c047_replay_evaluation_requires_dataset_and_window_identity_and_cannot_promote_runtime_authority

**Authority status:** READY / ADMITTED

### C-048 — API and egress composition

**Normative basis:** 5.1, 5.15; modularity law in docs/11.1

**Behaviour to prove:** Split tests by explicit application services/composition ports; prove API cannot invent domain authority or depend on private repository storage.

**Positive case:** Nominal typed path produces the stated output and preserves owner-issued identity.

**Negative case:** Missing mandatory authority, invalid type, duplicate/conflict or forbidden authority fails with the specified bounded error/withholding behaviour.

**False-positive resistance:** A green test must not pass solely because a model validates, a registry row exists, or a process-memory object can be read in the same process.

**Extension/substitution:** Where this is a volatility boundary, add/replace one source, strategy, policy, state adapter or output consumer without editing unrelated domain modules.

**Replay/lineage:** Where material, assert source/config/policy IDs and deterministic domain output; do not include current wall-clock metadata in domain-result equivalence.

**Current test assessment:** partially_aligned

**Accepted target(s):** tests/tier_a/normative_authority/test_gate_c_outputs_replay_and_api.py::test_c021_c048_api_does_not_own_untyped_veto_or_risk_block_state; tests/tier_a/normative_authority/test_gate_c_outputs_replay_and_api.py::test_c041_c048_api_exit_close_path_rejects_missing_upstream_authority_instead_of_fabricating_ids

**Authority status:** READY / ADMITTED
