# Governance, Coefficients, Compatibility and Public Boundaries

## Authority propositions

`P-GOV-001`, `P-GOV-002`, `P-GOV-003`, `P-GOV-004`, `P-GOV-005`, `P-GOV-006`, `P-ARCH-005`, `P-API-001`.

Exact lineage is retained in [`../propositions/A05.md`](../propositions/A05.md), [`../propositions/A06.md`](../propositions/A06.md), [`../propositions/A07.md`](../propositions/A07.md), [`../propositions/A10.md`](../propositions/A10.md), [`../propositions/A11.md`](../propositions/A11.md), [`../propositions/A15.md`](../propositions/A15.md) and [`../propositions/B02.md`](../propositions/B02.md).

## 1. Canonical vocabulary

Canonical vocabulary is generated from governed contract surfaces, not imported blindly from a stale snapshot. It owns aliases, duplicate-label resolution and contract linkage. Its schema includes:

- family;
- setup variant;
- execution expression;
- horizon;
- raw/derived classification;
- stage owner;
- contract linkage.

It also explicitly owns Step-0 calendar/horizon routing, candidate-family generation, generic playbook hierarchy terms, carry handoff and carry-horizon branches.

Enforcement rejects conflicting duplicate labels, undefined aliases and governed runtime surfaces without canonical entries. Vocabulary is not a free-form glossary and does not redesign the runtime.

## 2. Approved mutable runtime surfaces

The admitted mutable runtime surfaces are exactly:

- `entry_gate_score_floor`;
- `zone_score_threshold`;
- `distance_to_vwap_soft_limit_pct`;
- `risk_vix_caution_threshold`;
- `risk_vix_hot_threshold`;
- `max_risk_per_trade`;
- `target_fresh_deployable_pct`;
- `hedge_required`.

Execution truth and review expose the operative values. Consumers cannot depend on implied or hidden policy state.

## 3. Coefficient authority

The admitted coefficient universe records, for each entry:

- owning stage;
- units;
- baseline;
- minimum and maximum envelope;
- transform family;
- allowed upstream drivers;
- authority version and lineage.

The scope separates eight mutable runtime surfaces, sixteen behavioural temporal thresholds and two timing parameters. Timing parameters cannot masquerade as alpha coefficients. The corpus does not contain the full identifier/value table for the sixteen-plus-two subset; that external detail remains unresolved.

Unknown surfaces, absurd ranges and illegal transform families fail validation. The legacy example registry remains reference-only.

Runtime services load baselines, floors and caps from governed authority rather than private constants. Resolved values carry owner, authority version, baseline reference and numeric envelope. The governed universe cannot widen by drift.

## 4. Compatibility law

Compatibility survives until an explicit retirement or replacement names the affected seam. A compatibility field, wrapper or flat representation must be labelled, bounded and delegated to the current authority. It cannot become a second source of truth.

The historical stage-local seam work remains evidence. Corrective authority must repair field-level ownership, transitive consumer handling and overstated claims without rewriting history.

The corpus references Gates 151–156 but does not contain them. Their proposed subjects—field ownership, Stage-5/6 authority, overlay/terminal authority, downstream consumers, consequence routing and anti-drift closeout—are not imported as completed design.

## 5. Public API and broker boundaries

Public output crosses an explicit DTO projection boundary, either through a dedicated egress adapter or deliberately narrow route-local projection. The choice must be explicit. Projection cannot depend on arbitrary internal dictionary shape or bleed into orchestration.

The broker boundary is protocol/interface-only unless later authority admits more. Structural closure cannot invent a live adapter, network calls, credentials, external execution or placement behaviour.
