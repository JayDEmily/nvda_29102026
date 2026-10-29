# N15 — Product and protocol proof

## Status and semantic owner

- Status: **CURRENT NORMATIVE AUTHORITY after PB-15 acceptance/commit**.
- Record ID: `N15_PRODUCT_PROOF`.
- Semantic owner: the bounded product/protocol proof-contract authority.
- N15 governs how a current product/protocol implementation claim is bound to proof. It does not own the product meaning being tested, implementation allocation, architecture/bootstrap proof admission or operational commissioning.

## Normative propositions

### N15-P01 — Product proof is downstream, exact and claim-limited

Proof is derived from already-admitted current product/protocol propositions. A test, manifest, registry row, command, receipt, file location, historical green result or passing aggregate cannot create product meaning, semantic ownership, implementation status, packet authority, operational readiness or adjacent behaviour.

Every material proof claim must name the exact current proposition IDs and the exact implementation/boundary claim exercised. Green proof establishes no more than the assertions and path actually exercised under the recorded environment, inputs, dependencies, state and versions.

### N15-P02 — A current product blocking set exists only for an activated implementation/promotion claim

N15 proof obligations are current normative requirements, but a physical proof family becomes a current blocker only when current implementation/promotion authority asserts conformance to the product proposition(s) that family proves.

For each such claim, the admitted blocking set must be derived from the exact proposition/boundary claim. Historical test existence, historical Tier-A/Tier-C status, path location, a familiar M/K identifier or this N15 record alone cannot activate a physical blocker.

At PB-15 there is no admitted current product runtime module/allocation and no current product test-family population. Therefore the current physical product blocker population in this reconciliation repository is empty. This is an implementation-state fact, not a waiver of the proof obligations below.

### N15-P03 — Every activated blocking family has exact proposition, boundary and proof-level traceability

Every activated blocking proof family must identify:

1. exact current proposition ID(s), never only a whole document;
2. the implementation target/version/identity under current implementation authority;
3. the exact boundary exercised;
4. the proof level required by that boundary;
5. authoritative inputs/fixtures/state and any dependency substitutions;
6. positive, prohibited/false-positive, missing-authority and lawful-absence cases applicable to the cited proposition;
7. expected failure signal;
8. declared environment and exact command;
9. result-changing policy/configuration/executable versions materially used; and
10. limitations and adjacent claims not proved.

One proof family may cite several propositions only where its assertions genuinely exercise each cited proposition. One proposition may require several families where its claim crosses multiple boundaries.

### N15-P04 — Proof level must match the claimed semantic boundary

The smallest adequate combination is selected from the claim actually made:

- deterministic/component proof for bounded algorithms and invariants;
- contract proof for typed contracts and producer/consumer expectations;
- integration proof across real semantic-owner boundaries;
- state proof for versioning, duplicate/conflict, mutation, readback and restart only where those properties are claimed;
- sequential/end-to-end proof when the claim spans the governed cross-owner lifecycle; and
- N14-compatible replay proof when authoritative replay/re-execution is claimed.

A passing lower-level slice cannot substitute for a missing contract, integration, state, restart, end-to-end or replay boundary that is part of the claim. Counts, coverage, import success, schema construction, file presence or registration alone are not semantic proof.

### N15-P05 — Negative, degraded, identity and guardrail cases are first-class proof

For every activated product proposition, proof must exercise the owner-specific negative/fail-closed/degraded/unknown/withheld/rejected/pending/unresolved cases that are material to that proposition, plus identity/lineage preservation, lawful optional absence, deterministic equivalence and substitution/extension behaviour where the proposition claims them.

Where N06 protects the implemented proposition, the applicable `N06-Gxx` guardrail is a negative-proof overlay. The proof must cite both the guardrail and the exact protected proposition(s) actually exercised. N06 does not create a new product behaviour or permit one generic failure outcome to replace owner-specific law.

### N15-P06 — Proof execution is attributable, reproducible and isolated

An activated product proof claim must identify the declared execution environment, exact command(s), relevant implementation and authority-file versions, inputs/fixtures/dependency substitutions and pre/post governed repository state.

A read-only proof command must not mutate governed source, normative authority, configuration, fixtures, canonical product data, owner state or proof authority. Any lawful generation/mutation workflow requires separate explicit authority and a separately inspectable intended diff before checking. Unexpected governed mutation invalidates the proof claim even when assertions pass.

### N15-P07 — Aggregate promotion proof is complete for the exact claim and cannot escalate status

For any product promotion claim, one authoritative aggregate procedure must resolve and execute every currently admitted blocking family activated by that exact claim and fail closed on missing, red, skipped-without-authority, collection-failed or unreconciled proof.

