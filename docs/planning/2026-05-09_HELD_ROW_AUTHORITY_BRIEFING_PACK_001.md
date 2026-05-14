# HELD_ROW_AUTHORITY_BRIEFING_PACK_001

Date: 2026-05-09
Status: planning-only authority brief pack
Scope: remaining roadmap rows that are held by authority, reservation, or runtime sensitivity

This file is a planning control artefact. It does not open implementation authority.

## 1. Operating rule

The active roadmap now has no unacted, non-held implementation row. Future code work must therefore start by explicitly opening one of the held authority lanes, or by running a planning/reconciliation branch that does not mutate runtime behaviour.

Any future implementation branch must read `AGENTS.md`, `PLANS.md`, `ROADMAP_LEDGER.md`, the relevant architecture-map row, the normative documents for the row, the relevant tests/source/config files, and this brief if the row is held here.

## 2. Recommended order

Recommended implementation-opening order after planning:

1. `roadmap_live_position_and_inventory_architecture`
2. `roadmap_downstream_capital_deployment_authority`
3. `roadmap_parallel_risk_lane`
4. `roadmap_financial_and_event_calendar_architecture`
5. `roadmap_dynamic_coefficient_and_modifier_authority`
6. `roadmap_opening_architecture_and_placement_readiness`
7. `roadmap_playbook_library_architecture`
8. `roadmap_exit_and_close_architecture`

Reason: inventory/state truth should exist before fresh-capital decisions; capital should precede opening placement; independent risk and calendar context should be explicit before coefficient/risk weighting changes; reserved playbook and exit/close rows should not be opened until their architecture reservation is deliberately changed.

## 3. Authority briefs by row

### 3.1 `roadmap_live_position_and_inventory_architecture` — row `5.13`

What it is: the post-entry state system for position, exposure, inventory, and capital-state truth.

What it does: reads execution/fill/state receipts and repository state, then emits live inventory snapshots, position state, exposure state, and capital/inventory receipts.

Why it matters next: it is the cleanest runtime-adjacent row to open first because it can be bounded as state/read/write truth before opening fresh capital, broker placement, or exit behaviour.

Authority phrase required before implementation:

```text
Open row 5.13 live position and inventory architecture for bounded state/read/write hardening only. Do not open broker placement, new candidate formation, raw signal preparation, or ungoverned capital mutation.
```

Likely read set:

- `AGENTS.md`
- `PLANS.md`
- `ROADMAP_LEDGER.md`
- `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md`, row `5.13`
- `docs/07_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_CORE.md`
- `docs/07.1_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_WORKING.md`
- `docs/08_TESTING_AND_PROMOTION_CORE.md`
- `src/nvda_desk/domain/downstream/live_inventory.py`
- `src/nvda_desk/downstream/live_inventory.py`
- `src/nvda_desk/services/downstream_live_inventory_service.py`
- `src/nvda_desk/downstream/state_reader.py`
- `src/nvda_desk/repositories/position_repository.py`
- `src/nvda_desk/repositories/capital_state_repository.py`
- `src/nvda_desk/persistence/receipt_ledger.py`
- `tests/tier_a/downstream_runtime/test_downstream_live_inventory_service_surface.py`
- `tests/tier_a/downstream_runtime/test_downstream_state_reader_service_surface.py`
- `tests/tier_a/persistence/test_position_repository_surface.py`
- `tests/tier_a/persistence/test_capital_state_repository_surface.py`

Likely proof gate:

- Live inventory must consume only lawful execution/state receipts and repository state.
- Reads must be copy-safe and deterministic.
- Writes must reject ungoverned capital mutation and duplicate durable truth.
- No broker placement or new recommendation formation may appear.

### 3.2 `roadmap_downstream_capital_deployment_authority` — row `5.11`

What it is: the downstream decision point that decides whether fresh capital may be deployed after serial and parallel products exist.

What it does: consumes serial candidate material, downstream pre-deployment result, parallel risk packet, capital state, bounded deployment policy, and final join/risk product; emits deploy/stand-down decision, authorised deployable percentage, authorised notional, and capital-deployment receipt.

Why it matters after inventory: fresh-capital authority should not be hardened until live state/capital-state readers are truthful enough to consume.

Authority phrase required before implementation:

```text
Open row 5.11 downstream capital deployment authority for bounded fresh-capital decision contract hardening. Do not open opening placement mechanics, candidate formation, serial-stage decisions, or parallel-risk generation.
```

Likely read set:

- `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md`, row `5.11`
- `docs/07_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_CORE.md`
- `src/nvda_desk/contracts/capital.py`
- `src/nvda_desk/capital/authority.py`
- `src/nvda_desk/domain/capital/deployment.py`
- `src/nvda_desk/services/capital_deployment_service.py`
- `src/nvda_desk/contracts/downstream.py`
- `src/nvda_desk/risk/join/final_join.py`
- `tests/tier_a/capital_deployment/*`

