# Independent D012 implementation review

Disposition: **PASS for the bounded controlled D012 implementation/candidate scope**.
Reference: `independent-review/g61-d012-implementation/5a7bcfe/20261019`.
Reviewer: `/root/g61_d012_implementation_review`, independent judgement; no implementation or shared repository writes.

## Exact subject and authority

Reviewed code/configuration/control/proof candidate `5a7bcfe252a633ec8d13d9a9e2fbe1709b0ea188`, tree `a8ff96bc45862d4cbaee4d89c7f6f3e4baf40160`, against preparation baseline `c8fa2ea91416432ed7426bf1f5b1083b93a9ee51` and accepted root section 7.1. Actual native reruns executed clean evidence-packaging HEAD `6b737fa1b7bd540e857f91c211f7898bfd4e1e83`. `git diff --exit-code 5a7bcfe HEAD -- src config tools tests implementation/authority` returned 0; the only intervening tracked paths are the execution ledger and evidence-package documents/logs. Do not conflate these two commits.

The accepted D012 brief is SHA256 `a31c482d2dc4822539ede99e955761319585af4badea93b9fc279638e1e1f393`; incorporated contract `b8907ef6fba60ab18aadc1a1899997dde11f55735544fee6f2d13d21c7e2a02c`; reviewed generation1 `26d2b4e371c38b0960cb6081798cc618c9f308567d0df12b2aa40f3777dd2a25`. Current acceptance/standing human-checkpoint delegation is the root's `owner-chat/20261019T222804/D012-and-standing-human-exceptions`, not a proof waiver or invented implementation acceptance.

Read governing guardrails, agent/test-local instructions, current root authority, D012 brief/contract, incorporated version2/version3 meaning, original calculation brief, candidate package, current physical proof/specimens, production package, loader/control diff, and relevant reviewer/repair lineage. The three changed M02 source files, unchanged public seam/selection, additional descriptor/binding/admission, control tests and module metadata were inspected. Original catalogue/binding/generation directories, M00/A00/M01 source, pins/vendor, and existing product proof remained unchanged against the preparation baseline in the scoped preservation diff.

## Findings and recurrence

No new Critical, Important or Minor implementation finding was identified in this bounded review. Consequently no new ISOLATED/RECURRENT_CLASS repair is routed.

Relevant lineage was not treated as acceptance by label: G5.2 metadata/fresh-process inadequacies and `a9b4c56`; G5.3 same-ID eligibility-filter omission, proof `78a279f` and repair `b25eea9`; D012 control RETURN/V2 exact-root ownership repair (`7289806`, application `50e6ae9`), physical-proof RETURN/V2 (`9b692ec`/`7eaddf9`), admission `2de5283`, preserved missing-capability RED `17e21d7`, behaviour `80c1946`, first typing/promotion failure `3c95f28`, and finite-exponent local-name repair `5a7bcfe` were inspected. The direct orphan-support probe below confirms the earlier RECURRENT_CLASS control invariant in the current loader. The admitted duplicate/order/page/representation cases execute in the independent strict D012 run. The local-name repair changes no arithmetic law or proof expectation.

## Direct fixture-independent evidence

`direct_review.py` imports only declared MMT/M00 public APIs plus the accepted raw SQLite technical persistence constructor; it imports no Worker helper/fixture or production arithmetic/canonical helper. Inputs/configuration/authority are explicit literals. All observations are admitted by actual public M00 commands to `raw.sqlite`; foundation stores are separate real files.

Observed exit0 on CPython3.12.14/SQLite3.53.1:

- Initially empty history, then direct materialise for bid100.00/ask102.0 under precision1, Emax1/Emin-1, every Decimal trap enabled: exact result tuple for2.00. Advance clock one day, retry directly: exact original occurrence/time/ID retained.
- Five unavailable requests, each immediately followed by bounded history read: subject, missing registered parameter version, strategy context, D013 and future cutoff all return None and leave existing nonempty history exactly unchanged.
- Independently change only definition version, parameter version, selection version, bid mapping version, ask mapping version, one binding's unit version, and cutoff. Every call appends a distinct ID; direct exact old/new reads preserve Decimal tuples, types and references.
- Original authority refuses D012 registration and D012 materialisation; its independently created D011 fact remains exactly readable under original admission.
- Fresh read-only subprocess, receiving only path/IDs, recovers exact typed occurrences, both definition versions, every registered parameter/selection/unit/mapping version and bounded history. Another writer subprocess creates/materialises its own store and exits before a separate read-only process recovers the same complete occurrence. No calculator/raw reader or configuration re-registration is supplied to readers.
- Admit a changed real raw bid104.00, then direct materialise: crossed result -2.00 with a new ID; first fact remains unchanged.

