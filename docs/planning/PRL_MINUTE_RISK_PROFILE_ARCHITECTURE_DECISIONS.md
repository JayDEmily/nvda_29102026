# PRL minute-level risk profile architecture decisions

Status: `accepted`
Branch: `work/prl-minute-risk-profile-architecture-decisions`
Baseline commit: `3c5b1db57704c56445bc382c83faa536c1586a6b`

This document is an architecture-comprehension and decision-resolution artefact only. It does not implement `PRL-MRP-003` or any later runtime behaviour.

## 1. Context

The accepted master roadmap left four open design questions that should be resolved before further implementation leaves proceed:

1. Which config surface owns freshness age thresholds after deterministic defaults?
2. What exact promotion artefact carries the workbook `Parallel Risk Lane Signal Inventory` into runtime config/contracts?
3. Should VIX coefficient-authority reconciliation preserve current hardcoded behaviour as compatibility mode?
4. Where should deterministic description templates live: config, vocabulary data, or a dedicated template registry?

This pass reads the repo as a governed system rather than as a generic schema exercise. It resolves those questions using repo-native architecture, runtime ownership, workbook authority, vocabulary governance, existing tests, and trader-cognition intent.

## 2. Accepted baseline

- The Parallel Risk Lane is an independent lane that assesses the present environment while the serial desk-cognition spine forms the candidate. It does not form the candidate. Evidence: `docs/03_DOMAIN_MODEL_CORE.md:64-72`.
- The lane does not allocate capital and is not a numbered serial stage. Evidence: `docs/01_NORMATIVE_CORE.md:71-79`.
- Runtime ownership says the lane output answers what the independent lane concluded about the present environment, not what candidate was formed. Evidence: `docs/07_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_CORE.md:106-118`.
- Working ownership restricts row `5.8` to admitted temporal/regime/options-flow primitives or selected temporal serial-stage packets and forbids capital sizing, broker placement, order execution, candidate formation, coefficient/modifier policy, review explanation authority, and hidden portfolio mutation. Evidence: `docs/07.1_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_WORKING.md:66-72`.
- The native architecture blueprint identifies the current implementation-truth status as `thin_seam`; lawful outputs are a parallel risk packet, independent risk envelope, and caution/block signals. Evidence: `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:254-269`.
- Workbook content cannot become runtime truth by direct read; the lawful lineage is workbook concept/cell, typed promotion into config/contracts with lineage, then runtime consumption from typed config/contracts only. Evidence: `docs/reference/SIGNAL_WORKBOOK_AUTHORITY.md:26-35`.
- Vocabulary governance is an admission system, not a free-form glossary. Durable terms cannot land in live surfaces without governance. Evidence: `docs/10_VOCABULARY_AND_TERM_GOVERNANCE_CORE.md:6-34` and `docs/vocabulary/README.md:18-23`.
- The currently implemented enriched contract surface is metadata-only: `AuthorityFlags` default-denies forbidden authorities, `SignalSnapshotEntry` has workbook-lineage metadata only, and `ParallelRiskMinuteProfile` carries template/vocabulary refs without rendering text. Evidence: `src/nvda_desk/contracts/parallel_risk.py:142-169`, `src/nvda_desk/contracts/parallel_risk.py:172-195`, and `src/nvda_desk/contracts/parallel_risk.py:295-329`.

## 3. Human-level system comprehension

### 3.1 What the Parallel Risk Lane is for

The Parallel Risk Lane is a bounded runtime authority for independent environmental-risk description. Its minute-level future product should answer: what is dangerous, fragile, crowded, stale, asymmetric, illiquid, event-sensitive, cognitively demanding, or structurally unusual about the current market instance. It is not a generic analytics bucket; it is a separate row `5.8` runtime lane with its own output and trace.

Evidence:

- Domain model: assesses present environment while the serial spine forms candidate: `docs/03_DOMAIN_MODEL_CORE.md:64-72`.
- Runtime ownership: output describes the lane's conclusion about the present environment: `docs/07_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_CORE.md:106-118`.
- Native architecture: purpose is independent risk assessment outside serial desk-cognition spine: `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:254-263`.

### 3.2 What it is explicitly not allowed to do

The lane must not form candidates, select playbooks, allocate capital, size positions, issue orders, mutate serial-stage internals, become review judgement, or read workbook/reference artefacts directly at runtime.

