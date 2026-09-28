# Review-cycle request

**Status:** `ACTIVE`

## Cycle identity

- **Cycle:** `TESTER_VI18_L1_1790637840`
- **Current actor:** `TESTER`
- **Leaf:** `VI-18-L1 — final freeze and durable recovery artefact`
- **Exact Worker candidate:** `3113d10d1c3acb3d077c5c27547ea4caa5b01e7f`
- **Exact candidate tree:** `f43ed9ae73f1d44b763fbcb94250e5d31e18ce4a`
- **Worker evidence-packet commit:** `da179be52ec16976f2f94347fc7766c17e006b2e`
- **Accepted predecessor / VI-18 routed baseline:** `4df802c3ebe67409125c58655534814f24b9ae2b` / tree `4a15cb1ba7877ee765a395c1d6cd1a986a72cb48`
- **Accepted package candidate:** `332c1f95da032f841e8779ef21fe3c1fceb698a2` / tree `3abec93134d128978ad6bcedbd0dfa6cf4334ec6`
- **Accepted distribution:** `nvda-architecture-kernel==1.0.0`
- **Accepted wheel SHA-256:** `d311960234c932c2507f7b1671c8d53bff3ec234692e65ca27b440293e37e127`
- **Accepted sdist SHA-256:** `135e47f6ab531e8e650a2ee1adc9582965e1c81d97d08dfdc854757a790629fa`
- **Recovery artefact:** `NVDA_G03_VI18_L1_TERMINAL_RECOVERY_FULL_GIT_AND_PACKAGE_20260929.tar.gz`
- **Recovery SHA-256:** `156c0e720e69e1a31a307d8751582616f9187c6a3ee6947dfa22c413e840b251`
- **Recovery bytes:** `5965855`
- **Recovery source/readback ref-set SHA-256:** `2ea2adac6e8183ab8ee028c502741a8b28330787c321b75e4bdb7cd0cefd20a2`

## Mandatory readback

Read root `README.md`, full `GUARDRAILS.md`, root `AGENTS.md`, complete accepted `EXEC_PLAN.md`,
`handoff/control/CURRENT_STATE.md`, this request, the exact VI-18 Worker evidence, accepted VI-14 through VI-17
Worker/Tester/promotion evidence needed to establish prerequisites, accepted BICP/IWO/authority needed to classify
Remaining Unknowns and boundedness, current architecture/product registrations, exact package artefacts, the supplied
recovery artefact and Git history/integrity evidence. Read any applicable nested `AGENTS.md` / `AGENTS.override.md` for
paths inspected.

The Worker evidence is evidence to challenge, not a substitute for independent verification. Review exact frozen
candidate `3113d10...`, not the later Tester-routing tip.

## Tester proposition

Independently review exact candidate `3113d10d1c3acb3d077c5c27547ea4caa5b01e7f` / tree
`f43ed9ae73f1d44b763fbcb94250e5d31e18ce4a` under VI-18 section 10 of the accepted ExecPlan. At minimum:

1. independently establish that VI-14-L1, VI-15-L1, VI-15-L2, VI-16-L1, VI-17-L1 and VI-17-L2 exact candidate/Tester
   prerequisites are accepted ancestors of the VI-18 predecessor/candidate;
2. independently bind the accepted final implementation/package candidate, distribution identity, wheel/sdist filenames
   and hashes to the VI-18 candidate;
3. independently bind final product aggregate evidence (479/479, six families, 13/13 obligations) and architecture
   aggregate evidence (74/74) to their exact independently reviewed result identities and check later drift does not
   stale those results;
4. independently verify that no `src/**`, `tests/**`, `config/**`, `pyproject.toml`, dependency or accepted package-byte
   mutation entered VI-18 after the upstream reviews bearing on those bytes;
5. independently reconstruct the Remaining Unknown list from the accepted IWO plus VI-04/VI-15 closures and decide
   whether the Worker terminal record leaves all still-unresolved matters explicitly unresolved/out of scope rather than
   selecting hidden defaults;
6. independently inspect current architecture/package surfaces and decide whether P01/DMPV3, K01, authoritative replay,
   live provider/network, external effects/accounts, validation/quarantine, D001+, downstream consumers and the other
   recorded unadmitted capability classes remain inactive;
7. independently hash the supplied recovery artefact, freshly extract it, verify its recorded manifest identities,
   branch/HEAD/tree/main, clean state, ref-set digest, `git diff --check`, suitable `git fsck`, accepted package hashes and
   ability to reconstruct the accepted active Git history at the VI-18 routed baseline;
8. specifically challenge the recorded recovery-manifest repair: the superseded archive hash
   `8252286763da8c98b8df0cca589f9785902a3e6021eb1b28ef2dc5c2ac22bacd` must not be treated as accepted; the supplied
   corrected archive must independently validate to SHA-256 `156c0e720e69e1a31a307d8751582616f9187c6a3ee6947dfa22c413e840b251`
   and ref-set SHA-256 `2ea2adac6e8183ab8ee028c502741a8b28330787c321b75e4bdb7cd0cefd20a2`;
9. independently verify the candidate repository is clean, `git diff --check` passes and Git integrity/ancestry is
   sufficient for the terminal bounded claim;
10. preserve the accepted thin-history boundary and PyYAML 6.0.3 overlay provenance limitation; do not upgrade either to
    a stronger claim than the evidence permits;
11. decide whether the exact frozen candidate truthfully records terminal boundedness without claiming production
    commissioning, provider integration, downstream trading capability, full arbitrary-host reproducibility or resolution
    of preserved Remaining Unknowns;
12. record the first unmet invariant if terminal acceptance is not supported.

Do not repair the candidate in the Tester role. Do not promote/close out terminal state in this Tester cycle.

## Permitted terminal disposition

The VI-18-L1 Tester verdict is exactly one of:

- `PASS`
- `FAIL_REPAIRABLE`
- `BLOCKED`

On `PASS`, record the exact independent disposition and route a subsequent Worker terminal close-out/promotion step that
preserves candidate/Tester ancestry and then stops at the bounded-implementation boundary. A Tester `PASS` is necessary
but does not itself perform that terminal promotion.
