# NVDA Raw Signal — First Codex Run Handoff

**Date:** 17 August 2026
**Status:** Operational handoff for the first transfer and first Codex planning run.
**Authority:** This document does not create or alter Raw Signal semantic or architecture authority. `AGENTS.md`, `.agent/PLANS.md`, `authority/AUTHORITY_MANIFEST.md`, the source artefacts identified there, and accepted architecture authority remain controlling within their jurisdictions.

## 1. Purpose

Preserve the clean accepted repository while making the first Windows 11 -> WSL2 -> Codex Desktop transfer deliberate, observable, and reversible. No Codex project instruction should be sent until the archive, WSL substrate, sandbox/runtime, Python environment, Git state, and effective Codex configuration have been checked.

The first Codex interaction is planning only. Implementation begins only after the Codex plan has been reviewed by the systems architect and independently checked for fidelity to the same repository authority.

## 2. Accepted source archive identity

The canonical clean handoff supplied for this first run is:

```text
NVDA_RAW_SIGNAL_CODEX_HANDOFF_20260813_FINAL_V2.tar.gz
SHA-256: c7f0e7d569939224b6175262c2048adf59c790f8ca2bbcfd0a68b582bfe5165c
```

Observed repository identity after fresh extraction during this handoff preparation:

```text
branch: main
HEAD: 05bd00adfbd418b17d4d521939da37d859b6bb5f
commit_count: 1
commit_subject: baseline: accepted NVDA Raw Signal Codex execution repository
git_fsck_full_strict: PASS
worktree: clean
.python-version: 3.13.5
```

The following similarly named archive is **not** the first-run clean handoff and must not be substituted:

```text
NVDA_RAW_SIGNAL_CONSTRUCTION_LINEAGE_20260813_FINAL_V2.tar.gz
SHA-256: 9d8f6d27690485801448284b9146b6cfec53ec5300d49f95fc5e5f6346025a65
```

That archive preserves construction lineage rather than the one-commit clean execution baseline.

## 3. First-run operating principle

For this first transfer, do not compress the environment checks into one large script. Run one acceptance gate at a time and inspect the output before continuing.

At any failed or materially ambiguous gate:

1. stop at that gate;
2. record the observed fact;
3. diagnose that layer only;
4. do not pre-emptively repair downstream layers;
5. resume only when the failed invariant is understood and the correction is authorised.

No failure in transfer, WSL, Bubblewrap, Python, Git, project trust, or Codex configuration should be misclassified as a Raw Signal semantic failure.

## 4. Manual acceptance sequence before any Codex project prompt

### Gate A — Windows download identity

Objective: prove that the browser download is the exact clean handoff archive.

Required evidence:

- exact filename;
- byte presence in the normal Windows Downloads location;
- SHA-256 equals `c7f0e7d569939224b6175262c2048adf59c790f8ca2bbcfd0a68b582bfe5165c`;
- gzip/tar integrity;
- no renaming used as identity proof.

Do not proceed on filename similarity alone.

### Gate B — WSL substrate

Objective: prove that Codex will operate in the intended Linux environment.

Check before repository transfer:

- intended Ubuntu distribution;
- WSL2, not WSL1;
- expected architecture;
- user/home directory;
- intended project path under native Linux storage such as `/home/...`, not a working repository under `/mnt/c/...`;
- Windows/WSL boundary is understood before moving bytes.

Current OpenAI guidance states that Codex in WSL2 uses the Linux sandbox implementation and that from Codex 0.115 the Linux sandbox uses Bubblewrap, so WSL1 is no longer supported.

### Gate C — Bubblewrap and Linux sandbox substrate

Objective: prove the sandbox substrate itself, not merely the existence of a package name.

Check:

- `bwrap` resolves to the expected executable;
- installed Bubblewrap version;
- package ownership/source where relevant;
- required namespace/seccomp behaviour is not blocked by the WSL/container host;
- the current Codex build is compatible with the observed WSL/Bubblewrap environment.

Do not reinstall or upgrade Bubblewrap merely because a different version exists. Diagnose first.

### Gate D — Codex installation and execution surface

Objective: establish which Codex runtime will execute the project.

Check:

- Codex Desktop app version;
- Codex CLI version where the CLI is part of the local toolchain;
- Desktop agent is configured to run in WSL rather than accidentally using the native Windows sandbox;
- integrated terminal choice is recorded separately from agent execution choice;
- Git is available to the app/review surface.

Do not open the repository for substantive work yet.

### Gate E — Python/build environment

Objective: prove the project can reproduce its declared runtime without silently substituting another interpreter.

Check:

- `.python-version` requires `3.13.5`;
- actual Python interpreters available;
- `pyenv` state where used;
- `uv` version and location;
- lockfile presence and compatibility;
- vendored wheelhouse/integrity surfaces required for offline or pinned installation;
- no dependency or interpreter mutation merely to obtain green output.

If the expected environment is absent, that is an environment finding. Reconstruction should follow the repository's actual locked requirements rather than an ad hoc upgrade.

### Gate F — global Codex configuration

Objective: establish the effective machine/user configuration before the project layer is trusted or loaded.

Inspect the actual `CODEX_HOME` used by the execution surface and, where applicable:

- user `config.toml`;
- user hooks;
- rules/permissions;
- selected profile;
- model/provider settings;
- approval and sandbox settings;
- any machine-local provider, base-URL, notification, or telemetry settings that project config cannot override.

Do not delete or rewrite global configuration during inspection.

Current OpenAI guidance states that an untrusted project does not load its project `.codex/` layer, while user/system configuration remains active. Some provider/profile/telemetry keys are intentionally user-level and are ignored in project config.

### Gate G — transfer into native WSL

Objective: move the already verified archive across the Windows/WSL transport boundary without creating a second source of truth.

Rules:

- the Windows copy is transport only;
- the archive hash must match before and after copying into WSL;
- keep the working repository under native WSL storage;
- do not place the source tarball inside the Git repository;
- do not treat the transport copy as a new version.

### Gate H — fresh hydration and Git integrity

Objective: prove the hydrated repository is the intended Git object before Codex sees it.

Require:

```text
branch: main
HEAD: 05bd00adfbd418b17d4d521939da37d859b6bb5f
commit_count: 1
worktree: clean
```

Also check:

- archive extracts to exactly one intended repository;
- `.git` is present;
- `git fsck --full --strict` passes;
- no staged, unstaged, or untracked residue was introduced by transfer/hydration;
- expected instruction/configuration/authority surfaces exist.

### Gate I — project Codex configuration versus global configuration

Objective: identify the effective configuration rather than assuming project settings replace every global setting.

The clean repository currently contains:

```toml
[agents]
default_subagent_model = "gpt-5.6-terra"
default_subagent_reasoning_effort = "medium"
```

This project file configures **default subagents**. It does not set the main parent model or parent reasoning effort for the first planning thread.

Compare project configuration against the active global/user configuration before execution. In particular:

- project trust must be established before project `.codex/` config can load;
- user/system config remains relevant;
- project config cannot override certain host/provider/profile settings;
- hooks are additive across active sources rather than ordinary last-writer-wins replacement;
- any hook must be reviewed against its actual current definition before it is trusted.

No project-local hooks are present in this clean repository at the time of this handoff preparation.

### Gate J — open the exact WSL repository in Codex, but do not start project work

Objective: prove the live app/session sees the same workspace and configuration that was verified externally.

Before `/plan`:

- confirm the exact repository path;
- confirm Git branch/HEAD;
- confirm the selected main model/reasoning level;
- inspect effective configuration/instruction sources using current supported Codex introspection commands where available;
- inspect configured hooks/trust state where hooks are present;
- keep the session non-mutating until planning begins.

Only after Gates A-J are satisfactory should the first project planning prompt be sent.

## 5. Main-model policy for the first planning run

### Decision

Use:

```text
GPT-5.6 Sol
reasoning: High
mode: Plan
```

Do **not** default this first planning pass to Extra High merely because the repository is complex.

### Reasoning

Current OpenAI model guidance says:

- higher reasoning can improve complex work but takes longer and uses more tokens;
- use the lowest reasoning effort that produces the required result;
- both High and Extra High suit difficult work with multiple steps, sources, or trade-offs;
- Extra High is especially appropriate for long, agentic, reasoning-heavy tasks;
- Ultra adds automatic subagent delegation and is unnecessary for this first coherent parent planning pass.

