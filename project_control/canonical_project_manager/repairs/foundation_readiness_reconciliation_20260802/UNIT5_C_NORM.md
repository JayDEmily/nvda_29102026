# Unit 5 C-NORM — Residual Physical Failure Adjudication

## Status

Acceptance-audited against the user's 2026-08-02 binding instruction. Every
existing assertion is treated as binding. A test may change only where governing
normative authority proves that its exact seam, field location or claimed role is
obsolete, and only when the original behavioural proposition is preserved in an
explicit replacement assertion. Ambiguous authority is a stop condition.

No Unit 5 test may be retired, weakened, skipped, xfail-marked, broadened,
redirected for convenience or hidden through fixture substitution. Every changed
test node is recorded in
`evidence/UNIT5_TEST_CHANGE_AUTHORITY_REGISTER.tsv` with its old node, authority,
replacement assertion and red-to-green evidence.

## Authority

- User instruction on 2026-08-02: assertions binding; no retirement,
  re-authoring, weakening, skip, xfail, broadening or redirection for green.
- `project_control/canonical_project_manager/CONTINUATION.md` sections 8.5 and 10.
- `docs/03.2_INPUT_AND_CALENDAR_DOMAIN_WORKING.md` typed options law.
- `docs/04.2_PREPARED_DATA_CONTRACTS_WORKING.md` common-context allocation law.
- `docs/07.1_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_WORKING.md` runtime-owner law.
- `docs/07.2_STATE_RISK_AND_REPLAY_WORKING.md` M12/M13 owner law.
- `docs/09.1_DMPV3_PROTOCOL_WORKING.md` complete K07 role and caller-owned
  identity law.
- `docs/11.1_NATIVE_ARCHITECTURE_BLUEPRINT_WORKING.md` exact M05/M06/M12 seams.

## Test-change law

Only three dispositions are admissible:

1. **Production repair, assertion unchanged.** The original test node and
   behavioural assertion remain intact and turn red-to-green through owner code.
2. **Authority-complete fixture or owner binding, proposition unchanged.** A
   fixture supplies newly mandatory caller-owned facts, or a proof invokes the
   already-governing owner, while every original behavioural assertion is retained
   or strengthened.
3. **Normative supersession with explicit replacement.** Higher authority proves
   that the old role or direct field location is non-admitted. The original domain
   proposition is asserted first, followed by the current-law fail-closed or
   owned-location assertion. The old node and replacement node remain mapped.

There is no admissible retirement disposition in Unit 5.

## Unit 5A — typed options evidence and bounded common context

The source/preparation boundary owns typed options evidence. Cognition may
consume only an `OptionsEvidenceEnvelope` or a repository-owned prepared
snapshot that preserves that envelope's identity. A generic mapping is not
options authority. The compatibility `StageInputBundle` exposes one optional
`CommonStageContext` plus narrow carrier references; when the context is
present, every carrier reference must match it. Existing direct legacy
constructors may remain context-less, but the canonical translator must emit the
context from prepared authority and may not fabricate absent facts.

Pass condition: C004/C009/C013/C016 are green, typed adapters remain green,
generic mapping input fails closed, and existing direct compatibility callers do
not acquire invented identity.

## Unit 5B — packet-role and parallel-risk compatibility adjudication

`capital_deployment_decision` and `parallel_risk_bootstrap_input` are not K07
roles and must not be admitted. The capital decision's action, input trace and
receipt identity remain explicitly asserted before the legacy packet helper is
required to fail closed. The old Module-8 bootstrap specimen may exist only as
an explicitly non-binding `diagnostic_packet`; its producer identity, execution
context, target lineage, source artefact identity and input fingerprint must be
explicit. Its output may use `parallel_risk_packet` only as compatibility
evidence and may not feed the canonical M09 route. Canonical M06 remains the
only live Parallel Risk owner.

Pass condition: no new K07 role is added; original capital-decision propositions
remain asserted; compatibility packets carry explicit metadata; canonical M06
proof remains green; retained specimen and observation tests prove non-binding
behaviour without fabricated identity.

## Unit 5C — serial compatibility orchestration and candidate identity

The legacy `DeskRuntimeOrchestrator` must reject a structurally invalid stage
mapping instead of returning a partial-success receipt. Where retained tests
exercise its typed compatibility path, runtime execution context and packet
identity are explicit. Candidate families and the playbook registry are owned
inputs to eligibility/expression evaluation, and execution output preserves the
selected candidate identity without capital, broker or placement authority.

Pass condition: C025/C027/C031/C033/C034 and the complete affected serial cone
are green with the original fail-closed and identity propositions intact.

## Unit 5D — downstream carry and review evidence

Overnight carry records the policy version that formed its recommendation and
replay preserves the caller-owned next-session source identity. Daily review
packets expose explicit missing material and source lineage while remaining
review-only and unable to mutate runtime authority.

Pass condition: C042/C044 and affected downstream/review tests are green; direct
field checks are replaced only by stronger behavioural evidence where the same
proposition is exercised through the public owner.

## Unit 5E — current transaction and replay owners

C024 is proved through the existing M13 state-kernel public API; no second
`persistence.transactions` owner is created. C046 is proved through the existing
M12 evidence/replay public API; comparison-only compatibility output remains
non-authoritative and cannot claim reconstruction. The replacement assertions
include absence of reproduced-output identity/fingerprint and absence of runtime
promotion or side effects.

Pass condition: the proposition-preserving C024/C046 owner bindings pass against
M13/M12, their native module proofs remain green, and no compatibility alias
competes for ownership.

## Unit 5 acceptance

Acceptance requires all of the following on the audited tree:

- the 46 Unit 4 failing propositions are green: 45 under their original node IDs and one under its authority-mapped replacement;
- every changed test node is accounted for in the authority register;
- no assertion is dropped, weakened, skipped, xfailed or retired;
- complete physical Tier A, Tier B, Tier C and signed `alpha_current` are green;
- proof authority and all proof-block definitions describe the same universe;
- every vocabulary namespace is candidate-clean with occurrence-level
  dispositions only;
- the bounded Python write set passes Ruff, Black and byte compilation;
- Git contains no hidden generated or uncommitted executable mutation.
