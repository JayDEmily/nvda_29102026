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

## Current tranche — D038, D040 and D041 planning

Root EXEC_PLAN.md on work/v2-d038-d040-d041-plan-20261024 is the proposed successor plan from fc82a07. D037, D039 and D042–D056 are completed controlled profiles; their ledger remains at that Git baseline. D038/D040/D041 remain BLOCKED until exact source/numeric/profile authority and D040/D041 downstream ownership are accepted. Planning does not commission implementation, product tests or missing policy choices. Preserve P02 jurisdiction; do not assign these scores to M02 by convenience.

For later accepted/commissioned work, retain two declared cases per resolved signal, six as absolute ceiling not target; one independent final semantic reviewer/sole runtime executor; no routine RED, duplicate GREEN, accepted unaffected test rerun, speculative probe, broad sweep or whole-branch review. Omitted RED is reduced test-first evidence. Assess discriminatory assertions/public-seam fixture independence within the declared cases, not through extra runs. Scope static checks to new/changed Python. Reuse unchanged family/context/environment inspection, canonical declarations, immutable provenance and concise evidence references.

Relevant material repair permits recovery of only the failed check; successful checks only after material evidence invalidation. The current new signal's failed initial strict pair may rerun as the same aggregate after documented relevant material repair under the carried-forward owner exception, preserving original output/defect/rationale/subsequent result. No retries without repair, accepted-signal reruns or shared runner changes to implement recovery. These rules take effect with acceptance/commission of the new plan; its authority holds cannot be bypassed by a generic execution instruction.

## Planning

There is no separate normative `PLANS.md` role in the target governance model.

The root `EXEC_PLAN.md`, once explicitly accepted for the current tranche, is the single active planning document. It contains the current gates, leaves, dependencies, acceptance conditions, progress, discoveries, deferred work and close-out evidence. It cannot create or override `GUARDRAILS.md` or accepted domain authority.

## Repository navigation and validation

Use repository-native entry points rather than inventing parallel workflows. Inspect `README.md`, `Makefile`, `pyproject.toml`, relevant architecture/normative documents, schemas and tests before choosing commands or changing structure.

Run only validations that actually bear on the proposition being changed, plus any mandatory checks imposed by applicable instructions or the accepted ExecPlan. Record the commands and observed results; do not report a check as run if it was not run.

Do not modify `GUARDRAILS.md` during ordinary work. Any proposed guardrail change requires explicit current human/programme authority.

Current owner exception24October2026: D038 profile at c6737d5 is explicitly accepted and implementation commissioned; the earlier20signal schedule is superseded. Apply current root §9 and owning D038 brief with two cases/sole independent final executor/bounded recovery. D040/D041 authority holds remain. No prior accepted test rerun.

Current owner delegation24October2026 explicitly authorises settling D040/D041 ownership/profile choices and completing both. Root §11 supersedes their earlier approval holds; preserve P02 jurisdiction through lawful new-owner admission. Two cases/sole independent executor/no historical reruns remain mandatory. Exact owning authority must be frozen and bound before implementation.
