# L14 independent tester handoff — prepared, NOT EXECUTED

29 October 2026 UTC. All mandatory source/proof authorship leaves L02–L12 are IMPLEMENTED_UNTESTED; L13 is DOCUMENTARY_DISPOSITION with D145 capability BLOCKED/PAUSED. G5/L14 has no product/static/runtime results or independent acceptance yet. This document and its inventories are implementation-thread preparation only. They do not certify semantic adequacy, test collection, environment readiness or programme completion.

## Required thread and transfer boundary

The accepted root EXEC_PLAN.md status explicitly requires “manual iPhone transfer of the latest **cumulative additive Git bundle** between implementation and independent tester threads, with GitHub/Codex excluded.” Section5 assigns “Independent tester thread — L14 only.” Section4/L14 requires restoring the identical fixed full-history baseline plus the most recent additive in that independent thread. Therefore an internal worker/subagent run here cannot stand in for the required transfer/sole executor. No new implementation permission is needed; the remaining prerequisite is the owner's manual transfer and that tester's verified intake.

Use only the latest final handoff additive bundle announced with this document; intermediate L01–L13 downloads are unnecessary. Its external receipt supplies exact final candidate HEAD/tree/ref tips/SHA256, because a bundle cannot embed its own final checksum. Source checkpoint before these handoff-only documents is `ffdc1150cb472550d23952751f931c414fd5ee31`; all Python/authority/proof bytes remain those of that commit. Run future proofs against the final restored handoff HEAD, recording its full SHA, not an inferred predecessor SHA.

Fixed baseline: `97f944d51ab9e403250fe76910e2754b50425c73`. Full original ref inventory and baseline archive/bundle SHA256 are in ../TRANSFER_BASELINE.md and SOURCE_AND_ASSET_INVENTORY.json. Independent tester possession is UNCONFIRMED. The contained full-history bundle SHA256 is `91db4a1989bff366c1f547c5776ca886c276b6b1310027ae929aa1cd1efee4b9`; it is a one-time prerequisite, not inside the latest additive. All authoritative frozen input/oracle/profile/proof files and pinned dependency wheels are tracked. Exact wheel hashes are in the asset inventory. The CPython runtime itself is external and unqualified here; identify/hash it independently before execution. The attached PY313 wheelhouse is not a substitute. No PostgreSQL server is required or authorised.

## Copy-ready instruction for the independent tester thread

> Act as the independent sole L14 semantic reviewer and strict proof executor for the accepted root downstream reconciliation R2 plan. Restore and verify the original L00 full-history baseline97f944d51ab9e403250fe76910e2754b50425c73 plus the latest cumulative additive attached here. Read GUARDRAILS.md, scoped AGENTS, root EXEC_PLAN.md, L01 authority and handoff/downstream_reconciliation/L14/INDEPENDENT_TESTER_HANDOFF.md in full where governing. Verify receiver baseline/ref/object/tree/inventory and environment before product work. Inspect each mandatory owner/proof independently, including shared helpers and source/fixture/oracle/return-repair lineage. Run only the authorised scoped static/ingress checks and eleven exact native strict aggregates in dependency order, two physical cases each, preserving raw evidence and exact counts/SHA/generation. Stop dependent proofs at the first missing/failed invariant. Return bounded repair obligations to implementation, preserving failures; do not weaken tests/claims or run unrelated/broad suites. Retain old evidence when unchanged; decide precise shared-interface invalidations. Independently disposition L00/L01/L13 documentary work and I01–I08. D145 stays paused and has no product test in this phase. Commit actual evidence/dispositions, export/fresh-verify/save/expose the final cumulative additive against the same baseline. Report exact remaining partial/blocked work; no acceptance from packaging alone.

## Restore on a clean receiver

The filenames below are shell variables for the files actually transferred; set them to existing receiver paths, keeping the exact external SHA checks. Git-only mechanics are allowed before product tests.

