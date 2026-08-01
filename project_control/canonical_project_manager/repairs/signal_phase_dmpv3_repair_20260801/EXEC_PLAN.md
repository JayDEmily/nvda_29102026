# NVDA Signal-Informed Intraday Phase and DMPV3 Repair Plan

**Status:** Planning only — no repository changes performed  
**Created:** 2026-08-01  
**Project baseline branch:** `work/m12-review-replay-v1`  
**Project baseline commit:** `9364b4698f417ab9aaebe9e24d8a4a4e3cb98971`  
**Project archive SHA-256:** `ba6d0bf4bfbfefb34105d078c904287a1980271f89e1deada5ff39a7abfb8f02`  
**Repair-brief archive SHA-256:** `538041a978543caa4324d0ddd0a581e6ddecbe1e53a6871f0a9b6516edcf1294`

---

## 1. Objective

Repair two missed cross-module acceptance units without rolling back accepted downstream work:

1. Implement the missing signal-informed intraday phase capability and integrate it lawfully into M05.
2. Make DMPV3 carriage mandatory for canonical M05 and M06 outputs entering M09, including validation, lineage and downstream compatibility.

The repair must preserve accepted M01–M13 work, close normative contradictions before code changes, add seam-level proof, and return the repository to a state suitable for M00 final composition.

---

## 2. Current project position

The accepted architecture contains **M00–M15**:

- **M00–M13:** runtime and delivery architecture.
- **M14:** proof and promotion governance.
- **M15:** vocabulary governance.

M01–M13 have accepted implementation slices. M00 final composition has not started.

The relevant dependency chain is:

```text
M03 preparation
   ├── M05 serial cognition ──┐
   └── M06 parallel risk ─────┤
                              ▼
                         M09 capital
                              ▼
                         M10 → M11

M04 packet protocol ──────────┤
M12 evidence/replay consumes packet and evidence contracts
```

This is a forward repair against an almost-composed runtime. Rollback is not the default because it would discard accepted downstream work without resolving the architectural seams.

---

## 3. Confirmed defects

### 3.1 Signal-informed intraday phase

The normative behaviour exists, but the production module does not.

Confirmed symptoms:

- The expected module `nvda_desk.domain.temporal.intraday_phase` is absent.
- Existing C-026 tests fail with `ModuleNotFoundError`.
- Current temporal behaviour remains a fixed clock classifier.
- M05 consumes `session_state` rather than a typed signal-informed phase result.
- No accepted session-scoped prior-phase/history repository is integrated.

### 3.2 Mandatory DMPV3 carriage

The DMPV3 helper implementation is not the main defect. The missing work is integration.

Confirmed symptoms:

- M05 and M06 return domain objects directly.
- M09 accepts those objects directly.
- M09 has no mandatory packet-validation boundary for canonical M05/M06 ingress.
- Current authority describes M05 and M06 packet carriage as optional.
- The repair brief requires mandatory canonical carriage before M09.
- `FinalRiskDecision` does not preserve the required packet and execution lineage.
- A legacy orchestrator invents execution identities and uses a non-admitted packet role.

### 3.3 Test blind spot

Existing isolated M04/M05/M06/M09 tests pass, while seam behaviour is missing.

Observed baseline:

```text
Signal-informed phase tests:
3 failed
Cause: missing nvda_desk.domain.temporal.intraday_phase
```

```text
Focused M04/M05/M06/M09 tests:
373 passed
```

```text
Legacy serial/packet boundary tests:
143 failed, 3 passed
Primary cause: caller-owned scenario identity now required
```

```text
Legacy parallel-risk contract:
1 failed, 7 passed
Cause: parallel_risk_bootstrap_input is not an admitted K07 role
```

These failures must not be resolved by weakening M04.

---

## 4. Governing execution method

Follow repository authority in this order:

1. User instruction.
2. This repair plan and the supplied repair brief.
3. `AGENTS.md` and applicable overrides.
4. Existing canonical ExecPlan.
5. Normative architecture and protocol documents.
6. Tests.
7. Production source and configuration.
8. Ledgers and receipts.

For each semantic acceptance unit:

1. Read all in-scope authority, tests and production files in full.
2. Amend normative documents first.
3. Add or update expected-red tests.
4. Implement only the bounded production changes.
5. Run focused and downstream validation.
6. Record exact evidence.
7. Commit one acceptance unit at a time.
8. Do not weaken tests, validation or packet law.

