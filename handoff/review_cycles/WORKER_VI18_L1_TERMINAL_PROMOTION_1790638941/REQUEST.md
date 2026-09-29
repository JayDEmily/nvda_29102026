# Review-cycle request

**Status:** `ACTIVE`

## Cycle identity

- **Cycle:** `WORKER_VI18_L1_TERMINAL_PROMOTION_1790638941`
- **Current actor:** `WORKER`
- **Leaf:** `VI-18-L1 — terminal promotion, close-out and STOP`
- **Exact accepted VI-18 candidate:** `3113d10d1c3acb3d077c5c27547ea4caa5b01e7f`
- **Candidate tree:** `f43ed9ae73f1d44b763fbcb94250e5d31e18ce4a`
- **Independent VI-18 Tester PASS:** `905494677d697341b424d57c855fdd999571c7c3`
- **Tester cycle:** `TESTER_VI18_L1_1790637840`
- **Current accepted `main` baseline:** `4df802c3ebe67409125c58655534814f24b9ae2b`
- **Accepted recovery artefact SHA-256:** `156c0e720e69e1a31a307d8751582616f9187c6a3ee6947dfa22c413e840b251`
- **Accepted recovery ref-set SHA-256:** `2ea2adac6e8183ab8ee028c502741a8b28330787c321b75e4bdb7cd0cefd20a2`
- **Accepted wheel SHA-256:** `d311960234c932c2507f7b1671c8d53bff3ec234692e65ca27b440293e37e127`
- **Accepted sdist SHA-256:** `135e47f6ab531e8e650a2ee1adc9582965e1c81d97d08dfdc854757a790629fa`

## Mandatory readback

Read root `README.md`, full `GUARDRAILS.md`, root `AGENTS.md`, complete accepted `EXEC_PLAN.md`,
`handoff/control/CURRENT_STATE.md`, this request, the exact VI-18 Worker candidate evidence, and
`implementation/proof/VI18_L1_INDEPENDENT_TESTER_DISPOSITION.md` before acting.

## Authorised action

This is terminal promotion/close-out only. Do not reopen implementation, proof, packaging or VI-14 through VI-17 work.

1. verify exact candidate `3113d10...` and Tester PASS `9054946...` are descendants of current accepted `main` baseline
   `4df802c...` and that the Tester PASS contains the accepted candidate in ancestry;
2. promote the exact accepted VI-18 candidate/Tester lineage to `main` using preserved ancestry under the existing
   promotion discipline;
3. do not promote this routing-only commit merely because it exists; preserve the accepted Tester PASS lineage as the
   semantic acceptance boundary;
4. make no `src/**`, `tests/**`, `config/**`, `pyproject.toml`, dependency or package-byte change;
5. preserve accepted wheel/sdist hashes and the independently reviewed recovery artefact identity exactly;
6. record the actual resulting terminal `main` commit/tree, accepted candidate/Tester identities, package/recovery hashes,
   Remaining Unknown/non-claim boundary, repository clean/integrity state and STOP disposition;
7. update `EXEC_PLAN.md` progress and `handoff/control/CURRENT_STATE.md` only as required to truthfully record terminal
   closure;
8. verify final repository clean state, `git diff --check`, suitable `git fsck`, and ancestry of the accepted candidate
   and Tester PASS to terminal `main`;
9. produce the final full-Git handoff/recovery packet for the Programme Owner and verify its readback against the final
   terminal Git identity. This final handoff packet does not replace the independently reviewed VI-18 recovery artefact
   SHA-256 above with a new artefact under the same acceptance claim;
10. **STOP**. Do not create a successor implementation leaf, U07, VI-19 or downstream capability cycle.

If terminal promotion cannot preserve the exact accepted ancestry or any substantive byte change would be required, stop
and report the first unmet invariant rather than improvising.

## Required outcome

Record either:

- terminal close-out complete on `main`, with exact commit/tree and STOP; or
- the first blocker preventing exact terminal close-out.

No further Tester cycle is authorised merely for administrative close-out if the Worker makes only the exact
non-substantive terminal records allowed above. Any substantive change makes the VI-18 Tester acceptance stale and must
return for independent review before terminal closure.
