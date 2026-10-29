# PA-02 claim-scoped product-proof control implementation plan

> For agentic workers: PROPOSED DOCUMENTARY DESIGN ONLY. If this exact authority and an execution plan are later accepted, use the native, single-worker execution method and the executing-plans workflow, one semantic unit per pass. No test or implementation execution is authorised by this document's existence.

**Goal:** Extend the existing product-proof control to support the exact D011 foundation claim while preserving the separate M00 claim and all M01 proof lineage.

**Architecture:** Keep the existing M00 authority/family/aggregate documents and schemas byte-identical. Add a claim catalogue and an exact-brief-bound foundation proof contract/admission record. Reuse the current validator/runner with claim-scoped resolution; keep kernel architecture promotion separate.

**Tech stack:** Existing CPython 3.13.5, PyYAML 6.0.3, pytest 9.0.3, mypy 1.20.1 and standard library; no new dependency or runtime architecture owner.

**Spec:** `FOUNDATION_IMPLEMENTATION_BRIEF_PROPOSED.md` sections 3, 8–10, together with the exact companions incorporated by its revised bytes. Preparation starts at `be16a8e1641ed9f1457a81c464948cb4d95ecd22`, tree `0d186621e6add96affe49c6971d0a62dbcef1656`. The previous proposed brief hash is `8f51e887fd8a71ceabcafc38444a033de9db284f4647f4012e29f5ea52fc668b`; the revised proposal is a different byte object requiring its own acceptance. Neither version is recorded here as accepted for implementation.

## Global constraints

- Current pass: documents, primary-source copies, standard-library parsing and file/Git/archive integrity only. No tests, application imports/execution, runtime validators, lint, type checking, database/provider calls or environment bootstrap.
- Frozen guardrails/agents, closed root plan, mathematical/catalogue/workbook/register/backlog, production source, tests, active schemas/configuration and main remain unchanged.
- No guessed numeric foundation identifier, automatic allocation/activation, M01 migration/retirement, native-source admission or live external effect.
- M00 keeps all 13 existing required product IDs, `IA22R01-PROD-009`, forbidden predecessor `IA17-PROD-009`, exact BICP/IRB and six current families. Product tier treatment stays `NOT_CLASSIFIED`.
- Foundation claim means only the controlled D011 pilot. The remaining 125 foundation and 83 downstream IDs stay unavailable through its materialisation path; the full target and peer allocations remain intact.
- Source/test presence, catalogue validity, admission, adequate proof, executed proof and owner acceptance remain separate claims.

## Review focus

1. A stale authority or proof file still passes because only its path/ID was checked: bind exact bytes and check the admitted generation before and after execution.
2. A M00 obligation/family is relabelled as foundation proof: retain distinct profiles and reject cross-claim membership or overlapping physical ownership.
3. The 87 M01 files disappear from control accounting: enumerate them explicitly as preserved transitional evidence without admitting or discrediting their historical propositions.
4. An empty, skipped, xfailed, deselected or collection-broken run is reported as successful proof: require complete collection and strict outcomes for every selected family.
5. RED proof is blocked by a demand that production already be active: separate authorised proof development for a registered bootstrap owner from promotion, which still requires the admitted active target and all applicable evidence.

## 1. What the supplied evidence establishes

The September 13 handover describes a proposed admission tranche ending at a BICP, before physical product proof/code. Its old empty-registry state is historical. The September 19 CODE-001 method and its current-state file explicitly describe a proposed V0 whose independent challenge and programme freeze had not occurred in that package. They are useful method evidence; supplying them does not adopt C00–C12 or activate their old plan.

The extracted N15 and N19 hashes exactly match the current repository's VI-09 design and M00 BICP lineage:

| Record | Exact SHA-256 | Relevant meaning |
| --- | --- | --- |
| N15 | `62bbaed0306e1cf3e85de3e482284f967a971e5ff806d75e7674dd7c35d8403e` | P01–P08/P12: claim-limited authority, exact family/boundary/environment, negative cases, attributable execution, complete aggregate and historical-status limits. |
| N19 | `d46567a2594657e26c54d3c0bb45e44c4adadca58b8ca349d516f980dc7504fb` | P01/P02/P04/P05/P11/P12: product/architecture axes remain distinct and scope must be re-derived after a changed claim. |