`adversarial_review.py` uses SQLite backup for six separate disposable corrupt-store copies. Public reader construction refuses each: correctly rehashed midpoint101.00; numerically equal but representation-wrong2 instead of2.00; lineage canonical-value representation mismatch; payload content hash; D index; logical-content hash. Each refusal is a non-uncertain owner persistence failure. No actual production/populated store is opened.

For controls it extracts exact5a7bcfe into a disposable copy, bypassing Worker copy fixtures. The actual loader resolves all3 claims READY with their original/new exact generations. A malformed extra descriptor key rejects both original selected claims. Move only copied descriptor/physical proof out: both originals remain READY; add nested/helper.py under the now-descriptor-absent exact D012 root: both originals reject unowned source. No authority/catalogue/generation is resealed.

## Fresh commands and observed results

All native commands ran from `/workspace/scratch/d549b6d808a9/g52-recovery/repository`, with `PYTHONDONTWRITEBYTECODE=1` and interpreter `/workspace/scratch/d549b6d808a9/g52-dev/bin/python`.

| Arguments after interpreter | Observation | Log |
| --- | --- | --- |
| `tools/run_product_proof_gate.py --aggregate neutral_market_measurement_truth_d012` | 80passed, READY, strict/process0; exact new authority/gen1 | strict_d012.log |
| `tools/run_product_proof_gate.py --aggregate neutral_market_measurement_truth_pilot` | 113passed, strict/process0; original authority/gen4 | strict_foundation.log |
| `tools/run_product_proof_gate.py --aggregate raw_signal_occurrence_truth_sqlite` | 30passed, strict/process0; original authority/gen3 | strict_m00.log |
| `tools/run_promotion_gate.py --set architecture_kernel` | 133passed, 11families, zero dependency/public-seam violations, process0 | architecture.log |
| `-m mypy --cache-dir=/workspace/scratch/d549b6d808a9/d012-implementation-review-bssOwx/mypy-cache src tools/product_proof_claims.py tools/product_proof_outcomes.py tools/validate_product_proof.py tools/run_product_proof_gate.py` | Success34files, process0; retained M01 untyped-body notes | mypy.log |
| `-m ruff check src/nvda_desk/market_measurement_truth tools/product_proof_claims.py tests/architecture/test_proof_control.py tests/product/market_measurement_d012` | PASS, process0 | scoped_ruff.log |
| `-m ruff check src tests tools` | process1: exactly inherited M01 E501 `_financial_policy.py:58`, `test_m01_stage1_semantics.py:1932` | full_ruff.log |

The strict D012 run independently executes signed/locked/negative/zero and aligned-representation arithmetic, ambient traps, refusal/selection/pagination/duplicate variants, real transaction precommit rollback, uncertain postcommit acknowledgement/retry, first-public-write competition, fresh process, independent storage corruption, predecessor-source D011 recovery, and positive/negative static specimens. No skip/xfail/deselection/governed mutation counted as proof success. Full Ruff is expressly not green; its two unchanged accepted inherited findings are not a new D012 defect or a repair commission.

To reproduce the direct scripts use a fresh disposable directory (the scripts intentionally create absent files), preserving the scripts unmodified there:

`PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/workspace/scratch/d549b6d808a9/g52-recovery/repository/src /workspace/scratch/d549b6d808a9/g52-dev/bin/python <fresh-directory>/direct_review.py`

Then run `adversarial_review.py` in the same fresh directory with the same environment. Its control snapshot is fixed to5a7bcfe and source repository path is explicit. Original executed files/logs remain at `/workspace/scratch/d549b6d808a9/d012-implementation-review-bssOwx/`.

## Decision boundary

PASS supports current candidate-specific controlled D012 admission judgement after the root preserves this actual evidence. It is not itself owner/delegated candidate ACCEPT, next-family authority, G6.1 completion, FULL126_COMPLETE, native IBKR/source certification, provider/live effects, A00 composition, populated-store compatibility, migration/retirement, production SLA, hostile-code isolation or main merge. Those scopes were not reviewed or executed. No implementation repair was made. Scratch evidence includes only review scripts/logs, disposable proof stores/copies and the report; shared worktree remained clean at verification.
