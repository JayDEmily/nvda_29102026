# G6.1 D014 — controlled direct-raw exact ratio

Date: 20 October 2026, Australia/Melbourne.
Status: PROPOSED_FOR_INDEPENDENT_DESIGN_REVIEW; NOT_IMPLEMENTATION_ADMISSION.

## 1. Intent, alternatives and boundary

Continue the existing accepted root plan and controlled D011/D012/D013 implementation, not a new foundation. D014 is the next proposed direct-raw algebra unit because its fixed equation consumes two raw values and needs the now-proved exact ratio carrier, unlike the existing D013 predecessor-only facet. Numerical ID order alone does not establish this choice. This bounded unit proves direct-raw exact-ratio selection, immutable identity and durable readback; it is not a complete G6.1 schedule.

Accepted K02 fixes D014=(bid_size-ask_size)/(bid_size+ask_size), with exactly R033,R036 and no derived predecessor, P_BASIC and catalogue units "-1 to 1". For controlled bid_size2/ask_size1 the exact result is1/3. Reusing Decimal would require unauthorised rounding or silently refusing nonterminating results. Widening the old Decimal result or the fixed two-predecessor D013 request would break existing contracts. Selected design: additive direct-raw ratio occurrence/read/write facet, existing CalculationRequestV1/raw-lineage/configuration records and ExactRatioV1, separate owner-local SQLite file. Do not build a general formula/result framework.

The controlled source is explicitly not IBKR. Exact finite Decimal inputs are preserved, including fractional sizes, signed zero and trailing-zero representation. Arithmetic uses the fixed signed equation and nonzero-denominator law without inventing integer-only, tick, magnitude, precision, positivity or clipping rules. Nonnegative input pairs naturally yield a result in[-1,1]; that observation is not an extra constructor/selection bound. Signed artificial algebra witnesses do not certify negative native displayed sizes. Native provider validity/sentinels/units/scale/time/market-data state need their own admitted mapping; this brief supplies none. No claim of physical size eligibility is made by controlled arithmetic.

Owner standing delegation owner-chat/20261019T222804/D012-and-standing-human-exceptions permits a concrete later design/brief/root disposition after actual review. It neither accepts these currently proposed bytes nor waives proof/review. Exact current root EXEC_PLAN.md and G5_EXECUTION_RECORD.md remain sole plan and ledger. No additional approval prompt is needed for a routine human-only checkpoint once its actual evidence exists.

## 2. Governing meaning and compatibility

Incorporated accepted mathematical brief SHA603b850802a418780109095e7ae69bcece449da79fb24140a6d50297605e927c, effective catalogue SHA67bacbcf77afa766cec220a8d4a0f9589c9568d4a1f5c5818334915adf72e549 and foundation version2/SQLite version3 supply K02, raw projection law, immutable versions, typed complete lineage, no-look-ahead, history, public/read-write separation, trusted-application storage and all retained target/hold boundaries. Historical draft headings/old catalogue/PostgreSQL text do not override accepted overlays.

Existing M02 is the sole owner; intent order modify:M02 then modify:G01. Future exact binding implementation/authority/G6_1_D014_IMPLEMENTATION_AUTHORITY_BINDING.yaml must bind this actual raw digest and a genuine concrete delegated disposition. No new ID/package/edge/lifecycle, M00/A00/M01/private peer change, dependency/pin/vendor change, provider acquisition/integration/live/account/order effect, populated-store migration/retirement/main merge. CPython3.12.14 and existing exact offline dependencies remain.

All old public declarations/bodies/types/namespace/identities/store bytes retain their accepted behaviour. Existing create_owner/create_reader keep their exact D011/D012 authority scope; existing create_ratio_owner/create_ratio_reader retain D013-only semantics, two complete predecessor snapshots and their isolated profile. Do not pass direct raw facts through the predecessor facet or return a rational result as Decimal. Existing public-AST preservation canaries are bounded to their accepted additive units, not new permanent legislation.

## 3. Exact additive public seam

