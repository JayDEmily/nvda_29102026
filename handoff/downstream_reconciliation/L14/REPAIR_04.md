# L14 bounded repair 04 — clean D137 first-admission lineage

Status: **RETURNED_FOR_REPAIR recovery candidate; independent strict verification pending**. This is ordinary-history recovery, not an amendment of the malformed immutable generation or proof control.

## Observed failure and recurrence

At `5ca757c256d764bd4848dc8f9c80f433a9c2863d`, the sole independent executor's first SOURCE strict invocation failed before collection with `missing required properties: ['previous_generation']`, exit1. Counts remain null; no collected/passed count is inferred. Its all-sibling loader encountered D137's original generation0001, first admitted at `81e86b5e70138558526dbe335657919f5cf5b4cf`, lacking the mandatory explicit `previous_generation:null`. Generation0002 linked that malformed immutable record. This is proof-admission preflight failure, not observed D137 calculation failure. All ten downstream strict claims remained NOT_ATTEMPTED.

The independent reviewer classified **RECURRENT_CLASS immutable-admission lineage**, after reading the same mechanism and lawful recovery in `handoff/foundation_implementation/d131_execution/strict-failure-analysis.md`. The documentary audit examined25 native admission snapshots and identified only the original D137 first admission with this missing property. Original return, audit, all actual5ca command outputs/metadata and stdout/stderr are preserved under `evidence/return_04/`. Failed SOURCE raw output SHA256 is `10eaecb9cd49205c890b331ee122832adf0925c0f193cdf94ab4a41f9538a871`.

## Root-authorised ordinary-history recovery

Root approved the concrete two-commit recovery before branch creation. No existing ref was reset, force-updated, merged with invalid ancestry, rewritten or pruned.

1. Preserve `refs/heads/work/reconciliation-oct29` at `5ca757c256d764bd4848dc8f9c80f433a9c2863d`, retaining the malformed generation, every rejected candidate/repair and its complete history. Preserve `refs/heads/work/reconciliation-resumed` at `2efb2f6031d7d86f79d1a8dbd56b466f9d4facc0`. All original baseline refs remain prerequisites.
2. Create `refs/heads/work/reconciliation-l14-recovered` from `7f7a6311230a42b91398b70841dd6129989421e7`, immediately before D137's first admission. Ordinary commit `89adfdd0414c8df1047a3f260a5330defbeace60` restores the original L12 payload and establishes D137 generation0001 with mandatory explicit null and matching first pointer from the outset. Original L12 production/test/proof/authority bytes are retained; only the new initial generation record/pointer differ. Lawful generation0001 SHA256 is `f1a0ec6b8ce248ae40c13ef31ab18fc6b088a8a781b2d42e2af230b975a0f29a`.
3. In the second ordinary commit, carry forward the reviewed final5ca tree, preserving the lawful generation0001. Carry forward the reviewed D137 generation0002 fields/family/support hashes, linking instead to this branch's lawful generation0001; update its matching pointer/current claim index. Corrected generation0002 SHA256 is `e772751269c05a5b4682d07c0d049b305ad3d1202a5fc7919bd8359836d6bdd0`. All other immutable generations are carried byte-identically. The final recovery commit/HEAD is reported by the external checkpoint receipt.

The malformed D137 lineage is **DO_NOT_CARRY_FORWARD** to the new active branch. Its exact bytes and the branch containing them remain recoverable unchanged. The new lawful generation records are first introduced on this branch, rather than editing a previously admitted immutable record on that lineage. Schema, runner, generic historical validation, claims, contract, two physical cases and acceptance meaning remain unchanged. No pointer-only fix, nullification of an old pointer or omission of required retained generations is used.

## Byte equivalence and evidence reuse boundary

`REPAIR_04_BLOB_EQUIVALENCE.json` records a Git-object comparison between the reviewed5ca tree and staged recovery tree (excluding only that inventory's own later addition). Every production, test, tool, implementation-authority, frozen downstream authority and owning proof-contract blob must match exactly. Every generation outside the narrowly recovered D137 directory must match exactly. Intentional differences are confined to the recovered D137 admission metadata, its current documentary index, this recovery record/ledger and preserved execution evidence.

The independent executor already obtained **Ruff28-file PASS, mypy16-file PASS and eleven exact authority-ingress PASS** at5ca. The unchanged source/test/tool/authority/proof bytes support reuse subject to its independent judgement. A new branch/HEAD alone does not justify duplicate green checks. Only the unsuccessful SOURCE strict invocation is eligible for retry after this material admission repair; the other ten native aggregates remain first executions. No product result or final acceptance is implied by byte equivalence.

No implementation-worker executable checks ran. Git readback/hash/inventory operations establish transfer/source identity only. Root must export the cumulative additive from unchanged fixed baseline `97f944d51ab9e403250fe76910e2754b50425c73`, including the new recovered branch, retained failed oct29 branch and resumed branch, fresh-verify original refs/history plus every exported ref/tree, then save/expose before the sole independent executor continues. D145 and unrelated holds remain paused.
