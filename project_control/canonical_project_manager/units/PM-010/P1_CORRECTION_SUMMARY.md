# Reopened P1 PM-007–PM-010 Correction Summary

## Worker result

- Reopened worker validation: `pass`
- Project-manager acceptance: pending
- P1 acceptance: not claimed
- P2/P3/P4/Gate D work: not begun
- Commit: none

## Rebuilt semantic totals

- P1 decisions: 129
- Canonical records/generated entries: 117
- Alias-only decisions: 3
- Quarantined unsupported decisions: 9
- Projected semantic-decision references: 120

## Rebuilt candidate evidence

- Exact occurrence dispositions: 499
- Governing-normative occurrences in the integrated audit register: 59
- Separately preserved PM-008 downstream state-read occurrence: 1
- Governing-normative occurrences routed to P2: 0
- Unresolved audit candidates: 0
- Occurrence identity: path + line + column + normalised phrase + source-context SHA-256

## Reopened semantic corrections

- `PM-007:SSC-010 Serial Desk-cognition` is explicitly dispositioned as a lawful alias of canonical `PM-007:SSC-015 Serial Desk-cognition Spine`.
- Every PM-007 fixed label is covered exactly once; the new canonical Spine row does not silently replace the assigned fixed label.
- `PM-009:PRP-004 Stage-read State` is quarantined because no higher normative proposition establishes a distinct per-stage read-status record.
- The downstream `state-read` proposition is removed from PM-009 and governed under `PM-008:OPC-010 Downstream State-reader Layer`.
- Deleted Stage-read human-registry occurrences are removed from PM-009 occurrence evidence.

## Strengthened validation

- PM-003–PM-009 fixed labels are parsed directly from each worker brief.
- Every parsed exact fixed label must occur exactly once in its owning adjudication register.
- Fixed-label replacement cannot pass through unchanged row arithmetic.
- Integrated semantic roles, registry references, generated JSON, occurrence dispositions, audit report and stamp are cross-checked.
- Source locators and declared source revisions are validated.
- The new-occurrence probe proves a prior phrase disposition does not suppress a new path occurrence with unchanged text.

## Validation status

- Reopened semantic/projection validator: PASS
- Exact fixed-label coverage: PASS
- Source-locator validator: PASS
- New-occurrence audit probe: PASS
- Generated JSON determinism/parity: PASS
- Audit/stamp parity: PASS
- `git diff --check`: PASS
- Read-only Tier A vocabulary diagnostics: 83 passed, 18 failed

The diagnostic failures remain recorded because existing tests expect unsupported concepts, a duplicate human heading for an alias, or the previous audit fixture/suppression protocol. No test was edited or suppressed.
