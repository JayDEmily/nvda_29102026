# Parallel Control Repair 2 PM Record

## Trigger

Parallel Control T1 correctly returned `HARD_BLOCK` at tester commit `44bede21b1d90ec8cdfac386baed7d2ee247eddb` because the Repair 1 tester brief required a project-folder rollout-plan attachment whose exact filename and SHA-256 were not available.

## Adjudication

The block is a Project Manager control-package defect, not a tester defect. The available project-folder planning document is:

- filename: `NVDA Parallel Workflow — Project-Specific Architecture and Rollout….md`
- SHA-256: `e6290bd0a10afe5a1f0e0029464603ae4af11bc850bec3462367a6753ce61f16`

The hard-block evidence is preserved unchanged. Repair 2 creates a new retest brief rather than rewriting the historical Repair 1 brief.

## Authorised repair

- preserve the tester hard-block commit and evidence;
- create `PARALLEL_CYCLE_01_CONTROL_REPAIR_2/PARALLEL_CONTROL_T1_RETEST_BRIEF.md`;
- bind the retest to the exact available rollout-plan filename and SHA-256;
- update live PM control pointers from Repair 1 awaiting test to Repair 2 awaiting retest;
- keep all worker lanes blocked pending independent retest PASS and separate PM acceptance.

## Prohibitions retained

No production source, physical tests, runtime configuration, proof registry, lane assignment output or worker-launch authority is changed by this repair.
