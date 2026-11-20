# NVIDIA V2 D091/L01b — Independent strict product Tester Phase A intake report

**Date:** 20 November 2026 (Australia/Melbourne)  
**Disposition:** **PHASE_A_INTAKE_VERIFIED; READY_FOR_SEPARATE_CASE_RELEASE_REVIEW; PRODUCT_EXECUTION_HELD**.  
**This is a non-product Tester receiver/runner intake, not product proof, semantic TESTED_ACCEPTED, an active case release, a closed G1 gate, or a request to merge.** All 33 physical cases remain held. Product import, pytest collection and product runs: **zero**.

## 1. Commission, role, identity and fixed source boundary

Repository: `JayDEmily/nvda_29102026`, Worker PR #27. I am the distinct *strict product Tester* performing only its first, separately commissioned Phase A intake. The complete commissioning document was read at immutable Worker commit `5f39633cbfc98b6bb1031d1387e4ff9c04540a0d`, path `handoff/m02_completion_28_execution/L04/D091_STRICT_TESTER_INTAKE_20261120/INDEPENDENT_STRICT_TESTER_INTAKE_COMMISSION.md` (Git blob `c9266ddd26ab413a0fc0abe5d004d96f1dd2ce20`).

The **Worker's separately committed fixed identity record**, independently fetched from GitHub at commit `44f4713e9c7cbf89d3b36c475864a79ff0f175ed`, file `handoff/m02_completion_28_execution/L04/D091_STRICT_TESTER_INTAKE_20261120/STRICT_TESTER_IDENTITY_AND_EXECUTION_HOLD.md` (Git blob `b60c7b573857971403f235ec0b2cfe762ab377a5`), identifies this new commissioned conversation as:

`https://chatgpt.com/g/g-p-6ad546f307e88191b64b94d0851da624-nvda-6-1/c/6aff8bbe-5c5c-83ec-99eb-6988bcf8aba7`

That record separately reports correct original prompt delivery and quotes the opening assistant acknowledgement in this conversation. This is a **Worker-attributed observed ChatGPT conversation URL**, not a message permalink or a claim that this Tester independently queried the browser UI. It identifies a different conversation from the continuing Worker and prior non-product preflight reviewer. The owner standing grant (Worker commit `9f6c4fd0ac87ae56904705d405fd11b7422e6810`, file `handoff/m02_completion_28_execution/L04/D091_STANDING_CONDITIONAL_AUTHORITY_20261120/OWNER_STANDING_CONDITIONAL_EXECUTION_GRANT.md`, clauses 2–3) conditionally designates the first distinct commissioned and recorded thread. **Identity/Phase A role: verified against the later Worker record. Case execution designation: not yet independently released.**

The **only pinned product candidate** is commit `b7d044a4f84b7f70703322c250cbd82cee6f4589`, tree `0704cd4ebe09801e7116ed517cceda756f5e1dbf`, **direct parent** `4c8124dae1d88ce293e916f18734ab18b02ad240`. Subsequent Worker authority/identity commits do not update that product candidate. The independent intake branch was prescribed as `review/d091-l01b-strict-tester-intake-20261120-gpt6`, directly from this candidate; only this report file may be added.

Authority actually inspected: full frozen `GUARDRAILS.md` at Worker and candidate (identical blob `54a4407609941f63f6b902076688ff102a3d5ba2`); root `AGENTS.md` (blob `b5b8f73bfef62cf34643aef419e6931599ad08b1`); applicable `tests/AGENTS.override.md` (blob `66666cc012889e585ef4da80049d5ee2a0244c53`); root `EXEC_PLAN.md` (429 lines in successive sections; blob `76e8dd7af85cee33e306c351206e69fc049129fb`); `handoff/astra_adr_continuation_20261115/INSTALLATION_RECEIPT.md` (blob `e57e705184ec8d5d4f5804c3c1473cfc8b975483`); and `handoff/planning/t01_owner_lint_integration_20261115/DEPENDENCY_WINDOWS.md` (blob `8edc15a1af78482060091edb4db4e287a3d63a98`). The installed receipt supersedes inherited proposal-stage labels **on this Worker branch**, without itself releasing product cases. The earlier non-product review at `31b109d1c3818f326c48abbf2f51f6e218cb2c36` was inspected for scope and contrast, **not** substituted for any of the fresh checks below.

## 2. Independently created isolated Ubuntu Git receiver

Device: online `DESKTOP-I188O30`, Windows Remote Desktop Commander, **WSL Ubuntu** as `jds`, `git version 2.53.0`. My newly created receiver is:

`/home/jds/nvda_d091_strict_tester_intake_20261120_gpt6`

The path did not exist before my creation. It is distinct from Worker and earlier non-product preflight receivers. I wrote my own host-side non-product receiver script at `C:\Users\james\AppData\Local\Temp\nvda_strict_tester_phaseA_receiver_20261120.sh`; ran `wsl.exe -d Ubuntu -e bash /mnt/c/Users/james/AppData/Local/Temp/nvda_strict_tester_phaseA_receiver_20261120.sh`; **exit 0**. Complete command/output record: `/home/jds/nvda_d091_strict_tester_phaseA_receiver_log_20261120.txt` (outside repository). Key actual commands:

```sh
git init -q /home/jds/nvda_d091_strict_tester_intake_20261120_gpt6
git -C /home/jds/nvda_d091_strict_tester_intake_20261120_gpt6 remote add origin https://github.com/JayDEmily/nvda_29102026.git
# git fetch --no-tags origin: exact Worker branch + five recovery branch refspecs
git -C /home/jds/nvda_d091_strict_tester_intake_20261120_gpt6 checkout -q --detach b7d044a4f84b7f70703322c250cbd82cee6f4589
# restore each of 66 exact manifest refs using git cat-file -t, git update-ref, then git rev-parse --verify
# fetch six separately pinned documentary evidence commit objects under refs/receiver/evidence/*
git -C /home/jds/nvda_d091_strict_tester_intake_20261120_gpt6 fsck --full
git -C /home/jds/nvda_d091_strict_tester_intake_20261120_gpt6 status --porcelain=v1
```

