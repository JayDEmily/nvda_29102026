# Serial runtime parallel risk packet boundary alignment report — 2026-04-22

## Known true before execution

- The first deliberate DMP boundary remains `serial runtime -> packet carriage`.
- Serial runtime already emitted ordered stage packets, but parallel risk still bootstrapped from `StageInputBundle` rather than the admitted serial-runtime boundary packet product.
- For this tranche, the admitted selected ingress subset is temporal only.
- Parallel risk had to consume the selected temporal stage packet, derive both downstream packet ids internally from `receipt["stage_packets"]["temporal"]["id"]`, and fail closed with `serial_runtime_temporal_packet_id_contract_mismatch` if that seed did not match the required prefix.

## Baseline

- Baseline branch: `work/serial-runtime-parallel-risk-packet-boundary-alignment-20260422` started from accepted baseline HEAD `fdcbffae586b0ebf76bb16e6d88ce82b277079fb`.
- Baseline tag present before execution: `module-8-historical-receipt-normalisation-exactness-authoritative-closeout-20260422`.
- Active work branch: `work/serial-runtime-parallel-risk-packet-boundary-alignment-20260422`.

## Brief defect and authorised correction

A real brief defect was encountered during execution: the brief both required retention of in-repo specimen artefacts and simultaneously treated any file outside the original execution list as disallowed.

Authorised tranche-specific correction applied:

- retain only `var/audit/specimens/serial_runtime_parallel_risk_boundary/serial_runtime_receipt.json`
- retain only `var/audit/specimens/serial_runtime_parallel_risk_boundary/selected_stage_packets.json`
- retain only `var/audit/specimens/serial_runtime_parallel_risk_boundary/bootstrap_input_packet.json`
- retain only `var/audit/specimens/serial_runtime_parallel_risk_boundary/parallel_risk_lane_output_packet.json`
- retain only `var/audit/specimens/serial_runtime_parallel_risk_boundary/parallel_risk_observation_record.json`
- retain only `var/audit/specimens/serial_runtime_parallel_risk_boundary/specimen_receipt.md`

No other specimen directory was widened or touched.

## What changed

### Code and proof surfaces changed

1. `src/nvda_desk/contracts/parallel_risk.py`
2. `src/nvda_desk/risk/parallel/evaluate.py`
3. `src/nvda_desk/services/parallel_risk_lane_service.py`
4. `src/nvda_desk/testing/harnesses/__init__.py`
5. `src/nvda_desk/testing/harnesses/serial_runtime_parallel_risk_boundary_specimen.py`
6. `tests/tier_a/parallel_risk/test_parallel_risk_lane_service_surface.py`
7. `tests/tier_a/persistence/test_parallel_risk_observation_store_surface.py`
8. `tests/tier_a/testing_harnesses/test_serial_runtime_parallel_risk_boundary_specimen_surface.py`
9. `var/audit/ledgers/serial_runtime_parallel_risk_packet_boundary_alignment_ledger.json`
10. `var/audit/reports/2026-04-22_serial_runtime_parallel_risk_packet_boundary_alignment_closeout.md`
11. The six authorised specimen artefacts under `var/audit/specimens/serial_runtime_parallel_risk_boundary/`

### Boundary shift made

- `ParallelRiskLaneService.run_from_serial_runtime(...)` now accepts the serial-runtime receipt, selects the temporal stage packet only, validates that the selected packet id starts with `dmp::serial::temporal::`, derives `time_token` from the remainder, emits bootstrap packet id `dmp::parallel_risk::bootstrap_input::{time_token}`, emits lane packet id `dmp::parallel_risk::output::{time_token}`, and fails closed with `serial_runtime_temporal_packet_id_contract_mismatch` if the prefix contract is broken.
- The bootstrap adapter now translates the selected serial-runtime temporal stage packet into the existing bounded bootstrap payload shape rather than reopening the earlier typed seam.
- The bootstrap payload now records `bootstrap_source = "serial_runtime.stage_packets.temporal"` and truthful stage-read state: temporal admitted for live semantic read; non-temporal serial packets present in the boundary product but not admitted for live semantic read in this tranche.
- The specimen harness now proves the admitted boundary path and writes exactly six retained artefacts under `var/audit/specimens/serial_runtime_parallel_risk_boundary/`.

## Proof

### Targeted test proof

Command:
`PYTHONPATH=src pytest -q tests/tier_a/runtime/test_serial_stage_packet_emission_surface.py`

Output:
```text
.                                                                        [100%]
1 passed in 0.22s
```

Command:
`PYTHONPATH=src pytest -q tests/tier_a/parallel_risk/test_parallel_risk_lane_service_surface.py`

Output:
```text
..                                                                       [100%]
2 passed in 0.26s
```

Command:
`PYTHONPATH=src pytest -q tests/tier_a/persistence/test_parallel_risk_observation_store_surface.py`

Output:
```text
..                                                                       [100%]
2 passed in 0.23s
```

Command:
`PYTHONPATH=src pytest -q tests/tier_a/testing_harnesses/test_serial_runtime_parallel_risk_boundary_specimen_surface.py`

Output:
```text
..                                                                       [100%]
2 passed in 0.45s
```

### Compile proof

Command:
`python -m compileall src`

Output excerpt:
```text
Listing 'src'...
Listing 'src/nvda_desk'...
Listing 'src/nvda_desk/testing'...
Listing 'src/nvda_desk/testing/harnesses'...
Listing 'src/scripts'...
```

### Deterministic specimen proof

Retained specimen receipt:

- selected temporal stage packet: `dmp::serial::temporal::20260421T093100Z`
- bootstrap input packet: `dmp::parallel_risk::bootstrap_input::20260421T093100Z`
- parallel risk lane packet: `dmp::parallel_risk::output::20260421T093100Z`
- selected stage packets contains exactly `temporal`
- bootstrap lineage depends only on the selected temporal packet
- lane lineage depends only on the bootstrap packet

## Deferred by design

- upstream DMP expansion above the serial-runtime boundary
- Stage B parallel-risk expansion
- Stage C parallel-risk expansion
- final-risk join work
- capital-deployment work
- trade-placement work
- blueprint workbook redesign or cleanup beyond the authorised retained specimen artefacts
- any widening of selected ingress beyond temporal in this tranche

## Closeout identifiers

- Branch: `work/serial-runtime-parallel-risk-packet-boundary-alignment-20260422`
- Head commit: `Exact final tagged commit hash is captured in git closeout evidence and the execution response; embedding a self-referential final commit hash inside the same committed files would change the commit id.`
- Annotated tag: `serial-runtime-parallel-risk-packet-boundary-alignment-authoritative-closeout-20260422`
- Branch remains unmerged.