OpenAI publishes no task-specific quantitative guarantee that Extra High will produce a material planning-quality improvement over High for this repository. The marginal benefit is therefore **Unknown until tested on this workload**.

The first plan should start at High because:

1. it is difficult, multi-source semantic/architecture planning;
2. it is deliberately not yet long-running implementation;
3. the plan will receive a second independent review against the same repository authority;
4. Extra High remains available for a bounded reconsideration if High produces a demonstrably inadequate plan.

This is a quality/cost control, not a prohibition on Extra High.

## 6. First Plan-mode instruction

Do not activate Goal mode yet. The repository deliberately leaves selection of the first bounded semantic unit to Codex after current-source inspection.

Use this first instruction:

```text
/plan Before proposing implementation or modifying the repository, read the governing repository material and inspect the actual repository and live environment. Read AGENTS.md, .agent/PLANS.md, authority/AUTHORITY_MANIFEST.md, the complete seven-sheet rendered workbook authority, the cross-module data-identity and DMPV3 governance authority, every accepted architecture authority enumerated by the manifest, the NVDA semantic-orchestrator skill, the custom-agent definitions and configuration, and inspect the current implementation, schemas, templates, proof configuration and tests sufficiently to understand the neutral starting state. Inspect the authoritative .xlsx directly wherever workbook presentation or structure could affect meaning.

Form your view from the current authoritative repository only; do not seek or reconstruct historical or forensic implementations.

Then identify the first coherent bounded NVDA Raw Signal semantic unit using source meaning and the Intent-to-Evidence Systems Realisation Method (IESRM) defined by the semantic skill, not implementation convenience. Propose the task-specific ExecPlan required by .agent/PLANS.md. Preserve systems-architect semantic acceptance authority. Do not implement yet and do not pre-assume hooks or other control mechanisms.
```

Purpose: understand the current authoritative repository and propose the first defensible plan. Do not tell Codex in advance which semantic unit it must choose.

## 7. Independent plan review before Goal mode

After Codex produces its Plan-mode result, stop before `/goal`.

The systems architect should provide the **plan verbatim** to an independent GPT-5.6 Sol review thread that can inspect the same clean repository/tarball.

The independent review is not a competing architecture exercise. Its job is to test the plan against the same authority and report concrete defects or risks only.

Review questions:

1. Does the plan actually follow the repository authority hierarchy?
2. Does the first bounded unit arise from source meaning rather than implementation convenience?
3. Does it preserve IESRM and the systems-architect acceptance boundaries?
4. Has any accepted `Unknown` silently become a design choice?
5. Has a material dependency or cross-unit closure obligation been omitted?
6. Has the plan imported knowledge from historical/failed implementation that the clean run should not know?
7. Has it added hooks, state machines, ledgers, receipt systems, or other control machinery without a demonstrated missing invariant?
8. Are implementation/review units too broad to preserve semantic independence, or fragmented beyond the actual semantic closure boundary?
9. Are validation and stopping conditions adequate and evidence-based?
10. Does the plan preserve enough engineering freedom for Codex rather than dictating an unproved solution?

Suggested independent-review disposition vocabulary:

```text
ACCEPT
ACCEPT_WITH_SPECIFIC_CONCERNS
RETURN_TO_CODEX_FOR_RECONSIDERATION
```

Any concern must cite the exact repository/source basis. The reviewer should not replace Codex's plan merely because it would have chosen a different engineering route.

If the independent review finds a genuine hard planning problem, use that bounded issue as the candidate for escalation to Sol Extra High rather than rerunning the whole plan at higher effort by default.

## 8. Plan acceptance rule

The systems architect reviews Codex's plan once, informed by the independent review.

The acceptance question is:

> Does this plan preserve the objective, authority, source meaning and semantic method while leaving Codex enough engineering freedom?

It is **not**:

> Would another model or the systems architect have engineered it differently?

If material concerns remain, return those bounded concerns to Codex in Plan mode and let Codex reconsider its own plan. Do not author proof or implementation while the plan remains unresolved.

## 9. First Goal after plan acceptance

Only after the plan is accepted should Goal mode be activated.

Use:

```text
/goal Complete the first bounded NVDA Raw Signal semantic unit identified in the approved Plan-mode result, preserving authoritative source meaning from understanding through an authorised, tested, minimally implemented and independently semantically validated vertical slice. First materialise the approved plan as the root EXEC_PLAN.md required by .agent/PLANS.md and keep it accurate throughout the work.

Apply the Intent-to-Evidence Systems Realisation Method (IESRM) as the gated semantic method defined in .agents/skills/nvda-semantic-orchestrator/SKILL.md. Codex may investigate, derive, challenge, recommend, write, test and implement within authorised scope, but must not grant itself systems-architect semantic acceptance. At every material IESRM gate requiring systems-architect disposition, stop only for that bounded semantic decision and present the source-backed interpretation, independent challenge, material alternatives, consequences and remaining Unknowns. After an Accepted disposition, continue autonomously under the same goal. Rejected, Deferred or unresolved gates do not authorise dependent semantic work.

Use authority/AUTHORITY_MANIFEST.md and its identified sources as the domain authority, preserve the accepted architecture authority enumerated there, and preserve current direct user authority including PostgreSQL persistence and the distinct scheduled 30-second capture-set clock. Do not invent missing semantics, collapse Unknown into certainty, or substitute tests, implementation or historical reasoning for source authority.

Between semantic gates, own ordinary engineering execution autonomously: choose the next action from the evidence, use bounded custom agents where their independence or specialisation adds value, diagnose and repair ordinary repository, tooling, configuration and test problems within authorised scope, keep Git and EXEC_PLAN.md current, and choose the smallest adequate engineering mechanism rather than introducing speculative control machinery.

Complete this goal only when the bounded unit has passed every material authorised semantic gate, its normative authority is explicit, adversarial proof has been established, the minimal implementation satisfies that authority and proof, an independent semantic reviewer has checked the implementation against the source-backed authorised meaning, affected architecture and aggregate validation pass, the Git state is coherent and clean, and the final evidence distinguishes what is demonstrated from what remains Unknown.

If no defensible path remains under current authority, a systems-architect semantic disposition is required, or an irreducible protected security/trust or UI boundary prevents further progress, stop with the exact blocker, evidence already established, what remains unresolved, and the smallest decision or action that would unlock progress. Do not stop merely to ask the user for routine commands, retries, implementation choices or continuation.
```

One Goal should govern the accepted bounded unit. Do not create one Goal per small implementation step.

## 10. What this handoff deliberately does not change

This preparation does **not**:

- alter `AGENTS.md`;
- alter `.agent/PLANS.md`;
- alter the semantic-orchestrator skill;
- alter the six custom-agent TOMLs;
- alter `.codex/config.toml`;
- create an `EXEC_PLAN.md` before Codex performs the Plan-mode work;
- select the first Raw Signal semantic unit on Codex's behalf;
- alter accepted Raw Signal or architecture semantics;
- pre-install, upgrade, or repair the user's WSL/Codex/Python environment;
- treat environment verification as semantic Gate work.

The repository remains a clean semantic starting point plus this explicit first-run operational handoff.

## 11. Official OpenAI references used for operational claims

Only current official OpenAI material was used for Codex product/runtime claims in this handoff:

- Codex models and reasoning effort: `https://developers.openai.com/codex/models`
- Codex best practices and Plan mode: `https://developers.openai.com/codex/learn/best-practices`
- Codex app commands: `https://developers.openai.com/codex/app/commands`
- Codex Windows/WSL guidance: `https://developers.openai.com/codex/windows/wsl`
- Codex Windows app guidance: `https://developers.openai.com/codex/windows/windows-app`
- Codex configuration basics: `https://developers.openai.com/codex/config-basic`
- Codex advanced configuration: `https://developers.openai.com/codex/config-advanced`
- Codex hooks: `https://developers.openai.com/codex/hooks`
- Codex approvals/security: `https://developers.openai.com/codex/agent-approvals-security`
- Codex goal workflow: `https://developers.openai.com/codex/use-cases/follow-goals`

## 12. First future action

When Ubuntu/WSL access is available again, resume at **Gate A** and work through the gates manually. Do not skip ahead because the same machine previously worked: the purpose of this first-run protocol is to establish the actual environment that will execute this exact repository.
