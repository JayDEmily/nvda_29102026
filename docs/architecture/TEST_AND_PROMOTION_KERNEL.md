# Test and Promotion Kernel

## Normative propositions

- **AK-PROOF-001 — Exact proof admission.** Every physical architecture/bootstrap test has one exact admitted path, tier, lifecycle, proposition set, proof block and promotion-set disposition. Folder placement and textual proposition IDs do not create proof authority.
- **AK-PROOF-002 — Registry-derived aggregate gate.** The blocking architecture promotion set is derived from admitted proof configuration and executes every current blocking proof block. A green result proves only the propositions actually exercised by those tests in that environment.

## Tier and lifecycle

Tier and lifecycle are independent:

- Tier A — blocking proof for a current admitted architecture proposition;
- Tier B — bounded current shadow proof;
- Tier C — historical, observational, slow or operational assurance.

Lifecycle values are `current_blocking`, `current_nonblocking` and `historical`. File location does not create authority.

## Physical-test admission

Every physical `test_*.py` file anywhere beneath the admitted architecture/bootstrap test jurisdictions must have exactly one family admission, including nested directories. Every admitted path must resolve to exactly one physical file.

Proof blocks select family identifiers only. Test paths are derived from the family registry; a second independent path list is prohibited.

## Proposition traceability

A family may cite only existing normative proposition identifiers. Mechanical occurrence of an identifier establishes addressability/binding only. It does not establish that the test semantically entails or completely proves the proposition.

The human/reviewer proof question remains: do the assertions and exercised path actually bear on the claimed proposition at the required proof level?

## Aggregate gate

`architecture_kernel` is the blocking architecture promotion-set identifier unless current accepted proof authority explicitly replaces it. The repository-owned runner validates registries/schemas, resolves exact family/block membership, executes all blocking proof and fails closed on missing, red or inconsistent proof.

The aggregate does not establish future domain semantics, implementation maturity or operational fitness merely by being green.
