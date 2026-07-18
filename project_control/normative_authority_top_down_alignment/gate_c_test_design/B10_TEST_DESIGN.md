# Gate C test-design pack — B10

## Acceptance rule

Tests in this pack express the frozen normative propositions and Gate B semantic behaviour. They do not take current code or current test colour as authority. A red result against the untouched alpha implementation is valid Gate C evidence.

## Requirements

### C-038 — Opening and placement readiness

**Normative basis:** 5.12

**Behaviour to prove:** Prove missing receipt/candidate fails closed, no broker side effect, handoff identity/constraints, and future broker adapter substitution.

**Positive case:** Nominal typed path produces the stated output and preserves owner-issued identity.

**Negative case:** Missing mandatory authority, invalid type, duplicate/conflict or forbidden authority fails with the specified bounded error/withholding behaviour.

**False-positive resistance:** A green test must not pass solely because a model validates, a registry row exists, or a process-memory object can be read in the same process.

**Extension/substitution:** Where this is a volatility boundary, add/replace one source, strategy, policy, state adapter or output consumer without editing unrelated domain modules.

**Replay/lineage:** Where material, assert source/config/policy IDs and deterministic domain output; do not include current wall-clock metadata in domain-result equivalence.

**Current test assessment:** normatively_aligned

**Accepted target(s):** tests/tier_a/downstream_runtime/test_opening_placement_readiness_surface.py; test_opening_authority_boundary_surface.py; test_capital_downstream_placement_boundary.py

**Authority status:** READY / ADMITTED

### C-039 — Paper broker execution lifecycle

**Normative basis:** 5.12-5.13

**Behaviour to prove:** Prove protocol-only invariants, lifecycle idempotency, event ordering and adapter replacement without domain change.

**Positive case:** Nominal typed path produces the stated output and preserves owner-issued identity.

**Negative case:** Missing mandatory authority, invalid type, duplicate/conflict or forbidden authority fails with the specified bounded error/withholding behaviour.

**False-positive resistance:** A green test must not pass solely because a model validates, a registry row exists, or a process-memory object can be read in the same process.

**Extension/substitution:** Where this is a volatility boundary, add/replace one source, strategy, policy, state adapter or output consumer without editing unrelated domain modules.

**Replay/lineage:** Where material, assert source/config/policy IDs and deterministic domain output; do not include current wall-clock metadata in domain-result equivalence.

**Current test assessment:** normatively_aligned

**Accepted target(s):** tests/tier_a/downstream_runtime/test_fwd015_broker_execution_lifecycle_contract.py; tests/tier_a/adapters_egress/test_broker_boundary_surface.py

**Authority status:** READY / ADMITTED

### C-040 — Live position and inventory snapshot

**Normative basis:** 5.13, 5.16

**Behaviour to prove:** Prove authoritative writer/readers, fill idempotency, restart persistence when admitted, and that inventory cannot alter serial outputs except through an explicit later contract.

**Positive case:** Nominal typed path produces the stated output and preserves owner-issued identity.

**Negative case:** Missing mandatory authority, invalid type, duplicate/conflict or forbidden authority fails with the specified bounded error/withholding behaviour.

**False-positive resistance:** A green test must not pass solely because a model validates, a registry row exists, or a process-memory object can be read in the same process.

**Extension/substitution:** Where this is a volatility boundary, add/replace one source, strategy, policy, state adapter or output consumer without editing unrelated domain modules.

**Replay/lineage:** Where material, assert source/config/policy IDs and deterministic domain output; do not include current wall-clock metadata in domain-result equivalence.

**Current test assessment:** partially_aligned

**Accepted target(s):** tests/tier_a/downstream_runtime/test_downstream_live_inventory_service_surface.py; test_live_inventory_authority_boundary_surface.py; test_live_inventory_transform_boundary_surface.py

**Authority status:** READY / ADMITTED