The aggregate must preserve exact family/proposition/boundary membership and enough evidence to reproduce what ran. Targeted development slices are not aggregate promotion evidence unless current proof authority explicitly defines them as the complete set for that claim.

Green product proof supports only the bounded conformance/status decision separately authorised by current implementation/promotion authority. It does not by itself promote a placeholder/reserved/future surface to implemented, commission live trading, prove production fitness, create durability, activate a packet profile or allocate architecture identity.

### N15-P08 — Stateful, durable and external-effect proof follows the exact claim

State/write/idempotency/atomicity proof is blocking only for the current owner propositions and implementation properties actually claimed.

- N03 state proof must establish the admitted phase-state write/version/transition semantics when N03 state implementation is claimed.
- N12 local execution-state/receipt atomicity and idempotency proof must establish the exact N12 consistency boundary when implemented.
- N13 canonical-state/write/idempotency/atomicity proof must establish the exact N13 consistency boundary when implemented.
- restart/durability proof is required only if current implementation authority claims durable/restart behaviour; same-process/process-memory evidence cannot prove a stronger durability claim.
- external-effect/broker proof is required only if separate current operational authority activates that capability; it must include N12 fail-closed preconditions, uncertain-effect truth and no unsupported retry/fallback/success claims.
- external account truth/reconciliation proof is required only if a separate current reconciliation authority exists.

A local transaction or green state test cannot prove an untested external effect, external account state or durability property.

### N15-P09 — Authoritative replay proof uses exact N14 material and remains side-effect free

When a claim includes authoritative replay or governed semantic re-execution, proof must bind the exact N14 replay class, target-owner material, result-changing contracts/policies/configuration/executable versions, state/order facts and original missing/degraded/unknown conditions required by the target proposition.

Proof must cover authoritative match, semantic mismatch and non-authoritative incomplete outcomes as applicable; preserved versus new occurrence identity; comparison-only non-authority; and the prohibition on current-state/current-clock repair, live side effects and runtime-authority promotion.

A deterministic comparison, retained hash/path or successful fixture run cannot substitute for missing N14 replay authority.

### N15-P10 — Packet proof is conditional on an actually current named-seam carrier profile

No packet-specific product proof obligation is active merely because historical family 08/09 or kernel placeholder `P01` contains DMPV3 concepts.

Current SCC02/N21 direct typed owner seams remain the baseline and no current N16 carrier profile is admitted. Therefore packet proof is currently inactive.

If later accepted authority activates packetised carriage for a named seam, the proof trigger becomes true for that seam. Blocking proof must then bind the exact current carrier propositions and both semantic endpoints and cover, as applicable:

- envelope conformance and carrier identity/version/validation;
- producer emission and consumer acceptance;
- semantic-owner/seam distinction and no carrier ownership leakage;
- invalid/degraded carrier states;
- numeric integrity including sign, zero, scale, precision and magnitude where material; and
- omission/null/explicit-state distinctions where state meaning depends on them.

Producer-only or consumer-only proof is insufficient for a claimed packetised seam.

### N15-P11 — Modifier-specific proof is conditional on a concrete current modifier specification

N21 governance alone does not activate a concrete modifier/coefficient proof family. A modifier-specific blocker exists only when a current target explicitly activates an independently admitted target-specific modifier specification.

When triggered, proof must establish the modifier specification's exact source-state authority, activation predicate, target surface, restrictive/permitted transformation, bounds, precedence/compatibility, missing/invalid failure law, deterministic lineage and target-authority closure. For N11 it must prove restrictive-only behaviour and inability to create eligibility/capital authority.

Historical modifier/module/coefficient identities, examples or green tests do not satisfy this trigger.

### N15-P12 — Historical proof populations and green states are not current authority

Historical Gate-C/Gate-D plans, expected-red populations, receipts, `TP-*` control IDs, `TC-OPS-*` operational IDs, DMPV3 packet tests, historical M/K/package targets and historical green states remain evidence only unless a current proof decision explicitly rebinds a claim to current propositions and current implementation authority.

The reusable proof patterns may inform current proof design, but their old identity, tier, path, command, receipt or success state does not become a current blocker or current PASS by continuity.

## Current blocking-proof profiles

The table defines the exact semantic boundary and proposition set from which a future blocking family may be admitted. A profile is **inactive** until its trigger is satisfied by current implementation/promotion authority. Within an active profile, physical families must still cite the exact proposition subset they actually exercise; the table is not permission for one broad test to claim an entire row without semantic coverage.

