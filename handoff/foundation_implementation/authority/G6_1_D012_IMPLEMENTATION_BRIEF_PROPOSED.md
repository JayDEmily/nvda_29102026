# G6.1 — controlled D012 scalar extension: proposed exact implementation brief

Date: 19 October 2026 — Australia/Melbourne.
Status: PROPOSED_FOR_EXACT_IMPLEMENTATION_ACCEPTANCE; NOT_ACTIVE_AUTHORITY.

## 1. Purpose and limits

Extend existing M02 neutral market measurement truth with one additional controlled scalar, D012 absolute bid-ask spread, whose accepted equation is ask minus bid. This is the first bounded unit inside G6.1, not completion of G6.1 or a replacement for its remaining families. D012 is recommended because it requires no new D predecessor, mathematical convention, result shape or controlled raw source. No requirement makes unrelated time/calendar/macro families predecessors of this scalar. The root plan remains the only planning authority; its explicitly labelled proposed amendment operationalises this brief only after exact acceptance.

Final Gate5 ACCEPT is owner-chat/20261019T2214/Gate5-final-acceptance. Delivered evidence commit ecb57538d0513a680c9e2ce2d0def4d992c3d833 and promoted source candidate b83a1a071153d3bdff7f0aa1b6b49bcd3c90ceb2/tree4e2d3197c929ec9f06e0fdc6b0e204244c3c1a78 remain distinct from this new proposal. Gate5 is controlled D011 only.

The original 126 foundation targets, 83 downstream identities/26 peers, all36 work receivers/54 inherited obligations/eight holds remain. Only D012 is newly proposed for controlled execution. D011 retains its accepted scope. Other124 foundation identities and all83 downstream outputs remain unenabled. Native D012 admission, complete source-family certification and full126 acceptance remain outstanding. No numerical completion percentage is inferred.

## 2. Incorporated authority

The exact byte table below incorporates the accepted version3 profile and its version2 public/selection/identity semantics. Read them in full. The original calculation brief §5 K02 fixes D012 = ask - bid; the current catalogue row D012 binds R034/R035, no D dependency, K02_ALGEBRA/P_BASIC/price. The accepted version2 brief governs the effective catalogue and mathematical overlays; its historical original-catalogue digest is not substituted for the later accepted current catalogue. This proposal changes no original equation or overlay.

The only semantic additions/replacements are those explicit in this brief. Where version2/version3 says only D011 is enabled, preserve that rule under the original authority; this new authority additionally permits the exact D012 instance below. Storage/environment replacements already accepted in version3 remain in force. Original authorities, proof generations, bindings and claims remain byte-identical. An implementation worker must not relabel them as accepting these new bytes.

## 3. Architectural projection

Ingress intents, in order: modify M02; modify G01. M02 already exists and is active; no create intent, numeric allocation or new owner/package/seam is needed. G01 covers only the bounded additional claim/admission control in §7. M00 source/API, A00, M01, existing dependency rules and all other architecture objects remain unchanged. Existing M02→M00 public-only dependency and absence of an A00 edge remain.

Future binding path: implementation/authority/G6_1_D012_IMPLEMENTATION_AUTHORITY_BINDING.yaml. It binds the raw SHA256 of this exact brief to actual external acceptance, not the old version3 acceptance. It must not replace FOUNDATION_IMPLEMENTATION_AUTHORITY_BINDING.yaml.

No public dataclass, field, Protocol, factory signature or persistence schema changes. Use nvda_desk.market_measurement_truth.api; result remains finite Decimal, price, scalar_decimal. This brief does not admit generic object/Any results, new recursive carriers or structured output families.

## 4. Exact controlled instance

Use all version2 §5 controlled NVDA cash-share inputs verbatim: provider foundation-pilot-fixture; variant cash_quote_v1; scope foundation-pilot-fixture/cash_quote_v1; R034 bid/R035 ask mappings mmt-pilot-bid/mmt-pilot-ask, quote.bid/quote.ask, price, no selection identity or revision vintage. Unit mmt-pilot-price version1 is exact identity Decimal(1), Decimal(0); parameter mmt-pilot-basic version1 is P_BASIC/NVDA/member tuple(NVDA). Selection mmt-pilot-selection version1 has same-subject join, freshness60seconds, skew10seconds, true_instant only, empty basket, page100/limit1000. Version2 alternatives retain precisely the old brief's same-payload-except-version rule.