| Receiver predicate | Direct, separate Tester observation |
| --- | --- |
| HEAD | `b7d044a4f84b7f70703322c250cbd82cee6f4589` — exact |
| Tree | `0704cd4ebe09801e7116ed517cceda756f5e1dbf` — exact |
| Parent | `4c8124dae1d88ce293e916f18734ab18b02ad240` — exact |
| Tracked `git ls-files` count | **4,339** |
| Tracked `git ls-tree -r --full-tree HEAD` count | **4,339** |
| SHA-256 of raw `git ls-tree` output (with terminating newlines) | `9aa670a5ce63d059b5b9037d9e366e4b71c2a0f550251a709e22ad5e755a9e22` |
| Original manifest blob | `162b242eee672bbaa1b4a1e30d63bb2d71657fe3` |
| Original manifest raw SHA-256 | `7cb2abfd6e5a4828c6a1e61a1e960d5649c4ab59449423d9189256ee425d3606` |
| Exact manifest original refs | **66/66 distinct names and SHA tips**, each local Git commit object verified and restored; 0 wrong or missing |
| Extra pinned documentary evidence commits | **6** fetched under separate `refs/receiver/evidence/*`, not counted as original 66 |
| `git fsck --full` | **exit 0**, empty stdout/stderr after ref restoration and evidence fetch |
| `git status --porcelain=v1` | **empty**, clean pinned detached receiver at qualification |

Five fetched recovery branch tips independently verified: `recovery/legacy-d010-20261111` = `77471e5a851ec04e73c6dc63988868064de930f8`; `recovery/legacy-d131-20261111` = `fa709f645ac5ac21b861836db74ab23da9f8e17a`; `recovery/legacy-m00-brief2-20261111` = `0c86b187a23e750d39ce04f772f7d52c1bd578b0`; `recovery/legacy-next20-20261111` = `8e0c89b2cdf4ef504931fea894d89b2f85b2ce2e`; `recovery/r2-g0-f02-20261111` = `16b7cc67f5d24336d3768e2da006819474a8c792`.

The six additional fetched fixed evidence commits: `38d4b44c9bceca883ed0a676e7b9b36d684ad54e`, `76fe3adba5f6a0f3e003997e03f87a2e56614b71`, `b15a9ee49e7d3d36e7d42a18ee956c9447f853e8`, `c7ebfbf10810d483d926cd00c1a4983a6c07e461`, `e64cc5b69279a088cc11c9c74d146a0fecb30517`, `5f47fdce8064d7cfcb452621323cbcca57af167d`. Full GitHub global ref universe was **not** exhaustively restored; assertion is deliberately limited to the declared five recovery refs, 66 original names, and six evidence refs. Historical L00 cumulative archive/bundle bytes were **not** reconstructed or requalified: the scoped installed `PINNED_REMOTE_CHECKPOINT` path uses independently received Git objects. Historic asset deficits remain historic and are not declared repaired or universally irrelevant.

## 3. Independent original sources, physical tests, negative assets and active M02 generation — static bytes only

My independent standard-library Python audit was created at `C:\Users\james\AppData\Local\Temp\nvda_strict_tester_phaseA_static_20261120.py` and invoked with:

```sh
wsl.exe -d Ubuntu -e python3 /mnt/c/Users/james/AppData/Local/Temp/nvda_strict_tester_phaseA_static_20261120.py
```

**Exit 0.** It used `pathlib`, `hashlib`, `json`, Git `hash-object`, and `ast.parse` against files in my isolated receiver; it imported no product module and did not invoke pytest, collect tests or run product code. It individually compared **every** admitted case against the frozen owner list and actual ledger, **every** non-null negative fixture's physical SHA-256, and the two test modules' top-level physical AST names to the declared node suffix sets. No fixture was treated as a positive R112 source.

| Asset / integrity requirement | Independently observed result |
| --- | --- |
| Active `handoff/m02_completion_28_execution/TEST_EVIDENCE_LEDGER.json` | Git blob `387eb533c436dc598d5dd75ca74322d2af60d00b`, raw SHA-256 `b00aceebe5bb5be06fec890d8497272f375b5cddea456eeae605085e2ecf3956` |
| Owner exact 33-case admission file | Git blob `abb09419a425ee5eb2b19ed911fb32ecba41fd81`, raw SHA-256 `132288211affdb52d3f5a6970bc484debdb204175f531087b8b9498bbb7175c7` |
| Case-list exact equality | **18 D091/L04 + 15 separate L01b/R112**, 33 distinct case IDs and node strings, two non-fungible 18/15 ceilings; all per-case expected stages, source fixture paths/hash and predecessor witness lists equal owner admission |
| Physical authored source `tests/product/m02_completion_28/d091/test_signal.py` | **18** exact top-level AST test functions, zero decorated test functions; SHA-256 `d1eab7802786344ecf9ab4d4e2f46b802aba6d2fea0c72d14ad149492504b86f` |
| Physical authored source `tests/product/m02_completion_28/l01b_r112/test_source.py` | **15** exact top-level AST test functions, zero decorated test functions; SHA-256 `1f648998ca4c64829a3655057598e5ae5687b6568bb7e9eebf7ca2f17caa56f5` |
| Negative-only external JSON fixtures | **27/27** distinct physical files and individually recalculated SHA-256 equal ledger: 12 D091, 15 L01b; remaining 6 D091 cases explicitly have null fixture path/hash |
| R112 sole original successful batch | `handoff/m02_completion_28_execution/L01b/CONTROLLED_BATCH_INPUTS.json`, 29,537 bytes, SHA-256 `1f4c46c5c247c78e3e18bb2de02c172f775379f664bad8e056ef6867a39d03dc`, Git blob `f882cd80ad9500a4fcf9aa05de9cadbc248769d6` |
| Exact owner-adopted synthetic R112 source contract bytes | `handoff/m02_completion_28_execution/L01b/R112_SOURCE_CONTRACT_PROPOSED.json`, 9,444 bytes, SHA-256 `31c811e77468f44c2e412893326bc6d5f9ea037cdbf28712ce8e213652fdfc63`, Git blob `bad8b3b2e536f2c0326cf1de995dc38793fd9936` |
| Active claim descriptor | `config/product_proof/m02_d091/claim.json`; SHA-256 `bcb6a09cabe9ab4fe34dbbcb4d598c79a646ddf581e53187dda373a08181fea5` |
| Immutable generation 0001 | `config/product_proof/m02_d091/generations/0001.json`; SHA-256 `429df0e6b732ed019f9bc62d67f36bc295b556f89f7da670e8d76fcce4581097` |
| Current pointer | `config/product_proof/m02_d091/admission.json`; SHA-256 `31cba6801940c2abfe0b9bcbb11bf9101cfe8e8bada1525218a4cf77300218af` |
| Generation physical binding | Claim `neutral_market_measurement_truth_d091`, target **M02**, gen 1, previous generation null; pointer-to-generation and both family hashes match physical bytes; no support files; brief/binding/contract SHA-256 independently match `d00849a9...`, `328827d6...`, `f5550570...` respectively |
| Dependency configuration | `.python-version` contains 3.13.5 (SHA-256 `e72b03ed5b70312f2782f2b05055b24670e126d50e24c4f2c559bf288f810`); `pyproject.toml` SHA-256 `c62bb0b0cbc96707de3444037a2e628c95cac75ebf8b44ebb0a5ebc9e5296225`; `uv.lock` SHA-256 `65800a98bc9f14fd7df23aac7206fe90d9d3c73c9b221bfbe7e90a4092c3290d`; **21/21** physical vendored wheels found and individually SHA-256 inspected |

