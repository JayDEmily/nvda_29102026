# ADR — Continuous execution without routine owner reapproval

**Date:** 12 November 2026 (Australia/Melbourne)  
**Status:** OWNER-DIRECTED GOVERNANCE CHANGE — WORKING BRANCH ONLY; NOT INSTALLED  
**Base:** `planning/t01-recovered-successor-20261111` @ `768f18672d5f8a226e806b9fff68984ae027d739`  
**Applies to:** NVIDIA V2 planning/implementation workflow once the particular governing ExecPlan is accepted and commissioned. It is not an independent programme scope expansion.

## Context

The owner has repeatedly commissioned execution through bounded plans and explicitly does **not** want a Worker to stop after each leaf, documentary review, checkpoint, gate preparation or handover solely to request another 'continue' or 'approve' instruction. The original R2 root `AGENTS.md` begins 'Changes require explicit owner authorisation'; the proposed successor repeats that wording, while the successor `EXEC_PLAN.md` separately contains legitimate source/policy decisions and an uninstalled-plan acceptance boundary. These are not interchangeable.

The frozen `GUARDRAILS.md` resolves current user direction above repository rules, distinguishes formal programme acceptance from technical evidence, and stops only **dependent** work on a failed required invariant or genuine required human decision. Its text and historic evidence remain unchanged.

## Decision

1. **Standing execution commission.** Once the owner has accepted and commissioned an exact bounded `EXEC_PLAN.md`, that commission is authority to undertake every *already in-scope and released* worker action through the plan's close-out, including normal edits, narrowly required validation, commits, checkpoint publication/readback, documentary handoffs, bounded repairs and proceeding to the next eligible leaf. Do **not** ask the owner for permission to continue after each step.
2. **Independent roles remain.** The Worker does not self-certify. Independent reviews occur through the specified separate reviewer/Tester with actual evidence. Under R2 CHAT_MANUAL, the separate Tester retains exclusive new product-test execution at L32, only for properly admitted cases; the Worker may not convert `IMPLEMENTED_UNTESTED` to `TESTED_ACCEPTED`.
3. **Blocked is local, not a global idle command.** On the first unmet invariant, stop its dependent actions, identify and record the exact missing evidence/authority, preserve the last proved state and continue other **independent authorised** tasks where dependencies and tool capability permit. Do not invent a policy, hide a failure, weaken proof or call a blocked item complete.
4. **Real owner decisions are exceptional.** New or amended domain/source/measurement policy where authority reserves a choice to the owner, activation of D145, an unapproved proof budget, material programme rescope, change to frozen `GUARDRAILS.md`, production/live-provider operations, purchases, irreversible external actions or promotion beyond the accepted branch need their own actual authority. A standing commission does not manufacture those permissions. Establish the missing decision precisely from current governing artefacts before escalating; work on other independent tasks meanwhile.
5. **Run until the actual boundary.** Continue within the available execution turn until all eligible work is complete or an external limit (tool/session access, model/context/response quota, runtime deadline) prevents further work. Record the latest Git checkpoint, remaining work and exact next step. Such a limit cannot be overridden by repository prose, and a chat does not continue running in the background.
6. **No repeated acceptance theatre.** A review result, clean diff, approved plan or passed gate does not automatically prove the next semantic obligation; equally, it does not create a fresh owner-approval requirement where an accepted plan already commissioned the task. The evidence/role gates remain, but routine discretionary owner pauses are removed.

## Specific reconciliation

- `GUARDRAILS.md`: **no change**. Its 'required human approval' stop applies only when an *actual* applicable authority requires a new decision; it does not mean reapproval of already commissioned leaves.
- Root `AGENTS.md` (working branch) and `PROPOSED_AGENTS.md`: replace blanket per-change owner-authorisation phrasing with standing in-scope authorisation and explicit continuous progression.
- `PROPOSED_EXEC_PLAN.md`: state the continuous-execution rule once in §2 and clarify the genuine decision boundary in §7, without altering any L00–L32 semantic leaf, 39-leaf coverage, seven external holds, case allocations or the approved D145 pause.
- `PROPOSED_TESTS_AGENTS.override.md`: prevent repeated permission pauses for cases that the accepted plan and ledger already release; never broaden the Tester role or start tests prematurely.
- Historical `EXEC_PLAN.md`, original ledgers, historical reviews and documentary receipts: preserved; they are not rewritten to retrospectively change a prior commission.
- The previously reviewed T01 proposal is a different set of Git blobs from this amended candidate. The 11 November independent `ACCEPT_DOCUMENTARY_PROPOSAL` report is evidence for its **original pinned** input, not independent review of these new bytes.

## Installation and evidence boundary

This branch is authorised to record the decision and prepare exact governance deltas. It does **not** install the proposed successor as active root authority, release any product case, qualify SQLite/PostgreSQL, merge to `main`, change frozen guardrails or reactivate D145. A later installation must bind the exact accepted governing revision and preserve a reviewable Git diff; **after** such acceptance/commission there is no per-leaf owner reapproval. Do not treat the current request to fix stop behaviour as an unbounded commission for unrelated product work.