| Profile | Trigger | Current proposition/boundary source | Minimum proof shape when activated | Current PB-15 state |
|---|---|---|---|---|
| `N15-B01` source/input/calendar | implementation claims N04 source/input/calendar conformance | `N04-P01` through `N04-P12`; source admission, identity/time, typed translation, options/calendar layers/precedence/degradation/provider substitution | typed contract + boundary integration + negative/conflict/absence/identity/time cases | inactive: no product implementation allocation |
| `N15-B02` prepared structural contracts | implementation claims N05 prepared/cognition-ingress contract conformance | `N05-P01` through `N05-P11`; envelope/payload, lineage/fingerprint, deterministic resolution receipts, narrowed ingress | contract + deterministic resolution + producer/consumer integration + negative widening/conflict cases | inactive |
| `N15-B03` calendar runtime owner | implementation claims N07 runtime calendar conformance | `N07-P01` through `N07-P09`; four-layer snapshot/projection, precedence, degraded/withheld states, side-effect closure | component + contract/integration + conflict/degradation/identity/time/side-effect cases | inactive |
| `N15-B04` prepared runtime owner | implementation claims N08 transformation conformance | `N08-P01` through `N08-P09`; exact N05 execution, lineage/receipts, deterministic non-emission/degradation, side-effect closure | component + contract/integration + deterministic equivalence + mandatory non-emission/optional degradation | inactive |
| `N15-B05` intraday phase | implementation claims N03 temporal-phase/state conformance | `N03-P01` through `N03-P12`; seven phases/unresolved, typed signals, hysteresis/monotonicity/correction/degradation/state/replay material | component + state + boundary integration + transition/degradation/correction/replay-material cases | inactive |
| `N15-B06` complete operating boundary | implementation/promotion claims a complete governed run or cross-owner operating sequence | `SCC01-P01` through `SCC01-P09`; order, six-stage spine, serial/parallel/pre-deployment/capital/execution/portfolio separation, explanation | sequential/end-to-end across the claimed real owner seams plus boundary-negative cases | inactive |
| `N15-B07` serial/parallel owners | implementation claims N09/N10/SCC02 conformance | `N09-P01` through `N09-P07`; `N10-P01` through `N10-P07`; `SCC02-P01` through `SCC02-P03`; separate branch authority and direct typed carriage baseline | separate owner component/contract proof + branch-independence integration + downstream convergence compatibility; no packet proof while trigger false | inactive |
| `N15-B08` terminal risk/capital | implementation claims N11 conformance | `N11-P01` through `N11-P10`; exact branch join, block-dominant eligibility, capital state/policy, bounds/rounding/receipt/side-effect closure | join integration + exhaustive precedence/negative states + arithmetic/property tests + lineage/side-effect closure | inactive |
| `N15-B09` modifier governance/application | separately admitted implementation authority creates a surface that claims N21 governance conformance, or a current target activates a concrete current modifier spec | `N21-P01` through `N21-P09` plus exact target proposition/specification when concrete | governance/target contract + precedence/conflict/missing-authority/restrictive-only cases | inactive: N21 is current governance, but no implementation surface or concrete modifier blocker is admitted |
| `N15-B10` execution local semantics | implementation claims N12 intent/attempt/event/receipt conformance | `N12-P01` through `N12-P07`, `N12-P10` through `N12-P12`; positive N11 gating, placement bounds, identities, event/receipt distinctions, idempotency, local atomicity | contract + owner integration + idempotency/conflict/state-atomicity + negative authority/event-distinction cases | inactive |
| `N15-B10E` external execution effects | separately admitted operational authority activates an external irreversible submission path | `N12-P08`, `N12-P09`, `N12-P10` and `N06-G08`; exact operational preconditions/uncertainty/idempotency/no implicit retry-fallback | hermetic fail-closed integration plus governed external-effect/reconciliation evidence at the exact activated boundary | inactive; no live broker/network capability commissioned |
| `N15-B11` portfolio/lifecycle | implementation claims N13 canonical state/lifecycle conformance without a stronger durability/external-account claim | `N13-P01` through `N13-P10`, plus `N13-P11`/`N13-P12` only for their no-overclaim/mechanism-separation boundaries; fill gating, one write boundary, lineage/idempotency/state version, hold/trim/close, atomic receipts | owner integration + state/idempotency/version tests + lifecycle invariants + atomicity/read-only boundary cases + negative proof that unclaimed durability/external-account truth is not asserted | inactive |
| `N15-B11D` portfolio durability/external account | separate current authority claims restart durability or external-account reconciliation | `N13-P11`, `N13-P12` plus exact separately admitted durability/reconciliation propositions | cross-process/restart or external reconciliation proof exactly matching claimed mechanism/authority | inactive; no such mechanism/authority selected |
| `N15-B12` replay | implementation claims N14 replay/review conformance or another owner claims authoritative replay | `N14-P01` through `N14-P12` plus the exact replay-target propositions | replay-class + exact-envelope/version/state + isolated re-execution + match/mismatch/incomplete + no-side-effect proof | inactive |
| `N15-B13` product guardrail overlay | any active implementation claim intersects an N06-protected proposition | `N06-P01`, applicable `N06-G01` through `N06-G10`, and every exact protected proposition exercised | negative/false-positive proof at the same owner/boundary level as the protected proposition | inactive until a protected implementation claim is active |
| `N15-B14` packet carrier | later accepted authority activates packetised carriage for a named seam | exact then-current carrier-profile propositions + both semantic endpoint propositions + `N15-P10` | producer + consumer + envelope/seam + invalid/degraded + numeric/state-integrity cases as applicable | inactive; packet trigger false |

