# Test and Promotion Kernel

## Tier and lifecycle

Tier and lifecycle are independent:

- Tier A — blocking proof for the current architecture-kernel claim;
- Tier B — bounded current shadow proof;
- Tier C — historical, observational, slow or operational assurance.

Current initial lifecycle values are `current_blocking`, `current_nonblocking` and `historical`. Folder placement does not create authority.

## Admission

Every admitted family records exact path, tier, lifecycle, normative proposition identifiers, owning proof block and promotion-set membership. Every physical `test_*.py` file under `tests/architecture` and `tests/bootstrap` must have exactly one admission.

Proof blocks select family identifiers only. Test paths are derived from the family registry; a second independent path list is prohibited.

## Aggregate gate

`architecture_kernel` is the sole current blocking promotion set. The repository-owned runner validates registries and schemas, resolves exact family and block membership, executes all blockers, records outcomes and fails closed on missing, red or inconsistent proof.

A passing gate proves only the architecture-kernel propositions named by its admitted families. It does not establish future domain semantics or implementation maturity.
