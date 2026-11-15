# T01 — independent PR #14 lint-policy and 23-path cumulative review

**Date:** 15 November 2026 (Melbourne). **Repository:** JayDEmily/nvda_29102026. **Independent reviewer:** separate ChatGPT conversation, not PR #14's author. **Scope:** policy adequacy, historical proof invariants, cumulative CI corrections, compatibility with Astra T01 and current main. No product proof or code changes.

## Verdict

**ACCEPT_POLICY_CANDIDATE — exact PR #14 SHA `831471d69afd092779a6810ee570285182be88a8`, for a bounded proposed lint-policy decision only.**

**NOT OWNER-ACCEPTED; NOT MAIN-MERGE AUTHORISED; NOT PRODUCT-PROOF ACCEPTED.** This reviewed design deliberately changes lint success from *zero Ruff findings* to *exactly 51 immutable historical findings and zero changed/new findings*. It is a defensible *proposed* historical exception because original proof-source bytes/generations are preserved and the actual verifier fails closed in independent falsifications. It must be expressly accepted by the programme owner before adoption. No inherited draft proposal, successful Actions run, or review verdict can self-authorise this change.

## 1. Exact pinned state and branch reconciliation

- Current main `a73349834fe4aa1422c194da0492315044b32b98`; root AGENTS includes the new 15 November continuous-execution instruction, Git blob `725f520eeb45f0febabf3ae813ce6bb09c54ee44`.
- PR #14: draft/open, head `831471d69afd092779a6810ee570285182be88a8`, base PR #12 successor `b67f3e92470fe4e3281546fbc6fc62e347d5f0ee`.
- Historical pre-AGENTS main `ded4b98e1e5999d1ddf2f067e660b691917bcd71` is the exact common ancestor.
- Historical main→PR #14 endpoint diff: **23 paths**. Current main→PR #14 endpoint diff: **24 paths**; the extra is root AGENTS, because PR #14 predates the owner instruction.
- Independent **normal merge simulation** in a disposable current-main worktree: `git -c user.name=ChatGPT-Independent-Reviewer -c user.email=chatgpt-review@localhost merge --no-commit --no-ff 831471d...` succeeded without conflict. Only the original 23 paths were staged; AGENTS remained exact blob `725f520...`. `git diff --cached --check` passed; `git merge --abort` returned to a clean main tree. No main merge occurred. **A wholesale tree replacement, unlike an ordinary merge, would lose AGENTS.**
- Astra `ADR_20261112_ASTRA_NVDA_METHOD_AND_FORWARD_ARCHITECTURE_REVIEWS.md`, methodology sections 4 and 6, advises a selective main-based candidate, retained historical refs and one exact owner adoption decision, not a wholesale unreviewed branch promotion.

## 2. All 23 cumulative paths — independently classified

| Class | Count | Exact paths/scope |
|---|---:|---|
| Required CI workflow | 1 | `.github/workflows/architecture-kernel.yml`: checkout now `fetch-depth: 0`, replaces all-zero Ruff step with proposed strict SHA-bound verifier; preserves locked sync, architecture promotion and diff check |
| Runtime/lock | 3 | `.python-version`, `pyproject.toml`, `uv.lock`: CPython 3.13.5, Linux x86_64 offline dependencies, Ruff 0.15.11 |
| New wheel archives | 4 | `librt`, `mypy`, `psycopg_binary`, `pyyaml` CPython 3.13 compatible wheel files |
| Non-admitted formatting | 2 | `src/nvda_desk/derived_signal_calculation_truth/_financial_policy.py` and `tests/product/derived_signal/test_m01_stage1_semantics.py`; original/candidate Python ASTs identical |
| Architecture tests | 4 | `test_identifier_taxonomy.py`, `test_implementation_authority_ingress.py`, `test_registry_schema.py`, `test_proof_control.py` under `tests/architecture/` |
| Historical pre-admission inventory | 1 | `tests/architecture/fixtures/pre_admission_20261018_inventory.json` |
| Proposed lint policy | 2 | `config/lint/PROPOSED_SHA_BOUND_RUFF_BASELINE.json` and `tools/proposed_admitted_ruff_baseline.py` |
| Historical submission/evidence | 6 | `handoff/planning/t01_immutable_ruff_20261114/PROPOSAL.md`; CI, pre-admission and lint review requests; fixture worker evidence and its retained raw 61-case log |

**Total 23/23.** The read-only audit JSON lists every exact changed path. The entire candidate remains unchanged in `GUARDRAILS.md`, root `AGENTS.md`/`EXEC_PLAN.md`, `tests/AGENTS.override.md`, `config/product_proof` admissions/generations, and all seven historically SHA-bound proof sources, relative to `ded4b98e`.

