# Independent D013 authored-proof adequacy review

Disposition: RETURN_FOR_AUTHORED_PROOF_REPAIR.
Reference: independent-review/g61-d013-proof/a31b71c/20261019.
Reviewer: /root/g61_d013_proof_review, fresh independent judgement; no subagents.

## Exact state and authority

Reviewed clean candidate a31b71cb4327d848c246844dc5b9619f63a37738, branch work/v2-g53-review-20261019, repository /workspace/scratch/d549b6d808a9/g52-recovery/repository. All four proof hashes independently matched:

| Relative to tests/product/market_measurement_d013 | SHA256 |
| --- | --- |
| test_ratio.py | 0d937bd323983f50f2dbba791748ae6e31a33dfdfc4744b01f97ba00f0f731d5 |
| _support.py | c71c80923f19e33685f0ff64721f692222d1b740f60c33726382711f769f59b4 |
| typing/valid_seam.py | 5dc8f3cc763ac09cbd42ecc8605355f89635b0bae33a25f3154cc38fcbc75b79 |
| typing/invalid_seam.py | 72e141ffa5d10038777a5ba5e2cd8636315088a9a538999138916c39adc25ae3 |

Read full GUARDRAILS.md, AGENTS.md, tests/AGENTS.override.md, current root plan progress and exact section7.2, full D013 brief/contract and relevant incorporated foundation/v3 SQLite/D012 semantics, original K02 and native temporal/lineage/predecessor/idempotence/read-seam clauses. Independently matched brief SHA256 1f53d9c21c6eb4b90213137c4699a0688f994cd0ed55e54082268d8477abc148 and contract SHA256 7eab93055c2e2f19e74563ec9588bbc04dfdb8664d4c8e3279527f70917d4a47. Read native binding/design delegated disposition and public-seam/ownership laws. Standing owner-chat/20261019T222804/D012-and-standing-human-exceptions is not a waiver of independent proof adequacy, immutable generation admission or later implementation review.

## F001 — Important, RECURRENT_CLASS: proof obligations escape their semantic scope

The authored proof excludes lawful implementations by expanding a bounded operation-specific invariant into an unqualified implementation-path/test-wide condition. This is source-level proof inadequacy before implementation, not an observed product defect or an intended domain RED.

Witness A: test_ratio.py lines961–970, profile branch of P05. The initial fact is already materialised at lines922–924 before the connection spy is installed. Inside the spy, the only materialise call is a retry of that same request at line962. Lines967/970 nevertheless require observing a write BEGIN IMMEDIATE and mode=rw connection. D013 brief section7 mandates BEGIN IMMEDIATE for new occurrence inserts and mandates that retry return the original complete fact/time. It does not require an already-existing retry to open a writer transaction. A conforming retry that validates and returns the existing complete fact through an independent read-only transaction fails these assertions. The test therefore fails to isolate the real first-insert transaction-policy proposition. Native first-write barriers/fault assertions elsewhere do not cure this profile-branch overconstraint.

Witness B: test_ratio.py lines476–490, unsupported-all branch of P02. Calls are cleared once before the branch, then208 different unsupported requests are issued, followed by one uniqueness assertion over the whole accumulated read trace. Brief section6's read-once rule is per request. A materialisation that reads each explicit predecessor once, then refuses an unsupported D with no write, has satisfied that bounded rule; after two such requests the test rejects repeated IDs anyway. The brief requires exact D013 scope/refusal but does not require this particular validation short-circuit ordering. The genuine domain assertion is None and unchanged history for every unsupported request, not one read budget for the entire208-request batch.

Required class-level closure: make every negative/positive proof assertion apply to the exact semantic operation, request and transaction phase to which accepted authority assigns it. Preserve actual first-write native transaction-policy evidence, later retry's original complete fact/time, per-request read-once discipline, all unsupported-ID refusals and immediately unchanged empty/populated histories. Show that the proof does not reject lawful read-only retry or independently bounded predecessor reads across separate refusal requests. Do not weaken accepted domain criteria or prescribe a production implementation to satisfy these test conveniences. No particular patch is prescribed.

Recurrence evidence: reviewed D012 original9b692ec -> revised7eaddf9 actual diff and G6_1_D012_PROOF_REVIEW_20261019.md. Those repairs established that one composed observation cannot prove separate integrity/version/first-write obligations. Also read D013 initial control REVIEW.md and V2 REVIEW.md plus primary526cee6/3269035 diffs: the original preservation test promoted one checkpoint's selected generation/readiness into a permanent live-pointer invariant; the repair preserved immutable history while admitting lawful advance/revoke transitions across all three claims. The current profile retry and multi-request trace witnesses repeat this D013 class of promoting an incidental observation/operation scope into generic law. Class closure is authority-defined above; no authority-gap BLOCKED is necessary.

## Other reviewed propositions and bounded observations

All six mandatory test names exist as six physical test functions. AST/source inspection projects179 parameter cases:2 +66*2 +12 +12 +20 +1. This is not actual pytest collection. Support provisions literal public data/configuration/stores only and does not materialise, retry or compute expected answers. The wire/identity oracle resides in the test module and imports no production serializer. Explicit huge-case IDs avoid automatic integer stringification. Arithmetic expectations for nonterminating/signed/zero/huge/tiny cases are independent literal integer answers; 5000-digit coefficient witnesses cover both numerator and denominator wire strings without changing interpreter conversion policy.