Likely proof gate:

- Capital authority must not form the candidate.
- Capital authority must not generate parallel risk.
- Bounds must be explicit and deterministic.
- Receipt must identify inputs and output without opening placement mechanics.

### 3.3 `roadmap_parallel_risk_lane` — row `5.8`

What it is: the independent risk assessment lane outside the serial desk-cognition path.

What it does: consumes bounded serial packets, risk context, market/caution context, and configuration authority; emits a parallel risk packet, independent risk envelope, and caution/block signals.

Why it matters after capital/inventory planning: it is a separate product that capital authority may consume, but it must stay independent from serial candidate formation and capital sizing.

Authority phrase required before implementation:

```text
Open row 5.8 parallel risk lane for bounded independent risk packet hardening. Do not open serial candidate formation, capital deployment sizing, serial-stage mutation, or hidden upstream reads.
```

Likely read set:

- `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md`, row `5.8`
- `docs/07_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_CORE.md`
- `src/nvda_desk/contracts/parallel_risk.py`
- `src/nvda_desk/domain/parallel_risk/*`
- `src/nvda_desk/risk/parallel/evaluate.py`
- `src/nvda_desk/services/parallel_risk_lane_service.py`
- `src/nvda_desk/persistence/parallel_risk_observations.py`
- `tests/tier_a/parallel_risk/*`
- `tests/tier_b/serial_boundaries/*`

Likely proof gate:

- Risk packet is independent from serial internals.
- Inputs are bounded packets only.
- Hidden reads are rejected.
- Output remains risk context, not deployment authority.

### 3.4 `roadmap_financial_and_event_calendar_architecture` — row `5.4`

What it is: checked calendar truth, event reference material, event projection, and calendar-derived runtime context.

What it does: imports checked-in calendar/reference sources and emits calendar authority packets, event projections, and session/event context for preparation.

Why it matters later: calendar truth affects runtime context and risk interpretation, so it needs a clean authority opening before it can affect behaviour.

Authority phrase required before implementation:

```text
Open row 5.4 financial and event calendar architecture for bounded checked-reference/calendar projection hardening. Do not open trading instructions, capital sizing, online calendar mutation, or candidate formation.
```

Likely read set:

- `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md`, row `5.4`
- `src/nvda_desk/calendar/reference/importer.py`
- `src/nvda_desk/calendar/reference/projection.py`
- `src/nvda_desk/calendar/operational/events.py`
- `src/nvda_desk/reference/calendar_import.py`
- `src/nvda_desk/reference/calendar_projection.py`
- `src/nvda_desk/contracts/reference_data.py`
- `tests/tier_a/calendar_reference/test_calendar_reference_projection_crosswalk.py`
- `tests/tier_a/calendar_operational/test_calendar_operational_surface.py`

Likely proof gate:

- Checked reference material is deterministic.
- Event projection is replayable.
- Calendar output does not become a trading instruction or capital decision.

### 3.5 `roadmap_dynamic_coefficient_and_modifier_authority` — row `5.9`

What it is: bounded coefficient, threshold, modifier, and state-conditioned adjustment authority.

What it does: consumes governed coefficient config and admitted state/runtime context; emits bounded coefficients, modifier packets, and applied-threshold decisions.

Why it is high blast-radius: coefficients can silently change behaviour across serial, risk, playbook, and review surfaces, so they must be governed and replayable before they influence runtime.

Authority phrase required before implementation:

```text
Open row 5.9 dynamic coefficient and modifier authority for bounded config/schema/replay hardening. Do not open unbounded runtime mutation, hidden strategy changes, capital deployment decisions, or source-data ingestion.
```

Likely read set:

- `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md`, row `5.9`
- `src/nvda_desk/config/coefficient_authority.py`
- `src/nvda_desk/config/bundle_loader.py`
- `src/nvda_desk/contracts/coefficient_authority.py`
- `src/nvda_desk/contracts/modifiers.py`
- `src/nvda_desk/cognition/modifiers/state_conditioned.py`
- `src/nvda_desk/services/coefficient_authority_service.py`
- `config/coefficient_authority.v1.yaml`
- `tests/tier_a/config/test_sequence8_coefficient_modifier_authority_specimen.py`
- `tests/tier_a/modifiers/test_state_conditioned_modifier_surface.py`

Likely proof gate:

- Config schema and bounds are explicit.
- State-conditioned modifier output is deterministic.
- Coefficients cannot hide a strategy change or capital decision.