Evidence:

- Top-level normative prohibition: `docs/01_NORMATIVE_CORE.md:71-79`.
- Working row `5.8` forbidden mixing: `docs/07.1_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_WORKING.md:66-72`.
- Contract-level forbidden keys: `src/nvda_desk/contracts/parallel_risk.py:21-41`.
- Evaluator hidden-key rejection: `src/nvda_desk/risk/parallel/evaluate.py:177-243`.
- `AuthorityFlags` validator rejects any true forbidden authority flag: `src/nvda_desk/contracts/parallel_risk.py:142-169`.

### 3.3 How trader-cognition intent maps to runtime architecture

The trader-cognition sources are asking for disciplined conditionality, not strategy churn. The trader adapts stance, permissions, expression, and emphasis from evolving conditions, while contextualising headlines and asking what changed, what is priced, what the options surface implies, what kind of day it is, and which playbooks are valid. Evidence: `/mnt/data/a serious trader does not wake up each day with a brand-new strategy….md:1-15`.

For PRL, that means the lane should describe the environment and confidence/uncertainty inputs that make the moment dangerous. It should not choose the playbook or expression. Event calendar material belongs first as routing/context/risk metadata, not a heavy predictive signal. Evidence: `/mnt/data/a serious trader does not wake up each day with a brand-new strategy….md:243-287`.

The GS transcript widens the desired signal surface to VWAP, realised vol, IV rank, implied move, skew, gamma exposure, OI changes, dealer pressure, spread/depth, VIX/VVIX, event hooks, and unusual flow. Evidence: `/mnt/data/GS_Tier1_Desk_Transcript.md:236-366`. It also maps day phases such as open chaos, order-book stabilisation, lunch drift, and closing auction prep. Evidence: `/mnt/data/GS_Tier1_Desk_Transcript.md:586-712`. Those are future environmental-risk descriptions, not current lawful values unless typed sources exist.

### 3.4 How current code implements only a thin seam

Current PRL code builds an environment assessment and risk envelope around source temporal/window metadata, VIX level, and front/next DTE relation. `assess_environment` mostly copies temporal/window context. `assess_risk_envelope` adds caution for scheduled event tag, DTE inversion, and VIX >= 30, and hard block for VIX >= 50. Evidence: `src/nvda_desk/domain/parallel_risk/environment_assessment.py:14-107`.

The evaluator can build bootstrap packets, evaluate the lane packet, and reject forbidden authority keys; market translation enrichment is explicitly not implemented. Evidence: `src/nvda_desk/risk/parallel/evaluate.py:93-132` and `src/nvda_desk/risk/parallel/evaluate.py:177-243`.

### 3.5 How workbook governance affects signal inventory

The expected signal inventory belongs in the governed workbook as a reference/governance artefact, but runtime must consume only typed promoted config/contracts. The workbook authority doc is explicit: direct runtime reads are forbidden; typed promotion into config/contracts with lineage is the lawful path. Evidence: `docs/reference/SIGNAL_WORKBOOK_AUTHORITY.md:26-35`.

The signal-inventory work should therefore create and later promote a `Parallel Risk Lane Signal Inventory` workbook tab, but runtime expected-signal checks must load a typed promotion artefact, not the workbook.

### 3.6 How vocabulary governance affects plain-English output

Plain-English PRL description must not be free-form generation. The vocabulary system is an admission process, and the canonical vocabulary file/schema/generator are the authoritative artefacts. Evidence: `docs/10_VOCABULARY_AND_TERM_GOVERNANCE_CORE.md:13-34`, `docs/vocabulary/README.md:18-23`, and `docs/vocabulary/CONSOLIDATION_WORKFLOW.md:3-22`.

The governed term `Parallel Risk Lane` is already registered as the independent parallel risk authority lane producing risk packet material without reading or mutating serial candidate formation. Evidence: `docs/vocabulary/vocabulary_registry.md:161-163`.

Description output must therefore be deterministic and template-governed, with references to canonical vocabulary terms. It should not store templates inside the canonical vocabulary file, because vocabulary governance says that folder is not a runtime redesign surface and not a free-form glossary. Evidence: `docs/vocabulary/README.md:12-23`.

