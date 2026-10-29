# Review-cycle request

**Status:** `ACTIVE`

## Cycle identity

- **Cycle:** `WORKER_VI15_L2_1790582161`
- **Current actor:** `WORKER`
- **Leaf:** `VI-15-L2 — complete aggregate promotion and truthful package/install proof`
- **Accepted predecessor:** VI-15-L1 promotion close-out on `main` at `abccadf20d10daa29e739c6ba54a970fcff41614`
- **Authorised distribution:** `nvda-architecture-kernel==1.0.0`

## Mandatory readback

Read root `README.md`, full `GUARDRAILS.md`, root `AGENTS.md`, complete accepted `EXEC_PLAN.md`,
`handoff/control/CURRENT_STATE.md`, this request, `implementation/proof/VI15_L1_PROMOTION_EVIDENCE.md`,
`implementation/authority/VI15_L1_FINAL_DISTRIBUTION_AUTHORITY.md`, the independent VI-15-L1 Tester
disposition, current `pyproject.toml`, `Makefile`, package/build configuration, proof-control configuration,
and any nested `AGENTS.md` / `AGENTS.override.md` that applies to files touched or proof surfaces used.

## Authorised action

Execute only VI-15-L2 under section 7 of the accepted ExecPlan, on one work branch from the accepted
VI-15-L1 `main` state:

1. establish the complete product blocking set as one separately attributable proof axis;
2. establish the complete architecture/bootstrap blocking set as a separate proof axis;
3. fail closed on red, incomplete or unauthorised skipped coverage;
4. build the configured wheel and sdist from the exact clean committed candidate state;
5. inventory and inspect wheel/sdist contents;
6. install the built distribution into an environment outside the repository/source tree with no
   repository path injection or source-tree substitution;
7. prove the installed distribution exposes the admitted Raw Signal Occurrence Truth/A00 behaviour
   required by the package proposition;
8. prove unadmitted/inactive capability is absent from the installed distribution or otherwise remains
   lawfully inactive under current authority;
9. record exact package filenames, byte sizes and cryptographic hashes;
10. record the exact build/proof toolchain and environment identities bearing on provenance;
11. freeze one exact VI-15-L2 candidate and route it to a fresh independent Tester.

Do not broaden product semantics, owner identity, module admission, dependencies, PostgreSQL authority
or inactive capability merely to make packaging convenient. Do not begin VI-16 in this cycle.

Stop at the first unmet invariant required by the ExecPlan, including a red/incomplete blocking axis,
source-tree/path-injected install proof, package identity mismatch, inactive-capability activation or
required evidence that cannot be established.