Definition is CalculationDefinitionV1 with fields in existing public order:
D012; D012-SPREAD-1; K02_ALGEBRA; equation string R035 - R034; raw_dependencies tuple(R034,R035); derived_dependencies empty tuple; P_BASIC; price; scalar_decimal; authority_refs exactly the original calculation brief and current catalogue paths/digests in the incorporation table, in that order. D012-SPREAD-2 is permitted solely as the same immutable payload with changed definition-version string for version-sensitive identity proof. No other definition is admitted.

Reference request copies the version2 reference request field-for-field except derived_signal_id D012 and calculation_definition_version D012-SPREAD-1. It has as-of/cutoff 2026-10-16T01:00:00Z; empty context_refs; R034 then R035 bindings to exact version1 mapping/unit refs; subject NVDA. Public M00 raw observations and native records, event/receipt timestamps, IDs, sequence1/2, public opaque factories and optional None fields are exactly version2 §5. Clock is 2026-10-16T01:00:01Z. Bid100/ask102 produces Decimal(2), with raw lineage R034 then R035, no predecessor, universe/window/supersedes None. Units mean USD per one NVDA cash share in this controlled instance.

This remains a controlled record contract, not an asserted IBKR field mapping. No provider connection, subscription, calendar or exchange-open assertion is needed or implied.

## 5. Selection, arithmetic and exact identity

Apply the complete accepted version2 §5 selection/refusal algorithm and G5.3 duplicate-consistency repair to D012. Enumerate complete quiescent public M00 history; compare repeated observation identity/content before eligibility, including ineligible conflicting copies, page/order variants and exact representation. Distinct-ID ineligible facts do not invalidate a lawful older eligible result. Same-ID identical facts deduplicate. Preserve ranking by eligible event/receipt/within-scope sequence, ambiguity refusal, exact60second/10second inclusive limits, temporal kind/format, immutable mapping/source/unit matching and no prefix calculation after incomplete/cyclic pagination. No live-history snapshot capability is claimed.

D012 is signed ask minus bid. Its name “absolute spread” denotes price units rather than relative percentage; it does not authorise abs(ask-bid). Crossed100ask/102bid yields -2; locked quotes yield0. Do not add positivity, crossed-market, tick-size, finite magnitude thresholds or exchange-open heuristics. Preserve the original finite Decimal input domain; nonfinite/non-Decimal projections refuse. Raw native storage's broader numeric domain remains unchanged.

Compute exact finite Decimal subtraction independent of ambient precision, rounding and traps, using coefficient/exponent arithmetic or equivalently proved local context. For an exact output representation, align both input exponents to their minimum; subtract the signed integer coefficients ask minus bid; return digits at that exponent, preserving trailing zeroes. Zero output has positive sign and the aligned exponent. For bid100.00/ask102.0 expect Decimal tuple(0,(2,0,0),-2); bid-2.00/ask-1.0 gives1.00. These representation choices affect new D012 only; they do not redefine D011's existing representation. Unrepresentable/resource-failed arithmetic returns no occurrence rather than rounded truth; no global Decimal/interpreter policy changes.

Use the existing canonical tagged content, namespace neutral_market_measurement_truth/v1, mmt1 identity construction and full immutable references. The request D/version distinguishes D012 from D011. New D012 occurrences carry this exact new brief digest; original D011 construction under the original brief retains its digest and IDs. New-scope D011 occurrences, if constructed under this brief, carry this new digest and are separate append-only facts. No equality/retry is promised across different authority digests.

Under the original brief digest, D012 registration must reject and D012 materialisation must return None. Under this new accepted digest, exactly the old controlled D011 and new D012 definitions may register; absent definitions still refuse. Admission is trusted offline construction, not a caller's power to create authority. Runtime may compare exact known digest/profile identity, but must not import governance tools. M02's original brief allowance and new allowance must be separately proved; a blanket D012 allowlist independent of construction authority is insufficient.

Original and new proof stores are separate disposable files. A read facet is bound to the corresponding admission digest. Reading an original disposable D011 store with its original admission must still recover exactly the original fact. No mixed-authority production-store compatibility or migration is asserted. Reader restart must verify D012 against its own equation/definition, not the current hard-coded midpoint validator; wrong result under a correctly hashed payload still fails.

## 6. Bounded future implementation surfaces

