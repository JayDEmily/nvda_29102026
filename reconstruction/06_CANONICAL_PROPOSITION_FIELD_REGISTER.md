# Canonical proposition field register

## Status and use

This register is the mandatory semantic-field adjunct to the 83 proposition records under `reconstruction/propositions/`. Each entry incorporates its linked proposition record and decomposes the canonical instruction into the fields required by `AGENTS.md:L117-L136`. The proposition record remains the source-line evidence surface; this register does not create new authority or certify independent review. Where the admitted corpus does not specify a detail, the field says so rather than inventing it.

Current population: 80 active propositions, one partially superseded proposition and two unresolved propositions. Independent semantic review remains outstanding; see the tranche reviews and final assurance report.

## P-DAT-001 — Ingress substrate and truth fences

- **Proposition record:** `reconstruction/propositions/A01.md`
- **Canonical instruction:** The system must expose typed ingress contracts for event flags, spot data, peer-equity data, macro data and realised volatility. These may proxy only from deterministic runtime inputs. VWAP accumulation and VWAP rate-of-change must remain explicitly unavailable/fenced until raw tick-derived state exists. The ingress layer must not create named playbooks, broker behaviour or hidden side state.
- **Class and current authority state:** data contract; active.
- **Introduction and authority chain:** **Lineage:** introduced by `source_planning/2026-03-25_GATE28_INGRESS_SUBSTRATE_CONTRACTS.md:L8-L18`; truth boundaries at `:L22-L32`.
- **Historical aliases:** VWAP and VWAP-ROC labels are preserved only as fenced future surfaces until raw tick state exists.
- **Inputs and validity constraints:** Deterministic runtime event, spot, peer-equity, macro and realised-volatility inputs; raw tick-derived state for VWAP/ROC.
- **Transformation, calculation, decision or routing semantics:** Validate provenance, proxy only from admitted deterministic inputs, and fence unsupported accumulation/ROC.
- **Outputs and guarantees:** Typed ingress contracts with explicit provenance and proxy/unavailable status.
- **Time and state semantics:** Ingress reflects the current supplied observation; VWAP state exists only after lawful tick accumulation.
- **Null, boundary and failure behaviour:** Missing tick state keeps VWAP/ROC unavailable; no synthetic value or hidden side state.
- **Dependencies and downstream consequences:** Vendor/runtime input providers and downstream typed consumers.
- **Explicit exclusions and non-goals:** No playbook creation, scheduling, broker behaviour or concealed state.
- **Unresolved questions:** Exact raw-tick accumulation, retention and ROC-window policies are not specified.

## P-CTX-001 — Advisory market-context synthesis

- **Proposition record:** `reconstruction/propositions/A01.md`
- **Canonical instruction:** The market-context layer must provide macro score, peer divergence, volume-spike, macro-adaptive, Asia-precursor, engine-score and signal-scan surfaces with explicit upstream provenance. `run_signal_scan` is a typed advisory wrapper that preserves scan intent, configured desk-window scope and candidate-count summaries; it must not imply scheduling, broker triggering, named-playbook expansion or live-trading approval.
- **Class and current authority state:** derived context; active.
- **Introduction and authority chain:** **Lineage:** `source_planning/2026-03-25_GATE29_MARKET_CONTEXT_SYNTHESIS_CONTRACTS.md:L8-L18`, `:L22-L32`.
- **Historical aliases:** The `run_signal_scan` name is preserved as a typed advisory wrapper, not a scheduler.
- **Inputs and validity constraints:** Provenanced macro, peer, volume, Asia-precursor and engine-score inputs plus configured desk-window scope.
- **Transformation, calculation, decision or routing semantics:** Deterministically synthesise context scores and scan summaries without changing execution authority.
- **Outputs and guarantees:** Typed macro score, peer divergence, volume-spike, macro-adaptive, precursor, engine-score and candidate-count summaries.
- **Time and state semantics:** Window scope is configuration supplied to each scan; no autonomous clock or loop is implied.
- **Null, boundary and failure behaviour:** Unavailable upstream provenance must remain explicit rather than becoming an inferred score.
- **Dependencies and downstream consequences:** Macro-signal and engine-score producers; advisory consumers.
- **Explicit exclusions and non-goals:** No scheduling, broker trigger, playbook expansion or live approval.
- **Unresolved questions:** Formulae and thresholds for the listed context scores are not restated.

## P-OPT-001 — Options ingress and primary-flow honesty

- **Proposition record:** `reconstruction/propositions/A01.md`
- **Canonical instruction:** The system must represent options data, metadata, gamma pressure, IV-versus-realised-volatility, skew inflection, volatility corridor and VIX-spread context as typed surfaces. Quote-chain, metadata and realised-volatility dependencies must remain explicit; proxying is permitted only where deterministic source surfaces exist. This layer has no execution, broker or approval authority.
- **Class and current authority state:** options data/derived context; active.
- **Introduction and authority chain:** **Lineage:** `source_planning/2026-03-25_GATE30_OPTIONS_INGRESS_PRIMARY_FLOW_CONTRACTS.md:L8-L18`, `:L22-L33`.
- **Historical aliases:** No historical aliases are stated.
- **Inputs and validity constraints:** Quote-chain, option metadata and realised-volatility inputs with deterministic provenance.
- **Transformation, calculation, decision or routing semantics:** Project typed option observations into gamma, IV/RV, skew, corridor and VIX-spread context; proxy only where supported.
- **Outputs and guarantees:** Typed options-data and options-context surfaces with explicit dependency provenance.
- **Time and state semantics:** Observation timing follows the supplied option and volatility inputs; no separate state rule is stated.
- **Null, boundary and failure behaviour:** Absent dependencies must remain absent/fenced; unsupported values may not be fabricated.
- **Dependencies and downstream consequences:** Options quote/metadata ingress and realised-volatility authority.
- **Explicit exclusions and non-goals:** No execution, broker or approval authority.
- **Unresolved questions:** Exact derivation formulae and validity ranges are not stated.

## P-CTX-002 — Higher-order composites remain descriptive

- **Proposition record:** `reconstruction/propositions/A01.md`
- **Canonical instruction:** Options-behaviour clustering, execution-context scoring, compression-regime detection and OBV/VI flow confirmation are higher-order descriptive composites. OBV/VI confirmation must fail/fence explicitly when OBV tape dependencies are absent. None is an approval or execution trigger, and this layer must not widen into downstream archetype, ladder or named-playbook authority.
- **Class and current authority state:** derived context; active.
- **Introduction and authority chain:** **Lineage:** `source_planning/2026-03-25_GATE31_HIGHER_ORDER_CONTEXT_COMPOSITES.md:L7-L23`.
- **Historical aliases:** OBV/VI confirmation retains its named composite identity.
- **Inputs and validity constraints:** Options behaviour, execution context, compression signals and OBV tape where available.
- **Transformation, calculation, decision or routing semantics:** Compute descriptive clustering, scoring, regime detection and flow confirmation.
- **Outputs and guarantees:** Higher-order descriptive context only.
- **Time and state semantics:** Per supplied observation/window; no persistent decision state is admitted.
- **Null, boundary and failure behaviour:** OBV/VI must explicitly fail or fence when OBV tape is absent.
- **Dependencies and downstream consequences:** P-OPT-001 and upstream market/flow features.
- **Explicit exclusions and non-goals:** No approval trigger; no archetype, ladder or named-playbook ownership.
- **Unresolved questions:** Composite formulae and thresholds are not stated.

## P-PLAY-001 — Archetype and entry-gate advisory boundary

- **Proposition record:** `reconstruction/propositions/A02.md`
- **Canonical instruction:** Archetype matching/tagging and the entry gate operate only on existing runtime candidates. The entry gate is advisory and may veto under permission or event-window stress; it must not invent playbooks or imply execution approval.
- **Class and current authority state:** playbook eligibility; active.
- **Introduction and authority chain:** **Lineage:** `source_planning/2026-03-25_GATE32_ARCHETYPE_ENTRY_GATE_BRIDGE_CONTRACTS.md:L7-L22`.
- **Historical aliases:** Archetype tags and entry-gate labels are preserved.
- **Inputs and validity constraints:** Existing runtime candidates, permission state and event-window stress.
- **Transformation, calculation, decision or routing semantics:** Match/tag existing candidates and apply an advisory veto gate.
- **Outputs and guarantees:** Archetype annotations and an advisory admit/veto result.
- **Time and state semantics:** Acts on the current candidate set and current event/permission state.
- **Null, boundary and failure behaviour:** No candidate means nothing to invent; stressed or disallowed state may veto.
- **Dependencies and downstream consequences:** Candidate-generation, permission and temporal-state owners.
- **Explicit exclusions and non-goals:** No playbook invention and no execution approval.
- **Unresolved questions:** Matching scores and veto thresholds are not stated.

## P-EXE-001 — Ladder readiness is preview-only

- **Proposition record:** `reconstruction/propositions/A02.md`
- **Canonical instruction:** Ladder construction, fill-bias adjustment, VVIX shaping and volatility-sentiment context form an advisory readiness layer. VVIX may reshape only the current preview ladder, not broker orders; volatility sentiment remains posture-facing rather than execution approval.
- **Class and current authority state:** execution preparation; active.
- **Introduction and authority chain:** **Lineage:** `source_planning/2026-03-25_GATE33_LADDER_EXECUTION_READINESS_CONTRACTS.md:L7-L23`.
- **Historical aliases:** Preview ladder, fill-bias, VVIX shaping and volatility-sentiment names are preserved.
- **Inputs and validity constraints:** Current preview ladder, fill context, VVIX and volatility sentiment.
- **Transformation, calculation, decision or routing semantics:** Construct and reshape advisory execution readiness geometry.
- **Outputs and guarantees:** A preview-only ladder/readiness result and posture-facing sentiment context.
- **Time and state semantics:** Changes apply only to the current preview, not durable broker state.
- **Null, boundary and failure behaviour:** Missing inputs must not be converted into broker orders or approval.
- **Dependencies and downstream consequences:** Execution-template/context inputs and posture consumers.
- **Explicit exclusions and non-goals:** No live order mutation or execution approval.
- **Unresolved questions:** Geometry formulae and input-validity ranges are not stated.

## P-DEC-001 — Confidence and conviction do not grant capital authority

- **Proposition record:** `reconstruction/propositions/A02.md`
- **Canonical instruction:** Signal-conflict detection, confidence scoring and conviction-tier allocation are bounded advisory scoring surfaces. They must not claim hidden certainty, broker approval or capital deployment authority.
- **Class and current authority state:** posture/permission; active.
- **Introduction and authority chain:** **Lineage:** `source_planning/2026-03-25_GATE34_POSTURE_PERMISSION_CORE_CONTRACTS.md:L7-L21`.
- **Historical aliases:** Confidence score and conviction tier remain advisory labels.
- **Inputs and validity constraints:** Signals and detected conflicts.
- **Transformation, calculation, decision or routing semantics:** Compute bounded confidence and conviction classifications.
- **Outputs and guarantees:** Advisory conflict, confidence and conviction outputs.
- **Time and state semantics:** Current-evaluation state only; no durable capital state.
- **Null, boundary and failure behaviour:** Uncertainty must not be hidden or converted into certainty.
- **Dependencies and downstream consequences:** Signal/context producers and downstream posture consumers.
- **Explicit exclusions and non-goals:** No broker approval or capital-deployment authority.
- **Unresolved questions:** Scoring formulae and tier thresholds are not stated.

## P-EXE-002 — Execution orchestration remains deterministic dry-run

- **Proposition record:** `reconstruction/propositions/A02.md`
- **Canonical instruction:** Entry planning, position allocation, order simulation, broker adaptation, bot orchestration and execution tags may form a deterministic dry-run chain. The broker adapter must remain fenced from credentials, live acknowledgements and live bridge claims; bot orchestration must not imply a daemon, scheduler or live loop; execution tags are preview explainability only.
- **Class and current authority state:** execution orchestration; active.
- **Introduction and authority chain:** **Lineage:** `source_planning/2026-03-25_GATE35_EXECUTION_ORCHESTRATION_CORE_CONTRACTS.md:L7-L25`.
- **Historical aliases:** Broker adapter, bot orchestration and execution tags survive only with dry-run meaning.
- **Inputs and validity constraints:** Entry plan, allocation policy, simulated order inputs and deterministic adapter inputs.
- **Transformation, calculation, decision or routing semantics:** Compose a deterministic dry-run chain and emit explainability tags.
- **Outputs and guarantees:** Preview plans, simulated orders, adapter output and execution tags.
- **Time and state semantics:** No daemon, scheduler or live loop; outputs are simulation-time state.
- **Null, boundary and failure behaviour:** Credentials, live acknowledgements and live bridge behaviour remain fenced/unavailable.
- **Dependencies and downstream consequences:** P-EXE-001 and bounded allocation/template authorities.
- **Explicit exclusions and non-goals:** No live placement, network execution or autonomous loop.
- **Unresolved questions:** Simulation fill model and adapter protocol details are not stated.

## P-STATE-001 — Preview state is not booked truth

- **Proposition record:** `reconstruction/propositions/A03.md`
- **Canonical instruction:** Execution logs, position books, trade logs and unrealised tracking are preview/advisory state only. Missing-surface markers must remain explicit, and no surface may be treated as live broker inventory, booked ledger or settlement truth.
- **Class and current authority state:** execution state; active.
- **Introduction and authority chain:** **Lineage:** `source_planning/2026-03-25_GATE36_EXECUTION_STATE_LEDGER_SPINE_CONTRACTS.md:L7-L24`.
- **Historical aliases:** Execution log, position book, trade log and unrealised tracking names retain preview-only meaning.
- **Inputs and validity constraints:** Preview execution events and any explicitly available simulated state.
- **Transformation, calculation, decision or routing semantics:** Record and aggregate advisory state while preserving missing-surface markers.
- **Outputs and guarantees:** Preview logs/books/tracking outputs, explicitly not booked truth.
- **Time and state semantics:** State is local preview continuity, not settlement or broker inventory.
- **Null, boundary and failure behaviour:** Missing surfaces stay marked missing; no booked values are inferred.
- **Dependencies and downstream consequences:** Dry-run execution and lifecycle outputs.
- **Explicit exclusions and non-goals:** No live broker inventory, ledger, settlement or booked P&L.
- **Unresolved questions:** Retention, transaction and reconciliation policies are not stated.

## P-EXE-003 — Exit, re-entry and fill feedback remain advisory

- **Proposition record:** `reconstruction/propositions/A03.md`
- **Canonical instruction:** Partial exits, take-profit, trailing-stop, re-entry markers, fill-feedback routing and ladder continuity are preview-only. They must not imply broker-side state or live ladder management; continuity may be represented by deterministic preview identity/hash.
- **Class and current authority state:** lifecycle; active.
- **Introduction and authority chain:** **Lineage:** `source_planning/2026-03-25_GATE37_EXIT_REENTRY_CONTINUITY_CONTRACTS.md:L7-L26`.
- **Historical aliases:** Partial exit, take-profit, trailing stop, re-entry, fill feedback and ladder continuity retain preview semantics.
- **Inputs and validity constraints:** Preview position/lifecycle state, simulated fills and ladder identity.
- **Transformation, calculation, decision or routing semantics:** Apply advisory lifecycle transitions and route preview feedback.
- **Outputs and guarantees:** Preview exit/re-entry markers, feedback and deterministic continuity identity/hash.
- **Time and state semantics:** Transitions occur only within preview state; continuity may use deterministic identity.
- **Null, boundary and failure behaviour:** No broker-side state may be inferred; missing live fills remain absent.
- **Dependencies and downstream consequences:** P-STATE-001 and dry-run execution outputs.
- **Explicit exclusions and non-goals:** No live ladder management or broker-side lifecycle control.
- **Unresolved questions:** Exit thresholds and re-entry rules are not stated.

## P-REV-001 — Review ledger and attribution are descriptive

- **Proposition record:** `reconstruction/propositions/A03.md`
- **Canonical instruction:** P&L, module trace attribution, module scoring and daily summaries are descriptive preview outputs. They must not claim booked broker P&L, settlement, or decision authority.
- **Class and current authority state:** review/attribution; active.
- **Introduction and authority chain:** **Lineage:** `source_planning/2026-03-25_GATE38_REVIEW_LEDGER_ATTRIBUTION_SPINE_CONTRACTS.md:L7-L24`.
- **Historical aliases:** P&L and module scoring labels retain descriptive-preview meaning.
- **Inputs and validity constraints:** Preview execution, attribution and trace data.
- **Transformation, calculation, decision or routing semantics:** Aggregate descriptive P&L, attribution, scoring and daily summaries.
- **Outputs and guarantees:** Operator-facing review ledger and summaries.
- **Time and state semantics:** Review is retrospective over preview records; no booked state is created.
- **Null, boundary and failure behaviour:** Missing evidence must remain explicit; no settlement or booked P&L inference.
- **Dependencies and downstream consequences:** Preview state, trace and module-output provenance.
- **Explicit exclusions and non-goals:** No settlement or decision authority.
- **Unresolved questions:** Attribution/scoring formulae and summary horizons are not stated.

## P-REV-002 — Feedback and hedge overlays cannot self-actuate