Those exact records are copied under `../evidence/pa02_sources/` for portable readback. Current kernel law continues to govern its own jurisdiction. The revised foundation proposal incorporates the named general proof requirements for its proposed claim; it does not activate N15's unrelated packet, modifier, execution, portfolio or replay profiles, or turn N19's old state descriptions into current facts.

Current primary evidence is `implementation/proof/VI09_PRODUCT_PROOF_CONTROL_DESIGN.md`, its worker/evidence lineage, the three active product-proof documents/schemas, and complete validator/runner source. VI-09 intentionally implemented one Raw Signal claim. This was a bounded first-case control, not a promise of a generic multi-owner mechanism. Git history introduces the validator and authority schema at `6d7eede672ede38ea0a9afe5acee4157b8b9bf72`; no later change to those implementation files was found on the inspected lineage. The later six-family M00 registry is separately preserved. Historical VI-09 green results are not execution evidence for this candidate.

Static path comparison establishes 93 current physical product test files: six under `raw_signal` match the current M00 family registry; 87 under `derived_signal` do not belong to that registry. The current validator compares the whole physical product tree against its six M00 paths, so its parity condition is unsatisfied by these source sets. This is a direct source/set comparison, not a validator run or a new judgement on all 87 tests' semantic adequacy/acceptance.

## 2. Recommended control change and authority projection

Use **claim-scoped validation and execution through the existing tools**. Do not retarget the M00 authority, widen its IA identifiers, invent a foundation BICP or move tests to avoid admission. A foundation claim may derive from its independently accepted exact brief and incorporated proof contract; AK-INGRESS does not mandate the old M00 BICP methodology for every later owner.

The revised single foundation brief supplies three proposed projection intents: create category M with machine responsibility name `neutral_market_measurement_truth`; bounded modify M00 for the reader declaration; bounded modify G01 for this proof-control mechanism. G01 is currently the framework `proof_and_promotion` governance plane, with no runtime dependency. No new governance object or runtime owner is created for a validator.

The human responsibility label remains “neutral market measurement truth”. The underscore spelling is necessary for the actual ingress schema's create-name pattern `^[a-z][a-z0-9_]*$`. It is not a numeric reservation or a change in product meaning.

This is a proposed control contract and implementation plan, not an applied source patch. A future worker must present the resulting exact schema/configuration/tool diff against this contract before applying it to the active candidate. Unspecified product meaning is not implementation freedom. Routine function bodies may be written from the exact interfaces/invariants below only after authority exists.

## 3. Exact file changes proposed for later execution

| Future surface | Exact change / responsibility |
| --- | --- |
| `config/product_proof/claims.json` | New closed claim catalogue; registers the two independent profiles and explicit transitional path accounting described below. |
| `schemas/product_proof_claims.schema.json` | Closed schema for the catalogue; exact required/forbidden fields in section 4. |
| `schemas/accepted_brief_product_proof.schema.json` | Closed schema for the foundation contract in `FOUNDATION_PILOT_PROOF_CONTRACT_PROPOSED.json`; no permissive replacement for the M00 schema. |
| `schemas/product_proof_admission.schema.json` | Closed schema for current-generation pointer and immutable generation record described in section 5. |
| `config/product_proof/market_measurement/admission.json` | Initial exact object `{"schema_version":"1.0","current_generation":null}`. Empty is incomplete, never successful proof. |
| `tools/product_proof_claims.py` | Shared catalogue/path/authority/admission resolver; immutable typed result for both entry points. It owns control mechanics only. |
| `tools/validate_product_proof.py` | Preserve its callable's default M00 claim; add explicit `--claim`; dispatch legacy validation unchanged in meaning and foundation validation through the shared resolver. Replace global M00-only parity with the explicit complete accounting rule. |
| `tools/run_product_proof_gate.py` | Preserve default M00 aggregate ID; resolve one selected claim once; run only its admitted families; enforce strict outcomes and pre/post source/proof integrity. |
| `tools/product_proof_outcomes.py` | Small pytest plugin for observed collection/outcomes, fresh per-run report and no-skip/no-xfail policy; no product calculation. |
| `tests/architecture/test_proof_control.py` | Add the section 7 generic admission/control falsifiers to this existing physical family. Preserve its existing valid tests. No D011 equation or product behaviour is proved in this architecture family. |
| `config/proof/test_families.yaml` | For existing family `proof_control` only, add AK-INGRESS-001/002 to its existing AK-PROOF-001/002 binding for exact brief/admission control checks. Keep all 11 physical architecture families, blocks and promotion-set membership unchanged. |

