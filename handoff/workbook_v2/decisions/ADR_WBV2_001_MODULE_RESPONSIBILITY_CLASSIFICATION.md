# ADR-WBV2-001 — Raw truth, derived-raw calculations and unallocated downstream responsibilities

**Status:** Programme-owner-directed **V2 review criterion**; proposed future architecture, **NOT** an accepted M01 ownership amendment.
**Recorded:** 2026-10-14 (Australia/Melbourne)
**Scope:** Workbook V2 classification of D001–D209 only. M00 and M01 accepted semantics, module IDs, normative catalogue, code, tests and active `EXEC_PLAN.md` are not changed.

## Decision purpose

Separate (1) acquired raw signal truth, (2) reusable strategy-independent calculation truth, and (3) everything requiring modelling, strategy, candidate/portfolio state, risk or action policy, or other downstream responsibilities. Avoid hard-coding playbooks and tuned coefficients into the market calculation foundation. A family label, paper citation or existing kernel grouping does not allocate a software module.

## M00 — raw signal truth (existing owner)

M00 acquires authorised external/internal raw signals; preserves native values, identifiers, units, timestamps, ordering, provenance and histories; exposes admitted typed projections. It does not compute D-signal mathematical transformations, forecasts or trades. **Not every M00 `Rxxx` is market data**: the catalogue also contains account/risk, position, order/execution, operational clock and other records. Do not silently treat M00 as exclusively market quotes.

## M01-1 — derived raw market calculations (PROPOSED identity only)

A D-signal belongs to this proposed responsibility **only if**:

1. Every numerical data-input path terminates in appropriate M00 raw **market/source-time** signals, or other already-qualifying derived-raw market calculations; the graph is acyclic. Pure provider timestamp/session/calendar or data-integrity transformations of these signals are eligible.
2. The mathematical meaning is exact, fixed and descriptive: arithmetic, temporal transformation, rate/return, historical/statistical estimator, objectively defined order-book measurement or deterministic non-strategy data transformation. This may include a data-fitted descriptive regression, but not a chosen predictive scenario or a tuned scoring model.
3. There is no independent strategy coefficient, discretionary feature weight, judgemental predictive-model assumption, playbook activation gate, policy/decision threshold, or candidate/portfolio/order-intent context. Fixed numerical constants and versioned, **non-strategy** measurement conventions (e.g., five full trading days, immutable calendar, defined comparator/basket or precision) are permitted; changing meaning requires a new calculation-definition version, not silent runtime substitution.
4. Exact source identities, history sufficiency, temporal/cutoff alignment, sampling/selection rules, input and output units, and invalid/missing-input refusal are specified. No valid occurrence until all prerequisites exist; no fabricated zero, extrapolation, history or future knowledge.
5. The D-signal has an individually identifiable implementation/contract and an independently executable test suite, covering exact positive, boundary, negative/refusal, lineage, versioning and retry behaviour. Sharing low-level mathematical utilities is permissible; unit tests must not require unrelated calculations to run.
6. Valid calculated results are durable, reproducible, versioned and traceable to exact input occurrences. Multiple downstream consumers may reuse the result without recomputing upstream mathematics.

**Classification versus implementation acceptance:** This pass assesses *semantic eligibility* from exact authoritative definitions and source dependencies. `YES — proposed M01-1` does **not** assert that requirement 5 or runtime persistence/proof has been independently demonstrated. A separate implementation/test census and independent review are required before allocating or accepting a production module.

## All other D-signals — unallocated

Any D-signal failing the semantic criterion is **not admitted to proposed M01-1**. It is retained in the 209-row universe as an unallocated downstream responsibility. It may represent a model-based inference, composite factor, scenario, shared intermediate strategy calculation, candidate/portfolio economics, risk policy, playbook computation, execution measurement, model evaluation or operational scheduling. There is **no** presumption that all remaining D-signals form one module, or that every D-signal or family gets its own module. One downstream intermediate calculation may serve multiple playbooks.

A `NO — not admitted` based on insufficient fixed semantic evidence is **not** a determination that a signal is invalid, useless or permanently ineligible. It is a refusal to certify a criterion that is not established. The row-level register records such uncertainty and the actual disqualifier.

## V2 workbook and governance constraints

- Keep original D001–D209 and original family assignments; the 40-family and 13-calculation-class proposals remain separately identified as unapproved reviews.
- Record exactly one row-level YES/NO **proposed semantic eligibility** outcome for each D-ID; preserve a reason, effective normative row reference, original V1 row and dependency evidence. No eligibility inferred from family or proposed calculation-class alone.
- Create a **candidate-only M01-1 worksheet** in the V2 research copy. It displays only YES D-identifiers. The complete 209-row YES/NO audit remains a separate committed CSV, not a covert deletion of the other D-signals.
- Do not change the root `GUARDRAILS.md`, the accepted M01 brief/catalogue/`EXEC_PLAN.md`, M00/M01 source, tests, schema or architecture registry on this V2 branch.
- Subsequent module allocation/implementation requires a separate authority decision, exact dependency/interface migration and independent test-proof/lineage verification. The paused M01 Stage 1 is not reclassified as completed by this worksheet.

## Authority and evidence

Current Programme Owner instruction (14 October 2026) authorised recording the above criteria and performing one D001–D209 classification pass. Governing repository hierarchy: `GUARDRAILS.md`, `AGENTS.md`, `EXEC_PLAN.md`; effective M01 authority in `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md` and `NVDA_DERIVED_SIGNAL_CATALOGUE.csv` (SHA-256 `26c5486d1a4c7ff68025c7ce2d7e6847a7798759b847a716c942fd05345f3803`); original research workbook SHA-256 `519ea9449297d564ae4a02afc1bf4e60e4471631c81a0842620f9fb60bb4f9ae`.

**Result:** review-only boundary and auditable eligibility proposal, *not* an admitted new architecture identity or accepted mathematical/test proof.
