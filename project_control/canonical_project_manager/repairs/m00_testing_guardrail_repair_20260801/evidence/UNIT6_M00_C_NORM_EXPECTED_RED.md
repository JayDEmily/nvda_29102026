# Unit 6 — M00 C-NORM and Expected-Red C-PROOF

**Outcome:** PASS
**Date:** 2026-08-01
**Branch:** `work/m00-testing-guardrail-repair-v1`
**Baseline commit:** `17e7d653938bfe731089148c48cc9ab8ec52ae04`
**Production implementation:** not started in this unit

## Admitted authority

Architecture authority `M00-FINAL-COMPOSITION-V1` admits nine exact propositions:

- `M00-COMP-001` — exact transport-neutral public seam;
- `M00-COMP-002` — inward dependency direction and public-owner boundaries;
- `M00-COMP-003` — explicit run dependencies, identity, time and policy authority;
- `M00-COMP-004` — canonical M03→M04→M05/M06→M09→M10→M11 paper path;
- `M00-COMP-005` — fail-closed authority and terminal block/no-trade outcomes;
- `M00-COMP-006` — hermetic paper-only fresh execution/lifecycle scope;
- `M00-COMP-007` — immutable aggregate receipt and separate M12 query/replay path;
- `M00-COMP-008` — legacy orchestrator/API mutable owners remain quarantined;
- `M00-COMP-009` — narrow pass-through delegation without semantic reimplementation.

The governed M00 vocabulary admits exactly `ApplicationCommand`, `ApplicationQuery`, `ApplicationRunReceipt` and `RunCoordinator` under namespace `m00`.

## Expected-red proof

The admitted family is `m00_final_composition_contract`, lifecycle `next_gate_expected_red`, proof-block lifecycle `expected_red_c_proof`.

Reference, ordering, failure, query separation and named-mutant challenges:

```text
PYTHONPATH=src .venv/bin/python -m pytest -q \
  tests/tier_a/m00_application_shell/test_m00_application_shell_contract.py \
  -k 'not production_m00_public_seam_exists_and_is_closed'

7 passed, 1 deselected
```

Exact production-seam challenge:

```text
PYTHONPATH=src .venv/bin/python -m pytest -q \
  tests/tier_a/m00_application_shell/test_m00_application_shell_contract.py \
  -k production_m00_public_seam_exists_and_is_closed

1 failed, 7 deselected
ModuleNotFoundError: No module named 'nvda_desk.m00_application_shell'
exit 1
```

Full proof-block execution reached the same truthful state: seven tests passed and the single production import failed for the intentionally absent package. The proof block was corrected to own only extant C-PROOF/normative surfaces; future production files are added to ownership when Unit 7 creates them.

## Authority and vocabulary validation

```text
PYTHONPATH=src .venv/bin/python scripts/build_canonical_vocabulary.py
PASS

PYTHONPATH=src .venv/bin/python -m pytest -q \
  tests/tier_a/vocabulary/test_vocabulary_canonical_builder_parity.py
4 passed

PYTHONPATH=src .venv/bin/python -m pytest -q \
  tests/tier_b/proof_model/test_proof_authority_contract.py
11 passed

PYTHONPATH=src .venv/bin/python scripts/proof_authority.py --check
proof_authority=PASS families=196 tests=198 blocks=67

.venv/bin/python -m black --check \
  tests/support/m00_application_shell_contract_harness.py \
  tests/tier_a/m00_application_shell/test_m00_application_shell_contract.py \
  tests/tier_a/vocabulary/test_vocabulary_canonical_builder_parity.py
PASS

.venv/bin/python -m ruff check \
  tests/support/m00_application_shell_contract_harness.py \
  tests/tier_a/m00_application_shell/test_m00_application_shell_contract.py \
  tests/tier_a/vocabulary/test_vocabulary_canonical_builder_parity.py
PASS

git diff --check
PASS
```

## Gate decision

Unit 6 passes because normative meaning is explicit, the smallest truthful public-seam proof is admitted, all non-production challenges are green, and the only red node is the intentionally missing M00 package. Unit 7 may now implement that seam. No accepted M01–M13 meaning is reopened by this decision.
