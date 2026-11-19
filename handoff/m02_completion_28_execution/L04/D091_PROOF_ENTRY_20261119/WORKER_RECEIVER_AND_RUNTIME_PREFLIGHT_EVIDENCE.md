# D091/L01b PR #27 — Worker-only fresh receiver and offline runner preflight

**19 November 2026, Melbourne. Evidence class: directly executed non-product commands on DESKTOP-I188O30 WSL Ubuntu.** Disposition: **WORKER_PREFLIGHT_STATIC_PASS / INDEPENDENT_STRICT_TESTER_AND_CASE_RELEASE_NOT_YET_ESTABLISHED.**

## Governing and pinned scope

- User requested continuation of PR #27 towards proof: “Sorry, I've lost track of where we are. So, I guess to prove things, so just go. PR 27. So do what you need to do.”
- **Pinned candidate assessed by these commands:** `b7d044a4f84b7f70703322c250cbd82cee6f4589`, tree `0704cd4ebe09801e7116ed517cceda756f5e1dbf`; latest Worker branch advanced only by the subsequently published **receiver preflight commission** `b2a448684a8a2bc6e1495ae461fe637ea92d3622`. Never substitute a moving PR branch for the pinned candidate.
- Read full `GUARDRAILS.md`, `AGENTS.md`, `tests/AGENTS.override.md`, root `EXEC_PLAN.md` in sections, post-install independent verdict/closeout, current ledger and dependency windows. The owner-installed November governance status is resolved by `handoff/astra_adr_continuation_20261115/INSTALLATION_RECEIPT.md`; inherited proposal headers are earlier drafting language.
- Separate independent non-product receiver/runner commission: `handoff/m02_completion_28_execution/L04/D091_PROOF_ENTRY_20261119/INDEPENDENT_RECEIVER_RUNNER_PREFLIGHT_COMMISSION.md` on `b2a44868` (blob `64a89044132ad2f989af2230423c3ef3574f603f`). That independent report remains **unpublished**; this is **Worker** evidence only, and no strict Tester is designated.

## Exact fresh Git receiver — observed PASS on the Worker side only

Created new isolated `/home/jds/nvda_d091_receiver_worker_preflight_20261119` under WSL; did not modify existing source/checkouts. Used `git init`, `git remote add origin https://github.com/JayDEmily/nvda_29102026.git`, and fetched the live PR #27 Worker branch plus these five historical recovery branches: `recovery/legacy-d010-20261111`, `recovery/legacy-d131-20261111`, `recovery/legacy-m00-brief2-20261111`, `recovery/legacy-next20-20261111`, `recovery/r2-g0-f02-20261111`.

Initial guard compared the moving remote Worker branch to the earlier pinned candidate and **stopped** at `b2a44868` versus `b7d044a4`. This reflected the **expected single commission commit**, not an assumed changed source. Preserved the freshly fetched receiver, verified the immutable `b7d044a4` object was an ancestor of remote `b2a44868`, then detached checkout at the exact pinned `b7d044a4`.

Used the original Git-manifest `handoff/planning/t01_recovered_successor_20261111/ORIGINAL_66_REFS.json`, Git blob `162b242eee672bbaa1b4a1e30d63bb2d71657fe3`, and direct `git cat-file -e` checks to establish **66/66 original tip objects present**. Re-created all **66 exact original ref names**, including legacy non-branch names, using `git update-ref`; then verified each `git rev-parse --verify <ref>` equals the manifest tip. `git fsck --full --no-reflogs` returned exit 0; 4,339 tracked files, clean worktree and exact candidate tree `0704cd4ebe09801e7116ed517cceda756f5e1dbf`. Native output file: `/home/jds/nvda_d091_worker_receiver_fsck_20261119.log`. **This receiver is not an independently authenticated strict Tester receiver and does not establish all non-Git asset prerequisites.**

## Original proof bytes and case holds — direct static readback

Read original candidate's actual active `TEST_EVIDENCE_LEDGER.json` blob `387eb533c436dc598d5dd75ca74322d2af60d00b` and bytes under fresh checkout, not case-result reports:

| Exact item | Observed |
| --- | --- |
| D091/L04 case identities | **18/18**, all `OWNER_FINITE_ADMITTED_EXECUTION_HELD`, `execution_authorised=false` |
| Separate L01b/R112 source-support case identities | **15/15**, same execution hold |
| Distinct negative fixture SHA-256 values | **27/27 matched** directly against their on-disk JSON bytes and ledger |
| Original R112 positive closed-batch JSON SHA-256 | `1f4c46c5c247c78e3e18bb2de02c172f775379f664bad8e056ef6867a39d03dc` |
| D091 18-case test source SHA-256 | `d1eab7802786344ecf9ab4d4e2f46b802aba6d2fea0c72d14ad149492504b86f` |
| L01b 15-case test source SHA-256 | `1f648998ca4c64829a3655057598e5ae5687b6568bb7e9eebf7ca2f17caa56f5` |
| Installed generation-1 JSON SHA-256 | `429df0e6b732ed019f9bc62d67f36bc295b556f89f7da670e8d76fcce4581097` |
| Active `admission.json` pointer against that generation | **matched** |

