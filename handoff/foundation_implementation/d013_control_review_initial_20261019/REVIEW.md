# Independent D013 pre-application control review

Disposition: RETURN. Reference independent-review/g61-d013-control/3ea87b2/20261019. No shared repository writes; no acceptance or application to the active candidate.

## Exact scope

Reviewed candidate 3ea87b243fc330eee14b47d8b9c56405c55dac59 on work/v2-g53-review-20261019. Reviewed exact unapplied handoff/foundation_implementation/G6_1_D013_CONTROL_CANDIDATE_20261019.patch SHA256 7c56924cafef9491abb8e2d39bb3930c037131c2d8b0058ceb95431158749519. Applied with apply_patch only to disposable copies, relocating solely its tools/product_proof_claims.py destination. Stable patched loader SHA256 eb622b799454e2c2462a1ea251cfdf061bf2dd15f0ae3470f17ab1e98e96b93f; original loader SHA256 656094bca1603e8c650d6ddfdd62a72e868dfb7e695d794696792cb18067ba1e. Git diff 5a7bcfe..3ea87b2 confirms original loader unchanged from accepted D012 source.

Read governing GUARDRAILS.md, root/test-local agent instructions, current root plan/latest progress and complete in-scope §7.2 semantics, exact D013 brief/contract/native binding/design receipt, D012 brief/control review and loader/tests/strict runner/outcome/schema controls. Exact D013 brief SHA256 1f53d9c21c6eb4b90213137c4699a0688f994cd0ed55e54082268d8477abc148; contract SHA256 7eab93055c2e2f19e74563ec9588bbc04dfdb8664d4c8e3279527f70917d4a47. Delegated design/brief/root disposition is recorded independently of this review under owner-chat/20261019T222804/D012-and-standing-human-exceptions. A review receipt cannot imply domain implementation authority or runtime proof.

## F001 — Important, RECURRENT_CLASS: current checkpoint becomes a permanent live-pointer invariant

Location: tests/architecture/test_proof_control.py:test_d013_actual_original_claim_generations_are_preserved (lines 93–111 in reviewed bytes). The test reads live selected claim resolution and asserts exact current generation hashes for all three original claims. This correctly observes preservation at this exact checkpoint, but as a durable generic architecture test it forbids a separately lawful later generation advance even when every old immutable generation byte remains unchanged. Immutable-history preservation and eternal current-pointer equality are different propositions.

Independent direct discriminator (pointer_transition_probe.py; no Worker fixture): in the disposable actual accepted D012 universe, retain gen1 and its exact file/support hashes; add a synthetic gen2 with previous_generation=gen1 and fresh explicit canary review/admission refs; update only the canary pointer. The unchanged public loader validates admission history and returns READY_FOR_PROOF, generation 3be0c2d7ad18f9a4bdf13046d8cbe60874e6246ff8ec1345d9bc902689dbe80f. Calling only the reviewed new test function raises AssertionError. The script restores the original pointer and removes the synthetic generation. This is admission-control canary evidence, not an actual human admission, domain proof, or execution of D013 behaviour.

Semantic lineage inspected: bd787fb moved pre-admission assumptions into explicit disposable state; its actual-state test still pinned foundation incompleteness. cc89069 repaired that assertion after lawful physical generation admission; 5a3e178 repaired its bootstrap assertion after lawful activation. Current hardcoded live generation selection repeats the checkpoint-as-invariant mechanism. Also inspected 9b53f93 → 7289806 undeclared-support/orphan repair lineage and current 13 negative controls' positive readiness guard, which prevents unknown-claim vacuity. Those orphan/vacuity controls show no new defect here.

Required class-level proposition: generic control proof must preserve and validate immutable old generation content and correct claim association without treating one checkpoint's current pointer/status/count as permanent law. Separately lawful advancement must remain admissible while revoked/reused/forged or mismatched generation transitions still reject. Current exact-unit preservation remains reportable evidence. Closure must distinguish these cases across all three original claims; no specific implementation patch is prescribed.

## F002 — Minor, ISOLATED: exact loader patch fails mandatory scoped lint

