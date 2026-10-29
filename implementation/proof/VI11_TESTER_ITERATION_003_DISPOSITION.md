# VI-11 Tester Iteration 003 disposition

## Identity

- tester packet: `NVDA_G03_VI11_TESTER_ITERATION_003_20260920.tar(1).gz`
- tester packet SHA-256: `d4f9313b1dffec900f101ca9f6ba563d65656b0fe2472036491d6d0928dc3141`
- reviewed submission: `e778df15d7a478741cde53ffe8a0373e59e2820e` / tree `4612b37480e5145d769a88cf73590b511273ae1c`
- reviewed VI-10 proof target: `f83efd9b489dbe7072da8c96320504a468c55a1a` / tree `beba36d889696915bbcecccd861dab9ab0c1a4cd`
- tester verdict: `FAIL`
- tester response SHA-256: `74a39cc175d3d34837971b76e78007fd891940ca7a3d5db76af7036a5df9a482`

## Findings accepted for proof-layer repair

1. `T003-F001` CRITICAL — U05 same-process durability/restart false positive.
2. `T003-F002` CRITICAL — test-facing construction glue can substitute semantic implementation.
3. `T003-F003` CRITICAL — assessment outcomes are caller-selected rather than evidence-discriminated.
4. `T003-F004` CRITICAL — U02 policy-version case requires forbidden active-policy overlap.
5. `T003-F005` IMPORTANT — identity-layer substitution matrix absent.
6. `T003-F006` IMPORTANT — v1 compatibility proof overclaims physical discrimination.

## Owning layer and disposition

The accepted `EXEC_PLAN.md` section 6.7 assigns proof inadequacy to the proof layer. No finding requires changing the IRB/BICP, METHOD-006 authority, architecture allocation or production implementation.

The failed proof candidate remains preserved in ordinary Git history. A successor VI-10 proof candidate will repair only proof design/control metadata, proof helpers and physical product tests. VI-12R remains prohibited until a fresh VI-11 reviewer accepts the successor proof candidate.
