# Handover — Foundation Readiness Unit 3

## Checkpoint

- Branch: `work/foundation-readiness-reconciliation-v1`
- Accepted base: `3876f17108b5c2e42510dff66e7248d622c10e47`
- Unit 1 commit: `1d48393`
- Unit 2 commit: `a7136bf`
- Current state: Unit 3 C-NORM aligned; C-PROOF intentionally red; no Unit 3 production implementation has begun.
- Environment: repository `.venv`, CPython 3.13.5, built from the supplied locked runtime and development wheelhouses.

## What is present

`UNIT3_C_NORM.md` defines the bounded typed-ingress change. The two modified Tier A files establish three current-law cases: reject mapping payloads at the M01 request seam, translate JSON through the registered M01 payload contract, and make M00 delegate transport translation to M01. Control pointers already identify Unit 3 as active.

## Current proof result

Command:

```bash
.venv/bin/python -m pytest -q \
  tests/tier_a/ingress/test_m01_source_admission_contract.py \
  tests/tier_a/m00_application_shell/test_m00_upstream_workflow_contract.py \
  -k unit3
```

Observed: `3 failed, 25 deselected`. All three fail at the same intended boundary: production `SourceAdmissionRequest.typed_payload` still requires a dictionary and rejects the concrete `MarketSnapshotPayload`. This is expected-red evidence, not an accepted or green Unit 3 result.

## Resume

Continue the active ExecPlan at Unit 3. Implement only the admitted M01 typed request/registered transport-translation seam and M00 delegation described in `UNIT3_C_NORM.md`; keep legacy compatibility loaders unselected. Then run the targeted proof, the affected M01/M00/entry cones, required proof/vocabulary controls, and complete physical Tier A before recording or committing Unit 3 acceptance.
