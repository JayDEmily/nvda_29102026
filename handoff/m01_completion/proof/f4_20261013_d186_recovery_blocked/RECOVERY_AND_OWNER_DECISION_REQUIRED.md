# M01 Stage-1 F4 — RC08 D186 recovery boundary

Date: 2026-10-13 (Australia/Melbourne). Disposition: `BLOCKED / NORMATIVE_TYPED_PROJECTION_AUTHORITY`.
This is an engineering evidence checkpoint, **not** a revised accepted source, corrected D186 implementation, or independent-review candidate.

## Git baseline and authorised scope

- Source RC08 preservation handoff; baseline HEAD `44875e9b98cace7a3337230fe9997bd355f7a6f1` / tree `b906639e1c53bedb3ac4df1ed446b3b094a6ec33`.
- Recovery request: recreate the lost post-RC08 D186 proof/repair without rewriting existing history, then continue only against defined semantics; Stage 2 prohibited.
- Governing files read: root `GUARDRAILS.md`, `AGENTS.md`, `EXEC_PLAN.md`, test-local `tests/AGENTS.override.md`; accepted brief `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md` §5 K08/K16, normative CSV D155/D186, admitted `api.py`, `_stage1.py`, RC08 clarification proposal.
- Existing RED proof commit `3db5952` precedes proposed repair; existing test `tests/product/derived_signal/test_m01_f4_cross_stage_d186_entry_anchor.py` is retained unmodified.

## Observations in current runtime

1. `python -m pytest -q tests/product/derived_signal/test_m01_f4_cross_stage_d186_entry_anchor.py`: **1 failed**, `TypeError: parameters tuple values must contain immutable scalar values` at `api.py` immutable parameter admission. Exact output in `BASELINE_EXISTING_RED.log`. This is pre-production and does not exercise the intended anchor resolution.
2. Direct admitted-type probe: scalar-valued flat parameter names are accepted; nested named feature pairs are rejected. `TYPED_CARRIER_PROBE.log`.
3. Direct controlled D155 own-kernel schema probe using its exact nine CSV predecessor identities returns ordered 4-tuples `(Dxxx, component_value, component_occurrence_id, metadata)`, **not** the flat `(feature_name, Decimal)` tuples used in the inherited D186 test. Some D155 constituent values are themselves structured under accepted rules, so no blanket numeric extractor is established by D155 assembly. This probe exercises own-kernel shape only; it is not public Stage-2 integration or a proof of current-provider data.
4. In `src/nvda_desk/derived_signal_calculation_truth/_stage1.py`, D186 dereferences `EntryStateContextV1.entry_state_vector`, which is absent from the admitted class; the only entry anchor field is `d155_occurrence_id`.
5. The RC08 `CONSOLIDATED_OWNER_CLARIFICATION_PROPOSAL.md` explicitly identifies the literal flat key convention and exact feature-identity/extractor grammar as not yet accepted normative authority. The prior worker's reported later repair/test passes were not recovered into the supplied Git archive.

## First unmet invariant and stop boundary

Accepted K08 mathematics requires comparing compatible *scalar* feature values extracted from the actual stored/current D155 occurrences, with explicit immutable per-feature weights/scales. K16 preserves named, heterogeneous component values without implicit flattening or weighting. No accepted D186 rule presently establishes a deterministic, typed scalar-feature projection for the structured D155 carrier or selects literal P_RULE keys.

A replacement using an arbitrary `similarity_weight:<name>` key scheme or silently treating the D155 component tuple as a flat scalar vector would create unapproved meaning. Merely retrieving the correct D155 occurrence would not close this semantic gap. Under guardrails, downstream production repair and a Stage-1 review candidate are therefore stopped here.

## Bounded programme-owner decision requested

Approve or replace **one** exact, versioned D186 `P_RULE` feature-profile definition within the existing `CalculationParameterSetV1.parameters` value types. Proposed law for approval:

- Feature `j` is identified by an explicitly ordered, distinct `similarity_feature:j` tuple comprising the canonical D155 component `Dxxx`, a named deterministic scalar-extractor identifier, and its exact component/path argument(s). Use only extraction operations explicitly permitted for D186; where the retained D155 component is non-scalar and no extractor is named, refuse.
- For each `j`, store immutable `similarity_weight:j` and `similarity_scale:j` Decimal scalars in the same parameter set. Require exact 1:1 coverage of declared features, non-negative weights summing exactly to one, and strictly positive scales. Reject collisions, undeclared/missing fields, repeated features and silently dropped feature ids. Use a canonical integer index syntax (`1`, `2`, ..., contiguous) so the key grammar is deterministic and collision-free.
- Resolve `EntryStateContextV1.d155_occurrence_id` against the exact D155 history; require one matching earlier entry occurrence, one compatible current occurrence, the same immutable D155 feature/component schema and temporal/version/subject compatibility. Both occurrence IDs must survive in lineage. No inline entry payload, fallback to newest entry, implicit feature extractor, future reference, or implicit default is allowed.
- Mathematical output remains unchanged: `distance_squared`, `similarity = exp(-0.5*d²)`, and per-feature `(raw_delta, standardised_delta)` with deterministic feature ordering.

**Note:** the approved extractor repertoire and path grammar must be explicit; K07 has defined extractors, but their application to D186 cannot be inferred without authority. The proposed representation is not adopted by this memo. If the programme owner approves reusing the *already accepted K07 scalar-extractor definitions* for D186 (`component(path)`, `class_probability(label)`, `weighted_component_sum`, `probability_margin`, `normalised_entropy`, etc.) with their existing argument requirements and validation, that supplies the missing extractor law without inventing a new one.

## Remaining Stage-1 boundary

RC08's D178/D189/D192 exact unit/risk questions remain independently underdefined. All 30 cross-stage rows remain not demonstrated ready for the consolidated Stage-1 independent review. The present checkpoint must not be presented as Stage-1 acceptance or a reviewer candidate.