Source of fixture check: non-product script `C:\Users\james\AppData\Local\Temp\nvda_d091_worker_static_pin_audit_20261119.py`; executed via `wsl.exe -d Ubuntu -- python3`, exit 0. No product imports, pytest collection, assertion-oracle executions or business code calls.

## Current Python / SQLite and offline dependencies

- A previously selected `/home/jds/nvda_uv3135_20261112/.venv/bin/python` is CPython **3.13.5** (executable SHA-256 `0eba26d5f04a3673ee264ca406ef286d5025da098c1a24987a8118c23d69153c`) but exposes SQLite **3.49.1**. It is **not** evidence of selected 3.54.1 product-runner linkage.
- Discovered an existing *different* private CPython 3.13.5/SQLite3.54.1 build at `/home/jds/nvda_python3135_sqlite3541_20261117/`. Direct SHA-256: Python binary `d114ec20c65fb65c77608f7b8b7110d0ff95e3b3c814f65580dad17fb56e012c`; private `sqlite/lib/libsqlite3.so.0` `44a469c2ed17ee19dca5f0c949f97b98b7ad0f1260bdb41fc153a4530324fb2f`; `_sqlite3` extension `52d1d07388e3ccadf59d5071088f69c52d43071bb15092291798392407d28ab7`. With explicit `LD_LIBRARY_PATH=/home/jds/nvda_python3135_sqlite3541_20261117/sqlite/lib`, current stdlib inspection reports CPython **3.13.5**, SQLite **3.54.1**, source ID `2026-10-16 14:45:20 555e07ef33f69a0957d24d8e555b702464a131d6f1607f4c3c1e4551e8e6ca76`; loaded map points to that precise private library and hash. The local Nov-17 `qualification_receipt.json` reports nine bounded non-product checks; **this Worker did not rerun those nine checks**. Its 44a469... library bytes are **different** from the independently reconstructed historical c537069... library bytes; neither is silently substituted for the other.
- Created isolated virtual environment **outside the Git repository** at `/home/jds/nvda_d091_worker_proof_runner_venv_20261119` from the current private Python; used strictly `pip --no-index --find-links /home/jds/nvda_d091_receiver_worker_preflight_20261119/vendor/wheels`, no network/package resolver downgrade. Installed exact pinned `pytest==9.0.3`, `PyYAML==6.0.3`, `ruff==0.15.11`, `mypy==1.20.1`, `psycopg==3.3.4`, `hatchling==1.29.0` and their available wheel dependencies. Direct `importlib.metadata` confirmed all six versions. Selected venv process with the explicit private `LD_LIBRARY_PATH` loaded SQLite 3.54.1 and hash `44a469...`. Install command/output: `/home/jds/nvda_d091_worker_proof_runner_install_20261119.log`.
- Pinned fresh candidate `.python-version` SHA-256 `e72b03ed5b70312f2782f2b05055b24670e126d50e24c4f2c559bf288f810`; `pyproject.toml` `c62bb0b0cbc96707de3444037a2e628c95cac75ebf8b44ebb0a5ebc9e5296225`; `uv.lock` `65800a98bc9f14fd7df23aac7206fe90d9d3c73c9b221bfbe7e90a4092c3290d`. **No product module import, product test run, collection, product qualification or case verdict.**

## First unclosed gates — no false PASS

1. **Genuinely independent receiver/runner report pending.** Published commission is fixed, but Chrome launched the NVDA project URL as a blank `Untitled` window with no accessible project composer. A single guarded refresh did not restore its editor. Attempt to navigate a saved existing review via exact visible project link was stopped before invocation by a foreground-focus mismatch. **No separate reviewer prompt was sent**. This is a specific Windows UI handover blockage; not evidence of network-wide ChatGPT refusal or a repo defect. A separate independent thread can fulfil the fixed commission directly, without modifying this candidate.
2. **Strict Tester and exact product proof release not established.** All **33** cases retain the unchanged ledger's `execution_authorised=false`, `claim_generation_binding=UNBOUND_FUTURE_PRODUCT_CANDIDATE`, and `SEPARATE_INDEPENDENT_TESTER_NOT_YET_DESIGNATED`. The present broad owner direction commissions continued prerequisites; it is **not a record of a specifically designated strict Tester or released 33 concrete product-test nodes**. No product case was run by Worker.
3. **Non-Git asset and strict runner applicability remain to be adjudicated independently.** Historical `OUTSTANDING_ASSETS_CURRENT.json` has five blocked inventory rows representing four old historical exact byte assets and a separate historical CPython3.12.14 toolchain unknown. Do not claim these are necessary for the specific D091 run without tracing its actual receiver dependencies. The new venv is a reproducible, statically checked candidate—not a separate Tester's product runner qualification.
4. **No programme state promotion.** No change to source, test files, proof generation, admissions, ledger, GUARDRAILS, AGENTS, ExecPlan, D145 or PR merge. PR #27 remains a draft Worker branch until separately accepted. Do not infer `TESTED_ACCEPTED` from a registered generation.

**Next exact action:** obtain separate reviewer receiver/runner preflight against `b7d044a4` by the already-published commission at `b2a44868`; independently read its GitHub report. Then produce an exact, immutable case/runner/role release decision under accepted dependency windows and direct source authority; only the specifically designated strict Tester may perform real 33-case executions. Do not repeat 33 documentary oracle reviews or re-request the already granted implementation/generation approval.
