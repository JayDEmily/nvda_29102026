# T01 — NVIDIA V2 authority and repository reconciliation

**Date:** 10 November 2026, Australia/Melbourne  
**Status:** `T01_PARTIAL_VERIFIED / BLOCKED_FINAL_SUCCESSOR_BASELINE_PUBLICATION`  
**Purpose:** Planning evidence and recommended successor authority, not current execution authority, implementation, or independent product-test acceptance.  
**Repository:** https://github.com/JayDEmily/nvda_29102026  
**Review source:** `planning/ubuntu-postgresql-transition-20261110` @ `465de451d9c0bcd055d6385c0fc5d10cb9c49013`  
**Related proposal:** `SUCCESSOR_AUTHORITY_PROPOSAL.md` in this directory.

## 1. Exact observed GitHub topology (10 November)

Windows-side `git ls-remote --heads` and GitHub connector agreed on:
- `main` — `7e2601a5e050d76202b1b6d3f69fc167a04c91f7`;
- `execution/accepted-r1-20261030` — `363923d47b81fca50e64036bef3c8601501e3c16`;
- `planning/chat-manual-r2-20261030` — `6feb50bf8a96e244cbd68eb57536f940be6335b3`;
- `planning/ubuntu-postgresql-transition-20261110` — `465de451d9c0bcd055d6385c0fc5d10cb9c49013`;
- disposable `experiment/chatgpt-handoff-arithmetic-20261110-01` — `18090360b24fca36721cfa939d88a7cdc799b73f`.

GitHub commit comparison:
- R1 → GitHub R2: `ahead=8, behind=0`, exact ancestor, six distinct changed paths (including AGENTS, tests override, root ExecPlan and planning artefacts).
- GitHub R2 → November planning: `ahead=6, behind=0`; six new historical/planning files, **no update to root ExecPlan or test ledger at this stage**.
- Current `main` → November planning: diverged at `8ff7d82377e9bf8f9fc75c1ecef70f0ab29a2ada`. November is **19 commits ahead** of that merge base, while `main` has **three separate later commits** containing the ChatGPT–GitHub runbook/AGENTS pointer. Neither head supersedes the other by timestamp or label alone.

**Authority:** The R1 execution branch root plan expressly says `OWNER_ACCEPTED_AND_COMMISSIONED` but records L00 `BLOCKED_TRANSFER`. GitHub R2's root ExecPlan expressly says `PROPOSED_NOT_ACTIVE`. The November T00–T07 supplementary plan is `PROPOSED_NOT_ACTIVE`. There is no evidence that merely making later planning commits installed a new active root programme.

Original `GUARDRAILS.md` Git blob `54a4407609941f63f6b902076688ff102a3d5ba2` is unchanged on inspected R1, GitHub R2, November and main branches. It is frozen.

## 2. Later recovered R2/G0/F02 lineage and direct evidence

