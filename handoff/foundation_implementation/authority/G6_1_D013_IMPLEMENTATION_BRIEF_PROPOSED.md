# G6.1 D013 — exact ratio and explicit predecessor closure

Date: 19 October 2026 — Australia/Melbourne.
Status: PROPOSED_DESIGN_AND_IMPLEMENTATION_AUTHORITY; NOT_YET_ADMITTED.

## 1. Intent, alternatives and bounded choice

Continue the accepted project, not a replacement foundation design. Following controlled D012 acceptance at5f998db, the next proposed G6.1 unit is controlled D013, whose existing K02 equation is `100 * D012 / D011`. It proves an actual derived-from-derived chain and its complete durable public lineage. It does not complete G6.1. No new source, mathematical equation, kernel or D dependency is introduced.

The reference existing producers return midpoint101 and spread2. The mathematically exact percentage is200/101, which has no finite Decimal expansion. This is a result-representation issue, not an IBKR input-range issue. Native prices remain the already accepted exact finite Decimal domain; no provider magnitude, tick, positivity or account/order assumption follows.

Alternatives assessed:

| Approach | Consequence |
| --- | --- |
| Reuse Decimal v1 and choose precision/rounding | Would introduce a new approximation convention into P_BASIC, which permits subject/member selection only. Ambient precision is not authority. Not selected. |
| Refuse every non-terminating result | Would silently shrink the admitted nonzero-denominator algebra domain. Not selected. |
| Add an exact rational public result and explicit predecessor request | Preserves the equation and complete finite-input ratio domain, leaves all v1 Decimal signatures/bytes intact and requires no dependency or numerical tolerance. Selected proposal. |

This is an additive architectural interface/storage extension, not a widening of the accepted Decimal result type. It supplies no general recursive carrier or implementation for later time/vector/transcendental families. Further result shapes still need exact authority.

Current owner standing delegation is owner-chat/20261019T222804/D012-and-standing-human-exceptions. It permits a later concrete delegated design/brief/plan disposition after actual review; it is not recorded here as acceptance of this unreviewed proposal. No proof, binding or production change may inherit the old brief's acceptance. Root EXEC_PLAN.md remains the sole active plan.

## 2. Authority, boundary and compatibility

Incorporated exact bytes are in §11. Original mathematical brief K02 fixes D013; §§8/11–15 fix history, no-look-ahead, complete typed lineage, compatible predecessors, immutable identity and public read/write separation. Its effective catalogue row D013 has no direct R dependency and exact ordered predecessor dependencies D011,D012, K02_ALGEBRA/P_BASIC/percent. Original catalogue digest is superseded by the effective accepted overlays already incorporated by version2; do not restore historical dependencies or reseal old objects.

Existing M02 remains sole semantic owner. Ingress intents, in order: modify:M02, modify:G01. Existing M02 package/public seam/dependency edge to M00 remain; this same-owner predecessor read creates no new cross-owner edge. No M00/A00/M01/private peer modification, numeric allocation or lifecycle change. New binding path is implementation/authority/G6_1_D013_IMPLEMENTATION_AUTHORITY_BINDING.yaml, with exact raw brief digest and genuine standing-delegation disposition reference only after admission.

Preserve every existing public symbol, signature, result type and namespace byte behaviour. Existing create_owner/create_reader remain v1 D011/D012 only under their own exact authorities; never return a rational object through MeasurementReadsV1 or MeasurementOwnerV1. New symbols below are additive exports of the same declared api.py seam. No old store is opened for migration or rewritten. Rational proof files are separate from both raw and v1 foundation files. No mixed physical-store compatibility is claimed.

## 3. Exact public records and validation

All new public records are frozen, slotted dataclasses, with fields in the order below and the existing exact runtime constructor discipline: no bool-as-int, coercion, Any/object/variadic public substitute, naive/non-UTC datetime or empty identity. Type/shape errors raise TypeError, malformed content raises ValueError. Exact unavailable requests return None. Storage faults use existing PersistenceFailureV1, retaining outcome_uncertain.

Reuse existing VersionRefV1, AuthorityArtifactRefV1, OwnerAdmissionV1, CalculationDefinitionV1, CalculationParameterSetV1, InputSelectionPolicyVersionV1, UnitConventionVersionV1, MemoryStorageV1, SQLiteStorageV1 and SQLiteReadStorageV1 without alteration.

