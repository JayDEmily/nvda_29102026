# Review-cycle request

**Status:** `ACTIVE`

## Cycle identity

- **Cycle:** `TESTER_VI17_L1_1790601177`
- **Current actor:** `TESTER`
- **Leaf:** `VI-17-L1 — authority and lineage reconstruction`
- **Exact Worker candidate:** `c07d5277512f600669b05a88cc2c174af3e3b046`
- **Exact candidate tree:** `5a156a0170bb31ab2253822a9cf3172bd610f5fe`
- **Worker audit-packet preparation commit:** `2f4fa4f199a18e55865babf9667da14ad23987fc`
- **Accepted VI-16 candidate:** `9248f3b1788f8e99e59a0482c4cc393c27942715` / tree `5560c97ad83a05190603c323eb4fbfa0c21d983d`
- **VI-16 Tester PASS:** `9f5f7e90b463365fb39c361f2e346d9e67c6d915`
- **Accepted package candidate:** `332c1f95da032f841e8779ef21fe3c1fceb698a2` / tree `3abec93134d128978ad6bcedbd0dfa6cf4334ec6`
- **Accepted wheel SHA-256:** `d311960234c932c2507f7b1671c8d53bff3ec234692e65ca27b440293e37e127`
- **Accepted sdist SHA-256:** `135e47f6ab531e8e650a2ee1adc9582965e1c81d97d08dfdc854757a790629fa`

## Mandatory readback

Read root `README.md`, full `GUARDRAILS.md`, root `AGENTS.md`, complete accepted `EXEC_PLAN.md`,
`handoff/control/CURRENT_STATE.md`, this request, applicable nested test instructions, accepted BICP/IRB, implementation
authorisation, fixed IWO, VI-04 authority closure, VI-06 blocked-review/Programme-Owner-direction records, explicit later
authority additions, VI-08 architecture admission, product/architecture proof-control registrations, accepted U01-U06
implementation/review/promotion evidence, VI-14/VI-15/VI-16 acceptance evidence, current source/configuration and exact
package artefacts.

The Worker map is evidence to challenge, not a substitute for reconstruction. Review the exact frozen candidate, not
the later routing tip.

## Tester proposition

Independently reconstruct exactly `c07d5277512f600669b05a88cc2c174af3e3b046` / tree `5a156a0170bb31ab2253822a9cf3172bd610f5fe` under section 9 of the accepted ExecPlan and decide
whether authority-to-final-candidate lineage is independently reproducible with no material gap or unauthorised semantic
mutation. At minimum:

1. recompute/rebind the fixed BICP, IRB, VI-04, IWO and distribution-authority identities;
2. preserve the exact VI-06 fact pattern: the independent IWO review remained `BLOCKED`, while later explicit Programme
   Owner direction authorised proceeding with the fixed IWO for this run; do not silently convert the blocked review to PASS;
3. independently identify and assess each material post-root authority addition, including Raw Signal catalogue carriage,
   U03 recurrence/lineage/domain/static-typing authority and VI-15 distribution metadata authority;
4. reconstruct the active Git boundary: current local history roots at `8133432ba8a07e4d04d83b14af5c3c4bd12e6b0e`;
   recorded external predecessor `d095954c16a9818eadb60d6364148229f2dc4558` is not present as a local Git object. Determine
   independently whether the primary thin-transport/recovery evidence makes that explicit provenance bridge sufficient or
   whether it is a material authority/lineage gap; never represent the external identity as local ancestry;
5. reconstruct architecture admission, durable registry/allocation, semantic owner, dependency direction and public seam;
6. reconstruct product and architecture proof obligations, family memberships, successor/forbidden obligation status and
   accepted proof lineage;
7. independently verify exact U01-U06 candidate/review/promotion ancestry plus VI-14, VI-15 and VI-16 accepted lineage;
8. audit net substantive changed paths against the governing authority for each accepted implementation/package tranche;
9. inspect authority-path Git history and determine whether any semantic authority was silently mutated or invented;
10. trace accepted authority -> IWO -> proof -> source/configuration -> exact package candidate and package bytes;
11. verify no substantive `src/**`, `tests/**`, `config/**` or `pyproject.toml` drift from accepted package candidate
    `332c1f95...` through the exact VI-17-L1 candidate;
12. verify the accepted wheel/sdist hashes and relevant inventory/source-byte binding;
13. verify candidate cleanliness, ancestry and Git integrity.

Do not repair the candidate in the Tester role. Any material repairable defect is `FAIL / RETURN_TO_WORKER`; an
irreconcilable authority gap is `BLOCKED`.

## Permitted disposition

The VI-17-L1 Tester verdict is exactly one of:

- `PASS`
- `FAIL / RETURN_TO_WORKER`
- `BLOCKED`

On `PASS`, record the exact independent disposition and route a subsequent Worker for preserved-ancestry VI-17-L1
promotion/close-out. Do not begin VI-17-L2 in the Tester role.
