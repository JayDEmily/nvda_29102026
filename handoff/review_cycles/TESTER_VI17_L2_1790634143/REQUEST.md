# Review-cycle request

**Status:** `ACTIVE`

## Cycle identity

- **Cycle:** `TESTER_VI17_L2_1790634143`
- **Current actor:** `TESTER`
- **Leaf:** `VI-17-L2 — provenance, environment and repository-integrity audit`
- **Exact Worker candidate:** `57712201296c6da811e4e6838d0f3fb302239df4`
- **Exact candidate tree:** `1b017b6c01176fc61963a63bcf12d843aac8d0db`
- **Worker audit-packet preparation commit:** `98c345809694883fe9493f588e87ed815b75996b`
- **Accepted VI-17-L1 candidate:** `c07d5277512f600669b05a88cc2c174af3e3b046` / tree `5a156a0170bb31ab2253822a9cf3172bd610f5fe`
- **VI-17-L1 Tester PASS:** `5397a90dd2e245e17bd5e0eb526861396dae3082`
- **VI-17-L1 promotion close-out:** `d37e5951560d1f1a2b2704888b2b2e15002288f5`
- **Accepted package candidate:** `332c1f95da032f841e8779ef21fe3c1fceb698a2` / tree `3abec93134d128978ad6bcedbd0dfa6cf4334ec6`
- **Accepted distribution:** `nvda-architecture-kernel==1.0.0`
- **Accepted wheel SHA-256:** `d311960234c932c2507f7b1671c8d53bff3ec234692e65ca27b440293e37e127`
- **Accepted sdist SHA-256:** `135e47f6ab531e8e650a2ee1adc9582965e1c81d97d08dfdc854757a790629fa`
- **Preserved proof-bootstrap SHA-256:** `01050287798e53e38f33794e201df53adbe6fcba03024a027ac36d3d9cea66b8`
- **Preserved PostgreSQL-runtime SHA-256:** `59822410ac6855365c90765de5071182ab382e87d9e9a2622424e7787c4e5caf`

## Mandatory readback

Read root `README.md`, full `GUARDRAILS.md`, root `AGENTS.md`, complete accepted `EXEC_PLAN.md`,
`handoff/control/CURRENT_STATE.md`, this request, applicable nested test instructions, the exact VI-17-L2 Worker evidence,
accepted VI-15-L2 Worker/Tester package evidence, accepted VI-16 whole-BICP evidence, accepted U05 PostgreSQL proof
evidence, current package artefacts, preserved proof-bootstrap/PostgreSQL runtime receipts and manifests, current
architecture/product proof registrations, and Git history/integrity evidence required by this leaf.

The Worker audit is evidence to challenge, not a substitute for independent verification. Review the exact frozen
candidate `5771220...`, not the later routing tip.

## Tester proposition

Independently review exact candidate `57712201296c6da811e4e6838d0f3fb302239df4` / tree
`1b017b6c01176fc61963a63bcf12d843aac8d0db` under VI-17-L2 section 9 of the accepted ExecPlan and decide whether one
provenance/integrity state is sufficient for final freeze without an unresolved identity, environment, package or
repository-integrity gap. At minimum:

1. independently hash and inventory the supplied wheel/sdist and verify their distribution name/version, sizes and
   metadata against the accepted package candidate;
2. independently bind wheel runtime bytes and repository-backed sdist members to exact package candidate `332c1f95...`;
3. independently reconstruct the external dependency/build-toolchain identities used for accepted build/proof/install
   and preserve the boundary between exact recorded provenance and any stronger reproducible-build claim;
4. independently rebind the preserved proof-bootstrap and PostgreSQL-runtime archive hashes and inspect their internal
   integrity/identity evidence; assess the explicitly recorded PyYAML 6.0.3 overlay limitation rather than silently
   upgrading it to a fully self-contained environment-reproduction claim;
5. independently verify PostgreSQL 17.9 proof-environment identity and the accepted UTF8 / `fsync=on` /
   `synchronous_commit=on` / `full_page_writes=on` / Unix-socket-only durability configuration, without conflating it
   with the earlier SQL_ASCII transfer-validation cluster recorded in the portable-runtime receipt;
6. independently bind the final product and architecture aggregate results to their exact reviewed candidates and check
   that later source/proof/config/dependency bytes do not detach those results from the final state;
7. independently verify the accepted external installed-package proof identity, including package-only import origin,
   exact wheel binding, PostgreSQL-backed A00/M00 challenge and inactive-capability exclusion;
8. inspect current architecture/product registrations and verify inactive P01/K01 and other unadmitted capability
   closure against actual package/runtime inventory;
9. verify candidate cleanliness, `git diff --check` and suitable Git integrity checks;
10. independently verify reachable ancestry for all accepted U01-U06 and VI-14/VI-15/VI-16/VI-17-L1
    candidate/review/promotion identities, preserving the accepted thin-root/external-predecessor boundary;
11. verify absence of unreviewed `src/**`, `tests/**`, `config/**` or `pyproject.toml` drift after the accepted package
    candidate and through this exact VI-17-L2 candidate;
12. assess whether the recorded recovery/resumability prerequisites are sufficient for later VI-18 terminal artefact
    creation without creating or accepting that VI-18 artefact in this Tester leaf.

Do not repair the candidate in the Tester role. Any material repairable defect is `FAIL / RETURN_TO_WORKER`; an
irreconcilable authority/provenance/integrity gap is `BLOCKED`.

## Permitted disposition

The VI-17-L2 Tester verdict is exactly one of:

- `PASS`
- `FAIL / RETURN_TO_WORKER`
- `BLOCKED`

On `PASS`, record the exact independent disposition and route a subsequent Worker for preserved-ancestry VI-17-L2
promotion/close-out. Do not begin VI-18 in the Tester role.