The existing `config/product_proof/{authority,families,aggregates}.yaml` and `schemas/product_proof_{authority,family,aggregate}.schema.json` remain exact. Existing M00 tests and BICP/IRB are untouched. `Makefile`, project dependencies, production packages and all domain mathematical authority are outside PA-02's implementation surface.

Physical D011 test authoring/admission and calculator code are later semantic units. This control unit must close with the foundation still lacking an admitted proof generation; do not author a dummy product test to make it ready.

## 4. Catalogue, contract and path-accounting shapes

All JSON objects reject duplicate keys and unknown properties. Use only the schema subset actually supported by `nvda_desk.architecture.schema`: type/required/properties/items/const/enum/pattern/minLength/minItems/uniqueItems/allOf/if/then/not. Do not assume `$ref`, `oneOf`, `else`, URI resolution or new schema features work. Do not relax the current schema engine. Use explicit semantic checks for path prefix, uniqueness, cross-reference and conditional relationships.

`claims.json` is an exact byte copy of the supplied `PA02_PRODUCT_PROOF_CLAIMS_PROPOSED.json`, which is incorporated by the revised brief. It has exactly `schema_version="2.0"`, `control_authority`, `claims` and `transitional_dispositions`. `control_authority` has exactly `brief_path` and `binding_path`, pointing to the revised brief and its future native binding. That binding must authorise the G01 modification. `claims` is a non-empty array of distinct entries. Common fields are `claim_id`, `profile`, `physical_root`. IDs use the existing lower-case identifier pattern; paths are safe repository-relative POSIX paths. Profiles are exactly:

| Profile | Additional required fields | Forbidden fields |
| --- | --- | --- |
| `legacy_bicp_v1` | `legacy_config_root` | `contract_path`, `binding_path`, `admission_path` |
| `accepted_brief_v1` | `contract_path`, `binding_path`, `admission_path` | `legacy_config_root` |

Initial entries are exactly:

```json
[
  {
    "claim_id": "raw_signal_occurrence_truth_product",
    "profile": "legacy_bicp_v1",
    "physical_root": "tests/product/raw_signal",
    "legacy_config_root": "config/product_proof"
  },
  {
    "claim_id": "neutral_market_measurement_truth_pilot",
    "profile": "accepted_brief_v1",
    "physical_root": "tests/product/market_measurement",
    "contract_path": "handoff/foundation_implementation/authority/FOUNDATION_PILOT_PROOF_CONTRACT_PROPOSED.json",
    "binding_path": "implementation/authority/FOUNDATION_IMPLEMENTATION_AUTHORITY_BINDING.yaml",
    "admission_path": "config/product_proof/market_measurement/admission.json"
  }
]
```

`transitional_dispositions` is the single path `handoff/foundation_implementation/authority/PA02_PRODUCT_PATH_DISPOSITIONS_PROPOSED.json`. It enumerates the exact 87 preserved M01 paths and six M00 paths, with baseline SHA-256 as provenance. Its digest is incorporated by the revised brief. Its own required fields/types are exactly those supplied in that JSON; no additional dispositions are inferred from a directory wildcard. Changing that approved path population requires a reviewable scope amendment. Baseline content hashes are not a runtime freeze on unrelated M01 development, and confer no proof admission.

The foundation contract's exact JSON bytes are the supplied `FOUNDATION_PILOT_PROOF_CONTRACT_PROPOSED.json`. Its closed top-level fields are `schema_version`, `claim_id`, `semantic_brief_path`, `target`, `proof_axis`, `product_tier_treatment`, `architecture_proof_axis`, `required_proof_ids`, `families`, `required_support_files`, `optional_support_files`, `execution_policy`. Target fields are category/responsibility name/package/public seam; no numeric object ID. Version is `1.0`; axes/tier are fixed as supplied. Required IDs are exactly ordered FND-P01–P07, with no duplicates.