- **Proposition record:** `reconstruction/propositions/A03.md`
- **Canonical instruction:** Variant tracing/performance, feedback summaries, macro alignment and confidence-divergence logging are operator-facing diagnostics, not self-optimising loops. A tail-hedge injector may emit only an advisory hedge candidate and must not imply placement, booked protection or auto-routing.
- **Class and current authority state:** review/diagnostics; active.
- **Introduction and authority chain:** **Lineage:** `source_planning/2026-03-25_GATE39_REVIEW_OVERLAYS_FEEDBACK_CHAIN_CONTRACTS.md:L7-L26`.
- **Historical aliases:** Variant performance, feedback, macro alignment, divergence and tail-hedge candidate labels are preserved.
- **Inputs and validity constraints:** Review traces, variant outcomes, macro alignment, confidence divergence and hedge context.
- **Transformation, calculation, decision or routing semantics:** Produce diagnostic summaries and optionally an advisory hedge candidate.
- **Outputs and guarantees:** Operator-facing diagnostics and a non-actuating hedge candidate.
- **Time and state semantics:** Feedback remains review-time evidence and cannot become an automatic learning loop.
- **Null, boundary and failure behaviour:** Missing evidence cannot trigger self-optimisation or placement.
- **Dependencies and downstream consequences:** P-REV-001 plus market/posture context.
- **Explicit exclusions and non-goals:** No self-actuation, auto-routing, booked protection or placement.
- **Unresolved questions:** Hedge-candidate formulae and feedback retention rules are not stated.

## P-TMP-001 — Signal-aware temporal state is Step-1 truth

- **Proposition record:** `reconstruction/propositions/A04.md`
- **Canonical instruction:** Step 1 must use a signal-aware temporal-state classifier based on primitive temporal observables rather than elapsed-minute buckets. Temporal orchestration and the outward `TemporalContextOutput` remain stable, including DMP consumers; event-window labels must be consistent.
- **Class and current authority state:** temporal classification; active.
- **Introduction and authority chain:** **Lineage:** `source_planning/2026-03-25_GATE40_TEMPORAL_STATE_REPLACEMENT.md:L5-L15`, `:L32-L34`.<br>**Supersession:** replaces hard clock-bucket classification as truth, while preserving the outward payload contract.
- **Historical aliases:** `session_clock`/elapsed-minute bucket truth is superseded; `TemporalContextOutput` remains the outward compatibility contract.
- **Inputs and validity constraints:** Primitive temporal observables and event-window facts.
- **Transformation, calculation, decision or routing semantics:** Classify signal-aware temporal state instead of selecting elapsed-minute buckets.
- **Outputs and guarantees:** Stable `TemporalContextOutput` with consistent temporal and event-window labels.
- **Time and state semantics:** Step 1 owns current temporal-state truth; orchestration and consumers retain the outward shape.
- **Null, boundary and failure behaviour:** Insufficient primitives must not be replaced by hard clock-bucket certainty.
- **Dependencies and downstream consequences:** Calendar/event inputs and DMP/serial downstream consumers.
- **Explicit exclusions and non-goals:** No return to elapsed-minute truth and no silent payload break.
- **Unresolved questions:** The complete classifier formula and state thresholds are not stated.

## P-DAT-002 — Raw capture and derived features are separate authority layers

- **Proposition record:** `reconstruction/propositions/A04.md`
- **Canonical instruction:** Direct vendor/feed observations belong only in raw capture. VWAP, realised volatility, skew, term structure, pin, gamma and participation ratios are derived features. The mixed legacy catalogue is continuity-only and non-authoritative. Playbooks must consume deterministic derived services rather than reproduce ad hoc chain mathematics.
- **Class and current authority state:** data doctrine; active.
- **Introduction and authority chain:** **Lineage:** `source_planning/2026-03-25_GATE41_RAW_DERIVED_SIGNAL_WORKBOOK.md:L5-L20`, `:L26-L28`.
- **Historical aliases:** The mixed legacy catalogue survives only as non-authoritative continuity evidence.
- **Inputs and validity constraints:** Direct vendor/feed observations and deterministic feature-service inputs.
- **Transformation, calculation, decision or routing semantics:** Separate raw observations from derived VWAP, RV, skew, term, pin, gamma and participation calculations.
- **Outputs and guarantees:** Raw capture records and separately governed derived-feature outputs.
- **Time and state semantics:** Raw precedes derivation; no derived value is admitted as direct capture.
- **Null, boundary and failure behaviour:** Unavailable source truth remains absent; playbooks may not recreate ad hoc mathematics.
- **Dependencies and downstream consequences:** Raw ingress, feature services and playbook consumers.
- **Explicit exclusions and non-goals:** No mixed raw/derived authority and no workbook-as-runtime shortcut.
- **Unresolved questions:** Specific derivation formulae are governed elsewhere or unresolved here.

## P-DAT-003 — Dense/coarse options capture and volume baselines

- **Proposition record:** `reconstruction/propositions/A04.md`
- **Canonical instruction:** Capture same-bucket historical volume, trade-count and spread baselines. During regular trading hours capture the front two expiries densely every 30 seconds over a near-spot strike band; capture farther tenors more coarsely for curve context only. Raw option rows target expiry, DTE, strike, side, bid, ask, last, IV, delta, gamma, open interest and volume where vendor supplied.
- **Class and current authority state:** raw capture policy; active.
- **Introduction and authority chain:** **Lineage:** `source_planning/2026-03-25_GATE42_VOLUME_BASELINE_AND_OPTIONS_RAW_CAPTURE.md:L5-L21`.
- **Historical aliases:** No historical aliases are stated.
- **Inputs and validity constraints:** Regular-trading-hours option quotes and historical same-bucket baseline observations.
- **Transformation, calculation, decision or routing semantics:** Capture front expiries densely every 30 seconds near spot and farther tenors coarsely; retain vendor-supplied row fields.
- **Outputs and guarantees:** Raw option rows plus volume, trade-count and spread baselines.
- **Time and state semantics:** Dense cadence applies during regular hours; farther tenor capture is curve-context only.
- **Null, boundary and failure behaviour:** Vendor-absent fields remain absent; coarse tenors may not claim dense coverage.
- **Dependencies and downstream consequences:** Option vendor feed, session calendar and raw storage.
- **Explicit exclusions and non-goals:** No derived-feature or decision authority in raw rows.
- **Unresolved questions:** Near-spot band width, farther-tenor cadence and retention are not stated.

## P-PLAY-002 — Deterministic options-first playbooks

- **Proposition record:** `reconstruction/propositions/A04.md`
- **Canonical instruction:** Add `front_expiry_pin_pressure`, `term_structure_dislocation` and `skew_pressure_reversal` as deterministic options-led playbooks. They qualify only in focused options states and must not displace existing baseline playbooks in their established cases. They may not read ad hoc broker UI fields, rename DMP payload identity or silently redefine legacy playbooks.
- **Class and current authority state:** playbook catalogue; active.
- **Introduction and authority chain:** **Lineage:** `source_planning/2026-03-25_GATE43_OPTIONS_FIRST_PLAYBOOK_EXPANSION.md:L5-L20`, `:L22-L30`.
- **Historical aliases:** The three named playbooks are canonical names; baseline playbook identities remain intact.
- **Inputs and validity constraints:** Deterministic derived options states and existing baseline playbook context.
- **Transformation, calculation, decision or routing semantics:** Qualify `front_expiry_pin_pressure`, `term_structure_dislocation` and `skew_pressure_reversal` only in focused states.
- **Outputs and guarantees:** Eligible options-led playbook candidates with preserved DMP identity.
- **Time and state semantics:** Qualification uses current focused options state; no persistence rule is stated.
- **Null, boundary and failure behaviour:** Unsupported/ad hoc broker UI fields cannot qualify a playbook.
- **Dependencies and downstream consequences:** P-DAT-002/P-DAT-003 derived services, registry and DMP carriage.
- **Explicit exclusions and non-goals:** No displacement or silent redefinition of baseline playbooks.
- **Unresolved questions:** Exact qualification thresholds are not stated.

## P-PROTO-001 — Stable typed DMP stage wrapper

- **Proposition record:** `reconstruction/propositions/A05.md`
- **Canonical instruction:** Widened temporal and playbook inputs must remain inside a stable typed DMP stage wrapper around `TemporalContextOutput`. Posture, execution and review consume typed stage outputs, not raw broker data; stage payload identity must not be silently renamed.
- **Class and current authority state:** protocol; active until later DMP-version changes.
- **Introduction and authority chain:** **Lineage:** `source_planning/2026-03-25_GATE44_DMP_COMPATIBILITY_AND_PLAYBOOK_AUDIT.md:L5-L14`.
- **Historical aliases:** `TemporalContextOutput` and existing stage payload identity are preserved within the wrapper.
- **Inputs and validity constraints:** Typed widened temporal/playbook inputs and stable temporal output.
- **Transformation, calculation, decision or routing semantics:** Wrap stage data in a stable typed DMP stage carrier.
- **Outputs and guarantees:** Typed stage outputs consumed by posture, execution and review.
- **Time and state semantics:** Active until expressly replaced at a later protocol boundary.
- **Null, boundary and failure behaviour:** Raw broker data or renamed identities are invalid at this seam.
- **Dependencies and downstream consequences:** P-TMP-001, playbook outputs and downstream stage consumers.
- **Explicit exclusions and non-goals:** No raw-broker bypass and no silent payload rename.
- **Unresolved questions:** Full wrapper schema is not restated.

## P-PLAY-003 — Registry hierarchy with explicit compatibility

- **Proposition record:** `reconstruction/propositions/A05.md`
- **Canonical instruction:** The playbook registry must represent `family`, `setup_variant`, `execution_expression`, `horizon`, `priority`, `constraints` and `risk_overrides`, preserve deterministic runtime order, and provide an explicit bridge from the flat registry. Overlays and execution templates do not automatically become top-level families. The design must not enumerate every hypothetical play, collapse posture/risk into playbooks or create an LLM ontology.
- **Class and current authority state:** playbook registry; active.
- **Introduction and authority chain:** **Lineage:** `source_planning/2026-03-25_GATE47_PLAYBOOK_REGISTRY_V2.md:L5-L19`, `:L25-L33`.
- **Historical aliases:** The former flat registry remains only through an explicit compatibility bridge.
- **Inputs and validity constraints:** Governed family, setup variant, expression, horizon, priority, constraints and risk overrides.
- **Transformation, calculation, decision or routing semantics:** Build a deterministic hierarchical registry and bridge legacy flat entries explicitly.
- **Outputs and guarantees:** Ordered hierarchical registry entries with compatibility projection.
- **Time and state semantics:** Registry order is deterministic; compatibility persists only as governed bridge state.
- **Null, boundary and failure behaviour:** Undefined aliases, ambiguous hierarchy or incompatible entries must not be silently accepted.
- **Dependencies and downstream consequences:** P-GOV-001 vocabulary and runtime candidate/selection consumers.
- **Explicit exclusions and non-goals:** No exhaustive hypothetical ontology; overlays/templates do not automatically become families.
- **Unresolved questions:** Retirement timing for the flat bridge is not stated.

## P-CARRY-001 — Carry is a separate typed horizon branch

- **Proposition record:** `reconstruction/propositions/A05.md`
- **Canonical instruction:** Intraday close state must hand off through a typed packet to separate `overnight`, `weekend` and `event_carry` branches, including Friday-close and pre-event cases. Allowed actions are `flatten`, `hold_small`, `hold_baseline`, `add_carry` and `block_carry`, each subject to explicit legal conditions. Carry must not be disguised as intraday eligibility, fake booked-position state or silently alter mandatory-flatten policy.
- **Class and current authority state:** carry decisioning; active.
- **Introduction and authority chain:** **Lineage:** `source_planning/2026-03-25_GATE48_CARRY_HORIZON_HANDOFF.md:L5-L19`, `:L25-L33`.
- **Historical aliases:** Carry action names `flatten`, `hold_small`, `hold_baseline`, `add_carry`, `block_carry` are canonical.
- **Inputs and validity constraints:** Typed intraday close state, horizon/calendar context and explicit legal conditions.
- **Transformation, calculation, decision or routing semantics:** Route to separate overnight, weekend or event-carry branch and select a lawful action.
- **Outputs and guarantees:** Typed carry decision with explicit branch and action.
- **Time and state semantics:** Operates at intraday close, including Friday and pre-event cases.
- **Null, boundary and failure behaviour:** Absent legal conditions cannot authorise carry; mandatory flatten remains binding.
- **Dependencies and downstream consequences:** Step-0 calendar/horizon routing, inventory context and downstream carry handling.
- **Explicit exclusions and non-goals:** No disguise as intraday eligibility and no fake booked-position state.
- **Unresolved questions:** Complete legal-condition and override matrix is not stated.

## P-TMP-002 — Canonical outward temporal naming with bounded wrapper

- **Proposition record:** `reconstruction/propositions/A05.md`
- **Canonical instruction:** Canonical outward Step-1 surfaces use `temporal_state`; `session_clock` may survive only as an explicit compatibility wrapper. The migration must avoid hidden DMP renames, silent API breakage and any return to elapsed-minute bucket truth.
- **Class and current authority state:** terminology/compatibility; active.
- **Introduction and authority chain:** **Lineage:** `source_planning/2026-03-25_GATE49_TEMPORAL_COMPATIBILITY_SURFACE_DECISION.md:L5-L18`, `:L24-L36`.
- **Historical aliases:** `session_clock` is a bounded compatibility alias; `temporal_state` is canonical outward naming.
- **Inputs and validity constraints:** Step-1 temporal output and compatibility consumers.
- **Transformation, calculation, decision or routing semantics:** Project canonical `temporal_state` while delegating any retained wrapper explicitly.
- **Outputs and guarantees:** Stable outward temporal naming without changing DMP identity.
- **Time and state semantics:** Compatibility survives only as an explicit wrapper; elapsed-minute truth remains retired.
- **Null, boundary and failure behaviour:** Silent API/DMP rename or hidden alias behaviour is invalid.
- **Dependencies and downstream consequences:** P-TMP-001, P-PROTO-001 and external consumers.
- **Explicit exclusions and non-goals:** No dual truth or return to clock buckets.
- **Unresolved questions:** Wrapper retirement date is not stated.

## P-GOV-001 — Canonical vocabulary is contract-linked governance

- **Proposition record:** `reconstruction/propositions/A06.md`
- **Canonical instruction:** Canonical vocabulary must be regenerated from current governed surfaces, not blindly imported from a stale snapshot. It must govern aliases and duplicate labels and include family, setup variant, execution expression, horizon, raw/derived status, stage owner and contract linkage. Enforcement must reject conflicting duplicate labels, undefined aliases and runtime surfaces lacking canonical entries. Vocabulary must not become a free-form glossary or redesign the runtime.
- **Class and current authority state:** vocabulary governance; active.
- **Introduction and authority chain:** **Lineage:** `source_planning/2026-03-25_GATE50_VOCABULARY_GOVERNANCE_REBASE.md:L5-L19`, `:L25-L33`.
- **Historical aliases:** Historical vocabulary snapshots and duplicate labels are evidence, not authority.
- **Inputs and validity constraints:** Current governed runtime surfaces, aliases, contracts and ownership metadata.
- **Transformation, calculation, decision or routing semantics:** Regenerate deterministically, validate aliases/duplicates and require contract-linked entries.
- **Outputs and guarantees:** Canonical vocabulary covering family, variant, expression, horizon, raw/derived status, owner and contract linkage.
- **Time and state semantics:** Regeneration reflects current admitted surfaces; version lifecycle is not otherwise specified.
- **Null, boundary and failure behaviour:** Reject conflicts, undefined aliases and unregistered runtime labels.
- **Dependencies and downstream consequences:** Runtime contracts, registry builders and governance validation.
- **Explicit exclusions and non-goals:** No free-form glossary and no runtime redesign by vocabulary.
- **Unresolved questions:** Versioning and change-approval mechanics are not fully stated.

## P-ARCH-001 — Cognitive stage and boundary ownership must be explicit

- **Proposition record:** `reconstruction/propositions/A06.md`
- **Canonical instruction:** The cognitive workflow must explicitly assign stage ownership, candidate-generation boundaries, execution-expression ownership, carry-branch boundaries and Step-0 calendar/horizon routing semantics so downstream stages cannot claim ambiguous authority.
- **Class and current authority state:** workflow ownership; active.
- **Introduction and authority chain:** **Lineage:** `source_planning/2026-03-26_GATE51_COGNITIVE_WORKFLOW_IMPLEMENTATION_MAP.md:L5-L13`, `:L25-L34`.
- **Historical aliases:** Step-0 and stage ownership terms are preserved as architectural boundaries.
- **Inputs and validity constraints:** Calendar/horizon routing, candidates, expressions, carry and stage outputs.
- **Transformation, calculation, decision or routing semantics:** Assign each decision and handoff to an explicit stage owner and boundary.
- **Outputs and guarantees:** An inspectable cognitive workflow with unambiguous ownership.
- **Time and state semantics:** Stage order and routing state remain explicit across the run.
- **Null, boundary and failure behaviour:** Ambiguous or duplicated authority is invalid and must remain unresolved rather than inferred.
- **Dependencies and downstream consequences:** P-GOV-001/002 vocabulary, protocols and all downstream stages.
- **Explicit exclusions and non-goals:** No downstream stage may absorb upstream policy by convenience.
- **Unresolved questions:** Complete package/module allocation is not fixed by this proposition.

## P-PLAY-004 — Native family → variant → expression runtime model

- **Proposition record:** `reconstruction/propositions/A06.md`
- **Canonical instruction:** `family -> setup_variant -> execution_expression` must be a native runtime model. Family and variant candidates are emitted natively; execution and review preserve their lineage. The former flat list survives only as an explicit tested compatibility bridge.
- **Class and current authority state:** playbook hierarchy; active.
- **Introduction and authority chain:** **Lineage:** `source_planning/2026-03-26_GATE52_NATIVE_PLAYBOOK_HIERARCHY_IMPLEMENTATION.md:L5-L13`, `:L24-L36`.
- **Historical aliases:** The flat playbook list survives only as an explicit tested compatibility bridge.
- **Inputs and validity constraints:** Family, setup-variant and execution-expression definitions plus candidate context.
- **Transformation, calculation, decision or routing semantics:** Emit family and variant candidates natively and preserve lineage through execution/review.
- **Outputs and guarantees:** Hierarchical candidates and selected expression lineage.
- **Time and state semantics:** Deterministic runtime order; compatibility bridge is transitional.
- **Null, boundary and failure behaviour:** Missing hierarchy may not be hidden by flat labels.
- **Dependencies and downstream consequences:** P-PLAY-003 registry, execution and review.
- **Explicit exclusions and non-goals:** No collapse of family/variant/expression ownership.
- **Unresolved questions:** Flat-bridge retirement point is not stated.