### 3.7 How tests enforce authority boundaries

The existing test surface protects PRL contracts, evaluator behaviour, forbidden authority-key rejection, candidate fragility as descriptive-only, calendar context-only authority, source temporal truth, upstream quarantine boundaries, workbook-boundary specimens, and vocabulary governance. These tests should be extended incrementally rather than bypassed.

Examples:

- Existing PRL contract/evaluation tests are the guard for contract regressions and hidden authority expansion.
- Financial-calendar runtime snapshot explicitly has `candidate_formation_allowed = False` and `capital_sizing_allowed = False`; evidence in implementation: `src/nvda_desk/calendar/operational/events.py:55-62`.
- Source temporal truth must preserve source/capture/persist separation: `docs/04.1_TECHNICAL_ARCHITECTURE_WORKING.md:18-37`.

### 3.8 What implementation drift would look like in this repo

Implementation drift would include:

- adding useful-looking Bloomberg-style values before typed upstream sources exist;
- using the workbook directly at runtime because it is convenient;
- silently switching VIX thresholds from current PRL behaviour to coefficient-authority posture thresholds;
- emitting plain-English prose not tied to deterministic templates and canonical vocabulary;
- using risk-family states as implicit capital permission;
- hiding candidate/playbook/order/sizing semantics in a `risk` field;
- changing service/evaluator semantics before contract/domain tests define the new packet surface;
- marking deferred rich signal families as implemented because the schema can name them.

The roadmap must keep future leaves small because each of those drift modes crosses a repo boundary.

## 4. Runtime/dataflow map

| Layer | Current artefact/file | Current capability | Future PRL role | Boundary risk | Evidence |
|---|---|---|---|---|---|
| Raw source/capture temporal fields | `src/nvda_desk/contracts/temporal.py`; `docs/04.1_TECHNICAL_ARCHITECTURE_WORKING.md` | Preserves source time, capture time, persisted time, provider/channel/granularity | Freshness register and signal snapshot time basis | Substituting capture/persist time for source time | `docs/04.1_TECHNICAL_ARCHITECTURE_WORKING.md:18-37` |
| Temporal context | `src/nvda_desk/domain/temporal/session_clock.py`; `src/nvda_desk/services/temporal_context_service.py` | Coarse session state, active tags, next event | Session/freshness inputs for minute profile | Over-claiming granular phase before source exists | `src/nvda_desk/services/temporal_context_service.py:17-41` |
| Regime context | `src/nvda_desk/contracts/regime.py`; `src/nvda_desk/domain/regime/classification.py` | NVDA/NQ/VIX input and simple regime output | Current macro/volatility risk signal surface | Treating posture thresholds as PRL thresholds without migration | `src/nvda_desk/domain/regime/classification.py:8-52` |
| Options-flow context | `src/nvda_desk/contracts/options_flow.py`; `src/nvda_desk/domain/options_flow/surface_state.py` | Spot/front DTE/next DTE; simple term-state/skew/gamma fields | Preserve current DTE risk; defer real options surface | Calling current gamma state real dealer gamma | `src/nvda_desk/domain/options_flow/surface_state.py:8-51` |
| Upstream raw signals | `src/nvda_desk/contracts/upstream_signal.py`; `src/nvda_desk/upstream/raw_signal_ingress.py` | Raw signal family/scope/payload admission and quarantine | Missing/quarantined register after typed bridge | Consuming arbitrary raw payload directly | `src/nvda_desk/upstream/raw_signal_ingress.py:14-93` |
| Market substrate | `src/nvda_desk/contracts/market_substrate.py` | Generic observations with family/value/units/source IDs | Future lawful signal snapshot source after typing | Treating generic `value` as semantically typed | `src/nvda_desk/contracts/market_substrate.py:9-51` |
| Calendar events/projection | `src/nvda_desk/calendar/operational/events.py`; `src/nvda_desk/calendar/reference/projection.py` | Context-only runtime snapshot with proximity/materiality; reference projection tags | Event-proximity register and event risk atoms | Letting calendar imply trade permission | `src/nvda_desk/calendar/operational/events.py:35-62`, `src/nvda_desk/calendar/operational/events.py:87-151` |
| Coefficient authority | `config/coefficient_authority.v1.yaml`; `src/nvda_desk/config/coefficient_authority.py` | Typed YAML config with workbook refs and bounded coefficient service | Future governed threshold/config reference where appropriate | Silent behaviour drift from current PRL thresholds | `config/coefficient_authority.v1.yaml:1-37`, `src/nvda_desk/config/coefficient_authority.py:31-58` |
| Signal workbook | `data/reference/signal_workbooks/2026-03-25_NVDA_SIGNAL_WORKBOOK_v3_bounds_handoff_copy.xlsx`; `docs/reference/SIGNAL_WORKBOOK_AUTHORITY.md` | Governed reference workbook; no direct runtime reads | Authoritative expected-signal inventory source before typed promotion | Runtime workbook read | `docs/reference/SIGNAL_WORKBOOK_AUTHORITY.md:26-35` |
| Vocabulary dictionary | `data/vocabulary/canonical_vocabulary.json`; `docs/vocabulary/*` | Canonical terms and admission workflow | Govern terms referenced by deterministic templates | Making vocabulary data a runtime prose engine | `docs/vocabulary/README.md:12-23`, `docs/vocabulary/CONSOLIDATION_WORKFLOW.md:3-22` |
| PRL contracts | `src/nvda_desk/contracts/parallel_risk.py` | Existing packet + new minute profile/atom/snapshot models | Contract carrier for future profile | Adding action/sizing/order fields | `src/nvda_desk/contracts/parallel_risk.py:129-329` |
| PRL evaluator/service | `src/nvda_desk/risk/parallel/evaluate.py`; `src/nvda_desk/services/parallel_risk_lane_service.py` | Packet construction/evaluation and service coordination | Later optional enriched profile assembly/integration | Service API drift before tests | `src/nvda_desk/risk/parallel/evaluate.py:93-132`, `src/nvda_desk/services/parallel_risk_lane_service.py:32-90` |
| Tests/receipts/ledger | `tests/tier_a/parallel_risk/*`; `ROADMAP_LEDGER.md` | Protects contracts, envelope behaviour, authority boundaries | Test-first leaf progression and evidence trail | Claiming readiness without leaf proof | `docs/08_TESTING_AND_PROMOTION_CORE.md:41-48` |