ExactRatioV1 fields: numerator:int; denominator:int. Require denominator>0, gcd(abs(numerator),denominator)=1 and zero exactly0/1. This is a value carrier, not an implicit float/Decimal conversion API. A caller supplying2/2 or0/2 is rejected rather than silently canonicalised. Calculation itself constructs the canonical reduced pair. Arbitrary exact integers are supported subject only to truthful resource failure; never change the interpreter conversion limit or add a financial magnitude heuristic.

PredecessorEvidenceV1 fields:

- occurrence:DerivedSignalOccurrenceV1
- definition:CalculationDefinitionV1
- parameter_set:CalculationParameterSetV1
- input_selection_policy:InputSelectionPolicyVersionV1
- unit_conventions:tuple[UnitConventionVersionV1,...]
- projection_mappings:tuple[raw_api.RawSignalProjectionMappingV1,...]

These are complete public-read snapshots, not caller-supplied precomputed inputs. They permit independent validation and fresh recovery without a live raw reader or predecessor calculator.

RatioCalculationRequestV1 fields:

- derived_signal_id:str
- subject_instrument:str
- as_of_utc:datetime
- knowledge_cutoff_utc:datetime
- calculation_definition_version:str
- parameter_set_ref:VersionRefV1
- predecessor_occurrence_ids:tuple[str,...]

The predecessor tuple contains exactly two distinct nonempty IDs, in D011,D012 order at evaluation. No raw bindings, strategy context, arbitrary callbacks, result, numerical policy or hidden optional profile is admitted. The explicit IDs select immutable facts, not the numerically latest arbitrary rows.

RatioOccurrenceV1 has exactly all existing DerivedSignalOccurrenceV1 fields in their existing order and types, except result:ExactRatioV1, followed by predecessor_evidence:tuple[PredecessorEvidenceV1,...]. This is a separate declared dataclass, not a subclass accepted by old exact-type validation. Enforce outer direct raw_input_lineage=(), predecessor_occurrence_ids equal the two nested occurrence IDs in order, universe/window/supersedes=None, convention_refs=(), parameter_context_refs=(request.parameter_set_ref,), units=percent, result_shape=scalar_exact_ratio. Ultimate raw/configuration/unit/selection lineage is complete in the two nested evidence records, not falsely labelled new direct R dependencies.

## 4. Exact public facets and constructors

MeasurementRatioReadsV1 methods:

- get_derived_occurrence(derived_occurrence_id:str)->RatioOccurrenceV1|None
- list_derived_history(*,derived_signal_id:str,subject_instrument:str,effective_at_or_before_utc:datetime,knowledge_at_or_before_utc:datetime,limit:int)->tuple[RatioOccurrenceV1,...]
- get_calculation_definition(*,derived_signal_id:str,calculation_definition_version:str)->CalculationDefinitionV1|None
- get_parameter_set(ref:VersionRefV1)->CalculationParameterSetV1|None

History retains the existing exact-int limit1..1000 and inclusive effective/knowledge filters, ordered by effective_as_of_utc, knowledge_cutoff_utc, derived_occurrence_id descending, then truncated to limit, exactly as v1. Invalid shape/content raises TypeError/ValueError as v1; unknown lawful reads give None/(). No writer/materialise capability on the read facet.

MeasurementRatioOwnerV1 has reads:MeasurementRatioReadsV1 property and materialise(request:RatioCalculationRequestV1)->RatioOccurrenceV1|None.

Factories, keyword-only and exact signatures:

- create_ratio_owner(*,admission:OwnerAdmissionV1,predecessor_reader:MeasurementReadsV1,definitions:tuple[CalculationDefinitionV1,...],parameter_sets:tuple[CalculationParameterSetV1,...],storage:MemoryStorageV1|SQLiteStorageV1,utc_now:Callable[[],datetime])->MeasurementRatioOwnerV1
- create_ratio_reader(*,admission:OwnerAdmissionV1,storage:SQLiteReadStorageV1)->MeasurementRatioReadsV1

The writer registers only D013 definitions and its own parameter sets atomically. The predecessor reader exposes the already-declared same-owner public v1 methods; D013 neither invokes its writer nor gets direct M00 or predecessor SQL access. No arbitrary resolver/protocol or internal M01 import. A request does not recursively materialise missing predecessors in this bounded version; the public caller sequences real D011 and D012 producers first. Absence refuses. This proves the fixed topological chain without scaffolding a general graph engine.

## 5. Controlled definitions and admissible instances

New admission is exactly existing objectM02 plus the accepted raw digest of this brief, and no other digest. It is trusted offline construction, not a caller's power to grant programme authority. Wrong digest/object registration fails closed.