## P-CARRY-002 — Carry handoff includes inventory, lineage and action ceilings

- **Proposition record:** `reconstruction/propositions/A06.md`
- **Canonical instruction:** The close-state/carry packet must include held-position or inventory context and family/setup/playbook lineage. Weekend, ordinary overnight and event carry remain explicit branches with deterministic allowed-action ceilings, downgrade and override rules that are explanation-safe.
- **Class and current authority state:** carry decisioning; active; clarifies P-CARRY-001.
- **Introduction and authority chain:** **Lineage:** `source_planning/2026-03-26_GATE53_CARRY_WEEKEND_EVENT_FORMALISATION.md:L5-L13`, `:L23-L35`.
- **Historical aliases:** Existing carry branches/actions from P-CARRY-001 remain canonical.
- **Inputs and validity constraints:** Close state, held inventory/positions, family/setup/playbook lineage and horizon context.
- **Transformation, calculation, decision or routing semantics:** Apply branch-specific ceilings, downgrade and override rules.
- **Outputs and guarantees:** Explanation-safe carry packet with inventory, lineage and bounded action.
- **Time and state semantics:** Separate ordinary overnight, weekend and event-carry states.
- **Null, boundary and failure behaviour:** Missing inventory or illegal conditions cannot be replaced with fake position truth.
- **Dependencies and downstream consequences:** P-CARRY-001, calendar routing, inventory and review.
- **Explicit exclusions and non-goals:** No silent widening of action ceilings or flatten obligations.
- **Unresolved questions:** Detailed ceiling values and override precedence are not stated.

## P-PROTO-002 — DMP v2 replaces v1 as the sole live packet protocol

- **Proposition record:** `reconstruction/propositions/A07.md`
- **Canonical instruction:** Live runtime packet production uses DMP v2 except at the expressly admitted serial-runtime downstream boundary where P-PROTO-003 promotes DMPV3. DMP v1 remains archived historical context only and is never a producer dependency.
- **Class and current authority state:** protocol version authority; `partially_superseded` at the named DMPV3 boundary.
- **Introduction and authority chain:** **Authority chain:** 1. Gate 54 temporarily fixed DMP v1 as the live producer for the workflow-modification tranche and v2 as a secondary migration/inspection surface: `source_planning/2026-03-26_GATE54_DMP_BINDING_SURFACE_DECISION.md:L5-L12`.<br>  2. The same source records that this freeze was tranche-bounded and later Gates 56–58 promoted v2: `:L20-L27`.<br>  3. Gate 57 explicitly promotes DMP v2 across runtime and imported-module emissions and ends v1 canonical-producer status: `source_planning/2026-03-26_GATE57_DMP_V2_CANONICAL_PROMOTION.md:L1-L5`.<br>  4. Gate 58 removes mixed mode: v1 is archived historical context only and v2 is the sole live protocol: `source_planning/2026-03-26_GATE58_DMP_V1_RETIREMENT.md:L1-L5`.<br>**Supersession:** the Gate-54 v1-live proposition is explicitly superseded by Gates 57–58; its unaffected historical explanation survives.
- **Historical aliases:** DMP v1 becomes archived historical context; DMP v2 is the sole live producer protocol until later bounded replacement.
- **Inputs and validity constraints:** Live runtime stage outputs requiring packet production.
- **Transformation, calculation, decision or routing semantics:** Emit through DMP v2 and reject v1 as a live producer dependency.
- **Outputs and guarantees:** One live DMP v2 packet protocol plus archived v1 evidence.
- **Time and state semantics:** Gate 54 temporary mixed authority is superseded by Gates 57–58; later P-PROTO-003 replaces v2 only at its named boundary.
- **Null, boundary and failure behaviour:** Mixed v1/v2 live production is invalid.
- **Dependencies and downstream consequences:** P-PROTO-001, stage producers and packet consumers.
- **Explicit exclusions and non-goals:** No live DMP v1 production.
- **Unresolved questions:** Unaffected DMP v2 schema details are not restated.

## P-GOV-002 — Workflow-routing vocabulary has explicit owners

- **Proposition record:** `reconstruction/propositions/A07.md`
- **Canonical instruction:** Canonical vocabulary must explicitly own Step-0 calendar/horizon routing, candidate-family generation, generic playbook family/setup/expression labels, carry handoff and carry-horizon branch terms, and must regenerate deterministically from its builder.
- **Class and current authority state:** vocabulary governance; active; extends P-GOV-001.
- **Introduction and authority chain:** **Lineage:** `source_planning/2026-03-26_GATE55_VOCABULARY_GOVERNANCE_ALIGNMENT.md:L5-L18`, `:L28-L32`.
- **Historical aliases:** Step-0, family/setup/expression and carry terms are canonical routing labels.
- **Inputs and validity constraints:** Current workflow routing surfaces and vocabulary builder inputs.
- **Transformation, calculation, decision or routing semantics:** Assign explicit owners and regenerate vocabulary deterministically.
- **Outputs and guarantees:** Owned canonical entries for routing, candidate generation, hierarchy and carry.
- **Time and state semantics:** Vocabulary generation follows the current governed workflow state.
- **Null, boundary and failure behaviour:** Unowned or non-deterministically generated terms are invalid.
- **Dependencies and downstream consequences:** P-GOV-001, P-ARCH-001, registry and carry contracts.
- **Explicit exclusions and non-goals:** No implicit ownership through naming alone.
- **Unresolved questions:** Detailed vocabulary entries are external to this proposition.

## P-DAT-004 — Canonical raw artefacts preserve source truth and provenance

- **Proposition record:** `reconstruction/propositions/A08.md`
- **Canonical instruction:** A canonical raw artefact must be admitted from actual repository raw content, not reconstructed from a workbook or padded with fabricated rows. It preserves source identity/capture time, OHLCV bars, repeated quote-level option-chain snapshots, normalised event rows and timestamp/session anchoring. Prepared values remain deterministically derived and must not be handwritten into raw artefacts.
- **Class and current authority state:** raw-data authority; active, bounded to the admitted artefact.
- **Introduction and authority chain:** **Lineage:** `source_planning/2026-03-30_GATE101_CANONICAL_RAW_BUNDLE_ADMISSION.md:L5-L20`, `:L22-L48`.
- **Historical aliases:** The specimen source name `gate_e_manual_pack` and bounded identity values are preserved.
- **Inputs and validity constraints:** Actual repository raw content with source/capture identity, bars, option snapshots and events.
- **Transformation, calculation, decision or routing semantics:** Admit without workbook reconstruction or padding; normalise event rows and anchor timestamps/sessions.
- **Outputs and guarantees:** Canonical raw artefact preserving provenance, four bars, three snapshots, 30 quote rows and two events in the bounded specimen.
- **Time and state semantics:** Capture time is `2026-03-23T13:55:00Z`; prepared values are derived later.
- **Null, boundary and failure behaviour:** Fabricated rows or handwritten prepared values invalidate the artefact.
- **Dependencies and downstream consequences:** Raw repository content, preparation service and provenance controls.
- **Explicit exclusions and non-goals:** No general coverage claim from the specimen.
- **Unresolved questions:** Vendor completeness and broader raw-corpus coverage are not established.

## P-TRACE-001 — Lawful raw-to-review execution path

- **Proposition record:** `reconstruction/propositions/A08.md`
- **Canonical instruction:** The lawful path is `raw bundle -> prepared runtime dataset -> cognition inputs -> review outputs`. Raw input is typed, preparation occurs through the checked-in preparation service, cognition conversion is explicit, and runtime execution uses the resulting typed inputs. Prepared snapshots may not be injected by hand as the primary ingress. Coverage gaps and orphan rows remain visible. Identical inputs must yield stable packet IDs, lineage and review output.
- **Class and current authority state:** end-to-end path/reproducibility; active.
- **Introduction and authority chain:** **Lineage:** `source_planning/2026-03-30_GATE102_CANONICAL_RAW_PATH_HARNESS.md:L5-L25`, `source_planning/2026-03-30_GATE102_CANONICAL_RAW_PATH_HARNESS.md:L27-L47`, `source_planning/2026-03-30_GATE102_CANONICAL_RAW_PATH_HARNESS.md:L49-L53`.
- **Historical aliases:** Dataset `gate102_canonical_raw_runtime`, sequence `seq-opening-balance` and playbook `continuation_ladder` are frozen specimen identities.
- **Inputs and validity constraints:** Typed raw bundle, checked-in preparation service, cognition converter and bounded supportive regime/inventory fixture.
- **Transformation, calculation, decision or routing semantics:** Run raw → prepared dataset → cognition inputs → governed runtime → review; preserve visible gaps and deterministic identity.
- **Outputs and guarantees:** Stable packet IDs, lineage and review; specimen outputs 100.0 chain coverage, 75.0 bar coverage, one orphan, three snapshots, spot 116.0, same-session event, balanced options, allow, 30.25 and continuation ladder.
- **Time and state semantics:** The first prepared sequence and all specimen states are frozen; identical inputs reproduce them.
- **Null, boundary and failure behaviour:** Hand-injected prepared snapshots are not primary ingress; gaps/orphans cannot be hidden.
- **Dependencies and downstream consequences:** P-DAT-004, preparation, cognition, serial runtime and review.
- **Explicit exclusions and non-goals:** No broader production-default or coverage claim.
- **Unresolved questions:** Supportive companion fixture generality and broader raw paths are not established.

## P-TRACE-002 — Raw/prepared parity is explicit and bounded

- **Proposition record:** `reconstruction/propositions/A08.md`
- **Canonical instruction:** Raw-path and prepared-path executions must be semantically equal on an explicitly declared comparable surface: temporal, options-flow, regime, inventory, risk-budget and sequence inputs; stage packet IDs, lineage, review packet, event-window state, options cluster, permission, deployable capital, active playbooks and review summary. Any future lawful divergence must be documented explicitly rather than implied.
- **Class and current authority state:** parity/replay; active.
- **Introduction and authority chain:** **Lineage:** `source_planning/2026-03-30_GATE103_RAW_PREPARED_PARITY.md:L5-L16`, `:L18-L43`.
- **Historical aliases:** Raw-path and prepared-path labels are retained as comparable entry modes.
- **Inputs and validity constraints:** Declared comparable temporal, options-flow, regime, inventory, risk-budget and sequence inputs.
- **Transformation, calculation, decision or routing semantics:** Execute both paths and compare every named semantic surface.
- **Outputs and guarantees:** Equality of stage packet IDs, lineage, review, event/options/permission/capital/playbook/summary outputs.
- **Time and state semantics:** Parity applies to identical declared inputs; lawful future divergence must be documented.
- **Null, boundary and failure behaviour:** Undeclared divergence or omitted comparison surface is a failure.
- **Dependencies and downstream consequences:** P-TRACE-001 and all compared stage contracts.
- **Explicit exclusions and non-goals:** No implied parity outside the declared surface.
- **Unresolved questions:** Treatment of intentional future divergence is procedural, not fully specified.

## P-TEST-001 — High-risk behavioural invariants

- **Proposition record:** `reconstruction/propositions/A08.md`
- **Canonical instruction:** Modifier kill switches and deployable-capital caps must remain stable under combined high-risk inputs; playbook eligibility must preserve no-trade behaviour across permission/event/options combinations; ordered event queries must progress monotonically and never move the next-event cursor backwards. Property/stateful testing is bounded to high-risk services and does not authorise indiscriminate test expansion.
- **Class and current authority state:** behavioural law revealed by tests; active.
- **Introduction and authority chain:** **Lineage:** `source_planning/2026-03-30_GATE104_PROPERTY_STATEFUL.md:L5-L26`, `:L28-L32`.
- **Historical aliases:** Named invariant behaviours, not historical test-file names, are canonical.
- **Inputs and validity constraints:** Combined high-risk modifier inputs, permission/event/options combinations and ordered event queries.
- **Transformation, calculation, decision or routing semantics:** Assert kill-switch/cap stability, no-trade preservation and monotonic cursor progress.
- **Outputs and guarantees:** Deterministic invariant outcomes and bounded stateful/property evidence.
- **Time and state semantics:** Event cursor must never move backwards; repeated high-risk combinations remain stable.
- **Null, boundary and failure behaviour:** Invariant violation is failure; test scope must not be widened indiscriminately.
- **Dependencies and downstream consequences:** Modifier, eligibility and temporal/event-query services.
- **Explicit exclusions and non-goals:** No blanket property-testing mandate.
- **Unresolved questions:** Specific generators and numerical domains are not stated.

## P-ARCH-002 — Typed ingress, transactional persistence and API translation boundaries

- **Proposition record:** `reconstruction/propositions/A09.md`
- **Canonical instruction:** Typed ingress must distinguish permitted coercion from prohibited payload shapes. Persistence seams must provide explicit commit/rollback transaction behaviour. API dependency seams must map success and typed lookup failure without widening domain authority. This does not impose repo-wide strict defaults or require every route to be covered identically.
- **Class and current authority state:** boundary contract; active, bounded.
- **Introduction and authority chain:** **Lineage:** `source_planning/2026-03-30_GATE105_INGRESS_DB_API.md:L5-L23`.
- **Historical aliases:** No historical aliases are stated.
- **Inputs and validity constraints:** Typed ingress payloads, persistence transactions and API dependency results.
- **Transformation, calculation, decision or routing semantics:** Validate allowed coercions/shapes; commit or roll back explicitly; translate success and typed lookup failure.
- **Outputs and guarantees:** Bounded typed ingress, transactional persistence and API translation results.
- **Time and state semantics:** Transaction state is atomic at the seam; no repo-wide default is implied.
- **Null, boundary and failure behaviour:** Prohibited payload shapes, failed transactions and lookup failures remain explicit.
- **Dependencies and downstream consequences:** Ingress, database/session and API dependency boundaries.
- **Explicit exclusions and non-goals:** No domain-authority widening and no claim of identical coverage for every route.
- **Unresolved questions:** Exact coercion matrix and transaction/API schemas are not stated.

## P-DAT-005 — Normalised feature packet and exact carried feature set

- **Proposition record:** `reconstruction/propositions/A09.md`
- **Canonical instruction:** A provenance-bearing normalised prepared feature packet must survive raw-to-prepared conversion and cognition ingress, with review-visible coverage. Its admitted fields are: `intraday_move_vs_rolling_range_5m`, `distance_to_vwap_vs_rolling_range_5m`, `intraday_move_vs_price_realised_vol_15m`, `front_iv_vs_front_realised_vol_ratio`, `next_iv_vs_next_realised_vol_ratio`, `atm_straddle_vs_spot_pct`, and `near_spot_front_volume_share`.
- **Class and current authority state:** prepared feature carriage; active.
- **Introduction and authority chain:** **Lineage:** `source_planning/2026-03-30_GATE115_NORMALISED_PREPARED_RUNTIME_FEATURES.md:L5-L19`, `:L21-L29`, `:L41-L45`.
- **Historical aliases:** The seven admitted field names are canonical carried-feature identifiers.
- **Inputs and validity constraints:** Raw/prepared inputs sufficient to derive the seven named normalised features plus provenance.
- **Transformation, calculation, decision or routing semantics:** Derive and carry the exact feature set through preparation and cognition ingress.
- **Outputs and guarantees:** Provenance-bearing normalised feature packet with review-visible coverage.
- **Time and state semantics:** Features survive raw-to-prepared conversion and cognition ingress for the same run.
- **Null, boundary and failure behaviour:** Missing source data must remain explicit; carriage does not authorise tuned thresholds.
- **Dependencies and downstream consequences:** P-DAT-002, preparation, cognition ingress and review.
- **Explicit exclusions and non-goals:** No additional fields, decision-law consumption or threshold authority by implication.
- **Unresolved questions:** Formulae, units and validity ranges for the seven fields are not stated.

## P-TMP-003 — Event-class timing profiles and calendar-aware next session

- **Proposition record:** `reconstruction/propositions/A09.md`
- **Canonical instruction:** Temporal classification must apply explicit timing profiles for macro-like, policy, company-like, expiry and venue-session events and expose the applied profile. Macro-like events use tighter imminent windows; company-like events retain longer same-session and cooling-off windows. Calendar authority must carry declared future trading days so next-session hints do not rely on weekend-only shortcuts.
- **Class and current authority state:** temporal policy; active; extends P-TMP-001.
- **Introduction and authority chain:** **Lineage:** `source_planning/2026-03-30_GATE116_EVENT_CLASS_TEMPORAL_WINDOWS.md:L5-L19`, `:L21-L30`.
- **Historical aliases:** Macro-like, policy, company-like, expiry and venue-session profile labels are canonical.
- **Inputs and validity constraints:** Event class, event timestamps and declared future trading days.
- **Transformation, calculation, decision or routing semantics:** Select the explicit event-class profile and calculate event windows/next-session hints calendar-aware.
- **Outputs and guarantees:** Applied timing profile, temporal class and valid next-session hint.
- **Time and state semantics:** Macro windows are tighter; company windows retain longer same-session/cooling-off periods.
- **Null, boundary and failure behaviour:** Weekend-only shortcuts or missing calendar authority cannot manufacture next-session truth.
- **Dependencies and downstream consequences:** P-TMP-001, event calendar and future-session authority.
- **Explicit exclusions and non-goals:** No generic one-window policy across event classes.
- **Unresolved questions:** Exact profile durations are not restated here.

