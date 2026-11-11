# T01 independent documentary and Git-integrity review — recovered R2/G0/F02 successor

**Review date:** 11 November 2026 (Australia/Melbourne)  
**Reviewer:** separate ChatGPT documentary-review conversation; not the T01 proposal Worker, the prior F02 reviewer, or the later L32 product Tester.  
**Disposition: `ACCEPT_DOCUMENTARY_PROPOSAL`** — acceptance of the **reviewable proposed authority package only**, not programme/owner approval, active-plan installation, a new backend, product evidence, or permission to implement.  
**Repository:** `JayDEmily/nvda_29102026`  
**Pinned input:** `aa8dc23608bb6d655aebd74e390a8b3d341735c7`; tree `e58d34ef63c7c52f40cfdd0d6d45120a857fb978`; direct parent `16b7cc67f5d24336d3768e2da006819474a8c792`.  
**Reviewer output branch:** `review/t01-successor-independent-20261111`, created from **exact pinned input**, not the later handover branch HEAD `768f18672d5f8a226e806b9fff68984ae027d739`.  
**Sole commissioned output:** this `handoff/review/t01_successor_independent_20261111/INDEPENDENT_REVIEW.md`. The resulting Git commit ID is verified and reported in the external GitHub readback/response; embedding that commit ID inside its own contents would be a circular hash requirement.  
**Review boundary:** documentary semantics, authority, ledger comparison and Git transfer integrity. **Zero NVDA product tests, runtime qualifications, code edits, active governing-file replacements, merges or source-branch ref updates.**

## 1. Governing authority and review inputs

The commission is `handoff/planning/t01_recovered_successor_20261111/INDEPENDENT_DOC_REVIEW_HANDOVER.md` at handover commit `768f1867…` (Git blob `5499f7dc845e91508f73ec29b9a47f8463d249a0`, lines 1–32). This handover postdates the exact candidate and is deliberately **not** included in the pinned candidate tree.

The following identified text/JSON artefacts were inspected **in full** (full programmatic parsing/comparison where noted), with Git blob identities:

