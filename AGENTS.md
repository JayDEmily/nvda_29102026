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

## Planning

There is no separate normative `PLANS.md` role in the target governance model.

The root `EXEC_PLAN.md`, once explicitly accepted for the current tranche, is the single active planning document. It contains the current gates, leaves, dependencies, acceptance conditions, progress, discoveries, deferred work and close-out evidence. It cannot create or override `GUARDRAILS.md` or accepted domain authority.

## Repository navigation and validation

Use repository-native entry points rather than inventing parallel workflows. Inspect `README.md`, `Makefile`, `pyproject.toml`, relevant architecture/normative documents, schemas and tests before choosing commands or changing structure.

Run only validations that actually bear on the proposition being changed, plus any mandatory checks imposed by applicable instructions or the accepted ExecPlan. Record the commands and observed results; do not report a check as run if it was not run.

Do not modify `GUARDRAILS.md` during ordinary work. Any proposed guardrail change requires explicit current human/programme authority.
