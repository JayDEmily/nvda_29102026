# NVDA rebuild — continuation brief v3
**Date:** 2026-04-19  
**Purpose:** preserve history of the work completed beyond `nvda_supplemental_continuation_brief_2026-04-19.md`, then queue the next bounded tranche in the obvious next order.  
**Important execution rule:** this document is a **brief only**. Do **not** start implementation from this document in the same turn that creates it.

---

## 1. Direct answer

The previous supplemental brief is now **closed and superseded**.

It is no longer the correct queue because the authority-closure work it carried forward has been completed, and substantial additional work has already landed beyond it.

Evidence:
- current execution receipt records `125 passed`, `17` workbook benchmark families covered, `0` deferred benchmark families, and `0` deferred native registry families remaining at `var/reports/continuation_execution_receipt_2026-04-19.md:3-12`
- current coverage report records `136` scanned source files and `0` uncovered source files at `var/reports/source_coverage_gap_report_2026-04-19.md:1-7`
- retained authority closure is recorded as complete at `var/reports/continuation_execution_receipt_2026-04-19.md:39-43`

So the new brief must do two things:
1. preserve the overrun work as historical closure
2. queue the next bounded truth-pass wave only

---

## 2. State basis for this brief

### Repo state used for this brief
- branch: `work/post-wave1-contract-truth-pass-20260419` at `var/reports/continuation_execution_receipt_2026-04-19.md:4`
- commit basis recorded in the current receipt: `3540521e3c0e35c2270e01daf77b91f97ea2ffa9` at `var/reports/continuation_execution_receipt_2026-04-19.md:5`
- current native shell: `125 passed` at `var/reports/continuation_execution_receipt_2026-04-19.md:12`

### Authority state used for this brief
- active native tests admitted in registry: `84` at `var/reports/continuation_execution_receipt_2026-04-19.md:6`
- registry family count: `110` at `var/reports/continuation_execution_receipt_2026-04-19.md:7`
- workbook benchmark families covered: `17/17` at `var/reports/continuation_execution_receipt_2026-04-19.md:8-10`
- deferred native registry families remaining: `0` at `var/reports/continuation_execution_receipt_2026-04-19.md:11`
- source coverage gaps: `0` at `var/reports/source_coverage_gap_report_2026-04-19.md:3-5`

---

## 3. Historical carry-forward — work completed beyond the previous brief

This section is intentionally historical. It records what has already been done so the next implementation thread does not re-open closed work.

### 3.1 Authority closure that is now complete
The previous supplemental brief carried forward registry/crosswalk/proof/README truth work. That is now closed.

Evidence:
- `config/retained_test_registry.yaml` now admits every active Tier A and Tier B native test file at `var/reports/continuation_execution_receipt_2026-04-19.md:39-40`
- `config/test_architecture_crosswalk.yaml` resolves every workbook benchmark family to covered status at `var/reports/continuation_execution_receipt_2026-04-19.md:41`
- `config/proof_blocks.yaml` is admitted and executable at `var/reports/continuation_execution_receipt_2026-04-19.md:42`
- no `deferred_pending_*` entries remain at `var/reports/continuation_execution_receipt_2026-04-19.md:43`

### 3.2 Upstream raw-signal tranche already landed
The repo now contains bounded upstream raw-signal contracts and ingress support that were not present in the earlier brief.

Evidence:
- `src/nvda_desk/contracts/dataset_packets.py` recorded in the current receipt at `var/reports/continuation_execution_receipt_2026-04-19.md:15`
- `src/nvda_desk/upstream/raw_signal_coverage.py` at `var/reports/continuation_execution_receipt_2026-04-19.md:16`
- `src/nvda_desk/upstream/raw_signal_ingress.py` at `var/reports/continuation_execution_receipt_2026-04-19.md:17`
- supporting Tier A and Tier B blockers at `var/reports/continuation_execution_receipt_2026-04-19.md:18-23`

### 3.3 Review/replay and DMP determinism work already landed
Additional work also landed in review/replay and packet determinism.

Evidence:
- review/replay helpers at `src/nvda_desk/review/imported_module_citations.py` and `src/nvda_desk/replay/review_compare.py` recorded at `var/reports/continuation_execution_receipt_2026-04-19.md:24-27`
- review-stage helper bug fix recorded against `src/nvda_desk/downstream/review_stage.py` and its blocker at `var/reports/continuation_execution_receipt_2026-04-19.md:28-30`
- DMP packet determinism hardening recorded against `src/nvda_desk/packets/dmp_packets.py` and its blocker at `var/reports/continuation_execution_receipt_2026-04-19.md:31-33`

### 3.4 Downstream domain determinism work already landed
The repo now has downstream domain determinism blockers that were not part of the earlier brief.

