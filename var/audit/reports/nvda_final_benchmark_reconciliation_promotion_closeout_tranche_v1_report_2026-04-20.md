# NVDA final benchmark reconciliation / promotion closeout tranche v1 — closeout report

Date: 2026-04-20

## Exact promoted baseline and final tranche branch

- required pre-tranche `main`: `5a0bafb74b0a512cd32efae548501b1366d9b161`
- promoted `main`: `fdecdf1b14d59ee9f7ab1446ecf00cc70c1a9005`
- final tranche branch: `work/final-benchmark-reconciliation-promotion-closeout-tranche-v1-20260420`
- branch HEAD immediately before this report-closeout leaf: `e5603da6d41741fb46d014513a9725c9593f4f16`
- verified `git merge-base main HEAD`: `fdecdf1b14d59ee9f7ab1446ecf00cc70c1a9005`

## Direct answer

The current repo now satisfies the migration programme and the benchmark blueprint **by lineage and explicit reservation resolution**.

Literal benchmark-home count remains **21 / 24**.
The remaining three literal absences are no longer open drift:

- `src/nvda_desk/legacy/imported/` → **retired / quarantined benchmark reservation**
- `src/nvda_desk/analysis/scenarios/` → **resolved reserved absence / containment**
- `src/nvda_desk/observability/` → **resolved reserved absence / containment**

No benchmark item remains unknown / unreconciled.

## Final benchmark matrix

| Layer | Workbook home | Workbook status | Final classification | Direct evidence |
|---|---|---:|---|---|
| Entry | `nvda_desk.entry` | Locked | physically present native home | `src/nvda_desk/entry/` |
| API | `nvda_desk.api` | Locked | physically present native home | `src/nvda_desk/api/` |
| Config | `nvda_desk.config` | Locked | physically present native home | `src/nvda_desk/config/` |
| Reference | `nvda_desk.reference` | Locked | physically present native home | `src/nvda_desk/reference/` |
| Ingress | `nvda_desk.ingress` | Locked | physically present native home | `src/nvda_desk/ingress/` |
| Preparation | `nvda_desk.preparation` | Locked | physically present native home | `src/nvda_desk/preparation/` |
| Schemas | `nvda_desk.schemas` | Locked | physically present native home | `src/nvda_desk/schemas/` |
| Packets | `nvda_desk.packets` | Locked | physically present native home | `src/nvda_desk/packets/` |
| Cognition Ingress | `nvda_desk.cognition.ingress` | Locked | physically present native home | `src/nvda_desk/cognition/ingress/` |
| Serial Cognition | `nvda_desk.cognition.serial` | Locked | physically present native home | `src/nvda_desk/cognition/serial/` |
| Modifier | `nvda_desk.cognition.modifiers` | Locked | physically present native home | `src/nvda_desk/cognition/modifiers/` |
| Risk Parallel | `nvda_desk.risk.parallel` | Locked | physically present native home | `src/nvda_desk/risk/parallel/` |
| Risk Join | `nvda_desk.risk.join` | Locked | physically present native home | `src/nvda_desk/risk/join/` |
| Capital | `nvda_desk.capital` | Locked | physically present native home | `src/nvda_desk/capital/` |
| Downstream | `nvda_desk.downstream` | Locked | physically present native home | `src/nvda_desk/downstream/` |
| Persistence | `nvda_desk.persistence` | Locked | physically present native home | `src/nvda_desk/persistence/` |
| Calendar Projection | `nvda_desk.calendar.reference` | Locked | physically present native home | `src/nvda_desk/calendar/reference/` |
| Operational Event Store | `nvda_desk.calendar.operational` | Locked | physically present native home | `src/nvda_desk/calendar/operational/` |
| Imported Modules | `nvda_desk.legacy.imported` | Provisional | retired / quarantined benchmark reservation | `legacy_import/README.md` |
| Replay & Evaluation | `nvda_desk.analysis.replay` | Locked | physically present native home | `src/nvda_desk/analysis/replay/` |
| Carry / Overnight / SLV | `nvda_desk.analysis.scenarios` | Provisional | resolved reserved absence / containment | `tests/tier_a/analysis/test_replay_evaluation_surface.py` |
| Testing | `nvda_desk.testing` | Locked | physically present native home | `src/nvda_desk/testing/` |
| Observability | `nvda_desk.observability` | Provisional | resolved reserved absence / containment | `tests/tier_a/observability/test_observability_reservation_surface.py` |
| Migrations | `nvda_desk.persistence.migrations` | Locked | physically present native home | `src/nvda_desk/persistence/migrations/` |

