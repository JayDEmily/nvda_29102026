# Independent D014 generation2 authored-proof adequacy

Disposition: PASS_FOR_AUTHORED_PROOF_ADMISSION_GENERATION_2.
Reference: independent-review/g61-d014-proof-gen2/96086e4/20261020.
Reviewer: /root/d014_proof_review_v2; independent judgement, no implementation or shared edits.

## Exact subject and authority

Verified clean HEAD96086e437cd8081e8617aef9324a4b0ee27784d7/tree834e0090acf3c4ce2d3ae4450a737d1a413dbbd3 in /workspace/scratch/d549b6d808a9/resume-20261020-ejayrse7/repository.

| Physical source | SHA256 |
| --- | --- |
| test_raw_ratio.py | 7e26d16d59ac42ac456e631e2acb8a5bee204e937550d5667f6bc580ba99f836 |
| _support.py | 49c6149d1ff64e002154b275bc9c54793cf60623bb0c9878c0fd5539fbc058e6 |
| typing/valid_seam.py | 3d1e2ac2449fc13be7db8f0e26c2b505dee5e6810d591dd190d4044bf859dacc |
| typing/invalid_seam.py | 84b2806f0c8be162321c35f792f987550a3cf2ff428d37edd007042fcc699fc9 |

Accepted brief SHA c23ea315c94b478c568f105e94891a03af62393792a1478c33027a0371738bb8 and contract SHA54850f780c4442924e2d28ed319ae5f0fb109e291b367391ac0a4c86190294fc reverified unchanged. GUARDRAILS/fullAGENTS/tests override reread; current root latest repair/first-stop/frontier/admission entries inspected, with unchanged accepted section7.3 governing. Accepted brief/contract and the exact current diff89dc128..96086e4 were inspected directly. Initial/previous D014 review, duplicate/schema repair lineage, operation-scope ruling, D0127eaddf9 and D0133876ad0 analysis from the prior complete review remain applicable to unchanged bytes; this new verdict is not inferred from their prior PASS labels.

Previous review independent-review/g61-d014-authored-proof-v2/ec0f363/20261020, reportSHA0374311fc92ee0cc8fcbf16f0b02558b4ee37e166ded73622053a1f7b396e6af, reviewed gen1 physicaltest588abd5c.... Current gen1f531b7216a3ce1e468015b40d6d3ca01742b56eb09587e49a972d41f33a47b23 and pointer remain byte-identical to genuine admission6543a576. They still reference old physical bytes: this review does not admit the current changed test, modify the pointer or treat current resolver readiness as already established. Every production source byte is identical to0d3600c, independently verified with git diff; no production repair is bundled into this proof change.

## Observed first failure and diagnosis

Read complete first-failure ruling, serial executed harness, readiness/mypy/P01–P04 metadata, mypy output, full first traceback and four-case footer; independently parsed the entire1198-line P01–P04 log and reverified all three raw log hashes against metadata. Actual preserved candidate0d3600c passed native readiness and source/control typing38files, then P01–P04 collected173 and returned4failed169passed33.11s. Exactly four IndexErrors at original physical415 occur for repeated-cursor/page-cap x empty/populated. Each traceback has native page items=() and kwargs cursor='1'. Harness exits at the first failed invariant, before P05/P06/full strict. These are attributed historical observations, not reruns by this reviewer and not202-success evidence.

Direct primary M00 public list_projected_raw_history source1816–1885 interprets a numeric cursor as an offset and slices projected[offset:offset+limit]. With one bid projection, offset1 is empty. Original adapter delegated every fabricated next cursor to that finite native sequence before indexing page.items[0], so it raised before emitting its intended repeated/infinite fault. Complete unchanged _selection.py confirms that it calls the public reader, rejects malformed/repeated/empty-nonterminal cursors and refuses exhausted policy caps; it does not need to swallow fixture IndexError. No production defect is diagnosed by this log.

Classification of the observed proof inadequacy: Important / ISOLATED. Mechanism is incompatible protocol composition: a synthetic continuation token was erroneously used as the finite producer's native offset, destroying the generator's own precondition. Prior F001 was absent independent duplicate order/page/native-representation discriminators; F002 was declaration-versus-current-row constraint evidence; prior D013/D014 scope findings promoted an operation-specific rule to a generic invariant. None is the same seed/continuation precondition mechanism. Calling every insufficient test recurrent would erase those materially different invariants. This does not justify repairing only the latest witness: class-level closure within this isolated mechanism must cover all four synthetic-cursor modes, not only the two that happened to reach offset1.

## Revised source adequacy

The source now obtains a real R033 projection using actual public project_raw_value with exact ID/mapping after the ordinary explicit raw admissions. This is a literal/public input seed only, not a materialised result, expected-answer helper or hidden retry. It is captured only for the four synthetic modes. The active R033 synthetic branch occurs before native history delegation and asserts the seed's exact ProjectedRawValueV1 type, then emits an exact public ProjectedRawHistoryPageV1. Nonactive initial population and other R IDs/modes continue through actual M00 history.

