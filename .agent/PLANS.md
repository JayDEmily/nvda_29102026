# Codex Execution Plans (ExecPlans)

This file defines the standing requirements for task-specific ExecPlans in this repository. It is not an ExecPlan and does not prescribe the solution to the current task.

## When to use an ExecPlan

For complex, multi-step, architectural, or semantic work, inspect the repository and live environment in Plan mode before substantive changes, then create one root `EXEC_PLAN.md`.

The ExecPlan governs the local engineering sequence. It must remain subordinate to `AGENTS.md` and the repository authorities identified there.

## How to use an ExecPlan

Treat `EXEC_PLAN.md` as a living, self-contained document. Keep it accurate as work progresses, discoveries are made, decisions change, and validation is performed. A future worker should be able to resume safely from the repository and the current ExecPlan without needing the earlier conversation.

Do not ask the user for routine next steps while executing an authorised plan. Resolve ordinary engineering ambiguities and tooling problems autonomously. If a genuine authority, protected trust/security, or irreducible UI boundary is reached, record the blocker precisely and escalate it.

Do not pre-decide implementation mechanisms merely because they existed in earlier work. Investigate first and choose the smallest adequate mechanism for the demonstrated need.

## Required contents

Every ExecPlan must contain:

### Purpose / Big Picture

State the outcome, why it matters, and what observable result will demonstrate success.

### Current State

Orient the reader to the relevant repository areas, current Git state, live environment assumptions, and facts established by inspection.

### Scope

State what the plan will change and what it will deliberately leave alone.

### Plan of Work

Describe milestones in dependency order. Each milestone must produce an observable result and state how that result will be checked. Name concrete files and commands only after inspecting the repository.

### Progress

Maintain a dated checklist that reflects the actual current state at every stopping point.

### Surprises & Discoveries

Record material observations discovered during execution. Distinguish observed facts from hypotheses or proposed explanations.

### Decision Log

Record consequential local engineering decisions and the reasoning for them.

### Validation

State the inspections, commands, tests, reviews, or behaviours that support completion claims, together with the limits of that evidence.

### Outcomes & Retrospective

At closeout, state what changed, what was demonstrated, what remains unresolved or `Unknown`, and the final Git state.

## Plan quality

An ExecPlan must be specific enough to execute and resume, but no longer than needed to preserve intent, decisions, progress, and proof. It is a working engineering document, not a receipt ledger.

Prefer observable outcomes over process ceremony. Prefer ordinary Git and workspace recovery over new control infrastructure. Revise the plan when evidence invalidates an assumption rather than forcing the implementation to match the old plan.

## Freeze

This file is the standing ExecPlan standard and is frozen. Do not modify `.agent/PLANS.md` unless the user explicitly reopens it. The task-specific `EXEC_PLAN.md` is the living document Codex creates and updates.