Definition D013 / D013-RELATIVE-SPREAD-1 / K02_ALGEBRA / equation string `100 * D012 / D011` / raw_dependencies=() / derived_dependencies=(D011,D012) / P_BASIC / percent / scalar_exact_ratio. authority_refs are exactly original mathematical brief and effective current catalogue paths/digests from §11, in that order. D013-RELATIVE-SPREAD-2 has the same content except definition-version string, solely for immutable version proof. All other definitions reject.

Parameter sets are exactly existing mmt-pilot-basic versions1/2, P_BASIC/NVDA/(NVDA), as already accepted; no rounding/precision field is added. Identical registrations are idempotent, different payload at one identity/version conflicts atomically. The complete registered set is persisted, not reconstructed from a hard-coded successful value by the reader.

Predecessors must both be actual existing-v1 occurrences under the exact accepted D012 brief digest a31c482d2dc4822539ede99e955761319585af4badea93b9fc279638e1e1f393 and objectM02/neutral_market_measurement_truth/v1. This expressly admits that prior authority as input compatibility, not as this new output's authority. Mixing original Gate5 and new-scope predecessor authorities refuses. Existing v1 D011-MIDPOINT-1/-2 and D012-SPREAD-1/-2 and their already accepted controlled configurations are the only predecessor definitions. These may vary independently when they retain their accepted same-equation payload; parameter, selection, mapping, unit and input content must satisfy the pair rules below. No old definition/version is silently mapped to a new one.

Reference sequence uses the exact accepted D012 controlled raw inputs/times/configuration, actual public M00 SQLite writer and public projections; actual public v1 writer materialises D011 and D012 under D012 authority. Then use their two returned IDs in a D013 request with NVDA, as-of/cutoff2026-10-16T01:00:00Z, definitionD013-RELATIVE-SPREAD-1, parammmt-pilot-basic1, clock2026-10-16T01:00:01Z. Expected ExactRatioV1(200,101). Proof stores are separate absent disposable files; no provider/native supply is asserted.

## 6. Predecessor selection, validation and exact arithmetic

For every request, require as_of<=cutoff<=UTCclock and exact D013/NVDA/registered definition/parameter domain. Read each explicit predecessor ID once through MeasurementReadsV1. Require returned ID matches requested ID and full exact declared type. Resolve its definition, parameter, selection, each mapping and each unit from the same public reader; absent/incomplete/ambiguous evidence refuses.

Validate each complete evidence snapshot against the accepted v1 controlled definition/configuration/content/identity/eligibility law, including exact canonical Decimal representations, lineage, content-hash-derived mmt1 identity, authority, equation and calculated time. A correctly shaped forged result, mismatched metadata or correctly rehashed wrong equation is not a lawful predecessor. Reconstruct the original logical request/configuration/lineage payload from its typed snapshots and check the existing identity and complete occurrence. Reuse the one owner-local authoritative v1 equation/content validator where suitable; do not add a competing midpoint/spread semantic path or import governance at runtime. The public seam is not power to attach an unchecked D label to any number.

Both predecessors must match the request's exact NVDA/as-of/knowledge-cutoff and parameter ref. They must use equal selection-policy content/ref, equal ordered raw lineage including projection identity/value/temporal/mapping/unit content, and equal ordered mapping/unit snapshots. Only each predecessor's own D ID, accepted definition version/hash, result, calculated time and consequent occurrence ID differ. Each calculated time must be at/after its knowledge cutoff and not after the new calculation's clock. Defining one pair from different quote facts or incompatible versions refuses, even if the ratio would happen to equal the reference result. This is complete controlled input compatibility, not latest-feed/native history certification.

After validation, compute the accepted equation solely from the two typed predecessor results. Convert each finite Decimal to its exact signed integer coefficient and power-of-ten ratio, compute100*spread/midpoint with integer operations, reduce by gcd, move denominator sign to numerator, and emit canonical zero0/1. Midpoint0 (including signed zero) gives no occurrence. Nonzero negative midpoint and crossed/negative-price inputs follow the equation; no positivity/abs/tick/magnitude heuristic. Ambient Decimal precision/rounding/traps must not affect the result or ID. Resource/arithmetic failure produces no occurrence, never a rounded value.