| Repository path or exact relative location | Blob SHA-1 | Review role |
|---|---|---|
| `GUARDRAILS.md` | `54a4407609941f63f6b902076688ff102a3d5ba2` | Frozen authority; fully read |
| `AGENTS.md` | `d5bf2084af7016b2204f3a131e1cce5c35633939` | Existing local-R2 authority; fully read |
| `tests/AGENTS.override.md` | `fb502203947d2075d9a6e29f39c4fe6c7e0a66a1` | Existing test-local authority; fully read |
| `EXEC_PLAN.md` | `95aa1090e02585673f81f16e9a72c150353c0120` | Original recovered F02 463-line local R2 plan; fully parsed/compared |
| `handoff/m02_completion_28_execution/EXECUTION_REGISTER.json` | `cd3f1f82119b62d6ddc596db91e2e1851cfe8829` | 39 original leaf records; fully parsed |
| `handoff/m02_completion_28_execution/TEST_EVIDENCE_LEDGER.json` | `3bca28fae4ac0e1d743a981e4157487312b10c13` | Original 35 obligations; fully parsed |
| `handoff/planning/m02_foundation_completion_20261030/TEST_EVIDENCE_LEDGER.schema.json` | `4ee6833042c488ae90c8b76ccacac82273bfe772` | Actual Draft 2020-12 schema; fully parsed |
| `handoff/planning/t01_recovered_successor_20261111/PROPOSED_EXEC_PLAN.md` | `71c85f948a54ae6fd4a442793f00dfb1c354273c` | Complete 486-line proposal; fully read and compared |
| `.../PROPOSED_AGENTS.md` | `797e7c0c3160e679e41ed3cac2fd342d928243bd` | Complete proposed root instructions |
| `.../PROPOSED_TESTS_AGENTS.override.md` | `04a8a97eb8b293c378639de8d48d6295edcf2e70` | Complete proposed test-local instructions |
| `.../PROPOSED_TEST_EVIDENCE_LEDGER.json` | `c2387b3aa5478d828b133cb8813646448e2fec25` | Proposed complete ledger; independently schema-validated and structurally compared |
| `.../T01_RECONCILIATION_AND_DECISION.md` | `3dd051abf98cf1a9f7a5160cdee967c022c26888` | Source/owner-decision chronology and proposal status |
| `.../PROPOSAL_SOURCE_MANIFEST.json` | `196a1264e83fe4b795fc347ae5e365f6d061d512` | Source blobs, original 35 IDs and original 66-ref declaration |
| `.../ORIGINAL_66_REFS.json` | `162b242eee672bbaa1b4a1e30d63bb2d71657fe3` | All 66 literal ref/name-tip records independently reconstructed |
| `.../GITHUB_REMOTE_RECEIVER_RECEIPT.json` | `36ca7cb350d8e4a5d30bbf91158254eec275ecb4` | Prior Worker receiver claims, independently checked where specified |
| `.../UBUNTU_F02_RESTORATION_RECEIPT.json` | `47d4aec6d15ea61adaccf5962fc8be709a17d936` | Historical local archive/commit claims; external assets **not** independently rehashed here |
| `docs/automation/CHATGPT_GITHUB_HANDOVER_UIA_20261110.md` | `1ccb7f48efa85b62b046a127fdf45f53865ac3a4` | Whole 178-line ChatGPT/GitHub runbook; blob also identical on `main` |
| `handoff/foundation_implementation/authority/SQLITE_PROFILE_OWNER_AMENDMENT_20261018.md` | `e63a6fc61965532635e9c65f6159c665ae4b5df6` | Original 18 October accepted SQLite profile and preserved historical PG meaning |
| `handoff/planning/ubuntu_postgresql_transition_20261110/ADR_20261110_POSTGRESQL_ADDITIONAL_BACKEND.md` | `70fefd11f62c27b794c475861baf9038a8f1fd42` | Complete separate November owner-endorsed M00 PG proposal |
| `handoff/planning/ubuntu_postgresql_transition_20261110/EXEC_PLAN.md` | `1edea70410a86214bdf7506fb2602fa4c5f5b5ff` | Complete separate November proposed T00–T07 plan |
| `handoff/planning/ubuntu_postgresql_transition_20261110/T00_F02_INDEPENDENT_BOUNDED_REVIEW_20261110.md` | `be4126eb1d9d19f9bdd8f1705269bdb4f213a222` | Original independent F02 documentary verdict retained, not reissued |
| `handoff/ubuntu_transfer_20261110/ADR_20261110_GITHUB_REPOSITORY_HANDOVER_FINDINGS.md` | `16bc753bd5c6647d7421c4deacfd26593ceb7f5a` | Historical GitHub/Ubuntu observations; not new governing authority |

The eight `.../` entries above share the exact prefix `handoff/planning/t01_recovered_successor_20261111/`. The November ADR, proposed plan, F02 review and transfer findings were fetched separately from `planning/ubuntu-postgresql-transition-20261110` at `465de451d9c0bcd055d6385c0fc5d10cb9c49013`; they are **not** presumed to reside in F02 ancestry. The other documentary files were inspected from pinned `aa8dc…` or its exact original parent `16b7…`, as appropriate.

**Not inspected/verified for this documentary acceptance:** all M00/M01/M02 source bodies, all product-test bodies, every historical evidence ref outside the mapped original 66, physical SQLite shared libraries/source tarballs, original downloaded ZIP/bundle bytes, and actual PostgreSQL server/driver operation. No defect in these unexamined surfaces is alleged.

## 2. Exact input and F02 baseline

Fresh Git `cat-file -p`/revision checks establish:

| Object | Commit | Tree | Direct parent |
|---|---|---|---|
| Recovered F02 source | `16b7cc67f5d24336d3768e2da006819474a8c792` | `2b2bd7c1b7342f22909339a99150e2a395039e06` | `9a4f1e827accdd7cfe3d7a14d5575573589b1acd` |
| T01 proposed candidate | `aa8dc23608bb6d655aebd74e390a8b3d341735c7` | `e58d34ef63c7c52f40cfdd0d6d45120a857fb978` | `16b7cc67f5d24336d3768e2da006819474a8c792` |

