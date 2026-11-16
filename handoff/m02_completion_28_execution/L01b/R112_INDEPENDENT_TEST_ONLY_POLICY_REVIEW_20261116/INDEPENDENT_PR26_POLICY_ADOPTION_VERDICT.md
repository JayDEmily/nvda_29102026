# Independent R112/D091 PR #26 owner-adoption review — 16 November 2026

**VERDICT: `ACCEPT_TEST_ONLY_POLICY_ADOPTION_ONLY`.** The evidence establishes the owner's *scope-only* adoption of A–E at the original PR #26 request boundary, 25 negative/fault specimens with independently verified bytes, and the separation of two request-only F specimens. This is a **documentary test-policy disposition only**: no executable read/fault-port implementation approval, new successful R112 source, physical-case admission, case budget, qualified runner, source/case/claim binding, product test, owner merge or D145 reactivation is conferred.

## 1. Candidate, authority and independent review scope

- **Repository:** `JayDEmily/nvda_29102026`; **PR #26 exact reviewed HEAD:** `4683f2a0d9f052ee18c8ca5ef31ab93923cca374`; **Git tree:** `71103bb23a4b3cdc9af0084bd6a04983f25a63cd` (both independently read with `git rev-parse`/`git show -s --format=%T` in an isolated fresh checkout).
- **Direct parent:** `230395c88d6724f7e1689ae47c5164d180096c34`, the original unapproved owner-decision request. Its parent is predecessor PR #25 Worker `e52318c0ea399e5e585aef985803950f0e793d3a`. GitHub compares independently confirm `e52318c... → 4683f2a...` is ahead two commits, zero behind, with exactly **seven** new policy-directory paths; `230395c... → 4683f2a...` is ahead one, zero behind, with only **four** additive files: owner adoption MD/JSON, reviewer handover and its static validator. No `src/`, `tests/`, ledger, root-governance or successful-fixture paths changed. The original request's immutable Git blob is `a9781b08937a25f21b1436bc716cdac13329f7a5`.
- Read in full at this exact commit: `GUARDRAILS.md` (blob `54a4407609941f63f6b902076688ff102a3d5ba2`), root `AGENTS.md` (`b5b8f73bfef62cf34643aef419e6931599ad08b1`), 429-line root `EXEC_PLAN.md` (`76e8dd7af85cee33e306c351206e69fc049129fb`), and `tests/AGENTS.override.md` (`66666cc012889e585ef4da80049d5ee2a0244c53`). Checked root and all directory ancestors for `AGENTS.md` / `AGENTS.override.md`; no further applicable handoff override was found. Root planning documents retain historical/draft language; no draft text was treated as product-test release.
- Read `handoff/m02_completion_28_execution/L01b/R112_NEGATIVE_FAULT_POLICY_DECISION_20261116/INDEPENDENT_POLICY_ADOPTION_REVIEW_REQUEST.md`, `OWNER_DECISION_REQUEST.md`, `PROPOSED_NEGATIVE_SOURCE_AND_FAULT_POLICY.json`, both `OWNER_TEST_ONLY_POLICY_ADOPTION_20261116` records, and both static validators in full. Also inspected original `L01b/R112_SOURCE_CONTRACT_PROPOSED.json`, `L01b/CONTROLLED_BATCH_INPUTS.json`, the earlier exact owner-source adoption MD/JSON, `L04/D091_PROOF_ADMISSION_REVISION_20261116/STAGE_PRECEDENCE.md`, `L04/D091_ORIGINAL_GETTER_FAULT_PREP_20261116/GETTER_READ_PORT_BOUNDARY.md`, both original fixture bundles/indexes and the active `TEST_EVIDENCE_LEDGER.json`. Independently fetched/read PR #25's reviewer verdict `14127e0e444781b1868eb51dc74b37eaf9efc327` (`ACCEPT_GETTER_PREPARATION_ONLY`), without treating its documentary acceptance as a product-test permission.
- **Owner-authentication limit:** The adoption record quotes the immediately preceding direct question, “Do you approve scopes A–E on PR #26 at the exact commit above, strictly as test-only policy permissions? The physical-case budgets and execution prerequisites would remain separate decisions.” It quotes the owner's full answer “Yep, I approve.” This statement is supported as the owner reply in the available project conversation; the Git record itself is **Worker-authored secondary preservation**, not a separately authenticated GitHub owner comment, cryptographic signature or independent approval of broader authority.

## 2. Independent read-only verification and reproducibility