---

## 5. Branch and repository strategy

Create a forward repair branch from the accepted baseline:

```text
work/signal-phase-dmpv3-repair-v1
```

Base:

```text
9364b4698f417ab9aaebe9e24d8a4a4e3cb98971
```

Required controls:

- Verify archive hash, branch, HEAD and clean worktree before mutation.
- Confirm complete Git history.
- Do not reset, rebase, squash or rewrite accepted history.
- Do not cherry-pick old module branches over the accepted current branch.
- Amend the existing canonical ExecPlan rather than create a competing plan.
- Insert this repair before M00 final composition.
- Correct any stale ExecPlan headline that still reports M11 as the latest accepted module.
- Create the required current-target full-read manifest before changing authority or code.

---

# Acceptance Unit A — Signal-Informed Intraday Phase

## 6. A1 — Reconcile authority

Update the normative surfaces so they state one unambiguous design.

Required decisions:

- The temporal domain owns phase meanings and transition policy.
- M03 owns admitted typed signal preparation.
- A session-scoped repository owns prior accepted phase and bounded history.
- M05 owns orchestration of the temporal stage, not phase semantics.
- Fixed clock classification is only a coarse prior.
- `unresolved`, `clock_only_degraded` and `held_degraded` cannot create positive permission.
- State transitions must be deterministic and replayable.
- Corrections must preserve superseded-state lineage.
- Alpha persistence claims must be honest.

Minimum documents to inspect and amend:

- `docs/02.2_SIGNAL_INFORMED_INTRADAY_PHASE_WORKING.md`
- `docs/07.1_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_WORKING.md`
- `docs/11.1_NATIVE_ARCHITECTURE_BLUEPRINT_WORKING.md`
- Relevant Atlas behaviour mappings, including B07.2
- Namespaced vocabulary authority
- `project_control/canonical_project_manager/EXEC_PLAN.md`
- Current roadmap and dependency surfaces

### A1 exit gate

Pass only when:

- Ownership is singular and non-conflicting.
- Input, output, state, degradation and correction contracts are explicit.
- M05 integration is defined without transferring temporal semantics into M05.
- No document still implies clock-only classification is canonical.

---

## 7. A2 — Establish expected-red proof

Retain the existing C-026 tests and add production-facing proof for:

- Same clock time with different sustained signals.
- Clock-only degraded classification.
- Minimum dwell.
- Hysteresis.
- A single noisy observation not causing regression.
- Stale signal families.
- Missing signal families.
- Contradictory authoritative venue state.
- Lawful correction and superseded-state lineage.
- Deterministic replay.
- M05 temporal-stage integration.
- Downstream fail-closed behaviour.
- Copy-safe repository state.
- Policy-version lineage.

Add plausible mutants for:

- Replacing signal logic with fixed clock thresholds.
- Ignoring minimum dwell.
- Ignoring hysteresis.
- Allowing illegal regression.
- Dropping correction lineage.
- Treating degraded states as positive permission.
- Hidden mutable evaluator state.
- Non-deterministic replay.

### A2 exit gate

Pass only when:

- New tests fail for the intended missing behaviour.
- Failures are not caused by broken fixtures or unrelated imports.
- Each test maps to an explicit normative requirement.
- Mutants are capable of failing the corresponding proof.

---

## 8. A3 — Implement bounded production surfaces

Add the temporal domain module:

```text
nvda_desk.domain.temporal.intraday_phase
```

Required public contracts:

- `IntradayPhase`
- `IntradayPhaseEvidence`
- `IntradayPhasePolicy`
- `IntradayPhaseEvaluator`

Also define explicit typed contracts for:

- Evaluation result.
- Prior accepted phase state.
- Bounded phase history.
- Repository protocol.
- Correction and supersession lineage.
- Policy/version identity.

Implementation requirements:

- Deterministic.
- Replayable.
- No hidden mutable evaluator state.
- Injected repository protocol.
- Process-memory repository permitted for alpha use only.
- Copy-safe state access.
- Versioned policy and state.
- No false durability claim.
- Fixed clock input used only as a prior.
- Degraded or unresolved states fail closed.

M05 integration:

- Add a narrow temporal-stage adapter.
- Keep `SerialRunner` pure and deterministic.
- Keep repository access outside the pure serial algorithm.
- Keep packet construction outside the temporal evaluator.
- Feed M05 a typed phase result rather than an unqualified session-state string.

### A3 exit gate

Pass only when:

- Existing and new temporal tests pass.
- M05 consumes the typed result lawfully.
- Replay produces identical results from identical inputs and state.
- No downstream permission is created from degraded evidence.
- No unrelated M05 logic is rewritten.

---

# Acceptance Unit B — Mandatory DMPV3 M05/M06-to-M09 Boundary

## 9. B1 — Resolve normative contradiction

Replace the current optional-carriage rule with the following:

- Pure internal M05 and M06 domain objects remain lawful inside their modules.
- Canonical M05 and M06 outputs crossing into M09 require DMPV3.
- DMPV3 is not required at raw M01 capture, calendar ingestion or internal M03 preparation.
- Packet identity and execution context are supplied by the composition/execution owner.
- M05 and M06 must not invent packet IDs, trace IDs, run IDs, scenario IDs, module-instance IDs, module versions or emission times.
- M09 must validate the canonical packet boundary before capital logic.

### B1 exit gate

Pass only when:

- No authority still states that canonical M05/M06-to-M09 carriage is optional.
- Raw-input and internal-computation boundaries are explicitly excluded.
- Execution-context ownership remains consistent with M04.
- M09’s validation ownership is explicit.

---

## 10. B2 — Establish lawful common parentage

Use the admitted `prepared_context_packet` at the M03 output boundary.

Required lineage:

- It is the parent of the first M05 `stage_packet`.
- It is the parent of the M06 `parallel_risk_packet`.
- It supplies the common trace/run/scenario context.
- It binds both branches to the same prepared-data lineage.
- Later M05 stage packets preserve ordered dependency lineage.

This is a boundary packet. It does not require packetisation of raw capture or all internal M01–M03 transformations.

### B2 exit gate

Pass only when:

- Both M05 and M06 packets have lawful K07 parentage.
- Both packets resolve to the same prepared context.
- Execution-context identity matches across both branches.
- No new packet role is invented without normative admission.

---

## 11. B3 — Add boundary adapters

### M05 adapter

The adapter must:

- Accept caller-owned execution and packet context.
- Wrap actual ordered `StageOutput` objects with `build_stage_packet`.
- Preserve parent and dependency order.
- Preserve prepared lineage.
- Preserve source artefacts.
- Preserve M07/M08 authority.
- Carry the terminal formed `SerialCandidate` using the accepted stage-packet profile.
- Avoid successful candidate carriage for stand-down, withheld or rejected results.
- Avoid creating packet identities internally.

### M06 adapter

The adapter must:

- Accept the same caller-owned execution context.
- Wrap the actual `ParallelRiskAssessment` with `build_parallel_risk_packet`.
- Preserve observations.
- Preserve policy versions.
- Preserve prepared lineage.
- Preserve cautions, hard blocks, unknowns and limitations.
- Avoid changing the risk meaning during packet construction.
- Avoid creating packet identities internally.

Reuse existing M04 builders:

- `build_stage_packet`
- `build_parallel_risk_packet`

Do not duplicate or weaken M04 packet law.

### B3 exit gate

Pass only when:

- Packet adapters are thin and deterministic.
- Domain algorithms remain packet-agnostic.
- Caller-owned identity is enforced.
- Packet payload semantics equal the original domain-object semantics.
- Invalid or incomplete execution context fails closed.

---

## 12. B4 — Make canonical M09 ingress packet-only

Add a canonical M09 entry point that accepts typed M05 and M06 DMP envelopes.

Before capital logic, validate:

- Packet role.
- Schema and typed payload.
- Producer identity.
- Module identity.
- Stage identity.
- Exact K07 common validation.
- Exact role-specific validation.
- Caller-owned trace/run/scenario.
- Packet validation status.
- Parent lineage.
- Dependency lineage.
- Source identity.
- Prepared-context identity.
- Prepared-context fingerprint.
- Matching execution context across M05 and M06.
- Compatible prepared input.
- Payload semantic fingerprint.
- Packet carriage fingerprint.

Only after validation may M09 call a private pure join using the existing domain objects.

The current direct-object join must become either:

- A private internal helper; or
- A clearly named transitional adapter that cannot bypass canonical packet validation.