**Existing source-policy distinction:** `handoff/m02_completion_28_execution/L01b/R112_OPERATIVE_DECISION_PREP_20261115/OWNER_SOURCE_ADOPTION_20261115.md` approves the exact R112 synthetic *policy* for L01b→L04 but explicitly withholds automatic source/runtime/strict case admission. The later `.../R112_NEGATIVE_FAULT_POLICY_DECISION_20261116/OWNER_TEST_ONLY_POLICY_ADOPTION_20261116.md` admits test-only malformed/fault stimuli, *not* a replacement positive cohort. The immutable original source contract retains its proposal-time status string; that string alone is not proof current programme policy is absent. Critically, the **active ledger** still has D091 `source_identity.contract_id=UNRESOLVED_BIND_AT_L04` and `profile_id=PROPOSED_NOT_ADMITTED`, while the source-support allocation retains unresolved source/generation bindings. Actual binding and operative release remain distinct from byte integrity.

## 4. My own executable, loaded native SQLite library and dependency metadata probes

I independently created a **non-product** standard-library metadata probe, `C:\Users\james\AppData\Local\Temp\nvda_strict_tester_phaseA_runtime_20261120.py`, and actually invoked:

```powershell
wsl.exe -d Ubuntu -e /home/jds/nvda_d091_worker_proof_runner_venv_20261119/bin/python /mnt/c/Users/james/AppData/Local/Temp/nvda_strict_tester_phaseA_runtime_20261120.py
```

**Exit 0**. This uses an already installed physical interpreter/venv, **but these are this Tester's own process-level observations**, not the prior reviewer's inherited claims. It did **not** create a new package installation and did **not** import the NVDA product or run pytest. Selected process and actual loader identities:

| Runtime predicate | Actual observed value |
| --- | --- |
| Intended future interpreter invocation | `/home/jds/nvda_d091_worker_proof_runner_venv_20261119/bin/python` (must be explicit, not generic Python or `uv run`) |
| Resolved interpreter | `/home/jds/nvda_python3135_sqlite3541_20261117/python/bin/python3.13` |
| CPython and executable SHA-256 | **3.13.5** (GCC 15.2.0); `d114ec20c65fb65c77608f7b8b7110d0ff95e3b3c814f65580dad17fb56e012c` |
| Native `_sqlite3` extension | `/home/jds/nvda_python3135_sqlite3541_20261117/python/lib/python3.13/lib-dynload/_sqlite3.cpython-313-x86_64-linux-gnu.so`, SHA-256 `52d1d07388e3ccadf59d5071088f69c52d43071bb15092291798392407d28ab7` |
| `sqlite3.sqlite_version` | **3.54.1** |
| Actual `select sqlite_source_id()` | `2026-10-16 14:45:20 555e07ef33f69a0957d24d8e555b702464a131d6f1607f4c3c1e4551e8e6ca76` |
| `PRAGMA compile_options` | **46**; including `ENABLE_COLUMN_METADATA`, `ENABLE_DBSTAT_VTAB`, `ENABLE_FTS3`, `ENABLE_FTS4`, `ENABLE_FTS5`, `ENABLE_MATH_FUNCTIONS`, `ENABLE_PERCENTILE`, `ENABLE_RTREE`, `THREADSAFE=1`, `MUTEX_PTHREADS`, `TEMP_STORE=1` |
| Actual loaded native SQLite library from process `/proc/self/maps` | `/home/jds/nvda_python3135_sqlite3541_20261117/sqlite/lib/libsqlite3.so.0`, SHA-256 `44a469c2ed17ee19dca5f0c949f97b98b7ad0f1260bdb41fc153a4530324fb2f` |
| ELF dynamic linkage | `NEEDED libsqlite3.so.0`; `RUNPATH /home/jds/nvda_python3135_sqlite3541_20261117/deps/usr/lib/x86_64-linux-gnu:/home/jds/nvda_python3135_sqlite3541_20261117/sqlite/lib` |
| `LD_LIBRARY_PATH` | **unset** for this probed process: linkage established via RUNPATH |
| Distribution metadata, no product imports | pytest **9.0.3**, Ruff **0.15.11**, mypy **1.20.1**, PyYAML **6.0.3**, psycopg **3.3.4**, hatchling **1.29.0**, iniconfig **2.3.1**, packaging **26.3**, pluggy **1.7.0** |

