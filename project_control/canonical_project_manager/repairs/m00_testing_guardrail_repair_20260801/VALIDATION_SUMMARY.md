# M00 Testing Guardrail Repair — Validation Summary

## Unit 1 — Admission authority

**Outcome:** PASS

Known true:

- `config/retained_test_registry.yaml` parses as schema `v4`.
- Its canonical admission model covers all 195 physical `test_*.py` files under Tier A/B/C exactly once.
- Lifecycle totals are 13 current-blocking families, 38 current-nonblocking families, 6 next-gate expected-red families, 63 superseded-compatibility families and 73 historical families.
- The 13 current-blocking module families resolve to exactly 15 physical tests.
- `config/proof_blocks.yaml` parses as schema `v2`; `pre_m00_current` selects those 13 families through 13 proof blocks, with no duplicate family or path membership.
- Every selected block has an exact accepted normative proposition identifier or locator.
- The authority validator rejects duplicate paths, invalid tiers, invalid lifecycles, unknown family references, command/registry membership disagreement and missing proposition locators.

Validation evidence:

```text
python scripts/proof_authority.py --check
proof_authority=PASS families=193 tests=195 blocks=64

python -m pytest tests/tier_b/proof_model/test_proof_authority_contract.py -q
8 passed

python scripts/run_proof_block.py --check-all
proof_blocks_check_all=PASS count=64

python -m pytest tests/tier_b/proof_model/test_proof_executor_contract.py::test_proof_executor_emits_block_header_before_child_output tests/tier_b/proof_model/test_proof_executor_contract.py::test_proof_executor_runs_manifest_commands_without_shell_evaluation tests/tier_b/proof_model/test_checkpoint_receipt_contract.py -q
4 passed

git diff --check
PASS (no output)
```

The complete legacy proof-executor contract was also exercised through 19 of 21 cases in one run before the external 300-second command limit; the final two cases were rerun explicitly and passed. This is recorded as segmented proof rather than represented as one uninterrupted suite result.

## Open next gate

Unit 2: reconcile the single active control state and make the current/legacy API test lifecycles explicit and non-conflicting.

## Unit 2 — Current control and API authority reconciliation

**Outcome:** PASS

Known true:

- Canonical ExecPlan, live roadmap and process overlay identify one active control pack: `PRE-M00-TESTING-GUARDRAIL-REPAIR-V1`.
- The stale M12 active-pack declaration is now retained only as historical programme evidence; it no longer claims current control.
- `tests/tier_a/api/test_fwd005_api_exposure_contract.py` is explicitly `superseded_compatibility` because it requires API-owned mutable CRUD and authority-event state.
- `tests/tier_a/normative_authority/test_gate_c_outputs_replay_and_api.py` is explicitly `next_gate_expected_red` and excluded from the current green claim until its gate opens.
- The registry contains an exclusive `api_state_ownership` claim group. Validation fails if both contradictory families are activated.

Validation evidence:

```text
python -m pytest tests/tier_b/proof_model/test_proof_authority_contract.py -q
11 passed

python scripts/proof_authority.py --check
proof_authority=PASS families=193 tests=195 blocks=64

git diff --check
PASS (no output)
```

## Open next gate

Unit 3: implement the aggregate promotion executor and sufficient tamper-evident receipts.