### Proposed lawful data path

```text
workbook/reference doctrine
  → typed promotion artefact with workbook lineage
  → config/contracts admitted by repo governance
  → runtime PRL input/signal snapshot
  → RiskAtomState / SignalSnapshotEntry / registers
  → ParallelRiskMinuteProfile
  → downstream/review consumption as environmental risk only
```

Forbidden shortcut:

```text
runtime PRL → Excel workbook direct read
```

## 5. Decision summary

| Question | Recommended decision | Decision type | Evidence | Rejected alternatives | Why rejected | Implementation impact | Tests required | Roadmap leaves affected |
|---|---|---|---|---|---|---|---|---|
| Which config surface owns freshness age thresholds after deterministic defaults? | Create a dedicated governed PRL profile config surface, initially planned as `config/parallel_risk_lane_profile.v1.yaml`, typed by a future PRL config contract. PRL-MRP-003 uses deterministic defaults only and records threshold IDs/refs as absent until the config leaf opens. | `resolved_with_senior_engineering_judgement` | PRL may consume configuration authority, but source temporal truth must preserve source/capture/persist distinction: `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:262-268`, `docs/04.1_TECHNICAL_ARCHITECTURE_WORKING.md:18-37`. Existing coefficient authority is coefficient/posture-oriented: `config/coefficient_authority.v1.yaml:8-37`. | Coefficient authority owns freshness; hidden constants in domain forever; workbook direct reads. | Freshness is data-quality/runtime observation policy, not posture coefficient authority; hidden constants impede governance; direct workbook runtime reads are forbidden. | Update PRL-MRP-003 to implement deterministic defaults and leave config threshold refs optional; add later config leaf if thresholds need governance. | Unit tests for fresh/stale/unknown using deterministic defaults; no config read in PRL-MRP-003. | PRL-MRP-003, PRL-MRP-021, PRL-MRP-026 |
| What exact promotion artefact carries the workbook `Parallel Risk Lane Signal Inventory` into runtime config/contracts? | Use `config/parallel_risk_signal_inventory.v1.yaml` as the typed promotion artefact, validated by future `ParallelRiskSignalInventoryDocument` / `ParallelRiskExpectedSignalRecord` contracts. It must carry workbook path/sheet/range/hash lineage per record. | `resolved_with_senior_engineering_judgement` | Workbook promotion law requires workbook → typed config/contracts with lineage → runtime consumption only: `docs/reference/SIGNAL_WORKBOOK_AUTHORITY.md:26-35`. Coefficient authority already demonstrates YAML config with workbook refs: `config/coefficient_authority.v1.yaml:1-37`. | Code constant inventory; runtime workbook reader; Markdown table as authority. | Code constants and Markdown lack workbook-governed lineage; runtime workbook reader violates authority. | Update workbook leaves to create tab first, then promote to YAML+contract before runtime use. | Tests proving runtime uses YAML/contract only and does not read workbook. | PRL-MRP-004, PRL-MRP-006, PRL-MRP-007, PRL-MRP-008, PRL-MRP-009, PRL-MRP-020 |
| Should VIX coefficient-authority reconciliation preserve current hardcoded behaviour as compatibility mode? | Yes. Preserve current PRL VIX behaviour as compatibility mode first: VIX >= 30 caution and VIX >= 50 block. Reconcile with governed config only in an explicit later migration leaf with tests and no silent drift. | `resolved_from_repo` | Current PRL implements VIX >= 30 caution and >= 50 block: `src/nvda_desk/domain/parallel_risk/environment_assessment.py:48-107`. Coefficient authority contains different posture thresholds 24/32: `config/coefficient_authority.v1.yaml:8-37`. Testing law requires relevant touched proof to remain green: `docs/08_TESTING_AND_PROMOTION_CORE.md:41-48`. | Switch immediately to 24/32; ignore coefficient authority forever; blend thresholds silently. | Immediate switch silently changes behaviour; ignoring config blocks governance; blending is untestable drift. | PRL-MRP-012 preserves compatibility; PRL-MRP-013 plans explicit migration to governed PRL-specific config or named compatibility policy. | Regression tests for 30/50 behaviour; migration tests before any threshold change. | PRL-MRP-012, PRL-MRP-013, PRL-MRP-015, PRL-MRP-018 |
| Where should deterministic description templates live? | Use a dedicated deterministic template registry, planned as `data/parallel_risk/description_templates.v1.json`, validated by future contracts. Templates reference canonical vocabulary entries but do not live inside canonical vocabulary data. | `resolved_from_repo` | Vocabulary artefacts are authoritative for terms, and workflow is feeder-only; vocabulary is not a runtime redesign surface or free-form glossary: `docs/vocabulary/README.md:12-23`, `docs/vocabulary/CONSOLIDATION_WORKFLOW.md:3-22`. Durable terms require governance: `docs/10_VOCABULARY_AND_TERM_GOVERNANCE_CORE.md:6-34`. | Put templates inside canonical vocabulary JSON; put templates in threshold config; generate free-form prose in code. | Vocabulary data should not become runtime renderer; threshold config is the wrong semantic owner; free-form prose violates deterministic/controlled-language requirement. | PRL-MRP-023 formalises constraints; PRL-MRP-024 adds registry contract/tests; PRL-MRP-025 implements renderer only after tests. | Template registry schema tests, vocabulary-ref validation, forbidden trade-advice phrase tests, deterministic output tests. | PRL-MRP-023, PRL-MRP-024, PRL-MRP-025 |