Examples independently expected from accepted equations: bid1/ask3 -> midpoint2/spread2 ->100/1; bid102/ask100 ->-200/101; bid-3/ask-1 -> midpoint-2/spread2 ->-100/1; equal nonzero prices ->0/1; bid-1/ask1 -> zero midpoint ->None. Scaled/trailing-zero native inputs retain their exact predecessor representation and identity even when the reduced ratio is numerically equal.

## 7. Canonical identity, durable state and complete readback

Namespace neutral_market_measurement_truth/exact_ratio/v1; opaque ID prefix mmtr1:. Use canonical sorted-key ASCII UTF8 JSON with fixed compact separators/allow_nanFalse as existing v1. Preserve all existing v1 tags/opaque identity factories and Decimal tuples in nested evidence. ExactRatioV1 encodes exactly {kind:exact_ratio,numerator:<canonical signed integer text>,denominator:<canonical positive integer text>}; no plus sign/leading zeros/negative zero. Encode/decode integer digits without relying on Python's bounded decimal string conversion. Public integer fields remain ints. Noncanonical ratio/tag/payload bytes refuse.

Logical identity payload has exactly owner_object_id, owner_namespace, implementation_brief_sha256, request, definition_content_sha256, parameter_set, predecessor_evidence. Its SHA256 determines mmtr1 ID. Exclude this new calculation's calculated_at from logical identity so later-clock retry returns the original complete occurrence/time. Include full two predecessor evidence snapshots, not only a list of D labels or floating values. Output payload also preserves full new occurrence, exact tagged ratio and all metadata. Verify complete typed equality and logical/content hashes/indexes at decode, not merely a valid JSON shape.

Use a new owner-local SQLite file with application_id0x4E560003, user_version1, DELETE journal, synchronousEXTRA, foreign_keysON, busy_timeout0, STRICT tables and per-operation independent read/write connections. Writer creation is exclusive-create only when createTrue; createFalse reopens only an existing matching file. No overwrite, symlink, URI/query path, directory or special-file target. Read-only uses URI mode=ro plus query_onlyON and never creates/mutates a file. Existing v1/raw files and new ratio files must reject one another's writer/read construction. This is owner/type separation in one trusted application, not OS/credential/hostile-code isolation.

Exactly three tables with the existing immutable insert-only transaction pattern:

- mmt_ratio_definition_v1: owner_namespace TEXT, derived_signal_id TEXT, calculation_definition_version TEXT, payload BLOB, content_sha256 TEXT; composite namespace/D/version primary key.
- mmt_ratio_parameter_v1: owner_namespace TEXT, context_id TEXT, version TEXT, payload BLOB, content_sha256 TEXT; composite namespace/context/version primary key.
- mmt_ratio_occurrence_v1: derived_occurrence_id TEXT primary key; owner_object_id TEXT, owner_namespace TEXT, implementation_brief_sha256 TEXT, derived_signal_id TEXT, calculation_definition_version TEXT, subject_instrument TEXT, effective_as_of_utc TEXT, knowledge_cutoff_utc TEXT, logical_identity_payload BLOB, logical_identity_sha256 TEXT, payload BLOB, content_sha256 TEXT; foreign key namespace/D/version to the definition table.

All fields NOT NULL. All three tables have BEFORE UPDATE/DELETE abort triggers. Validate exact declared table/trigger schema and foreign-key integrity; no schema downgrade, extra-table tolerance or silent repair. Definitions/parameter snapshots referenced by each occurrence must resolve exactly; nested predecessor evidence is persisted as part of each occurrence, not an SQL foreign key into another store. Store the full registered definitions/parameters and recover them through public getters without caller re-registration.

Registration is one atomic immutable transaction; a conflicting existing definition/parameter rolls back every new registration. New occurrence inserts use BEGIN IMMEDIATE and immutable same-ID/same-content idempotence. A later retry must preserve first calculated_at; conflicting same-ID content refuses. Precommit failure rolls back, postcommit lost acknowledgement raises PersistenceFailureV1(outcome_uncertain=True), confirmed noncommit is false, and retry resolves the one original fact. Competing identical first public materialisations cannot create two facts; a truthful busy failure is permitted, followed by retry of the same fact. Reader validates every stored fact's full predecessor evidence, equation, identity/index/hash/representation and exact definition/parameter links; no raw reader, live calculator or precomputed fixture is required after writer exit.

## 8. Bounded proof-control addition and implementation surfaces