```bash
BASE_SHA=97f944d51ab9e403250fe76910e2754b50425c73
# Verify both payload SHA256 values against the external receipts first.
git init receiver
git -C receiver fetch "$BASELINE_BUNDLE" '+refs/*:refs/*'
git -C receiver rev-parse refs/heads/work/downstream-reconciliation-20261028
git -C receiver bundle verify "$ADDITIVE_BUNDLE"
git -C receiver fetch "$ADDITIVE_BUNDLE" \
  refs/heads/work/reconciliation-oct29:refs/heads/work/reconciliation-oct29 \
  refs/heads/work/reconciliation-resumed:refs/heads/work/reconciliation-resumed
git -C receiver checkout work/reconciliation-oct29
git -C receiver merge-base --is-ancestor "$BASE_SHA" HEAD
git -C receiver fsck --full
git -C receiver status --porcelain=v1 --untracked-files=all
```

Verify all66 original refs/tips against TRANSFER_BASELINE.md; additive includes HEAD/current work/reconciliation-oct29 and retained work/reconciliation-resumed at2efb2f6031d7d86f79d1a8dbd56b466f9d4facc0. Verify current HEAD/tree and each tracked blob against final external receipt/restoration inventory. Compare all source/checksum inventories to bytes, distinguishing handoff-only files added after source checkpoint. Preserve original refs; do not force-update baseline, rewrite history or require intermediate leaf bundles. Failure stops product execution. Source-side fresh restores do not replace this receiver confirmation.

## Environment, independent review and scoped preflight

Use CPython3.12.14, pytest9.0.3, mypy1.20.1, Ruff0.15.11 and PyYAML6.0.3 from the accepted environment/pins; accepted prior SQLite evidence used3.53.1. Record actual Python executable/hash, complete versions, SQLite linked version, package identities, OS and commands. A missing required pinned runtime is an explicit environment BLOCKER; do not substitute3.13 or claim a successful qualification. Runtime qualification is permitted only now in L14, and none was run here.

Inspect governing architecture ownership/dependency/ingress law; accepted source/API/allocation plus frozen profile/recipe/oracle/provenance files; each immutable native brief/binding/claim/contract/current generation; changed production/public/storage code; test support and both physical cases independently. Inspect historical original owner proofs/returns and the L03/L04 Mapping/readback and L10 prefix-completeness source repairs. The final source inventory and generation index contain byte hashes, not schema/semantic validation results. Independently resolve every actual authority conflict before affected proofs.

Scope manifests list changed Python from baseline through source checkpoint. From the repository root, execute the following **only at L14**, recording command, candidate SHA, raw output and exit status:

```bash
mapfile -t RUFF_FILES < handoff/downstream_reconciliation/L14/RUFF_SCOPE.txt
"$NVDA_PROOF_PYTHON" -m ruff check "${RUFF_FILES[@]}"
mapfile -t MYPY_FILES < handoff/downstream_reconciliation/L14/MYPY_SCOPE.txt
PYTHONPATH=src "$NVDA_PROOF_PYTHON" -m mypy "${MYPY_FILES[@]}"
```

Mypy scope is changed production/tools; Ruff scope also covers changed tests/support. Do not suppress diagnostics or broaden to unrelated whole-repository suites. If imported legacy code causes a diagnostic, preserve the exact finding and determine its relevance; do not silently exempt it. Exact ingress for each of the11 named source/D owners uses the repository CLI:

```bash
PYTHONPATH=src "$NVDA_PROOF_PYTHON" tools/validate_implementation_authority.py \
  --binding implementation/authority/DOWNSTREAM_NATIVE_SOURCE_BINDING.yaml \
  --brief handoff/downstream_reconciliation/authority/briefs/NATIVE_SOURCE_BRIEF.md
```