## P-CTX-003 — Precursor context carries economics, not availability alone

- **Proposition record:** `reconstruction/propositions/A10.md`
- **Canonical instruction:** Precursor packets must carry both aggregated raw-field presence and derived economic values. Financial-calendar precursor projection routes through market-state synthesis, and supportive, contradictory and hostile precursor states must be able to produce distinguishable posture and review consequences.
- **Class and current authority state:** market context; active.
- **Introduction and authority chain:** **Lineage:** `source_planning/2026-03-30_GATE117_PRECURSOR_ECONOMICS.md:L1-L5`.
- **Historical aliases:** Precursor packet identity is preserved while its semantics widen from availability to economics.
- **Inputs and validity constraints:** Aggregated raw-field presence plus derived precursor economic values.
- **Transformation, calculation, decision or routing semantics:** Project financial-calendar precursor data through market-state synthesis and classify support/contradiction/hostility.
- **Outputs and guarantees:** Economically meaningful precursor context with distinguishable posture/review consequences.
- **Time and state semantics:** Current precursor state is tied to its source event/session context.
- **Null, boundary and failure behaviour:** Availability alone is insufficient; missing economics must not be treated as support.
- **Dependencies and downstream consequences:** Calendar precursor projection, market-state synthesis, posture and review.
- **Explicit exclusions and non-goals:** No binary presence-only interpretation.
- **Unresolved questions:** Economic formulae and classification thresholds are not stated.

## P-GOV-003 — Approved mutable runtime surfaces are explicit and observable

- **Proposition record:** `reconstruction/propositions/A10.md`
- **Canonical instruction:** The approved mutable surfaces are `entry_gate_score_floor`, `zone_score_threshold`, `distance_to_vwap_soft_limit_pct`, `risk_vix_caution_threshold`, `risk_vix_hot_threshold`, `max_risk_per_trade`, `target_fresh_deployable_pct`, and `hedge_required`. The modifier packet resolves their operative values, execution output carries them, and review exposes the same values; no consumer may depend on hidden side channels or implied policy state.
- **Class and current authority state:** runtime policy authority; active.
- **Introduction and authority chain:** **Lineage:** `source_planning/2026-03-30_GATE118_MUTABLE_SURFACE_RECONCILIATION.md:L5-L17`, `:L19-L28`.
- **Historical aliases:** The eight listed mutable-surface identifiers are canonical.
- **Inputs and validity constraints:** Modifier inputs, governed policy values and the eight admitted mutable surfaces.
- **Transformation, calculation, decision or routing semantics:** Resolve operative values in the modifier packet and carry the same values through execution and review.
- **Outputs and guarantees:** Observable, lineaged values for all eight surfaces.
- **Time and state semantics:** Values are resolved per runtime decision and remain consistent across stages.
- **Null, boundary and failure behaviour:** Hidden side-channel or implied policy state is invalid.
- **Dependencies and downstream consequences:** Modifier authority, execution output and review.
- **Explicit exclusions and non-goals:** No mutation outside the admitted surface set.
- **Unresolved questions:** Numeric ranges and precedence are specified later by coefficient authority.

## P-PLAY-005 — Candidate adjudication is score-driven and review-visible

- **Proposition record:** `reconstruction/propositions/A10.md`
- **Canonical instruction:** When multiple playbooks are eligible, execution must rank them deterministically by scored reasons, using registry priority only as a tie-break. It emits one explicit lead, candidate adjudication records, lead score and contradiction-resolution state, all visible to review.
- **Class and current authority state:** candidate selection; active.
- **Introduction and authority chain:** **Lineage:** `source_planning/2026-03-30_GATE119_CANDIDATE_ADJUDICATION.md:L5-L13`, `:L19-L22`.
- **Historical aliases:** Lead, candidate adjudication and contradiction-resolution labels are canonical outputs.
- **Inputs and validity constraints:** Multiple eligible playbooks, scored reasons and registry priorities.
- **Transformation, calculation, decision or routing semantics:** Rank deterministically by score, use priority only as tie-break and resolve contradictions.
- **Outputs and guarantees:** One explicit lead, adjudication records, lead score and contradiction state visible to review.
- **Time and state semantics:** Selection is deterministic for the current candidate set.
- **Null, boundary and failure behaviour:** Ties without governed priority or missing scores must not yield hidden selection.
- **Dependencies and downstream consequences:** Eligibility, registry, execution and review.
- **Explicit exclusions and non-goals:** No priority-first selection or opaque lead choice.
- **Unresolved questions:** Score formula and tie-break details beyond priority are not stated.

## P-EXE-004 — Governed execution geometry is template-backed

- **Proposition record:** `reconstruction/propositions/A10.md`
- **Canonical instruction:** Execution templates own bounded defaults for directional bias, ladder spacing, chase distance, stop distance, take-profit distance, hedge ratio and base per-slice risk. Execution output carries explicit geometry and notes, derived contextually from the selected template and current state. Geometry may respond to event/gamma stress but must not create a second execution doctrine.
- **Class and current authority state:** execution expression; active.
- **Introduction and authority chain:** **Lineage:** `source_planning/2026-03-30_GATE120_EXECUTION_GEOMETRY.md:L5-L13`, `:L19-L23`.
- **Historical aliases:** Named geometry fields retain their canonical template-backed meaning.
- **Inputs and validity constraints:** Selected execution template, current event/gamma context and posture/execution state.
- **Transformation, calculation, decision or routing semantics:** Resolve directional bias, ladder/chase/stop/take-profit distances, hedge ratio and per-slice risk.
- **Outputs and guarantees:** Explicit execution geometry and explanatory notes.
- **Time and state semantics:** Geometry is per current execution candidate and may respond to event/gamma stress.
- **Null, boundary and failure behaviour:** Missing template authority cannot be replaced with private defaults.
- **Dependencies and downstream consequences:** Playbook selection, template registry and execution output.
- **Explicit exclusions and non-goals:** No second execution doctrine or broker placement authority.
- **Unresolved questions:** Template values, units and stress transforms are not stated.

## P-RISK-001 — One authoritative final-risk join

- **Proposition record:** `reconstruction/propositions/A11.md`
- **Canonical instruction:** After execution synthesis and before review, one authoritative risk join evaluates posture, modifier, execution and final-risk inputs and returns `allow`, `derisk` or `block`. It preserves pre-final-risk snapshots and structured lineage, applies the disposition to execution, and exposes the result and reasons to review. Final risk is part of the runtime authority chain, not a detached advisory service.
- **Class and current authority state:** terminal risk; active.
- **Introduction and authority chain:** **Lineage:** `source_planning/2026-03-31_GATE121_FINAL_RISK_GATEWAY_JOIN.md:L5-L15`, `:L21-L25`.
- **Historical aliases:** `final_risk_join` and dispositions `allow`, `derisk`, `block` are canonical.
- **Inputs and validity constraints:** Posture, modifier, execution and final-risk inputs plus pre-final snapshots.
- **Transformation, calculation, decision or routing semantics:** Evaluate once after execution synthesis, apply disposition to execution and preserve reasons/lineage.
- **Outputs and guarantees:** Authoritative final-risk decision, reshaped execution and review-visible reasons.
- **Time and state semantics:** Join occurs after execution synthesis and before review; pre-final state remains inspectable.
- **Null, boundary and failure behaviour:** Missing/invalid inputs cannot be bypassed by detached advisory logic.
- **Dependencies and downstream consequences:** P-DEC-002, modifier, execution and review.
- **Explicit exclusions and non-goals:** No second final-risk authority or detached advisory-only interpretation.
- **Unresolved questions:** Exact overlay formula and failure default are not stated.

## P-GOV-004 — Coefficient scope separates behaviour from timing

- **Proposition record:** `reconstruction/propositions/A11.md`
- **Canonical instruction:** The governed coefficient universe must explicitly identify owner stage, units, bound class, baseline and sane min/max envelopes. The initial scope contains eight mutable runtime surfaces and separates sixteen behavioural temporal thresholds from two timing parameters so clock windows do not masquerade as alpha coefficients. Scope widening requires explicit admission.
- **Class and current authority state:** coefficient governance; active.
- **Introduction and authority chain:** **Lineage:** `source_planning/2026-03-31_GATE122_COEFFICIENT_SCOPE_FREEZE.md:L5-L13`, `:L20-L24`.
- **Historical aliases:** Behavioural temporal thresholds and timing parameters remain distinct governance classes.
- **Inputs and validity constraints:** Eight mutable surfaces, sixteen behavioural temporal thresholds and two timing parameters.
- **Transformation, calculation, decision or routing semantics:** Assign owner, units, bound class, baseline and sane min/max; separate clock timing from behavioural coefficients.
- **Outputs and guarantees:** A frozen governed coefficient universe and metadata.
- **Time and state semantics:** Scope is frozen until explicit admission; timing parameters do not masquerade as alpha.
- **Null, boundary and failure behaviour:** Unknown/unadmitted coefficients cannot enter silently.
- **Dependencies and downstream consequences:** P-GOV-003, P-TMP-003 and coefficient authority.
- **Explicit exclusions and non-goals:** No scope widening by workbook or implementation convenience.
- **Unresolved questions:** The full identifier list is not repeated in this proposition.

## P-GOV-005 — Typed coefficient authority and validation

- **Proposition record:** `reconstruction/propositions/A11.md`
- **Canonical instruction:** One typed governed authority contract covers admitted mutable surfaces, temporal thresholds and timing parameters. Each entry carries owner stage, units, baseline, min/max envelope, transform family and allowed upstream drivers. Unknown surfaces, absurd ranges and illegal transforms fail deterministically. Legacy example registries remain reference-only.
- **Class and current authority state:** configuration authority; active.
- **Introduction and authority chain:** **Lineage:** `source_planning/2026-03-31_GATE123_COEFFICIENT_AUTHORITY_CONTRACT.md:L5-L14`, `:L20-L24`.
- **Historical aliases:** Legacy example registries are reference-only aliases, not authority.
- **Inputs and validity constraints:** Admitted surfaces/thresholds/timing parameters and candidate authority entries.
- **Transformation, calculation, decision or routing semantics:** Validate owner, units, baseline, envelope, transform family and upstream drivers.
- **Outputs and guarantees:** One typed governed authority contract with deterministic rejection behaviour.
- **Time and state semantics:** Entries are versioned authority state; exact lifecycle is not otherwise stated.
- **Null, boundary and failure behaviour:** Unknown surfaces, absurd ranges and illegal transforms fail deterministically.
- **Dependencies and downstream consequences:** P-GOV-004 and runtime policy loaders.
- **Explicit exclusions and non-goals:** No private/legacy registry authority.
- **Unresolved questions:** Versioning, persistence and approval workflow are not fully stated.

## P-GOV-006 — Runtime values load from governed authority and carry lineage

- **Proposition record:** `reconstruction/propositions/A11.md`
- **Canonical instruction:** Mutable-surface baselines, floors and caps are loaded from the governed coefficient authority rather than private class constants. Each resolved value carries owner stage, authority version, baseline reference and numeric envelope. This externalisation does not alter the admitted surface universe.
- **Class and current authority state:** policy resolution; active.
- **Introduction and authority chain:** **Lineage:** `source_planning/2026-03-31_GATE124_EXTERNALISED_MUTABLE_SURFACE_AUTHORITY.md:L5-L9`, `source_planning/2026-03-31_GATE124_EXTERNALISED_MUTABLE_SURFACE_AUTHORITY.md:L15-L18`.
- **Historical aliases:** Private class constants lose authority; the two frozen specimen values retain stage-specific meaning.
- **Inputs and validity constraints:** Governed coefficient entries, runtime drivers and the admitted mutable surface set.
- **Transformation, calculation, decision or routing semantics:** Load baselines/floors/caps, resolve values with lineage, then apply modifier before final risk.
- **Outputs and guarantees:** Resolved values with owner, authority version, baseline reference and envelope; specimen 20.625 pre-final and 13.4062 post-final.
- **Time and state semantics:** Ordering is modifier resolution first, authoritative final-risk derisk second.
- **Null, boundary and failure behaviour:** Private constants or collapse of the two stage values is invalid.
- **Dependencies and downstream consequences:** P-GOV-005, modifier packet, P-RISK-001 and review.
- **Explicit exclusions and non-goals:** No widening of the coefficient universe.
- **Unresolved questions:** General resolution precedence beyond the admitted evidence is not fully stated.

## P-REV-003 — Review exposes the exact resolved coefficient chain

- **Proposition record:** `reconstruction/propositions/A12.md`
- **Canonical instruction:** Review must carry the same resolved-surface chain used by runtime policy, including baseline reference, baseline and effective values, clamp state, precedence band, source policy IDs and authority version. It must not reconstruct a second coefficient story from free text. Raw and prepared paths preserve identical coefficient lineage.
- **Class and current authority state:** review lineage; active.
- **Introduction and authority chain:** **Lineage:** `source_planning/2026-03-31_GATE125_REVIEW_VISIBLE_COEFFICIENT_LINEAGE.md:L5-L9`, `:L15-L17`.
- **Historical aliases:** No historical aliases are stated.
- **Inputs and validity constraints:** The exact resolved-surface chain used by runtime policy.
- **Transformation, calculation, decision or routing semantics:** Carry baseline/effective values, clamp, precedence, policy IDs and authority version without reconstruction.
- **Outputs and guarantees:** Review-visible coefficient chain identical across raw and prepared paths.
- **Time and state semantics:** Review reflects the same run-time resolution and parity state.
- **Null, boundary and failure behaviour:** Free-text reconstruction or divergent lineage is failure.
- **Dependencies and downstream consequences:** P-GOV-005/006, runtime policy and P-TRACE-002.
- **Explicit exclusions and non-goals:** No second coefficient story.
- **Unresolved questions:** Review schema beyond listed fields is not stated.

## P-TMP-004 — Governed temporal thresholds with explicit unit conversion

- **Proposition record:** `reconstruction/propositions/A12.md`
- **Canonical instruction:** Admitted temporal thresholds and timing parameters load through governed identifiers from the coefficient authority. Percent primitives are converted deterministically when authority is expressed in basis points. Non-admitted controls such as break-count floors and selected open-window guards remain explicit rather than being silently absorbed. Workbooks remain research provenance, not direct runtime law, and no Asia/Japan coefficient may enter by stealth.
- **Class and current authority state:** temporal threshold authority; active; extends P-TMP-003.
- **Introduction and authority chain:** **Lineage:** `source_planning/2026-03-31_GATE126_BOUNDED_TEMPORAL_THRESHOLD_AUTHORITY.md:L4-L13`, `source_planning/2026-03-31_GATE126_BOUNDED_TEMPORAL_THRESHOLD_AUTHORITY.md:L22-L32`; corroborated by `source_planning/2026-03-31_GATE130_RUNTIME_EXPECTATION_REFRESH.md:L4-L13`.
- **Historical aliases:** Named governed identifiers and bounded specimen states/values are preserved.
- **Inputs and validity constraints:** Admitted temporal thresholds/timing parameters, percent primitives, coefficient authority and canonical raw/prepared specimens.
- **Transformation, calculation, decision or routing semantics:** Load governed thresholds, convert basis points deterministically and run temporal/final-risk path.
- **Outputs and guarantees:** Threshold decisions plus frozen outcomes: 0.95 destabilising→19.6625; prepared/raw event-imminent, no playbooks, derisk, 0.0.
- **Time and state semantics:** Values apply to the bounded threshold edge and all three prepared snapshots; final risk occurs before review.
- **Null, boundary and failure behaviour:** Non-admitted controls stay explicit; workbooks/Asia/Japan values cannot enter silently.
- **Dependencies and downstream consequences:** P-GOV-005/006, P-TMP-003, P-RISK-001, P-TRACE-001/002 and review.
- **Explicit exclusions and non-goals:** No universal-default claim or coefficient-scope widening.
- **Unresolved questions:** Complete threshold identifiers and exact unit rules are not restated.

## P-TRACE-003 — Replay carries deterministic governed coefficient snapshots

- **Proposition record:** `reconstruction/propositions/A12.md`
- **Canonical instruction:** Replay/calibration output must carry a deterministic snapshot identifier derived from the same governed resolved-surface evidence used by runtime and review. Snapshot IDs and admitted evidence are exposed on audit packets, replay runs and comparisons by coefficient set; replay must not privately reconstruct coefficients.
- **Class and current authority state:** replay lineage; active.
- **Introduction and authority chain:** **Lineage:** `source_planning/2026-03-31_GATE127_REPLAY_COEFFICIENT_VISIBILITY_AND_PACK_CLOSEOUT.md:L4-L14`, `:L23-L25`.
- **Historical aliases:** Snapshot identifier is the canonical replay lineage handle.
- **Inputs and validity constraints:** Governed resolved-surface evidence used by runtime and review.
- **Transformation, calculation, decision or routing semantics:** Derive a deterministic snapshot ID and attach it to audit packets, replay runs and comparisons.
- **Outputs and guarantees:** Replay/calibration outputs with consistent coefficient snapshot lineage.
- **Time and state semantics:** Identical governed evidence yields the same snapshot identity.
- **Null, boundary and failure behaviour:** Private coefficient reconstruction or unmatched evidence is invalid.
- **Dependencies and downstream consequences:** P-GOV-005/006, P-REV-003 and replay services.
- **Explicit exclusions and non-goals:** No separate replay coefficient authority.
- **Unresolved questions:** Snapshot-hash algorithm and retention are not stated.

## P-ARCH-003 — Review stages and packet-emitting stages are distinct