## 6. ADR-001 freshness threshold ownership

Status: `accepted`

Decision:

Freshness age thresholds after deterministic defaults should be owned by a dedicated governed PRL profile config surface, initially named `config/parallel_risk_lane_profile.v1.yaml`, validated by a future typed contract. `PRL-MRP-003` should not create or read that config. It should implement deterministic default classification only and leave threshold-source references explicit/empty.

Evidence:

- Source temporal law distinguishes source observation time, capture time, and persistence time, and forbids substituting capture/persist time for source observation truth: `docs/04.1_TECHNICAL_ARCHITECTURE_WORKING.md:18-37`.
- PRL may consume configuration authority as a lawful input, but must avoid hidden upstream reads: `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:262-268`.
- Existing coefficient authority is workbook-derived coefficient/modifier authority with posture thresholds and surfaces, not general data-quality freshness policy: `config/coefficient_authority.v1.yaml:1-37`.

Consequences:

- PRL-MRP-003 remains small: no config file, no coefficient-authority wiring, no workbook read.
- Future threshold governance can be added without rewriting the freshness data model.
- `FreshnessRegisterEntry` can carry `max_allowed_age_seconds` and source refs now while leaving ownership explicit.

Rejected alternatives:

- Put freshness thresholds in `coefficient_authority.v1.yaml`: rejected because freshness is data-quality policy, not posture coefficient authority.
- Keep hidden constants forever: rejected because governed thresholds need traceable ownership.
- Read thresholds from workbook at runtime: rejected by workbook authority.

