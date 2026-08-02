# Post-alpha Comprehensive Material-Debt Retirement ExecPlan

## Status

**Status:** `ACTIVE:UNIT7_VOCABULARY_ADJUDICATION`
**Created:** 2026-08-02
**Owner:** User-authorised worker under the completed canonical alpha plan
**Canonical parent plan:** `project_control/canonical_project_manager/EXEC_PLAN.md`
**Parent status:** `COMPLETE:ALPHA_CONSOLIDATED_WITH_EXPLICIT_DEBT`
**Baseline commit:** `d4bffb8f95141e95353182c3e4c6e6ddc8e15472`
**Worker branch:** `work/post-alpha-comprehensive-debt-retirement-v1`
**Control-pack ID:** `POST-ALPHA-COMPREHENSIVE-DEBT-RETIREMENT-V1`
**Live pointer:** `ROADMAP_LEDGER_V2.md`
**Current-target full-read manifest:** `project_control/canonical_project_manager/repairs/post_alpha_comprehensive_debt_retirement_20260802/FULL_READ_MANIFEST.tsv`

## Objective

Retire every unresolved material-debt item recorded at the accepted post-alpha
baseline, without reopening accepted M00–M13 meaning except where an admitted
new proposition requires a bounded extension. The programme covers:

1. `ALPHA-DEBT-006` — migrate the stale promotion-set identifier while preserving historical receipt comparability;
2. `ALPHA-DEBT-008` — compose canonical M01 source admission, M02 calendar projection and M03 preparation into the user-facing M00 workflow;
3. `ALPHA-DEBT-005` — add exact owner-fact contracts so M06 concentration, inventory and liquidity observations are complete when authorised evidence exists and remain explicit unknowns otherwise;
4. `ALPHA-DEBT-004` — establish durable state/evidence storage, restart recovery and explicit live-provider/broker adapter boundaries with fail-closed operational safety;
5. `ALPHA-DEBT-002` — define and admit Tier C operational assurance against the concrete surfaces created by this programme; and
6. `ALPHA-DEBT-003` — human-adjudicate the current vocabulary candidates one namespace and one exact occurrence at a time until all admitted namespaces rerun clean or a precisely evidenced hard blocker remains.

`ALPHA-DEBT-001` and `ALPHA-DEBT-007` remain closed controls and are not
reimplemented.

## Authority

Authority order is:

`user instruction → canonical plan → AGENTS/overrides → this plan → routed normative documents → admitted proof → implementation/configuration → evidence`.

This plan is subordinate to the completed canonical plan. It may add post-alpha
normative propositions, tests and implementation required to retire the listed
debt; it may not rewrite historical acceptance or weaken existing proof.

## Invariants

- M00 remains the canonical application composition owner.
- M01 owns source identity/admission; M02 owns calendar truth; M03 owns prepared-data truth.
- M06 consumes owner-issued facts and never fabricates concentration, inventory or liquidity evidence.
- M09 remains the first final risk/capital join; upstream operational work cannot bypass it.
- M10 live submission is impossible unless explicit live mode, credentials, safety interlocks and an authorised broker adapter are all present.
- Durable repositories preserve atomicity, idempotency, lineage and restart truth; process memory is never represented as durable truth.
- Tier C is admitted only for slow operational/integration claims that cannot be established by Tier A/B; it is not a dumping ground.
- Vocabulary adjudication is semantic human judgement. Scripts may inventory and validate but cannot auto-accept dispositions.
- Existing resolved debt, historical receipts and accepted module semantics remain intact unless a current failing proposition proves a bounded incompatibility.
- No profitability claim, autonomous strategy mutation or unrestricted live trading authority is introduced.

## Scope

### In scope

- subordinate control, normative overlays, propositions, test admission/proof selection and evidence for the six unresolved debt items;
- M00/M01/M02/M03 transport and composition surfaces required for raw-source-to-prepared-data operation;
- exact M06 owner-fact contracts and bounded M11/M13 read models needed to supply them;
- durable M13-compatible repositories and restart recovery for accepted state/evidence surfaces;
- explicit market-data and broker ports/adapters, operational mode/safety configuration and hermetic substitutes;
- Tier C tests for installed, restart, durable, provider-substitution, broker-safety and end-to-end operational paths;
- vocabulary registry/dispositions/touch stamps and exact source/docs/test wording required by adjudication;
- promotion-key migration with compatibility alias/receipt verification as required.

### Out of scope

- changing trading strategy, playbook eligibility, coefficient policy, capital-sizing policy or lifecycle policy merely to make operational tests pass;
- real-money order submission during validation;
- storing or committing credentials;
- external provider/broker account creation, funding, entitlement purchase or human approval;
- profitability, production SLO or regulatory certification claims;
- merge, rebase, push, publication or history rewrite.

## Acceptance units

### Unit 0 — Register the comprehensive subordinate pack

**Pass:** exact baseline and branch are clean; this plan and current full-read
manifest exist; roadmap/process/proof authority identify exactly this active
pack; canonical plan remains completed.

### Unit 1 — Promotion-set identifier migration (`ALPHA-DEBT-006`)

**Required reads:** testing/promotion core and working documents, proof schema,
runner, Make/CI and historical receipt evidence.

**Pass:** a current semantic promotion key replaces `pre_m00_current`; legacy
key use is either a verified compatibility alias or rejected with an explicit
migration error; existing receipts remain independently verifiable; aggregate
membership is unchanged before later units.

### Unit 2 — Canonical raw-source-to-M03 workflow (`ALPHA-DEBT-008`)

**Required reads:** M00, M01, M02, M03 normative propositions, public contracts,
entry adapters and all affected tests in full.