All names are exports of existing nvda_desk.market_measurement_truth.api. Reuse unchanged OwnerAdmissionV1, VersionRefV1, AuthorityArtifactRefV1, CalculationDefinitionV1, CalculationParameterSetV1, InputSelectionPolicyVersionV1, UnitConventionVersionV1, RawInputBindingV1, RawInputLineageV1, CalculationRequestV1, RawProjectionReaderV1, ExactRatioV1, MemoryStorageV1, SQLiteStorageV1, SQLiteReadStorageV1 and PersistenceFailureV1.

RawRatioOccurrenceV1 is a separate frozen/slotted dataclass with exactly DerivedSignalOccurrenceV1's existing field names/order/types, except result:ExactRatioV1. It is neither its subclass nor RatioOccurrenceV1. Enforce complete two-item ordered R033/R036 raw_input_lineage, predecessor_occurrence_ids=(), parameter_context_refs=(request.parameter_set_ref,request.input_selection_policy_ref), convention_refs containing every unique selected unit ref sorted by(context_id,version), universe/window/supersedes=None, units="-1 to 1", result_shape="scalar_exact_ratio". Existing strict constructor discipline applies: exact declared types/no bool-as-int/coercion/empty identity/naive or non-UTC datetime; type errors TypeError, malformed content ValueError. ExactRatioV1 remains canonical reduced signed integer numerator/positive denominator, zero0/1.

MeasurementRawRatioReadsV1 has exactly MeasurementReadsV1's public methods and keyword structure, with only occurrence return replaced by RawRatioOccurrenceV1:

- get_derived_occurrence(derived_occurrence_id:str)->RawRatioOccurrenceV1|None
- list_derived_history(*,derived_signal_id:str,subject_instrument:str,effective_at_or_before_utc:datetime,knowledge_at_or_before_utc:datetime,limit:int)->tuple[RawRatioOccurrenceV1,...]
- get_calculation_definition(*,derived_signal_id:str,calculation_definition_version:str)->CalculationDefinitionV1|None
- get_parameter_set(ref:VersionRefV1)->CalculationParameterSetV1|None
- get_input_selection_policy(ref:VersionRefV1)->InputSelectionPolicyVersionV1|None
- get_unit_convention(ref:VersionRefV1)->UnitConventionVersionV1|None
- get_projection_mapping(ref:VersionRefV1)->raw_api.RawSignalProjectionMappingV1|None

History: exact-int limit1..1000, inclusive effective/knowledge filters, descending effective_as_of_utc/knowledge_cutoff_utc/derived_occurrence_id, truncate after ordering. Unknown lawful reads None/(); invalid arguments TypeError/ValueError. No materialise on reader.

MeasurementRawRatioOwnerV1 has reads:MeasurementRawRatioReadsV1 property and materialise(request:CalculationRequestV1)->RawRatioOccurrenceV1|None.

Exact keyword-only factories:

- create_raw_ratio_owner(*,admission:OwnerAdmissionV1,raw_projection_reader:RawProjectionReaderV1,definitions:tuple[CalculationDefinitionV1,...],parameter_sets:tuple[CalculationParameterSetV1,...],input_selection_policies:tuple[InputSelectionPolicyVersionV1,...],unit_conventions:tuple[UnitConventionVersionV1,...],raw_projection_mappings:tuple[raw_api.RawSignalProjectionMappingV1,...],storage:MemoryStorageV1|SQLiteStorageV1,utc_now:Callable[[],datetime])->MeasurementRawRatioOwnerV1
- create_raw_ratio_reader(*,admission:OwnerAdmissionV1,storage:SQLiteReadStorageV1)->MeasurementRawRatioReadsV1

No callback/formula policy, automatic predecessor production or context/model/strategy input. Store exceptions retain truthful outcome_uncertain; unavailable lawful requests returnNone without a fact.

## 4. Exact controlled registrations and request

Admission is only M02 plus this accepted brief's raw digest after actual admission. Wrong object/digest rejects registration; no fallback to older authority.

Definition: D014/D014-SIZE-IMBALANCE-1/K02_ALGEBRA/equation "(R033 - R036) / (R033 + R036)"/raw_dependencies=(R033,R036)/derived_dependencies=()/P_BASIC/units "-1 to 1"/shape scalar_exact_ratio. D014-SIZE-IMBALANCE-2 differs only in definition-version spelling for immutable version proof. authority_refs are mathematical brief then effective catalogue, exact paths/digests in§10. All other definitions reject.