Required tests:

- Fresh/stale/unknown classification with deterministic defaults.
- Source/capture/persist distinction preserved.
- No config or workbook read in PRL-MRP-003.

Affected roadmap leaves:

- PRL-MRP-003
- PRL-MRP-021
- PRL-MRP-026

## 7. ADR-002 workbook signal-inventory promotion artefact

Status: `accepted`

Decision:

The exact runtime promotion artefact for the future workbook tab should be `config/parallel_risk_signal_inventory.v1.yaml`, validated by future contracts named `ParallelRiskSignalInventoryDocument` and `ParallelRiskExpectedSignalRecord` or equivalent. Each promoted signal record should carry workbook lineage: workbook path, sheet name `Parallel Risk Lane Signal Inventory`, row/range, source raw/derived workbook refs, classification, expected use, and promotion hash/version.

Evidence:

- Workbook content never becomes runtime truth by direct read; runtime consumption occurs only after typed promotion into config/contracts with lineage: `docs/reference/SIGNAL_WORKBOOK_AUTHORITY.md:26-35`.
- Workbook lane-relevant additions require paired updates to the reference doc and planning pack: `docs/reference/SIGNAL_WORKBOOK_AUTHORITY.md:41-51`.
- Existing coefficient authority demonstrates repo-native YAML config with workbook refs and typed loading: `config/coefficient_authority.v1.yaml:1-37`, `src/nvda_desk/config/coefficient_authority.py:31-58`.

Consequences:

- Workbook remains the governance/reference source of expected-signal inventory.
- Runtime PRL never reads Excel.
- Missing/unavailable checks can depend on typed records with lineage.

Rejected alternatives:

- Isolated code constant: rejected because it divorces expected signals from workbook lineage.
- Markdown table: rejected because it is not typed runtime promotion.
- Direct workbook runtime read: rejected by workbook authority.

Required tests:

- Runtime expected-signal inventory loader reads YAML/contract only.
- Workbook lineage refs are present.
- No Excel read during runtime PRL execution.

Affected roadmap leaves:

- PRL-MRP-004
- PRL-MRP-006
- PRL-MRP-007
- PRL-MRP-008
- PRL-MRP-009
- PRL-MRP-020

## 8. ADR-003 VIX threshold compatibility and reconciliation

Status: `accepted`

Decision:

Preserve the current PRL VIX hardcoded behaviour as compatibility mode before reconciliation. Current PRL envelope behaviour is VIX >= 30 caution and VIX >= 50 hard block. A later reconciliation leaf may migrate thresholds into governed PRL config or a named compatibility-policy adapter, but must do so explicitly with tests and release-note/ledger evidence.

Evidence:

- Current implemented envelope logic uses VIX >= 30 for caution and >= 50 for hard block: `src/nvda_desk/domain/parallel_risk/environment_assessment.py:48-107`.
- Coefficient authority contains different `risk_vix_caution_threshold` and `risk_vix_hot_threshold` baseline values 24 and 32 under posture ownership: `config/coefficient_authority.v1.yaml:8-37`.
- Testing/promotion law requires the Tier A proof that owns touched surfaces not be red or unreconciled: `docs/08_TESTING_AND_PROMOTION_CORE.md:41-48`.

Consequences:

- PRL-MRP-012 is preservation-only.
- PRL-MRP-013 becomes an explicit migration/reconciliation leaf.
- No silent behaviour drift occurs while atoms/profile assembly are added.

Rejected alternatives:

- Immediate 24/32 switch: rejected as silent behaviour change and owner-stage mismatch.
- Permanent hardcoded 30/50 without governance: rejected as non-governed drift over time.
- Blend thresholds: rejected as ambiguous and hard to test.