**Pass:** one explicit application request carries raw source facts and calendar
inputs through M01 admission, M02 projection and M03 preparation before the
existing M00 paper command; owner outputs and lineage remain exact; transports
contain no domain logic; expected-red proof precedes implementation.

### Unit 3 — M06 owner-fact completeness (`ALPHA-DEBT-005`)

**Required reads:** M06 risk law, M11 inventory/portfolio contracts, M13 read
ports and the accepted M00 composition path.

**Pass:** exact concentration, inventory and liquidity owner-fact contracts are
supplied from authorised owner repositories/providers; complete facts yield
typed observations; absent/stale facts remain explicit unknown/degraded; no
facts are inferred or fabricated.

### Unit 4 — Durable state, evidence and restart recovery (`ALPHA-DEBT-004A`)

**Required reads:** M10–M13 state/transaction/replay law and current repository
ports/implementations.

**Pass:** a transactional durable backend implements the accepted state/evidence
ports, survives process restart, preserves idempotency and receipt lineage, and
can rebuild authoritative M11/M12 views without process-memory claims.

### Unit 5 — Explicit live-provider and broker operational boundary (`ALPHA-DEBT-004B`)

**Required reads:** M01 external-source law, M10 execution law, broker boundary,
configuration and safety doctrine.

**Pass:** concrete adapter boundaries exist for live market data and broker
submission; default and test modes are offline/fail-closed; live mode requires
explicit credentials/configuration, kill switch and account/environment match;
no validation submits a real order. A missing credential or unavailable external
endpoint is reported as a hard operational blocker, not bypassed.

### Unit 6 — Tier C operational assurance (`ALPHA-DEBT-002`)

**Required reads:** testing/promotion doctrine and every operational surface
created in Units 2–5.

**Authorised bounded existing-proof support extension:** `tests/support/m00_application_shell_contract_harness.py` and `tests/support/m09_k11_k14_contract_harness.py` may accept one optional already-validated `PreparedDataEnvelope` so Tier C can prove that the exact M03 owner product enters the existing M00 run. Existing Tier A assertions and default fixture behaviour must remain unchanged.

**Pass:** Tier C has explicitly admitted slow tests for raw-source-to-paper,
durable restart/recovery, provider substitution, broker safety and installed
operation; the route is separately executable and cannot enter ordinary Tier A
promotion accidentally.

### Unit 7 — Vocabulary adjudication (`ALPHA-DEBT-003`)

**Required reads:** vocabulary core/working law, canonical registry, audit tool,
all exact candidate contexts and directly governed module vocabulary.

**Pass:** each current candidate is read and dispositioned one namespace at a
time; accepted wording/aliases are changed only where semantically warranted;
module and global audits rerun clean, or remaining candidates are listed as
hard blockers with exact unavailable authority. Counts alone are not acceptance.

### Unit 8 — Aggregate closeout

**Pass:** all targeted and affected proofs, current Tier A promotion, Tier B,
Tier C, installed-package, style/lint, authority, vocabulary and Git checks pass;
material-debt register is reconciled truthfully; exact remaining external
blockers are recorded; a full-history checkpoint is produced and independently
verified.

## Validation route

Validation increases from unit-local proof to affected module proof, current
promotion, Tier B shadow, Tier C operational route, installed-package smoke,
style/lint, vocabulary and archive integrity. No unexecuted command is called a
pass. External live connectivity is never simulated into a production claim.

## Prohibited shortcuts

No skips/xfails, weakened assertions, fabricated owner facts, fake durability,
credential fallbacks, implicit live mode, silent network use, source-to-M03
logic in transport code, mass vocabulary replacement, generated disposition
acceptance, broad suppression or edited proof evidence.

## Evidence

- Plan and manifest: this directory.
- Unit evidence: `evidence/UNIT<n>_*.md` and concise machine-readable artefacts.
- Validation summary: `VALIDATION_SUMMARY.md`.
- Updated debt register: canonical final-alpha consolidation directory, only at
  evidenced unit closeout.

## Progress

- 2026-08-02: user explicitly authorised one subordinate plan covering all remaining material debt and instructed execution.
- 2026-08-02: branch `work/post-alpha-comprehensive-debt-retirement-v1` created from `d4bffb8f95141e95353182c3e4c6e6ddc8e15472`.
- 2026-08-02: Unit 0 passed: exact branch/baseline, singular active control pack, 15 proof-authority contract tests, live authority reconciliation, Black/Ruff and manifest validation.
- 2026-08-02: Unit 1 passed: `alpha_current` is the canonical promotion key; `pre_m00_current` is a membership-identical compatibility alias; 39 focused control tests pass and all retained legacy receipts verify.
- 2026-08-02: Unit 2 passed: the expected-red M00 upstream proof is implemented; M01 issues distinct source-artifact identity, M02 projection lineage enters M03, and canonical CLI/ASGI preparation routes are current-blocking.
- 2026-08-02: Unit 4 passed: bounded SQLite M13 state/receipt and typed evidence ports survive restart, preserve exact idempotency/conflict/rollback truth, and restore M11 fill/lifecycle history plus M12 replay material; 237 affected tests pass and proof authority resolves 18 blocking blocks.
- 2026-08-02: Unit 5 passed: explicit live-placement, provider and broker boundaries are offline/fail-closed by default, require injected transports and credentials, retain M00 paper-only semantics, and pass 138 affected tests with 19 current promotion blocks.
- 2026-08-02: Unit 6 passed at working-tree validation: five separately executable Tier C operational cases pass; the family is current-nonblocking and excluded from `alpha_current`; final clean-commit rerun is recorded in Unit 7 entry validation.
- 2026-08-02: Unit 6 exact clean-commit validation passed at `bb44560`: installed-package smoke, Tier C 5/5, alpha promotion 19/19 with 802 tests, Tier B 90/90, Black and Ruff.