Repeat that command only with the ten exact D bindings/briefs named in PRE_TEST_CLAIM_INDEX.json (D087,D131,D134,D135,D136,D138,D139,D140,D143,D137), preserving each result. Necessary public import/claim/schema/partition/generation/preflight is exercised by the unchanged strict runner and fixed loader; inspect its current path before deciding any extra scoped check. No broad architecture/promotion suite, direct pytest duplicate, collection-only probe or M00 replay is prescribed. The claim loader validates the fixed M00 Brief2 extension as a build dependency; this is not an instruction to rerun M00's37-case product proof.

## Exact native proof order and obligations

Every row has exactly **two** physical cases expected, prepared NOT_RUN. SOURCE uses test_native_source_success/test_native_source_refusal; all D rows test_native_success/test_native_refusal. Planned total:22, not observed collection or passes. Each success retains exact metadata/lineage and public read-only SQLite reopening/unchanged bytes; every refusal has no appended occurrence/history. Every D retains its two original legacy cases separately, total4 per identity under ceiling6; unchanged legacy cases are historical evidence, not automatically rerun.

| Leaf | Strict aggregate | Current generation | Owning proposition |
| --- | --- | --- | --- |
| L02 | `neutral_market_measurement_truth_native_source` | 0003 | A4 prefix → outgoing/incoming restart discovery → explicit complete freshG2; refusal reset/incomplete rewarm-up and exact unorderable tied pair. |
| L03 | `neutral_market_measurement_truth_native_d087` | 0002 | Explicit CALL1.30 and PUT2.30 with four distinct role members; missing CALL R036 plus complete stale CALL refusal, no PUT fallback. |
| L04 | `neutral_market_measurement_truth_native_d131` | 0001 | Actual native public D087 A2 and separate C1 exact permitted reference context; band0.50 yields8; separate error317 with matched predecessor time refuses. |
| L05 | `neutral_market_measurement_truth_native_d134` | 0001 | Native side1 bid5+3=8 without requiring R189; omit final R187 with other three roles visible. |
| L06 | `neutral_market_measurement_truth_native_d135` | 0001 | Native side0 ask top-two6 and actual top-one2 as distinct requests; separate error317 after complete warm-up refuses. |
| L07 | `neutral_market_measurement_truth_native_d136` | 0001 | Actual public D1348 and D1356 with exact common top-two source yield1/7; actual top-one D1352 refuses unchanged top-two request. |
| L08 | `neutral_market_measurement_truth_native_d138` | 0001 | Actual unchanged public D011100; three-level separate recipe yields bid7/2 and ask5/2; separate reset refuses. |
| L09 | `neutral_market_measurement_truth_native_d139` | 0001 | R001 collector-receipt4s bucket/native bidpositions1–2, complete pre-window prefix and inserts3/5 yield count1/2,size2; omit operation only. |
| L10 | `neutral_market_measurement_truth_native_d140` | 0001 | Actual standing6 before native size0 delete in2s bucket yields count1/2,size3; nonexistent position9 refuses all fields present. |
| L11 | `neutral_market_measurement_truth_native_d143` | 0001 | Cross-MPID bid0 insert → public intermediate shifted snapshot → delete; full both-side ALPHA6/BETA2, HHI5/8; missing final R193 with size1 visible refuses. |
| L12 | `neutral_market_measurement_truth_native_d137` | 0001 | Explicit CALL59/45 and PUT58/25 four-member quote assemblies, no D087 predecessor; missing CALL R036 with other three/PUT visible refuses. |

Run each exact aggregate separately in the order above, with raw logs outside the repository so the gate's clean-tree guard is not tripped. Keep the tree clean throughout the run; commit actual evidence/dispositions only at appropriate reviewed boundaries. The source runner executes exactly one admitted family and checks strict outcomes, immutable governed bytes and clean state. Do not bypass it with bare pytest.

```bash
PYTHONPATH=src "$NVDA_PROOF_PYTHON" tools/run_product_proof_gate.py --aggregate neutral_market_measurement_truth_native_source
```

```bash
PYTHONPATH=src "$NVDA_PROOF_PYTHON" tools/run_product_proof_gate.py --aggregate neutral_market_measurement_truth_native_d087
```