Each contract family has exactly the fields supplied in the JSON: ID, path, proof IDs, required test names, boundary, proof levels, inputs, substitutions, four case dimensions, failure signals, limitations/nonclaims, environment/material versions, tier and command. Every scalar text is non-empty; text arrays are distinct/non-empty except an explicitly empty dependency-substitution list if none is used. All four case dimensions contain non-empty `cases` XOR a non-empty bounded `not_applicable_reason`. Proof levels use the existing six-value vocabulary. Paths are distinct and below the declared physical root; commands are exactly `python -m pytest <that path>` as metadata, never shell-evaluated. Proof-ID union equals the required set, and family/name/proposition associations equal this incorporated contract, not a worker's rewritten interpretation.

The profile is not a central hard-coded foundation-ID exception. It validates each claim against that claim's accepted, hash-incorporated contract; unrelated identifiers cannot enter by matching a broad regex. The legacy profile still derives its exact 13 IDs/route/bindings from its unchanged M00 BICP.

### Complete physical accounting

Enumerate every physical `tests/product/**/test_*.py` path. Partition it into exactly one of: a selected/other registered claim's admitted family; a declared candidate family awaiting admission; or an exact preserved transitional path. Reject overlapping namespaces/claims, duplicate ownership, undeclared/moved/new test paths, path traversal, absolute paths and symlink escapes. An expected missing admitted physical file is an error. A declared candidate file is visible as unadmitted and cannot run as promotion proof. The empty pre-authoring foundation directory is lawful and incomplete.

M00 aggregate membership remains its exact six admitted families. The 87 M01 paths are accounted for but are not members of M00 or the foundation aggregate. Their original source/historical evidence remains available; outstanding proof/reuse dispositions retain WI-11/WI-23/WI-29 receivers. This explicit proposed jurisdiction change replaces the old one-claim/global-path assumption; it does not silently ignore files, revoke separately accepted historical evidence or assert whole-M01 completion.

Do not invent a repo-wide “all product PASS”. Each selected aggregate names its claim, target, authority digest, admitted generation and exact paths. Product claim results and `architecture_kernel` remain separate evidence.

## 5. Exact authority, proof generation and target states

For the foundation profile, read the native binding schema and exact brief bytes; require `ACCEPTED_FOR_IMPLEMENTATION`, non-empty external authority reference and matching raw SHA-256. Actual human acceptance remains a higher-authority fact the schema cannot prove. Require the exact create-name/category and bounded M00/G01 modify intents in the revised brief. Numeric create candidates are never durable allocations merely because a binding validates.

The revised brief contains one exact line for each of `PA02-PROOF-CONTRACT-SHA256`, `PA02-PATH-DISPOSITIONS-SHA256` and `PA02-CLAIM-CATALOGUE-SHA256`, followed by colon/space and 64 lowercase hexadecimal characters. Require each exactly once and match the corresponding companion's bytes, including the active catalogue copied from the proposal. Validate the control-authority binding before letting a catalogue classify or exclude any physical path; the foundation claim's semantic brief/binding must match that control authority in this bounded version. This is a narrow companion byte-binding grammar, not a Markdown semantic parser. The proposal itself is incorporated in the brief's exact Annex table. A changed proposal, contract, catalogue, path disposition or brief requires fresh appropriate acceptance; do not inherit the previous proposed digest.

Resolve the actual owner by its exact admitted package/seam in current architecture state, and verify category/responsibility/allocation. No zero/multiple matches, guessed M02 or freshly re-resolved create candidate may substitute for the allocated identity. Pre-admission proof design may remain non-runnable. For authorised development proof, a separately registered bootstrap/non-composable owner is sufficient target attribution; promotion additionally requires the active admitted owner and applicable architecture evidence. This distinction does not permit runtime composition of a bootstrap owner.

The admission pointer has exactly `schema_version="1.0"` and `current_generation`, where null means unadmitted. A non-null pointer is an object with exactly repository-relative `path` and `sha256`, referring to an immutable generation JSON under `config/product_proof/market_measurement/generations/`.

A generation has exactly: `schema_version="1.0"`, `claim_id`, positive integer `generation`, `brief_sha256`, `binding_sha256`, `contract_sha256`, actual `implementation_target_id`, `adequacy_review_ref`, `admission_authority_ref`, `family_files`, `support_files`, `previous_generation`. References are non-empty. Each file row has exactly path and SHA-256; rows are distinct and match required contract families/support files plus any explicitly used optional helper. The binding digest must equal the exact native acceptance/projection record used for this generation, not just another record naming the same brief. The first generation's previous pointer is null; later generations point to the exact preceding file/hash. Keep all generations in Git and reject a hash mismatch. A new generation requires fresh adequacy review/admission; do not reseal a changed test around the implementation.