Preserve original config/product_proof/claims.json, all existing brief/binding/contract/generation bytes and strict runner/outcome/schema semantics. Add one fixed optional descriptor config/product_proof/market_measurement_d013/claim.json with exactly schema_version1.0, claim_idneutral_market_measurement_truth_d013, this brief_path, §2 binding_path, contract_path from §10, physical_roottests/product/market_measurement_d013, admission_pathconfig/product_proof/market_measurement_d013/admission.json. No caller-discovered arbitrary descriptors or schema relaxation. Exact native intents/brief/contract marker/target must validate before any claim partition, including when an original claim is selected. Descriptor absent plus any Python source/symlink in this exact root must reject. All present extensions share the complete disjoint physical partition; reject duplicate family/proof/root ownership and cross-claim generations. D012 remains separately exact-bound and all original claims still resolve unchanged.

The new generation directory is config/product_proof/market_measurement_d013/generations/, beginning immutable0001 only after independent physical proof adequacy/admission. Null admission is incomplete, not RED/GREEN. Current bounded pre-admission fixture helper may explicitly reset only both optional extension trees/descriptors in disposable copies, preserving its original missing-target universe; actual-state direct multi-claim checks must separately establish global ownership. No real proof is removed.

Permitted code surfaces: api.py additive records/facets/exports/factories; new _rational.py for exact controlled service/ratio codec/validation; new _rational_sqlite.py for this isolated storage profile; existing _evaluation.py only indispensable additive ratio-tag support preserving v1 bytes; _catalogue.py/_sqlite.py only indispensable reuse extraction preserving original public/semantic behaviour, with an evidenced bounded root ruling before change. Prefer no modification of existing v1 behaviour. config/architecture/modules.yaml may truthfully describe admitted D013 result scope/state roles, without new edge/lifecycle/composition. G01 tools/product_proof_claims.py may add the fixed optional descriptor/common combined-claim handling; retain original _authority and strict runner. Existing tests/architecture/test_proof_control.py owns new falsifiers. No other runtime/schema/dependency/pin/vendor/M00/A00/M01 file is in scope.

## 9. Independent proof and acceptance conditions

Complete physical source must be authored and independently reviewed before generation admission or production behaviour. _support.py provisions literal public records/configuration only; no pre-materialisation, automatic predecessor calculation or expected-result computation. Tests themselves sequence real M00 admission, D011 then D012 production, public predecessor reads, then D013 evaluation. An injected predecessor adapter may isolate refusal dimensions but cannot establish real producer integration or durability.

D013-P01 actual full public producer chain, exact200/101 and full typed lineage/configuration/authority/units/shape. Retain actual source-independent arithmetic expected answers.

D013-P02 each missing/wrong owner/authority/D/order/definition/version/subject/as-of/cutoff/parameter/selection/mapping/unit/projection/representation/hash/time dimension independently refuses, followed immediately by unchanged empty and nonempty D013 history. This ratio factory permits onlyD013: all other125foundation identities, includingD011/D012, and83downstream identities refuse through it. The original v1 factories retain their existingD011/D012 scope and still refuseD013. Thus the remaining123foundation identities stay unenabled across both surfaces. Full native metadata/representation falsifiers, not only a fake None adapter. Lawful independent definition-version alternatives and complete same-version pair controls remain.

D013-P03 canonical positive/negative/zero/nonterminating ratios, denominator/sign/reduction/type validation and exact magnitude/exponent witnesses independent of ambient Decimal traps. Reject rounding/truncation/finite-only output shortcuts. These are calculation/storage-domain cases, not IBKR magnitude claims. Include original Decimal representations0/-0/trailing zeroes and prove their exact nested lineage is not normalised away.

D013-P04 direct materialise→later-clock retry; independently change D013 definition version, exact predecessor definition IDs, same-source raw observation identity/representation and compatible parameter chain; old/new facts remain exact. For dimensions whose compatibility requires joint predecessor changes, prove single mismatched reference refusal separately rather than claim an isolated positive identity experiment. Same-ID/content conflict, atomic configuration conflict and definition getters are required.

D013-P05 actual separate SQLite stores; committed result visible independently; writer child creates/materialises/exits before fresh read-only child receives only path/admission/IDs and recovers full typed occurrence, every registered definition/parameter and bounded history without calculators/readers. Exercise native precommit rollback, postcommit uncertainty/idempotent recovery, and genuine competing identical first writes with a barrier before first COMMIT and no preexisting fact. Independently corrupt payload, content hash, logical hash, index, rational canonical representation, nested predecessor/configuration, correctly rehashed wrong equation and wrong-owner file. Each refuses rather than normalising or returning a partial fact.