Evidence:
- `src/nvda_desk/domain/downstream/opening.py` at `var/reports/continuation_execution_receipt_2026-04-19.md:34-35`
- `src/nvda_desk/domain/downstream/live_inventory.py` at `var/reports/continuation_execution_receipt_2026-04-19.md:35-36`
- direct blocker at `tests/tier_a/downstream_runtime/test_downstream_domain_determinism.py` at `var/reports/continuation_execution_receipt_2026-04-19.md:34-37`

### 3.5 Native shell and coverage state to preserve as the historical floor
Any next implementation tranche starts from this floor, not from the old brief’s `74 passed` state.

Evidence:
- native shell `125 passed` at `var/reports/continuation_execution_receipt_2026-04-19.md:12`
- verification rerun list at `var/reports/continuation_execution_receipt_2026-04-19.md:45-50`
- `136` source files scanned and `0` uncovered at `var/reports/source_coverage_gap_report_2026-04-19.md:1-7`

---

## 4. Verified reasons the next tranche is no longer “authority closure”

The obvious next order is now a **typed seam and stage-truth pass** across the thinnest remaining runtime families.

Why this is the correct next order:

### 4.1 Several service/domain seams still return untyped dictionaries where bounded contracts already exist or should exist
Examples:
- `ExecutionService.evaluate()` returns a raw `dict` containing `expression` and `lifecycle_plan` at `src/nvda_desk/services/execution_service.py:11-19`
- `build_lifecycle_plan()` returns a raw `dict` instead of a typed lifecycle contract at `src/nvda_desk/domain/execution/lifecycle_plan.py:8-12`
- `ParallelRiskLaneService.evaluate()` returns a raw `dict` with `environment`, `candidate_audit`, and `lane_packet` at `src/nvda_desk/services/parallel_risk_lane_service.py:10-18`
- `assess_environment()` and `audit_candidate()` both return raw `dict` values at:
  - `src/nvda_desk/domain/parallel_risk/environment_assessment.py:8-14`
  - `src/nvda_desk/domain/parallel_risk/candidate_audit.py:6-12`
- `evaluate_overlay_risk()` consumes and returns raw dictionaries at `src/nvda_desk/domain/final_risk/overlay.py:8-13`
- `apply_terminal_join()` still accepts a raw `overlay_result: dict` at `src/nvda_desk/domain/final_risk/terminal_join.py:9-15`

### 4.2 Some contracts exist but are not yet used as real coordination seams
Examples:
- `StageLocalHandoffSurface` exists but is only a contract declaration at `src/nvda_desk/contracts/execution.py:23-26`; the current code search shows no runtime/service use of it outside contract-model tests
- `FinalRiskJoinReceipt` exists, but the overlay stage still feeds it with an untyped dictionary at:
  - `src/nvda_desk/contracts/risk.py:6-10`
  - `src/nvda_desk/domain/final_risk/overlay.py:8-13`
  - `src/nvda_desk/domain/final_risk/terminal_join.py:9-15`

### 4.3 The runtime orchestrator is still a stage-key receipt, not a typed stage-handoff coordinator
Current behaviour:
- validates stage names only at `src/nvda_desk/runtime/orchestrator.py:54-60`
- records executed/missing stages at `src/nvda_desk/runtime/orchestrator.py:62-70`
- returns a dictionary receipt only at `src/nvda_desk/runtime/orchestrator.py:72-74`

That is acceptable as a bounded shell, but it is now the next obvious candidate for truth-pass hardening because the surrounding stage families exist.

### 4.4 Capital authority remains intentionally bounded but still overly generic at the seam
Current state:
- input carries `final_risk_action: str` rather than a tighter final-risk seam object at `src/nvda_desk/contracts/capital.py:10-14`
- authority logic uses that raw string plus `fresh_cash_pct` at `src/nvda_desk/capital/authority.py:19-26`

That is lawful for the current phase, but it is now one of the thinnest remaining admitted seams.

---

## 5. Correct next ordered continuation queue

This queue is deliberately about the **same size class** as the previous supplemental brief: one bounded tranche of meaningful work, not a repo-wide rewrite.

### Phase A — execution/final-risk/capital seam typing

#### 1. Replace raw execution service dictionaries with typed execution coordination surfaces
Do all of the following together:
- add one typed lifecycle-plan contract instead of returning a raw dictionary from `src/nvda_desk/domain/execution/lifecycle_plan.py:8-12`
- add one typed execution coordination receipt instead of returning a raw dictionary from `src/nvda_desk/services/execution_service.py:14-19`
- keep the service boundary small; do not absorb policy into the service

#### 2. Promote `StageLocalHandoffSurface` from dormant contract to live seam
Use the already-admitted contract at `src/nvda_desk/contracts/execution.py:23-26` as the actual seam between:
- execution post-modifier output
- pre-final-risk handoff

