# Review evidence

**Status:** `COMPLETE`

## Binding

- role: fresh independent Reviewer 022 / TESTER
- authorised scope: repaired IWO-U01 only; U02 not assessed
- source transport SHA-256:
  `219b29c6204f795d0b075e4eee75bba47e86d122319299376050ed56cebd16b5`
- exact source transport filename:
  `NVDA_G03_TESTER_VI13R_U01_R022_1790117393_FULL_GIT_20260923.tar(1).gz`
- transported repository HEAD before review:
  `2cc4d7c65189aa4ec2048dd77f987e16ff831da0`
- repaired U01 candidate:
  `e8b659d7849d2f95b64ba32bed8090a8290358d4`
- candidate tree:
  `62b074c0e94215a75fb64c5eb934af55be1ded3a`
- Reviewer-021 disposition commit:
  `1637f39980aa3ca476429d85e267a9cb0e575fe5`
- complete repair diff SHA-256:
  `542b3e3a907193774154f2a73bab1a3ebb9af488221e0393e77e6780369b8f6e`
- repair changed exactly:
  `src/nvda_desk/raw_signal_occurrence_truth/api.py`,
  `tests/product/raw_signal/test_u01_contract_owner_boundary.py`, and
  `tests/product/raw_signal/typecheck/public_seam_positive.py`.

## Governing material inspected

Read in full before substantive review: root `README.md`, `GUARDRAILS.md`, root `AGENTS.md`, current
`EXEC_PLAN.md`, `tests/AGENTS.override.md`, active `handoff/control/CURRENT_STATE.md`, active cycle
`REQUEST.md`, and `implementation/handoff/REVIEWER_022_VI13R_U01_REPAIR_REVIEW.md`.

For U01 semantics and repair assessment the review also read the complete accepted IRB, the complete
current IWO, Reviewer-021 disposition, Worker repair evidence, complete Reviewer-021-to-repair diff,
complete current U01 `api.py`, complete U01 proof, support module, and positive/negative static
specimens. No U02 implementation acceptance was assessed.

## Exact candidate validation

Validation ran in a detached worktree at the exact candidate. Exact project-pinned reviewer tools
were provisioned outside the repository from supplied project artefacts:

- Python 3.13.5
- pytest 9.0.3
- mypy 1.20.1 (compiled)
- Ruff 0.15.11

Results after correcting reviewer-environment source-path/dependency setup (the initial direct mypy
and architecture-tool invocations lacked `MYPYPATH`/`PYTHONPATH` and PyYAML in the isolated venv;
those environment-only failures are preserved in `COMMANDS.txt` rather than attributed to the
candidate):

- focused U01 pytest: **297 passed**
- strict positive mypy specimen: **rc 0**
- strict negative mypy specimen: **rc 1 as intended**, with all 15 marked negative sites diagnosed
  at lines 15, 18, 21, 23, 28, 34, 43, 48, 53, 59, 64, 67, 70, 73 and 76
- `python -m mypy src --show-error-codes`: **success; 15 source files**
- Ruff over `src tests tools`: **pass**
- product-proof structural validation: **pass; 6 families, 13/13 obligations**
- architecture validation: **pass; 0 dependency/public-seam violations**
- dependency validation: **pass**
- public-seam validation: **pass**
- `architecture_kernel` promotion: **74 passed**
- candidate `git diff --check`: **rc 0**
- candidate `git fsck --full --strict`: **rc 0**

## Finding closure

### W-U01-F001 — CLOSED

The repaired generic allowed-discriminant constructor makes `receipt_only` coherent by setting
`source_timestamp_raw` absent. Independent runtime challenge also confirmed that `receipt_only`
with a non-absent source timestamp still raises `ValueError`; semantic production law was not
weakened.

### W-U01-F002 — CLOSED

The proof compares normalised/resolved diagnostic paths. The focused pytest suite passes, and direct
pinned mypy independently emits the intended type diagnostic at every one of the 15 marked negative
sites.

### R021-U01-F003 — CLOSED

`_NativeRecordSnapshot` copies the input mapping and returns copied nested values through a read-only
`Mapping` interface. The repaired proof covers mutation of the caller mapping, a nested caller
alias, a nested value returned through the payload, and direct mapping assignment. An independent
focused runtime challenge repeated all four paths and preserved provider-native `None`.

A deliberately broader probe showed that an arbitrary `memoryview` value cannot be deep-copied.
This was not promoted to a U01 finding: no admitted provider mapping or current authority establishes
that Python runtime value class as provider-logical input, and the bounded VI-13R method prohibits
reopening implementation-independent hypothetical hardening without an authority-bearing or
realised-domain defect.

### R021-U01-F004 — CLOSED

The public seam now exports typed factories for concept, contract, policy, eligibility, scope,
capture, observation, assessment, provider, delivery and ingestion-sequence-scope identities. The
positive mypy specimen constructs all five U01 payloads only through
`nvda_desk.raw_signal_occurrence_truth.api`; no underscore/private identity import or annotation
introspection is required. Runtime checks confirm the factories are exported and produce distinct
identity layers.

## Scope challenge

The repair diff is restricted to the three declared U01/proof paths. Current command/read methods
for later behaviours continue to call `_not_implemented("IWO-U02")` through
`_not_implemented("IWO-U05")`. No schedule generation, provider admission mapping, receipt
relation/assessment behaviour, persistence/reconciliation or downstream capability was admitted by
this repair.

## Disposition

**PASS**.

U01 is accepted for lawful promotion. U02 remains prohibited until that promotion has occurred; it
is authorised to begin only after the accepted U01 state is on forward `main`.