All four fault meanings remain independently discriminated:

| Mode | Generated protocol | Owning refusal |
| --- | --- | --- |
| cursor | Nonempty real-seeded page, next='bad' | malformed cursor |
| repeated-cursor | Nonempty seeded page, next='1' on every response | repeated continuation |
| empty-cursor | Empty items with nonterminal next | empty nonterminal page |
| page-cap | Nonempty seeded pages, increasing numeric next forever | policy1000-page exhaustion |

Because generated responses no longer index a native offset page, repeated and capped streams can actually reach their intended reader-protocol condition. No production exception catch, skip, None/history weakening, special result or lowered cap is introduced. Former unreachable generator block is removed rather than leaving a second competing path. This is source-level closure of the identified precondition defect, not observed repaired-case GREEN.

Independent protocol_probe.py uses its own plain dataclass/token/consumer model, not project types, extracted functions or authored helpers. It independently reproduces IndexError from one-record offset1, then demonstrates that separately seeded malformed/repeated/empty/infinite streams reach their respective protocol conditions without native-offset delegation. Its model counts1/2/1/1000 describe the documentary consumer only: they are not restored generic public total-call assertions or actual product traces.

AST comparison confirms every other test/helper function is unchanged from the exact prior reviewed source, selection test decorators remain identical, and the full request mutation/materialise/None/immediate history/getter tail after Reader is unchanged. Six mandatory names,50refusal+7positive+16duplicate labels under empty/nonempty history,14arithmetic,11identity,28storage and1typing still source-project202 cases. No new collection was run.

Previous F001 Important RECURRENT_CLASS closure is preserved: full provider/representation/stale/receipt x reverse/forward x same/crosspage duplicate grid, identical crosspage positive and immediate histories remain. Previous F002 Important ISOLATED closure is preserved: exact PK ordinals/FK/CHECK/native invalid-kind and five full-row/trigger/profile-preserving valid downgrade modes remain. The new patch does not touch any of these. Prior operation-scope ruling is upheld: policy cap/refusal remains, without an unsupported generic total-call budget; actual noninitial-cursor M00 positive/result remains. All actual first-INSERT/native fault/fresh readonly writer-exit recovery/integrity/equation and independent asymmetric version dimensions are unchanged authored assertions, not newly executed results.

Literal support remains unchanged and does not materialise/retry/calculate an answer. P01 actual public absence→admit→projection→materialise sequence remains explicit rather than fixture-composed. At this review stage no changed authored module can lawfully be executed before immutable gen2 admission; fixture independence is assessed by decomposition against the public source and the independent documentary protocol model, not falsely claimed as an actual new public runtime observation. The later implementation reviewer must still directly exercise required public ordering under lawful admission.

Static specimens are byte-identical: positive exact public types remain source-compatible, not newly run mypy. Negative sites remain18/19/20/21/22assignment,23attr-defined,24/25arg-type,26/27assignment: exactly seven assignment/one attr-defined/two arg-type errors,10total with exact line/code set enforced by the unchanged harness. No import/Any error is admitted as substitute. This review does not use prior source/control38mypy success as evidence that the specimen P06 has executed.

## Actual reviewer validation and limits

Fresh commands, all exit0, pinned CPython3.12.14 with shell/bin/bash loginfalse:

- static_review.py: compile-only four sources; exact physical/authority hashes; six names/202 projected cases/10 sites; unchanged nonselection ASTs and refusal tail; early synthetic return; unchanged production0d3600c/gen1/pointer; preserved log hashes/four-exception protocol observations.
- protocol_probe.py: independent finite model described above; no project/authored import or execution.
- python -m ruff check tests/product/market_measurement_d014: All checks passed!

Using verification-before-completion required these fresh bounded checks and narrow claims. It did not authorise changed product execution. Output is explicitly transcribed in STATIC_RESULTS.md, not purported original stdout bytes.

No remaining source-adequacy finding within this bounded repair. The observed Important/ISOLATED adapter-precondition defect is CLOSED AT AUTHORED-SOURCE ADEQUACY ONLY. No admission, repaired product pytest/collection/mypy/specimen/aggregate, source fix, shared write, new worktree, protected-process or network operation occurred. No P05/P06/full202 runtime success or implementation acceptance is inferred.

This candidate may proceed to concrete delegated immutable generation2 admission linking preserved gen1, then actual replay of the four prior failures and complete173 before the previously unreached28P05/P06/full strict obligations. First failure and gen1/source history remain preserved. No in-place reseal or direct unadmitted workaround is authorised. Standing22:28 supplies human-checkpoint delegation only; no routine owner prompt is missing. G6.1/native/full126/latergate/provider/live/composition/migration/retirement/main acceptance remain outside this verdict.