No such admitted generation exists in this preparation. Null is the truthful initial state. Revocation clears the active pointer in a separately authorised commit while retaining the old generation; it cannot silently reinstate an earlier generation. New generations must advance the number and reference the retained predecessor. The generation file/hash and authority acceptance are reviewed before its pointer becomes current.

The resolver distinguishes pending authority, target and proof from invalid supplied authority. A missing not-yet-issued binding/target/generation produces an explicit non-runnable state. A supplied but malformed, mismatched or conflicting one is an error. Neither state may be reported as product proof success. `READY_FOR_PROOF` means eligible to run, not green or admitted implementation.

## 6. Exact tool interfaces and execution behaviour

Define frozen internal records in `tools/product_proof_claims.py`:

```python
@dataclass(frozen=True, slots=True)
class AdmittedProductFamily:
    family_id: str
    path: str
    proof_ids: tuple[str, ...]
    required_test_names: tuple[str, ...]
    sha256: str | None

@dataclass(frozen=True, slots=True)
class ProductProofClaim:
    claim_id: str
    profile: str
    target_id: str | None
    target_status: str | None
    authority_sha256: str | None
    generation_sha256: str | None
    state: str
    families: tuple[AdmittedProductFamily, ...]
    support_files: tuple[tuple[str, str], ...]
    governed_files: tuple[tuple[str, str], ...]

def load_product_proof_claim(
    repository_root: Path, claim_id: str,
) -> ProductProofClaim: ...

def validate_product_proof(
    repository_root: Path,
    claim_id: str = "raw_signal_occurrence_truth_product",
) -> list[str]: ...

def run_product_proof(repository_root: Path, aggregate_id: str) -> int: ...
```

`state` is one of `AWAITING_AUTHORITY`, `AWAITING_TARGET`, `INCOMPLETE_NO_PHYSICAL_FAMILIES`, `INCOMPLETE_COVERAGE`, `READY_FOR_PROOF`. The first applicable unmet prerequisite determines state, in that order. Legacy M00 has its existing active-target requirement and its existing three readiness values. Unknown claim/profile is an error; never fall back to M00. No runtime import of these governance tools is added.

Refactor the existing validator's legacy checks into an internal legacy-profile routine without changing BICP, IRB, route, tier, predecessor, metadata or coverage requirements. Its physical parity input is the claim's accounted path set; global completeness is checked by the shared partition. Do not simply change the scan to `raw_signal` and lose other paths.

The CLI adds `--claim`, defaulting to the existing M00 ID. Its successful exit means control validity only and must print that distinction plus the exact readiness. Missing pending authority/target/proof is explicitly incomplete; a supplied invalid authority fails non-zero. The aggregate runner continues to use `--aggregate`, default unchanged. It calls the shared resolver once and uses that immutable snapshot for membership and execution.

Runner exit meanings: 0 only for a complete observed successful selected product aggregate; 1 validation or test/outcome failure; 2 dirty governed start; 3 unknown aggregate; 4 pending/not-ready/inactive promotion target; 5 empty or incomplete observed collection; 6 unexpected governed mutation. Do not convert an infrastructure error, skip or missing dependency into intended RED or success.

Before running, require clean tracked/untracked worktree as currently required and capture content hashes for the brief, binding, contract, catalogue, admission pointer/generation, selected family/support files and active control/registry/tool sources. Build argv from the pinned interpreter and resolved family paths; do not evaluate metadata commands with a shell or honour arbitrary extra selectors. Clear inherited `PYTEST_ADDOPTS` that could deselect/change mandatory collection. Use a new temporary outcome-report directory outside governed data, with a fresh nonce and expected file/test-name map.

The runner loads `tools/product_proof_outcomes.py` as a pytest plugin through `-p product_proof_outcomes`, with the tools directory explicitly available to that subprocess. The plugin observes collection and all test reports; it does not supply product fixtures or expected values. It writes a fresh JSON report with nonce, exact collected node IDs, per-file counts, pass/fail/skip/xfail/xpass counts, collection errors and final session exit status. Write through a temporary file then atomic rename. Missing/invalid/stale report is failure. Reject zero collected tests in any selected family, missing mandatory foundation test names, collection errors, deselection of required proof, every skip/xfail/xpass and any failing outcome. Lawful optional absence is a passing assertion about absence, not a skipped test.

