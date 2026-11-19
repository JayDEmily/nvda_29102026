# NVIDIA V2 D091/L01b — independent non-product receiver and runner preflight

**Review date:** 20 November 2026, Melbourne.  
**Disposition: READY_FOR_CASE_RELEASE_DECISION — NON-PRODUCT PREFLIGHT ONLY.**  
**Product execution: HELD / NOT AUTHORISED.**  
**Reviewer jurisdiction:** a separate independent preflight assessor, not the strict product Tester. No product imports, pytest collection, tests, test results, Tester appointment, case/ledger mutation, branch merge, main promotion, D145, provider connection or PostgreSQL activity.

## 1. Exact reviewed boundary and authorities

Repository: JayDEmily/nvda_29102026, Worker PR #27. The **sole candidate** is b7d044a4f84b7f70703322c250cbd82cee6f4589, tree 0704cd4ebe09801e7116ed517cceda756f5e1dbf, with direct parent 4c8124dae1d88ce293e916f18734ab18b02ad240. The commission is later, **not** the candidate: Worker commit b2a448684a8a2bc6e1495ae461fe637ea92d3622, full path handoff/m02_completion_28_execution/L04/D091_PROOF_ENTRY_20261119/INDEPENDENT_RECEIVER_RUNNER_PREFLIGHT_COMMISSION.md, Git blob 64a89044132ad2f989af2230423c3ef3574f603f; full text inspected.

Complete governing GitHub reads on the pinned candidate: GUARDRAILS.md (Git blob 54a4407609941f63f6b902076688ff102a3d5ba2), AGENTS.md (b5b8f73bfef62cf34643aef419e6931599ad08b1), tests/AGENTS.override.md (66666cc012889e585ef4da80049d5ee2a0244c53) and complete 61,320-character root EXEC_PLAN.md in successive sections (76e8dd7af85cee33e306c351206e69fc049129fb). Installed governance receipt handoff/astra_adr_continuation_20261115/INSTALLATION_RECEIPT.md (e57e705184ec8d5d4f5804c3c1473cfc8b975483) records exact owner installation on the Worker branch. Inherited "proposed/not active" drafting labels in root do **not** undo that subsequent exact installation. Its accepted dependency-focused proof windows and PINNED_REMOTE_CHECKPOINT are prerequisites, **not** case execution releases.

Other complete applicable governing/preflight reads on the pinned candidate:
- handoff/planning/t01_owner_lint_integration_20261115/DEPENDENCY_WINDOWS.md, Git blob 8edc15a1af78482060091edb4db4e287a3d63a98.
- handoff/m02_completion_28_execution/L04/D091_PROOF_ADMISSION_PREP_20261116/RUNTIME_TRANSFER_AND_TESTER_GATES.md, blob c8a55aa3d3031af14a30754b3d5d988cd9101b97.
- handoff/astra_adr_continuation_20261115/RUNTIME_QUALIFICATION.md, blob c76b33d681293b18fea6482a4fd7e910c76c06cf.
- handoff/astra_adr_continuation_20261115/OUTSTANDING_ASSETS_CURRENT.json, blob 91aefda37293af24552cbf662300dc51d07fced3.
- handoff/planning/t01_recovered_successor_20261111/GITHUB_REMOTE_RECEIVER_RECEIPT.json, blob 36ca7cb350d8e4a5d30bbf91158254eec275ecb4.
- handoff/m02_completion_28_execution/L04/D091_POST_INSTALL_REGISTRATION_20261119/REGISTRATION_CLOSEOUT_AND_HOLDS.md, blob d1109c6c3ec3411ac924b42b488e1ee1cbb7793e.
- The actual ledger, two physical authored tests, owner-adopted R112 source/test-only policy, proposal, active claim/generation/pointer, product-proof loader/gate/outcomes entrypoints and package configuration were inspected at the pinned candidate. Historical independent acceptance reports were inspected at their **separate original review commits**, not falsely presumed to be files in this Worker tree: exact case adequacy 38d4b44c9bceca883ed0a676e7b9b36d684ad54e, conditional reference applicability 76fe3adba5f6a0f3e003997e03f87a2e56614b71, generation preinstallation b15a9ee49e7d3d36e7d42a18ee956c9447f853e8 and post-installation c7ebfbf10810d483d926cd00c1a4983a6c07e461. They clear documentary design/registration only, not product execution.

The existing owner's latest "So do what you need to do" continued in-scope proof prerequisites. It did **not** name the sole independent strict Tester or individually convert false ledger case-execution flags into true. The earlier exact implementation approval and generation-1 registration approval are already recorded and are **not** requested again. An independently evaluated separate, candidate-bound **case-release/Tester designation** is still required.

## 2. Independent fresh Ubuntu receiver — directly observed, verified

New isolated receiver, **not** the existing Worker/Tester checkout: /home/jds/nvda_d091_independent_receiver_20261120_b7d044 on online Windows DESKTOP-I188O30 / WSL Ubuntu, user jds. Created with git init and origin=https://github.com/JayDEmily/nvda_29102026.git, fetched the specified Worker branch and all five named recovery branches, and detached checked out the **exact** candidate. Git version 2.53.0. Neither source checkout nor Worker branch was modified.

