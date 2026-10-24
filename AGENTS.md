# NVDA architecture kernel — agent operating map

## Start here

Before every response to the user in this project thread, reread `GUARDRAILS.md` in full. For substantive repository work, this pre-response reread is mandatory even if the file was read earlier in the same conversation.

Before substantive work in this repository:

1. read `GUARDRAILS.md` in full;
2. read this file in full;
3. read any applicable nested `AGENTS.md` or `AGENTS.override.md` for the files in scope;
4. read the explicitly accepted current `EXEC_PLAN.md` when the task is plan-governed;
5. read the normative, architecture and evidence material required by that task.

Direct current user instruction outranks repository instructions. `GUARDRAILS.md` is the highest repository-level guardrail authority. More-specific nested agent instructions apply only within their scope and may not contradict higher authority.

## Repository role

This repository is the NVDA behaviour-neutral architecture kernel. Do not infer that NVIDIA trading capability, module semantics, gate completion or historical acceptance exists merely because related scaffolding, tests, plans or history are present.

Current or historical programme claims must be established from evidence before they are carried forward.

## Working rules

- Understand the purpose and evidence of inherited work before preserving or changing it.
- Do not treat commit messages, `PASS`/`COMPLETED` labels, green tests, manifests or prior-worker summaries as semantic authority.
- Work only within the current explicit user instruction and, when present, the accepted `EXEC_PLAN.md`.
- Work one semantic acceptance unit at a time unless independence is established.
- Do not weaken tests, validation, authority or evidence requirements to obtain green.
- At the first failed or absent required invariant, stop dependent downstream work and preserve the first failure.
- Report verified facts, inference, unknowns and blockers distinctly. Never promote inference to fact for conversational convenience.
- Do not reject or correct a broader user recollection using only evidence about a narrower subset; establish the scope relationship first.
- Historical/forensic material may be inspected when authorised, but it remains evidence rather than active authority unless explicitly admitted.

### Reviewer lineage and recurrence rule

A fresh reviewer is independent in judgement, not historically blind. Before routing any `FAIL / RETURN_TO_WORKER`, inspect the relevant Git lineage for the current semantic unit far enough to identify prior reviewer findings and the Worker repairs that answered them. Do not use a fixed commit count; follow the semantic lineage needed to decide whether the new failure is isolated or another manifestation of the same mechanism.

Classify the finding before handoff:

- `ISOLATED` — materially new mechanism; route the bounded defect normally.
- `RECURRENT_CLASS` — materially related to prior failures/repairs in the same semantic unit; identify the common mechanism/invariant and route the class-level proposition that must become true, not merely the newest witness.

After a second successive materially related failure in one semantic unit, this recurrence classification is mandatory. If the relevant authority cannot define class-level closure, the reviewer returns `BLOCKED` on the authority gap rather than delegating an impossible or open-ended patch sequence to another Worker. The reviewer may state the required proposition and evidence, but should not prescribe a specific code patch unless authority itself requires that implementation.

### Reviewer fixture-independence rule

Fresh review must also be independent of Worker convenience composition where that composition can hide the semantic distinction under review. When a proposition materially depends on command ordering, optional operations, absence, omission, or a state transition, the reviewer must exercise at least one authority-derived sequence through the declared public seam without relying exclusively on a Worker helper/fixture that bundles multiple semantic operations.

This is a bounded adversarial-review heuristic, not a requirement to duplicate the Worker test suite or proliferate speculative tests. Reuse Worker fixtures where they faithfully isolate the proposition; bypass or decompose them only where their composition could pre-satisfy, mask, or collapse the condition being reviewed. Record the direct sequence and observed result when it bears on disposition.

## Current tranche — D057–D076 authorised execution

Root EXEC_PLAN.md on work/v2-d057-d076-plan-20261024 is the proposed successor from accepted d0a905292c7439aec5bd9f099700f0ac58bdda25. The owner has now accepted the supplied conditional plan and separately authorised execution (“No, I accept it. I authorize. Proceed.”). Prior planning-only restrictions below are historical commission statements; current execution follows root §§3–9/12, with all five holds retained. Earlier D037–D056 and D038/D040/D041 schedules are completed historical evidence, preserved at their exact Git checkpoints. The prior delegation of choices for D040/D041 does not silently extend to this tranche.

Fifteen controlled foundation proposals are specified; D061/D062/D064/D065/D070 retain root §5's explicit missing profile/source/prerequisite/owner conditions. P02 is existing M03; P03 is a distinct proposed event-policy responsibility, not runtime M03 or automatic M02 admission. No numeric owner reservation, new prerequisite D001 implementation or silent deferral is authorised. Numeric execution stops at the first unresolved unit unless owner explicitly dispositions it. The owner has explicitly deferred all five named holds under root §§13–14. Execute D063/D066–D069/D071–D076 in that order, preserving the held requirements; no newly encountered defect is automatically deferred.

After owner acceptance and separate execution commission: exactly two cases per resolved signal, six absolute ceiling not target; one independent final semantic reviewer/sole strict runtime executor, no routine runtime RED, duplicate GREEN, accepted unaffected rerun, speculative probe, hidden scenario loop, broad sweep or whole-branch review. Omitted RED reduces test-first evidence. Substantive source/case discrimination and fixture-independent public actions belong inside the declared pair. Preserve immutable generations/full original output and one verified saved cumulative full-history download after each acceptance before advancing.

Carry forward narrow recovery: only failed check after documented relevant material repair; current new signal's failed strict two-case aggregate may rerun as the same aggregate under the owner's23October16:14 exception. Successful evidence reruns only on documented material invalidation, not packaging/sessions/reviewer changes. No shared runner changes for recovery. Preserve old/new outcomes, defect, affected proposition and repair reason; no automatic regressions.

Use scoped warranted mypy/Ruff only new/changed Python and necessary new-file/owner ingress/import checks. Reuse unchanged authority/family/context/environment verification. No dependency install, requalification or product test for this planning/review task. Full semantic authority remains mandatory; relevant prior inspection may be reused when unchanged. GUARDRAILS.md stays frozen.

The owner expressly permits independent review of this plan, aiming for two rounds while allowing necessary further material repair. This authorises documentary reviewer delegation now, not product acceptance or an extra implementation-review programme.

## Planning

There is no separate normative `PLANS.md` role in the target governance model.

The root `EXEC_PLAN.md`, once explicitly accepted for the current tranche, is the single active planning document. It contains the current gates, leaves, dependencies, acceptance conditions, progress, discoveries, deferred work and close-out evidence. It cannot create or override `GUARDRAILS.md` or accepted domain authority.

## Repository navigation and validation

Use repository-native entry points rather than inventing parallel workflows. Inspect `README.md`, `Makefile`, `pyproject.toml`, relevant architecture/normative documents, schemas and tests before choosing commands or changing structure.

Run only validations that actually bear on the proposition being changed, plus any mandatory checks imposed by applicable instructions or the accepted ExecPlan. Record the commands and observed results; do not report a check as run if it was not run.

Do not modify `GUARDRAILS.md` during ordinary work. Any proposed guardrail change requires explicit current human/programme authority.

Historical exception/delegation and closure records for D038/D040/D041 remain at d0a9052:AGENTS.md and that checkpoint's root plan. The new proposed scope above supersedes those completed schedules without altering accepted source/proof/history.
