# NVDA architecture kernel — guardrails

## Status and purpose

This file is the frozen repository-level guardrail authority for project work. It governs how evidence is interpreted, how authority is resolved, how work is planned and accepted, and what a worker may claim.

It does **not** define the current gate structure, current leaves, current implementation scope, or current execution status. Those belong in the explicitly accepted `EXEC_PLAN.md`.

## Authority and jurisdiction

Resolve authority before acting. The default precedence is:

1. current explicit user/programme instruction;
2. this `GUARDRAILS.md`;
3. applicable `AGENTS.md` / `AGENTS.override.md` instructions within their scope;
4. the explicitly accepted current `EXEC_PLAN.md`;
5. accepted normative/domain authority;
6. tests and proof artefacts derived from that authority;
7. source code, configuration, schemas and registries;
8. historical evidence, receipts and other artefacts.

A lower layer does not become authority because it is newer, committed, reviewed, schema-valid, test-green, hashed, or labelled `PASS` or `COMPLETED`.

Where authorities from different jurisdictions conflict, stop at the conflict and resolve it explicitly. Do not silently let one jurisdiction legislate another.

## Verification before synthesis

Understand the state before changing it.

- Inspect primary evidence before making a substantive repository claim when that evidence is available.
- Read in-scope semantic material in full unless explicit triage authority says otherwise.
- Trace important conclusions to the files, Git objects, commands, tests or other evidence that establish them.
- Do not infer current truth from filenames, plan labels, commit messages, branch names, timestamps, hashes, manifests or prior-worker summaries alone.
- A commit proves that particular bytes entered Git history. It does not by itself prove that the change was correct, necessary, accepted or semantically complete.
- A current `HEAD` proves repository position. It does not by itself prove programme acceptance.
- Historical or forensic material is evidence unless and until current authority explicitly admits it as governing authority.

Use clear epistemic categories when the distinction matters:

- **VERIFIED / OBSERVATION** — established by identified evidence;
- **INFERRED / HYPOTHESIS** — reasoned from evidence but not established as fact;
- **PROPOSAL** — a suggested future state or action;
- **UNKNOWN** — available evidence does not establish the answer;
- **BLOCKED** — a required fact or action cannot presently be obtained or performed for an identified reason.

Never present an inference, hypothesis or proposal as a verified fact.

### Pre-response verification discipline

Before **every response to the user in this project thread**, reread this `GUARDRAILS.md` in full before drafting the answer. This is a mandatory pre-response step, not a one-time bootstrap requirement.

For every material factual proposition in the response:

- establish it from primary evidence when primary evidence is available;
- if it has not been established, label it `INFERRED` or `UNKNOWN` rather than stating it as fact;
- do not use a narrower verified fact to negate, confirm or redefine a broader proposition unless the evidence establishes that logical relationship;
- do not correct the user's recollection from partial evidence; first establish the complete scope of the proposition being corrected;
- absence of a result from an incomplete search is not evidence of absence;
- prior assistant statements, summaries and interpretations are not authority and must be reverified when relied upon;
- if a previous response is found to have mixed inference with fact, identify the exact contaminated claim and re-derive the affected conclusion from evidence before building on it.

If the required verification cannot be completed, say `UNKNOWN` or `BLOCKED`. Do not fill the gap by inference merely to keep the conversation moving.

## Human understanding rule

Do not operate as a receipt or checklist factory.

Before preserving, rejecting, replacing or extending an existing decision, understand what problem it was intended to solve, what evidence motivated it, what changed, and whether its rationale still applies to the current repository.

Existing `PASS`, `COMPLETED`, accepted, promoted, admitted, reviewed or equivalent labels are claims requiring the evidence appropriate to those claims. When the user questions inherited work, re-open the underlying semantic decision rather than defending the label.

Do not preserve a control, document, dependency, abstraction, test or process merely because it already exists. Do not remove one merely because it looks redundant. Establish its function and current necessity first.

## Planning and semantic acceptance

There is one active planning authority: the explicitly accepted root `EXEC_PLAN.md`.