The authoritative *scope* of the available 10 November independent review is:
[`T00_F02_INDEPENDENT_BOUNDED_REVIEW_20261110.md` at November planning HEAD](https://github.com/JayDEmily/nvda_29102026/blob/465de451d9c0bcd055d6385c0fc5d10cb9c49013/handoff/planning/ubuntu_postgresql_transition_20261110/T00_F02_INDEPENDENT_BOUNDED_REVIEW_20261110.md).

That independent reviewer records:
- repaired candidate `16b7cc67f5d24336d3768e2da006819474a8c792`; tree `2b2bd7c1b7342f22909339a99150e2a395039e06`; immediate parent `9a4f1e827accdd7cfe3d7a14d5575573589b1acd`;
- exact original full-history baseline `97f944d51ab9e403250fe76910e2754b50425c73`; all 66/66 original ref names/tips independently revalidated; 67 restored named refs total; 4,024 tracked paths; inventory SHA-256 `6e24293d7908a3bce9e950bfd16cfa967c06c907a4f72bf54b8de0172dbdd432`;
- both `git bundle verify` operations and `git fsck --full --no-reflogs` returned exit 0 in a fresh temporary receiver;
- repaired candidate changed **exactly two documentary files**: `handoff/m02_completion_28_execution/L00/R2_G0_SQLITE_INDEPENDENT_REVIEW_REQUEST.md` and `R2_SQLITE_RUNTIME_DECISION.md`;
- F02 mechanism: predecessor documentation claimed a tracked `tools/with_pinned_sqlite.sh` that did not exist. Repaired documents correctly identify tracked `tools/check_sqlite_runtime.py` and a conditional, explicit `NVDA_SQLITE_LIBDIR` / `LD_LIBRARY_PATH` launch path. The historical helper string remains only as a disclosure of the original error;
- **`F01 ACCEPT_DOCUMENTARY` (retained), `F02 ACCEPT_DOCUMENTARY_F02`, `PASS_GIT_CHECKPOINT_16b7cc67`** — the specific original documentary finding is resolved;
- **NO independently executed Python 3.13.5 / SQLite 3.54.1 dynamic-link qualification, NO product test, NO activation or G1–G5 acceptance.**

Exact 31 October raw handover identity, recorded by the reviewer:
- ZIP: `NVDA_R2_G0_L00_F02_INDEPENDENT_REVIEW_HANDOFF_20261031.zip`, 1,034,400 bytes, SHA-256 `987aef326d301775e313cdc32556924bef52c446e68ac4ff1c18508aae43767a`;
- additive bundle: 1,000,499 bytes, SHA-256 `b95f05ceba8d873603a5c79894011d2b0babbfc43df674e54175a55b0f11ad2b`;
- original baseline archive: 42,559,431 bytes, SHA-256 `4d02c82894513bff8d07af7a2af6a151cd3f5f14ece581ac0bf0d87ea9ed0430`; embedded bundle SHA-256 `91db4a1989bff366c1f547c5776ca886c276b6b1310027ae929aa1cd1efee4b9`.

**Present assessor's independent limitation:** GitHub `fetch_commit` for `16b7cc67...` failed; `git cat-file -t` in live Ubuntu `/home/jds/nvda_29102026` also failed. The checkout is clean `main` at the earlier `8ff7d823...`, not the repaired branch. Attempts to materialise original F02 ZIP and bundle from their reported Library file IDs again returned `This Project file does not have an authorized raw-byte materialization path`. The exact F02 files were not in the currently mounted `/mnt/data` set or located by a bounded Windows Downloads/Desktop/Documents search. **We inspected the new independent review and its result; we did not re-run its actual F02 restore.** Current remote publication and receiving checkout of this exact object are NOT established.

This **does not reverse** the scoped 10 November independent acceptance. It means the user-selected future GitHub/Ubuntu execution infrastructure cannot yet consume that exact accepted candidate as a verified, reachable Git source.

## 3. Reconciled governed programme scope

Read current R1 root plan, GitHub R2 root plan, November supplementary plan, GUARDRAILS, root AGENTS and applicable `tests/AGENTS.override.md`. Read current registers and proposal ledgers directly.

**R1 live execution register:** 39 leaves: `L00 BLOCKED_TRANSFER` (one), `NOT_ATTEMPTED_DEPENDS_ON_L00` (37), `D145 PAUSED_IMPLEMENTATION` (one). No successor product acceptance was established by the 10 November F02 documentary review.

**Proof ledger comparison:** 35 proof IDs, same ordered IDs in R1 and R2 proposed; **zero** product runs and **zero authorised physical cases** in either ledger. R1 schedules independent per-implementation-leaf work under `WORK_DELEGATED` and an attributed subagent. R2 proposal schedules **34** nonpaused obligations for the separate manual Tester at `L32`, with **one** D145 item on paused `L31`. The proposed variant changes reviewer identity, execution schedule and mode; it does not rewrite existing case results. Proposed future budget stays **60 D-signal cases**, **up to 14 supporting cases**; these are proposed allocations, not executed cases.

**Identity accounting:** 126 conditional foundation identities = 98 historically accepted controlled profiles + 28 held. Of the 28, 20 core and seven mandatory extensions are targeted for *new* controlled implementation; D145 is the separate paused 28th identity. Seven external programme holds remain outside the 28; exact unchanged evidence reuse and any additional PG claims are separate. No new acceptance claim is derived here.

## 4. Exact governance versions and prospective revisions

- R1 root `AGENTS.md` is the old 97-line historical-instruction map (blob `fd471d4502368f4e530be9b8c1c76051883e8ad7`). Its test override (blob `280b50c5c028b2460b7e5c8920259dfaba5cb180`) concerns earlier schedules.
- GitHub R2/November planning proposes shorter mode-neutral root `AGENTS.md` (blob `64cb85ce484920d49d7530951a78efc16ef9deef`) and `tests/AGENTS.override.md` (blob `8a1f4f093133f93cfb984d73907ecfae8beeb456`), including the L32 separate Tester rule. **These exact bytes are proposals on these branches**, not installed on the accepted R1 branch.
- Current `main` root `AGENTS.md` has **one new line** routing cross-thread work to `docs/automation/CHATGPT_GITHUB_HANDOVER_UIA_20261110.md`, which exists on main. This newer operational protocol does not automatically appear in the November branch or the F02 candidate; future successor construction must reconcile that intentional line/file without turning its presence into new programme acceptance.
- The F02 independent reviewer reports its recovered candidate's own governing files unchanged from the F02 predecessor. This assessor has **not** read them from the exact repaired Git tree (unavailable); do **not** copy GitHub R2's file bytes over it by assumption.

**Owner directions separately established by conversations and current user handover:** two independent ChatGPT conversations (Worker and Tester), Ubuntu + GitHub as execution and durable transfer, reintroduced *additional* PostgreSQL for M00 alongside retained M00/M02 SQLite, and T01 planning before implementation. These directions do not authorise a different mathematical law, reactivation of D145, ad hoc tests, source overwrite, automatic main merge or material version-policy change.

## 5. PostgreSQL and Python boundaries

The owner-endorsed [November PostgreSQL ADR](https://github.com/JayDEmily/nvda_29102026/blob/465de451d9c0bcd055d6385c0fc5d10cb9c49013/handoff/planning/ubuntu_postgresql_transition_20261110/ADR_20261110_POSTGRESQL_ADDITIONAL_BACKEND.md) adds a separately qualified M00 PostgreSQL profile; it does **not** migrate M02, activate M01, discard existing SQLite proof or expand the 27 D target.

Source-level checks on GitHub planning snapshot show `src/nvda_desk/raw_signal_occurrence_truth/_postgres.py` exists, and A00 `create_application(postgres_dsn, sqlite_path)` already has mutually exclusive selection and backend creation. `pyproject.toml` already specifies `psycopg[binary]==3.3.4` as optional and `psycopg==3.3.4` in development, but still pins `requires-python ==3.12.14` with Ruff/mypy 3.12. `config/architecture/modules.yaml` records M00 active, M01 bootstrap and M02 active. These are **configuration/source observations**, not working PostgreSQL 18.6 or Python 3.13.5 runtime test results. Read-only T01 does not authorise server installation or code changes.

Normative cross-owner constraints actually inspected: `docs/architecture/OWNERSHIP_AND_COMPONENT_LAW.md`, `PUBLIC_SEAM_LAW.md`, `TEST_AND_PROMOTION_KERNEL.md`, and the 18 October accepted SQLite owner amendment. They preserve M00 semantic ownership, lawful typed public seams, distinct state writers, exact admitted proofs and scoped backend meanings. A future production claim needs its own backend-specific proof.

## 6. New two-chat handover evidence: positive, but bounded

The 10 November [operational runbook on current main](https://github.com/JayDEmily/nvda_29102026/blob/7e2601a5e050d76202b1b6d3f69fc167a04c91f7/docs/automation/CHATGPT_GITHUB_HANDOVER_UIA_20261110.md) records:
- A fresh ChatGPT conversation was created **inside the NVDA_6.1 project** via Windows UI Automation through Remote Desktop Commander.
- It received the exact short prompt `Check the latest NVIDIA GitHub handover and carry out the authorised next task.`
- With no branch name in its message, it independently found experiment branch `experiment/chatgpt-handoff-arithmetic-20261110-01`, input `5dd6ecc6f8ad56d030a24eba8caaf48b7a7fecb4`, computed `10 + 10 = 20` and committed result `18090360b24fca36721cfa939d88a7cdc799b73f`.
- An independent GitHub fetch/diff and `git ls-remote` verified exactly one added result file, one new commit, no NVIDIA product changes.

**Satisfied:** chat initiation, discovery, authenticated GitHub read/write and a simple commit-return.  
**Still outstanding for T02:** independent *fresh* full Git receiver, exact all-ref named-map/tip closure (66 baseline + required additional refs), candidate tree/tracked-blob inventory, non-Git evidence hashes, `git fsck --full` and test-role identity on the actual recovered R2 source. The arithmetic probe is not such a test. Until full remote checkpoint equivalence is established and accepted, no assertion that old cumulative-additive obligations have already been replaced.

## 7. T01 evidence decision and proposed path

**VERIFIED:** branch ancestry/topology; published R1/R2/November/main instruction and ledger differences; 10 November external `ACCEPT_DOCUMENTARY_F02` report; current unavailability of the repaired Git object in GitHub and ordinary Ubuntu checkout; safe demonstrated chat initiation/commit mechanics; exact unchanged 39/35/27/28/D145 programme census.

**UNKNOWN/NOT VERIFIED:** raw F02 bundle in this session, local rebuilt-and-loaded SQLite 3.54.1 on current Ubuntu, exact 463-line recovered F02 root-plan bytes, F02 candidate branch publication and full named-ref history closure in GitHub, current PG18.6 executable server/driver and independent strict Tester product proof.

**Recommended candidate baseline:** the independently reviewed recovered `16b7cc67...` Git candidate as **historical substrate**, *after* actual source availability and receiver restoration, not a blind replacement with newer GitHub R2 proposal. Apply current owner-approved mode decisions, relevant November ADR and proven handover documentation as separate, reviewable non-destructive successor commits. Record exact parent/tree and preserves ref union. Promote only the **accepted successor** after exact-text review/owner adoption; never mutate frozen `GUARDRAILS.md` or rewrite existing history.

**First unmet T01 promotion invariant:** the exact `16b7cc67...` source and required refs are not presently fetchable in the intended shared Git/Ubuntu environment, so an installable byte-exact root successor cannot honestly be produced by modifying that source tree yet. The scoped documentary F02 reviewer verdict remains valid evidence; publication/reconciliation remains open.

**Next bounded activity (planning/evidence only):** make the reviewed additive/baseline accessible to the authorised receiver, verify exact objects/refs, reconcile recovered root AGENTS/override/plan/ledgers against this proposal and current main operational pointer, then independently review exact amended successor bytes for owner acceptance. T02 transfer qualification and later T03/T04 runtime/PG qualification follow their explicit prerequisites. No product tests or implementation now.

## 8. Inspected and uninspected evidence

**Directly inspected fully:** GitHub `GUARDRAILS.md`; R1, R2 and November root AGENTS and test override; R1 and R2 root plans; November T00 review, ADR, T00–T07 plan, historical recovery notes and R2 transition review; ownership/seam/promotion kernel and accepted SQLite owner amendment. Direct ledger parsing; GitHub comparison endpoints; local Windows/Ubuntu branch and object read-only checks.

**Not directly inspected:** the exact 16b7 candidate's original Git tree (unavailable to current receiver), its ZIP/bundle bytes (materialisation refused), all 4,024 tracked paths individually, complete original F02 review raw attachments, current PostgreSQL executable runtime, current full wheelhouse execution or any new product test. None of these are misreported as inspected.

**T01 outcome:** documented evidence and a conditional successor-authority proposal; **not** an installed active root plan, a released recovered checkpoint or resumed NVIDIA implementation.