# Independent post-installation review

**Verdict: ACCEPT_EXACT_DOCUMENTARY_INSTALLATION. No important installation finding remains open.**

Final reviewed and remotely fetched commit: `1138f44436d08010f7b34adb9eea9a2eaff2759f`, tree `a3663a1698699786b9b55032c2d1fc522b14ebc2`, branch `work/astra-adr-recovery-qualification-20261115`. Original installation commit `28cad2d958aa4356925aaa2ecc258c95529598f2` remains its ancestor. Published main remains `02a19ae02678824908568d8db08f0e1d015cb861`.

Read frozen GUARDRAILS in full, installed AGENTS/test override and EXEC_PLAN, owner installation authority, installation receipt/verification and predecessor identity inventory. This review checks the exact installed result of the previously reviewed package; it does not repeat the prior semantic review, recovery checks or SQLite probes.

## Verified installation and preservation

Independently compared actual Git bytes, current working bytes and immutable source at `a28702cde241b3f833b51071aac8cb41591b37dd`. All five installed targets exactly equal their corresponding approved `PROPOSED_*` source blobs: root AGENTS, root EXEC_PLAN, tests/AGENTS.override, current execution register and current test-evidence ledger. The source proposal files themselves are unchanged.

Relative to pre-installation checkpoint `f8fcb10af147eb7a50217e9712a012b9558a868d`, these are the only modified existing paths. Additional final-tree paths are confined to continuation handoff evidence and predecessor archives. Frozen GUARDRAILS, product source, product tests, configuration, tools, vendored dependencies, Python/lock/build and CI configuration are byte-identical to accepted main. The authorised test-local override is the sole change beneath tests/. No admission, generation, pointer or historical product proof was changed.

All five predecessor archives independently match their actual pre-installation Git bytes, original blob identities and SHA256 metadata. The old AGENTS gzip decompresses to exactly the original bytes and to the raw archive retained in commit28cad2. Its compressed hash also matches. The earlier raw archive is DO_NOT_CARRY_FORWARD in the final active tree; it remains recoverable from ordinary Git history. Gzip packaging therefore resolves the archive EOF-whitespace issue without changing original evidence bytes. Full endpoint `git diff --check` passes.

The installed register retains39 leaves; the ledger retains35 proof obligations. Every authorised case count is zero, every admitted-case list is empty and every execution-run list is empty. D145 is `M02-C28-D145`, scheduled at paused L31 with BLOCKED semantic status, zero ceiling and no cases/runs. Installation supplies no product release.

Fetched exact final commit from the published branch into the already independently checked receiver and compared its complete tracked listing to the local pinned commit. Head/tree/listing match; working tree was clean at verification. Main remote identity is unchanged. No recovery test, runtime mechanism or product test was rerun.

## Authority and remaining boundary

The committed owner authority and installation receipt explicitly install the exact five source blobs on this working branch. They explain inherited PROPOSAL/NOT_ACTIVE drafting labels without silently editing the approved source. Main has not installed or merged this set. This acceptance covers exact documentary installation, including retained history and archive packaging.

A separate product commission, source/policy/admission decisions, profile-specific runtime qualification, runner bindings and designated independent strict product Tester remain required where applicable. Historical asset gaps remain as previously reported. No G1–G5 product acceptance, PostgreSQL operation, main merge or D145 reactivation follows from this verdict.

Independent command/identity evidence: `/tmp/astra_install_checks.json`.
