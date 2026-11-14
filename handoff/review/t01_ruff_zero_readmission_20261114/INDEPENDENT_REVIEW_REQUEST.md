# T01 — Zero-Ruff successor sources, unadmitted proof review

**14 November 2026 (Australia/Melbourne) — WORKER CANDIDATE / NOT ADMITTED / INDEPENDENT ADEQUACY REVIEW PENDING.**

## Authority, baseline and precise claim

Repository: `JayDEmily/nvda_29102026`. Work branch: `work/t01-ruff-zero-readmission-20261114`. Exact proof-preserving base: `b67f3e92470fe4e3281546fbc6fc62e347d5f0ee` (PR #12). Source-only preparation commit: `28baa81fb02f7aad34b0b652b5477788998bb48f`.

Owner direction on 14 November 2026: **preserve PR #14 as evidence, do not merge it, resolve all 51 historical Ruff findings by compliant successor source and proper independent proof re-admission rather than accepting a permanent lint exception**. The owner subsequently commissioned continuous execution. This authorises scoped preparation, not a fabricated independent adequacy verdict, retrospective admission, product-proof success or merging main.

Normative boundaries actually inspected: frozen `GUARDRAILS.md`; root `AGENTS.md`; `tests/AGENTS.override.md` (independent reviewer sole strict product-proof executor); active root `EXEC_PLAN.md` (M02 documentary task; unrelated product work not implied by that historic plan); current `tools/product_proof_claims.py:256–406` (immutable selected generation/file identity and Git transition law), `tools/run_product_proof_gate.py:24–82` (clean repository, READY active claim, strict actual outcomes), and `handoff/foundation_implementation/authority/PA02_PRODUCT_PROOF_ADMISSION_PROPOSED.md:125–193` (methodological evidence: fresh adequacy review and admission, immutable previous generations, distinct readiness and actual proof). **PA02's proposed label is not used as an independent new authorisation.** Actual prior accepted generation 2 for D014 was only admitted after independent reviewer clearance and a separate recorded programme disposition in the G5 execution history.

## Source-only repair and exact observed evidence

Exactly **seven** files change relative to the PR #12 base: one existing pilot required support file, D030, D031, D032, D033, D035 and D036 existing physical family files. The current generation in each of these seven claims pins the original bytes. No product maths, expected decimals, claim contract, signal identity, test selection, admission validator, previous generation, live admission pointer, runtime, locked dependencies, independent architecture tests or frozen governance has been changed.

New source content is **byte-identical** to the corresponding seven edits first prepared in historical PR #7 `8674d1e6fb81cefe6cd66ec45808348bb4f2e793`, but PR #7's mistake (changing SHA-admitted files without new generations) is deliberately *not carried forward as an acceptance claim*. The specific 51 Ruff findings are E501 38 / I001 5 / B905 4 / RUF007 4. Current local locked Ruff 0.15.11 runs `ruff check src tests tools` with **exit 0, All checks passed**.

Static audit compares each changed file with its exact parent Git blob: imports are the same except for adding `itertools.pairwise`, the **non-import AST is identical** after replacing the four explicit `pairwise(SAMPLES)` nodes with their prior `zip(SAMPLES,SAMPLES[1:])` representation. For the actual four literal SAMPLES sequences, the adjacent-interval tuples are equal (5 / 30 / 5 / 10 intervals). This is evidence of syntax equivalence for the reviewed edits, **not a substitute for a product-proof or independent semantic adequacy review**. No product test has been executed by this Worker.

## Complete seven-claim prospective admission register

`PROPOSED_SUCCESSOR_GENERATIONS.json` is a **review-only and intentionally non-admissible** manifest. It records exact current pointer path/hash, current generation, proposed successor number/path, every complete proposed family/support hash row, full historical brief/binding/contract/target fields, and current contract's required test names. The two authority fields for each proposed generation are deliberately `null`. The file lives under `handoff/review/`, **not** under active `config/product_proof`.

| Existing claim | Current generation | Proposed successor | Changed file |
| --- | ---: | ---: | --- |
| `neutral_market_measurement_truth_pilot` | 4 | 5 | `typing/valid_seam.py` (required support) |
| `neutral_market_measurement_truth_d030` | 2 | 3 | `test_trade_rate_zscore.py` |
| `neutral_market_measurement_truth_d031` | 2 | 3 | `test_volume_rate_zscore.py` |
| `neutral_market_measurement_truth_d032` | 2 | 3 | `test_five_minute_realised_volatility.py` |
| `neutral_market_measurement_truth_d033` | 2 | 3 | `test_thirty_minute_realised_volatility.py` |
| `neutral_market_measurement_truth_d035` | 2 | 3 | `test_five_day_realised_volatility.py` |
| `neutral_market_measurement_truth_d036` | 2 | 3 | `test_ten_day_realised_volatility.py` |

The pilot contract selects five physical families; the remaining six contracts select one each, giving **11 exact physical families** and **15 required function names** in aggregate. They are **seven separate claim-scoped aggregates**, not one new catch-all product proof.

The current selected generations retain their original path/hash and Git history. No new `config/product_proof/**/generations/000[35].json` file exists and no `admission.json` pointer has advanced. Accordingly the current resolver will reject the seven changed bytes against the old active generations. This is the **expected first unsatisfied proof invariant**, not an accepted candidate or a permission to bypass the validator.

## Required independent sequence and nonconflation

1. **Independent source adequacy review before new admission.** Fetch exact committed branch head, verify parent and the seven source diffs, the approved contracts/briefs, all original retained generations and current proof-control rules; determine that source assertions and meanings remain adequate. Verify every modified claim independently. Record a concrete judgement and exact artifact/commit references. A source-only Ruff/AST PASS is not that judgement.
2. **Explicit, authority-backed generation transition.** Only after review and an actual programme admission decision, supply each claim's genuine new `adequacy_review_ref` and `admission_authority_ref`. Materialise its complete proposed record as the next immutable generation in its respective `config/product_proof/<claim>/generations/` tree, hash actual JSON bytes, advance that claim's active pointer and commit the exact transition with full Git history. Do not reuse an old review ref, forge an approval string, rewrite the previous record, skip a generation or combine unrelated authority into a single claim. Validate current status/retained history after each lawful admission.
3. **Strict controlled product-proof execution** is reserved for the authorised independent tester, not this author. In a *clean* correctly pinned Git checkout after admission, run the exact existing `tools/run_product_proof_gate.py --aggregate <claim_id>` **one claim at a time**. Retain full stdout/stderr, selection/collection, observed pass/refusal outcome, pre/post governed snapshot and strict no-skip/no-xfail rule for each. Respect each governing per-signal proof budget and legitimate retry rules. Any failure stops dependent advancement, retains first failure and prevents auto-repetition.
4. **CI and integration after appropriate admission/testing.** Verify original whole-tree Ruff (zero findings) and original mandatory Tier A `architecture-kernel` CI at the fully reviewed, admitted target. Require separate independent review of the cumulative candidate, and only then consider integration into main. Draft PR #14 remains a historical evidence-only policy experiment, **not** the future zero-Ruff merge vehicle.
5. Preserve D145 suspension, all original 39 leaves/35 documentary proof obligations, frozen roots, older generation files, experimental branches and Git history. No unrelated source, maths, profile, authority or production strategy change is implied.

`VERIFY_SOURCE_CANDIDATE.py` is a **read-only static audit**: it checks exact parent/candidate Git blobs, source AST, adjacent-pair equivalence, seven prospective transitions, unchanged current admission pointers and zero Ruff 0.15.11 findings. It requires a clean worktree and does **not** execute `pytest`, the product-proof gate or an admission writer. If any of those checks fails, stop and report exact evidence.

## Worker close-out status

**VERIFIED:** 7 source edits committed; exact seven-claim dependency population established; unchanged predecessors; zero whole-tree Ruff; AST/pairwise preliminary verification. **PENDING:** independent adequacy of new proof bytes, actual programme admission authority, seven legal successor generation commits, independent strict product execution and full architecture CI at the admitted source state. No merge or programme activation authorised.