| Path | Permitted purpose |
| --- | --- |
| src/nvda_desk/market_measurement_truth/_catalogue.py | Exact authority-scoped D011/D012 registration/request routing, preserving old controls and definitions. |
| src/nvda_desk/market_measurement_truth/_evaluation.py | Exact D012 subtraction; existing midpoint/codec remains conformant. |
| src/nvda_desk/market_measurement_truth/_sqlite.py | Definition-aware D012 full-content validation/readback using existing schema/transaction/encoding. |
| config/architecture/modules.yaml | Truthful addition of controlled D012 output/scope metadata after admission; no lifecycle/dependency/composition expansion. |
| implementation/authority/G6_1_D012_IMPLEMENTATION_AUTHORITY_BINDING.yaml | New exact modify binding only after real acceptance. |
| tools/product_proof_claims.py | Bounded extension resolution, authority and combined physical ownership described below. |
| tests/architecture/test_proof_control.py | Existing control-family extension falsifiers; original valid controls retained. |
| config/product_proof/market_measurement_d012/ | Additional exact admission/generation records only after reviewed proof admission. |
| tests/product/market_measurement_d012/ | The exact companion's new physical product proof and support/specimens. |

The existing api.py, _selection.py, schema SQL and run_product_proof_gate.py should need no change. A discovered indispensable change requires an evidenced bounded ruling under the root plan before editing; no silent public/API/schema redesign. No new dependency or generic storage/strategy framework.

## 7. Exact bounded proof-control extension

OBSERVATION: tools/product_proof_claims.py _authority validates the original active catalogue against the exact version3 marker; load_product_proof_claim currently requires each claim's contract and binding to belong to that one control authority. Adding D012 directly to config/product_proof/claims.json invalidates the accepted raw/foundation claims. _partition also rejects new unowned product paths. Therefore neither an appended catalogue entry nor direct unadmitted pytest is a lawful shortcut.

Proposed resolution: retain the original catalogue and _authority validation unchanged, and support one additional exact optional descriptor at config/product_proof/market_measurement_d012/claim.json. This is a bounded D012 addition, not arbitrary path/command discovery. No descriptor means the original universe; an unknown selected claim still rejects. When present, validate it before physical partitioning for every claim, so corrupted extension files cannot escape ownership checks.

Exact descriptor shape has no extra keys: schema_version string1.0; claim_id neutral_market_measurement_truth_d012; brief_path equal to this brief path; binding_path equal to §3 binding path; contract_path equal to the incorporated G6_1_D012_PROOF_CONTRACT_PROPOSED.json path; physical_root tests/product/market_measurement_d012; admission_path config/product_proof/market_measurement_d012/admission.json. Each is an exact string, not a caller selector. Validate native binding against this brief and exact ordered modify:M02/modify:G01 intents, real external acceptance, the brief's D012-PROOF-CONTRACT-SHA256 marker and raw contract hash. Validate the contract with existing accepted_brief_product_proof.schema.json; no schema relaxation. Reuse existing _target, _generation and strict runner/outcome semantics. The new target must resolve existing active M02 and its allocation; generation must match this new brief/binding/contract/claim.

Form the combined physical partition from original validated claims plus this validated extension, rejecting overlapping roots, duplicate family/proof ownership, cross-claim generation and unowned support/tests. Extension paths and descriptor are governed candidate bytes in the existing snapshot. Existing original claims retain original authority/generation hashes, no reseal. New claim uses its own immutable directory/history beginning generation1; null pointer means incomplete, never READY. The unchanged strict runner selects the new claim with --aggregate neutral_market_measurement_truth_d012. Require every named test and complete successful setup/call/teardown; skips/xfails/xpasses/deselection/zero collection/mutation remain failure.

Before implementing this control change, author and commit independent expected controls in the existing architecture family: old catalogue/hash/generation unchanged and original claims still resolve; exact new descriptor resolves only after acceptance/admission; missing/wrong binding/brief/contract hashes, wrong target or intents, cross-claim IDs/generation, overlap/unowned physical source and malformed/extra descriptor fields reject. Direct runner witnesses must prove exit-success skipped outcomes still fail and pre/post mutation still fails. Proof-only incomplete descriptor/admission must not be represented as domain RED. Review this control proof and concrete change before application under the accepted new scope.

## 8. Physical proof and required observations

D012-PROOF-CONTRACT-SHA256: b8907ef6fba60ab18aadc1a1899997dde11f55735544fee6f2d13d21c7e2a02c

The exact companion supplies one physical coherent family and six named propositions; no tests are yet authored/admitted/run. New proof root is disjoint from the immutable D011 root. _support.py provisions literal public records/stores only; it neither calculates expectations nor pre-materialises/retries. Static specimens are owner-local and their exact expected diagnostic sites/codes/counts must be reviewed/admitted with physical proof before execution.

D012-P01: actual M00 public file-backed owner/projection→M02 public materialise, reference2, signed-crossed-2/locked0/negative-price1 examples, complete typed references/raw lineage and exact equation/definition.

D012-P02: missing/wrong source/subject/unit/version/field, future/stale/skew, multi-page latest eligible selection, order independence, duplicate-consistency variants and incomplete pagination; each refusal followed by direct bounded history read proving no new occurrence. Full124 unenabled foundation/83 downstream rejection under extended scope; old admission continues to refuse D012.