`git diff --name-status 16b7cc67… aa8dc236…` shows **exactly ten added documentary files**: the runbook and the nine proposal/recovery receipt files in `handoff/planning/t01_recovered_successor_20261111/`. No tracked file is modified or deleted; in particular the six original governing/register/ledger blob identities above match exactly at F02 and T01 input. The F02 last-commit changed-path query returned just `L00/R2_G0_SQLITE_INDEPENDENT_REVIEW_REQUEST.md` and `L00/R2_SQLITE_RUNTIME_DECISION.md`.

The existing independent 10 November F02 verdict is **`ACCEPT_DOCUMENTARY_F02 / PASS_GIT_CHECKPOINT` for F02 exact bytes**. Its original scope explicitly excludes independent physical SQLite dynamic linking and all NVIDIA product tests (`T00_F02_INDEPENDENT_BOUNDED_REVIEW_20261110.md`, heading and §§3–5). This T01 review retains that finding without transforming it into general active-plan acceptance.

## 3. Independent GitHub receiver — commands and observed results

A **new** bare Git receiver was created on authorised `DESKTOP-I188O30` / WSL Ubuntu: `/tmp/nvda-t01-independent-review-20261111-receiver.git`. This is not the prior proposal Worker's receiver and did not mutate the user's existing NVDA checkout. In the commands below, `$R` is explanatory shorthand for this exact Git-dir path; literal remote invocations used the full path.

```text
wsl.exe --exec git ls-remote https://github.com/JayDEmily/nvda_29102026.git 'refs/heads/recovery/*' refs/heads/planning/t01-recovered-successor-20261111
wsl.exe --exec git init --bare /tmp/nvda-t01-independent-review-20261111-receiver.git
wsl.exe --exec git --git-dir=/tmp/nvda-t01-independent-review-20261111-receiver.git fetch --no-tags https://github.com/JayDEmily/nvda_29102026.git +refs/heads/recovery/r2-g0-f02-20261111:refs/remotes/review/r2-g0-f02 +refs/heads/recovery/legacy-d010-20261111:refs/remotes/review/legacy-d010 +refs/heads/recovery/legacy-d131-20261111:refs/remotes/review/legacy-d131 +refs/heads/recovery/legacy-m00-brief2-20261111:refs/remotes/review/legacy-m00-brief2 +refs/heads/recovery/legacy-next20-20261111:refs/remotes/review/legacy-next20 +refs/heads/planning/t01-recovered-successor-20261111:refs/remotes/review/t01-handover +refs/heads/planning/ubuntu-postgresql-transition-20261110:refs/remotes/review/ubuntu-postgres
wsl.exe --exec git --git-dir=/tmp/nvda-t01-independent-review-20261111-receiver.git show-ref
wsl.exe --exec git --git-dir=/tmp/nvda-t01-independent-review-20261111-receiver.git cat-file -p aa8dc23608bb6d655aebd74e390a8b3d341735c7
wsl.exe --exec git --git-dir=/tmp/nvda-t01-independent-review-20261111-receiver.git cat-file -p 16b7cc67f5d24336d3768e2da006819474a8c792
wsl.exe --exec git --git-dir=/tmp/nvda-t01-independent-review-20261111-receiver.git diff --name-status 16b7cc67f5d24336d3768e2da006819474a8c792 aa8dc23608bb6d655aebd74e390a8b3d341735c7
wsl.exe --exec git --git-dir=/tmp/nvda-t01-independent-review-20261111-receiver.git fsck --full --no-reflogs
```

Published recovery branch `ls-remote` and **separately fetched** `show-ref` both matched all five announced SHA-1 tips:

| GitHub published branch | SHA-1 verified |
|---|---|
| `recovery/r2-g0-f02-20261111` | `16b7cc67f5d24336d3768e2da006819474a8c792` |
| `recovery/legacy-d010-20261111` | `77471e5a851ec04e73c6dc63988868064de930f8` |
| `recovery/legacy-d131-20261111` | `fa709f645ac5ac21b861836db74ab23da9f8e17a` |
| `recovery/legacy-m00-brief2-20261111` | `0c86b187a23e750d39ce04f772f7d52c1bd578b0` |
| `recovery/legacy-next20-20261111` | `8e0c89b2cdf4ef504931fea894d89b2f85b2ce2e` |

The same fetch independently obtained the proposed handover branch `768f18672d5f8a226e806b9fff68984ae027d739` and November PG planning branch `465de451d9c0bcd055d6385c0fc5d10cb9c49013`.

**Independent manifest reconstruction**, executed by Python `subprocess` against the fresh Git receiver, without invoking the Worker's restoration script:

```python
# refs = json.loads(git show aa8dc236…:handoff/planning/t01_recovered_successor_20261111/ORIGINAL_66_REFS.json)
# Check each source ref with: git check-ref-format <ref>
# Atomically restore all literal name/tip pairs:
git update-ref --stdin
start
create <ref_1> <tip_1>
...
create <ref_66> <tip_66>
prepare
commit
# For each of 66: git rev-parse --verify <ref>, compare full tip.
git ls-tree -r --full-tree 16b7cc67f5d24336d3768e2da006819474a8c792
git fsck --full --no-reflogs
```

The above is a faithful command-method transcription with `<ref_N>` placeholders for all 66 literal entries in the immutable source JSON; the actual execution used an atomic `git update-ref --stdin` input generated from all 66 parsed records. **Observed results**: 66/66 `check-ref-format` valid; atomic `update-ref` exit **0** (`start: ok; prepare: ok; commit: ok`); all 66 original name/tip identities independently matched; 13 distinct Git tip object IDs all present; F02 **4,024** tracked entries; exact raw SHA-256 of `git ls-tree -r --full-tree` output **`6e24293d7908a3bce9e950bfd16cfa967c06c907a4f72bf54b8de0172dbdd432`**; `git fsck --full --no-reflogs` exit **0**, empty stdout/stderr after ref restoration. These are current independent **Git-source object/namespace integrity** checks.

**Limitation:** GitHub hosts five physical published source-recovery refs, **not all 66 original names**. Those 66 names were recreated from the exact manifest in the fresh receiver. This verifies all 66 declared name/tip pairs and Git objects reachable through the fetched sources. It does **not** establish that every other historical evidence ref or any non-Git SQLite asset is independently available. T02's complete separate **Tester-chat** checkpoint/asset proof remains pending; this ChatGPT documentary reviewer does not declare itself the L32 Tester.

## 4. Proposed plan versus exact recovered F02 authority

The independent comparator extracted **all** `^### L… —` leaf sections from the recovered 463-line `EXEC_PLAN.md` and the proposed 486-line `PROPOSED_EXEC_PLAN.md`. Result: **39 source leaves, 39 proposed leaves, identical leaf IDs and no omission/new leaf**. After removing each standard local-vs-proposed handover paragraph, the core contracts of **37** leaves are textually identical; the only remaining context changes are:

- **L00** (`PROPOSED_EXEC_PLAN.md` lines 79–85): adds the dated independent F02 documentary acceptance and expressly says the successor is not active until owner approval. It does not release any held profile, D identity or gate.
- **L32 / §5** (lines 383–394, 408–430): explains the historical 3.46.1/3.54.1 evidence scope and proposes the GitHub pinned-checkpoint method, while retaining the separate Tester, prerequisite-order strict product proofs, full ref/asset verification, refusal/lineage law, historical evidence and no blanket regressions. The **historical local cumulative bundle** remains an explicitly distinct fallback until owner checkpoint-method approval.

