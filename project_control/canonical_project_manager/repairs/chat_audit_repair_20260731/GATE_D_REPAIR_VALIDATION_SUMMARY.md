# M03/M05/M06 adversarial Gate D repair validation

## Disposition

`PASS:GATE_D_REPAIR_ACCEPTED:M03_M05_M06_ADVERSARIAL_AUTHORITY`

Canonical base: `55e3b0b154bcd1829de133222f1c5ce0a13a1361`
Expected-red proof baseline: `6d03237`
Branch: `work/chat-audit-repair-m03-m05-m06-v1`

The repair integrates the eight authority-supported defects from the independent novel audit and the one supported proposition from the user-supplied M05 selected handoff. The handoff remains consideration evidence, not authority.

## Accepted implementation

### M03 K05/K06

- a degraded contributing source cannot form a valid/complete envelope;
- every declared degraded-source limitation is retained by the envelope;
- competing source/capture pairs for one typed payload field require exactly one K06 receipt covering those pairs;
- selected/degraded receipt values must equal the emitted typed payload value;
- unavailable/withheld receipts cannot coexist with non-null payload values;
- derivation receipt state/value must agree with the emitted payload.

### M05 K08/K09

- prepared validation/completeness states are closed literal domains;
- valid context requires complete state with no limitations or unavailable-owner facts;
- degraded context requires degraded state and an explicit gap;
- every terminal serial result has deterministic `serial_result_id`;
- only formed results additionally have a distinct `candidate_id`;
- every terminal result carries the actual stage-output prefix and failed-stage output.

### M06 K10

- VIX caution/block thresholds are finite, non-negative and strictly ordered;
- the implemented evaluator accepts only `parallel-risk.compat.v1`;
- the implemented aggregate accepts only `parallel-risk.aggregate.v1`;
- copied or directly reconstructed inputs/assessments remain constrained by those closed domains.

## Selected-handoff disposition

Admitted:

- deterministic terminal `serial_result_id`, distinct from formed `candidate_id`;
- rejection of identity-role substitution.

Dismissed:

- cumulative stage dependencies;
- six separate contexts;
- generated `not_evaluated` outputs;
- generic registered payload carriers;
- Worker A control receipts and raw logs.

The dismissed material conflicts with the accepted common-context/selective-dependency design, widens the bounded carrier seam or lacks normative authority.

## Validation

### Focused and independent

| Check | Result |
|---|---:|
| Existing focused M03/M05/M06 cases before repair | 87 passed |
| Expected-red repair cases at `6d03237` | 12 failed |
| Current focused M03/M05/M06 proof | 99/99 passed |
| Original positive/metamorphic script | 8/8 passed |
| Original adversarial audit | 7 cases reject as expected; the unsupported-version setup now rejects earlier at input construction |
| Replacement unsupported-version cases | 2/2 passed |
| Static compilation | passed |
| `git diff --check` | passed |

The original unsupported-version audit case expected input construction to succeed and evaluator execution to reject later. The repaired public boundary rejects the unsupported label during input construction; this is stricter and is covered by two admitted replacement cases.

### Repository controls

| Check | Result |
|---|---:|
| Proof manifests | 60/60 passed |
| Proof-executor contract | 21/21 passed |
| Tier B | 49/49 passed |
| Vocabulary canonical parity | 4/4 passed |
| All vocabulary files, individually | 100 passed/3 unchanged failures |

The three vocabulary failures are unchanged at baseline: `candidate_audit`, `mutable_runtime_surface`, and the candidate-schema category-set expectation.

### Tier A baseline/current comparison

The complete Tier A set was run as the non-vocabulary partition plus all 17 vocabulary files individually.

| Tree | Passed | Failed |
|---|---:|---:|
| Expected-red proof baseline `6d03237` | 1,508 | 268 |
| Repair candidate | 1,520 | 256 |
| Delta | +12 | -12 |

Exact node comparison:

- 12 admitted repair failures resolved;
- zero new failing nodes;
- all 256 remaining nodes reproduce at the proof baseline.

### Tool availability

Ruff and Black are not installed in the locked environment. No unpinned substitute was used.

## Remaining boundary

M09 K11/fresh-capital authority has not started. This repair does not claim live trading, profitability, production durability or completion of downstream modules.
