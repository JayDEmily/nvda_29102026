# M13 Implementation Repair V1 — Independent PM Audit Receipt

Date: 2026-07-27 (Australia/Melbourne)
Repository: JayDEmily/Nvda11
Authoritative base: review/m13-proof-v8 at df17277247e4d68c260318e6306d4788de410a4c
Worker branch: work/m13-state-kernel-implementation-repair-v1
Worker commit: 616fade4123def7870b7950bb3e644ffcc0ccc5a

## Independent source reconstruction

The accepted V7 Git bundle was cloned locally at exact base commit df17277. Only the two production patches from worker commit 616fade were applied.

Resulting Git blob IDs:

- contracts.py: 6b0629ea9de66d5bf5bd12c6e6aa830ec86dc4f6
- in_memory.py: 5778b73df5e111aba882657dfaa67ce7de508d35

These exactly match the blobs fetched from GitHub at 616fade.

Frozen proof SHA-256:

- a3ad3e8b51e2dd73119ecbec2e546f8d4e594346efaa8bf588c90b67798b8843

## Independent validation

- M13 proof: 152 passed
- Persistence Tier A: 188 passed
- Proof blocks: PASS, 52
- Proof executor: 21 passed
- Checkpoint shadow: 2 passed
- Architecture boundary: PASS
- Vocabulary exact parity: 1 passed
- YAML parsing: PASS, 10 files
- Python compilation: PASS
- git diff --check: PASS
- Ruff and Black: not installed in the PM runtime; worker outputs were inspected instead

## Independent source-derived mutation campaign

Six mutants were created from the exact repaired source. Every mutant failed both the complete M13 family and its designated target without collection or interface errors:

1. no active-attempt guard — PASS rejection
2. module-global active-attempt guard — PASS rejection
3. guard installed after mutation starts — PASS rejection
4. guard cleared before participant commit — PASS rejection
5. receipt scope checks only command type — PASS rejection
6. resulting version accepts float/bool — PASS rejection

## Independent repository-shadow comparison

The same Linux environment was used for both exact base and repaired source:

- baseline failures: 105
- repaired failures: 61
- resolved failures: 44
- resolved set equals all and only M13 expected-red failures: true
- new failures: 0

The worker's Windows run reported 107 to 63. The absolute count differs by two because of environment-specific shadow behaviour, but both comparisons establish the same controlled delta: exactly 44 M13 failures resolved and no new failures within a like-for-like environment.

## Disposition

PASS — M13-IMPLEMENT-REPAIR-V1 is independently accepted at commit 616fade4123def7870b7950bb3e644ffcc0ccc5a.

This receipt does not merge to main or open M01. Canonical PM control closeout remains the next repository gate.