All 39 existing leaf sections contain the proposed scoped GitHub handover rule instead of the prior local leaf transfer rule; this is a **prospective authority/transport substitution**, not an installed change. Exact unchanged source `GUARDRAILS.md`, `AGENTS.md`, `tests/AGENTS.override.md`, `EXEC_PLAN.md` and both original registers were independently checked by matching their Git blobs at F02 and pinned T01. The source `EXECUTION_REGISTER.json` parses as exactly **39** original leaves; no new source-run or product-progress claim is created.

The proposal preserves, with explicit original clauses/identities: **27 mandatory new D identities (20 core + seven further)**, **28 unresolved including D145 held/paused at L31**, **seven external holds D061/D064/D065/D070/D084/D114/D115**, 98 prior historical controlled profiles and conditional 126 accounting; stock **and** selected options for D141/D142/D144 (`PROPOSED_EXEC_PLAN.md` lines 11–15, 19–67, 370–380, 395–405, 430–440). The proposal does not promote old SQLite/other evidence to current runtime or source authority. It retains the same mathematical/refusal conditions for all corresponding leaf contracts, including joint OLS and mixed-fit refusal, 30-second D142 terminal no-recovery, D144 whole matched-book/skew/units and D145 source-event-time hold (leaf sections L01a/L02/L03/L05/L06/L31/L32).

The proposed root `AGENTS` adds designated GitHub checkpoint and runbook pointers without contradicting frozen guardrails. The proposed `tests/AGENTS.override.md` preserves the worker `IMPLEMENTED_UNTESTED` versus separate L32 Tester distinction, original strict tests, historical results and bounded rerun law (`PROPOSED_AGENTS.md` lines 1–29; `PROPOSED_TESTS_AGENTS.override.md` lines 1–12; `GUARDRAILS.md` “Tests, proof and implementation” / “Planning and semantic acceptance”). **No demonstrated conflicting acceptance rule or deletion of the 39 leaf contracts was found in the inspected proposal.**

## 5. Independent JSON Schema and complete ledger comparison

On the fresh receiver, Python 3 `jsonschema` **4.19.2** `Draft202012Validator.check_schema(schema)` accepted the actual original `TEST_EVIDENCE_LEDGER.schema.json`; `list(Draft202012Validator(schema).iter_errors(proposed_ledger))` returned **0** validation errors.

Structured Python JSON equality `original['proof_obligations'] == proposed['proof_obligations']` returned **`True` for all 35 objects in order, including every nested requirement/source identity, prior evidence, case allocation and execution field**; not merely equal count. Original/proposed IDs match exactly. The only top-level changed fields are `ledger_status` (**ACTIVE→DRAFT**), `repository` and `execution_mode`; this records the separate uninstalled proposal, with no release of old evidence or product runs. Programmatic sums for the proposed 35 obligations: **0 runs; 0 authorised physical cases; 0 cases; 34 scheduled at L32 and one D145 at L31**. D145 remains `BLOCKED`, `NOT_APPLICABLE_D145_PAUSED`, zero cases, unchanged original object. Refer to `PROPOSED_TEST_EVIDENCE_LEDGER.json` lines 1–15 and its `proof_obligations` array through line 1208, and matching original `TEST_EVIDENCE_LEDGER.json` lines 1–1208.

This establishes **documentary schema and structural preservation**, not correctness/execution of any future product case.

## 6. Separate SQLite/PostgreSQL authority and automation evidence

The **18 October** accepted owner SQLite amendment (`.../SQLITE_PROFILE_OWNER_AMENDMENT_20261018.md` §§1–4) deliberately adopted a trusted-application SQLite isolation profile and preserved PostgreSQL history/semantic law. The separately fetched **10 November** owner-endorsed ADR (`.../ADR_20261110_POSTGRESQL_ADDITIONAL_BACKEND.md` §§1–5) proposes a **distinct additional M00 PostgreSQL backend**, with exact later environment/proof admissions. It explicitly retains existing **M00/M02 SQLite**, retains **M01 bootstrap**, and does not activate PG, migrate SQLite, or accept PostgreSQL 18.6 execution. The separate 10 November proposed `EXEC_PLAN.md` §§0–8 contains T00–T07 planning stages with **no competing active root**. The T01 successor `PROPOSED_EXEC_PLAN.md` §§7–10 (lines 435–486) carries this as supplemental stages rather than silently inserting PostgreSQL into the 39 leaves/35 signal obligations. Thus **no documentary incompatibility was established** between these specific scopes. Whether a later concrete M00 PG implementation satisfies public contracts is outside this review.

