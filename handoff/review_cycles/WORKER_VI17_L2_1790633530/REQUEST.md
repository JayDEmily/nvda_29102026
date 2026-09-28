# Review-cycle request

**Status:** `ACTIVE`

## Cycle identity

- **Cycle:** `WORKER_VI17_L2_1790633530`
- **Current actor:** `WORKER`
- **Leaf:** `VI-17-L2 — provenance, environment and repository-integrity audit`
- **Accepted predecessor:** VI-17-L1 promotion close-out on `main` at `d37e5951560d1f1a2b2704888b2b2e15002288f5` / tree `31f6d6fa107633716996d135e479bd0a058fb76a`
- **Accepted VI-17-L1 candidate:** `c07d5277512f600669b05a88cc2c174af3e3b046` / tree `5a156a0170bb31ab2253822a9cf3172bd610f5fe`
- **VI-17-L1 Tester PASS:** `5397a90dd2e245e17bd5e0eb526861396dae3082`
- **Accepted package candidate:** `332c1f95da032f841e8779ef21fe3c1fceb698a2` / tree `3abec93134d128978ad6bcedbd0dfa6cf4334ec6`
- **Accepted wheel SHA-256:** `d311960234c932c2507f7b1671c8d53bff3ec234692e65ca27b440293e37e127`
- **Accepted sdist SHA-256:** `135e47f6ab531e8e650a2ee1adc9582965e1c81d97d08dfdc854757a790629fa`

## Mandatory readback

Read root `README.md`, full `GUARDRAILS.md`, root `AGENTS.md`, complete accepted `EXEC_PLAN.md`,
`handoff/control/CURRENT_STATE.md`, this request, VI-17-L1 Worker/Tester/promotion evidence, accepted VI-15 package evidence,
VI-16 whole-BICP evidence, current package artefacts, proof/build/runtime environment evidence, PostgreSQL proof-environment
evidence, current architecture/product proof registrations, and Git history/integrity evidence required by this leaf. Read any
applicable nested `AGENTS.md` / `AGENTS.override.md` for files inspected or changed.

## Authorised action

Execute only VI-17-L2 under section 9 of the accepted ExecPlan:

1. audit and record final package hashes/inventories and final distribution identity;
2. audit external dependency and toolchain identities used for accepted proof/build;
3. audit PostgreSQL proof-environment identity and relevant durability configuration;
4. bind final product and architecture aggregate results and final package/install proof identity;
5. verify inactive-capability closure;
6. verify repository clean state, `git diff --check`, suitable Git integrity checks, reachable accepted ancestry, and absence of post-review substantive byte drift;
7. record recovery/resumability prerequisites needed for VI-18 without creating the VI-18 recovery artefact in this leaf;
8. make only audit/provenance/evidence mutations; do not repair substantive implementation or authority defects inside VI-17-L2;
9. freeze one exact VI-17-L2 candidate and route it to a fresh independent Tester.

Do not claim reproducible-build identity unless directly established. Do not self-award VI-17-L2 acceptance. Do not begin VI-18 before a fresh Tester PASS and preserved-ancestry promotion of the accepted VI-17-L2 lineage.
