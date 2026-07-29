# Parallel Workflow Control V1 — PM Self-audit Rejection

## Disposition

`REJECTED_BEFORE_WORKER_LAUNCH:PARALLEL_WORKFLOW_ENABLEMENT_V1`

The structural checkpoint at commit `9e404df7c13f7cca170e05e4c9f76b8ec4548ffa` is mechanically intact but is not launch-authorised. No lane worker or tester was launched from it.

## Defects requiring repair

1. durable parallel-control terms were used before M15 vocabulary admission;
2. global full-read-manifest law conflicted with lane write sets;
3. Lane 1A omitted the applicable `tests/AGENTS.override.md` route;
4. worker/tester return names and the tester portability contract were underspecified;
5. the authoring PM had not obtained independent control validation;
6. the registry lacked revision, commit, artefact, queue and integration lineage fields;
7. the cumulative global manifest was incorrectly treated as current-target lane evidence;
8. the claim of worker informational isolation was broader than the actual brief route because workers were required to read the global registry.

## Preserved facts

The four selected dependency-independent roots, exact `Lane 1AW/1AT` through `Lane 4AW/4AT` names, held Lanes 5–6, pairwise disjoint module-local write sets and serial PM integration remain valid design decisions.
