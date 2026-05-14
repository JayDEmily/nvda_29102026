# Bounded intake control repair receipt — post-row044 linkage-gap reconciliation 002

## Scope

This receipt records creation of a bounded evidence packet for the current residual linkage-gap IDs only. It is not reconciliation proof and not target closure proof.

## Created artefacts

- `var/audit/active_code_atlas_001/bounded_reconciliation_intake_001/tools/extract_bounded_reconciliation_packet.py`
- `var/audit/active_code_atlas_001/bounded_reconciliation_intake_001/packet/ACTIVE_CODE_ATLAS_PRIMARY_LINKAGE_GAP_RECONCILIATION_002_BOUNDED_EVIDENCE_PACKET.json`
- `var/audit/active_code_atlas_001/bounded_reconciliation_intake_001/reports/ACTIVE_CODE_ATLAS_PRIMARY_LINKAGE_GAP_RECONCILIATION_002_BOUNDED_EVIDENCE_PACKET_REPORT.json`
- `var/audit/active_code_atlas_001/bounded_reconciliation_intake_001/reports/extract_bounded_reconciliation_packet.stdout.json`
- `var/audit/active_code_atlas_001/bounded_reconciliation_intake_001/reports/extract_bounded_reconciliation_packet.status`
- `var/audit/active_code_atlas_001/bounded_reconciliation_intake_001/ACTIVE_CODE_ATLAS_PRIMARY_LINKAGE_GAP_RECONCILIATION_002_BOUNDED_INTAKE_CONTROL_ARTEFACT.md`

## Admitted residual IDs

Queue rows: `ACATQ-0044`, `ACATQ-0045`, `ACATQ-0046`

Comparison groups: `ACABC-0035`, `ACABC-0045`, `ACABC-0046`, `ACABC-0047`, `ACABC-0048`

## Direct reference boundary

Direct referenced Atlas records admitted from selected comparison records:

- `atlas_donor_service_downstream_live_inventory_001`
- `atlas_donor_service_downstream_live_inventory_002`
- `atlas_donor_vocabulary_001`
- `atlas_donor_vocabulary_002`
- `atlas_donor_vocabulary_003`
- `atlas_donor_vocabulary_004`
- `atlas_donor_vocabulary_005`
- `atlas_donor_vocabulary_006`
- `atlas_donor_vocabulary_007`
- `atlas_donor_vocabulary_008`
- `atlas_donor_vocabulary_009`
- `atlas_donor_vocabulary_010`

Direct referenced Bridge satisfaction records admitted from selected join records:

- `NIS-0101`
- `NIS-0102`
- `NIS-0103`
- `NIS-0104`
- `NIS-0105`
- `NIS-0106`
- `NIS-0107`
- `NIS-0108`
- `NIS-0109`
- `NIS-0110`
- `NIS-0951`
- `NIS-0952`

## Packet metadata

- Path: `var/audit/active_code_atlas_001/bounded_reconciliation_intake_001/packet/ACTIVE_CODE_ATLAS_PRIMARY_LINKAGE_GAP_RECONCILIATION_002_BOUNDED_EVIDENCE_PACKET.json`
- SHA256: `75b573372ef737ee8249b913b7e93922cdf14fc163e49cf118d36013b04c2844`
- Byte count: 190098
- Line count: 4730

## Extraction result

- Extractor status file: `var/audit/active_code_atlas_001/bounded_reconciliation_intake_001/reports/extract_bounded_reconciliation_packet.status` = `0`
- Extraction report validation status: `PASS`
- Unrelated ID errors: `[]`

## Non-closure declaration

This repair only makes the next material-file intake honest and bounded. The reconciliation target remains open. Any future reconciliation mutation must first read the bounded packet in full and validate the regenerated manifest.

## Proof commands

The final proof-command results are recorded in the closeout response for this worker pass.