**Architecture changes:** M03 already appears as `configured_market_conditions` in actual admitted registry/allocations, making M04 the next free module ID. Updated test expectations reflect that source state. The historical pre-admission fixture prunes only a *disposable* copy to exact original membership. Independent `git ls-tree` at `86b23f1ef5bf4a1510e93333fa4b2cfc869c3b71` matched **101 original Python paths, 93 physical `test_*.py` files and six proof-config files**. The fixture's historical membership is correct; it does **not** claim retained Python-file bytes equal the old versions. The later current M00 Brief2 acceptance test now uses a separate current-universe copy, retaining positive validation and both original falsifiers. These are architecture-fixture repairs, not rewriting physical product proof.

**Four wheel archives:** independent read-only ZIP CRC and all populated wheel `RECORD` SHA-256 entries passed; physical SHA-256 and sizes are in the wheel inventory receipt. `uv.lock` refers to vendored wheel paths and versions, without individual wheel SHA-256 records. Git pins their candidate bytes; publisher-origin/provenance was not independently authenticated. GitHub Actions' locked install passed, which verifies CI installability—not full product-runtime compatibility.

## 3. SHA-bound policy: independent test results

**Normative authority:** `docs/architecture/TEST_AND_PROMOTION_KERNEL.md` AK-PROOF-001/002, and frozen GUARDRAILS, require exact product-proof membership and all registry-derived architecture proof; neither accepts a Ruff exception automatically.

The proposed gate still invokes complete Ruff **0.15.11** over `src tests tools`. Independently reproduced **exactly 51** historical errors: `E501=38, I001=5, B905=4, RUF007=4`, digest `08ae839b0596c31ecb73a4667845f0d19dfe0c4503c52079434dd98e835a2a8f`.

For each of seven immutable proof files, independent calculations matched the original historical main byte SHA, proposed lint manifest SHA, current admission pointer, exact generation record SHA, claim identity and family/support membership. Candidate's seven proof files remain byte-identical to historical main. The manifest's own SHA-256 is `d38367ce1f63a1731c0cd9b69e12af021a291d71b0206f83ba17f3b69dbfc97c`.

**Independent actual CLI falsifications (5/5 reject):**
1. Change admitted proof-source bytes → `admitted source bytes changed`.
2. Change active generation pointer → `selected generation changed`.
3. Change current generation JSON bytes → `generation bytes or pointer changed`.
4. Change lint policy manifest bytes → `baseline manifest byte identity changed`.
5. Introduce a new Ruff F821 in previously clean source → `Ruff findings changed by path`.

Untampered verifier succeeded before and after, all edits reversed in *disposable* `nvda_t01_pr14_falsification_20261115`, worktree clean. No product proof/test or real admission mutation. Full read-only audit, adversarial script, exact JSON results and wheel inventory are committed beside this report.

**Policy limitation:** preserving the 51 is not the same as fixing their lint violations. The policy explicitly grandfathers unchanged original proof bytes; introducing any changed diagnostic is refused. This is narrower than a broad ignore but still a real change to the lint acceptance criterion. Prior PR #7 broke proof admission by reformatting original SHA-bound files, as evidenced in Issue #8; this is the **RECURRENT_CLASS** risk being addressed.

**F09 — An alternative lint entry point is not reconciled.** The current repository `Makefile:23` has a `lint` target that still directly runs `ruff check src tests tools`, while the PR #14 workflow substitutes the SHA-bound verifier. The reviewer executed `make lint` in the untouched PR #14 disposable candidate with the pinned Ruff 0.15.11; it reported `Found 51 errors.` and `make: *** [Makefile:23: lint] Error 1`. The separate CI workflow did pass using the proposal's different criterion. This is a **verified divergence of two lint entry points**, not a failure of the proposed mandatory CI verifier or a product-code defect. **Recommendation if the owner adopts the revised repository lint policy:** explicitly reconcile `Makefile`'s `lint` target to that accepted gate in the newly reviewed integration candidate, retaining Ruff's unmodified traversal and exact historical SHA checks. This would add an **additional changed path** beyond the original 23; neither the earlier 23-path review nor its Actions run proves the modified Makefile. The archival command in `docs/evidence/akr5/AKR5_STRUCTURAL_READINESS.md` is historical evidence, not an active workflow. No Makefile change was implemented by this review. The exact direct command/output is retained as `INDEPENDENT_MAKE_LINT_PRECHECK.py` and `INDEPENDENT_MAKE_LINT_RESULT.json`: `make lint` exit code **2**, expected **51** Ruff diagnostics, and clean PR #14 source worktree.

## 4. Real CI evidence and remaining acceptance boundaries

At exact PR #14 head, [GitHub Actions run 43553729850](https://github.com/JayDEmily/nvda_29102026/actions/runs/43553729850), job `132321748235` on 14 November: **all steps SUCCESS**. CPython **3.13.5** `uv sync --locked --extra dev` passed; proposed verifier matched 51/digest; unmodified `tools/run_promotion_gate.py --set architecture_kernel` ran **221/221 architecture/bootstrap checks PASS in 1747.09s** (11 admitted test families); `git diff --check` passed. These are genuine CI observations at the **draft head**, not self-authorisation of a policy and not seven physical product-proof aggregates.

