# User-requested preservation checkpoint — 13 October 2026

**PAUSED. Not a Stage-1 acceptance or completed reviewer candidate. Stage 2 has not started.**

Latest instruction: “Can you pause work and make everything downloadable so we don't lose any work?”
Development stopped at that instruction. Remaining local edits are preserved by an
ordinary work-in-progress Git commit; its exact HEAD/tree are in the archive's
`CHECKPOINT_READBACK.json`. No history is rewritten or pruned.

## Authority and work preserved

The owner approved the exact D178/D189/D192 resolution and the D175 reference-calibrated
policy. `authority/F4_OWNER_APPROVED_CLARIFICATION_20261013.md` records the approval.
Both earlier proposal records remain historical evidence with their original labels.
Only the approved D175/D189 catalogue context conjunctions changed; no R/D edges changed.
The effective catalogue SHA-256 is `26c5486d1a4c7ff68025c7ce2d7e6847a7798759b847a716c942fd05345f3803`.

Implemented work includes immutable RiskScope; D178 net-edge premium conversion;
D164 structured execution-cost consumption; D175 exact reference limits; D176 exact
ceiling consumption; D189 joint four-Greek clipping; D192 actual monetary breach and
precedence; the narrow D175 account-subject selector; and actual producer provenance.
Proof commits precede the related production repairs. Package version stays 1.0.0.

## Independent review and repairs

`INDEPENDENT_REVIEW_RETURN.md` records a fresh review of production 95ae8c3:
RETURN_TO_WORKER / RECURRENT_CLASS, with four Important findings and no Stage-1 acceptance.
The original executable reviewer witnesses are preserved alongside that report.

The four findings concern source units/quantities, independent component rounding,
actual producer provenance, and canonical D187 score metadata. The repair proofs
were separately committed at 1e7d125 before production repair 4ed7586. A further
snapshot-correspondence proof at a4aa6ba precedes the latest preserved edits.
No independent re-review of the repaired final tree has occurred.

## Verification actually obtained

- Pinned Python 3.13.5, pytest 9.0.3, mypy 1.20.1, ruff 0.15.11,
  psycopg 3.3.4 and PyYAML 6.0.3 are installed.
- Derived-signal suite: 773 passed before the latest snapshot-correspondence edits.
- Architecture/bootstrap suite: 74 passed before those latest edits.
- Full product suite: 1197 passed, **55 PostgreSQL fixture errors**; not a green full suite.
- Structural architecture, dependency direction/cycle and public-seam checks passed.
- Whole source/test/tool lint passed before the latest snapshot-correspondence edits.
- Admitted type check reported no issues in 22 source files before those latest edits;
  its notes expressly state that unannotated function bodies are not checked by default.
- Latest focused review regressions: **15 passed** after the snapshot-correspondence edits.

Logs retain earlier failed runs as well as later results; filenames alone are not proof.
The 174 / 144 / 30 population is mechanically accounted for in CATALOGUE_READBACK.json;
that static census does not independently establish full runtime acceptance.

## Remaining work on resumption

1. Read GUARDRAILS, AGENTS, accepted EXEC_PLAN, current authority and this checkpoint.
2. Finish review-class reconciliation and verify the exact latest tree, including
   full lint/type/regression after the snapshot edits. Preserve prior RED history.
3. Reconcile remaining Stage-1 evidence to the full 174 own-kernel / 144 public-closed /
   30 cross-stage obligations. Do not promote historical or sampled proof to exhaustive acceptance.
   The older cross-stage progress generator still contains historical blocked labels
   and has not been regenerated against the approved contracts.
4. Run the required PostgreSQL checks in a legitimate non-root environment.
5. Freeze one independently reviewable Stage-1 candidate only when its actual obligations
   are met. No Stage-1 acceptance is implied and Stage 2 remains unauthorised.

PostgreSQL 17.9 is supplied and extracted, but this host maps only UID/GID 0.
`runuser -u oai` cannot set groups, `chown` to oai reports Invalid argument, and
an alternate user mapping via unshare is denied. The database startup/non-root checks
were not bypassed. The 55 PostgreSQL tests error on their required DSN fixture.

The source-preflight PF-03/PF-04 entries remain explicitly scoped inferences/source
contract questions, not newly established mathematical defects. They were not
silently repaired or declared closed in this financial-policy work.