**Qualification limit:** This is process-specific executable/extension/loaded-library identity with identified compile features, *not* full lock-reproducible installation proof, actual SQLite 3.53.1→3.54.1 historical product compatibility, or successful product owner/codec/readback execution. No product test has been collected or executed. Any later case release must bind this **exact chosen process** or a separately byte-qualified alternative, accepted backend features/compatibility and environment to the precise released candidate/source.

## 5. Static loader/gate review — no import or execution

All three scripts were read as text and parsed with Python `ast.parse`, no NVDA module imports:

- `tools/product_proof_claims.py`: SHA-256 `59b9a6037142f7d553aa731f7b1926b81dadd6fcca23bf0a267121dfa94a5bae`, lines 350–433 (`_generation`) validate pointer chain/gen/family hashes; lines 819–902 (`_d091_l01b_extension`) bind exact M02 owning target, physical families and 18/15 admitted names. **Static only**; `load_product_proof_claim` was not invoked.
- `tools/run_product_proof_gate.py`: SHA-256 `149ebd876b08c9a7874248de5e196a3c6c6d322b0556ee6f234b72bc6e6f1334`, lines 24–81. Checks clean checkout and claim state; constructs `[sys.executable, "-m", "pytest", "-p", "product_proof_outcomes", *paths]`. **Not invoked**.
- `tools/product_proof_outcomes.py`: SHA-256 `1aafb2d33395d20e2a41ce7cc78e0c2dd2e934149f727ba888832559865a2273`, lines 56–107. Static set logic checks `expected_names <= collected_by_file` (lines 85–89), **not exact collected-node equality**. Current governing dependency windows require actual complete node-set equality. A later strict Tester Phase B must independently enforce exact equality, including no extra/hidden parametrised nodes, beyond success of this gate.

**Only intended future execution shape, not an authorised or executed command:** from a qualified clean pinned receiver, with the exact interpreter and *after* a separately committed verified individual finite-case release, `/home/jds/nvda_d091_worker_proof_runner_venv_20261119/bin/python tools/run_product_proof_gate.py --aggregate neutral_market_measurement_truth_d091 --repository <candidate-bound-receiver>`, plus independent exact collection equality and per-case raw semantic evidence. This is **not** a Phase A instruction to run it now.

## 6. Explicit release-predicate assessment

| Prerequisite | Phase A evidence/disposition |
| --- | --- |
| New, genuinely distinct sole strict Tester identity | **VERIFIED by independent GitHub readback of Worker commit `44f4713...`**, fixed chat URL and owner-standing clause 3. Worker attribution to observed browser, not separate UI session inspection by Tester |
| Exact candidate commit/tree/parent, 4,339 tracked objects, clean new receiver | **VERIFIED in this Tester's own receiver** |
| Five recovery refs, all 66 original named/tip refs, additional six reviewer objects, full Git closure | **VERIFIED by fresh individual Git checks and `git fsck --full` exit 0**; not a claim about every possible global GitHub ref |
| Original successful R112 source, owner-adopted contract and 27 negative-only fixtures | **VERIFIED EXACT BYTES**, original success distinct from negative cohorts; owner policy adoption read; operative source readiness **NOT YET BOUND** |
| Exactly 18 + 15 authored physical test names/sha and finite owner case census | **VERIFIED STATIC AST/PHYSICAL BYTES**, not actual pytest collection |
| Current active single M02 claim/gen1/pointer and two family hashes | **VERIFIED STATIC**, loader not executed, no additional G01 claim/family |
| CPython3.13.5 / native SQLite3.54.1 / wheel and dependency identities | **VERIFIED ACTUAL SELECTED PROCESS + loaded library SHA**, 21/21 vendored wheel SHA-read and installed package versions; full historical compatibility and case-specific runtime acceptance **UNPROVEN** |
| Active source/profile/owner/parent acceptance and legal public M00 ingress | **BLOCKED FOR PRODUCT EXECUTION**: D091 ledger `UNRESOLVED_BIND_AT_L04` / `PROPOSED_NOT_ADMITTED`; qualified admitted L01b source/profile/closure, live parent/reuse and full public ingress semantics not established by static evidence alone |
| Exact case-to-claim/generation/candidate/parent/runner release | **BLOCKED AUTHORITY**: active ledger `repository.candidate_commit=UNBOUND_FUTURE_PRODUCT_CANDIDATE`; every case `claim_generation_binding=UNBOUND_FUTURE_PRODUCT_CANDIDATE` and `execution_authorised=false`; both family `execution_release=false` |
| Release record independently verified and same Tester conversation notified | **NOT PRESENT IN THIS PINNED CANDIDATE/PHASE A**. A future Worker release and independently checked changed active ledger are mandatory before any case |
| Case collection, reached refusals, independent success/oracles, durable SQLite readback, product verdict | **NOT ATTEMPTED; authorised count 0 executed count 0** |

**Disposition:** My separate Phase A Git receiver and specific installed Python/SQLite non-product runtime have sufficient directly observed evidence to permit a *later, separately authorised exact case-release assessment*. **I do not know whether every remaining source/parent/compatibility predicate can be cleared without further evidence.** The first product-execution blockers are the explicit active-ledger held/unbound finite cases and unproven source/profile/parent/compatibility release binding. I am **NOT READY TO EXECUTE** any of the 33 cases. No product-test PASS is declared, and no case status or active proof authority has been amended. The designated Worker must investigate and independently verify all still-unbound predicates before issuing any exact candidate-bound finite release; then notify this **same** Tester conversation. A Phase A PASS cannot self-issue Phase B.

## 7. Publication and mutation boundary

Only report path authorised on `review/d091-l01b-strict-tester-intake-20261120-gpt6`:

`handoff/m02_completion_28_execution/L04/D091_STRICT_TESTER_INDEPENDENT_INTAKE_20261120/TESTER_RECEIVER_AND_RUNNER_INTAKE_REPORT.md`

This report is authored from independent checks and immutable sources. Its own remote commit/tree, direct sole parent, one-report diff and complete GitHub readback must be checked **after** GitHub publication, not falsely preclaimed in the file.

**Zero** product imports, **zero** pytest collections, **zero** product cases executed, **zero** product-test assertions, **zero** active ledger/claim/generation/pointer/test/guardrail/ExecPlan edits. No Worker branch change, main or PR #27 merge, broker/provider action, PostgreSQL action, or D145 reactivation.

### Appendix A — individual 66 original historical refs

The following 66 names and tips are from pinned `ORIGINAL_66_REFS.json`. Each row was independently object-typed as `commit`, restored with `git update-ref`, then full-SHA compared against `git rev-parse --verify` in this Tester's isolated receiver, **66/66 MATCH** (full raw command log retained at the external path above):

| No. | Exact original ref | Independently checked tip | Observed |
| ---: | --- | --- | --- |
| 1 | `refs/heads/work/downstream-reconciliation-20261028` | `97f944d51ab9e403250fe76910e2754b50425c73` | MATCH |
| 2 | `refs/heads/work/m00-brief2-execution-20261027` | `2f933701978b8318c21d5df5a119836ad4a83ecc` | MATCH |
| 3 | `refs/recovered/draft/archive/l04-checkpoint/checkpoint-recovered/archive/d143-input/heads/work/v2-d131-clean-lineage-20261026` | `fa709f645ac5ac21b861836db74ab23da9f8e17a` | MATCH |
| 4 | `refs/recovered/draft/archive/l04-checkpoint/checkpoint-recovered/archive/d143-input/heads/work/v2-d135-topone-amendment-20261027` | `17d7553cf3ad92700f849f696134de67b64b0dfa` | MATCH |
| 5 | `refs/recovered/draft/archive/l04-checkpoint/checkpoint-recovered/archive/d143-input/heads/work/v2-d136-rejected-refusal-20261026` | `fa709f645ac5ac21b861836db74ab23da9f8e17a` | MATCH |
| 6 | `refs/recovered/draft/archive/l04-checkpoint/checkpoint-recovered/archive/d143-input/remotes/origin/HEAD` | `fa709f645ac5ac21b861836db74ab23da9f8e17a` | MATCH |
| 7 | `refs/recovered/draft/archive/l04-checkpoint/checkpoint-recovered/archive/d143-input/remotes/origin/work/v2-d131-clean-lineage-20261026` | `fa709f645ac5ac21b861836db74ab23da9f8e17a` | MATCH |
| 8 | `refs/recovered/draft/archive/l04-checkpoint/checkpoint-recovered/archive/d143-input/remotes/origin/work/v2-next20-d010-clean-lineage-20261026` | `77471e5a851ec04e73c6dc63988868064de930f8` | MATCH |
| 9 | `refs/recovered/draft/archive/l04-checkpoint/checkpoint-recovered/archive/d143-input/remotes/origin/work/v2-next20-execution-20261026` | `8e0c89b2cdf4ef504931fea894d89b2f85b2ce2e` | MATCH |
| 10 | `refs/recovered/draft/archive/l04-checkpoint/checkpoint-recovered/archive/d143-input/tags/checkpoint/d014-controlled-accepted-20261022` | `d5706537d03801cca9caa9078952496c59fbf41d` | MATCH |
| 11 | `refs/recovered/draft/archive/l04-checkpoint/checkpoint-recovered/archive/d143-input/tags/checkpoint/g4-research-20261021` | `f0190af646378441b5eabfc3616c26b3fc46c252` | MATCH |
| 12 | `refs/recovered/draft/archive/l04-checkpoint/checkpoint-recovered/heads/work/m00-brief2-execution-20261027` | `5219004223e33291f1b831382e8427742e00427f` | MATCH |
| 13 | `refs/recovered/draft/archive/l04-checkpoint/checkpoint-recovered/heads/work/m00-brief2-plan-20261027` | `bc02a472eaa3a07c7f112dee48e5b1f6fa1764dc` | MATCH |
| 14 | `refs/recovered/draft/archive/l04-checkpoint/checkpoint-recovered/heads/work/v2-d135-topone-amendment-20261027` | `17d7553cf3ad92700f849f696134de67b64b0dfa` | MATCH |
| 15 | `refs/recovered/draft/archive/l04-checkpoint/checkpoint-recovered/remotes/origin/HEAD` | `17d7553cf3ad92700f849f696134de67b64b0dfa` | MATCH |
| 16 | `refs/recovered/draft/archive/l04-checkpoint/checkpoint-recovered/remotes/origin/work/v2-d131-clean-lineage-20261026` | `fa709f645ac5ac21b861836db74ab23da9f8e17a` | MATCH |
| 17 | `refs/recovered/draft/archive/l04-checkpoint/checkpoint-recovered/remotes/origin/work/v2-d135-topone-amendment-20261027` | `17d7553cf3ad92700f849f696134de67b64b0dfa` | MATCH |
| 18 | `refs/recovered/draft/archive/l04-checkpoint/checkpoint-recovered/remotes/origin/work/v2-d136-rejected-refusal-20261026` | `fa709f645ac5ac21b861836db74ab23da9f8e17a` | MATCH |
| 19 | `refs/recovered/draft/archive/l04-checkpoint/checkpoint-recovered/tags/checkpoint/d014-controlled-accepted-20261022` | `d5706537d03801cca9caa9078952496c59fbf41d` | MATCH |
| 20 | `refs/recovered/draft/archive/l04-checkpoint/checkpoint-recovered/tags/checkpoint/g4-research-20261021` | `f0190af646378441b5eabfc3616c26b3fc46c252` | MATCH |
| 21 | `refs/recovered/draft/archive/l04-checkpoint/heads/work/m00-brief2-execution-20261027` | `b05577a3a87b3bc23279075ef052125b9cab8ab1` | MATCH |
| 22 | `refs/recovered/draft/archive/l04-checkpoint/remotes/origin/HEAD` | `5219004223e33291f1b831382e8427742e00427f` | MATCH |
| 23 | `refs/recovered/draft/archive/l04-checkpoint/remotes/origin/work/m00-brief2-execution-20261027` | `5219004223e33291f1b831382e8427742e00427f` | MATCH |
| 24 | `refs/recovered/draft/archive/l04-checkpoint/remotes/origin/work/m00-brief2-plan-20261027` | `bc02a472eaa3a07c7f112dee48e5b1f6fa1764dc` | MATCH |
| 25 | `refs/recovered/draft/archive/l04-checkpoint/remotes/origin/work/v2-d135-topone-amendment-20261027` | `17d7553cf3ad92700f849f696134de67b64b0dfa` | MATCH |
| 26 | `refs/recovered/draft/archive/l04-checkpoint/tags/checkpoint/d014-controlled-accepted-20261022` | `d5706537d03801cca9caa9078952496c59fbf41d` | MATCH |
| 27 | `refs/recovered/draft/archive/l04-checkpoint/tags/checkpoint/g4-research-20261021` | `f0190af646378441b5eabfc3616c26b3fc46c252` | MATCH |
| 28 | `refs/recovered/draft/heads/work/m00-brief2-execution-20261027` | `0c86b187a23e750d39ce04f772f7d52c1bd578b0` | MATCH |
| 29 | `refs/recovered/draft/remotes/origin/HEAD` | `b05577a3a87b3bc23279075ef052125b9cab8ab1` | MATCH |
| 30 | `refs/recovered/draft/remotes/origin/work/m00-brief2-execution-20261027` | `b05577a3a87b3bc23279075ef052125b9cab8ab1` | MATCH |
| 31 | `refs/recovered/draft/tags/checkpoint/d014-controlled-accepted-20261022` | `d5706537d03801cca9caa9078952496c59fbf41d` | MATCH |
| 32 | `refs/recovered/draft/tags/checkpoint/g4-research-20261021` | `f0190af646378441b5eabfc3616c26b3fc46c252` | MATCH |
| 33 | `refs/recovered/heads/work/m00-brief2-execution-20261027` | `d14cb0102bfdf405bc157c7e4fa3e0d1714fb41a` | MATCH |
| 34 | `refs/recovered/recovered/checkpoint-recovered/archive/d143-input/heads/work/v2-d131-clean-lineage-20261026` | `fa709f645ac5ac21b861836db74ab23da9f8e17a` | MATCH |
| 35 | `refs/recovered/recovered/checkpoint-recovered/archive/d143-input/heads/work/v2-d135-topone-amendment-20261027` | `17d7553cf3ad92700f849f696134de67b64b0dfa` | MATCH |
| 36 | `refs/recovered/recovered/checkpoint-recovered/archive/d143-input/heads/work/v2-d136-rejected-refusal-20261026` | `fa709f645ac5ac21b861836db74ab23da9f8e17a` | MATCH |
| 37 | `refs/recovered/recovered/checkpoint-recovered/archive/d143-input/remotes/origin/HEAD` | `fa709f645ac5ac21b861836db74ab23da9f8e17a` | MATCH |
| 38 | `refs/recovered/recovered/checkpoint-recovered/archive/d143-input/remotes/origin/work/v2-d131-clean-lineage-20261026` | `fa709f645ac5ac21b861836db74ab23da9f8e17a` | MATCH |
| 39 | `refs/recovered/recovered/checkpoint-recovered/archive/d143-input/remotes/origin/work/v2-next20-d010-clean-lineage-20261026` | `77471e5a851ec04e73c6dc63988868064de930f8` | MATCH |
| 40 | `refs/recovered/recovered/checkpoint-recovered/archive/d143-input/remotes/origin/work/v2-next20-execution-20261026` | `8e0c89b2cdf4ef504931fea894d89b2f85b2ce2e` | MATCH |
| 41 | `refs/recovered/recovered/checkpoint-recovered/archive/d143-input/tags/checkpoint/d014-controlled-accepted-20261022` | `d5706537d03801cca9caa9078952496c59fbf41d` | MATCH |
| 42 | `refs/recovered/recovered/checkpoint-recovered/archive/d143-input/tags/checkpoint/g4-research-20261021` | `f0190af646378441b5eabfc3616c26b3fc46c252` | MATCH |
| 43 | `refs/recovered/recovered/checkpoint-recovered/heads/work/m00-brief2-execution-20261027` | `5219004223e33291f1b831382e8427742e00427f` | MATCH |
| 44 | `refs/recovered/recovered/checkpoint-recovered/heads/work/m00-brief2-plan-20261027` | `bc02a472eaa3a07c7f112dee48e5b1f6fa1764dc` | MATCH |
| 45 | `refs/recovered/recovered/checkpoint-recovered/heads/work/v2-d135-topone-amendment-20261027` | `17d7553cf3ad92700f849f696134de67b64b0dfa` | MATCH |
| 46 | `refs/recovered/recovered/checkpoint-recovered/remotes/origin/HEAD` | `17d7553cf3ad92700f849f696134de67b64b0dfa` | MATCH |
| 47 | `refs/recovered/recovered/checkpoint-recovered/remotes/origin/work/v2-d131-clean-lineage-20261026` | `fa709f645ac5ac21b861836db74ab23da9f8e17a` | MATCH |
| 48 | `refs/recovered/recovered/checkpoint-recovered/remotes/origin/work/v2-d135-topone-amendment-20261027` | `17d7553cf3ad92700f849f696134de67b64b0dfa` | MATCH |
| 49 | `refs/recovered/recovered/checkpoint-recovered/remotes/origin/work/v2-d136-rejected-refusal-20261026` | `fa709f645ac5ac21b861836db74ab23da9f8e17a` | MATCH |
| 50 | `refs/recovered/recovered/checkpoint-recovered/tags/checkpoint/d014-controlled-accepted-20261022` | `d5706537d03801cca9caa9078952496c59fbf41d` | MATCH |
| 51 | `refs/recovered/recovered/checkpoint-recovered/tags/checkpoint/g4-research-20261021` | `f0190af646378441b5eabfc3616c26b3fc46c252` | MATCH |
| 52 | `refs/recovered/recovered/heads/work/m00-brief2-execution-20261027` | `b05577a3a87b3bc23279075ef052125b9cab8ab1` | MATCH |
| 53 | `refs/recovered/recovered/remotes/origin/HEAD` | `5219004223e33291f1b831382e8427742e00427f` | MATCH |
| 54 | `refs/recovered/recovered/remotes/origin/work/m00-brief2-execution-20261027` | `5219004223e33291f1b831382e8427742e00427f` | MATCH |
| 55 | `refs/recovered/recovered/remotes/origin/work/m00-brief2-plan-20261027` | `bc02a472eaa3a07c7f112dee48e5b1f6fa1764dc` | MATCH |
| 56 | `refs/recovered/recovered/remotes/origin/work/v2-d135-topone-amendment-20261027` | `17d7553cf3ad92700f849f696134de67b64b0dfa` | MATCH |
| 57 | `refs/recovered/recovered/tags/checkpoint/d014-controlled-accepted-20261022` | `d5706537d03801cca9caa9078952496c59fbf41d` | MATCH |
| 58 | `refs/recovered/recovered/tags/checkpoint/g4-research-20261021` | `f0190af646378441b5eabfc3616c26b3fc46c252` | MATCH |
| 59 | `refs/recovered/remotes/origin/HEAD` | `b05577a3a87b3bc23279075ef052125b9cab8ab1` | MATCH |
| 60 | `refs/recovered/remotes/origin/work/m00-brief2-execution-20261027` | `b05577a3a87b3bc23279075ef052125b9cab8ab1` | MATCH |
| 61 | `refs/recovered/tags/checkpoint/d014-controlled-accepted-20261022` | `d5706537d03801cca9caa9078952496c59fbf41d` | MATCH |
| 62 | `refs/recovered/tags/checkpoint/g4-research-20261021` | `f0190af646378441b5eabfc3616c26b3fc46c252` | MATCH |
| 63 | `refs/remotes/origin/HEAD` | `d14cb0102bfdf405bc157c7e4fa3e0d1714fb41a` | MATCH |
| 64 | `refs/remotes/origin/work/m00-brief2-execution-20261027` | `d14cb0102bfdf405bc157c7e4fa3e0d1714fb41a` | MATCH |
| 65 | `refs/tags/checkpoint/d014-controlled-accepted-20261022` | `d5706537d03801cca9caa9078952496c59fbf41d` | MATCH |
| 66 | `refs/tags/checkpoint/g4-research-20261021` | `f0190af646378441b5eabfc3616c26b3fc46c252` | MATCH |

