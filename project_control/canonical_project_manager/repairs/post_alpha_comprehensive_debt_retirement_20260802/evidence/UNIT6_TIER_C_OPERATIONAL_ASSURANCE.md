# Unit 6 — Tier C Operational Assurance

## Outcome

PASS at working-tree validation; an exact clean-commit rerun follows this unit commit before Unit 7 semantic changes.

## Admitted claims

- `TC-OPS-001`: exact admitted M01 source and M02 projection produce the M03 envelope consumed by the existing M00 paper run.
- `TC-OPS-002`: SQLite state and receipts survive a true separate Python process.
- `TC-OPS-003`: validation provider substitution is hermetic and does not claim a network fetch.
- `TC-OPS-004`: missing live broker credentials stop before transport invocation.
- `TC-OPS-005`: the non-editable installed package imports outside the repository under isolated path semantics.

## Lifecycle

The family `tier_c_operational_assurance` is `Tier C/current_nonblocking`, has its own proof block and `make tier-c` route, and is intentionally absent from `alpha_current`.

## Working-tree validation

- `make tier-c` → `5 passed`.
- Affected Tier A regression slice → `75 passed`.
- Complete Tier B shadow → `90 passed`.
- Proof manifest validation → `73 blocks` reconciled.
- Proof authority → `201 families / 203 physical tests / 73 blocks`.
- `alpha_current` remains `19 blocks / 19 families / 21 test paths`.
- Black → `486 files unchanged`; Ruff → zero findings.
- The environment was rebuilt offline from the accepted V6 runtime and V4 dev/build wheelhouses before the installed and separate-process checks.
- No real network endpoint or broker order was used.

## Guardrail retained

The M00/M09 test-support extension accepts an optional already-validated `PreparedDataEnvelope`; default Tier A fixture behaviour is unchanged.