- **Proposition record:** `reconstruction/propositions/A13.md`
- **Canonical instruction:** The review-stage sequence includes the terminal `final_risk_join`, while stage packet identifiers cover only packet-emitting runtime stages plus review. Expectations must follow the actual governed distinction rather than a pre-final-risk stage tail.
- **Class and current authority state:** runtime/review ordering; active.
- **Introduction and authority chain:** **Lineage:** `source_planning/2026-03-31_GATE130_RUNTIME_EXPECTATION_REFRESH.md:L4-L13`.
- **Historical aliases:** `final_risk_join` is a review-stage entry but not necessarily a packet-emitting stage ID.
- **Inputs and validity constraints:** Governed runtime stage order, packet emitters and review sequence.
- **Transformation, calculation, decision or routing semantics:** Maintain separate ordered lists for review stages and packet-emitting stages.
- **Outputs and guarantees:** Correct stage expectations and identifiers.
- **Time and state semantics:** Terminal final-risk join is included before review; packet IDs remain scoped to actual emitters.
- **Null, boundary and failure behaviour:** Pre-final tail assumptions or invented packet IDs are invalid.
- **Dependencies and downstream consequences:** P-RISK-001, packet protocols and review.
- **Explicit exclusions and non-goals:** No forced one-to-one mapping between review stages and packet emitters.
- **Unresolved questions:** Complete emitter list is not restated.

## P-TRACE-004 — Bounded sibling scenario packs are anchored and explicit

- **Proposition record:** `reconstruction/propositions/A13.md`
- **Canonical instruction:** A bounded semantic scenario pack contains materially distinct but non-absurd sibling scenarios anchored to an admitted prepared-runtime path. Each scenario names its perturbations; the admitted Gate-132 pack contains five scenarios.
- **Class and current authority state:** scenario evidence; active.
- **Introduction and authority chain:** **Lineage:** `source_planning/2026-03-31_GATE132_BOUNDED_TRACE_SCENARIO_PACK.md:L1-L14`.
- **Historical aliases:** The admitted Gate-132 five-scenario pack is preserved as a bounded specimen.
- **Inputs and validity constraints:** An admitted prepared-runtime anchor and explicit non-absurd perturbations.
- **Transformation, calculation, decision or routing semantics:** Construct materially distinct sibling scenarios and name every perturbation.
- **Outputs and guarantees:** A five-scenario bounded semantic evidence pack.
- **Time and state semantics:** All siblings share the declared anchor and differ only by stated perturbations.
- **Null, boundary and failure behaviour:** Unanchored, absurd or hidden perturbations are invalid.
- **Dependencies and downstream consequences:** P-TRACE-001 and prepared-runtime authority.
- **Explicit exclusions and non-goals:** No native scenario-engine or general scenario catalogue is admitted.
- **Unresolved questions:** The five scenario contents are not reproduced in this proposition.

## P-TRACE-005 — Bounded trace review is semantic proof, not alpha tuning

- **Proposition record:** `reconstruction/propositions/A13.md`
- **Canonical instruction:** Bounded sibling trace review is a distinct late-phase semantic proof. It runs the declared scenarios through the live decision path and applies broad human-sanity expectations without claiming to tune alpha or establish profitability.
- **Class and current authority state:** review regime; active.
- **Introduction and authority chain:** **Lineage:** `source_planning/2026-03-31_GATE133_BOUNDED_TRACE_REVIEW_REGIME.md:L1-L13`.
- **Historical aliases:** No historical aliases are stated.
- **Inputs and validity constraints:** Declared bounded sibling scenarios and live decision path.
- **Transformation, calculation, decision or routing semantics:** Execute each scenario and apply broad human-sanity review.
- **Outputs and guarantees:** Late-phase semantic proof evidence.
- **Time and state semantics:** Review occurs after scenario declaration against current governed path.
- **Null, boundary and failure behaviour:** A result cannot be treated as alpha tuning or profitability proof.
- **Dependencies and downstream consequences:** P-TRACE-004, serial/final-risk/review path.
- **Explicit exclusions and non-goals:** No optimisation, calibration authority or profit claim.
- **Unresolved questions:** Human-sanity criteria are deliberately broad and not numerically complete.

## P-ARCH-004 — Intermediate stage ownership must remain inspectable

- **Proposition record:** `reconstruction/propositions/A14.md`
- **Canonical instruction:** The runtime must distinguish: posture before modifier mutation; cited eligibility before execution; execution before modifier mutation; execution after modifier mutation but before terminal risk; and the terminal risk decision before final execution reshaping. Review and trace consumers must be able to inspect these ownership boundaries rather than seeing only the final mutated objects.
- **Class and current authority state:** stage ownership; active.
- **Introduction and authority chain:** **Introduction:** overwrite/consumer inventory at `source_planning/2026-04-01_GATE142_OVERWRITE_AND_OWNERSHIP_INVENTORY.md:L5-L55`.<br>**Historical baseline:** the observed sequence was first frozen at `source_planning/2026-04-01_GATE141_STAGE_LOCAL_HANDOFF_PACK_BOOTSTRAP.md:L7-L24`; its planning/status language is not runtime proof.<br>**Required preserved fields:** `:L76-L105`.
- **Historical aliases:** The five named intermediate ownership surfaces are canonical seam identities.
- **Inputs and validity constraints:** Posture, eligibility, execution pre/post modifier, terminal-risk decision and final reshaping.
- **Transformation, calculation, decision or routing semantics:** Preserve each stage-local object before downstream mutation and expose it to review/trace.
- **Outputs and guarantees:** Inspectable intermediate ownership boundaries.
- **Time and state semantics:** Order is posture → eligibility → execution pre-modifier → execution post-modifier/pre-final → final-risk → final reshaping.
- **Null, boundary and failure behaviour:** Overwriting or exposing only final mutated objects is invalid.
- **Dependencies and downstream consequences:** P-DEC-002, P-GOV-007, P-RISK-001 and review.
- **Explicit exclusions and non-goals:** No outcome change is authorised merely to expose seams.
- **Unresolved questions:** Exact object schemas are specified in the cited source, not fully repeated here.

## P-TRACE-006 — Additive StageLocalHandoffSurface

- **Proposition record:** `reconstruction/propositions/A14.md`
- **Canonical instruction:** `StageLocalHandoffSurface` additively carries `cited_posture_pre_modifier`, `cited_eligibility`, `execution_pre_modifier`, `execution_post_modifier_pre_final_risk`, and `final_risk_decision` into review and runtime results. Existing seven-stage order, modifier packet, pre-final-risk compatibility fields, final-risk join, final outcomes and DMP v2 packet order remain unchanged.
- **Class and current authority state:** trace/review carriage; active; implements P-ARCH-004 without changing outcomes.
- **Introduction and authority chain:** **Lineage:** `source_planning/2026-04-01_GATE143_ADDITIVE_STAGE_LOCAL_HANDOFF.md:L5-L17`, `:L19-L45`, `:L47-L62`.
- **Historical aliases:** `StageLocalHandoffSurface` and its five field names are canonical.
- **Inputs and validity constraints:** The five preserved stage-local objects from P-ARCH-004.
- **Transformation, calculation, decision or routing semantics:** Additively carry them into runtime results and review.
- **Outputs and guarantees:** Nested handoff surface while preserving existing order, packets and outcomes.
- **Time and state semantics:** Carriage is additive within the same run; existing seven-stage/DMP order remains.
- **Null, boundary and failure behaviour:** Missing or mutated seam values break inspectability; no fallback reconstruction is authorised.
- **Dependencies and downstream consequences:** P-ARCH-004, runtime result and review contracts.
- **Explicit exclusions and non-goals:** No outcome, final-risk or DMP-order change.
- **Unresolved questions:** Compatibility retirement is not stated.

## P-DEC-002 — Posture hard invariants, local envelope and annotations are separate

- **Proposition record:** `reconstruction/propositions/A14.md`
- **Canonical instruction:** Posture evaluation materialises hard-block truth in `hard_invariants`; base permission, posture label, deployable-capital envelope and derisk reasons in `local_envelope`; and selector/modifier notes in `downstream_annotations`. Non-posture notes must not contaminate posture-owned surfaces. Flat fields and reasons may survive as compatibility only, with no outcome or stage-order change.
- **Class and current authority state:** posture ownership; active.
- **Introduction and authority chain:** **Lineage:** `source_planning/2026-04-01_GATE144_POSTURE_HARD_INVARIANTS_AND_LOCAL_ENVELOPE.md:L5-L19`, `:L21-L35`, `:L37-L57`.
- **Historical aliases:** Flat posture fields/reasons survive only as compatibility aliases.
- **Inputs and validity constraints:** Posture inputs, hard-block facts, permission/capital envelope and downstream notes.
- **Transformation, calculation, decision or routing semantics:** Partition truth into `hard_invariants`, `local_envelope` and `downstream_annotations`.
- **Outputs and guarantees:** Typed posture output with uncontaminated ownership surfaces.
- **Time and state semantics:** Materialised during posture evaluation before modifier and terminal risk.
- **Null, boundary and failure behaviour:** Non-posture notes may not enter posture-owned fields; missing hard invariants cannot be hidden.
- **Dependencies and downstream consequences:** P-ARCH-004, modifier, execution and review.
- **Explicit exclusions and non-goals:** No selector/modifier ownership in posture and no outcome/order change.
- **Unresolved questions:** Flat compatibility retirement is not stated.

## P-GOV-007 — Modifier packet is authority; flat mutation is compatibility

- **Proposition record:** `reconstruction/propositions/A15.md`
- **Canonical instruction:** `ModifierRuntimePacket` is the authoritative modifier decision. Posture-owned fields remain intact; any flat posture or execution changes are recorded as a bounded compatibility bridge with packet authority, applied policy IDs and deployable-capital consequences. Execution must not invent a second private modifier interpretation, and stage/final-risk semantics remain unchanged.
- **Class and current authority state:** modifier authority; active.
- **Introduction and authority chain:** **Lineage:** `source_planning/2026-04-01_GATE145_MODIFIER_EMITTED_POLICY_COMPATIBILITY_BRIDGE.md:L5-L15`, `:L17-L36`, `:L38-L59`.
- **Historical aliases:** Flat posture/execution mutation is a bounded compatibility projection only.
- **Inputs and validity constraints:** `ModifierRuntimePacket`, posture-owned fields, policy IDs and deployable-capital consequences.
- **Transformation, calculation, decision or routing semantics:** Resolve modifier authority in the packet and project any required flat changes with explicit lineage.
- **Outputs and guarantees:** Authoritative modifier packet plus bounded compatibility effects.
- **Time and state semantics:** Modifier acts after posture and before final risk.
- **Null, boundary and failure behaviour:** A private execution interpretation or unlineaged flat mutation is invalid.
- **Dependencies and downstream consequences:** P-GOV-006, P-DEC-002, execution and P-RISK-001.
- **Explicit exclusions and non-goals:** No second modifier authority and no stage/final-risk semantic change.
- **Unresolved questions:** Compatibility retirement is not stated.

## P-PLAY-006 — Eligibility admits; execution owns and adjudicates candidates

- **Proposition record:** `reconstruction/propositions/A15.md`
- **Canonical instruction:** Stage 5 owns admissibility: permission/no-trade reasons plus admissible/watch families, variants and playbook IDs. Stage 6 owns candidate execution: received IDs, adjudicated IDs, selected lead and contradiction lineage. Compatibility lists may remain, but the boundary must not alter admissibility, lead selection, geometry, terminal risk or packet order.
- **Class and current authority state:** stage authority; active.
- **Introduction and authority chain:** **Lineage:** `source_planning/2026-04-01_GATE146_ELIGIBILITY_ADMISSIBILITY_AND_EXECUTION_CANDIDATE_OWNERSHIP.md:L5-L17`, `:L19-L41`, `:L43-L67`.
- **Historical aliases:** Compatibility candidate lists may survive but do not own the boundary.
- **Inputs and validity constraints:** Stage-5 permission/reasons and candidate families/variants/IDs; Stage-6 received candidates and scores.
- **Transformation, calculation, decision or routing semantics:** Stage 5 admits/watches; Stage 6 adjudicates, selects lead and records contradiction lineage.
- **Outputs and guarantees:** Distinct admissibility and execution-candidate outputs.
- **Time and state semantics:** Stage order is fixed: eligibility before execution.
- **Null, boundary and failure behaviour:** Execution may not invent admissibility; compatibility lists may not alter results.
- **Dependencies and downstream consequences:** P-PLAY-004/005, P-ARCH-004, execution, final risk and packets.
- **Explicit exclusions and non-goals:** No boundary collapse or changes to geometry/final risk/packet order.
- **Unresolved questions:** Candidate scoring details remain governed by P-PLAY-005.

## P-RISK-002 — Overlay evaluation and posture-aware terminal application are distinct

- **Proposition record:** `reconstruction/propositions/A15.md`
- **Canonical instruction:** Preserve the raw market/portfolio overlay decision separately from posture-aware terminal application. Terminal application records whether it aligned, further derisked or escalated the overlay, using explicit overlap classes. A compatibility wrapper may return the final decision, but final allow/derisk/block outcomes, execution effects, stage order and DMP packet order remain unchanged.
- **Class and current authority state:** terminal-risk decomposition; active; clarifies P-RISK-001.
- **Introduction and authority chain:** **Lineage:** `source_planning/2026-04-01_GATE147_OVERLAY_EVALUATION_AND_TERMINAL_RISK_APPLICATION.md:L5-L17`, `:L19-L44`, `:L46-L68`.
- **Historical aliases:** The seven overlap-class labels are canonical; compatibility final-decision wrapper may remain.
- **Inputs and validity constraints:** Raw market/portfolio overlay decision and posture state.
- **Transformation, calculation, decision or routing semantics:** Evaluate overlay separately, then apply posture-aware terminal disposition and classify overlap.
- **Outputs and guarantees:** Overlay decision, terminal application, overlap class and final allow/derisk/block result.
- **Time and state semantics:** Overlay precedes terminal application; final effects preserve stage/DMP order.
- **Null, boundary and failure behaviour:** Collapsed or unexplained override is invalid.
- **Dependencies and downstream consequences:** P-RISK-001, posture, execution and review.
- **Explicit exclusions and non-goals:** No new final outcome set or packet-order change.
- **Unresolved questions:** Overlay calculation details are not stated.

## P-REV-004 — Preserved seams are first-class review and trace outputs

- **Proposition record:** `reconstruction/propositions/A15.md`
- **Canonical instruction:** Review packets and bounded trace results expose admissibility, candidate ownership, overlay decision and terminal application directly while retaining nested stage-local handoff and `final_risk_join` compatibility. Human trace reports compare Stage-5 admission, Stage-6 lead ownership, overlay and terminal decisions. Preserved seams must agree with the compatibility final outcome and must not change runtime decisions.
- **Class and current authority state:** review/trace; active.
- **Introduction and authority chain:** **Lineage:** `source_planning/2026-04-01_GATE148_REVIEW_TRACE_REPLAY_AND_LEGACY_EXPECTATION_RECONCILIATION.md:L5-L19`, `:L21-L56`, `:L58-L65`.
- **Historical aliases:** `final_risk_join` compatibility and nested handoff names remain visible.
- **Inputs and validity constraints:** Admissibility, candidate ownership, overlay, terminal application and stage-local handoff.
- **Transformation, calculation, decision or routing semantics:** Expose and compare all preserved seams against the final compatibility outcome.
- **Outputs and guarantees:** Review packets and human trace reports with direct seam evidence.
- **Time and state semantics:** Review follows runtime and must reflect the same run/order.
- **Null, boundary and failure behaviour:** Disagreement between seams and final outcome is failure; review may not repair runtime.
- **Dependencies and downstream consequences:** P-TRACE-006, P-PLAY-006, P-RISK-002.
- **Explicit exclusions and non-goals:** No runtime-decision change through review.
- **Unresolved questions:** Report formatting is not specified.

## P-ARCH-005 — Compatibility survives until explicit retirement; successor scope is bounded

- **Proposition record:** `reconstruction/propositions/A15.md`
- **Canonical instruction:** Existing compatibility surfaces remain active until explicitly retired. The historical seam work is retained as evidence, but corrective work must address field-level ownership, transitive consumers and overstated downstream claims rather than rewriting history. Independent parallel risk, a final arbiter, dynamic coefficient redesign and broader portfolio replacement are explicitly deferred by this corpus point.
- **Class and current authority state:** migration boundary; active.
- **Introduction and authority chain:** **Lineage:** `source_planning/2026-04-02_GATE150_CORRECTIVE_SUCCESSOR_PACK_BOOTSTRAP.md:L5-L20`, `:L43-L60`, `:L62-L74`.
- **Historical aliases:** Existing compatibility surfaces and historical seam evidence retain their names until explicit retirement.
- **Inputs and validity constraints:** Current compatibility surfaces, transitive consumers and historical seam evidence.
- **Transformation, calculation, decision or routing semantics:** Preserve until explicit retirement and constrain corrective work to field-level ownership and truthful scope.
- **Outputs and guarantees:** Bounded migration state with evidence continuity.
- **Time and state semantics:** Compatibility persists across successor work unless expressly retired.
- **Null, boundary and failure behaviour:** Missing Gates 151–156 cannot be inferred as authority.
- **Dependencies and downstream consequences:** P-ARCH-004/P-TRACE-006 and successor authority.
- **Explicit exclusions and non-goals:** No independent final arbiter, dynamic coefficient redesign or portfolio replacement at this corpus point.
- **Unresolved questions:** Contents of absent Gates 151–156 and later retirement decisions remain unresolved.

## P-ARCH-006 — Typed contracts carry coordination truth without absorbing policy