The legacy M00 default also receives this strict aggregate outcome guard: N15-P07 already requires failed/skipped-without-authority proof to block. This strengthens enforcement of its existing obligation; it changes no accepted product proposition or test. No skip waiver is proposed. Targeted development commands may execute an admitted proof slice after explicit execution authority, but cannot be presented as aggregate promotion evidence.

After the subprocess, compare the exact governed-file hashes and repository state with the captured snapshot even if tests fail. A clean `git status` alone cannot detect ignored tracked-content side effects or an admitted test changed during execution and restored incompletely. The report must state what ran, exact candidate/authority/proof/environment and observed outcome. Neither the runner nor a report activates the owner or approves release.

## 7. One coherent future control implementation unit

**Consumes:** revised exact foundation brief and its four incorporated PA-02 companions; existing M00 authority/control bytes; native binding schema; current G01 and proof laws; a separately accepted execution plan and test authority.

**Produces:** the section 3 control changes, with preserved M00 semantics and truthful incomplete foundation state. It produces no D011 product tests/code and no foundation proof PASS.

- [ ] Derive and commit discriminating control proof in the existing physical `test_proof_control.py`, with the exact additional proposition admission described in section 3, before changing tool behaviour. Assertions must cover the matrix below. Retain all current valid tests.
- [ ] Under explicit future test authority, run `python -m pytest tests/architecture/test_proof_control.py`. Guard a not-yet-existing resolver/plugin check inside the test so intended RED is an attributable missing-capability assertion, not a collection/import crash. Establish a lawful fixture/positive control before relying on mutated negative cases. Missing interpreter/dependencies are infrastructure failures. Preserve RED and its commit.
- [ ] Create only the exact catalogue/schemas/resolver/plugin/admission pointer and bounded entry-point changes in sections 3–6. Keep the foundation pointer null. Present the concrete source diff for review against this accepted contract before applying it to the active implementation candidate; do not broaden scope on a convenient failing check.
- [ ] Run the admitted targeted control proof, `make lint`, `python -m mypy tools/product_proof_claims.py tools/product_proof_outcomes.py tools/validate_product_proof.py tools/run_product_proof_gate.py`, native authority validation and `make promotion-gate` under the accepted execution scope. Check `python tools/validate_product_proof.py --claim raw_signal_occurrence_truth_product` and the foundation counterpart: the latter must truthfully report incomplete before an admitted generation exists. The real retained M00 aggregate `python tools/run_product_proof_gate.py --aggregate raw_signal_occurrence_truth_product` is required runner regression after its exact existing environment, including PostgreSQL, is established. A blocked required regression remains blocked; it cannot be replaced by control-fixture success. These product tests supplement control tests and do not prove D011 or other new domain behaviour.
- [ ] Obtain an independent semantic/control review of the exact candidate, including the default M00 route and preserved path dispositions. Record all observed results and first failures. Owner acceptance closes this control unit only; D011 proof/code remains later work.

| Future falsifier | Required observation |
| --- | --- |
| `test_legacy_m00_claim_is_preserved` | Exact 13 IDs, six paths, route/BICP/IRB/tier/predecessor remain; existing corrupt-BICP/route/metadata cases reject. |
| `test_foundation_claim_is_separate` | Exact five contract families/seven FND IDs; M00 or AK IDs cannot enter it; foundation IDs cannot enter M00. |
| `test_native_brief_and_companion_bytes_are_bound` | Wrong/changed byte hash, duplicate marker, missing acceptance, invalid create name or fabricated numeric create field fails; schema validity alone does not prove human approval. |
| `test_physical_product_partition_is_complete` | Six current M00 and exact 87 preserved M01 paths are accounted for; extra/nested/moved/overlapping/unowned/symlink path fails. M01 source/history is retained and not counted as current foundation proof. |
| `test_pending_authority_target_and_empty_proof_are_not_success` | Null pointer and absent target/binding remain incomplete; malformed supplied objects fail; runner cannot return 0. |
| `test_target_status_does_not_make_red_circular` | Registered bootstrap target permits separately authorised admitted development proof; inactive target cannot pass promotion; package/seam mismatch or ambiguous owner fails. |
| `test_proof_generation_hash_and_supersession` | Edited/replaced proof/support bytes, stale review/context, wrong target/generation or pointer/hash mismatch fails; revocation retains old generation and blocks execution. |
| `test_aggregate_collects_all_required_proof` | Zero/missing mandatory collected function or whole family, selector/deselection or collection error is non-success. |
| `test_skipped_xfailed_and_xpassed_proof_cannot_pass` | Each outcome prevents success for both claim profiles; green pytest exit alone is insufficient. |
| `test_outcome_report_is_fresh_and_exact` | Missing report, stale nonce, wrong node/path set, corrupted JSON or mismatched exit status fails. |
| `test_governed_mutation_and_dirty_start_fail_closed` | Dirty start or changed governed bytes after a probe blocks; no post-test hash update may reseal it. |
| `test_claim_membership_is_registry_derived` | Unknown claim/profile or arbitrary command cannot fall back to an aggregate; exactly the selected admitted paths execute, architecture/product results remain distinct. |