Each following configuration has exact versions1/2 only:

- CalculationParameterSetV1("mmt-size-basic",version,"P_BASIC","NVDA",("NVDA",)).
- InputSelectionPolicyVersionV1("mmt-size-selection",version,("subject_instrument",),timedelta(seconds=60),timedelta(seconds=10),("true_instant",),(),"foundation-size-fixture","cash_size_v1","foundation-size-fixture/cash_size_v1",100,1000).
- UnitConventionVersionV1("mmt-size-shares",version,"shares","shares",Decimal("1"),Decimal("0")).
- Mapping IDs mmt-size-bid / mmt-size-ask, respective R033/R036, provider foundation-size-fixture, source_variant cash_size_v1, native_field_path=("quote","bid_size") / ("quote","ask_size"), native_units shares, selection_identity_field_paths=(). Use existing exact RawSignalProjectionMappingV1 field order/types.

Registrations are exact-content immutable/idempotent and atomic across definitions/all configurations. A conflict rolls back every new member. Each binding may independently select lawful mapping/unit versions1/2: no blanket equal-version requirement between bid and ask. Unit snapshots in identity are unique and sorted by(context_id,version); projection mappings and raw lineage follow ordered R033,R036 bindings. No precision/free mathematical parameter, rate inference or native provider spelling is introduced.

Reference request uses D014/NVDA/as-of=cutoff2026-10-16T01:00:00Z/definition D014-SIZE-IMBALANCE-1/param mmt-size-basic1/selection mmt-size-selection1/context_refs=()/ordered raw bindings R033 then R036, mapping refs mmt-size-bid1/mmt-size-ask1 and shared mmt-size-shares1/subject NVDA. Clock2026-10-16T01:00:01Z. Actual public M00 records have bid Decimal("2") event T-2s/receipt T-1s/sequence1, ask Decimal("1") event T-1s/receipt T/sequence2, true_instant/UTC/exact ISO-Z timestamps, fixture source/scope/native_units shares and respective R tag. Expected ExactRatioV1(1,3). Fixtures are literal controlled records, not observed provider collection.

## 5. Raw selection, eligibility and arithmetic

Require as_of<=cutoff<=clock, registered exact D014/NVDA/definition/parameter/selection, no extra contexts, exact two distinct ordered bindings and compatible registered mappings/unit definitions. All other208identities, including D011/D012/D013 and all83downstream identities, refuse through this factory. Prior factories continue refusing D014.

Consume only public bounded M00 projected history; no raw/private SQL/provider parsing fallback. Reuse unchanged _selection.select/eligible for its already-proved exact type/provider/variant/subject/mapping/field/native-unit/Decimal/UTC metadata, event<=asof, receipt<=cutoff, event<=receipt, freshness60s, complete stable pagination/deduplication, equal-rank ambiguity and page-cap refusal. Verify selected pair event skew<=10s. Preserve full exact native projection and canonical conversion plus mapping/unit refs in RawInputLineageV1. Native exact Decimal tuples must not be normalised away. Unit conversion is the exact configured identity; magnitude does not supply units. Reuse must not introduce the old price-only catalogue restriction: it is the new registrations that bind R033/R036/shares.

Compute bid_size-ask_size and bid_size+ask_size using integer coefficients/aligned exponents, then reduce their quotient by gcd with positive denominator. No ambient Decimal precision/rounding/traps, float conversion, guessed quantisation or global integer-string-limit mutation. Denominator0, including signed zero, producesNone. Preserve signed algebra; never abs/clamp. Resource/arithmetic failure yields no occurrence or a truthful persistence failure where applicable, never rounded output.

Independent examples:2/1→1/3;1/2→-1/3;3/1→1/2;equal nonzero→0/1;2/0→1/1;0/2→-1/1;0/0→None; artificial1/-1→None. Fractional2.50/1.25→1/3, retaining those raw Decimal tuples. Signed artificial -3/1→2/1 is an algebra witness only, not certification of physical negative displayed quantities. Large/tiny exponents and >4300-digit rational components must retain exact wire output without special limits.

