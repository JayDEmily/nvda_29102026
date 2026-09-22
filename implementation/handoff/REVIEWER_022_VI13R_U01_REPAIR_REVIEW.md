# Reviewer 022 — VI-13R U01 bounded repair re-review

## Assignment

Act as the fresh independent VI-13R reviewer for the repaired **IWO-U01 only**. Review the exact
repaired candidate against current authority, Reviewer 021's four findings, and the bounded U01
proof. Return `PASS`, `FAIL / RETURN_TO_WORKER`, or `BLOCKED`. Do not begin or assess U02.

## Exact target

- accepted forward `main` before U01 remains `95c0aeabf3b76316bd32870ffe6c311be8ad1237`;
- rejected first U01 production candidate: `d14190cdfe845fdd60629ca9b1eed8d1d2704d44`;
- Reviewer 021 fail commit: `1637f39980aa3ca476429d85e267a9cb0e575fe5`;
- repaired Worker branch: `work/vi12r-u01-reviewer021-repair`;
- repaired candidate: `e8b659d7849d2f95b64ba32bed8090a8290358d4` / tree
  `62b074c0e94215a75fb64c5eb934af55be1ded3a`;
- Worker repair evidence: `implementation/proof/VI12R_U01_REVIEWER021_REPAIR_EVIDENCE.md`.

Bind the supplied archive separately by SHA-256 after transport verification.

## Mandatory read order

1. `GUARDRAILS.md` in full;
2. root `AGENTS.md` in full;
3. current `EXEC_PLAN.md` in full, especially 6.3-6.4C, 6.7, VI-12R and VI-13R;
4. `tests/AGENTS.override.md`;
5. `handoff/authority/IRB_ACCEPTED_IMPLEMENTATION_BRIEF.md` in full;
6. `implementation/work_order/VI05_IMPLEMENTATION_WORK_ORDER_CANDIDATE_001.md`, especially U01;
7. `implementation/proof/VI13R_U01_REVIEWER_021_DISPOSITION.md`;
8. `implementation/proof/VI12R_U01_REVIEWER021_REPAIR_EVIDENCE.md`;
9. complete diff `1637f39980aa3ca476429d85e267a9cb0e575fe5..e8b659d7849d2f95b64ba32bed8090a8290358d4`
   and complete current `src/nvda_desk/raw_signal_occurrence_truth/api.py`;
10. complete U01 proof and positive/negative typecheck specimens.

## Required four-finding disposition

Independently establish whether each exact Reviewer-021 finding is closed:

1. `W-U01-F001` — lawful `receipt_only` positive construction is coherent while non-absent
   provider timestamp remains rejected;
2. `W-U01-F002` — relative/absolute mypy paths are normalised and all 15 static-negative sites
   are still required and diagnosed;
3. `R021-U01-F003` — `native_record` cannot be altered after construction through caller alias,
   nested caller alias, returned nested value, or direct payload mapping mutation, without changing
   provider-native value/null meaning;
4. `R021-U01-F004` — A00 can construct every required identity-bearing U01 payload through only
   declared public API symbols, with runtime/static identity separation preserved.

Challenge the realised repair for concrete U01 defects. Apply the bounded-proof methodology: do
not reopen an implementation-independent search for arbitrary hypothetical future escapes.

## Environment / execution

Perform the current bounded preflight. U01 does not require PostgreSQL or namespace setup. Where
available, run at least:

```text
python --version
python -m pytest --version
python -m mypy --version
python -m ruff --version
python -m pytest -q tests/product/raw_signal/test_u01_contract_owner_boundary.py
python -m mypy --strict --disallow-any-expr --show-error-codes --no-error-summary tests/product/raw_signal/typecheck/public_seam_positive.py
python -m mypy --strict --disallow-any-expr --show-error-codes --no-error-summary tests/product/raw_signal/typecheck/public_seam_negative.py
python -m mypy src --show-error-codes
python -m ruff check src tests tools
python tools/validate_product_proof.py
python tools/validate_architecture.py
python tools/check_dependencies.py
python tools/check_public_seams.py
python tools/run_promotion_gate.py --set architecture_kernel
git diff --check
git fsck --full --strict
```

The negative mypy specimen is expected to return non-zero; establish that all 15 marked negative
sites are diagnosed. Do not interpret that expected non-zero as a review failure.

## Verdict law

- `PASS` only if all four Reviewer-021 findings are closed, no new material U01 defect remains,
  and the repaired candidate still implements U01 only.
- `FAIL / RETURN_TO_WORKER` for a concrete remaining U01 implementation/proof defect; identify the
  exact defeated proposition, owning layer and smallest repair.
- `BLOCKED` only when required U01 evidence cannot be obtained.

Record the independent disposition in Git and return a full-Git TAR. State explicitly whether U02
is authorised after lawful U01 promotion or remains prohibited.
