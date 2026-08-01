# Post-alpha M00 Transport Adapter Remediation ExecPlan

**Status:** `ACTIVE:UNIT5_INSTALLED_VALIDATION_CLOSEOUT`
**Created:** 2026-08-02
**Owner:** User-authorised worker under the completed canonical alpha plan
**Canonical parent plan:** `project_control/canonical_project_manager/EXEC_PLAN.md`
**Parent status:** `COMPLETE:ALPHA_CONSOLIDATED_WITH_EXPLICIT_DEBT`
**Debt item:** `ALPHA-DEBT-001`
**Baseline commit:** `ef4aa1ae556df07871eca4ef93777edc189af8ed`
**Worker branch:** `work/post-alpha-m00-transport-adapters-v1`
**Control-pack ID:** `POST-ALPHA-M00-TRANSPORT-ADAPTERS-V1`
**Live pointer:** `ROADMAP_LEDGER_V2.md`
**Current-target full-read manifest:** `project_control/canonical_project_manager/repairs/post_alpha_m00_transport_adapters_20260802/FULL_READ_MANIFEST.tsv`

## 1. Relationship to canonical authority

This is a bounded subordinate debt-remediation plan. It does not replace, amend,
or reopen the accepted M00–M13 alpha semantics or the completed canonical plan.
It implements the already-recorded recommendation for `ALPHA-DEBT-001`: make
CLI and ASGI thin transport adapters to the accepted M00 public seam.

The existing broad `nvda_desk.api.app.HttpApp`, `nvda_desk.api.deps`, and
`DeskRuntimeOrchestrator` remain noncanonical compatibility evidence. This plan
may stop canonical entry surfaces from selecting them; it may not silently
repair them into a competing composition root or claim their removal.

## 2. Objective

Provide one explicit, transport-neutral user-facing route into the accepted M00
contracts by:

1. translating CLI JSON into `ApplicationCommand` or `ApplicationQuery`;
2. translating bounded ASGI requests into the same exact contracts;
3. requiring an explicitly injected `RunCoordinator` with no service locator,
   hidden policy, wall-clock, network read, mutable singleton or fabricated
   identity;
4. returning M00/M12 products without reinterpretation; and
5. preserving all existing module-owner semantics and promotion proof.

## 3. Scope

### In scope

- `src/nvda_desk/entry/cli.py`, `src/nvda_desk/entry/asgi.py`, and
  `src/nvda_desk/entry/__init__.py`;
- a bounded transport-only support module under `src/nvda_desk/entry/` only if
  needed to avoid duplicated JSON/ASGI mechanics;
- `tests/tier_a/entry/test_entry_boundary_surface.py` reauthored as current
  expected-red/current-blocking transport proof;
- the narrow M00 static quarantine assertion that currently forbids every
  legitimate transport import of M00;
- test admission/proof authority, active-control validation, manifests,
  evidence and closeout records required by those changes.

### Out of scope

- M00 command/query/coordinator domain semantics except a proven transport
  compatibility defect;
- M01–M13 owner implementations, policies, decisions or persistence;
- raw-source-to-M03 composition (`ALPHA-DEBT-008`);
- broad `HttpApp`, cached dependency providers or legacy orchestrator repair;
- live data, broker connectivity, durable operation, Tier C or production claims;
- global vocabulary debt or unrelated formatting/refactor work;
- merge, rebase, push, publication or history rewrite.

## 4. Invariants

- Authority remains `user → canonical plan → AGENTS/overrides → this plan →
  normative documents → admitted tests → implementation`.
- M00 remains the only canonical composition root and owns translation,
  dependency assembly and run lifecycle only.
- Entry adapters may import only M00 transport contracts/coordinator and
  transport/mechanical dependencies; they may not import domain-owner modules,
  `api.app`, `api.deps`, `runtime.orchestrator`, clocks or network clients.
- `RunCoordinator` is required explicit input. No default application graph is
  constructed by CLI or ASGI.
- CLI and ASGI must produce equivalent model validation and serialisation
  behaviour for the same command/query payload.
- Query handling remains read-only M12 delegation; command handling remains the
  accepted offline paper path.
- The legacy compatibility surfaces remain visible but noncanonical.

## 5. Acceptance units

### Unit 0 — Register the subordinate pack

**Pass:** baseline and branch identity are exact and clean; this plan and full-read
manifest exist; roadmap/process/control validator identify exactly one active
post-alpha pack; canonical plan remains completed.

### Unit 1 — Admit expected-red transport proof

**Pass:** entry tests state exact CLI/ASGI translation, explicit injection,
contract validation, response/error, query-side-effect and legacy-quarantine
laws; the proof fails only because current entry code selects legacy routes;
registry/proof authority records the family as `next_gate_expected_red`.

### Unit 2 — Implement canonical CLI adapter

**Pass:** typed command/query payloads are parsed by M00 contracts, delegated to
an injected coordinator and serialised without reinterpretation; no legacy
imports or hidden defaults remain in the CLI surface.

### Unit 3 — Implement canonical ASGI adapter

**Pass:** bounded health, command and query routes translate JSON to M00 contracts,
require explicit coordinator injection, return deterministic JSON and fail
closed on malformed input/method/path without domain logic.

### Unit 4 — Promote and reconcile proof

**Pass:** entry family becomes current-blocking; M00 static quarantine permits
only the exact entry adapter imports; admission/proof membership is singular and
all affected Tier A/Tier B controls pass.

### Unit 5 — Installed validation and closeout

**Pass:** clean offline non-editable environment; installed entry smoke; aggregate
promotion gate, Tier B, scoped Black/Ruff and authority reconciliation pass;
plan/roadmap/process return to a closed canonical-alpha-with-debt state with
`ALPHA-DEBT-001` resolved and remaining debt unchanged.

## 6. Prohibited shortcuts

Do not weaken Pydantic validation, add permissive fallback mappings, default a
coordinator, construct domain services in transport code, call the wall clock,
read external state, suppress tests, silently promote compatibility tests, or
remove legacy code merely to satisfy static assertions.

## 7. Evidence and closeout

Record concise reproducible evidence in `VALIDATION_SUMMARY.md` and novel failure
artefacts under `evidence/`. Successful raw output is not committed by default.
Each unit receives a bounded commit. Final closeout must name Git state, exact
commands/counts, receipt hash, unresolved debt and a full-history checkpoint if
requested or required by the active route.

## 8. Progress

- 2026-08-02: user authorised a new subordinate plan and execution for
  `ALPHA-DEBT-001`.
- 2026-08-02: branch `work/post-alpha-m00-transport-adapters-v1` created from
  accepted alpha commit `ef4aa1ae556df07871eca4ef93777edc189af8ed`.
- 2026-08-02: Unit 0 control registration passed; active pack identity reconciles across roadmap, process overlay and proof authority.
- 2026-08-02: Unit 1 admitted the transport family as expected-red. All 15 transport cases fail for the intended legacy-selection/missing-M00-adapter reasons; production source remains unchanged.
- 2026-08-02: Unit 2 implemented the explicit M00 CLI command/query adapter; four focused cases pass.
- 2026-08-02: Unit 3 implemented the minimal ASGI adapter; all 15 transport cases pass.
- 2026-08-02: Unit 4 narrowed M00 import quarantine to the two authorised entry adapters, promoted the entry family to current-blocking, and reconciled 15 proof blocks / 17 paths. Fifty-eight focused tests pass. Unit 5 installed validation and closeout is open.