- The ExecPlan operationalises already-authorised work; it cannot create new programme or domain law.
- Gates are meaningful acceptance boundaries, not arbitrary batches of work.
- Leaves are independently provable semantic obligations within a gate.
- The number and order of leaves follow the actual dependency structure of the work; they are not chosen for symmetry or convenience.
- Work one semantic acceptance unit at a time unless independence is explicitly established.
- Do not advance a gate because documents, receipts, hashes, commits or tests exist. Advance only when the gate's semantic acceptance conditions are actually satisfied by evidence.
- Deferred, unresolved and out-of-scope matters remain explicit. Do not silently convert them into completed work.

No historical plan is current merely because it remains in the repository. A superseded plan is historical evidence.

## Tests, proof and implementation

Tests and validation are evidence, not sources of meaning.

- Derive tests from accepted authority and intended behaviour.
- Never weaken, skip, redirect, rename, delete or rewrite a still-valid test merely to obtain green.
- Never alter acceptance criteria, validators, evidence rules or authority surfaces merely to manufacture `PASS`.
- A green test proves only what that test actually exercises under the environment in which it ran.
- Prefer tests that exercise the committed/configured production path over convenient hand-built fixtures when the production path is the proposition under test.
- Distinguish static validation, unit proof, integration proof, runtime evidence and semantic acceptance; one does not silently substitute for another.
- Implementation follows accepted meaning and proof obligations; implementation convenience does not create requirements.

## Change discipline

Make the smallest change that fully satisfies the accepted semantic obligation without weakening surrounding guarantees.

Before modifying a file, establish:

1. why it is in scope;
2. which authority permits the change;
3. what proposition the change is intended to make true;
4. what evidence will establish that proposition afterwards.

Do not make opportunistic adjacent changes unless they are required for the authorised unit or separately authorised.

Do not claim a capability is unavailable until the relevant current tool, configuration, schema or repository surface has been inspected. If the direct route is blocked, identify the exact missing capability, then investigate alternatives. Present a workaround only after its required steps have been verified end-to-end.

## Carry-forward and Git-history law

When work proceeds from an existing Git state toward a new target tree, material that should not exist in the target active tree must be classified as `DO_NOT_CARRY_FORWARD`, not `REMOVE` or `DELETE`, unless actual destruction is explicitly intended and separately authorised.

`DO_NOT_CARRY_FORWARD` means:

- the material is not present in the target active tree;
- the change is recorded by ordinary Git history;
- the material remains recoverable from prior commits and repository history.

Do not conflate absence from the target tree with destruction of historical evidence.

Do not rewrite, prune or otherwise destroy Git history unless that destructive action is explicitly authorised.

ExecPlans, inventories and acceptance records must use `DO_NOT_CARRY_FORWARD` for this case.

## Failure and stop law

At the first absent or failed required invariant:

1. stop downstream execution that depends on it;
2. preserve the last proved state and the first unmet invariant;
3. distinguish observed failure from diagnosis;
4. diagnose only within authorised scope;
5. do not redesign or repair downstream stages that were never reached.

Stop for an unresolved authority conflict, missing required source/authority, proved dependency or credential blocker, unavailable required capability, unsafe tool/context state, or required human approval.

Partial verified progress is preferable to speculative completion.

## Claims and close-out

Do not claim `PASS`, fixed, implemented, verified, clean, complete, accepted, admitted, conformant or equivalent without evidence sufficient for that exact proposition.

For material work, close-out must identify:

- what was inspected or changed;
- the exact repository/Git state where relevant;
- the validation or evidence actually obtained;
- unresolved, deferred or blocked matters;
- the boundary between verified fact and inference.

A review receipt is not semantic correctness. A semantic review is not programme admission. A commit is not acceptance. A clean worktree is not correctness.

## Frozen status and governance change

`GUARDRAILS.md` is frozen during ordinary project execution. No worker, reviewer, plan, test, validator, hook, script or implementation task may self-amend it or authorise its mutation.

A change to this file requires explicit current human/programme authority and must be treated as a governance change, not as ordinary implementation work. The proposed change must be shown exactly and accepted before it becomes governing authority.

`AGENTS.md` and `EXEC_PLAN.md` may not contradict this file. If they do, this file governs until the conflict is explicitly resolved by higher authority.
