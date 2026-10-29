# D014 bounded preapplication diagnostic followup

Disposition: BLOCKED_UNSAFE_REVIEW_STATE. No preapplication PASS or candidate-loader defect is established by this followup.

Reference: independent-review/g61-d014-control-followup/641bdfd/20261019.
Reviewer: /root/g61_d014_control_review. One bounded diagnostic only; no subagents, suite reruns, shared writes, cleanup after failure, or domain work.

## Exact scope and provenance

The initial BLOCKED report remains historical evidence, not overwritten or retrospectively relabelled. This followup addresses its one remaining sequence distinction: literal descriptor installation → null incomplete new claim with all four old claims ready → descriptor removal → four separate orphan variants through all five selections → cleanup and four-original readiness baselines.

Fresh private clone `candidate` starts at 641bdfd7993bde601c4ea2fa106c5335305a5f5d, tree4e2ba963816bbbf8ce858b70b80a1bd74fbfd975. The exact previously reviewed patch08ea24676070b2998e719243ad00a953d7ab8242a56aa77ecfd3012494e5ec0e was applied only to this private clone. Proposed module SHA256 remains b2670e26f51d4b6f4fc8c656c859b9e5d63ca9aadd84ff2f818ff06cd9bb118a; active module remains4720fb69f9d6b34032742ce47585b57f1be3610305061faf2ac9d1458c66c478. Test hash e038ed1eca2847b8ed79495ea19b9e2cdaf4a3b3cdfdbb01c15f07111c45de44 and brief hash c23ea315c94b478c568f105e94891a03af62393792a1478c33027a0371738bb8 also match the initial review.

Read-only Git comparison c990f8b..641bdfd across src/tools/config/schemas/tests/implementation-authority/handoff-authority returns empty/exit0: the intervening review preservation did not change these scopes. An initial attempt ran that Git comparison from the nonrepository parent directory and printed Git usage; it is not evidence of an empty diff. The corrected `git -C candidate diff --exit-code ...` is the actual successful comparison.

The executed exact_sequence.py was saved before execution, SHA2568cca9ad3b347d2ecaccea6c6b048e85a85e30d648b6aef88a3fba48a701a7274. Its before/after hashes are identical. Unlike the initial v1 script, these actual executed bytes are retained unchanged, not reconstructed. run_once.py SHA256ae2ceafe2b7a526320e5b6ad6324320d6115a606957d9eceaba576c9dccff3d7 writes invocation_before.json before starting the child, preserves merged stdout/stderr directly in binary mode, then records actual process status and hashes in invocation_after.json.

Exact invocation: `/workspace/scratch/d549b6d808a9/g52-dev/bin/python /workspace/scratch/d549b6d808a9/d014-followup-n3toOACB/exact_sequence.py`, cwd `/workspace/scratch/d549b6d808a9/d014-followup-n3toOACB`.

## Observed result and first unmet invariant

Process exit1. The diagnostic stops at selected call40, `cleanup-original/test_orphan.py`, claim `neutral_market_measurement_truth_d013`. It does not execute the fourth/dangling witness or anything downstream after that failure.

The script captures the resolved imported module path and exact hash, complete D014 config/physical inventory, and verifies183 original product-proof/physical-test/implementation-authority/handoff-authority file digests before and after every selected call. It prints the complete original manifest initially. Manifest SHA25656712c8069232679394a3e39453de01dadf7722d62de4b0dd4faec9654a2bac8 remains unchanged; all183 protected original files and the proposed module remain unchanged at the failure.

Call40 before inventory, exact paths relative to candidate:

| Path | Observed state |
| --- | --- |
| config/product_proof/market_measurement_d014/claim.json | Absent |
| config/product_proof/market_measurement_d014/admission.json |60bytes, SHA695df8981732f6da102abdb12de435e7cf0cb561d1c05b9c64f1db9704386dd9; null pointer |
| tests/product/market_measurement_d014 | Directory only |
| tests/product/market_measurement_d014/nested | Empty directory |
| Any D014 physical Python source or symlink | Absent from complete inventory |

Call40 after inventory contains the same entries plus:

| Newly observed path | State |
| --- | --- |
| tests/product/market_measurement_d014/.rsync-tmp | Directory |
| tests/product/market_measurement_d014/.rsync-tmp/test_orphan.py |64bytes, SHA0df1e6df0ea848c41bad608fec6c255333c771c4a32e82347fc93c8f4b992cba |