```bash
PYTHONPATH=src "$NVDA_PROOF_PYTHON" tools/run_product_proof_gate.py --aggregate neutral_market_measurement_truth_native_d131
```

```bash
PYTHONPATH=src "$NVDA_PROOF_PYTHON" tools/run_product_proof_gate.py --aggregate neutral_market_measurement_truth_native_d134
```

```bash
PYTHONPATH=src "$NVDA_PROOF_PYTHON" tools/run_product_proof_gate.py --aggregate neutral_market_measurement_truth_native_d135
```

```bash
PYTHONPATH=src "$NVDA_PROOF_PYTHON" tools/run_product_proof_gate.py --aggregate neutral_market_measurement_truth_native_d136
```

```bash
PYTHONPATH=src "$NVDA_PROOF_PYTHON" tools/run_product_proof_gate.py --aggregate neutral_market_measurement_truth_native_d138
```

```bash
PYTHONPATH=src "$NVDA_PROOF_PYTHON" tools/run_product_proof_gate.py --aggregate neutral_market_measurement_truth_native_d139
```

```bash
PYTHONPATH=src "$NVDA_PROOF_PYTHON" tools/run_product_proof_gate.py --aggregate neutral_market_measurement_truth_native_d140
```

```bash
PYTHONPATH=src "$NVDA_PROOF_PYTHON" tools/run_product_proof_gate.py --aggregate neutral_market_measurement_truth_native_d143
```

```bash
PYTHONPATH=src "$NVDA_PROOF_PYTHON" tools/run_product_proof_gate.py --aggregate neutral_market_measurement_truth_native_d137
```

## Shared invalidation and unresolved audit points

- L03 public DTO adapter changed dict-only traversal to Mapping; L04 introduced full typed-tree readback comparison for M00 native mapping snapshots. SOURCE current generation0003 and D0870002 bind the final support bytes; later native claims bind the same support. Earlier generations remain immutable. All current claims are unexecuted, so no previous native GREEN exists to reuse. Any subsequent support change requires affected-claim assessment/new immutable generation before warranted proof.
- L10 changed shared source completeness qualification from final row-count floor to completion of the exact known-empty warm-up prefix, retained through lawful deletion and cleared on control invalidation. Review SOURCE plus D131/D134/D135/D136/D138/D139/D140/D143 and applicable predecessors; quote no-book warm-up is a distinct path. No consumer may be accepted solely because another owner's proof passed.
- L08 added only the admitted slope profile and existing public D011 RawInputLineageV1 codec type; L09/L10 add closed rate profiles. Shared source/profile/codec changes require exact affected-claim review, not a blanket E2E suite. D138 uses actual public D011 and D131 actual native D087; D136 uses two actual public native readers.
- D137 reuses L03's assembly helper without D087 output. A repair to _native_option._assemble affects D087,D137 and D131's required D087; reassess their proof status. Do not silently replace asynchronous membership with a fused raw occurrence.
- L03/L04 record an open documentary ordering point: literal A2 oracle members are listed chronologicalSEQ11/12/13/14, while the public API explicitly requires role order R033/R034/R035/R036=SEQ12/11/13/14. Candidate tests assert role→identity mapping and API role order. Independently establish that the oracle list is membership rather than an incompatible ordering rule; if genuinely conflicting, stop the affected proof and resolve authority rather than rewriting frozen bytes to obtain green.
- L02 changed shared RecordState by opt-in encode/identity_field with original canonical/derived_occurrence_id defaults. Source-side assessment is that old owner requests/namespaces/serialisation remain unchanged; independent reviewer must establish the actual default-path proposition. No old test/authority/generation changed. Reuse old evidence only after assessing this and additive api.py/proof-loader changes; rerun retained old claims only on precise material invalidation, with recorded reason. No broad old regression is authorised by convenience.
- Original M00 implementation, native outputs/fixtures and SQLite compatibility remain unchanged against baseline; reuse that exact old evidence only. PostgreSQL separate codec/runtime remains deferred; no parity claim. Live IBKR/entitlements, M01 activation, A00 composition and catalogue-wide readiness remain excluded.

