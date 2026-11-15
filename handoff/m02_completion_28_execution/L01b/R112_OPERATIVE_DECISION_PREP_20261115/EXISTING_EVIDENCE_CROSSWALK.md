# Evidence reuse investigation — R112/D091 exact scope

**Status:** INVESTIGATED / REUSE NOT AUTOMATICALLY ADMITTED. This is a source/code/proof inventory, not a new product proof or blanket conclusion about old green outcomes.

## Directly inspected existing surfaces

| Existing source or test | Grounded proposition | **Does not** by itself establish |
|---|---|---|
| `tests/product/derived_signal/test_ds_t01_m00_projection.py::test_exact_mapping_is_required_and_catalogue_provenance_never_guesses_field` | Existing M00 tests require explicit raw projection mapping and refuse ambiguous maps | Proposed R112 mapping/provider/contract identity acceptance |
| Same file, `test_projection_exposes_exact_mapped_selection_identity_and_refuses_missing_dimension` | Native identity selectors are exposed exactly; omitted dimension can refuse | R112's 11 new identity fields at correct option/model/generation and custom receipt-only selection |
| Same file, `test_projected_history_is_bounded_repeatably_ordered_and_paginates_without_duplication` | Historical test exercises fixed-input pagination, ordered/unique results under its original fixture | Snapshot/seal across pages while concurrent admissions occur; no-append exclusive coordinator guarantee |
| `tests/product/m00_brief2/test_ibkr_history.py::test_history_negative`, cases N04/N05/N10/N13/N16 | Existing documented negative test *code* addresses receipt/event query, tied rows, provider/selector changes, future observation and conflicting retries under M00-Brief2 | An independently accepted R112 model-delta native-domain refusal, or coverage of all D091 negative cases |
| `src/nvda_desk/raw_signal_occurrence_truth/api.py`, `project_raw_value`/raw getter | M00 preserves projected `Decimal` and exposes original raw observation getter | Validation that original `observation.native_units` agrees with `mapping.native_units` unless future consumer checks it |
| `src/nvda_desk/market_measurement_truth/_selection.py` | Current pilot requires true UTC event instant and missing selection identity | New receipt-only R112 profile: never reuse by silently disabling conditions |
| `src/nvda_desk/market_measurement_truth/api.py`, `_native_codec.py` | Current exact record types and lossless tagged codec have explicitly finite allowed carriers | Categorical D091 result codec, readback and persisted record; no silent conversion to Decimal |

The old `m00_brief2` proof claim points to `config/product_proof/m00_brief2/admission.json`, its own generation `0005.json`, and a distinct control-history/IBKR fixture domain. The `EVIDENCE_REUSE_INDEX.json` explicitly says `REUSABLE_FOR_UNCHANGED_EXACT_PROPOSITIONS_ONLY`. **Reuse decision remains UNKNOWN** until an independent Tester examines actual admitted old commands/raw outcomes, exact source versions, generation/runner and material-invalidation analysis for each proposed mapped R112 proposition.

## Exact D091 finite two-node constraint

- Original `M02-C28-D091` proposes only two **physical** case IDs: `D091-CONTROLLED-SUCCESS` and `D091-CONTROLLED-REACHED_REFUSAL`; path `tests/product/m02_completion_28/d091/test_signal.py`; six is a ceiling, not permission to add four.
- `SUCCESS` proposal has 12 exact positive raw members/requests, all five adopted bins and both signed endpoints; the source batch contains 15 members total. Each positive has its own exact receipt/as_of; one latest query is not 12 selections.
- `REACHED_REFUSAL` anchor is an otherwise lawful exact Decimal `1.01` carried through M00. Its native R112 value is outside [-1,1] and must *reach* the D091 range invariant, **not** fail at mapping, wrong identity, missing units or clock.
- `NaN`, absent, wrong metadata/model/units/generation, receipt/sequence/tie/page completeness and unsuccessful durable write remain separately identified. Exact reusable older evidence, or independently approved finite binding within the two nodes, is still unproved. Do not hide separately parameterised cases under an asserted single pytest node. If coverage requires more physical nodes, obtain actual prior authority and case allocation, not a ceiling inference.

**Disposition:** Existing M00 tests supply useful scoped candidate evidence for non-invalidation analysis, not a demonstrated waiver for R112/D091 product proofs. There is currently no admitted D091 product result or reusable exact R112 source proof.