## 6. Identity, public state and canonical codec

Namespace neutral_market_measurement_truth/raw_exact_ratio/v1; prefix mmtraw1:. Canonical sorted-key ASCII UTF8 JSON, compact separators/allow_nanFalse, exact existing opaque/Decimal/datetime/timedelta tags and D013 exact_ratio integer-text tag. Reuse the single existing ratio codec; only add the new exact dataclass to its decode allowlist. No old encoding/decoding behaviour changes and no duplicated competing integer codec.

Logical identity has exactly owner_object_id,owner_namespace,implementation_brief_sha256,request,definition_content_sha256,parameter_set,input_selection_policy,unit_conventions,projection_mappings,raw_input_lineage. Own calculated_at excluded; complete request/configuration and raw projection/native/canonical representations included. SHA256 gives opaque ID. Later-clock retry returns first complete fact/time; conflicting same-ID logical/content refuses, changed material input/definition/parameter/selection/unit/mapping/asof/cutoff gives append-only distinct identity. Full typed payload/hash/index/logical validation and independent recomputation of exact equation/configuration/eligibility are mandatory on recovery. No read-time calculator/raw reader or caller re-registration.

## 7. Separate durable profile

New file application_id0x4E560004/user_version1, DELETE/synchronousEXTRA/foreign_keysON/busy_timeout0, per-operation independent connections; readonly URI mode=ro/query_onlyON. Exact original absolute regular-file/path/no-symlink/no-URI-query/exclusive-create rules apply via unchanged _sqlite._path. Old raw/v1/D013 files reject new reader/writer construction and vice versa. No migration/overwrite/repair/populated-store compatibility claim.

Exactly three STRICT tables, each field NOT NULL; DDL structure follows current v1 _sqlite tables, but fixed names below and immutable-trigger message "immutable raw-ratio record":

- mmt_raw_ratio_definition_v1: owner_namespace TEXT,derived_signal_id TEXT,calculation_definition_version TEXT,payload BLOB,content_sha256 TEXT; composite first3 primary key.
- mmt_raw_ratio_configuration_v1: owner_namespace TEXT,kind TEXT CHECK(kind IN ('parameter','selection','unit','raw_mapping')),context_id TEXT,version TEXT,payload BLOB,content_sha256 TEXT; composite first4 primary key.
- mmt_raw_ratio_occurrence_v1: derived_occurrence_id TEXT primary key,owner_object_id TEXT,owner_namespace TEXT,implementation_brief_sha256 TEXT,derived_signal_id TEXT,calculation_definition_version TEXT,subject_instrument TEXT,effective_as_of_utc TEXT,knowledge_cutoff_utc TEXT,logical_identity_payload BLOB,logical_identity_sha256 TEXT,payload BLOB,content_sha256 TEXT; foreign key(namespace,D,definition-version) to exact definition table.

Six BEFORE UPDATE/DELETE abort triggers, fixed names <table>_update/<table>_delete. Validate exact declared table/trigger schema and foreign_key_check, no extra/missing/downgrade tolerance. Persist every registered configuration/definition, not only successful fact dependencies. Atomic immutable registration; BEGIN IMMEDIATE append/idempotent same-ID/fullcontent; no preexisting fact substitutes for genuine first-insert proof. Precommit rollback confirmed-noncommit uncertaintyfalse; postcommit lost acknowledgement uncertaintytrue; retry resolves one first fact. Independent concurrent first writers may report truthful busy then retry, never two facts. Reader reconstructs all typed facts/configuration/history using only path/admission/requested IDs.

## 8. Bounded change and proof-control surfaces

Permitted runtime: api.py additive records/facets/factories/exports only; new _raw_rational.py direct-raw service/registrations/validation; new _raw_rational_sqlite.py isolated profile; _rational.py only add RawRatioOccurrenceV1 to exact decode allowlist, reusing existing canonical ratio codec unchanged. Unchanged _selection.py/_evaluation.py/_catalogue.py/_sqlite.py may be imported owner-locally for proved helpers, never silently edited. Any indispensable additional extraction requires its own evidenced root ruling before edit, not a blanket refactoring grant. Truthful M02 metadata only after actual engineeringGREEN.