## Final reserved / provisional disposition list

1. `legacy.imported`
   - Workbook state: provisional / reserved.
   - Current repo truth: no native package at `src/nvda_desk/legacy/imported/`.
   - Reconciled disposition: **retired / quarantined benchmark reservation**.
   - Governing evidence: `legacy_import/README.md`, `tests/tier_a/legacy_imported/test_imported_module_containment_surface.py`, and `var/audit/reports/nvda_imported_module_subsystem_disposition_tranche_v1_report_2026-04-20.md`.

2. `analysis.scenarios`
   - Workbook state: provisional.
   - Current repo truth: no native package at `src/nvda_desk/analysis/scenarios/`; replay remains the admitted analysis owner.
   - Reconciled disposition: **resolved reserved absence / containment**.
   - Governing evidence: `tests/tier_a/analysis/test_replay_evaluation_surface.py` and `var/audit/reports/nvda_provisional_scenarios_observability_resolution_tranche_v1_report_2026-04-20.md`.

3. `observability`
   - Workbook state: provisional.
   - Current repo truth: no native package at `src/nvda_desk/observability/`.
   - Reconciled disposition: **resolved reserved absence / containment**.
   - Governing evidence: `tests/tier_a/observability/test_observability_reservation_surface.py` and `var/audit/reports/nvda_provisional_scenarios_observability_resolution_tranche_v1_report_2026-04-20.md`.

## Final proof / governance / receipt reconciliation summary

### Frozen governance pack

Observed directly:

- `migration_prebuild/AGENTS.override.md` still routes the active read order through the frozen `00` → `14` stack.
- `migration_prebuild/13_tranche_leaf_commit_promotion_law_2026-04-20.md` still governs one active leaf at a time, one real commit per closed leaf, and tranche-scoped promotion.
- `migration_prebuild/14_frozen_authority_and_mutability_law_2026-04-20.md` still fixes the mutability boundary: frozen migration/audit-history surfaces and live workbook only.

Judgement: **aligned**.

### Locked benchmark workbook by lineage

Observed directly:

- the active closeout benchmark is the locked blueprint workbook at `migration_prebuild/01_nvda_best_practice_blueprint_v3_final.xlsx`;
- the repo workbook-authority lineage docs still keep workbook-derived reference authority discoverable without making the workbook direct runtime truth;
- the current repo now reconciles every `Target_Structure` family either as a physically present native home or as an explicit resolved reservation outcome.

Judgement: **aligned by lineage**.

### Retained proof programme

Observed directly from `config/retained_test_registry.yaml` and the native test tree:

| Benchmark proof family | Closeout status | Evidence |
|---|---|---|
| Typed contracts and validators | retained mirror present | `tests/tier_a/reference_data/`, `tests/tier_a/packets/`, `tests/tier_a/review_runtime/`, `tests/tier_a/parallel_risk/`, `tests/tier_a/upstream_cognition/test_regime_contract_models.py` |
| Config authority separation | retained mirror present | `tests/tier_a/config/test_config_authority_surface.py` |
| Reference vs ingress separation | retained mirror present | `tests/tier_a/reference_data/test_reference_data_contract.py`, `tests/tier_a/ingress/test_raw_bundle_loader_surface.py`, `tests/tier_a/calendar_reference/test_calendar_reference_projection_crosswalk.py` |
| Preparation seam | retained mirror present | `tests/tier_a/upstream_cognition/test_prepared_runtime_substrate_surface.py`, `tests/tier_a/seam_boundaries/test_prepared_ingress_checkpoint_surface.py` |
| Ingress translation | retained mirror present | `tests/tier_a/upstream_cognition/test_cognition_ingress_mapping_surfaces.py`, `tests/tier_a/upstream_cognition/test_cognition_ingress_translation_coordinator.py` |
| Deterministic stage logic | retained mirror present | `tests/tier_a/upstream_cognition/`, `tests/tier_a/serial_recommendation/`, `tests/tier_b/serial_boundaries/` |
| Packet carriage | retained mirror present | `tests/tier_a/packets/test_reference_packet_carriage.py` |
| Modifier lane | retained mirror present | `tests/tier_a/modifiers/test_state_conditioned_modifier_surface.py` |
| Parallel risk lane | retained mirror present | `tests/tier_a/parallel_risk/` |
| Capital authority separation | retained mirror present | `tests/tier_a/capital_deployment/` |
| Persistence domain ownership | retained mirror present | `tests/tier_a/persistence/`, `tests/tier_a/options_flow_history/` |
| Migration lifecycle | retained mirror present | `tests/tier_a/migrations/test_migration_lifecycle_surface.py` |
| Downstream shell honesty | retained mirror present | `tests/tier_a/downstream_runtime/` |
| Imported-module containment | retained mirror present | `tests/tier_a/legacy_imported/test_imported_module_containment_surface.py` |
| Calendar projection vs CRUD split | retained mirror present | `tests/tier_a/calendar_reference/test_calendar_reference_projection_crosswalk.py`, `tests/tier_a/calendar_operational/test_calendar_operational_surface.py` |
| Replay/scenario containment | retained mirror present | `tests/tier_a/analysis/test_replay_evaluation_surface.py` |
| Canonical specimen path | retained mirror present | `tests/tier_a/testing_harnesses/test_canonical_runtime_specimen_surface.py` |