## Evidence, repair and disposition requirements

For each command preserve candidate full SHA/tree, command/env, claim/current generation/source bytes, raw stdout/stderr hash, collected/passed/skipped/xfailed/xpassed counts, exit code and independent semantic judgement. A preflight/collection failure is a failed obligation; null counts are not zeros or passes. The prepared JSON index intentionally contains null observed counts and NOT_RUN. Store raw logs outside the worktree during strict execution, then commit the actual evidence/index without altering originals.

At first failed invariant stop downstream dependent proofs. Record observed failure separately from diagnosis, inspect prior return/repair lineage, classify isolated/recurrent mechanism and return one bounded obligation to implementation. A repair must be material, scoped, committed and delivered as a new verified cumulative additive from the unchanged baseline. Preserve earlier outputs/generations; only rerun the unsuccessful proof after its documented repair and successful claims materially invalidated by that repair. Do not weaken, rename, skip or delete valid tests/claims. The independent tester remains sole executor through the repair cycle.

Independently review L00/L01 source/authority readiness and L13 disposition; D145 has no product test and remains paused. For every L02–L12 assign TESTED_ACCEPTED, RETURNED_FOR_REPAIR, BLOCKED or NOT_ATTEMPTED with exact evidence. Reconcile I01–I08, old/new profiles, M00 immutable evidence, backend limits and all holds in final coverage. G2/G3/G4 acceptance and final COMPLETED require every mandatory L14 obligation and the final reviewed cumulative additive transfer. A partial outcome must stay partial.

## Current leaf and coverage ledger

| Item | Implementation-thread handoff status | Independent result |
| --- | --- | --- |
| L00 | Original independently reviewed documentary baseline retained | New L14 source/authority audit pending |
| L01 | AUTHORITY_READY / NOT_RUN, commissioned immutable source/profile/oracle/allocation | Pending |
| L02–L12 | IMPLEMENTED_UNTESTED, all eleven current native claims authored | NOT_RUN; all observed counts unknown |
| L13 | DOCUMENTARY_DISPOSITION, D145 capability BLOCKED/PAUSED | Documentary review pending |
| L14/G5 | Handoff prepared only | NOT_ATTEMPTED; manual receiver intake/environment/semantic/static/product proof pending |
| I01 native sides | Versioned source/book consumers authored | Pending SOURCE/book owner proofs |
| I02 receipt/time | Native carriers/separate clock selection authored | Pending scoped readback/eligibility proofs |
| I03 controls | Public observation discovery and replay invalidation authored | Pending helper/consumer proofs |
| I04 subscribed positions | D143 shared-side replay and full MPID grouping authored | Pending intermediate-state proof |
| I05 async quotes | D087/D137 new assembly profile, stock atomic path retained | Pending exact scope/refusal/readback proofs |
| I06 D145 | Exact event-clock conflict and resumption proposal recorded | BLOCKED capability; documentary review pending |
| I07 SQLite/PostgreSQL | Prior unchanged M00 SQLite evidence retained; native M02 readback authored | New native readback pending; PostgreSQL excluded |
| I08 proof control | Fixed11 sibling extension/current generations authored | Pending ingress/schema/strict loader/static checks |

## Final transfer after L14

Commit actual reviewed evidence/dispositions and any repaired code. Keep the fixed baseline and all original refs/history. Generate one cumulative post-baseline additive containing HEAD/current branch and every relevant new/updated ref, fresh-restore original baseline+latest additive, compare HEAD/tree/ref/blob inventory, ancestry and fsck, compute/report bundle SHA256 and save/expose it. Include an in-Git next-export manifest; report actual final HEAD/checksum externally. No GitHub/Codex or full-history-per-leaf fallback. Packaging is transfer integrity, never a substitute for the eleven owning proofs and independent acceptance.