Recorded command procedure (all in fresh isolated receiver, via Remote Desktop Commander):

    git init /home/jds/nvda_d091_independent_receiver_20261120_b7d044
    git -C /home/jds/nvda_d091_independent_receiver_20261120_b7d044 remote add origin https://github.com/JayDEmily/nvda_29102026.git
    git -C RECEIVER fetch --no-tags origin refs/heads/work/t01-d091-finite-adequacy-20261116:refs/remotes/origin/work/t01-d091-finite-adequacy-20261116 [plus each of five recovery branch refs below, with exact destination remote alias]
    git -C RECEIVER checkout --detach b7d044a4f84b7f70703322c250cbd82cee6f4589
    git -C RECEIVER rev-parse HEAD HEAD^{tree}
    git -C RECEIVER ls-tree -r --full-tree HEAD
    git -C RECEIVER ls-files
    git -C RECEIVER status --porcelain=v1
    git -C RECEIVER fsck --full

"RECEIVER" in command templates means the absolute receiver directory named above, not a shell variable. Git fetch, checkout, ls-tree, ls-files, status and **git fsck --full** returned exit code **0**. Freshly verified output:

- HEAD: b7d044a4f84b7f70703322c250cbd82cee6f4589 (exact).
- Tree: 0704cd4ebe09801e7116ed517cceda756f5e1dbf (exact).
- Full tracked leaf-tree inventory: **4,339** paths; SHA-256 of raw git ls-tree -r --full-tree HEAD stdout (with terminator newlines): **9aa670a5ce63d059b5b9037d9e366e4b71c2a0f550251a709e22ad5e755a9e22**. Independently enumerated git ls-files count: 4,339.
- git status --porcelain=v1: **empty**; no modified/untracked receiver files.
- git fsck --full: **exit 0**, stdout empty, stderr empty, after original ref restoration and after six additional evidence-commit refs fetched. This establishes reachable object closure of the fetched names/objects, not proof of every GitHub ref never enumerated.

Verified fetched recovery alias tips exactly:
1. recovery/legacy-d010-20261111 = 77471e5a851ec04e73c6dc63988868064de930f8
2. recovery/legacy-d131-20261111 = fa709f645ac5ac21b861836db74ab23da9f8e17a
3. recovery/legacy-m00-brief2-20261111 = 0c86b187a23e750d39ce04f772f7d52c1bd578b0
4. recovery/legacy-next20-20261111 = 8e0c89b2cdf4ef504931fea894d89b2f85b2ce2e
5. recovery/r2-g0-f02-20261111 = 16b7cc67f5d24336d3768e2da006819474a8c792

For original historical refs the actual pinned Git-tracked manifest was parsed directly, **not a prior review summary**: handoff/planning/t01_recovered_successor_20261111/ORIGINAL_66_REFS.json, Git blob 162b242eee672bbaa1b4a1e30d63bb2d71657fe3, byte SHA-256 **7cb2abfd6e5a4828c6a1e61a1e960d5649c4ab59449423d9189256ee425d3606**. There are **66/66 unique exact original ref names**. For **each** entry, used git cat-file -t <tip> (confirmed commit), git update-ref <exact original ref> <manifest tip>, then independently git rev-parse --verify <exact original ref> and compared full SHA. **66 verified, 0 missing, 0 wrong tips, 0 wrong names, 0 object-type failures.** The original names are recreated locally; GitHub's five recovery aliases are **not** falsely identified as the original 66 names.