P04 independently changes D013 definition, each predecessor definition and compatible parameter/selection/mapping/unit chains, with one-sided refusals where pairing is required. P05 contains a genuine first-public-write barrier with no committed preexisting fact, native pre/postcommit acknowledgement faults, separate payload/content-hash/logical-hash/index corruptions, canonical-ratio/configuration/link/schema/owner failures, and writer-child exit followed by a fresh read-only child receiving only path/admission/ID and recovering occurrence/all definitions/all parameters/history. These are authored-source observations, not executed evidence.

Nested-equation discriminator reviewed and retained: lines1157–1190 change only the nested midpoint result101 ->999, set outer result200/999, rehash outer logical identity and content, and retain the nested oldmmt1 ID. I independently inspected existing _catalogue._Owner.materialise payload construction and _sqlite._validate_occurrence reconstruction. The old logical identity contains owner/authority/request/definition/configuration/raw lineage; it excludes result and calculated_at. The retained nested ID is consequently correct for the unchanged old logical inputs. An identity-only validator cannot distinguish that forged nested result; the old equation/full-content validator must. An earlier provisional reviewer hypothesis that this needed a changed nested ID was disproved by these primary sources and is expressly withdrawn, not a finding.

Fixture-independent ordering/absence review: directly analysed the actual source-level public sequence, not an invocation of Worker fixture composition: public M00 admit_raw_observation_occurrence establishes two raw facts; old public create_owner registers configuration but does not materialise occurrences; the explicit old public materialise(D011) then materialise(D012) calls produce their own exact facts, after which ratio_seam is first called. Inspected _catalogue._Owner.materialise's public-read selection -> exact arithmetic -> complete logical payload -> append, and _sqlite._validate_occurrence reconstruction. This establishes source ordering in P01 and all physical test entry points without assuming a helper already supplied predecessors. P02's active missing reader returns None for the explicitly requested midpoint and immediately asserts unchanged history. No missing seam/API invocation or domain execution was used to claim an actual new-seam absence result.

P06 boundary note, not an additional finding: lines1328–1330 compare full ASTs of old public declarations, including their bodies, rather than merely fields/signatures/return types. This is stronger than semantic compatibility alone. The current admitted surface is additive-only and no indispensable change to those old declarations has been established, so this review does not demand an existing-node rewrite or remove that canary. Any later genuinely necessary old-body change must first be resolved against the exact brief/root scope, not justified merely by test failure.

## Static specimens

Reviewed positive specimen against exact declared new public records/facets/factory signatures and preserved old Decimal surface: source-level compatible; no Any/object substitute or missing-import escape is authored. Actual positive mypy GREEN remains after implementation.

Reviewed negative specimen exact sites/codes/count:

| Line | Code | Proposition |
| --- | --- | --- |
| 16 | assignment | Old Decimal reader cannot satisfy ratio reader |
| 17 | assignment | Old occurrence cannot satisfy ratio occurrence |
| 18 | assignment | ExactRatioV1 is not Decimal |
| 19 | attr-defined | Ratio reader has no materialise |
| 20 | arg-type | Ratio owner requires RatioCalculationRequestV1 |
| 21 | arg-type | Ratio reader requires SQLiteReadStorageV1, not writer storage |
| 22 | assignment | Ratio occurrence is not old occurrence |

Exactly seven reviewed sites, four assignment/one attr-defined/two arg-type. Authored harness checks exact line/code set, overall error count7, exit1 and empty stderr, so import/dependency/Any diagnostics cannot stand in for the seven intended errors. These are source-reviewed expected diagnostics, NOT executed mypy observations; no new-API specimen was executed before admission/implementation.

## Commands actually run and limits

Read-only inspection used cat/sed/rg/nl/wc against the listed authority/proof/source/configuration/README/Makefile/pyproject and lineage records. Git commands actually run: status --short; rev-parse HEAD; diff9b692ec7eaddf9 on D012test_spread.py; log --oneline9b692ec..7eaddf9; show/stat and full test diffs526cee6/3269035. sha256sum verified the four proof files and D013 brief/contract. No shared file was edited.

Executable bounded checks, all exit0:

- /workspace/scratch/d549b6d808a9/g52-dev/bin/python /workspace/scratch/d549b6d808a9/d013-authored-proof-review-cdXhTW/static_review.py: compile-only four files, AST six required functions,66 refusal labels/20 storage labels, projected179 cases, exact seven negative sites, independently extracted old identity keys from producer and decoder excluding result/clock. No module imports/execution.
- /workspace/scratch/d549b6d808a9/g52-dev/bin/python -m ruff check tests/product/market_measurement_d013: All checks passed!

Evidence script is adjacent static_review.py; bounded tool output is transcribed in STATIC_RESULTS.md. No domain pytest, collection, strict product aggregate, new API calls, new specimen mypy, mutation canary or implementation behaviour was executed. No full control/regression/architecture suite was repeated. Existing control GREEN/design admission were read with their original attribution, not adopted as this review's runtime evidence. No actual generation admission, RED/GREEN, implementation acceptance, fullG6.1/full126/native/provider/live/composition/migration/retirement/main claim follows. RETURN requires bounded unadmitted proof repair and fresh adequacy review before generation/admitted RED/production.
