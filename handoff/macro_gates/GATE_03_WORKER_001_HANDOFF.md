# G03 Worker 001 Handoff — VI-08 Architecture Admission

## Status

`HANDOFF_SPEC_READY / PACKET_REBUILD_REQUIRED`

## Bounded objective

Execute VI-08 only: apply the accepted VI-07 minimal architecture-admission design to the supplied skeletal repository. Do not implement Raw Signal product behaviour.

## Exact source lineage

- genuine pre-implementation predecessor: `d095954c16a9818eadb60d6364148229f2dc4558`
- predecessor tree: `7fdb0e5308f3af187134bc3ebf633835748e9475`
- PM handoff commit: `7795705727d8ac2935949ba9e4acce672fa463a1`
- PM handoff tree: `f34d17bfda83e52f58dfe72760e4f286e083355c`
- supplied worker repository visible commit count: `1`

The handoff commit contains PM planning/authority/handoff material only. It contains no VI-08 product/architecture mutation.

## Worker packet specification

The previously prepared packet `NVDA_G03_WORKER_001_VI08_PACKET_20260919.tar.gz` is **SUPERSEDED** because it embedded a local wheelhouse. Do not dispatch or rely on that packet.

The replacement packet, when prepared, must contain:

- native shallow Git repository at the exact PM handoff commit;
- skeletal architecture source/config/tests;
- exact accepted BICP JSON/Markdown;
- exact accepted IRB;
- fixed VI-05 IWO JSON/Markdown;
- VI-04 authority closure;
- PM-derived VI-07 architecture-admission design;
- bounded Worker 001 brief and provenance/hash manifest.

It must **not** contain wheelhouses, package archives, virtual environments, or dependency payloads. Dependency artefacts are available separately as Project attachments; the Worker is told where that dependency source exists and owns environment setup/use.

It deliberately does not contain the full implementation/admission Git history or unrelated NVIDIA corpus.

## Baseline evidence inherited from the superseded packet preparation

The following evidence was recorded during the earlier packet preparation:

- implementation-authority ingress: `PASS`, resolving `create:raw_signal_occurrence_truth->M00, modify:A00`;
- structural architecture validation: `PASS`;
- architecture/bootstrap tests: `74/74 PASS`;
- architecture promotion gate: `PASS`;
- mypy: `PASS`;
- ruff: `PASS`.

Do not treat the old archive readback as evidence for the replacement packet. The replacement packet requires its own transport/hash readback when it is actually built. These checks establish baseline state only; they do not establish VI-08 completion.

## Excluded PM execution

PM inline commits after `d095954...` that performed VI-08/VI-09/VI-10 work are `DO_NOT_CARRY_FORWARD`. They remain recoverable in PM Git history but are not ancestors of Worker 001 and must not be used as implementation authority or candidate output.

## Return route

Worker 001 returns exact commit/tree, changed paths, commands/results and blockers/concerns. The PM then constructs the applicable independent review/test handoff from that exact returned candidate.