Do not leave this as a contract that is only asserted by model tests.

#### 3. Replace untyped final-risk overlay dictionaries with typed overlay contracts
Do all of the following together:
- introduce a typed overlay result contract
- make `evaluate_overlay_risk()` return that contract instead of a raw dictionary
- make `apply_terminal_join()` consume that typed contract instead of `overlay_result: dict`
- keep `FinalRiskJoinReceipt` as the final emitted surface unless a stronger replacement is required by direct code evidence

#### 4. Tighten the capital authority seam so it consumes final-risk truth, not a free string
Do all of the following together:
- replace `final_risk_action: str` in the capital input path with a tighter final-risk seam value or structured input proven by the admitted final-risk output
- preserve the rule that capital deployment authority remains downstream of final-risk and does not leak upstream into the serial spine
- add direct blockers that fail if capital authority begins consuming unauthorised upstream/cognition fields

### Phase B — parallel-risk lane typing and integrity

#### 5. Replace raw parallel-risk dictionaries with typed environment/audit/coordination contracts
Do all of the following together:
- add a typed environment assessment contract for `src/nvda_desk/domain/parallel_risk/environment_assessment.py:8-14`
- add a typed candidate-audit contract for `src/nvda_desk/domain/parallel_risk/candidate_audit.py:6-12`
- replace the raw service dictionary in `src/nvda_desk/services/parallel_risk_lane_service.py:13-18` with one typed lane evaluation receipt

#### 6. Keep the lane doctrinally separate from the serial spine while making it less placeholder-like
Add blockers that prove all of the following:
- the lane remains co-resident and separate from the serial spine
- the lane does not mutate serial stage outputs
- the lane packet and its supporting receipts remain deterministic under repeated identical inputs

### Phase C — runtime orchestrator truth pass

#### 7. Promote the runtime orchestrator from stage-key receipt to typed stage-handoff validation
Do all of the following together:
- keep the governed stage order in `src/nvda_desk/runtime/orchestrator.py:37-48`
- add typed validation for admitted stage surfaces rather than only validating stage-name membership at `src/nvda_desk/runtime/orchestrator.py:54-60`
- preserve the orchestrator as a coordinator; do not let it absorb stage policy

#### 8. Add one bounded end-to-end typed runtime pass blocker
This blocker should prove one lawful typed path across at least:
- temporal
- regime
- options-flow
- posture
- eligibility
- execution
- final-risk
- capital

It does not need full market policy. It does need truthful typed handoff behaviour.

### Phase D — API/egress/persistence shell truth

#### 9. Tighten outbound DTO and broker-boundary contracts
Current egress surfaces are still very thin:
- `to_api_dto()` is a generic converter at `src/nvda_desk/adapters/egress/api_dto_adapter.py:8-17`
- `BrokerProtocol` is a minimal protocol only at `src/nvda_desk/adapters/egress/broker_protocol.py:7-12`

Add one bounded truth-pass that:
- proves stable DTO projection for the newly typed execution/final-risk/parallel-risk surfaces
- keeps the broker boundary interface separate from any concrete adapter
- fails if outbound DTO shape starts depending on arbitrary dictionary structure rather than admitted contracts

#### 10. Tighten persistence shell truth without widening into full migration work
Do not admit real Alembic revisions yet unless required by evidence. Instead:
- keep the zero-revision placeholder state explicit
- add one bounded persistence blocker that proves the typed execution/final-risk/capital receipts can be represented without migration drift or repository ambiguity
- keep the current migration placeholder truth surfaces lawful and explicit

---

## 6. Verification gates for the next implementation thread

After each bounded phase above, rerun all of the following:
- `python scripts/validate_test_authority.py`
- `PYTHONPATH=src pytest -q tests/tier_a tests/tier_b`
- `python -m compileall src tests/tier_a tests/tier_b scripts`
- `python scripts/report_source_coverage_gaps.py`

And then update together in the same change set:
- `var/reports/continuation_execution_receipt_2026-04-19.md`
- `var/reports/source_coverage_gap_report_2026-04-19.md`
- `config/retained_test_registry.yaml` if any new native test file is added
- `config/proof_blocks.yaml` only if a new durable proof block is actually admitted

---

## 7. Stop/go rule for the next thread

Use this exact rule:
- do **not** reopen authority-closure work unless a verification gate fails and produces direct evidence of authority drift
- do **not** widen into arbitrary new subsystems
- do the work in the order above
- complete Phase A before widening to Phase B
- complete Phase B before widening to Phase C
- complete Phase C before widening to Phase D
- if a new defect is found outside the current phase, fix it only when it is a direct blocker to the active phase; otherwise record it in the execution receipt and keep sequence discipline

This is the correct continuation brief after the previous supplemental brief has been completed and materially overrun.