Used a **separate isolated Ubuntu checkout** at `/tmp/nvda-r112-policy-independent-4683f2a0` fetched from the exact SHA, detached and unchanged (`git status --porcelain` empty). An independent Python verifier outside the repository at `C:\\Users\\james\\AppData\\Local\\Temp\\nvda_r112_policy_independent_hash_20261116.py` used `hashlib.sha256(Path.read_bytes())` and semantic `json.loads` comparisons. **Its independently observed results** were:

- `INDEPENDENT_READ_ONLY_BYTE_AND_AUTHORITY_CHECK_PASS`: **27/27 individual file SHA-256 values match**, **27/27 case/path/hash triples match the union of the original 24 and later three fixture indexes**, group counts exactly A=15, B=2, C=2, D=3, E=3, F=2, and 27 distinct IDs/paths. Four additional SHA-256 matches: adopted successful-source contract, unchanged 15-member source, the original 24-fixture bundle and new three-getter bundle.
- `INDEPENDENT_FULL_BUNDLE_MEMBER_EQUIVALENCE_PASS`: **24/24** original and **3/3** getter fixture files parse to exactly the respective bundled JSON objects by `case_id` (not merely matching index claims). Full 27-member union checked.
- The original successful source and both bundle **Git blob IDs** match predecessor `e52318c...`; source cohort contains 15 distinct raw occurrence IDs; D091 active ledger Git blob also matches predecessor.
- Separately executed the candidate's `validate_owner_test_only_adoption.py` without product test import/execution; output `R112_OWNER_A_E_TEST_ONLY_POLICY_ADOPTION_STATIC_PASS`, 27 fixture hashes, no case budget or product-run release. This validator is **corroboration**, not a substitute for the independent verifier.
- Directly inspected B specimens: tied cohort has **two distinct IDs** with identical receipt and sequence; overflow cohort has **65 distinct IDs**. C repeated-cursor specimen has page sizes **8 then 4**, next cursor `"8"` repeated; C conflicting-ID specimen reuses an earlier ID with changed projected value. Inspected E rollback/uncertain-acknowledgement/content-conflict semantics and F's two request-only mutations as documentary proposals.

No M00/M02 product case, SQLite fault, read-port injection or runtime qualification was executed. No full L00 66-ref fresh receiver/`git fsck` or complete product acceptance was performed; the isolated checkout verifies only this review's documentary Git/byte scope.

### All 27 independently checked file hashes (exact PR #26 manifest)