- **Proposition record:** `reconstruction/propositions/B01.md`
- **Canonical instruction:** Execution lifecycle, execution coordination, final-risk overlay, parallel-risk assessment and outbound projection must cross admitted boundaries through typed contracts rather than arbitrary dictionaries. `StageLocalHandoffSurface` is the live execution-to-final-risk seam. The runtime orchestrator validates typed stage surfaces in governed order but remains a coordinator and must not absorb stage policy. Services remain small coordination owners, and outbound DTO shape derives from admitted contracts rather than incidental mapping keys.
- **Class and current authority state:** `bounded_repair`; active; refines P-ARCH-002, P-ARCH-003, P-ARCH-004 and P-TRACE-006 without replacing their ownership rules.
- **Introduction and authority chain:** **Lineage:** `source_successor_briefs/nvda_next_continuation_brief_v3_2026-04-19.md:L95-L120`, `:L137-L155`, `:L179-L208`.<br>**Authority effect:** Repairs thin or dormant seam realisations identified by the successor brief; it does not establish that the repairs were implemented and does not replace the original stage, handoff or compatibility semantics.
- **Historical aliases:** `StageLocalHandoffSurface` remains the live execution-to-final-risk seam; arbitrary dictionaries lose authority.
- **Inputs and validity constraints:** Typed lifecycle, coordination, risk, parallel-risk and outbound contracts.
- **Transformation, calculation, decision or routing semantics:** Validate typed stage surfaces in order while keeping orchestration policy-free; project DTOs from contracts.
- **Outputs and guarantees:** Typed coordination seams and bounded service outputs.
- **Time and state semantics:** Governed order persists through each run; no hidden orchestration state is admitted.
- **Null, boundary and failure behaviour:** Arbitrary mapping keys or thin dormant seams cannot claim authority.
- **Dependencies and downstream consequences:** P-ARCH-002/003/004, P-TRACE-006 and downstream DTO projection.
- **Explicit exclusions and non-goals:** Orchestrator and services may not absorb stage policy.
- **Unresolved questions:** Exact contract schemas and implementation status are not established.

## P-RISK-003 — Capital authority consumes typed final-risk truth and remains downstream

- **Proposition record:** `reconstruction/propositions/B01.md`
- **Canonical instruction:** Capital deployment authority consumes the admitted final-risk result through a typed or otherwise constrained final-risk seam, not a free string and not arbitrary upstream cognition fields. It remains downstream of terminal risk and must not leak capital policy into the serial cognitive spine. Direct negative checks should make unauthorised upstream-field consumption observable.
- **Class and current authority state:** `clarification`; active; clarifies P-RISK-001 and P-RISK-002.
- **Introduction and authority chain:** **Lineage:** `source_successor_briefs/nvda_next_continuation_brief_v3_2026-04-19.md:L122-L127`, `:L157-L162`.<br>**Authority effect:** Makes the original downstream final-risk/capital boundary explicit; it does not define a new capital-allocation formula.
- **Historical aliases:** Free-string final-risk input is explicitly non-authoritative.
- **Inputs and validity constraints:** Typed/constrained final-risk result.
- **Transformation, calculation, decision or routing semantics:** Validate and pass final-risk truth to capital authority without reading arbitrary cognition fields.
- **Outputs and guarantees:** Bounded capital-authority input with observable negative checks.
- **Time and state semantics:** Capital remains strictly downstream of terminal risk.
- **Null, boundary and failure behaviour:** Unauthorised upstream-field consumption is a failure.
- **Dependencies and downstream consequences:** P-RISK-001/002 and capital deployment.
- **Explicit exclusions and non-goals:** No capital policy in serial cognition and no allocation formula by this proposition.
- **Unresolved questions:** Capital formula is supplied later by P-CAP-002.

## P-PRISK-001 — Parallel risk is a deterministic, non-mutating sibling lane

- **Proposition record:** `reconstruction/propositions/B01.md`
- **Canonical instruction:** A parallel-risk lane may be co-resident with the governed runtime but remains structurally separate from the serial spine. It produces typed environment assessment, candidate audit and lane-evaluation receipts; it must not mutate serial-stage outputs, and repeated identical inputs must produce deterministic lane packets and supporting receipts.
- **Class and current authority state:** `new_design_authority`; active within the bounded successor scope.
- **Introduction and authority chain:** **Lineage:** `source_successor_briefs/nvda_next_continuation_brief_v3_2026-04-19.md:L99-L105`, `:L163-L176`.<br>**Authority effect:** Introduces the bounded parallel-risk lane that A061 had explicitly deferred. It does not yet authorise a final arbiter, portfolio replacement or serial-spine policy mutation.
- **Historical aliases:** Parallel-risk lane, environment assessment, candidate audit and lane-evaluation receipt labels are canonical.
- **Inputs and validity constraints:** Typed bounded environment/candidate inputs independent of serial mutation.
- **Transformation, calculation, decision or routing semantics:** Evaluate deterministically in a co-resident sibling lane and emit typed packets/receipts.
- **Outputs and guarantees:** Environment assessment, candidate audit and lane-evaluation evidence.
- **Time and state semantics:** Identical inputs reproduce lane packets and receipts; lane remains structurally separate.
- **Null, boundary and failure behaviour:** Mutation of serial outputs or nondeterminism is invalid.
- **Dependencies and downstream consequences:** Serial outputs, typed contracts and review/audit consumers.
- **Explicit exclusions and non-goals:** No final arbiter, portfolio replacement or serial-policy mutation.
- **Unresolved questions:** Exact lane calculations and later stages are not yet defined.

## P-API-001 — Public DTO projection is bounded; broker integration remains protocol-only unless admitted

- **Proposition record:** `reconstruction/propositions/B02.md`
- **Canonical instruction:** Public API output crosses an explicit DTO projection boundary located either in a dedicated egress adapter or in narrower route-local boundary code. The choice must be explicit; projection must not depend on arbitrary internal dictionary shape and must not bleed into orchestration. The broker boundary is an interface/protocol reservation by default. No live adapter, network, credentials or external execution behaviour may be invented merely to close a structural reservation.
- **Class and current authority state:** `new_design_authority`; active within the bounded successor scope.
- **Introduction and authority chain:** **Lineage:** `source_successor_briefs/nvda_api_dto_broker_boundary_resolution_tranche_v1_brief_2026-04-20.md:L11-L29`, `:L83-L114`, `:L159-L215`.<br>**Authority effect:** Extends P-ARCH-006's typed egress rule with a bounded public-projection and broker-interface decision. It does not claim any concrete API or broker implementation exists.
- **Historical aliases:** No concrete route/package alias is canonical; broker remains a protocol reservation.
- **Inputs and validity constraints:** Admitted internal contracts and public-response requirements.
- **Transformation, calculation, decision or routing semantics:** Project through an explicit egress adapter or explicitly bounded route-local boundary.
- **Outputs and guarantees:** Public DTO independent of arbitrary internal dictionaries; broker interface reservation.
- **Time and state semantics:** Projection occurs at egress; no live network lifecycle is admitted.
- **Null, boundary and failure behaviour:** Missing live broker implementation remains absent rather than fabricated.
- **Dependencies and downstream consequences:** P-ARCH-006, API boundary and broker protocol.
- **Explicit exclusions and non-goals:** No orchestration bleed, credentials, network or external execution.
- **Unresolved questions:** Exact DTO schema and broker protocol are not stated.

## P-ARCH-007 — Boundary composition, raw ingress, preparation and reference authority remain separate

- **Proposition record:** `reconstruction/propositions/B02.md`
- **Canonical instruction:** Boundary bootstrap and API wiring compose the application but do not own runtime orchestration or broker logic. Raw-bundle/source decoding is upstream ingress; preparation owns subsequent runtime preparation; cognition ingress owns semantic translation. Calendar/reference import remains a reference-authority boundary and must not be reclassified as ordinary runtime ingress. Compatibility wrappers may remain thin, but may not obscure these ownership separations.
- **Class and current authority state:** `clarification`; active; clarifies P-DAT-001, P-DAT-002, P-DAT-004, P-ARCH-001, P-ARCH-002 and P-ARCH-006.
- **Introduction and authority chain:** **Lineage:** `source_successor_briefs/nvda_boundary_home_convergence_tranche_v2_brief_2026-04-20.md:L95-L107`, `:L141-L180`, `:L187-L206`, `:L297-L305`.<br>**Authority effect:** The named package homes and file cuts are `implementation_specific_instruction`; the enduring authority is the ownership separation.
- **Historical aliases:** Thin compatibility wrappers may remain; package/file names are non-canonical implementation detail.
- **Inputs and validity constraints:** Boundary bootstrap/API wiring, raw decoding, preparation, cognition translation and calendar/reference imports.
- **Transformation, calculation, decision or routing semantics:** Compose boundaries while preserving separate ownership and ordered handoffs.
- **Outputs and guarantees:** Explicit application composition with distinct ingress/preparation/cognition/reference seams.
- **Time and state semantics:** Raw decoding precedes preparation, which precedes cognition translation; reference import remains separate.
- **Null, boundary and failure behaviour:** Compatibility wrappers may not obscure or reclassify ownership.
- **Dependencies and downstream consequences:** P-DAT-001/002/004, P-ARCH-001/002/006.
- **Explicit exclusions and non-goals:** No runtime orchestration/broker ownership in bootstrap and no calendar-as-ordinary-ingress collapse.
- **Unresolved questions:** Exact package homes are not canonical.

## P-LEG-001 — Imported legacy material is quarantined evidence unless a bounded advisory bridge is proven necessary

- **Proposition record:** `reconstruction/propositions/B02.md`
- **Canonical instruction:** Historical imported material is not native runtime authority by default. It remains quarantined as source evidence and must not be imported by native runtime or treated as native test authority. A native imported-module surface may exist only when a live dependence proves retirement false, and then only as the minimum advisory, contract or registry bridge: it cannot silently own serial runtime behaviour or recreate the historical subsystem wholesale.
- **Class and current authority state:** `bounded_amendment`; active.
- **Introduction and authority chain:** **Lineage:** `source_successor_briefs/nvda_imported_module_subsystem_disposition_tranche_v1_brief_2026-04-20.md:L9-L33`, `:L83-L96`, `:L125-L176`, `:L178-L203`.<br>**Authority effect:** Resolves a successor-era provisional subsystem boundary without importing the external workbook or current-code observations as proof. No claim is made that quarantine or bridge implementation was completed.
- **Historical aliases:** Historical imported module/package names remain evidence labels, not native authority.
- **Inputs and validity constraints:** Quarantined legacy artefacts and any proven live dependency.
- **Transformation, calculation, decision or routing semantics:** Default to quarantine; admit only the minimum advisory/contract/registry bridge when dependence proves retirement false.
- **Outputs and guarantees:** Either quarantined evidence or a bounded native bridge with explicit scope.
- **Time and state semantics:** Quarantine is the default continuing state; admission requires contemporaneous proof.
- **Null, boundary and failure behaviour:** Absent proof keeps the bridge absent; no native runtime/test authority is inferred.
- **Dependencies and downstream consequences:** Native runtime, compatibility governance and external legacy evidence.
- **Explicit exclusions and non-goals:** No wholesale subsystem recreation or serial-runtime ownership.
- **Unresolved questions:** Whether any specific bridge is required/implemented remains unresolved without external evidence.

## P-PERSIST-001 — Migration lifecycle is explicit and separate from persistence business ownership

- **Proposition record:** `reconstruction/propositions/B03.md`
- **Canonical instruction:** Schema-migration lifecycle has an explicit owner distinct from runtime persistence domains, repositories, models and sessions. A package-owned migration boundary may coexist with an external migration-tool root, but their relationship must be explicit and bounded. Migration ownership must not become an excuse to relocate execution records, market observations, positions, capital state, review state, research logs or module-registry policy.
- **Class and current authority state:** `new_design_authority`; active within the bounded successor scope.
- **Introduction and authority chain:** **Lineage:** `source_successor_briefs/nvda_persistence_migration_lifecycle_tranche_v1_brief_2026-04-20.md:L118-L136`, `:L174-L219`, `:L223-L249`.<br>**Authority effect:** The exact package path and Alembic topology are `implementation_specific_instruction`; the enduring design rule is separation of migration lifecycle from persistence business semantics.
- **Historical aliases:** Package/tool path names are implementation-specific; migration lifecycle and business persistence retain separate identities.
- **Inputs and validity constraints:** Schema migrations, external migration-tool root and persistence domain repositories/models/sessions.
- **Transformation, calculation, decision or routing semantics:** Assign explicit migration ownership and define its bounded relationship to tooling.
- **Outputs and guarantees:** A migration lifecycle boundary separate from business persistence.
- **Time and state semantics:** Migration state evolves schema; it does not own runtime records or policy state.
- **Null, boundary and failure behaviour:** Ambiguous or implicit migration ownership is invalid.
- **Dependencies and downstream consequences:** Database schema tooling and all persistence domains.
- **Explicit exclusions and non-goals:** No relocation/ownership of execution, observations, positions, capital, review, research or registry policy.
- **Unresolved questions:** Exact migration topology and package path are not canonical.

## P-REPLAY-001 — Replay/evaluation is analysis-only; specimen harnesses are test-only

- **Proposition record:** `reconstruction/propositions/B03.md`
- **Canonical instruction:** Replay/evaluation replays prepared, runtime or fixture-backed artefacts and compares outputs. It is analysis-only: it does not decode raw ingress, place live orders, mutate live core state or imply a scenario engine. Research/evaluation persistence is append-only and separate from live execution, opening-policy and market-observation persistence. A canonical specimen-path harness may assemble admitted fixtures and contracts but remains test-only and must not become a secret runtime orchestrator or require live API/broker execution.
- **Class and current authority state:** `new_design_authority`; active; complements P-TRACE-003, P-TRACE-004 and P-TRACE-005.
- **Introduction and authority chain:** **Lineage:** `source_successor_briefs/nvda_replay_evaluation_specimen_tranche_v1_brief_2026-04-20.md:L92-L104`, `:L162-L211`, `:L213-L240`, `:L242-L273`.<br>**Authority effect:** Introduces bounded replay and specimen responsibilities without admitting `analysis.scenarios` or observability.
- **Historical aliases:** Replay/evaluation and specimen harness names retain analysis/test-only meaning.
- **Inputs and validity constraints:** Prepared, runtime or fixture-backed artefacts and admitted contracts.
- **Transformation, calculation, decision or routing semantics:** Replay and compare outputs; append research/evaluation evidence; assemble test specimen paths.
- **Outputs and guarantees:** Analysis results and test-only specimen evidence.
- **Time and state semantics:** Replay is offline/analysis-only; persistence is append-only and separate from live state.
- **Null, boundary and failure behaviour:** No raw decoding, live mutation/order, secret orchestration or live API/broker requirement.
- **Dependencies and downstream consequences:** P-TRACE-003/004/005, prepared/runtime artefacts and research persistence.
- **Explicit exclusions and non-goals:** No scenario engine or live execution ownership.
- **Unresolved questions:** Replay comparison metrics and retention are not fully stated.

## P-RES-001 — Scenario and observability disposition is conditional and unresolved

- **Proposition record:** `reconstruction/propositions/B03.md`
- **Canonical instruction:** For each proposed native family, the admitted successor law allows only two truthful branches. **Bounded admission** is lawful only if a prior admissibility audit proves that a real bounded native owner already exists and admission would reflect current behaviour rather than fabricate capability. Otherwise the lawful result is **reserved / containment**: keep the native package absent and make that absence explicit through bounded proof/reporting rather than a placeholder package.
- **Class and current authority state:** `unresolved`; open conditional reservation.
- **Introduction and authority chain:** **Lineage:** conditional outcomes and default at `source_successor_briefs/nvda_provisional_scenarios_observability_resolution_tranche_v1_brief_2026-04-20.md:L24-L34`; branch rules at `source_successor_briefs/nvda_provisional_scenarios_observability_resolution_tranche_v1_brief_2026-04-20.md:L144-L186`; rerun/default qualification at `source_successor_briefs/nvda_provisional_scenarios_observability_resolution_tranche_v1_full_reset_rerun_brief_2026-04-20.md:L136-L160`; expected closeout with truth override at `source_successor_briefs/nvda_final_benchmark_reconciliation_promotion_closeout_tranche_v1_brief_2026-04-20.md:L37-L49`.<br>**Authority effect:** No unconditional scenario-engine or observability-subsystem absence is canonicalised. The unresolved proposition preserves both lawful branches and the prohibitions that apply to any later bounded admission.
- **Historical aliases:** `analysis.scenarios` and `observability` remain proposed family labels; neither branch is canonicalised.
- **Inputs and validity constraints:** External admissibility audit evidence for each proposed family.
- **Transformation, calculation, decision or routing semantics:** Select bounded admission only when a real bounded native owner is proven; otherwise select reserved/containment.
- **Outputs and guarantees:** For each family, an explicitly evidenced admission or explicit absence/containment.
- **Time and state semantics:** Decision remains unresolved until external current-code/workbook/report evidence is formally admitted.
- **Null, boundary and failure behaviour:** Absent or contradictory evidence cannot be converted into unconditional retirement or placeholder admission.
- **Dependencies and downstream consequences:** B029 conditional law, B030 rerun claims, B022 truth override and external audit surfaces.
- **Explicit exclusions and non-goals:** Scenarios: no live trading/orchestration/replay/API widening; observability: no business decisions, packet mutation, persistence policy or orchestration.
- **Unresolved questions:** Which branch applies to either family is unresolved.

## P-PROTO-003 — DMPV3 begins at the serial-runtime downstream boundary

