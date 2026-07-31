# M04 K07 Gate D Validation Summary

## Scope

Source checkpoint: `c9122e9d732f01de5f08af4b366df255270b7d0f`.

Accepted surface: M04-owned DMPV3 K07 packet carriage only. The change enforces
caller/owner-held execution context, producer identity/version, explicit
emission time, the exact role-lineage matrix, owner-executed validation,
truthful diagnostic/rejection targeting and bounded optional degradation.
No payload, domain-decision, state, persistence, live or production authority
is added.

## Acceptance results

| Check | Result | Evidence |
|---|---|---|
| Admitted K07 proof | PASS — 271/271 | `PROOF_BLOCK_M04_K07.txt` |
| K07 plus retained admitted partial case | PASS — 272/272 | `TARGETED_AND_ADMITTED_PROOF.txt` |
| Proof-block manifest | PASS — 53/53 | `PROOF_BLOCK_CHECK_ALL.txt` |
| Affected packet shadow | 78 passed / 64 failed; all failing nodes pre-existed and are classified | `AFFECTED_PACKET_TESTS.txt`, `AFFECTED_SHADOW_CLASSIFICATION.tsv` |
| Tier A shadow | 1,312 passed / 271 failed | `FULL_SUITE_SHADOW_TIER_A.txt` |
| Source Tier A shadow | 1,307 passed / 272 failed | `BASELINE_C9122_TIER_A_SHADOW.txt` |
| Tier A delta | zero new failing nodes; one resolved; four new tests pass | `FULL_SUITE_SHADOW_COMPARISON.txt`, `FULL_SUITE_SHADOW_DELTA.tsv` |
| Tier B shadow | PASS — 49/49 across 13 physical files | `FULL_SUITE_SHADOW_TIER_B_PARTITIONED.txt` |
| Tier C shadow | no tests collected | `FULL_SUITE_SHADOW_TIER_C.txt` |
| Architecture | PASS | `ARCHITECTURE_CHECKS.txt` |
| M04 vocabulary | PASS — zero unresolved candidates across 96 scoped files | `VOCABULARY_STAMP_M04.txt` |
| Global vocabulary shadow | BLOCKED — 50 shared/pre-existing candidates | `VOCABULARY_AUDIT_GLOBAL_SHADOW.txt` |
| Compile/diff/line length | PASS | `STATIC_CHECKS.txt` |
| Repository integrity | PASS | `GIT_FSCK.txt` |
| Pinned Ruff | UNAVAILABLE — mirror HTTP 404 for locked `orjson==3.11.7`; no substitute used | `RUFF_PINNED_CHECK.txt` |

## Source-checkpoint comparison

The current Tier A suite has no failing test node that was absent at the source
checkpoint. One admitted K07 failure is resolved. Four newly added K07 proof
cases pass. Seventy-four pre-existing failing nodes now reject at an earlier or
more exact governed boundary; those reordered reasons are recorded rather than
misreported as newly green legacy compatibility.

## Paused-checkpoint defects corrected before acceptance

1. Named validation checks were represented as successful without executing
   their owner validators.
2. A diagnostic/rejection packet could use an input fingerprint as its only
   purported target reference.
3. Validation ordering masked an admitted missing execution-context failure
   behind a different missing field.
4. Callback type annotations did not match the one-argument runtime contracts.
5. M04-owned canonical-envelope and validation-completeness results were
   constants rather than computations over actual emitted facts.

## Boundary

The global vocabulary shadow and the unavailable pinned Ruff environment are
open external/shared validation conditions. Neither was hidden, suppressed or
substituted. The admitted M04 proof, M04-scoped vocabulary gate, architecture
checks and checkpoint comparison establish the bounded K07 acceptance claim.