New fixed descriptor config/product_proof/market_measurement_d014/claim.json: exactly schema_version1.0,claim_id neutral_market_measurement_truth_d014,brief_path thisfile,binding_path§2,contract_path§9,physical_root tests/product/market_measurement_d014,admission_path config/product_proof/market_measurement_d014/admission.json. G01 tools/product_proof_claims.py may add only this third static descriptor, preserving original _authority/runner/outcome/schema. Every selected claim validates all present exact descriptors and complete disjoint physical ownership; malformed/overlap/cross-generation/wrong target/brief/binding/contract reject globally. Descriptor absent plus any Python/symlink under its exact root rejects globally, including support/nested helpers; null admission remains incomplete.

Existing tests/architecture/test_proof_control.py owns new control falsifiers. Its pre-admission disposable missing-target universe may explicitly reset all three optional extension roots/descriptors only; actual-state direct multi-claim checks separately prove ownership. Protect immutable prior generation bytes, not freeze live selected status; retain lawful advance/revoke controls. Exact proposed control diff and proof require independent preapplication review and concrete disposition before source application.

Physical product family and literal-only support/specimens are authored and independently reviewed before immutable generation1 admission or new runtime behaviour. No direct unadmitted product pytest workaround. No original catalogue/binding/brief/contract/generation bytes change. New generation path config/product_proof/market_measurement_d014/generations/0001.json with real independent-review/admission references only after actual evidence.

## 9. Independent proof and acceptance

D014-PROOF-CONTRACT-SHA256: 54850f780c4442924e2d28ed319ae5f0fb109e291b367391ac0a4c86190294fc

Exact contract path handoff/foundation_implementation/authority/G6_1_D014_PROOF_CONTRACT_PROPOSED.json; the exact contract marker and digest are recorded immediately above. One physical tests/product/market_measurement_d014/test_raw_ratio.py with six exact mandatory test names in that contract; support _support.py plus typing/valid_seam.py and invalid_seam.py. Support only provisions literal public records/configuration/files; no pre-materialise/retry/expected-answer helper.

- D014-P01 actual M00 public admit/projection→newowner materialise→reads, reference1/3/fullraw/config/authority/units/shape; absent before input admission, both memory and actual separate SQLite.
- D014-P02 independent missing/wrong type/provider/variant/subject/unit/temporal metadata/field/mapping/order/Rtag/context/definition/profile/asof/cutoff/future/stale/skew/pagination/equal-rank/duplicate-content refusal, immediate unchanged empty and nonempty history. Exact208other-ID refusal, old factories refuseD014; genuine version positive controls distinguish invalid setup.
- D014-P03 canonical signed/nonterminating/fractional/zero/denominatorzero/exponent/huge-integer wire and native tuple preservation, independent literal expected answers, low ambient precision/traps, no integer-only/magnitude/clipping policy. Arithmetic artificial-domain cases are not native validity proof.
- D014-P04 direct firstmaterialise→laterclockretry, each definition/parameter/selection/unit/bidmapping/askmapping/rawidentity/native representation/asof/cutoff independently changed where lawful, exact old/new getters/history/filter/order/limits; one-sided incompatible references refuse; atomic conflicting registration rolls back newly introduced members.
- D014-P05 genuine public first INSERT barrier before COMMIT with no old fact; precommit/postcommit faults and retry, separate connection/process visible commitment, writer child exits then fresh readonly child gets only path/admission/IDs and recovers full typed occurrences/allregistered configs/history unchanged file bytes. Separate payload/contenthash/logicalhash/index/canonicalratio/native-representation/configuration links and fully rehashed wrong equation corruption must reject. Exact schema/profile/trigger/path/read-only/cross-owner refusals; memory is not durable proof.
- D014-P06 positive exact types and reviewed negative line/code/count diagnostics: old Decimal reader/fact and D013 predecessor reader/fact cannot satisfy new raw ratio facet; new exact ratio is not Decimal; reader cannot materialise; bad request/storage rejected statically. Original complete strict D013/D012/foundation/M00 and architecture promotion, mypy/scopedRuff required; no import-error/Any workaround.

