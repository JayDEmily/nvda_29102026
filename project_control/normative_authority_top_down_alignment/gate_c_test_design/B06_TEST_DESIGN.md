# Gate C test-design pack — B06

## Acceptance rule

Tests in this pack express the frozen normative propositions and Gate B semantic behaviour. They do not take current code or current test colour as authority. A red result against the untouched alpha implementation is valid Gate C evidence.

## Requirements

### C-022 — Bounded SQLite persistence

**Normative basis:** 5.4, 5.16

**Behaviour to prove:** Prove only the intended bounded SQL contract; define separate repository ports before connecting material runtime state.

**Positive case:** Nominal typed path produces the stated output and preserves owner-issued identity.

**Negative case:** Missing mandatory authority, invalid type, duplicate/conflict or forbidden authority fails with the specified bounded error/withholding behaviour.

**False-positive resistance:** A green test must not pass solely because a model validates, a registry row exists, or a process-memory object can be read in the same process.

**Extension/substitution:** Where this is a volatility boundary, add/replace one source, strategy, policy, state adapter or output consumer without editing unrelated domain modules.

**Replay/lineage:** Where material, assert source/config/policy IDs and deterministic domain output; do not include current wall-clock metadata in domain-result equivalence.

**Current test assessment:** implementation_locked

**Accepted target(s):** tests/tier_a/persistence/test_fwd003_durable_sql_contract.py; tests/tier_a/persistence/test_persistence_session_boundary_surface.py

**Authority status:** READY / ADMITTED

### C-023 — In-memory persistence adapters

**Normative basis:** 5.16; docs/04.1_TECHNICAL_ARCHITECTURE_WORKING.md:78-110

**Behaviour to prove:** Create shared repository contract tests that run against memory and future durable adapters, explicitly separating persistence semantics from interface semantics.

**Positive case:** Nominal typed path produces the stated output and preserves owner-issued identity.

**Negative case:** Missing mandatory authority, invalid type, duplicate/conflict or forbidden authority fails with the specified bounded error/withholding behaviour.

**False-positive resistance:** A green test must not pass solely because a model validates, a registry row exists, or a process-memory object can be read in the same process.

**Extension/substitution:** Where this is a volatility boundary, add/replace one source, strategy, policy, state adapter or output consumer without editing unrelated domain modules.

**Replay/lineage:** Where material, assert source/config/policy IDs and deterministic domain output; do not include current wall-clock metadata in domain-result equivalence.

**Current test assessment:** implementation_locked

**Accepted target(s):** tests/tier_a/normative_authority/test_gate_c_state_calendar_and_repositories.py::test_c019_c023_shared_memory_repository_contract_is_copy_safe_and_instance_isolated

**Authority status:** READY / ADMITTED

### C-024 — Receipt and execution record ledgers

**Normative basis:** 5.15-5.16

**Behaviour to prove:** Prove receipt sequencing, idempotency and consistency with state changes at the smallest admitted transaction boundary.

**Positive case:** Nominal typed path produces the stated output and preserves owner-issued identity.

**Negative case:** Missing mandatory authority, invalid type, duplicate/conflict or forbidden authority fails with the specified bounded error/withholding behaviour.

**False-positive resistance:** A green test must not pass solely because a model validates, a registry row exists, or a process-memory object can be read in the same process.

**Extension/substitution:** Where this is a volatility boundary, add/replace one source, strategy, policy, state adapter or output consumer without editing unrelated domain modules.

**Replay/lineage:** Where material, assert source/config/policy IDs and deterministic domain output; do not include current wall-clock metadata in domain-result equivalence.

**Current test assessment:** partially_aligned

**Accepted target(s):** tests/tier_a/persistence/test_receipt_ledger_surface.py; test_execution_records_repository_surface.py; tests/tier_b/proof_model/test_checkpoint_receipt_contract.py

**Authority status:** BLOCKED — The smallest admitted cross-state transaction boundary remains unresolved.