Pinned command: /workspace/scratch/d549b6d808a9/g52-dev/bin/python -m ruff check tools/product_proof_claims.py tests/architecture/test_proof_control.py. Actual exit 1: tools/product_proof_claims.py:426:101 E501, line length 106 > 100, generated binding_path f-string. One finding, exact output in lint.log. This is new control-path formatting, not either inherited M01 E501 finding. Required proposition: the exact proposed changed control scope passes its mandatory lint without changing authority/semantics or unrelated files.

## Verified control observations

- Exact patched targeted command /workspace/scratch/d549b6d808a9/g52-dev/bin/python -m pytest tests/architecture/test_proof_control.py -k d013: 23 passed, 62 deselected, 42.10s, exit 0. Its strict synthetic success/skip/governed-mutation cases prove exits 0/1/6, not domain arithmetic.
- Independent stable full-family rerun in stable-repository: same pinned interpreter -m pytest tests/architecture/test_proof_control.py: 85 passed, 104.62s, exit 0.
- Scoped four-tool mypy command from root plan: Success: no issues found in 4 source files, exit 0.
- Native D013 binding validation: PASS exact brief digest; candidate_targets modify:M02, modify:G01; exit 0.
- Direct script bypasses all Worker copy/generation fixtures. Actual D012 test_spread.py exists; actual D013 physical/config roots are absent. All three actual original claims start READY_FOR_PROOF, retaining generations: M00 SQLite 51e87129c2a31c71599b7a01beb8ba39717ed5118a4d5c849bcb2015b6c80c6f; foundation 24a5af4054c277b01a140ec43481e86851e5e76263826644a80993c12c2495b7; D012 26d2b4e371c38b0960cb6081798cc618c9f308567d0df12b2aa40f3777dd2a25.
- Introduce separately only _support.py, nested/helper.py, test_orphan.py, dangling.py symlink under the descriptor-absent exact D013 root: each of the three original selected claims rejects every case with unowned D013 extension Python source without descriptor. Restore between witnesses; actual original generations remain equal.
- Add exact D013 descriptor/null admission but no physical product source: original claims remain READY unchanged; new claim uses its own exact D013 authority and is INCOMPLETE_NO_PHYSICAL_FAMILIES with no generation. Add extra descriptor key: all four selected claims reject. Restore descriptor; bind new authority to D012's different brief digest: all four reject exact brief-byte mismatch. Restore all canaries; original baseline is identical.
- Literal fixed D012/D013 resolver factorisation preserves _authority/runner/outcomes/schema meanings. Complete combined contract partition, family/proof ownership and per-extension _generation validation occur before selected-claim return. Exact eight/eleven incorporated-row checks remain fixed by identity, not arbitrary discovery.
- Stable copy comparison: 205 in-scope source/config/authority/schema/product-proof files byte-identical with actual shared original; only tools/product_proof_claims.py differs in stable Git status.

## Review process limitation and preserved first results

An initial full-family run in repository overlapped this reviewer's deliberate direct mutation canaries and produced 18 failed/67 passed, exit 1, 93.70s. It is contaminated reviewer execution and is not attributed to the candidate or used for disposition. A fresh separate stable-repository was copied from the unchanged actual candidate, exact patch applied, no direct mutations performed there, and its full 85-case run passed. The actual negative F001 discriminator was run directly and separately; F002 was reproduced against the stable copy.

No actual D013 domain test/source/proof/generation was created or executed; no active source/config/proof was edited. No product aggregate or architecture promotion/source-wide mypy was run for this pre-application review; these remain ordered post-application requirements. No full126/G6.1/native/source/live/composition/migration/retirement/main admission follows. Current synthetic canaries cannot establish domain correctness. RETURN requires bounded proof/control repair and exact revised pre-application review, not a new unspecified domain authority.

## Evidence files

Fresh scratch directory /workspace/scratch/d549b6d808a9/d013-review-9IMqxv contains this REVIEW.md, direct_review.py/.log, pointer_transition_probe.py/.log, targeted_review.log (recorded command/outcome summary), full_review.log (recorded command/outcome summary), lint.log (exact output), static_and_preservation.log. Stable full-family working copy is stable-repository; direct adversarial copy is repository. Exact script/log hashes are supplied separately with handoff. All generation/descriptor writes described above are disposable canaries only.