| Group | Unique specimen ID | Calculated SHA-256 (matches manifest, index and bundle member) |
| --- | --- | --- |
| A | `L01B-R112-CONTROLLED-NATIVE-UNITS-REFUSAL` | `b337bb83a61b02fd470f5fa06cbeeb6c9bc4c22327cfb080bd1e3d0a8e594b33` |
| A | `L01B-R112-CONTROLLED-SOURCE-PROVIDER-REFUSAL` | `311449aecf4aa3cf92dcedb6cf50d5d04c70af10531d2a119e032f0c2755679d` |
| A | `L01B-R112-CONTROLLED-SOURCE-VARIANT-REFUSAL` | `633d5c5a648fb6e9af5835cfde545f753e9d7b9570a7475ec5e6214582a4a12b` |
| A | `L01B-R112-CONTROLLED-CONTRACT-ID-REFUSAL` | `5707a23b542a5e6117fca02c926ffb50e8d9687bd48252696728b7bd71d75aae` |
| A | `L01B-R112-CONTROLLED-UNDERLYING-REFUSAL` | `8f56be39fe73c6f9d33eca45a90d8ce4e638000583f5517aa989e7a5adca1c41` |
| A | `L01B-R112-CONTROLLED-SECURITY-TYPE-REFUSAL` | `3a62d4f6aeabedf87000c2c5fe1aae7957c6da2d42f78a6eecf594878182193d` |
| A | `L01B-R112-CONTROLLED-RIGHT-REFUSAL` | `cf6d3be90a5cc04ba142673e82b57b38511be1003b3548712fc3e2eda1dc122d` |
| A | `L01B-R112-CONTROLLED-EXPIRY-DATE-REFUSAL` | `ff9736a906aebf132d97a7b04c8a14018f704a41371361f3abc3eef3c401acd6` |
| A | `L01B-R112-CONTROLLED-STRIKE-REFUSAL` | `a4c3634f248289bff0c427dc6a66360f087a42c60efdf79048338c5b4223feaf` |
| A | `L01B-R112-CONTROLLED-CURRENCY-REFUSAL` | `2fc2210a4fe21ca42a0964dd5d1cbeee11e8c98c5b08cfc838564bed4bf53fe3` |
| A | `L01B-R112-CONTROLLED-MODEL-VARIANT-REFUSAL` | `696f8c8141d90f598850d4325ffa0d5a137290b104e28d20b49af36d97f18c62` |
| A | `L01B-R112-CONTROLLED-SCALE-REFUSAL` | `ecaf3846158cf5da5075051350b4e2af8d50e01a7a6f5c80cdf61e75243c6e2d` |
| A | `L01B-R112-CONTROLLED-GENERATION-REFUSAL` | `cd1fbb5e284ba83b9219aaae4d413f9ee7c07e4b161e7d8658c96387e27d56d4` |
| A | `L01B-R112-CONTROLLED-REQUEST-ID-REFUSAL` | `d1c56064e3c5c94cd9457024ba993b85e694d58056ea449b762fc966b3f5539f` |
| F | `D091-CONTROLLED-RECEIPT-ASOF-REFUSAL` | `cf079a54252dd708201d09c3e76c216221bc3f7b6b07beb1914888674a37d706` |
| F | `D091-CONTROLLED-CUTOFF-ORDER-REFUSAL` | `53c9a8d7c7eaf38a4544584ceea518881c49469f976a206be6f7c4010ba548b7` |
| A | `L01B-R112-CONTROLLED-SEQUENCE-SCOPE-REFUSAL` | `0604d7e5c15d6de8c651cdcc3233c8d56334b97e394487b7810e5d977bc6d39e` |
| B | `D091-CONTROLLED-TOP-RANK-TIE-REFUSAL` | `0d34b51e309db8799bd6426f1e183a80e1d9244354cda2867af2b1e7271ef0fc` |
| B | `D091-CONTROLLED-OVER-64-REFUSAL` | `ba7129a821d9e6434be9fc5fcc454d8ebd78f043c090255f0c1c2cfde630caf7` |
| C | `D091-CONTROLLED-CURSOR-NONPROGRESS-REFUSAL` | `4031f4640a1373c377a623f442a0f2ec859a176ac725906c48cc6b2b1e5d2fcf` |
| C | `D091-CONTROLLED-DUPLICATE-ID-CONFLICT-REFUSAL` | `c9fbf5aa427b87d287f05e4b5cfe2daadb50e3236d1529654fd6450db6896c98` |
| E | `D091-CONTROLLED-PRECOMMIT-SQLITE-FAILURE` | `0f954fc8d7a132091576cb7af92072d7eabc839c47373189658130437cc4e20b` |
| E | `D091-CONTROLLED-UNCERTAIN-COMMIT-FAILURE` | `15b15b769d92258731c6cd72cc6ca322a331401249d42be74443f0166cd135e3` |
| E | `D091-CONTROLLED-SAME-ID-CONTENT-CONFLICT` | `93154f6bf3d26c09b1b74718112016d1002ef39efcaf084c189f1b4a1af06408` |
| D | `D091-CONTROLLED-ORIGINAL-GETTER-MISSING` | `ac1b985e87cb2f4ca0dfed0fd1dc3bb4c0fac8d5794ff4831cda2014a68810b3` |
| D | `D091-CONTROLLED-ORIGINAL-GETTER-UNITS-MISMATCH` | `a80a39c150eafb970089f40f7d8ba60c82ae43cb248abb5e472497f2edd49608` |
| D | `D091-CONTROLLED-ORIGINAL-GETTER-GENERATION-MISMATCH` | `e3b11ca22017e465fc63f11b102bbc6d696d2fe40436b6bc5a501e0da4078352` |

## 3. Decision-by-decision finding

| Scope | Adopted **test-only meaning** | Strict exclusion |
| --- | --- | --- |
| **A — 15** | Malformed original L01b raw-ingress negative stimuli may be considered for fail-closed source-admission proof | They do not become legitimate R112 members and may fail before D091; not reached D091-stage proof |
| **B — 2** | Distinct sealed private negative cohorts: exact tied 2-member rank; exact 65-member projected overflow | Neither may substitute for or expand the owner-adopted positive 15-member cohort |
| **C — 2** | D091 selector-only read-port H06 repeated cursor and H07 conflicting duplicate-ID responses | Do not claim ordinary immutable M00 emits these faults; cannot replace actual source sealing or true page-history traversal |
| **D — 3** | D091-only original-getter read responses G01 absent, G02 native-unit contradiction, G03 original generation contradiction | Trusted real M00 manifest/original getter and storage remain genuine/unmodified; the fault adapter cannot forge `SEALED`, provide M00 `commands`, or contaminate Stage B |
| **E — 3** | Disposable SQLite failure stimuli D01 precommit rollback, D02 uncertain postcommit acknowledgement, D03 immutable same-ID/content conflict | No assumed durability outcome without fresh independent readback; no general database/prod fault authority |
| **F — 2** | Request-data-only H01/H02 use the exact unchanged successful source, so no new source-policy decision was requested | Not part of the 25 approved A–E negative specimens; physical-case admission remains separate |