Preserve intended semantic RED before each behaviour; collection/import/environment/admission failure is not semantic RED. Use pinned native aggregate neutral_market_measurement_truth_d014; no skip/xfail/xpass/deselection/governed mutation success. Require complete new and four original strict aggregates, full source/control mypy, scoped changed-path Ruff and architecture promotion on one clean exact candidate; disclose standard full Ruff's two inherited M01E501 findings. Record first failure/repair lineage and exact evidence. Fresh independent design, preapplication control, authored-proof adequacy and implementation reviews are distinct stages; reviewer directly sequences absence→admit→materialise→laterretry/refusal with nonempty history/fresh recovery without Worker composition and classifies recurrence under AGENTS.

Concrete delegated acceptance under standing authority follows actual independent evidence, not a receipt alone. Save recoverable full Git/report. D014 acceptance is not G6.1/native/full126 acceptance: remaining122foundation identities and all83 downstream outputs stay unenabled across accepted controlled surfaces. Preserve actual G6.2→G6.3→G6.4 prerequisites and all source/profile/composition/transition/retirement/main holds.

## 10. Incorporated objects and source-reference boundary

| Object | Exact SHA256 |
| --- | --- |
| handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md | 603b850802a418780109095e7ae69bcece449da79fb24140a6d50297605e927c |
| handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv | 67bacbcf77afa766cec220a8d4a0f9589c9568d4a1f5c5818334915adf72e549 |
| handoff/foundation_implementation/authority/FOUNDATION_IMPLEMENTATION_BRIEF_PROPOSED.md | 282f7d73c5e2fdf36ded43781665764eaf95d4a35f687f99990b87c59f744ed7 |
| handoff/foundation_implementation/authority/SQLITE_IMPLEMENTATION_BRIEF_PROPOSED.md | 3ad4cdc9ffba4cf91ff9a27edf1dd3b1a9824a421514bb4b5a2cc1b9c504f233 |
| handoff/foundation_implementation/authority/G6_1_D013_IMPLEMENTATION_BRIEF_PROPOSED.md | 1f53d9c21c6eb4b90213137c4699a0688f994cd0ed55e54082268d8477abc148 |
| config/product_proof/claims.json | ad62fcd57ce837771f732864cbae7e47d9721f0311d21c3b96e05881d83cc317 |
| implementation/authority/FOUNDATION_IMPLEMENTATION_AUTHORITY_BINDING.yaml | 7c7fa7df69e75825853bf7b355343d9b6f793beab247b37223bfa71737248b87 |
| schemas/accepted_brief_product_proof.schema.json | 7bd1bacef89972e492299afc7c44d4c7fcbb72dfdb9d593a5afde286215067dc |

Read in-scope primary authority, not digests/labels alone. Original transitive accepted overlays and old immutable objects remain governing at their scopes. D013 source fingerprint is provenance, not a ban on this exact new allowlist addition if admitted.

Read-only reference investigation20October2026: retained workbook Raw Signals rows37/40 (R033/R036), SHA519ea9449297d564ae4a02afc1bf4e60e4471631c81a0842620f9fb60bb4f9ae, identifies TWS tickSize Bid/Ask Size tick0/3, not Client Portal or paired tick-by-tick. Workbook remains reference rather than guessed mapping law.

Current official reference https://www.interactivebrokers.com/docs/tws-api/doc/md/streaming-data lists bid/ask-size tick0/3, Python tickSize size:Decimal, watchlist snapshots rather than tick-by-tick, and separate callback/scale remarks. https://www.interactivebrokers.com/docs/tws-api/doc/md/live-ticks documents paired tickByTickBidAsk time plus Decimal sizes. Those are distinct variants; no timestamp or size-scale rule is transplanted between them. These observations support avoiding integer-only/decimal-limit assumptions, not a production mapping, observed collection, chosen SDK/server version or instrument/permission certification. Failed earlier documentation fetches supplied no facts; deprecated legacy pages are not current authority. Public documentation was retrieved over the network. No broker connection, provider data/API operation or SDK acquisition was performed.

This proposal requires exact independent review and concrete delegated design/brief/root disposition before any control/runtime/proof execution. No new binding, descriptor, physical proof, generation or runtime exists by its presence.

TS: 20-10-26 00:36
