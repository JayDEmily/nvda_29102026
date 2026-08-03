# Test-lineage change

## Preserved proposition

The active-control validator must fail closed unless the live roadmap names either exactly one active ExecPlan or the explicit no-plan state.

## Replaced test node

- Old node: `tests/tier_b/proof_model/test_proof_authority_contract.py::test_active_control_validation_rejects_unreconciled_programme_neutral_route`
- Reason for replacement: the old node required the process overlay to repeat the active ExecPlan path. The revised single-pointer control model intentionally removes that duplicate mutable pointer.
- Governing authority: direct user instruction; `PLANS.md`; `docs/06.1_PROCESS_AND_TRANCHE_LAW_WORKING.md`; `docs/08.1_TESTING_AND_PROMOTION_WORKING.md` proposition `TP-CONTROL-001`.
- Replacement node: `tests/tier_b/proof_model/test_proof_authority_contract.py::test_active_control_validation_rejects_named_inactive_plan`
- Additional fail-closed node: `tests/tier_b/proof_model/test_proof_authority_contract.py::test_active_control_validation_rejects_active_reserved_plan_when_roadmap_is_none`

The behavioural proposition is preserved and strengthened: the roadmap remains the sole active-plan pointer; a named plan must exist and declare active status; the reserved root plan cannot silently become active while the roadmap says `none`.
