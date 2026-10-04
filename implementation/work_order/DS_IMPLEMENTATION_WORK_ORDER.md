# Derived Signal Calculation Truth — bounded implementation work order

## Status and authority boundary

**ARCHITECTURE-ADMISSION WORK ORDER CANDIDATE — execution remains governed by the finalised PCM task graph.**

This record translates the admitted architecture boundary into bounded downstream work. It is not authority to begin production implementation immediately, does not bypass any test-first predecessor or independent-review leaf, and does not add calculation semantics beyond the accepted brief and catalogue.

The work order is bound to:

- accepted Derived Signal authority recorded by `.pcm/control/instantiation.json`;
- DS-A01 implementation-authority candidate and binding;
- DS-A02 independent-review PASS for packet `11685c4c6dd0f59f67fc9cf336980cd0c6f71d58af8587f97f86b4bd930e6098`;
- the DS-A03 architecture admission in `config/architecture/`.

## Admitted architecture target

- Runtime semantic owner: `M01`, `derived_signal_calculation_truth`.
- Current lifecycle state: `bootstrap`; DS-I01 now admits the bounded foundation implementation shell while composability and active runtime behaviour remain unadmitted pending later governed proof/implementation.
- Intended Python owner root: `nvda_desk.derived_signal_calculation_truth`.
- Declared public seam: `nvda_desk.derived_signal_calculation_truth.api`.
- Permitted runtime owner dependency: `M01 -> M00` only, through M00's declared public seam.
- M00 modification boundary: additive read-only typed raw-value/history projection only; M00 retains Raw Signal ownership and writer authority.
- M01 persistence boundary: calculation-owner schema/write role separate from M00, with no M01 database-role privilege over M00-owned relations. One PostgreSQL deployment remains permitted.
- External effects: none. Calculated action-like values remain facts.

The package/seam strings above are internal architecture boundary declarations required to identify the future owner and its one cross-owner import target. They do not select the final distribution/package release name or version governed later by `DS-PO01`.

## Governed downstream execution order

### DS-T01 — foundation proof first

Before any production behaviour change, establish executable proof for:

- exact field-level M00 projection and ambiguous-mapping refusal;
- stable bounded raw-history enumeration and temporal/receipt ordering;
- explicit unit/version/context/input-selection behaviour and fail-closed absence;
- M01 separate PostgreSQL schema/write-role boundary and no M00-table privilege;
- typed derived-result/lineage carriers and public-seam absence semantics;
- prohibition of provider-specific parsing fallback and external effects.

### DS-I01 — foundation implementation only after DS-T01 acceptance

Implement only the architecture already admitted here:

- M00 additive typed raw-value/history projection through the existing M00 public seam;
- M01 package/public calculation-read seam and bounded calculation-owner contracts;
- immutable/versioned calculation inputs and contexts required by accepted authority;
- M01-owned derived-occurrence and lineage persistence with separate writer boundary;
- no kernel semantics beyond what is required to support the admitted foundation contracts.

M01 may become `active` only through a later lawful task when executable package/seam existence and the applicable proof support that lifecycle transition. DS-A03 does not activate it.

### DS-T02 / DS-I02 — foundational deterministic kernel group

Follow the committed task graph for proof then implementation of catalogue rows bound to `K01_TIME`–`K08_RULE_BUCKET_POLICY`, `K16_STRUCTURED_ASSEMBLY` and `K17_ORDER_FLOW_IMBALANCE`, preserving exact catalogue dependencies, history sufficiency and version-consistent predecessor resolution.

### DS-T03 / DS-I03 — advanced kernel group

Follow the committed task graph for proof then implementation of `K09_SURFACE_DENSITY`–`K15_EVALUATION`, without implementation-selected model/convention changes or external-action activation.

### DS-T04 / DS-I04 — whole-catalogue integration

Establish the full accepted proof surface, then make only bounded defect closures needed for already-admitted semantics. No new D identity, dependency edge, kernel, typed-context meaning or external behaviour may be introduced.

Independent-review leaves remain separate and must be performed by a reviewer distinct from the candidate author wherever the finalised PCM plan requires it.

## Explicit non-authorities and deferred choices

This work order does not authorise or choose:

- any change to the accepted `D001`–`D209` meanings, kernels, dependencies or catalogue bindings;
- direct M01 access to M00-owned PostgreSQL relations;
- a second Derived Signal semantic owner or competing calculation path;
- provider/network integrations or provider-specific extraction fallback in M01;
- order, account, brokerage or other external effects;
- final distribution name/version before `DS-PO01`;
- concrete PostgreSQL schema/role names or physical table/index/partition layout;
- occurrence-ID algorithm;
- concrete provider/native-field mappings or production parameter/context instances;
- performance/SLA/RTO/RPO commitments;
- downstream authority to act on calculated values.

Any downstream need for one of those choices must follow its existing authority route or stop `BLOCKED`; it must not become an implementation default.
