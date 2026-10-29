# D040 — configured market-condition trend intensity

Status: ACCEPTED_FOR_IMPLEMENTATION under owner24October2026 explicit delegation to settle all decisions needed to complete D040/D041. This is a controlled engineering parameter instance; it is not a calibrated trading model.

## 1. Owner and ingress

Preserved P02 responsibility: configured_market_conditions, new runtime module, package nvda_desk.configured_market_conditions, public seam .api. Normal category-M create ingress resolves the next unused identifier; current mechanically resolved candidate is M03. Intent never supplies that number. After allocation, the active binding modifies the admitted owner and G01/M02 public consumer metadata. No automatic adoption of workbook working M03; no other P02 output is implemented. M01 historical engineering/state is preserved and not migrated; only this new exact controlled definition is published by this owner.

Dependencies: M02 public MeasurementWindowReadsV1, exact WindowMeasurementOccurrenceV1 snapshots; M00 public carriers only for lossless decode, no raw-state read or write. Inputs are immutable selected actual public predecessor IDs and exact profile/time. No peer service, M01 import, foreign private import or shared semantic score service.

## 2. Canonical profile

D040_PROFILE.json is the sole owning declaration of ordered eight feature entries and four predecessor contracts. Every root scalar extractor means component(result), otherwise component(result.named_field). Each pair uses bounded_ratio(x;s), clips after transform to [0,1] and [-1,0], then orientations +1 and -1, each weight1/4. Thus score = (|x1|/(.01+|x1|) + |x2|/(.03+|x2|) + |x3|/(.1+|x3|) + |x4|/(.001+|x4|))/4. Inputs are D020 log-return, D021 log-return, D027 percent_per_minute, D024 accel_1v5 in that order. Intercept0; no baseline, hidden transform or sigmoid. Result is generic unsigned score in [0,1). This measures multi-horizon movement/slope/acceleration intensity, not a separately established directional-consistency statistic or predicted trend persistence.

Immutable raw P_SCORE output uses exact reduced integer numerator/positive denominator over predecessor stored Decimal/ratio values. There is no intermediate or final rounding. Profile/definition changes require new immutable version and cannot silently alter this instance. Positive/negative clipping construction is K07 arithmetic, not an invented abs extractor.

## 3. Interface, lineage and durable contract

Public frozen/slotted records: FeatureV1(signal,path,units,transform,scale,clip,orientation,weight), DependencyV1(signal,owner,brief,definition,parameter,context,window), ScoreProfileV1(signal,definition,profile_id,kernel,units,output,intercept,features,dependencies), ScoreRequestV1(signal,subject,as_of_utc,knowledge_cutoff_utc,profile_id,predecessor_ids), FeatureEvidenceV1(feature,source_occurrence_id,extracted,transformed,oriented,weighted), ScoreOccurrenceV1(owner_object_id,owner_namespace,implementation_brief_sha256,derived_signal_id,derived_occurrence_id,request,profile,profile_sha256,predecessors,features,result,units,result_shape,effective_as_of_utc,knowledge_cutoff_utc,calculated_at_utc). Rational fields use M02's public ExactRatioV1 mathematical carrier. Profile scalars/tuples are exact typed values, not mutable dict configuration.

Public create_owner(admission,predecessor_reader,storage,utc_now) / create_reader(admission,storage) expose materialise(request), reads.get_derived_occurrence(id), bounded reads.list_derived_history with signal/subject/effective/knowledge/limit. Storage/admission reuse public M02 carrier shapes as transport only; owner admission must match M03 and this exact brief hash. Own ScoreReadsV1/ScoreOwnerV1 protocols; read-only facet has no write operation.

Fixed subjectNVDA/as-of20Oct2026 12:40Z/cutoff+1s, current time at least cutoff. Direct predecessors share subject/as-of/cutoff and cannot be calculated in the future. Public owner/namespace, brief, definition, parameter, context/version, window, units and result carrier must match the owning dependency manifest. D024's D020/D021 predecessors must equal those selected directly; no incoherent child lineage. Exact requested ID/order, no latest or incomplete fallback. Controlled close/price session versions are explicitly compatible at this instant despite distinct context IDs.

Lineage preserves full actual typed predecessor snapshots, including their raw source/configuration chains, plus each extracted/transformed/clipped/oriented/weighted exact value. Hash identity includes owner/namespace/brief, profile bytes, request and snapshots/results; excludes only calculation time and pending ID. Deterministic identical facts preserve first committed occurrence/time; conflicting same-ID content fails. Changed facts/versions produce append-only identity.