At present, **main still pins Python 3.12.14 and zero-Ruff lint**. The selected Ubuntu Python 3.13.5 independently reports built-in SQLite 3.49.1, whereas original seven-family contracts record Python 3.12.14/SQLite 3.53.1; separate proposed T01 plans discuss SQLite 3.54.1. None of these is automatically equivalent to the other. Runtime qualification remains a **later conditional product-testing gate**, not a demonstrated code defect.

**Important exact uninstalled state:**
- The independently accepted PR #3 documentary successor (`3d8f1fae...`, independent report `a982b163...`) remains draft/unmerged. Its 39 leaves, 35 original proof obligations (34 proposed L32 tests; D145 blocked at L31) and separate independent Tester survive, but the main root `EXEC_PLAN.md` is still the October documentary plan.
- PR #3's proposed replacement AGENTS predates today's new first-line owner directive; preserve current first line in any future exact integration. Dependency-focused earlier test windows are Astra's **proposal**, not already adopted by PR #3. Any amendment requires concurrent plan, test override and ledger changes and independent review.
- Original programme choice of lint acceptance policy, exact main integration, T01 successor installation, checkpoint-method change and any test-schedule amendment are reserved owner decisions. PR #14 has no owner adoption record.
- Current GitHub rulesets query yielded `[]`; direct branch-protection endpoint returned **403 Resource not accessible by integration**. Required-check/protection state is **UNKNOWN**, not independently cleared.
- Exact later full-history 66-plus-ref/non-Git receiver closure is not established by this review. No branch deletion or force rewrite. D145 remains PAUSED.

**Adoption-time inconsistency requiring deliberate revision:** PR #14's manifest status remains `PROPOSED_NOT_ACCEPTED`, its code requires that value, the verifier docstring says not wired into CI, and the Actions step is labelled `PROPOSAL ONLY`. These labels correctly describe the draft, but would be false if copied as *adopted* main policy. After an explicit owner decision, prepare an exact reviewable revision of the manifest-verifier SHA binding and step/docs and verify it anew. Never silently relabel existing passed evidence to apply to a changed candidate.

## 5. Disposition and recommended next action

| Proposition | Independent verdict |
|---|---|
| Bounded historical SHA-bound lint policy *design*, exact `831471d...` | **ACCEPT_POLICY_CANDIDATE** |
| Seven proof sources/generations/pointers unchanged | **PASS 7/7** |
| 51 diagnostics and exact Ruff 0.15.11 traversal | **PASS**, strictly pinned historical findings, not zero |
| Five adversarial refusals | **PASS 5/5** |
| Exact candidate mandatory GitHub architecture CI | **PASS 221/221** |
| Present-main no-commit merge feasibility | **PASS**, AGENTS preserved, no main changes |
| Four binary archive internal RECORD integrity | **PASS**; publisher provenance **UNKNOWN** |
| Owner lint acceptance / revised main-derived candidate / new CI | **PENDING** |
| T01 successor plan installation, new product proof, seven proof admissions | **NOT DONE/NOT AUTHORISED** |
| D145 | **PAUSED** |

**Recommended one path:** prepare one current-main-derived acceptance/integration candidate **after owner expressly adopts the narrowly specified policy**, preserving current AGENTS, reconciling the distinct Makefile `lint` entry point as an additional explicit changed path, and proposing coordinated T01 root/Tester/checkpoint updates for separate exact review. Do not merge historic PR #14 wholesale or install a provisional policy without owner adoption. Require fresh full CI on the final integration candidate, independent review of any changed policy/governance meaning, then exact authorised main promotion. Historic PR #14 and the alternative zero-Ruff proposal remain recoverable, not erased.

## 6. Audit scope and omissions

**Directly inspected:** full current GUARDRAILS, AGENTS, test-local override and active ExecPlan; normative AK-PROOF document; full PR #14 reviewer request, verifier, manifest, historical inventory; complete proposed T01 AGENTS/override/ExecPlan and original Astra methodology ADR from the preceding assessment; exact 23 changed paths and relevant Python/architecture test hunks; original historical fixture tree; Actions job/results/log; Git history and current-main merge behaviour; archived wheel contents. Full scripts/JSON provide exact commands, outputs and reproducible inputs. The additional `INDEPENDENT_MAKE_LINT_PRECHECK.py` and `INDEPENDENT_MAKE_LINT_RESULT.json` preserve the direct Makefile-lint failure at the untouched candidate without modifying the workflow or product files.

**Not performed:** independent re-execution of 221 architecture tests, product pytest/proof, main merge, any new proof generation or authority change, separate SQLite qualification, audit of publisher origin, GitHub branch protection admin readback, T02 complete additional-ref/non-Git receiver, full unchanged architecture test source audit or adoption of Astra future product architecture.

Review branch starts from current main, separate from PR #14. All actual temporary mutations were reversed on the disposable worktree. This report is an **independent technical reviewer judgement**, never an owner-policy decision or proof admission.
