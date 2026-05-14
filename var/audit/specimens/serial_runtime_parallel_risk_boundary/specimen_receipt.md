# serial-runtime-to-parallel-risk boundary specimen receipt

## boundary classification

This specimen proves the admitted serial runtime boundary packet set only.

## admitted path

- serial runtime boundary packet set: `receipt["stage_packets"]`
- selected temporal stage packet: `dmp::serial::temporal::20260421T093100Z`
- bootstrap input packet: `dmp::parallel_risk::bootstrap_input::20260421T093100Z`
- parallel risk lane packet: `dmp::parallel_risk::output::20260421T093100Z`

## packet-id derivation

- selected temporal stage packet id seed: `dmp::serial::temporal::20260421T093100Z`
- bootstrap input packet id: `dmp::parallel_risk::bootstrap_input::20260421T093100Z`
- parallel risk lane packet id: `dmp::parallel_risk::output::20260421T093100Z`

## deterministic artefacts written

- serial runtime receipt JSON: `var/audit/specimens/serial_runtime_parallel_risk_boundary/serial_runtime_receipt.json`
- selected stage packets JSON: `var/audit/specimens/serial_runtime_parallel_risk_boundary/selected_stage_packets.json`
- bootstrap input packet JSON: `var/audit/specimens/serial_runtime_parallel_risk_boundary/bootstrap_input_packet.json`
- parallel risk lane packet JSON: `var/audit/specimens/serial_runtime_parallel_risk_boundary/parallel_risk_lane_output_packet.json`
- parallel risk observation record JSON: `var/audit/specimens/serial_runtime_parallel_risk_boundary/parallel_risk_observation_record.json`
- specimen receipt Markdown: `var/audit/specimens/serial_runtime_parallel_risk_boundary/specimen_receipt.md`

## bounded proof notes

- selected stage packets contains exactly `temporal`
- bootstrap input packet lineage depends only on the selected temporal stage packet
- parallel risk lane packet lineage depends only on the bootstrap input packet
- only the selected temporal stage packet is admitted for live Module 8 semantic read in this tranche