Additional independently fetched and Git-fsck-validated evidence commits in **distinct local refs/receiver/evidence/**: 38d4b44c9bceca883ed0a676e7b9b36d684ad54e, 76fe3adba5f6a0f3e003997e03f87a2e56614b71, b15a9ee49e7d3d36e7d42a18ee956c9447f853e8, c7ebfbf10810d483d926cd00c1a4983a6c07e461, e64cc5b69279a088cc11c9c74d146a0fecb30517 and 5f47fdce8064d7cfcb452621323cbcca57af167d. These are evidence aliases, **not part of the original 66**. The complete global remote branch/tag universe and all possible extra historical assets were not exhaustively audited.

### Ref-by-ref original restoration evidence

The table gives **actual manifest-original names and tips**; every row was independently matched after local ref recreation (66/66), not assumed from a count.

| No. | Exact original ref name, reconstructed in isolated receiver | Verified tip SHA |
| ---: | --- | --- |
| 1 | refs/heads/work/downstream-reconciliation-20261028 | 97f944d51ab9e403250fe76910e2754b50425c73 |
| 2 | refs/heads/work/m00-brief2-execution-20261027 | 2f933701978b8318c21d5df5a119836ad4a83ecc |
| 3 | refs/recovered/draft/archive/l04-checkpoint/checkpoint-recovered/archive/d143-input/heads/work/v2-d131-clean-lineage-20261026 | fa709f645ac5ac21b861836db74ab23da9f8e17a |
| 4 | refs/recovered/draft/archive/l04-checkpoint/checkpoint-recovered/archive/d143-input/heads/work/v2-d135-topone-amendment-20261027 | 17d7553cf3ad92700f849f696134de67b64b0dfa |
| 5 | refs/recovered/draft/archive/l04-checkpoint/checkpoint-recovered/archive/d143-input/heads/work/v2-d136-rejected-refusal-20261026 | fa709f645ac5ac21b861836db74ab23da9f8e17a |
| 6 | refs/recovered/draft/archive/l04-checkpoint/checkpoint-recovered/archive/d143-input/remotes/origin/HEAD | fa709f645ac5ac21b861836db74ab23da9f8e17a |
| 7 | refs/recovered/draft/archive/l04-checkpoint/checkpoint-recovered/archive/d143-input/remotes/origin/work/v2-d131-clean-lineage-20261026 | fa709f645ac5ac21b861836db74ab23da9f8e17a |
| 8 | refs/recovered/draft/archive/l04-checkpoint/checkpoint-recovered/archive/d143-input/remotes/origin/work/v2-next20-d010-clean-lineage-20261026 | 77471e5a851ec04e73c6dc63988868064de930f8 |
| 9 | refs/recovered/draft/archive/l04-checkpoint/checkpoint-recovered/archive/d143-input/remotes/origin/work/v2-next20-execution-20261026 | 8e0c89b2cdf4ef504931fea894d89b2f85b2ce2e |
| 10 | refs/recovered/draft/archive/l04-checkpoint/checkpoint-recovered/archive/d143-input/tags/checkpoint/d014-controlled-accepted-20261022 | d5706537d03801cca9caa9078952496c59fbf41d |
| 11 | refs/recovered/draft/archive/l04-checkpoint/checkpoint-recovered/archive/d143-input/tags/checkpoint/g4-research-20261021 | f0190af646378441b5eabfc3616c26b3fc46c252 |
| 12 | refs/recovered/draft/archive/l04-checkpoint/checkpoint-recovered/heads/work/m00-brief2-execution-20261027 | 5219004223e33291f1b831382e8427742e00427f |
| 13 | refs/recovered/draft/archive/l04-checkpoint/checkpoint-recovered/heads/work/m00-brief2-plan-20261027 | bc02a472eaa3a07c7f112dee48e5b1f6fa1764dc |
| 14 | refs/recovered/draft/archive/l04-checkpoint/checkpoint-recovered/heads/work/v2-d135-topone-amendment-20261027 | 17d7553cf3ad92700f849f696134de67b64b0dfa |
| 15 | refs/recovered/draft/archive/l04-checkpoint/checkpoint-recovered/remotes/origin/HEAD | 17d7553cf3ad92700f849f696134de67b64b0dfa |
| 16 | refs/recovered/draft/archive/l04-checkpoint/checkpoint-recovered/remotes/origin/work/v2-d131-clean-lineage-20261026 | fa709f645ac5ac21b861836db74ab23da9f8e17a |
| 17 | refs/recovered/draft/archive/l04-checkpoint/checkpoint-recovered/remotes/origin/work/v2-d135-topone-amendment-20261027 | 17d7553cf3ad92700f849f696134de67b64b0dfa |
| 18 | refs/recovered/draft/archive/l04-checkpoint/checkpoint-recovered/remotes/origin/work/v2-d136-rejected-refusal-20261026 | fa709f645ac5ac21b861836db74ab23da9f8e17a |
| 19 | refs/recovered/draft/archive/l04-checkpoint/checkpoint-recovered/tags/checkpoint/d014-controlled-accepted-20261022 | d5706537d03801cca9caa9078952496c59fbf41d |
| 20 | refs/recovered/draft/archive/l04-checkpoint/checkpoint-recovered/tags/checkpoint/g4-research-20261021 | f0190af646378441b5eabfc3616c26b3fc46c252 |
| 21 | refs/recovered/draft/archive/l04-checkpoint/heads/work/m00-brief2-execution-20261027 | b05577a3a87b3bc23279075ef052125b9cab8ab1 |
| 22 | refs/recovered/draft/archive/l04-checkpoint/remotes/origin/HEAD | 5219004223e33291f1b831382e8427742e00427f |
| 23 | refs/recovered/draft/archive/l04-checkpoint/remotes/origin/work/m00-brief2-execution-20261027 | 5219004223e33291f1b831382e8427742e00427f |
| 24 | refs/recovered/draft/archive/l04-checkpoint/remotes/origin/work/m00-brief2-plan-20261027 | bc02a472eaa3a07c7f112dee48e5b1f6fa1764dc |
| 25 | refs/recovered/draft/archive/l04-checkpoint/remotes/origin/work/v2-d135-topone-amendment-20261027 | 17d7553cf3ad92700f849f696134de67b64b0dfa |
| 26 | refs/recovered/draft/archive/l04-checkpoint/tags/checkpoint/d014-controlled-accepted-20261022 | d5706537d03801cca9caa9078952496c59fbf41d |
| 27 | refs/recovered/draft/archive/l04-checkpoint/tags/checkpoint/g4-research-20261021 | f0190af646378441b5eabfc3616c26b3fc46c252 |
| 28 | refs/recovered/draft/heads/work/m00-brief2-execution-20261027 | 0c86b187a23e750d39ce04f772f7d52c1bd578b0 |
| 29 | refs/recovered/draft/remotes/origin/HEAD | b05577a3a87b3bc23279075ef052125b9cab8ab1 |
| 30 | refs/recovered/draft/remotes/origin/work/m00-brief2-execution-20261027 | b05577a3a87b3bc23279075ef052125b9cab8ab1 |
| 31 | refs/recovered/draft/tags/checkpoint/d014-controlled-accepted-20261022 | d5706537d03801cca9caa9078952496c59fbf41d |
| 32 | refs/recovered/draft/tags/checkpoint/g4-research-20261021 | f0190af646378441b5eabfc3616c26b3fc46c252 |
| 33 | refs/recovered/heads/work/m00-brief2-execution-20261027 | d14cb0102bfdf405bc157c7e4fa3e0d1714fb41a |
| 34 | refs/recovered/recovered/checkpoint-recovered/archive/d143-input/heads/work/v2-d131-clean-lineage-20261026 | fa709f645ac5ac21b861836db74ab23da9f8e17a |
| 35 | refs/recovered/recovered/checkpoint-recovered/archive/d143-input/heads/work/v2-d135-topone-amendment-20261027 | 17d7553cf3ad92700f849f696134de67b64b0dfa |
| 36 | refs/recovered/recovered/checkpoint-recovered/archive/d143-input/heads/work/v2-d136-rejected-refusal-20261026 | fa709f645ac5ac21b861836db74ab23da9f8e17a |
| 37 | refs/recovered/recovered/checkpoint-recovered/archive/d143-input/remotes/origin/HEAD | fa709f645ac5ac21b861836db74ab23da9f8e17a |
| 38 | refs/recovered/recovered/checkpoint-recovered/archive/d143-input/remotes/origin/work/v2-d131-clean-lineage-20261026 | fa709f645ac5ac21b861836db74ab23da9f8e17a |
| 39 | refs/recovered/recovered/checkpoint-recovered/archive/d143-input/remotes/origin/work/v2-next20-d010-clean-lineage-20261026 | 77471e5a851ec04e73c6dc63988868064de930f8 |
| 40 | refs/recovered/recovered/checkpoint-recovered/archive/d143-input/remotes/origin/work/v2-next20-execution-20261026 | 8e0c89b2cdf4ef504931fea894d89b2f85b2ce2e |
| 41 | refs/recovered/recovered/checkpoint-recovered/archive/d143-input/tags/checkpoint/d014-controlled-accepted-20261022 | d5706537d03801cca9caa9078952496c59fbf41d |
| 42 | refs/recovered/recovered/checkpoint-recovered/archive/d143-input/tags/checkpoint/g4-research-20261021 | f0190af646378441b5eabfc3616c26b3fc46c252 |
| 43 | refs/recovered/recovered/checkpoint-recovered/heads/work/m00-brief2-execution-20261027 | 5219004223e33291f1b831382e8427742e00427f |
| 44 | refs/recovered/recovered/checkpoint-recovered/heads/work/m00-brief2-plan-20261027 | bc02a472eaa3a07c7f112dee48e5b1f6fa1764dc |
| 45 | refs/recovered/recovered/checkpoint-recovered/heads/work/v2-d135-topone-amendment-20261027 | 17d7553cf3ad92700f849f696134de67b64b0dfa |
| 46 | refs/recovered/recovered/checkpoint-recovered/remotes/origin/HEAD | 17d7553cf3ad92700f849f696134de67b64b0dfa |
| 47 | refs/recovered/recovered/checkpoint-recovered/remotes/origin/work/v2-d131-clean-lineage-20261026 | fa709f645ac5ac21b861836db74ab23da9f8e17a |
| 48 | refs/recovered/recovered/checkpoint-recovered/remotes/origin/work/v2-d135-topone-amendment-20261027 | 17d7553cf3ad92700f849f696134de67b64b0dfa |
| 49 | refs/recovered/recovered/checkpoint-recovered/remotes/origin/work/v2-d136-rejected-refusal-20261026 | fa709f645ac5ac21b861836db74ab23da9f8e17a |
| 50 | refs/recovered/recovered/checkpoint-recovered/tags/checkpoint/d014-controlled-accepted-20261022 | d5706537d03801cca9caa9078952496c59fbf41d |
| 51 | refs/recovered/recovered/checkpoint-recovered/tags/checkpoint/g4-research-20261021 | f0190af646378441b5eabfc3616c26b3fc46c252 |
| 52 | refs/recovered/recovered/heads/work/m00-brief2-execution-20261027 | b05577a3a87b3bc23279075ef052125b9cab8ab1 |
| 53 | refs/recovered/recovered/remotes/origin/HEAD | 5219004223e33291f1b831382e8427742e00427f |
| 54 | refs/recovered/recovered/remotes/origin/work/m00-brief2-execution-20261027 | 5219004223e33291f1b831382e8427742e00427f |
| 55 | refs/recovered/recovered/remotes/origin/work/m00-brief2-plan-20261027 | bc02a472eaa3a07c7f112dee48e5b1f6fa1764dc |
| 56 | refs/recovered/recovered/remotes/origin/work/v2-d135-topone-amendment-20261027 | 17d7553cf3ad92700f849f696134de67b64b0dfa |
| 57 | refs/recovered/recovered/tags/checkpoint/d014-controlled-accepted-20261022 | d5706537d03801cca9caa9078952496c59fbf41d |
| 58 | refs/recovered/recovered/tags/checkpoint/g4-research-20261021 | f0190af646378441b5eabfc3616c26b3fc46c252 |
| 59 | refs/recovered/remotes/origin/HEAD | b05577a3a87b3bc23279075ef052125b9cab8ab1 |
| 60 | refs/recovered/remotes/origin/work/m00-brief2-execution-20261027 | b05577a3a87b3bc23279075ef052125b9cab8ab1 |
| 61 | refs/recovered/tags/checkpoint/d014-controlled-accepted-20261022 | d5706537d03801cca9caa9078952496c59fbf41d |
| 62 | refs/recovered/tags/checkpoint/g4-research-20261021 | f0190af646378441b5eabfc3616c26b3fc46c252 |
| 63 | refs/remotes/origin/HEAD | d14cb0102bfdf405bc157c7e4fa3e0d1714fb41a |
| 64 | refs/remotes/origin/work/m00-brief2-execution-20261027 | d14cb0102bfdf405bc157c7e4fa3e0d1714fb41a |
| 65 | refs/tags/checkpoint/d014-controlled-accepted-20261022 | d5706537d03801cca9caa9078952496c59fbf41d |
| 66 | refs/tags/checkpoint/g4-research-20261021 | f0190af646378441b5eabfc3616c26b3fc46c252 |

## 3. Exact scoped byte-asset inventory

All "REQUIRED_PRESENT" observations are for **this accessed preflight machine/receiver**, not automatically for a future different strict Tester computer. Historical asset status depends on the exact current proof route, not generic restoration folklore.

| Asset and requirement | Status | Direct observation / qualification |
| --- | --- | --- |
| Accepted controlled R112 **successful original** 15-member input, handoff/m02_completion_28_execution/L01b/CONTROLLED_BATCH_INPUTS.json | REQUIRED_PRESENT | 29,537 bytes; SHA-256 1f4c46c5c247c78e3e18bb2de02c172f775379f664bad8e056ef6867a39d03dc, equal to ledger/test/owner source pin. This is the sole original positive cohort, not replaced by malformed test fixtures. |
| R112 synthetic owner-adopted source contract, handoff/m02_completion_28_execution/L01b/R112_SOURCE_CONTRACT_PROPOSED.json | REQUIRED_PRESENT | 9,444 bytes; SHA-256 31c811e77468f44c2e412893326bc6d5f9ea037cdbf28712ce8e213652fdfc63, equal to pinned test/ledger source policy. An immutable file and owner adoption do **not** themselves prove product source-readiness. |
| **27** individually named negative-only external fixtures | REQUIRED_PRESENT | **27/27** actual receiver paths exist and their independently recomputed SHA-256 matches the case-ledger fixture_sha256: 12 D091 plus 15 L01b. Other 6 D091 nodes intentionally have fixture_path=null; do not invent files for these. No mismatches. |
| Two authored physical test modules | REQUIRED_PRESENT | AST read only, with 18+15 exact top-level named functions matching 33 ledger node names; SHA-256 d1eab7802786344ecf9ab4d4e2f46b802aba6d2fea0c72d14ad149492504b86f and 1f648998ca4c64829a3655057598e5ae5687b6568bb7e9eebf7ca2f17caa56f5, respectively. No pytest collection. |
| Current D091 claim descriptor, generation 0001, current pointer | REQUIRED_PRESENT | Exact SHA-256: descriptor bcb6a09cabe9ab4fe34dbbcb4d598c79a646ddf581e53187dda373a08181fea5; generation 429df0e6b732ed019f9bc62d67f36bc295b556f89f7da670e8d76fcce4581097; pointer 31cba6801940c2abfe0b9bcbb11bf9101cfe8e8bada1525218a4cf77300218af. Pointer generation hash and both generation family-file hashes matched actual bytes. |
| Python/lock/vendor wheel manifest | REQUIRED_PRESENT | .python-version exact 3.13.5 SHA-256 e72b03ed5b70312f2782f2b05055b24670e126d50e24c4f2c559bf288f810; pyproject.toml c62bb0b0cbc96707de3444037a2e628c95cac75ebf8b44ebb0a5ebc9e5296225; uv.lock 65800a98bc9f14fd7df23aac7206fe90d9d3c73c9b221bfbe7e90a4092c3290d; 21 vendor .whl physical files discovered and SHA-256 read. Metadata version match is not proof of full reproducible package installation from lock. |
| Actual selected CPython 3.13.5 + SQLite 3.54.1 runtime | REQUIRED_PRESENT | Existing immutable/read-only probed binary and native lib paths/hashes below. Present in this WSL environment, **non-Git**; distinct future Tester must verify its own loaded binary. |
| Historical L00 handover tar NVDA_M02_COMPLETION28_L00_HANDOVER.tar.gz (expected 96483d5a…) | NOT_MATERIAL to exact scoped current pinned-remote D091 candidate | Historical local/bundle handover route in OUTSTANDING_ASSETS_CURRENT.json reports missing original bytes; current installed PINNED_REMOTE_CHECKPOINT uses independently restored exact Git history. Historical provenance gap remains distinct and is not repaired by this classification. |
| Historical L00 additive bundle NVDA_M02_COMPLETION28_L00_ADDITIVE_FROM_97f944d51ab9.bundle (expected 589524d6…; listed twice in old inventory) | NOT_MATERIAL to this exact scoped candidate | Historical byte mismatch, 2 rows = 1 distinct asset; not used for current GitHub receiver. If separately commissioning the old bundle route, re-qualify actual bytes; do not claim match. |
| Historical L00 RESTORE.md (expected 61602cd0…) | NOT_MATERIAL to exact D091 candidate | Old inventory describes byte mismatch; not a current D091 fixture, contract, locked wheel or required pinned-remote Git transfer object. Historical mismatch remains unrepaired. |
| Historical NVDA_M02_RECOVERY_BASE_FULL_HISTORY.bundle (expected 96746582…) | NOT_MATERIAL to exact D091 pinned remote candidate | Historical missing bytes, not substituted or recreated; original exact 66 Git ref names/tips and fetched object closure independently restored for current scoped transport. |
| Historical CPython 3.12.14 + SQLite older toolchain | NOT_MATERIAL to selected CPython 3.13.5 D091 candidate | Historical original binary remains UNKNOWN in historical inventory and is not silently equated with the selected current runtime. This does not pass any other old 3.12-specific proof. |

The four legacy assets above correspond to **five** historical BLOCKED rows (one duplicate old additive bundle), plus one distinct historical 3.12 toolchain UNKNOWN; neither indicates five independent presently required D091 byte assets. The current candidate test files refer to the Git-tracked controlled original source/contract/27 fixture files, not those old archive names. "NOT_MATERIAL" is explicitly restricted to the installed current pinned-GitHub D091 route; this assessment does not certify their historical restoration.

## 4. Direct CPython, linked SQLite, wheel/runner preflight (non-product)

The **current scoped candidate runtime choice**, inspected by executing *only* Python standard-library metadata methods, is:

- Selected process invoked as /home/jds/nvda_d091_worker_proof_runner_venv_20261119/bin/python. It resolves to /home/jds/nvda_python3135_sqlite3541_20261117/python/bin/python3.13; **CPython 3.13.5 (GCC 15.2.0)**; executable SHA-256 **d114ec20c65fb65c77608f7b8b7110d0ff95e3b3c814f65580dad17fb56e012c**.
- Actual extension module: /home/jds/nvda_python3135_sqlite3541_20261117/python/lib/python3.13/lib-dynload/_sqlite3.cpython-313-x86_64-linux-gnu.so; SHA-256 **52d1d07388e3ccadf59d5071088f69c52d43071bb15092291798392407d28ab7**.
- Direct sqlite3.sqlite_version: **3.54.1**. Direct SQLite sqlite_source_id(): **2026-10-16 14:45:20 555e07ef33f69a0957d24d8e555b702464a131d6f1607f4c3c1e4551e8e6ca76**. PRAGMA compile_options: **46** rows, including ENABLE_COLUMN_METADATA, ENABLE_DBSTAT_VTAB, ENABLE_FTS3/4/5, ENABLE_MATH_FUNCTIONS, ENABLE_PERCENTILE, ENABLE_RTREE, THREADSAFE=1, MUTEX_PTHREADS and TEMP_STORE=1; no assumed equivalence with differently compiled historical 3.54.1.
- Actual /proc/self/maps **within that Python process** identifies loaded /home/jds/nvda_python3135_sqlite3541_20261117/sqlite/lib/libsqlite3.so.0, SHA-256 **44a469c2ed17ee19dca5f0c949f97b98b7ad0f1260bdb41fc153a4530324fb2f**. Direct readelf -d on that exact extension returns NEEDED libsqlite3.so.0 and **RUNPATH** /home/jds/nvda_python3135_sqlite3541_20261117/deps/usr/lib/x86_64-linux-gnu:/home/jds/nvda_python3135_sqlite3541_20261117/sqlite/lib. In the selected process LD_LIBRARY_PATH was **unset**. Thus its selected-library linkage is explicitly observed and enabled by RUNPATH, **not** by an alleged required LD_LIBRARY_PATH override for this interpreter.
- Installed distribution metadata in this selected venv: pytest **9.0.3**, Ruff **0.15.11**, mypy **1.20.1**, PyYAML **6.0.3**, psycopg **3.3.4**, hatchling **1.29.0**, iniconfig **2.3.1**, packaging **26.3**, pluggy **1.7.0**. 21 vendored wheels SHA-read, including CPython3.13 PyYAML, mypy and pure-platform-compatible pytest. No package install occurred.
- **Control experiment / materially different existing interpreter:** /home/jds/nvda_uv3135_20261112/.venv/bin/python resolves to /home/jds/nvda_uv3135_20261112/.uvpython/cpython-3.13.5-linux-x86_64-gnu/bin/python3.13, SHA-256 **0eba26d5f04a3673ee264ca406ef286d5025da098c1a24987a8118c23d69153c**. It is ALSO CPython 3.13.5 but sqlite3.sqlite_version **3.49.1**, source ID **2025-02-18 13:38:58 873d4e274b4988d260ba8354a9718324a1c26187a4ab4c1cc0227c03d0f10e70**, with no external libsqlite mapping (built-in _sqlite3). **The Python version string alone does not select the required SQLite runtime.**
- The older independently reported isolated build used LD_LIBRARY_PATH and a **different** libsqlite SHA-256 c53706980906943301153b630aeddba1b4aab6fe5eeda5752d8293952707db4e (RUNTIME_QUALIFICATION.md). Its non-product nine assertions and package state do not establish current D091 product PASS or byte equivalence with the measured RUNPATH library.

**Future exact runner selection condition:** explicitly execute the **same selected /home/jds/nvda_d091_worker_proof_runner_venv_20261119/bin/python** (or a separately qualified byte-pinned alternative) and re-check its resolved executable, native extension, loaded library SHA, source ID/options, dependency identity and feature/compatibility acceptance **in the separately designated Tester's actual receiver** before any released product node. Merely executing generic python, uv run or default pytest could choose the incompatible 3.49.1 process. The inspected current gate uses sys.executable; it does **not itself pin the executable or the linked library**. General 3.53.1-to-3.54.1 compatibility and the future product Tester environment are **not proven** by these non-product probes.

The first metadata script invocation on the control Python failed during script introspection because its built-in _sqlite3 lacks __file__; script was corrected for built-in/extension distinction and successfully rerun. This was a **metadata harness correction, not a product repair or product test**. Both successful final metadata inventories are preserved in this report by exact values and reproduction paths.

Non-product command line examples actually used:

    wsl.exe -d Ubuntu -e /home/jds/nvda_d091_worker_proof_runner_venv_20261119/bin/python /mnt/c/Users/james/AppData/Local/Temp/nvda_d091_runtime_preflight_20261120.py
    wsl.exe -d Ubuntu -e /home/jds/nvda_uv3135_20261112/.venv/bin/python /mnt/c/Users/james/AppData/Local/Temp/nvda_d091_runtime_preflight_20261120.py
    wsl.exe -d Ubuntu -e readelf -d /home/jds/nvda_python3135_sqlite3541_20261117/python/lib/python3.13/lib-dynload/_sqlite3.cpython-313-x86_64-linux-gnu.so

Helper scripts are outside the Git checkout in C:\Users\james\AppData\Local\Temp\; no governed source/test/ledger/report bytes were changed by receiver checks. All observations here are metadata and static syntax checks; **no NVIDIA product import or product computation** was undertaken.

## 5. Static product-proof loader, configured runner and current held nodes

**Exact metadata at candidate (source/object identity verified):**
- config/product_proof/m02_d091/claim.json: blob bdc4fef729a343684822e3a66cbb51a1d12dc517; raw SHA-256 bcb6a09cabe9ab4fe34dbbcb4d598c79a646ddf581e53187dda373a08181fea5.
- config/product_proof/m02_d091/generations/0001.json: blob 66bf5f718fa4462fafec8a7437caf6e20bc7c96f; raw SHA-256 429df0e6b732ed019f9bc62d67f36bc295b556f89f7da670e8d76fcce4581097.
- config/product_proof/m02_d091/admission.json: blob 839a79ced66356d4e9c5a6c96754a99c12b918b2; raw SHA-256 31cba6801940c2abfe0b9bcbb11bf9101cfe8e8bada1525218a4cf77300218af. Generation number=1, previous_generation=null, implementation_target=M02, one claim neutral_market_measurement_truth_d091, two distinct physical family files and zero generation support_files. Pointer digest equals generation's observed raw bytes.

Static loader file tools/product_proof_claims.py Git blob 4006a55adeff584aea45edd191c43a2fac9b3f73; raw SHA-256 **59b9a6037142f7d553aa731f7b1926b81dadd6fcca23bf0a267121dfa94a5bae**. Read its fixed _d091_l01b_extension, _generation, governed_snapshot, _partition and claim-loading logic. It binds descriptor, accepted target/binding/contract, test families and generation/pointer hashes, and can report metadata claim **READY_FOR_PROOF** when structurally complete. That name **does not release** any case or independently qualify execution, SQLite or Tester.

Static gate tools/run_product_proof_gate.py, blob a679ad91df7b2537491e5d8b52078fdac58ae790, checks clean Git, claim state and target, and then invokes **[sys.executable, "-m", "pytest", "-p", "product_proof_outcomes", *family_paths]** with report nonce and no plugin autoload. Gate was **not executed**. The associated tools/product_proof_outcomes.py, blob db4a05f2e0570fb27ac5a1cfe72b47d30e38d611, checks outcomes, no skip/xfail, set of files and **expected names as a subset of collected names**; the installed dependency-window law requires exact **collected-node equality**, which the distinct Tester must explicitly compare in addition to any runner success. Do not falsely equate the gate's expected-subset logic to complete 33-node budget enforcement.

The two family contract commands are generic python -m pytest on their explicit test paths, **not authorised runs**. The pyproject default pytest testpaths and Makefile/.github/workflows/architecture-kernel.yml exercise architecture/bootstrap or architecture CI, not these held D091/L01b product nodes. Configured runner/source entrypoints have been statically inspected, not imported.

**Current ledger exact observation:** handoff/m02_completion_28_execution/TEST_EVIDENCE_LEDGER.json, Git blob 387eb533c436dc598d5dd75ca74322d2af60d00b, retains:
- M02-C28-D091: **18/18** held; source_identity.contract_id=UNRESOLVED_BIND_AT_L04; profile_id=PROPOSED_NOT_ADMITTED; execution.runs=[].
- M02-C28-L01B-R112-SOURCE-SUPPORT: **15/15** separately held; source policy retains exact original source and contract hashes; execution.runs=[].
- **33/33** exact cases status OWNER_FINITE_ADMITTED_EXECUTION_HELD, execution_authorised=false, claim_generation_binding=UNBOUND_FUTURE_PRODUCT_CANDIDATE.
- Both reviewer fields SEPARATE_INDEPENDENT_TESTER_NOT_YET_DESIGNATED. Top-level ledger repository.candidate_commit=UNBOUND_FUTURE_PRODUCT_CANDIDATE and execution_mode.test_phase=DEPENDENCY_WINDOWS_THEN_L32_RECONCILIATION_PROPOSED_NOT_RELEASED. Owner finite-count permission does **not** override these explicit holds. No case identifier, case count or ledger entry was changed in this assessment.
- Pure standard-library Python ast.parse of both test modules verifies exactly 18 and 15 top-level functions and equality with the 33 declared nodes. No pytest collection or executed result is claimed.

## 6. Remaining precise independent strict Tester release predicates

The installed dependency-window source/transfer/role law is controlling. Each predicate remains separately attributable:

| Predicate for future 33-case product run | This preflight disposition | Necessary later binding |
| --- | --- | --- |
| Exact clean product candidate SHA, tree and parent; frozen source/tests/claim/generation/pointer | **VERIFIED only for b7d044a4…** in this receiver | Case release must name b7d044a4…/0704cd4… and parent 4c8124… (or separately review a materially changed new candidate), and Tester must receive that exact state. |
| Original historic Git receipt, 66 names/tips, full inventory/closure | **VERIFIED 66/66, 4,339, fsck 0** in this isolated non-Tester receiver | Separate strict Tester must independently repeat receiver qualification; this assessor cannot act as substitute. |
| Current controlled source original/contract/27 fixtures and two authored physical families | **VERIFIED_PRESENT by exact SHA-256** | Tester independently validate original SHA/fixture pins and admissible closed immutable M00 ingress/source occurrence, selected profile/clock/units/completeness and reached refusal/readback. No negative fixture is lawful additional successful input. |
| Approved source/meaning/definition/contract and L01b owning prerequisite | **PARTIAL:** owner-adopted R112 policy and documentary design history inspected, but current ledger still explicitly UNRESOLVED_BIND_AT_L04 / PROPOSED_NOT_ADMITTED | Record exact active **accepted** source/profile/contract IDs, SHA-256 and applicable independent operative source clearance, not replace them with historical proposal headings. Confirm no unresolved source ingress or domain decision. |
| Owning proof and dependency window/parent status | **HELD:** 18+15 test cases approved as finite identities only | Bind exact source-contract leaf L01b, M00 owner/checked ingress, direct catalogue dependencies and predecessor acceptance/reuse (when applicable), and correct G1 dependency timing. Do not use a G1 label to auto-release 33 tests. |
| Active one M02 claim, gen1 and pointer | **STATIC BYTES VERIFIED** | Separate Tester must load/verify with actual governed tool on exact eligible runtime after case release; no loader execution by reviewer. No fabricated third G01 family. |
| Exact case-admission status, release authority and finite 33-node bound | **BLOCKED_AUTHORITY:** 33 false case flags/unbound generation | A distinct **candidate-bound finite execution case-release decision** must explicitly reconcile and lawfully update authorised case statuses/bindings under programme governance before product execution; owner general "continue" and prior gen1 registration are not that exact release. |
| Runtime executable/package lock/SQLite loaded library and feature compatibility | **NON-PRODUCT ENVIRONMENT VERIFIED for selected WSL process** (CPython3.13.5/SQLite3.54.1 native library identity recorded) | Select exact runnable interpreter/extension/library in actual Tester environment and record binding hashes, accepted required-feature/compatibility evidence, package lock/wheel identities, backend and strict run command. Existing different 3.49.1 interpreter demonstrates need for explicit selection. |
| Actual configured runner and exact physical-node collection | **STATIC ENTRYPOINT INSPECTED; NOT RUN** | Strict Tester must use **only** released, exactly 18+15 source-named cases and independently require full **collected node ID equality**, no extras, skips, hidden parametrisation or claimed semantic pass from exit code alone. Preserve raw nonce/report/exit status and failures. |
| Separate sole independent strict product Tester designation | **BLOCKED_AUTHORITY:** not designated in current ledger | Explicit owner/programme record appointing a truly separate Tester and its independent receiver, scope, schedule and authority. Documentary reviewer cannot self-appoint. |
| Actual product evidence and durable SQLite/readback semantics | **NOT_ATTEMPTED** | Tester, after all releases, executes authorised actual product cases and independently evaluates exact public ingress, return/refusal stage, persisted typed readback and invalidation/re-run logic. No product PASS is declared now. |

**First unmet product-execution invariant:** explicit held finite-case execution release and absent independent designated Tester (with current ledger source/profile binding still unresolved). Therefore **downstream product execution stops**. This is not BLOCKED_RECEIVER on this preflight machine: its exact fresh Git closure is directly established. It is not a blanket BLOCKED_ENVIRONMENT: the chosen 3.13.5/3.54.1 interpreter and non-Git lib are independently identified and available, though a future exact product-runner qualification remains necessary.

**Decisive answer to the commission:** sufficient current **non-product receiver, byte-asset and concrete interpreter/linkage evidence** exists to prepare the **next bounded case-release decision**. The prior installation, authoring adequacy and metadata reviews cannot themselves activate 33 product tests. Separate future strict Tester, case-release record and source/environment acceptance remain **not obtained**; this document is **not** a new product admission or an execution instruction.

## 7. Publication scope and independent-review boundary

Prescribed branch: review/d091-l01b-proof-entry-receiver-20261119-gpt6, created **directly** from b7d044a4f84b7f70703322c250cbd82cee6f4589. **Only permitted new file:** handoff/m02_completion_28_execution/L04/D091_PROOF_ENTRY_INDEPENDENT_REVIEW_20261119/RECEIVER_AND_RUNNER_PREFLIGHT_REPORT.md. The review commit, tree, sole parent, exactly one-report diff, full GitHub file readback and remote branch HEAD require separate **post-publication** verification; this report does not pre-claim that future check.

**Next lawful Worker action:** reconcile this actual non-product evidence and prepare the exact candidate-bound finite case-execution release and separate independent strict Tester appointment under the installed dependency-window law, with no repeat approval request for the already installed M02→G01 implementation or exact metadata registration. If a required source, parent, runtime, asset or role binding cannot be established, preserve the held cases, identify its exact missing prerequisite and continue only independent non-product tasks.

**Direct non-product audit aids (outside Git receiver):** C:\Users\james\AppData\Local\Temp\nvda_d091_receiver_verify_20261120.py, nvda_d091_static_assets_20261120.py, nvda_d091_runtime_preflight_20261120.py. Their observed output is captured above in finite verifiable counts, SHAs, paths, exit codes and procedures; no hidden product run or manual data override is used. None of these machine-local scripts is a repository product runner, or part of an alleged future independent Tester's environment.