Extend `FinalRiskDecision` and M09 receipts to preserve:

- M05 packet ID.
- M05 carriage fingerprint.
- M06 packet ID.
- M06 carriage fingerprint.
- Trace ID.
- Run ID.
- Scenario ID.
- Validated prepared-context packet ID.
- Validated prepared-context fingerprint.
- Exact validated envelope lineage.

### B4 exit gate

Pass only when:

- Canonical M09 entry cannot be reached with unvalidated direct objects.
- Cross-branch execution-context mismatch is rejected.
- Prepared-context mismatch is rejected.
- Invalid role or lineage is rejected.
- Valid packets preserve prior capital semantics.
- Decision output contains complete packet lineage.

---

## 13. B5 — Define deterministic carriage fingerprinting

The current generic DMP envelope does not contain a universal packet-fingerprint field.

Recommended implementation:

- Add an M04-owned deterministic carriage-fingerprint function.
- Do not immediately add a mandatory field to every envelope unless normative review proves it necessary.
- Bind material:
  - packet role;
  - producer;
  - schema;
  - execution context;
  - parent and dependencies;
  - source/prepared lineage;
  - typed payload meaning.
- Make canonicalisation insensitive to dictionary and field ordering.
- Preserve packet occurrence ID and emission time as separate facts.
- Ensure semantically different payloads cannot share the same carriage fingerprint under the governed canonicalisation.

### B5 exit gate

Pass only when:

- Fingerprinting is deterministic.
- Ordering differences do not alter the fingerprint.
- Material semantic changes do alter the fingerprint.
- The algorithm is owned by M04.
- M05, M06 and M09 use the same implementation.

---

## 14. B6 — Repair or quarantine legacy paths

The old `DeskRuntimeOrchestrator` must not remain a competing canonical route.

Choose one bounded outcome:

1. Convert it into an explicit transitional adapter that requires caller-owned execution context; or
2. Quarantine it as legacy/inspection-only and route canonical tests through the new adapters.

Also:

- Remove canonical use of `parallel_risk_bootstrap_input`.
- Do not add that role to K07 merely to make an obsolete test pass.
- Do not regenerate trace/run/scenario identities from source time.
- Do not hard-code scenario context.
- Do not create packet IDs inside domain algorithms.

### B6 exit gate

Pass only when:

- There is one canonical M05/M06-to-M09 route.
- Legacy code cannot silently bypass M04 law.
- Obsolete packet roles are absent from the canonical route.
- Existing historical behaviour is either lawfully adapted or explicitly quarantined.

---

# Downstream Compatibility

## 15. M09–M12 reconciliation

Do not reopen downstream policy semantics unless changed contracts require it.

Validate:

### M09

- Decision construction.
- Capital receipt creation.
- Packet and execution lineage.
- Existing capital logic unchanged after valid ingress.

### M10

- Consumption of M09 decisions.
- Preservation of new decision lineage.
- No hidden dependency on direct M05/M06 objects.

### M11

- Lineage flowing from M10.
- No loss of packet identities or carriage fingerprints.

### M12

- Evidence and replay of changed packet and decision lineage.
- Deterministic reconstruction.
- No false proof claims.

Likely changes should be limited to:

- Fixture construction.
- Contract fields.
- Lineage propagation.
- Evidence/replay surfaces.

M01–M03, M07–M08 and M13 remain accepted prerequisites except for the narrow M03 boundary adapter and required public exports.

### Compatibility exit gate

Pass only when:

- Existing downstream semantics remain unchanged.
- New lineage is preserved through M12.
- Replay remains deterministic.
- No unrelated module is rewritten.

---

# Validation Programme

## 16. Per-unit validation

For each acceptance unit:

1. Capture exact baseline failures.
2. Record the expected-red node set.
3. Implement only the bounded change.
4. Run focused production tests.
5. Run affected integration tests.
6. Run downstream compatibility tests.
7. Run exact Tier A node comparison.
8. Run relevant Tier B tests.
9. Run vocabulary validation.
10. Run manifest validation.
11. Run plausible mutants.
12. Record unavailable tooling honestly.
13. Confirm clean Git state.
14. Commit the acceptance unit.
15. Produce a full-history checkpoint.

---

## 17. Required final proof

The repair is not complete unless evidence shows:

- Existing 373 focused M04/M05/M06/M09 tests remain green or have only authorised, explained contract updates.
- The three current C-026 import failures are resolved.
- New signal-state tests pass.
- New M05/M06-to-M09 seam tests pass.
- Clock-only substitution mutants fail.
- Dwell and hysteresis mutants fail.
- Illegal regression mutants fail.
- Dropped-lineage mutants fail.
- Packet-role substitution mutants fail.
- Execution-context mismatch mutants fail.
- Prepared-context mismatch mutants fail.
- Legacy caller-context failures are lawfully repaired or removed from the canonical route.
- `parallel_risk_bootstrap_input` is not used canonically.
- No unrelated Tier A failures are introduced.
- No test is weakened, skipped or suppressed.
- Git worktree is clean.
- Full-history checkpoint is created.
- Open Unknowns are listed explicitly.

---

# Commit and Checkpoint Strategy

## 18. Recommended commit sequence

Use one semantic acceptance unit per commit. A suitable sequence is:

1. `control: register signal-phase and dmpv3 repair`
2. `docs: reconcile signal-informed phase authority`
3. `tests: add signal-informed phase expected-red proof`
4. `feat: implement signal-informed intraday phase`
5. `docs: require dmpv3 carriage into m09`
6. `tests: add m05-m06-m09 packet seam proof`
7. `feat: add m05 and m06 packet boundary adapters`
8. `feat: enforce canonical packet ingress at m09`
9. `feat: preserve packet lineage through m09-m12`
10. `refactor: quarantine obsolete legacy packet route`
11. `test: close focused and downstream repair validation`
12. `control: close repair and resume m00 readiness`

Commit names may be adjusted to repository conventions, but semantic separation must remain.

---

## 19. Checkpoint contents

The final downloadable checkpoint must include:

- Complete `.git` history.
- Clean worktree.
- Current repair branch.
- All accepted commits.
- Updated canonical ExecPlan.
- Updated normative documents.
- Production changes.
- Tests.
- Validation outputs or receipts required by project authority.
- Full-read manifest.
- Open Unknowns.
- SHA-256 digest.
- Branch and HEAD identification.

Exclude caches, temporary artefacts and files that add no evidentiary or execution value.

---

# Ruled-Out Actions

## 20. Prohibited repair shortcuts

Do not:

- Roll back to old M05 or M06 checkpoints.
- Reset to `origin/main`.
- Rewrite accepted Git history.
- Revert strict M04 execution-context ownership.
- Generate trace/run/scenario defaults.
- Hard-code scenario identity.
- Require DMPV3 at raw input or calendar ingestion.
- Put packet construction inside M05 or M06 algorithms.
- Let canonical M09 accept unvalidated direct objects.
- Admit obsolete packet roles solely to make legacy tests green.
- Weaken, skip or suppress tests.
- Edit evidence to imply success.
- Begin broad M00 composition before both repair units and downstream compatibility pass.

---

# Execution Gates

## 21. Gate sequence

Proceed in this order:

1. **Repository verification**
2. **Control-plan amendment**
3. **Acceptance Unit A authority**
4. **Acceptance Unit A expected-red proof**
5. **Acceptance Unit A implementation**
6. **Acceptance Unit A validation**
7. **Acceptance Unit B authority**
8. **Acceptance Unit B expected-red proof**
9. **Acceptance Unit B boundary adapters**
10. **Acceptance Unit B M09 enforcement**
11. **Legacy-route resolution**
12. **M09–M12 compatibility**
13. **Full validation**
14. **Clean-state and checkpoint proof**
15. **Return to M00 final composition**

Do not skip from authority directly to implementation.

---

# Completion Definition

## 22. Repair complete

The repair is complete only when:

- Both acceptance units pass their normative, test, implementation and validation gates.
- Canonical M05/M06-to-M09 traffic uses validated DMPV3 carriage.
- Signal-informed intraday phase is implemented and integrated into M05.
- M09 preserves full validated packet lineage.
- M10–M12 remain compatible and deterministic.
- The legacy bypass is repaired or quarantined.
- No unrelated accepted module semantics are regressed.
- Git is clean.
- A full-history checkpoint is available.
- M00 can resume without unresolved seam ambiguity.

Until all conditions are evidenced, status remains **IN PROGRESS** or **UNKNOWN**, not complete.
