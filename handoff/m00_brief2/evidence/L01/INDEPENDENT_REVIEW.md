# Current disposition — L01 documentary PASS

Accepted exact revised `fixture_manifest_v1.json` SHA-256 `0628fb8a7196b44d0322ea438db7a180eb0f97b50f36cece0b2d0739dd0f4e04`. Independent expected oracle only: `EXPECTED_SYNTHETIC_OUTPUT_AUTHORISED`; actual M00 output and SQLite proof remain `NOT_ATTEMPTED`. The initial return and its first witnesses remain below unchanged, followed by repair/rereview evidence.

# L01 independent oracle review — RETURN_TO_WORKER

Reviewer `/root/l01_oracle_review`, 27 October 2026. Reviewed candidate fixture manifest SHA-256 `996b6984102fbdbf9e0ac9d7db27adf6479f312fb46eb48ef21ddd9127819ca1`, on accepted L00 baseline `487b822`. This is documentary oracle review only. L01 is not accepted; dependent L02 execution must wait for closure and hash-specific rereview.

## Findings

1. **ISOLATED — independent negative fixtures and absence expectations are not materialised.** Root L01 requires “Materialise N01–N18 independent perturbations and control fixtures in separate files”. `fixtures/negative/expectations_v1.jsonl` contains 18 prose expectations plus a generic base-scenario/isolation string. It specifies no concrete replacement occurrences, query arguments, cutoff values, duplicate identities/receipts/sequences, changed payload, collector receipt carrier, or machine-readable expected absence/rejection results. N11 even names depth scenario A4 as the base for its asynchronous quote-contract perturbation. No absence/rejection rows exist in the expected files. This does not fix the independent negative oracle before production exercise. Closure requires concrete isolated operands/query sequences and exact expected outcomes for each obligation, preserving positive bytes; N06 must cover its listed missing roles and N18 both carrier branches. Materialisation need not run product code.

2. **ISOLATED — the promised typed output schema is not defined.** `output_schema_v1.json` constrains `value` only to `{"type":"object"}`. `native_value_contract`, `null_and_absence`, and `canonical_order` are descriptive custom annotations, not validating schemas. Thus an observation row with `value={}` satisfies every declared validation constraint; so do arbitrary invalid Decimal/bool/datetime payloads inside it. Receipt fields are bare strings without an explicit datetime tag or validating type contract; absence/rejection/control shapes are unspecified. Root L01 explicitly requires tagged Decimal/int/bool/aware UTC datetime, null and explicit absence entries. Closure requires an enforceable versioned contract for all emitted kinds and typed values, with UTC receipt and null/absence distinction unambiguous. An explicit field schema can establish receipt datetime type without an extra redundant tag. No JSON Schema validator was installed/executed in this review; the empty-value witness follows directly from the full schema's declared constraints.

Lineage inspected: `git log --oneline --all -- handoff/m00_brief2` contains only accepted L00 `487b822`; no earlier L01 repair/reviewer lineage was found. Both findings are new mechanisms rather than a recurrent prior L01 repair class. The shared closure proposition is that the independent expected contract must be concrete and sufficiently constrained before actual production output is observed.

## Verified positive-oracle findings

Read governing GUARDRAILS, root AGENTS and current EXEC_PLAN, original brief in full (with repeated bounded reads where tool output truncation required), L00 review, and the complete L01 authoring/input/expected/mapping/schema/manifest/control/negative files. No nested handoff AGENTS instructions were present. Static inspection of `project_raw_value` confirmed that explicit per-occurrence catalogue roles prevent the declared price/size adaptation from cross-projecting bid and ask merely because native paths coincide. No M00 import or execution occurred.

Independently compared the original brief's literal rows against all 36 input observations: IDs, family versions/namespaces, subjects/right/expiry/multiplier, callback/tick type, receipt/date, scope/sequence, native values/types and Decimal lexical scales, source time/null/timezone, requested exchanges and MPIDs. Literal values agree. A1's native source text remains `2026-10-20T12:40:00.000Z`; normalising typed receipt display to six digits does not alter native source text. A2/A3 retain four independent occurrences each; tickPrice/tickSize use native price/size with a declared field adaptation and intended per-occurrence R roles. A5 is separate from A2/C1, B keeps its date/subjects/provider/SMART variant and seven literal IDs, and C keeps family V2. C2/C3 preserve side-relative positions across ALPHA/BETA and distinguish MPID from requested exchange. No direct PUT, live IBKR, actual output or SQLite readback claim is made.

Compared all 155 expected projection rows to their original literal event operands and mapping definitions: exact tagged native value, role/path, units, occurrence identity, source, receipt, scope/sequence, temporal fields, mapping ID/version and selection identities. Expected observation rows exactly equal their corresponding inputs. Each scenario has its own mapping group; B has separate STK/CALL groups. Declared synthetic request/generation/reqId choices remain collector metadata rather than authenticated broker identities. `build_oracle.py` imports pathlib/json/hashlib, not M00, and has no product invocation. It was read, not run by this reviewer.

