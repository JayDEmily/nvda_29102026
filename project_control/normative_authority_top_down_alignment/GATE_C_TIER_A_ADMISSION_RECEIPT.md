# Gate C Tier A Admission Receipt

## Decision

The five files under `tests/tier_a/normative_authority/` are explicitly admitted as **Tier A blocking proof for this active ExecPlan**. Their tier does not arise from directory placement. The admission authority is the user-authorised active programme, the Gate C test-authority register, this receipt and `GATE_C_TIER_A_PROMOTION_MANIFEST.tsv`, operating within `docs/08_TESTING_AND_PROMOTION_CORE.md`, `docs/08.1_TESTING_AND_PROMOTION_WORKING.md`, `config/retained_test_registry.yaml` and `config/proof_blocks.yaml`.

The central retained-test registry and proof-block manifest remain unchanged because both repository test law and the registry permit bounded active-pack authority. This receipt is that bounded authority.

## Exact admitted files

1. `tests/tier_a/normative_authority/test_gate_c_ingress_identity_and_dmp.py`
2. `tests/tier_a/normative_authority/test_gate_c_orchestration_playbook_and_risk.py`
3. `tests/tier_a/normative_authority/test_gate_c_outputs_replay_and_api.py`
4. `tests/tier_a/normative_authority/test_gate_c_remaining_normative_contracts.py`
5. `tests/tier_a/normative_authority/test_gate_c_state_calendar_and_repositories.py`

These files directly represent 34 ready Gate C requirements. Four additional ready requirements—`C-028`, `C-038`, `C-039` and `C-045`—remain proven solely by previously admitted Tier A/Tier B families recorded in `GATE_C_TEST_AUTHORITY_REGISTER.tsv`. Ten requirements remain blocked by missing normative authority and are not admitted through this receipt.

## Aggregate command

```bash
env PYTHONPATH=src python -m pytest \
  tests/tier_a/normative_authority/test_gate_c_ingress_identity_and_dmp.py \
  tests/tier_a/normative_authority/test_gate_c_orchestration_playbook_and_risk.py \
  tests/tier_a/normative_authority/test_gate_c_outputs_replay_and_api.py \
  tests/tier_a/normative_authority/test_gate_c_remaining_normative_contracts.py \
  tests/tier_a/normative_authority/test_gate_c_state_calendar_and_repositories.py
```

This command is the bounded aggregate for the five-file Gate C normative slice. It is not, by itself, the complete repository promotion gate for a later implementation claim. Each Gate D proof envelope must also name all existing Tier A dependants and Tier B shadow evidence for its touched surface.

## Expected-red semantics

A red assertion in this slice is blocking proof for the linked implementation unit. It does not invalidate Gate C when the assertion truthfully captures an implementation gap already recorded in `RED_GREEN_EVIDENCE.tsv`. It may not be weakened, skipped, reclassified or edited during Gate D merely to obtain green status.

## False-positive protection

The admission covers both positive behaviour and explicit anti-authority/false-positive constraints. In particular, the files prohibit nested external trading authority, silent untyped reclassification, fabricated execution identity, cross-instance state leakage, API-owned untyped risk state, duplicate evidence application and analysis/review promotion into runtime authority.

## Frozen test surface

Gate C2 grants no assertion or fixture mutation authority. If a later implementation unit exposes a contradiction between this admitted proof and another Tier A family, that unit returns to Gate C2 for explicit authority disposition. Production code must not be changed to satisfy two contradictory test authorities.
