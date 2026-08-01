# Acceptance Unit B — Validation Summary

## Outcome

**PASS** — canonical M05 and M06 outputs now cross into M09 only through validated DMPV3 envelopes. M09 preserves exact execution, prepared-context and packet-carriage lineage through capital decision and receipt surfaces. The old runtime orchestrator and bootstrap evaluator are explicitly noncanonical.

## Known true

- Expected-red seam proof commit: `b92baa7`.
- M04/M05/M06 egress implementation commit: `c464738`.
- Canonical M09 packet-ingress implementation commit: `9b40275`.
- Lineage hardening and legacy quarantine commit: `c2c8051`.
- Vocabulary governance closeout commit: `6868b07`.
- Focused M04–M12 route: **463 passed / 0 failed**.
- M09 canonical seam proof: **42 passed / 0 failed**.
- M10 downstream proof: **28 passed / 0 failed**.
- M11 downstream proof: **23 passed / 0 failed**.
- M12 downstream proof: **22 passed / 0 failed**.
- Tier B: **49 passed / 0 failed**.
- Proof manifests: **64 / 64 valid**.
- Touched namespaces M04/M05/M06/M09: **0 unresolved candidates** with current stamps.
- Complete Tier A comparison: **1,628 passed / 253 failed** at baseline versus **1,648 / 250** after repair; 17 added tests, three resolved C-026 nodes and **zero new failures**.
- Static compilation and Git diff check pass.

## Implemented surfaces

- M04-owned `DmpV3ExecutionContext`, prepared-context identity and deterministic carriage fingerprint.
- M05 `SerialCandidatePacketAdapter` using caller-owned execution and packet context.
- M06 `ParallelRiskPacketAdapter` using the same caller-owned execution context.
- Canonical packet-only M09 `join_final_risk` validation boundary.
- Private compatibility join that cannot authorise capital.
- Capital decision and receipt lineage for M05/M06 packet IDs and fingerprints, trace/run/scenario and prepared-context identity.
- Explicit noncanonical markers for the old `DeskRuntimeOrchestrator` and legacy parallel bootstrap evaluator.

## Behaviour proved

- Placeholder or generated execution identities are rejected.
- Raw/unpacketised M05 and M06 products cannot enter canonical M09 authority.
- Role, producer, K07 status, execution context, prepared parent and payload lineage are validated before capital logic.
- Cross-run and prepared-parent mismatch fail closed.
- Carriage fingerprinting ignores occurrence-only identity while binding material semantics.
- M05/M06 packet adapters reject wrong payload state or parent context.
- Packet lineage survives through capital decision and receipt.
- The compatibility domain join cannot authorise capital.
- The legacy orchestrator/bootstrap route is not canonical.

## Ruled out

- rollback or history rewrite;
- DMPV3 at raw M01/calendar ingestion;
- packet identity invented by M05 or M06;
- direct-object canonical M09 ingress;
- admission of `parallel_risk_bootstrap_input` merely to satisfy legacy tests;
- semantic rewrites of M10–M12 policy;
- promotion of the legacy runtime specimen.

## Open limitations

- The repository still has 250 unchanged Tier A baseline failures outside this repair.
- Three long-standing vocabulary-term/schema tests remain part of that unchanged set.
- Ruff and Black are unavailable in the execution environment.
- No live broker, live provider, durable temporal store or production-readiness claim follows.

## Next gate

M00 final composition. It has not started in this checkpoint.