The returned observation is ValueError `unowned D014 extension Python source without descriptor`, result null. The inventory comparison then raises `AssertionError: ('read-side state mutation', 'cleanup-original/test_orphan.py', 'neutral_market_measurement_truth_d013')` at exact_sequence.py line84, invoked by line109. The `.rsync-tmp` file's bytes/hash equal the earlier literal `test_orphan.py` witness recorded before call32.

Both inventories resolve the exact same module path `/workspace/scratch/d549b6d808a9/d014-followup-n3toOACB/candidate/tools/product_proof_claims.py` and exact proposed hash b2670e26.... Thus wrong-module ambiguity and script-version ambiguity do not account for this particular observation. A later read-only Git status shows the original `tests/product/market_measurement_d014/test_orphan.py` path reappeared as untracked, along with the intended null pointer and patched private loader. No cleanup was performed after failure; affected private root remains for inspection.

At the parent's explicit request, one final read-only sha256sum/od inspection of the reappeared original path safely establishes its current64 bytes and the same SHA0df1e6df... as the logged temporary-path entry. Exact retained hexadecimal bytes:

```text
23 20 54 65 6d 70 6f 72 61 72 79 20 6c 69 74 65
72 61 6c 20 6f 77 6e 65 72 73 68 69 70 20 63 6f
6e 74 72 6f 6c 20 6f 6e 6c 79 2c 20 6e 65 76 65
72 20 64 6f 6d 61 69 6e 20 70 72 6f 6f 66 2e 0a
```

These decode to `# Temporary literal ownership control only, never domain proof.` followed by LF. No candidate write, cleanup, process inspection, escalation or further diagnostic was performed by this reviewer after the stop; only report finalisation and this explicitly requested nonmutating witness-byte preservation.

## What this establishes—and what it does not

VERIFIED: the selected call is bracketed by different physical proof-jurisdiction inventories, while the original protected bytes and module digest remain stable. The script explicitly unlinks each original witness and verifies its absence before cleanup calls; it contains no creation of `.rsync-tmp`, no directory synchronisation command, and no creation of any new witness during call40. Its intended write scope is the exact descriptor/null pointer and each one literal orphan path, with explicit unlink between stages. The static loader is the same four-line proposal previously reviewed; no source repair was introduced.

UNKNOWN: which process, filesystem service, synchronisation mechanism, tool runtime, or other actor introduced the new entry, and whether that same mechanism caused either initial contradictory log. The name `.rsync-tmp` is an observation, not proof that a particular rsync process acted. The before/after snapshots do not identify a writer or establish an exact interleaving within the loader. The observed rejection is consistent with a newly present unowned Python file; this is not evidence that the loader rejected a stable clean physical universe incorrectly. A loader-caused write is also not established merely because the change was observed across its call.

The required first missing invariant is a stable, trustworthy physical proof universe during this bounded sequential read-side review. The diagnostic therefore supplies a more discriminating unsafe-review-state blocker, not sufficient verified evidence for preapplication PASS. This is not a missing routine human approval, nor would another approval alone establish state integrity. No candidate code-patch prescription or open-ended canary programme follows.

## Verified partial sequence and remaining boundary

Before call40 the instrumented sequence establishes four-original READY baseline; installation of the exact literal descriptor/null admission while all four original claims remain READY; new claim INCOMPLETE_NO_PHYSICAL_FAMILIES; descriptor removal and four-original READY; support/nested/test orphan rejection through all five selections; and successful cleanup baselines until the final D013 call of the third witness. These are partial verified observations, not completion of the full49-call sequence. Dangling-stage execution was not reached.

Prior complete130/38 control, static/native,44 isolated cases and earlier descriptor-absent clean20 sequence remain separately attributed in the initial report. None is rerun or relabelled here. The known phase/scope proof correction remains authority-supported RECURRENT_CLASS as previously analysed; this newly evidenced state-integrity blocker has no diagnosed candidate defect mechanism, so no speculative ISOLATED/RECURRENT_CLASS Worker repair is routed.

Exact merged log SHA2560f9971370603da9a6dd6371e6121a59e330e34c0aa0d4afba56fdf328c073e80. The retained log includes the full initial183-file manifest, every before/after inventory/result/error through call40, and traceback. invocation_before.json and invocation_after.json retain actual command/preexecution provenance/exit/hash. No log text normalisation, original-file overwrite, extra diagnostic run, active loader application, delegated acceptance, domain proof/generation/runtime, provider/API/SDK operation, or G6.1 completion is claimed.
