# Guardrails

## Authority

Apply authority in this order:

1. Current user instruction.
2. Governing brief or plan explicitly identified for the project.
3. Applicable `AGENTS.override.md` instructions.
4. `EXEC_PLAN.md`.
5. Normative documents.
6. Tests.
7. Source/configuration.
8. Evidence artefacts.

Lower authority cannot silently override higher authority.

## Evidence discipline

Use these epistemic states exactly:

- `VERIFIED` — directly established by inspected evidence.
- `INFERRED` — reasoned from evidence but not directly established.
- `UNKNOWN` — evidence does not establish the point.
- `BLOCKED` — a required operation or determination cannot lawfully proceed.

Do not promote `INFERRED`, `UNKNOWN`, or remembered information into `VERIFIED` without evidence.

## Re-entry

Conversation history, summaries, handovers, generated context, receipts, and memory are context, not governing authority. Re-entry must revalidate current repository authority and state.

`control/lcr.json` is the generated Leaf Continuation Record and carries no independent truth. Every load-bearing LCR value must be reproducible from committed Git/task/claims/receipt/governance evidence. An LCR edit cannot lawfully change the current leaf, unresolved claims, blockers, receipt provenance, checkpoint source, accepted base, next actor class, next leaf, or project status.

The generated LCR must not create a routine shadow commit for a substantive transition. In normal LCR-mode execution, stage the authorised transition, admit it with `checkpoint`, and commit the substantive change and regenerated LCR together once. A generated-state-only checkpoint commit is a compatibility/recovery path, not the normal progression mechanism.

Epistemic claims belong in `control/claims.json`. Any claim not recorded as `VERIFIED` remains unresolved for LCR purposes. Claims changes require explicit checkpoint admission.

## Delegated actor boundaries

The installed PCM `GUARDRAILS.md` and `AGENTS.md` are frozen methodology authority for a consuming project. Bootstrap/project planning must not create editable project-local replacements for those document types under `.pcm/project/`; project-specific authority belongs in the project objective, requirements, execution plan, task/delegation contracts and applicable pre-existing native authority. Lower project authority may specialise the project only where it does not conflict with the frozen methodology pair.

The user's appointment in the current thread determines its operational role. Leaf actor class identifies who must perform the next governed responsibility; it does not reassign that appointment. Repository state, generated context, session restart, successful admission, and general instructions to continue do not change the appointed role. Do not infer operational role from `control/delegation.json`, the LCR, session state, packets, or prior-thread memory. A fresh thread must have an unambiguous current user assignment before execution; a direct request to perform a specific worker task may supply that assignment without creating new role state.

A thread appointed PM/orchestrator may inspect repository state, draft project authority within its authorised planning or governance scope, including authorised bootstrap work while `template_mode=true`, and route work. It must not perform an execution leaf merely because its actor class is `AUTONOMOUS`, including analysis, proofs, tests, or source changes. At that boundary, identify the stable task ID and required worker, provide the bounded handoff instruction, and stop leaf execution for a separate worker thread. **Appointment and handoff are not execution.** Once the finalised task graph and delegation define a downstream responsibility, the PM may issue that bounded worker handoff prospectively before its dependencies make the leaf `ready`; the appointed worker may establish repository identity, authority and role, then wait. A not-yet-ready leaf blocks `context`, execution and acceptance for that leaf; it does not require the user to return through the PM merely to obtain a handoff that can already be derived from committed authority. Where an `AUTONOMOUS` responsibility has a declared `INDEPENDENT_REVIEW` successor, ensure a genuinely independent reviewer is already appointed by the time the candidate needs review. If an earlier test/proof responsibility was performed by a thread that did not author the implementation candidate and that thread is intended to perform the later independent review, the same chat thread may remain appointed or be reappointed for that review leaf; do not spawn an additional reviewer merely because test/proof and review are separate governed responsibilities. Otherwise appoint or dispatch the worker and reviewer together when that pair becomes known. The reviewer may establish repository identity, authority and reviewer role immediately, then wait; it must not issue a review result until the lawful review leaf, exact candidate and current review packet exist. Authorised governance maintenance remains subject to its existing admission rules and is not silently recategorised as ordinary worker execution.

An independent-review `REPAIR` that stays inside the admitted requirement, semantic-authority, write-scope, actor-class and acceptance/verification envelope routes directly to the owning `AUTONOMOUS` responsibility. The PM/orchestrator is not a required intermediary in that repair loop. Where append-only history requires a new bounded refinement ID, the assigned autonomous worker may append and admit the same-actor bounded refinement under the existing refinement contract, then return the changed candidate for a fresh packet/result to the already-appointed independent reviewer. A review `PASS` returns to the PM/orchestrator for the next governed transition. A repair that cannot remain inside the admitted envelope, or any unresolved authority/blocker condition, returns to PM/programme-owner governance rather than being forced through the direct repair loop. Physical transport between separate threads may be performed by the user and does not itself create a PM decision point.

Every executable leaf has exactly one actor class in `control/delegation.json`: `AUTONOMOUS`, `INDEPENDENT_REVIEW`, or `PROGRAMME_OWNER`. Delegation policy is part of the approved authority envelope and is mechanically projected into the LCR.

An autonomous worker may not continue through an `INDEPENDENT_REVIEW` or `PROGRAMME_OWNER` leaf. Independent review requires a reviewer actor instance distinct from the candidate author. That independence boundary does not by itself require a new chat thread: an already-independent test/proof thread may later perform the review leaf if currently appointed to that role and it did not author the candidate. Programme-owner review is not implied unless separately required. Programme-owner gates are reserved for material objective/envelope transitions.

Changing the delegation policy after it has been bound requires an explicit programme-owner admission. Repository-local enforcement is a consistency and workflow boundary; it does not claim cryptographic resistance to a deliberately malicious shell-capable worker.

## Fail closed

Stop when required governance is missing, unreadable, contradictory, stale, ambiguous, or incomplete. Partial lookup cannot prove absence, uniqueness, or freshness.

## Git and acceptance

The PCM V5 methodology identity is the exact committed `main` commit/tree of the field-use repository supplied for the project. Do not reconstruct methodology authority from predecessor branches, historical chats, or superseded development artefacts.

A task recorded as `accepted` requires a Git tag `accepted/TASK-ID` on the configured acceptance branch, and the tagged commit itself must record that task as accepted with accepted dependencies. The exact tag target is provenance and may not move silently.

Accepted history is append-only. Do not rewrite or reset accepted history to repair downstream work; create a new lawful lineage from the admitted recovery base.

Committed work and accepted work are distinct unless the project explicitly defines them as identical.

## Change discipline

Execute only the active `EXEC_PLAN.md` leaf and its permitted write scope. The V5 methodology source repository is a field-use baseline, not a methodology-development work queue; consuming-project execution occurs only through the project authority instantiated under `.pcm/project/`.

A worker may choose implementation details inside the accepted authority envelope. A worker may not change requirements, semantic authority, actor class, write scope, acceptance law, or route meaning without the programme-owner route.

If applicable governing authorities conflict, stop and resolve the conflict before implementation proceeds.