D012-P03: exact subtraction independently expected at low ambient precision with traps, widely separated exponents and long coefficients; verify exact Decimal tuples/trailing zeroes/signed input zero, finite-domain refusals and no heuristic thresholds. These are exact storage/calculation-domain witnesses, not IBKR feed-magnitude claims.

D012-P04: direct materialise→later-clock retry retains first time/ID, then exact changed raw/cutoff/configuration/definition versions append separate IDs; old/new reads and immutable registration conflict. D011/D012 same observations yield distinct D IDs/results. Unavailable optional predecessor/context/supersession remains absent.

D012-P05: separate real raw/foundation SQLite files; committed result independently visible, writer exit then fresh read-only process full typed recovery with no calculator/raw reader; native precommit rollback, postcommit uncertain acknowledgement and idempotent recovery, competing identical calls plus retry, payload/index/hash and wrong-equation corruption refuse. Exercise D012 path, not only inherit D011 logs. Keep trusted-application limits; no hostile-code isolation claim.

D012-P06: actual public factory/reader static specimens retain exact Decimal return and real M00 structural compatibility; wrong result/storage/facet types have exact expected diagnostics, dependency/import failures do not count. Original D011 aggregate/source remains unchanged and runnable with original admission; a disposable original-authority D011 store created by predecessor source is recovered by new candidate with original metadata. No real populated store is opened.

All six are required for this bounded candidate. Exact positive expected values derive from authority/literals, not production helpers. Independent reviewer performs at least one raw public sequence without convenience composition, reads repair lineage (especially duplicate-before-eligibility and fixture-count recurrence) and reports exact scope. A review receipt alone does not admit the candidate.

## 9. Execution and acceptance boundary

The proposed root amendment sequences control proof/diff admission, independent physical D012 proof adequacy and immutable generation admission, actual intended RED, bounded production, targeted/full applicable GREEN, fresh independent candidate review and owner disposition. Only a supported actual environment can establish RED/GREEN; current accepted pins/profile stay. Standard full Ruff's two inherited M01 E501 findings remain explicit, with no claim of standard-lint success. Run full source/control mypy, scoped changed-path lint, original foundation/M00 aggregates and architecture promotion, plus the new strict aggregate. Preserve first failure before diagnosis and stop dependent work.

Acceptance of this exact package would authorise its stated tests/control/production work within G6.1. It would not be acceptance of a future implementation or a full family source admission. No independent review or executed result is claimed by this proposal. No additional gate or per-D owner receipt is created beyond the exact authority and candidate-acceptance boundaries already required by the current plan. After bounded candidate acceptance, continue G6.1's remaining actual families with their specific authority. G6.2 must not begin before G6.1's required semantic closure.

## 10. Exact incorporated bytes

| Path | SHA-256 |
| --- | --- |
| handoff/foundation_implementation/authority/SQLITE_IMPLEMENTATION_BRIEF_PROPOSED.md | 3ad4cdc9ffba4cf91ff9a27edf1dd3b1a9824a421514bb4b5a2cc1b9c504f233 |
| handoff/foundation_implementation/authority/FOUNDATION_IMPLEMENTATION_BRIEF_PROPOSED.md | 282f7d73c5e2fdf36ded43781665764eaf95d4a35f687f99990b87c59f744ed7 |
| handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md | 603b850802a418780109095e7ae69bcece449da79fb24140a6d50297605e927c |
| handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv | 67bacbcf77afa766cec220a8d4a0f9589c9568d4a1f5c5818334915adf72e549 |
| handoff/foundation_implementation/authority/G6_1_D012_PROOF_CONTRACT_PROPOSED.json | b8907ef6fba60ab18aadc1a1899997dde11f55735544fee6f2d13d21c7e2a02c |
| config/product_proof/claims.json | ad62fcd57ce837771f732864cbae7e47d9721f0311d21c3b96e05881d83cc317 |
| implementation/authority/FOUNDATION_IMPLEMENTATION_AUTHORITY_BINDING.yaml | 7c7fa7df69e75825853bf7b355343d9b6f793beab247b37223bfa71737248b87 |
| schemas/accepted_brief_product_proof.schema.json | 7bd1bacef89972e492299afc7c44d4c7fcbb72dfdb9d593a5afde286215067dc |

All listed digests must match raw bytes before submission. Other incorporated version3 objects remain bound transitively by its exact table, not rehashed around new runtime source. This brief has no self-digest; its final raw SHA256 is recorded externally after documentary verification.

TS: 19-10-26 22:16
