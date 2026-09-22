# Reviewer 021 — VI-13R U01 implementation-coupled review

## Assignment

Act as the fresh independent VI-13R reviewer for **IWO-U01 only**. Review the actual first
production candidate against exact authority and the already-accepted bounded contract. Return
`PASS`, `FAIL / RETURN_TO_WORKER`, or `BLOCKED` for U01. Do not begin U02.

This is the first post-implementation review under the current ExecPlan's bounded proof sequencing.
The task is not to re-open an implementation-independent hunt for arbitrary hypothetical future
objects. Challenge the actual U01 candidate and any proof discriminator that bears on it.

## Exact target

- accepted forward `main` before U01: `95c0aea`;
- Worker branch: `work/vi12r-u01-contract-owner-boundary`;
- production candidate commit: `d14190cdfe845fdd60629ca9b1eed8d1d2704d44`;
- production candidate tree: `00f036fcd22a6e3ec6f79c5ddfeb9d210d1418b9`;
- production changed path: `src/nvda_desk/raw_signal_occurrence_truth/api.py` only;
- Worker evidence: `implementation/proof/VI12R_U01_IMPLEMENTATION_EVIDENCE.md` in the handoff
  successor commit that carries this assignment.

Bind the review separately to the supplied full-Git archive SHA-256 after transport verification.
Do not infer repository identity from the archive filename.

## Mandatory read order

Before substantive review:

1. root `GUARDRAILS.md` in full;
2. root `AGENTS.md` in full;
3. root `EXEC_PLAN.md` in full, especially sections 6.3-6.4C, 6.7, 6.10, VI-12R and VI-13R;
4. `tests/AGENTS.override.md`;
5. `handoff/authority/IRB_ACCEPTED_IMPLEMENTATION_BRIEF.md` in full;
6. `handoff/authority/BICP_CANDIDATE_005.md` and `.json` as needed to bind the accepted packet;
7. `implementation/work_order/VI05_IMPLEMENTATION_WORK_ORDER_CANDIDATE_001.md`, especially U01;
8. `implementation/proof/VI12R_U01_IMPLEMENTATION_EVIDENCE.md`;
9. the complete U01 production diff and complete current
   `src/nvda_desk/raw_signal_occurrence_truth/api.py`;
10. the complete U01 proof file and its support/typecheck specimens.

## U01 review proposition

Determine whether the exact candidate faithfully implements **IWO-U01 and only IWO-U01**:

- exact five canonical concepts / five `.v1` contracts;
- distinct identity layers and no cross-layer substitution;
- structural absence versus provider-native null;
- exact finite temporal/relation/assessment discriminants;
- BC-005 receipt-only/source-timestamp law without invented timezone/event time;
- M-owned typed command/read boundary with A00-only consumer direction preserved;
- public seam shape sufficient for later units;
- no schedule generation, provider mapping, persistence, replay, packet carriage or downstream
  capability implemented early.

Inspect actual code, not only test outcomes. Look for hidden defaults, identity collapse, mutable
state, semantic widening, acceptance of invalid values, inferred source/market time, forbidden
capability activation, or a typed seam that can be bypassed materially within the current U01
public contract.

## Mandatory disposition of Worker-observed discrepancies

Independently reproduce and classify both findings; do not accept the Worker's classification by
assertion.

### W-U01-F001 — receipt-only test contradiction

Check the default observation specimen, the parametrised discriminant-acceptance test, the explicit
temporal null-law test, and IRB BC-005/BC-009. Decide whether the failing `receipt_only` case is a
production defect or a proof-harness contradiction. If proof repair is required, identify the
smallest repair that preserves the accepted law; do not weaken receipt-only timestamp absence.

### W-U01-F002 — mypy diagnostic path parser

Run the exact negative specimen under repository-configured Python and pinned mypy. Confirm whether
all 15 intended `STATIC_NEGATIVE` substitutions actually produce type errors and whether the
pytest failure is solely the parser's absolute-versus-relative path assumption. If proof repair is
required, preserve the requirement that all 15 negative sites are diagnosed; do not weaken or
remove the static negative proof.

## Environment / execution control

Perform the bounded preflight required by ExecPlan 6.4B. U01 itself does not require PostgreSQL,
namespace isolation or persistence execution. Do not create a PostgreSQL environment merely for
this U01 review.

At minimum, where available and proposition-bearing:

```text
python --version
python -m pytest --version
python -m mypy --version
python -m ruff --version
python -m pytest -q tests/product/raw_signal/test_u01_contract_owner_boundary.py
python -m mypy --strict --disallow-any-expr --show-error-codes --no-error-summary \
  tests/product/raw_signal/typecheck/public_seam_positive.py
python -m mypy --strict --disallow-any-expr --show-error-codes --no-error-summary \
  tests/product/raw_signal/typecheck/public_seam_negative.py
python -m mypy src --show-error-codes
python -m ruff check src tests tools
python tools/validate_product_proof.py
python tools/validate_architecture.py
python tools/check_dependencies.py
python tools/check_public_seams.py
python tools/run_promotion_gate.py --set architecture_kernel
git diff --check
```

Run additional focused adversarial checks only where they bear on the actual U01 implementation or
a concrete false-positive path. Existing heavyweight U05/PostgreSQL/process proof is outside this
unit unless you establish a direct U01 dependency.

## Verdict law

Return one U01 verdict:

- `PASS` — U01 implementation meaning is correct and bounded; any proof-harness repair required by
  the two observed discrepancies has been independently identified with no unresolved material U01
  implementation defect. If your reviewer role is non-mutating, state the exact proof repair
  required and whether it blocks promotion until a Worker successor commits it.
- `FAIL / RETURN_TO_WORKER` — identify each concrete implementation or proof defect, the exact
  accepted proposition it defeats, and the smallest owning-layer repair. Do not broaden into U02.
- `BLOCKED` — required evidence to decide U01 cannot be obtained. State why it is necessary to U01.

A green architecture axis does not substitute for U01 semantic acceptance. Conversely, a
confirmed harness defect must not be repaired by changing correct product semantics merely to make
a contradictory or path-fragile test green.

## Required response

Record:

1. archive SHA-256 and verified Git identities;
2. exact material inspected and environment versions;
3. exact commands/results actually run;
4. semantic review of the complete production diff;
5. independent disposition of W-U01-F001 and W-U01-F002;
6. every new material finding with its authority/proposition and concrete failure path;
7. final `PASS`, `FAIL / RETURN_TO_WORKER`, or `BLOCKED` for U01;
8. explicit statement that U02 is either authorised to begin after lawful promotion, or remains
   prohibited pending the stated repair/re-review.
