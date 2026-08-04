# 2026-04-01 Gate 142 Overwrite and Ownership Inventory

Status: complete on `main`

## Purpose

Freeze the observed overwrite chain, stage-local ownership boundaries, and the immediate downstream consumers that currently depend on mutated runtime outputs before Gate 143 introduces any additive preserved handoff carriage.

## Observed overwrite chain on clean Gate 141 / Gate 140 baseline

### 1. Posture chain

Observed in `src/nvda_desk/services/cognition_runtime.py`:
- `self._posture.evaluate(...)` emits the first posture packet;
- selector emissions are then applied through `_posture_with_contract_citations(...)`;
- modifier policy is evaluated against the cited posture;
- `apply_to_posture(...)` mutates posture before Stage 5 eligibility runs.

Meaning now:
- downstream Stage 5 does **not** see the raw posture output;
- Stage 5 consumes a posture packet that has already absorbed selector citations and modifier mutation.

### 2. Eligibility chain

Observed in `src/nvda_desk/services/cognition_runtime.py`:
- `self._eligibility.evaluate(...)` runs against modifier-mutated posture;
- `_eligibility_with_contract_citations(...)` appends selector-contract reasons;
- the cited eligibility packet is then passed directly into Stage 6 execution.

Meaning now:
- execution consumes cited eligibility only;
- no preserved stage-local eligibility packet is carried to review or to the runtime result.

### 3. Execution and terminal-risk chain

Observed in `src/nvda_desk/services/cognition_runtime.py` and `src/nvda_desk/services/risk_gateway.py`:
- `self._execution.evaluate(...)` emits execution synthesis;
- `apply_to_execution(...)` mutates execution using the modifier runtime packet;
- `evaluate_runtime_join(...)` emits the terminal risk decision;
- `apply_final_join(...)` mutates execution again and stores compatibility surfaces such as `pre_final_risk_*` and `final_risk_join`.

Meaning now:
- review sees only the post-final-join execution object;
- the terminal risk decision exists as a local variable during runtime but is not preserved as its own review-visible handoff surface;
- the current `pre_final_risk_*` compatibility fields preserve only selected final-risk ancestry, not the full execution packet before terminal application.

### 4. Review and stage-packet dependency chain

Observed in `src/nvda_desk/services/review_explanation.py` and `src/nvda_desk/services/cognition_runtime.py`:
- review is built from `temporal`, `regime`, `options_flow`, final `posture`, final `eligibility`, final `execution`, and the modifier runtime packet;
- review then exposes `payload.execution.final_risk_join` and the mutated execution payload in the review packet;
- `stage_outputs` and DMP v2 stage packets are built only from the final per-stage payloads, not from preserved intermediate handoff objects.

Meaning now:
- review and trace consumers cannot inspect the cited posture, cited eligibility, execution before modifier mutation, or execution after modifier mutation but before terminal application unless those surfaces are admitted additively.

## Immediate consumer inventory that depends on mutated outputs

### Review consumers
- `src/nvda_desk/services/review_explanation.py`
- `src/nvda_desk/services/review_packets.py`
- `src/nvda_desk/api/app.py` daily review endpoint

### Trace / replay consumers
- `src/nvda_desk/testing/bounded_trace_review.py`
- `tests/test_dmp_review_trace.py`
- `tests/test_tranche_a_review_replay.py`

### Runtime expectation tests that currently read final mutated outputs
- `tests/test_gate121_final_risk_gateway_join.py`
- `tests/test_gate103_raw_prepared_parity.py`
- `tests/test_gate97_runtime_invariants.py`
- `tests/test_execution_review_runtime.py`
- `tests/test_gate125_review_visible_lineage.py`

## Retain / retire / amend / add matrix

### Retain in Gate 143
- seven-stage runtime order;
- existing `modifier_runtime_packet` carriage;
- existing `pre_final_risk_*` compatibility surfaces on `ExecutionExpressionOutput`;
- existing `final_risk_join` compatibility surface on `ExecutionExpressionOutput` and review packets.

### Retire in Gate 142
- nothing. Gate 142 is inventory only.

### Amend in Gate 143
- `ReviewExplanationInput` so review can accept an additive preserved handoff surface;
- `ReviewExplanationOutput` and `review_packet` so the preserved handoff surface is visible without replacing current outputs;
- `DeskCognitionRuntimeResult` so the runtime result can carry the preserved handoff surface directly.

### Add in Gate 143
- one additive typed handoff surface carrying only the preserved artefacts Gate 142 proved necessary:
  - cited posture before modifier mutation;
  - cited eligibility before downstream mutation/repackaging;
  - execution before modifier mutation;
  - execution after modifier mutation but before terminal-risk application;
  - terminal risk decision before `apply_final_join(...)` mutates execution.

## Gate 143 admission decision forced by Gate 142

Gate 143 must admit one additive preserved surface because the current compatibility fields do **not** preserve the full chain needed to inspect ownership boundaries cleanly. The minimum lawful additive surface is:
- `StageLocalHandoffSurface` carried additively into review input, review output, and the runtime result.

Gate 143 must keep all existing terminal behaviour stable. No stage count changes, no packet-order changes, and no retirement of `final_risk_join` or `pre_final_risk_*` compatibility fields is allowed in Gate 143.
