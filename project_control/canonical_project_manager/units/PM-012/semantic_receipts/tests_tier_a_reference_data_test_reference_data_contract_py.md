# Semantic receipt — `tests/tier_a/reference_data/test_reference_data_contract.py`

## Process and complete restatement
- Sequence/unit: `021` / `PM-012`; SHA-256 `c7ef907e36a200127e32543d751abd061f221ef30a4f05f2c1b0355d08f9cea4`.
- Read full test `1-69`, full `src/nvda_desk/contracts/reference_data.py`, and current routes. Targeted pytest: `3 passed in 0.18s`.
- The file dynamically imports one module, requires six named symbols, requires five to be dataclasses, and requires three named models to expose small field subsets. It constructs nothing and observes no validation, identity, four-layer calendar semantics, projection, failure, lineage, authority exclusion, immutability or substitution.

## Assertion-group relationships

| G | Test/assertion locator | Proposition ID / authority locator | Meaning, fit, exact proof and limitation | Falsifier / required failure | Relation / strength | Disposition |
|---|---|---|---|---|---|---|
| 1 | `22-34` | `N03.2-004`, `docs/03.2_INPUT_AND_CALENDAR_DOMAIN_WORKING.md:96-119`; separation `160-168` | Six implementation labels exist. Authority requires exact four governed layers and says `PrecursorRuntimePacket`-style labels are implementation evidence only when mapped. No mapping is asserted. | Remove one export; `34` fails. A semantically wrong six-model taxonomy passes. | `related_but_not_proved` / `presence_only` | Observational only. |
| 2 | `37-49` | `N03.2-004`, same locator | Five symbols are dataclass types. Dataclass form is not calendar ownership, identity, lineage or layer proof. | Convert one to non-dataclass; `49` fails. Wrong semantics in a dataclass pass. | `no_semantic_fit` / `signature_only` | No authority credit. |
| 3 | `52-69` | `N03.2-004`/`N03.2-005`/`N03.2-006`, `96-193`; row-5.4 traceability `docs/07.1...:172-177` | Three models contain selected field names. The authority requires layer/fact/version identity, explicit precedence/failure and projection trace. Field subsets do not prove those meanings; notably `PrecursorRuntimePacket` is explicitly not a fifth layer. | Remove a named field; `67-69` fails. Missing trace, invalid precedence and authority contamination pass. | `related_but_not_proved` / `signature_only` | P3 if retained as Tier-A semantic proof. |

## File-level disposition
- Groups/relationships: `3` / `3`.
- Final disposition: `NON_AUTHORITATIVE_OBSERVATIONAL`.
- The file is a structural inventory of legacy/current alpha contract names. It does not prove the governed four-layer financial-calendar model or the row-5.4 projection trace and cannot support Tier-A authority claims without behavioural reconstruction.
- No implementation or test mutation executed.
