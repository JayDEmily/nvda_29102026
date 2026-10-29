# Project Objective

## Project identity

- **Project ID:** `NVDA-LIFECYCLE-CONTROL-001`
- **Project label:** NVIDIA Project Lifecycle Control
- **Repository role:** project-control repository; not an NVIDIA product-code repository

## Authoritative objective

Establish and operate one formal macro-gated delivery control surface for NVIDIA work, using the accepted Project Lifecycle Methodology (PLM) as the outer lifecycle and invoking bounded NVIDIA specialist methodologies only at the Gate(s) where their authority is required.

The initial specialist chain is:

1. an Implementation Admission method that takes an accepted implementation-ready brief through current normative/architecture authority and produces an independently challenged Bounded Implementation Context Packet (BICP); then
2. a bounded implementation method that consumes an accepted BICP and produces verified bounded implementation without silently changing upstream meaning.

The control repository must keep macro lifecycle authority, specialist-method authority, execution evidence and product-code state distinct rather than merging them into one undifferentiated process.

## Definition of completion

This Project is complete when all of the following are true:

1. Gate 00 and Gate 01 have established an accepted project-control baseline and delivery architecture under the pinned PLM identity.
2. The macro Roadmap identifies when each specialist method is invoked and the exact handoff object required to enter and leave it.
3. A real authorised NVIDIA work item can move from its accepted upstream brief through Implementation Admission and then bounded implementation without a worker having to rediscover the whole NVIDIA corpus or invent missing authority.
4. Each Gate has auditable entry conditions, acceptance conditions, evidence, resulting authority effect and durable Git identity.
5. Specialist methodology rules remain local to their invoked scope and do not silently become universal Project law.
6. Final implementation claims are supported by the proof/review required by the invoked implementation method and by Gate-level composition evidence where PLM requires it.

Completion of this control Project does **not** by itself mean that the entire NVIDIA product/programme is implemented, deployed or commissioned.

## In scope

- project-level PLM Gate governance;
- project objective, guardrails, operator map, roadmap and current execution plan;
- exact pinning of governing methodology/source identities;
- selection and invocation of NVIDIA specialist methods;
- handoff contracts between macro Gates and specialist methods;
- bounded control/evidence state needed to execute and review Gates;
- provenance sufficient to reconstruct why a Gate was entered, accepted, blocked or superseded.

## Out of scope

- rewriting either specialist methodology merely to fit the macro lifecycle;
- treating the sample/current NVIDIA implementation run as proof that a reusable method is universally correct;
- NVIDIA product semantics not supplied by authoritative upstream material;
- product code during Gate 00 or Gate 01 bootstrap work;
- deployment, production commissioning or live trading/external effects unless separately authorised by later Project authority.

## Current material unknowns

- The supplied VI-06 repository is a concrete BICP-to-implementation workspace and current operationalisation of the successor method. Whether it is the exact reusable specialist-method source to pin for future runs, or evidence from which a separate reusable method repository should be selected, is not yet established in this Project.
- No separate PCM repository/version was supplied with the three current source repositories. Until one is explicitly pinned, this Project uses the frozen project-local control profile in `control/CONTROL_PROFILE.md` only where PLM permits an explicitly equivalent control mechanism.

## Change authority

Changing this objective or its Definition of Completion requires explicit current Programme Owner/user authority. An `EXEC_PLAN.md`, worker, reviewer, test or specialist method cannot change it.