### Appendix B — finite source-named case census and negative fixture byte hashes

`case_id` and function suffix correspond exactly to the pinned owner list, active ledger and AST-read physical modules. Fixture hashes were independently computed from every actual physical JSON file in this receiver; “none” is an explicit ledger null, **not** an omitted asset. Every row's execution status is from the unchanged pinned active ledger; no pytest collection:

| No. | Owner finite case identity | Source function suffix | Physical external negative fixture SHA-256 | Execution |
| ---: | --- | --- | --- | --- |
| 1 | `D091-CONTROLLED-SUCCESS` | `test_d091_controlled_success` | none (declared null) | HELD |
| 2 | `D091-CONTROLLED-REACHED_REFUSAL` | `test_d091_controlled_reached_refusal` | none (declared null) | HELD |
| 3 | `D091-CONTROLLED-SEAL-REFUSAL` | `test_d091_controlled_seal_refusal` | none (declared null) | HELD |
| 4 | `D091-CONTROLLED-NONFINITE-REFUSAL` | `test_d091_controlled_nonfinite_refusal` | none (declared null) | HELD |
| 5 | `D091-CONTROLLED-ABSENT-REFUSAL` | `test_d091_controlled_absent_refusal` | none (declared null) | HELD |
| 6 | `D091-CONTROLLED-RECEIPT-ASOF-REFUSAL` | `test_d091_controlled_receipt_asof_refusal` | `cf079a54252dd708201d09c3e76c216221bc3f7b6b07beb1914888674a37d706` | HELD |
| 7 | `D091-CONTROLLED-CUTOFF-ORDER-REFUSAL` | `test_d091_controlled_cutoff_order_refusal` | `53c9a8d7c7eaf38a4544584ceea518881c49469f976a206be6f7c4010ba548b7` | HELD |
| 8 | `D091-CONTROLLED-TOP-RANK-TIE-REFUSAL` | `test_d091_controlled_top_rank_tie_refusal` | `0d34b51e309db8799bd6426f1e183a80e1d9244354cda2867af2b1e7271ef0fc` | HELD |
| 9 | `D091-CONTROLLED-OVER-64-REFUSAL` | `test_d091_controlled_over_64_refusal` | `ba7129a821d9e6434be9fc5fcc454d8ebd78f043c090255f0c1c2cfde630caf7` | HELD |
| 10 | `D091-CONTROLLED-CURSOR-NONPROGRESS-REFUSAL` | `test_d091_controlled_cursor_nonprogress_refusal` | `4031f4640a1373c377a623f442a0f2ec859a176ac725906c48cc6b2b1e5d2fcf` | HELD |
| 11 | `D091-CONTROLLED-DUPLICATE-ID-CONFLICT-REFUSAL` | `test_d091_controlled_duplicate_id_conflict_refusal` | `c9fbf5aa427b87d287f05e4b5cfe2daadb50e3236d1529654fd6450db6896c98` | HELD |
| 12 | `D091-CONTROLLED-PRECOMMIT-SQLITE-FAILURE` | `test_d091_controlled_precommit_sqlite_failure` | `0f954fc8d7a132091576cb7af92072d7eabc839c47373189658130437cc4e20b` | HELD |
| 13 | `D091-CONTROLLED-UNCERTAIN-COMMIT-FAILURE` | `test_d091_controlled_uncertain_commit_failure` | `15b15b769d92258731c6cd72cc6ca322a331401249d42be74443f0166cd135e3` | HELD |
| 14 | `D091-CONTROLLED-SAME-ID-CONTENT-CONFLICT` | `test_d091_controlled_same_id_content_conflict` | `93154f6bf3d26c09b1b74718112016d1002ef39efcaf084c189f1b4a1af06408` | HELD |
| 15 | `D091-CONTROLLED-ORIGINAL-GETTER-MISSING` | `test_d091_controlled_original_getter_missing` | `ac1b985e87cb2f4ca0dfed0fd1dc3bb4c0fac8d5794ff4831cda2014a68810b3` | HELD |
| 16 | `D091-CONTROLLED-ORIGINAL-GETTER-UNITS-MISMATCH` | `test_d091_controlled_original_getter_units_mismatch` | `a80a39c150eafb970089f40f7d8ba60c82ae43cb248abb5e472497f2edd49608` | HELD |
| 17 | `D091-CONTROLLED-ORIGINAL-GETTER-GENERATION-MISMATCH` | `test_d091_controlled_original_getter_generation_mismatch` | `e3b11ca22017e465fc63f11b102bbc6d696d2fe40436b6bc5a501e0da4078352` | HELD |
| 18 | `D091-CONTROLLED-UNSEALED-REFUSAL` | `test_d091_controlled_unsealed_refusal` | none (declared null) | HELD |
| 19 | `L01B-R112-CONTROLLED-NATIVE-UNITS-REFUSAL` | `test_l01b_r112_controlled_native_units_refusal` | `b337bb83a61b02fd470f5fa06cbeeb6c9bc4c22327cfb080bd1e3d0a8e594b33` | HELD |
| 20 | `L01B-R112-CONTROLLED-SOURCE-PROVIDER-REFUSAL` | `test_l01b_r112_controlled_source_provider_refusal` | `311449aecf4aa3cf92dcedb6cf50d5d04c70af10531d2a119e032f0c2755679d` | HELD |
| 21 | `L01B-R112-CONTROLLED-SOURCE-VARIANT-REFUSAL` | `test_l01b_r112_controlled_source_variant_refusal` | `633d5c5a648fb6e9af5835cfde545f753e9d7b9570a7475ec5e6214582a4a12b` | HELD |
| 22 | `L01B-R112-CONTROLLED-CONTRACT-ID-REFUSAL` | `test_l01b_r112_controlled_contract_id_refusal` | `5707a23b542a5e6117fca02c926ffb50e8d9687bd48252696728b7bd71d75aae` | HELD |
| 23 | `L01B-R112-CONTROLLED-UNDERLYING-REFUSAL` | `test_l01b_r112_controlled_underlying_refusal` | `8f56be39fe73c6f9d33eca45a90d8ce4e638000583f5517aa989e7a5adca1c41` | HELD |
| 24 | `L01B-R112-CONTROLLED-SECURITY-TYPE-REFUSAL` | `test_l01b_r112_controlled_security_type_refusal` | `3a62d4f6aeabedf87000c2c5fe1aae7957c6da2d42f78a6eecf594878182193d` | HELD |
| 25 | `L01B-R112-CONTROLLED-RIGHT-REFUSAL` | `test_l01b_r112_controlled_right_refusal` | `cf6d3be90a5cc04ba142673e82b57b38511be1003b3548712fc3e2eda1dc122d` | HELD |
| 26 | `L01B-R112-CONTROLLED-EXPIRY-DATE-REFUSAL` | `test_l01b_r112_controlled_expiry_date_refusal` | `ff9736a906aebf132d97a7b04c8a14018f704a41371361f3abc3eef3c401acd6` | HELD |
| 27 | `L01B-R112-CONTROLLED-STRIKE-REFUSAL` | `test_l01b_r112_controlled_strike_refusal` | `a4c3634f248289bff0c427dc6a66360f087a42c60efdf79048338c5b4223feaf` | HELD |
| 28 | `L01B-R112-CONTROLLED-CURRENCY-REFUSAL` | `test_l01b_r112_controlled_currency_refusal` | `2fc2210a4fe21ca42a0964dd5d1cbeee11e8c98c5b08cfc838564bed4bf53fe3` | HELD |
| 29 | `L01B-R112-CONTROLLED-MODEL-VARIANT-REFUSAL` | `test_l01b_r112_controlled_model_variant_refusal` | `696f8c8141d90f598850d4325ffa0d5a137290b104e28d20b49af36d97f18c62` | HELD |
| 30 | `L01B-R112-CONTROLLED-SCALE-REFUSAL` | `test_l01b_r112_controlled_scale_refusal` | `ecaf3846158cf5da5075051350b4e2af8d50e01a7a6f5c80cdf61e75243c6e2d` | HELD |
| 31 | `L01B-R112-CONTROLLED-GENERATION-REFUSAL` | `test_l01b_r112_controlled_generation_refusal` | `cd1fbb5e284ba83b9219aaae4d413f9ee7c07e4b161e7d8658c96387e27d56d4` | HELD |
| 32 | `L01B-R112-CONTROLLED-REQUEST-ID-REFUSAL` | `test_l01b_r112_controlled_request_id_refusal` | `d1c56064e3c5c94cd9457024ba993b85e694d58056ea449b762fc966b3f5539f` | HELD |
| 33 | `L01B-R112-CONTROLLED-SEQUENCE-SCOPE-REFUSAL` | `test_l01b_r112_controlled_sequence_scope_refusal` | `0604d7e5c15d6de8c651cdcc3233c8d56334b97e394487b7810e5d977bc6d39e` | HELD |

**End of independent Phase A non-product intake; all 33 remain held.**