- **Proposition record:** `reconstruction/propositions/B04.md`
- **Canonical instruction:** Raw ingress, raw-to-prepared transfer, prepared-to-cognition ingress and serial stage-to-stage flow remain native typed carriers. The first deliberate DMPV3 boundary is the serial runtime's downstream packet-carriage product. The serial runtime emits one canonical bounded set of admitted packets; this set is operational handoff authority, not merely an after-the-fact trace artefact.
- **Class and current authority state:** `explicit_replacement`; active for the serial-runtime-to-parallel-risk handoff; partially supersedes P-PROTO-002's DMP-v2 live-packet rule at this boundary.
- **Introduction and authority chain:** **Lineage:** `source_successor_briefs/serial_runtime_parallel_risk_packet_boundary_alignment_brief_2026-04-22.md:L9-L34`, `:L38-L60`, `:L85-L113`.<br>**Supersession rationale:** This is incompatible with P-PROTO-002 only at the named downstream boundary because it expressly promotes DMPV3 there. P-PROTO-002's historical v1 retirement and unaffected protocol-governance rules survive.
- **Historical aliases:** DMP v2 remains historical/upstream where unaffected; DMPV3 becomes canonical only at the named downstream boundary.
- **Inputs and validity constraints:** Native typed raw, prepared, cognition and serial-stage outputs.
- **Transformation, calculation, decision or routing semantics:** Keep native carriers upstream and emit the canonical admitted DMPV3 set at serial-runtime downstream handoff.
- **Outputs and guarantees:** Operational DMPV3 packet set for downstream/parallel-risk carriage.
- **Time and state semantics:** DMPV3 begins only after serial runtime; upstream stage flow remains native typed.
- **Null, boundary and failure behaviour:** Earlier packetisation or after-the-fact-only trace treatment is invalid.
- **Dependencies and downstream consequences:** P-PROTO-002, serial runtime and parallel-risk ingress.
- **Explicit exclusions and non-goals:** No DMPV3 at raw/prepared/cognition or serial-internal seams by this authority.
- **Unresolved questions:** Complete emitted packet set/schema is defined only partially in later propositions.

## P-PRISK-002 — Parallel risk consumes selected serial packets, never serial internals

- **Proposition record:** `reconstruction/propositions/B04.md`
- **Canonical instruction:** Parallel-risk ingress consumes the temporal packet plus selected bounded stage packets from the admitted serial packet set. It must not read serial native internals directly and must not receive one oversized everything-packet. Parallel risk remains packet-in/packet-out and emits a lawful DMPV3 packet. A deterministic proof path must preserve typed/native carriage upstream, the exact point where DMPV3 begins, lawful temporal semantics and absence of direct serial-internal reads.
- **Class and current authority state:** `bounded_amendment`; active; amends P-PRISK-001's ingress boundary while preserving its deterministic, non-mutating sibling-lane semantics.
- **Introduction and authority chain:** **Lineage:** `source_successor_briefs/serial_runtime_parallel_risk_packet_boundary_alignment_brief_2026-04-22.md:L44-L60`, `:L115-L160`, `:L177-L190`, `:L213-L228`.<br>**Authority effect:** Replaces any earlier typed seam as the admitted live parallel-risk ingress boundary, but does not authorise final-risk, capital, trade placement or broader parallel-risk stages.
- **Historical aliases:** Any earlier direct typed seam is replaced at live parallel-risk ingress by selected DMPV3 packets.
- **Inputs and validity constraints:** Temporal packet and selected bounded serial stage packets.
- **Transformation, calculation, decision or routing semantics:** Consume packet-in, evaluate without direct serial reads, and emit lawful DMPV3 packet-out.
- **Outputs and guarantees:** Deterministic parallel-risk result preserving exact boundary proof.
- **Time and state semantics:** Ingress occurs after serial packet emission; packet order/lineage are preserved.
- **Null, boundary and failure behaviour:** Oversized everything-packet or direct serial-internal read is invalid.
- **Dependencies and downstream consequences:** P-PROTO-003, P-PRISK-001 and serial packet set.
- **Explicit exclusions and non-goals:** No final-risk, capital, trade placement or broader Stage B/C authority.
- **Unresolved questions:** Exact selected packet subset and evaluation formula are not fully stated.

## P-CAP-001 — Capital deployment preserves upstream posture ownership and downstream shell separation

- **Proposition record:** `reconstruction/propositions/B06.md`
- **Canonical instruction:** Capital deployment authority is downstream of serial candidate formation and posture permission. It must not absorb posture hard-invariant ownership. Posture permission may reach capital only through bounded serial candidate material or a downstream pre-deployment result. The capital contract may carry bounded capital values, while the downstream opening-authorisation result remains a distinct shell and its fields must not be absorbed into the capital contract.
- **Class and current authority state:** `bounded_repair`; active; narrows and operationalises P-RISK-003 and P-DEC-002 without changing their ownership direction.
- **Introduction and authority chain:** **Lineage:** `source_successor_briefs/2026-04-28_DOWNSTREAM_CAPITAL_DEPLOYMENT_AUTHORITY_PILOT_TRANCHE.md:L133-L147`.<br>**Authority effect:** Clarifies the lawful handoff around capital deployment. It does not define a capital-sizing formula, sizing policy, limit model or trade-placement authority; those remain unresolved because this source expressly describes broader sizing semantics as placeholder-thin: `source_successor_briefs/2026-04-28_DOWNSTREAM_CAPITAL_DEPLOYMENT_AUTHORITY_PILOT_TRANCHE.md:L199-L205`.
- **Historical aliases:** Downstream opening-authorisation shell remains distinct from the capital contract.
- **Inputs and validity constraints:** Bounded serial candidate/pre-deployment result, posture permission and supplied capital values.
- **Transformation, calculation, decision or routing semantics:** Pass permission downstream without absorbing posture invariants; keep capital and opening-authorisation shells separate.
- **Outputs and guarantees:** Bounded capital-deployment result and distinct downstream authorisation result.
- **Time and state semantics:** Capital follows serial candidate formation and posture permission.
- **Null, boundary and failure behaviour:** Placeholder-thin sizing semantics cannot be treated as complete authority.
- **Dependencies and downstream consequences:** P-RISK-003, P-DEC-002, serial candidate material and downstream authorisation.
- **Explicit exclusions and non-goals:** No posture ownership, sizing formula, limit model or trade placement.
- **Unresolved questions:** Sizing policy was unresolved here and is only boundedly amended by P-CAP-002.

## P-CAP-002 — Authorised notional is bounded by supplied capital state and the tighter deployment percentage

- **Proposition record:** `reconstruction/propositions/B07.md`
- **Canonical instruction:** Capital deployment requires explicit supplied capital state and bounded policy inputs. Authorised notional is computed from `available_capital_usd` using the lesser of `requested_deployable_pct` and `max_deployable_pct`; a hard-coded notional base is not authoritative. In algebraic form, subject to the percentage representation admitted by the consuming contract: `authorised_notional = available_capital_usd × min(requested_deployable_pct, max_deployable_pct)`.
- **Class and current authority state:** `bounded_amendment`; active; extends P-CAP-001 and resolves only the previously open bounded sizing rule.
- **Introduction and authority chain:** **Lineage:** `source_successor_briefs/2026-04-28_CAPITAL_DEPLOYMENT_AUTHORITY_PROOF_HARDENING_TRANCHE.md:L20-L35`.<br>**Authority effect:** Replaces placeholder/hard-coded-base sizing at this bounded capital-authority seam. It does not define percentage units or range, missing/invalid-input behaviour, portfolio aggregation, instrument limits, exposure netting, concentration policy, liquidity policy, final trade quantity or broker placement; those remain unresolved.
- **Historical aliases:** Hard-coded notional-base behaviour is replaced.
- **Inputs and validity constraints:** `available_capital_usd`, `requested_deployable_pct` and `max_deployable_pct` under an admitted percentage representation.
- **Transformation, calculation, decision or routing semantics:** Compute `available_capital_usd × min(requested_deployable_pct, max_deployable_pct)`.
- **Outputs and guarantees:** Bounded authorised notional no greater than the tighter deployment percentage.
- **Time and state semantics:** Calculation occurs at downstream capital-deployment authority for supplied current capital state.
- **Null, boundary and failure behaviour:** Percentage units/ranges and missing/invalid input behaviour are unresolved; no hard-coded base may substitute.
- **Dependencies and downstream consequences:** P-CAP-001 and supplied capital/policy contracts.
- **Explicit exclusions and non-goals:** No portfolio aggregation, limits, netting, concentration, liquidity, final quantity or broker placement.
- **Unresolved questions:** Percentage representation, validation and all broader sizing policies remain unresolved.

## P-TMP-005 — One provider-agnostic source temporal grammar governs observation, capture and persistence truth

- **Proposition record:** `reconstruction/propositions/B08.md`
- **Canonical instruction:** Source-facing and persisted temporal truth uses one architecture-level grammar containing, where applicable, `source_time_raw`, `source_time_kind`, `source_timezone_raw`, `source_time_utc`, `source_date`, `captured_at_utc`, `persisted_at_utc`, `source_provider`, `source_channel` and `time_granularity`. The grammar applies to raw captures, local capture files, derived raw surfaces, persistence records, workbook-derived specimens, replay/proof surfaces and packets where relevant. It is provider-agnostic and must represent timestamp-level, date-level and mixed-date reference-ledger sources without overfitting one provider.
- **Class and current authority state:** `new_design_authority`; active above packet-carriage protocols; extends P-TMP-001 through P-TMP-004 without replacing their market-phase and threshold semantics.
- **Introduction and authority chain:** **Lineage:** `source_successor_briefs/temporal_standard_tranche_1_normative_admission_brief_v2.md:L226-L250`, `:L266-L287`; `source_successor_briefs/temporal_standard_tranche_3_code_persistence_remediation_brief.md:L314-L357`.
- **Historical aliases:** Legacy local temporal grammars are non-authoritative; the ten named fields are canonical where applicable.
- **Inputs and validity constraints:** Source artefact time token/date/timezone/provider/channel plus repository capture/persistence events.
- **Transformation, calculation, decision or routing semantics:** Represent distinct observation, capture, persistence and packet facts using one provider-agnostic grammar.
- **Outputs and guarantees:** Temporal metadata preserving raw token, kind, timezone, UTC/date, provider/channel and granularity.
- **Time and state semantics:** Source observation, capture and persistence times remain distinct; timestamp/date/mixed-date sources are supported.
- **Null, boundary and failure behaviour:** No invented precision, false UTC normalisation or divergent module-local grammar.
- **Dependencies and downstream consequences:** Raw capture, persistence, workbook specimen, replay/proof and packet surfaces.
- **Explicit exclusions and non-goals:** No provider-specific overfitting and no collapse of distinct temporal facts.
- **Unresolved questions:** Allowed values, ranges and null rules for several fields remain unresolved.

## P-PROTO-004 — DMPV3 packet time is emission time, not source observation time

- **Proposition record:** `reconstruction/propositions/B08.md`
- **Canonical instruction:** `packet.time` records packet emission time. Source observation time may differ and must be preserved separately where relevant under P-TMP-005. DMPV3 inherits rather than redefines the upstream source temporal grammar, and must not manufacture source precision that did not exist.
- **Class and current authority state:** `bounded_amendment`; active; amends P-PROTO-003's packet-carriage semantics without changing the boundary where DMPV3 begins.
- **Introduction and authority chain:** **Lineage:** `source_successor_briefs/temporal_standard_tranche_1_normative_admission_brief_v2.md:L252-L264`; `source_successor_briefs/temporal_standard_tranche_3_code_persistence_remediation_brief.md:L327-L337`, `:L348-L357`.<br>**Authority effect:** Explicitly disallows overloaded packet-emission fields as substitutes for source-observation truth.
- **Historical aliases:** Overloaded `packet.time` as source observation time is retired.
- **Inputs and validity constraints:** Packet emission event and separately carried source temporal metadata.
- **Transformation, calculation, decision or routing semantics:** Set `packet.time` to emission time and inherit upstream source temporal truth separately.
- **Outputs and guarantees:** DMPV3 packet with truthful emission timestamp and non-overloaded source timing.
- **Time and state semantics:** Emission time may differ from source observation time.
- **Null, boundary and failure behaviour:** Missing source precision stays missing; packet time cannot substitute.
- **Dependencies and downstream consequences:** P-PROTO-003 and P-TMP-005.
- **Explicit exclusions and non-goals:** No source-time redefinition inside DMPV3.
- **Unresolved questions:** Packet-time precision/clock source is not fully specified.

## P-TMP-006 — Workbook-derived temporal truth is field-level provenance, not a synthetic same-moment observation

- **Proposition record:** `reconstruction/propositions/B08.md`
- **Canonical instruction:** Workbook dates are reference-ledger provenance. One anchor row may blend fields carrying different source dates. Workbook-derived specimens and promotions must preserve field-level provenance wherever dates differ, retain `source_date` as the lawful date-level observation where applicable, and must not masquerade as a same-moment live runtime capture. The workbook remains a governed reference ledger, not direct runtime authority.
- **Class and current authority state:** `clarification`; active; clarifies P-DAT-004, P-TRACE-001 and P-TRACE-003 for workbook-derived evidence.
- **Introduction and authority chain:** **Lineage:** `source_successor_briefs/temporal_standard_tranche_1_normative_admission_brief_v2.md:L277-L287`; `source_successor_briefs/temporal_standard_tranche_3_supplementary_brief_raw_truth_and_specimen_regeneration.md:L163-L170`.
- **Historical aliases:** Anchor row and field-level source dates retain separate identities.
- **Inputs and validity constraints:** Workbook anchor row plus per-field source dates/provenance.
- **Transformation, calculation, decision or routing semantics:** Map each field with its own lawful date-level provenance where dates differ.
- **Outputs and guarantees:** Workbook-derived specimen with field-level temporal lineage.
- **Time and state semantics:** Mixed-date fields remain mixed; anchor date is not a synthetic observation instant.
- **Null, boundary and failure behaviour:** Missing time precision must not be fabricated into UTC.
- **Dependencies and downstream consequences:** P-TMP-005, workbook reference ledger and specimen promotion.
- **Explicit exclusions and non-goals:** No direct runtime authority or same-moment live-capture claim.
- **Unresolved questions:** Workbook-specific field mapping is external to this proposition.

## P-TMP-007 — `source_time_raw` preserves the exact source token or remains null

- **Proposition record:** `reconstruction/propositions/B08.md`
- **Canonical instruction:** `source_time_raw` is the exact source-supplied time token captured from the source artefact. It must not be generated from `source_time_utc` or `source_date`. When the exact token is carried, preserve it explicitly; when it is not available on the surface, use `None`/`null` rather than fabricating a convenient normalised value. Workbook promotion follows the same rule.
- **Class and current authority state:** `bounded_repair`; active; repairs any normalised-value substitution permitted by a thin reading of P-TMP-005.
- **Introduction and authority chain:** **Lineage:** `source_successor_briefs/temporal_standard_tranche_3_supplementary_brief_raw_truth_and_specimen_regeneration.md:L37-L75`, `:L147-L170`.
- **Historical aliases:** `source_time_raw` has exact-token semantics; normalised substitutions are rejected.
- **Inputs and validity constraints:** Exact source-supplied time token, when present.
- **Transformation, calculation, decision or routing semantics:** Copy token exactly; otherwise write null.
- **Outputs and guarantees:** Exact raw temporal provenance or explicit absence.
- **Time and state semantics:** Value is capture provenance, not derived from UTC/date.
- **Null, boundary and failure behaviour:** Never generate from normalised fields; unavailable token remains null.
- **Dependencies and downstream consequences:** P-TMP-005 and workbook/raw promotion paths.
- **Explicit exclusions and non-goals:** No guessed or convenient normalised replacement.
- **Unresolved questions:** Token format validation is not specified.

## P-TMP-008 — Canonical temporal convergence replaces legacy aliases at admitted seams

- **Proposition record:** `reconstruction/propositions/B08.md`
- **Canonical instruction:** The active preparation/raw-bundle seam uses only the admitted canonical temporal grammar. Its internal `observed_at` field and any read of `bundle.provenance.observed_at` are retired. No alias, compatibility property, hidden fallback or dual grammar may retain that field. Workbook-derived Module 8 specimen carriage likewise retires `observed_at` and `next_event_at`; regenerated artefacts must use the canonical grammar. Other local names such as `starts_at`, `ends_at`, `recorded_at` or overloaded `emitted_at` are replaced only where they represented one of the canonical temporal facts on an admitted remediated surface; this source does not establish a repo-wide lexical ban outside those scopes.
- **Class and current authority state:** `explicit_replacement`; active at the named remediated surfaces.
- **Introduction and authority chain:** **Lineage:** `source_successor_briefs/temporal_standard_tranche_3_supplementary_brief_raw_truth_and_specimen_regeneration.md:L172-L198`; `source_successor_briefs/temporal_standard_tranche_3_supplementary_preparation_raw_bundle_remediation_brief.md:L75-L100`, `:L212-L265`.<br>**Supersession rationale:** This is convergence, not compatibility coexistence. It replaces the legacy seam grammar but does not erase historical evidence containing old field names.
- **Historical aliases:** `observed_at` and `next_event_at` are retired at named seams; other legacy names are replaced only when semantically equivalent there.
- **Inputs and validity constraints:** Active preparation/raw-bundle and Module 8 workbook-specimen temporal surfaces.
- **Transformation, calculation, decision or routing semantics:** Remove aliases/fallbacks/dual grammar and regenerate artefacts using P-TMP-005.
- **Outputs and guarantees:** Canonical-only temporal seam and regenerated specimens.
- **Time and state semantics:** Replacement applies at named remediated surfaces; historical evidence remains intact.
- **Null, boundary and failure behaviour:** Any alias, hidden fallback or dual grammar at those seams is failure.
- **Dependencies and downstream consequences:** P-TMP-005/007, preparation/raw bundle and Module 8 specimen carriage.
- **Explicit exclusions and non-goals:** No repo-wide lexical ban outside equivalent admitted scopes.
- **Unresolved questions:** Other seam migrations require separate evidence.

