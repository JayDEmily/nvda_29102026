# Semantic receipt — `tests/tier_a/upstream_cognition/test_fwd009_reopened_row_prepared_ingress_runtime_context_proof.py`

## Process/restatement
- Sequence/unit `028` / `PM-012`; SHA `a3300de568165f2609a7b7de5d6ae811bd932a0d24ccf381e08bc12deff0ebb9`.
- Read full test `1-398`, all 49 parameter cases, full preparation/context-packet/prepared-contract surfaces and current routes. Route is absent. Pytest: `49 passed in 0.28s`.
- The file maps 49 Atlas rows to 14 canned preparation behaviours, then tests selected packet, lineage, copying, feature derivation, service and transform specimens. It never reads the Atlas records or proves those semantic assignments.

## Assertion-group relationships

| G | Locator | Authority | Exact proof / limitation; falsifier | Relation / strength | Gate |
|---|---|---|---|---|---|
| 1 | `53-194` | `N08-011`, `docs/08_TESTING_AND_PROMOTION_CORE.md:69-101` | Only non-empty IDs; empty ID fails `194`, wrong non-empty mappings pass. | `related_but_not_proved` / `token_only` | P3 row traceability. |
| 2 | `196-222` | `N04.2-002`/`N04.2-006`, `docs/04.2...:27-64,126-146`; `N09-011`, `docs/09.1...:131-147` | Explicit packet IDs/role labels, review trace and deterministic payload fingerprint are carried. Change one observed field and `210-221` fails. Does not prove fingerprint inputs complete, lawful parent meaning, role validation or no authority side effects. | `bounded_separable_clause` / `identity_lineage` | Preserve narrow packet-carriage clause. |
| 3 | `224-235` | `N04.2-002`, `27-64` | Selected source kind/channel/sections/time and floored runtime bar are retained. Alter carrier and `226-234` fails. No schema/policy/derivation versions, artefact references or full source lineage. | `bounded_separable_clause` / `identity_lineage` | P3 completion. |
| 4 | `237-249` | `N04.2-001`, `17-25` | Two snapshots remain distinct and exported mapping mutation does not alter source snapshot. Mutate alias and `243-248` fails. No immutable envelope or persistence proof. | `bounded_separable_clause` / `boundary` | Preserve copy isolation. |
| 5 | `251-261` | `N04.2-004`/`N04.2-005`, `91-124` | Selected market/options fields and source-section tuple are produced. Change selection and `254-260` fails. It does not prove field-specific precedence/receipts; empty failure lists are not validation proof. | `related_but_not_proved` / `specimen_only` | P3 field-resolution receipts. |
| 6 | `263-275` | `N04.2-004`/`N04.2-006`, `91-146` | Five exact derived values and names are asserted. Change formula/output and `265-274` fails. No normative proposition authorises these formulas, rounding or inputs. | `authority_missing` / `behavioural` | Missing normative derivation authority. |
| 7 | `277-285` | `N04.2-001`/`N04.2-002`, `17-64` | Dataclass form, primary snapshot, lineage list and bar time exist. Structural specimen only; wrong semantic fields pass. | `related_but_not_proved` / `signature_only` | P3 typed envelope semantics. |
| 8 | `287-295` | `N04.2-001`, `17-25` | Source payload and exported mapping are detached from snapshot nested payload. Mutation must leave `front_premium`, else `293-294` fails. Does not prove object-wide immutability. | `bounded_separable_clause` / `boundary` | Preserve narrow copy safety. |
| 9 | `297-316` | `N04-002`, `docs/04.1...:21-42`; `N04.2-001` | AST import/name/field blacklists and exact four-field dataset shape. Listed token/symbol/field causes `300-315` failure; renamed/indirect donor semantics pass. | `related_but_not_proved` / `token_only` | P3 behavioural/dependency boundary. |
| 10 | `318-330` | `N04.2-002`, `27-64` | Legacy payload service emits selected alpha lineage labels and retains ID. Change field and `324-329` fails. Labels do not establish source truth, versions or fingerprints. | `historical_observational` / `specimen_only` | Gate D/P3 reconciliation. |
| 11 | `332-339` | `N04.2-004`/`N04.2-005` | Service converts one bundle and emits two derived values plus alignment label. Change output and `335-338` fails. Selection/derivation authority and conflict handling remain unproved. | `related_but_not_proved` / `specimen_only` | P3. |
| 12 | `341-355` | `N04.2-001`/`N04.2-002` | Two input forms become two snapshots/lineages without reported failures. Alter count/IDs and `349-354` fails. No dataset-level identity/version/fingerprint or actual validation. | `related_but_not_proved` / `specimen_only` | P3. |
| 13 | `357-384` (`options_flow_input_carriage`) | `N03.2-001`, `docs/03.2...:15-29`; `N04.2-008`, `179-203` | Generic snapshot preserves an arbitrary nested `options_flow_context` and common derived fields. The test never builds the typed options carrier or asserts the nested values. Falsifier changing asserted common fields fails `376-383`; losing/options-corrupting nested context may pass. | `related_but_not_proved` / `specimen_only` | P3 typed carrier proof. |
| 14 | `357-384` (`market_regime_input_carriage`) | `N04.2-008`, `179-203` | Same defect for arbitrary `market_regime_context`; no typed regime carrier or nested assertions. | `related_but_not_proved` / `specimen_only` | P3 typed carrier proof. |
| 15 | `386-396` | `N04-003`, `docs/04.1...:44-72`; `N04.2-002` | Event ID/tags, source time and floored runtime bar are carried into snapshot/payload. Alter field and `390-395` fails. No event authority, timezone consistency, calendar-layer identity or complete temporal lineage. | `bounded_separable_clause` / `identity_lineage` | Preserve narrow carriage only. |

## File disposition
- Groups/relationships `15/15`; final `BLOCKED_P3_REPAIR`.
- Decisive defects: unsupported 49-row semantic mapping; non-exhaustive AST/name/field blacklists; normatively unauthorised derivation formulas; and “options/regime carriage” branches that never observe typed carriers or their nested content.
- No implementation/test mutation executed.
