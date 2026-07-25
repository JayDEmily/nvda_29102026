# Semantic receipt — `tests/tier_a/packets/test_reference_packet_carriage.py`

## 1. Process record
- Sequence/unit: `020` / `PM-012`.
- SHA-256: `61a55a2caed8bb9e0497a8a980d413cb0790a8a3d1c3fa8afc07eed93b37ca41`.
- Test read in full: `1-154`; six tests treated as six assertion groups.
- Direct packet contracts/builders and both compatibility wrappers read in full; current retained/proof routes inspected.
- Validation: targeted pytest returned `6 passed in 0.19s`, exit `0`.

## 2. Complete file restatement
The file checks packet-builder and contract symbol presence; constructs a reference packet without caller trace/run context and checks selected canonical-shell fields plus current degraded defaults; constructs a generic stage packet and checks supplied lineage/summary/extension literals; constructs prepared and review packets and checks role labels/parent ID; and attempts to overwrite canonical schema-identification extension leaves. It does not exercise a typed reference payload, reference owner/version/semantic checks, role-specific mandatory lineage, source truth, actual validation checks, persistence, deterministic replay, or no-authority side effects.

## 3. Assertion-group relationships

| G | Exact test/assertion locator | Proposition ID and source locator | Behaviour, authority meaning, and fit | Exact proof / explicit non-proof | Exact-surface falsifier and required failure | Relation / strength | Disposition and return gate |
|---|---|---|---|---|---|---|---|
| 1 | `11-15` | `N09-001`, `docs/09_DMPV3_PROTOCOL_CORE.md:19-29`; builder allocation `155-165` | Four imported builder/helper symbols resolve. Canonical allocation is named, but presence is not emission proof. | Proves non-`None` symbols only. | Remove/rename one symbol; corresponding assertion fails. Inert wrong objects still pass. | `related_but_not_proved` / `presence_only` | Observational presence only. |
| 2 | `18-21` | `N09-001`, core `19-29` | Three imported envelope/helper classes resolve. | Proves class-symbol presence only. | Remove one export; `19-21` fails. Parallel/invalid grammar elsewhere passes. | `related_but_not_proved` / `presence_only` | Observational presence only. |
| 3 | `24-55` | `N09-001`/`N09-004`/`N09-005`; `N09-003`/`N09-006`/`N09-011`, working `25-39,81-91,139-147` | Reference builder carries selected shell/producer/source-artefact fields and current alpha default violations; dump/validate preserves specimen. | Proves listed fields and current degraded-default behaviour. It does not prove lawful reference identity, actual role checks, source artefact truth, governed trace/run identity or replay. | Change an asserted field/default or lose round-trip field; `35-55` fails. Fabricated reference meaning and unlawful default identities still pass. | `related_but_not_proved` / `historical_observational` | P3/Gate D: typed role checks and owner-supplied identities. |
| 4 | `58-91` | `N09-004`/`N09-005`/`N09-006`/`N09-007`/`N09-008`, core `60-153` | Generic builder carries supplied producer stage, parent/dependency lists, summary and execution context, and reports default `valid`. | Proves literal carriage and schema-leaf inference; not truth, mandatory subsets, extension admission or actual validation. | Alter a carrier; `84-91` fails. Fabricated inputs/default-valid still pass. | `related_but_not_proved` / `specimen_only` | P3: role-specific semantic validation. |
| 5 | `94-119` | `N09-011`, `docs/09.1_DMPV3_PROTOCOL_WORKING.md:131-147` | Prepared/review builders emit the exact current role/producer labels and parent ID. Authority additionally requires lineage/proof preservation and no live authority. | Proves selected labels and parent carriage only; does not observe non-authority, complete lineage, deterministic review or preparation correctness. | Change labels/parent; `114-119` fails. Hidden trading/risk mutation still passes. | `related_but_not_proved` / `specimen_only` | P3: observe bounded behaviour and no-side-effect boundary. |
| 6 | `122-154` | `N09-008`, core `141-153`, working `106-119` | Caller attempts to replace all three canonical schema-identification leaves; builder restores them and preserves unrelated execution context. | Proves canonical schema leaves win for a dict payload and unrelated leaf survives. It does not prove schema truth for arbitrary typed payloads or extension governance. | Let injected value win or erase execution context; `148-154` fails. Later misuse of extension metadata passes. | `bounded_separable_clause` / `boundary` | Preserve exact anti-overwrite clause. |

## 4. File-level disposition
- Assertion groups / relationships: `6` / `6`.
- Final disposition: `BLOCKED_P3_REPAIR`.
- Preserved proof: canonical schema-extension anti-overwrite and current alpha degradation observation.
- Blocking defect: the principal reference-carriage and bounded-role claims are inferred from labels, generic dict specimens and default status rather than typed reference semantics, mandatory lineage/validation, or observed authority isolation.
- Return gate: P3 test repair after role-specific packet contracts and checks are defined; Gate D owns correction of defaulted identity behaviour.
- No implementation or test mutation executed.