## Current non-blocking/excluded proof jurisdictions

- N18 architecture-projection implementation proof is PB-16/N19 jurisdiction. N15 does not preserve the historical eighteen-surface proof catalogue or allocate architecture proof surfaces.
- Current-kernel architecture/bootstrap proof remains governed by `AK-PROOF-001`/`AK-PROOF-002` and the immutable kernel proof registries; N15 does not duplicate or mutate them.
- Vocabulary semantic admission remains governed by `VOCABULARY_GOVERNANCE`; a passing proof artefact cannot create a durable term meaning.
- Repository/source-integrity/Git validation for this reconciliation programme is governance validation, not proof that a product runtime exists.

## Historical proof-population disposition

### `TP-*`

Historical `TP-ADMISSION-001`, `TP-SELECTION-001`, `TP-TRACE-001`, `TP-PROMOTION-001`, `TP-RECEIPT-001`, `TP-ENV-001` and `TP-CONTROL-001` are not current product blocker identifiers. Their reusable themes are represented by current-kernel proof control and N15-P01 through N15-P07; their old paths/registries/control state remain historical.

### `TC-OPS-*`

- `TC-OPS-001` -> historical upstream-to-paper target; current end-to-end execution proof must be newly derived from the current propositions/implementation if such a claim is later activated.
- `TC-OPS-002` -> historical SQLite restart target; current durability proof exists only under `N15-B11D` when a durable N13 mechanism is actually admitted.
- `TC-OPS-003` -> historical provider target; its hermetic-substitution idea may support a current adapter claim but the old target/green state is not current.
- `TC-OPS-004` -> historical broker target; its fail-closed idea is rebound conditionally to `N12-P08`, `N12-P09`, `N12-P10` and `N06-G08` under `N15-B10E`.
- `TC-OPS-005` -> historical installed-operation target; current installation/composition proof is architecture/PB-16 jurisdiction unless a separate product proposition requires more.

Completed Gate-C/Gate-D plans, receipts, expected-red populations and green status are historical programme evidence and cannot reactivate any of these IDs.

## Scope and explicit exclusions

This record owns current product/protocol proof semantics and conditional proof applicability. It does **not**:

- define or change N03/N04/N05/N07/N08/N09/N10/N11/N12/N13/N14/N21/N06 product meaning;
- allocate implementation/runtime/architecture identity;
- admit physical product tests in the immutable current-kernel registries;
- commission packet carriage, live broker/network effects, durable storage, external-account reconciliation or concrete modifiers;
- prove that any current product implementation exists; or
- replace PB-16 architecture-proof projection.

## Dependencies and trigger predicates

### Universal dependencies

N15 universally depends on the exact current proposition it claims to prove. Proof without an admitted semantic proposition has no product authority.

Generic architecture/bootstrap proof mechanics remain current-kernel-owned.

### Conditional packet dependency

Trigger: later accepted authority activates a current packet/carrier profile for a named seam.

False state: direct typed owner seams remain current and `N15-B14` is inactive.

True state: exact current carrier propositions and both endpoint propositions enter the blocking proof set under N15-P10.

### Conditional modifier dependency

Trigger: a current target activates an independently admitted concrete modifier specification.

False state: no concrete modifier proof blocker exists.

True state: exact modifier specification + target proposition(s) enter `N15-B09`.

### Conditional external-effect dependency

Trigger: separate current operational authority activates an external irreversible N12 submission capability.

False state: no live broker/network proof blocker exists.

True state: `N15-B10E` is blocking for the activated capability.

### Conditional durability/external-account dependency

Trigger: separate current implementation/reconciliation authority claims N13 restart durability or external-account truth/reconciliation.

