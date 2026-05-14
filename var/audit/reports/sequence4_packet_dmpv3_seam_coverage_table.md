# Sequence 4 packet/DMPV3 seam coverage table

| Check | Expected | Observed | Result |
|---|---:|---:|---|
| Atlas surface slices accounted | 18 | 18 | PASS |
| Sequence 1 records accounted upstream | 1,716 | 1716 | PASS |
| DMPV3 packet-carriage records assigned | 73 | 73 | PASS |
| Sequence 1 `requires packet/DMP seam work first` records assigned | 45 | 45 | PASS |
| Sequence 3 `future_packet_specimen_required_in_sequence4` records assigned | 45 | 45 | PASS |
| Duplicate relevant record assignments | 0 | 0 | PASS |
| Unassigned relevant records | 0 | 0 | PASS |
| Runtime source/test/normative/vocabulary/generated-slice mutations | 0 | 0 | PASS |
| Sequence 5 opened | 0 | 0 | PASS |

## Sequence 1 classification coverage within Sequence 4 record universe

| Sequence 1 classification | Count |
|---|---:|
| partially migrated | 28 |
| requires packet/DMP seam work first | 45 |

## Sequence 4 disposition coverage

| Sequence 4 disposition | Count |
|---|---:|
| existing_thin_dmpv3_seam_surface_recorded_future_proof_alignment_required | 28 |
| explicitly_deferred_packet_dmpv3_seam_specimen_or_contract_gate_required | 45 |

## Directory read-set status

| Directory | Status | Files read |
|---|---|---:|
| src/nvda_desk/contracts | present | 21 |
| src/nvda_desk/packets | present | 2 |
| src/nvda_desk/schemas | present | 4 |
| tests/tier_a/packets | present | 2 |
| var/audit/specimens/serial_runtime_parallel_risk_boundary | present | 6 |
| var/audit/specimens/module_8 | present | 5 |