D013-P06 additive static types: valid new ratio factory/read/request/result plus existing Decimal factory/read remain exact and compatible. Negative specimen must have exact reviewed diagnostic sites/codes/count and no import/dependency/Any loophole: old reader/result cannot satisfy ratio facet, new ratio cannot masquerade as Decimal or writer-as-reader/wrong storage. Actual complete original foundation/D012/M00 strict aggregates and kernel promotion required on the exact candidate; original governed bytes remain unchanged. Fresh review directly sequences at least one ordering/absence transition bypassing all Worker convenience composition and inspects relevant recurrence lineage.

Record actual RED before each behaviour change; missing import/dependency/control/admission is infrastructure, not intended semantic RED. Run complete strict new aggregate plus all three original aggregates, full source/control mypy, scoped changed-source/proof Ruff and architecture promotion; standard full Ruff's inherited two M01E501 findings stay disclosed. No skip/xfail/xpass/deselection/governed mutation can establish aggregate success. Independent candidate review precedes concrete delegated acceptance under standing authority. None of this is G6.1/full126/native completion or permission for G6.2 before its actual predecessor.

## 10. Incorporated proof contract

D013-PROOF-CONTRACT-SHA256: 7eab93055c2e2f19e74563ec9588bbc04dfdb8664d4c8e3279527f70917d4a47

Path: handoff/foundation_implementation/authority/G6_1_D013_PROOF_CONTRACT_PROPOSED.json. Physical family tests/product/market_measurement_d013/test_ratio.py, required _support.py plus typing/valid_seam.py and typing/invalid_seam.py. Exact claim neutral_market_measurement_truth_d013. Future strict entry: python tools/run_product_proof_gate.py --aggregate neutral_market_measurement_truth_d013. No physical proof, binding, descriptor, generation or implementation exists by this document's presence.

## 11. Exact incorporated byte objects

| Path | SHA256 |
| --- | --- |
| handoff/foundation_implementation/authority/SQLITE_IMPLEMENTATION_BRIEF_PROPOSED.md | 3ad4cdc9ffba4cf91ff9a27edf1dd3b1a9824a421514bb4b5a2cc1b9c504f233 |
| handoff/foundation_implementation/authority/FOUNDATION_IMPLEMENTATION_BRIEF_PROPOSED.md | 282f7d73c5e2fdf36ded43781665764eaf95d4a35f687f99990b87c59f744ed7 |
| handoff/foundation_implementation/authority/G6_1_D012_IMPLEMENTATION_BRIEF_PROPOSED.md | a31c482d2dc4822539ede99e955761319585af4badea93b9fc279638e1e1f393 |
| handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md | 603b850802a418780109095e7ae69bcece449da79fb24140a6d50297605e927c |
| handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv | 67bacbcf77afa766cec220a8d4a0f9589c9568d4a1f5c5818334915adf72e549 |
| handoff/foundation_implementation/authority/G6_1_D013_PROOF_CONTRACT_PROPOSED.json | 7eab93055c2e2f19e74563ec9588bbc04dfdb8664d4c8e3279527f70917d4a47 |
| config/product_proof/claims.json | ad62fcd57ce837771f732864cbae7e47d9721f0311d21c3b96e05881d83cc317 |
| implementation/authority/FOUNDATION_IMPLEMENTATION_AUTHORITY_BINDING.yaml | 7c7fa7df69e75825853bf7b355343d9b6f793beab247b37223bfa71737248b87 |
| schemas/accepted_brief_product_proof.schema.json | 7bd1bacef89972e492299afc7c44d4c7fcbb72dfdb9d593a5afde286215067dc |
| config/product_proof/market_measurement_d012/claim.json | c79983db5d6c1002f5230dfcee5f036601cea96a826a8e17df18a1924aef9561 |
| implementation/authority/G6_1_D012_IMPLEMENTATION_AUTHORITY_BINDING.yaml | f1eedec4aa2fcc543a66b709ecd925dd713d01ecabf19c776d5f1b07d3e15f8e |

Read all in-scope primary authority before action; hashes do not replace semantic review. Other version3 incorporated objects remain bound transitively; old source fingerprints are provenance rather than a freeze on a newly authorised additive seam. This proposal has no self-digest; its actual final raw digest is recorded externally after documentary verification. It requires exact design/authority/root-amendment disposition under standing delegation before behaviour. Frozen guardrails/agents remain unchanged; no alternate skill plan/ledger is introduced.

TS: 19-10-26 23:10