False state: `N15-B11D` is inactive.

True state: exact mechanism/reconciliation proposition(s) plus N13-P11/P12 enter the blocking set.

## Supersession and lineage

This record is a **SPLIT + REWRITE** of historical family-08 product/protocol proof semantics.

It retains exact claim-limited proof, proposition traceability, appropriate proof level, negative/missing-authority/status cases, proof isolation, aggregate completeness, status non-escalation and conditional packet/operational proof patterns.

It does not carry forward historical Gate-C/Gate-D control authority, `TP-*`/`TC-OPS-*` blocker identities, DMPV3 packet proof by default, historical M/K/package targets, historical environment/control-stack paths or historical green implementation status.

## Primary historical evidence

- `evidence/historical_normative/docs/08_TESTING_AND_PROMOTION_CORE.md:19-109` — environment, tiering and conditional packet proof;
- `evidence/historical_normative/docs/08_TESTING_AND_PROMOTION_CORE.md:111-192` — proof lifecycle/receipt/promotion closeout;
- `evidence/historical_normative/docs/08.1_TESTING_AND_PROMOTION_WORKING.md:5-59` — proof downstream of semantics, exact claim traceability and adequate proof levels/cases;
- `evidence/historical_normative/docs/08.1_TESTING_AND_PROMOTION_WORKING.md:61-118` — applicability/ownership separation, isolation, environment, aggregate gate and status preservation;
- `evidence/historical_normative/docs/08.1_TESTING_AND_PROMOTION_WORKING.md:120-165` — completed historical control state, TP controls and TC operational propositions.

## Current-authority/kernel references

Product/protocol/guardrail semantic sources:

- `normative/records/N04_DOMAIN_SOURCE_INPUT_CALENDAR.md`;
- `normative/records/N05_PREPARED_DATA_CONTRACTS.md`;
- `normative/records/N07_CALENDAR_RUNTIME_OWNER.md`;
- `normative/records/N08_PREPARED_RUNTIME_OWNER.md`;
- `normative/records/N03_INTRADAY_PHASE.md`;
- `normative/records/SCC01_OPERATING_BOUNDARY.md`;
- `normative/records/SCC02_SERIAL_PARALLEL_OWNERS.md`;
- `normative/records/N11_TERMINAL_RISK_CAPITAL.md`;
- `normative/records/N21_STATE_AND_PACKET_MODIFIERS.md`;
- `normative/records/N12_EXECUTION.md`;
- `normative/records/N13_PORTFOLIO_LIFECYCLE.md`;
- `normative/records/N14_REPLAY.md`;
- `normative/records/N06_PRODUCT_GUARDRAILS.md`.

Architecture/proof jurisdiction:

- `normative/records/N18_PRODUCT_ARCHITECTURE_PROJECTION.md`;
- `evidence/current_kernel/tree/docs/architecture/TEST_AND_PROMOTION_KERNEL.md:3-34`;
- `evidence/current_kernel/tree/config/proof/test_families.yaml`;
- `evidence/current_kernel/tree/config/proof/proof_blocks.yaml`;
- `evidence/current_kernel/tree/config/proof/promotion_sets.yaml`;
- `evidence/current_kernel/tree/schemas/test_family.schema.json`;
- `evidence/current_kernel/tree/config/architecture/modules.yaml`;
- `evidence/current_kernel/tree/config/architecture/implementation_allocations.yaml`;
- `evidence/current_kernel/tree/config/architecture/protocols.yaml`.

## Vocabulary implications

`N15-Pxx` and `N15-Bxx` are stable current proposition/proof-obligation locators, not runtime/domain object names or legacy vocabulary continuations. No historical proof-block/test-family name becomes a current durable term by appearing here.

## Architecture projection implications

N15 does not allocate a proof architecture surface. PB-16 may project N15 obligations into current-kernel architecture/proof grammar only after preserving exact current proposition/boundary traceability and without reviving the historical eighteen-surface catalogue.

## Guardrail implications

N15 operationalises N06 guardrails as negative proof only where their protected current propositions are part of an activated implementation claim. It cannot use proof to broaden product authority or make an inactive conditional capability current.

## Unresolved items

- No current physical product test family or product promotion set is admitted by PB-15.
- No current runtime module/allocation exists in the supplied architecture-kernel reference.
- No current packet carrier profile exists; packet proof is inactive.
- No concrete modifier/coefficient instance is active; target-specific modifier proof is inactive.
- No live broker/network capability is commissioned; external-effect proof is inactive.
- No N13 restart durability/external-account reconciliation mechanism is selected; that proof is inactive.
- PB-16 remains responsible for architecture-proof projection.
