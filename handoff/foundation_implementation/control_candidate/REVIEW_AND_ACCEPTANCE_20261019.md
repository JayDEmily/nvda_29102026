# Concrete SQLite proof-control candidate for acceptance

Status: PREPARED_FOR_EXACT_DIFF_ACCEPTANCE. Date:19October2026, Melbourne.

The owner requested continuation towards G5.2. Its accepted G5.1 prerequisites remain unfinished. This package supplies the concrete control implementation required before actual M00 SQLite proof admission and the later D011 units. It does not close G5.1 or start G5.2.

## Exact decision object

Accept application of the twelve-path control diff from baseline `6ba0314750627ba568552b5f502d4f77428ddb4c` to candidate `1bec046d6d1a0c310bfd197de70e9a00c3d80955`, tree `91e8b3ad2d2119360b87a510f3dcbe59737e4b58`, branch `work/v2-sqlite-control-candidate-20261019`, for provisional control use and subsequent separately adequate M00 proof admission. The exact patch is `SQLITE_CONTROL_DIFF_20261019.patch`, SHA256 `74edd8eff5e9b2404a3279a113c9cf69e1a3882946e9aca9e4bcb89e7f05ed7a`. The full candidate commits are retained on that branch in this repository; the active working tree has documentary handoff changes only. Main remains `77d82bd8ee4268673715fe7e5653b6a65a299b54`.

This is the concrete-diff acceptance already required by root ExecPlan §4 and incorporated version2 brief §10: “The concrete implementation diff and its proof admission must be reviewable and accepted before application.” The exact version3 brief and its four projection intents are already accepted; their acceptance is not being requested again. Applying these controls is distinct from final control acceptance, which still needs actual M00 SQLite regression and the remaining independent decision/bootstrap evidence.

## Bounded changes

| Path | Purpose |
| --- | --- |
| `config/product_proof/claims.json` | Exact accepted three-claim catalogue; historical PostgreSQL evidence, new raw SQLite claim and separate foundation claim. |
| `config/product_proof/raw_signal_sqlite/admission.json` | Initial null pointer, explicitly incomplete. |
| `config/product_proof/market_measurement/admission.json` | Initial null pointer, explicitly incomplete. |
| `config/proof/test_families.yaml` | Add only AK-INGRESS001/002 to existing proof_control binding; retain11physical families and block membership. |
| `schemas/product_proof_claims.schema.json` | Closed catalogue/profile fields. |
| `schemas/accepted_brief_product_proof.schema.json` | Closed accepted contract/family/target-intent fields. |
| `schemas/product_proof_admission.schema.json` | Closed pointer/generation/reference/file-row fields. |
| `tools/product_proof_claims.py` | Exact authority/companion bytes, current target/allocation, complete physical path/support partition, generation hashes/chain and retained admission-history progression. |
| `tools/product_proof_outcomes.py` | Actual collection and setup/call/teardown observation; fresh atomic report, strict complete outcomes. |
| `tools/validate_product_proof.py` | Keep legacy BICP/IRB/route/tier/predecessor checks; add explicit selected-claim validation and truthful pending states. |
| `tools/run_product_proof_gate.py` | Registry-derived exact selection, active target, clean start, nonce/report completeness, zero skip/xfail/xpass and governed pre/post hashes; default raw SQLite; explicit recorded historical refusal. |
| `tests/architecture/test_proof_control.py` | Existing3tests retained, authority-derived control witnesses and temporary isolated canaries;41cases in this family. |

The six historical raw tests and87M01tests remain unchanged. No new physical product test, actual admitted generation, owner allocation, M00/A00 production change, provider operation or D011 calculation is included. Temporary synthetic sixteen-function raw fixtures exist only in disposable control tests: they prove runner enforcement and are never actual product admission or product success.

## Execution evidence

`CONTROL_EXECUTION_20261019.log` preserves the actual initial RED, intermediate failure/diagnosis outputs, repair RED/GREEN, final full suite/promotion and inherited lint output in one portable evidence file. Earlier failed checks remain failures, with their narrower subsequent repair results stated below.