**Stage boundary:** Original `STAGE_PRECEDENCE.md` requires **B** trusted genuine original-manifest/getter checking, **C** genuine cursor exhaustion, and only then **D** D091 selector-specific projected-versus-original verification. A future test adapter may substitute the D091 consumer's read-only getter response **only after** genuine source sealing, without substituting the trusted private manifest getter. A fault detected at Stage B is not a proven Stage D refusal. The original getter seam and proposed stage hierarchy are documented, **not implemented or product-proved** by this policy decision. This distinction is consistent with PR #25's narrowly conditional preparation-only verdict.

## 4. Unchanged successful source, authority and outstanding releases

- Exact controlled-synthetic R112 source contract SHA-256: `31c811e77468f44c2e412893326bc6d5f9ea037cdbf28712ce8e213652fdfc63`; exact original successful 15-member batch SHA-256: `1f4c46c5c247c78e3e18bb2de02c172f775379f664bad8e056ef6867a39d03dc`. Neither changed in PR #26. Original owner adoption is controlled synthetic only; no live-provider source, extra original member, inferred event-time or public M00 snapshot/seal API follows.
- SHA-256 of original 24 negative-fixture bundle: `e433359c0b0cfdf4c6ed5c1dbe95ee7b7159d524f97917c3b7bfbc81d1867080`; three getter-fixture bundle: `c76e3189dce4c2ebed6ccd76afad38b0d56e3b20e1e30859cd8eb00dc8e9c8cd`. Each separately verified, with 27 exact individual-to-bundle object comparisons.
- **Physical proposals, not admitted cases:** 17 **D091/L04** plus 15 **L01b** = 32 proposed physical nodes, with final adequacy **not established**. This 32-case proposal is distinct from the 27 fixture count. Active `TEST_EVIDENCE_LEDGER.json` proof `M02-C28-D091` has `authorised_case_count=0`, `hard_ceiling=0`, `cases=[]`, `execution.runs=[]`. A historic prospective six-case ceiling does not apply as authorisation; separate exact owner proof-budget/adequacy decisions remain required for D091 and L01b. A successful documentary review here neither increases the ceiling nor releases one case.
- **Other outstanding gates:** exact negative source/selector fault-port implementation design and independent executable proof; L00 accepted 66-ref/asset receiver; qualified chosen CPython 3.13.5 / actual loaded SQLite features/runner; M02 D091 owner/category DTO/codec, claim/generation/pointer and durable readback; separately admitted finite physical cases with source identity and prerequisite ordering; separate strict product Tester and approved dependency-window schedule; any PR merge. These are **retained prerequisites, not alleged present defects** of the documentary PR. `D145` stays **PAUSED**.
- The record's `specific_test_port_code_implemented=false`, `l00_receiver_accepted=false`, `runner_sqlite_qualified=false` and `strict_tester_designated=false` are **attributed scope declarations**, not independently certified global repository absence. This review has not examined every external receiver or runtime and does not turn such limits into accusations.

## 5. Conclusion and scope-controlled handover

**`ACCEPT_TEST_ONLY_POLICY_ADOPTION_ONLY`**. Exact owner reply is adequately scoped to the immediately preceding A–E test-only question; no false import of F, case budget or positive-source expansion is justified. Independent byte, bundle membership, policy-count, ancestry, altered-path and active D091 ledger checks agree. No material discrepancy was established within the *owner-adoption documentary proposition*. This is **not** acceptance of test-seam implementation, physical-case adequacy, fixture execution, product semantics, receiver, runner or main promotion.

**Review branch:** `review/r112-d091-pr26-test-only-policy-independent-20261116-gpt6`, created from exactly `4683f2a0d9f052ee18c8ca5ef31ab93923cca374` for this independent verdict only. No product/governance/test/ledger/source/fixture modification, no case admission or product test, no PR merge and no D145 reactivation. The next independent work, if separately commissioned, is exact finite proof-adequacy and owner budget admission together with the remaining executable seam and runtime/Tester gates; it cannot be silently inferred from this verdict.