Own SQLite application_id0x4E560030, one immutable STRICT occurrence table, UPDATE/DELETE rejection triggers, exact schema/hash/canonical-codec/recomputed-own-result checks, acknowledged atomic transaction/readback, separate regular file, synchronousEXTRA/delete journal, read-only URI/query_only reopen. Trusted-application separation, not hostile-code/role certification. Copy accepted technical codec/store locally; never import M02 private code at runtime. Files api.py,_codec.py,_store.py,_score.py only. Failure types distinguish persistence failure from validly shaped unavailable request(None). No default storage fallback or foreign DB access.

## 4. Two strict cases and independent oracle

Physical tests/product/configured_conditions_d040/test_signal.py, sole test_d040_signal parameter IDs success/refusal. Both produce real public D019/D020/D021/D024/D027 from M00 raw facts; no old test function runs or supplied derived answer.

Close grid: T=12:40 close110; T-1m close120; T-5m close100; T-30m close121. Independently rounded50digit logs supply D019=ln(11/12), D020=ln(11/10), D021=ln(10/11). D024 accel_1v5 = storedD019 - storedD020/5 exactly. Current cumulative VWAP105 atT and prior100 atT-5m yield D027.percent_per_minute=1 exactly. Success has positive D020/D027 and negative D021/D024; it discriminates signed extraction, clipping and orientation, scale, order and weight. Independent standard-library Decimal log reasoning (no product imports) freezes exact numerator/denominator in this brief before implementation; the proof asserts those literals, full typed profile/eight feature evidence/selected IDs/snapshots/owner/time/units/identity and ordinary public durable read-only reopen.

Refusal: all these actual lawful prerequisites exist and are asserted before calling materialise; requested last slot contains the actual D027 ID instead of D024 (duplicate identity also forbidden). To avoid an earlier duplicate-ID refusal masking slot validation, request order D020,D021,D024,D027: four distinct lawful actual occurrences, D024 in D027's position. Must reach ordered predecessor contract mismatch and persist no score/history. This is the only negative scenario. No hidden case loop, probes, duplicate GREEN or routine RED. Independent reviewer assesses discrimination and missing runtime branch limits.

## 5. Acceptance, proof and limits

Two cases only; reviewer is sole strict executor. Scoped static typing/lint on new/changed paths once, scoped new-owner registry/dependency/seam/ingress checks once; unchanged evidence reused. Root §5 repair exception remains. No runtime RED is reduced test-first evidence. No other P02 signal, provider/TWS/API acquisition, M01 retirement/state migration, A00 composition, integration/E2E, native certification or predictive validity.

D040-PROOF-CONTRACT-SHA256: 6ce6c64925a121ecdcb387617d1a438fd1312371194d7382dcef6f29cc7e51df

| Path | SHA256 |
| --- | --- |
| handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md | 603b850802a418780109095e7ae69bcece449da79fb24140a6d50297605e927c |
| handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv | 67bacbcf77afa766cec220a8d4a0f9589c9568d4a1f5c5818334915adf72e549 |
| handoff/configured_market_conditions/authority/D040_PROFILE.json | bd1fc3456e87b81d8f8f2fc7660d4ead8385a207d355ed02e5c1c013c408e6ee |
| handoff/configured_market_conditions/authority/D040_PROOF_CONTRACT.json | 6ce6c64925a121ecdcb387617d1a438fd1312371194d7382dcef6f29cc7e51df |

## 6. Frozen independent numerical witness

Independent standard-library Decimal natural logs evaluated at90digits then rounded once to50digits half-even give D019=-0.087011376989629766167765901873749540976783972605843, D020=0.095310179804324860043952123280765092220605365308644, D021=-0.095310179804324860043952123280765092220605365308644. Acceleration is -530367064752473690882781632649512797104525228337859 / 5000000000000000000000000000000000000000000000000000.

Applying the independent rational equation from §2 yields result numerator 5772535406656219261377912607991856373340241174391084767687360450426598257465757437106508041379369440679236831282837968915857051448465837051135869377659 and denominator 6476193208071994787373802516837355775889104075051380024192619923330082866631786211844754150993808494152242338987090014704597913110058065819766936107372. These exact integers are the proof oracle; production code is not imported in their derivation.