Pinned interpreter/dependencies are the previously proved CPython3.12.14 profiles. The explicit optional-client compatibility environment supplies retained architecture imports; no database server is started.

- RED checkpoint `a75d2be`:25control cases collected,22failed at an explicit missing-resolver assertion and all3original tests passed. This was behavioural missing-capability evidence, after environment/import prerequisites; no import/collection error was called RED.
- First mechanics reached25/25. Further independently derived witnesses exposed4integrity omissions: preserved legacy control/test bytes, undeclared support helper and retained-generation rollback; all were corrected against their RED witnesses. The empty-reason XPASS canary also failed as required before its correction: presence of `wasxfail`, rather than its truthiness, now determines rejection.
- Reviewed candidate `9b53f9333281c938b9e7ea383c4386029a38e6e4` passed38control cases,109architecture/bootstrap tests and clean registry-derived architecture promotion. Both real product pointers remained null; raw runner refused with exit4, foundation was AWAITING_TARGET and old claim HISTORICAL_NOT_RUNNABLE.
- The post-review repair described below passes112architecture/bootstrap tests, including41control cases, with no failing/skipped/xfailed/xpassed required architecture proof. All4control tools pass mypy; all5changed Python files pass scoped Ruff. Full-tree Ruff still reports exactly the2inherited E501 findings in `_financial_policy.py:58` and `test_m01_stage1_semantics.py:1932`; those files match the baseline. No lint suppression or adjacent repair is included.
- Final clean registry-derived architecture promotion on `1bec046` exits0 with112passing tests,11physical families and zero dependency/public-seam violations. Actual version3 authority validation exits0 with the exact four intents; candidate resolution still makes no allocation. Both real product pointers remain null.

## Independent review and repair disposition

Reviewer `/root/sqlite_control_review` inspected all12changed paths and their authority/semantic lineage. Direct independent sequences bypassed worker fixture bundling: actual null pointer→runner exit4; disposable valid generation→changed family→hash rejection; raw generation carrying foundation claim→claim rejection; exit0 report carrying skipped call→exit1. Review of `9b53f93` returned an Important RECURRENT_CLASS admission-history finding and a Minor missing historical-reason finding; no Critical finding was established.

The important finding was valid: after revocation, restoring the exact old generation pointer returned READY_FOR_PROOF. The earlier retained-file rollback check did not establish monotonic admission history. Repair witnesses covered both uncommitted and committed reinstatement, with2failures observed; the lawful fresh-generation successor passed. The resolver now reads retained Git admission transitions plus current pointer bytes, checks referenced historical bytes and demands an advancing predecessor chain after revocation. All3witnesses then pass. This also prevents committing a counterfeit transition from laundering old admission.

The missing historical reason is repaired as an explicit contract requirement: the runner previously emitted a generic target-readiness failure despite a specific accepted catalogue reason. The direct historical-run assertion first failed, then the runner was changed to print the recorded reason and exit4. Treating this as a required correction avoids presenting a superseded PostgreSQL claim as an unexplained environment/target failure; it adds only that bounded refusal output.

Both repairs are in `1bec046`, with authority-derived RED→GREEN evidence and the112-test full suite. The final repaired candidate has not been independently re-reviewed; no such result is claimed. The independent findings and author verification remain separate evidence. No final control, G5.1 or pilot acceptance follows from a provisional control review or temporary canary green.

## Remaining order after exact diff acceptance

Apply only the accepted twelve-path diff, retain its provenance and validate the resulting actual candidate. Author/review/admit the four actual M00 SQLite proof families/support; run intended missing-storage RED; implement the bounded M00/A00 adapter/codec/exception/construction changes; obtain the actual full M00 SQLite aggregate and required regression. Then complete the independent control/M00 decision and lawful foundation bootstrap/reader admission needed to close G5.1. Only then author/review/admit and execute the four ordered G5.2 D011 units. G5.3/G6, source acquisition, populated-state migration, retirement and main merge remain outside current authority.