These are proposed test names/assertions, not authored or executed physical tests. Required review remains independent of worker helper composition. The reviewer must directly sequence: null admission -> attempted run; accepted generation -> changed file -> attempted run; good pytest exit with skip report -> rejected aggregate; and two claims -> cross-claim injection -> rejection.

## 8. Acceptance and precise remaining boundary

The design closes the documentary PA-02 design question: exact claim separation, source authority, target lifecycle, path accounting, proof generation, metadata and outcome enforcement are specified. It does **not** close PA-02's implementation/proof prerequisite. No active control is changed, no test is authored/run and no physical proof generation exists.

Before implementation: accept the revised foundation brief's exact bytes and the expressly incorporated PA-02 contract/proposal; accept/activate the successor root plan; record genuine external authority in native ingress; obtain the bounded G01/M00/new-owner admissions and explicit future test/implementation scope. An exact implementation diff must then be reviewed/applied within that authority. No separate decision about whether to reactivate CODE-001 is needed: this proposal does not adopt it.

The current owner instruction “Go” is recorded as authority to prepare this proposal after the prior brief, not as a fabricated `ACCEPTED_FOR_IMPLEMENTATION` receipt. The prepared artefacts are concrete for owner review. All full-target source/model/actual-state/consumer/transition holds remain unchanged.

## 9. Provenance, preparation checks and supplied-source limits

Only the September 13 admission package and September 19 method package were needed from the new attachments. Relevant members were read directly from the supplied local archives and copied byte-identically. The remaining ten packages were not used to broaden this unit; no bootstrap/runtime asset was executed.

| Supplied archive | SHA-256 |
| --- | --- |
| `NVDA_IMPLEMENTATION_ADMISSION_PM_HANDOVER_FULL_GIT_20260913.tar(1).gz` | `2f6fab54fa32b076da1baf250e699ed29ff21cc0e3707c424846f39dab92503a` |
| `NVDA_CODE_001_BICP_TO_CODE_METHOD_FULL_GIT_20260919.tar(2).gz` | `f7b2a53a5c7abff9322e8fc216d571266a1de9919902b536d81f1e79d80663cb` |

Source members: first package `PM_HANDOVER.md` and `METHOD-006_nvda-normative-corpus-reconciliation/normative/records/{N15_PRODUCT_PROOF,N19_ARCHITECTURE_PROOF_PROJECTION}.md`; second package `CODE_001_METHOD.md` and `CURRENT_STATE.md`, beneath their original archive roots. The copied current-state filename is qualified by date to avoid ambiguity. Their source bytes are evidence with the jurisdiction described above, never an activated historical plan.

Preparation self-review compares this design with A01 sections 3/8/10, actual VI-09 schemas/validator/runner, native ingress schema/implementation, N15/N19 and the complete 93-path inventory. The native create-name spelling is corrected in the revised proposed brief. Mechanical checks must confirm all seven FND IDs map to the same five physical paths/named propositions; all 93 existing paths are accounted for exactly once; supplied member copies and incorporated hashes match; only documentary paths change; old M00/control/production/root-plan/main bytes remain exact. No execution or independent-review result is claimed.

Final delivery includes the revised proposed brief, proof contract, exact path-disposition companion, this plan and the primary-source copies in one recoverable full-Git repository. The brief's final SHA-256 is computed after these exact companions are incorporated; no circular/self-referential digest is embedded.

TS: 17-10-26 21:39
