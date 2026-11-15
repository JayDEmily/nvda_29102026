# T01 zero-Ruff — current gate and integration reconciliation

**Observation date:** 15 November 2026, Australia/Melbourne. **Jurisdiction:** documentary Git/CI reconciliation of the existing seven-source T01 review, without proof admission or product execution.

## Exact active state

- Main: `a73349834fe4aa1422c194da0492315044b32b98`, containing the owner's first-line continuous-execution instruction in root `AGENTS.md` through merged PR #15.
- Active working branch: `work/t01-ruff-zero-readmission-20261114`. Its reviewed original source candidate is `c616dc5da96af2c2901f2c93e05bbf69f489a725`; subsequent merge `d155a86f92f2bd9a626409dda0b1bf95d158c656` brought in main, changing **only AGENTS.md** relative to the reviewed candidate. Separate merge `8b6790ef10372d112148562883124a81b97e561e` imported the independent review branch without altering any source, product contract, admission pointer, validator, runtime configuration, workflow or frozen governance file.
- Independent review branch: `review/t01-ruff7-source-adequacy-20261114` at `cd1c6be0f639c767368c7b6906288dc73e3919fd`. Its three committed reviews/preflights are reachable through the active branch's Git ancestry. The original independent source-adequacy verdict is `ACCEPT_SOURCE_ADEQUACY (7/7)`, pinned to **c616dc5d**, not a new programme admission.
- During reconciliation the merged working branch reproduced both original read-only `INDEPENDENT_AUDIT_RESULT.json` and `SCHEMA_ADMISSION_PREFLIGHT_RESULT.json` byte-for-byte with the Python 3.13.5 interpreter. No proof tests or active generation mutations occurred. The preservation check `git diff --exit-code c616dc5d <merged-tip> -- tests src config schemas tools .github/workflows pyproject.toml EXEC_PLAN.md GUARDRAILS.md` exited zero. Full `git fsck --full --strict --no-reflogs` passed.

## CI stage evidence, not inferred GREEN

- GitHub Actions run [43547826420](https://github.com/JayDEmily/nvda_29102026/actions/runs/43547826420) on the PR #12 fixture candidate `b67f3e92470fe4e3281546fbc6fc62e347d5f0ee` completed **FAILURE**: `uv sync --locked --extra dev` **success**, next `uv run ruff check src tests tools` **failure** at `Found 51 errors.` The promotion gate was **skipped**. The failures are the known historical immutably bound seven proof-source files (see independent review and Issue #8).
- The reviewed, later zero-Ruff source candidate has independently recorded local Ruff **0.15.11**, `ruff check src tests tools` **exit zero**, preserving all controlled assertions as reviewed. This is **not** a new GitHub Actions run or a claim that the architecture promotion gate passed.
- GitHub Actions run [43660620809](https://github.com/JayDEmily/nvda_29102026/actions/runs/43660620809) for main-derived AGENTS-only PR #15 failed earlier at `uv sync`: required Python **3.12.14** was unavailable; Ruff/promotion were skipped. Direct main has `.python-version` 3.12.14 and no `uv.lock`, while current T01 working branch pins **3.13.5**, retains its complete `uv.lock` and full-history `fetch-depth: 0` checkout. Do not try to repair main CI by promoting partially admitted product changes.
- Existing proof-family contract environment text is historically **CPython 3.12.14/SQLite 3.53.1**; the inspected Ubuntu Python 3.13.5 environment loads SQLite **3.49.1**. These are different and require governed runtime qualification before later product proof; mismatch is not itself a demonstrated code defect.

## Seven existing proposals — no active admission

| Claim | Current generation | Prospective generation |
|---|---:|---:|
| `neutral_market_measurement_truth_pilot` | 4 | 5 |
| `neutral_market_measurement_truth_d030` | 2 | 3 |
| `neutral_market_measurement_truth_d031` | 2 | 3 |
| `neutral_market_measurement_truth_d032` | 2 | 3 |
| `neutral_market_measurement_truth_d033` | 2 | 3 |
| `neutral_market_measurement_truth_d035` | 2 | 3 |
| `neutral_market_measurement_truth_d036` | 2 | 3 |

The source-only `PROPOSED_SUCCESSOR_GENERATIONS.json` remains deliberately **unadmitted**: the proposed embedded `adequacy_review_ref` and `admission_authority_ref` fields are still null, and no next-generation records are installed in `config/product_proof`. Although that earlier worker manifest still carries its historical `REQUIRES_FRESH_ADEQUACY` status string, independent adequacy was subsequently completed on another branch and its original report and audits have now been integrated *without editing the historically pinned manifest or weakening its static verifier*. This document reconciles chronology rather than rewriting the original worker assertion.

**First unmet authority invariant:** an actual current owner/programme admission decision specifically addressing the seven claim successors and the independent adequacy review at `8d1f340940b43f46be3143a8565e6cc2c73ebe1b`. Neither a status string, general instruction to continue, reviewer sign-off, schema shape pass, Ruff green nor Git merge supplies an authentic `admission_authority_ref`. Distinct scope: project owner approval of *this particular seven-generation proof admission*; not an unrestricted change to proof semantics, runtime, tests or D145.

Once authority is supplied, the still-dependent sequence is: claim-scoped immutable generation creation and history-safe active-pointer transitions; authorised independent sole-tester strict product aggregates one at a time with environment qualification; original complete CI (including promotions) at the admitted tip; independent cumulative candidate review; and only then potential main integration. Do not merge experimental PR #14, revive the Terra Max job or skip any failed invariant.

**Dispositions:** source adequacy `ACCEPT 7/7`; CI evidence specific to the named old runs; active new generations `NONE`; product proof `NOT_RUN`; admission authority `NOT_ESTABLISHED`; full CI `NOT_PROVED`; main feature merge `NOT_AUTHORISED`; D145 `PAUSED`.