The identical-blob runbook `docs/automation/CHATGPT_GITHUB_HANDOVER_UIA_20261110.md` §§1, 4–6 documents **one** short-message cross-thread ChatGPT → GitHub arithmetic/result-commit demonstration and states its own limits. It is adequate documentary evidence for a *possible handover mechanism*, **not** demonstrated repeated unattended operation, independent NVIDIA semantic review, complete future asset transport, or L32 product tests. The proposed checkpoint's independent full ref/asset requirements must still be satisfied at T02.

## 7. Disposition and next authorisation gates

| T01 material condition | Evidence-based disposition |
|---|---|
| Exact pinned recovered F02 source, predecessor and T01 candidate | **VERIFIED** by fresh Git objects; not substituted with old GitHub R2 proposal |
| F01/F02 historical independent documentary verdict | **RETAINED** from original 10 November review; no new F02 verdict and no SQLite runtime inference |
| Frozen/current governing root bytes left in place | **VERIFIED** same Git blob identities |
| Original 39 leaves/semantics, 27 identities, 35 proofs, D145 and holds | **VERIFIED** documentary/structural retention; no claim of implementation acceptance |
| Full proposed root/AGENTS/test-local review | **VERIFIED** inspected proposal; no demonstrated governance or proof-law conflict |
| Proposed ledger exact schema, full original obligation equality | **VERIFIED** Draft202012 zero errors, 35/35 structural equality, 34 L32/1 L31, zero runs/cases |
| Remote published F02 + four legacy branches, 66 original ref map, inventory, fsck | **VERIFIED** independently in fresh separate bare Git receiver |
| Additional original evidence aliases/non-Git archives and SQLite binary | **UNKNOWN / NOT VERIFIED** by this narrow receiver |
| Current independent Tester-chat T02 full source/evidence/asset restoration | **NOT YET ESTABLISHED**; documentary reviewer is not the distinct product Tester |
| Current Ubuntu Python/SQLite and M00 PostgreSQL runtime/backend qualification | **NOT TESTED / NOT ADMITTED**; requires separate scope and evidence |
| Proposed root, root AGENTS, test override, ledger activation | **NOT INSTALLED**; current explicit owner acceptance and separate installation commissioning needed |
| Product tests/code changes/gates D acceptances | **NOT PERFORMED** in this review; no additional admissions |

**Final disposition: `ACCEPT_DOCUMENTARY_PROPOSAL`.** The pinned successor is a coherent, fully preserved and independently inspectable **proposal** under the requirements checked above. This is **not** owner acceptance, automatic plan promotion, T02 Tester qualification, runtime/PG proof, or permission to start G1–G5 implementation. No bounded corrective documentary deficiency was demonstrated by the inspected evidence.

**Next precise owner boundary:** review and explicitly accept or amend the exact proposed `PROPOSED_EXEC_PLAN.md`, `PROPOSED_AGENTS.md`, `PROPOSED_TESTS_AGENTS.override.md`, proposed evidence ledger and the **new GitHub pinned checkpoint strategy**, with awareness of missing non-Git/evidence-ref qualification. Only a separately authorised promotion should install them as single active root authority. Then T02 independent Tester-chat receiver/asset closure and T03/T04 separately governed environment/backend contract work must satisfy their own first unmet invariants before dependent implementation/product proof. Existing historical results and statuses remain unchanged.

**Commit/readback law:** this report is the **only new file** commissioned on the named reviewer branch; its base is exact candidate `aa8dc236…`. The review commit/tree and no-extra-path Git diff must be checked after publication, with the commit SHA and link reported in the reviewer response.