Judgement: **materially aligned and truthful**.

### Live ledger, reports, briefs, and Git chronology

Observed directly:

- the live workbook remains at `var/audit/nvda_running_audit_log.xlsx`;
- the frozen report lineage exists for the executed closeout sequence under `var/audit/reports/`:
  - `nvda_boundary_home_convergence_tranche_v2_report_2026-04-20.md`
  - `nvda_persistence_migration_lifecycle_tranche_v1_report_2026-04-20.md`
  - `nvda_replay_evaluation_specimen_tranche_v1_report_2026-04-20.md`
  - `nvda_api_dto_broker_boundary_resolution_tranche_v1_report_2026-04-20.md`
  - `nvda_imported_module_subsystem_disposition_tranche_v1_report_2026-04-20.md`
  - `nvda_provisional_scenarios_observability_resolution_tranche_v1_report_2026-04-20.md`
- the matching brief lineage exists under `var/audit/briefs/` for the same tranche sequence;
- local `main` has been promoted to `fdecdf1b14d59ee9f7ab1446ecf00cc70c1a9005`;
- the final closeout branch starts from that promoted baseline and `git merge-base main HEAD` equals `fdecdf1b14d59ee9f7ab1446ecf00cc70c1a9005`.

Judgement: **aligned after closeout reconciliation; no unreconciled receipt drift remains hidden behind the three reservation outcomes**.

## Required direct verification

- current benchmark-home physical count: **21 / 24**
- `src/nvda_desk/legacy/imported/`: **absent**
- `src/nvda_desk/analysis/scenarios/`: **absent**
- `src/nvda_desk/observability/`: **absent**
- current branch: `work/final-benchmark-reconciliation-promotion-closeout-tranche-v1-20260420`
- current HEAD immediately before this report-closeout leaf: `e5603da6d41741fb46d014513a9725c9593f4f16`

## Proof floor

Commands run for this tranche:

```bash
PYTHONPATH=src pytest -q tests/tier_a tests/tier_b
python3 -m compileall src tests/tier_a tests/tier_b
```

Observed results:

- `PYTHONPATH=src pytest -q tests/tier_a tests/tier_b` → `104 passed in 2.77s`
- `python3 -m compileall src tests/tier_a tests/tier_b` → clean

## Final repo-status judgement

**accepted — benchmark-reconciled with explicit lawful reservations**

## What is now canonically true

- `main` has been promoted to the accepted rerun state at `fdecdf1b14d59ee9f7ab1446ecf00cc70c1a9005`.
- The final closeout branch begins from that promoted baseline and preserves serial leaf chronology.
- The repo physically carries 21 of the 24 workbook homes.
- The remaining three literal absences are not hidden drift:
  - `legacy.imported` is retired / quarantined;
  - `analysis.scenarios` is a resolved reserved absence;
  - `observability` is a resolved reserved absence.
- No prohibited runtime package was fabricated merely to satisfy literal package counting.
- The retained proof floor is green.

## Carry-forward state

**None.**