### 3.6 `roadmap_opening_architecture_and_placement_readiness` — row `5.12`

What it is: downstream opening authorisation, placement readiness, and handoff structure after deployment authority.

What it does: consumes capital deployment decision, candidate execution material, account/broker readiness context, and placement constraints; emits opening snapshot, readiness result, and placement handoff material.

Why it is late-order: it sits close to order placement, so capital and inventory boundaries should be cleaner first.

Authority phrase required before implementation:

```text
Open row 5.12 opening architecture and placement readiness for bounded contract/readiness hardening only. Do not open broker adapter implementation, live order placement, capital sizing, serial candidate formation, or parallel risk evaluation.
```

Likely read set:

- `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md`, row `5.12`
- `src/nvda_desk/downstream/opening.py`
- `src/nvda_desk/domain/downstream/opening.py`
- `src/nvda_desk/services/downstream_opening_service.py`
- `src/nvda_desk/contracts/downstream.py`
- `src/nvda_desk/contracts/execution.py`
- `src/nvda_desk/adapters/egress/broker_protocol.py`
- `tests/tier_a/downstream_runtime/test_downstream_opening_service_surface.py`
- `tests/tier_a/adapters_egress/test_broker_boundary_surface.py`

Likely proof gate:

- Opening readiness consumes capital authority output, not raw serial/risk internals.
- Broker adapter remains a boundary/protocol, not live placement behaviour.
- Placement handoff is explicit and non-executing.

### 3.7 `roadmap_playbook_library_architecture` — row `5.10`

What it is: target home for governed playbook definitions, eligibility constraints, play selection rules, and proofable playbook metadata.

What it does: emits playbook candidates, eligibility results, and playbook metadata receipts from vocabulary-lawful playbook definitions and governed context.

Why it is reserved: the blueprint marks the row reserved pending later admissibility and implementation evidence.

Authority phrase required before implementation:

```text
Open reserved row 5.10 playbook library architecture for bounded registry/eligibility planning or implementation, with explicit permission to change reserved architecture status. Do not open capital deployment, raw source ingestion, uncontrolled strategy mutation, or hidden coefficient ownership.
```

Likely read set:

- `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md`, row `5.10`
- `docs/10_VOCABULARY_AND_TERM_GOVERNANCE_CORE.md`
- `src/nvda_desk/config/playbook_registry.py`
- `src/nvda_desk/domain/eligibility/playbook_compilation.py`
- `src/nvda_desk/services/playbook_eligibility_service.py`
- `src/nvda_desk/contracts/eligibility.py`
- `config/playbook_registry.example.yaml`
- `tests/tier_b/serial_boundaries/test_playbook_eligibility_decontamination.py`

Likely proof gate:

- Playbook registry stays explicit and vocabulary-lawful.
- Eligibility does not smuggle capital deployment or coefficient ownership.
- Reserved status is changed only by explicit authority.

### 3.8 `roadmap_exit_and_close_architecture` — row `5.14`

What it is: target home for exit strategy, close execution, trimming, profit-taking, trailing stop, and position wind-down behaviour.

What it does: consumes live position state, risk context, playbook/exit policy, market state, and broker/execution constraints; emits exit decision, close handoff, exit receipt, and closure state.

Why it is last-order: it depends on live inventory truth and sits near broker/execution behaviour; the blueprint marks it reserved.

Authority phrase required before implementation:

```text
Open reserved row 5.14 exit and close architecture for bounded planning or contract hardening, with explicit permission to change reserved architecture status. Do not open broker execution, hidden live-inventory mutation, initial candidate formation, capital deployment sizing, or raw source ingestion.
```

Likely read set:

- `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md`, row `5.14`
- `src/nvda_desk/domain/downstream/live_inventory.py`
- `src/nvda_desk/downstream/live_inventory.py`
- `src/nvda_desk/contracts/downstream.py`
- `src/nvda_desk/adapters/egress/broker_protocol.py`
- `tests/tier_a/downstream_runtime/test_downstream_live_inventory_service_surface.py`
- `tests/tier_a/adapters_egress/test_broker_boundary_surface.py`

Likely proof gate:

- Exit/close contracts consume live inventory truth only through lawful state seams.
- Any broker/execution detail remains a handoff protocol unless live execution authority is opened.
- Reserved status is changed only by explicit authority.

## 4. Next planning branch if work resumes

Recommended next planning-only branch:

```text
SANDBOX_PACKAGE_ACCEPTANCE_RECONCILIATION_001
```

Purpose: reconcile local commits, reset-safe TAR outputs, receipt files, and ledger row states so a future merge/replay pass knows exactly what is local-sandbox truth, what is packaged, and what is externally accepted.

Stop after that reconciliation if the user has not opened runtime implementation authority.