## P-PERSIST-002 — Parallel-risk observation persistence is append/write-only to live runtime

- **Proposition record:** `reconstruction/propositions/B08.md`
- **Canonical instruction:** The parallel-risk observation store records observations without becoming a live-runtime read authority. The remediated store remains write-only from the live runtime's perspective in this bounded design; persistence must not feed hidden state back into the parallel lane or serial spine.
- **Class and current authority state:** `clarification`; active; extends P-PRISK-001 and P-PERSIST-001.
- **Introduction and authority chain:** **Lineage:** `source_successor_briefs/temporal_standard_tranche_3_code_persistence_remediation_brief.md:L327-L357`, `:L464-L478`.
- **Historical aliases:** No historical aliases are stated.
- **Inputs and validity constraints:** Parallel-risk observation records emitted by the live lane.
- **Transformation, calculation, decision or routing semantics:** Append/write observations without exposing a live reader.
- **Outputs and guarantees:** Persistent audit evidence unavailable as live decision input.
- **Time and state semantics:** Writes occur downstream/side-lane; serial and parallel runtime remain stateless with respect to stored history.
- **Null, boundary and failure behaviour:** Read-back or hidden feedback into runtime is invalid.
- **Dependencies and downstream consequences:** P-PRISK-001, P-PERSIST-001 and observation store.
- **Explicit exclusions and non-goals:** No live analytics/read authority.
- **Unresolved questions:** Retention, schema and offline-reader policy are not stated here.

## P-ARCH-008 — The serial cognitive spine remains stateless

- **Proposition record:** `reconstruction/propositions/B08.md`
- **Canonical instruction:** Temporal remediation must not introduce hidden state into the serial spine. State, persistence and observation history remain explicit downstream or side-lane concerns rather than implicit serial-stage memory.
- **Class and current authority state:** `clarification`; active; extends P-ARCH-001, P-ARCH-006 and P-PROTO-003.
- **Introduction and authority chain:** **Lineage:** `source_successor_briefs/temporal_standard_tranche_3_code_persistence_remediation_brief.md:L314-L357`, `:L464-L478`.
- **Historical aliases:** No historical aliases are stated.
- **Inputs and validity constraints:** Explicit current stage inputs only.
- **Transformation, calculation, decision or routing semantics:** Execute serial cognition without retaining hidden state or observation history.
- **Outputs and guarantees:** Stateless ordered stage outputs.
- **Time and state semantics:** State/history lives only in explicit downstream or sibling concerns.
- **Null, boundary and failure behaviour:** Implicit memory or persistence feedback is invalid.
- **Dependencies and downstream consequences:** P-ARCH-001/006, P-PROTO-003 and persistence boundaries.
- **Explicit exclusions and non-goals:** No hidden serial-stage memory.
- **Unresolved questions:** Explicit cache policy, if any, is not stated.

## P-ARCH-009 — Cognition ingress owns deterministic prepared-substrate translation into explicit typed stage inputs

- **Proposition record:** `reconstruction/propositions/B09.md`
- **Canonical instruction:** Cognition ingress, not the serial runtime, owns translation from the prepared runtime substrate into a typed bundle of stage inputs. It uses separate deterministic temporal, regime and options/flow mappers plus a thin coordinator; calculations remain in the mapper functions. Each stage input is explicit, lawful absence is represented as absence rather than wall-clock or zero-certainty fabrication, and regime incompleteness remains explicit and typed. The serial runtime consumes the admitted bundle and must not reach into preparation internals.
- **Class and current authority state:** `bounded_repair`; active; strengthens P-ARCH-001 and P-ARCH-007 at the preparation-to-cognition boundary.
- **Introduction and authority chain:** **Lineage:** `source_successor_briefs/module_4_cognition_ingress_implementation_brief_v2.md:L11-L17`, `:L115-L132`, `:L134-L198`, `:L200-L227`, `:L240-L260`.
- **Historical aliases:** No supportive fixture may become a silent alias for the native ingress path.
- **Inputs and validity constraints:** Prepared runtime substrate with temporal, regime and options/flow information, including lawful absence.
- **Transformation, calculation, decision or routing semantics:** Separate deterministic mappers calculate typed stage inputs; a thin coordinator assembles the bundle.
- **Outputs and guarantees:** Explicit cognition-ingress bundle consumed by serial runtime.
- **Time and state semantics:** Translation occurs once at preparation-to-cognition boundary; serial remains stateless.
- **Null, boundary and failure behaviour:** Absent values remain absent; no wall-clock or zero-certainty fabrication.
- **Dependencies and downstream consequences:** P-ARCH-007, preparation, typed stage contracts and P-SERIAL-001.
- **Explicit exclusions and non-goals:** No calculations in coordinator and no serial reach into preparation internals.
- **Unresolved questions:** Final regime-source completeness ownership remains unresolved under P-ARCH-010.

## P-ARCH-010 — Final ownership of regime-ingress completeness remains unresolved

- **Proposition record:** `reconstruction/propositions/B09.md`
- **Canonical instruction:** The prepared-substrate-to-regime-input seam must represent partial regime information explicitly, but this tranche does not settle whether preparation or cognition ingress finally owns regime-source completeness. Supportive fixtures must not silently replace the native path.
- **Class and current authority state:** `unresolved`; open reservation.
- **Introduction and authority chain:** **Lineage:** `source_successor_briefs/module_4_cognition_ingress_implementation_brief_v2.md:L193-L198`, `:L223-L227`, `:L256-L259`, `:L276-L290`.
- **Historical aliases:** Supportive fixtures are non-authoritative substitutes.
- **Inputs and validity constraints:** Partial prepared regime information and candidate source-completeness evidence.
- **Transformation, calculation, decision or routing semantics:** Represent partiality explicitly while deferring owner selection.
- **Outputs and guarantees:** Typed partial regime input plus an unresolved ownership reservation.
- **Time and state semantics:** Reservation persists until admitted evidence assigns completeness ownership.
- **Null, boundary and failure behaviour:** No silent fixture substitution or fabricated completeness.
- **Dependencies and downstream consequences:** P-ARCH-009, preparation and cognition ingress.
- **Explicit exclusions and non-goals:** No final owner inferred from this tranche.
- **Unresolved questions:** Whether preparation or cognition ingress owns regime completeness is unresolved.

## P-SERIAL-001 — The serial spine preserves six ordered, bounded and inspectable stage answers

- **Proposition record:** `reconstruction/propositions/B09.md`
- **Canonical instruction:** The serial stage order is: (1) temporal, (2) market regime, (3) options and flow, (4) posture and risk permission, (5) playbook eligibility, and (6) expression and execution. Each stage owns only its bounded answer and exposes a lawful typed, inspectable output. The stages must not be collapsed into one opaque blob, the serial spine remains stateless, and parallel risk, final risk, capital or downstream operations must not absorb serial meaning for convenience.
- **Class and current authority state:** `clarification`; active; extends P-ARCH-001, P-PLAY-006, P-DEC-002 and P-ARCH-008.
- **Introduction and authority chain:** **Lineage:** `source_successor_briefs/module_6_serial_spine_implementation_brief_v3.md:L52-L62`, `:L161-L173`, `:L230-L245`, `:L258-L275`.
- **Historical aliases:** The six numbered stage identities are canonical serial ordering.
- **Inputs and validity constraints:** Typed cognition-ingress bundle and each preceding stage output.
- **Transformation, calculation, decision or routing semantics:** Run temporal → regime → options/flow → posture/permission → eligibility → expression/execution, each with bounded ownership.
- **Outputs and guarantees:** Six inspectable typed stage answers.
- **Time and state semantics:** Order is fixed and stateless within each run.
- **Null, boundary and failure behaviour:** Opaque collapse, hidden state or ownership absorption is invalid.
- **Dependencies and downstream consequences:** P-ARCH-001/008/009, P-PLAY-006 and P-DEC-002.
- **Explicit exclusions and non-goals:** No parallel risk, final risk, capital or downstream semantics inside serial stages.
- **Unresolved questions:** Exact stage schemas/calculations are not fully restated.

## P-PROTO-005 — Serial stage packets are emitted only from lawful owned outputs

- **Proposition record:** `reconstruction/propositions/B09.md`
- **Canonical instruction:** DMPV3 stage-packet emission preserves serial stage order, dependencies and trace/run/scenario/lineage identity. A stage may be packetised only when its lawful typed output already exists and owns the emitted fields. If packetisation would require invented output fields, temporary convenience contracts, widened Module 8 Stage B/C logic, or widened final-risk/capital/downstream consumers, that emitter remains conditional or reserved rather than being faked.
- **Class and current authority state:** `bounded_amendment`; active; strengthens P-PROTO-003 and P-PROTO-004.
- **Introduction and authority chain:** **Lineage:** `source_successor_briefs/module_6_serial_spine_implementation_brief_v3.md:L201-L227`, `:L247-L275`, `:L373-L390`.<br>**Authority effect:** Packet-carriage completeness is subordinate to truthful stage ownership; a missing lawful stage output is an explicit reservation, not permission to invent an interim contract.
- **Historical aliases:** No convenience/interim packet contract is canonical.
- **Inputs and validity constraints:** Lawful typed stage output, dependencies and trace/run/scenario/lineage identity.
- **Transformation, calculation, decision or routing semantics:** Packetise only fields owned by the stage and preserve serial order/dependencies.
- **Outputs and guarantees:** Truthful DMPV3 stage packet or an explicit conditional/reserved emitter.
- **Time and state semantics:** Emission occurs only after lawful stage output exists.
- **Null, boundary and failure behaviour:** Missing outputs cannot be invented to achieve packet completeness.
- **Dependencies and downstream consequences:** P-PROTO-003/004, P-SERIAL-001 and stage contracts.
- **Explicit exclusions and non-goals:** No widened Module 8 Stage B/C, final risk, capital or downstream consumer by implication.
- **Unresolved questions:** Which optional emitters are ultimately admitted remains conditional on owned outputs.

## P-PROTO-006 — Live DMPV3 carriage has one canonical outer-envelope and builder truth

- **Proposition record:** `reconstruction/propositions/B10.md`
- **Canonical instruction:** Live inter-surface DMPV3 carriage uses one canonical outer-envelope grammar and repo-owned builder path. The shell carries truthful producer identity, explicit packet role and behaviour-class interpretation, bounded lineage, validation state, a human-facing summary and bounded extension data. Packet carriage owns transport grammar, not stage business meaning or stage ownership. Builders must be deterministic and stable; no touched live output may use a competing bespoke outer-packet grammar.
- **Class and current authority state:** `clarification`; active; extends P-PROTO-003 through P-PROTO-005 and P-ARCH-005.
- **Introduction and authority chain:** **Lineage:** `source_successor_briefs/module_7_dmpv3_packet_carriage_implementation_brief_v1.md:L92-L113`, `:L115-L167`, `:L193-L210`, `:L260-L310`.
- **Historical aliases:** Competing bespoke outer grammars are retired; any wrapper is labelled compatibility and delegates.
- **Inputs and validity constraints:** Lawful stage/business output plus producer, role, behaviour class, lineage, validation, summary and extension data.
- **Transformation, calculation, decision or routing semantics:** Build deterministically through one repo-owned canonical envelope builder.
- **Outputs and guarantees:** Stable DMPV3 outer envelope with truthful identity and bounded extensions.
- **Time and state semantics:** Builder output is deterministic per input; compatibility has no independent lifecycle authority.
- **Null, boundary and failure behaviour:** Invalid envelope/producer/lineage must fail validation; no second source of truth.
- **Dependencies and downstream consequences:** P-PROTO-003/004/005 and stage owners.
- **Explicit exclusions and non-goals:** Packet carriage does not own business meaning.
- **Unresolved questions:** Complete mandatory schema, validation and extension contents remain unresolved.

## P-PRISK-003 — Parallel-risk Stage A is a bounded DMPV3 bootstrap/evaluate lane

- **Proposition record:** `reconstruction/propositions/B10.md`
- **Canonical instruction:** Parallel risk has a mandatory Stage A path that receives one lawful bootstrap DMPV3 input packet and emits one lawful bootstrap parallel-risk DMPV3 output packet. It preserves invariant reads, stage-read state, dependency packet identity and trace/run/scenario/lineage identity. Its bounded answer is the independent lane's conclusion about the present environment; it does not become serial candidate formation, fresh-capital decision, final risk, downstream management, exit or close logic.
- **Class and current authority state:** `bounded_amendment`; active; extends P-PRISK-001 and P-PRISK-002 without authorising final-risk consumption.
- **Introduction and authority chain:** **Lineage:** `source_successor_briefs/module_8_parallel_risk_lane_implementation_brief_v2.md:L54-L68`, `:L222-L296`, `:L300-L316`.
- **Historical aliases:** Stage A, bootstrap input/output and bootstrap adapter labels are canonical; Stages B/C remain reservations.
- **Inputs and validity constraints:** Existing lawful upstream DMPV3 packet, or already-admitted truth wrapped by a bounded lane-owned adapter.
- **Transformation, calculation, decision or routing semantics:** Read invariants/stage state, evaluate current environment and emit one parallel-risk DMPV3 packet.
- **Outputs and guarantees:** Stage-A output preserving dependency packet and trace/run/scenario/lineage identity.
- **Time and state semantics:** Stage A is mandatory; B/C are conditional follow-ons only after lawful inputs exist.
- **Null, boundary and failure behaviour:** No upstream packet may be fabricated; absent B/C inputs keep those stages reserved.
- **Dependencies and downstream consequences:** P-PRISK-001/002, P-PROTO-006 and append-only persistence.
- **Explicit exclusions and non-goals:** No serial candidate formation, capital, final risk, management, exit or close logic.
- **Unresolved questions:** Stage B/C admission and exact Stage-A calculation remain unresolved.

## P-PERSIST-003 — Parallel-risk observations are append-only audit records with bounded packet lineage

- **Proposition record:** `reconstruction/propositions/B10.md`
- **Canonical instruction:** The parallel-risk-owned persistence seam appends receiptable observation records containing only admitted input packet IDs, emitted output packet IDs, a bounded observation payload, timestamps, trace/run/scenario IDs and lineage references required for later audit. It exposes no live readers, analytical readers, analytics tables or live read-back path. It must not become a shared hidden-state store.
- **Class and current authority state:** `bounded_amendment`; active; makes P-PERSIST-002's write-only boundary concrete.
- **Introduction and authority chain:** **Lineage:** `source_successor_briefs/module_8_parallel_risk_lane_implementation_brief_v2.md:L247-L280`, `:L317-L335`, `:L456-L479`.<br>**Authority effect:** This admits persistence for evidence and later analysis, not analytics or runtime feedback.
- **Historical aliases:** No historical aliases are stated.
- **Inputs and validity constraints:** Admitted input/output packet IDs, bounded observation payload, timestamps and trace/run/scenario/lineage IDs.
- **Transformation, calculation, decision or routing semantics:** Append one receiptable parallel-risk observation record.
- **Outputs and guarantees:** Append-only audit record suitable for later analysis.
- **Time and state semantics:** Persistence follows lane evaluation; no live read-back state exists.
- **Null, boundary and failure behaviour:** Readers, analytics tables or shared hidden state are prohibited.
- **Dependencies and downstream consequences:** P-PERSIST-002, P-PRISK-003 and DMPV3 lineage.
- **Explicit exclusions and non-goals:** No live analytics or runtime feedback.
- **Unresolved questions:** Retention, offline querying and schema evolution are not stated.

## P-TRACE-007 — Governed-workbook packet specimens are explicit, lineaged reference promotions through the native path

- **Proposition record:** `reconstruction/propositions/B10.md`
- **Canonical instruction:** A workbook-derived packet specimen is a bounded reference-ledger promotion, never a live admitted raw bundle or direct runtime authority. The mapping uses only lawfully supported typed-contract fields, keeps missing truth explicit, records exact workbook origin at field/row/cell level, and carries that origin through lawful packet lineage or bounded extension metadata plus a specimen receipt. It emits the bootstrap input packet, Stage A output packet and append-only observation record through the existing native builder/service path rather than hand-written JSON or a parallel packet path.
- **Class and current authority state:** `clarification`; active; extends P-TMP-006, P-TRACE-001, P-TRACE-003 and P-TRACE-004.
- **Introduction and authority chain:** **Lineage:** `source_successor_briefs/module_8_parallel_risk_lane_supplementary_brief_authoritative_closeout_and_packet_specimen.md:L46-L64`, `:L106-L143`, `:L160-L182`, `:L203-L249`; `source_successor_briefs/module_8_recovery_and_closeout_brief_from_paused_state.md:L91-L129`, `:L194-L245`.
- **Historical aliases:** `observed_at`/`next_event_at` specimen examples are superseded; workbook origin remains explicit.
- **Inputs and validity constraints:** Governed workbook fields/rows/cells, lawful typed-contract mappings and native packet/service path.
- **Transformation, calculation, decision or routing semantics:** Promote as reference-ledger evidence, preserve field-level provenance, emit input/output packets and append-only observation through native builders.
- **Outputs and guarantees:** Lineaged packet specimen and receipt, not a live raw bundle.
- **Time and state semantics:** Anchor-row and field source dates remain distinct; mixed dates are preserved.
- **Null, boundary and failure behaviour:** Unsupported fields remain absent; no fake UTC, hand-written JSON or parallel packet path.
- **Dependencies and downstream consequences:** P-TMP-006/007/008, P-TRACE-001/003/004, P-PROTO-006 and P-PRISK-003.
- **Explicit exclusions and non-goals:** No direct runtime authority or bespoke specimen execution path.
- **Unresolved questions:** Exact workbook mapping and complete extension schema remain external/unresolved.