| Scenario | Observations | Projections |
| --- | ---: | ---: |
| A1 | 1 | 4 |
| A2 | 4 | 4 |
| A3 | 4 | 4 |
| A4 | 4 | 20 |
| A5 | 3 | 15 |
| A6 | 2 | 10 |
| B | 7 | 35 |
| C1 | 3 | 15 |
| C2 | 4 | 24 |
| C3 | 4 | 24 |
| Total | 36 | 155 |

Five separately stored controls contain two reqId-shaped native errors 317/316 and three explicitly collector-origin reconnect/gap/restart events. Their receipts/sequences follow A4 and restart links G1 to G2; no R187 error substitution is present. These are documentary control specimens, not evidence of public discovery. Eighteen distinct negative obligation IDs exist, but finding 1 prevents accepting them as materialised fixtures.

Independent stdlib JSON/hash/arithmetic commands parsed every JSON/JSONL file, verified all ten manifest-listed file SHA-256 values, checked one expected observation per positive input, all per-event projection counts, exact projection operands and lineage fields, and the individually versioned mapping IDs. Family totals are A 18/57, B 7/35, C 11/63. Current file hashes match the candidate manifest; hashing establishes byte identity, not acceptance. Expected files contain observations/projections only. No product tests, SQLite sessions, production source changes, product proof admissions or actual-output generation were performed.

Required next disposition: repair only the documentary L01 contract defects, retain this first review as failure evidence, regenerate hashes for changed authorised artifacts and obtain independent rereview before checkpoint/advancement. Positive literal agreement is useful verified partial progress, not L01 acceptance.

## Repair rounds and final independent rereview

The worker added 18 concrete `Nxx_v1.jsonl` operand/query specifications, preserving all six A/B/C input/expected hashes and mapping manifest hash from the first review. The negative summary is now explicitly `index_only` and links each relative concrete specification; N11 correctly selects A2 and replaces its fourth occurrence's contract/right. N06 declares one-field-at-a-time fresh-store variants with every other native fact preserved exactly; N18 fixes both missing-carrier and valid typed collector-receipt branches. Other specifications fix the tied ID, post-cutoff receipt/sequence, replay conflict value, update/delete/zero-size operands, selectors and control references. These documents define the expected assertions; successful public execution is reserved for the assigned later leaves.

The worker also added five expected control output rows separate from the positive 36/155 and expanded the schema to closed kind-specific observation/projection/control/absence/rejection structures, required lineage fields, discriminated native tags and null/UTC constraints. Static architecture schema validation is documentary validation, not M00 product execution. Source timezone and temporal/source values remain compared exactly by the independent oracle even where the structural schema permits a broader string.

During bounded rereview the reviewer identified a related lexical-schema gap: initial repair patterns depended on the kernel validator's `re.fullmatch` while portable JSON Schema patterns use search semantics. Prefix/suffix junk could therefore satisfy unanchored Decimal/UTC patterns in a portable consumer. This was classified **RECURRENT_CLASS**, materially related to finding 2's permissive schema mechanism. The class-level closure proposition was that *every published native tag/lexical field and every output-kind field contract must encode the intended representation independently of validator convenience*. Worker repaired every schema pattern recursively with start/end anchors, rather than only the newest two witnesses. The N06 one-at-a-time clarification and stale N11 index base were resolved in the same bounded documentary round. No product/source correction was attempted.

Final independent command used stdlib JSON, pathlib, hashlib and copy plus unchanged `nvda_desk.architecture.schema.validate_instance` (not raw-observation/M00 code). It verified all 29 manifest-listed hashes, all 196 expected rows (36 observations, 155 projections, five controls), every schema pattern's anchors, and all 18 relative concrete-spec links/IDs/index flags. Five independently chosen malformed witnesses were rejected: empty projection value, Decimal `junk1junk`, receipt `junk2026-10-20T12:39:59.100000Zjunk`, bool value integer 1, and NoneType value string `null`. The first reviewer command used the wrong relative base for summary specification links and raised FileNotFoundError after its hash/schema checks; corrected resolution against the index file's parent passed. This was a reviewer command error, not a fixture failure.

Worker `author-check-final.log` additionally records 196 rows/29 hashes/six malformed witnesses/18 specifications after material schema/spec repairs. Reviewer did not rerun product checks or the authoring mutation script. Positive input and expected hashes are byte-identical to the independently table-compared initial candidate, so the original full 36/155 value/type/identity review remains applicable. The only generated fixture changes are the separately reviewed control/negative/schema contract additions and index corrections.

**Final disposition: PASS for L01 immutable independent expected-oracle contract**, exact manifest hash `0628fb8a7196b44d0322ea438db7a180eb0f97b50f36cece0b2d0739dd0f4e04`. No unresolved L01 documentary finding remains. No M00 admission, projection execution, SQLite persisted readback, control-discovery runtime, actual output, live entitlement or PostgreSQL certification is granted. L02 may begin only after the main worker commits and exposes the required independently accepted cumulative L01 checkpoint.
