# Gate 01 — Delivery Architecture and Initial Decomposition

## Contract identity

- **Gate ID:** `G01`
- **Contract revision:** `G01-R2`
- **Label:** Delivery Architecture and Initial Decomposition
- **Lifecycle state:** `DEFINED`

## Objective

Establish the bounded delivery architecture for this Project so the first substantive NVIDIA Gate can enter controlled execution without its workers rediscovering Project governance, specialist-method boundaries or the handoff chain.

## Entry criteria

- `G00 — Project Establishment` is accepted.
- Accepted G00 payload is commit `49fdc3bc3d7714079a21ade97ac3e824c7881b47`, tree `dc72a5ef25f227964b03e3720c6f092e680ee42d`.
- PLM commit `443e4870df9fe8b63f6ad6471e02508d78be6974` remains governing.
- Project-local bounded control profile v0.1 remains frozen and available for G01 Leaves.

## Delivery shape

`LINEAR` for the initial governed NVIDIA path:

`existing Implementation Admission result -> macro adoption/acceptance of exact BICP -> CODE-001 methodology qualification -> accepted CODE-001 run -> verified bounded implementation`

This does not assert that the entire NVIDIA programme is linear; it defines the first currently evidenced Project path only.

## Major modules / workstreams

1. **Lifecycle control** — this repository; owns macro Gate sequencing, exact method selection, Gate contracts, handoffs and acceptance records.
2. **Implementation Admission** — specialist decomposition method; consumes one exact authorised implementation-ready brief and produces one independently challenged accepted BICP.
3. **Bounded Implementation / CODE-001** — successor specialist method; consumes one exact accepted BICP and exact admitted architecture baseline, then derives proof and implementation through its own bounded gates.
4. **NVIDIA product/architecture repositories** — authoritative runtime/architecture state when a substantive Gate binds them; never treated as part of this control repository by implication.

## Major ordering / dependencies

1. G00 acceptance precedes G01 execution.
2. G01 must bind the specialist-method identities and first substantive Gate contract before G02 can become `READY`.
3. G02 must reconcile/adopt the exact existing Implementation Admission terminal result and establish whether BICP-CANDIDATE-005 is authorised as the macro-project downstream payload.
4. G03 must complete/qualify CODE-001 methodology authority before a product implementation run may be authorised.
5. G04 may execute the accepted CODE-001 method only from the exact G02-accepted BICP and its bound architecture baseline.
6. CODE-001 may not cross its code boundary until its own governance, proof and independent-review preconditions are satisfied.
7. Any BICP Remaining Unknown that becomes implementation-blocking returns to the lawful owning authority; implementation convenience cannot settle it.

## Architecture / domain boundaries

- PLM owns macro lifecycle semantics only.
- This control repository owns Project-level sequencing and evidence routing only.
- Implementation Admission owns brief-to-BICP projection only; it does not issue an implementation work order or product code.
- CODE-001 owns accepted-BICP-to-bounded-implementation process only; it does not re-author upstream semantics.
- NVIDIA architecture/normative sources remain authoritative only within their declared jurisdictions when an exact substantive Gate binds them.

## Environment / dependency strategy

No product runtime/build environment is frozen by G01. Product environment and dependency identities are bound by the substantive Gate and specialist method when evidence justifies them.

Project-control execution requires only a recoverable Git repository plus the exact source/method artefacts named by the active Gate.

## Verification strategy

Across this Project:

- exact identities are mechanically checked where load-bearing;
- semantic claims are checked against primary authority, not summaries;
- independent challenge is used where the invoked specialist method requires it;
- proof design, execution, adequacy and pass state remain distinct;
- Gate closeout consumes current valid Leaf evidence and adds composition evidence only where the Gate objective requires it;
- accepted handoff payload identity is kept distinct from transport/package identity where separable.

## Role model

- **Programme Owner/user:** reserved objective/governance changes, new semantic authority, required human acceptances and protected/irreversible actions.
- **PM:** Gate definition, bounded decomposition, specialist-method selection, routing, evidence reconciliation and closeout.
- **Worker:** one bounded authorised execution unit only.
- **Independent Reviewer:** source-first independent challenge where required; does not repair the candidate it is reviewing.

## Specialist methods

### Implementation Admission

Selected source candidate:

- package: `NVDA_IMPLEMENTATION_ADMISSION_FINAL_ACCEPTED_FULL_GIT_20260919.tar(1).gz`;
- package SHA-256: `9e23177ceb3407acd137f56e1ff3ae4fc3b91eb3a431da5295f8e02deaf377a7`;
- repository commit: `f64cf4c3f04e8e02ea368defb6d89d0f3ed0df7b`.

Observed terminal boundary: independently challenged accepted BICP, then STOP before Implementation Work Order, product tests or product code.

### CODE-001 bounded implementation

Reusable methodology source now located:

- package: `NVDA_CODE_001_BICP_TO_CODE_METHOD_FULL_GIT_20260919.tar(2).gz`;
- package SHA-256: `f7b2a53a5c7abff9322e8fc216d571266a1de9919902b536d81f1e79d80663cb`;
- branch: `main`;
- repository commit: `e580ee4450c51e98d254f9604708ee34a4912e66`;
- tree: `f0f36444b13b6952e1e66974cac3698e63c858d4`;
- methodology file status: `PROPOSED DESIGN V0`;
- repository ExecPlan status: methodology formalisation only; independent methodology challenge not yet completed.

Therefore CODE-001 is the correct reusable successor-method candidate, but **is not yet accepted specialist-method authority for a product implementation run**. G01 must preserve that distinction.

### VI-06 repository

`NVDA_VI06_COMPLETE_HANDOFF_20260919.tar(1).gz` is retained as concrete operational/reference-run evidence. It is not used as the reusable CODE-001 methodology authority now that the separate CODE-001 methodology repository is identified.

## Initial roadmap horizon

- **Current:** G01 — establish delivery architecture and first lawful handoff.
- **Next:** G02 — reconcile and adopt the existing Implementation Admission terminal result/BICP as an exact macro-project downstream input.
- **Near future:** G03 — complete independent challenge/freeze/Programme Owner acceptance of the reusable CODE-001 methodology.
- **Following:** G04 — execute the accepted CODE-001 method against the exact G02-accepted BICP to verified bounded implementation.
- **Distant:** created only as evidence justifies; no speculative full-programme Gate sequence is frozen here.

## Leaf set / decomposition status

- `G01-L01` — establish delivery shape, boundaries and ordering. **CANDIDATE COMPLETE** in this contract.
- `G01-L02` — bind specialist source identities and distinguish accepted authority from candidate methodology. **CANDIDATE COMPLETE** in this contract and `METHOD_PINS.md`.
- `G01-L03` — establish Project verification/evidence strategy and role model. **CANDIDATE COMPLETE** in this contract.
- `G01-L04` — define the first substantive G02 adoption Gate contract and exact PLM -> bounded-control handoff. **NOT STARTED**.
- `G01-L05` — G01 closeout check and Programme Owner acceptance. **NOT STARTED**.

No NVIDIA product implementation is authorised by these Leaves.

## Gate-level evidence

- accepted G00 payload and acceptance record;
- pinned PLM source;
- exact Implementation Admission source above;
- exact CODE-001 methodology candidate source above;
- VI-06 concrete reference-run evidence where needed to test the successor-method design against observed execution behaviour.

## Known unknowns / blockers

1. CODE-001 V0 is not yet independently challenged/frozen/accepted as reusable specialist-method authority.
2. The IA-24 files themselves still contain terminal-gate-pending wording even though the supplied repository `main` points at the IA-24 closeout commit. Macro adoption must therefore make the acceptance basis explicit instead of inferring it from branch placement or package naming.
3. Product baseline/runtime identities belong to G02/G04 binding and are intentionally not frozen here.

These do not block G01 planning. They block G03 `READY` or later product implementation where applicable.

## Frontier references

- `F-G01-001`: exact macro acceptance status of the existing IA-24/BICP handoff.
- `F-G01-002`: CODE-001 V0 acceptance status for reusable implementation use.

## Result / handoff object

If accepted, G01 produces:

- accepted delivery-architecture record;
- accepted specialist-method routing and identity status;
- first substantive G02 existing-handoff adoption Gate contract/ExecPlan;
- exact bounded-control handoff sufficient to start G02 without rediscovery of Project governance.

## Downstream consumer

`G02 — NVIDIA Implementation Admission`.

## Authority effect

`AUTHORISED_DOWNSTREAM_INPUT` limited to the exact accepted G02 Gate contract and handoff. G01 acceptance does not itself authorise product code.

## Handoff identity structure

- payload: accepted G01 delivery-architecture + G02 contract/binding state;
- wrapper/transport: any tarball/archive used to move that state, tracked separately where material.

## Risk/decomposition disposition

`ADEQUATELY_BOUNDED` for G01. The Gate changes control/routing state only and explicitly excludes product mutation.

## Composition requirement

`NONE` for G01 unless G01-L04 introduces interacting artefacts whose consistency cannot be established directly from the final Gate state.

## Change conditions

Re-open or revise G01 architecture planning only if a load-bearing change occurs in:

- Project objective/governance;
- accepted PLM identity;
- selected specialist-method boundary;
- handoff semantics between Implementation Admission and CODE-001;
- evidence showing the initial linear delivery shape is no longer valid.

## Exit criteria

G01 may be proposed for acceptance only when:

1. delivery shape, major boundaries and ordering are explicit;
2. specialist methods and their current authority status are exact;
3. verification/evidence and role model are explicit;
4. first substantive G02 Gate is sufficiently defined and exactly bound to enter bounded control without whole-corpus rediscovery;
5. no unresolved G01 issue is silently converted into product authority.
