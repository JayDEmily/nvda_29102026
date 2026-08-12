# NVDA Raw Signal clean restart — universal instructions

## Objective

Turn well-structured, semantically authoritative briefs into correct code without losing, inventing, or silently changing meaning.

## Authority and jurisdiction

Classify a disputed proposition before resolving it:

- current official OpenAI documentation plus direct live evidence govern Codex product/runtime facts;
- current direct user instruction and accepted programme decisions govern NVDA programme law;
- this file, `PLANS.md`, an accepted `EXEC_PLAN.md`, and admitted work orders govern execution only within delegated scope;
- accepted source/normative authority governs Raw Signal domain meaning.

A lower layer cannot become authority merely because it is newer, committed, reviewed, schema-valid, or green. Across jurisdictions, stop and reconcile the interface rather than silently letting one jurisdiction legislate another.

## Frozen programme authority

Root `AGENTS.md` and programme `PLANS.md` are **FROZEN** authority surfaces during ordinary Codex execution. Project workers, reviewers, PMs, skills, tests, implementation routines, validators, and recovery routines may read and obey them but must never edit, regenerate, rewrite, auto-maintain, or self-amend them.

A change to either file is a governance proposal outside the ordinary semantic work-order path. It requires current explicit human/programme authority, an exact candidate patch, fresh independent review, explicit human/programme acceptance, authorised control-plane application, and a fresh Codex session where instruction discovery is session-bound. No work order or delegation may authorise mutation of either frozen file.

`EXEC_PLAN.md` is not frozen in this sense. It may evolve only within an already-authorised bounded tranche and cannot create or supersede programme law.

When an ExecPlan is required, exactly one explicitly accepted root `EXEC_PLAN.md` is the current bounded execution authority. It operationalises accepted authority and cannot create programme or domain law. Completed or superseded ExecPlans are historical evidence: retire them from the active root role rather than appending to them indefinitely, and replace the root ExecPlan whenever the authorised tranche changes materially.

## Epistemic law

Keep these distinct: `OBSERVATION`, `HYPOTHESIS`, and `PROPOSAL`. Record `Unknown` when evidence does not establish a fact or cause. Governance may evolve, but it may not self-promote.

At the first absent or failed invariant: **STOP**. Preserve the last proved state and the first unmet invariant. Do not execute, diagnose, or redesign downstream stages that were never reached.

Do not claim PASS, fixed, verified, clean, complete, accepted, or implemented without the evidence required for that exact claim.

## Gate boundary

Gate 0 is a runtime/control admission for Gate 1A only. No Raw Signal semantic orchestration occurs before an explicit admitted Gate 0 PASS. Follow `docs/orchestration/BOOTSTRAP.md` for Gate 0; root instructions intentionally do not duplicate its commands.

The `nvda-semantic-orchestrator` skill is Gate 1+ only and must be invoked explicitly. It does not govern bootstrap, Gate 0, runtime recovery, hook repair, protected-control repair, or R2A/write-recovery work.

Normal semantic agents must not search forensic or legacy repositories. Historical inspection requires explicit authority.

## Domain, proof, and implementation law

For domain work: source authority > accepted normative authority > tests/proof > implementation. Tests derive from accepted authority and do not create requirements. Do not weaken, skip, redirect, rename, or delete a still-valid test merely to obtain green.

One semantic acceptance unit at a time. Fresh workers perform bounded work; fresh independent reviewers falsify it. Write-bearing work is serial unless explicit semantic and file independence has been proved.

Durable state records admitted truth, not the latest hypothesis, attempt, or narrative history. A work order is delegated execution authority, not a source of new programme/domain law. Review acceptance is not programme admission.

## Runtime command scope

Ordinary WSL control-plane work may use the locked project environment and approved bootstrap commands. Live Gate 0 uses only the exact nonce-bound command family defined by `BOOTSTRAP.md` and the protected arm record. Gate-specific exact commands override generic repository command guidance.