Required tests:

- Existing VIX caution/block regression at 30/50.
- Later migration tests showing old/new policy mode explicitly.

Affected roadmap leaves:

- PRL-MRP-012
- PRL-MRP-013
- PRL-MRP-015
- PRL-MRP-018

## 9. ADR-004 deterministic vocabulary-governed description template location

Status: `accepted`

Decision:

Deterministic PRL description templates should live in a dedicated template registry, planned as `data/parallel_risk/description_templates.v1.json`, with a future typed schema/contract. The registry should reference canonical vocabulary entries and template IDs. The canonical vocabulary file should remain vocabulary authority, not the runtime template store.

Evidence:

- Vocabulary README says the vocabulary folder is not a runtime redesign surface and not a free-form glossary; it points to workflow, canonical vocabulary, schema, and generator as authoritative artefacts: `docs/vocabulary/README.md:12-23`.
- The consolidation workflow is feeder-only and must classify candidate terms before admission: `docs/vocabulary/CONSOLIDATION_WORKFLOW.md:3-22`.
- Durable terms require governance before landing in docs/schemas/manifests/code: `docs/10_VOCABULARY_AND_TERM_GOVERNANCE_CORE.md:6-34`.

Consequences:

- The description engine is not opened until PRL-MRP-025.
- PRL-MRP-023 formalises vocabulary constraints first.
- PRL-MRP-024 creates metadata/contract tests for templates and vocabulary refs.
- Free-form generative text remains prohibited.

Rejected alternatives:

- Store templates inside `canonical_vocabulary.json`: rejected because vocabulary data is term authority, not runtime renderer.
- Store templates in threshold/config policy: rejected because description templates are controlled-language artefacts, not threshold policy.
- Generate prose directly in code: rejected because it bypasses vocabulary governance and deterministic testing.

Required tests:

- Template registry schema validation.
- References point to admitted vocabulary terms.
- Deterministic output for fixed inputs.
- No trade advice/playbook/capital/order/review wording.

Affected roadmap leaves:

- PRL-MRP-023
- PRL-MRP-024
- PRL-MRP-025

## 10. Implementation consequences

- `PRL-MRP-003` remains the next executable leaf and is restricted to deterministic freshness classification from existing temporal fields.
- Freshness threshold governance is deferred to a later PRL config leaf; do not touch coefficient authority in PRL-MRP-003.
- Expected-signal inventory runtime consumption is blocked until the workbook tab exists and is promoted into `config/parallel_risk_signal_inventory.v1.yaml` with contracts.
- VIX threshold reconciliation is not part of supported-risk-atom skeleton work; preservation comes first, migration later.
- Plain-English output remains metadata/template-reference-only until vocabulary constraints, template registry contract, and renderer tests are opened in sequence.

## 11. Tests required

- `PRL-MRP-003`: freshness deterministic defaults and source/capture/persist separation.
- `PRL-MRP-004` / `PRL-MRP-009`: no workbook runtime reads and typed inventory-only expected-signal consumption.
- `PRL-MRP-012`: current VIX 30/50 behaviour preservation.
- `PRL-MRP-013`: explicit compatibility-vs-governed threshold migration tests before any behaviour change.
- `PRL-MRP-023` to `PRL-MRP-025`: vocabulary refs, template registry validation, deterministic text, and forbidden advice wording.

## 12. Roadmap leaves affected

- `PRL-MRP-003`
- `PRL-MRP-004`
- `PRL-MRP-006`
- `PRL-MRP-007`
- `PRL-MRP-008`
- `PRL-MRP-009`
- `PRL-MRP-012`
- `PRL-MRP-013`
- `PRL-MRP-015`
- `PRL-MRP-018`
- `PRL-MRP-020`
- `PRL-MRP-021`
- `PRL-MRP-023`
- `PRL-MRP-024`
- `PRL-MRP-025`
- `PRL-MRP-026`

## 13. Unresolved items

The four prior roadmap questions are resolved by this document.

Remaining open questions that are not blockers for `PRL-MRP-003`:

1. Should event proximity intensity use continuous scores, discrete states, or both?
2. Which rich signal family should be sourced first after currently supported atoms are stable?
3. Which proof block eventually owns full PRL minute-profile verification?
